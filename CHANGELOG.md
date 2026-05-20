# Changelog

## 0.1.0-alpha.1 - 2026-05-17

First alpha baseline for the OpenClaw scientific working group container.

### Added

- OASIS ScienceClaw template mode with durable Control UI branding, a current-working-group banner, canonical working-group configuration, cockpit orientation, checkpoint, consensus, and contribution files.
- Canonical seeded workspace folders for datasets, outputs, maps, reports, manuscripts, presentations, notebooks, tasks, reviews, decisions, assumptions, runtime notes, cache, and config.
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
- Bounded distributed spatial-temporal runtime scaffold with a local worker path, optional Kubernetes manifests, STAC/COG/Zarr examples, output indexing, and job metadata conventions.
- Three-zone repository/workspace/external-storage architecture, including `/external_storage/local` support.
- Lightweight file-backed workspace CMS for reviewing private artifacts and promoting approved pages/assets into the MkDocs public site.
- Storage registry templates, provider profiles, schema, and safe helper commands for local, STAC, COG, S3-compatible, WebDAV, iRODS, and OSN-style storage patterns.
- Public publishing workflow docs, sample promoted report, and sample metadata-only dashboard pattern.
- Continuous improvement protocol, starter log, and role review template seeded into the working group scaffold.
- Pre-remodel capture audit notes for separating reusable template changes from private workspace/project artifacts.
- Lean Pandoc PDF toolchain added to the image with LaTeX packages needed for manuscript-style PDF exports.
- Smoke tests for working-group scaffold and secret validation.

### Notes

- Real Slack tokens, OpenAI keys, and local runtime state are intentionally excluded from git.
- Users should start from `.env.example`, create a local `.env`, invite the Slack bot to a channel, and use a `channel:<id>` target when possible.
