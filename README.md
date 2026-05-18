# ScienceClaw

ScienceClaw is an AI-native environmental synthesis workspace built on OpenClaw. It runs locally in Docker, keeps agent access focused on a narrow workspace, and supports ChatGPT/Codex OAuth login when your installed OpenClaw version and account allow it.

This repository gives you:

- a local Docker image for the OpenClaw CLI plus scientific utilities
- a Compose service with a persisted `/data/.openclaw` config directory
- image-level bootstrap defaults for the local Gateway, Control UI origins, default model, and starter workspace files
- an optional browser workspace UI through JupyterLab
- helper scripts for build, shell access, Codex OAuth login, and model status
- a simple MkDocs site with setup, security, and model/auth option notes

## Alpha Baseline

This repository is currently prepared as `0.1.0-alpha.1`: a reproducible base container for an OpenClaw scientific working group.

The alpha image seeds `/workspace` with the PI Liaison workflow, 11 bounded agent roles, shared memory files, project intake documents, review gates, and service templates. Users should not need to reload these files or recreate the agent setup after launching the container.

Slack is configured from local environment variables, not baked into the image. When Slack tokens are present, startup registers the Slack channel with OpenClaw using environment-backed credentials.

Model routing is role-aware. The PI Liaison and Scientific Director should stay on OpenAI/Codex OAuth or another approved high-reliability route, while narrower specialist agents can be evaluated against open-model API endpoints. The seeded workspace includes `MODEL_ASSIGNMENTS.md` for recording those choices.

Curated outputs from live container sessions can be preserved under `examples/`. The live `workspace/` directory stays ignored so local source materials, credentials, auth state, and project-specific runtime files are not accidentally committed.

The default workspace also includes reusable governance templates: team norms, decision protocol, memory quarantine, artifact registry, societal impact checklist, role reproducibility notes, data provenance folders, and a meeting template.

## ScienceClaw Workspace

The alpha container initializes a persistent `/data` layout alongside the compatibility `/workspace` mount:

- `/data/.openclaw` for OpenClaw state and auth profiles
- `/data/workspace` for the primary scientific workspace, also mounted as `/workspace`
- `/data/downloads` for user-approved downloads awaiting provenance notes
- `/data/outputs/reports`, `/data/outputs/figures`, and `/data/outputs/tables` for generated artifacts
- `/data/skills/core`, `/data/skills/experimental`, and `/data/skills/local` for future tool extension
- `/data/notebooks` for persistent notebooks
- `/data/stac` for geospatial catalog examples or configuration

Initialize or inspect that layout with:

```bash
scripts/init-data-layout.sh --data-root ./data
```

The image also includes baseline scientific and development tools: `git`, `gh`, `curl`, `wget`, `jq`, `ripgrep`, `tree`, `tmux`, `vim`, `nano`, `pandoc`, `poppler-utils`, `imagemagick`, `ghostscript`, `qpdf`, `gdal-bin`, `proj-bin`, LibreOffice, Python, `uv`, JupyterLab, and Playwright Python bindings. Example conversion scripts live in `examples/`.

## Why Docker?

Docker keeps OpenClaw, Node, and supporting shell tools separate from your laptop setup. You can rebuild the image, remove containers, or change project files without installing the OpenClaw CLI directly on macOS.

The important persistent pieces are mounted from the host:

- `~/.openclaw` -> `/data/.openclaw` for OpenClaw config, sessions, and auth profiles
- `./data` -> `/data` for persistent runtime state and outputs
- `./workspace` -> `/data/workspace` and `/workspace` for files you intentionally let the agent see

The container sets `OPENCLAW_AUTH_PROFILE_SECRET_DIR=/data/.openclaw/auth-profile-secrets` so OAuth profile encryption state is kept inside the same persisted mount.

Avoid mounting your whole home directory. Keep the workspace small and explicit.

## Image Bootstrap

The image now initializes the local OpenClaw setup before the requested command runs. This means the container starts with the same durable defaults instead of requiring manual repair after launch:

