# Template for "Coming Soon" Pages
from dash import html, dcc


home = html.Div(
    [
        html.H1("Welcome to the Home Page"),
        dcc.Link("Go to Wholesale", href="/wholesale"),
    ]
)


