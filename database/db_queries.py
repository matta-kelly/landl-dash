import sqlite3
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Database file
DB_FILE = "data_app.db"

def insert_data_into_db(data):
    """
    Insert processed data into the database.

    Args:
        data (dict): Dictionary of DataFrames to be inserted into the database.
    """
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        # Clean column names to avoid any leading/trailing spaces
        if 'sale_order_line' in data:
            sale_order_line = data['sale_order_line']
            sale_order_line.columns = sale_order_line.columns.str.strip()  # Remove any spaces
            for _, row in sale_order_line.iterrows():
                cursor.execute(
                    """
                    INSERT INTO sale_order_line (order_reference, sku, product, collection, product_template, product_category,
                                                 fabric_sku, fabric_type, quantity, subtotal, total_cost, unit_cost, unit_price,
                                                 order_status, invoice_status, delivery_status)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        row.get("Order Reference"),
                        row.get("SKU"),
                        row.get("Product"),
                        row.get("Collection"),
                        row.get("Product Template"),
                        row.get("Product Category"),
                        row.get("Fabric SKU"),
                        row.get("Fabric Type"),
                        row.get("Quantity"),
                        row.get("Subtotal"),
                        row.get("Total Cost"),
                        row.get("Unit Cost"),
                        row.get("Unit Price"),
                        row.get("Order Status"),
                        row.get("Invoice Status"),
                        row.get("Delivery Status"),
                    ),
                )
        else:
            logger.error("Missing or empty sale_order_line DataFrame.")

        if 'master_sku' in data:
            master_sku = data['master_sku']
            master_sku.columns = master_sku.columns.str.strip()  # Remove any spaces in the column names
            for _, row in master_sku.iterrows():
                cursor.execute(
                    """
                    INSERT OR REPLACE INTO master_sku (collection, fabric_code, sku_parent, sku, name, season, faho24_status, spsu25_status, 
                                                       sold_by_info, carded_non_carded, card_properties, properties, stones, color, 
                                                       cord_print_pattern, material, length, size, size_abbreviation, unit_cost, ws_price, 
                                                       ec_price, weight_lbs, upc, min_qty, ws_sku, ec_sku, amazon_sku, vendor, bom_category, 
                                                       yards_per_unit, labor_cost, card_sku, prefix, prepack_sku, prepack_assortment_qty, available_sizes)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        row.get("Collection"),
                        row.get("Fabric Code"),
                        row.get("SKU (Parent)"),
                        row.get("SKU"),
                        row.get("Name"),
                        row.get("Season"),
                        row.get("FAHO24 Status"),
                        row.get("SPSU25 Status"),
                        row.get("Sold by Info"),
                        row.get("Carded / Non-Carded"),
                        row.get("CARD PROPERTIES"),
                        row.get("Properties"),
                        row.get("Stones"),
                        row.get("Color"),
                        row.get("CORD/PRINT/PATTERN"),
                        row.get("Material"),
                        row.get("Length"),
                        row.get("Size"),
                        row.get("Size Abbreviation"),
                        row.get("Unit Cost"),
                        row.get("WS ($)"),
                        row.get("EC ($)"),
                        row.get("WEIGHT (LBS)"),
                        row.get("UPC"),
                        row.get("MIN. QTY"),
                        row.get("WS SKU?"),
                        row.get("EC SKU?"),
                        row.get("Amazon SKU"),
                        row.get("Vendor"),
                        row.get("BOM Category"),
                        row.get("Yards Per Unit"),
                        row.get("Labor Cost"),
                        row.get("Card SKU"),
                        row.get("Prefix"),
                        row.get("Prepack SKU"),
                        row.get("Prepack Assortment QTY"),
                        row.get("Available Sizes"),
                    ),
                )
        else:
            logger.error("Missing or empty master_sku DataFrame.")

        conn.commit()
        conn.close()
        logger.info("Data successfully inserted into the database.")
    except Exception as e:
        logger.error(f"Failed to insert data into the database: {e}")
        raise



### Not used yet
def fetch_filtered_data(query, params=None):
    """
    Fetch filtered data from the database based on a query.

    Args:
        query (str): SQL query string.
        params (tuple): Parameters for the query.

    Returns:
        list: Query results.
    """
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        results = cursor.fetchall()
        conn.close()
        return results
    except Exception as e:
        logger.error(f"Failed to fetch data from the database: {e}")
        return []


