import dash
from dash import Input, Output, ALL, MATCH, State
from simulator.config import Config
from weapons_db import WEAPON_PROPERTIES, PURPLE_WEAPONS
import plotly.graph_objects as go
import plotly.express as px


# Fixed color palette for damage types (keys are normalized to lowercase base token)
DAMAGE_TYPE_PALETTE = {
    'physical':  '#D97706',  # rich orange
    'fire':      '#DC2626',  # deep red
    'cold':      '#0EA5E9',  # icy blue
    'acid':      '#10B981',  # emerald green
    'electrical':'#2563EB',  # electric blue
    'sonic':     '#F59E0B',  # amber
    'negative':  '#6B7280',  # dark gray
    'positive':  '#D1D5DB',  # light gray
    'pure':      '#E879F9',  # magenta
    'magical':   '#8B5CF6',  # violet
    'divine':    '#FACC15',  # golden yellow
    'sneak': '#D97706',
    'massive': '#D97706',
    'death': '#D97706',
}

FALLBACK_COLORS = px.colors.qualitative.Plotly

# Dark theme helper to match Bootstrap dark mode
def apply_dark_theme(fig):
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#f8f9fa'),
        legend=dict(bgcolor='rgba(0,0,0,0)'),
        margin=dict(l=40, r=20, t=40, b=40),
    )
    axis_style = dict(
        gridcolor='rgba(255,255,255,0.06)',
        zerolinecolor='rgba(255,255,255,0.06)',
        tickfont=dict(color='#f8f9fa'),
        title=dict(font=dict(color='#f8f9fa'))
    )
    fig.update_xaxes(**axis_style)
    fig.update_yaxes(**axis_style)
    return fig

cfg = Config()

# Callback: toggle additional damage inputs visibility
def register_toggle_additional_damage(app):
    @app.callback(
        Output({'type': 'add-dmg-row', 'name': MATCH}, 'style'),
        Input({'type': 'add-dmg-switch', 'name': MATCH}, 'value'),
    )
    def toggle_additional_damage(show):
        style = {'display': 'flex'} if show else {'display': 'none'}
        return style

