# Databricks notebook source
# MAGIC %md
# MAGIC # Task A: Evaluation Task
# MAGIC This task reads a parameter and either succeeds or intentionally throws an error to demonstrate branching logic.

# COMMAND ----------

dbutils.widgets.text("simulate_failure", "false")
simulate_failure = dbutils.widgets.get("simulate_failure").lower()

print(f"Running Task A. simulate_failure parameter is set to: {simulate_failure}")
print("Target Schema: main.demo")

# COMMAND ----------

if simulate_failure == "true":
    raise Exception("Simulated task failure triggered! Routing to Task C...")
else:
    print("Task A completed successfully. Routing to Task B...")