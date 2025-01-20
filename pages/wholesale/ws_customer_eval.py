from dash import html, dcc
import plotly.express as px
import plotly.graph_objects as go
from flask import current_app

def ws_customer_eval():
    """
    Generates the layout for the Wholesale Customer Evaluation page, including:
    - Scatter plot for Revenue vs. IMU.
    - Map for geospatial analysis.
    - Segmentation insights (Radar Chart and Clustered Scatter Plot).

    Returns:
        dash.html.Div: Layout for the page.
    """

    # Access individual components if needed
    customer_scatter_data = current_app.config.get('wholesale_customer_scatter_data')
    geospatial_data = current_app.config.get('wholesale_geospatial_data')
    customer_segmentation_data = current_app.config.get('wholesale_customer_segmentation_data')

    # Scatter Plot Section
    scatter_section = html.Div()
    scatter_description = html.P()
    if customer_scatter_data is not None and not customer_scatter_data.empty:
        scatter_fig = px.scatter(
            customer_scatter_data,
            x="Total Revenue",
            y="IMU (%)",
            size="AOV",
            color="Order Frequency",
            hover_data=["Customer", "Order Frequency", "AOV"],
            title="Customer Revenue vs. IMU Analysis",
        )
        scatter_fig.update_layout(
            title_x=0.5,
            xaxis_title="Total Revenue ($)",
            yaxis_title="Profit Margin (IMU %)",
            template="simple_white",
            margin=dict(l=50, r=50, t=50, b=50),
            coloraxis_colorbar=dict(title="Order Frequency"),
        )
        scatter_fig.update_traces(marker=dict(opacity=0.7, line=dict(width=0.5, color="black")))
        scatter_section = dcc.Graph(figure=scatter_fig, style={"marginTop": "20px"})

        scatter_description = html.P(
            "The scatter plot visualizes customers with Total Revenue on the x-axis and IMU (Initial Markup Percentage) on "
            "the y-axis. Each bubble represents a customer, with the size of the bubble corresponding to the Average Order "
            "Value (AOV). The color of the bubbles represents the Order Frequency, transitioning from lighter to darker shades "
            "as frequency increases. Hovering over a bubble reveals detailed information about the customer, including their "
            "name, AOV, and order frequency. The layout uses a clean white background to ensure clarity."
        )

    # Map Section
    map_section = html.Div()
    map_description = html.P()
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

        map_description = html.P(
            "The choropleth map displays revenue distribution across the United States, with each state's color intensity "
            "corresponding to its Total Revenue. Darker shades of blue indicate higher revenue, while lighter shades represent "
            "lower revenue. Hovering over a state reveals additional details, including the total revenue, number of customers, "
            "and average revenue per customer. The map is confined to the USA for regional focus and uses a clean color palette "
            "for readability."
        )

    # Segmentation Insights Section
    segmentation_section = html.Div()
    segmentation_description = html.P()
    if customer_segmentation_data is not None and not customer_segmentation_data.empty:
        # Radar Chart for Cluster Insights
        cluster_summary = customer_segmentation_data.groupby("Cluster").agg(
            {
                "Total Revenue (Standardized)": "mean",
                "AOV (Standardized)": "mean",
                "IMU (%) (Standardized)": "mean",
                "Order Frequency (Standardized)": "mean",
            }
        ).reset_index()

        radar_fig = go.Figure()
        metrics = ["Total Revenue (Standardized)", "AOV (Standardized)", "IMU (%) (Standardized)", "Order Frequency (Standardized)"]
        for _, row in cluster_summary.iterrows():
            radar_fig.add_trace(
                go.Scatterpolar(
                    r=[row[metric] for metric in metrics],
                    theta=metrics,
                    fill='toself',
                    name=f"Cluster {int(row['Cluster'])}",
                )
            )
        radar_fig.update_layout(
            polar=dict(radialaxis=dict(visible=True)),
            title="Cluster Insights (Radar Chart)",
            showlegend=True,
        )
        radar_chart = dcc.Graph(figure=radar_fig, style={"marginTop": "20px"})

        # Scatter Plot for Clusters
        scatter_cluster_fig = px.scatter(
            customer_segmentation_data,
            x="Total Revenue",
            y="IMU (%)",
            color="Cluster",
            size="AOV",
            hover_data=["Customer", "Order Frequency", "Cluster"],
            title="Clustered Customer Scatter Plot",
        )
        scatter_cluster_fig.update_layout(
            title_x=0.5,
            xaxis_title="Total Revenue ($)",
            yaxis_title="Profit Margin (IMU %)",
            template="simple_white",
        )
        cluster_scatter_plot = dcc.Graph(figure=scatter_cluster_fig, style={"marginTop": "20px"})

        segmentation_section = html.Div(
            [
                html.H2("Customer Segmentation Insights", style={"textAlign": "center", "marginTop": "40px"}),
                radar_chart,
                cluster_scatter_plot,
            ]
        )

        segmentation_description = html.P(
            "The radar chart highlights the average values of standardized metrics (Total Revenue, AOV, IMU %, and Order "
            "Frequency) for each customer cluster, with each axis representing a metric. The clustered scatter plot visualizes "
            "individual customers with Total Revenue on the x-axis and IMU (%) on the y-axis. Bubble sizes correspond to AOV, "
            "and colors represent cluster assignments, helping distinguish customer groups based on behavior."
        )

    # Page Layout
    return html.Div(
        [
            html.H1("Wholesale Customer Evaluation", style={"textAlign": "center"}),

            html.H2("Revenue vs. IMU Analysis", style={"textAlign": "center", "marginTop": "20px"}),
            scatter_section,
            scatter_description,

            html.H2("Customer Revenue by State", style={"textAlign": "center", "marginTop": "40px"}),
            map_section,
            map_description,

            segmentation_section,
            segmentation_description,
        ],
        style={"padding": "20px"},
    )
