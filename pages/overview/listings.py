from flask import current_app
from dash import html
import dash_mantine_components as dmc
from data_preprocessing import listing_preprocessing

def listing():
    # Process the data
    data = listing_preprocessing.process_listing_data()

    # Extract statistics DataFrame
    stats_df = data["stats"]

    # Convert DataFrame to a Dash Mantine Table with enhanced styling
    table_header = html.Table(
        [
            html.Thead(
                html.Tr([
                    html.Th("Platform", style={"text-align": "left", "padding": "10px", "font-weight": "bold"}),
                    html.Th("Published", style={"text-align": "center", "padding": "10px", "font-weight": "bold"}),
                    html.Th("Unpublished", style={"text-align": "center", "padding": "10px", "font-weight": "bold"})
                ])
            ),
            html.Tbody(
                [
                    html.Tr([
                        html.Td(row["Platform"], style={"text-align": "left", "padding": "10px"}),
                        html.Td(row["Published"], style={"text-align": "center", "padding": "10px"}),
                        html.Td(row["Unpublished"], style={"text-align": "center", "padding": "10px"})
                    ])
                    for _, row in stats_df.iterrows()
                ]
            )
        ],
        style={
            "border-collapse": "collapse", 
            "width": "100%", 
            "font-family": "Arial, sans-serif", 
            "border": "1px solid #ddd", 
            "box-shadow": "0px 2px 4px rgba(0, 0, 0, 0.1)"
        }
    )

    # Return the table wrapped in a layout
    return dmc.Container([
        dmc.Title(
            "Listing Statistics", 
            style={"font-size": "24px", "margin-bottom": "20px", "text-align": "center", "font-weight": "600"}
        ),
        table_header
    ])
