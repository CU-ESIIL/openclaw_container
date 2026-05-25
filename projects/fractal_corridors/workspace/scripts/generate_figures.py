#!/usr/bin/env python3
"""Generate manuscript figures from simulation summary CSV.

Creates simple, colour‑blind‑friendly PNG figures using matplotlib.
Figures are saved in ``figures/urban_wildlife_corridors/``.
"""

import pathlib
import pandas as pd
import matplotlib.pyplot as plt

# Settings for reproducibility and style
plt.style.use('seaborn-v0_8-whitegrid')

# Paths (prefer Parquet for speed)
fig_dir = pathlib.Path('figures/urban_wildlife_corridors')
fig_dir.mkdir(parents=True, exist_ok=True)

csv_path = pathlib.Path('analysis/urban_wildlife_corridors/simulation_summary.csv')
parquet_path = csv_path.with_suffix('.parquet')
if parquet_path.exists():
    df = pd.read_parquet(parquet_path)
else:
    df = pd.read_csv(csv_path)
    # Write Parquet for future fast reads
    df.to_parquet(parquet_path, index=False)
    print('Created Parquet for faster future reads:', parquet_path)

# Helper to save figure
def save(fig, name):
    out_path = fig_dir / f"{name}.png"
    fig.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close(fig)

# 1. Total corridor length by geometry and scenario
fig, ax = plt.subplots(figsize=(6,4))
length_df = df[df['metric']=='total_corridor_length']
ax.bar(length_df['geometry'], length_df['mean'], color='steelblue')
# Note: hue not shown due to simplified plot
ax.set_ylabel('Mean total length')
ax.set_title('Total Corridor Length')
save(fig, 'total_corridor_length')

# 2. Persistent species per length
fig, ax = plt.subplots(figsize=(6,4))
pps_df = df[df['metric']=='persistent_species_per_length']
ax.bar(pps_df['geometry'], pps_df['mean'], color='seagreen')
# Note: hue not shown due to simplified plot
ax.set_ylabel('Species per length')
ax.set_title('Persistent Species per Corridor Length')
save(fig, 'species_per_length')

# 3. Final mean occupancy
fig, ax = plt.subplots(figsize=(6,4))
occ_df = df[df['metric']=='final_mean_occupancy']
ax.bar(occ_df['geometry'], occ_df['mean'], color='salmon')
# Note: hue not shown due to simplified plot
ax.set_ylabel('Mean occupancy')
ax.set_title('Final Mean Occupancy')
save(fig, 'final_mean_occupancy')

print('Figures generated in', fig_dir)
