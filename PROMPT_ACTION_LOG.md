# Prompt Action Log

This log records implementation prompts that change the reusable ScienceClaw/OASIS template. Keep private user data, credentials, and live workspace secrets out of this file.

## 2026-05-22 - Gateway 3 Reproducible Container Rebuild

### Prompt Summary

Reassess gateway 3 after the update banner was hidden but browser chat still failed. The user asked for a robust container shape: branded OpenClaw, file-structure visibility for produced content, and GitHub repository read/write capability.

### Files Changed

- `Dockerfile`
- `docker-compose.yml`
- `docker/service-entrypoint.sh`
- `docs/instance-runbook.md`
- `docs/operations.md`

### Architectural Decisions

- Pin the reusable image to OpenClaw `2026.5.18`, the current known-good local browser-chat baseline.
- Keep only the Gateway service responsible for OpenClaw startup, OpenClaw state, Slack registration, branding injection, agent registry, and sessions.
- Start JupyterLab without the OpenClaw Gateway entrypoint so it cannot mutate Gateway config or sessions.
- Start the CMS through a small service entrypoint that only loads GitHub secret files, mirrors `GITHUB_TOKEN`/`GH_TOKEN`, configures GitHub CLI credential helpers, and marks workspace repositories as safe directories.
- Preserve the file manager and GitHub repository manager as CMS features over the shared `/workspace`, not as OpenClaw session writers.

### Tests Run

- `bash -n docker/entrypoint.sh docker/service-entrypoint.sh scripts/start-instance.sh scripts/install-control-ui-branding.sh`
- `docker compose config --quiet`
- `docker compose build openclaw-local`
- Restarted gateway 3 with `OPENCLAW_STATE_DIR=/private/tmp/scienceclaw-project-three-openclaw ./scripts/start-instance.sh project-three 18791 8890 8092`.
- Verified rebuilt gateway 3 reports `OpenClaw 2026.5.18`.
- Verified gateway 3 has 11 agents with `openclaw agents list`.
- Verified direct agent smoke test returned `PINNED_OK`.
- Verified CMS file API returns the `/workspace` listing.
- Verified CMS GitHub status endpoint is reachable and reports unauthenticated when no GitHub token is present.
- Archived the poisoned `agent:main:gateway3-fixed` session and moved the browser to a fresh dashboard session.

### Known Limitations

- GitHub repository operations still require a `GITHUB_TOKEN`, `GH_TOKEN`, or interactive `gh auth login` inside the CMS service.
- The update notice can still appear in CLI status because a newer upstream OpenClaw package exists; local ScienceClaw upgrades remain a pinned-image rebuild workflow.
- Browser text-entry automation was blocked by the in-app browser clipboard layer, so the browser path was validated by connection/session state plus direct OpenClaw smoke tests rather than an automated typed UI prompt.

## 2026-05-22 - Gateway 3 Fresh Diagnosis and Verde Tool Profile Repair

### Prompt Summary

Reinspect gateways 1, 2, and 3 after gateway 3 continued failing to reply. Gateway 1 and 2 were running the older image and OpenClaw `2026.5.18`; gateway 3 was on the newer local image, also OpenClaw `2026.5.18`, but direct agent smoke tests failed with `session file changed while embedded prompt lock was released`.

### Files Changed

- `.env.example`
- `README.md`
- `docker/entrypoint.sh`
- `docs/instance-runbook.md`
- `docs/security-and-credentials.md`
- `scripts/start-instance.sh`

### Architectural Decisions

- Keep the AI-VERDE/OpenAI-compatible route on a minimal OpenClaw tool profile for the default ScienceClaw gateway path.
- Preserve automatic visible replies instead of the experimental `message_tool` reply mode for the local working-group template.
- Set `models.mode` to `merge` during bootstrap so provider additions do not replace working defaults.
- Keep gateway 3 heartbeat disabled for now; the direct smoke failure was reproduced without relying on heartbeat activity, so heartbeat is not the only root cause.
- Keep per-instance OpenClaw runtime state on local non-synced storage (`/private/tmp/scienceclaw-<instance>-openclaw`) while leaving the project workspace under `instances/<name>/workspace`.
- Treat GitHub Secrets as the scalable credential source, materialized into runner-local secret files and passed through provider `_FILE` variables.

### Tests Run

