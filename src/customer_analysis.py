def top_product_per_customer(df):
    return (
        df.groupby(["Customer_ID", "Category"])["Quantity"]
        .sum()
        .reset_index()
        .sort_values(["Customer_ID", "Quantity"], ascending=[True, False])
        .groupby("Customer_ID")
        .first()
    )