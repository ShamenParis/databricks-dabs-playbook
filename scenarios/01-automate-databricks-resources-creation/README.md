# Databricks Asset Bundle Global Resource Automation

A team-onboarded, template-driven generator for Databricks Asset Bundles (DAB). Teams define their resources using simple JSON configuration files — the generator produces a complete, deploy-ready DAB bundle (`databricks.yml`, `variables.yml`, `resources/*.yml`).

Compatible with Databricks Free Edition using serverless compute.

---

## Supported Resource Types

| Resource | Config Folder | Description |
|---|---|---|
| `job` | `configs/jobs/` | Workflows — Notebook, Python, SQL, nested Jobs and Pipelines |
| `pipeline` | `configs/pipelines/` | Delta Live Tables (DLT) pipelines |
| `dashboard` | `configs/dashboards/` | Lakeview AI/BI dashboards |
| `genie_space` | `configs/genie_spaces/` | Genie AI/BI spaces |
| `cluster` | `configs/clusters/` | All-purpose interactive clusters |
| `sql_warehouse` | `configs/sql_warehouses/` | SQL warehouses |
| `quality_monitor` | `configs/quality_monitors/` | Lakehouse Quality Monitors |

---

## Repository Structure

```
scenarios/01-automate-databricks-resources-creation/
    src/
        generate_resources.py       Main generator script
        job_config_validator.py     Multi-resource config validator
        requirements.txt
        templates/                  Jinja2 templates (one per resource type)
            databricks_template.yml
            variables_template.yml
            job_template.jinja2
            pipeline_template.jinja2
            dashboard_template.jinja2
            genie_space_template.jinja2
            cluster_template.jinja2
            sql_warehouse_template.jinja2
            quality_monitor_template.jinja2
        schema/                     JSON validation schemas
            job_schema.json
            pipeline_schema.json
            ...

    teams/
        <TeamName>/
            <Environment>/
                configs/
                    jobs/               Job JSON configs
                    pipelines/          DLT pipeline configs
                    dashboards/
                    genie_spaces/
                    clusters/
                    sql_warehouses/
                    quality_monitors/
                    variables/
                        environment.yml     Team and environment variables
                src/
                    notebooks/          Notebooks referenced by jobs and pipelines
                bundle/                 Generated output — do not edit manually
                    databricks.yml
                    variables.yml
                    resources/
                        jobs/
                        pipelines/
                        ...

    docs/                               Documentation
```

---

## Quick Start

### 1. Install Dependencies

```bash
pip install -r src/requirements.txt
databricks auth login  # or configure ~/.databrickscfg
```

### 2. Create Your Team

```bash
cp -r teams/DataEngineering teams/MyTeam
```

Edit `teams/MyTeam/Development/configs/variables/environment.yml` with your workspace URL and catalog name.

### 3. Add Resource Configurations

Place JSON config files in the appropriate `configs/<type>/` folder. See the [Scenarios and Configs Guide](./docs/SCENARIOS_AND_CONFIGS.md) for all patterns and field references.

### 4. Validate Configurations

```bash
python src/job_config_validator.py --team MyTeam --env Development
```

### 5. Generate the Bundle

```bash
python src/generate_resources.py --team MyTeam --env_name Development
```

### 6. Deploy to Databricks

```bash
cd teams/MyTeam/Development/bundle

databricks bundle validate
databricks bundle deploy -t development
```

---

## Generator CLI Reference

```bash
# Generate for a specific team and environment
python src/generate_resources.py --team <Team> --env_name <Env>

# Generate for all teams and environments
python src/generate_resources.py --all

# Generate only a specific resource type
python src/generate_resources.py --team <Team> --env_name <Env> --resource-type job

# Generate only resource YAMLs (skip databricks.yml and variables.yml)
python src/generate_resources.py --team <Team> --env_name <Env> --resources-only

# Generate only the bundle config files
python src/generate_resources.py --team <Team> --env_name <Env> --bundle-only
```

## Validator CLI Reference

```bash
# Validate all configs for a team and environment
python src/job_config_validator.py --team <Team> --env <Env>

# Validate all teams
python src/job_config_validator.py --all

# Validate only a specific resource type
python src/job_config_validator.py --team <Team> --env <Env> --resource-type job

# Validate a single file
python src/job_config_validator.py teams/MyTeam/Dev/configs/jobs/my_job.json

# CI/CD mode — quiet output, exit on first error
python src/job_config_validator.py --all --quiet --exit-on-error
```

---

## Limitations and Testing Status

### Tested and Working

| Resource | Status | Notes |
|---|---|---|
| Jobs | Deployed | Notebook, Python, SQL, nested jobs, and pipeline tasks |
| Pipelines | Deployed | Delta Live Tables — serverless and classic |
| Quality Monitors | Deployed | Timeseries, Snapshot, and Inference types |
| Dashboards | Deployed | Requires `CAN_READ` or `CAN_MANAGE` permissions |

### Disabled / Not Yet Validated

| Resource | Status | Notes |
|---|---|---|
| Apps | Disabled | Requires a Git repository to be linked in the workspace |
| Experiments | Disabled | Removed pending validation |
| Registered Models | Disabled | Removed pending validation |

### Known Limitations

- **Genie Spaces:** Databricks Asset Bundles currently require a `serialized_space` export from the Databricks UI. Genie Spaces cannot be built entirely from declarative config fields (`tables`, `instructions`). This feature is disabled until the DAB API supports full declarative configuration.

---

## Further Reading

- [Team Onboarding Guide](./docs/TEAM_ONBOARDING_GUIDE.md)
- [Scenarios and Configs Guide](./docs/SCENARIOS_AND_CONFIGS.md)
- [Databricks Asset Bundles Documentation](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/bundles/)
