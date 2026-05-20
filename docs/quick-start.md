# Quick Start

This page is the stable happy path for a new OASIS ScienceClaw checkout. It assumes you are comfortable enough to run a few terminal commands, but it does not assume deep Docker or GitHub knowledge.

## 1. Prepare Local Settings

```bash
cp .env.example .env
```

The `.env` file is local. Put tokens and local ports there, and do not commit it.

## 2. Initialize And Check The Workspace

```bash
make init-working-group
make doctor
```

`make init-working-group` creates the expected working-group scaffold. `make doctor` runs safe checks for repository structure, Docker availability, workspace files, and secret hygiene. Optional integrations may warn when they are not configured; warnings are not always failures.

## 3. Build And Start

```bash
make build
make up
```

The container starts with the PI Liaison workflow, a seeded `/workspace`, and the OASIS ScienceClaw branding. When multiple instances are running, use `docker compose ps` to confirm ports.

## 4. Run The Demo Workflow

```bash
make demo
```

The demo writes a deterministic toy habitat-suitability workflow to:

```text
workspace/outputs/demo/
  demo_habitat_suitability.csv
  figures/demo_habitat_suitability.svg
  metadata.json
  report.md
```

This demo is not intended to make a scientific claim. It proves that the workspace can run a reproducible scientific workflow and produce inspectable artifacts.

## 5. Review Outputs

Open the workspace UI or CMS and inspect `workspace/outputs/demo/`. The CMS/output review layer is where private outputs become reviewed public artifacts. Approved reports can be promoted into `docs/reports/`; small approved figures can move into `docs/assets/`.

## 6. Validate And Checkpoint

```bash
make smoke-test
make checkpoint
```

`make smoke-test` checks structure, secret hygiene, demo execution, and expected outputs. `make checkpoint` writes a local `workspace/CHECKPOINT.md` summary so the state of the session can survive rebuilds and handoffs.

## Core Commands

| Command | Purpose |
| --- | --- |
| `make build` | Build the local container image |
| `make up` | Start the local Compose stack |
| `make down` | Stop the local Compose stack |
| `make shell` | Open a shell in the OpenClaw container |
| `make init-working-group` | Create or refresh the local workspace scaffold |
| `make doctor` | Run safe local health checks |
| `make demo` | Run the deterministic environmental demo |
| `make smoke-test` | Run lightweight operational validation |
| `make checkpoint` | Write a local checkpoint summary |

