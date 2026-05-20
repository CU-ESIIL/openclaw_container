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

## I Restarted And Lost Something

The container filesystem is ephemeral. Check git, mounted workspace folders, named Docker volumes, `/data`, and `/external_storage`. If a file existed only inside the container runtime and was not mounted, it may not persist.

## I Think I Broke It

Run `git status`, make a checkpoint, and avoid destructive commands. Most template mistakes are recoverable if secrets were not committed and important work was saved to a durable location.

