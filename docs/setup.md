# Setup Guide

ScienceClaw is a small project for building and running an OpenClaw-based environmental synthesis workspace on your laptop in Docker.

It persists OpenClaw state in `~/.openclaw`, exposes that state inside the container at `/data/.openclaw`, mounts a narrow `./workspace` into `/data/workspace` and `/workspace`, and includes helpers for ChatGPT/Codex OAuth login when that route is available.

The image also bootstraps local defaults before each command runs: local Gateway mode, Docker-friendly Gateway bind settings, token auth, Control UI origins for local browser use, a Codex default model, the `/data` runtime layout, and starter workspace files from `docker/seed-workspace`.

The default workspace is a scientific working group scaffold for environmental data science. It includes 11 bounded roles, a PI Liaison gateway, shared memory registers, project folders, skeptic review, and human approval rules.

The `0.1.0-alpha.1` baseline is intended to be reproducible from the repository: build the image, provide local `.env` credentials, and the container seeds the working-group setup automatically.

## Quick Start

```bash
docker compose build
scripts/start.sh
scripts/login-codex.sh
scripts/status.sh
```

If OpenClaw opens a login URL from inside Docker, copy it into your laptop browser. If the CLI asks for a callback URL, paste the full browser redirect URL back into the terminal.

For Slack-connected Gateway operation, use the operations runbook:

```bash
scripts/start-gateway.sh
docker exec <container-id> openclaw channels status --channel slack --probe --timeout 20000
docker exec -it <container-id> openclaw models auth login --provider openai-codex --set-default
docker exec <container-id> openclaw agent --session-id slack-ready-check --message 'Reply with exactly: PI Liaison ready' --timeout 120
```

If Slack returns an access pairing code, approve the specific user:

```bash
docker exec -it <container-id> openclaw pairing approve slack <PAIRING_CODE>
```

Generated documents, heartbeat notes, soul files, and memory should be written under `/workspace` inside the container. They appear on the host under `./workspace`.

To inspect or edit files through the optional browser workspace UI:

```bash
docker compose up workspace-ui
```

Then open `http://127.0.0.1:8888` and use the `WORKSPACE_UI_TOKEN` value from `.env`, or the default local token `scienceclaw`.

## Auth Options

ChatGPT/Codex OAuth can be convenient when your OpenClaw version, account entitlement, quota, and provider policy support it. It is not guaranteed and may require periodic re-login.

OpenAI API-key mode uses `OPENAI_API_KEY` from `.env` and bills through your OpenAI API account. It is optional for OAuth mode, but it is usually more predictable for automation.

## Safety

Keep `./workspace` small and task-specific. Do not mount your whole home directory, browser profile, SSH keys, password manager exports, or other sensitive folders.

Read the full root-level `README.md` in the repository for troubleshooting details and verified OpenClaw documentation links.
