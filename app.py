# Standard library imports
from dataclasses import asdict

# Third-party imports
import dash
from dash import dcc, html, Input, Output, State, ctx, ALL
import dash_bootstrap_components as dbc
import pandas as pd

# Local imports
from simulator.damage_simulator import DamageSimulator
from simulator.config import Config
from components.navbar import build_navbar
from components.character_settings import build_character_settings
from components.additional_damage import build_additional_damage_panel
from components.simulation_settings import build_simulation_settings
from components.results_tab import build_results_tab
from components.reference_tab import build_reference_info_tab
from components.plots import build_plots_tab
import components.callbacks as callbacks


# Create a Config instance
cfg = Config()

# Initialize the Dash app with Bootstrap theme
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc_css])
server = app.server   # <-- important for Render


# Force mobile viewport scaling and Bootstrap dark mode
app.index_string = """
<!DOCTYPE html>
<html lang="en" data-bs-theme="dark">
    <head>
        {%metas%}
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>ADOH DPS Calculator</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
"""


# Update app layout to use modularized components
app.layout = dbc.Container([
    dcc.Store(id='config-store', storage_type='session'),
    dcc.Store(id='intermediate-value'),  # Store for calculation results
    dcc.Store(id='is-calculating', data=False),  # Store for tracking calculation state
    dcc.Store(id='immunities-store', data=cfg.TARGET_IMMUNITIES, storage_type='session'),  # keeps user edits

    # Navbar
    html.Div(build_navbar()),

    # Dark overlay with spinner
    html.Div(
        id='loading-overlay',
        children=dbc.Spinner(color='light', size='lg', type='border'),
        style={'display': 'none'}
    ),

    dbc.Container([
        dbc.Tabs(id='tabs', active_tab='configuration', children=[
            # Tab 1: Configuration
            dbc.Tab(label='Configuration', tab_id='configuration', children=[
                dbc.Container([
                    # Configuration Parameters
                    dbc.Row([
                        # Character settings
                        build_character_settings(cfg),

                        # Additional damage
                        build_additional_damage_panel(cfg),
                    ], class_name='mb-4', style={'display': 'flex', 'alignItems': 'flex-start'}),

                    html.Hr(),

                    # Simulation settings
                    dbc.Row([
                        build_simulation_settings(cfg)
                    ], class_name='mb-0', style={'display': 'flex', 'alignItems': 'flex-start'})
                ], fluid=True, class_name='border-bottom rounded-bottom border-start border-end p-5 mb-4'),
            ]),

            # Tab 2: Results
            build_results_tab(),

            # Tab 3: Plots
            build_plots_tab(),

            # Tab 4: Reference Information
            build_reference_info_tab(),

        ], style={'padding': '20px 0px 0px 0px'}),
    ], fluid=True, style={
        'maxWidth': '1200px',
        'margin': 'auto',
        'padding': '0px 0px 0px 0px'
    }),
], fluid=True, style={
    'margin': 'auto',
    'padding': '0px 0px 0px 0px'
})


# Register callbacks
callbacks.register_toggle_additional_damage(app)
callbacks.register_update_reference_info(app)
callbacks.register_reset_to_defaults(app)   # Register the reset-to-defaults callback
callbacks.register_plot_callbacks(app)


# Callback to disable inputs and show spinner when calculation starts
@app.callback(
     Output('loading-overlay', 'style', allow_duplicate=True),
    [Input('calculate-button', 'n_clicks'),
     Input('recalculate-button', 'n_clicks')],
    prevent_initial_call=True
)
def toggle_overlay(n_clicks_calc, n_clicks_recalc):
    if n_clicks_calc or n_clicks_recalc:
        # Show overlay
        return {
            "position": "fixed",
            "top": 0,
            "left": 0,
            "width": "100%",
            "height": "100%",
            "backgroundColor": "rgba(0, 0, 0, 0.5)",
            "display": "flex",  # flex to center spinner
            "justifyContent": "center",
            "alignItems": "center",
            "zIndex": 9999,
        }
    else:
        # Hide overlay
        return {"display": "none"}


