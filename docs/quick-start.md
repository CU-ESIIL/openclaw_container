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

## Restart Or Start Another Working Group

To restart the default local stack:

```bash
make up
```

To stop it:

```bash
make down
```

To start a separate working-group instance while another one is already open, use the instance helper with a unique name and ports:

```bash
scripts/start-instance.sh project-two 18790 8889 8091
```

This creates an isolated instance directory:

```text
instances/project-two/
  data/
  workspace/
  external_storage/
  openclaw/
```

The helper prints three links when it finishes:

| Link | Purpose |
| --- | --- |
| Gateway | OpenClaw chat and control UI for that instance |
| Workspace UI | JupyterLab file browser for that instance |
| Workspace CMS | Review and promote outputs for that instance |

Use a different instance name and different ports for each additional working group.

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

Click **Files** in the ScienceClaw sidebar to see a compact workspace listing. You can also open it directly:

```text
http://127.0.0.1:8090/files?path=/workspace
```

The file manager shows the container filesystem from `/`, but it treats `/workspace` as the normal project area. Browse to `workspace/outputs/demo/` to inspect the demo report, CSV table, and figure outputs. The CMS/output review layer is where private outputs become reviewed public artifacts. Approved reports can be promoted into `docs/reports/`; small approved figures can move into `docs/assets/`.

## 6. Connect Project Repositories

Click **GitHub Auth** in the ScienceClaw sidebar to see credential status and setup actions. You can also open it directly:

```text
http://127.0.0.1:8090/github
```

Use this tab for other repositories that the working group should inspect or contribute to. The current container repository remains infrastructure. Connected repositories are project workspaces and clone into:

```text
/workspace/repos/
```

For local GitHub CLI authentication inside the container, run:

```bash
gh auth login
gh auth setup-git
gh auth status
```

For repeatable appliance-style launches, use a local Docker secret instead of interactive login:

```bash
mkdir -p secrets
printf '%s\n' 'github_pat_or_fine_grained_token' > secrets/github_token
chmod 600 secrets/github_token
docker compose -f docker-compose.yml -f docker-compose.secrets.yml up -d
```

The token should be fine-grained and scoped to the organization repositories this working group is allowed to use. On startup, ScienceClaw reads the secret file, configures GitHub CLI for git credential use, and makes the same credential available to the OpenClaw agent runtime and the GitHub manager service.

Add repositories explicitly by `owner/repo`. Use the `read` tier for inspection and the `contribute` tier when the working group may create branches, commit changes, push branches, and open pull requests. Direct pushes to `main` and `master` are blocked by default.

## 7. Validate And Checkpoint

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
| `make workspace-smoke-test` | Validate the workspace file manager |
| `make github-smoke-test` | Validate the GitHub repository manager |
| `make checkpoint` | Write a local checkpoint summary |
