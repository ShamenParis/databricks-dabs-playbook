# Databricks notebook source
# MAGIC %md
# MAGIC # Delta Live Tables Pipeline
# MAGIC Declarative data pipeline moving data from Bronze (Raw) to Silver (Cleaned).

# COMMAND ----------

import dlt
import pyspark.sql.functions as F

# 1. Define the Bronze Layer (Raw Data)
@dlt.table(
    name="bronze_customers",
    comment="Raw customer ingestion layer."
)
def bronze_customers():
    print("Ingesting raw data into bronze...")
    # Simulating raw incoming data
    data = [(1, "Alice", "ACTIVE"), (2, "Bob", "INACTIVE"), (3, "Charlie", "ACTIVE")]
    return spark.createDataFrame(data, ["id", "name", "status"])

# COMMAND ----------

# 2. Define the Silver Layer (Cleaned Data)
# DLT automatically knows this must run AFTER bronze_customers
@dlt.table(
    name="silver_active_customers",
    comment="Filtered layer containing only active customers."
)
def silver_active_customers():
    print("Filtering active customers for silver layer...")
    # Read declaratively from the bronze table in the same pipeline
    return dlt.read("bronze_customers").filter(F.col("status") == "ACTIVE")