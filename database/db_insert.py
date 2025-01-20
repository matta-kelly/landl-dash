import sqlite3
import logging
import pandas as pd

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
                    INSERT INTO sale_order_line (created_on, sales_date, delivery_date, order_reference, sales_team, salesperson, customer, state, sku, 
                                                product, collection, product_template, product_category, fabric_sku, fabric_type, quantity, 
                                                subtotal, total_cost, unit_cost, unit_price, order_status, invoice_status, delivery_status, total_tax)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        row.get("Created on"),          # Corresponds to "created_on"
                        row.get("Sales Date"),          # Corresponds to "sales_date"
                        row.get("Delivery Date"),       # Corresponds to "delivery_date"
                        row.get("Order Reference"),     # Corresponds to "order_reference"
                        row.get("Sales Team"),          # Corresponds to "sales_team"
                        row.get("Salesperson"),         # Corresponds to "salesperson"
                        row.get("Customer"),            # Corresponds to "customer"
                        row.get("State"),               # Corresponds to "state"
                        row.get("SKU"),                 # Corresponds to "sku"
                        row.get("Product"),             # Corresponds to "product"
                        row.get("Collection"),          # Corresponds to "collection"
                        row.get("Product Template"),    # Corresponds to "product_template"
                        row.get("Product Category"),    # Corresponds to "product_category"
                        row.get("Fabric SKU"),          # Corresponds to "fabric_sku"
                        row.get("Fabric Type"),         # Corresponds to "fabric_type"
                        row.get("Quantity"),            # Corresponds to "quantity"
                        row.get("Subtotal"),            # Corresponds to "subtotal"
                        row.get("Total Cost"),          # Corresponds to "total_cost"
                        row.get("Unit Cost"),           # Corresponds to "unit_cost"
                        row.get("Unit Price"),          # Corresponds to "unit_price"
                        row.get("Order Status"),       # Corresponds to "order_status"
                        row.get("Invoice Status"),     # Corresponds to "invoice_status"
                        row.get("Delivery Status"),    # Corresponds to "delivery_status"
                        row.get("Total Tax"),           # Corresponds to "total_tax"
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
                    INSERT OR REPLACE INTO master_sku (ws_ship_date, release_month, category_group, category, sub_category, collection, fabric_code, sku_parent, sku, name, season, spsu25_status, 
                                                       sold_by_info, carded_non_carded, card_properties, properties, stones, color, 
                                                       cord_print_pattern, material, length, size, size_abbreviation, unit_cost, ws_price, 
                                                       ec_price, weight_lbs, upc, ws_sku, ec_sku, amazon_sku, vendor, 
                                                       yards_per_unit, labor_cost, prefix, prepack_sku, available_sizes)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        row.get("WS Ship Date"),
                        row.get("Release Month"),
                        row.get("Category Group"),
                        row.get("Category"),
                        row.get("Sub-Category"),
                        row.get("Collection"),
                        row.get("Fabric Code"),
                        row.get("SKU (Parent)"),
                        row.get("SKU"),
                        row.get("Name"),
                        row.get("Season"),
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
                        row.get("WS SKU?"),
                        row.get("EC SKU?"),
                        row.get("Amazon SKU"),
                        row.get("Vendor"),
                        row.get("Yards Per Unit"),
                        row.get("Labor Cost"),
                        row.get("Prefix"),
                        row.get("Prepack SKU"),
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

# CHECKER
def save_sql_table_to_csv(table_name, csv_file_path):
    """
    Save the content of an SQL table to a CSV file.
    
    Args:
        table_name (str): Name of the SQL table to export.
        csv_file_path (str): Path to save the CSV file.
    """
    try:
        # Connect to the database
        conn = sqlite3.connect(DB_FILE)
        
        # Query the entire table
        query = f"SELECT * FROM {table_name};"
        df = pd.read_sql_query(query, conn)
        
        # Save the DataFrame to a CSV
        df.to_csv(csv_file_path, index=False)
        
        print(f"Successfully saved {table_name} to {csv_file_path}")
        conn.close()
    except Exception as e:
        print(f"Error saving {table_name} to CSV: {e}")


