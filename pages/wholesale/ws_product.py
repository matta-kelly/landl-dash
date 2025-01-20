from dash import html, dcc
import plotly.express as px
from flask import current_app

def ws_product():
    """
    Generates the layout for the Wholesale Product Analysis page with a scatter plot
    for Profit Margin vs. Revenue.

    Returns:
        dash.html.Div: Layout for the page.
    """
    product_profit_analysis = current_app.config.get('wholesale_product_profit_analysis')

    if product_profit_analysis is None or product_profit_analysis.empty:
        return html.Div(
            [
                html.H1("Welcome to the Wholesale Product Analysis Page", style={"textAlign": "center"}),
                html.H2(
                    "No data available for Product Analysis at this time.",
                    style={"textAlign": "center", "color": "gray", "marginTop": "20px"},
                ),
            ]
        )

    # Create the scatter plot
    fig = px.scatter(
        product_profit_analysis,
        x="Total Revenue",
        y="Profit Margin (%)",
        size="Units Sold",
        color="Lifecycle Status",
        hover_data=["SKU"],
        title="Profit Margin vs. Revenue by Product",
        labels={
            "Total Revenue": "Total Revenue ($)",
            "Profit Margin (%)": "Profit Margin (%)",
            "Units Sold": "Units Sold",
            "Lifecycle Status": "Lifecycle Status",
        },
    )

    # Update the layout for better aesthetics
    fig.update_layout(
        title_x=0.5,
        xaxis_title="Total Revenue ($)",
        yaxis_title="Profit Margin (%)",
        template="simple_white",
        margin=dict(l=50, r=50, t=50, b=50),
        legend_title="Lifecycle Status",
    )

    # Update markers for better visibility
    fig.update_traces(marker=dict(opacity=0.7, line=dict(width=0.5, color="black")))

    # Create the layout
    return html.Div(
        [
            html.H1("Wholesale Product Analysis", style={"textAlign": "center"}),

            html.H2("Profit Margin vs. Revenue", style={"textAlign": "center", "marginTop": "20px"}),

            # Explanatory text
            html.Div(
                [
                    html.P(
                        "This scatter plot presents the relationship between total revenue and profit margin for products "
                        " Each point (or bubble) represents a unique product SKU. The x-axis indicates the total revenue"
                        " generated by the product, while the y-axis reflects the profit margin percentage (IMU%).",
                        style={"marginTop": "20px", "textAlign": "justify"},
                    ),
                    html.P(
                        "The size of the bubble corresponds to the total units sold, with larger bubbles indicating higher "
                        "sales volume. The color of each bubble represents the product's lifecycle status, such as 'Core', "
                        "'Seasonal', or 'Discontinued'. The color legend helps distinguish these categories visually, allowing "
                        "for an easy understanding of how lifecycle status relates to revenue and profit margin.",
                        style={"marginTop": "10px", "textAlign": "justify"},
                    ),
                    html.P(
                        "Hovering over a bubble reveals additional details about the product, including its SKU, lifecycle status, "
                        "total revenue, profit margin, and units sold. This interactivity allows users to drill down into individual "
                        "products for a more granular analysis.",
                        style={"marginTop": "10px", "textAlign": "justify"},
                    ),
                    html.P(
                        "The scatter plot is designed to help users visually identify trends, such as products with high revenue "
                        "but low profit margins, or those with high profit margins but low sales. These patterns can inform decisions "
                        "related to pricing, promotions, and inventory management. Products positioned in different regions of the "
                        "plot may suggest strategic opportunities or challenges.",
                        style={"marginTop": "10px", "textAlign": "justify"},
                    ),
                ],
                style={"margin": "20px auto", "width": "80%"},
            ),

            # Scatter plot
            dcc.Graph(figure=fig, style={"marginTop": "20px"}),
        ],
        style={"padding": "20px"},
    )
