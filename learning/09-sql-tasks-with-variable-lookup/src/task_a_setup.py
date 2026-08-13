# Databricks notebook source
# MAGIC %md
# MAGIC # Task A: Environment Setup
# MAGIC This notebook creates a target table in `main.demo` so our SQL task has data to manipulate.

# COMMAND ----------

print("Setting up target table for SQL execution...")

# Create a simple table in our standard catalog and schema
spark.sql("""
    CREATE TABLE IF NOT EXISTS main.demo.sql_lesson_data (
        id INT,
        status STRING,
        processed_date TIMESTAMP
    )
""")

# Clear any existing data for clean rerun testing
spark.sql("TRUNCATE TABLE main.demo.sql_lesson_data")

print("Table main.demo.sql_lesson_data is ready.")