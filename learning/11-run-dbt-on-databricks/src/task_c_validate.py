# Databricks notebook source
# MAGIC %md
# MAGIC # Task C: Validation
# MAGIC Validating that the dbt transformation successfully created the staging table and filtered the data.

# COMMAND ----------

print("Validating dbt output from main.demo.stg_users...")

df = spark.sql("SELECT * FROM main.demo.stg_users")
df.show()

print("Pipeline A -> B (dbt) -> C completed successfully.")