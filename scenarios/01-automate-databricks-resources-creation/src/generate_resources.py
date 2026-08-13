#!/usr/bin/env python3
"""
Databricks Asset Bundle Global Resource Generator
==================================================

Reads team/environment config files and generates a complete Databricks Asset Bundle
(databricks.yml, variables.yml, resources/*.yml) in each team's pipelines/ output folder.

Supports the following resource types:
  job, pipeline, dashboard, genie_space, app,
  cluster, sql_warehouse, experiment, registered_model, quality_monitor

Usage:
    python generate_resources.py --team <team> --env_name <env>
    python generate_resources.py --all
    python generate_resources.py --team DataEngineering --env_name Development --resource-type job

Directory conventions:
    teams/<Team>/<Env>/configs/jobs/              -> job configs (*.json)
    teams/<Team>/<Env>/configs/pipelines/         -> DLT pipeline configs
    teams/<Team>/<Env>/configs/dashboards/        -> Lakeview dashboard configs
    teams/<Team>/<Env>/configs/genie_spaces/      -> Genie space configs
    teams/<Team>/<Env>/configs/apps/              -> Databricks app configs
    teams/<Team>/<Env>/configs/clusters/          -> Cluster configs
    teams/<Team>/<Env>/configs/sql_warehouses/    -> SQL warehouse configs
    teams/<Team>/<Env>/configs/experiments/       -> MLflow experiment configs
    teams/<Team>/<Env>/configs/registered_models/ -> UC registered model configs
    teams/<Team>/<Env>/configs/quality_monitors/  -> Quality monitor configs
    teams/<Team>/<Env>/configs/variables/         -> environment.yml

Output is written to:
    teams/<Team>/<Env>/bundle/
        databricks.yml
        variables.yml
        resources/jobs/<bundle_name>.yml
        resources/pipelines/<bundle_name>.yml
        ...

Deploy locally with:
    cd teams/<Team>/<Env>/bundle
    databricks bundle validate
    databricks bundle deploy -t development
"""

import sys
import json
import os
import glob
import argparse
from pathlib import Path

# ── Bootstrap dependencies ─────────────────────────────────────────────────────
import subprocess
subprocess.check_call(
    [sys.executable, "-m", "pip", "install", "pyyaml", "jinja2"],
    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
)

import yaml
from jinja2 import Environment, FileSystemLoader, StrictUndefined

# ── Constants ──────────────────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).parent
TEMPLATE_DIR = SCRIPT_DIR / "templates"
TEAMS_DIR = Path("./teams")

# The subdirectory within teams/<Team>/<Env>/ where generated bundle files are written.
# Using the env root directly (empty string or ".") puts databricks.yml next to src/, configs/
# so notebook paths like ./src/notebooks/... resolve correctly from the bundle root.
BUNDLE_OUTPUT_SUBDIR = "bundle"  # teams/<Team>/<Env>/bundle/

# Maps resource_type -> (config subfolder, template file, output subfolder, bundle_name_key)
RESOURCE_TYPE_MAP = {
    "job":              ("jobs",              "job_template.jinja2",              "jobs"),
    "pipeline":         ("pipelines",         "pipeline_template.jinja2",         "pipelines"),
    "dashboard":        ("dashboards",        "dashboard_template.jinja2",        "dashboards"),
    "genie_space":      ("genie_spaces",      "genie_space_template.jinja2",      "genie_spaces"),
    "cluster":          ("clusters",          "cluster_template.jinja2",          "clusters"),
    "sql_warehouse":    ("sql_warehouses",    "sql_warehouse_template.jinja2",    "sql_warehouses"),
    "quality_monitor":  ("quality_monitors",  "quality_monitor_template.jinja2",  "quality_monitors"),
}

# The field in each config JSON that gives the bundle key (used as filename)
BUNDLE_NAME_KEYS = {
    "job":              "job_bundle_name",
    "pipeline":         "pipeline_bundle_name",
    "dashboard":        "dashboard_bundle_name",
    "genie_space":      "genie_bundle_name",
    "app":              "app_bundle_name",
    "cluster":          "cluster_bundle_name",
    "sql_warehouse":    "warehouse_bundle_name",
    "experiment":       "experiment_bundle_name",
    "registered_model": "model_bundle_name",
    "quality_monitor":  "monitor_bundle_name",
}


# ── Helper: discover teams / envs ──────────────────────────────────────────────
def get_all_teams_and_environments():
    """Return list of (team_name, env_name) for every team/env with a configs/ dir."""
    combinations = []
    for team_path in sorted(TEAMS_DIR.iterdir()):
        if not team_path.is_dir() or team_path.name.startswith("."):
            continue
        for env_path in sorted(team_path.iterdir()):
            if env_path.is_dir() and (env_path / "configs").exists():
                combinations.append((team_path.name, env_path.name))
    return combinations


def get_team_environments(team_name):
    team_path = TEAMS_DIR / team_name
    envs = []
    if not team_path.exists():
        return envs
    for env_path in sorted(team_path.iterdir()):
        if env_path.is_dir() and (env_path / "configs").exists():
            envs.append(env_path.name)
    return envs


