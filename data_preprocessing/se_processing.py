import pandas as pd
from flask import current_app

# Function to filter Surf Expo-specific sales
import pandas as pd

def filter_surf_expo_data(merged_data):
    """
    Filter the merged data for Surf Expo-specific sales. Includes only order lines
    with the Surf Expo column set to True.

    Args:
        merged_data (pd.DataFrame): The merged DataFrame containing all sales data.

    Returns:
        pd.DataFrame: Filtered DataFrame for Surf Expo sales.
    """
    if "Surf Expo" not in merged_data.columns:
        raise KeyError("'Surf Expo' column is missing from the merged data. Ensure it has been added during preprocessing.")

    # Filter merged data where 'Surf Expo' column is True
    surf_expo_data = merged_data[merged_data["Surf Expo"] == True]

    return surf_expo_data


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

# Main function to process Surf Expo data
def process_surf_expo_data():
    """
    Process Surf Expo-specific data, compute statistics, and return DataFrames and stats.
    Saves the filtered Surf Expo data to a CSV file for inspection.

    Returns:
        dict: Dictionary containing statistics and processed DataFrames.
    """
    # Access root data from Flask's config
    root_data = current_app.config.get('root_data')
    if not root_data:
        raise ValueError("Root data not available in Flask config.")

    # Access the merged data
    merged_data = root_data.get('merged_data')
    if merged_data is None:
        raise KeyError("'merged_data' is missing from root data.")

    # Filter for Surf Expo-specific sales using the 'Surf Expo' column
    if "Surf Expo" not in merged_data.columns:
        raise KeyError("'Surf Expo' column is missing from the merged data. Ensure it has been added during preprocessing.")

    surf_expo_data = merged_data[merged_data["Surf Expo"]]

    # Save the filtered Surf Expo data to a CSV file for inspection
    try:
        surf_expo_data.to_csv("./surf_expo_data_inspection.csv", index=False)
        print("Surf Expo data saved to surf_expo_data_inspection.csv for inspection.")
    except Exception as e:
        print(f"Error saving Surf Expo data to CSV: {e}")

    # Compute statistics
    stats = compute_statistics(surf_expo_data)

    return {
        "stats": stats,
        "merged_data": surf_expo_data,
        "filtered_sale_order_line": surf_expo_data
    }


if __name__ == "__main__":
    # Simulate running this function in isolation (if needed for testing)
    try:
        surf_expo_results = process_surf_expo_data()
        print("Surf Expo Statistics:")
        print(surf_expo_results["stats"])
        print("\nFiltered Surf Expo Data Preview:")
        print(surf_expo_results["merged_data"].head())
    except Exception as e:
        print(f"Error processing Surf Expo data: {e}")
