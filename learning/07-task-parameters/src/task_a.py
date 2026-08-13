# Databricks notebook source
# MAGIC %md
# MAGIC # 📤 Task A: Setting Task Values
# MAGIC This notebook determines dynamic values (like a table name) and passes them downstream.

# COMMAND ----------

# We will use our standard schema: main.demo
dynamic_table_name = "main.demo.daily_sales_landing"
current_mode = "incremental"

print(f"Setting target_table to: {dynamic_table_name}")
print(f"Setting run_mode to: {current_mode}")

# Use dbutils to set the task values so downstream tasks can grab them
dbutils.jobs.taskValues.set(key="target_table", value=dynamic_table_name)
dbutils.jobs.taskValues.set(key="run_mode", value=current_mode)

# COMMAND ----------

print("✅ Task A Complete. Values have been broadcasted.")