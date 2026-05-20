# Security And Credentials

ScienceClaw keeps secrets out of git and out of images. Credentials should be injected at runtime through local `.env` files, GitHub Secrets, Docker secrets, Kubernetes Secrets, or deployment-specific secret stores.

## Local Setup

```bash
cp .env.example .env
```

Edit `.env` locally. Do not commit it.

## What Requires Human Approval

Human approval is required before publishing, deleting files, pushing to GitHub, installing third-party skills, mounting new host folders, using external APIs with billing implications, or making sensitive public claims.

## Secret Hygiene

Run:

```bash
make smoke-test
scripts/check-secrets.sh
```

The smoke test checks that `.env` is not tracked and scans for obvious committed token patterns. `scripts/check-secrets.sh` validates Slack token shape without printing full values.

If a credential is exposed, revoke it first. History cleanup is not a substitute for rotation.

