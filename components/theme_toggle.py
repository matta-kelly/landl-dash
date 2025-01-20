from dash import html
import dash_mantine_components as dmc
from dash_iconify import DashIconify

def darkModeToggle():
    print("darkModeToggle function is being executed")  # Debug print
    return html.Div(
        dmc.Switch(
            offLabel=DashIconify(icon="radix-icons:moon", width=20),
            onLabel=DashIconify(icon="radix-icons:sun", width=20),
            size="xl",
            id="themeSwitch",
            style={"display": "flex", "paddingTop": "2px"},  # Updated style property
            persistence=True,
        ),
        id="themeSwitchHolder",
    )
