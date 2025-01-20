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

            # Delivery Trends by Product Category Section
            html.H2("Delivery Trends by Product Category", style={"textAlign": "center", "marginTop": "20px"}),

            html.Div(
                [
                    html.P(
                        "This stacked bar chart shows the delivery quantities for each product category (e.g., Clothing and Jewelry) "
                        "over time. The x-axis represents the delivery dates, while the y-axis shows the total quantity delivered. "
                        "The colors in the chart represent different product categories, allowing you to easily compare their delivery trends. "
                        "The stacked bars help visualize the combined and individual contributions of each category to the total deliveries on any given date.",
                        style={"marginTop": "20px", "textAlign": "justify"},
                    ),
                    html.P(
                        "Hovering over a bar displays detailed information, including the specific product category, the quantity delivered, "
                        "and the delivery date. This visualization helps you understand the distribution of deliveries across categories and identify "
                        "trends or anomalies over time.",
                        style={"marginTop": "10px", "textAlign": "justify"},
                    ),
                ],
                style={"margin": "20px auto", "width": "80%"},
            ),
            dcc.Graph(figure=fig_category, style={"marginTop": "20px"}),

            # Delivery Trends by Order Type Section
            html.H2("Delivery Trends by Order Type", style={"textAlign": "center", "marginTop": "40px"}),

            html.Div(
                [
                    html.P(
                        "This stacked bar chart visualizes the delivery quantities segmented by order type, such as Quotation and Sales, "
                        "over time. The x-axis represents the delivery dates, and the y-axis indicates the total quantity delivered. "
                        "The colors in the chart correspond to the different order types, enabling a clear distinction between them. "
                        "The stacked format allows you to see the cumulative quantities for all order types on a given date while preserving "
                        "the breakdown by type.",
                        style={"marginTop": "20px", "textAlign": "justify"},
                    ),
                    html.P(
                        "Hovering over the bars provides detailed information, including the order type, the quantity delivered, and the date. "
                        "This visualization is particularly useful for analyzing how delivery patterns differ between quotations and sales, helping you "
                        "identify trends or fluctuations in order fulfillment.",
                        style={"marginTop": "10px", "textAlign": "justify"},
                    ),
                ],
                style={"margin": "20px auto", "width": "80%"},
            ),
            dcc.Graph(figure=fig_status, style={"marginTop": "20px"}),
        ],
        style={"padding": "20px"},
    )
