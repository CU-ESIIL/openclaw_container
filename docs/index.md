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

</div>

## Start Here

```bash
docker compose build
scripts/login-codex.sh
scripts/status.sh
```

The full walkthrough is in the [README](README.md). The [pricing comparison](pricing.md) explains when OAuth, API keys, hosted service, or local models make sense.
