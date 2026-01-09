import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score

def predict_store_sales(df):
    X = df[["Store_Area", "Items_Available", "Daily_Customer_Count"]]
    y = np.log1p(df["Store_Sales"])   # 🔥 KEY FIX

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestRegressor(
        n_estimators=500,
        max_depth=None,
        random_state=42
    )

    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    return r2_score(y_test, preds)