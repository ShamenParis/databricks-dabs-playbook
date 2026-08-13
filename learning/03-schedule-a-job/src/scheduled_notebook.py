# Databricks notebook source
# MAGIC %md
# MAGIC # 🕒 Scheduled Daily Aggregation
# MAGIC This notebook is orchestrated via Databricks Asset Bundles and runs on a schedule.

# COMMAND ----------

from datetime import datetime

current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(f"🚀 Scheduled job started at: {current_time}")

# COMMAND ----------

# In a Databricks notebook environment, the 'spark' session is automatically provided.
print("Executing daily data aggregation...")

# Simulate data processing
data = [("Sales", 15000), ("Marketing", 3200), ("Engineering", 8500)]
df = spark.createDataFrame(data, ["Department", "Daily_Spend"])

df.show()

# COMMAND ----------

print("✅ Scheduled run completed successfully.")