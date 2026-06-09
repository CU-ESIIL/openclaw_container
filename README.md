# OASIS ScienceClaw

OASIS ScienceClaw is a reproducible environmental data science working-group appliance built on OpenClaw. It packages a local container runtime, a seeded scientific workspace, a PI Liaison workflow, review-oriented output handling, and documentation for launching new working groups from a consistent base.

The goal is not to create a generic chatbot wrapper. The goal is a transparent scientific workspace where humans, agents, files, and outputs have clear roles.

## Who This Is For

This repository is for environmental scientists, ecologists, geographers, synthesis researchers, tribal collaborators, students, postdocs, and workshop teams who want a ready-to-use computational workspace without becoming infrastructure engineers.

It is also for maintainers who need a reusable template for multiple working groups.

## Why It Exists

ScienceClaw preserves the working-group model:

```text
GitHub = control plane
repo = memory
container = runtime
```

The container can be rebuilt. The scientific memory should persist in the repository, mounted workspace folders, volumes, or external storage. Agents may recommend. Humans approve.

## Quick Start

```bash
cp .env.example .env
make init-working-group
make doctor
make build
make up
```

Open the main chat UI with the tokenized dashboard URL from:

```bash
docker compose exec openclaw-local openclaw dashboard --no-open
```

Use the printed `127.0.0.1:18789` URL for the PI Liaison chat. The `127.0.0.1:8090` service is the workspace CMS and file-review sidecar, not the primary chat page.

Run the end-to-end demo:

```bash
make demo
make smoke-test
make checkpoint
```

The demo writes a small reproducible environmental workflow to `workspace/outputs/demo/`, including a CSV table, SVG figure, metadata, and report.

Open the integrated workspace file manager from the ScienceClaw sidebar or at `http://127.0.0.1:8090/files?path=/workspace`. It lets you browse the container from `/`, while write operations are restricted to safe project areas such as `/workspace`, `/workspace/outputs`, `/data/outputs`, and `/tmp`.

Open the GitHub Repository Manager from the same sidebar or at `http://127.0.0.1:8090/github`. It lets you authorize selected project repositories, clone them into `/workspace/repos/`, inspect branch status, and use a branch-and-pull-request workflow without granting agents account-wide GitHub access.

For organization repository access, provide a fine-grained GitHub token through `.env` or a mounted secret file. The intended local-secret path is:

```bash
mkdir -p secrets
printf '%s\n' 'github_pat_or_fine_grained_token' > secrets/github_token
chmod 600 secrets/github_token
docker compose -f docker-compose.yml -f docker-compose.secrets.yml up -d
```

At startup the container reads the secret file, exposes it only inside the running process as `GITHUB_TOKEN`/`GH_TOKEN`, and configures GitHub CLI for git operations. Agents and the GitHub manager still operate only on explicitly authorized repositories under `/workspace/repos/`.

For scalable launches, keep the same file-based secret contract but source the values from GitHub Secrets, Codespaces secrets, Kubernetes Secrets, or a deployment secret manager. A GitHub runner or deployment host should materialize short-lived secret files, set `GITHUB_TOKEN_FILE` and other provider `_FILE` variables, and start the container; the repository and image should never contain credential values.

To start a second working-group instance while another one is already open:

```bash
scripts/start-instance.sh project-two 18790 8889 8091
```

That command creates a separate `instances/project-two/` workspace and prints links for the Gateway, Workspace UI, and CMS. Validate the new instance before project work: it should show the 11-agent working group, with `main` as the PI Liaison. If the agent dropdown is missing or a session-lock error appears, use the [multi-instance runbook](docs/instance-runbook.md) rather than copying whole OpenClaw state directories between instances.

## Core Commands

| Command | Purpose |
| --- | --- |
| `make build` | Build the local container image |
| `make up` | Start the local Docker Compose stack |
| `make down` | Stop the local Docker Compose stack |
| `make shell` | Open a shell in the OpenClaw container |
| `make init-working-group` | Create or refresh the workspace scaffold |
| `make doctor` | Run safe local health checks |
| `make demo` | Run the deterministic environmental demo workflow |
| `make smoke-test` | Validate structure, demo outputs, and secret hygiene |
| `make workspace-smoke-test` | Validate the workspace file manager and path restrictions |
| `make github-smoke-test` | Validate the GitHub repository manager safety checks |
| `make checkpoint` | Write a local checkpoint summary |

## Storage Model

ScienceClaw uses three zones:

- **Repository**: infrastructure, scripts, docs, templates, examples, tests, and reviewed public artifacts.
- **`/workspace`**: active scientific work, project memory, drafts, agent reports, and working outputs.
- **`/external_storage`**: large data, mounted institutional storage, and durable artifacts that should not be committed.

Secrets belong in `.env`, GitHub Secrets, Docker secrets, Kubernetes Secrets, or deployment-specific secret stores. They do not belong in git, markdown files, screenshots, or prompt logs.

## Safety Model

- The PI Liaison is the primary human-facing coordinator.
- Specialist agents work through shared files and review packets.
- Slack, when enabled, should talk to the PI Liaison rather than execution agents.
- Human approval is required before publication, deletion, GitHub pushes, new mounts, third-party tools, billed APIs, or sensitive claims.
- Routine analysis packages may be installed inside a running disposable container when logged; durable dependencies should be added to requirements or the Dockerfile.
- Kubernetes workers are optional bounded execution jobs, not autonomous self-spawning agents.

## Stable And Experimental

Stable in the current alpha:

- container build and local Docker Compose workflow
- seeded `/workspace` structure
- OASIS ScienceClaw branding
- PI Liaison and working-group file scaffold
- storage model and secret hygiene conventions
- deterministic demo workflow
- smoke tests and health checks
- CMS/output review pattern
- integrated workspace file manager for browsing, previews, safe editing, and output inspection
- GitHub repository manager for selected project repositories
- MkDocs documentation structure

Experimental or deployment-specific:

- Slack automation
- advanced model routing
- Kubernetes-backed workers
- distributed worker scheduling
- persistent memory synchronization across deployments
- automated public publishing
- cloud deployment patterns

## Documentation

Start with:

- [Quick Start](docs/quick-start.md)
- [Architecture](docs/architecture.md)
- [Storage Model](docs/storage-model.md)
- [Agent Team](docs/agent-team.md)
- [CMS and Output Review](docs/cms-output-review.md)
- [Workspace File Manager](docs/workspace-file-manager.md)
- [GitHub Repository Manager](docs/github-repository-manager.md)
- [Security and Credentials](docs/security-and-credentials.md)
- [Troubleshooting](docs/troubleshooting.md)

The MkDocs site source lives in `docs/`.

## Current Status

This repository is being stabilized as `0.1.0-alpha.1`. It is suitable for local template development and working-group appliance testing. It is not yet a promise of fully managed autonomy, production-grade orchestration, or unattended publishing.

Preserve OpenClaw attribution when extending the template: OASIS ScienceClaw is powered by OpenClaw.
