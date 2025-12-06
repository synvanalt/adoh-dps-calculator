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
    CHANGE_THRESHOLD: float = 0.0002
    STD_THRESHOLD: float = 0.0002

    # USER INPUTS - CHARACTER
    AB: int = 68
    AB_CAPPED: int = 70
    AB_PROG: str = "5APR Classic"
    AB_PROGRESSIONS: Dict[str, Any] = field(default_factory=lambda: {
        "4APR Classic":                     [0, -5, -10, 0],
        "4APR & Blinding Speed":            [0, -5, -10, 0, -5],
        "4APR & Rapid Shot":                [0, -5, -10, 0, -5],
        "4APR & R.Shot & B.Speed":          [0, -5, -10, 0, -5, -10],
        "4APR Dual-Wield":                  [0, -5, -10, "dw_hasted", 0, -5],
        "4APR Dual-Wield & B.Speed":        [0, -5, -10, "dw_hasted", "dw_bspeed", 0, -5],
        "5APR Classic":                     [0, -5, -10, -15, 0],
        "5APR Shifter":                     [0, -5, -10, 0, -5],
        "5APR & Blinding Speed":            [0, -5, -10, -15, 0, -5],
        "5APR & Rapid Shot":                [0, -5, -10, -15, 0, -5],
        "5APR & R.Shot & B.Speed":          [0, -5, -10, -15, 0, -5, -10],
        "5APR Dual-Wield":                  [0, -5, -10, -15, "dw_hasted", 0, -5],
        "5APR Dual-Wield & B.Speed":        [0, -5, -10, -15, "dw_hasted", "dw_bspeed", 0, -5],
        "Monk APR":                         [0, -3, -6, -9, -12, -15, 0],
        "Monk APR & Flurry":                [0, -3, -6, -9, -12, -15, 0, -5],
        "Monk APR & Flurry & B.Speed":      [0, -3, -6, -9, -12, -15, 0, -5, -10],
        "Monk Kama Dual-Wield":             [0, -3, -6, -9, -12, -15, "dw_hasted", 0, -5],
        "Monk Kama Dual-Wield & Flurry":    [0, -3, -6, -9, -12, -15, "dw_hasted", "dw_flurry", 0, -5],
        "Monk Kama Dual-Wield & B.Speed":   [0, -3, -6, -9, -12, -15, "dw_hasted", "dw_bspeed", 0, -5],
        "Monk Kama Dual-Wield & Flurry & B.Speed":  [0, -3, -6, -9, -12, -15, "dw_hasted", "dw_flurry", "dw_bspeed", 0, -5],
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

    # EXTRA DAMAGE SOURCES: name: [enabled, {damage_type: [dice, sides, flat]}]
    ADDITIONAL_DAMAGE: Dict[str, Any] = field(default_factory=lambda: {
        "Flame_Weapon":     [True,  {'fire_fw':     [1, 4, 10]}],
        "Darkfire":         [False, {'fire_fw':     [1, 6, 10]}],
        "Weapon_Spec":      [False, {'physical':    [0, 0, 2]}],
        "Epic_Weapon_Spec": [False, {'physical':    [0, 0, 4]}],
        "Bane_of_Enemies":  [False, {'physical':    [2, 6, 0]}],
        "Blade_Thirst":     [False, {'physical':    [0, 0, 6]}],
        "Favored_Enemy":    [False, {'physical':    [0, 0, 9]}],
        "Tenacious_Blow":   [False, {'physical':    [0, 0, 8]}],
        "Enchant_Arrow":    [False, {'physical':    [0, 0, 15]}],
        "Bard_Song":        [False, {'physical':    [0, 0, 3]}],
        "Divine_Favor":     [False, {'magical':     [0, 0, 5]}],
        "Divine_Might":     [False, {'divine':      [0, 0, 11]}],
        "Divine_Wrath":     [False, {'pure':        [0, 0, 13]}],
        "Defeaning_Clang":  [False, {'sonic':       [0, 0, 3]}],
        "Bless_Weapon":     [False, {'divine':      [2, 6, 0]}],
        "Sneak_Attack":     [False, {'sneak':       [5, 6, 0]}],
        "Death_Attack":     [False, {'death':       [3, 6, 0]}],
        "Pure_Set_Bonus":   [False, {'pure':        [1, 4, 0]}],
    })


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