- Compared gateway 1, 2, and 3 with `docker ps`, `openclaw --version`, `openclaw status`, and `openclaw agents list`.
- Confirmed gateway 2 passed: `openclaw agent --agent main --session-id gateway2-fresh-codex-smoke-20260522a --model verde/js2/gpt-oss-120b --message "Reply with exactly: OK" --timeout 120 --json`.
- Confirmed gateway 3 failed before repair on fresh explicit sessions, while the session JSONL still contained the assistant reply.
- Patched gateway 3 runtime config to match gateway 2's `models.mode`, visible reply mode, and minimal Verde tool profile.
- Confirmed gateway 3 passed after repair: `openclaw agent --agent main --session-id gateway3-fresh-codex-smoke-20260522c --model verde/js2/gpt-oss-120b --message "Reply with exactly: OK" --timeout 120 --json`.
- Restarted gateway 3 with OpenClaw state mounted from `/private/tmp/scienceclaw-project-three-openclaw`.
- Confirmed gateway 3 browser chat replied with `G3_UI_OK`.

### Known Limitations

- Gateway 3's currently running container was repaired through its mounted runtime config. Rebuild/recreate from the updated image is still needed to prove the reusable entrypoint fix from a clean start.
- Heartbeats remain disabled on gateway 3 until a safe heartbeat session strategy is designed and tested.
- GitHub Secrets are documented as the intended scalable source, but a production deployment workflow still needs a target runtime choice such as self-hosted runner, Codespaces, Kubernetes, or another host.

## 2026-05-22 - Multi-Instance Gateway Recovery Runbook

### Prompt Summary

Document the repeated gateway setup problem observed while spawning additional ScienceClaw instances: missing agent dropdowns, one-agent OpenClaw state, stale or locked `agent:main:main` sessions, confusing update banners, and uncertainty about whether GitHub or the Gateway caused the failure.

### Files Changed

- `docs/instance-runbook.md`
- `docs/use/launch-locally.md`
- `docs/troubleshooting.md`
- `docs/operations.md`
- `scripts/start-instance.sh`
- `mkdocs.yml`

### Architectural Decisions

- Treat each spawned ScienceClaw instance as a separate appliance with its own Gateway, OpenClaw state, workspace, data root, external storage, JupyterLab port, and CMS port.
- Validate a new instance before project work by checking OpenClaw version, status, agent registry, sessions, and a dedicated smoke-test session.
- Use unique smoke-test session ids. Do not run CLI smoke tests against the browser's active `agent:main:main` transcript.
- If a session-lock error appears, archive the failed transcript instead of deleting the whole OpenClaw state directory.
- If an instance only has `main`, restore the agent registry without copying another instance's token, port, allowed origins, sessions, or project workspace.
- After a live `openclaw update`, reapply the ScienceClaw Control UI branding layer because upstream package updates replace the patched Control UI asset directory.

### Tests Run

- Documentation and script edits only in this action.
- Earlier operational diagnosis used `openclaw status`, `openclaw agents list`, `openclaw sessions --agent main --json`, `openclaw tasks list --json`, `docker logs`, and direct `openclaw agent` smoke tests.

### Known Limitations

- The root OpenClaw session-lock behavior is upstream/runtime behavior, not fully controlled by this repository.
- The runbook documents recovery and prevention. It does not add a fully automated repair command.
- OpenClaw update banners should be interpreted cautiously; version changes must be validated per instance, and ScienceClaw branding may need to be reapplied after live updates.

### Unresolved Issues

- Decide whether `scripts/start-instance.sh` should eventually run the validation checks automatically and fail fast if the 11-agent registry is missing.
- Consider adding a dedicated `scripts/validate-instance.sh` helper once the OpenClaw CLI behavior stabilizes.

## 2026-05-20 - Next Phase Stabilization

### Prompt Summary

Stabilize the feature-rich OpenClaw container prototype into a documented, reusable OASIS ScienceClaw working-group appliance. Emphasis: onboarding clarity, architecture communication, one end-to-end workflow, smoke tests, operational commands, reproducibility, and human trust.

### Files Changed

- `README.md`
- `Makefile`
- `scripts/demo_environmental_workflow.py`
- `scripts/smoke_test.sh`
- `docs/quick-start.md`
- `docs/architecture.md`
- `docs/storage-model.md`
- `docs/agent-team.md`
- `docs/cms-output-review.md`
- `docs/slack-integration.md`
- `docs/kubernetes-workers.md`
- `docs/security-and-credentials.md`
- `docs/troubleshooting.md`
- `mkdocs.yml`
- `CHANGELOG.md`

### Architectural Decisions

- Keep the README as a concise front door and move long-form explanation into MkDocs pages.
- Establish `make demo` and `make smoke-test` as the stable operational proof path.
- Use a deterministic synthetic environmental workflow rather than network data or API keys.
- Keep Kubernetes and Slack documented as optional or experimental surfaces.
- Preserve the PI Liaison, human-review, CMS/output review, and three-zone storage models.

