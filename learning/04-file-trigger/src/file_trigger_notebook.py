# Databricks notebook source
# MAGIC %md
# MAGIC # 📂 File Arrival Processor
# MAGIC This notebook is automatically triggered by Databricks when a new file lands in the configured Unity Catalog Volume.

# COMMAND ----------

from datetime import datetime

current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(f"🚀 File Arrival Trigger activated at: {current_time}")

# COMMAND ----------

# In a real-world scenario, you would dynamically read the incoming file here.
# For example: df = spark.read.csv("/Volumes/main/default/landing_zone/")

print("Scanning landing zone for new data...")
print("Processing incoming files...")

# Simulate processing
data = [("event_id_789", "SUCCESS", "2026-08-12")]
df = spark.createDataFrame(data, ["Event_ID", "Status", "Processed_Date"])

df.show()

# COMMAND ----------

print("✅ File processing completed. Ready for the next arrival.")