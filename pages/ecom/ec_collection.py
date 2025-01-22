from flask import current_app
from dash import html, dcc
import dash_mantine_components as dmc
import plotly.express as px

def ec_collection():
    """
    Generates the layout for the eCommerce collection analysis page.

    Returns:
        dash.html.Div: Layout for the page.
    """
    # Get the processed collection data from Flask's config
    collection_data = current_app.config.get('ec_collection_data')

    if collection_data is None or collection_data.empty:
        return html.Div(
            [
                html.H1("Collection Analysis", style={"textAlign": "center"}),
                html.P("No data available for collection analysis.", style={"textAlign": "center"}),
            ],
            style={"padding": "20px"},
        )

    # Filter out '90PKT Harem Pants' for the scatter plot
    filtered_collection_data = collection_data[
        collection_data["Collection"] != "90PKT Harem Pants"
    ]

    # Create scatter plot of Quantity Sold vs. Total Revenue by Collection
    scatter_fig = px.scatter(
        filtered_collection_data,
        x="Quantity",  # X-axis: Quantity Sold
        y="Subtotal",  # Y-axis: Total Revenue
        size="Number of Orders",  # Bubble size: Number of Orders
        color="Category",  # Set color by Category
        hover_name="Collection",  # Hover info: Collection name
        title="Collection Performance: Quantity Sold vs. Total Revenue",
        labels={
            "Quantity": "Quantity Sold",
            "Subtotal": "Total Revenue",
            "Collection": "Collection",
            "Number of Orders": "Number of Orders",
            "Category": "Category",
        },
    )

    # Customize layout and style
    scatter_fig.update_layout(
        xaxis_title="Quantity Sold",
        yaxis_title="Total Revenue",
        title_x=0.5,
    )

    # Create page layout
    return html.Div(
        [
            html.H1("Collection Analysis", style={"textAlign": "center"}),

            # Add descriptive text for the scatter plot
            dcc.Markdown(
                """
                This scatter plot visualizes the performance of collections based on Quantity Sold and Total Revenue.

                **Features of the plot:**
                 **x-axis**: Total Quantity Sold for the collection.
                 **y-axis**: Total Revenue generated by the collection.
                 **Point size**: Reflects the number of orders the collection appears in. Larger points indicate collections with higher order counts.
                 **Point color**: Represents the `Category` of the collection, differentiating between various product categories.

                *Note*: The collection '90PKT Harem Pants' has been excluded from this visualization for better clarity.
                """,
                style={"textAlign": "center", "marginTop": "20px", "lineHeight": "1.5"},
            ),

            # Plotly scatter plot
            html.H2("Performance Overview", style={"textAlign": "center", "marginTop": "40px"}),
            dcc.Graph(figure=scatter_fig, style={"marginTop": "20px"}),

            # Data Table
            html.H2("Collection Data Summary", style={"textAlign": "center", "marginTop": "40px"}),
            dmc.Table(
                [
                    html.Thead(
                        html.Tr(
                            [
                                html.Th("Collection"),
                                html.Th("Total Revenue"),
                                html.Th("Quantity Sold"),
                                html.Th("Avg Revenue per Unit"),
                                html.Th("Number of Orders"),
                            ]
                        )
                    ),
                    html.Tbody(
                        [
                            html.Tr(
                                [
                                    html.Td(row["Collection"]),
                                    html.Td(f"${row['Subtotal']:,.2f}"),
                                    html.Td(f"{row['Quantity']:,}"),
                                    html.Td(f"${row['Avg Revenue per Unit']:,.2f}"),
                                    html.Td(f"{row['Number of Orders']:,}"),
                                ]
                            )
                            for _, row in collection_data.sort_values(by="Subtotal", ascending=False).iterrows()
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
