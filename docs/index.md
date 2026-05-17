# OpenClaw Local Docker

Run an agent on your laptop, keep the workspace sandboxed, and authenticate with ChatGPT/Codex OAuth when available.

[Read the setup guide](README.md){ .md-button .md-button--primary }
[Compare options](pricing.md){ .md-button }

<div class="grid cards" markdown>

- **Local control**

  ---

  Build the CLI image yourself, persist config on your machine, and decide exactly which project files are mounted into `/workspace`.

- **Subscription login**

  ---

  Use ChatGPT/Codex OAuth when your OpenClaw version, account, quota, and provider policy support it.

- **Safe workspace**

  ---

  Keep agent access focused on `./workspace` instead of exposing your whole home directory or unrelated cloud folders.

- **Bootstrapped defaults**

  ---

  Start with the local Gateway, Control UI origins, Codex model route, and starter heartbeat/soul workspace files already initialized by the image.

- **Scientific working group**

  ---

  Use an 11-role environmental data science scaffold with a PI Liaison, shared memory, evidence standards, skeptic review, and human approval gates.

</div>

## Start Here

```bash
docker compose build
scripts/login-codex.sh
scripts/status.sh
```

The full walkthrough is in the [README](README.md). The [pricing comparison](pricing.md) explains when OAuth, API keys, hosted service, or local models make sense.

Read [Security](security.md) before connecting Slack tokens to the PI Liaison.
