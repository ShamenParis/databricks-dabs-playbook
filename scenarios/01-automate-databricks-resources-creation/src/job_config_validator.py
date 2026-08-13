#!/usr/bin/env python3
"""
Databricks Asset Bundle Config Validator
=========================================

Validates team resource configuration JSON files against per-resource-type JSON schemas.

Supports:
  job, pipeline, dashboard, genie_space, app,
  cluster, sql_warehouse, experiment, registered_model, quality_monitor

Usage:
    # Validate all configs for a team/environment
    python job_config_validator.py --team DataEngineering --env Development

    # Validate all teams and environments
    python job_config_validator.py --all

    # Validate a specific resource type
    python job_config_validator.py --team DataEngineering --env Development --resource-type job

    # Validate a single JSON file
    python job_config_validator.py teams/DataEngineering/Development/configs/jobs/my_job.json

    # Quiet mode (CI/CD — only print errors)
    python job_config_validator.py --all --quiet

    # Exit on first error
    python job_config_validator.py --all --exit-on-error

Exit codes:
    0  All configs valid
    1  One or more invalid configs / errors
"""

import json
import argparse
import os
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

try:
    from jsonschema import validate, ValidationError
    from jsonschema.validators import Draft7Validator
except ImportError:
    print("ERROR: jsonschema not installed. Run: pip install jsonschema")
    sys.exit(1)


# ── Constants ──────────────────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).parent
SCHEMA_DIR = SCRIPT_DIR / "schema"
TEAMS_DIR = Path("./teams")

RESOURCE_TYPE_SUBDIR = {
    "job":              "jobs",
    "pipeline":         "pipelines",
    "dashboard":        "dashboards",
    "genie_space":      "genie_spaces",
    "app":              "apps",
    "cluster":          "clusters",
    "sql_warehouse":    "sql_warehouses",
    "experiment":       "experiments",
    "registered_model": "registered_models",
    "quality_monitor":  "quality_monitors",
}

RESOURCE_TYPE_SCHEMA = {
    "job":              "job_schema.json",
    "pipeline":         "pipeline_schema.json",
    "dashboard":        "dashboard_schema.json",
    "genie_space":      "genie_space_schema.json",
    "app":              "app_schema.json",
    "cluster":          "cluster_schema.json",
    "sql_warehouse":    "sql_warehouse_schema.json",
    "experiment":       "experiment_schema.json",
    "registered_model": "registered_model_schema.json",
    "quality_monitor":  "quality_monitor_schema.json",
}


# ── Schema loader ──────────────────────────────────────────────────────────────
class SchemaCache:
    """Lazy-loads and caches JSON schemas."""
    _cache: Dict[str, Dict] = {}

    @classmethod
    def get(cls, resource_type: str) -> Optional[Dict]:
        if resource_type in cls._cache:
            return cls._cache[resource_type]
        schema_file = SCHEMA_DIR / RESOURCE_TYPE_SCHEMA.get(resource_type, "")
        if not schema_file.exists():
            print(f"  Warning: schema not found for resource_type '{resource_type}' at {schema_file}")
            return None
        with open(schema_file, "r", encoding="utf-8") as f:
            schema = json.load(f)
        cls._cache[resource_type] = schema
        return schema


