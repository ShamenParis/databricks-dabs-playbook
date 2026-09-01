---
layout: default
title: "02. Job with Parameters"
parent: Learning Modules
nav_order: 2
permalink: /learning/02-job-parameters
---

# 02: Job with Parameters

<a href="https://github.com/ShamenParis/databricks-dabs-playbook/tree/main/learning/02-job-parameters" class="btn-source" target="_blank">📂 View Source Code</a>

---

In this module, you will learn two core enterprise concepts:

1. **Modular Architecture:** Separating DAB configurations into dedicated resource folders (`jobs/`, `pipelines/`, etc.).
2. **Dynamic Workflows:** Defining job parameters and passing them into a PySpark script at runtime.

## What Are We Building?

![DAB Architecture Setup]({{ site.baseurl }}/images/learning/02-job-parameters/01-architecture-diagram.png)

## Prerequisites and Local Setup

> Complete the [Prerequisites and Local Setup]({{ site.baseurl }}/prerequisites) before continuing.

## Bundle Structure

1. `databricks.yml` — The master control file that uses `include:` to load external YAML files.
2. `resources/jobs/parameterized_job.yml` — Contains the job definition and default parameter values.
3. `src/job_parameters.py` — A PySpark script that uses `argparse` to accept command-line arguments.

## How to Deploy and Run

Once authenticated, navigate to this folder (`02-job-parameters`) in your terminal.

**Step 1: Validate and deploy**

```bash
databricks bundle validate
databricks bundle deploy
```

![Validation Deploy Success]({{ site.baseurl }}/images/learning/02-job-parameters/02-validation-deploy-success.png)

**Step 2: Run the job with default parameters**

This uses the default values defined in `resources/jobs/parameterized_job.yml`.

```bash
databricks bundle run parameterized_job
```

![Job Run Default Values]({{ site.baseurl }}/images/learning/02-job-parameters/03-run-job-with-default-param.png)

![Workflow UI View]({{ site.baseurl }}/images/learning/02-job-parameters/04-run-job-ui-with-default-param.png)

**Step 3: Run the job with overridden parameters**

You can inject new values at runtime without changing any code.

```bash
databricks bundle run parameterized_job --params environment=production,greeting="Hello YouTube"
```

![Job Run New Values]({{ site.baseurl }}/images/learning/02-job-parameters/05-run-job-with-new-param.png)

![Workflow UI View]({{ site.baseurl }}/images/learning/02-job-parameters/06-run-job-ui-with-new-param.png)
