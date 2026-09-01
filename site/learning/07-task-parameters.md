---
layout: default
title: "07. Task Parameters"
parent: Learning Modules
nav_order: 7
permalink: /learning/07-task-parameters
---

# 07: Task Parameters — Passing Values Between Tasks

<a href="https://github.com/ShamenParis/databricks-dabs-playbook/tree/main/learning/07-task-parameters" class="btn-source" target="_blank">📂 View Source Code</a>

---

In this module, you will learn how to pass dynamic values from an upstream task to multiple downstream tasks. This is a core pattern for building data-aware pipelines where the output of one step controls the behaviour of the next.

The workflow uses `dbutils.jobs.taskValues.set()` in Task A to broadcast values, and routes those values to Task B and Task C using the `base_parameters` mapping syntax in the bundle configuration.

## What Are We Building?

![DAB Architecture Setup]({{ site.baseurl }}/images/learning/07-task-parameters/01-architecture-diagram.png)

## Prerequisites and Local Setup

> Complete the [Prerequisites and Local Setup]({{ site.baseurl }}/prerequisites) before continuing.

## Bundle Structure

1. `databricks.yml` — Master control file.
2. `resources/jobs/task_parameters_job.yml` — Defines the `base_parameters` mapping (e.g., `{% raw %}{{tasks.task_a.values.target_table}}{% endraw %}`).
3. `src/task_a.py` — Sets values using `dbutils.jobs.taskValues.set()`.
4. `src/task_b.py` and `src/task_c.py` — Retrieve values using `dbutils.widgets.get()`.

## How to Deploy and Run

Once authenticated, navigate to this folder (`07-task-parameters`) in your terminal.

**Step 1: Validate and deploy**

```bash
databricks bundle validate
databricks bundle deploy
```

![Validation and Deployment Success]({{ site.baseurl }}/images/learning/07-task-parameters/02-validation-deploy-success.png)

**Step 2: Run the job**

```bash
databricks bundle run task_parameters_job
```

![Run Workflow Success]({{ site.baseurl }}/images/learning/07-task-parameters/03-workflow-ui.png)

**Step 3: Verify the output**

Task B and Task C execute in parallel. Each receives the values broadcast by Task A.

<video controls width="100%" style="border-radius:8px; margin:1em 0;"><source src="{{ site.baseurl }}/images/learning/07-task-parameters/04-task-parameters.mp4" type="video/mp4">Your browser does not support the video tag.</video>
