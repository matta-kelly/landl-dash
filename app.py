import logging
import dash
from dash import Dash, dcc, html, Output, Input
import dash_mantine_components as dmc
from components.theme import theme
from data_preprocessing import data_loader
from components.theme_toggle import darkModeToggle
from components import layout
from pages.home import home
from pages.wholesale.ws_home import ws_home
from pages.wholesale.ws_shipping_fufillment import ws_shipping_fulfillment
from pages.wholesale.ws_rep_view import ws_rep_view
from pages.wholesale.ws_customer_eval import ws_customer_eval
from pages.wholesale.ws_product import ws_product
from pages.ecom.ec_home import ec_home
from pages.wholesale.se_expo import se_recap
from database import db_insert, db_setup
import os
import pandas as pd

from components.navbar_links import generate_navbar  # Import navbar generator
from data_preprocessing import root_processing, ecom_processing, wholesale_processing

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

# Initilize DB
try:
    db_setup.initialize_db()  # Creates tables if they don't exist
    logging.info("Database initialized successfully.")
except Exception as e:
    logging.error(f"Failed to initialize the database: {e}")

# Preload data during initialization
try:
    # Load raw data using data_loader
    data = data_loader.load_data()
    
    # Store the processed data in Flask's server config
    db_insert.insert_data_into_db(data)
    logging.info("Data preloaded successfully and stored in SQL DB")

    #Checking
    db_insert.save_sql_table_to_csv("sale_order_line", "./data/sql_sale_order_line.csv")
    db_insert.save_sql_table_to_csv("master_sku", "./data/sql_master_sku.csv")
except Exception as e:
    logging.error(f"Error during data preloading: {e}")
    # Better fallback logic

# Function to set root data
def load_root_data():
    try:
        # Process root data and store it in the app's config
        root_data = root_processing.process_root_data()  # Process the data and return results
        app.server.config['root_data'] = root_data  # Store it in the app config
        logging.info("Root data successfully loaded and stored.")
    except Exception as e:
        logging.error(f"Failed to load root data: {e}")


# Function to set eCommerce data
def load_ecom_data():
    try:
        # Ensure Flask app context is available
        with app.server.app_context():
            # Process eCommerce data and store it in the app's config
            ecom_data_result = ecom_processing.process_ecom_data()  # Process the data and return results

            # Save individual components of the eCommerce data into Flask's config
            app.server.config['ecom_stats'] = ecom_data_result.get("stats")
            app.server.config['ecom_merged_data'] = ecom_data_result.get("merged_data")
            app.server.config['ecom_filtered_sale_order_line'] = ecom_data_result.get("filtered_sale_order_line")

            logging.info("eCommerce data successfully loaded and stored.")
    except Exception as e:
        logging.error(f"Failed to load eCommerce data: {e}")

# Function to set wholesale data
def load_wholesale_data():
    try:
        # Ensure Flask app context is available
        with app.server.app_context():
            # Process wholesale data and store it in the app's config
            wholesale_data_result = wholesale_processing.process_wholesale_data()  # Process the data and return results

            # Save individual components of the wholesale data into Flask's config
            app.server.config['wholesale_stats'] = wholesale_data_result.get("stats")
            app.server.config['wholesale_merged_data'] = wholesale_data_result.get("merged_data")
            app.server.config['wholesale_filtered_sale_order_line'] = wholesale_data_result.get("filtered_sale_order_line")
            app.server.config['wholesale_delivery_distribution'] = wholesale_data_result.get("delivery_distribution")
            app.server.config['wholesale_rep_summary'] = wholesale_data_result.get("rep_summary")
            app.server.config['wholesale_product_profit_analysis'] = wholesale_data_result.get("product_profit_analysis")
            app.server.config['wholesale_customer_scatter_data'] = wholesale_data_result.get("customer_scatter_data")
            app.server.config['wholesale_geospatial_data'] = wholesale_data_result.get("geospatial_data")
            app.server.config['wholesale_customer_segmentation_data'] = wholesale_data_result.get("customer_segmentation_data")

            logging.info("Wholesale data successfully loaded and stored.")
    except Exception as e:
        logging.error(f"Failed to load wholesale data: {e}")

# Ensure this is called before app starts serving requests
load_root_data()
load_ecom_data()
load_wholesale_data()

# Log app initialization
logger.debug("Dash app initialized successfully.")

# Wrap the layout in MantineProvider
app.layout = dmc.MantineProvider(
    id="mantine-provider",
    theme=theme,
    forceColorScheme="light",  # Default light mode
    children=[
        dcc.Store(id="theme-store", data={"theme": "light"}),  # Global theme state
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


# Page path-to-function mapping
page_mapping = {
    "/": home,
    "/home": home,
    "/wholesale": ws_home,
    "/wholesale/shipping": ws_shipping_fulfillment,
    "/wholesale/product": ws_product,
    "/wholesale/rep-view": ws_rep_view,
    "/wholesale/customer-eval": ws_customer_eval,
    "/wholesale/se": se_recap,
    "/ecom": ec_home,
}

# Callback for dynamic page rendering
@app.callback(
    Output("page-content", "children"),  # Update the page-content container
    Input("url", "pathname"),           # Listen to changes in the URL pathname
)

def render_page_content(pathname):
    try:
        logger.info(f"Routing triggered with pathname: {pathname}")
        page = page_mapping.get(pathname, lambda: html.Div(
            dmc.Text("404: Page not found", ta="center", c="red", size="xl"),
            style={"textAlign": "center", "marginTop": "50px"},
        ))
        return page()
    except Exception as e:
        logger.error(f"Error in render_page_content callback: {e}")
        return html.Div("An error occurred.")

    
@app.callback(
    [
        Output("theme-store", "data"),  # Update the theme store
        Output("mantine-provider", "theme"),  # Update the Mantine theme dynamically
        Output("mantine-provider", "forceColorScheme"),  # Update color scheme (light/dark)
        Output("header", "style"),  # Update header style
        Output("header-text", "style"),  # Update header text style
    ],
    Input("themeSwitch", "checked"),  # Listen for changes in the toggle state
)
def update_theme(is_dark_mode):
    """
    Updates the theme for the app and applies corresponding styles.
    """
    if is_dark_mode:
        dark_theme = {
            **theme,  # Base theme
            "colorScheme": "dark",
        }
        header_style = {
            "backgroundColor": "#1a202c",
            "color": "#e2e8f0",
        }
        text_style = {
            "color": "#e2e8f0",
        }
        return {"theme": "dark"}, dark_theme, "dark", header_style, text_style
    else:
        light_theme = {
            **theme,  # Base theme
            "colorScheme": "light",
        }
        header_style = {
            "backgroundColor": "#f8f9fa",
            "color": "#1a202c",
        }
        text_style = {
            "color": "#1a202c",
        }
        return {"theme": "light"}, light_theme, "light", header_style, text_style





if __name__ == "__main__":
    logger.debug("Starting the Dash app.")
    app.run(host="0.0.0.0", port=8080)
