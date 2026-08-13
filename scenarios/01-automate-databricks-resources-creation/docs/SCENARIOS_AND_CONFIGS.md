# Scenarios and Configurations Guide

This document outlines the various deployment scenarios supported by the automation framework and provides instructions on how to add and manage configurations.

## Overview

The Databricks Asset Bundles generator allows Data Engineers and Analysts to define their resources declaratively using simple JSON files. The framework supports a variety of complex workflow orchestration and resource generation scenarios.

---

## 1. Job Orchestration Scenarios

### 1.1 Standard Notebook/Python/SQL Jobs
Schedule standard notebooks, Python scripts, or SQL files to run automatically.
- **How to add**: Place a JSON file in `configs/jobs/`.
- **Config requirements**:
  - `resource_type: "job"`
  - Define `tasks` array where `task_type` is `notebook_task`, `python_task`, or `sql_task`.
  - For Notebook tasks, provide `notebook_path`.
  - Provide `schedule_cron_expression` to run on a schedule.

### 1.2 Running Jobs Inside Jobs (Nested Jobs)
Orchestrate a "master" job that triggers one or more existing Databricks jobs as individual tasks.
- **How to add**: Use the `run_job_task` type inside your job config.
- **Config requirements**:
  - `task_type: "run_job_task"`
  - Provide the Databricks `job_id` of the job you want to run.
  - (Optional) Provide `job_parameters` to pass arguments to the nested job.

### 1.3 Running Pipelines from Jobs
Trigger a Delta Live Tables (DLT) pipeline directly from a job workflow, allowing you to sequence data ingestion jobs before DLT processing.
- **How to add**: Use the `pipeline_task` type inside your job config.
- **Config requirements**:
  - `task_type: "pipeline_task"`
  - Provide the Databricks `pipeline_id` of the target pipeline.
  - (Optional) Set `full_refresh: true` if you want to force a full recompute.

### 1.4 Setting Up Task Dependencies
Sequence tasks so they run only after previous tasks succeed.
- **How to add**: Use the `dependance_task_keys` array on the downstream task.
- **Config requirements**:
  - Add the upstream task's `task_key` to the `dependance_task_keys` array of the downstream task. The framework will automatically map this to the DAB `depends_on` block.

---

## 2. Pipeline Scenarios

### 2.1 Delta Live Tables (DLT)
Deploy scalable streaming and batch pipelines.
- **How to add**: Place a JSON file in `configs/pipelines/`.
- **Config requirements**:
  - `resource_type: "pipeline"`
  - Define `clusters` (or use serverless).
  - Define the `libraries` array pointing to your pipeline notebooks.
  - Set `continuous: true` for 24/7 streaming or `false` for triggered batch runs.

---

## 3. Data Quality & Analytics Scenarios

### 3.1 Lakehouse Quality Monitors
Attach automatic data quality monitoring to your Unity Catalog tables.
- **How to add**: Place a JSON file in `configs/quality_monitors/`.
- **Config requirements**:
  - `resource_type: "quality_monitor"`
  - Provide the fully qualified `table_name`.
  - Set `monitor_type` to `timeseries`, `snapshot`, or `inference`.
  - For timeseries, provide the `timestamp_col`.

### 3.2 AI/BI Dashboards (Lakeview)
Deploy interactive dashboards directly from code.
- **How to add**: Place a JSON file in `configs/dashboards/`.
- **Config requirements**:
  - `resource_type: "dashboard"`
  - Ensure `sql_warehouse_id` is defined in your environment variables.
  - Provide `file_path` pointing to your exported `.lvdash.json` file. If omitted, the framework deploys an empty dashboard for you to populate in the Databricks UI.

---

## Adding Configurations

To add any configuration:
1. Copy one of the sample JSON files from the documentation or an existing team config.
2. Place it in the appropriate `teams/<TeamName>/<Environment>/configs/<resource_type>/` folder.
3. Validate your config using: `python src/job_config_validator.py --team <TeamName> --env <Environment>`
4. Generate the bundle using: `python src/generate_resources.py --team <TeamName> --env_name <Environment>`
5. Deploy from the `bundle` directory: `databricks bundle deploy -t development`.
