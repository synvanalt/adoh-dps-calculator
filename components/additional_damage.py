from dash import html
import dash_bootstrap_components as dbc
from typing import Literal


def build_additional_damage_rows(additional_damage_dict):
    persist_type: Literal["local", "session", "memory"] = "session"

    rows = []
    for key, val in additional_damage_dict.items():

        # Combine label into the Switch component so there is no separate html.Label element
        switch = dbc.Switch(
            id={'type': 'add-dmg-switch', 'name': key},
            label=key.replace('_', ' '),
            value=val[0],
            persistence=True,
            persistence_type=persist_type,
        )

        # Extract damage params from dict format
        # val[1] example: {'fire_fw': [1, 4, 10]}
        dmg_type_key, dmg_nums = next(iter(val[1].items()))

        # Prettifying the damage type names for better readability
        if dmg_type_key == 'fire_fw':
            dmg_type_name = 'Fire'
        elif dmg_type_key in ('sneak', 'death'):
            dmg_type_name = 'Physical'
        else:
            dmg_type_name = dmg_type_key.title() if dmg_type_key else ''

        # Different layout for Flame Weapon, dice damage, and flat damage
        if key == 'Flame_Weapon' or key == 'Darkfire':
            widgets = html.Div([
                dbc.Input(
                    id={'type': 'add-dmg-input1', 'name': key},
                    type='number',
                    value=dmg_nums[0],  # num dice
                    step=1,
                    persistence=True,
                    persistence_type=persist_type,
                    class_name='add-dmg-input',
                    style={'marginRight': '0.2em'},
                ),
                html.Span("d", style={'marginRight': '0.2em'}),
                dbc.Input(
                    id={'type': 'add-dmg-input2', 'name': key},
                    type='number',
                    value=dmg_nums[1],  # sides
                    step=1,
                    persistence=True,
                    persistence_type=persist_type,
                    class_name='add-dmg-input',
                ),
                html.Span("+", style={'marginLeft': '0.2em', 'marginRight': '0.2em'}),
                dbc.Input(
                    id={'type': 'add-dmg-input3', 'name': key},
                    type='number',
                    value=dmg_nums[2] if len(dmg_nums) > 2 else 0,  # flat
                    step=1,
                    persistence=True,
                    persistence_type=persist_type,
                    class_name='add-dmg-input',
                ),
                html.Span(f"{dmg_type_name}", style={'marginLeft': '0.5em'}),
            ], id={'type': 'add-dmg-row', 'name': key}, style={'display': 'none'})

        elif dmg_nums and dmg_nums[0] != 0:  # dice damage
            widgets = html.Div([
                dbc.Input(
                    id={'type': 'add-dmg-input1', 'name': key},
                    type='number',
                    value=dmg_nums[0],  # num dice
                    step=1,
                    persistence=True,
                    persistence_type=persist_type,
                    class_name='add-dmg-input',
                    style={'marginRight': '0.2em'},
                ),
                html.Span("d", style={'marginRight': '0.2em'}),
                dbc.Input(
                    id={'type': 'add-dmg-input2', 'name': key},
                    type='number',
                    value=dmg_nums[1],  # sides
                    step=1,
                    persistence=True,
                    persistence_type=persist_type,
                    class_name='add-dmg-input',
                ),
                html.Span(f"{dmg_type_name}", style={'marginLeft': '0.5em'}),
                dbc.Input(
                    id={'type': 'add-dmg-input3', 'name': key},
                    type='number',
                    value=dmg_nums[2] if len(dmg_nums) > 2 else 0,  # flat
                    step=1,
                    persistence=True,
                    persistence_type=persist_type,
                    class_name='add-dmg-input',
                    style={'display': 'none'},
                ),
            ], id={'type': 'add-dmg-row', 'name': key}, style={'display': 'none'})

        else:  # flat damage
            widgets = html.Div([
                dbc.Input(
                    id={'type': 'add-dmg-input1', 'name': key},
                    type='number',
                    value=dmg_nums[0] if dmg_nums is not None else 0,  # num dice (hidden)
                    step=1,
                    persistence=True,
                    persistence_type=persist_type,
                    class_name='add-dmg-input',
                    style={'display': 'none'},
                ),
                dbc.Input(
                    id={'type': 'add-dmg-input2', 'name': key},
                    type='number',
                    value=dmg_nums[1] if dmg_nums is not None else 0,  # sides / flat amount
                    step=1,
                    persistence=True,
                    persistence_type=persist_type,
                    class_name='add-dmg-input',
                    style={'width': '25%'},
                ),
                html.Span(f"{dmg_type_name.title()}", style={'marginLeft': '0.5em'}),
                dbc.Input(
                    id={'type': 'add-dmg-input3', 'name': key},
                    type='number',
                    value=dmg_nums[2] if (dmg_nums and len(dmg_nums) > 2) else 0,  # flat
                    step=1,
                    persistence=True,
                    persistence_type=persist_type,
                    class_name='add-dmg-input',
                    style={'display': 'none'},
                ),
            ], id={'type': 'add-dmg-row', 'name': key}, style={'display': 'none'})

        # Combined row: switch on left and widgets on right
        combined = dbc.Row([
            dbc.Col(switch, xs=6, md=6),
            dbc.Col(widgets, xs=6, md=6),
        ], class_name='switcher add-dmg-row')
        rows.append(combined)

    return rows


def build_additional_damage_panel(cfg):
    return dbc.Col([
        html.H4('Additional Damage', className='mb-4 add-dmg-header'),

        dbc.Row([
            dbc.Col(
                build_additional_damage_rows(cfg.ADDITIONAL_DAMAGE),
                xs=12, md=12,
            )
        ], className='border rounded p-3 mb-4'),
    ], xs=12, md=6, class_name='col-right')
