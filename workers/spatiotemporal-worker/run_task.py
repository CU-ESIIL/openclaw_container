#!/usr/bin/env python3
"""Run a bounded ScienceClaw spatiotemporal worker task."""

from __future__ import annotations

import argparse
import base64
import html
import json
import os
import platform
import shutil
import sys
import traceback
from contextlib import redirect_stderr, redirect_stdout
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import yaml
except Exception:  # pragma: no cover - dependency check path
    yaml = None


TINY_PNG = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAFgwJ/lwZ9WQAAAABJRU5ErkJggg=="
)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def slugify(value: str) -> str:
    allowed = []
    for char in value.lower():
        if char.isalnum():
            allowed.append(char)
        elif char in ("-", "_", " "):
            allowed.append("-")
    return "-".join("".join(allowed).split("-")) or "scienceclaw-task"


def read_task(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if yaml is None:
        data = read_simple_task_yaml(text)
    else:
        data = yaml.safe_load(text)
    if not isinstance(data, dict):
        raise ValueError(f"Task config must be a mapping: {path}")
    return data


def parse_scalar(value: str) -> Any:
    value = value.strip()
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1]
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False
    if value.startswith("[") and value.endswith("]"):
        items = [item.strip() for item in value[1:-1].split(",") if item.strip()]
        return [parse_scalar(item) for item in items]
    try:
        return int(value)
    except ValueError:
        pass
    try:
        return float(value)
    except ValueError:
        return value


def read_simple_task_yaml(text: str) -> dict[str, Any]:
    """Parse the simple task YAML shape used by ScienceClaw examples."""
    data: dict[str, Any] = {}
    section: str | None = None
    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        if not line.startswith(" "):
            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip()
            if value:
                data[key] = parse_scalar(value)
                section = None
            else:
                data[key] = {}
                section = key
        elif section and ":" in line:
            key, _, value = line.strip().partition(":")
            data[section][key.strip()] = parse_scalar(value)
    return data


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def status_template(job_id: str, task: dict[str, Any], output_dir: Path, status: str) -> dict[str, Any]:
    return {
        "job_id": job_id,
        "task_name": task.get("task_name", job_id),
        "status": status,
        "started_at": utc_now(),
        "finished_at": None,
        "worker_image": os.environ.get("SCIENCECLAW_WORKER_IMAGE", "local-python"),
        "output_dir": str(output_dir),
        "error": None,
    }


def package_versions() -> dict[str, str]:
    versions = {"python": platform.python_version()}
    for name in [
        "rasterio",
        "xarray",
        "geopandas",
        "pystac_client",
        "duckdb",
        "numpy",
        "pandas",
    ]:
        try:
            module = __import__(name)
            versions[name] = getattr(module, "__version__", "unknown")
        except Exception:
            versions[name] = "not-installed"
    return versions


def query_stac(task: dict[str, Any], offline: bool) -> dict[str, Any]:
    inputs = task.get("inputs", {})
    if offline:
        return {
            "mode": "offline-demo",
            "stac_api": inputs.get("stac_api"),
            "collection": inputs.get("collection"),
            "matched_items": 0,
            "selected_assets": ["red", "nir"],
            "note": "Offline mode generated deterministic metadata without network access.",
        }

    try:
        from pystac_client import Client
    except Exception as exc:
        return {
            "mode": "dependency-missing",
            "error": f"pystac-client unavailable: {exc}",
            "selected_assets": [],
        }

    client = Client.open(inputs["stac_api"])
    search = client.search(
        collections=[inputs["collection"]],
        bbox=inputs.get("bbox"),
        datetime=inputs.get("datetime"),
        max_items=int(inputs.get("max_items", 5)),
    )
    items = list(search.items())
    selected_assets: list[str] = []
    if items:
        requested = task.get("analysis", {}).get("bands", [])
        assets = items[0].assets.keys()
        selected_assets = [asset for asset in requested if asset in assets]
        if not selected_assets:
            selected_assets = list(items[0].assets.keys())[:5]
    return {
        "mode": "stac-query",
        "stac_api": inputs.get("stac_api"),
        "collection": inputs.get("collection"),
        "bbox": inputs.get("bbox"),
        "datetime": inputs.get("datetime"),
        "matched_items": len(items),
        "first_item_id": items[0].id if items else None,
        "selected_assets": selected_assets,
    }