# Callback to update reference information
def register_update_reference_info(app):
    @app.callback(
        [Output('weapon-properties', 'children'),
         Output('purple-weapons', 'children'),
         Output('target-immunities', 'children')],
        [Input('calculate-button', 'n_clicks'),
         Input('recalculate-button', 'n_clicks'),
         Input('weapon-dropdown', 'value'),
         Input('shape-weapon-switch', 'value'),
         Input('shape-weapon-dropdown', 'value'),
         Input('target-immunities-switch', 'value'),
         Input({'type': 'immunity-input', 'name': ALL}, 'value')],
    )
    def update_reference_info(_, __, selected_weapons, shape_weapon_override, shape_weapon, boss_immunities, immunity_values):
        if not selected_weapons:
            return "No weapon selected", str(cfg.TARGET_IMMUNITIES), "No weapon selected"

        # Format weapon properties for all selected weapons
        base_weapon_props = []
        for weapon in selected_weapons:
            base_weapon = weapon.split('_')[0]

            if shape_weapon_override:  # Override the weapon properties with the selected shape weapon
                base_weapon = shape_weapon
                override_msg = f" (overridden by '{base_weapon}')"
            else:
                override_msg = ""

            props = WEAPON_PROPERTIES.get(base_weapon, "Weapon not found")
            props_name = f"{weapon}{override_msg}:"
            props_dmg = f"{props['dmg'][0]}d{props['dmg'][1]}"
            props_dmg_type = f"{props['dmg'][2].title()}"
            props_crit = f"Crit: {props['threat']}-20/x{props['multiplier']}"
            props_size = f"Size: {props['size']}"
            base_weapon_props.append((props_name, props_dmg, props_dmg_type, props_crit, props_size))

        # Format purple weapon information for all selected weapons
        purple_weapon_props = []
        for weapon in selected_weapons:
            properties = PURPLE_WEAPONS.get(weapon, {})
            props_name = f"{weapon}:"
            props_dmg = []

            # properties is now a dict mapping dmg-type -> params
            for key, val in properties.items():
                if key == 'legendary' and isinstance(val, dict):
                    proc = val.get('proc')
                    proc_str = f"{int(proc * 100)}%" if isinstance(proc, (int, float)) else ("On-Crit" if proc == 'on_crit' else str(proc))
                    # handle effect key separately
                    for leg_key, leg_val in val.items():
                        if leg_key == 'proc':
                            continue
                        if leg_key == 'effect':
                            props_dmg.append(f"Legendary {proc_str}: {leg_val.replace('_', ' ').title()}")
                            continue
                        # leg_val expected to be [dice, sides] or [dice, sides, flat]
                        dice = leg_val[0]
                        sides = leg_val[1]
                        flat = leg_val[2] if len(leg_val) > 2 else None
                        if dice == 0 and flat:
                            props_dmg.append(f"{flat} {leg_key.title()} (Legendary {proc_str})")
                        elif dice > 0 and flat:
                            props_dmg.append(f"Legendary {proc_str}: {dice}d{sides}+{flat} {leg_key.title()}")
                        else:
                            props_dmg.append(f"Legendary {proc_str}: {dice}d{sides} {leg_key.title()}")

                else:
                    # val can be a list [dice, sides]/[dice, sides, flat] or dict (vs_race mapping)
                    if "vs_race" in key and isinstance(val, dict):
                        # vs_race entry; val is {actual_type: [dice, sides]}
                        for actual_type, nums in val.items():
                            dice = nums[0]
                            sides = nums[1]
                            flat = nums[2] if len(nums) > 2 else None
                            if dice == 0 and flat:
                                props_dmg.append(f"{flat} {actual_type.title()} (vs. race)")
                            elif dice > 0 and flat:
                                props_dmg.append(f"{dice}d{sides}+{flat} {actual_type.title()} (vs. race)")
                            else:
                                props_dmg.append(f"{dice}d{sides} {actual_type.title()} (vs. race)")
                    else:
                        dice = val[0]
                        sides = val[1]
                        flat = val[2] if len(val) > 2 else None
                        if dice == 0 and flat:
                            props_dmg.append(f"{flat} {key.title()}")
                        elif dice > 0 and flat:
                            props_dmg.append(f"{dice}d{sides}+{flat} {key.title()}")
                        else:
                            props_dmg.append(f"{dice}d{sides} {key.title()}")

            props_dmg = ", ".join(props_dmg)
            purple_weapon_props.append((props_name, str(props_dmg)))

        def prettify_text(text):
            """Helper function to align text in columns for better readability"""
            col_widths = [max(len(row[i]) for row in text) for i in range(len(text[0]))]    # find max column widths
            formatted_lines = []
            for row in text:
                line = "  ".join(row[i].ljust(col_widths[i]) for i in range(len(row)))
                formatted_lines.append(line)
            return "\n".join(formatted_lines)

        # Map immunity inputs back into a dictionary (normalize % -> fraction)
        cfg.TARGET_IMMUNITIES = {
            name: ((val or 0) / 100)        # (None or 0) → 0
            for name, val in zip(cfg.TARGET_IMMUNITIES.keys(), immunity_values)
        }

        imms_data = [f"{k.title()}: {int(v * 100)}%" for k, v in cfg.TARGET_IMMUNITIES.items()]
        imms_data = "\n".join(imms_data)

        return (
            prettify_text(base_weapon_props),
            prettify_text(purple_weapon_props),
            imms_data,
        )

