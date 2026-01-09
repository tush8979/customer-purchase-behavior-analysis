import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.data_loader import load_transactions
from src.customer_analysis import top_product_per_customer
from src.clustering import customer_clustering
from src.market_basket import market_basket_analysis
from src.area_analysis import area_wise_demand

# ===================== PAGE CONFIG =====================
st.set_page_config(
    page_title="Retail Intelligence Dashboard",
    layout="wide"
)

# ===================== DARK THEME =====================
st.markdown("""
<style>
    .stApp {
        background-color: #0E1117;
        color: white;
    }
    [data-testid="stMetricValue"] {
        color: #4CAF50;
    }
</style>
""", unsafe_allow_html=True)

# ===================== SIDEBAR =====================
st.sidebar.title("📊 Controls")

# ---- Data Source ----
st.sidebar.markdown("### 📂 Data Source")
uploaded_file = st.sidebar.file_uploader(
    "Upload Transactions CSV",
    type=["csv"]
)

if uploaded_file is not None:
    df = load_transactions(uploaded_file)
    st.sidebar.success("Custom dataset loaded")
else:
    df = load_transactions("data/sample_transactions.csv")
    st.sidebar.info("Using sample dataset")

# ---- Filters ----
st.sidebar.markdown("---")
st.sidebar.markdown("### 🎯 Filters")

selected_city = st.sidebar.multiselect(
    "Select City",
    options=df["Area"].unique(),
    default=list(df["Area"].unique())
)

selected_category = st.sidebar.multiselect(
    "Select Product Category",
    options=df["Category"].unique(),
    default=list(df["Category"].unique())
)

df = df[
    (df["Area"].isin(selected_city)) &
    (df["Category"].isin(selected_category))
]

# ---- Strategy Controls ----
st.sidebar.markdown("---")
st.sidebar.markdown("### 📈 Strategy Assumptions")

initiative = st.sidebar.selectbox(
    "Strategic Initiative",
    ["New Product Launch", "Cost Optimization", "Market Expansion"]
)

growth_rate = st.sidebar.slider("Revenue Growth (%)", 5, 30, 12)
marketing_ratio = st.sidebar.slider("Marketing Expense (%)", 5, 30, 15)
personnel_ratio = st.sidebar.slider("Personnel Cost (%)", 5, 40, 25)

# ===================== HEADER =====================
st.title("🛒 Retail Intelligence & Executive Strategy Dashboard")
st.subheader(f"Strategic Initiative: **{initiative}**")

# ===================== STRATEGY MODEL =====================
years = [2019, 2020, 2021, 2022, 2023]
base_revenue = [80, 92, 103, 115, 127]
revenue = [r * (1 + growth_rate / 100) for r in base_revenue]

finance_df = pd.DataFrame({
    "Year": years,
    "Revenue": revenue
})

finance_df["COGS"] = finance_df["Revenue"] * 0.10
finance_df["Marketing"] = finance_df["Revenue"] * marketing_ratio / 100
finance_df["Personnel"] = finance_df["Revenue"] * personnel_ratio / 100
finance_df["EBITDA"] = finance_df["Revenue"] - (
    finance_df["COGS"] +
    finance_df["Marketing"] +
    finance_df["Personnel"]
)
finance_df["Tax"] = finance_df["EBITDA"] * 0.15
finance_df["Net Profit"] = finance_df["EBITDA"] - finance_df["Tax"]

# ===================== EXECUTIVE KPIs =====================
k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Revenue", f"{finance_df['Revenue'].sum():.1f} MCHF")
k2.metric("Gross Margin", f"{(finance_df['Revenue'].sum() - finance_df['COGS'].sum()):.1f} MCHF")
k3.metric("EBITDA", f"{finance_df['EBITDA'].sum():.1f} MCHF")
k4.metric("Net Profit", f"{finance_df['Net Profit'].sum():.1f} MCHF")

# ===================== ML KPIs =====================
st.markdown("---")
st.subheader("📌 ML Key Performance Indicators")

m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Customers", df["Customer_ID"].nunique())
m2.metric("Total Transactions", df["Invoice ID"].nunique())
m3.metric("Top Category", df["Category"].value_counts().idxmax())
m4.metric("Avg Basket Size", round(df["Quantity"].mean(), 2))

# ===================== FINANCIAL TABLE =====================
st.markdown("---")
st.subheader("📋 Initiative Valuation (5 Years)")
st.dataframe(finance_df.style.format("{:.1f}"))

# ===================== COST ANALYSIS =====================
st.markdown("---")
st.subheader("💰 Cost Analysis")

cost_df = pd.DataFrame({
    "Cost Type": ["COGS", "Marketing", "Personnel"],
    "Amount": [
        finance_df["COGS"].sum(),
        finance_df["Marketing"].sum(),
        finance_df["Personnel"].sum()
    ]
})

pie = px.pie(
    cost_df,
    names="Cost Type",
    values="Amount",
    hole=0.45
)
st.plotly_chart(pie, use_container_width=True)

# ===================== YEARLY PROFIT =====================
st.markdown("---")
st.subheader("📊 Yearly Profit Overview")

fig = go.Figure()
fig.add_bar(x=finance_df["Year"], y=finance_df["EBITDA"], name="EBITDA")
fig.add_bar(x=finance_df["Year"], y=finance_df["Tax"], name="Tax")
fig.add_scatter(
    x=finance_df["Year"],
    y=finance_df["Net Profit"],
    name="Net Profit",
    mode="lines+markers"
)
fig.update_layout(barmode="group")
st.plotly_chart(fig, use_container_width=True)

# ===================== ML INSIGHTS =====================
st.markdown("---")
st.header("🤖 Machine Learning Insights")

# ---- Top Product per Customer ----
st.subheader("🧾 Top Product per Customer")
st.dataframe(top_product_per_customer(df))

# ---- Area-wise Demand ----
st.subheader("📍 Area-wise Product Demand")
area_df = area_wise_demand(df)
st.dataframe(area_df.head(10))

area_chart = px.bar(
    area_df.head(10),
    x="Area",
    y="Quantity",
    color="Category",
    title="Top Product Categories by Area"
)
st.plotly_chart(area_chart, use_container_width=True)

# ---- Customer Segmentation ----
st.subheader("👥 Customer Segmentation")
st.dataframe(customer_clustering(df))

# ---- Market Basket Analysis ----
st.subheader("🧺 Market Basket Analysis")
rules = market_basket_analysis(df)
st.dataframe(rules.head(10))

# ===================== EXPORT =====================
st.markdown("---")
st.subheader("📥 Export Report")

@st.cache_data
def convert_df(dataframe):
    return dataframe.to_csv(index=False).encode("utf-8")

csv = convert_df(df)

st.download_button(
    label="⬇️ Download Filtered Data (CSV)",
    data=csv,
    file_name="retail_analysis_report.csv",
    mime="text/csv"
)