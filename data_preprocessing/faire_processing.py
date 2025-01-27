import pandas as pd
from flask import current_app

# Function to filter Faire-specific sales
def filter_faire_data(merged_data, faire_orders):
    """
    Filter the merged data for Faire-specific sales (Sales Team = 'Faire').

    Args:
        merged_data (pd.DataFrame): The merged DataFrame containing all sales data.

    Returns:
        pd.DataFrame: Filtered DataFrame for Faire sales.
    """
    if merged_data.empty or faire_orders.empty:
        return pd.DataFrame()

    # Ensure the column names align
    faire_orders = faire_orders.rename(columns=lambda x: x.strip())  # Strip whitespace from columns
    faire_order_references = faire_orders["Order Reference"].unique()  # List of relevant order references

    # Filter merged_data for these orders
    filtered = merged_data[merged_data["Order Reference"].isin(faire_order_references)]

    return filtered

# Function to filter data for a specific date range (Winter Faire)
def filter_winter_data(faire_data):
    """
    Filter the Faire-specific data for winter sales (January 21st, 2025 to January 24th, 2025).

    Args:
        faire_data (pd.DataFrame): Filtered Faire data.

    Returns:
        pd.DataFrame: DataFrame for the specified winter date range.
    """
    if "Sales Date" not in faire_data.columns:
        raise KeyError("'Sales Date' column is missing from the Faire data.")

    # Ensure we work on a copy of the data to avoid the SettingWithCopyWarning
    faire_data = faire_data.copy()

    # Ensure that 'Sales Date' is in datetime format
    faire_data["Sales Date"] = pd.to_datetime(faire_data["Sales Date"], errors="coerce")
    
    # Filter for the specified date range
    winter_data = faire_data[
        (faire_data["Sales Date"] >= "2025-01-21") &
        (faire_data["Sales Date"] < "2025-01-25")
    ]
    return winter_data

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

# Main processing function
def process_faire_data():
    """
    Process Faire-specific data, compute statistics, and return DataFrames and stats.
    """
    # Access root data from Flask's config
    root_data = current_app.config['root_data']
    if not root_data:
        raise ValueError("Root data not available in Flask config.")
    
    faire_orders = pd.read_csv('./data/f-sales-orders.csv')

    # Access the merged data
    merged_data = root_data['merged_data']

    # Filter for Faire-specific sales
    faire_data = filter_faire_data(merged_data, faire_orders)

    # Filter for Winter Faire data
    winter_data = filter_winter_data(faire_data)

    # Compute statistics
    stats = compute_statistics(faire_data)
    winter_stats = compute_statistics(winter_data)

    # Return structured data
    return {
        "stats": stats,
        "faire_data": faire_data,  # Filtered Faire data
        "winter_data": winter_data,  # Filtered winter data
        "winter_stats": winter_stats,
    }


if __name__ == "__main__":
    # Simulate running this function in isolation (if needed for testing)
    try:
        faire_results = process_faire_data()
        print("Faire Statistics:")
        print(faire_results["stats"])
        print("\nWinter Faire Statistics:")
        print(faire_results["winter_stats"])
        print("\nFiltered Faire Data Preview:")
        print(faire_results["faire_data"].head())
        print("\nFiltered Winter Data Preview:")
        print(faire_results["winter_data"].head())
    except Exception as e:
        print(f"Error processing Faire data: {e}")
