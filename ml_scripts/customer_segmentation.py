import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

def load_data(data=None, filepath=None, testing=True):
    """
    Load and preprocess wholesale data from a file (testing mode) or in-memory (production mode).

    Args:
        data (pd.DataFrame): In-memory wholesale data (production mode).
        filepath (str): Path to the CSV file (testing mode).
        testing (bool): Flag indicating the mode.

    Returns:
        pd.DataFrame: Preprocessed wholesale data.
    """
    if testing:
        if filepath is None:
            raise ValueError("Filepath must be provided in testing mode.")
        print(f"Loading wholesale data from {filepath} for testing.")
        data = pd.read_csv(filepath)
    else:
        if data is None:
            raise ValueError("Data must be provided in production mode.")
    
    # Filter out rows with invalid or missing data
    data = data.dropna(subset=["Subtotal", "Total Cost", "Order Reference"])
    data = data[data["Subtotal"] > 0]

    print(f"Data loaded and filtered. Rows after filtering: {len(data)}")
    return data

def prepare_customer_data(data):
    """
    Prepares the customer data for clustering by engineering features and adding standardized versions.

    Args:
        data (pd.DataFrame): The input DataFrame containing customer transaction data.

    Returns:
        pd.DataFrame: A DataFrame with engineered features, including standardized versions.
    """
    required_columns = ["Customer", "Subtotal", "Total Cost", "Order Reference"]
    for col in required_columns:
        if col not in data.columns:
            raise KeyError(f"'{col}' column is missing from the data.")

    # Add 'IMU (%)' column if not present
    if "IMU (%)" not in data.columns:
        data["IMU (%)"] = ((data["Subtotal"] - data["Total Cost"]) / data["Subtotal"]) * 100

    # Compute Total Revenue per Customer
    revenue = data.groupby("Customer")["Subtotal"].sum().rename("Total Revenue")

    # Compute Average Order Value (AOV) per Customer
    orders = data.groupby("Customer")["Order Reference"].nunique().rename("Order Frequency")
    aov = (revenue / orders).rename("AOV")

    # Compute Average IMU (%) per Customer
    avg_imu = data.groupby("Customer")["IMU (%)"].mean().rename("IMU (%)")

    # Merge features into a single DataFrame
    customer_features = pd.concat([revenue, aov, avg_imu, orders], axis=1).reset_index()

    # Normalize the features
    scaler = StandardScaler()
    features_to_normalize = ["Total Revenue", "AOV", "IMU (%)", "Order Frequency"]
    standardized_features = scaler.fit_transform(customer_features[features_to_normalize])

    # Add standardized columns to the DataFrame
    for i, feature in enumerate(features_to_normalize):
        customer_features[f"{feature} (Standardized)"] = standardized_features[:, i]

    return customer_features

def perform_kmeans_clustering(data, max_clusters=10, random_state=42):
    """
    Performs K-Means clustering and determines the optimal number of clusters.

    Args:
        data (pd.DataFrame): The DataFrame containing standardized features.
        max_clusters (int): Maximum number of clusters to test.
        random_state (int): Seed for reproducibility.

    Returns:
        dict: Contains cluster assignments, cluster centers, and evaluation metrics.
    """
    results = {
        "cluster_assignments": None,
        "optimal_k": None,
        "silhouette_scores": [],
        "inertia_values": [],
    }

    for k in range(2, max_clusters + 1):
        kmeans = KMeans(n_clusters=k, random_state=random_state)
        kmeans.fit(data)
        results["inertia_values"].append(kmeans.inertia_)
        results["silhouette_scores"].append(silhouette_score(data, kmeans.labels_))

    # Determine the optimal k using Silhouette Scores
    results["optimal_k"] = results["silhouette_scores"].index(max(results["silhouette_scores"])) + 2
    kmeans = KMeans(n_clusters=results["optimal_k"], random_state=random_state)
    kmeans.fit(data)
    results["cluster_assignments"] = kmeans.labels_

    return results

# Standalone Testing
def compute_customer_segmentation(wholesale_data=None, testing=True):
    """
    Computes customer segmentation by clustering based on engineered features.

    Args:
        wholesale_data (pd.DataFrame): The wholesale data (required in production mode).
        testing (bool): Flag indicating whether the function is in testing mode.

    Returns:
        pd.DataFrame: Customer features with cluster assignments.
    """
    filepath = "./data/wholesale_data_inspection.csv"
    
    # Load and preprocess data
    data = load_data(data=wholesale_data, filepath=filepath, testing=testing)

    # Prepare the customer data
    customer_features = prepare_customer_data(data)

    # Extract standardized features for clustering
    standardized_features = customer_features[[
        "Total Revenue (Standardized)",
        "AOV (Standardized)",
        "IMU (%) (Standardized)",
    ]]

    # Perform clustering
    clustering_results = perform_kmeans_clustering(standardized_features)
    customer_features["Cluster"] = clustering_results["cluster_assignments"]

    return customer_features




# If this script is run directly (not imported)
if __name__ == "__main__":
    try:
        # Example for testing the standalone script
        customer_segmentation_data = compute_customer_segmentation(testing=True)  # Ensure testing is True
        customer_segmentation_data.to_csv("./data/customer_segmentation.csv", index=False)
        print("Customer segmentation data saved to customer_segmentation.csv.")
    except Exception as e:
        print(f"Error computing customer segmentation data: {e}")
