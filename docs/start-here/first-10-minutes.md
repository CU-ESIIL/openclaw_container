# First 10 Minutes

This page gives you one small successful loop: launch, look around, make a safe edit, and checkpoint the state.

!!! tip "This is a quick win path"
    You can safely skip advanced deployment, Kubernetes, and storage configuration for now.

## 1. Open The Repository

Start in the repository folder:

```bash
pwd
ls
```

You should see files such as `Dockerfile`, `docker-compose.yml`, `README.md`, `docs/`, `docker/`, and `scripts/`.

## 2. Prepare Local Settings

Copy the example environment file if `.env` does not exist:

```bash
cp .env.example .env
```

Edit `.env` only for local settings and tokens. Do not commit `.env`.

## 3. Launch The Container

```bash
docker compose up --build
```

If you already built the image, this may be enough:

```bash
docker compose up
```

## 4. Open The Workspace Interfaces

Typical local links are:

| Interface | What It Is For |
| --- | --- |
| OpenClaw Control UI | Chat, sessions, agents, and model routes |
| JupyterLab | File browsing, notebooks, markdown, figures, and previews |
| Workspace CMS | Reviewing private drafts and promoting public pages |

Ports can vary when multiple instances are running. Use:

```bash
docker compose ps
```

## 5. Check Health

Run:

```bash
make doctor
scripts/status.sh
scripts/test-working-group.sh
```

These commands inspect the setup without asking agents to perform open-ended work.

## 6. Make One Safe Edit

Open `PROJECT_CHARTER.md` in the workspace and update the project title or purpose.

This is safe because it changes project memory, not credentials or container internals.

## 7. Checkpoint

At the end of a session, record what changed in the working group notes or checkpoint files. If the change belongs in the reusable template, commit it to git. If it is private project work, keep it in the mounted workspace or external storage.

```bash
make checkpoint
```

!!! warning "Do not commit secrets"
    `.env`, API keys, Slack tokens, private data, and credentials should stay local or in a secret manager.
