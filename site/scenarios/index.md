---
layout: default
title: Enterprise Scenarios
nav_order: 4
has_children: true
has_toc: false
permalink: /scenarios/
---

# Enterprise Scenarios

Real-world deployment scenarios built with Databricks Asset Bundles (DABs). Each scenario is self-contained and production-grade.

---

| # | Scenario | Description | Tech Stack |
| :--- | :--- | :--- | :--- |
| 01 | [01. Automate Databricks Resource Creation]({{ site.baseurl }}/scenarios/01-automate-databricks-resources-creation) | Template-driven automation for deploying Databricks resources (Jobs, Pipelines, Monitors, Dashboards) | DABs, YAML, Jinja2, Python |
| 02 | [02. Enterprise Databricks Orchestration]({{ site.baseurl }}/scenarios/02-enterprise-databricks-orchestration) | Modular enterprise repository structure with domain-driven workflows, dynamic glob loading, and cross-job/pipeline orchestrations | DABs, YAML, DLT, Python |

---

More scenarios coming soon covering:

- **Governance and Security:** Unity Catalog, Data Sharing, and securing production workloads.
- **Orchestration:** Databricks Jobs and advanced Workflows.
- **Data Engineering and ML:** Delta Live Tables (DLT) and MLOps on Databricks.
- **Automation:** CI/CD pipelines tailored for Databricks environments.
