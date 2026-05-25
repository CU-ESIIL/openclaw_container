#!/usr/bin/env python3
"""Run the stochastic corridor simulation (Node.js) and stream its CSV output
directly to a Parquet file.

The Node script `scripts/simulate_corridor_population_dynamics.js` writes a CSV
file `analysis/urban_wildlife_corridors/simulation_summary.csv`.  This wrapper
executes the Node script, waits for completion, then reads the generated CSV and
writes it to Parquet using pyarrow.  The CSV is retained for backwards
compatibility, but the primary artifact is the Parquet file.
"""
import subprocess, os, sys
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

# Paths
node_script = os.path.join(os.path.dirname(__file__), "simulate_corridor_population_dynamics.js")
analysis_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "analysis", "urban_wildlife_corridors"))
csv_path = os.path.join(analysis_dir, "simulation_summary.csv")
parquet_path = os.path.join(analysis_dir, "simulation_summary.parquet")

# Ensure analysis directory exists
os.makedirs(analysis_dir, exist_ok=True)

# Run the Node simulation
print("Running Node simulation...")
proc = subprocess.run(["node", node_script], cwd=os.path.dirname(node_script))
if proc.returncode != 0:
    print(f"Node script failed with exit code {proc.returncode}", file=sys.stderr)
    sys.exit(1)

# Verify CSV was produced
if not os.path.exists(csv_path):
    print(f"Expected CSV output not found at {csv_path}", file=sys.stderr)
    sys.exit(1)

# Load CSV and write Parquet
print(f"Loading CSV from {csv_path}")
df = pd.read_csv(csv_path)
print(f"Writing Parquet to {parquet_path}")
table = pa.Table.from_pandas(df)
pq.write_table(table, parquet_path)
print("Parquet generation complete.")
