---
layout: default
title: Learning Modules
nav_order: 3
has_children: true
has_toc: false
permalink: /learning/
---

# Learning Modules

Structured learning modules for Databricks Asset Bundles (DABs). Each module builds on the previous one, starting from a basic "Hello World" deployment and progressing to advanced workflow orchestration patterns.

> **Before you begin**, make sure you've completed the [Prerequisites and Local Setup]({{ site.baseurl }}/prerequisites).

---

| # | Module | Description | Tech Stack |
| :--- | :--- | :--- | :--- |
| 01 | [01. Introduction to DABs]({{ site.baseurl }}/learning/01-introduction-to-dab) | Set up your local environment and deploy your first Hello World Databricks Asset Bundle | DABs, YAML, Python |
| 02 | [02. Job with Parameters]({{ site.baseurl }}/learning/02-job-parameters) | Define job parameters and pass dynamic values into a PySpark script at runtime | DABs, YAML, PySpark |
| 03 | [03. Schedule a Job]({{ site.baseurl }}/learning/03-schedule-a-job) | Automate job execution with Quartz cron expressions and deploy notebooks as Python files | DABs, YAML, Python |
| 04 | [04. File Trigger]({{ site.baseurl }}/learning/04-file-trigger) | Trigger a job automatically when a new file lands in a Unity Catalog Volume | DABs, YAML, Unity Catalog |
| 05 | [05. Table Update Trigger]({{ site.baseurl }}/learning/05-table-update-trigger) | Trigger a job automatically when a Delta Table is updated | DABs, YAML, Delta Lake |
| 06 | [06. Run Multiple Tasks]({{ site.baseurl }}/learning/06-run-multiple-tasks) | Build a Directed Acyclic Graph (DAG) with parallel tasks and sequential dependencies | DABs, YAML, Python |
| 07 | [07. Task Parameters]({{ site.baseurl }}/learning/07-task-parameters) | Pass dynamic values from an upstream task to multiple downstream tasks using `taskValues` | DABs, YAML, Python |
| 08 | [08. Conditional Execution]({{ site.baseurl }}/learning/08-use-if-else-task) | Implement success and failure routing using the `run_if` parameter | DABs, YAML, Python |
| 09 | [09. SQL Tasks with Variable Lookup]({{ site.baseurl }}/learning/09-sql-tasks-with-variable-lookup) | Execute raw SQL files on a SQL Warehouse and resolve infrastructure IDs dynamically using `lookup` | DABs, YAML, SQL |
| 10 | [10. SQL Alerts]({{ site.baseurl }}/learning/10-run-sql-alerts) | Provision SQL Alerts and trigger them from a Workflow using `alert_task` | DABs, YAML, SQL |
| 11 | [11. Run dbt on Databricks]({{ site.baseurl }}/learning/11-run-dbt-on-databricks) | Orchestrate a dbt Core project natively in Databricks Workflows using the `dbt_task` type | DABs, YAML, dbt, SQL |
| 12 | [12. Create a Pipeline]({{ site.baseurl }}/learning/12-create-pipeline) | Provision a Serverless Delta Live Tables pipeline with Bronze and Silver layers | DABs, YAML, DLT, Python |
| 13 | [13. Advanced Orchestration]({{ site.baseurl }}/learning/13-advanced-job-pipeline) | Build a master orchestrator that triggers a notebook, a DLT pipeline, and a child job in a single workflow | DABs, YAML, DLT, Python |
