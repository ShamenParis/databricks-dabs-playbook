# Databricks notebook source
# DLT Bronze Ingestion Notebook — deployed as a DLT library.

# COMMAND ----------
# MAGIC %md
# MAGIC # Bronze Layer — Raw Data Ingestion (DLT)
# MAGIC Reads raw data from the landing zone and creates a DLT streaming table in Bronze.

# COMMAND ----------

import dlt
from pyspark.sql import functions as F

SOURCE_PATH = "/mnt/landing/events"   # Update to your landing path

@dlt.table(
    name="bronze_raw_events",
    comment="Raw events ingested from the landing zone.",
    table_properties={"quality": "bronze"},
)
def bronze_raw_events():
    return (
        spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", "json")
        .option("cloudFiles.schemaLocation", "/mnt/schemas/raw_events")
        .load(SOURCE_PATH)
        .withColumn("ingestion_timestamp", F.current_timestamp())
        .withColumn("_source_file", F.input_file_name())
    )
