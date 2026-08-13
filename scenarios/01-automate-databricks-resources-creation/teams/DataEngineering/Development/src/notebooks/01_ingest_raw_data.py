# Databricks notebook source
# This file is deployed to Databricks as a notebook via DAB.

# COMMAND ----------
# MAGIC %md
# MAGIC # 01 — Ingest Raw Data
# MAGIC
# MAGIC Reads raw event data from the landing zone and writes it to the Bronze layer.

# COMMAND ----------

import sys

# Job parameters passed in via base_parameters
dbutils.widgets.text("table_name", "raw_events")
dbutils.widgets.text("source_path", "/mnt/landing/events")

table_name = dbutils.widgets.get("table_name")
source_path = dbutils.widgets.get("source_path")

print(f"Ingesting table: {table_name}")
print(f"Source path:     {source_path}")

# COMMAND ----------

# Read from landing zone (adjust for your data format)
df = spark.read.format("json").load(source_path)

print(f"Rows read: {df.count()}")
df.printSchema()

# COMMAND ----------

# Write to Bronze layer (Unity Catalog)
catalog = spark.conf.get("spark.databricks.sql.initial.catalog.name", "dataengineering_dev")
target_table = f"{catalog}.bronze.{table_name}"

(
    df.write
    .format("delta")
    .mode("append")
    .saveAsTable(target_table)
)

print(f"✓ Written to: {target_table}")
