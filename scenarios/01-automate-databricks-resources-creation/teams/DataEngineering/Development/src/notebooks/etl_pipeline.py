# This file is deployed to Databricks as a Python script via DAB (spark_python_task).

import sys
import argparse
from datetime import datetime

def parse_args():
    parser = argparse.ArgumentParser(description="ETL Pipeline")
    parser.add_argument("--environment", default="development")
    parser.add_argument("--batch_date", default=datetime.today().strftime("%Y-%m-%d"))
    return parser.parse_args()

def main():
    args = parse_args()
    print(f"Running ETL pipeline for environment={args.environment}, batch_date={args.batch_date}")

    # ── Replace the code below with your actual ETL logic ──────────────────────
    from pyspark.sql import SparkSession
    spark = SparkSession.builder.appName("ETLPipeline").getOrCreate()
    catalog = spark.conf.get("spark.databricks.sql.initial.catalog.name", "dataengineering_dev")

    print(f"Catalog: {catalog}")
    print("ETL pipeline completed successfully.")

if __name__ == "__main__":
    main()
