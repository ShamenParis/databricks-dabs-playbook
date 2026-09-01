---
layout: default
title: "04. File Trigger"
parent: Learning Modules
nav_order: 4
permalink: /learning/04-file-trigger
---

# 04: File Trigger

<a href="https://github.com/ShamenParis/databricks-dabs-playbook/tree/main/learning/04-file-trigger" class="btn-source" target="_blank">📂 View Source Code</a>

---

In this module, you will learn how to configure a Databricks Job to automatically run the moment a new file lands in a Unity Catalog Volume or cloud storage path. This enables event-driven data pipelines rather than relying on fixed schedules.

## What Are We Building?

![DAB Architecture Setup]({{ site.baseurl }}/images/learning/04-file-trigger/01-architecture-diagram.png)

## Prerequisites and Local Setup

> Complete the [Prerequisites and Local Setup]({{ site.baseurl }}/prerequisites) before continuing.

### Setting Up Unity Catalog and a Volume

If you do not yet have a Unity Catalog and Volume, create them as follows.

**Option 1: Using the Databricks UI**

![Create Catalog]({{ site.baseurl }}/images/learning/04-file-trigger/01-create_catalog.png)

**Option 2: Using the CLI**

```bash
databricks catalogs create main
databricks volumes create main demo landing_zone MANAGED
```

## Bundle Structure

1. `databricks.yml` — The master control file.
2. `resources/jobs/file_trigger_job.yml` — Contains the `trigger: file_arrival` block, which monitors a specific path for new files.
3. `src/file_trigger_notebook.py` — The notebook that executes when the trigger fires.

## How to Deploy and Run

Once authenticated, navigate to this folder (`04-file-trigger`) in your terminal.

**Step 1: Validate and deploy**

```bash
databricks bundle validate
databricks bundle deploy
```

![Validation Deploy Success]({{ site.baseurl }}/images/learning/04-file-trigger/02-validation-deploy-sucess.png)

**Step 2: Verify the trigger in the UI**

Once deployed, the job will enter a "Waiting for file" state. You can verify this in the Databricks Workflows UI.

![UI View]({{ site.baseurl }}/images/learning/04-file-trigger/03-workspace-ui.png)

**Step 3: Trigger the job**

Upload a sample file (such as a `.csv` or `.txt`) into your `/Volumes/main/default/landing_zone` volume using the Databricks Catalog UI. The job will automatically start within 60 seconds.

A test file is available at [docs/downloads/04-file-trigger/trigger.csv](https://github.com/ShamenParis/databricks-dabs-playbook/raw/main/docs/downloads/04-file-trigger/trigger.csv).

<video controls width="100%" style="border-radius:8px; margin:1em 0;"><source src="{{ site.baseurl }}/images/learning/04-file-trigger/04-trigger-file-test.mp4" type="video/mp4">Your browser does not support the video tag.</video>
