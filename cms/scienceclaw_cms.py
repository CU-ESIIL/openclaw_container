#!/usr/bin/env python3
"""Minimal file-backed ScienceClaw workspace CMS."""

from __future__ import annotations

import html
import json
import mimetypes
import os
import posixpath
import shutil
import urllib.parse
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

DEFAULT_ROOTS = "/workspace,/data/outputs,/repo/docs,/repo/examples,/repo/storage,/external_storage/local"
STATUSES = ["draft", "needs_review", "approved", "published"]
VISIBILITIES = ["private", "public", "metadata_only"]
TEXT_EXTENSIONS = {".md", ".txt", ".py", ".sh", ".yml", ".yaml", ".json", ".csv", ".html", ".css", ".js", ".toml"}
ASSET_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".csv", ".json", ".geojson", ".html"}


class Root:
    def __init__(self, name: str, path: Path):
        self.name = name
        self.path = path.resolve()


def configured_roots() -> list[Root]:
    raw = os.environ.get("SCIENCECLAW_CMS_ROOTS", DEFAULT_ROOTS)
    roots: list[Root] = []
    seen: set[Path] = set()
    for item in raw.split(","):
        item = item.strip()
        if not item:
            continue
        path = Path(item).resolve()
        if path in seen:
            continue
        seen.add(path)
        path.mkdir(parents=True, exist_ok=True)
        name = path.name or str(path)
        if str(path) == "/workspace":
            name = "workspace"
        elif str(path) == "/data/outputs":
            name = "outputs"
        elif str(path).startswith("/repo/"):
            name = f"repo-{path.name}"
        roots.append(Root(name, path))
    return roots


ROOTS = configured_roots()


def find_root(name: str) -> Root:
    for root in ROOTS:
        if root.name == name:
            return root
    raise ValueError(f"Unknown root: {name}")


def safe_path(root_name: str, rel_path: str = "") -> tuple[Root, Path]:
    root = find_root(root_name)
    clean_rel = posixpath.normpath("/" + rel_path).lstrip("/")
    path = (root.path / clean_rel).resolve()
    if path != root.path and root.path not in path.parents:
        raise ValueError("Path escapes configured root.")
    return root, path


def metadata_path(path: Path) -> Path:
    return path.with_name(f"{path.name}.scienceclaw.meta.json")


def read_metadata(path: Path) -> dict[str, Any]:
    meta = metadata_path(path)
    if not meta.exists():
        return {
            "status": "draft",
            "visibility": "private",
            "created_by": "scienceclaw-cms",
            "source_files": [str(path)],
            "outputs": [],
            "external_data": [],
        }
    try:
        return json.loads(meta.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"status": "draft", "visibility": "private", "metadata_error": f"Invalid JSON: {meta}"}


