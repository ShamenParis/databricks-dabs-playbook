---
layout: default
title: Home
nav_order: 1
permalink: /
---

<div class="hero-section">
  <h1 class="hero-title">Databricks DABs Playbook</h1>
  <p class="hero-subtitle">Production-ready Declarative Automation Bundle templates — scenario-based learning, visual architectures, and copy-paste-ready code.</p>
</div>

<div class="stats-bar">
  <div class="stat">
    <div class="stat-number">13</div>
    <div class="stat-label">Learning Modules</div>
  </div>
  <div class="stat">
    <div class="stat-number">2</div>
    <div class="stat-label">Enterprise Scenarios</div>
  </div>
  <div class="stat">
    <div class="stat-number">8+</div>
    <div class="stat-label">Resource Types</div>
  </div>
</div>

## What's Inside

- **Visual Architectures:** Diagram-first approach for every scenario.
- **Production Code:** Copy-paste-ready `databricks.yml` and project files.
- **Cost Optimisation:** Built-in best practices for compute configurations.

---

<div class="section-header">
  <h2>Learning Modules</h2>
</div>

Start from zero and build your way up to advanced DAB orchestration patterns.

<div class="module-grid">

<a href="{{ site.baseurl }}/learning/01-introduction-to-dab" class="module-card">
  <div class="card-number">Module 01</div>
  <div class="card-title">01. Introduction to DABs</div>
  <div class="card-desc">Set up your local environment and deploy your first Hello World Databricks Asset Bundle</div>
  <div class="card-tags"><span class="tag">DABs</span><span class="tag">YAML</span><span class="tag">Python</span></div>
</a>
<a href="{{ site.baseurl }}/learning/02-job-parameters" class="module-card">
  <div class="card-number">Module 02</div>
  <div class="card-title">02. Job with Parameters</div>
  <div class="card-desc">Define job parameters and pass dynamic values into a PySpark script at runtime</div>
  <div class="card-tags"><span class="tag">DABs</span><span class="tag">YAML</span><span class="tag">PySpark</span></div>
</a>
<a href="{{ site.baseurl }}/learning/03-schedule-a-job" class="module-card">
  <div class="card-number">Module 03</div>
  <div class="card-title">03. Schedule a Job</div>
  <div class="card-desc">Automate job execution with Quartz cron expressions and deploy notebooks as Python files</div>
  <div class="card-tags"><span class="tag">DABs</span><span class="tag">YAML</span><span class="tag">Python</span></div>
</a>
<a href="{{ site.baseurl }}/learning/04-file-trigger" class="module-card">
  <div class="card-number">Module 04</div>
  <div class="card-title">04. File Trigger</div>
  <div class="card-desc">Trigger a job automatically when a new file lands in a Unity Catalog Volume</div>
  <div class="card-tags"><span class="tag">DABs</span><span class="tag">YAML</span><span class="tag">Unity Catalog</span></div>
</a>
<a href="{{ site.baseurl }}/learning/05-table-update-trigger" class="module-card">
  <div class="card-number">Module 05</div>
  <div class="card-title">05. Table Update Trigger</div>
  <div class="card-desc">Trigger a job automatically when a Delta Table is updated</div>
  <div class="card-tags"><span class="tag">DABs</span><span class="tag">YAML</span><span class="tag">Delta Lake</span></div>
</a>
<a href="{{ site.baseurl }}/learning/06-run-multiple-tasks" class="module-card">
  <div class="card-number">Module 06</div>
  <div class="card-title">06. Run Multiple Tasks</div>
  <div class="card-desc">Build a Directed Acyclic Graph (DAG) with parallel tasks and sequential dependencies</div>
  <div class="card-tags"><span class="tag">DABs</span><span class="tag">YAML</span><span class="tag">Python</span></div>
</a>
<a href="{{ site.baseurl }}/learning/07-task-parameters" class="module-card">
  <div class="card-number">Module 07</div>
  <div class="card-title">07. Task Parameters</div>
  <div class="card-desc">Pass dynamic values from an upstream task to multiple downstream tasks using `taskValues`</div>
  <div class="card-tags"><span class="tag">DABs</span><span class="tag">YAML</span><span class="tag">Python</span></div>
</a>
<a href="{{ site.baseurl }}/learning/08-use-if-else-task" class="module-card">
  <div class="card-number">Module 08</div>
  <div class="card-title">08. Conditional Execution</div>
  <div class="card-desc">Implement success and failure routing using the `run_if` parameter</div>
  <div class="card-tags"><span class="tag">DABs</span><span class="tag">YAML</span><span class="tag">Python</span></div>
