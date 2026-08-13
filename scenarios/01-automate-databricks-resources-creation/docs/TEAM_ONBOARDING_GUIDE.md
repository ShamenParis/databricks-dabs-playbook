# Team Onboarding Guide — DAB Global Resource Automation

This guide walks you through onboarding a new team and deploying Databricks resources using the DAB Global Resource Generator.

---

## Prerequisites

- Python 3.11 or later
- Databricks CLI installed (`pip install databricks-cli` or `brew install databricks`)
- Databricks workspace access (Free Edition or paid)
- Python dependencies: `pip install -r src/requirements.txt` (run from the scenario root)

---

## Step-by-Step Onboarding

### Step 1 — Create Your Team Directory Structure

In the `teams/` folder, create your team and environment directories:

```bash
TEAM="MyTeam"
ENV="Development"

mkdir -p teams/$TEAM/$ENV/configs/jobs
mkdir -p teams/$TEAM/$ENV/configs/pipelines
mkdir -p teams/$TEAM/$ENV/configs/dashboards
mkdir -p teams/$TEAM/$ENV/configs/genie_spaces
mkdir -p teams/$TEAM/$ENV/configs/clusters
mkdir -p teams/$TEAM/$ENV/configs/sql_warehouses
mkdir -p teams/$TEAM/$ENV/configs/quality_monitors
mkdir -p teams/$TEAM/$ENV/configs/variables
mkdir -p teams/$TEAM/$ENV/src/notebooks
mkdir -p teams/$TEAM/$ENV/bundle
```

Alternatively, copy an existing team as a starting point:

```bash
cp -r teams/DataEngineering teams/MyTeam
```

---

### Step 2 — Configure `environment.yml`

Edit `teams/<Team>/<Env>/configs/variables/environment.yml` with your workspace and catalog details:

```yaml
variables:
  - name: team_short_name
    value: "my_team"

  - name: env_short_name
    value: "dev"

  # Free Edition: https://community.cloud.databricks.com
  # Paid workspace: https://adb-xxxx.azuredatabricks.net
  - name: workspace_host
    value: "https://community.cloud.databricks.com"

  # Service principal (leave blank for Free Edition)
  - name: service_principal_name
    value: ""

  - name: environment_version
    value: "5"

  - name: catalog_name
    value: "my_catalog_dev"

  - name: schema_name
    value: "default"

  # Required for dashboards and Genie Spaces
  # Find in Databricks UI > SQL Warehouses > Connection Details
  - name: sql_warehouse_id
    value: ""

  - name: cost_centre
    value: "COST123"
```

---

### Step 3 — Add Resource Configurations

Place JSON config files in the appropriate `configs/<type>/` folder.

**Minimum job configuration (Free Edition):**

```json
{
  "resource_type": "job",
  "job_bundle_name": "my_team_daily_job",
  "job_name": "My Team — Daily Processing",
  "use_serverless": true,
  "tasks": [
    {
      "task_key": "run_notebook",
      "task_type": "notebook_task",
      "notebook_path": "./src/notebooks/my_notebook.py",
      "source": "WORKSPACE"
    }
  ]
}
```

See the [Scenarios and Configs Guide](./SCENARIOS_AND_CONFIGS.md) for all supported resource types and configuration patterns.

---

### Step 4 — Validate Configurations

Run the validator from the scenario root before generating the bundle:

```bash
python src/job_config_validator.py --team MyTeam --env Development
python src/job_config_validator.py --team MyTeam --env Development --resource-type pipeline
```

Fix any reported errors before proceeding.

---

### Step 5 — Generate the Bundle

```bash
python src/generate_resources.py --team MyTeam --env_name Development
```

This produces the following output:

```
teams/MyTeam/Development/bundle/
    databricks.yml
    variables.yml
    resources/
        jobs/
            my_team_daily_job.yml
        ...
```

---

### Step 6 — Authenticate with the Databricks CLI

**Free Edition:**

```bash
databricks auth login --host https://community.cloud.databricks.com
```

**Azure Databricks:**

```bash
databricks auth login --host https://adb-xxxx.azuredatabricks.net
```

Or configure manually in `~/.databrickscfg`:

```ini
[DEFAULT]
host = https://community.cloud.databricks.com
token = dapiXXXXXXXXXXXX
```

---

### Step 7 — Deploy to Databricks

```bash
cd teams/MyTeam/Development/bundle

databricks bundle validate
databricks bundle deploy -t development

# Run a job immediately (optional)
databricks bundle run <job_bundle_name> -t development
```

---

### Step 8 — Verify in the Databricks UI

1. Navigate to your Databricks workspace.
2. **Workflows** — confirm your job appears with the correct name and settings.
3. **Delta Live Tables** — confirm your pipeline appears (if configured).
4. **Dashboards** — confirm Lakeview dashboards appear in the expected folder.
5. **SQL Warehouses** — confirm the warehouse exists (if configured).

---

## Directory Convention

```
teams/
    <TeamName>/
        <Environment>/
            configs/
                jobs/               One .json file per job
                pipelines/          One .json file per DLT pipeline
                dashboards/         One .json file per Lakeview dashboard
                genie_spaces/       One .json file per Genie Space
                clusters/           One .json file per cluster
                sql_warehouses/     One .json file per SQL warehouse
                quality_monitors/   One .json file per quality monitor
                variables/
                    environment.yml     Team and environment variables
            src/
                notebooks/          Notebooks referenced by jobs and pipelines
            bundle/                 Generated output — do not edit manually
```

---

## Adding a New Environment

To add a `Production` environment:

1. Copy your `Development` folder: `cp -r teams/MyTeam/Development teams/MyTeam/Production`
2. Update `configs/variables/environment.yml` with production values.
3. Update job configs: set `"pause_status": false` for schedules and use the production catalog.
4. Generate: `python src/generate_resources.py --team MyTeam --env_name Production`
5. Deploy: `databricks bundle deploy -t production`

---

## Best Practices

- **One config file per resource** — keeps configs focused and easy to review.
- **Use `pause_status: true`** for schedules in development to prevent accidental runs.
- **Use `${var.catalogName}`** in resource names to keep configs environment-agnostic.
- **Always validate before generating** — run the validator first to catch errors early.
- **Do not edit the `bundle/` folder manually** — it is generated output. Edit configs and regenerate.
- **Commit configs, not generated files** — consider adding `teams/*/bundle/` to `.gitignore`.

---

## Troubleshooting

| Issue | Solution |
|---|---|
| `bundle validate` fails with unknown field | Check the template is up to date; the field may not be supported in your CLI version |
| `run_as` errors on Free Edition | Set `"job_run_as": ""` in the job config or leave it blank |
| Dashboard deploys but shows empty content | The `.lvdash.json` asset file must be included in the bundle |
| Genie Space deployment fails | Ensure `sql_warehouse_id` is set in `environment.yml` |
