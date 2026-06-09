# Troubleshooting

Troubleshooting is part of reproducible scientific work. Start with checks that inspect state without deleting anything.

```bash
git status
docker compose ps
make doctor
make smoke-test
```

## Container Will Not Start

Ports may already be in use, Docker may not be running, or `.env` may contain conflicting values. Check `docker compose ps` and `docker compose logs`. Do not delete volumes until you know what they contain.

## I Cannot Find My Files

Check whether the file belongs in the repository, `/workspace`, `/data/outputs`, or `/external_storage`. Active project work normally lives in `/workspace`; large data normally lives in `/external_storage`.

## Secrets Are Not Working

Confirm `.env` exists and run `scripts/check-secrets.sh`. If tokens were changed in Slack or another provider, restart services so the new environment is loaded.

## The UI Looks Wrong

Hard refresh the browser. If branding files changed, restart the container or rerun the branding installer inside the container. The upstream OpenClaw UI is still the base interface; ScienceClaw branding is a local skin.

If this happened immediately after `openclaw update`, the update likely replaced the patched Control UI assets. Reapply the ScienceClaw branding layer for that instance, then restart the gateway. The [multi-instance runbook](instance-runbook.md) includes the exact recovery commands.

## The Browser Opened The Wrong Page

The default local stack exposes three different browser surfaces:

- `http://127.0.0.1:18789/` is the main OpenClaw chat and control UI.
- `http://127.0.0.1:8090/` is the CMS sidecar for files, reports, and GitHub repository management.
- `http://127.0.0.1:8888/lab` is JupyterLab.

If you opened `8090` expecting the chat page, switch to the Gateway URL or use the tokenized dashboard link from:

```bash
docker compose exec openclaw-local openclaw dashboard --no-open
```

That is the most reliable local browser entry point.

## Browser Says `Auth required` Or `Device pairing required`

`Auth required` means the browser reached the Gateway, but it does not yet have a matching token. Use the token-bearing URL from:

```bash
docker compose exec openclaw-local openclaw dashboard --no-open
```

`Device pairing required` means the token worked, but this browser still needs one-time approval from the Gateway host:

```bash
docker compose exec openclaw-local openclaw devices list
docker compose exec openclaw-local openclaw devices approve <REQUEST_ID>
```

Reload the chat page after approval. If the transcript itself is stuck after connecting, start one fresh chat session before assuming the Gateway is down.

## Agent Dropdown Is Missing

The working-group template should show 11 agents, with `main` named PI Liaison. If the dropdown only shows `main`, the new instance did not load the full agent registry.

Check from the gateway container:

```bash
docker exec <gateway-container> openclaw agents list
```

Do not copy an entire OpenClaw state directory from another instance. Preserve the instance's own gateway token, port, allowed origins, sessions, and project workspace. Restore only the agent registry and related defaults. The [multi-instance runbook](instance-runbook.md) has the full validation and repair path.

## Agent Stops Responding With Session-Lock Errors

If logs show:

```text
session file changed while embedded prompt lock was released
```

stop sending prompts into that transcript. Inspect tasks and sessions, then archive the failed `agent:main:main` transcript rather than deleting all OpenClaw state.

```bash
docker exec <gateway-container> openclaw tasks list --json
docker exec <gateway-container> openclaw sessions --agent main --json
docker logs --tail 120 <gateway-container>
```

For smoke tests, use an explicit session id such as `instance-smoke-$(date +%s)`. Do not test against the same browser transcript that is open in the UI.

## I Restarted And Lost Something

The container filesystem is ephemeral. Check git, mounted workspace folders, named Docker volumes, `/data`, and `/external_storage`. If a file existed only inside the container runtime and was not mounted, it may not persist.

## I Think I Broke It

Run `git status`, make a checkpoint, and avoid destructive commands. Most template mistakes are recoverable if secrets were not committed and important work was saved to a durable location.
