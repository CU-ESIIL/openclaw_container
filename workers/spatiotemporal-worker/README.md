# Spatiotemporal Worker

This worker runs bounded spatial-temporal analysis tasks from YAML configuration files. The first implementation is intentionally modest: it proves the runtime pattern without requiring a production-scale geospatial workflow.

The worker can:

- read a task configuration file
- query STAC metadata when network access and dependencies are available
- run in offline demo mode for smoke tests
- create a quicklook figure
- write `task.yaml`, `status.json`, `logs.txt`, `metadata.json`, `report.md`, and `report.html`
- exit cleanly with a clear status

## Run Locally

```bash
./scripts/run_worker_local.sh examples/spatiotemporal/tasks/example_stac_preview.yaml
```

Set `SCIENCECLAW_WORKER_OFFLINE=1` to force a deterministic offline run:

```bash
SCIENCECLAW_WORKER_OFFLINE=1 ./scripts/run_worker_local.sh examples/spatiotemporal/tasks/example_stac_preview.yaml
```

## Task Contract

Workers accept explicit task YAML files only. They should not accept arbitrary shell commands. Output directories must live under `/data/outputs/jobs` unless a human operator deliberately changes the runtime policy.
