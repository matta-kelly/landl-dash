from dash import html
import dash_mantine_components as dmc
from dash_iconify import DashIconify

def darkModeToggle():
    return html.Div(
        dmc.Switch(
            offLabel=DashIconify(icon="radix-icons:moon", width=20),
            onLabel=DashIconify(icon="radix-icons:sun", width=20),
            size="xl",
            id="themeSwitch",
            sx={"display": "flex", "paddingTop": "2px"},
            persistence=True,
        ),
        id="themeSwitchHolder",
    )
