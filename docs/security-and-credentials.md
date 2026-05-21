# Security And Credentials

ScienceClaw keeps secrets out of git and out of images. Credentials should be injected at runtime through local `.env` files, GitHub Secrets, Docker secrets, Kubernetes Secrets, or deployment-specific secret stores.

For reusable local deployments, prefer mounted secret files over literal tokens in `.env`. The optional `docker-compose.secrets.yml` overlay reads `secrets/github_token`, mounts it at `/run/secrets/github_token`, and sets `GITHUB_TOKEN_FILE`/`GH_TOKEN_FILE` for the services that need repository access. The entrypoint reads the secret into the running process and configures GitHub CLI for git operations; it does not copy the token into the image or the repository.

## Local Setup

```bash
cp .env.example .env
```

Edit `.env` locally. Do not commit it.

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