def write_metadata(path: Path, updates: dict[str, Any]) -> dict[str, Any]:
    meta = read_metadata(path)
    meta.update(updates)
    meta.setdefault("created_at", datetime.now(timezone.utc).isoformat())
    meta["updated_at"] = datetime.now(timezone.utc).isoformat()
    metadata_path(path).write_text(json.dumps(meta, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return meta


def render_page(title: str, body: str) -> bytes:
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} - ScienceClaw CMS</title>
<style>
:root {{ --blue:#234a65; --cyan:#42bcdc; --green:#007135; --ink:#161a19; --line:#e3e3e3; }}
body {{ margin:0; font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; color:var(--ink); background:#f7faf9; }}
header {{ display:flex; align-items:center; gap:0.9rem; padding:0.85rem 1.1rem; border-bottom:1px solid var(--line); background:white; position:sticky; top:0; z-index:2; }}
header img {{ width:2.4rem; height:2.4rem; object-fit:contain; }}
header strong {{ color:var(--blue); font-size:1.05rem; }}
main {{ max-width:1120px; margin:0 auto; padding:1.2rem; }}
a {{ color:#006c8c; text-decoration:none; }}
a:hover {{ text-decoration:underline; }}
.toolbar, .panel {{ background:white; border:1px solid var(--line); border-radius:8px; padding:1rem; margin-bottom:1rem; }}
.roots {{ display:flex; flex-wrap:wrap; gap:0.45rem; }}
.pill {{ display:inline-flex; padding:0.3rem 0.55rem; border:1px solid var(--line); border-radius:999px; background:#f9fbfb; font-size:0.9rem; }}
table {{ width:100%; border-collapse:collapse; background:white; border:1px solid var(--line); border-radius:8px; overflow:hidden; }}
th, td {{ padding:0.55rem 0.65rem; border-bottom:1px solid var(--line); text-align:left; vertical-align:top; }}
th {{ background:#edf5f2; color:var(--blue); }}
tr:last-child td {{ border-bottom:0; }}
textarea {{ width:100%; min-height:28rem; font:0.92rem ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; border:1px solid var(--line); border-radius:6px; padding:0.7rem; box-sizing:border-box; }}
button, .button {{ border:0; border-radius:6px; background:var(--green); color:white; padding:0.45rem 0.7rem; font-weight:650; cursor:pointer; }}
.button.secondary, button.secondary {{ background:var(--blue); }}
input, select {{ border:1px solid var(--line); border-radius:6px; padding:0.42rem; }}
pre {{ overflow:auto; background:#0f1720; color:#eef7f7; padding:1rem; border-radius:8px; }}
.preview img {{ max-width:100%; height:auto; border:1px solid var(--line); border-radius:8px; }}
.muted {{ color:#5d666b; }}
</style>
</head>
<body>
<header><img src="/brand/scienceclaw.png" alt=""><div><strong>ScienceClaw Workspace CMS</strong><br><span class="muted">private workspace review and public MkDocs promotion</span></div></header>
<main>{body}</main>
</body>
</html>""".encode("utf-8")


def rel_link(root: str, path: Path, root_path: Path) -> str:
    rel = "" if path == root_path else path.relative_to(root_path).as_posix()
    return f"/browse?root={urllib.parse.quote(root)}&path={urllib.parse.quote(rel)}"


class Handler(BaseHTTPRequestHandler):
    server_version = "ScienceClawCMS/0.1"

    def do_GET(self) -> None:  # noqa: N802
        try:
            parsed = urllib.parse.urlparse(self.path)
            if parsed.path == "/":
                self.send_html("ScienceClaw CMS", self.home())
            elif parsed.path == "/browse":
                query = urllib.parse.parse_qs(parsed.query)
                root = query.get("root", [ROOTS[0].name])[0]
                rel = query.get("path", [""])[0]
                self.send_html("Browse", self.browse(root, rel))
            elif parsed.path == "/edit":
                query = urllib.parse.parse_qs(parsed.query)
                self.send_html("Edit", self.edit(query.get("root", [""])[0], query.get("path", [""])[0]))
            elif parsed.path == "/raw":
                query = urllib.parse.parse_qs(parsed.query)
                self.send_raw(query.get("root", [""])[0], query.get("path", [""])[0])
            elif parsed.path == "/brand/scienceclaw.png":
                self.send_brand()
            else:
                self.send_error(404)
        except Exception as exc:  # noqa: BLE001 - visible local diagnostic.
            self.send_html("Error", f"<div class='panel'><h1>Error</h1><pre>{html.escape(str(exc))}</pre></div>", status=500)

    def do_POST(self) -> None:  # noqa: N802
        try:
            length = int(self.headers.get("Content-Length", "0"))
            payload = urllib.parse.parse_qs(self.rfile.read(length).decode("utf-8"))
            action = payload.get("action", [""])[0]
            root = payload.get("root", [""])[0]
            rel = payload.get("path", [""])[0]
            if action == "save":
                self.save_markdown(root, rel, payload.get("content", [""])[0])
            elif action == "metadata":
                self.update_metadata(root, rel, payload)
            elif action == "promote":
                self.promote(root, rel, payload.get("target", ["reports"])[0])
            else:
                self.send_error(400, "Unknown action")
        except Exception as exc:  # noqa: BLE001
            self.send_html("Error", f"<div class='panel'><h1>Error</h1><pre>{html.escape(str(exc))}</pre></div>", status=500)

    def home(self) -> str:
        roots = " ".join(f"<a class='pill' href='/browse?root={urllib.parse.quote(root.name)}'>{html.escape(root.name)}: {html.escape(str(root.path))}</a>" for root in ROOTS)
        return f"""
<section class="panel">
<h1>ScienceClaw workspace CMS</h1>
<p>This local tool lets a human review private workspace outputs, attach provenance/status metadata, and promote approved public artifacts into the MkDocs docs tree. It does not execute agent code or publish without a repository action.</p>
<div class="roots">{roots}</div>
</section>
<section class="panel">
<h2>Promotion model</h2>
<ol>
<li>Drafts start in <code>/workspace</code> or <code>/data/outputs</code>.</li>
<li>The CMS records status sidecars next to the source file.</li>
<li>Approved Markdown can be promoted to <code>docs/reports/</code> or <code>docs/dashboard/</code>.</li>
<li>Small public assets can be copied into <code>docs/assets/cms/</code>.</li>
<li>Large private outputs stay in external storage and are represented by metadata or public links.</li>
</ol>
</section>
"""

    def browse(self, root_name: str, rel: str) -> str:
        root, path = safe_path(root_name, rel)
        breadcrumb = f"<a href='/'>CMS</a> / <a href='{rel_link(root.name, root.path, root.path)}'>{html.escape(root.name)}</a>"
        if path != root.path:
            parts = path.relative_to(root.path).parts
            acc: list[str] = []
            for part in parts:
                acc.append(part)
                breadcrumb += f" / <a href='{rel_link(root.name, root.path.joinpath(*acc), root.path)}'>{html.escape(part)}</a>"
        if path.is_dir():
            rows = []
            if path != root.path:
                rows.append(f"<tr><td><a href='{rel_link(root.name, path.parent, root.path)}'>..</a></td><td>directory</td><td></td></tr>")
            for item in sorted(path.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower())):
                if item.name.startswith(".") and not item.name.endswith(".scienceclaw.meta.json"):
                    continue
                rel_item = item.relative_to(root.path).as_posix()
                kind = "directory" if item.is_dir() else item.suffix.lower().lstrip(".") or "file"
                size = "" if item.is_dir() else str(item.stat().st_size)
                rows.append(f"<tr><td><a href='/browse?root={urllib.parse.quote(root.name)}&path={urllib.parse.quote(rel_item)}'>{html.escape(item.name)}</a></td><td>{kind}</td><td>{size}</td></tr>")
            return f"<div class='toolbar'>{breadcrumb}</div><table><thead><tr><th>Name</th><th>Kind</th><th>Bytes</th></tr></thead><tbody>{''.join(rows)}</tbody></table>"
        return self.preview(root, path)

    def preview(self, root: Root, path: Path) -> str:
        rel = path.relative_to(root.path).as_posix()
        meta = read_metadata(path)
        status_options = "".join(f"<option {'selected' if meta.get('status') == s else ''}>{s}</option>" for s in STATUSES)
        visibility_options = "".join(f"<option {'selected' if meta.get('visibility') == s else ''}>{s}</option>" for s in VISIBILITIES)
        edit = ""
        if path.suffix.lower() in TEXT_EXTENSIONS:
            edit = f"<a class='button secondary' href='/edit?root={urllib.parse.quote(root.name)}&path={urllib.parse.quote(rel)}'>Edit text</a>"
        promote = ""
        if path.suffix.lower() in TEXT_EXTENSIONS | ASSET_EXTENSIONS:
            promote = f"""<form method="post" style="display:inline-block;margin-left:.4rem">
<input type="hidden" name="action" value="promote"><input type="hidden" name="root" value="{html.escape(root.name)}"><input type="hidden" name="path" value="{html.escape(rel)}">
<select name="target"><option value="reports">reports</option><option value="dashboard">dashboard</option><option value="assets">assets</option></select>
<button type="submit">Promote</button></form>"""
        body = f"<div class='toolbar'><a href='{rel_link(root.name, path.parent, root.path)}'>Back</a> / {html.escape(rel)}<br>{edit}{promote}</div>"
        body += f"""<section class="panel"><h2>Status metadata</h2>
<form method="post">
<input type="hidden" name="action" value="metadata"><input type="hidden" name="root" value="{html.escape(root.name)}"><input type="hidden" name="path" value="{html.escape(rel)}">
Status <select name="status">{status_options}</select>
Visibility <select name="visibility">{visibility_options}</select>
<button type="submit">Save status</button>
</form>
<pre>{html.escape(json.dumps(meta, indent=2, sort_keys=True))}</pre></section>"""
        body += f"<section class='panel preview'><h2>Preview</h2>{self.preview_content(root.name, rel, path)}</section>"
        return body

    def preview_content(self, root_name: str, rel: str, path: Path) -> str:
        suffix = path.suffix.lower()
        if suffix in {".png", ".jpg", ".jpeg", ".gif", ".svg"}:
            return f"<img src='/raw?root={urllib.parse.quote(root_name)}&path={urllib.parse.quote(rel)}' alt=''>"
        if suffix in TEXT_EXTENSIONS:
            text = path.read_text(encoding="utf-8", errors="replace")
            return f"<pre>{html.escape(text[:120000])}</pre>"
        return f"<p>No inline preview for <code>{html.escape(suffix or 'file')}</code>. Use raw download through the file browser.</p>"

    def edit(self, root_name: str, rel: str) -> str:
        root, path = safe_path(root_name, rel)
        if path.suffix.lower() not in TEXT_EXTENSIONS:
            raise ValueError("Only text-like files can be edited.")
        text = path.read_text(encoding="utf-8", errors="replace")
        return f"""<div class="toolbar"><a href="/browse?root={urllib.parse.quote(root.name)}&path={urllib.parse.quote(rel)}">Back to preview</a></div>
<form method="post" class="panel">
<input type="hidden" name="action" value="save"><input type="hidden" name="root" value="{html.escape(root.name)}"><input type="hidden" name="path" value="{html.escape(rel)}">
<textarea name="content">{html.escape(text)}</textarea>
<p><button type="submit">Save</button></p>
</form>"""

    def save_markdown(self, root_name: str, rel: str, content: str) -> None:
        _, path = safe_path(root_name, rel)
        if path.suffix.lower() not in TEXT_EXTENSIONS:
            raise ValueError("Only text-like files can be edited.")
        path.write_text(content, encoding="utf-8")
        write_metadata(path, {"status": "draft", "visibility": "private", "last_edited_by": "scienceclaw-cms"})
        self.redirect(f"/browse?root={urllib.parse.quote(root_name)}&path={urllib.parse.quote(rel)}")

    def update_metadata(self, root_name: str, rel: str, payload: dict[str, list[str]]) -> None:
        _, path = safe_path(root_name, rel)
        status = payload.get("status", ["draft"])[0]
        visibility = payload.get("visibility", ["private"])[0]
        if status not in STATUSES or visibility not in VISIBILITIES:
            raise ValueError("Invalid status or visibility.")
        write_metadata(path, {"status": status, "visibility": visibility})
        self.redirect(f"/browse?root={urllib.parse.quote(root_name)}&path={urllib.parse.quote(rel)}")

    def promote(self, root_name: str, rel: str, target: str) -> None:
        _, source = safe_path(root_name, rel)
        repo_docs = Path(os.environ.get("SCIENCECLAW_REPO_ROOT", "/repo")).resolve() / "docs"
        repo_docs.mkdir(parents=True, exist_ok=True)
        suffix = source.suffix.lower()
        slug = source.stem.lower().replace(" ", "-").replace("_", "-")
        if target in {"reports", "dashboard"} and suffix in TEXT_EXTENSIONS:
            target_dir = repo_docs / target
            target_dir.mkdir(parents=True, exist_ok=True)
            dest = target_dir / f"{slug}{suffix if suffix in {'.md', '.html'} else '.md'}"
            body = source.read_text(encoding="utf-8", errors="replace")
            if dest.suffix == ".md":
                body = f"<!-- Promoted from {source} by ScienceClaw CMS. Review before publishing. -->\n\n{body}"
            dest.write_text(body, encoding="utf-8")
        elif target == "assets" and suffix in ASSET_EXTENSIONS:
            target_dir = repo_docs / "assets" / "cms"
            target_dir.mkdir(parents=True, exist_ok=True)
            dest = target_dir / source.name
            shutil.copy2(source, dest)
        else:
            raise ValueError("Unsupported promotion target for this file type.")
        write_metadata(source, {"status": "published", "visibility": "public", "publish_target": str(dest)})
        self.redirect(f"/browse?root={urllib.parse.quote(root_name)}&path={urllib.parse.quote(rel)}")

    def send_html(self, title: str, body: str, status: int = 200) -> None:
        payload = render_page(title, body)
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def send_raw(self, root_name: str, rel: str) -> None:
        _, path = safe_path(root_name, rel)
        if path.is_dir():
            self.send_error(400, "Cannot fetch raw directory.")
            return
        content_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        data = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def send_brand(self) -> None:
        candidates = [
            Path("/repo/docs/assets/brand/scienceclaw.png"),
            Path(__file__).resolve().parents[1] / "docs" / "assets" / "brand" / "scienceclaw.png",
        ]
        for candidate in candidates:
            if candidate.exists():
                data = candidate.read_bytes()
                self.send_response(200)
                self.send_header("Content-Type", "image/png")
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)
                return
        self.send_error(404)

    def redirect(self, url: str) -> None:
        self.send_response(303)
        self.send_header("Location", url)
        self.end_headers()


def main() -> int:
    port = int(os.environ.get("SCIENCECLAW_CMS_PORT", "8090"))
    server = ThreadingHTTPServer(("0.0.0.0", port), Handler)
    print(f"ScienceClaw CMS listening on http://0.0.0.0:{port}")
    print("Allowed roots:")
    for root in ROOTS:
        print(f"  {root.name}: {root.path}")
    server.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
