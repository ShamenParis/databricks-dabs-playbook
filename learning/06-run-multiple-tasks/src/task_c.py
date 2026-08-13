# Databricks notebook source
# MAGIC %md
# MAGIC # 📊 Task C: Aggregation
# MAGIC This task waits for Task B to finish, completing the A -> B -> C pipeline.

# COMMAND ----------

print("🚀 Running Task C: Reading from main.demo.clean_events...")
print("Aggregating daily metrics...")
print("Saving metrics to main.demo.daily_metrics...")
print("✅ Task C Complete.")