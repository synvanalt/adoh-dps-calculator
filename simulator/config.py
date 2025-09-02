from dataclasses import dataclass, field, asdict
from typing import Dict, List, Any


@dataclass
class Config:
    # USER INPUTS - TARGET
    TARGET_AC: int = 65
    TARGET_IMMUNITIES_FLAG: bool = True
    TARGET_IMMUNITIES: Dict[str, float] = field(default_factory=lambda: {
        "pure": 0.0,
        "magical": 0.1,
        "positive": 0.1,
        "divine": 0.1,
        "negative": 0.25,
        "sonic": 0.25,
        "acid": 0.25,
        "electrical": 0.25,
        "cold": 0.25,
        "fire": 0.25,
        "physical": 0.35,
    })

    # SIMULATION SETTINGS
    DEFAULT_WEAPONS: List[str] = field(default_factory=lambda: ["Scythe"])
    ROUNDS: int = 15000
    DAMAGE_LIMIT_FLAG: bool = False
    DAMAGE_LIMIT: int = 6000
    DAMAGE_VS_RACE: bool = False

    # USER INPUTS - CHARACTER
    AB: int = 68
    AB_CAPPED: int = 70
    AB_PROG: str = "Classic 5APR"
    AB_PROGRESSIONS: Dict[str, Any] = field(default_factory=lambda: {
        "Classic 5APR":                     [0, -5, -10, -15, 0],
        "Shifter 5APR":                     [0, -5, -10, 0, -5],
        "Dual-Wield APR":                   [0, -5, -10, -15, "-dw_penalty", 0, -5],
        "Dual-Wield & Blinding Speed":      [0, -5, -10, -15, "-dw_penalty", 0, -5, -10],
        "Ranged & Rapid Shot":              [0, -5, -10, -15, 0, -5],
        "Ranged & R.Shot & B.Speed":        [0, -5, -10, -15, 0, -5, -10],
        "Monk APR":                         [0, -3, -6, -9, -12, -15, 0],
        "Monk & Flurry":                    [0, -3, -6, -9, -12, -15, 0, -5],
        "Monk & Flurry & B.Speed":          [0, -3, -6, -9, -12, -15, 0, -5, -10],
        "Monk Kama & Dual-Wield":           [0, -3, -6, -9, -12, -15, "-dw_penalty", 0, -5],
        "Monk Kama & Dual-Wield & Flurry":  [0, -3, -6, -9, -12, -15, "-dw_penalty", 0, -5, -10],
    })

    TOON_SIZE: str = "M"        # "S" / "M" / "L"
    COMBAT_TYPE: str = "melee"  # "melee" or "ranged"
    MIGHTY: int = 0
    ENHANCEMENT_BONUS: int = 10
    STR_MOD: int = 21
    TWO_HANDED: bool = False
    WEAPONMASTER: bool = False
    KEEN: bool = True
    IMPROVED_CRIT: bool = True
    SHAPE_WEAPON_OVERRIDE: bool = False
    SHAPE_WEAPON: str = "Scythe"

    # EXTRA DAMAGE SOURCES
    ADDITIONAL_DAMAGE: Dict[str, Any] = field(default_factory=lambda: {
        "Flame_Weapon":     [True,  [1, 4, "fire_fw", 10]],
        "Darkfire":         [False, [1, 6, "fire_fw", 10]],
        "Weapon_Spec":      [False, [0, 2, "physical", 0]],
        "Epic_Weapon_Spec": [False, [0, 4, "physical", 0]],
        "Blade_Thirst":     [False, [0, 6, "physical", 0]],
        "Favored_Enemy":    [False, [0, 9, "physical", 0]],
        "Enchant_Arrow":    [False, [0, 15, "physical", 0]],
        "Bard_Song":        [False, [0, 3, "physical", 0]],
        "Divine_Favor":     [False, [0, 5, "magical", 0]],
        "Divine_Might":     [False, [0, 11, "divine", 0]],
        "Divine_Wrath":     [False, [0, 13, "pure", 0]],
        "Bane_of_Enemies":  [False, [2, 6, "physical", 0]],
        "Sneak_Attack":     [False, [5, 6, "sneak", 0]],
        "Death_Attack":     [False, [3, 6, "death", 0]],
        "Pure_Set_Bonus":   [False, [1, 4, "pure", 0]],
    })

