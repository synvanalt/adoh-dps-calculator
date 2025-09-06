from weapons_db import WEAPON_PROPERTIES, PURPLE_WEAPONS
from simulator.config import Config


class Weapon:
    def __init__(self, weapon_name: str, config: Config):
        self.cfg = config
        self.name_base = weapon_name.split('_')[0]      # Example: Convert 'Dagger_PK' to 'Dagger'
        self.name_purple = weapon_name                  # Keep the full name 'Dagger_PK' for purple weapons management

        # Validate that the weapon exists in WEAPON_PROPERTIES
        if self.name_base not in WEAPON_PROPERTIES:
            raise ValueError(f"Weapon '{self.name_base}' not found in WEAPON_PROPERTIES")

        # Load weapon properties from the database
        # Example: 'Halberd': {'dmg': [1, 10, 'slashing & piercing'], 'threat': 20, 'multiplier': 3, 'size': 'L'},
        properties = WEAPON_PROPERTIES[self.cfg.SHAPE_WEAPON] if self.cfg.SHAPE_WEAPON_OVERRIDE else WEAPON_PROPERTIES[self.name_base]

        dice = properties['dmg'][0]
        sides = properties['dmg'][1]
        self.dmg = {'physical': [dice, sides, 0]}   # To fit the convention of [dice, sides, flat]
        self.threat_base = properties['threat']
        self.multiplier_base = properties['multiplier']
        self.size = properties['size']

        self.crit_threat = self.get_crit_threat()
        self.crit_multiplier = self.crit_multiplier()

    def get_crit_threat(self):
        """
        :return: The minimum value of the weapon's threat range, e.g., for Scimitar (with range 18-20) it should be 18
        """
        threat_range_max = 20  # Always 20 in NWN
        threat_range_min = self.threat_base
        base_threat_range = (threat_range_max - threat_range_min + 1)

        if self.cfg.KEEN:
            threat_range_min -= base_threat_range
        if self.cfg.IMPROVED_CRIT:
            threat_range_min -= base_threat_range
        if self.cfg.WEAPONMASTER:
            threat_range_min -= 2

        return threat_range_min

    def crit_multiplier(self):
        """
        :return: Critical hit multiplier, e.g., for a non-WM character wielding Scimitar it should be 2
        """
        if self.cfg.WEAPONMASTER:  # Add +1 to the multiplier if character is a Weaponmaster
            multiplier = self.multiplier_base + 1
        else:
            multiplier = self.multiplier_base

        return multiplier

    def enhancement_bonus(self):
        ammo_based_weapons = ['Heavy Crossbow', 'Light Crossbow', 'Longbow', 'Shortbow', 'Sling']
        if self.name_base == 'Scythe':
            enhancement_dmg = 20
        elif self.name_base == 'Dwarven Waraxe' and self.cfg.DAMAGE_VS_RACE:
            enhancement_dmg = 12
        elif self.name_base in ammo_based_weapons:
            enhancement_dmg = 0
        else:
            enhancement_dmg = self.cfg.ENHANCEMENT_BONUS
        return {'physical': [0, 0, enhancement_dmg]}    # To fit the convention of [dice, sides, flat]

    def strength_bonus(self):
        """
        :return: The flat physical damage added by Strength of the character
        """
        throwing_weapons = ['Darts', 'Throwing Axe']  # Throwing weapons that have "auto-mighty" property

        # two_handed = WEAPONS_TO_RUN[self.name_purple].get('TWO_HANDED', None)
        # two_handed = self.cfg.TWO_HANDED if two_handed is None else two_handed

        if self.name_base in throwing_weapons:  # Ranged weapons, but only for throwing weapons
            str_dmg = self.cfg.STR_MOD
        elif self.cfg.COMBAT_TYPE == 'melee':
            str_dmg = self.cfg.STR_MOD * 2 if self.cfg.TWO_HANDED else self.cfg.STR_MOD
        elif self.cfg.COMBAT_TYPE == 'ranged':  # Ranged weapons, excluding T.Axe
            str_dmg = min(self.cfg.STR_MOD, self.cfg.MIGHTY)
        else:
            raise ValueError(f"Invalid combat type: {self.cfg.COMBAT_TYPE}. Expected 'melee' or 'ranged'.")

        return {'physical': [0, 0, str_dmg]}    # To fit the convention of [dice, sides, flat]

    def aggregate_damage_sources(self):
        """
        :return: A dictionary of all damage sources (base weapon damage, strength bonus damage, etc.)
        Each item in the dictionary should be a list, and within it a sublist per damage type.
        For example: 'purple_dmg': [[2, 4, 'magical'], [1, 6, 'physical']]
        This master-list will later be looped over when damage is calculated.
        """
        dmg_src_dict = {
            'base_dmg': self.dmg,
            'purple_dmg': PURPLE_WEAPONS[self.name_purple],
            'enhancement_dmg': self.enhancement_bonus(),
            'str_dmg': self.strength_bonus(),
            'additional_dmg': [v[1] for v in self.cfg.ADDITIONAL_DAMAGE.values() if v[0] is True],
        }
        return dmg_src_dict

    def get_legend_proc_rate_theoretical(self, crit_rate):
        """
        :return: The theoretical chance to trigger a legend proc, based on the weapon's legend property
        """
        legend_proc_rate = 0.0
        purple_props = PURPLE_WEAPONS.get(self.name_purple, {})
        legendary = purple_props.get('legendary') if isinstance(purple_props, dict) else None
        if legendary:
            proc = legendary.get('proc')
            if isinstance(proc, (float, int)):
                legend_proc_rate = float(proc)
            elif isinstance(proc, str) and proc == 'on_crit':
                legend_proc_rate = crit_rate / 100
            else:
                legend_proc_rate = 0.0

        return legend_proc_rate
