import pandas as pd
import os
import plotly.express as px

# Path to the data folder
DATA_FOLDER = './data'

# File names
FILES = {
    "sku_inventory": "sku-inventory.csv",
    "sales_orders": "sales-orders.csv",
    "sale_order_line": "sale-order-line.csv",
    "master_sku": "master-sku.csv"
}

# Function to load all datasets
def load_datasets(files, folder):
    """
    Load all datasets and return them as a dictionary of DataFrames.

    Args:
        files (dict): Dictionary of file names.
        folder (str): Path to the folder containing the files.

    Returns:
        dict: Dictionary of DataFrames.
    """
    dataframes = {}
    for key, file_name in files.items():
        file_path = os.path.join(folder, file_name)
        try:
            dataframes[key] = pd.read_csv(file_path)
            print(f"Loaded {file_name} successfully.")
        except Exception as e:
            print(f"Error loading {file_name}: {e}")
    return dataframes

# Function to merge SPSU25 Status and Product Category from Master SKU
def merge_spsu25_status(sale_order_line, master_sku):
    """
    Merge SPSU25 Status and Category from master_sku into the sale_order_line DataFrame.

    Args:
        sale_order_line (pd.DataFrame): The sale_order_line DataFrame.
        master_sku (pd.DataFrame): The master_sku DataFrame.

    Returns:
        pd.DataFrame: Merged DataFrame.
    """
    if "SKU" not in sale_order_line.columns or "SKU (Parent)" not in master_sku.columns:
        raise KeyError("Missing SKU columns in one of the DataFrames.")
    
    merged_data = pd.merge(
        sale_order_line,
        master_sku[["SKU", "SPSU25 Status", "Category Group", "SKU (Parent)"]],  # Include Category
        left_on="SKU",
        right_on="SKU",
        how="left"
    )
    return merged_data


# Function to compute statistics
def compute_statistics(filtered_sale_order_line):
    """
    Compute key statistics from the filtered sale_order_line DataFrame.

    Args:
        filtered_sale_order_line (pd.DataFrame): The filtered sale_order_line DataFrame.

    Returns:
        dict: Dictionary of computed statistics.
    """
    if filtered_sale_order_line.empty:
        return {
            "total_orders": 0,
            "total_revenue_sold": 0.0,
            "total_revenue_quotation": 0.0,
            "avg_order_value": 0.0,
            "top_selling_product": "N/A"
        }

    # Total orders (unique order references)
    total_orders = filtered_sale_order_line["Order Reference"].nunique()

    # Total revenue for "sale" status
    total_revenue_sold = filtered_sale_order_line[
        filtered_sale_order_line["Order Status"] == "sale"
    ]["Subtotal"].sum()

    # Total revenue for "draft" status (quotation)
    total_revenue_quotation = filtered_sale_order_line[
        filtered_sale_order_line["Order Status"] == "draft"
    ]["Subtotal"].sum()

    # Average order value (calculated from sold orders)
    avg_order_value = (
        filtered_sale_order_line[
            filtered_sale_order_line["Order Status"] == "sale"
        ].groupby("Order Reference")["Subtotal"].sum().mean()
    )

    # Top-selling product by quantity
    top_selling_product = (
        filtered_sale_order_line.groupby("SKU")["Quantity"].sum().idxmax()
        if not filtered_sale_order_line.empty
        else "N/A"
    )

    return {
        "total_orders": total_orders,
        "total_revenue_sold": total_revenue_sold,
        "total_revenue_quotation": total_revenue_quotation,
        "avg_order_value": avg_order_value,
        "top_selling_product": top_selling_product,
    }


# Function to add Surf Expo column to the merged data
def add_surf_expo_column(merged_data, sales_orders):
    """
    Add a Surf Expo column to the merged data. The column will have True if the
    order reference exists in sales-orders, otherwise False.

    Args:
        merged_data (pd.DataFrame): The merged DataFrame containing all sales data.
        sales_orders (pd.DataFrame): The DataFrame containing sales order data.

    Returns:
        pd.DataFrame: The merged DataFrame with the new Surf Expo column.
    """
    if "Order Reference" not in sales_orders.columns:
        raise KeyError("'Order Reference' column is missing from sales-orders.csv.")
    if "Order Reference" not in merged_data.columns:
        raise KeyError("'Order Reference' column is missing from the merged data.")

    valid_orders = sales_orders["Order Reference"].unique()
    merged_data["Surf Expo"] = merged_data["Order Reference"].isin(valid_orders)
    return merged_data


# Updated process_root_data function
def process_root_data():
    """
    Load and process data, compute statistics, and return cleaned/merged DataFrames and stats.
    Additionally, save the merged DataFrame to a CSV file for inspection.

    Returns:
        dict: Dictionary containing statistics and processed DataFrames.
    """
    # Load datasets
    dataframes = load_datasets(FILES, DATA_FOLDER)

    # Extract specific DataFrames
    sales_orders = dataframes.get("sales_orders")
    sale_order_line = dataframes.get("sale_order_line")
    master_sku = dataframes.get("master_sku")

    # Ensure required DataFrames are loaded
    if sale_order_line is not None and sales_orders is not None and master_sku is not None:
        # Merge SPSU25 Status and Category
        merged_data = merge_spsu25_status(sale_order_line, master_sku)

        # Add Surf Expo column
        merged_data = add_surf_expo_column(merged_data, sales_orders)

        # Save merged_data to a CSV file for inspection
        try:
            merged_data.to_csv("./data/merged_data_inspection.csv", index=False)
            print("Merged data saved to merged_data_inspection.csv for inspection.")
        except Exception as e:
            print(f"Error saving merged data to CSV: {e}")

        # Compute statistics
        stats = compute_statistics(sale_order_line)

        return {
            "stats": stats,
            "merged_data": merged_data,
            "filtered_sale_order_line": sale_order_line,
        }
    else:
        raise ValueError("Error: Missing required datasets.")


if __name__ == "__main__":
    # Process data and retrieve results
    results = process_root_data()

    # Display results for debugging
    print("Statistics:")
    print(results["stats"])
    print("\nMerged Data Preview:")
    print(results["merged_data"].head())
