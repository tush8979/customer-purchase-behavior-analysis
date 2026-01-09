import matplotlib.pyplot as plt

def area_sales(df):
    df.groupby('Area')['Total_Amount'].sum().plot(kind='bar')
    plt.title("Area-wise Sales")
    plt.show()