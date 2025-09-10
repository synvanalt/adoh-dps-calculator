# Third-party imports
import dash
from dash import dcc, html, Input, Output, State, ctx, ALL
import dash_bootstrap_components as dbc

# Local imports
from simulator.config import Config
from components.navbar import build_navbar
from components.character_settings import build_character_settings
from components.additional_damage import build_additional_damage_panel
from components.simulation_settings import build_simulation_settings
from components.results_tab import build_results_tab
from components.reference_tab import build_reference_info_tab
from components.plots import build_plots_tab
import callbacks.ui_callbacks as cb_ui
import callbacks.core_callbacks as cb_core
import callbacks.plots_callbacks as cb_plots


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

    # Dark overlay with spinner during calculation
    html.Div(
        id='loading-overlay',
        children=dbc.Spinner(color='light', size='lg', type='border'),
        style={'display': 'none'}
    ),

    # Error modal to catch exceptions in risky calculation part
    dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("Oops, unexpected error..."), close_button=False),
            dbc.ModalBody(id='global-error-body'),
            dbc.ModalFooter(dbc.Button("Close", id='close-global-error', class_name='ms-auto')),
        ],
        id='global-error-modal',
        is_open=False,
        backdrop='static',
        style={"zIndex": 99999},
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
cb_ui.register_ui_callbacks(app, cfg)
cb_core.register_core_callbacks(app, cfg)
cb_plots.register_plots_callbacks(app)

if __name__ == '__main__':
    app.run(debug=True)
