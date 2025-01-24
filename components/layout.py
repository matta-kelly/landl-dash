import dash_mantine_components as dmc
from components.date_filter import date_filter
from components.theme_toggle import darkModeToggle

# Define the AppShell layout
layout = dmc.AppShell(
    children=[
        dmc.AppShellHeader(
            dmc.Group(
                [
                    dmc.Title("L and L Sales Dashboard", order=2, style={"marginRight": "auto"}),  # Push title to the left
                    dmc.Text(
                        "Last Updated: 2025-01-24 @ 10:15AM PST",  # Manually set the last updated date
                        id="last-update",
                        size="sm",
                        style={"color": "black", "marginRight": "25px"},  # Styling for the text
                    ),
                    #darkModeToggle(),
                    #date_filter(),  # Place the date filter on the right
                    
                ],
                align="center",  # Vertically align elements
                justify="space-between",  # Spread elements to opposite ends
                style={"padding": "0 16px"},  # Add padding for cleaner appearance
            ),
            withBorder=True,
            style={"backgroundColor": "#f8f9fa"},  # Optional: Add a light background for the header
        ),
        dmc.AppShellNavbar(
            id="navbar",  # Dynamic navbar placeholder
            children=[
                #"Navbar Content Placeholder",
                *[dmc.Skeleton(height=28, mt="sm", animate=False) for _ in range(10)],
                
            ],
            p="md",
            withBorder=True,
        ),
        dmc.AppShellMain(
            dmc.Container(
                id="page-content",  # Dynamic page content placeholder
                #style={"padding": "16px"},
            ),
        ),
    ],
    header={"height": 60},  # Set header height
    padding="md",  # Use AppShell padding
    navbar={
        "width": {"base": 200, "sm": 250, "lg": 300},  # Responsive navbar width
        "breakpoint": "sm",  # Collapse navbar on small screens
        "collapsed": {"mobile": True},  # Default collapsed on mobile
    },
    id="appshell",  # Assign an ID for dynamic interaction
)