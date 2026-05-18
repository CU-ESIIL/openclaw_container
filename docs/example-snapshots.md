# Example Snapshots

The repository keeps the live `/workspace` directory ignored because it can contain local source materials, generated notes, runtime state, credentials, and project-specific files. When a workspace run produces outputs that should be preserved, copy a curated snapshot into `examples/`.

The first captured snapshot is `examples/urban_wildlife_corridors/`. It includes agent-generated documents, reports, a simulation script, analysis tables, and a figure from a Phase 0 urban wildlife corridor project. It intentionally excludes the original source uploads, `.env` files, OpenClaw auth state, Slack state, and broad runtime logs.

Use snapshots for reviewable examples of how the PI Liaison and working group structure behave. Do not treat a snapshot as default seed material for all new users unless the files belong in `docker/seed-workspace`.
