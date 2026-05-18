#!/usr/bin/env python3
"""Render or submit a ScienceClaw Kubernetes Job after human review."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from render_job_manifest import render


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task", required=True, help="Task YAML path.")
    parser.add_argument("--job-id", help="Stable Kubernetes job id/name.")
    parser.add_argument("--image", default="ghcr.io/cu-esiil/openclaw_container/spatiotemporal-worker:latest")
    parser.add_argument("--namespace", default="scienceclaw")
    parser.add_argument("--apply", action="store_true", help="Apply with kubectl. Default is print-only.")
    args = parser.parse_args()

    manifest = render(Path(args.task), args.job_id, args.image, args.namespace)
    if not args.apply:
        print(manifest)
        print("# Dry-run only. Re-run with --apply after human review.", file=sys.stderr)
        return 0

    process = subprocess.run(["kubectl", "apply", "-f", "-"], input=manifest, text=True, check=False)
    return process.returncode


if __name__ == "__main__":
    raise SystemExit(main())
