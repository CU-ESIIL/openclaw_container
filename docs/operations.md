# Operations Guide

This page documents the reproducible operating path for the OpenClaw scientific working group container with Slack Socket Mode and ChatGPT/Codex OAuth.

The working deployment has four separate gates:

1. Docker starts the OpenClaw Gateway.
2. Slack Socket Mode connects to the Gateway.
3. The Slack user is paired and approved.
4. The Gateway has a fresh model login for `openai-codex`.

Treat these as separate checks. A failure in one layer can look like a silent Slack failure from the user's perspective.

## Start the Gateway

Create a local `.env` from `.env.example`, add Slack tokens, and validate them:

```bash
cp .env.example .env
scripts/check-secrets.sh
```

Start the long-running Gateway container:

```bash
scripts/start-gateway.sh
```

The script prints a Docker container id. Keep that id for diagnostics. You can also rediscover it:

```bash
docker ps --filter name=openclaw
```

## Verify Slack

Probe Slack Socket Mode from inside the running container:

```bash
docker exec <container-id> openclaw channels status --channel slack --probe --timeout 20000
```

A healthy Slack connection should report that the Slack provider is enabled, configured, running, connected, and healthy.

## Pair a Slack User

The first time a Slack user talks to the app, OpenClaw may reply with "access not configured" and a pairing code.

Approve that user inside the running Gateway container:

```bash
docker exec -it <container-id> openclaw pairing approve slack <PAIRING_CODE>
```

This approval is stored in the persisted OpenClaw config mount under `~/.openclaw`. Pair each human operator explicitly. Do not approve unknown users or broad groups without review.

## Refresh Codex OAuth in the Live Gateway

For Slack replies, re-authenticate in the same running Gateway container that Slack is using:

```bash
docker exec -it <container-id> openclaw models auth login --provider openai-codex --set-default
```

Open the OAuth URL in your local browser. After sign-in, paste the full `localhost:1455/auth/callback?...` redirect URL back into the terminal prompt.

Then verify model auth:

```bash
docker exec <container-id> openclaw models status
```

Healthy Codex OAuth status should show the `openai-codex` profile and may show usage/quota information. If status only says the profile expires later but agent calls still return `token_expired`, rerun the login inside the live Gateway container.

## Smoke Test the Agent

Before testing Slack, run a direct agent reply check:

```bash
docker exec <container-id> openclaw agent --session-id slack-ready-check --message 'Reply with exactly: PI Liaison ready' --timeout 120
```

Expected output:

```text
PI Liaison ready
```

Then test in Slack:

```text
@Science_advisory_team hi
```

## Common Failure Modes

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| Slack says `access not configured` | Slack user is not paired | Run `openclaw pairing approve slack <PAIRING_CODE>` inside the Gateway container |
| Slack provider is not connected | Socket Mode token, bot token, channel, or Slack app setup is wrong | Run `scripts/check-secrets.sh`, check Socket Mode, app-level token, bot membership, and event subscriptions |
| Slack replies with `Model login expired` | Gateway cannot refresh Codex OAuth | Run `openclaw models auth login --provider openai-codex --set-default` inside the live Gateway container |
| Direct agent test fails with `token_expired` | OAuth metadata exists but backend refresh is rejected | Re-auth in the live Gateway container; restart Gateway only after confirming the profile works |
| Direct messages show "Sending messages to this app has been turned off" | Slack App Home messages are disabled | Enable the App Home Messages tab and reinstall the Slack app |

## Scaling Notes

Use one narrowly mounted `workspace/` per scientific working group or project. Avoid mounting the user's whole home directory. The source scaffold lives in `docker/seed-workspace`; runtime notes and project files live in the mounted `workspace/`.

For multiple Slack channels, prefer explicit channel ids in `.env` or deployment-specific environment files. Use a stable value such as `channel:C0123456789` when supported, because channel names can change.

For multiple users, approve each Slack sender intentionally and document who is allowed to operate the Liaison. Slack should remain the PI Liaison interface, not a direct execution surface for every agent.

For multiple deployments, keep secrets out of images and git. Build the same image, provide different `.env` files or deployment secrets, and keep each deployment's `~/.openclaw` state separate.

For long-running use, expect occasional OAuth refresh. The reproducible recovery path is live-container re-auth, Slack health probe, model status, direct agent smoke test, then Slack test.
