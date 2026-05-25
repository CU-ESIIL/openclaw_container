# Workspace Notes

## 2026-05-25 Handoff

Gateway 3 imported gateway 1's scientific working content into:

```text
/workspace/imports/gateway1-2026-05-25
```

Gateway 1 was left running. The import excluded OpenClaw runtime state, auth/session stores, `.env`, key/token files, `.git`, virtual environments, caches, and old backups.

## Active Next Actions

- [ ] Review `tasks_queue.json` from the imported snapshot.
- [ ] Decide which manuscript draft is current.
- [ ] Decide whether to promote selected files from the import into `/workspace/projects/fractal-corridors` or leave the import as read-only source material.
- [ ] Identify external datasets that should be mounted or streamed rather than copied into `/workspace`.
- [ ] Decide the public GitHub repository name and owner before release work.

## Notes For Agents

Start from the import and project manifest. Do not assume all gateway 1 runtime context should be reproduced in gateway 3. Recreate environments from scripts, manifests, and documented dependencies.
