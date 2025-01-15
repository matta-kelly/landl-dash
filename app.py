import logging
import dash
from dash import Dash, dcc, html, Output, Input
import dash_mantine_components as dmc
from theme import theme
from components.theme_toggle import theme_toggle
from components import layout
from pages.home import home
from pages.wholesale.ws_home import ws_home
from pages.wholesale.ws_shipping_fufillment import ws_shipping_fufillment
from pages.wholesale.ws_rep_view import ws_rep_view
import os

# Disable file watching for Dash
os.environ["DASH_NO_DEV_TOOLS"] = "1"


# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize the Dash app with external React libraries
app = dash.Dash(
    __name__,
    external_scripts=[
        "https://unpkg.com/react@18/umd/react.development.js",
        "https://unpkg.com/react-dom@18/umd/react-dom.development.js"
    ],
    suppress_callback_exceptions=True,
    update_title="Loading...",
    title="Wholesale Dashboard",
)

# Log app initialization
logger.debug("Dash app initialized successfully.")

# Wrap the layout in MantineProvider
app.layout = dmc.MantineProvider(
    id="mantine-provider",
    theme=theme,
    forceColorScheme="light",
    children=[
        dcc.Location(id="url", refresh=False),  # Tracks current URL
        dmc.Text(id="debug-pathname"),  # Display current pathname for debugging
        layout.layout,  # Use the layout object from components/layout.py
    ],
)

# Log the application layout setup
logger.debug("Application layout set.")


# Callback for dynamic page rendering
@app.callback(
    Output("page-content", "children"),  # Update the page-content container
    [Input("url", "pathname")],         # Listen to changes in the URL pathname
)
def render_page_content(pathname):
    return display_page(pathname)

def display_page(pathname):
    try:
        logger.info(f"Routing triggered with pathname: {pathname}")
        if not pathname or pathname == "/":
            logger.debug("Rendering home page.")
            return home
        elif pathname == "/wholesale":
            logger.debug("Rendering wholesale home page.")
            return ws_home
        elif pathname == "/wholesale/shipping":
            logger.debug("Rendering wholesale shipping page.")
            return ws_shipping_fufillment
        elif pathname == "/wholesale/rep-view":
            logger.debug("Rendering wholesale rep view page.")
            return ws_rep_view
        else:
            logger.debug("404: Page not found.")
            return html.Div(
                dmc.Text("404: Page not found", ta="center", c="red", size="xl"),
                style={"textAlign": "center", "marginTop": "50px"},
            )
    except Exception as e:
        logger.error(f"Error in display_page callback: {e}")
        return html.Div("An error occurred.")

if __name__ == "__main__":
    logger.debug("Starting the Dash app.")
    app.run(debug=True)
