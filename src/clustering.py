from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

def customer_clustering(df):
    features = df.groupby("Customer_ID").agg({
        "Quantity": "sum",
        "Total_Amount": "sum",
        "Invoice ID": "nunique"
    })

    features.rename(columns={
        "Invoice ID": "Num_Transactions"
    }, inplace=True)

    n_samples = len(features)
    if n_samples < 2:
        return "Not enough customers for clustering"

    n_clusters = min(3, n_samples)

    scaler = StandardScaler()
    scaled = scaler.fit_transform(features)

    model = KMeans(n_clusters=n_clusters, random_state=42)
    features["Cluster"] = model.fit_predict(scaled)

    return features