# data_loader.py

import logging
from odoo_api.odoo_integration import query_odoo_data  # Future integration
import pandas as pd
import os


logger = logging.getLogger(__name__)

# Path to the data folder
DATA_FOLDER = './data'

# File names
FILES = {
    "sale_order_line": "sale-order-line.csv",
    "master_sku": "master-sku.csv"
}

# Global state for cached/preloaded data
cached_data = None


def load_csv_data():
    """
    Load all datasets from CSV files, preprocess them, and return as a dictionary of DataFrames.

    Returns:
        dict: Dictionary of preprocessed DataFrames for each CSV file.
    Raises:
        Exception: If any CSV file fails to load.
    """
    dataframes = {}
    for key, file_name in FILES.items():
        file_path = os.path.join(DATA_FOLDER, file_name)
        try:
            dataframes[key] = pd.read_csv(file_path)
            logger.info(f"Loaded {file_name} successfully.")
        except Exception as e:
            logger.error(f"Error loading {file_name}: {e}")
            raise  # Re-raise exception to handle it at a higher level

    # Preprocess the loaded DataFrames
    dataframes = preprocess_csv(dataframes)
    return dataframes


def load_data():
    """
    Preload data during app startup. Attempts to query Odoo, falls back to CSV.
    """
    global cached_data
    try:
        logger.info("Attempting to query Odoo for data.")
        cached_data = query_odoo_data()
        logger.info("Data successfully loaded from Odoo.")
    except Exception as e:
        logger.error(f"Failed to load data from Odoo: {e}")
        logger.info("Falling back to CSV data.")
        try:
            cached_data = load_csv_data()
            if not cached_data:
                raise ValueError("No data loaded from CSV files.")
            logger.info("Data successfully loaded from CSV.")
        except Exception as e:
            logger.error(f"Failed to load data from CSV: {e}")
            cached_data = None  # Explicitly set to None

    return cached_data


# CSV HELPER
def preprocess_csv(dataframes):
    """
    Preprocess all loaded CSV DataFrames:
    - Fill blanks with NaN.
    - Strip leading and trailing spaces from string columns.
    - Handle data consistency issues where necessary.
    - Ensure numeric columns are converted to the appropriate data type.

    Args:
        dataframes (dict): Dictionary of DataFrames to preprocess.

    Returns:
        dict: Preprocessed DataFrames.
    """
    for key, df in dataframes.items():
        logger.info(f"Preprocessing DataFrame: {key}")
        
        # Clean column names (strip spaces)
        df.columns = df.columns.str.strip()

        # Fill blanks with NaN
        df.fillna(value=pd.NA, inplace=True)

        # Process every column
        for col in df.columns:
            # If the column is of type string, strip spaces
            if df[col].dtype == "object":
                df[col] = df[col].astype(str).str.strip()
            # If the column is numeric, convert to numeric (coerce invalid to NaN)
            else:
                df[col] = pd.to_numeric(df[col], errors="coerce")

        # Log after processing
        logger.info(f"Preprocessed DataFrame: {key}")
        dataframes[key] = df

    return dataframes