# ── Helper: load variables ─────────────────────────────────────────────────────
def load_variables(team_name, env_name):
    """
    Load all *.yml files from configs/variables/ and return a flat dict.
    Supports both:
      - Azure DevOps template format  (variables: [{name: x, value: y}])
      - Simple key-value format       (key: value)
    """
    variables_path = TEAMS_DIR / team_name / env_name / "configs" / "variables"
    variables = {}
    if not variables_path.exists():
        print(f"  Warning: no variables folder at {variables_path}")
        return variables

    for file_path in sorted(variables_path.glob("*.yml")):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
            if not data:
                continue
            if isinstance(data.get("variables"), list):
                for item in data["variables"]:
                    if "name" in item and "value" in item:
                        variables[item["name"]] = item["value"]
            else:
                variables.update(data)
        except Exception as exc:
            print(f"  Warning: could not load {file_path}: {exc}")

    return variables


# ── Helper: load resource configs ─────────────────────────────────────────────
def load_resource_configs(team_name, env_name, resource_type):
    """Return list of config dicts for a given resource_type."""
    config_subdir, _, _ = RESOURCE_TYPE_MAP[resource_type]
    config_path = TEAMS_DIR / team_name / env_name / "configs" / config_subdir
    configs = []

    if not config_path.exists():
        return configs

    for file_path in sorted(config_path.glob("*.json")):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                cfg = json.load(f)
            cfg["_file_path"] = str(file_path)
            # Only include configs matching this resource_type
            if cfg.get("resource_type") == resource_type:
                configs.append(cfg)
        except Exception as exc:
            print(f"  Error loading {file_path}: {exc}")

    return configs


# ── Jinja2 environment ─────────────────────────────────────────────────────────
def make_jinja_env():
    return Environment(
        loader=FileSystemLoader(str(TEMPLATE_DIR)),
        keep_trailing_newline=True,
    )


def render_resource(cfg, resource_type, variables, team_name, env_name):
    """
    Render a resource config to a YAML string using Jinja2 templates.
    """
    jinja_env = make_jinja_env()
    _, template_file, _ = RESOURCE_TYPE_MAP[resource_type]
    tmpl = jinja_env.get_template(template_file)
    
    # Pre-render tasks if it's a job
    if resource_type == "job" and "tasks" in cfg:
        task_tmpl = jinja_env.get_template("task_template.jinja2")
        rendered_tasks = []
        for t in cfg["tasks"]:
            t_context = {
                "use_serverless": cfg.get("use_serverless", True),
                "job_cluster_key": cfg.get("job_cluster_key", "default_cluster"),
                **t
            }
            # Task-specific flags for the template
            t_context["timeout_seconds_flag"] = "timeout_seconds" in t
            t_context["task_dependency_flag"] = "dependance_task_keys" in t and t["dependance_task_keys"]
            t_context["warning_flag"] = "warning_duration_seconds" in t
            t_context["task_email_notification_flag"] = "email_notification" in t
            rendered_tasks.append(task_tmpl.render(**t_context))
        cfg["tasks_yaml"] = "\n".join(rendered_tasks)

    context = {
        "team_name": team_name,
        "env_name": env_name,
        "variables": variables,
        **cfg
    }
    
    return tmpl.render(**context)



# ── Output writer ─────────────────────────────────────────────────────────────
def write_resource_yml(rendered_yaml, resource_type, bundle_name, output_base):
    """Write a rendered resource YAML to the appropriate resources/ subfolder."""
    _, _, output_subdir = RESOURCE_TYPE_MAP[resource_type]
    output_dir = output_base / "resources" / output_subdir
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"{bundle_name}.yml"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(rendered_yaml)
        if not rendered_yaml.endswith("\n"):
            f.write("\n")
    return output_file


