# Security And Credentials

ScienceClaw keeps secrets out of git and out of images. Credentials should be injected at runtime through local `.env` files, GitHub Secrets, Docker secrets, Kubernetes Secrets, or deployment-specific secret stores.

For reusable local deployments, prefer mounted secret files over literal tokens in `.env`. The optional `docker-compose.secrets.yml` overlay reads `secrets/github_token`, mounts it at `/run/secrets/github_token`, and sets `GITHUB_TOKEN_FILE`/`GH_TOKEN_FILE` for the services that need repository access. The entrypoint reads the secret into the running process and configures GitHub CLI for git operations; it does not copy the token into the image or the repository.

## Local Setup

```bash
cp .env.example .env
```

Edit `.env` locally. Do not commit it.

For GitHub repository access, prefer a token file over a literal token in `.env`:

```bash
mkdir -p secrets
printf '%s\n' 'PASTE_YOUR_FINE_GRAINED_TOKEN_HERE' > secrets/github_token
chmod 600 secrets/github_token
```

For the gateway 3 prototype, start or restart the instance with the secrets overlay enabled:

```bash
SCIENCECLAW_GITHUB_TOKEN_FILE=./secrets/github_token \
SCIENCECLAW_USE_SECRETS_OVERLAY=1 \
scripts/start-instance.sh project-three 18791 8890 8092
```

After the instance is running, open **GitHub Auth** in the ScienceClaw sidebar and click **Configure git credentials**. That action configures GitHub CLI and git credential use inside the running services without exposing the token in logs or browser output.

## GitHub Secrets Deployment Pattern

For scalable launches, store credentials in GitHub Secrets and materialize them only on the runner or deployment host. Do not copy a local `.env` into the repository, image, or workspace.

Recommended secret names:

| GitHub Secret | Runtime variable | Purpose |
| --- | --- | --- |
| `SCIENCECLAW_GITHUB_TOKEN` | `GITHUB_TOKEN_FILE` / `GH_TOKEN_FILE` | Fine-grained repository access |
| `SCIENCECLAW_VERDE_LLM_API_KEY` | `VERDE_LLM_API_KEY_FILE` | AI-VERDE model route |
| `SCIENCECLAW_OPENAI_API_KEY` | `OPENAI_API_KEY_FILE` | Optional OpenAI API-key route |
| `SCIENCECLAW_SLACK_BOT_TOKEN` | `SLACK_BOT_TOKEN_FILE` | Slack bot token |
| `SCIENCECLAW_SLACK_APP_TOKEN` | `SLACK_APP_TOKEN_FILE` | Slack Socket Mode app token |
| `SCIENCECLAW_TAVILY_API_KEY` | `TAVILY_API_KEY_FILE` | Optional web-search provider |

The manual runtime workflow also accepts common local `.env`-style aliases for Verde and Slack: `VERDE_LLM_API_KEY`, `VERDE_LLM_BASE_URL`, `VERDE_LLM_DEFAULT_MODEL`, `SLACK_BOT_TOKEN`, `SLACK_APP_TOKEN`, and `SLACK_DEFAULT_CHANNEL`. Prefer repository variables for non-secret values such as `VERDE_LLM_BASE_URL`, `VERDE_LLM_DEFAULT_MODEL`, and `SLACK_DEFAULT_CHANNEL`, but the workflow can read them from secrets if they were entered there during setup.

For repository push/pull access from the agents and GitHub manager, add `SCIENCECLAW_GITHUB_TOKEN`. That token should be a fine-grained GitHub personal access token scoped only to the repositories ScienceClaw should manage.

On a GitHub-hosted runner, self-hosted runner, or Codespaces startup task, write each secret to a runner-local file and point the container at that file:

```bash
mkdir -p secrets
printf '%s\n' "${SCIENCECLAW_GITHUB_TOKEN}" > secrets/github_token
chmod 600 secrets/github_token

SCIENCECLAW_GITHUB_TOKEN_FILE=./secrets/github_token \
docker compose -f docker-compose.yml -f docker-compose.secrets.yml up -d
```

For spawned instances, use the instance helper instead of raw Compose:

```bash
SCIENCECLAW_GITHUB_TOKEN_FILE=./secrets/github_token \
SCIENCECLAW_USE_SECRETS_OVERLAY=1 \
scripts/start-instance.sh project-three 18791 8890 8092
```

For a long-running shared deployment, prefer a self-hosted runner, Kubernetes Secret, or cloud secret manager rather than a GitHub-hosted Actions runner. GitHub-hosted runners are ephemeral and are best for build, smoke-test, or image publication jobs; they are not a durable place to host the live Gateway.

The repository includes a manual workflow for this pattern:

```text
.github/workflows/scienceclaw-runtime.yml
```

Run **ScienceClaw runtime from secrets** from the GitHub Actions tab. For a durable instance, use a self-hosted runner label. The workflow writes a runner-local `.env` plus a Docker secret file from GitHub Secrets, starts an instance with `scripts/start-instance.sh`, runs gateway and CMS smoke checks, and prints local runtime links in the job summary. The generated files remain on the runner and are not committed to git.

When `authorize_launch_repo` is left at its default `true`, the workflow also records the current repository in `/workspace/.openclaw-github/authorized-repos.yaml` and clones it into `/workspace/repos/<repo>`. If `SCIENCECLAW_GITHUB_TOKEN` is present, that launch repository is registered with `contribute` permission so agents and the GitHub manager can create branches, push branches, and open pull requests back to the same repository.

Keep OpenClaw runtime state separate from secrets. Session files, locks, OAuth caches, and gateway tokens should live on local runtime storage for the instance, not in GitHub and not in cloud-synced repository folders. For local multi-instance runs on macOS, `scripts/start-instance.sh` uses `/private/tmp/scienceclaw-<instance>-openclaw` by default for this reason. On GitHub Actions runners, it uses `$RUNNER_TEMP/scienceclaw-<instance>-openclaw`; on other Linux hosts, it falls back to `/tmp`.

## What Requires Human Approval

Human approval is required before publishing, deleting files, pushing to GitHub, installing third-party OpenClaw skills, mounting new host folders, using external APIs with billing implications, modifying credentials, changing durable image dependencies, or making sensitive public claims.

Routine package installs inside a running disposable container are treated differently from durable template changes. If an analysis needs a Python package such as `scikit-learn`, the agent may install it inside the running container and log the command and purpose. If the package is needed for future deployments, add it to `requirements-spatiotemporal.txt`, `requirements.txt`, or the `Dockerfile` through a reviewed repository change.

## Secret Hygiene

Run:

```bash
make smoke-test
scripts/check-secrets.sh
```

The smoke test checks that `.env` is not tracked and scans for obvious committed token patterns. `scripts/check-secrets.sh` validates Slack token shape without printing full values.

If a credential is exposed, revoke it first. History cleanup is not a substitute for rotation.
