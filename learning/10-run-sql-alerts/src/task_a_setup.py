# Databricks notebook source
# MAGIC %md
# MAGIC # Task A: Environment Setup
# MAGIC We are creating a table and intentionally inserting an 'ERROR' record so our SQL Alert will trigger successfully.

# COMMAND ----------

print("Setting up target table for the Alert...")

# Create the table
spark.sql("""
    CREATE TABLE IF NOT EXISTS main.demo.alerts_data (
        id INT,
        status STRING,
        processed_date TIMESTAMP
    )
""")

spark.sql("TRUNCATE TABLE main.demo.alerts_data")

# Insert a failure record to ensure the alert condition (error_count > 0) is met
spark.sql("""
    INSERT INTO main.demo.alerts_data (id, status, processed_date)
    VALUES 
        (1, 'SUCCESS', current_timestamp()),
        (2, 'ERROR', current_timestamp())
""")

print("Table main.demo.alerts_data is populated with an ERROR record.")