- `gateway.mode=local`
- `gateway.bind=lan`, so Docker's `127.0.0.1:18789` port can reach the Gateway
- token auth enabled, with a generated token persisted in `~/.openclaw/openclaw.json` unless `OPENCLAW_GATEWAY_TOKEN` is provided
- Control UI origins allowed for `http://127.0.0.1:18789` and `http://localhost:18789`
- default model set from `OPENCLAW_MODEL`, or `OPENCLAW_DEFAULT_MODEL` when `OPENCLAW_MODEL` is unset
- `openai` and `codex` plugins enabled in config
- starter workspace files copied from `docker/seed-workspace` into `/workspace` when missing

The seed copy is non-destructive. If you edit workspace memory, heartbeat notes, soul notes, or generated documents, the entrypoint does not overwrite them on the next launch.

To disable workspace seeding for a run:

```bash
OPENCLAW_SEED_WORKSPACE=0 scripts/start.sh
```

## ChatGPT/Codex OAuth vs OpenAI API Keys

OpenClaw can use different OpenAI auth paths:

- **ChatGPT/Codex OAuth** uses an interactive account login, often tied to ChatGPT or Codex subscription entitlements.
- **OpenAI API key mode** uses `OPENAI_API_KEY` and bills through the OpenAI API platform.

OAuth can be convenient and may be the cheapest path when it is available, but it is not guaranteed. Support can depend on your OpenClaw version, account entitlement, provider policy, quota windows, and occasional re-login requirements. API keys are usually more predictable for automation because billing, limits, and credentials are explicit.

The Codex OAuth command used by this repo is documented by OpenClaw as:

```bash
openclaw models auth login --provider openai-codex
```

## Secrets and Credentials

Slack credentials for the PI Liaison live in a local `.env` file. They must never be committed, hardcoded, pasted into chat, stored in markdown notes, or printed in logs.

Create your local environment file from the template:

```bash
cp .env.example .env
```

Edit `.env` and set:

```dotenv
SLACK_BOT_TOKEN=xoxb-your-real-token
SLACK_APP_TOKEN=xapp-1-APPID-INSTALLID-your-real-token
SLACK_DEFAULT_CHANNEL=#science-working-group
```

Optional open-model API experiment variables can also live in `.env`:

```dotenv
VERDE_LLM_BASE_URL=https://llm-api.cyverse.ai/v1
VERDE_LLM_API_KEY=
VERDE_LLM_DEFAULT_MODEL=
VERDE_LLM_PROVIDER_NAME=verde
```

AI-VERDE API documentation is available at <https://aiverde-docs.cyverse.ai/api/>. After adding a local key, list available models with:

```bash
curl -s -L "${VERDE_LLM_BASE_URL}/models" \
  -H "Authorization: Bearer ${VERDE_LLM_API_KEY}" \
  -H "Content-Type: application/json"
```

The currently documented candidate model inventory is in `docs/model-routing.md` and seeded into `/workspace/MODEL_ASSIGNMENTS.md`. Confirm availability with the API before assigning a model to a role.

Before startup, run:

```bash
scripts/check-secrets.sh
```

The checker refuses missing or placeholder Slack tokens and prints only masked previews, such as `xoxb-****abcd`.

`SLACK_APP_TOKEN` must be a Slack app-level Socket Mode token with the `connections:write` scope. Do not use the Slack signing secret or legacy verification token here.

Rotate Slack tokens immediately if they appear in git, screenshots, prompt logs, terminal transcripts, browser captures, or chat. Revoke the old token in Slack, regenerate it, update `.env`, restart the service, and inspect git history if the token was committed.

Slack should connect only to the PI Liaison. Slack messages should enter queues and workspace memory for reviewable routing; they should not directly trigger arbitrary shell execution or bypass human approval rules.

Slack-side setup also matters. Enable Socket Mode, invite the bot to the target channel, enable the App Home Messages tab if direct messages are needed, subscribe to `app_mention` and `message.im` bot events as appropriate, and reinstall the app after changing scopes or events.

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

Start a long-running Gateway for Slack inbound messages:

```bash
scripts/start-gateway.sh
```

Start the optional browser workspace UI:

```bash
docker compose up workspace-ui
```