### Tests Run

- `bash -n` on new shell scripts.
- `make help`.
- `make demo`.
- `make smoke-test`.
- `scripts/test-scienceclaw-layout.sh`.
- `make doctor`.
- `make checkpoint`.
- Local markdown link checks.

### Known Limitations

- Host Python may not include the full geospatial stack; `make smoke-test` reports that as a warning outside the container while still validating the deterministic demo workflow.
- MkDocs build requires MkDocs dependencies to be installed in the current environment or run inside an environment with `requirements.txt`.
- The demo workflow is operational proof only and should not be interpreted as a scientific model.

### Unresolved Issues

- CI should eventually run `make smoke-test` inside the built container image to validate the full geospatial stack.
- Additional screenshots and polished diagrams can be added after the documentation structure settles.

## 2026-05-20 - Workspace File Manager

### Prompt Summary

Add a clean, integrated workspace file manager so ScienceClaw users can browse the container, inspect `/workspace`, preview outputs, edit safe text files, and understand what agents created without switching to a separate notebook interface.

### Files Changed

- `cms/scienceclaw_cms.py`
- `Dockerfile`
- `docker/entrypoint.sh`
- `branding/control-ui/scienceclaw-brand.js`
- `branding/control-ui/scienceclaw-brand.css`
- `scripts/install-control-ui-branding.sh`
- `scripts/seed_file_manager_demo.py`
- `scripts/smoke_test_workspace.sh`
- `scripts/smoke_test.sh`
- `Makefile`
- `README.md`
- `docs/quick-start.md`
- `docs/architecture.md`
- `docs/workspace-file-manager.md`
- `docs/workspace-cms.md`
- `mkdocs.yml`

### Architectural Decisions

- Extend the existing lightweight CMS service instead of introducing a second file-management framework.
- Use `/` as the visual browsing root while failing closed around sensitive files and directories.
- Restrict browser write operations to safe roots such as `/workspace`, `/data/outputs`, and `/tmp`.
- Add an OpenClaw sidebar Files link that opens the file manager for the matching ScienceClaw instance.
- Seed a tiny demo workspace at startup unless `SCIENCECLAW_SEED_FILE_MANAGER_DEMO=0` is set.
- Keep JupyterLab as the advanced analytics interface; the file manager is for inspection, output review, and small edits.

### Tests Run

- `python3 -m py_compile cms/scienceclaw_cms.py scripts/seed_file_manager_demo.py scripts/demo_environmental_workflow.py`
- `bash -n scripts/smoke_test_workspace.sh`
- `bash -n scripts/smoke_test.sh`
- `scripts/smoke_test_workspace.sh`
- `make smoke-test`
- `git diff --check`

### Known Limitations

- The Files link opens the CMS file manager route on the CMS port rather than reverse-proxying the route through the OpenClaw gateway.
- The Markdown renderer is intentionally lightweight and designed for inspection, not full static-site rendering parity.
- Browser-side drag-and-drop upload is not yet implemented; standard file upload is supported.

### Recommended Next Steps

- Add a reverse proxy route if OpenClaw exposes a stable extension point for embedding `/files` under the gateway origin.
- Add optional richer previews for Parquet, GeoJSON, rasters, and notebooks after the core file workflow is stable.

## 2026-05-20 - GitHub Repository Manager

### Prompt Summary

Add a dedicated GitHub manager so ScienceClaw/OpenClaw users can authorize selected external project repositories, clone them into the workspace, inspect branch status, and follow a branch-and-pull-request contribution workflow without granting agents broad account-wide GitHub access.

### Files Changed

- `.env.example`
- `Makefile`
- `README.md`
- `branding/control-ui/scienceclaw-brand.css`
- `branding/control-ui/scienceclaw-brand.js`
- `cms/scienceclaw_cms.py`
- `docs/architecture.md`
- `docs/github-repository-manager.md`
- `docs/quick-start.md`
- `docs/workspace-cms.md`
- `mkdocs.yml`
- `scripts/smoke_test.sh`
- `scripts/smoke_test_github_manager.sh`

### Auth Model Chosen

The first implementation supports GitHub CLI authentication with `gh auth login` and `gh auth setup-git`, plus optional fine-grained `GITHUB_TOKEN` injection through local secrets. GitHub App authentication is documented as the preferred long-term approach but is not required for this first version.

### Implementation Strategy

