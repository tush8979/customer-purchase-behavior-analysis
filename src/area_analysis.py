def area_wise_demand(df):
    return (
        df.groupby(["Area", "Category"])["Quantity"]
        .sum()
        .reset_index()
        .sort_values(["Area", "Quantity"], ascending=[True, False])
    )