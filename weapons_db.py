WEAPON_PROPERTIES = {
    # Size column is used to determine DUAL-WIELD penalty
    # MELEE TWO-HANDED WEAPONS:
    'Halberd':          {'dmg': [1, 10, 'slashing & piercing'], 'threat': 20, 'multiplier': 3, 'size': 'L'},
    'Heavy Flail':      {'dmg': [1, 10, 'bludgeoning'],         'threat': 19, 'multiplier': 2, 'size': 'L'},
    'Greataxe':         {'dmg': [1, 12, 'slashing'],            'threat': 20, 'multiplier': 3, 'size': 'L'},
    'Greatsword':       {'dmg': [2, 6,  'slashing'],            'threat': 19, 'multiplier': 2, 'size': 'L'},
    'Scythe':           {'dmg': [2, 4,  'slashing & piercing'], 'threat': 20, 'multiplier': 4, 'size': 'L'},
    'Spear':            {'dmg': [1, 8,  'piercing'],            'threat': 20, 'multiplier': 3, 'size': 'L'},
    'Trident':          {'dmg': [1, 8,  'piercing'],            'threat': 20, 'multiplier': 2, 'size': 'L'},

    # DOUBLE-SIDED WEAPONS:
    'Dire Mace':        {'dmg': [1, 8, 'bludgeoning'],  'threat': 20, 'multiplier': 2, 'size': 'slashing'},
    'Double Axe':       {'dmg': [1, 8, 'bludgeoning'],  'threat': 20, 'multiplier': 3, 'size': 'slashing'},
    'Two-Bladed Sword': {'dmg': [1, 8, 'slashing'],     'threat': 19, 'multiplier': 2, 'size': 'slashing'},

    # RANGED WEAPONS - THROWING:
    'Darts':            {'dmg': [1, 4, 'piercing'],     'threat': 20, 'multiplier': 2, 'size': 'T'},
    'Throwing Axes':    {'dmg': [1, 6, 'slashing'],     'threat': 20, 'multiplier': 3, 'size': 'slashing'},

    # RANGED WEAPONS - AMMO-BASED:
    'Heavy Crossbow':   {'dmg': [1, 10, 'piercing'],   'threat': 18, 'multiplier': 2, 'size': 'L'},
    'Light Crossbow':   {'dmg': [1, 8,  'piercing'],    'threat': 18, 'multiplier': 2, 'size': 'M'},
    'Longbow':          {'dmg': [1, 8,  'piercing'],    'threat': 20, 'multiplier': 3, 'size': 'L'},
    'Shortbow':         {'dmg': [1, 6,  'piercing'],    'threat': 20, 'multiplier': 3, 'size': 'M'},
    'Sling':            {'dmg': [1, 4,  'bludgeoning'], 'threat': 20, 'multiplier': 2, 'size': 'slashing'},

    # MONK WEAPONS:
    'Gloves':           {'dmg': [1, 3, 'bludgeoning'], 'threat': 20, 'multiplier': 2, 'size': 'T'},
    'Kama':             {'dmg': [1, 6, 'slashing'],    'threat': 20, 'multiplier': 2, 'size': 'T'},
    'Quarterstaff':     {'dmg': [1, 6, 'bludgeoning'], 'threat': 20, 'multiplier': 2, 'size': 'L'},
    'Shuriken':         {'dmg': [1, 3, 'piercing'],    'threat': 20, 'multiplier': 2, 'size': 'T'},

    # MEDIUM WEAPONS:
    'Bastard Sword':    {'dmg': [1, 10, 'slashing'],   'threat': 19, 'multiplier': 2, 'size': 'M'},
    'Battleaxe':        {'dmg': [1, 8,  'slashing'],    'threat': 20, 'multiplier': 3, 'size': 'M'},
    'Dwarven Waraxe':   {'dmg': [1, 10, 'slashing'],   'threat': 20, 'multiplier': 3, 'size': 'M'},
    'Katana':           {'dmg': [1, 10, 'slashing'],   'threat': 19, 'multiplier': 2, 'size': 'M'},
    'Light Flail':      {'dmg': [1, 8,  'bludgeoning'], 'threat': 20, 'multiplier': 2, 'size': 'M'},
    'Longsword':        {'dmg': [1, 8,  'slashing'],    'threat': 19, 'multiplier': 2, 'size': 'M'},
    'Morningstar':      {'dmg': [1, 8,  'bludgeoning & piercing'],  'threat': 20, 'multiplier': 2, 'size': 'M'},
    'Rapier':           {'dmg': [1, 6,  'piercing'],    'threat': 18, 'multiplier': 2, 'size': 'M'},
    'Scimitar':         {'dmg': [1, 6,  'slashing'],    'threat': 18, 'multiplier': 2, 'size': 'M'},
    'Warhammer':        {'dmg': [1, 8,  'bludgeoning'], 'threat': 20, 'multiplier': 3, 'size': 'M'},

    # SMALL\TINY WEAPONS:
    'Club':             {'dmg': [1, 6, 'bludgeoning'], 'threat': 20, 'multiplier': 2, 'size': 'M'},
    'Dagger':           {'dmg': [1, 4, 'piercing'],    'threat': 19, 'multiplier': 2, 'size': 'T'},
    'Handaxe':          {'dmg': [1, 6, 'piercing'],    'threat': 20, 'multiplier': 3, 'size': 'T'},
    'Kukri':            {'dmg': [1, 4, 'piercing'],    'threat': 18, 'multiplier': 2, 'size': 'T'},
    'Light Hammer':     {'dmg': [1, 8, 'bludgeoning & piercing'],  'threat': 20, 'multiplier': 2, 'size': 'slashing'},
    'Mace':             {'dmg': [1, 6, 'bludgeoning'], 'threat': 20, 'multiplier': 2, 'size': 'slashing'},
    'Shortsword':       {'dmg': [1, 6, 'slashing'],    'threat': 19, 'multiplier': 2, 'size': 'slashing'},
    'Sickle':           {'dmg': [1, 6, 'slashing'],    'threat': 20, 'multiplier': 2, 'size': 'slashing'},
    'Whip':             {'dmg': [1, 6, 'slashing'],    'threat': 20, 'multiplier': 2, 'size': 'slashing'},
}
PURPLE_WEAPONS = {
    # MELEE TWO-HANDED WEAPONS:
    # HALBERD SNEAK WAS 2D6
    'Halberd': [[2, 6, 'sneak'], [2, 12, 'physical'], [0, 200, 'massive'], [1, 30, 'legendary', 'fire', 0.05], [1, 30, 'legendary', 'pure', 0.05]], # Ahrim's Sacrifice, hold on hit, 43
    'Heavy Flail': [[2, 12, 'physical'], [2, 6, 'negative'], [2, 6, 'divine'], [2, 6, 'magical'], [0, 5, 'legendary', 'physical', 0.05]], # [0, 2.5, 'physical']], # None
    'Greataxe': [[2, 12, 'physical'], [2, 8, 'divine'], [2, 12, 'fire'], [2, 8, 'vs_race_undead', 'physical']], # immune level drain
    'Greatsword_Desert': [[2, 12, 'physical'], [2, 8, 'divine'], [2, 8, 'fire'], [2, 12, 'massive'], [1, 6, 'pure']],  # Pure vs. Evil
    'Greatsword_Legion': [[2, 12, 'physical'], [2, 8, 'divine'], [2, 8, 'cold'], [2, 12, 'massive'], [0, 0, 'legendary', 'effect_sunder', 0.05]],  # Sunder effect (-2 AC for 2 rounds)
    'Greatsword_Tyr': [[2, 12, 'physical'], [2, 12, 'divine'], [2, 6, 'fire'], [2, 8, 'vs_race_undead_outsider', 'pure']], # Tyr
    'Scythe': [[2, 12, 'physical'], [2, 6, 'negative']],
    'Spear': [[2, 10, 'physical'], [2, 6, 'acid'], [2, 6, 'cold'], [2, 6, 'fire'], [2, 6, 'electrical'], [2, 6, 'legendary', 'acid', 0.05], [2, 6, 'legendary', 'pure', 0.05]], # [0, .35, 'acid'], [0, .35, 'pure']],  # freedom
    'Trident_Fire': [[2, 12, 'physical'], [2, 12, 'fire'], [1, 12, 'magical'], [1, 12, 'negative']], # Blind on hit, fire immune 20% cold vuln 10$
    'Trident_Ice': [[2, 12, 'physical'], [2, 12, 'cold'], [2, 10, 'magical'], [1, 10, 'massive'], [2, 6, 'legendary', 'cold', 'on_crit'], [2, 6, 'legendary', 'pure', 'on_crit']],  # Icy veng

    # DOUBLE-SIDED WEAPONS:
    'Dire Mace': [[8, 6, 'physical'], [2, 6, 'magical']],   # 10% phys immune
    'Double Axe': [[7, 6, 'physical'], [1, 12, 'negative'], [0, 10, 'massive'], [2, 20, 'legendary', 'physical', 0.05]],  # Wounding, vamp regen
    'Two-Bladed Sword': [[2, 12, 'physical'], [2, 6, 'positive'], [2, 6, 'negative'], [2, 6, 'massive']], # +3 AC, on hit doom

    # RANGED WEAPONS - THROWING:
    'Darts': [[2, 6, 'magical'], [2, 12, 'pure'], [2, 12, 'legendary', 'pure', 0.05]],  # [0, 0.65, 'pure']],  # none
    'Throwing Axes': [[7, 6, 'sonic'], [1, 6, 'massive']],  # silence on hit

    # RANGED WEAPONS - AMMO-BASED:
    'Heavy Crossbow': [[2, 12, 'physical'], [2, 8, 'acid'], [1, 12, 'magical'], [2, 6, 'fire'], [2, 8, 'massive']], # Was "Bolts"
    'Light Crossbow': [[2, 12, 'physical'], [2, 8, 'acid'], [1, 12, 'magical'], [1, 10, 'cold'], [1, 10, 'massive']],
    'Longbow': [[2, 12, 'physical'], [2, 8, 'negative'], [1, 12, 'magical'], [2, 6, 'fire'], [2, 6, 'massive'], [2, 6, 'legendary', 'fire', 'on_crit'], [2, 6, 'legendary', 'pure', 'on_crit']],    # Was "Arrows"
    'Shortbow': [[2, 12, 'physical'], [2, 8, 'negative'], [1, 12, 'magical'], [1, 10, 'electrical'], [2, 8, 'massive']],
    'Sling': [[2, 8, 'physical'], [2, 8, 'fire'], [2, 6, 'pure'], [2, 6, 'divine']],  # was Bullets

    # MONK WEAPONS:
    'Gloves_Shandy': [[2, 6, 'physical'], [2, 6, 'acid'], [2, 6, 'magical'], [2, 6, 'divine']],  # Legendary remove immunities
    'Gloves_Adam': [[2, 8, 'physical'], [2, 8, 'pure'], [2, 8, 'divine'], [1, 6, 'sneak']],    # Doom
    'Kama': [[2, 8, 'physical'], [2, 6, 'divine'], [2, 6, 'positive']],  # 4 regen, 5% neg & pos
    'Quarterstaff': [[2, 10, 'physical'], [2, 10, 'cold'], [2, 10, 'fire']],  # 10% fire/cold immune
    'Shuriken': [[2, 6, 'physical'], [2, 6, 'negative'], [2, 4, 'pure'], [2, 6, 'sneak']],

    # MEDIUM WEAPONS:
    'Bastard Sword': [[2, 6, 'physical'], [2, 6, 'divine'], [2, 6, 'magical'], [2, 6, 'negative'], [1, 6, 'sneak']], # None
    'Battleaxe': [[2, 8, 'physical'], [2, 8, 'magical'], [2, 8, 'negative']],  # divine resist 5/ 5% immune
    'Dwarven Waraxe': [[2, 8, 'physical'], [2, 10, 'acid'], [2, 8, 'negative'], [2, 6, 'vs_race_dragon', 'pure']],  # [0, 2, 'physical']], # vs Dragons
    'Katana': [[2, 12, 'physical'], [2, 6, 'divine'], [2, 8, 'sonic'], [2, 20, 'legendary', 'fire', 0.05]], # [0, 1.05, 'fire']],  # level drain on hit
    'Light Flail': [[7, 6, 'physical'], [2, 8, 'pure'], [0, 0, 'legendary', 'effect_sunder', 0.05]],  # sunder
    'Longsword': [[2, 8, 'physical'], [2, 12, 'cold'], [2, 6, 'magical'], [2, 6, 'legendary', 'cold', 'on_crit'], [2, 6, 'legendary', 'pure', 'on_crit']],  # Icy Veng, 2d6 pierce v. undead
    'Morningstar': [[2, 6, 'physical'], [7, 6, 'positive'], [1, 6, 'massive']],  # divine extend, 10% pos immune
    'Rapier': [[2, 6, 'physical'], [2, 6, 'magical'], [2, 6, 'cold'], [0, 25, 'massive']],  # + pp skill
    'Scimitar': [[7, 6, 'physical'], [7, 6, 'massive']],  # 5% phys immune
    'Warhammer': [[2, 8, 'physical'], [2, 8, 'positive'], [2, 8, 'magical']],  # on hit confuse

    # SMALL\TINY WEAPONS:
    'Club_Fish': [[2, 10, 'physical'], [7, 6, 'acid']],  # acid resist 20, on-hit stun
    'Club_Stone': [[2, 8, 'physical'], [7, 6, 'sonic']],  # 5% reduce immunities by 5% for 2 rounds
    'Dagger_LW': [[2, 6, 'physical'], [2, 4, 'divine'], [2, 4, 'acid'], [2, 4, 'pure'], [0, 300, 'legendary', 'physical', 0.01]], # [0, 3, 'physical']],  # Leg Last Words
    'Dagger_PK': [[2, 6, 'physical'], [2, 6, 'negative'], [0, 60, 'massive']], # Leg PHASE
    'Handaxe': [[2, 6, 'physical'], [2, 6, 'negative'], [2, 8, 'acid'], [2, 6, 'legendary', 'acid', 0.05], [2, 6, 'legendary', 'pure', 0.05]],    # [0, .35, 'acid'], [0, .35, 'pure']], # 10% acid immune, on hit poison
    'Kukri': [[2, 6, 'physical'], [2, 6, 'divine'], [2, 6, 'magical'], [1, 4, 'positive']],  # dmg vs alignment
    'Light Hammer': [[2, 10, 'physical'], [2, 12, 'cold'], [1, 6, 'magical'], [2, 6, 'legendary', 'cold', 'on_crit'], [2, 6, 'legendary', 'pure', 'on_crit']],  # [0, .35, 'electrical'], [0, .35, 'pure']]
    'Mace': [[2, 12, 'physical'], [2, 12, 'electrical'], [1, 6, 'pure'], [2, 6, 'legendary', 'electrical', 0.05], [2, 6, 'legendary', 'pure', 0.05]], # [0, .35, 'electrical'], [0, .35, 'pure']], # call Thunder, on-hit stun
    'Shortsword_Cleaver': [[2, 6, 'physical'], [2, 6, 'acid'], [2, 6, 'negative'], [2, 12, 'massive']],  # regen/vampiric
    'Shortsword_Adam': [[2, 6, 'physical'], [2, 6, 'divine'], [2, 6, 'pure']],
    'Sickle': [[2, 10, 'physical'], [2, 10, 'divine']],  # none
    'Whip': [[2, 6, 'physical'], [2, 8, 'positive'], [2, 10, 'acid'], [2, 12, 'legendary', 'acid', 0.05]], # [0, 0.65, 'acid']],  # acid rain
}

