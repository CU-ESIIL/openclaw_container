# OpenClaw Local Docker

Run an agent on your laptop, keep the workspace sandboxed, and authenticate with ChatGPT/Codex OAuth when available.

[Read the setup guide](setup.md){ .md-button .md-button--primary }
[Alpha baseline](alpha.md){ .md-button }
[Operations](operations.md){ .md-button }
[Model/auth options](model-options.md){ .md-button }

<div class="grid cards" markdown>

- **Local control**

  ---

  Build the CLI image yourself, persist config on your machine, and decide exactly which project files are mounted into `/workspace`.

- **Model options**

  ---

  Start with ChatGPT/Codex OAuth when available, or switch to API-key mode when repeatable automation matters more.

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

The full walkthrough is in the [setup guide](setup.md). The [model/auth options](model-options.md) page explains when OAuth, API keys, hosted service, or local models make sense.

Read [Security](security.md) before connecting Slack tokens to the PI Liaison.

Use the [Operations guide](operations.md) for the reproducible Slack pairing, live Gateway OAuth refresh, and smoke-test sequence.
