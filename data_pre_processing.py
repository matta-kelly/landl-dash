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
    "master_sku": "master-sku.csv",
    "cleaned_data": "cleaned_data.csv"
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

# Function to filter sale_order_line by valid orders
def filter_sale_order_line_by_orders(sale_order_line, sales_orders):
    """
    Filter the sale_order_line DataFrame to include only rows with Order Reference
    present in the sales_orders DataFrame.

    Args:
        sale_order_line (pd.DataFrame): The main sales order line data.
        sales_orders (pd.DataFrame): The sales orders containing valid orders.

    Returns:
        pd.DataFrame: Filtered sale_order_line DataFrame.
    """
    if "Order Reference" not in sales_orders.columns or "Order Reference" not in sale_order_line.columns:
        raise KeyError("Missing 'Order Reference' column in one of the DataFrames.")
    
    valid_orders = sales_orders["Order Reference"].unique()
    return sale_order_line[sale_order_line["Order Reference"].isin(valid_orders)]

# Function to merge SPSU25 Status
def merge_spsu25_status(sale_order_line, master_sku):
    """
    Merge SPSU25 Status from master_sku into the sale_order_line DataFrame.

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
        master_sku[["SKU (Parent)", "SPSU25 Status"]],
        left_on="SKU",
        right_on="SKU (Parent)",
        how="left"
    )
    return merged_data

# Function to compute SPSU25 Status distribution
def compute_spsu25_distribution(merged_data):
    """
    Compute the distribution of SPSU25 Status as percentages.

    Args:
        merged_data (pd.DataFrame): The merged DataFrame with SPSU25 Status.

    Returns:
        pd.DataFrame: DataFrame containing SPSU25 Status and their percentages.
    """
    if "SPSU25 Status" not in merged_data.columns:
        raise KeyError("Missing 'SPSU25 Status' column in the merged data.")
    
    status_counts = merged_data["SPSU25 Status"].value_counts(normalize=True) * 100
    status_distribution = status_counts.reset_index().rename(columns={
        "index": "SPSU25 Status",
        "SPSU25 Status": "Percentage"
    })
    return status_distribution

# Function to create SPSU25 Status pie chart
def create_spsu25_pie_chart(spsu25_distribution):
    """
    Create a Plotly pie chart for SPSU25 Status distribution.

    Args:
        spsu25_distribution (pd.DataFrame): DataFrame with SPSU25 Status and percentages.

    Returns:
        dict: Plotly figure object for the pie chart.
    """
    if spsu25_distribution is not None and not spsu25_distribution.empty:
        pie_chart = px.pie(
            spsu25_distribution,
            names="SPSU25 Status",
            values="Percentage",
            title="SPSU25 Status Distribution",
            hole=0.4,
        )
        return pie_chart
    else:
        return {
            "data": [],
            "layout": {"title": "No Data Available for SPSU25 Status"},
        }

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
            "total_revenue": 0.0,
            "avg_order_value": 0.0,
            "top_selling_product": "N/A"
        }

    total_orders = filtered_sale_order_line["Order Reference"].nunique()
    total_revenue = filtered_sale_order_line["Subtotal"].sum()
    avg_order_value = (
        filtered_sale_order_line.groupby("Order Reference")["Subtotal"].sum().mean()
    )
    top_selling_product = (
        filtered_sale_order_line.groupby("SKU")["Quantity"]
        .sum()
        .idxmax()
        if not filtered_sale_order_line.empty
        else "N/A"
    )

    return {
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "avg_order_value": avg_order_value,
        "top_selling_product": top_selling_product,
    }

# Main logic
if __name__ == "__main__":
    # Load datasets
    dataframes = load_datasets(FILES, DATA_FOLDER)

    # Extract specific DataFrames
    sales_orders = dataframes.get("sales_orders")
    sale_order_line = dataframes.get("sale_order_line")
    master_sku = dataframes.get("master_sku")

    # Ensure required DataFrames are loaded
    if sale_order_line is not None and sales_orders is not None and master_sku is not None:
        # Filter sale_order_line by valid orders from sales_orders
        filtered_sale_order_line = filter_sale_order_line_by_orders(sale_order_line, sales_orders)

        # Merge SPSU25 Status
        merged_data = merge_spsu25_status(filtered_sale_order_line, master_sku)

        # Compute SPSU25 Status distribution
        spsu25_distribution = compute_spsu25_distribution(merged_data)

        # Create pie chart
        spsu25_pie_chart = create_spsu25_pie_chart(spsu25_distribution)

        # Compute statistics
        stats = compute_statistics(filtered_sale_order_line)

        # Display results for debugging
        print("Statistics:")
        print(stats)
        print("\nSPSU25 Status Distribution:")
        print(spsu25_distribution)
    else:
        print("Error: Missing required datasets.")
