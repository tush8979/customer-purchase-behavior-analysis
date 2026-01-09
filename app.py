import streamlit as st
from src.data_loader import load_transactions
from src.customer_analysis import top_product_per_customer
from src.clustering import customer_clustering
from src.market_basket import market_basket_analysis
from src.area_analysis import area_wise_demand

st.set_page_config(page_title="Retail Intelligence Dashboard", layout="wide")

st.title("🛒 Customer Purchase Behavior Analysis")

# Load data (sample file for Streamlit)
df = load_transactions("data/sample_transactions.csv")

# ---------------- TOP PRODUCT ----------------
st.subheader("🧾 Top Product per Customer")
st.dataframe(top_product_per_customer(df))

# ---------------- AREA DEMAND ----------------
st.subheader("📍 Area-wise Product Demand")
st.dataframe(area_wise_demand(df).head(10))

# ---------------- CUSTOMER CLUSTERING ----------------
st.subheader("👥 Customer Segmentation")
st.dataframe(customer_clustering(df))

# ---------------- MARKET BASKET ----------------
st.subheader("🧺 Market Basket Analysis")
rules = market_basket_analysis(df)
st.dataframe(rules.head(10))