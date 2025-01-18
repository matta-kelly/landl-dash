import dash_mantine_components as dmc
from dash import html, Input, Output, State, callback
from dash_iconify import DashIconify

def sidebarNav(pathname, title="Menu", border=True, collapse=True):
    """
    Generates a collapsible sidebar navigation based on the provided pathname.

    Args:
        pathname (str): The current URL pathname to generate dynamic links.
        title (str): The title for the mobile navbar.
        border (bool): Whether to include a border.
        collapse (bool): Whether the sidebar should be collapsible.

    Returns:
        html.Div: The sidebar navigation component.
    """
    from components.navbar_links import generate_navbar  # Import your dynamic navbar generator
    nav_links = generate_navbar(pathname)  # Generate navbar links dynamically

    navStyle = {"margin": "0", "position": "sticky"}
    navClass = ""
    if border:
        navStyle["borderRight"] = "1pt solid black"

    navStyle = {**navStyle, "flexDirection": "column", "height": "100vh"}
    if collapse:
        navClass = "collapsible"

    # Add pin button and mobile navbar support
    nav = html.Div(
        [
            # Desktop Navbar
            dmc.MediaQuery(
                dmc.Navbar(
                    children=[
                        dmc.Avatar(style={"display": "block", "width": "100%"}),
                        *nav_links,  # Insert dynamically generated links
                    ],
                    style=navStyle,
                    id="navbar",
                    className=navClass,
                ),
                smallerThan="601",
                styles={"display": "none"},
            ),
            # Mobile Navbar
            dmc.MediaQuery(
                html.Div(
                    dmc.Grid(
                        [
                            dmc.Col(
                                title,
                                style={
                                    "display": "flex",
                                    "justifyContent": "center",
                                    "alignItems": "center",
                                },
                                span=10,
                                offset=1,
                            ),
                            dmc.Col([html.Div(className="fa-solid fa-bars")], span=1),
                        ],
                        style={"width": "100vw", "margin": 0},
                    ),
                    id="mobileNav",
                    style={"position": "sticky"},
                ),
                largerThan="601",
                styles={"display": "none"},
            ),
            # Mobile Drawer
            dmc.Drawer(
                children=[
                    dmc.Avatar(style={"display": "block", "width": "100%"}),
                    *nav_links,  # Insert dynamically generated links
                ],
                title=title,
                id="mobileMenu",
                size="full",
                position="top",
            ),
        ]
    )
    return nav
