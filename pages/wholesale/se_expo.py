from flask import current_app
from dash import html, dcc
import dash_mantine_components as dmc
import dash_table
import plotly.express as px
from data_preprocessing import se_processing
import pandas as pd


def format_number(value):
    """Format numbers with commas and two decimal places."""
    try:
        return f"{value:,.2f}"
    except ValueError:
        return value  # If formatting fails, return the original value


def se_recap():
    # Process the Surf Expo data
    recap_data = se_processing.process_surf_recap()

    # Extract the data returned from processing
    stats = recap_data["stats"]
    top_items = recap_data["top_items"]
    category_summary = recap_data["category_summary"]
    geospatial_data = recap_data["geospatial_data"]
    # Handle missing `sales_rep_summary` gracefully
    sales_rep_summary = recap_data.get("sales_rep_summary", pd.DataFrame())
    category_comparison = recap_data.get("category_comparison", pd.DataFrame())
    product_comparison = recap_data.get("product_comparison", pd.DataFrame())
    collection_data = recap_data.get("collection_summary", pd.DataFrame())

    #Debug: Print column names to confirm
    print("Category Summary Columns:", category_summary.columns)

    # Ensure the column name consistency
    if "Percent of Total Revenue" not in category_summary.columns:
        total_revenue = category_summary["Sales_Dollar"].sum()
        category_summary["Percent of Total Revenue"] = (
            (category_summary["Sales_Dollar"] / total_revenue) * 100
        )

    # Format the percentage column
    category_summary["Percent of Total Revenue"] = category_summary["Percent of Total Revenue"].apply(
        lambda x: f"{x:.2f}%"
    )

    # Format numeric columns with commas and two decimal places
    numeric_columns = ["Sales_Qty", "Sales_Dollar", "AUR"]
    for col in numeric_columns:
        category_summary[col] = category_summary[col].apply(format_number)


    # Stats Summary Cards
    stats_summary = dmc.Group(
        [
            dmc.Card(
                children=[
                    dmc.Text("Total Orders (Sales)", fw=500, size="lg"),
                    dmc.Text(f"{stats['total_orders']:,}", size="xl", c="blue"),
                ],
                withBorder=True,
                shadow="sm",
                padding="md",
            ),
            dmc.Card(
                children=[
                    dmc.Text("Total Units Sold", fw=500, size="lg"),
                    dmc.Text(f"{stats['total_units']:,}", size="xl", c="green"),
                ],
                withBorder=True,
                shadow="sm",
                padding="md",
            ),
            dmc.Card(
                children=[
                    dmc.Text("Total Revenue (Sales)", fw=500, size="lg"),
                    dmc.Text(f"${stats['total_revenue']:,.2f}", size="xl", c="orange"),
                ],
                withBorder=True,
                shadow="sm",
                padding="md",
            ),
            dmc.Card(
                children=[
                    dmc.Text("Average Unit Retail (AUR)", fw=500, size="lg"),
                    dmc.Text(f"${stats['avg_unit_revenue']:,.2f}", size="xl", c="purple"),
                ],
                withBorder=True,
                shadow="sm",
                padding="md",
            ),
            dmc.Card(
                children=[
                    dmc.Text("Total Quotations", fw=500, size="lg"),
                    dmc.Text(f"{stats['total_quotations']:,}", size="xl", c="cyan"),
                ],
                withBorder=True,
                shadow="sm",
                padding="md",
            ),
            dmc.Card(
                children=[
                    dmc.Text("Revenue in Quotations", fw=500, size="lg"),
                    dmc.Text(f"${stats['revenue_quotations']:,.2f}", size="xl", c="pink"),
                ],
                withBorder=True,
                shadow="sm",
                padding="md",
            ),
        ],
        justify="center",
        gap="xl",
        style={"marginTop": "20px"},
    )


    # Correct column names for the DataTable
    column_headers = {
        "Product Category": "Category",             # Display-friendly name for "Product Category"
        "Sales_Qty": "Quantity Sold",               # Display-friendly name for "Sales_Qty"
        "Sales_Dollar": "Revenue ($)",              # Display-friendly name for "Sales_Dollar"
        "AUR": "Average Unit Revenue (AUR)",        # Display-friendly name for "AUR"
        "Percent of Total Revenue": "Percent of Total Revenue", # Display-friendly name for "% of Total Revenue"
    }

    # Category Summary Table with renamed headers
    category_summary_table = html.Div(
        dash_table.DataTable(
            data=category_summary.to_dict("records"),  # Convert DataFrame to dictionary
            columns=[
                {"name": column_headers[col], "id": col} for col in category_summary.columns
            ],
            style_table={"overflowX": "auto"},
            style_header={
                "backgroundColor": "rgb(30, 30, 30)",
                "color": "white",
                "fontWeight": "bold",
            },
            style_cell={"textAlign": "left", "padding": "10px"},
        ),
        style={"marginBottom": "30px"},
    )

    # Ensure numeric formatting for the comparison table
    if not category_comparison.empty:
        numeric_columns = category_comparison.columns.difference(["Category Group"])
        for col in numeric_columns:
            category_comparison[col] = category_comparison[col].apply(format_number)

    # Category Comparison Table
    category_comparison_table = html.Div()
    if not category_comparison.empty:
        category_comparison_table = html.Div(
            dash_table.DataTable(
                data=category_comparison.to_dict("records"),
                columns=[
                    {"name": col, "id": col} for col in category_comparison.columns
                ],
                style_table={"overflowX": "auto"},
                style_header={
                    "backgroundColor": "rgb(30, 30, 30)",
                    "color": "white",
                    "fontWeight": "bold",
                },
                style_cell={"textAlign": "left", "padding": "10px"},
            ),
            style={"marginBottom": "30px"},
        )

    # Top Items Visualization
    top_items_plot = html.Div()
    if not top_items.empty:
        # Use the correct columns for the plot based on top_items
        top_items_fig = px.bar(
            top_items,
            x="Subtotal",  # Revenue column
            y="Product Category",  # Category column
            color="SPSU25 Status",  # Status column
            orientation="h",
            title="Top Items by Revenue",
            hover_data=["Quantity", "Subtotal"],  # Add quantity and revenue to the hover tooltip
        )
        top_items_fig.update_layout(
            xaxis_title="Revenue ($)",
            yaxis_title="Product Category",
            title_x=0.5,
            margin=dict(l=50, r=50, t=50, b=50),
            template="simple_white",
        )
        top_items_plot = dcc.Graph(figure=top_items_fig, style={"marginBottom": "30px"})

    # Sales Rep Summary Table
    sales_rep_table = html.Div()
    if not sales_rep_summary.empty:
        sales_rep_summary = sales_rep_summary.copy()
        
        # Format numeric columns, including "Total Revenue"
        numeric_columns = ["Revenue in Quotations", "Revenue in Sales", "Total Revenue"]
        for col in numeric_columns:
            sales_rep_summary[col] = sales_rep_summary[col].apply(format_number)

        # Build the DataTable
        sales_rep_table = html.Div(
            dash_table.DataTable(
                data=sales_rep_summary.to_dict("records"),
                columns=[
                    {"name": "Salesperson", "id": "Salesperson"},
                    {"name": "Number of Orders", "id": "Number of Orders"},
                    {"name": "Revenue in Quotations ($)", "id": "Revenue in Quotations"},
                    {"name": "Revenue in Sales ($)", "id": "Revenue in Sales"},
                    {"name": "Total Revenue ($)", "id": "Total Revenue"},  # Add the new column
                ],
                style_table={"overflowX": "auto"},
                style_header={
                    "backgroundColor": "rgb(30, 30, 30)",
                    "color": "white",
                    "fontWeight": "bold",
                },
                style_cell={"textAlign": "left", "padding": "10px"},
            ),
            style={"marginBottom": "30px"},
        )


    # Map Section
    map_section = html.Div()
    if geospatial_data is not None and not geospatial_data.empty:
        # Map full state names to their abbreviations
        state_abbreviation_map = {
            "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA",
            "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE", "Florida": "FL", "Georgia": "GA",
            "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA", "Kansas": "KS",
            "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD", "Massachusetts": "MA",
            "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS", "Missouri": "MO", "Montana": "MT",
            "Nebraska": "NE", "Nevada": "NV", "New Hampshire": "NH", "New Jersey": "NJ", "New Mexico": "NM",
            "New York": "NY", "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK",
            "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC", "South Dakota": "SD",
            "Tennessee": "TN", "Texas": "TX", "Utah": "UT", "Vermont": "VT", "Virginia": "VA", "Washington": "WA",
            "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY"
        }

        geospatial_data["State"] = geospatial_data["State"].map(state_abbreviation_map)
        geospatial_data = geospatial_data.dropna(subset=["State"])
        map_fig = px.choropleth(
            geospatial_data,
            locations="State",
            locationmode="USA-states",
            color="Total_Revenue",
            hover_name="State",
            hover_data={
                "Total_Revenue": ":$.2f",
                "Customer_Count": ":,",
                "Avg_Revenue_Per_Customer": ":$.2f",
            },
            title="Customer Revenue by State",
            color_continuous_scale="Blues",
            scope="usa",
        )
        map_fig.update_layout(
            title_x=0.5,
            margin=dict(l=50, r=50, t=50, b=50),
            geo=dict(bgcolor="rgba(0,0,0,0)"),
            coloraxis_colorbar=dict(title="Revenue ($)", tickformat="$.2f"),
        )
        map_section = dcc.Graph(figure=map_fig, style={"marginTop": "20px"})


    scatter_plot = html.Div()
    if not product_comparison.empty:
        # Create the scatter plot
        scatter_fig = px.scatter(
            product_comparison,
            x="Total Revenue",  # X-axis: Revenue
            y="Profit Margin (%)",  # Y-axis: Profit Margin
            color="Collection",  # Color points by collection
            size="Units Sold",  # Optional: Use size for units sold
            hover_data=["SKU", "Collection", "Total Revenue", "Profit Margin (%)", "Units Sold"],  # Add hover details
            title="Revenue vs. Profit Margin by Collection",
        )

        scatter_fig.update_layout(
            xaxis_title="Total Revenue ($)",
            yaxis_title="Profit Margin (%)",
            title_x=0.5,
            margin=dict(l=50, r=50, t=50, b=50),
            template="simple_white",
        )

    # Add the scatter plot to a Div
    scatter_plot = dcc.Graph(figure=scatter_fig, style={"marginBottom": "30px"})

    

    # Layout
    return html.Div(
        [   
            dmc.Title("Surf Expo Recap", order=1, style={"textAlign": "center", "marginBottom": "30px"}),
            stats_summary,
            html.Hr(),
            dmc.Title("Category Comparison: Jewelry vs. Clothing", order=4, style={"marginTop": "20px"}),
            category_comparison_table,  # Add the new comparison table
            html.Hr(),
            dmc.Title("Revenue vs. Profit Margin", order=4, style={"marginTop": "20px"}),  # Title for scatter plot
            scatter_plot,  # Add scatter plot here
            html.Hr(),
            dmc.Title("Category Summary", order=4, style={"marginTop": "20px"}),
            category_summary_table,
            html.Hr(),
            dmc.Title("Sales Rep Summary", order=4, style={"marginTop": "20px"}),  # Added title
            sales_rep_table,  # Added Sales Rep Table
            html.Hr(),
            dmc.Title("Top Items by Revenue", order=4, style={"marginTop": "20px"}),
            top_items_plot,
            html.Hr(),
            dmc.Title("Customer Revenue by State", order=4, style={"marginTop": "20px"}),
            map_section,
        ],
        style={"padding": "20px"},
    )