# Callback to run calculation
@app.callback(
    Output('is-calculating', 'data'),
    Output('intermediate-value', 'data'),
    Output('config-store', 'data'),
    Input('loading-overlay', 'style'),
    State('config-store', 'data'),
    State('ab-input', 'value'),
    State('ab-capped-input', 'value'),
    State('ab-prog-dropdown', 'value'),
    State('toon-size-dropdown', 'value'),
    State('combat-type-dropdown', 'value'),
    State('mighty-input', 'value'),
    State('enhancement-bonus-input', 'value'),
    State('str-mod-input', 'value'),
    State({'type': 'melee-switch', 'name': 'two-handed'}, 'value'),
    State({'type': 'melee-switch', 'name': 'weaponmaster'}, 'value'),
    State('keen-switch', 'value'),
    State('improved-crit-switch', 'value'),
    State('shape-weapon-switch', 'value'),
    State('shape-weapon-dropdown', 'value'),
    State({'type': 'add-dmg-switch', 'name': ALL}, 'value'),
    State({'type': 'add-dmg-input1', 'name': ALL}, 'value'),
    State({'type': 'add-dmg-input2', 'name': ALL}, 'value'),
    State({'type': 'add-dmg-input3', 'name': ALL}, 'value'),
    State('weapon-dropdown', 'value'),
    State('target-ac-input', 'value'),
    State('rounds-input', 'value'),
    State('damage-limit-switch', 'value'),
    State('damage-limit-input', 'value'),
    State('dmg-vs-race-switch', 'value'),
    State('relative-change-input', 'value'),
    State('relative-std-input', 'value'),
    State('target-immunities-switch', 'value'),
    State({'type': 'immunity-input', 'name': ALL}, 'value'),
    prevent_initial_call=True
)
def run_calculation(spinner, current_cfg, ab, ab_capped, ab_prog, toon_size, combat_type, mighty, enhancement_bonus,
                    str_mod, two_handed, weaponmaster, keen, improved_crit, shape_weapon_override, shape_weapon,
                    add_dmg_state, add_dmg1, add_dmg2, add_dmg3,
                    weapons, target_ac, rounds, dmg_limit_flag, dmg_limit, dmg_vs_race,
                    relative_change, relative_std, immunity_flag, immunity_values):

    # if not ctx.triggered_id or not weapons:
    if spinner['display'] == 'none' or not weapons:
        return False, dash.no_update, current_cfg

    # if ctx.triggered_id == 'calculate-button' or ctx.triggered_id == 'recalculate-button':
    if spinner['display'] == 'flex':
        print("Starting simulation...")
        # Start calculation
        if current_cfg is None:
            # fallback
            current_cfg = asdict(cfg)
            print('current_cfg was None and is initialized')

        # build config dict instead of mutating globals
        current_cfg['AB'] = ab
        current_cfg['AB_CAPPED'] = ab_capped
        current_cfg['AB_PROG'] = ab_prog
        current_cfg['TOON_SIZE'] = toon_size
        current_cfg['COMBAT_TYPE'] = combat_type
        current_cfg['MIGHTY'] = mighty
        current_cfg['ENHANCEMENT_BONUS'] = enhancement_bonus
        current_cfg['STR_MOD'] = str_mod
        current_cfg['TWO_HANDED'] = two_handed
        current_cfg['WEAPONMASTER'] = weaponmaster
        current_cfg['KEEN'] = keen
        current_cfg['IMPROVED_CRIT'] = improved_crit
        current_cfg['SHAPE_WEAPON_OVERRIDE'] = shape_weapon_override
        current_cfg['SHAPE_WEAPON'] = shape_weapon
        current_cfg['TARGET_AC'] = target_ac
        current_cfg['ROUNDS'] = rounds
        current_cfg['DAMAGE_LIMIT_FLAG'] = dmg_limit_flag
        current_cfg['DAMAGE_LIMIT'] = dmg_limit
        current_cfg['DAMAGE_VS_RACE'] = dmg_vs_race
        current_cfg['CHANGE_THRESHOLD'] = relative_change / 100     # convert to fraction
        current_cfg['STD_THRESHOLD'] = relative_std / 100           # convert to fraction
        current_cfg['TARGET_IMMUNITIES_FLAG'] = immunity_flag

        # Map immunity inputs back into a dictionary (normalize % -> fraction)
        current_cfg['TARGET_IMMUNITIES'] = {
            name: val / 100
            for name, val in zip(cfg.TARGET_IMMUNITIES.keys(), immunity_values)
        }

        # Update additional damage sources
        current_cfg['ADDITIONAL_DAMAGE'] = {
            key: [add_dmg_state[idx], {next(iter(val[1].keys())): [add_dmg1[idx], add_dmg2[idx], add_dmg3[idx]]}]
            for idx, (key, val) in enumerate(cfg.ADDITIONAL_DAMAGE.items())
        }

        # Calculate DPS for all selected weapons
        results_dict = {}
        user_cfg = Config(**current_cfg)    # convert dict back to Config object
        for weapon in weapons:
            # print(f'Running simulation for {weapon} with config:\n{user_cfg.__repr__()}\n')
            calculator = DamageSimulator(weapon, user_cfg)
            results_dict[weapon] = calculator.simulate_dps()

        return False, results_dict, current_cfg

    return False, dash.no_update, current_cfg