Then open `http://127.0.0.1:8888` with the `WORKSPACE_UI_TOKEN` value from `.env` or the default local token `scienceclaw`.

Verify Slack Socket Mode:

```bash
docker exec <container-id> openclaw channels status --channel slack --probe --timeout 20000
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

For Slack-connected operation, the most reliable OAuth refresh path is inside the live Gateway container:

```bash
docker exec -it <container-id> openclaw models auth login --provider openai-codex --set-default
```

If Slack returns a pairing code, approve the specific Slack user:

```bash
docker exec -it <container-id> openclaw pairing approve slack <PAIRING_CODE>
```

Then smoke-test the model path before testing Slack:

```bash
docker exec <container-id> openclaw agent --session-id slack-ready-check --message 'Reply with exactly: PI Liaison ready' --timeout 120
```

See `docs/operations.md` for the full reproducible Slack/Gateway runbook.

Generated documents, heartbeat notes, soul files, and memory files should be saved under `/workspace` inside the container. They will appear on the host under `./workspace`.

## Scientific Working Group Mode

The container seeds `/workspace` as a reproducible environmental data science working group. The goal is not to create ten unconstrained chatbots; it is to create a small, reviewable scientific institution with roles, memory, evidence standards, disagreement, and human review.

The default setup includes 11 bounded roles in `/workspace/AGENTS.md`:

- PI Liaison / User Interview Agent
- Scientific Director
- Deputy Director / Integrator
- Data Engineer / Infrastructure Scientist
- Quantitative Modeler
- Domain Scientist
- Scientific Narrative Lead
- Technical Communicator
- Citation & Evidence Curator
- Skeptic / Adversarial Reviewer
- Societal Impact / Translation Agent

Use `AGENTS.md` as the role charter. Each role has a mission, responsibilities, allowed changes, actions that require approval, required outputs, review cadence, and failure modes. The structure is intentionally bounded so autonomous work has a clear scope.

Use `MODEL_ASSIGNMENTS.md` as the routing register. Keep the PI Liaison and Scientific Director on the most reliable approved route, and evaluate open-model APIs first on bounded specialist tasks before promoting them to defaults.

Use `documents/TEAM_NORMS.md`, `documents/DECISION_PROTOCOL.md`, `documents/ARTIFACT_REGISTRY.md`, and the seeded role reproducibility notes to make the working group auditable across sessions. Treat them as templates to review during project intake.

Start a project by drafting a project charter in `/workspace/documents`. The charter should define the research question, intended outputs, candidate data sources, expected review gates, and any sensitive domains that require extra human review.

Use these folders by default:

- `/workspace/analysis` for reproducible analysis outputs, diagnostics, and notebooks
- `/workspace/scripts` for initialization, smoke tests, utilities, and reproducible workflows
- `/workspace/figures` for generated figures and figure provenance notes
- `/workspace/literature` for citation notes, source inventories, evidence tables, and license notes
- `/workspace/daily_notes` for dated working notes
- `/workspace/agent_reports` for role-specific memos, skeptic reviews, and handoff notes

Skeptic review is required before major claims are promoted into reports, manuscripts, presentations, or public pages. The Skeptic role should identify alternative explanations, weak evidence, hidden assumptions, and unresolved objections. Those objections should be resolved, accepted as limitations, or escalated to human review.

Impact translation happens after claims are evidence-backed and reviewed. The Societal Impact / Translation Agent can prepare audience maps, misuse notes, and cautious translation drafts, but human approval is required before policy recommendations or claims about communities, Tribes, Indigenous knowledge, public health, legal rules, or other sensitive domains.

Human approval rules live in `/workspace/HUMAN_REVIEW.md`. Approval is required before deleting files, pushing to GitHub, installing third-party OpenClaw skills, mounting new host folders, sending emails or messages, modifying credentials, publishing web pages, running expensive jobs, or using external APIs with billing implications.

Keep the mounted workspace narrow. Mounting the whole home directory gives autonomous agents unnecessary access to unrelated personal files, browser profiles, credentials, SSH keys, cloud folders, and other sensitive data. This repo intentionally mounts only `./workspace` plus OpenClaw's persisted config directory.

To re-run the initializer manually inside the container:

```bash
/workspace/scripts/init-working-group.sh
```

To verify the scaffold locally:

```bash
scripts/test-working-group.sh
```

## PI Liaison Workflow

By default, the container launches into the PI Liaison / User Interview Agent. The experience should feel like talking to a chief of staff for the scientific working group: one human-facing agent gathers the right context, turns your answers into structured project files, and coordinates the rest of the team.

The user talks mainly to the PI Liaison. The PI Liaison talks to the working group through `TEAM_BRIEF.md`, `INITIAL_TASKS.md`, and role assignments in `AGENTS.md`. Other agents should not interrupt the user directly unless explicitly invited.

The startup interview lives in `/workspace/PROJECT_INTAKE.md`, and the startup prompt lives in `/workspace/prompts/pi-liaison-startup.md`. After intake, the PI Liaison drafts `/workspace/PROJECT_CHARTER.md`, updates `/workspace/TEAM_BRIEF.md`, creates `/workspace/INITIAL_TASKS.md`, and records user preferences or constraints in `/workspace/USER_CONTEXT.md`.

Other agents file questions in `/workspace/QUESTIONS_FOR_USER.md`. The PI Liaison reviews that queue, merges duplicates, removes low-value interruptions, and asks the user only batched, high-priority questions with the decision each question blocks.

The PI Liaison also submits milestone summaries, draft reports, and publication packages to the user for review. It does not approve publication, deletion, pushing to GitHub, new skills, external API use, or sensitive claims on the user's behalf.

This keeps the working group coordinated without turning the user into a dispatcher for every role. It reduces interruptions and prevents agent chaos by making one role responsible for intake, routing, question batching, and review packets.

To launch the PI Liaison manually inside the container:

```bash
/workspace/scripts/start-pi-liaison.sh
```

The liaison startup runs `/workspace/scripts/check-secrets.sh` before opening the Slack-connected flow. If `SLACK_BOT_TOKEN`, `SLACK_APP_TOKEN`, or `SLACK_DEFAULT_CHANNEL` are missing or still placeholders, startup stops cleanly.

To start a plain shell instead of the liaison workflow:

```bash
OPENCLAW_START_PI_LIAISON=0 scripts/start.sh
```

For Slack to call into OpenClaw while you are not using the interactive TUI, run:

```bash
scripts/start-gateway.sh
```

This starts the Gateway in a detached container after validating `.env`.

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

## Publishing Images

GitHub Actions build the container for pull requests and can publish tagged releases. The GHCR workflow publishes to GitHub Container Registry. The Docker Hub workflow is optional and expects repository-level secrets or variables, not local `.env` values:

- `DOCKERHUB_USERNAME`
- `DOCKERHUB_TOKEN`
- optional repository variable `DOCKERHUB_IMAGE`, defaulting to `cu-esiil/scienceclaw`

Do not put Docker Hub publishing credentials in `.env`; that file is loaded into local runtime containers.

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

Check whether the configured model belongs to the same provider as your auth profile. This image defaults to `codex/gpt-5.5`, which is the Codex-routed model family exposed by the installed OpenClaw Codex plugin. Override it with `OPENCLAW_DEFAULT_MODEL` or `OPENCLAW_MODEL` if your account or OpenClaw version exposes a different route.

### Token or session expired

Run the login helper again:

```bash
scripts/login-codex.sh
```

OAuth-backed sessions may expire or need refreshing.

If `openclaw models status` shows a fresh OAuth profile but agent runs still fail
with `OAuth token refresh failed` or `token_expired`, treat the OAuth route as
stale in the running Gateway. Re-auth inside the live Gateway container:

```bash
docker exec -it <container-id> openclaw models auth login --provider openai-codex --set-default
```

Then run the direct agent smoke test from the Quick Start section. If repeated live-container re-auth still fails, use API-key mode for automation.

### Slack says access is not configured

Approve the Slack pairing code shown by the bot:

```bash
docker exec -it <container-id> openclaw pairing approve slack <PAIRING_CODE>
```

Pair each human operator intentionally. Do not approve unknown Slack users.

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
