# components/theme_toggle.py
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from dash import Input, Output, State, callback

# Theme toggle component
theme_toggle = dmc.ActionIcon(
    [
        dmc.Paper(DashIconify(icon="radix-icons:sun", width=25), darkHidden=True),
        dmc.Paper(DashIconify(icon="radix-icons:moon", width=25), lightHidden=True),
    ],
    variant="transparent",
    color="yellow",
    id="theme-toggle",
    size="lg",
)

# Callback to toggle the theme
@callback(
    Output("mantine-provider", "forceColorScheme"),
    Input("theme-toggle", "n_clicks"),
    State("mantine-provider", "forceColorScheme"),
    prevent_initial_call=True,
)
def toggle_theme(n_clicks, current_theme):
    return "dark" if current_theme == "light" else "light"
