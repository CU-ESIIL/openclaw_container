#!/usr/bin/env python3
"""Run Monte‑Carlo replicates of the corridor simulation for all designs.

The script loops over a list of design labels (nearest, mst, dendritic, hierarchical, hybrid) and
executes `run_simulation_stream.py` many times (default 30 replicates) for each design.
It aggregates the `final_mean_occupancy` and `persistent_species_per_length` metrics into
CSV files under `analysis/urban_wildlife_corridors/monte_carlo/`.

This is a placeholder implementation – it re‑uses the existing environment variable
`ANALYSIS_ROOT` to point to a per‑design subdirectory, then calls the Node simulation
wrapper. In a real workflow one would parallelise the runs and store each replicate
separately.
"""
import os, subprocess, pathlib, pandas as pd
from pathlib import Path

# Settings
replicates = int(os.getenv('MC_REPLICATES', '30'))
base_analysis = Path('analysis') / 'urban_wildlife_corridors' / 'monte_carlo'
base_analysis.mkdir(parents=True, exist_ok=True)

designs = ['nearest_web', 'minimum_spanning_tree', 'dendritic_tree', 'hierarchical', 'hybrid_dendritic']

# Function to run a single simulation for a design
def run_one(design, run_id):
    analysis_root = base_analysis / f"{design}_run{run_id}"
    analysis_root.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env['ANALYSIS_ROOT'] = str(analysis_root)
    # Optionally set design via env variable for the Node script (if it reads HIERARCHY_TYPE)
    env['HIERARCHY_TYPE'] = design
    subprocess.run(['python3', 'scripts/run_simulation_stream.py'], env=env, check=True)
    # Load summary CSV (or Parquet) produced by the wrapper
    summary = analysis_root / 'simulation_summary.csv'
    if summary.exists():
        df = pd.read_csv(summary)
        df['run_id'] = run_id
        df['design'] = design
        return df
    else:
        return None

all_dfs = []
for design in designs:
    print(f"Running Monte‑Carlo for design {design} ({replicates} replicates)")
    for i in range(1, replicates + 1):
        df = run_one(design, i)
        if df is not None:
            all_dfs.append(df)

if all_dfs:
    combined = pd.concat(all_dfs, ignore_index=True)
    out_csv = base_analysis / 'monte_carlo_summary.csv'
    combined.to_csv(out_csv, index=False)
    print(f"Monte‑Carlo summary written to {out_csv}")
else:
    print("No data collected.")
