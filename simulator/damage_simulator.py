from simulator.weapon import Weapon
from simulator.attack_simulator import AttackSimulator
from simulator.stats_collector import StatsCollector
from simulator.legend_effect import LegendEffect
from simulator.config import Config
from copy import deepcopy
from collections import deque
import statistics
import math
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


class DamageSimulator:
    def __init__(self, weapon_chosen, config: Config, progress_callback=None):
        self.cfg = config
        self.stats = StatsCollector()   # Create object for collecting statistics
        self.weapon = Weapon(weapon_chosen, config=self.cfg)  # Pass Config instance to Weapon
        self.attack_sim = AttackSimulator(weapon_obj=self.weapon, config=self.cfg)
        self.legend_effect = LegendEffect(stats_obj=self.stats, weapon_obj=self.weapon, attack_sim=self.attack_sim)
        self.progress_callback = progress_callback

        self.dmg_type_names = []    # List of dmg type names, e.g., ['physical', 'acid']
        self.dmg_dict = {}    # Keys are dmg type names, Values are lists of damage dice, e.g., [[2, 6], [1, 8]]
        self.dmg_dict_legend = {}
        self.collect_damage_from_all_sources()

        # Convergence params, z-score lookup (normal distribution)
        z_values = {0.90: 1.645, 0.95: 1.96, 0.99: 2.576}
        self.confidence = 0.99
        self.z = z_values.get(self.confidence, 2.576)
        self.window_size = 15

        # Convergence tracking - crit allowed
        self.total_dmg = 0
        self.dps_window = deque(maxlen=self.window_size)
        self.dps_rolling_avg = []
        self.dps_per_round = []
        self.cumulative_damage_per_round = []

        # Convergence tracking - crit immune
        self.total_dmg_crit_imm = 0
        self.dps_crit_imm_window = deque(maxlen=self.window_size)
        self.dps_crit_imm_rolling_avg = []
        self.dps_crit_imm_per_round = []
        self.cumulative_damage_by_type = {}

    def collect_damage_from_all_sources(self):
        """Collect damage information from all sources and organize it into dictionaries"""
        damage_sources = self.weapon.aggregate_damage_sources()

        for src_name, dmg_source in damage_sources.items():
            if isinstance(dmg_source, dict):
                for key, val in dmg_source.items():
                    # Handling purple legendary damage specially
                    if key == 'legendary' and isinstance(val, dict):
                        # val is { 'proc': 0.05, 'fire': [1, 30], ... , 'effect': 'sunder' }
                        for leg_key, leg_val in val.items():
                            if leg_key in ('proc', 'effect'):
                                self.dmg_dict_legend[leg_key] = leg_val  # Store proc and effect directly
                                continue
                            # leg_val expected to be [dice, sides] or [dice, sides, flat]
                            dice = leg_val[0]
                            sides = leg_val[1]
                            flat = leg_val[2] if len(leg_val) > 2 else None
                            dmg_entry = [dice, sides] if flat is None else [dice, sides, flat]
                            self.dmg_dict_legend.setdefault(leg_key, []).append(dmg_entry)

                    # vs_race_* mapping where val is a dict {actual_type: [dice, sides]}
                    elif 'vs_race' in key and isinstance(val, dict):
                        if not self.cfg.DAMAGE_VS_RACE: # Check config DAMAGE_VS_RACE flag
                            continue                    # Ignore damage entry if flag off
                        actual_type, nums = next(iter(val.items()))
                        dice = nums[0]
                        sides = nums[1]
                        flat = nums[2] if len(nums) > 2 else None
                        dmg_entry = [dice, sides] if flat is None else [dice, sides, flat]
                        self.dmg_dict.setdefault(actual_type, []).append(dmg_entry)

                    # Regular damage entries, e.g., 'fire': [dice, sides] or 'physical': [dice, sides, flat]
                    else:
                        dice = val[0]
                        sides = val[1]
                        flat = val[2] if len(val) > 2 else None
                        dmg_entry = [dice, sides] if flat is None else [dice, sides, flat]
                        self.dmg_dict.setdefault(key, []).append(dmg_entry)

            # Handling additional damage entries that are lists of dicts, e.g., [{'fire_fw': [1, 4, 10]}, {'acid': [1, 6]}]
            elif isinstance(dmg_source, list):
                for item in dmg_source:
                    if isinstance(item, dict):
                        # Handling additional damage entries that are dicts, e.g., {'fire_fw': [1, 4, 10]}
                        dmg_type_key, dmg_nums = next(iter(item.items()))
                        dice = dmg_nums[0]
                        sides = dmg_nums[1]
                        flat = dmg_nums[2] if len(dmg_nums) > 2 else None
                        dmg_entry = [dice, sides] if flat is None else [dice, sides, flat]
                        self.dmg_dict.setdefault(dmg_type_key, []).append(dmg_entry)

                    else:
                        # Handling unexpected formats gracefully
                        print(f"Warning: Unexpected damage source format in list: {item}")
                        continue

            else:
                print(f"Warning: Unexpected damage source format: {dmg_source}")
                continue

    def convergence(self, round_num) -> bool:
        dps_window_mean = statistics.mean(self.dps_window)
        dps_window_stdev = statistics.stdev(self.dps_window)

        # STD check with 'dynamic_window' values
        relative_std = dps_window_stdev / dps_window_mean

        # Relative change check with 'dynamic_window' values
        relative_change = (max(self.dps_window) - min(self.dps_window)) / dps_window_mean

        # Convergence check
        if relative_std < self.cfg.STD_THRESHOLD and relative_change < self.cfg.CHANGE_THRESHOLD:
            print(f"Converged after {round_num} rounds ({self.confidence * 100}% CI).")
            return True

        else:
            return False

    def simulate_dps(self):
        self.stats.init_zeroes_lists(self.attack_sim.attacks_per_round)
        total_rounds = self.cfg.ROUNDS
        round_num = 0

        for round_num in range(1, total_rounds + 1):
            total_round_dmg = 0
            total_round_dmg_crit_imm = 0

            for attack_idx, attack_ab in enumerate(self.attack_sim.attack_prog):
                self.stats.attempts_made += 1
                self.stats.attempts_made_per_attack[attack_idx] += 1

                legend_ab_bonus = self.legend_effect.ab_bonus()  # Get the AB bonus from the legendary effect
                legend_ac_reduction = self.legend_effect.ac_reduction()  # Get the AC reduction from the legendary effect
                current_ab = min(attack_ab + legend_ab_bonus, self.attack_sim.ab_capped)
                outcome, roll = self.attack_sim.attack_roll(current_ab, defender_ac_modifier=legend_ac_reduction)

                if outcome == 'miss':  # Attack missed the opponent, no damage is added
                    continue

                else:  # Attack hits, critical hit logic is managed within this part:
                    self.stats.hits += 1
                    self.stats.hits_per_attack[attack_idx] += 1

                    # On Critical Hit damage is NOT multiplied(!), it is rolled multiple times!
                    crit_multiplier = 1 if outcome == 'hit' else self.weapon.crit_multiplier

                    legend_dmg_sums, legend_dmg_common, legend_imm_factors = (
                        self.legend_effect.get_legend_damage(self.dmg_dict_legend, crit_multiplier)
                    )

                    dmg_dict = deepcopy(self.dmg_dict)  # Prep dmg dict for CRIT calculation

                    dmg_sneak = dmg_dict.pop('sneak', [])                                                # Remove the 'sneak' dmg from crit multiplication
                    dmg_sneak_max = max(dmg_sneak, key=lambda sublist: sublist[0], default=None)         # Find the highest 'Sneak' dmg, can't stack sneak

                    dmg_death = dmg_dict.pop('death', [])                                           # Remove the 'sneak' dmg from crit multiplication
                    dmg_death_max = max(dmg_death, key=lambda sublist: sublist[0], default=None)    # Find the highest 'Sneak' dmg, can't stack sneak

                    def get_max_dmg(dmg_list):
                        dice = dmg_list[0]
                        sides = dmg_list[1]
                        flat = dmg_list[2] if len(dmg_list) > 2 else 0
                        return dice * sides + flat

                    dmg_massive = dmg_dict.pop('massive', [])                          # Remove the 'Massive' dmg from crit multiplication
                    dmg_massive_max = max(dmg_massive, key=get_max_dmg, default=None)  # Find the highest 'Massive' dmg, can't stack massive

                    dmg_flameweap = dmg_dict.pop('fire_fw', [])                            # Remove the 'Flame Weapon' dmg from crit multiplication
                    dmg_flameweap_max = max(dmg_flameweap, key=get_max_dmg, default=None)  # Find the highest 'Flame on Hit' dmg, can't stack multiple on-hits

                    if legend_dmg_common:   # Checking if list is NOT empty, then adding the legend common damage to ordinary damage dictionary
                        dmg_type_name = legend_dmg_common.pop(2)
                        dmg_popped = dmg_dict.pop(dmg_type_name, [])
                        dmg_popped.extend([legend_dmg_common])
                        dmg_dict[dmg_type_name] = dmg_popped

                    dmg_dict_crit_imm = deepcopy(dmg_dict)  # Make a deep copy of dmg dict for NON-CRIT calculation

                    if crit_multiplier > 1:     # Store an additional dictionary for damage without crit multiplication
                        self.stats.crit_hits += 1
                        self.stats.crits_per_attack[attack_idx] += 1
                        dmg_dict = {k: [i for i in v for _ in range(crit_multiplier)]
                                    for k, v in dmg_dict.items()}  # Copy dice information X times (X = crit multiplier)
                        if dmg_massive_max is not None:
                            dmg_dict['physical'].append(dmg_massive_max)  # Add 'Massive' again after dmg rolls have been multiplied

                    if dmg_sneak_max is not None:   # Add 'Sneak Attack' again after crit dmg rolls have been multiplied
                        dmg_dict.setdefault('physical', []).append(dmg_sneak_max)
                        dmg_dict_crit_imm.setdefault('physical', []).append(dmg_sneak_max)

                    if dmg_death_max is not None:   # Add 'Death Attack' again after crit dmg rolls have been multiplied
                        dmg_dict.setdefault('physical', []).append(dmg_death_max)
                        dmg_dict_crit_imm.setdefault('physical', []).append(dmg_death_max)

                    if dmg_flameweap_max is not None:   # Add 'Flame Weapon' again after crit dmg rolls have been multiplied
                        dmg_dict.setdefault('fire', []).append(dmg_flameweap_max)
                        dmg_dict_crit_imm.setdefault('fire', []).append(dmg_flameweap_max)

                    dmg_sums = self.get_damage_results(dmg_dict, legend_imm_factors)
                    dmg_sums_crit_imm = dmg_sums if crit_multiplier == 1 else self.get_damage_results(dmg_dict_crit_imm, legend_imm_factors)

                attack_dmg = sum(dmg_sums.values()) + sum(legend_dmg_sums.values())
                attack_dmg_crit_imm = sum(dmg_sums_crit_imm.values()) + sum(legend_dmg_sums.values())

                # Update cumulative damage by type for plotting/analysis
                for k, v in dmg_sums.items():
                    self.cumulative_damage_by_type[k] = self.cumulative_damage_by_type.get(k, 0) + v
                for k, v in legend_dmg_sums.items():
                    self.cumulative_damage_by_type[k] = self.cumulative_damage_by_type.get(k, 0) + v

                total_round_dmg += attack_dmg
                total_round_dmg_crit_imm += attack_dmg_crit_imm

            self.total_dmg += total_round_dmg
            self.total_dmg_crit_imm += total_round_dmg_crit_imm

            # Track cumulative total damage per round for plotting
            self.cumulative_damage_per_round.append(self.total_dmg)

            # Current average DPS - crit allowed
            rolling_dpr = self.total_dmg / round_num
            rolling_dps = rolling_dpr / 6
            current_dps = total_round_dmg / 6
            self.dps_window.append(rolling_dps)
            self.dps_rolling_avg.append(rolling_dps)
            self.dps_per_round.append(current_dps)

            # Current average DPS - crit immune
            rolling_dpr_crit_imm = self.total_dmg_crit_imm / round_num
            rolling_dps_crit_imm = rolling_dpr_crit_imm / 6
            current_dps_crit_imm = total_round_dmg_crit_imm / 6
            self.dps_crit_imm_window.append(rolling_dps_crit_imm)
            self.dps_crit_imm_rolling_avg.append(rolling_dps_crit_imm)
            self.dps_crit_imm_per_round.append(current_dps_crit_imm)

            # Stop if damage limit is reached
            if self.cfg.DAMAGE_LIMIT_FLAG and self.total_dmg >= self.cfg.DAMAGE_LIMIT:
                print(f"\nDamage limit of {self.cfg.DAMAGE_LIMIT} reached at round {round_num}, stopping simulation.")
                break

            # Check for convergence
            if len(self.dps_window) >= self.window_size:
                if self.convergence(round_num):
                    break

        # DPS values (crit allowed)
        dps_mean = statistics.mean(self.dps_per_round)
        dps_stdev = statistics.stdev(self.dps_per_round) if round_num > 1 else 0
        dps_error = self.z * (dps_stdev / math.sqrt(round_num))

        # DPS values (crit immune)
        dps_crit_imm_mean = statistics.mean(self.dps_crit_imm_per_round)
        dps_crit_imm_stdev = statistics.stdev(self.dps_crit_imm_per_round) if round_num > 1 else 0
        dps_crit_imm_error = self.z * (dps_crit_imm_stdev / math.sqrt(round_num))
        # Averaging crit-allowed and crit-immune
        dps_both = (dps_mean + dps_crit_imm_mean) / 2

        dpr = self.total_dmg / round_num
        dpr_crit_imm = self.total_dmg_crit_imm / round_num
        dph = self.total_dmg / self.stats.hits
        dph_crit_imm = self.total_dmg_crit_imm / self.stats.hits
        summary = (
            f"AB: {self.attack_sim.attack_prog} | Weapon: {self.weapon.name_purple} | Crit: {self.weapon.crit_threat}-20/x{self.weapon.crit_multiplier} | "
            f"Target AC: {self.cfg.TARGET_AC} | Target Immunities: {self.cfg.TARGET_IMMUNITIES_FLAG} | Rounds averaged: {round_num}\n"
            f"DPS (Crit allowed | immune): {dps_mean:.2f} ± {dps_error:.2f} | {dps_crit_imm_mean:.2f} ± {dps_crit_imm_error:.2f}\n"
            # f"DPS (Crit immune): {dps_crit_imm_mean:.2f} ± {dps_crit_imm_error:.2f}\n"
            f"TOTAL damage inflicted (Crit allowed | immune): {self.total_dmg} | {self.total_dmg_crit_imm}\n"
            # f"TOTAL damage inflicted (Crit immune): {self.total_dmg_crit_imm}\n"
            f"AVERAGE damage inflicted per HIT (Crit allowed | immune): {dph:.2f} | {dph_crit_imm:.2f}\n"
            # f"AVERAGE damage inflicted per HIT (Crit immune): {dph_crit_imm:.2f}\n"
            f"AVERAGE damage inflicted per ROUND (Crit allowed | immune): {dpr:.2f} | {dpr_crit_imm:.2f}\n"
            # f"AVERAGE damage inflicted per ROUND (Crit immune): {dpr_crit_imm:.2f}\n"
        )
        print(summary)

        self.stats.calc_rates_percentages()
        legend_proc_theoretical = self.attack_sim.get_legend_proc_rate_theoretical()

        return {
            "avg_dps_both": round(dps_both, 2),
            "dps_crits": round(dps_mean, 2),
            "dps_no_crits": round(dps_crit_imm_mean, 2),
            "dps_per_round": self.dps_per_round,
            "dps_rolling_avg": self.dps_rolling_avg,
            "cumulative_damage_per_round": self.cumulative_damage_per_round,
            "damage_by_type": self.cumulative_damage_by_type,
            "attack_prog": self.attack_sim.attack_prog,
            "hit_rate_actual": self.stats.hit_rate,
            "crit_rate_actual": self.stats.crit_hit_rate,
            "legend_proc_rate_actual": self.stats.legend_proc_rate,
            "hits_per_attack": self.stats.hits_per_attack,
            "crits_per_attack": self.stats.crits_per_attack,
            "hit_rate_theoretical": self.attack_sim.get_hit_chance() * 100,
            "crit_rate_theoretical": self.attack_sim.get_crit_chance() * 100,
            "legend_proc_rate_theoretical": legend_proc_theoretical * 100,
            "hit_rate_per_attack_theoretical": [x * 100 for x in self.attack_sim.hit_chance_list],
            "crit_rate_per_attack_theoretical": [x * 100 for x in self.attack_sim.crit_chance_list],
            "summary": summary,
        }

    def get_damage_results(self, damage_dict: dict, imm_factors: dict):
        damage_sums = {}
        for dmg_key, dmg_list in damage_dict.items():
            for dmg_sublist in dmg_list:
                dmg_popped = damage_sums.pop(dmg_key, 0)
                num_dice = dmg_sublist[0]
                num_sides = dmg_sublist[1]
                flat_dmg = dmg_sublist[2] if len(dmg_sublist) > 2 else 0    # Get flat damage if it exists, otherwise 0
                dmg_roll_results = self.attack_sim.damage_roll(num_dice, num_sides, flat_dmg)
                damage_sums[dmg_key] = dmg_popped + dmg_roll_results

        # Finally, apply target immunities and vulnerabilities
        damage_sums = self.attack_sim.damage_immunity_reduction(damage_sums, imm_factors)

        return damage_sums

    def plot_dps(self):
        # Prepare dataframe for seaborn
        rounds = list(range(1, len(self.dps_rolling_avg) + 1))
        df = pd.DataFrame({
            "Round": rounds,
            "MeanDPS": self.dps_rolling_avg,
            # "LowerCI": [m - e for m, e in zip(dps_means, dps_moes)],
            # "UpperCI": [m + e for m, e in zip(dps_means, dps_moes)]
        })

        # Plot with seaborn
        plt.figure(figsize=(10, 6))
        sns.lineplot(data=df, x="Round", y="MeanDPS", label="Mean DPS", color="blue")

        # Add the confidence interval as a filled area
        # plt.fill_between(df["Round"], df["LowerCI"], df["UpperCI"], alpha=0.2, color="blue", label="95% CI")

        plt.xlabel("Rounds simulated")
        plt.ylabel("DPS")
        plt.title("DPS Convergence with Margin of Error")
        plt.legend()
        plt.grid(True)
        plt.show()