- Store authorized repositories in `/workspace/.openclaw-github/authorized-repos.yaml`.
- Clone repositories only under `/workspace/repos/`.
- Implement `read`, `contribute`, and visible-but-disabled `admin` permission tiers.
- Use argument-array `git` and `gh` invocations for narrow operations.
- Block direct writes and pushes on `main` and `master`.
- Add a branded GitHub link beside Files in the OpenClaw sidebar.

### Tests Run

- `python3 -m py_compile cms/scienceclaw_cms.py scripts/seed_file_manager_demo.py scripts/demo_environmental_workflow.py`
- `bash -n scripts/smoke_test_github_manager.sh scripts/smoke_test_workspace.sh scripts/smoke_test.sh docker/entrypoint.sh`
- `scripts/smoke_test_github_manager.sh`
- `make smoke-test`
- `git diff --check`

### Known Limitations

- The GitHub manager opens on the CMS port rather than being reverse-proxied under the OpenClaw gateway origin.
- Authenticated remote operations require valid GitHub credentials and are not exercised by unauthenticated smoke tests.
- GitHub App authentication, automatic issue management, review UI, and merge automation are not implemented.

### Recommended Next Steps

- Add optional GitHub App installation support for selected repositories.
- Add richer PR status display once authenticated integration tests are available.
- Add an optional prompt/action-log append helper for connected repositories that already use `PROMPT_ACTION_LOG.md`.

## 2026-05-21 - Secret-Backed GitHub Agent Access

### Prompt Summary

Make the desired deployment experience explicit: a user can pull or build the ScienceClaw container, provide credentials through local secrets, and start a working group whose agents and GitHub manager can operate on selected organization repositories.

### Files Changed

- `.env.example`
- `README.md`
- `docker-compose.secrets.yml`
- `docker/entrypoint.sh`
- `docs/github-repository-manager.md`
- `docs/quick-start.md`
- `docs/security-and-credentials.md`

### Architectural Decisions

- Support `_FILE` secret variables for Slack, OpenAI, AI-VERDE, GitHub, and Tavily credentials.
- Mirror `GITHUB_TOKEN` and `GH_TOKEN` at startup so GitHub CLI and standard tooling can use the same secret.
- Configure GitHub CLI/git credential helpers during container startup when a GitHub token is present.
- Keep repository access bounded by the GitHub manager allowlist and `/workspace/repos/` clone root.

### Tests Run

- `bash -n docker/entrypoint.sh`
- `docker compose -f docker-compose.yml -f docker-compose.secrets.yml config`

### Known Limitations

- The current local containers must be rebuilt or recreated to pick up entrypoint changes.
- Fine-grained GitHub tokens still need the correct repository scopes from GitHub; ScienceClaw cannot grant missing organization permissions.
- GitHub App installation remains the preferred long-term organization-scale auth model.

## 2026-05-21 - Gateway 3 Session-Lock Recovery

### Prompt Summary

Recover the third local ScienceClaw gateway after repeated OpenClaw browser-chat failures with `session file changed while embedded prompt lock was released`.

### Files Changed

- `docs/instance-runbook.md`

### Architectural Decisions

- Treat OpenClaw `2026.5.18` as the current known-good local baseline because gateway 2 remained stable on that version.
- Treat OpenClaw `2026.5.20` as unvalidated for the branded multi-instance template after gateway 3 repeatedly failed browser sessions on that version.
- Preserve runtime work by archiving failed session transcripts instead of deleting the full OpenClaw state directory.
- Disable the default PI Liaison heartbeat for gateway 3 by setting the `main` agent heartbeat interval to an empty string; the 30-minute default heartbeat was repeatedly touching `agent:main:main` and recreating the lock failure.

### Tests Run

- `docker exec scienceclaw-project-three-openclaw-local-run-add2042ee2e3 openclaw --version`
- `docker exec scienceclaw-project-three-openclaw-local-run-add2042ee2e3 openclaw status`
- `docker exec scienceclaw-project-three-openclaw-local-run-add2042ee2e3 openclaw agent --agent main --session-id gateway3-518-smoke-... --model verde/js2/gpt-oss-120b --message "Reply with exactly: OK" --timeout 120 --json`
- `docker exec scienceclaw-project-three-openclaw-local-run-add2042ee2e3 openclaw agent --agent main --session-id gateway3-final-smoke-... --model verde/js2/gpt-oss-120b --message "Reply with exactly: OK" --timeout 120 --json`

### Known Limitations

- The browser UI still needs a fresh session after recovery; old tabs can hold stale session state.
- The update banner will still appear because `2026.5.20` exists upstream, but updating the active gateway should wait until a browser-session smoke test validates the newer release.
