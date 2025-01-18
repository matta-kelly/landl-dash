from dash import dcc
import dash_mantine_components as dmc

def date_filter():
    """
    Creates a date picker range component.

    Returns:
        dmc.Group: A Mantine group containing the date picker range.
    """
    return dmc.Group(
        [
            dmc.Text("Filter by Date:", size="md", fw=500, style={"marginRight": "10px"}),  # Use 'fw' for font weight
            dcc.DatePickerRange(
                id="date-picker-range",
                start_date=None,  # Default start date (can be set dynamically later)
                end_date=None,    # Default end date (can be set dynamically later)
                display_format="YYYY-MM-DD",
                style={"border": "1px solid #ccc", "borderRadius": "5px", "padding": "5px"},
            ),
        ],
        justify="right",
        gap="sm",  # Corrected argument for spacing
    )
