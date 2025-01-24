import dash_mantine_components as dmc
from components.date_filter import date_filter
from components.theme_toggle import darkModeToggle

# Define the AppShell layout
layout = dmc.AppShell(
    children=[
        # Header Section
        dmc.AppShellHeader(
            dmc.Group(
                [
                    # Title aligned to the left
                    dmc.Title("L and L Sales Dashboard", order=2, style={"marginRight": "auto"}),

                    # Last updated text aligned to the right
                    dmc.Text(
                        "Last Updated: 2025-01-24 @ 12:30PM PST",  # Example last updated date
                        id="last-update",
                        size="sm",
                        style={"color": "black", "marginRight": "25px"},
                    ),

                    # Dark mode toggle and date filter can be uncommented when needed
                    # darkModeToggle(),
                    # date_filter(),
                ],
                align="center",  # Vertically align elements
                justify="space-between",  # Spread elements to opposite ends
                style={"padding": "0 16px"},  # Add padding for cleaner appearance
            ),
            withBorder=True,
            style={"backgroundColor": "#f8f9fa"},  # Optional: Add a light background for the header
        ),

        # Navbar Section
        dmc.AppShellNavbar(
            id="navbar",  # Dynamic navbar placeholder
            children=[
                *[dmc.Skeleton(height=28, mt="sm", animate=False) for _ in range(10)],  # Placeholder for loading state
            ],
            p="md",
            withBorder=True,
        ),

        # Main Content Section
        dmc.AppShellMain(
            dmc.Container(
                id="page-content",  # Dynamic page content placeholder
                fluid=True,  # Allow dynamic resizing, but with a constrained max width
                style={
                    "padding": "16px",
                    "overflowX": "auto",  # Enable horizontal scrolling for content overflow
                    "maxWidth": "1200px",  # Constrain the maximum width to prevent it from being too wide
                    "margin": "0 auto",  # Center the content horizontally
                },
            ),
        )
    ],

    # AppShell Configuration
    header={"height": 60},  # Set header height
    padding="md",  # Use AppShell padding

    # Navbar Configuration
    navbar={
        "width": {"base": 200, "sm": 250, "lg": 300},  # Responsive navbar width
        "breakpoint": "sm",  # Collapse navbar on small screens
        "collapsed": {"mobile": True},  # Default collapsed on mobile
    },

    id="appshell",  # Assign an ID for dynamic interaction
)
