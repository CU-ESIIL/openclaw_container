#!/usr/bin/env python3
"""Generate a randomized network geometry (null model) and run the corridor simulation.

This script creates a random geometric graph with the same number of nodes and edges as the
baseline designs, then invokes the existing simulation pipeline (`run_simulation_stream.py`).
It is a placeholder; future work will replace the random generator with a proper null‑model
(e.g., degree‑preserving edge rewiring).
"""
import os, subprocess, json, random
from pathlib import Path

# Settings – match existing analysis root
analysis_root = os.getenv('ANALYSIS_ROOT') or Path('analysis') / 'null_model'
analysis_root = Path(analysis_root).resolve()
analysis_root.mkdir(parents=True, exist_ok=True)

# Simple random geometric graph generator (placeholder)
num_nodes = 2000
radius = 0.05  # placeholder distance threshold
coords = [(random.random(), random.random()) for _ in range(num_nodes)]
edges = []
for i in range(num_nodes):
    xi, yi = coords[i]
    for j in range(i+1, num_nodes):
        xj, yj = coords[j]
        if (xi-xj)**2 + (yi-yj)**2 < radius**2:
            edges.append((i, j))

# Write a minimal network JSON for the Node script to consume
network_path = analysis_root / 'null_network.json'
with open(network_path, 'w') as f:
    json.dump({"nodes": list(range(num_nodes)), "edges": edges}, f)

# Set env to point to this analysis root and run the existing simulation wrapper
env = os.environ.copy()
env['ANALYSIS_ROOT'] = str(analysis_root)
print(f"Running simulation on null model at {analysis_root}")
subprocess.run(['python3', 'scripts/run_simulation_stream.py'], env=env, check=True)

print('Null model simulation complete. Results are in', analysis_root)
