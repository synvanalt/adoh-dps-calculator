from dash import html
import dash_bootstrap_components as dbc


def build_reference_info_tab():
    return dbc.Tab(label='Reference Info', tab_id='reference', children=[
        dbc.Container([
            html.H5('Base Weapon Properties:', className='mt-4'),
            html.Pre(id='weapon-properties', className='border rounded p-3 bg-dark-subtle'),

            html.H5('Purple Weapon Properties:', className='mt-4'),
            html.Pre(id='purple-weapons', className='border rounded p-3 bg-dark-subtle'),

            html.H5('Target Immunities:', className='mt-4'),
            html.Pre(id='target-immunities', className='border rounded p-3 bg-dark-subtle'),
        ], fluid=True, className='border-bottom rounded-bottom border-start border-end p-4 mb-4')
    ])