# Callback to reset all settings to defaults
def register_reset_to_defaults(app):
    @app.callback(
        Output('config-store', 'data', allow_duplicate=True),
        Output('ab-input', 'value', allow_duplicate=True),
        Output('ab-capped-input', 'value', allow_duplicate=True),
        Output('ab-prog-dropdown', 'value', allow_duplicate=True),
        Output('toon-size-dropdown', 'value', allow_duplicate=True),
        Output('combat-type-dropdown', 'value', allow_duplicate=True),
        Output('mighty-input', 'value', allow_duplicate=True),
        Output('enhancement-bonus-input', 'value', allow_duplicate=True),
        Output('str-mod-input', 'value', allow_duplicate=True),
        Output({'type': 'melee-switch', 'name': 'two-handed'}, 'value', allow_duplicate=True),
        Output({'type': 'melee-switch', 'name': 'weaponmaster'}, 'value', allow_duplicate=True),
        Output('keen-switch', 'value', allow_duplicate=True),
        Output('improved-crit-switch', 'value', allow_duplicate=True),
        Output('shape-weapon-switch', 'value', allow_duplicate=True),
        Output('shape-weapon-dropdown', 'value', allow_duplicate=True),
        Output({'type': 'add-dmg-switch', 'name': ALL}, 'value', allow_duplicate=True),
        Output({'type': 'add-dmg-input1', 'name': ALL}, 'value', allow_duplicate=True),
        Output({'type': 'add-dmg-input2', 'name': ALL}, 'value', allow_duplicate=True),
        Output({'type': 'add-dmg-input3', 'name': ALL}, 'value', allow_duplicate=True),
        Output('weapon-dropdown', 'value', allow_duplicate=True),
        Output('target-ac-input', 'value', allow_duplicate=True),
        Output('rounds-input', 'value', allow_duplicate=True),
        Output('damage-limit-switch', 'value', allow_duplicate=True),
        Output('damage-limit-input', 'value', allow_duplicate=True),
        Output('dmg-vs-race-switch', 'value', allow_duplicate=True),
        Output('relative-change-input', 'value', allow_duplicate=True),
        Output('relative-std-input', 'value', allow_duplicate=True),
        Output('target-immunities-switch', 'value', allow_duplicate=True),
        Output({'type': 'immunity-input', 'name': ALL}, 'value', allow_duplicate=True),
        Output('immunities-store', 'data', allow_duplicate=True),
        Output('reset-toast', 'is_open', allow_duplicate=True),
        Input('reset-button', 'n_clicks'),
        State('immunities-store', 'data'),
        prevent_initial_call=True
    )
    def reset_to_defaults(n_clicks, immunities_store):
        if n_clicks:
            default_cfg = Config()

            reset_immunities_store = {
                name: (val or 0)  # Convert percentages back to fractions
                for name, val in default_cfg.TARGET_IMMUNITIES.items()
            }

            return (
                default_cfg.__dict__,
                default_cfg.AB,
                default_cfg.AB_CAPPED,
                default_cfg.AB_PROG,
                default_cfg.TOON_SIZE,
                default_cfg.COMBAT_TYPE,
                default_cfg.MIGHTY,
                default_cfg.ENHANCEMENT_BONUS,
                default_cfg.STR_MOD,
                default_cfg.TWO_HANDED,
                default_cfg.WEAPONMASTER,
                default_cfg.KEEN,
                default_cfg.IMPROVED_CRIT,
                default_cfg.SHAPE_WEAPON_OVERRIDE,
                default_cfg.SHAPE_WEAPON,
                [val[0] for val in default_cfg.ADDITIONAL_DAMAGE.values()],
                [next(iter(val[1].values()))[0] for val in default_cfg.ADDITIONAL_DAMAGE.values()],
                [next(iter(val[1].values()))[1] for val in default_cfg.ADDITIONAL_DAMAGE.values()],
                [next(iter(val[1].values()))[2] for val in default_cfg.ADDITIONAL_DAMAGE.values()],
                default_cfg.DEFAULT_WEAPONS,
                default_cfg.TARGET_AC,
                default_cfg.ROUNDS,
                default_cfg.DAMAGE_LIMIT_FLAG,
                default_cfg.DAMAGE_LIMIT,
                default_cfg.DAMAGE_VS_RACE,
                default_cfg.CHANGE_THRESHOLD * 100,  # convert to percentage
                default_cfg.STD_THRESHOLD * 100,     # convert to percentage
                default_cfg.TARGET_IMMUNITIES_FLAG,
                [val * 100 for val in default_cfg.TARGET_IMMUNITIES.values()],
                reset_immunities_store,
                True  # Open the toast
            )
        return dash.no_update


