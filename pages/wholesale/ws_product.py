from dash import html, dcc
import plotly.express as px

def ws_product():
    """
    Generates the layout for the Wholesale Product Analysis page with a scatter plot
    for Profit Margin vs. Revenue.

    Returns:
        dash.html.Div: Layout for the page.
    """
    # Load processed product profit analysis data
    from data_preprocessing.wholesale_processing import process_wholesale_data
    wholesale_data_result = process_wholesale_data()
    product_profit_analysis = wholesale_data_result.get("product_profit_analysis")

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
                        "This scatter plot visualizes the relationship between total revenue and profit margin "
                        "for each product in our wholesale catalog. Each bubble represents a product SKU, with the "
                        "size of the bubble indicating the total units sold. The color coding corresponds to the product's "
                        "lifecycle status, such as 'Core', 'Seasonal', or 'Discontinued'.",
                        style={"marginTop": "20px", "textAlign": "justify"},
                    ),
                    html.P(
                        "Key insights from this graph include identifying products with high revenue but low profit margins, "
                        "or those with high profit margins but low sales. Use the tooltips to hover over each bubble and see "
                        "detailed information about the SKU, revenue, and units sold.",
                        style={"marginTop": "10px", "textAlign": "justify"},
                    ),
                    html.P(
                        "This analysis can help guide decisions about inventory management, pricing strategies, and which "
                        "products to promote or phase out. You can use the legend to focus on specific lifecycle statuses "
                        "and filter the data visually.",
                        style={"marginTop": "10px", "textAlign": "justify"},
                    ),
                    html.P(
                        "This page will soon include a filter to explore products based on their lifecycle status, "
                        "such as 'Core', 'Seasonal', or 'Discontinued'. This feature will allow you to focus on specific "
                        "categories of products and gain targeted insights to support strategic decision-making.",
                        style={"marginTop": "20px", "textAlign": "center"}
                    ),

                ],
                style={"margin": "20px auto", "width": "80%"},
            ),

            # Scatter plot
            dcc.Graph(figure=fig, style={"marginTop": "20px"}),
        ],
        style={"padding": "20px"},
    )
