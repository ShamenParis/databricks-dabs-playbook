# 12: Create a Delta Live Tables Pipeline

In this module, you will learn how to provision a Serverless Delta Live Tables (DLT) pipeline using Databricks Asset Bundles. DLT is a declarative framework where you define the desired state of your tables rather than explicitly sequencing tasks — Databricks automatically builds the execution graph and manages compute.

The pipeline in this module demonstrates a Bronze-to-Silver pattern: raw data is ingested into a Bronze table, then filtered into a Silver table containing only active records.

## What Are We Building?

![DAB Architecture Setup](../../docs/learning/12-create-pipeline/01-architecture-diagram.png)

## Prerequisites and Local Setup

[Prerequisites and Local Setup](../../docs/learning/00-initial-setup/README.md)

## Bundle Structure

1. `databricks.yml` — Master control file.
2. `resources/pipelines/dlt_pipeline.yml` — Defines the pipeline configuration using serverless compute and targeting the `main.demo` catalog and schema.
3. `src/dlt_pipeline_notebook.py` — Uses the `dlt` library to declaratively define the Bronze and Silver tables.

## How to Deploy and Run

Once authenticated, navigate to this folder (`12-create-pipeline`) in your terminal.

**Step 1: Validate and deploy**

```bash
databricks bundle validate
databricks bundle deploy
```

**Step 2: Run the pipeline**

Note: use `demo_dlt_pipeline` (the pipeline key), not a job key.

```bash
databricks bundle run demo_dlt_pipeline
```

**Step 3: Verify the output**

In the Databricks UI, navigate to the **Delta Live Tables** tab. You will see the pipeline DAG rendered visually, with `bronze_customers` flowing into `silver_active_customers`. You can also query `main.demo.silver_active_customers` directly in the SQL Editor.

![DLT Pipeline Graph](../../docs/learning/12-create-pipeline/02-dlt-pipeline-graph.png)