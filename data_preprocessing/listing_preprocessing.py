import pandas as pd
from flask import current_app

# Function to compute statistics
def compute_statistics(listings):
    # Extract the platform from the "Instance" column
    listings['Platform'] = listings['Instance'].str.extract(r'\[(.*?)\]')

    # Determine published and unpublished status
    listings['Published_Status'] = listings['Published'].notnull().map({True: 'Published', False: 'Unpublished'})

    # Group by platform and publication status, then count
    platform_status_counts = (
        listings.groupby(['Platform', 'Published_Status'])
        .size()
        .unstack(fill_value=0)
        .reset_index()
    )

    # Ensure column order
    platform_status_counts = platform_status_counts.rename(columns={
        'Published': 'Published',
        'Unpublished': 'Unpublished'
    })

    return platform_status_counts

# Main processing function
def process_listing_data():
    """
    Process Faire-specific data, compute statistics, and return DataFrames and stats.
    """
    # Load the data
    listings = pd.read_csv('./data/listings.csv')

    # Compute statistics
    stats = compute_statistics(listings)

    # Return structured data
    return {
        "stats": stats,
    }