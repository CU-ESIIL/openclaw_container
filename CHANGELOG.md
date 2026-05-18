# Changelog

## 0.1.0-alpha.1 - 2026-05-17

First alpha baseline for the OpenClaw scientific working group container.

### Added

- Reproducible `/workspace` seed under `docker/seed-workspace`.
- Eleven bounded working-group roles, including the PI Liaison / User Interview Agent as the default human-facing role.
- Project memory, intake, charter, team brief, initial tasks, human-review, assumption, decision, and question-queue files.
- PI Liaison startup prompt and startup script.
- Slack credential handling through local `.env` variables, with masked validation.
- Environment-backed Slack channel registration at container startup.
- Security documentation for Slack tokens and token rotation.
- Operations documentation for Slack Socket Mode, Slack user pairing, live Gateway Codex OAuth refresh, and direct agent smoke tests.
- Role-based model routing documentation and seeded `MODEL_ASSIGNMENTS.md` for open-model API experiments.
- Curated example snapshot area, including an urban wildlife corridors project capture from a live working-group run.
- Seeded template governance package: team norms, decision protocol, memory quarantine, artifact registry, societal impact checklist, meeting template, data directories, and role reproducibility notes.
- ScienceClaw `/data` layout, optional JupyterLab workspace UI, baseline scientific shell tools, document conversion examples, and brand assets.
- ScienceClaw documentation page with ESIIL-informed palette and workspace architecture notes.
- Smoke tests for working-group scaffold and secret validation.

### Notes

- Real Slack tokens, OpenAI keys, and local runtime state are intentionally excluded from git.
- Users should start from `.env.example`, create a local `.env`, invite the Slack bot to a channel, and use a `channel:<id>` target when possible.
