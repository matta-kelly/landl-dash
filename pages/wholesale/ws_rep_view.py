from dash import html
import dash_mantine_components as dmc
from flask import current_app

def ws_rep_view():
    """
    Generates the layout for the Wholesale Rep View page with improved table styling,
    including totals per rep in the far-right column.

    Returns:
        dash.html.Div: Layout for the page.
    """
    rep_summary = current_app.config.get('wholesale_rep_summary')


    if rep_summary is None or rep_summary.empty:
        return html.Div(
            [
                html.H1("Welcome to the Wholesale Rep View Page", style={"textAlign": "center"}),
                html.H2(
                    "No data available for Rep View at this time.",
                    style={"textAlign": "center", "color": "gray", "marginTop": "20px"},
                ),
            ]
        )

    # Prepare the data
    rep_summary_reset = rep_summary.reset_index()

    # Ensure all column names are strings and formatted properly
    rep_summary_reset.columns = [
        " ".join(map(str, col)) if isinstance(col, tuple) else str(col)
        for col in rep_summary_reset.columns
    ]

    # Rename columns for clarity
    renamed_columns = {
        col: col.replace("Quotation", "Quotation Amount")
                .replace("Revenue", "Revenue Amount")
                .replace("-", " ")
        for col in rep_summary_reset.columns if col != "Salesperson"
    }
    rep_summary_reset.rename(columns=renamed_columns, inplace=True)

    # Add totals for each rep as a new column
    rep_summary_reset["Total Quotation $"] = rep_summary_reset.filter(like="Quotation").sum(axis=1)
    rep_summary_reset["Total Revenue $"] = rep_summary_reset.filter(like="Revenue").sum(axis=1)

    # Prepare table headers and rows
    table_columns = [
        html.Th(col, style={"border": "1px solid black", "padding": "10px", "textAlign": "center", "backgroundColor": "#f0f0f0"})
        for col in rep_summary_reset.columns
    ]
    table_rows = [
        html.Tr(
            [
                html.Td(
                    f"${cell:,.2f}" if isinstance(cell, (float, int)) else cell,
                    style={"border": "1px solid black", "padding": "8px", "textAlign": "center"},
                )
                for cell in row
            ],
            style={"backgroundColor": "#ffffff" if i % 2 == 0 else "#f9f9f9"}
        )
        for i, row in enumerate(rep_summary_reset.itertuples(index=False, name=None))
    ]

    # Add totals row at the bottom
    totals = rep_summary_reset.iloc[:, 1:].sum()
    totals_row = html.Tr(
        [html.Td("Total", style={"fontWeight": "bold", "border": "1px solid black", "padding": "8px", "textAlign": "center"})]
        + [
            html.Td(
                f"${totals[col]:,.2f}",
                style={
                    "fontWeight": "bold",
                    "border": "1px solid black",
                    "padding": "8px",
                    "textAlign": "center",
                    "backgroundColor": "#e0f7fa",
                },
            )
            for col in totals.index
        ],
        style={"backgroundColor": "#e0f7fa"}
    )
    table_rows.append(totals_row)

    # Create the layout
    return html.Div(
        [
            html.H1("Wholesale Rep View", style={"textAlign": "center"}),

            html.H2("Monthly Summary by Sales Rep", style={"textAlign": "center", "marginTop": "20px"}),

            # Table displaying the rep summary
            dmc.Table(
                [
                    html.Thead(html.Tr(table_columns)),
                    html.Tbody(table_rows),
                ],
                striped=False,
                highlightOnHover=False,
                withTableBorder=False,
                withColumnBorders=False,
                style={"margin": "0 auto", "width": "90%", "marginTop": "20px", "borderCollapse": "collapse"},
            ),
        ],
        style={"padding": "20px"},
    )
