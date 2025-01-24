from flask import current_app
from dash import html
import dash_mantine_components as dmc


def channel():
    """
    Generates the layout for the Channel Comparison page with unified tables for SKUs and collections, 
    with clear separation between channels.

    Returns:
        dash.html.Div: Layout for the page.
    """
    # Access preloaded data
    root_data = current_app.config['root_data']
    channel_data = root_data['channel_comparison']  # Top 10 data for channels

    # Extract SKU and collection data
    ecom_top_10 = channel_data['ecom_top_10']
    wholesale_top_10 = channel_data['wholesale_top_10']
    faire_top_10 = channel_data['faire_top_10']

    ecom_top_collections = channel_data['ecom_top_collections']
    wholesale_top_collections = channel_data['wholesale_top_collections']
    faire_top_collections = channel_data['faire_top_collections']

    # Ensure all groups have the same number of rows for SKUs
    max_rows_skus = max(len(ecom_top_10), len(wholesale_top_10), len(faire_top_10))
    ecom_top_10 = ecom_top_10.reindex(range(max_rows_skus)).fillna({"SKU (Parent)": "", "Quantity": 0, "Subtotal": 0})
    wholesale_top_10 = wholesale_top_10.reindex(range(max_rows_skus)).fillna({"SKU (Parent)": "", "Quantity": 0, "Subtotal": 0})
    faire_top_10 = faire_top_10.reindex(range(max_rows_skus)).fillna({"SKU (Parent)": "", "Quantity": 0, "Subtotal": 0})

    # Ensure all groups have the same number of rows for collections
    max_rows_collections = max(len(ecom_top_collections), len(wholesale_top_collections), len(faire_top_collections))
    ecom_top_collections = ecom_top_collections.reindex(range(max_rows_collections)).fillna({"Collection": "", "Quantity": 0, "Subtotal": 0})
    wholesale_top_collections = wholesale_top_collections.reindex(range(max_rows_collections)).fillna({"Collection": "", "Quantity": 0, "Subtotal": 0})
    faire_top_collections = faire_top_collections.reindex(range(max_rows_collections)).fillna({"Collection": "", "Quantity": 0, "Subtotal": 0})

    # Define custom styles for channel groups with vertical separators
    ecom_style = {"backgroundColor": "#e0f7fa"}  # Light blue for eCommerce
    wholesale_style = {"backgroundColor": "#f1f8e9"}  # Light green for Wholesale
    faire_style = {"backgroundColor": "#fce4ec"}  # Light pink for Faire
    vertical_border_style = {"borderRight": "2px solid black"}  # Vertical separation border

    # Create table rows for SKUs
    sku_rows = []
    for i in range(max_rows_skus):
        sku_rows.append(
            dmc.TableTr(
                [
                    # eCommerce data
                    dmc.TableTd(ecom_top_10.iloc[i]["SKU (Parent)"], style=ecom_style),
                    dmc.TableTd(f"{int(ecom_top_10.iloc[i]['Quantity']):,}" if ecom_top_10.iloc[i]["Quantity"] else "", style=ecom_style),
                    dmc.TableTd(f"${ecom_top_10.iloc[i]['Subtotal']:,.2f}" if ecom_top_10.iloc[i]["Subtotal"] else "", style={**ecom_style, **vertical_border_style}),
                    # Wholesale data
                    dmc.TableTd(wholesale_top_10.iloc[i]["SKU (Parent)"], style=wholesale_style),
                    dmc.TableTd(f"{int(wholesale_top_10.iloc[i]['Quantity']):,}" if wholesale_top_10.iloc[i]["Quantity"] else "", style=wholesale_style),
                    dmc.TableTd(f"${wholesale_top_10.iloc[i]['Subtotal']:,.2f}" if wholesale_top_10.iloc[i]["Subtotal"] else "", style={**wholesale_style, **vertical_border_style}),
                    # Faire data
                    dmc.TableTd(faire_top_10.iloc[i]["SKU (Parent)"], style=faire_style),
                    dmc.TableTd(f"{int(faire_top_10.iloc[i]['Quantity']):,}" if faire_top_10.iloc[i]["Quantity"] else "", style=faire_style),
                    dmc.TableTd(f"${faire_top_10.iloc[i]['Subtotal']:,.2f}" if faire_top_10.iloc[i]["Subtotal"] else "", style=faire_style),
                ],
                style={"borderBottom": "1px solid #ddd"},  # Add subtle row borders
            )
        )

    # Create table rows for collections
    collection_rows = []
    for i in range(max_rows_collections):
        collection_rows.append(
            dmc.TableTr(
                [
                    # eCommerce data
                    dmc.TableTd(ecom_top_collections.iloc[i]["Collection"], style=ecom_style),
                    dmc.TableTd(f"{int(ecom_top_collections.iloc[i]['Quantity']):,}" if ecom_top_collections.iloc[i]["Quantity"] else "", style=ecom_style),
                    dmc.TableTd(f"${ecom_top_collections.iloc[i]['Subtotal']:,.2f}" if ecom_top_collections.iloc[i]["Subtotal"] else "", style={**ecom_style, **vertical_border_style}),
                    # Wholesale data
                    dmc.TableTd(wholesale_top_collections.iloc[i]["Collection"], style=wholesale_style),
                    dmc.TableTd(f"{int(wholesale_top_collections.iloc[i]['Quantity']):,}" if wholesale_top_collections.iloc[i]["Quantity"] else "", style=wholesale_style),
                    dmc.TableTd(f"${wholesale_top_collections.iloc[i]['Subtotal']:,.2f}" if wholesale_top_collections.iloc[i]["Subtotal"] else "", style={**wholesale_style, **vertical_border_style}),
                    # Faire data
                    dmc.TableTd(faire_top_collections.iloc[i]["Collection"], style=faire_style),
                    dmc.TableTd(f"{int(faire_top_collections.iloc[i]['Quantity']):,}" if faire_top_collections.iloc[i]["Quantity"] else "", style=faire_style),
                    dmc.TableTd(f"${faire_top_collections.iloc[i]['Subtotal']:,.2f}" if faire_top_collections.iloc[i]["Subtotal"] else "", style=faire_style),
                ],
                style={"borderBottom": "1px solid #ddd"},  # Add subtle row borders
            )
        )

    # Headers with bottom border for separation
    header_style = {"borderBottom": "2px solid black"}

    # Define headers for SKUs
    sku_header = dmc.TableThead(
        dmc.TableTr(
            [
                dmc.TableTh("eCommerce SKU", style={**ecom_style, **header_style}),
                dmc.TableTh("Qty Sold (eCom)", style={**ecom_style, **header_style}),
                dmc.TableTh("Revenue (eCom)", style={**ecom_style, **vertical_border_style, **header_style}),
                dmc.TableTh("Wholesale SKU", style={**wholesale_style, **header_style}),
                dmc.TableTh("Qty Sold (Wholesale)", style={**wholesale_style, **header_style}),
                dmc.TableTh("Revenue (Wholesale)", style={**wholesale_style, **vertical_border_style, **header_style}),
                dmc.TableTh("Faire SKU", style={**faire_style, **header_style}),
                dmc.TableTh("Qty Sold (Faire)", style={**faire_style, **header_style}),
                dmc.TableTh("Revenue (Faire)", style={**faire_style, **header_style}),
            ]
        )
    )

    # Define headers for collections
    collection_header = dmc.TableThead(
        dmc.TableTr(
            [
                dmc.TableTh("eCommerce Collection", style={**ecom_style, **header_style}),
                dmc.TableTh("Qty Sold (eCom)", style={**ecom_style, **header_style}),
                dmc.TableTh("Revenue (eCom)", style={**ecom_style, **vertical_border_style, **header_style}),
                dmc.TableTh("Wholesale Collection", style={**wholesale_style, **header_style}),
                dmc.TableTh("Qty Sold (Wholesale)", style={**wholesale_style, **header_style}),
                dmc.TableTh("Revenue (Wholesale)", style={**wholesale_style, **vertical_border_style, **header_style}),
                dmc.TableTh("Faire Collection", style={**faire_style, **header_style}),
                dmc.TableTh("Qty Sold (Faire)", style={**faire_style, **header_style}),
                dmc.TableTh("Revenue (Faire)", style={**faire_style, **header_style}),
            ]
        )
    )

    # Create tables
    sku_table = dmc.Table(children=[sku_header, dmc.TableTbody(sku_rows)], withTableBorder=True)
    collection_table = dmc.Table(children=[collection_header, dmc.TableTbody(collection_rows)], withTableBorder=True)

    # Layout
    return html.Div(
        [
            html.H1("Channel Comparison", style={"textAlign": "center"}),
            dmc.Card(html.Div(sku_table, style={"overflowX": "auto"})),
            dmc.Card(html.Div(collection_table, style={"overflowX": "auto"})),
        ]
    )
