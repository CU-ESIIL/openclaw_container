#!/usr/bin/env python3
"""Run a sweep over kernel (dispersal distance) values and plot occupancy.
The script edits `scripts/simulate_corridor_population_dynamics.js` to set
`kernelMin` and `kernelMax` (and keeps a low dispersal rate), runs the
simulation, extracts the mean `final_mean_occupancy` across all geometries
and scenarios, and produces a line plot.
"""
import pathlib, re, subprocess, shutil, json, sys
import pandas as pd
import matplotlib.pyplot as plt

JS_PATH = pathlib.Path('scripts/simulate_corridor_population_dynamics.js')
ORIG_CONTENT = JS_PATH.read_text()

# Sweep kernel values (min=max for simplicity)
kernel_vals = [round(x,3) for x in [i/1000 for i in range(1,21)]]  # 0.001 to 0.020 step 0.001
# Fixed low dispersal rates (min/max)
disp_min, disp_max = 0.001, 0.005

results = []

for k in kernel_vals:
    # Create modified content
    content = ORIG_CONTENT
    # replace dispersalRateMin/Max
    content = re.sub(r"dispersalRateMin:\s*[^,]+,", f"dispersalRateMin: {disp_min},", content)
    content = re.sub(r"dispersalRateMax:\s*[^,]+,", f"dispersalRateMax: {disp_max},", content)
    # replace kernelMin/Max
    content = re.sub(r"kernelMin:\s*[^,]+,", f"kernelMin: {k},", content)
    content = re.sub(r"kernelMax:\s*[^,]+,", f"kernelMax: {k},", content)
    # write temporary file
    JS_PATH.write_text(content)
    # Run simulation with reduced replicates/steps for quick sweep
    # Temporarily adjust PARAMS in the JS file before execution
    # Replace replicates, maxSteps, dispersal rates, kernel, patches, and set a high distance mortality
    content_mod = re.sub(r"replicates:\s*[^,]+,", "replicates: 20,", content)
    content_mod = re.sub(r"maxSteps:\s*[^,]+,", "maxSteps: 2000,", content_mod)
    content_mod = re.sub(r"dispersalRateMin:\s*[^,]+,", "dispersalRateMin: 0.0001,", content_mod)
    content_mod = re.sub(r"dispersalRateMax:\s*[^,]+,", "dispersalRateMax: 0.0005,", content_mod)
    # kernel already set above; also enforce high distance mortality for all scenarios
    content_mod = re.sub(r"dispersalMortalityPerDistance:\s*[^,]+,", "dispersalMortalityPerDistance: 0.30,", content_mod)
    JS_PATH.write_text(content_mod)
    try:
        subprocess.run(['node', str(JS_PATH)], check=True, timeout=300)
    except subprocess.CalledProcessError as e:
        print('Simulation failed for kernel', k, file=sys.stderr)
        continue
    # Restore full original after each run (handled later)
    # Load summary (prefer Parquet for speed)
    summary_parquet = pathlib.Path('analysis/urban_wildlife_corridors/simulation_summary.parquet')
    summary_csv = pathlib.Path('analysis/urban_wildlife_corridors/simulation_summary.csv')
    if summary_parquet.exists():
        df = pd.read_parquet(summary_parquet)
    else:
        df = pd.read_csv(summary_csv)
        # Write Parquet for future fast reads
        df.to_parquet(summary_parquet, index=False)
        print('Created Parquet for faster future reads:', summary_parquet)
    # Filter final_mean_occupancy metric
    occ = df[df['metric']=='final_mean_occupancy']['mean']
    mean_occ = occ.mean()
    results.append({'kernel':k, 'mean_occupancy':mean_occ})
    print(f'Kernel {k}: mean occupancy {mean_occ:.3f}')

# Restore original JS file
JS_PATH.write_text(ORIG_CONTENT)

# Save results CSV
out_csv = pathlib.Path('analysis/urban_wildlife_corridors/occupancy_sweep.csv')
pd.DataFrame(results).to_csv(out_csv, index=False)

# Plot
plt.figure(figsize=(6,4))
plt.plot([r['kernel'] for r in results], [r['mean_occupancy'] for r in results], marker='o')
plt.xlabel('Dispersal kernel (fraction of edge length)')
plt.ylabel('Mean final occupancy')
plt.title('Occupancy vs. Dispersal distance')
plt.grid(True)
fig_path = pathlib.Path('figures/urban_wildlife_corridors/occupancy_vs_kernel.png')
fig_path.parent.mkdir(parents=True, exist_ok=True)
plt.savefig(fig_path, dpi=300, bbox_inches='tight')
print('Figure saved to', fig_path)
