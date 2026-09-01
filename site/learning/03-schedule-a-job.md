---
layout: default
title: "03. Schedule a Job"
parent: Learning Modules
nav_order: 3
permalink: /learning/03-schedule-a-job
---

# 03: Schedule a Job

<a href="https://github.com/ShamenParis/databricks-dabs-playbook/tree/main/learning/03-schedule-a-job" class="btn-source" target="_blank">📂 View Source Code</a>

---

In this module, you will learn how to automate job execution using cron schedules and how to deploy standard Python files as Databricks Notebooks.

Key concepts covered:

1. **Notebook Source Format:** Using `# Databricks notebook source` to version-control notebooks as standard Python files while allowing cell-by-cell execution with `# COMMAND ----------`.
2. **Cron Scheduling:** Automating workflows using the `schedule` block with Quartz cron expressions.

## What Are We Building?

![DAB Architecture Setup]({{ site.baseurl }}/images/learning/03-schedule-a-job/01-architecture-diagram.png)

## Prerequisites and Local Setup

> Complete the [Prerequisites and Local Setup]({{ site.baseurl }}/prerequisites) before continuing.

## Bundle Structure

1. `databricks.yml` — The master control file that uses `include:` to load external YAML files.
2. `resources/jobs/scheduled_job.yml` — Contains the job definition and the Quartz cron schedule configuration.
3. `src/scheduled_notebook.py` — A Python file formatted as a Databricks Notebook.

## How to Deploy and Run

Once authenticated, navigate to this folder (`03-schedule-a-job`) in your terminal.

**Step 1: Validate and deploy**

```bash
databricks bundle validate
databricks bundle deploy
```

![Validation Deploy Success]({{ site.baseurl }}/images/learning/03-schedule-a-job/02-validation-deploy-success.png)

**Step 2: Verify the schedule**

Once deployed, the job will automatically run based on the cron schedule (every day at 8:00 AM London time). You can verify the schedule is active in the Databricks Workflows UI.

![Workflow UI View]({{ site.baseurl }}/images/learning/03-schedule-a-job/03-scheduled-job-ui.png)