# ── Main resource generator ────────────────────────────────────────────────────
def generate_resources(team_name, env_name, resource_type_filter=None):
    """
    Generate all DAB resource files for a given team/environment.
    """
    output_base = TEAMS_DIR / team_name / env_name / BUNDLE_OUTPUT_SUBDIR
    output_base.mkdir(parents=True, exist_ok=True)

    variables = load_variables(team_name, env_name)
    types_to_process = (
        [resource_type_filter] if resource_type_filter else list(RESOURCE_TYPE_MAP.keys())
    )

    total_generated = 0

    for rtype in types_to_process:
        configs = load_resource_configs(team_name, env_name, rtype)
        if not configs:
            continue

        bundle_name_key = BUNDLE_NAME_KEYS[rtype]

        for cfg in configs:
            bundle_name = cfg.get(bundle_name_key)
            if not bundle_name:
                print(f"  Warning: missing '{bundle_name_key}' in {cfg.get('_file_path', '?')} — skipping")
                continue

            # Dashboards and Genie spaces require a SQL Warehouse ID
            if rtype in ("dashboard", "genie_space"):
                warehouse_id = variables.get("sql_warehouse_id", "").strip()
                if not warehouse_id:
                    print(
                        f"  ⚠ [{rtype}] {bundle_name} skipped — "
                        f"set sql_warehouse_id in environment.yml to enable dashboards/genie spaces"
                    )
                    continue

            try:
                rendered = render_resource(cfg, rtype, variables, team_name, env_name)
                out_file = write_resource_yml(rendered, rtype, bundle_name, output_base)
                print(f"  ✓ [{rtype}] {bundle_name} → {out_file.relative_to(output_base)}")
                total_generated += 1
            except Exception as exc:
                print(f"  ✗ [{rtype}] {bundle_name}: {exc}")
                raise

    if total_generated == 0:
        print(f"  Warning: no resource configs found for {team_name}/{env_name}")

    # ── Sync team source files into the bundle output ──────────────────────────
    # Notebooks and apps must be inside the bundle root for DAB to include them.
    # We copy src/ (notebooks, apps, assets) into bundle/src/ on every generation run.
    import shutil
    team_env_root = TEAMS_DIR / team_name / env_name
    src_dir = team_env_root / "src"
    bundle_src_dir = output_base / "src"
    if src_dir.exists():
        if bundle_src_dir.exists():
            shutil.rmtree(bundle_src_dir)
        shutil.copytree(str(src_dir), str(bundle_src_dir))
        print(f"  ✓ src/ synced → {bundle_src_dir.relative_to(output_base)}")

    return total_generated


# ── Generate databricks.yml ────────────────────────────────────────────────────
def generate_databricks_yml(team_name, env_name):
    variables = load_variables(team_name, env_name)
    jinja_env = make_jinja_env()
    tmpl = jinja_env.get_template("databricks_template.yml")

    context = {
        "team_name": team_name,
        "env_name": env_name,
        "variables": variables,
        "cli_profile": variables.get("cli_profile", "").strip(),
        "workspace_host_literal": f"${{var.workspaceHost}}",
        "run_as_spn": bool(variables.get("service_principal_name")),
    }

    content = tmpl.render(**context)
    output_path = TEAMS_DIR / team_name / env_name / BUNDLE_OUTPUT_SUBDIR / "databricks.yml"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")
    print(f"  ✓ databricks.yml → {output_path}")





# ── Generate variables.yml ─────────────────────────────────────────────────────
def generate_variables_yml(team_name, env_name):
    variables = load_variables(team_name, env_name)
    jinja_env = make_jinja_env()
    tmpl = jinja_env.get_template("variables_template.yml")

    context = {
        "team_name": team_name,
        "env_name": env_name,
        "variables": variables,
    }

    content = tmpl.render(**context)
    output_path = TEAMS_DIR / team_name / env_name / BUNDLE_OUTPUT_SUBDIR / "variables.yml"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")
    print(f"  ✓ variables.yml → {output_path}")


# ── CLI ────────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="Databricks Asset Bundle Global Resource Generator"
    )
    parser.add_argument("--all", action="store_true", help="Process all teams and environments")
    parser.add_argument("--team", help="Team name (e.g. DataEngineering)")
    parser.add_argument("--env_name", help="Environment name (e.g. Development). Requires --team")
    parser.add_argument(
        "--resource-type",
        choices=list(RESOURCE_TYPE_MAP.keys()),
        help="Only generate a specific resource type",
    )
    parser.add_argument("--resources-only", action="store_true", help="Skip databricks.yml and variables.yml")
    parser.add_argument("--bundle-only", action="store_true", help="Only generate databricks.yml and variables.yml")

    args = parser.parse_args()

    if not args.all and not args.team:
        parser.error("Specify --all or --team")
    if args.env_name and not args.team:
        parser.error("--env_name requires --team")

    # Build list of (team, env) pairs
    if args.all:
        pairs = get_all_teams_and_environments()
        if not pairs:
            print("No team/environment combinations found under teams/")
            sys.exit(1)
    elif args.team and args.env_name:
        pairs = [(args.team, args.env_name)]
    elif args.team:
        envs = get_team_environments(args.team)
        if not envs:
            print(f"No environments found for team '{args.team}'")
            sys.exit(1)
        pairs = [(args.team, env) for env in envs]
    else:
        parser.error("Specify --all, --team, or --team + --env_name")

    # Process
    for team_name, env_name in pairs:
        print(f"\n{'='*70}")
        print(f"  Team: {team_name}   Environment: {env_name}")
        print(f"{'='*70}")
        try:
            if not args.bundle_only:
                count = generate_resources(team_name, env_name, args.resource_type)
            if not args.resources_only:
                generate_databricks_yml(team_name, env_name)
                generate_variables_yml(team_name, env_name)
            print(f"  ✓ Done: {team_name}/{env_name}")
        except Exception as exc:
            print(f"  ✗ Failed: {team_name}/{env_name}: {exc}")
            if not args.all:
                sys.exit(1)

    print(f"\n{'='*70}")
    print("  Generation complete!")
    print(f"{'='*70}")
    print("\nNext steps:")
    print("  cd teams/<Team>/<Env>/bundle")
    print("  databricks bundle validate")
    print("  databricks bundle deploy -t development")


if __name__ == "__main__":
    main()
