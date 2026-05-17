# OpenClaw Local Docker

Run OpenClaw locally in Docker with a small, persistent workspace and support for ChatGPT/Codex OAuth login when your installed OpenClaw version and account allow it.

This repository gives you:

- a local Docker image for the OpenClaw CLI
- a Compose service with a persisted `/root/.openclaw` config directory
- helper scripts for build, shell access, Codex OAuth login, and model status
- a simple MkDocs site with a practical pricing-style comparison

## Why Docker?

Docker keeps OpenClaw, Node, and supporting shell tools separate from your laptop setup. You can rebuild the image, remove containers, or change project files without installing the OpenClaw CLI directly on macOS.

The important persistent pieces are mounted from the host:

- `~/.openclaw` -> `/root/.openclaw` for OpenClaw config, sessions, and auth profiles
- `./workspace` -> `/workspace` for files you intentionally let the agent see

The container sets `OPENCLAW_AUTH_PROFILE_SECRET_DIR=/root/.openclaw/auth-profile-secrets` so OAuth profile encryption state is kept inside the same persisted mount.

Avoid mounting your whole home directory. Keep the workspace small and explicit.

## ChatGPT/Codex OAuth vs OpenAI API Keys

OpenClaw can use different OpenAI auth paths:

- **ChatGPT/Codex OAuth** uses an interactive account login, often tied to ChatGPT or Codex subscription entitlements.
- **OpenAI API key mode** uses `OPENAI_API_KEY` and bills through the OpenAI API platform.

OAuth can be convenient and may be the cheapest path when it is available, but it is not guaranteed. Support can depend on your OpenClaw version, account entitlement, provider policy, quota windows, and occasional re-login requirements. API keys are usually more predictable for automation because billing, limits, and credentials are explicit.

The Codex OAuth command used by this repo is documented by OpenClaw as:

```bash
openclaw models auth login --provider openai-codex
```

## Prerequisites

- Docker Desktop or Docker Engine with Docker Compose v2
- Git
- A ChatGPT/Codex account for OAuth mode, or an OpenAI API key for API-key mode

## Quick Start

Clone the repository:

```bash
git clone <your-repo-url>
cd <your-repo-directory>
```

Build the image:

```bash
docker compose build
```

Open an interactive shell in the container:

```bash
docker compose run --rm openclaw-local
```

Or use the helper:

```bash
scripts/start.sh
```

Log in with ChatGPT/Codex OAuth from your host terminal:

```bash
scripts/login-codex.sh
```

If OpenClaw opens a browser URL from inside Docker, copy that URL into your laptop browser. If the browser lands on a callback or redirect URL and the CLI asks for it, paste the full callback URL back into the terminal.

Check model/auth status:

```bash
scripts/status.sh
```

## API-Key Mode

Copy the example environment file:

```bash
cp .env.example .env
```

Set `OPENAI_API_KEY` only if you want API-key mode. It is optional for Codex OAuth mode.

```dotenv
OPENAI_API_KEY=sk-...
OPENCLAW_MODEL=openai/gpt-5.1-codex
```

Then run:

```bash
docker compose run --rm openclaw-local openclaw models status
```

## Keeping Your Laptop Usable

The Compose service asks Docker for about 2 CPUs and 4 GB of memory:

- `cpus: "2.0"`
- `mem_limit: 4g`
- `deploy.resources.limits.memory: 4G`

Docker Desktop settings still matter. If builds or agent sessions feel heavy, reduce concurrent work, keep the mounted workspace small, and avoid large generated files or logs inside `workspace/`.

## Security Notes

Treat autonomous agents as software with file and network access.

- Do not mount sensitive folders such as your whole home directory, browser profile, password manager exports, SSH keys, or cloud-drive roots.
- Put only task-specific files in `workspace/`.
- Do not store secrets in Git.
- Only install trusted OpenClaw skills or plugins.
- Review generated commands before running them against important files or remote systems.

## Troubleshooting

### `openclaw: command not found`

Rebuild the image:

```bash
docker compose build --no-cache
```

Then check the installed CLI:

```bash
docker compose run --rm openclaw-local openclaw --version
```

### OAuth callback fails

Docker/headless login flows may not be able to open your browser directly. Copy the login URL into your browser, complete the account flow, then paste the full callback URL into the CLI if prompted.

### Model route not found

Run:

```bash
scripts/status.sh
```

Check whether the configured model belongs to the same provider as your auth profile. For Codex OAuth, model IDs commonly use the `openai-codex/...` provider route.

### Token or session expired

Run the login helper again:

```bash
scripts/login-codex.sh
```

OAuth-backed sessions may expire or need refreshing.

### Docker on Apple Silicon

This image uses the multi-architecture `node:24-bookworm-slim` base. Docker Desktop on Apple Silicon should build the native arm64 image by default. If you force an amd64 build, expect slower performance under emulation.

### Falling back to `OPENAI_API_KEY`

If OAuth is unavailable, create `.env` from `.env.example`, set `OPENAI_API_KEY`, and choose an API-key-backed model. API-key mode is often the most predictable path for automation.

## Documentation Site

Preview the site locally:

```bash
python -m pip install -r requirements.txt
mkdocs serve
```

Then open `http://127.0.0.1:8000`.

## Verified References

- [OpenClaw install docs](https://documentation.openclaw.ai/install)
- [OpenClaw Docker docs](https://documentation.openclaw.ai/install/docker)
- [OpenClaw model auth docs](https://docs.openclaw.ai/cli/models)
- [OpenClaw model providers](https://openclawlab.com/en/docs/concepts/model-providers/)
