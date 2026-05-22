# Gateway 3 Handoff

Last updated: 2026-05-22 15:14 MDT

This note captures the current state of gateway 3 after the rebuild and the remaining work for the next session.

## Current Goal

Build a robust, reproducible ScienceClaw/OpenClaw container with:

- branded OpenClaw Control UI
- reliable PI Liaison chat
- browsable project file structure and outputs
- GitHub repository read/write workflow for authorized project repositories
- scalable credential injection through environment variables, secret files, and eventually GitHub Secrets

## What Was Wrong

Gateway 3 had accumulated too many moving parts at once. The most important finding was that the workspace CMS and Jupyter services were using the full OpenClaw gateway entrypoint. That meant non-gateway services could run workspace seeding, branding installation, GitHub/Slack setup, and OpenClaw bootstrap logic even though only the Gateway should own OpenClaw runtime state.

Separately, the active browser transcript `agent:main:gateway3-fixed` was poisoned by repeated Verde `reasoning-only assistant turn` failures. Fresh direct CLI sessions worked, but the browser kept reusing that bad transcript.

The update banner was not the main problem. It was an upstream OpenClaw package notice for `2026.5.20`; the local Docker dashboard update path cannot complete the managed-service handoff. The banner was suppressed in the ScienceClaw branding layer, but the real stabilization was the container/service split and version pin.

## Changes Made

- Pinned the Docker image to OpenClaw `2026.5.18` with `ARG OPENCLAW_VERSION=2026.5.18` in `Dockerfile`.
- Added `docker/service-entrypoint.sh` for non-gateway services.
- Updated `docker-compose.yml` so:
  - `openclaw-local` uses the full OpenClaw gateway entrypoint and owns OpenClaw state.
  - `workspace-cms` uses the lightweight service entrypoint and only serves files/GitHub manager.
  - `workspace-ui` bypasses the OpenClaw entrypoint and runs JupyterLab directly.
- Rebuilt `openclaw-local`.
- Restarted gateway 3 on port `18791`, workspace UI on `8890`, CMS on `8092`.
- Reapplied ScienceClaw branding and suppressed unsupported updater notices.
- Moved the browser to a fresh dashboard session.
- Removed the active `agent:main:gateway3-fixed` registry key and archived its session files under:

```text
/private/tmp/scienceclaw-project-three-openclaw/agents/main/sessions/archived-20260522-pinned-rebuild/
```

## Current Live Links

```text
Gateway 3 chat:
http://127.0.0.1:18791/chat?session=agent%3Amain%3Adashboard%3A53fdac2b-ddd7-4eed-860c-ea527110ff03

Workspace UI:
http://127.0.0.1:8890/lab?token=scienceclaw

Workspace CMS:
http://127.0.0.1:8092

Files:
http://127.0.0.1:8092/files?path=/workspace

GitHub manager:
http://127.0.0.1:8092/github
```

## Current Validation

Passing checks:

```bash
bash -n docker/entrypoint.sh docker/service-entrypoint.sh scripts/start-instance.sh scripts/install-control-ui-branding.sh
docker compose config --quiet
git diff --check
docker exec scienceclaw-project-three-openclaw-local-run-96075a70e8ae openclaw --version
docker exec scienceclaw-project-three-openclaw-local-run-96075a70e8ae openclaw agents list
docker exec scienceclaw-project-three-openclaw-local-run-96075a70e8ae openclaw agent --agent main --session-id gateway3-pinned-smoke-20260522 --model verde/js2/gpt-oss-120b --message 'Reply with exactly: PINNED_OK' --timeout 120 --json
curl -fsS 'http://127.0.0.1:8092/api/file/list?path=/workspace'
curl -fsS 'http://127.0.0.1:8092/api/github/status'
```

Observed results:

- OpenClaw version is `2026.5.18`.
- 11 ScienceClaw agents are present.
- Direct PI Liaison smoke test returned `PINNED_OK`.
- CMS file API returns the shared `/workspace` listing.
- CMS GitHub status endpoint works, but reports unauthenticated without a token.
- Heartbeats are disabled on gateway 3.
- CLI status still reports an available upstream update to `2026.5.20`; this is expected and should not be handled through the dashboard.

## Remaining Work

1. Verify browser chat manually in the fresh session.
2. Decide whether the PI Liaison should stay on Verde or move to a higher-reliability Codex/OAuth route.
3. Re-authenticate Codex inside the live gateway if using `codex/gpt-5.5`:

```bash
docker exec -it scienceclaw-project-three-openclaw-local-run-96075a70e8ae openclaw models auth login --provider openai-codex --set-default
docker exec scienceclaw-project-three-openclaw-local-run-96075a70e8ae openclaw models status
```

4. Authenticate GitHub for the CMS/GitHub manager:

```bash
docker exec -it scienceclaw-project-three-workspace-cms-1 gh auth login
docker exec scienceclaw-project-three-workspace-cms-1 gh auth setup-git
```

or provide a fine-grained token through `GITHUB_TOKEN`, `GH_TOKEN`, or mounted `_FILE` variables.

5. Test the GitHub manager end to end:
   - authorize `CU-ESIIL/WUI_boundary`
   - clone or fetch
   - create an agent branch
   - edit a safe file in `/workspace/repos/...`
   - commit
   - push
   - open a PR

6. Decide the scalable GitHub Secrets workflow:
   - GitHub Actions self-hosted runner
   - Codespaces/devcontainer
   - Docker host pulling secrets from Actions into local secret files
   - Kubernetes/other orchestrator

7. Add an automated instance validator script, probably `scripts/validate-instance.sh`, covering:
   - version
   - gateway reachability
   - 11-agent registry
   - heartbeat state
   - direct smoke test on a fresh session id
   - CMS file API
   - GitHub manager status

8. Consider adding a safe session archive helper instead of manually editing `sessions.json`.

## Cautions

- Do not reuse `gateway3-fixed`; that session was the bad browser transcript.
- Do not click the dashboard update button for local Docker gateways.
- Do not allow CMS or Jupyter services to mount or mutate OpenClaw state.
- Do not print tokens, OAuth callback codes, Slack tokens, GitHub tokens, or model API keys in docs or logs.
- Treat `openclaw@2026.5.18` as the current known-good local baseline until a newer version passes browser chat validation.
