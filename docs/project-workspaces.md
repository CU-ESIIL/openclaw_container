# Project Workspaces

ScienceClaw project folders keep active scientific work organized without turning the container into a data warehouse. A project folder is a small routing map: it points to workspace files, GitHub repositories, external storage, remote catalogs, and review notes.

Use:

```text
/workspace/projects/<project-slug>/
```

Recommended files:

```text
README.md
PROJECT.yaml
DATA_MANIFEST.md
GITHUB_REPOS.md
EXTERNAL_LINKS.md
WORKSPACE_NOTES.md
```

## What Belongs In A Project Folder

- project identity, status, and human owner
- links to imported snapshots or active workspace folders
- GitHub repositories and local clone paths
- external data stores, mounts, catalogs, and access modes
- data licenses, citations, sensitivity notes, and cache policy
- handoffs, assumptions, and next actions

## What Does Not Belong

- full external drives
- large raw data dumps
- OAuth state, API keys, tokens, callback URLs, or secrets
- OpenClaw runtime/session state
- local virtual environments or package caches

## Gateway 3 Pattern

Gateway 3 can take over work from older gateways by importing a snapshot under `/workspace/imports/` and creating a project control folder under `/workspace/projects/`.

For example:

```text
/workspace/imports/gateway1-2026-05-25
/workspace/projects/fractal-corridors
```

The import is the preserved source material. The project folder is the active routing layer that tells agents which files, repos, and external stores to use next.

## External Data

Prefer stream-first or mount-first access:

- STAC catalogs for discovery
- COG, Zarr, Parquet, NetCDF, and cloud/object-storage formats for lazy reads
- WebDAV, iRODS, S3-compatible, OSN-style, or institutional drives through explicit mounts
- `/external_storage/local/<project-slug>` for local large data

Document the source, access method, format, license, citation, sensitivity, and storage mode before copying data into `/workspace`.
