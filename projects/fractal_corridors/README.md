# Fractal Corridors Project Snapshot

This folder preserves the domain work developed in container 1. It is project
content, not ScienceClaw/OpenClaw container infrastructure.

## Source

- Source container family: `openclaw_container-*` / container 1
- Source workspace mount: `workspace/`
- Snapshot destination: `projects/fractal_corridors/workspace/`
- Snapshot date: 2026-05-24

## Preserved Content

The snapshot includes manuscript drafts, agent reports, simulation code,
simulation outputs, figures, literature notes, project memory files, source
materials, and generated corridor/network data.

Important locations:

- `PROJECT.yaml` - project identity and routing map.
- `DATA_MANIFEST.md` - data inventory, storage mode, and future data rules.
- `GITHUB_REPOS.md` - repository plan and live gateway 3 GitHub registry pointer.
- `EXTERNAL_LINKS.md` - external storage and gateway 3 handoff links.
- `STORAGE.yml` - project-level storage aliases.
- `GATEWAY1_HANDOFF.md` - gateway 1 to gateway 3 handoff note.
- `GATEWAY3_RESOURCE_MAP.md` - tracked copy of the live gateway 3 resource map for this project.
- `WORKSPACE_NOTES.md` - active next actions and agent handoff notes.
- `workspace/documents/urban_wildlife_corridors/` - manuscript draft and
  supporting narrative documents.
- `workspace/agent_reports/urban_wildlife_corridors/` - theory, review,
  validation, and team synthesis notes.
- `workspace/scripts/` - simulation, network generation, visualization, and
  experiment scripts.
- `workspace/analysis/` - simulation summaries, sensitivity tables, parquet
  results, and experiment outputs.
- `workspace/output/reticulation/` - reticulation experiment JSON summaries.
- `workspace/figures/urban_wildlife_corridors/` - generated figures.
- `workspace/data/` - small raster, derived vector, synthetic landscape, and
  reticulation input data.
- `workspace/references.bib` - bibliography used by the project.

## GitHub-Safe Adjustments

The original workspace contained runtime and dependency folders that should not
be committed. These were intentionally excluded:

- `.openclaw/`
- `.venv/`
- `venv/`
- `__pycache__/`
- `.ipynb_checkpoints/`
- `memory/.dreams/`
- `tmp/`
- `logs/openclaw-gateway.log`
- `services/`

One generated file was too large for normal GitHub storage:

```text
workspace/data/derived/Montreal/nearest_web.geojson
```

The original was about 359 MB, so it was preserved as:

```text
workspace/data/derived/Montreal/nearest_web.geojson.gz
```

Use `gzip -dk workspace/data/derived/Montreal/nearest_web.geojson.gz` from this
folder to restore the GeoJSON when needed.

## Secret Check

This snapshot was scanned for common Slack, GitHub, OpenAI, token, PEM, and key
patterns. The only matches were placeholder/token-handling strings inside
`check-secrets.sh` and `mask-secrets.sh`.
