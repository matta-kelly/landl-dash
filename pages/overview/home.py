from flask import current_app
from dash import html, dcc
import dash_mantine_components as dmc
import plotly.express as px

def home():
    # Access preloaded data
    root_data = current_app.config['root_data']
    stats = root_data['stats']
    merged_data = root_data['merged_data']

    # Compute Clothing vs. Jewelry data
    clothing_data = merged_data[merged_data["Category Group"] == "CLOTHING"]
    jewelry_data = merged_data[merged_data["Category Group"] == "JEWELRY"]

    # Group clothing data by Parent SKU
    clothing_data_grouped = clothing_data.groupby("SKU (Parent)", as_index=False).agg({
        "Subtotal": "sum",  # Sum up revenue for each Parent SKU
        "Quantity": "sum",  # Sum up quantity sold
    }).sort_values(by="Subtotal", ascending=False).head(15)  # Top 10 Clothing

    # Group jewelry data by Parent SKU
    jewelry_data_grouped = jewelry_data.groupby("SKU (Parent)", as_index=False).agg({
        "Subtotal": "sum",  # Sum up revenue for each Parent SKU
        "Quantity": "sum",  # Sum up quantity sold
    }).sort_values(by="Subtotal", ascending=False).head(15)  # Top 10 Jewelry

    # Filter out rows where Fabric SKU is 'A'
    fabric_data = merged_data[(merged_data["Fabric SKU"] != 'A') & (merged_data["Fabric SKU"] != '<NA>')]

    # Combined table with Parent SKUs
    combined_rows = []
    max_rows = max(len(clothing_data_grouped), len(jewelry_data_grouped))
    for i in range(max_rows):
        combined_rows.append(
            dmc.TableTr(
                [
                    # Clothing data
                    dmc.TableTd(
                        clothing_data_grouped.iloc[i]["SKU (Parent)"] if i < len(clothing_data_grouped) else "",
                        style={"backgroundColor": "#e0f7fa"},
                    ),
                    dmc.TableTd(
                        f"{int(clothing_data_grouped.iloc[i]['Quantity']):,}" if i < len(clothing_data_grouped) else "",
                        style={"backgroundColor": "#e0f7fa"},
                    ),
                    dmc.TableTd(
                        f"${clothing_data_grouped.iloc[i]['Subtotal']:,.2f}" if i < len(clothing_data_grouped) else "",
                        style={"backgroundColor": "#e0f7fa", "borderRight": "2px solid black"},
                    ),
                    # Jewelry data
                    dmc.TableTd(
                        jewelry_data_grouped.iloc[i]["SKU (Parent)"] if i < len(jewelry_data_grouped) else "",
                        style={"backgroundColor": "#fce4ec"},
                    ),
                    dmc.TableTd(
                        f"{int(jewelry_data_grouped.iloc[i]['Quantity']):,}" if i < len(jewelry_data_grouped) else "",
                        style={"backgroundColor": "#fce4ec"},
                    ),
                    dmc.TableTd(
                        f"${jewelry_data_grouped.iloc[i]['Subtotal']:,.2f}" if i < len(jewelry_data_grouped) else "",
                        style={"backgroundColor": "#fce4ec"},
                    ),
                ],
                style={"borderBottom": "1px solid #ddd"},
            )
        )

    # Table header for Parent SKUs
    combined_table_header = dmc.TableThead(
        dmc.TableTr(
            [
                dmc.TableTh("Clothing SKU", style={"backgroundColor": "#e0f7fa"}),
                dmc.TableTh("Qty Sold (Clothing)", style={"backgroundColor": "#e0f7fa"}),
                dmc.TableTh("Revenue (Clothing)", style={"backgroundColor": "#e0f7fa", "borderRight": "2px solid black"}),
                dmc.TableTh("Jewelry SKU", style={"backgroundColor": "#fce4ec"}),
                dmc.TableTh("Qty Sold (Jewelry)", style={"backgroundColor": "#fce4ec"}),
                dmc.TableTh("Revenue (Jewelry)", style={"backgroundColor": "#fce4ec"}),
            ],
            style={"borderBottom": "2px solid black"},
        )
    )

    combined_table_body = dmc.TableTbody(combined_rows)

    # Unified table for Clothing and Jewelry Parent SKUs
    combined_table = dmc.Table(
        children=[combined_table_header, combined_table_body],
        striped=False,
        highlightOnHover=True,
        withTableBorder=True,
        withColumnBorders=True,
        verticalSpacing="sm",
        horizontalSpacing="md",
    )

    # Compute Clothing vs. Jewelry stats by SKU (not Parent SKU)
    clothing_data_sku_grouped = clothing_data.groupby("SKU", as_index=False).agg({
        "Subtotal": "sum",
        "Quantity": "sum",
    })

    jewelry_data_sku_grouped = jewelry_data.groupby("SKU", as_index=False).agg({
        "Subtotal": "sum",
        "Quantity": "sum",
    })

    clothing_stats = {
        "total_skus": clothing_data_sku_grouped["SKU"].nunique(),
        "total_revenue": clothing_data_sku_grouped["Subtotal"].sum(),
        "productivity_per_sku": clothing_data_sku_grouped["Subtotal"].sum() / clothing_data_sku_grouped["SKU"].nunique()
        if clothing_data_sku_grouped["SKU"].nunique() > 0 else 0,
    }

    jewelry_stats = {
        "total_skus": jewelry_data_sku_grouped["SKU"].nunique(),
        "total_revenue": jewelry_data_sku_grouped["Subtotal"].sum(),
        "productivity_per_sku": jewelry_data_sku_grouped["Subtotal"].sum() / jewelry_data_sku_grouped["SKU"].nunique()
        if jewelry_data_sku_grouped["SKU"].nunique() > 0 else 0,
    }

    # SPSU25 Status Distribution Pie Chart
    spsu25_distribution = merged_data["SPSU25 Status"].value_counts(normalize=True).reset_index()
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
            html.H1("Welcome to the Home Page", style={"textAlign": "center"}),

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
                            dmc.Text("Revenue Sold", fw=500, size="lg"),
                            dmc.Text(f"${stats['total_revenue_sold']:,.2f}", size="xl", c="green"),
                        ],
                        withBorder=True,
                        shadow="sm",
                        padding="md",
                    ),
                    dmc.Card(
                        children=[
                            dmc.Text("Revenue in Quotation", fw=500, size="lg"),
                            dmc.Text(f"${stats['total_revenue_quotation']:,.2f}", size="xl", c="purple"),
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
                                    html.Td("Total SKUs sold", style={"padding": "10px", "fontWeight": "bold"}),
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
            ),


            # SPSU25 Pie Chart
            html.H2("SPSU25 Status Distribution", style={"textAlign": "center", "marginTop": "40px"}),
            dcc.Graph(figure=pie_chart, style={"marginTop": "20px"}),

            # Combined Clothing and Jewelry Parent SKU Table
            html.H2("Top 20 Clothing and Jewelry Parent SKUs", style={"textAlign": "center", "marginTop": "40px"}),
            html.Div(combined_table, style={"overflowX": "auto"}),

            # Fabric SKU Table
            html.H2("Fabric SKU Summary", style={"textAlign": "center", "marginTop": "40px"}),
            dmc.Table(
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
                            for _, row in fabric_data.groupby("Fabric SKU", as_index=False)
                            .agg({"Quantity": "sum", "Subtotal": "sum"})
                            .sort_values(by="Subtotal", ascending=False)
                            .head(30)
                            .iterrows()
                        ]
                    ),
                ],
                striped=True,
                highlightOnHover=True,
                withTableBorder=True,
                withColumnBorders=True,
            ),
        ],
        style={"padding": "20px"},
    )
