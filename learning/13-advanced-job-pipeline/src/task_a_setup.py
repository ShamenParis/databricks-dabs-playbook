# Databricks notebook source
print("Setting up raw data for the pipeline...")
spark.sql("CREATE TABLE IF NOT EXISTS main.demo.raw_advanced_data (id INT, amount DOUBLE, status STRING)")
spark.sql("TRUNCATE TABLE main.demo.raw_advanced_data")
spark.sql("INSERT INTO main.demo.raw_advanced_data VALUES (1, 150.50, 'COMPLETED'), (2, 45.00, 'PENDING')")
print("Table main.demo.raw_advanced_data is ready.")