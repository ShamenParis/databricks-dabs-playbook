---
layout: default
title: "09. SQL Tasks with Variable Lookup"
parent: Learning Modules
nav_order: 9
permalink: /learning/09-sql-tasks-with-variable-lookup
---

# 09: SQL Tasks with Variable Lookup

<a href="https://github.com/ShamenParis/databricks-dabs-playbook/tree/main/learning/09-sql-tasks-with-variable-lookup" class="btn-source" target="_blank">📂 View Source Code</a>

---

In this module, you will learn two advanced enterprise patterns for orchestrating SQL workloads on Databricks:

1. **The `sql_task` type** — Executing raw SQL files directly on a Databricks SQL Warehouse.
2. **Variable Lookups** — Hardcoding infrastructure IDs such as a Warehouse ID is an anti-pattern because IDs differ across environments. The DAB `lookup` feature dynamically resolves the ID of a named resource at deploy time and injects it into the workflow configuration.

## What Are We Building?

![DAB Architecture Setup]({{ site.baseurl }}/images/learning/09-sql-tasks-with-variable-lookup/01-architecture-diagram.png)

## Prerequisites and Local Setup

> Complete the [Prerequisites and Local Setup]({{ site.baseurl }}/prerequisites) before continuing.

**Additional requirement:** A SQL Warehouse named exactly `Serverless Starter Warehouse` must exist in your Databricks Workspace (this is usually present by default).

## Bundle Structure

1. `databricks.yml` — Master control file. Uses the `variables` and `lookup` blocks to dynamically resolve the `sql_warehouse_id` by warehouse name at deploy time.
2. `resources/jobs/sql_orchestration_job.yml` — Defines the workflow using `sql_task` and the `${var.sql_warehouse_id}` substitution syntax.
3. `src/task_a_setup.py` — A Python notebook that creates and populates a Delta table in `main.demo`.
4. `src/task_b_transform.sql` — A raw SQL script that inserts and aggregates data using the SQL Warehouse engine.

## How to Deploy and Run

Once authenticated, navigate to this folder (`09-sql-tasks-with-variable-lookup`) in your terminal.

**Step 1: Validate and deploy**

```bash
databricks bundle validate
databricks bundle deploy
```

![Deployment Success]({{ site.baseurl }}/images/learning/09-sql-tasks-with-variable-lookup/02-success-deploy.png)

**Step 2: Run the job**

```bash
databricks bundle run sql_orchestration_job
```

![SQL Orchestration]({{ site.baseurl }}/images/learning/09-sql-tasks-with-variable-lookup/03-sql-job.png)
