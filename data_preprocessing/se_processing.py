import pandas as pd
from flask import current_app


# Function to filter wholesale-specific sales
def filter_se_data(merged_data, expo_orders):
    """
    Filter sale_order_line data for Surf Expo orders.

    Args:
        merged_data (pd.DataFrame): The complete wholesale sale_order_line data.
        expo_orders (pd.DataFrame): The list of Surf Expo order references.

    Returns:
        pd.DataFrame: Filtered sale_order_line data specific to Surf Expo.
    """
    if merged_data.empty or expo_orders.empty:
        return pd.DataFrame()

    # Ensure the column names align
    expo_orders = expo_orders.rename(columns=lambda x: x.strip())  # Strip whitespace from columns
    expo_order_references = expo_orders["Order Reference"].unique()  # List of relevant order references

    # Filter merged_data for these orders
    filtered = merged_data[merged_data["Order Reference"].isin(expo_order_references)]

    return filtered


# Function to compute category summary
def generate_category_summary(filtered_sale_order_line):
    """
    Generates a summary DataFrame by category, including metrics for Sales Qty, Sales $, AUR, and % of Total Revenue.

    Args:
        filtered_sale_order_line (pd.DataFrame): Filtered sale_order_line DataFrame.

    Returns:
        pd.DataFrame: Aggregated DataFrame with category summaries.
    """
    # Define empty DataFrame with the required columns
    if filtered_sale_order_line.empty:
        return pd.DataFrame(columns=[
            "Product Category", "Sales_Qty", "Sales_Dollar", "AUR", "Percent of Total Revenue"
        ])

    # Ensure required columns exist
    required_columns = ["Product Category", "Quantity", "Subtotal"]
    for col in required_columns:
        if col not in filtered_sale_order_line.columns:
            raise ValueError(f"Missing required column: {col}")

    # Compute base metrics grouped by Product Category
    summary = filtered_sale_order_line.groupby("Product Category").agg(
        Sales_Qty=("Quantity", "sum"),
        Sales_Dollar=("Subtotal", "sum")
    ).reset_index()

    # Calculate AUR (Average Unit Revenue), handle division by zero
    summary["AUR"] = summary["Sales_Dollar"] / summary["Sales_Qty"]
    summary["AUR"] = summary["AUR"].fillna(0)  # Replace NaN with 0 if division fails

    # Calculate total sales dollar for the entire dataset
    total_sales_dollar = summary["Sales_Dollar"].sum()

    # Add % of Total Revenue column
    summary["Percent of Total Revenue"] = (summary["Sales_Dollar"] / total_sales_dollar) * 100

    # Add grand totals at the bottom
    grand_totals = pd.DataFrame({
        "Product Category": ["Total"],
        "Sales_Qty": [summary["Sales_Qty"].sum()],
        "Sales_Dollar": [summary["Sales_Dollar"].sum()],
        "AUR": [summary["Sales_Dollar"].sum() / summary["Sales_Qty"].sum() if summary["Sales_Qty"].sum() > 0 else 0],
        "Percent of Total Revenue": [100.0],  # Grand total should always be 100%
    })

    # Concatenate the detailed summary and grand totals
    result = pd.concat([summary, grand_totals], ignore_index=True)

    return result

# Function to retrieve top items in each category
def get_top_items(filtered_sale_order_line, n=5):
    """
    Get the top N items in each category by revenue, separated by Core, New, and Limited.

    Args:
        filtered_sale_order_line (pd.DataFrame): The filtered sale_order_line DataFrame.
        n (int): Number of top items to retrieve per category and type.

    Returns:
        pd.DataFrame: DataFrame with top N items in each category and type.
    """
    if filtered_sale_order_line.empty:
        return pd.DataFrame(columns=["Product Category", "SPSU25 Status", "Subtotal", "Quantity"])

    top_items = filtered_sale_order_line.groupby(["Product Category", "SPSU25 Status"]).apply(
        lambda x: x.nlargest(n, "Subtotal")
    ).reset_index(drop=True)

    return top_items


