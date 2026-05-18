# TOOLS.md - Local Tool Notes

Use this file to document local, non-secret tool details for a deployment.

Do not store credentials, API keys, passwords, OAuth callbacks, SSH private keys, tokens, or sensitive host paths here. Store secrets only in approved local secret mechanisms such as `.env` or OpenClaw's local auth store.

## Tool Inventory

| Tool or service | Purpose | Access method | Notes | Review needed |
| --- | --- | --- | --- | --- |
| OpenClaw Gateway | Local agent gateway and Slack connection | Docker service | Started by repo scripts | Human approval for auth changes |
| Slack | PI Liaison intake and review surface | Socket Mode env vars | PI Liaison only | Human approval for external messaging scope |
| AI-VERDE / CyVerse | Optional open-model API experiments | `.env` placeholders | See `MODEL_ASSIGNMENTS.md` | Human approval for provider changes |
| Spatiotemporal worker | Bounded STAC/COG/Zarr analysis jobs | Task YAML and worker image | Local worker runs and optional Kubernetes Jobs | Human approval before cluster execution, new mounts, or broad RBAC |

## Local Notes

Add deployment-specific notes here only when they are safe to commit or safe to keep in the local workspace. If a note would expose private infrastructure or credentials, do not put it here.
