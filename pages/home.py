# Template for "Coming Soon" Pages

from dash import html

layout = html.Div(
    className="coming-soon-container",
    children=[
        html.H1("Coming Soon", className="coming-soon-title"),
        html.P(
            "This page is under construction. Check back soon for updates!",
            className="coming-soon-description",
        ),
    ],
)

