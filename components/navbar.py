import dash_bootstrap_components as dbc


def build_navbar():
    navbar = dbc.Navbar(
        dbc.Container(
            [
                dbc.NavbarBrand("ADOH DPS Calculator", className="ms-2"),
                dbc.Nav(
                    [
                        # dbc.NavItem(dbc.NavLink("Home", href="#")),
                        # dbc.NavItem(dbc.NavLink("About", href="#")),
                    ],
                    className="ms-auto",
                    navbar=True,
                ),
            ],
            fluid=True,
        ),
        color="primary",
        dark=True,
    )
    return navbar
