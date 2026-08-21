# Databricks notebook source

df = spark.createDataFrame([('Alice', 1), ('Bob', 2), ('Charlie', 3)], ['name', 'id'])
df.display()

print("This is notebook A")