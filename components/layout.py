import dash_mantine_components as dmc

# Define the AppShell layout
layout = dmc.AppShell(
    children=[
        dmc.AppShellHeader(
            dmc.Group(
                [
                    dmc.Title("L and L Sales Dashboard", order=2),
                    #dmc.Text("Choose a section from the navbar."),
                ],
                h="100%",
                px="md",
            ),
            withBorder=True,
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
                style={"padding": "16px"},
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
