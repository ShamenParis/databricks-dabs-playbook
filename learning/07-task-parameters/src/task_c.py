# Databricks notebook source
# MAGIC %md
# MAGIC # 📥 Task C: Parallel Parameter Reception
# MAGIC This notebook also receives the table name from Task A, running concurrently with Task B.

# COMMAND ----------

dbutils.widgets.text("table_to_process", "default_table")

# COMMAND ----------

target = dbutils.widgets.get("table_to_process")

print(f"🚀 Task C received target table: {target}")
print(f"Running data quality checks on {target}...")

# COMMAND ----------

print("✅ Task C Complete.")