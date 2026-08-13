# Databricks notebook source
# MAGIC %md
# MAGIC # 📥 Task B: Receiving Task Values
# MAGIC This notebook receives the parameters passed by Task A via the YAML configuration.

# COMMAND ----------

# Create widgets to accept the incoming base_parameters
dbutils.widgets.text("table_to_process", "default_table")
dbutils.widgets.text("run_mode", "default_mode")

# COMMAND ----------

# Retrieve the values
target = dbutils.widgets.get("table_to_process")
mode = dbutils.widgets.get("run_mode")

print(f"🚀 Task B received target table: {target}")
print(f"🚀 Task B received run mode: {mode}")

print(f"Executing {mode} logic on {target}...")

# COMMAND ----------

print("✅ Task B Complete.")