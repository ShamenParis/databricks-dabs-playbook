# 08: Conditional Execution with run_if

In production data engineering, pipelines will inevitably encounter failures. Rather than letting an entire workflow fail, you can define conditional branching to route execution based on the outcome of a previous task.

In this module, you will learn how to use the `run_if` parameter to implement success and failure paths within a single Databricks Workflow:

- **Task A** — The root evaluation task.
- **Task B** — Executes only if Task A succeeds (`run_if: ALL_SUCCESS`).
- **Task C** — Executes only if Task A fails (`run_if: ALL_FAILED`).

## What Are We Building?

![DAB Architecture Setup](../../docs/learning/08-use-if-else-task/01-architecture-diagram.png)

## Prerequisites and Local Setup

[Prerequisites and Local Setup](../../docs/learning/00-initial-setup/README.md)

## Bundle Structure

1. `databricks.yml` — Master control file.
2. `resources/jobs/if_else_job.yml` — Defines the workflow with `run_if` conditions.
3. `src/task_a.py` — Reads a parameter and either succeeds or raises an exception to simulate a failure.
4. `src/task_b.py` — The success path notebook.
5. `src/task_c.py` — The failure path and recovery notebook.

## How to Deploy and Run

Once authenticated, navigate to this folder (`08-use-if-else-task`) in your terminal.

**Step 1: Validate and deploy**

```bash
databricks bundle validate
databricks bundle deploy
```

**Step 2: Run the success path**

Run the job with default parameters. Task A will succeed and route to Task B.

```bash
databricks bundle run if_else_job
```

![Success Path](../../docs/learning/08-use-if-else-task/02-success-if-else.png)

**Step 3: Run the failure path**

Override the parameter to simulate a failure in Task A. The DAG will route to Task C instead.

```bash
databricks bundle run if_else_job --params simulate_failure=true
```

![Failure Path](../../docs/learning/08-use-if-else-task/03-failed-if-else.png)