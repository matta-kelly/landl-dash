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


def compute_delivery_quantity_distribution(filtered_data):
    """
    Compute the distribution of delivery quantities (date-only) from the filtered DataFrame,
    separating by product categories (e.g., Clothing vs. Jewelry) and by order status
    (e.g., Quotation vs. Sales).

    Args:
        filtered_data (pd.DataFrame): The filtered DataFrame.

    Returns:
        pd.DataFrame: DataFrame containing the delivery quantity distribution by category and status.
    """
    required_columns = ["Delivery Date", "Quantity", "Category Group", "Order Status"]
    for col in required_columns:
        if col not in filtered_data.columns:
            raise KeyError(f"'{col}' column is missing from the filtered data.")
    
    # Parse the Delivery Date column to datetime, forcing errors to NaT
    filtered_data = filtered_data.copy()
    filtered_data["Delivery Date"] = pd.to_datetime(filtered_data["Delivery Date"], errors="coerce")

    # Drop rows with invalid delivery dates
    filtered_data = filtered_data.dropna(subset=["Delivery Date"])

    # Remove the time part, keeping only the date
    filtered_data["Delivery Date"] = filtered_data["Delivery Date"].dt.date

    # Map order statuses to Quotation vs. Sales
    filtered_data["Order Type"] = filtered_data["Order Status"].apply(
        lambda x: "Quotation" if x == "draft" else "Sales"
    )

    # Aggregate quantities by date, category, and order type
    delivery_quantity_distribution = (
        filtered_data.groupby(["Delivery Date", "Category Group", "Order Type"])["Quantity"]
        .sum()
        .reset_index()
    )

    # Sort by date for clarity
    delivery_quantity_distribution = delivery_quantity_distribution.sort_values("Delivery Date")

    return delivery_quantity_distribution


def compute_monthly_demand(filtered_data):
    """
    Compute monthly demand per Parent SKU, separated by Clothing and Jewelry.

    Args:
        filtered_data (pd.DataFrame): The filtered DataFrame.

    Returns:
        dict: Two DataFrames: one for Clothing and one for Jewelry.
    """
    required_columns = ["Delivery Date", "Quantity", "SKU (Parent)", "Category Group"]
    for col in required_columns:
        if col not in filtered_data.columns:
            raise KeyError(f"'{col}' column is missing from the filtered data.")
    
    # Parse the Delivery Date column to datetime and extract the month
    filtered_data = filtered_data.copy()
    filtered_data["Delivery Date"] = pd.to_datetime(filtered_data["Delivery Date"], errors="coerce")
    filtered_data = filtered_data.dropna(subset=["Delivery Date"])
    filtered_data["Month"] = filtered_data["Delivery Date"].dt.to_period("M").astype(str)

    # Group by Month, Parent SKU, and Category Group
    grouped_data = (
        filtered_data.groupby(["Month", "SKU (Parent)", "Category Group"])["Quantity"]
        .sum()
        .reset_index()
    )

    # Separate the data into Clothing and Jewelry
    clothing_data = grouped_data[grouped_data["Category Group"] == "CLOTHING"]
    jewelry_data = grouped_data[grouped_data["Category Group"] == "JEWELRY"]

    # Pivot the data for Clothing
    clothing_pivot = clothing_data.pivot_table(
        index="SKU (Parent)",
        columns="Month",
        values="Quantity",
        aggfunc="sum",
        fill_value=0
    )

    # Pivot the data for Jewelry
    jewelry_pivot = jewelry_data.pivot_table(
        index="SKU (Parent)",
        columns="Month",
        values="Quantity",
        aggfunc="sum",
        fill_value=0
    )

    return {"clothing": clothing_pivot, "jewelry": jewelry_pivot}

def compute_rep_monthly_summary(filtered_data):
    """
    Compute monthly summary of total amount in quotation and total revenue for each sales rep.

    Args:
        filtered_data (pd.DataFrame): The filtered DataFrame.

    Returns:
        pd.DataFrame: Pivot table showing reps as rows, months as columns, and total values for
                      quotations and revenue.
    """
    required_columns = ["Delivery Date", "Salesperson", "Order Status", "Subtotal"]
    for col in required_columns:
        if col not in filtered_data.columns:
            raise KeyError(f"'{col}' column is missing from the filtered data.")

    # Parse the Delivery Date column to datetime and extract the month
    filtered_data = filtered_data.copy()
    filtered_data["Delivery Date"] = pd.to_datetime(filtered_data["Delivery Date"], errors="coerce")
    filtered_data = filtered_data.dropna(subset=["Delivery Date"])
    filtered_data["Month"] = filtered_data["Delivery Date"].dt.to_period("M").astype(str)

    # Separate data into quotations and sales
    filtered_data["Type"] = filtered_data["Order Status"].apply(
        lambda x: "Quotation" if x == "draft" else "Revenue"
    )

    # Group by Month, Salesperson, and Type, and sum the Subtotal
    grouped_data = (
        filtered_data.groupby(["Month", "Salesperson", "Type"])["Subtotal"]
        .sum()
        .reset_index()
    )

    # Pivot the data to create separate columns for Quotation and Revenue
    pivot_table = grouped_data.pivot_table(
        index="Salesperson",
        columns=["Month", "Type"],
        values="Subtotal",
        aggfunc="sum",
        fill_value=0
    )

    return pivot_table