# Callback to update results based on stored calculation results
@app.callback(
    [Output('comparative-table', 'children'),
     Output('detailed-results', 'children')],
    [Input('intermediate-value', 'data')]
)
def update_results(results_dict):
    if not results_dict:
        return "Run simulation to see results...", ""

    detailed_results = []
    for weapon, results in results_dict.items():
        detailed_weapon_results = dbc.Card([
            dbc.CardHeader(html.H5(weapon, className='mb-0')),
            dbc.CardBody([
                # Attack Stats, Hit and Crit rates per attack
                dbc.Row([
                    dbc.Col([
                        html.H6('Summary', className='mb-3'),
                        html.Pre(results["summary"], className='border rounded p-3 bg-dark-subtle', style={'overflow-x': 'auto'}),
                    ], class_name='mb-4'),
                ]),
                dbc.Row([
                    # Attack Statistics - full width on mobile, 4 cols on desktop
                    dbc.Col([
                        html.H6('Attack Statistics', className='mb-3'),
                        html.Div([
                            dbc.Table([
                                html.Thead([html.Tr([html.Th('Statistic'), html.Th('Actual'), html.Th('Theoretical')])]),
                                html.Tbody([
                                    html.Tr([html.Td('Hit Rate'),
                                             html.Td(f'{results["hit_rate_actual"]:.1f}%'),
                                             html.Td(f'{results["hit_rate_theoretical"]:.1f}%')]),
                                    html.Tr([html.Td('Crit Rate'),
                                             html.Td(f'{results["crit_rate_actual"]:.1f}%'),
                                             html.Td(f'{results["crit_rate_theoretical"]:.1f}%')]),
                                    html.Tr([html.Td('Legend Proc Rate'),
                                             html.Td(f'{results["legend_proc_rate_actual"]:.1f}%'),
                                             html.Td(f'{results["legend_proc_rate_theoretical"]:.1f}%')]),
                                ])
                            ], bordered=True, hover=True, striped=True, size='sm', class_name='table-responsive')
                        ], style={'overflow-x': 'auto'})
                    ], xs=12, md=4, class_name='mb-4'),

                    # Hit Rate per Attack - full width on mobile, 4 cols on desktop
                    dbc.Col([
                        html.H6('Hit Rate per Attack', className='mb-3'),
                        html.Div([
                            dbc.Table([
                                html.Thead([html.Tr([html.Th('Attack #'), html.Th('Actual %'), html.Th('Theoretical %')])]),
                                html.Tbody([
                                    html.Tr([
                                        html.Td(f'Attack {i + 1}'),
                                        html.Td(f'{results["hits_per_attack"][i]:.1f}%'),
                                        html.Td(f'{results["hit_rate_per_attack_theoretical"][i]:.1f}%')
                                    ]) for i in range(len(results["hits_per_attack"]))
                                ])
                            ], bordered=True, hover=True, striped=True, size='sm', class_name='table-responsive')
                        ], style={'overflow-x': 'auto'})
                    ], xs=12, md=4, class_name='mb-4'),

                    # Crit Rate per Attack - full width on mobile, 4 cols on desktop
                    dbc.Col([
                        html.H6('Crit Rate per Attack', className='mb-3'),
                        html.Div([
                            dbc.Table([
                                html.Thead([html.Tr([html.Th('Attack #'), html.Th('Actual %'), html.Th('Theoretical %')])]),
                                html.Tbody([
                                    html.Tr([
                                        html.Td(f'Attack {i + 1}'),
                                        html.Td(f'{results["crits_per_attack"][i]:.1f}%'),
                                        html.Td(f'{results["crit_rate_per_attack_theoretical"][i]:.1f}%')
                                    ]) for i in range(len(results["crits_per_attack"]))
                                ])
                            ], bordered=True, hover=True, striped=True, size='sm', class_name='table-responsive')
                        ], style={'overflow-x': 'auto'})
                    ], xs=12, md=4, class_name='mb-4')
                ], class_name='gx-4', style={'alignItems': 'flex-start'})  # Add horizontal spacing between columns
            ])
        ], class_name='mb-4')
        detailed_results.append(detailed_weapon_results)

    # Create comparative table - made responsive
    comparative_df = pd.DataFrame({
        weapon: {
            'Weapon': weapon,
            'Avg DPS (50/50)': results["avg_dps_both"],
            'DPS (Crit Allowed)': results["dps_crits"],
            'DPS (Crit Immune)': results["dps_no_crits"],
            'Hit %': results["hit_rate_actual"],
            'Crit %': results["crit_rate_actual"],
            'Legend Proc %': results["legend_proc_rate_actual"],
        }
        for weapon, results in results_dict.items()
    }).transpose()

    comparative_df = comparative_df.reset_index(drop=True).sort_values('Avg DPS (50/50)', ascending=False)

    # Wrap table in a responsive div
    comparative_table = html.Div([
        dbc.Table.from_dataframe(       # type: ignore[attr-defined]
            comparative_df.round(2),
            bordered=True,
            hover=True,
            striped=True,
            class_name='table-responsive mb-4',
        )
    ], style={'overflow-x': 'auto'})

    return comparative_table, html.Div(detailed_results)


