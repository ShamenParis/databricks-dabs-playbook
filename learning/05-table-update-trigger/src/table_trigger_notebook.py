# Databricks notebook source
# MAGIC %md
# MAGIC # 🔄 Table Update Processor
# MAGIC This notebook is automatically triggered by Databricks when the upstream Delta table (`main.default.landing_table`) receives new data.

# COMMAND ----------

from datetime import datetime

current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(f"🚀 Table Update Trigger activated at: {current_time}")

# COMMAND ----------

print("Reading the latest version of main.default.landing_table...")
print("Executing downstream transformations and aggregations...")

# Simulate processing the updated table
data = [("Row_Count", 45000), ("Latest_Commit_Version", 12)]
df = spark.createDataFrame(data, ["Metric", "Value"])

df.show()

# COMMAND ----------

print("✅ Downstream processing completed successfully.")