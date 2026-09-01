---
layout: default
title: "13. Advanced Orchestration"
parent: Learning Modules
nav_order: 13
permalink: /learning/13-advanced-job-pipeline
---

# 13: Advanced Job and Pipeline Orchestration

<a href="https://github.com/ShamenParis/databricks-dabs-playbook/tree/main/learning/13-advanced-job-pipeline" class="btn-source" target="_blank">📂 View Source Code</a>

---

In this module, you will build a Master Orchestrator workflow that ties together all major Databricks resource types within a single bundle deployment. The master job executes a local notebook, triggers a Delta Live Tables pipeline, and then triggers a completely separate Databricks Workflow.

This pattern reflects real enterprise architectures where pipelines and reporting jobs are maintained by different teams but need to be coordinated within a single orchestration layer.

## What Are We Building?

![DAB Architecture Setup]({{ site.baseurl }}/images/learning/13-advanced-job-pipeline/01-architecture-diagram.png)

## Prerequisites and Local Setup

> Complete the [Prerequisites and Local Setup]({{ site.baseurl }}/prerequisites) before continuing.

## Bundle Structure

1. `databricks.yml` — Master control file that loads all resources via `**/*.yml`.
2. `resources/pipelines/dlt_pipeline.yml` — The declarative DLT pipeline.
3. `resources/jobs/child_job.yml` — A standalone child reporting workflow.
4. `resources/jobs/master_job.yml` — The master orchestrator. Uses `notebook_task`, `pipeline_task`, and `run_job_task` to chain the resources together using their dynamically resolved IDs (e.g., `${resources.pipelines.advanced_dlt_pipeline.id}`).
5. `src/` — Python and DLT source files for each task.

## How to Deploy and Run

Once authenticated, navigate to this folder (`13-advanced-job-pipeline`) in your terminal.

**Step 1: Validate and deploy**

```bash
databricks bundle validate
databricks bundle deploy
```

**Step 2: Run the master job**

You only need to trigger the master job. It will automatically trigger the DLT pipeline and the child job in sequence.

```bash
databricks bundle run master_orchestration_job
```

**Step 3: Verify the output**

In the Workflows UI, you will see Task A execute locally as a notebook, Task B show a dedicated pipeline execution node, and Task C show a direct link to the triggered `child_reporting_job` run instance.

<video controls width="100%" style="border-radius:8px; margin:1em 0;"><source src="{{ site.baseurl }}/images/learning/13-advanced-job-pipeline/02-advance-etl.mp4" type="video/mp4">Your browser does not support the video tag.</video>