# Callback to update tabs
@app.callback(
    Output('tabs', 'active_tab'),
    [Input('intermediate-value', 'data')]
)
def switch_to_results(results):
    if results:
        return 'results'
    return dash.no_update


# Callback to re-enable inputs after calculation
@app.callback(
Output('loading-overlay', 'style', allow_duplicate=True),
    [Input('intermediate-value', 'data')],
    prevent_initial_call=True
)
def toggle_overlay(results):
    if results:
        # Hide overlay
        return {"display": "none"}
    else:
        # Show overlay
        return {
            "position": "fixed",
            "top": 0,
            "left": 0,
            "width": "100%",
            "height": "100%",
            "backgroundColor": "rgba(0, 0, 0, 0.5)",
            "display": "flex",  # flex to center spinner
            "justifyContent": "center",
            "alignItems": "center",
            "zIndex": 9999,
        }

# Callback to toggle target immunities inputs
@app.callback(
    Output({'type': 'immunity-input', 'name': ALL}, 'value'),
    Output('immunities-store', 'data'),
    Input('target-immunities-switch', 'value'),
    State('config-store', 'data'),
    State('immunities-store', 'data'),
    State({'type': 'immunity-input', 'name': ALL}, 'value'),
    prevent_initial_call=True
)
def toggle_immunities(apply_immunities, cfg_store, immunities_store, current_input_values):
    names = list(cfg.TARGET_IMMUNITIES.keys())
    n = len(names)

    # Ensure store dict exists
    immunities_store = immunities_store or {}

    if apply_immunities:
        # Prefer the most recent user values saved in immunities-store
        if any(name in immunities_store for name in names):
            return [round(immunities_store.get(name, 0) * 100) for name in names], immunities_store

        # Fallback to config-store values (fractions -> percentages)
        if cfg_store and "TARGET_IMMUNITIES" in cfg_store:
            return [round(cfg_store["TARGET_IMMUNITIES"].get(name, 0) * 100) for name in names], immunities_store

        # Final fallback: zeros
        return [0] * n, immunities_store

    else:
        # Switch off → save current values to immunities-store before setting to 0
        updated_store = {
            name: (val or 0) / 100  # Convert percentages back to fractions
            for name, val in zip(names, current_input_values)
        }
        return [0] * n, updated_store


