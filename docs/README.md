# README

OpenClaw Local Docker is a small project for building and running the OpenClaw CLI on your laptop in Docker.

It persists OpenClaw state in `~/.openclaw`, keeps OAuth auth-profile secrets under that same mount, mounts only `./workspace` into the container, and includes helpers for ChatGPT/Codex OAuth login when that route is available.

## Quick Start

```bash
docker compose build
scripts/start.sh
scripts/login-codex.sh
scripts/status.sh
```

If OpenClaw opens a login URL from inside Docker, copy it into your laptop browser. If the CLI asks for a callback URL, paste the full browser redirect URL back into the terminal.

## Auth Options

ChatGPT/Codex OAuth can be convenient when your OpenClaw version, account entitlement, quota, and provider policy support it. It is not guaranteed and may require periodic re-login.

OpenAI API-key mode uses `OPENAI_API_KEY` from `.env` and bills through your OpenAI API account. It is optional for OAuth mode, but it is usually more predictable for automation.

## Safety

Keep `./workspace` small and task-specific. Do not mount your whole home directory, browser profile, SSH keys, password manager exports, or other sensitive folders.

Read the full root-level `README.md` in the repository for troubleshooting details and verified OpenClaw documentation links.