WEAPONS_TO_RUN = {
    # # LARGE WEAPONS:
    # 'Halberd':              {'AB_MOD': None, 'AB_PROG': 'classic_5apr', 'TWO_HANDED': True},
    # 'Heavy Flail':          {'AB_MOD': None, 'AB_PROG': None, 'TWO_HANDED': True},
    'Greataxe':             {'AB_MOD': None, 'AB_PROG': 'classic_5apr', 'TWO_HANDED': True},
    # 'Greatsword_Desert':    {'AB_MOD': None, 'AB_PROG': 'classic_5apr', 'TWO_HANDED': True},
    # 'Greatsword_Legion':       {'AB_MOD': None, 'AB_PROG': 'classic_5apr', 'TWO_HANDED': True},
    # 'Greatsword_Tyr':       {'AB_MOD': None, 'AB_PROG': 'classic_5apr', 'TWO_HANDED': True},
    # 'Scythe':               {'AB_MOD': None, 'AB_PROG': 'classic_5apr', 'TWO_HANDED': True},
    # 'Spear':                {'AB_MOD': None, 'AB_PROG': None, 'TWO_HANDED': True},
    # 'Trident_Fire':         {'AB_MOD': None, 'AB_PROG': 'classic_5apr', 'TWO_HANDED': True},
    # 'Trident_Ice':          {'AB_MOD': None, 'AB_PROG': 'classic_5apr', 'TWO_HANDED': True},
    #
    # # DOUBLE-SIDED WEAPONS:
    # 'Dire Mace':        {'AB_MOD': None, 'AB_PROG': None},
    # 'Double Axe':       {'AB_MOD': None, 'AB_PROG': None},
    # 'Two-Bladed Sword': {'AB_MOD': None, 'AB_PROG': None},
    #
    # # RANGED WEAPONS - THROWING:
    # 'Darts':            {'AB_MOD': None, 'AB_PROG': None},
    # 'Throwing Axes':    {'AB_MOD': None, 'AB_PROG': None},
    #
    # # RANGED WEAPONS - AMMO-BASED:
    # 'Heavy Crossbow':   {'AB_MOD': None, 'AB_PROG': None},
    # 'Light Crossbow':   {'AB_MOD': None, 'AB_PROG': None},
    # 'Longbow':          {'AB_MOD': None, 'AB_PROG': None},
    # 'Shortbow':         {'AB_MOD': None, 'AB_PROG': None},
    # 'Sling':            {'AB_MOD': None, 'AB_PROG': None},
    #
    # # MONK WEAPONS:
    # 'Gloves_Shandy':    {'AB_MOD': None, 'AB_PROG': None},
    # 'Gloves_Adam':      {'AB_MOD': None, 'AB_PROG': None},
    # 'Kama':             {'AB_MOD': None, 'AB_PROG': 'monk_kama_dw_flurry'},
    # 'Quarterstaff':     {'AB_MOD': None, 'AB_PROG': None, 'TWO_HANDED': None},
    # 'Shuriken':         {'AB_MOD': None, 'AB_PROG': None},
    #
    # MEDIUM WEAPONS:
    # 'Bastard Sword':    {'AB_MOD': None, 'AB_PROG': None},
    # 'Battleaxe':        {'AB_MOD': None, 'AB_PROG': None},
    # 'Dwarven Waraxe':   {'AB_MOD': None, 'AB_PROG': None},
    # 'Katana':           {'AB_MOD': None, 'AB_PROG': None},
    # 'Light Flail':      {'AB_MOD': None, 'AB_PROG': None},
    # 'Longsword':        {'AB_MOD': None, 'AB_PROG': None},
    # 'Morningstar':      {'AB_MOD': None, 'AB_PROG': None},
    # 'Rapier':           {'AB_MOD': None, 'AB_PROG': None},
    # 'Scimitar':         {'AB_MOD': None, 'AB_PROG': None},
    # 'Warhammer':        {'AB_MOD': None, 'AB_PROG': None},
    #
    # # SMALL\TINY WEAPONS:
    # 'Club':                 {'AB_MOD': None, 'AB_PROG': None},
    # 'Dagger_LW':            {'AB_MOD': None, 'AB_PROG': None},
    # 'Dagger_PK':            {'AB_MOD': None, 'AB_PROG': None},
    # 'Handaxe':              {'AB_MOD': None, 'AB_PROG': None},
    # 'Kukri':                {'AB_MOD': None, 'AB_PROG': None},
    # 'Light Hammer':         {'AB_MOD': None, 'AB_PROG': None},
    # 'Mace':                 {'AB_MOD': None, 'AB_PROG': None},
    # 'Shortsword_Cleaver':   {'AB_MOD': None, 'AB_PROG': None},
    # 'Shortsword_Adam':      {'AB_MOD': None, 'AB_PROG': None},
    # 'Sickle':               {'AB_MOD': None, 'AB_PROG': None},
    # 'Whip':                 {'AB_MOD': None, 'AB_PROG': None},
}


if __name__ == '__main__':
    # --- Usage example ---
    cfg = Config()

    # Access like dataclass
    print(cfg.AB)
    print(cfg.AB_PROGRESSIONS["Classic 5APR"])

    # Update dynamically from a Dash widget
    cfg.AB = 72
    cfg.ADDITIONAL_DAMAGE["Darkfire"][0] = True

    print(cfg.AB)
    print(cfg.ADDITIONAL_DAMAGE["Darkfire"])

    # Convert to dict for JSON / dcc.Store
    config_dict = asdict(cfg)

    # Restore from JSON:
    # Config(**json_data)