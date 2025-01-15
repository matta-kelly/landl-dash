import dash
from dash import dcc, html, Input, Output
from pages import home
from pages.wholesale.ws_home import layout as ws_home_layout
from pages.wholesale.ws_shipping_fufillment import layout as ws_shipping_layout
from pages.wholesale.ws_rep_view import layout as ws_rep_view_layout
from pages.wholesale.ws_customer_eval import layout as ws_customer_layout
from pages.wholesale.surf_expo.se_home import layout as se_home_layout
from pages.wholesale.surf_expo.se_shipping_fufillment import layout as se_shipping_layout
from pages.wholesale.surf_expo.se_rep_view import layout as se_rep_view_layout
from pages.wholesale.surf_expo.se_customer_eval import layout as se_customer_layout
from pages.ecom.ec_home import layout as ec_home_layout

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=["/assets/styles.css"], suppress_callback_exceptions=True)
app.title = "Sales Order Dashboard"

# Layout of the app
app.layout = html.Div(
    children=[
        html.H1("Sales Order Dashboard", className="header-title"),
        dcc.Tabs(
            id="main-tabs",
            value="home",
            children=[
                dcc.Tab(label="Home", value="home"),
                dcc.Tab(label="Wholesale", value="wholesale"),
                dcc.Tab(label="Ecom", value="ecom"),
            ],
        ),
        html.Div(id="main-tabs-content"),
    ],
    className="container",
)

# Callback to manage the main tabs
@app.callback(
    Output("main-tabs-content", "children"),
    Input("main-tabs", "value"),
)
def render_main_tabs(selected_tab):
    if selected_tab == "home":
        return home.layout
    elif selected_tab == "wholesale":
        return html.Div(
            children=[
                dcc.Tabs(
                    id="wholesale-tabs",
                    value="ws-home",
                    children=[
                        dcc.Tab(label="Home", value="ws-home"),
                        dcc.Tab(label="Shipping / Fulfillment", value="ws-shipping"),
                        dcc.Tab(label="Rep View", value="ws-rep"),
                        dcc.Tab(label="Customer Evaluation", value="ws-customer"),
                        dcc.Tab(label="Surf Expo", value="surf-expo"),
                    ],
                ),
                html.Div(id="wholesale-tabs-content"),
            ]
        )
    elif selected_tab == "ecom":
        return html.Div(
            children=[
                dcc.Tabs(
                    id="ecom-tabs",
                    value="ec-home",
                    children=[
                        dcc.Tab(label="Home", value="ec-home"),
                    ],
                ),
                html.Div(id="ecom-tabs-content"),
            ]
        )

# Callback to manage the wholesale tabs
@app.callback(
    Output("wholesale-tabs-content", "children"),
    Input("wholesale-tabs", "value"),
)
def render_wholesale_tabs(selected_tab):
    if selected_tab == "ws-home":
        return ws_home_layout
    elif selected_tab == "ws-shipping":
        return ws_shipping_layout
    elif selected_tab == "ws-rep":
        return ws_rep_view_layout
    elif selected_tab == "ws-customer":
        return ws_customer_layout
    elif selected_tab == "surf-expo":
        return html.Div(
            children=[
                dcc.Tabs(
                    id="surf-expo-tabs",
                    value="se-home",
                    children=[
                        dcc.Tab(label="Home", value="se-home"),
                        dcc.Tab(label="Shipping / Fulfillment", value="se-shipping"),
                        dcc.Tab(label="Rep View", value="se-rep"),
                        dcc.Tab(label="Customer Evaluation", value="se-customer"),
                    ],
                ),
                html.Div(id="surf-expo-tabs-content"),
            ]
        )

# Callback to manage the Surf Expo tabs
@app.callback(
    Output("surf-expo-tabs-content", "children"),
    Input("surf-expo-tabs", "value"),
)
def render_surf_expo_tabs(selected_tab):
    if selected_tab == "se-home":
        return se_home_layout
    elif selected_tab == "se-shipping":
        return se_shipping_layout
    elif selected_tab == "se-rep":
        return se_rep_view_layout
    elif selected_tab == "se-customer":
        return se_customer_layout

# Callback to manage the ecom tabs
@app.callback(
    Output("ecom-tabs-content", "children"),
    Input("ecom-tabs", "value"),
)
def render_ecom_tabs(selected_tab):
    if selected_tab == "ec-home":
        return ec_home_layout

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
