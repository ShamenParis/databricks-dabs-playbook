---
layout: default
title: "01. Introduction to DABs"
parent: Learning Modules
nav_order: 1
permalink: /learning/01-introduction-to-dab
---

# 01: Introduction to Declarative Automation Bundles (DABs)

<a href="https://github.com/ShamenParis/databricks-dabs-playbook/tree/main/learning/01-introduction-to-dab" class="btn-source" target="_blank">📂 View Source Code</a>

---

In this module, you will set up your local development environment, authenticate with Databricks, and deploy your first "Hello World" Databricks Asset Bundle.

## What Are We Building?

![DAB Architecture Setup]({{ site.baseurl }}/images/learning/01-introduction-to-dab/01-architecture-diagram.png)

## Prerequisites and Local Setup

> Complete the [Prerequisites and Local Setup]({{ site.baseurl }}/prerequisites) before continuing.

## Bundle Structure

This module contains two core files:

1. `src/hello_world.py` — A basic Python script that prints a status message.
2. `databricks.yml` — The declarative configuration that tells Databricks how to deploy and run the script as a job.

## How to Deploy and Run

Once authenticated, navigate to this folder (`01-introduction-to-dab`) in your terminal.

**Step 1: Validate the bundle**

Ensures your YAML syntax is correct before deploying to the cloud.

```bash
databricks bundle validate
```

![Validation Success]({{ site.baseurl }}/images/learning/01-introduction-to-dab/02-validation-success.png)

**Step 2: Deploy the bundle**

Syncs your local files to the Databricks workspace and creates the job definition.

```bash
databricks bundle deploy
```

![Deployment Success]({{ site.baseurl }}/images/learning/01-introduction-to-dab/03-bundle-deploy.png)

**Step 3: Run the job**

Triggers the job execution directly from your terminal.

```bash
databricks bundle run hello_world_job
```

![Run Success]({{ site.baseurl }}/images/learning/01-introduction-to-dab/04-job-success.png)

## Expected Result

Navigate to Workflows in your Databricks workspace. You will see a job named `01_Hello_World_DAB`. Check the run logs to confirm the Python script executed successfully.

![Run Success in UI]({{ site.baseurl }}/images/learning/01-introduction-to-dab/05-job-success-ui.png)
