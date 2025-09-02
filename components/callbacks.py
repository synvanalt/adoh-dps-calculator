import dash
from dash import Input, Output, ALL, MATCH, State
from simulator.config import Config
from weapons_db import WEAPON_PROPERTIES, PURPLE_WEAPONS


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
            properties = PURPLE_WEAPONS.get(weapon, "Weapon not found")
            props_name = f"{weapon}:"
            props_dmg = []
            for dmg in properties:
                if 'legendary' in dmg[2].lower():
                    legend_proc_type = f"{int(dmg[4] * 100)}%" if type(dmg[4]) in [float, int] else "On-Crit"
                    if 'effect' in dmg[3].lower():
                        props_dmg.append(f"Legendary {legend_proc_type}: {dmg[3].replace('_', ' ').title()}")
                    else:
                        props_dmg.append(f"Legendary {legend_proc_type}: {dmg[0]}d{dmg[1]} {dmg[3].title()}")
                elif dmg[0] == 0:   # Not dice, just flat damage
                    props_dmg.append(f"{dmg[1]} {dmg[2].title()}")
                else:
                    props_dmg.append(f"{dmg[0]}d{dmg[1]} {dmg[2].title()}")
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
                [val[1][0] for val in default_cfg.ADDITIONAL_DAMAGE.values()],
                [val[1][1] for val in default_cfg.ADDITIONAL_DAMAGE.values()],
                [val[1][3] for val in default_cfg.ADDITIONAL_DAMAGE.values()],
                default_cfg.DEFAULT_WEAPONS,
                default_cfg.TARGET_AC,
                default_cfg.ROUNDS,
                default_cfg.DAMAGE_LIMIT_FLAG,
                default_cfg.DAMAGE_LIMIT,
                default_cfg.DAMAGE_VS_RACE,
                default_cfg.TARGET_IMMUNITIES_FLAG,
                [val * 100 for val in default_cfg.TARGET_IMMUNITIES.values()],
                reset_immunities_store,
                True  # Open the toast
            )
        return dash.no_update