# Callback: toggle melee/ranged dependent params OFF and disabled
@app.callback(
    # Output({'type': 'melee-row', 'name': ALL}, 'style'),
    Output({'type': 'melee-switch', 'name': ALL}, 'value'),
    Output('mighty-input', 'value'),
    Output({'type': 'melee-switch', 'name': ALL}, 'disabled', allow_duplicate=True),
    Output('mighty-input', 'disabled', allow_duplicate=True),
    Input('combat-type-dropdown', 'value'),
    prevent_initial_call='initial_duplicate'
)
def toggle_melee_params(combat_type):
    n = len(ctx.outputs_list[0])  # number of matching melee rows

    if combat_type == 'ranged':
        return (
            [False] * n,                  # Turn OFF all melee switches
            20,                           # Set mighty to 20
            [True] * n,                   # Disable all melee switches
            False                         # Enable mighty input
        )

    elif combat_type == 'melee':
        return (
            [dash.no_update] * n,         # Don't update the melee switches
            0,                            # Set mighty to 0
            [False] * n,                  # Enable all melee switches
            True                          # Disable mighty input
        )

    else:
        return dash.no_update


# Callback: toggle shape weapon visibility
@app.callback(
    Output('shape-weapon-dropdown', 'style'),
    Input('shape-weapon-switch', 'value'),
)
def toggle_shape_weapon(show):
    style = {'display': 'flex'} if show else {'display': 'none'}
    return style


# Callback: toggle damage limit visibility
@app.callback(
    Output('damage-limit-input', 'style'),
    Input('damage-limit-switch', 'value'),
)
def toggle_damage_limit(show):
    style = {'display': 'flex'} if show else {'display': 'none'}
    return style


# Callback to update config-store when inputs change
@app.callback(
    Output('config-store', 'data', allow_duplicate=True),
    Input({'type': 'immunity-input', 'name': ALL}, 'value'),
    State('config-store', 'data'),
    State('target-immunities-switch', 'value'),
    prevent_initial_call=True
)
def update_store_from_inputs(values, cfg_data, switch_on):
    names = list(cfg.TARGET_IMMUNITIES.keys())
    cfg_data = cfg_data or {}

    # Build a list of current store values for comparison
    stored_values = [round(cfg_data.get("TARGET_IMMUNITIES", {}).get(name, 0) * 100) for name in names]

    # Only update store if user manually changed an input while switch is ON
    if not switch_on or values == stored_values:
        return dash.no_update

    cfg_data["TARGET_IMMUNITIES"] = {
        name: (val or 0) / 100 for name, val in zip(names, values)
    }
    return cfg_data


if __name__ == '__main__':
    app.run(debug=True)
