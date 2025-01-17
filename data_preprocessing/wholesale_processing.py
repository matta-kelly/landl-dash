import pandas as pd
from flask import current_app

# Function to filter wholesale-specific sales
def filter_wholesale_data(merged_data):
    """
    Filter the merged data for wholesale-specific sales (Sales Team = 'Wholesale').

    Args:
        merged_data (pd.DataFrame): The merged DataFrame containing all sales data.

    Returns:
        pd.DataFrame: Filtered DataFrame for wholesale sales.
    """
    if "Sales Team" not in merged_data.columns:
        raise KeyError("'Sales Team' column is missing from the merged data.")
    
    wholesale_data = merged_data[merged_data["Sales Team"] == "Wholesale"]
    return wholesale_data

# Function to compute statistics
def compute_statistics(filtered_data):
    """
    Compute key statistics from the filtered DataFrame.

    Args:
        filtered_data (pd.DataFrame): The filtered DataFrame.

    Returns:
        dict: Dictionary of computed statistics.
    """
    if filtered_data.empty:
        return {
            "total_orders": 0,
            "total_revenue": 0.0,
            "avg_order_value": 0.0,
            "top_selling_product": "N/A"
        }

    total_orders = filtered_data["Order Reference"].nunique()
    total_revenue = filtered_data["Subtotal"].sum()
    avg_order_value = (
        filtered_data.groupby("Order Reference")["Subtotal"].sum().mean()
    )
    top_selling_product = (
        filtered_data.groupby("SKU")["Quantity"]
        .sum()
        .idxmax()
        if not filtered_data.empty
        else "N/A"
    )

    return {
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "avg_order_value": avg_order_value,
        "top_selling_product": top_selling_product,
    }

# Main function to process wholesale data
def process_wholesale_data():
    """
    Process wholesale-specific data, compute statistics, and return DataFrames and stats.
    Saves the filtered wholesale data to a CSV file for inspection.

    Returns:
        dict: Dictionary containing statistics and processed DataFrames.
    """
    # Access root data from Flask's config
    root_data = current_app.config['root_data']
    if not root_data:
        raise ValueError("Root data not available in Flask config.")

    # Access the merged data
    merged_data = root_data['merged_data']

    # Filter for wholesale-specific sales
    wholesale_data = filter_wholesale_data(merged_data)

    # Save the filtered wholesale data to a CSV file for inspection
    try:
        wholesale_data.to_csv("./wholesale_data_inspection.csv", index=False)
        print("Wholesale data saved to wholesale_data_inspection.csv for inspection.")
    except Exception as e:
        print(f"Error saving wholesale data to CSV: {e}")

    # Compute statistics
    stats = compute_statistics(wholesale_data)

    return {
        "stats": stats,
        "merged_data": wholesale_data,
        "filtered_sale_order_line": wholesale_data
    }

if __name__ == "__main__":
    # Simulate running this function in isolation (if needed for testing)
    try:
        wholesale_results = process_wholesale_data()
        print("Wholesale Statistics:")
        print(wholesale_results["stats"])
        print("\nFiltered Wholesale Data Preview:")
        print(wholesale_results["merged_data"].head())
    except Exception as e:
        print(f"Error processing wholesale data: {e}")
