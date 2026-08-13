# Databricks notebook source
# This file is deployed to Databricks as a notebook via DAB.

# COMMAND ----------
# MAGIC %md
# MAGIC # 02 — Transform Data
# MAGIC
# MAGIC Reads from Bronze layer, applies transformations, writes to Silver layer.

# COMMAND ----------

from pyspark.sql import functions as F

# Job parameters
dbutils.widgets.text("table_name", "raw_events")
table_name = dbutils.widgets.get("table_name")

catalog = spark.conf.get("spark.databricks.sql.initial.catalog.name", "dataengineering_dev")
source_table = f"{catalog}.bronze.{table_name}"
target_table = f"{catalog}.silver.{table_name}"

print(f"Transforming: {source_table} → {target_table}")

# COMMAND ----------

df = spark.table(source_table)

# Example transformations — adapt to your schema
df_transformed = (
    df
    .withColumn("ingestion_date", F.current_date())
    .withColumn("ingestion_ts", F.current_timestamp())
    .dropDuplicates()
    .filter(F.col("event_id").isNotNull())
)

print(f"Rows after transform: {df_transformed.count()}")

# COMMAND ----------

(
    df_transformed.write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable(target_table)
)

print(f"✓ Written to: {target_table}")
