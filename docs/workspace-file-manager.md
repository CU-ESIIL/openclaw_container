# Workspace File Manager

The ScienceClaw workspace file manager is the everyday file surface for the container. It is meant to make the system feel like a visible scientific workspace instead of an invisible agent runtime. Users can see where project files live, what agents created, where outputs were written, and which artifacts are ready for review.

Open it from the ScienceClaw sidebar with **Files**. The branded Control UI shows a compact live workspace listing directly in the sidebar, with the full file manager available for deeper inspection. It is also available directly at:

```text
http://127.0.0.1:8090/files?path=/workspace
```

For additional instances, replace `8090` with that instance's CMS port.

The full file manager shares the CMS header navigation. Use **Back to OpenClaw** to return to the matching OpenClaw chat/control page without relying on the browser back button.

## What It Shows

The file manager uses `/` as the visual root. This lets users inspect the container layout and understand that `/workspace` is only one part of the running environment. The interface labels system paths as read-only and treats `/workspace` as the normal project area.

The most important shortcuts are:

| Shortcut | Purpose |
| --- | --- |
| `/workspace` | Active working-group memory, drafts, scripts, reports, and agent files |
| `/workspace/outputs` | Primary result folder for figures, tables, reports, logs, and job outputs |
| `/data/outputs` | Durable output mount used by worker jobs and the output review layer |
| `/tmp` | Scratch space for temporary files |

## Safe Operations

Normal file operations are available inside safe writable roots:

- create folders
- create text files
- upload files
- download files
- rename files
- copy or move files through the API
- delete files with explicit confirmation
- edit safe text formats in the browser

Editable text formats include Markdown, Python, R, JSON, YAML, TOML, shell scripts, CSV, HTML, CSS, JavaScript, and plain text. Binary files are never opened in the text editor.

## Previews

The file manager provides lightweight previews for common scientific artifacts:

| Type | Preview behavior |
| --- | --- |
| Markdown | Rendered headings, code blocks, tables, and local images |
| CSV/TSV | First rows in a scrollable table |
| PNG, JPEG, GIF, WebP, SVG | Inline image preview with file metadata |
| Text files | Monospace read-only preview with an edit option when writable |

This is not a full notebook or IDE. JupyterLab remains the advanced analysis environment. The file manager is for quick inspection, transparent workspace navigation, and small edits.

## Security Model

The browser can inspect the container from `/`, but write operations are restricted by default. System paths are visible for transparency and locked against casual edits.

The service blocks sensitive paths and names, including `.env`, `.env.*`, `.git`, `.openclaw`, `.ssh`, `/proc`, `/sys`, `/dev`, secret mount paths, `node_modules`, `__pycache__`, private keys, token files, and directories named `secrets`. Blocked files are hidden from listings and cannot be previewed, downloaded, edited, moved, renamed, copied, or deleted.

Every operation resolves and normalizes the requested path before access. If a path is sensitive or outside a safe writable root for a write operation, the request fails closed.

## Relationship To CMS Review

The file manager and CMS share the same lightweight service. The file manager helps users inspect and manage workspace files. The CMS review workflow adds status metadata and promotes approved artifacts into the MkDocs documentation tree. In practice, a user can inspect outputs in `/workspace/outputs`, mark an artifact as ready for review, and then promote only the public, reviewed version.

## Smoke Test

Run:

```bash
make workspace-smoke-test
```

The test starts the file manager on a temporary port, seeds a tiny demo workspace, verifies previews and editing, confirms upload and delete confirmation behavior, and checks that sensitive files are blocked. The container entrypoint also seeds the tiny demo workspace by default so a new deployment has a Markdown file, CSV, image, and editable script available for immediate inspection. Set `SCIENCECLAW_SEED_FILE_MANAGER_DEMO=0` to disable that seeding.