PURPLE_WEAPONS_LEGEND_DURATION = [  # Weapons with effects that last TWO (actually FIVE) rounds
    'Darts',
    'Club_Stone',
    'Greatsword_Legion',
    'Heavy Flail',
    'Light Flail',
]

WEAPON_PROPERTIES_OLD = {
    # MELEE TWO-HANDED WEAPONS:
    'Halberd': [[1, 10, 'slash & pierce'], [20, 20, 'threat'], [3, 'multiplier']],
    'Heavy Flail': [[1, 10, 'bludgeon'], [19, 20, 'threat'], [2, 'multiplier']],
    'Greataxe': [[1, 12, 'slash'], [20, 20, 'threat'], [3, 'multiplier']],
    'Greatsword Desert': [[2, 6, 'slash'], [19, 20, 'threat'], [2, 'multiplier']],
    'Greatsword Tyr': [[2, 6, 'slash'], [19, 20, 'threat'], [2, 'multiplier']],
    'Scythe': [[2, 4, 'slash & pierce'], [20, 20, 'threat'], [4, 'multiplier']],
    'Spear': [[1, 8, 'pierce'], [20, 20, 'threat'], [3, 'multiplier']],
    'Trident Fire': [[1, 8, 'pierce'], [20, 20, 'threat'], [2, 'multiplier']],
    'Trident Ice': [[1, 8, 'pierce'], [20, 20, 'threat'], [2, 'multiplier']],

    # DOUBLE-SIDED WEAPONS:
    'Dire Mace': [[1, 8, 'bludgeon'], [20, 20, 'threat'], [2, 'multiplier']],
    'Double Axe': [[1, 8, 'bludgeon'], [20, 20, 'threat'], [3, 'multiplier']],
    'Two-Bladed Sword': [[1, 8, 'bludgeon'], [19, 20, 'threat'], [2, 'multiplier']],

    # RANGED WEAPONS - THROWING:
    'Darts': [[1, 4, 'pierce'], [20, 20, 'threat'], [2, 'multiplier']],
    'Throwing Axes': [[1, 6, 'slash'], [20, 20, 'threat'], [3, 'multiplier']],

    # RANGED WEAPONS - AMMO-BASED:
    'Heavy Crossbow': [[1, 10, 'pierce'], [18, 20, 'threat'], [2, 'multiplier']],
    'Light Crossbow': [[1, 8, 'pierce'], [18, 20, 'threat'], [2, 'multiplier']],
    'Longbow': [[1, 8, 'pierce'], [20, 20, 'threat'], [3, 'multiplier']],
    'Shortbow': [[1, 6, 'pierce'], [20, 20, 'threat'], [3, 'multiplier']],
    'Sling': [[1, 4, 'bludgeon'], [20, 20, 'threat'], [2, 'multiplier']],

    # MONK WEAPONS:
    'Gloves Shandy': [[1, 3, 'bludgeon'], [20, 20, 'threat'], [2, 'multiplier']],
    'Gloves Adam': [[1, 3, 'bludgeon'], [20, 20, 'threat'], [2, 'multiplier']],
    'Kama': [[1, 6, 'slash'], [20, 20, 'threat'], [2, 'multiplier']],
    'Quarterstaff': [[1, 6, 'bludgeon'], [20, 20, 'threat'], [2, 'multiplier']],
    'Shuriken': [[1, 3, 'pierce'], [20, 20, 'threat'], [2, 'multiplier']],

    # MEDIUM WEAPONS:
    'Bastard Sword': [[1, 10, 'slash'], [19, 20, 'threat'], [2, 'multiplier']],
    'Battleaxe': [[1, 8, 'slash'], [20, 20, 'threat'], [3, 'multiplier']],
    'Dwarven Waraxe': [[1, 10, 'slash'], [20, 20, 'threat'], [3, 'multiplier']],
    'Katana': [[1, 10, 'slash'], [19, 20, 'threat'], [2, 'multiplier']],
    'Light Flail': [[1, 8, 'bludgeon'], [20, 20, 'threat'], [2, 'multiplier']],
    'Longsword': [[1, 8, 'slash'], [19, 20, 'threat'], [2, 'multiplier']],
    'Morningstar': [[1, 8, 'bludgeon & pierce'], [20, 20, 'threat'], [2, 'multiplier']],
    'Rapier': [[1, 6, 'pierce'], [18, 20, 'threat'], [2, 'multiplier']],
    'Scimitar': [[1, 6, 'slash'], [18, 20, 'threat'], [2, 'multiplier']],
    'Warhammer': [[1, 8, 'bludgeon'], [20, 20, 'threat'], [3, 'multiplier']],

    # SMALL\TINY WEAPONS:
    'Club': [[1, 6, 'bludgeon'], [20, 20, 'threat'], [2, 'multiplier']],
    'Dagger LW': [[1, 4, 'pierce'], [19, 20, 'threat'], [2, 'multiplier']],
    'Dagger PK': [[1, 4, 'pierce'], [19, 20, 'threat'], [2, 'multiplier']],
    'Handaxe': [[1, 6, 'pierce'], [20, 20, 'threat'], [3, 'multiplier']],
    'Kukri': [[1, 4, 'pierce'], [18, 20, 'threat'], [2, 'multiplier']],
    'Light Hammer': [[1, 8, 'bludgeon & pierce'], [20, 20, 'threat'], [2, 'multiplier']],
    'Mace': [[1, 6, 'bludgeon'], [20, 20, 'threat'], [2, 'multiplier']],
    'Shortsword Cleaver': [[1, 6, 'slash'], [19, 20, 'threat'], [2, 'multiplier']],
    'Shortsword Adam': [[1, 6, 'slash'], [19, 20, 'threat'], [2, 'multiplier']],
    'Sickle': [[1, 6, 'slash'], [20, 20, 'threat'], [2, 'multiplier']],
    'Whip': [[1, 6, 'slash'], [20, 20, 'threat'], [2, 'multiplier']],
}