# Function to compute overall Surf Expo statistics
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
            "total_units": 0,
            "total_cost": 0.0,
            "total_revenue": 0.0,
            "avg_unit_revenue": 0.0,
            "total_quotations": 0,
            "revenue_quotations": 0.0,
        }

    # Normalize Order Status column for consistent comparisons
    filtered_sale_order_line["Order Status"] = (
        filtered_sale_order_line["Order Status"].str.lower().str.strip()
    )

    # Check unique values in Order Status column
    print("Unique Order Status Values:", filtered_sale_order_line["Order Status"].unique())

    # Separate sales and quotations
    sales_orders = filtered_sale_order_line[filtered_sale_order_line["Order Status"] == "sale"]
    quotation_orders = filtered_sale_order_line[filtered_sale_order_line["Order Status"] == "draft"]

    # Debugging: Log counts after filtering
    print("Number of Sales Orders:", sales_orders.shape[0])
    print("Number of Quotation Orders:", quotation_orders.shape[0])

    # Total orders and quotations
    total_orders = sales_orders["Order Reference"].nunique()
    total_quotations = quotation_orders["Order Reference"].nunique()

    # Total units for sales
    total_units = sales_orders["Quantity"].sum()

    # Total cost for sales
    total_cost = sales_orders["Total Cost"].sum()

    # Revenue for sales and quotations
    total_revenue = sales_orders["Subtotal"].sum()
    revenue_quotations = quotation_orders["Subtotal"].sum()

    # Average Unit Revenue (AUR) for sales
    avg_unit_revenue = total_revenue / total_units if total_units > 0 else 0.0

    return {
        "se_total_orders": total_orders,
        "se_total_units": total_units,
        "se_total_cost": total_cost,
        "se_total_revenue": total_revenue,
        "se_avg_unit_revenue": avg_unit_revenue,
        "se_total_quotations": total_quotations,
        "se_revenue_quotations": revenue_quotations,
    }

# Sales by Rep
def breakout_by_sales_rep(filtered_sale_order_line):
    """
    Breaks out the number of orders, revenue in quotations, and revenue in sales by sales rep.
    Adds a totals row at the bottom of the summary and a 'Total Revenue' column.
    """
    if filtered_sale_order_line.empty:
        return pd.DataFrame(columns=["Salesperson", "Number of Orders", "Revenue in Quotations", "Revenue in Sales", "Total Revenue"])

    # Normalize "Order Status" for consistent filtering
    filtered_sale_order_line["Order Status"] = filtered_sale_order_line["Order Status"].str.lower().str.strip()

    # Aggregate by Sales Rep with separate filters for sales and quotations
    sales_rep_summary = (
        filtered_sale_order_line.groupby("Salesperson").apply(lambda group: pd.Series({
            "Number of Orders": group["Order Reference"].nunique(),
            "Revenue in Quotations": group.loc[group["Order Status"] != "sale", "Subtotal"].sum(),
            "Revenue in Sales": group.loc[group["Order Status"] == "sale", "Subtotal"].sum(),
        }))
        .reset_index()
    )

    sales_rep_summary.columns = ["Salesperson", "Number of Orders", "Revenue in Quotations", "Revenue in Sales"]

    # Add a 'Total Revenue' column
    sales_rep_summary["Total Revenue"] = (
        sales_rep_summary["Revenue in Quotations"] + sales_rep_summary["Revenue in Sales"]
    )

    # Calculate totals for each column
    totals_row = {
        "Salesperson": "Total",
        "Number of Orders": sales_rep_summary["Number of Orders"].sum(),
        "Revenue in Quotations": sales_rep_summary["Revenue in Quotations"].sum(),
        "Revenue in Sales": sales_rep_summary["Revenue in Sales"].sum(),
        "Total Revenue": sales_rep_summary["Total Revenue"].sum(),
    }

    # Append the totals row
    sales_rep_summary = pd.concat([sales_rep_summary, pd.DataFrame([totals_row])], ignore_index=True)

    return sales_rep_summary

