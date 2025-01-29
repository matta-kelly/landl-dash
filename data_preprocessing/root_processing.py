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

# Home page Content
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
        "sku_parent": "SKU (Parent)",
        "sales_date": "Sales Date",
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


def compute_sales_team_revenue_by_week(merged_data):
    """
    Returns a DataFrame of *weekly* total revenue (Subtotal) by Sales Team,
    excluding draft/quotation logic, ensuring Faire & Wholesale orders don't overlap.
    
    Columns returned: ["Sales Week", "Sales Team", "Subtotal"].
      - "Sales Week" is the start-of-week date (Sunday-based by default).
    """
    # --- 1) Load Faire references, identify overlap ---
    faire_orders = pd.read_csv("./data/f-sales-orders.csv")
    faire_orders = faire_orders.rename(columns=lambda x: x.strip())
    faire_refs = set(faire_orders["Order Reference"].unique())

    # --- 2) Separate out Faire (sale only) ---
    faire_data = merged_data[
        (merged_data["Order Reference"].isin(faire_refs)) &
        (merged_data["Order Status"] == "sale")
    ]
    faire_grouped = faire_data.groupby("Sales Date", as_index=False)["Subtotal"].sum()
    faire_grouped["Sales Team"] = "Faire"

    # --- 3) Wholesale (exclude Faire overlap) ---
    wholesale_data = merged_data[
        (merged_data["Sales Team"] == "Wholesale") &
        (~merged_data["Order Reference"].isin(faire_refs)) &
        (merged_data["Order Status"] == "sale")
    ]
    wholesale_grouped = wholesale_data.groupby("Sales Date", as_index=False)["Subtotal"].sum()
    wholesale_grouped["Sales Team"] = "Wholesale"

    # --- 4) All other teams (excluding Website, Wholesale, Faire) ---
    all_teams = merged_data["Sales Team"].dropna().unique()
    other_teams = [t for t in all_teams if t not in ["Website", "Wholesale", "Faire"]]

    df_list = [faire_grouped, wholesale_grouped]

    for team in other_teams:
        team_data = merged_data[
            (merged_data["Sales Team"] == team) &
            (merged_data["Order Status"] == "sale")
        ]
        grouped = team_data.groupby("Sales Date", as_index=False)["Subtotal"].sum()
        grouped["Sales Team"] = team
        df_list.append(grouped)

    # Combine all channels into a single DataFrame
    channel_stats_dates = pd.concat(df_list, ignore_index=True)

    # Convert Sales Date to proper datetime
    channel_stats_dates["Sales Date"] = pd.to_datetime(channel_stats_dates["Sales Date"], errors="coerce")

    # --- 5) Filter out future dates (past "today") ---
    today = pd.to_datetime("today").normalize()
    channel_stats_dates = channel_stats_dates[channel_stats_dates["Sales Date"] <= today]

    # --- 6) Convert daily dates to weekly buckets ---
    #    (Sunday-based by default, but you can customize with "W-MON" if needed)
    channel_stats_dates["Sales Week"] = channel_stats_dates["Sales Date"].dt.to_period("W")
    channel_stats_dates["Sales Week"] = channel_stats_dates["Sales Week"].apply(lambda r: r.start_time)

    # --- 7) Group by (Sales Week, Sales Team), summing Subtotal ---
    weekly_revenue = (
        channel_stats_dates
        .groupby(["Sales Week", "Sales Team"], as_index=False)["Subtotal"]
        .sum()
    )

    return weekly_revenue



### - Overview pages
def channel_comparison(merged_data):
    """
    Create DataFrames for the top 10 parent SKUs and top 10 collections for eCommerce, Wholesale, and Faire channels.

    Args:
        merged_data (pd.DataFrame): The merged data containing all sales data.

    Returns:
        dict: A dictionary containing six DataFrames:
            - 'ecom_top_10': Top 10 parent SKUs for eCommerce
            - 'wholesale_top_10': Top 10 parent SKUs for Wholesale
            - 'faire_top_10': Top 10 parent SKUs for Faire
            - 'ecom_top_collections': Top 10 collections for eCommerce
            - 'wholesale_top_collections': Top 10 collections for Wholesale
            - 'faire_top_collections': Top 10 collections for Faire
    """
    

    # Filter data by Sales Team
    ecom_data = merged_data[merged_data["Sales Team"] == "Shopify"]
    wholesale_data = merged_data[merged_data["Sales Team"] == "Wholesale"]

    # Faire is herry- Rigged a bit
    faire_orders = pd.read_csv('./data/f-sales-orders.csv')
    faire_orders = faire_orders.rename(columns=lambda x: x.strip())  # Strip whitespace from columns
    faire_order_references = faire_orders["Order Reference"].unique()  # List of relevant order references
    faire_data = merged_data[merged_data["Order Reference"].isin(faire_order_references)]
    

    # Top 10 parent SKUs for each channel
    ecom_top_10 = (
        ecom_data.groupby("SKU (Parent)")
        .agg({"Quantity": "sum", "Subtotal": "sum"})
        .sort_values(by="Subtotal", ascending=False)
        .head(10)
        .reset_index()
    )

    wholesale_top_10 = (
        wholesale_data.groupby("SKU (Parent)")
        .agg({"Quantity": "sum", "Subtotal": "sum"})
        .sort_values(by="Subtotal", ascending=False)
        .head(10)
        .reset_index()
    )

    faire_top_10 = (
        faire_data.groupby("SKU (Parent)")
        .agg({"Quantity": "sum", "Subtotal": "sum"})
        .sort_values(by="Subtotal", ascending=False)
        .head(10)
        .reset_index()
    )

    # Top 10 collections for each channel
    ecom_top_collections = (
        ecom_data.groupby("Collection")
        .agg({"Quantity": "sum", "Subtotal": "sum"})
        .sort_values(by="Subtotal", ascending=False)
        .head(10)
        .reset_index()
    )

    wholesale_top_collections = (
        wholesale_data.groupby("Collection")
        .agg({"Quantity": "sum", "Subtotal": "sum"})
        .sort_values(by="Subtotal", ascending=False)
        .head(10)
        .reset_index()
    )

    faire_top_collections = (
        faire_data.groupby("Collection")
        .agg({"Quantity": "sum", "Subtotal": "sum"})
        .sort_values(by="Subtotal", ascending=False)
        .head(10)
        .reset_index()
    )

    return {
        # Top 10 parent SKUs
        "ecom_top_10": ecom_top_10,
        "wholesale_top_10": wholesale_top_10,
        "faire_top_10": faire_top_10,
        # Top 10 collections
        "ecom_top_collections": ecom_top_collections,
        "wholesale_top_collections": wholesale_top_collections,
        "faire_top_collections": faire_top_collections,
    }



# - Main processing loop
def process_root_data():
    """
    Load, process, and compute statistics. This function merges data and calculates the required statistics.
    
    Returns:
        dict: A dictionary containing the computed statistics, merged data, and channel comparisons.
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

        # 4. Generate channel comparison DataFrames
        channel_comparison_data = channel_comparison(merged_data)

        channel_stats_weeks = compute_sales_team_revenue_by_week(merged_data)

        # 5. Return a dictionary containing the statistics, merged data, and channel comparison data
        return {
            "stats": stats,
            "merged_data": merged_data,
            "channel_comparison": channel_comparison_data,
            "channel_stats_weeks": channel_stats_weeks,
        }

    except Exception as e:
        logger.error(f"Error processing data: {e}")
        raise