# ── Validator class ────────────────────────────────────────────────────────────
class ResourceConfigValidator:
    """Validates resource config JSON files for Databricks Asset Bundles."""

    def __init__(self, quiet: bool = False):
        self.quiet = quiet
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def _log(self, msg: str):
        if not self.quiet:
            print(msg)

    def _err(self, msg: str):
        print(msg)
        self.errors.append(msg)

    def _warn(self, msg: str):
        if not self.quiet:
            print(f"  ⚠  {msg}")
        self.warnings.append(msg)

    # ── Schema validation ────────────────────────────────────────────────────
    def validate_file(self, file_path: Path) -> bool:
        """Validate a single JSON config file. Returns True if valid."""
        self._log(f"\n  Validating: {file_path}")
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                cfg = json.load(f)
        except json.JSONDecodeError as exc:
            self._err(f"  ✗ Invalid JSON in {file_path}: {exc}")
            return False
        except FileNotFoundError:
            self._err(f"  ✗ File not found: {file_path}")
            return False

        resource_type = cfg.get("resource_type")
        if not resource_type:
            self._err(f"  ✗ Missing 'resource_type' field in {file_path}")
            return False

        if resource_type not in RESOURCE_TYPE_SCHEMA:
            self._err(f"  ✗ Unknown resource_type '{resource_type}' in {file_path}")
            self._log(f"     Valid types: {', '.join(RESOURCE_TYPE_SCHEMA.keys())}")
            return False

        schema = SchemaCache.get(resource_type)
        if schema is None:
            self._warn(f"No schema available for '{resource_type}' — skipping schema validation")
            return True

        validator = Draft7Validator(schema)
        schema_errors = list(validator.iter_errors(cfg))

        if schema_errors:
            self._err(f"  ✗ Schema validation failed ({len(schema_errors)} error(s)):")
            for err in schema_errors:
                path = " → ".join(str(p) for p in err.path) or "(root)"
                self._err(f"     • [{path}] {err.message}")
            return False

        # Resource-type-specific business logic checks
        ok = self._business_logic_checks(cfg, file_path, resource_type)
        if ok:
            self._log(f"  ✓ Valid [{resource_type}]: {file_path.name}")
        return ok

    # ── Business logic checks ────────────────────────────────────────────────
    def _business_logic_checks(self, cfg: Dict, file_path: Path, resource_type: str) -> bool:
        """Run resource-type-specific business logic validation."""
        if resource_type == "job":
            return self._check_job(cfg, file_path)
        if resource_type == "pipeline":
            return self._check_pipeline(cfg, file_path)
        if resource_type == "quality_monitor":
            return self._check_quality_monitor(cfg, file_path)
        return True

    def _check_job(self, cfg: Dict, file_path: Path) -> bool:
        ok = True
        use_serverless = cfg.get("use_serverless", True)

        # Classic cluster needs a job_cluster_key
        if not use_serverless and not cfg.get("job_cluster_key"):
            self._err(f"  ✗ Job with use_serverless=false must specify 'job_cluster_key'")
            ok = False

        # Tasks must have the right fields for their type
        tasks = cfg.get("tasks", [])
        task_keys = set()
        for task in tasks:
            key = task.get("task_key", "")
            if key in task_keys:
                self._err(f"  ✗ Duplicate task_key '{key}'")
                ok = False
            task_keys.add(key)

            task_type = task.get("task_type", "notebook_task")
            if task_type == "notebook_task" and not task.get("notebook_path"):
                self._err(f"  ✗ Task '{key}' of type notebook_task must have 'notebook_path'")
                ok = False
            if task_type == "python_task" and not task.get("python_file"):
                self._err(f"  ✗ Task '{key}' of type python_task must have 'python_file'")
                ok = False

            # Circular dependency detection
            for dep in task.get("dependance_task_keys", []):
                if dep == key:
                    self._err(f"  ✗ Task '{key}' depends on itself")
                    ok = False

        # schedule and trigger are mutually exclusive
        if cfg.get("schedule") and cfg.get("trigger"):
            self._err("  ✗ 'schedule' and 'trigger' are mutually exclusive")
            ok = False

        return ok

    def _check_pipeline(self, cfg: Dict, file_path: Path) -> bool:
        ok = True
        for lib in cfg.get("libraries", []):
            if not lib.get("notebook_path") and not lib.get("python_file"):
                self._err("  ✗ Each pipeline library must have 'notebook_path' or 'python_file'")
                ok = False
        return ok

    def _check_quality_monitor(self, cfg: Dict, file_path: Path) -> bool:
        ok = True
        monitor_type = cfg.get("monitor_type", "snapshot")
        if monitor_type in ("timeseries", "inference"):
            if not cfg.get("timestamp_col"):
                self._err(f"  ✗ monitor_type '{monitor_type}' requires 'timestamp_col'")
                ok = False
            if not cfg.get("granularities"):
                self._err(f"  ✗ monitor_type '{monitor_type}' requires 'granularities'")
                ok = False
        if monitor_type == "inference" and not cfg.get("prediction_col"):
            self._err("  ✗ monitor_type 'inference' requires 'prediction_col'")
            ok = False
        return ok

    # ── Batch validation ────────────────────────────────────────────────────
    def validate_team_env(
        self, team_name: str, env_name: str, resource_type_filter: Optional[str] = None
    ) -> Tuple[int, int]:
        """
        Validate all configs for a team/environment.
        Returns (valid_count, invalid_count).
        """
        types = [resource_type_filter] if resource_type_filter else list(RESOURCE_TYPE_SUBDIR.keys())
        valid, invalid = 0, 0

        for rtype in types:
            subdir = RESOURCE_TYPE_SUBDIR[rtype]
            config_path = TEAMS_DIR / team_name / env_name / "configs" / subdir
            if not config_path.exists():
                continue
            for json_file in sorted(config_path.glob("*.json")):
                if self.validate_file(json_file):
                    valid += 1
                else:
                    invalid += 1

        return valid, invalid