def compute_product_profit_analysis(filtered_data):
    """
    Compute product-level data for profit margin vs. revenue scatter plot.

    Args:
        filtered_data (pd.DataFrame): The filtered DataFrame containing sales data.

    Returns:
        pd.DataFrame: A DataFrame containing total revenue, profit margin, units sold,
                      and lifecycle status (SPSU25 Status) by product.
    """
    required_columns = ["SKU", "Subtotal", "Quantity", "Total Cost", "SPSU25 Status"]
    for col in required_columns:
        if col not in filtered_data.columns:
            raise KeyError(f"'{col}' column is missing from the filtered data.")

    # Compute revenue and total cost by SKU
    product_data = filtered_data.groupby("SKU", as_index=False).agg(
        {
            "Subtotal": "sum",  # Total revenue
            "Quantity": "sum",  # Units sold
            "Total Cost": "sum",  # Total cost
            "SPSU25 Status": "first",  # Take the first lifecycle status per SKU
        }
    )

    # Calculate profit margin
    product_data["Profit Margin (%)"] = (
        ((product_data["Subtotal"] - product_data["Total Cost"]) / product_data["Subtotal"]) * 100
    ).round(2)

    # Replace infinite or NaN values with 0 (in case of division by zero)
    product_data["Profit Margin (%)"] = product_data["Profit Margin (%)"].replace([float("inf"), -float("inf")], 0).fillna(0)

    # Rename columns for clarity
    product_data.rename(
        columns={
            "Subtotal": "Total Revenue",
            "Quantity": "Units Sold",
            "SPSU25 Status": "Lifecycle Status",
        },
        inplace=True,
    )

    return product_data

def compute_customer_scatter_data(filtered_data):
    """
    Compute data for the customer evaluation scatter plot.

    Args:
        filtered_data (pd.DataFrame): The filtered DataFrame containing sales data.

    Returns:
        pd.DataFrame: A DataFrame containing total revenue, IMU, AOV, order frequency,
                      and SPSU25 status for each customer.
    """
    required_columns = ["Customer", "Subtotal", "Quantity", "Unit Price", "Unit Cost", "Order Reference", "SPSU25 Status"]
    for col in required_columns:
        if col not in filtered_data.columns:
            raise KeyError(f"'{col}' column is missing from the filtered data.")

    # Compute total revenue, total quantity, and number of orders per customer
    customer_data = filtered_data.groupby("Customer").agg(
        total_revenue=pd.NamedAgg(column="Subtotal", aggfunc="sum"),
        total_quantity=pd.NamedAgg(column="Quantity", aggfunc="sum"),
        num_orders=pd.NamedAgg(column="Order Reference", aggfunc="nunique"),
        avg_unit_price=pd.NamedAgg(column="Unit Price", aggfunc="mean"),
        avg_unit_cost=pd.NamedAgg(column="Unit Cost", aggfunc="mean"),
        lifecycle_status=pd.NamedAgg(column="SPSU25 Status", aggfunc="first")
    ).reset_index()

    # Calculate IMU (Initial Markup)
    customer_data["IMU (%)"] = (
        ((customer_data["avg_unit_price"] - customer_data["avg_unit_cost"]) / customer_data["avg_unit_price"]) * 100
    ).round(2)

    # Calculate AOV (Average Order Value)
    customer_data["AOV"] = (customer_data["total_revenue"] / customer_data["num_orders"]).round(2)

    # Ensure IMU and AOV are cleaned (e.g., no infinities or NaNs)
    customer_data["IMU (%)"] = customer_data["IMU (%)"].replace([float("inf"), -float("inf")], 0).fillna(0)
    customer_data["AOV"] = customer_data["AOV"].replace([float("inf"), -float("inf")], 0).fillna(0)

    # Rename columns for clarity
    customer_data.rename(
        columns={
            "total_revenue": "Total Revenue",
            "num_orders": "Order Frequency",
            "lifecycle_status": "Lifecycle Status",
        },
        inplace=True,
    )

    return customer_data

