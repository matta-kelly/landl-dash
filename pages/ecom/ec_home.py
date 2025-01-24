from flask import current_app
from dash import html, dcc
import dash_mantine_components as dmc
import plotly.express as px


def ec_home():
    """
    Generates the layout for the eCommerce homepage.

    Returns:
        dash.html.Div: Layout for the page.
    """
    # Access preloaded data
    stats = current_app.config.get('ecom_stats')
    ecom_data = current_app.config.get('ecom_merged_data')

    # Compute Clothing vs. Jewelry data
    clothing_data = ecom_data[ecom_data["Category Group"] == "CLOTHING"]
    jewelry_data = ecom_data[ecom_data["Category Group"] == "JEWELRY"]

    # Group clothing and jewelry data by Parent SKU for the big table
    clothing_data_grouped = clothing_data.groupby("SKU (Parent)", as_index=False).agg({
        "Subtotal": "sum",
        "Quantity": "sum",
    })
    jewelry_data_grouped = jewelry_data.groupby("SKU (Parent)", as_index=False).agg({
        "Subtotal": "sum",
        "Quantity": "sum",
    })

    # Group clothing and jewelry data by SKU (not Parent SKU) for the small table
    clothing_sku_grouped = clothing_data.groupby("SKU", as_index=False).agg({
        "Subtotal": "sum",
        "Quantity": "sum",
    })
    jewelry_sku_grouped = jewelry_data.groupby("SKU", as_index=False).agg({
        "Subtotal": "sum",
        "Quantity": "sum",
    })

    # Compute Clothing Stats (based on SKUs)
    clothing_stats = {
        "total_skus": clothing_sku_grouped["SKU"].nunique(),
        "total_revenue": clothing_sku_grouped["Subtotal"].sum(),
        "productivity_per_sku": (
            clothing_sku_grouped["Subtotal"].sum() / clothing_sku_grouped["SKU"].nunique()
            if clothing_sku_grouped["SKU"].nunique() > 0 else 0
        ),
    }

    # Compute Jewelry Stats (based on SKUs)
    jewelry_stats = {
        "total_skus": jewelry_sku_grouped["SKU"].nunique(),
        "total_revenue": jewelry_sku_grouped["Subtotal"].sum(),
        "productivity_per_sku": (
            jewelry_sku_grouped["Subtotal"].sum() / jewelry_sku_grouped["SKU"].nunique()
            if jewelry_sku_grouped["SKU"].nunique() > 0 else 0
        ),
    }

    # Filter and sort top Parent SKUs by revenue for the big table
    top_clothing = clothing_data_grouped.sort_values(by="Subtotal", ascending=False).head(15)
    top_jewelry = jewelry_data_grouped.sort_values(by="Subtotal", ascending=False).head(15)

    # Custom styles for each group
    clothing_style = {"backgroundColor": "#e0f7fa"}  # Light blue for clothing
    jewelry_style = {"backgroundColor": "#fce4ec"}  # Light pink for jewelry
    vertical_border_style = {"borderRight": "2px solid black"}  # Vertical separator


    # Combined table rows with styling
    combined_rows = []
    for clothing_row, jewelry_row in zip(top_clothing.itertuples(), top_jewelry.itertuples()):
        combined_rows.append(
            dmc.TableTr(
                [
                    # Clothing data
                    dmc.TableTd(clothing_row._1, style=clothing_style),
                    dmc.TableTd(f"{clothing_row.Quantity:,}", style=clothing_style),
                    dmc.TableTd(f"${clothing_row.Subtotal:,.2f}", style={**clothing_style, **vertical_border_style}),
                    # Jewelry data
                    dmc.TableTd(jewelry_row._1, style=jewelry_style),
                    dmc.TableTd(f"{jewelry_row.Quantity:,}", style=jewelry_style),
                    dmc.TableTd(f"${jewelry_row.Subtotal:,.2f}", style=jewelry_style),
                ],
                style={"borderBottom": "1px solid #ddd"},  # Add subtle row borders
            )
        )


    # Small Table (Clothing vs Jewelry Summary Stats)
    clothing_vs_jewelry_stats_table = dmc.Table(
        [
            html.Thead(
                html.Tr(
                    [
                        html.Th("Metric", style={"textAlign": "left", "fontWeight": "bold", "padding": "10px"}),
                        html.Th("Clothing", style={"textAlign": "center", "fontWeight": "bold", "padding": "10px"}),
                        html.Th("Jewelry", style={"textAlign": "center", "fontWeight": "bold", "padding": "10px"}),
                    ],
                    style={"borderBottom": "2px solid #000", "backgroundColor": "#f8f9fa"},
                )
            ),
            html.Tbody(
                [
                    html.Tr(
                        [
                            html.Td("Total SKUs Sold", style={"padding": "10px", "fontWeight": "bold"}),
                            html.Td(f"{clothing_stats['total_skus']:,}", style={"textAlign": "center", "padding": "10px"}),
                            html.Td(f"{jewelry_stats['total_skus']:,}", style={"textAlign": "center", "padding": "10px"}),
                        ],
                        style={"borderBottom": "1px solid #ddd"},
                    ),
                    html.Tr(
                        [
                            html.Td("Total Revenue", style={"padding": "10px", "fontWeight": "bold"}),
                            html.Td(f"${clothing_stats['total_revenue']:,.2f}", style={"textAlign": "center", "padding": "10px"}),
                            html.Td(f"${jewelry_stats['total_revenue']:,.2f}", style={"textAlign": "center", "padding": "10px"}),
                        ],
                        style={"borderBottom": "1px solid #ddd"},
                    ),
                    html.Tr(
                        [
                            html.Td("Productivity per SKU", style={"padding": "10px", "fontWeight": "bold"}),
                            html.Td(f"${clothing_stats['productivity_per_sku']:,.2f}", style={"textAlign": "center", "padding": "10px"}),
                            html.Td(f"${jewelry_stats['productivity_per_sku']:,.2f}", style={"textAlign": "center", "padding": "10px"}),
                        ],
                    ),
                ]
            ),
        ],
        striped=False,
        highlightOnHover=True,
        withTableBorder=True,
        withColumnBorders=True,
        style={"width": "80%", "margin": "0 auto", "border": "1px solid #ccc", "borderRadius": "8px"},
    )


    # Combined table header with styling
    combined_table_header = dmc.TableThead(
        dmc.TableTr(
            [
                dmc.TableTh("Clothing SKU", style=clothing_style),
                dmc.TableTh("Qty Sold (Clothing)", style=clothing_style),
                dmc.TableTh("Revenue (Clothing)", style={**clothing_style, **vertical_border_style}),
                dmc.TableTh("Jewelry SKU", style=jewelry_style),
                dmc.TableTh("Qty Sold (Jewelry)", style=jewelry_style),
                dmc.TableTh("Revenue (Jewelry)", style=jewelry_style),
            ],
            style={"borderBottom": "2px solid black"},  # Thicker border for the header
        )
    )

    # Combined table body
    combined_table_body = dmc.TableTbody(combined_rows)
    
    # Combined Clothing and Jewelry Table
    combined_table = dmc.Table(
        children=[combined_table_header, combined_table_body],
        striped=False,
        highlightOnHover=True,
        withTableBorder=True,
        withColumnBorders=True,
        verticalSpacing="sm",
        horizontalSpacing="md",
    )

    # SPSU25 Pie Chart
    spsu25_distribution = ecom_data["SPSU25 Status"].value_counts(normalize=True).reset_index()
    spsu25_distribution.columns = ["SPSU25 Status", "proportion"]

    pie_chart = px.pie(
        spsu25_distribution,
        names="SPSU25 Status",
        values="proportion",
        title="SPSU25 Status Distribution",
    )

    # Fabric SKU Table
    fabric_data = ecom_data[(ecom_data["Fabric SKU"] != 'A') & (ecom_data["Fabric SKU"] != '<NA>')]
    fabric_data_grouped = fabric_data.groupby("Fabric SKU", as_index=False).agg({
        "Subtotal": "sum",
        "Quantity": "sum",
    })

    fabric_table = dmc.Table(
        [
            html.Thead(
                html.Tr(
                    [
                        html.Th("Fabric SKU"),
                        html.Th("Qty Sold"),
                        html.Th("Total Revenue"),
                    ]
                )
            ),
            html.Tbody(
                [
                    html.Tr(
                        [
                            html.Td(row["Fabric SKU"]),
                            html.Td(f"{row['Quantity']:,}"),
                            html.Td(f"${row['Subtotal']:,.2f}"),
                        ]
                    )
                    for _, row in fabric_data_grouped.sort_values(by="Subtotal", ascending=False).head(30).iterrows()
                ]
            ),
        ],
        striped=True,
        highlightOnHover=True,
        withTableBorder=True,
        withColumnBorders=True,
    )

    # Layout
    return html.Div(
        [
            html.H1("Welcome to the E-Commerce Home Page", style={"textAlign": "center"}),

            # Summary Stats Cards
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
                            dmc.Text("Total Revenue", fw=500, size="lg"),
                            dmc.Text(f"${stats['total_revenue']:,.2f}", size="xl", c="green"),
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

            # Small Table
            html.H2("Clothing vs. Jewelry", style={"textAlign": "center", "marginTop": "40px"}),
            clothing_vs_jewelry_stats_table,

            # Pie Chart
            html.H2("SPSU25 Status Distribution", style={"textAlign": "center", "marginTop": "40px"}),
            dcc.Graph(figure=pie_chart),

            # Combined Big Table
            html.H2("Top 20 Clothing and Jewelry Parent SKUs", style={"textAlign": "center", "marginTop": "40px"}),
            html.Div(combined_table, style={"overflowX": "auto"}),

            # Fabric SKU Table
            html.H2("Fabric SKU Summary", style={"textAlign": "center", "marginTop": "40px"}),
            fabric_table,
        ],
        style={"padding": "20px"},
    )
