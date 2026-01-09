# 🛒 Customer Purchase Behavior Analysis & Retail Intelligence System

An end-to-end **Retail Analytics and Machine Learning project** that analyzes supermarket transaction data to understand customer buying behavior, perform market basket analysis, segment customers, analyze area-wise demand, and predict store-level sales. The project is deployed as an interactive **Streamlit dashboard**.

---

## 🚀 Features
- Customer → Product purchase analysis
- Market Basket Analysis (Apriori)
- Customer Segmentation using K-Means
- Area-wise product demand analysis
- Store Sales Prediction using ML
- Interactive Streamlit dashboard

---

## 🧠 Tech Stack
- Python
- Pandas, NumPy
- Scikit-learn
- MLxtend
- Statsmodels
- Streamlit

---

## 📁 Project Structure
customer-purchase-behavior-analysis/
│
├── app.py
├── main.py
├── requirements.txt
├── README.md
│
├── data/
│   └── sample_transactions.csv
│
└── src/
├── data_loader.py
├── customer_analysis.py
├── clustering.py
├── market_basket.py
├── area_analysis.py
└── store_sales_prediction.py

---

## ▶️ How to Run Locally

```bash
pip install -r requirements.txt
python main.py --transactions data/sample_transactions.csv
streamlit run app.py