</a>
<a href="{{ site.baseurl }}/learning/09-sql-tasks-with-variable-lookup" class="module-card">
  <div class="card-number">Module 09</div>
  <div class="card-title">09. SQL Tasks with Variable Lookup</div>
  <div class="card-desc">Execute raw SQL files on a SQL Warehouse and resolve infrastructure IDs dynamically using `lookup`</div>
  <div class="card-tags"><span class="tag">DABs</span><span class="tag">YAML</span><span class="tag">SQL</span></div>
</a>
<a href="{{ site.baseurl }}/learning/10-run-sql-alerts" class="module-card">
  <div class="card-number">Module 10</div>
  <div class="card-title">10. SQL Alerts</div>
  <div class="card-desc">Provision SQL Alerts and trigger them from a Workflow using `alert_task`</div>
  <div class="card-tags"><span class="tag">DABs</span><span class="tag">YAML</span><span class="tag">SQL</span></div>
</a>
<a href="{{ site.baseurl }}/learning/11-run-dbt-on-databricks" class="module-card">
  <div class="card-number">Module 11</div>
  <div class="card-title">11. Run dbt on Databricks</div>
  <div class="card-desc">Orchestrate a dbt Core project natively in Databricks Workflows using the `dbt_task` type</div>
  <div class="card-tags"><span class="tag">DABs</span><span class="tag">YAML</span><span class="tag">dbt</span><span class="tag">SQL</span></div>
</a>
<a href="{{ site.baseurl }}/learning/12-create-pipeline" class="module-card">
  <div class="card-number">Module 12</div>
  <div class="card-title">12. Create a Pipeline</div>
  <div class="card-desc">Provision a Serverless Delta Live Tables pipeline with Bronze and Silver layers</div>
  <div class="card-tags"><span class="tag">DABs</span><span class="tag">YAML</span><span class="tag">DLT</span><span class="tag">Python</span></div>
</a>
<a href="{{ site.baseurl }}/learning/13-advanced-job-pipeline" class="module-card">
  <div class="card-number">Module 13</div>
  <div class="card-title">13. Advanced Orchestration</div>
  <div class="card-desc">Build a master orchestrator that triggers a notebook, a DLT pipeline, and a child job in a single workflow</div>
  <div class="card-tags"><span class="tag">DABs</span><span class="tag">YAML</span><span class="tag">DLT</span><span class="tag">Python</span></div>
</a>

</div>

---

<div class="section-header">
  <h2>Enterprise Scenarios</h2>
</div>

Production-grade, real-world deployment patterns.

<div class="module-grid">

<a href="{{ site.baseurl }}/scenarios/01-automate-databricks-resources-creation" class="module-card">
  <div class="card-number">Scenario 01</div>
  <div class="card-title">01. Automate Databricks Resource Creation</div>
  <div class="card-desc">Template-driven automation for deploying Databricks resources (Jobs, Pipelines, Monitors, Dashboards)</div>
  <div class="card-tags"><span class="tag">DABs</span><span class="tag">YAML</span><span class="tag">Jinja2</span><span class="tag">Python</span></div>
</a>
<a href="{{ site.baseurl }}/scenarios/02-enterprise-databricks-orchestration" class="module-card">
  <div class="card-number">Scenario 02</div>
  <div class="card-title">02. Enterprise Databricks Orchestration</div>
  <div class="card-desc">Modular enterprise repository structure with domain-driven workflows, dynamic glob loading, and cross-job/pipeline orchestrations</div>
  <div class="card-tags"><span class="tag">DABs</span><span class="tag">YAML</span><span class="tag">DLT</span><span class="tag">Python</span></div>
</a>

</div>

---

<div class="author-section">
  <img src="{{ site.baseurl }}/images/learning/00-initial-setup/mvp_logo.svg" alt="Shamen Paris" class="author-logo">
  <div class="author-info">
    <div class="author-name">Shamen Paris</div>
    <div class="author-title">Databricks MVP | Data & AI Consultant</div>
    <div class="author-links">
      <a href="https://medium.com/@shamen1209">Medium Articles</a>
      <a href="https://www.youtube.com/@shamnix_data_and_ai">YouTube Channel</a>
    </div>
  </div>
</div>
