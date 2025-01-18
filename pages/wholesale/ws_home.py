from flask import current_app
from dash import html, dcc
import dash_mantine_components as dmc
import plotly.express as px

def ws_home():
    """
    Generates the layout for the Wholesale homepage.

    Returns:
        dash.html.Div: Layout for the page.
    """
    # Access wholesale data processing
    from data_preprocessing.wholesale_processing import process_wholesale_data

    # Get the filtered wholesale data (as a DataFrame) and stats
    wholesale_data_result = process_wholesale_data()
    stats = wholesale_data_result['stats']
    wholesale_data = wholesale_data_result['merged_data']  # Use the correct key 'merged_data'

    # Compute Clothing vs. Jewelry data
    clothing_data = wholesale_data[wholesale_data["Category Group"] == "CLOTHING"]
    jewelry_data = wholesale_data[wholesale_data["Category Group"] == "JEWELRY"]

    # Group clothing data by SKU
    clothing_data_grouped = clothing_data.groupby("SKU", as_index=False).agg({
        "Subtotal": "sum",
        "Quantity": "sum",
    })

    # Group jewelry data by SKU
    jewelry_data_grouped = jewelry_data.groupby("SKU", as_index=False).agg({
        "Subtotal": "sum",
        "Quantity": "sum",
    })

    # Compute Clothing Stats
    clothing_stats = {
        "total_skus": clothing_data_grouped["SKU"].nunique(),
        "total_revenue": clothing_data_grouped["Subtotal"].sum(),
        "productivity_per_sku": (
            clothing_data_grouped["Subtotal"].sum() / clothing_data_grouped["SKU"].nunique()
            if clothing_data_grouped["SKU"].nunique() > 0 else 0
        ),
    }

    # Compute Jewelry Stats
    jewelry_stats = {
        "total_skus": jewelry_data_grouped["SKU"].nunique(),
        "total_revenue": jewelry_data_grouped["Subtotal"].sum(),
        "productivity_per_sku": (
            jewelry_data_grouped["Subtotal"].sum() / jewelry_data_grouped["SKU"].nunique()
            if jewelry_data_grouped["SKU"].nunique() > 0 else 0
        ),
    }

    # Create SPSU25 Status Distribution Pie Chart
    spsu25_distribution = wholesale_data["SPSU25 Status"].value_counts(normalize=True).reset_index()
    spsu25_distribution.columns = ["SPSU25 Status", "proportion"]

    pie_chart = px.pie(
        spsu25_distribution,
        names="SPSU25 Status",
        values="proportion",
        title="SPSU25 Status Distribution",
    )

    # Create the layout
    return html.Div(
        [
            html.H1("Welcome to the Wholesale Home Page", style={"textAlign": "center"}),

            # Summary Stats in Cards
            dmc.Group(
                [
                    dmc.Card(
                        children=[
                            dmc.Text("Total Orders", fw=500, size="lg"),
                            dmc.Text(f"{stats['total_orders']:,}", size="xl", c="blue"),
                        ],
                        withBorder=True,
                        shadow="sm",
                        padding="md",
                    ),
                    dmc.Card(
                        children=[
                            dmc.Text("Revenue in Quotation", fw=500, size="lg"),
                            dmc.Text(f"${stats['total_revenue_quotation']:,.2f}", size="xl", c="orange"),
                        ],
                        withBorder=True,
                        shadow="sm",
                        padding="md",
                    ),
                    dmc.Card(
                        children=[
                            dmc.Text("Revenue Sold", fw=500, size="lg"),
                            dmc.Text(f"${stats['total_revenue_sold']:,.2f}", size="xl", c="green"),
                        ],
                        withBorder=True,
                        shadow="sm",
                        padding="md",
                    ),
                    dmc.Card(
                        children=[
                            dmc.Text("Average Order Value", fw=500, size="lg"),
                            dmc.Text(f"${stats['avg_order_value']:,.2f}", size="xl", c="purple"),
                        ],
                        withBorder=True,
                        shadow="sm",
                        padding="md",
                    ),
                    dmc.Card(
                        children=[
                            dmc.Text("Top-Selling Product", fw=500, size="lg"),
                            dmc.Text(stats['top_selling_product'], size="xl", c="red"),
                        ],
                        withBorder=True,
                        shadow="sm",
                        padding="md",
                    ),
                ],
                justify="center",
                gap="xl",
                style={"marginTop": "20px"},
            ),

            # Clothing vs Jewelry Table
            html.H2("Clothing vs. Jewelry", style={"textAlign": "center", "marginTop": "40px"}),
            dmc.Table(
                [
                    html.Thead(
                        html.Tr(
                            [
                                html.Th("Metric"),
                                html.Th("Clothing"),
                                html.Th("Jewelry"),
                            ]
                        )
                    ),
                    html.Tbody(
                        [
                            html.Tr(
                                [
                                    html.Td("Total SKUs Sold"),
                                    html.Td(f"{clothing_stats['total_skus']:,}"),
                                    html.Td(f"{jewelry_stats['total_skus']:,}"),
                                ]
                            ),
                            html.Tr(
                                [
                                    html.Td("Total Revenue"),
                                    html.Td(f"${clothing_stats['total_revenue']:,.2f}"),
                                    html.Td(f"${jewelry_stats['total_revenue']:,.2f}"),
                                ]
                            ),
                            html.Tr(
                                [
                                    html.Td("Productivity per SKU"),
                                    html.Td(f"${clothing_stats['productivity_per_sku']:,.2f}"),
                                    html.Td(f"${jewelry_stats['productivity_per_sku']:,.2f}"),
                                ]
                            ),
                        ]
                    ),
                ],
                striped=True,
                highlightOnHover=True,
                withTableBorder=True,
                withColumnBorders=True,
                style={"margin": "0 auto", "width": "80%", "marginTop": "20px"},
            ),

            # SPSU25 Pie Chart
            html.H2("SPSU25 Status Distribution", style={"textAlign": "center", "marginTop": "40px"}),
            dcc.Graph(figure=pie_chart, style={"marginTop": "20px"}),

            # Clothing Collections Table
            html.H2("Clothing Collections", style={"textAlign": "center", "marginTop": "40px"}),
            dmc.Table(
                [
                    html.Thead(
                        html.Tr(
                            [
                                html.Th("Name"),
                                html.Th("Qty Sold"),
                                html.Th("Total Revenue"),
                            ]
                        )
                    ),
                    html.Tbody(
                        [
                            html.Tr(
                                [
                                    html.Td(row["SKU"]),
                                    html.Td(f"{row['Quantity']:,}"),
                                    html.Td(f"${row['Subtotal']:,.2f}"),
                                ]
                            )
                            for _, row in clothing_data_grouped.sort_values(by="Subtotal", ascending=False).head(10).iterrows()
                        ]
                    ),
                ],
                striped=True,
                highlightOnHover=True,
                withTableBorder=True,
                withColumnBorders=True,
                style={"margin": "0 auto", "width": "80%", "marginTop": "20px"},
            ),

            # Jewelry Collections Table
            html.H2("Jewelry Collections", style={"textAlign": "center", "marginTop": "40px"}),
            dmc.Table(
                [
                    html.Thead(
                        html.Tr(
                            [
                                html.Th("Name"),
                                html.Th("Qty Sold"),
                                html.Th("Total Revenue"),
                            ]
                        )
                    ),
                    html.Tbody(
                        [
                            html.Tr(
                                [
                                    html.Td(row["SKU"]),
                                    html.Td(f"{row['Quantity']:,}"),
                                    html.Td(f"${row['Subtotal']:,.2f}"),
                                ]
                            )
                            for _, row in jewelry_data_grouped.sort_values(by="Subtotal", ascending=False).head(10).iterrows()
                        ]
                    ),
                ],
                striped=True,
                highlightOnHover=True,
                withTableBorder=True,
                withColumnBorders=True,
                style={"margin": "0 auto", "width": "80%", "marginTop": "20px"},
            ),
        ],
        style={"padding": "20px"},
    )
