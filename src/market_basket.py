from mlxtend.frequent_patterns import apriori, association_rules
import pandas as pd

def market_basket_analysis(df):
    # Create basket: Invoice × Category
    basket = df.pivot_table(
        index="Invoice ID",
        columns="Category",
        values="Quantity",
        aggfunc="sum",
        fill_value=0
    )

    # Convert to binary
    basket = basket.applymap(lambda x: 1 if x > 0 else 0)

    frequent_items = apriori(
        basket,
        min_support=0.05,
        use_colnames=True
    )

    rules = association_rules(
        frequent_items,
        metric="lift",
        min_threshold=1
    )

    return rules[["antecedents", "consequents", "support", "confidence", "lift"]]