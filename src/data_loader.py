import pandas as pd
import os

# ---------- TRANSACTION DATA (CUSTOMER BEHAVIOR) ----------
import pandas as pd
import os

def load_transactions(source):
    """
    source can be:
    - file path (str)
    - Streamlit UploadedFile
    """

    # Case 1: Uploaded via Streamlit
    if hasattr(source, "read"):
        df = pd.read_csv(source)

    # Case 2: File path
    else:
        if not os.path.exists(source):
            raise FileNotFoundError(f"Transactions file not found: {source}")
        df = pd.read_csv(source)

    df.columns = df.columns.str.strip()

    # Column mapping for Supermarket Sales dataset
    mapping = {
        "City": "Area",
        "Customer type": "Customer_ID",
        "Product line": "Category",
        "Unit price": "Price"
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