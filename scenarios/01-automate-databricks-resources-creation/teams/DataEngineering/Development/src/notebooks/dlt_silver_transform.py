# Databricks notebook source
# DLT Silver Transformation Notebook

# COMMAND ----------
# MAGIC %md
# MAGIC # Silver Layer — Data Cleansing and Joining (DLT)
# MAGIC Reads from the bronze table, cleans data, and creates a silver streaming table.

# COMMAND ----------

import dlt
from pyspark.sql import functions as F

@dlt.table(
    name="silver_cleaned_events",
    comment="Cleaned and validated events ready for analysis.",
    table_properties={"quality": "silver"}
)
@dlt.expect_or_drop("valid_timestamp", "ingestion_timestamp IS NOT NULL")
def silver_cleaned_events():
    return (
        dlt.read_stream("bronze_raw_events")
        .withColumn("processed_date", F.to_date("ingestion_timestamp"))
        .filter(F.col("processed_date").isNotNull())
    )
