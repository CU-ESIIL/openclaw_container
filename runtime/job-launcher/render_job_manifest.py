#!/usr/bin/env python3
"""Render a bounded Kubernetes Job manifest for a ScienceClaw worker task."""

from __future__ import annotations

import argparse
import re
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except Exception:  # pragma: no cover
    yaml = None


DEFAULT_IMAGE = "ghcr.io/cu-esiil/openclaw_container/spatiotemporal-worker:latest"
ALLOWLISTED_IMAGES = {
    DEFAULT_IMAGE,
    "scienceclaw-spatiotemporal-worker:local",
}


def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9-]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value[:55] or "scienceclaw-job"


def load_task(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if yaml is None:
        data = read_simple_task_yaml(text)
    else:
        data = yaml.safe_load(text)
    if not isinstance(data, dict):
        raise ValueError("Task YAML must be a mapping.")
    return data


def parse_scalar(value: str):
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
        return [parse_scalar(item.strip()) for item in value[1:-1].split(",") if item.strip()]
    try:
        return int(value)
    except ValueError:
        pass
    try:
        return float(value)
    except ValueError:
        return value


def read_simple_task_yaml(text: str) -> dict:
    data = {}
    section = None
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


def validate_task(task: dict, image: str) -> None:
    required = ["task_name", "output_dir", "inputs", "analysis", "outputs"]
    missing = [key for key in required if key not in task]
    if missing:
        raise ValueError(f"Task is missing required fields: {', '.join(missing)}")
    output_dir = str(task["output_dir"])
    if not output_dir.startswith("/data/outputs/jobs/"):
        raise ValueError("Task output_dir must start with /data/outputs/jobs/")
    if image not in ALLOWLISTED_IMAGES:
        raise ValueError(f"Worker image is not allowlisted: {image}")


def render(task_path: Path, job_id: str | None, image: str, namespace: str) -> str:
    task = load_task(task_path)
    validate_task(task, image)
    name = slugify(job_id or f"{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}-{task['task_name']}")
    configmap_name = f"{name}-task"
    task_text = task_path.read_text(encoding="utf-8")
    indented_task = "\n".join(f"    {line}" for line in task_text.splitlines())
    return f"""apiVersion: v1
kind: ConfigMap
metadata:
  name: {configmap_name}
  namespace: {namespace}
  labels:
    app.kubernetes.io/name: scienceclaw
    scienceclaw.esl/job-id: {name}
data:
  task.yaml: |
{indented_task}
---
apiVersion: batch/v1
kind: Job
metadata:
  name: {name}
  namespace: {namespace}
  labels:
    app.kubernetes.io/name: scienceclaw
    scienceclaw.esl/job-type: spatiotemporal-worker
    scienceclaw.esl/job-id: {name}
spec:
  backoffLimit: 1
  activeDeadlineSeconds: 1800
  ttlSecondsAfterFinished: 86400
  template:
    metadata:
      labels:
        app.kubernetes.io/name: scienceclaw
        scienceclaw.esl/job-type: spatiotemporal-worker
        scienceclaw.esl/job-id: {name}
    spec:
      serviceAccountName: scienceclaw-job-runner
      restartPolicy: Never
      containers:
        - name: worker
          image: {image}
          imagePullPolicy: IfNotPresent
          args: ["--task", "/task/task.yaml"]
          env:
            - name: DATA_ROOT
              value: /data
            - name: SCIENCECLAW_JOB_ID
              value: {name}
            - name: SCIENCECLAW_WORKER_IMAGE
              value: {image}
          resources:
            requests:
              cpu: "500m"
              memory: 1Gi
            limits:
              cpu: "2"
              memory: 4Gi
          volumeMounts:
            - name: scienceclaw-data
              mountPath: /data
            - name: task-config
              mountPath: /task
              readOnly: true
      volumes:
        - name: scienceclaw-data
          persistentVolumeClaim:
            claimName: scienceclaw-data
        - name: task-config
          configMap:
            name: {configmap_name}
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task", required=True, help="Task YAML path.")
    parser.add_argument("--job-id", help="Stable Kubernetes job id/name.")
    parser.add_argument("--image", default=DEFAULT_IMAGE, help="Allowlisted worker image.")
    parser.add_argument("--namespace", default="scienceclaw", help="Kubernetes namespace.")
    args = parser.parse_args()
    print(render(Path(args.task), args.job_id, args.image, args.namespace))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