def write_quicklook(output_dir: Path, task: dict[str, Any], stac_info: dict[str, Any]) -> list[str]:
    figures_dir = output_dir / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)
    png_path = figures_dir / "quicklook.png"
    svg_path = figures_dir / "quicklook.svg"
    generated = []

    try:
        import matplotlib.pyplot as plt
        import numpy as np

        x = np.linspace(0, 1, 64)
        y = np.linspace(0, 1, 64)
        grid = np.outer(np.sin(x * np.pi), np.cos(y * np.pi)) + 1
        fig, ax = plt.subplots(figsize=(5, 4))
        image = ax.imshow(grid, cmap="viridis")
        ax.set_title(task.get("task_name", "ScienceClaw quicklook"))
        ax.set_xticks([])
        ax.set_yticks([])
        fig.colorbar(image, ax=ax, fraction=0.046, pad=0.04)
        fig.tight_layout()
        fig.savefig(png_path, dpi=140)
        plt.close(fig)
    except Exception:
        png_path.write_bytes(TINY_PNG)

    generated.append(str(png_path))
    svg_path.write_text(
        "\n".join(
            [
                "<svg xmlns='http://www.w3.org/2000/svg' width='640' height='360' viewBox='0 0 640 360'>",
                "<rect width='640' height='360' fill='#234A65'/>",
                "<circle cx='180' cy='180' r='110' fill='#42BCDC' opacity='0.85'/>",
                "<circle cx='360' cy='180' r='95' fill='#007135' opacity='0.78'/>",
                f"<text x='40' y='315' fill='white' font-family='sans-serif' font-size='24'>{html.escape(str(task.get('task_name', 'ScienceClaw task')))}</text>",
                f"<text x='40' y='345' fill='white' font-family='sans-serif' font-size='16'>mode: {html.escape(str(stac_info.get('mode', 'unknown')))}</text>",
                "</svg>",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    generated.append(str(svg_path))
    return generated


def write_report(output_dir: Path, task: dict[str, Any], stac_info: dict[str, Any], outputs: list[str]) -> list[str]:
    report_md = output_dir / "report.md"
    report_html = output_dir / "report.html"
    task_name = task.get("task_name", "ScienceClaw task")
    lines = [
        f"# {task_name}",
        "",
        "This is a bounded ScienceClaw worker report. Outputs require human review before reuse.",
        "",
        "## Input Summary",
        "",
        f"- STAC API: `{task.get('inputs', {}).get('stac_api', 'not provided')}`",
        f"- Collection: `{task.get('inputs', {}).get('collection', 'not provided')}`",
        f"- Bounding box: `{task.get('inputs', {}).get('bbox', 'not provided')}`",
        f"- Datetime: `{task.get('inputs', {}).get('datetime', 'not provided')}`",
        "",
        "## Worker Summary",
        "",
        f"- Mode: `{stac_info.get('mode', 'unknown')}`",
        f"- Matched STAC items: `{stac_info.get('matched_items', 'unknown')}`",
        f"- Selected assets: `{', '.join(stac_info.get('selected_assets', [])) or 'none'}`",
        "",
        "## Generated Outputs",
        "",
    ]
    lines.extend([f"- `{Path(path).relative_to(output_dir)}`" for path in outputs])
    report_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    report_html.write_text(
        "<!doctype html><html><head><meta charset='utf-8'><title>"
        + html.escape(str(task_name))
        + "</title></head><body><pre>"
        + html.escape(report_md.read_text(encoding="utf-8"))
        + "</pre></body></html>\n",
        encoding="utf-8",
    )
    return [str(report_md), str(report_html)]


def run(task_path: Path, output_override: str | None, offline: bool) -> int:
    task = read_task(task_path)
    task_name = str(task.get("task_name", "scienceclaw-task"))
    job_id = os.environ.get("SCIENCECLAW_JOB_ID") or f"{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}-{slugify(task_name)}"
    output_dir = Path(output_override or task.get("output_dir") or f"/data/outputs/jobs/{job_id}")
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "figures").mkdir(exist_ok=True)
    (output_dir / "tables").mkdir(exist_ok=True)
    (output_dir / "maps").mkdir(exist_ok=True)

    shutil.copyfile(task_path, output_dir / "task.yaml")
    status = status_template(job_id, task, output_dir, "running")
    write_json(output_dir / "status.json", status)

    log_path = output_dir / "logs.txt"
    try:
        with log_path.open("a", encoding="utf-8") as log, redirect_stdout(log), redirect_stderr(log):
            print(f"[{utc_now()}] Starting ScienceClaw worker task: {task_name}")
            print(f"[{utc_now()}] Output directory: {output_dir}")
            stac_info = query_stac(task, offline=offline)
            generated = []
            if task.get("outputs", {}).get("make_quicklook", True):
                generated.extend(write_quicklook(output_dir, task, stac_info))
            if task.get("outputs", {}).get("make_report", True):
                generated.extend(write_report(output_dir, task, stac_info, generated))
            metadata = {
                "job_id": job_id,
                "task_name": task_name,
                "created_at": utc_now(),
                "input_sources": task.get("inputs", {}),
                "analysis": task.get("analysis", {}),
                "stac": stac_info,
                "generated_outputs": generated,
                "software_versions": package_versions(),
            }
            write_json(output_dir / "metadata.json", metadata)
            print(f"[{utc_now()}] Finished ScienceClaw worker task: {task_name}")
        status["status"] = "succeeded"
        status["finished_at"] = utc_now()
        write_json(output_dir / "status.json", status)
        print(str(output_dir))
        return 0
    except Exception as exc:
        with log_path.open("a", encoding="utf-8") as log:
            log.write(f"[{utc_now()}] Worker failed: {exc}\n")
            log.write(traceback.format_exc())
        status["status"] = "failed"
        status["finished_at"] = utc_now()
        status["error"] = str(exc)
        write_json(output_dir / "status.json", status)
        print(f"ScienceClaw worker failed: {exc}", file=sys.stderr)
        return 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task", required=True, help="Path to task YAML.")
    parser.add_argument("--output-dir", help="Override output directory.")
    parser.add_argument("--offline", action="store_true", help="Do not call remote APIs; create deterministic demo outputs.")
    args = parser.parse_args()
    offline = args.offline or os.environ.get("SCIENCECLAW_WORKER_OFFLINE") == "1"
    return run(Path(args.task), args.output_dir, offline)


if __name__ == "__main__":
    raise SystemExit(main())