# ── CLI ────────────────────────────────────────────────────────────────────────
def get_all_team_envs():
    pairs = []
    for team_path in sorted(TEAMS_DIR.iterdir()):
        if not team_path.is_dir():
            continue
        for env_path in sorted(team_path.iterdir()):
            if env_path.is_dir() and (env_path / "configs").exists():
                pairs.append((team_path.name, env_path.name))
    return pairs


def main():
    parser = argparse.ArgumentParser(description="Databricks Asset Bundle Config Validator")
    parser.add_argument("files", nargs="*", help="Specific JSON files to validate")
    parser.add_argument("--all", action="store_true", help="Validate all teams and environments")
    parser.add_argument("--team", help="Team name")
    parser.add_argument("--env", help="Environment name (alias: --env_name)")
    parser.add_argument("--env_name", help="Environment name")
    parser.add_argument(
        "--resource-type", "--job-type",
        choices=list(RESOURCE_TYPE_SUBDIR.keys()),
        dest="resource_type",
        help="Only validate a specific resource type",
    )
    parser.add_argument("--quiet", "-q", action="store_true", help="Only print errors")
    parser.add_argument("--exit-on-error", action="store_true", help="Exit immediately on first error")
    args = parser.parse_args()

    env_name = args.env_name or args.env
    validator = ResourceConfigValidator(quiet=args.quiet)
    total_valid, total_invalid = 0, 0

    if args.files:
        for f in args.files:
            ok = validator.validate_file(Path(f))
            if ok:
                total_valid += 1
            else:
                total_invalid += 1
                if args.exit_on_error:
                    sys.exit(1)
    elif args.all:
        for team, env in get_all_team_envs():
            if not args.quiet:
                print(f"\n{'─'*60}")
                print(f"  Team: {team} / Env: {env}")
                print(f"{'─'*60}")
            v, i = validator.validate_team_env(team, env, args.resource_type)
            total_valid += v
            total_invalid += i
            if i > 0 and args.exit_on_error:
                sys.exit(1)
    elif args.team and env_name:
        if not args.quiet:
            print(f"\nValidating: {args.team} / {env_name}")
        v, i = validator.validate_team_env(args.team, env_name, args.resource_type)
        total_valid += v
        total_invalid += i
    elif args.team:
        for env_path in sorted((TEAMS_DIR / args.team).iterdir()):
            if not env_path.is_dir():
                continue
            if not args.quiet:
                print(f"\nEnvironment: {env_path.name}")
            v, i = validator.validate_team_env(args.team, env_path.name, args.resource_type)
            total_valid += v
            total_invalid += i
            if i > 0 and args.exit_on_error:
                sys.exit(1)
    else:
        parser.error("Specify files, --all, --team, or --team + --env")

    # Summary
    print(f"\n{'='*60}")
    print(f"  Valid:   {total_valid}")
    print(f"  Invalid: {total_invalid}")
    print(f"{'='*60}")

    sys.exit(0 if total_invalid == 0 else 1)


if __name__ == "__main__":
    main()
