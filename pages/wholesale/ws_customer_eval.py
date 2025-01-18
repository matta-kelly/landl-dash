from dash import html, dcc
import plotly.express as px

def ws_customer_eval():
    """
    Generates the layout for the Wholesale Customer Evaluation page with a scatter plot
    for Revenue vs. IMU and a map for geospatial analysis.

    Returns:
        dash.html.Div: Layout for the page.
    """
    # Load processed customer scatter data
    from data_preprocessing.wholesale_processing import process_wholesale_data
    wholesale_data_result = process_wholesale_data()
    customer_scatter_data = wholesale_data_result.get("customer_scatter_data")
    geospatial_data = wholesale_data_result.get("geospatial_data")

    # Verify and handle scatter plot data
    if customer_scatter_data is None or customer_scatter_data.empty:
        scatter_section = html.Div(
            [
                html.H2(
                    "No data available for Customer Scatter Plot at this time.",
                    style={"textAlign": "center", "color": "gray", "marginTop": "20px"},
                )
            ]
        )
    else:
        # Create the scatter plot
        scatter_fig = px.scatter(
            customer_scatter_data,
            x="Total Revenue",
            y="IMU (%)",
            size="AOV",
            color="Order Frequency",
            hover_data=["Customer", "Order Frequency", "AOV"],
            title="Customer Revenue vs. IMU Analysis",
            labels={
                "Total Revenue": "Total Revenue ($)",
                "IMU (%)": "Profit Margin (IMU %)",
                "AOV": "Average Order Value ($)",
                "Order Frequency": "Order Frequency",
            },
        )

        # Update scatter plot layout
        scatter_fig.update_layout(
            title_x=0.5,
            xaxis_title="Total Revenue ($)",
            yaxis_title="Profit Margin (IMU %)",
            template="simple_white",
            margin=dict(l=50, r=50, t=50, b=50),
            coloraxis_colorbar=dict(title="Order Frequency"),
        )

        # Update marker visuals
        scatter_fig.update_traces(marker=dict(opacity=0.7, line=dict(width=0.5, color="black")))

        scatter_section = dcc.Graph(figure=scatter_fig, style={"marginTop": "20px"})

    # Verify and handle map data
    if geospatial_data is None or geospatial_data.empty:
        map_section = html.Div(
            [
                html.H2(
                    "No data available for Geospatial Analysis at this time.",
                    style={"textAlign": "center", "color": "gray", "marginTop": "20px"},
                )
            ]
        )
    else:
        
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

        # Remove invalid or unmapped states
        geospatial_data = geospatial_data.dropna(subset=["State"])

        # Create the choropleth map
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

        # Update map layout
        map_fig.update_layout(
            title_x=0.5,
            margin=dict(l=50, r=50, t=50, b=50),
            geo=dict(bgcolor="rgba(0,0,0,0)"),
            coloraxis_colorbar=dict(title="Revenue ($)", tickformat="$.2f"),
        )

        map_section = dcc.Graph(figure=map_fig, style={"marginTop": "20px"})

    # Page layout
    return html.Div(
        [
            html.H1("Wholesale Customer Evaluation", style={"textAlign": "center"}),

            html.H2("Revenue vs. IMU Analysis", style={"textAlign": "center", "marginTop": "20px"}),

            html.Div(
                [
                    html.P(
                        "The scatter plot provides insights into customer performance by plotting total revenue against profit "
                        "margin (IMU). Each bubble represents a customer, with the size indicating their average order value (AOV) "
                        "and the color reflecting their order frequency. Hovering over a data point reveals details such as the customer's "
                        "total revenue, order frequency, and AOV.",
                        style={"marginTop": "20px", "textAlign": "justify"},
                    ),
                ],
                style={"margin": "20px auto", "width": "80%"},
            ),

            scatter_section,

            html.H2("Customer Revenue by State", style={"textAlign": "center", "marginTop": "40px"}),

            html.Div(
                [
                    html.P(
                        "The map illustrates customer revenue distribution across the United States. States with higher revenue are "
                        "displayed in darker shades, highlighting key regions driving sales. Hover over a state to view detailed metrics, "
                        "including total revenue, customer count, and average revenue per customer.",
                        style={"marginTop": "20px", "textAlign": "justify"},
                    ),
                ],
                style={"margin": "20px auto", "width": "80%"},
            ),

            map_section,
        ],
        style={"padding": "20px"},
    )
