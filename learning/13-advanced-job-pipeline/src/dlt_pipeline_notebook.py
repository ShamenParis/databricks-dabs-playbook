# Databricks notebook source
import dlt
import pyspark.sql.functions as F

@dlt.table(name="bronze_transactions")
def bronze_transactions():
    return spark.read.table("main.demo.raw_advanced_data")

@dlt.table(name="silver_completed_transactions")
def silver_completed_transactions():
    return dlt.read("bronze_transactions").filter(F.col("status") == "COMPLETED")