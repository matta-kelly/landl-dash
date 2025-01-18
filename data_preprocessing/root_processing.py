import sqlite3
import pandas as pd
import logging

# Configure logging
logger = logging.getLogger(__name__)

DB_FILE = "data_app.db"  # Make sure this points to your database file

def query_db(query, params=None):
    """
    Execute a query on the database and fetch results.
    """
    try:
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        cursor = conn.cursor()
        cursor.execute(query, params or [])
        results = cursor.fetchall()
        conn.close()
        return results
    except Exception as e:
        logger.error(f"Failed to execute query: {e}")
        raise

def merge_spsu25_status():
    """
    Merge sale_order_line with master_sku based on SKU using SQL JOIN.
    """
    query = """
    SELECT 
        sale_order_line.*, 
        master_sku.SPSU25_Status, 
        master_sku.Category_Group, 
        master_sku.SKU_Parent
    FROM sale_order_line
    LEFT JOIN master_sku 
        ON sale_order_line.sku = master_sku.sku;
    """
    merged_data = query_db(query)
    # Convert to DataFrame
    merged_data_df = pd.DataFrame(merged_data)
    return merged_data_df

def compute_statistics(filtered_sale_order_line):
    """
    Compute key statistics from the filtered sale_order_line DataFrame using SQL queries.
    """
    # Total orders
    total_orders_query = "SELECT COUNT(DISTINCT \"Order Reference\") AS total_orders FROM sale_order_line;"
    total_orders = query_db(total_orders_query)[0]["total_orders"]

    # Total revenue sold (Order Status = 'sale')
    total_revenue_sold_query = "SELECT SUM(\"Subtotal\") AS total_revenue_sold FROM sale_order_line WHERE \"Order Status\" = 'sale';"
    total_revenue_sold = query_db(total_revenue_sold_query)[0]["total_revenue_sold"]

    # Total revenue for quotations (Order Status = 'draft')
    total_revenue_quotation_query = "SELECT SUM(\"Subtotal\") AS total_revenue_quotation FROM sale_order_line WHERE \"Order Status\" = 'draft';"
    total_revenue_quotation = query_db(total_revenue_quotation_query)[0]["total_revenue_quotation"]

    # Average order value (sold orders)
    avg_order_value_query = """
    SELECT AVG(SUM("Subtotal")) AS avg_order_value
    FROM sale_order_line
    WHERE "Order Status" = 'sale'
    GROUP BY "Order Reference";
    """
    avg_order_value = query_db(avg_order_value_query)[0]["avg_order_value"]

    # Top-selling product by quantity
    top_selling_product_query = """
    SELECT "SKU", SUM("Quantity") AS total_quantity
    FROM sale_order_line
    GROUP BY "SKU"
    ORDER BY total_quantity DESC
    LIMIT 1;
    """
    top_selling_product = query_db(top_selling_product_query)[0]["SKU"]

    # Return statistics as a dictionary
    return {
        "total_orders": total_orders,
        "total_revenue_sold": total_revenue_sold,
        "total_revenue_quotation": total_revenue_quotation,
        "avg_order_value": avg_order_value,
        "top_selling_product": top_selling_product,
    }

def process_root_data():
    """
    Load and process data, compute statistics, and return cleaned/merged DataFrames and stats.
    """
    try:
        # Merge data from sale_order_line and master_sku
        merged_data = merge_spsu25_status()

        # Compute statistics
        stats = compute_statistics(merged_data)

        # Returning a dictionary to store in Flask config
        return {
            "stats": stats,
            "merged_data": merged_data
        }
    except Exception as e:
        logger.error(f"Error processing data: {e}")
        raise
