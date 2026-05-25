#!/usr/bin/env python3
"""Simple task orchestrator for OpenClaw project.
It reads `tasks_queue.json` (a list of dicts with keys `name` and `command`) and
spawns a sub‑agent for each task using the OpenClaw CLI.
The orchestrator runs as an isolated sub‑agent; it does not wait for each
sub‑task to finish before launching the next one, relying on the push‑based
completion events that OpenClaw provides.
"""
import json, subprocess, shlex, os, sys

QUEUE_FILE = "tasks_queue.json"

if not os.path.exists(QUEUE_FILE):
    print(f"[orchestrator] No queue file found at {QUEUE_FILE}", file=sys.stderr)
    sys.exit(1)

with open(QUEUE_FILE) as f:
    tasks = json.load(f)

if not isinstance(tasks, list):
    print("[orchestrator] Invalid queue format: expected a list", file=sys.stderr)
    sys.exit(1)

for task in tasks:
    name = task.get("name")
    cmd = task.get("command")
    if not name or not cmd:
        continue
    # Build the OpenClaw CLI command to spawn a sub‑agent
    cli_cmd = [
        "openclaw",
        "sessions",
        "spawn",
        f"--task={cmd}",
        f"--taskName={name}",
        "--runtime=subagent",
        "--mode=run",
        "--context=isolated",
    ]
    # Execute the command; capture output for debugging
    try:
        result = subprocess.run(cli_cmd, capture_output=True, text=True, check=True)
        print(f"[orchestrator] Spawned {name}: {result.stdout.strip()}")
    except subprocess.CalledProcessError as e:
        print(f"[orchestrator] Failed to spawn {name}: {e.stderr}", file=sys.stderr)

print("[orchestrator] All tasks dispatched.")
