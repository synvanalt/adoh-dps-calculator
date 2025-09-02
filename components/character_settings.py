from dash import html
import dash_bootstrap_components as dbc
from weapons_db import WEAPON_PROPERTIES
from typing import Literal


def build_character_settings(cfg):
    persist_type: Literal["local", "session", "memory"] = "session"

    return dbc.Col([
        html.H4('Character Settings', className='mb-4'),

        # Attack Bonus Settings
        dbc.Row([
            dbc.Col(dbc.Label(
                'Attack Bonus (AB):',
                html_for='ab-input'
            ), xs=6, md=6),
            dbc.Col(dbc.Input(
                id='ab-input',
                type='number',
                value=cfg.AB,
                persistence=True,
                persistence_type=persist_type
            ), xs=6, md=6)
        ], class_name=''),

        dbc.Row([
            dbc.Col(dbc.Label(
                'AB Capped:',
                html_for='ab-capped-input',
            ), xs=6, md=6),
            dbc.Col(dbc.Input(
                id='ab-capped-input',
                type='number',
                value=cfg.AB_CAPPED,
                persistence=True,
                persistence_type=persist_type
            ), xs=6, md=6)
        ], class_name=''),

        dbc.Row([
            dbc.Col(dbc.Label(
                'AB Progression:',
                html_for='ab-prog-dropdown',
            ), xs=6, md=6),
            dbc.Col(dbc.Select(
                id='ab-prog-dropdown',
                options=[{"label": key, "value": key} for key in cfg.AB_PROGRESSIONS.keys()],
                value="Classic 5APR",  # default value
                persistence=True,
                persistence_type=persist_type,
            ), xs=6, md=6)
        ], class_name=''),

        dbc.Row([
            dbc.Col(dbc.Label(
                'Character Size:',
                html_for='toon-size-dropdown',
            ), xs=6, md=6),
            dbc.Col(dbc.Select(
                id='toon-size-dropdown',
                options=[
                    {'label': 'Small', 'value': 'S'},
                    {'label': 'Medium', 'value': 'M'},
                    {'label': 'Large', 'value': 'L'}
                ],
                value=cfg.TOON_SIZE,
                persistence=True,
                persistence_type=persist_type,
            ), xs=6, md=6)
        ], class_name=''),

        # Combat Settings
        dbc.Row([
            dbc.Col(dbc.Label(
                'Combat Type:',
                html_for='combat-type-dropdown',
            ), xs=6, md=6),
            dbc.Col(dbc.Select(
                id='combat-type-dropdown',
                options=[
                    {'label': 'Melee', 'value': 'melee'},
                    {'label': 'Ranged', 'value': 'ranged'}
                ],
                value=cfg.COMBAT_TYPE,
                persistence=True,
                persistence_type=persist_type,
            ), xs=6, md=6)
        ], class_name=''),

        dbc.Row([
            dbc.Col(dbc.Label(
                'Mighty (Ranged):',
                html_for='mighty-input',
            ), xs=6, md=6),
            dbc.Col(dbc.Input(
                id='mighty-input',
                type='number',
                value=cfg.MIGHTY,
                persistence=True,
                persistence_type=persist_type,
            ), xs=6, md=6)
        ], class_name=''),

        # Character Stats
        dbc.Row([
            dbc.Col(dbc.Label(
                'Enhancement Bonus:',
                html_for='enhancement-bonus-input',
            ), xs=6, md=6),
            dbc.Col(dbc.Input(
                id='enhancement-bonus-input',
                type='number',
                value=cfg.ENHANCEMENT_BONUS,
                persistence=True,
                persistence_type=persist_type,
            ), xs=6, md=6)
        ], class_name=''),

        dbc.Row([
            dbc.Col(dbc.Label(
                'Strength Modifier:',
                html_for='str-mod-input',
            ), xs=6, md=6),
            dbc.Col(dbc.Input(
                id='str-mod-input',
                type='number',
                value=cfg.STR_MOD,
                persistence=True,
                persistence_type=persist_type,
            ), xs=6, md=6)
        ], class_name=''),

        # Two-Handed Weapon: combine switch+label into single Col using label kwarg
        dbc.Row([
            dbc.Col(dbc.Switch(
                id={'type': 'melee-switch', 'name': 'two-handed'},
                label='Two-Handed Weapon',
                label_style={'marginLeft': '0.5em'},
                value=cfg.TWO_HANDED,
                persistence=True,
                persistence_type=persist_type,
            ), xs=12, md=12),
        ], class_name='switcher', id={'type': 'melee-row', 'name': 'two-handed'}),

        # Weaponmaster: single Col with label inside switch
        dbc.Row([
            dbc.Col(dbc.Switch(
                id={'type': 'melee-switch', 'name': 'weaponmaster'},
                label='Weaponmaster',
                value=cfg.WEAPONMASTER,
                persistence=True,
                persistence_type=persist_type,
            ), xs=12, md=12),
        ], class_name='switcher', id={'type': 'melee-row', 'name': 'weaponmaster'}),

        # Critical Hit Settings: Keen
        dbc.Row([
            dbc.Col(dbc.Switch(
                id='keen-switch',
                label='Keen',
                value=cfg.KEEN,
                persistence=True,
                persistence_type=persist_type,
            ), xs=12, md=12),
        ], class_name='switcher'),

        # Critical Hit Settings: Improved Crit
        dbc.Row([
            dbc.Col(dbc.Switch(
                id='improved-crit-switch',
                label='Improved Critical',
                value=cfg.IMPROVED_CRIT,
                persistence=True,
                persistence_type=persist_type,
            ), xs=12, md=12),
        ], class_name='switcher'),

        # Shape Weapon Override: switch and dropdown inline on md, stacked on xs
        dbc.Row([
            dbc.Col(dbc.Switch(
                id='shape-weapon-switch',
                label='Shape Weapon Override',
                value=cfg.SHAPE_WEAPON_OVERRIDE,
                persistence=True,
                persistence_type=persist_type,
            ), xs=6, md=6),
            dbc.Col(dbc.Select(
                id='shape-weapon-dropdown',
                options=[{"label": key, "value": key} for key in WEAPON_PROPERTIES.keys()],
                value=cfg.SHAPE_WEAPON,  # default value
                persistence=True,
                persistence_type=persist_type,
                style={'display': 'none'},
            ), xs=6, md=6),
        ], class_name='switcher'),
    ], xs=12, md=6, class_name='col-left')
