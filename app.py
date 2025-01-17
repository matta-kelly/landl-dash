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
from pages.wholesale.ws_customer_eval import ws_customer_eval
from pages.wholesale.surf_expo.se_home import se_home
from pages.wholesale.surf_expo.se_customer_eval import se_customer_eval
from pages.wholesale.surf_expo.se_rep_view import se_rep_view
from pages.wholesale.surf_expo.se_shipping_fufillment import se_shipping_fufillment
from pages.ecom.ec_home import ec_home
import os

from components.navbar import generate_navbar  # Import navbar generator
from data_preprocessing.root_processing import process_root_data

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
    title="L&L Dash",
)


# Access the Flask server
server = app.server

# Preload data during initialization
try:
    data_results = process_root_data()  # Call your processing function
    server.config['root_data'] = data_results  # Store the results in Flask's config
    logging.info("Data preloaded successfully and stored in Flask server config.")
except Exception as e:
    logging.error(f"Error during data preloading: {e}")


# Log app initialization
logger.debug("Dash app initialized successfully.")

# Wrap the layout in MantineProvider
app.layout = dmc.MantineProvider(
    id="mantine-provider",
    theme=theme,
    forceColorScheme="light",
    children=[
        dcc.Location(id="url", refresh=False),  # Tracks current URL
        layout.layout,  # Use the layout object from components/layout.py
    ],
)

# Log the application layout setup
logger.debug("Application layout set.")


# Callback for dynamic navbar rendering
@app.callback(
    Output("navbar", "children"),  # Update navbar dynamically
    Input("url", "pathname"),     # Listen for URL changes
)

def update_navbar(pathname):
    logger.debug(f"Updating navbar for pathname: {pathname}")
    navbar_content = generate_navbar(pathname)
    logger.debug(f"Generated navbar content: {navbar_content}")
    return navbar_content

# Callback for dynamic page rendering
@app.callback(
    Output("page-content", "children"),  # Update the page-content container
    Input("url", "pathname"),           # Listen to changes in the URL pathname
)

def render_page_content(pathname):
    try:
        logger.info(f"Routing triggered with pathname: {pathname}")
        if pathname == "/" or pathname == "/home":
            logger.debug("Rendering home page.")
            return home()
        elif pathname == "/wholesale":
            logger.debug("Rendering wholesale home page.")
            return ws_home()
        elif pathname == "/wholesale/shipping":
            logger.debug("Rendering wholesale shipping page.")
            return ws_shipping_fufillment
        elif pathname == "/wholesale/rep-view":
            logger.debug("Rendering wholesale rep view page.")
            return ws_rep_view
        elif pathname == "/wholesale/customer-eval":
            logger.debug("Rendering wholesale customer evaluation page.")
            return ws_customer_eval
        elif pathname == "/wholesale/surf-expo":
            logger.debug("Rendering wholesale surf expo home page.")
            return se_home()
        elif pathname == "/wholesale/surf-expo/customer-eval":
            logger.debug("Rendering wholesale surf expo customer evaluation page.")
            return se_customer_eval
        elif pathname == "/wholesale/surf-expo/rep-view":
            logger.debug("Rendering wholesale surf expo rep view page.")
            return se_rep_view
        elif pathname == "/wholesale/surf-expo/shipping":
            logger.debug("Rendering wholesale surf expo shipping page.")
            return se_shipping_fufillment
        elif pathname == "/ecom":
            logger.debug("Rendering ecom home page.")
            return ec_home()
        else:
            logger.debug("404: Page not found.")
            return html.Div(
                dmc.Text("404: Page not found", ta="center", c="red", size="xl"),
                style={"textAlign": "center", "marginTop": "50px"},
            )
    except Exception as e:
        logger.error(f"Error in render_page_content callback: {e}")
        return html.Div("An error occurred.")

if __name__ == "__main__":
    logger.debug("Starting the Dash app.")
    app.run(host="0.0.0.0", port=8080, debug=True)
