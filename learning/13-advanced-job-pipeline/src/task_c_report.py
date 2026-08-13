# Databricks notebook source
print("Child Job Executing: Generating summary report...")
df = spark.sql("SELECT * FROM main.demo.silver_completed_transactions")
df.show()
print("Reporting complete.")