# Category Group Breakdown
def category_group_summary(filtered_sale_order_line):
    """
    Generate a summary of revenue for Clothing and Jewelry, broken down by status.

    Args:
        filtered_sale_order_line (pd.DataFrame): The filtered sale_order_line DataFrame.

    Returns:
        pd.DataFrame: A pivot table summarizing revenue for Clothing and Jewelry by status.
    """
    if filtered_sale_order_line.empty:
        return pd.DataFrame(columns=["Category Group", "SPSU25 Status", "Revenue"])

    # Ensure necessary columns exist
    required_columns = ["Category Group", "SPSU25 Status", "Subtotal"]
    for col in required_columns:
        if col not in filtered_sale_order_line.columns:
            raise KeyError(f"Missing required column: {col}")

    # Group data by Category Group and SPSU25 Status and sum the revenue
    summary = (
        filtered_sale_order_line.groupby(["Category Group", "SPSU25 Status"])["Subtotal"]
        .sum()
        .reset_index()
    )

    # Pivot the table to have SPSU25 Status as columns and Category Group as rows
    pivot_summary = summary.pivot(
        index="Category Group", columns="SPSU25 Status", values="Subtotal"
    )

    # Replace NaN with 0 for cleaner display
    pivot_summary = pivot_summary.fillna(0)

    # Add a total column for each row
    pivot_summary["Total"] = pivot_summary.sum(axis=1)

    # Add a total row for each column
    pivot_summary.loc["Total"] = pivot_summary.sum()

    category_comparison = pivot_summary.reset_index()

    return category_comparison

#geospatial analysis from wholesale
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


# Product analysis
def compute_product_profit_analysis(filtered_sale_order_line):
    """
    Compute product-level data for profit margin vs. revenue scatter plot.

    Args:
        filtered_data (pd.DataFrame): The filtered DataFrame containing sales data.

    Returns:
        pd.DataFrame: A DataFrame containing total revenue, profit margin, units sold,
                      collection, and lifecycle status (SPSU25 Status) by product.
    """
    required_columns = ["SKU", "Subtotal", "Quantity", "Total Cost", "SPSU25 Status", "Collection"]
    for col in required_columns:
        if col not in filtered_sale_order_line.columns:
            raise KeyError(f"'{col}' column is missing from the filtered data.")

    # Compute revenue and total cost by SKU
    product_data = filtered_sale_order_line.groupby("SKU", as_index=False).agg(
        {
            "Subtotal": "sum",  # Total revenue
            "Quantity": "sum",  # Units sold
            "Total Cost": "sum",  # Total cost
            "SPSU25 Status": "first",  # Take the first lifecycle status per SKU
            "Collection": "first",  # Take the first collection per SKU
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


# Function to process Surf Expo sales recap
def process_surf_recap():
    """
    Process and summarize Surf Expo sales recap data.
    """
    # Retrieve wholesale data and Surf Expo order list
    wholesale_data = current_app.config.get('wholesale_merged_data')
    expo_orders = pd.read_csv('./data/se-sales-orders.csv')

    if wholesale_data is None or expo_orders.empty:
        return {
            "stats": {},
            "top_items": pd.DataFrame(),
            "category_summary": pd.DataFrame(),
            "sales_rep_summary": pd.DataFrame(),
            "category_comparison" : pd.DataFrame(),
            "product_comparison": pd.DataFrame(),
            "collection_summary": pd.DataFrame(),
        }

    # Filter wholesale data for Surf Expo
    filtered_so_line = filter_se_data(wholesale_data, expo_orders)

    # Compute statistics
    stats = compute_statistics(filtered_so_line)

    # Get top items
    top_items = get_top_items(filtered_so_line)

    # Generate category summary
    category_summary = generate_category_summary(filtered_so_line)

    # Compute geospatial data
    geospatial_data = compute_geospatial_data(filtered_so_line)

    # Compute sales rep breakout
    sales_rep_summary = breakout_by_sales_rep(filtered_so_line)

    # Status/ Category Group
    category_comparison = category_group_summary(filtered_so_line)

    product_comparison = compute_product_profit_analysis(filtered_so_line)

   
    return {
        "stats": stats,
        "top_items": top_items,
        "category_summary": category_summary,
        "geospatial_data": geospatial_data,
        "sales_rep_summary": sales_rep_summary,
        "category_comparison": category_comparison,
        "product_comparison": product_comparison,
    }