def compute_geospatial_data(filtered_data):
    """
    Compute total revenue and customer count by state/region for geospatial analysis.

    Args:
        filtered_data (pd.DataFrame): The filtered DataFrame containing wholesale data.

    Returns:
        pd.DataFrame: DataFrame containing state-level revenue and customer count.
    """
    required_columns = ["State", "Subtotal", "Customer"]
    for col in required_columns:
        if col not in filtered_data.columns:
            raise KeyError(f"'{col}' column is missing from the filtered data.")

    # Extract valid state names from "State" column
    filtered_data = filtered_data.copy()
    filtered_data["State"] = (
        filtered_data["State"].str.extract(r'([A-Za-z\s]+)\s\(US\)', expand=False).str.strip()
    )

    # Drop rows with missing or invalid state names
    filtered_data = filtered_data.dropna(subset=["State", "Subtotal"])

    # Aggregate data by state
    geospatial_data = (
        filtered_data.groupby("State")
        .agg(
            Total_Revenue=("Subtotal", "sum"),
            Customer_Count=("Customer", "nunique"),
            Avg_Revenue_Per_Customer=("Subtotal", lambda x: x.sum() / x.nunique())
        )
        .reset_index()
    )

    # Sort by total revenue for better visualization
    geospatial_data = geospatial_data.sort_values("Total_Revenue", ascending=False)

    return geospatial_data


# Updated main function to process wholesale data with testing mode
def process_wholesale_data(testing=False):
    """
    Process wholesale-specific data, compute statistics, and return DataFrames and stats.
    Supports testing mode to load data directly from CSV.

    Args:
        testing (bool): If True, loads data from `wholesale_data_inspection.csv`.

    Returns:
        dict: Dictionary containing statistics, processed DataFrames, and additional processed data.
    """
    if testing:
        try:
            # Load wholesale data from CSV
            wholesale_data = pd.read_csv("./data/wholesale_data_inspection.csv")
            print("Loaded wholesale data from CSV for testing.")
        except FileNotFoundError:
            raise FileNotFoundError("The wholesale_data_inspection.csv file is missing. Ensure it exists for testing.")
    else:
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
            wholesale_data.to_csv("./data/wholesale_data_inspection.csv", index=False)
            print("Wholesale data saved to wholesale_data_inspection.csv for inspection.")
        except Exception as e:
            print(f"Error saving wholesale data to CSV: {e}")

    # Compute statistics
    stats = compute_statistics(wholesale_data)

    # Compute delivery date distribution
    try:
        delivery_distribution = compute_delivery_quantity_distribution(wholesale_data)
        delivery_distribution.to_csv("./data/delivery_date_distribution.csv", index=False)
        print("Delivery date distribution saved to delivery_date_distribution.csv.")
    except Exception as e:
        print(f"Error computing delivery date distribution: {e}")
        delivery_distribution = None

    # Compute rep monthly summary
    try:
        rep_summary = compute_rep_monthly_summary(wholesale_data)
        rep_summary.to_csv("./data/rep_monthly_summary.csv", index=False)
        print("Rep monthly summary saved to rep_monthly_summary.csv.")
    except Exception as e:
        print(f"Error computing rep monthly summary: {e}")
        rep_summary = None

    # Compute product profit analysis
    try:
        product_profit_analysis = compute_product_profit_analysis(wholesale_data)
        product_profit_analysis.to_csv("./data/product_profit_analysis.csv", index=False)
        print("Product profit analysis saved to product_profit_analysis.csv.")
    except Exception as e:
        print(f"Error computing product profit analysis: {e}")
        product_profit_analysis = None

    # Compute customer scatter plot data
    try:
        customer_scatter_data = compute_customer_scatter_data(wholesale_data)
        customer_scatter_data.to_csv("./data/customer_scatter_data.csv", index=False)
        print("Customer scatter data saved to customer_scatter_data.csv.")
    except Exception as e:
        print(f"Error computing customer scatter data: {e}")
        customer_scatter_data = None

    # Compute geospatial data
    try:
        geospatial_data = compute_geospatial_data(wholesale_data)
        geospatial_data.to_csv("./data/geospatial_data.csv", index=False)
        print("Geospatial data saved to geospatial_data.csv.")
    except Exception as e:
        print(f"Error computing geospatial data: {e}")
        geospatial_data = None

    try:
        from ml_scripts.customer_segmentation import compute_customer_segmentation
        
        # Pass wholesale_data only when not in testing mode
        customer_segmentation_data = compute_customer_segmentation(wholesale_data=wholesale_data, testing=False)  # testing=False for production
        customer_segmentation_data.to_csv("./data/customer_segmentation.csv", index=False)
        print("Customer segmentation data saved to customer_segmentation.csv.")
    except Exception as e:
        print(f"Error computing customer segmentation data: {e}")
        customer_segmentation_data = None


    

    return {
        "stats": stats,
        "merged_data": wholesale_data,
        "filtered_sale_order_line": wholesale_data,
        "delivery_distribution": delivery_distribution,
        "rep_summary": rep_summary,
        "product_profit_analysis": product_profit_analysis,
        "customer_scatter_data": customer_scatter_data,
        "geospatial_data": geospatial_data,
        "customer_segmentation_data": customer_segmentation_data,
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
