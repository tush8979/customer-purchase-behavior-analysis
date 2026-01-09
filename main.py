import argparse
import logging
from src.data_loader import load_transactions, load_store_sales
from src.customer_analysis import top_product_per_customer
from src.clustering import customer_clustering
from src.store_sales_prediction import predict_store_sales

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main(args):
    if args.transactions:
        logger.info("Running customer behavior pipeline")
        df = load_transactions(args.transactions)
        print("\nTop Product per Customer:\n", top_product_per_customer(df))
        print("\nCustomer Clusters:\n", customer_clustering(df))

    if args.store_sales:
        logger.info("Running store sales prediction pipeline")
        store_df = load_store_sales(args.store_sales)
        r2 = predict_store_sales(store_df)
        print(f"\nStore Sales Prediction R2 Score: {r2:.2f}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Retail Intelligence System"
    )
    parser.add_argument(
        "--transactions",
        help="Path to transaction dataset (customer behavior)"
    )
    parser.add_argument(
        "--store-sales",
        help="Path to store sales dataset (store prediction)"
    )
    args = parser.parse_args()
    main(args)