import pandas as pd
from flask import current_app

# Function to filter eCommerce-specific sales
def filter_ecom_data(merged_data):
    """
    Filter the merged data for eCommerce-specific sales (Sales Team = 'Shopify').

    Args:
        merged_data (pd.DataFrame): The merged DataFrame containing all sales data.

    Returns:
        pd.DataFrame: Filtered DataFrame for eCommerce sales.
    """
    if "Sales Team" not in merged_data.columns:
        raise KeyError("'Sales Team' column is missing from the merged data.")
    
    ecom_data = merged_data[merged_data["Sales Team"] == "Shopify"]
    return ecom_data

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

def process_ecom_data():
    """
    Process eCommerce-specific data, compute statistics, and return DataFrames and stats.
    """
    # Access root data from Flask's config
    root_data = current_app.config['root_data']
    if not root_data:
        raise ValueError("Root data not available in Flask config.")

    # Access the merged datae
    merged_data = root_data['merged_data']

    # Filter for eCommerce-specific sales
    ecom_data = filter_ecom_data(merged_data)

    # Save the filtered eCommerce data to a CSV file for inspection
    try:
        ecom_data.to_csv("./data/ecom_data_inspection.csv", index=False)
        print("E-commerce data saved to ecom_data_inspection.csv for inspection.")
    except Exception as e:
        print(f"Error saving e-commerce data to CSV: {e}")

    # Compute statistics
    stats = compute_statistics(ecom_data)

    # Return structured data
    return {
        "stats": stats,
        "merged_data": ecom_data,  # Filtered eCommerce data
        "filtered_sale_order_line": ecom_data,
    }


if __name__ == "__main__":
    # Simulate running this function in isolation (if needed for testing)
    try:
        ecom_results = process_ecom_data()
        print("E-Commerce Statistics:")
        print(ecom_results["stats"])
        print("\nFiltered E-Commerce Data Preview:")
        print(ecom_results["merged_data"].head())
    except Exception as e:
        print(f"Error processing eCommerce data: {e}")