def register_plot_callbacks(app):
    # Populate weapon dropdown with available weapons from the simulation results
    @app.callback(
        Output('plots-weapon-dropdown', 'options'),
        Output('plots-weapon-dropdown', 'value'),
        Input('intermediate-value', 'data'),
    )
    def populate_weapon_dropdown(results_dict):
        if not results_dict:
            return [], None
        weapons = list(results_dict.keys())
        options = [{'label': w, 'value': w} for w in weapons]
        # default to first weapon
        return options, weapons[0]

    # DPS Comparison bar chart
    @app.callback(
        Output('plots-dps-comparison', 'figure'),
        Input('intermediate-value', 'data')
    )
    def update_dps_comparison_figure(results_dict):
        fig = go.Figure()
        if not results_dict:
            fig.update_layout(title='No simulation data')
            apply_dark_theme(fig)
            return fig

        weapons = []
        dps_crits = []
        dps_no_crits = []
        dps_avg = []

        for weapon, results in results_dict.items():
            weapons.append(weapon)
            dps_crits.append(results['dps_crits'])
            dps_no_crits.append(results['dps_no_crits'])
            dps_avg.append(results['avg_dps_both'])

        # Create grouped bar chart
        fig.add_trace(go.Bar(name='Crits Allowed', x=weapons, y=dps_crits))
        fig.add_trace(go.Bar(name='Crits Immune', x=weapons, y=dps_no_crits))
        fig.add_trace(go.Bar(name='Average DPS', x=weapons, y=dps_avg))

        # Update layout for better readability
        fig.update_layout(
            barmode='group',
            xaxis_title='Weapons',
            yaxis_title='DPS',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        apply_dark_theme(fig)
        return fig

    # Per-weapon plots: DPS vs damage and damage breakdown pie
    @app.callback(
        Output('plots-weapon-dps-vs-damage', 'figure'),
        Output('plots-weapon-breakdown', 'figure'),
        Input('plots-weapon-dropdown', 'value'),
        State('intermediate-value', 'data')
    )
    def update_weapon_plots(selected_weapon, results_dict):
        empty_fig = go.Figure()
        empty_fig.update_layout(title='No simulation data')
        apply_dark_theme(empty_fig)

        if not results_dict or not selected_weapon or selected_weapon not in results_dict:
            return empty_fig, empty_fig

        results = results_dict[selected_weapon]

        # DPS vs Cumulative Damage: use cumulative damage (x) vs rolling avg DPS (x)
        dps_vals = results.get('dps_rolling_avg') or results.get('dps_per_round') or []
        cum_damage = results.get('cumulative_damage_per_round') or []
        fig1 = go.Figure()
        if dps_vals and cum_damage:
            n = min(len(dps_vals), len(cum_damage))
            # X = cumulative damage, Y = DPS
            fig1.add_trace(go.Scatter(x=cum_damage[:n], y=dps_vals[:n], mode='lines+markers', marker=dict(opacity=0.9)))
            fig1.update_layout(title=f'', xaxis_title='Cumulative Damage', yaxis_title='Mean DPS')
        else:
            fig1.update_layout(title='Insufficient data for DPS vs Damage')
        apply_dark_theme(fig1)

        # Damage breakdown pie
        dmg_by_type = results.get('damage_by_type') or {}
        if dmg_by_type:
            labels = [k.split('_')[0].title() for k in dmg_by_type.keys()]
            values = [v for v in dmg_by_type.values()]
            colors = []
            for lab in labels:
                key = lab.lower()
                col = DAMAGE_TYPE_PALETTE.get(key)
                if not col:
                    col = FALLBACK_COLORS[abs(hash(lab)) % len(FALLBACK_COLORS)]
                colors.append(col)

            fig2 = px.pie(names=labels, values=values, title=f'')
            fig2.update_traces(textinfo='percent+label', textfont=dict(color='#f8f9fa'), marker=dict(colors=colors, line=dict(color='rgba(255,255,255,0.06)', width=1)))
        else:
            fig2 = go.Figure()
            fig2.update_layout(title='No damage breakdown available')
        apply_dark_theme(fig2)

        return fig1, fig2
