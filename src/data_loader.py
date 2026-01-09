import pandas as pd
import os

# ---------- TRANSACTION DATA (CUSTOMER BEHAVIOR) ----------
def load_transactions(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Transactions file not found: {path}")

    df = pd.read_csv(path)
    df.columns = df.columns.str.strip()

    # Kaggle Supermarket Sales column mapping
    mapping = {
        "InvoiceDate": "Date",
        "Date": "Date",
        "City": "Area",
        "Product line": "Category",
        "Unit price": "Price",
        "Customer type": "Customer_ID"
    }
    df.rename(columns=mapping, inplace=True)

    required = ["Date", "Quantity", "Price"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise KeyError(f"Missing columns in transactions.csv: {missing}")

    df["Date"] = pd.to_datetime(df["Date"])
    df["Total_Amount"] = df["Quantity"] * df["Price"]

    return df


# ---------- STORE SALES DATA (REGRESSION) ----------
def load_store_sales(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Store sales file not found: {path}")

    df = pd.read_csv(path)

    # ---- HARD NORMALIZATION (VERY IMPORTANT) ----
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )

    # ---- FLEXIBLE COLUMN MAPPING ----
    column_mapping = {
        "store_id": "Store_ID",
        "store_area": "Store_Area",
        "items_available": "Items_Available",
        "daily_customer_count": "Daily_Customer_Count",
        "store_sales": "Store_Sales"
    }

    df.rename(columns=column_mapping, inplace=True)

    # ---- FINAL REQUIRED CHECK ----
    required = [
        "Store_Area",
        "Items_Available",
        "Daily_Customer_Count",
        "Store_Sales"
    ]

    missing = [c for c in required if c not in df.columns]
    if missing:
        raise KeyError(
            f"Missing columns in store_sales.csv: {missing}\n"
            f"Available columns: {list(df.columns)}"
        )

    return df

    # Normalize column names
    df.columns = (
        df.columns
        .str.strip()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )

    required = [
        "Store_Area",
        "Items_Available",
        "Daily_Customer_Count",
        "Store_Sales"
    ]

    missing = [c for c in required if c not in df.columns]
    if missing:
        raise KeyError(f"Missing columns in store_sales.csv: {missing}")

    return df