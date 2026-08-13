# Databricks notebook source
# MAGIC %md
# MAGIC # Task C: Failure Path
# MAGIC This notebook only executes if Task A fails (`run_if: ALL_FAILED`).

# COMMAND ----------

print("Task C Executing: Recovery / Alert Path!")
print("Task A failed. Running cleanup processes and sending failure alerts...")