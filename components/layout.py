# components/layout.py
import dash_mantine_components as dmc
from components.theme_toggle import theme_toggle

# Define the AppShell layout
layout = dmc.AppShell(
    header={
        "height": 60,  # Set header height
        "withBorder": True,  # Add a bottom border to the header
    },
    navbar={
        "width": 300,  # Set navbar width
        "breakpoint": "sm",  # Navbar collapses on small screens
        "collapsed": {"mobile": True},  # Collapsed by default on mobile
    },
    footer={
        "height": 40,  # Set footer height
        "withBorder": True,  # Add a top border to the footer
    },
    padding="md",
    children=[
        dmc.AppShellHeader(
            dmc.Group(
                [
                    dmc.Title("L and L Sales Dashboard", order=2),
                    theme_toggle,
                ],
                justify="space-between",
                align="center",
                h="100%",
                px="md",
            )
        ),
        dmc.AppShellNavbar(
            children=dmc.Text("Navigation will go here", size="sm"),
            p="md",
        ),
        dmc.AppShellMain(
            children=[
                dmc.Container(
                    id="page-content",  # Placeholder for dynamic content
                    style={"padding": "16px"},
                )
            ]
        ),
        dmc.AppShellFooter(
            dmc.Text(
                "© 2025 Wholesale Dashboard. All rights reserved.",
                size="xs",
                ta="center",
            ),
            p="sm",
            withBorder=True,
        ),
    ]
)
