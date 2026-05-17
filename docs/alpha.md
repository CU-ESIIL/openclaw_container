# Alpha Baseline

Version `0.1.0-alpha.1` is the first reproducible OpenClaw scientific working group baseline for this repository.

The default container image seeds `/workspace` with the scientific working group structure, PI Liaison workflow, bounded agent role definitions, project memory files, intake documents, and human-review rules. Users should not need to recreate the agent setup manually after launching the container.

Slack credentials are not part of the image or git history. The image expects local environment-backed credentials from `.env`, registers the Slack channel with OpenClaw using `--use-env`, and validates required Slack variables before the PI Liaison starts.

## Reproduce the Alpha

```bash
cp .env.example .env
scripts/check-secrets.sh
docker compose build
scripts/start.sh
```

For a long-running Gateway service:

```bash
scripts/start-gateway.sh
```

## What Is Included

- Eleven role definitions in `AGENTS.md`.
- PI Liaison startup prompt in `prompts/pi-liaison-startup.md`.
- Working-group memory files: `MEMORY.md`, `ROADMAP.md`, `DECISIONS.md`, `ASSUMPTIONS.md`, and `HUMAN_REVIEW.md`.
- Intake and routing files: `PROJECT_INTAKE.md`, `PROJECT_CHARTER.md`, `TEAM_BRIEF.md`, `INITIAL_TASKS.md`, `QUESTIONS_FOR_USER.md`, and `USER_CONTEXT.md`.
- Directory READMEs for documents, analysis, figures, literature, meetings, daily notes, agent reports, logs, heartbeat, soul, prompts, services, and scripts.
- Slack secret validation and masking helpers.

## What Is Not Included

- Real Slack tokens.
- Real OpenAI API keys.
- User-specific OpenClaw auth profiles.
- Runtime logs, generated drafts, project outputs, or private workspace memory.
