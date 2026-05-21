# Prompt Action Log

This log records implementation prompts that change the reusable ScienceClaw/OASIS template. Keep private user data, credentials, and live workspace secrets out of this file.

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
