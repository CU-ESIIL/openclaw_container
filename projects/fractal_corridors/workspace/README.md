# Environmental Data Science Working Group

This `/workspace` directory is the persistent scientific working area for OpenClaw inside the container. It is designed to behave like a small environmental data science synthesis center: bounded roles, shared memory, reproducible analysis, documented assumptions, explicit disagreement, and human review.

## Start Here

1. Start with the PI Liaison interview in `PROJECT_INTAKE.md`.
2. Draft or review `PROJECT_CHARTER.md`.
3. Let the PI Liaison create `TEAM_BRIEF.md` and `INITIAL_TASKS.md`.
4. Record initial assumptions in `ASSUMPTIONS.md`.
5. Use `ROADMAP.md` to choose the current project phase.
6. Put literature and citation notes in `literature/`.
7. Put reproducible scripts in `scripts/` and analysis outputs in `analysis/`.
8. Put figures in `figures/`, with notes linking each figure to scripts and data sources.
9. Require Skeptic review before promoting major claims.
10. Use `HUMAN_REVIEW.md` before any external, destructive, expensive, or sensitive action.

## Directory Map

- `documents/` - charters, reports, manuscripts, memos, and synthesis drafts
- `analysis/` - reproducible analysis outputs and notebooks
- `figures/` - generated figures and figure provenance notes
- `literature/` - papers, source notes, citation inventories, and evidence tables
- `meetings/` - agendas, minutes, and action items
- `daily_notes/` - dated working notes
- `agent_reports/` - role-specific memos, reviews, and handoff notes
- `logs/` - user-requested logs or summaries
- `heartbeat/` - periodic check notes and lightweight reminders
- `soul/` - role tone, continuity, and working norms
- `prompts/` - startup prompts and role-specific prompt templates
- `scripts/` - initialization, checks, reproducible workflows, and utilities

## PI Liaison

The PI Liaison / User Interview Agent is the default human-facing role. Other agents should file questions in `QUESTIONS_FOR_USER.md` instead of interrupting the user directly. The PI Liaison deduplicates those questions, asks only the highest-value followups, and returns milestone reports or drafts to the user for review.

## Security Notes

Do not treat agents as safe just because the workspace is structured. Third-party skills, broad filesystem mounts, autonomous shell access, external APIs, and credentials all require careful review. Keep the mounted workspace narrow; do not mount the whole home directory.
