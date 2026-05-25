#!/usr/bin/env python3
"""Generate experiment grid from species traits, run simulations, and save results.

Steps:
1. Load data/derived/species_traits.json and extract unique kernel values.
2. Write them to data/experiment_grid.json as a list of objects: [{"kernel": value}, ...]
3. For each kernel, modify scripts/simulate_corridor_population_dynamics.js to set kernelMin and kernelMax.
4. Run the Node simulation.
5. Read the generated summary (parquet if present, else CSV) and compute the mean of the `final_mean_occupancy` metric.
6. Collect results and write to analysis/urban_wildlife_corridors/experiment_results.parquet.
7. Log progress to logs/experiment_run.log.
"""

import json
import pathlib
import subprocess
import pandas as pd
import logging
import sys
import re

# Setup paths
BASE_DIR = pathlib.Path.cwd()
SPECIES_TRAITS_PATH = BASE_DIR / "data" / "derived" / "species_traits.json"
GRID_PATH = BASE_DIR / "data" / "experiment_grid.json"
JS_PATH = BASE_DIR / "scripts" / "simulate_corridor_population_dynamics.js"
ORIG_JS_CONTENT = JS_PATH.read_text()
ANALYSIS_DIR = BASE_DIR / "analysis" / "urban_wildlife_corridors"
RESULT_PARQUET = ANALYSIS_DIR / "experiment_results.parquet"
LOG_PATH = BASE_DIR / "logs" / "experiment_run.log"

# Ensure directories exist
ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.FileHandler(LOG_PATH), logging.StreamHandler(sys.stdout)],
)

def load_kernels():
    try:
        traits = json.loads(SPECIES_TRAITS_PATH.read_text())
    except Exception as e:
        logging.error(f"Failed to read species traits: {e}")
        sys.exit(1)
    kernels = sorted({round(item["kernel"], 5) for item in traits if "kernel" in item})
    return kernels

def write_grid(kernels):
    grid = [{"kernel": k} for k in kernels]
    GRID_PATH.write_text(json.dumps(grid, indent=2))
    logging.info(f"Wrote experiment grid with {len(kernels)} kernels to {GRID_PATH}")

def run_simulation_for_kernel(k):
    # Modify JS content for the given kernel (both min and max)
    content = ORIG_JS_CONTENT
    content = re.sub(r"kernelMin:\s*[^,]+,", f"kernelMin: {k},", content)
    content = re.sub(r"kernelMax:\s*[^,]+,", f"kernelMax: {k},", content)
    JS_PATH.write_text(content)
    # Execute Node simulation
    try:
        subprocess.run(["node", str(JS_PATH)], check=True, timeout=300)
        logging.info(f"Simulation completed for kernel {k}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Simulation failed for kernel {k}: {e}")
        return None
    except subprocess.TimeoutExpired:
        logging.error(f"Simulation timed out for kernel {k}")
        return None
    # Load summary and compute mean occupancy
    summary_parquet = ANALYSIS_DIR / "simulation_summary.parquet"
    summary_csv = ANALYSIS_DIR / "simulation_summary.csv"
    if summary_parquet.exists():
        df = pd.read_parquet(summary_parquet)
    elif summary_csv.exists():
        df = pd.read_csv(summary_csv)
    else:
        logging.error(f"No summary file found after kernel {k} run")
        return None
    occ = df[df["metric"] == "final_mean_occupancy"]["mean"]
    mean_occ = float(occ.mean()) if not occ.empty else None
    return {"kernel": k, "mean_occupancy": mean_occ}

def main():
    kernels = load_kernels()
    write_grid(kernels)
    results = []
    for k in kernels:
        res = run_simulation_for_kernel(k)
        if res:
            results.append(res)
    # Restore original JS file
    JS_PATH.write_text(ORIG_JS_CONTENT)
    if results:
        df_res = pd.DataFrame(results)
        df_res.to_parquet(RESULT_PARQUET, index=False)
        logging.info(f"Written results parquet with {len(results)} rows to {RESULT_PARQUET}")
    else:
        logging.warning("No simulation results were collected.")

if __name__ == "__main__":
    main()
