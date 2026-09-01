---
layout: default
title: "05. Table Update Trigger"
parent: Learning Modules
nav_order: 5
permalink: /learning/05-table-update-trigger
---

# 05: Table Update Trigger

<a href="https://github.com/ShamenParis/databricks-dabs-playbook/tree/main/learning/05-table-update-trigger" class="btn-source" target="_blank">📂 View Source Code</a>

---

In this module, you will learn how to configure a Databricks Job to automatically run the moment a specific Delta Table is updated. This pattern is common in Lakehouse architectures where pipelines are chained by data availability rather than rigid schedules.

## What Are We Building?

![DAB Architecture Setup]({{ site.baseurl }}/images/learning/05-table-update-trigger/01-architecture-diagram.png)

## Prerequisites and Local Setup

> Complete the [Prerequisites and Local Setup]({{ site.baseurl }}/prerequisites) before continuing.

### Additional Requirement

You must have a Unity Catalog Delta table at `main.demo.landing_table`. If you do not have one, run the following SQL:

```sql
CREATE TABLE IF NOT EXISTS main.demo.landing_table (col1 INT, col2 STRING);
```

Alternatively, update the `table_names` configuration in `table_trigger_job.yml` to point to an existing Delta table in your workspace.

## Bundle Structure

1. `databricks.yml` — The master control file.
2. `resources/jobs/table_trigger_job.yml` — Contains the `trigger: table_update` block, which monitors a Delta table's transaction log for changes.
3. `src/table_trigger_notebook.py` — The downstream notebook that executes when the trigger fires.

## How to Deploy and Run

Once authenticated, navigate to this folder (`05-table-update-trigger`) in your terminal.

**Step 1: Validate and deploy**

```bash
databricks bundle validate
databricks bundle deploy
```

![Validation Deployment Success]({{ site.baseurl }}/images/learning/05-table-update-trigger/02-validation-deploy-success.png)

**Step 2: Verify the trigger in the UI**

Once deployed, the job will enter a "Waiting for table update" state. You can verify this in the Databricks Workflows UI under the Job details.

![Workspace UI]({{ site.baseurl }}/images/learning/05-table-update-trigger/03-workspace-ui.png)

**Step 3: Trigger the job**

Run a simple `INSERT`, `UPDATE`, or `MERGE` statement against `main.demo.landing_table` using the Databricks SQL Editor or a notebook. The job will detect the Delta commit and start automatically.

[View Demo: 04-trigger-job.mp4](../../docs/learning/05-table-update-trigger/04-trigger-job.mp4)
