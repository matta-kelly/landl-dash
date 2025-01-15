import dash_bootstrap_components as dbc
from dash import html

# Sidebar component
def create_sidebar():
    return dbc.Nav(
        [
            # Home Tab
            dbc.NavLink("Home", href="/", active="exact"),

            # Wholesale Section
            dbc.NavLink("Wholesale", href="/wholesale", active="exact"),
            dbc.Nav(
                [
                    dbc.NavLink("Home", href="/wholesale/home", active="exact"),
                    dbc.NavLink("Shipping / Fulfillment", href="/wholesale/shipping", active="exact"),
                    dbc.NavLink("Rep View", href="/wholesale/rep", active="exact"),
                    dbc.NavLink("Customer Evaluation", href="/wholesale/customer", active="exact"),
                    dbc.Nav(
                        [
                            dbc.NavLink("Home", href="/wholesale/surf-expo/home", active="exact"),
                            dbc.NavLink("Shipping / Fulfillment", href="/wholesale/surf-expo/shipping", active="exact"),
                            dbc.NavLink("Rep View", href="/wholesale/surf-expo/rep", active="exact"),
                            dbc.NavLink("Customer Evaluation", href="/wholesale/surf-expo/customer", active="exact"),
                        ],
                        navbar=True,
                    ),
                ],
                navbar=True,
            ),

            # Ecom Section
            dbc.NavLink("Ecom", href="/ecom", active="exact"),
        ],
        vertical=True,
        pills=True,
        style={"height": "100vh", "padding": "10px"},
    )
