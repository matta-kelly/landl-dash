# Template for "Coming Soon" Pages
from dash import html, dcc

ws_rep_view = html.Div(
    [
        html.H1("Welcome to the Wholesale Rep View Page"),
        html.H2("Coming Soon!", style={"textAlign": "center", "color": "gray", "marginTop": "20px"}),
        html.P(
            "This page is under construction and will be available soon.",
            style={"textAlign": "center", "color": "gray", "marginTop": "10px"}
        ),
    ]
)
