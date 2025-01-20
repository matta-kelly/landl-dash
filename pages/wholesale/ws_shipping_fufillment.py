from dash import html, dcc
import plotly.express as px
import dash_mantine_components as dmc
from flask import current_app

def ws_shipping_fulfillment():
    """
    Generates the layout for the Wholesale Shipping and Fulfillment page with stacked bar charts
    for delivery quantities by product category and order type, along with delivery distribution.

    Returns:
        dash.html.Div: Layout for the page.
    """

    delivery_distribution = current_app.config.get('wholesale_delivery_distribution')


    # Handle missing or None delivery distribution gracefully
    if delivery_distribution is None or delivery_distribution.empty:
        return html.Div(
            [
                html.H1("Wholesale Shipping and Fulfillment", style={"textAlign": "center"}),
                html.H2(
                    "No delivery distribution data available.",
                    style={"textAlign": "center", "color": "gray", "marginTop": "20px"},
                ),
            ]
        )

    # Create the stacked bar chart for Clothing vs. Jewelry
    fig_category = px.bar(
        delivery_distribution,
        x="Delivery Date",
        y="Quantity",
        color="Category Group",
        title="Delivery Quantity by Category Over Time",
        labels={
            "Delivery Date": "Date",
            "Quantity": "Total Quantity Delivered",
            "Category Group": "Product Category",
        },
    )
    fig_category.update_layout(
        barmode="stack",
        title_x=0.5,
        xaxis_title="Delivery Date",
        yaxis_title="Quantity Delivered",
        template="simple_white",
        margin=dict(l=50, r=50, t=50, b=50),
        legend_title="Product Category",
    )

    # Create the stacked bar chart for Quotation vs. Sales
    fig_status = px.bar(
        delivery_distribution,
        x="Delivery Date",
        y="Quantity",
        color="Order Type",
        title="Delivery Quantity by Order Type Over Time",
        labels={
            "Delivery Date": "Date",
            "Quantity": "Total Quantity Delivered",
            "Order Type": "Order Type",
        },
    )
    fig_status.update_layout(
        barmode="stack",
        title_x=0.5,
        xaxis_title="Delivery Date",
        yaxis_title="Quantity Delivered",
        template="simple_white",
        margin=dict(l=50, r=50, t=50, b=50),
        legend_title="Order Type",
    )

    # Create the layout
    return html.Div(
        [
            html.H1("Wholesale Shipping and Fulfillment", style={"textAlign": "center"}),

            html.H2("Delivery Trends by Product Category", style={"textAlign": "center", "marginTop": "20px"}),
            dcc.Graph(figure=fig_category, style={"marginTop": "20px"}),

            html.H2("Delivery Trends by Order Type", style={"textAlign": "center", "marginTop": "40px"}),
            dcc.Graph(figure=fig_status, style={"marginTop": "20px"}),
        ],
        style={"padding": "20px"},
    )
