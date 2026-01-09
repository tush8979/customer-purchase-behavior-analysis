from statsmodels.tsa.arima.model import ARIMA

def forecast_sales(df):
    daily = df.groupby('Date')['Total_Amount'].sum()
    model = ARIMA(daily, order=(1,1,1)).fit()
    return model.forecast(7)