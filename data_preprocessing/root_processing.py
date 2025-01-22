import sqlite3
import pandas as pd
import logging

# Configure logging
logger = logging.getLogger(__name__)

DB_FILE = "data_app.db"  # Path to your SQLite database

def query_db(query, params=None):
    """
    Execute a query on the database and return the results as a list of dictionaries.
    
    Args:
        query (str): The SQL query to be executed.
        params (tuple): Optional parameters to bind to the query.
        
    Returns:
        list: A list of rows from the database, each row as a dictionary.
    """
    try:
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        cursor = conn.cursor()
        cursor.execute(query, params or [])
        results = cursor.fetchall()
        # Extract column names from the cursor description
        columns = [col[0] for col in cursor.description]
        conn.close()
        
        # Return results with correct column names
        return results, columns
    except Exception as e:
        logger.error(f"Failed to execute query: {e}")
        raise


def merge_master_sku():
    """
    Merge `sale_order_line` with `master_sku` using an SQL LEFT JOIN.
    Fetches sale order data and related master SKU details like SPSU25 Status, Category Group, and SKU Parent.

    Returns:
        pd.DataFrame: A DataFrame with merged data from sale_order_line and master_sku.
    """
    query = """
    SELECT 
        sale_order_line.*, 
        master_sku.spsu25_status, 
        master_sku.category_group, 
        master_sku.sku_parent,
        master_sku.category
    FROM sale_order_line
    LEFT JOIN master_sku 
        ON sale_order_line.sku = master_sku.sku;
    """
    merged_data, columns = query_db(query)
    merged_data_df = pd.DataFrame(merged_data, columns=columns)

    return merged_data_df


def rename_columns(merged_data_df):
    """
    Rename the columns of the merged DataFrame to match the expected naming convention for the app.

    Args:
        merged_data_df (pd.DataFrame): The merged data to rename columns for.

    Returns:
        pd.DataFrame: The DataFrame with renamed columns.
    """
    merged_data_df.rename(columns={
        "order_reference": "Order Reference",
        "delivery_date": "Delivery Date",
        "sales_team": "Sales Team",
        "salesperson": "Salesperson",
        "customer": "Customer",
        "state": "State",
        "sku": "SKU",
        "product": "Product",
        "collection": "Collection",
        "product_template": "Product Template",
        "product_category": "Product Category",
        "fabric_sku": "Fabric SKU",
        "fabric_type": "Fabric Type",
        "quantity": "Quantity",
        "subtotal": "Subtotal",
        "total_cost": "Total Cost",
        "unit_cost": "Unit Cost",
        "unit_price": "Unit Price",
        "order_status": "Order Status",
        "invoice_status": "Invoice Status",
        "delivery_status": "Delivery Status",
        "total_tax": "Total Tax",
        "total": "Total",
        "spsu25_status": "SPSU25 Status",
        "category_group": "Category Group",
        "category": "Category",
        "sku_parent": "SKU (Parent)"
    }, inplace=True)

    return merged_data_df


def compute_statistics(merged_data):
    """
    Compute key statistics from the merged DataFrame.

    Args:
        merged_data (pd.DataFrame): The merged data to compute statistics from.

    Returns:
        dict: A dictionary with computed statistics.
    """
    stats = {}

    # 1. Total orders: Count of unique "Order Reference"
    stats["total_orders"] = merged_data["Order Reference"].nunique()

    # 2. Total revenue for 'sale' orders
    stats["total_revenue_sold"] = merged_data[merged_data["Order Status"] == "sale"]["Subtotal"].sum()

    # 3. Total revenue for 'draft' orders (quotations)
    stats["total_revenue_quotation"] = merged_data[merged_data["Order Status"] == "draft"]["Subtotal"].sum()

    # 4. Average order value (for 'sale' orders)
    avg_order_value = merged_data[merged_data["Order Status"] == "sale"].groupby("Order Reference")["Subtotal"].sum().mean()
    stats["avg_order_value"] = avg_order_value

    # 5. Top-selling product (by quantity)
    top_selling_product = merged_data.groupby("SKU")["Quantity"].sum().idxmax()
    stats["top_selling_product"] = top_selling_product

    return stats


def process_root_data():
    """
    Load, process, and compute statistics. This function merges data and calculates the required statistics.
    
    Returns:
        dict: A dictionary containing the computed statistics and merged data.
    """
    try:
        # 1. Merge sale_order_line with master_sku
        merged_data = merge_master_sku()

        # 2. Rename columns for consistency
        merged_data = rename_columns(merged_data)

        merged_data.to_csv("./data/merged_data_inspection.csv", index=False)
        print("Loaded wholesale data from CSV for testing.")

        # 3. Compute statistics based on the merged data
        stats = compute_statistics(merged_data)

        # 4. Return a dictionary containing the statistics and merged data
        return {
            "stats": stats,
            "merged_data": merged_data
        }

    except Exception as e:
        logger.error(f"Error processing data: {e}")
        raise


if __name__ == "__main__":
    # Process data and retrieve results
    results = process_root_data()

    # Display results for debugging
    print("Statistics:")
    print(results["stats"])
    print("\nMerged Data Preview:")
    print(results["merged_data"].head())  # Display first 5 rows for preview
