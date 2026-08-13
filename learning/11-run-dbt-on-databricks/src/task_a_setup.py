# Databricks notebook source
# MAGIC %md
# MAGIC # Task A: Environment Setup
# MAGIC We are creating a raw table with mixed status records for dbt to process.

# COMMAND ----------

print("Setting up raw data for dbt...")

spark.sql("""
    CREATE TABLE IF NOT EXISTS main.demo.raw_dbt_users (
        id INT,
        name STRING,
        status STRING
    )
""")

spark.sql("TRUNCATE TABLE main.demo.raw_dbt_users")

spark.sql("""
    INSERT INTO main.demo.raw_dbt_users (id, name, status)
    VALUES 
        (1, 'Alice', 'active'),
        (2, 'Bob', 'inactive'),
        (3, 'Charlie', 'active')
""")

print("Table main.demo.raw_dbt_users is ready.")