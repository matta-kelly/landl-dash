# Template for "Coming Soon" Pages
from dash import html, dcc

ws_product = html.Div(
    [
        html.H1("Welcome to the Wholesale Product Analysis Page"),
        html.H2("Coming Soon!", style={"textAlign": "center", "color": "gray", "marginTop": "20px"}),
        html.P(
            "This page is under construction and will be available soon.",
            style={"textAlign": "center", "color": "gray", "marginTop": "10px"}
        ),
    ]
)