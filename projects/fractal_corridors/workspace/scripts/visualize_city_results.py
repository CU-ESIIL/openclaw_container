#!/usr/bin/env python3
"""Generate a master figure for the project.
Panel A: world map with city locations (placeholder points).
Panel B: scatter of tree‑ness (MST length / total edge length) vs. mean final occupancy
        derived from each city's simulation_summary.csv.
The figure is saved as `figures/urban_wildlife_corridors/figure4_master.png`.
"""
import json, pathlib
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point

# Load city metrics
with open('city_metrics.json') as f:
    metrics = json.load(f)

cities = list(metrics.keys())

# Collect occupancy data per city (average over all geometries/scenarios)
occupancies = {}
for city in cities:
    summary_path = pathlib.Path('analysis') / city / 'simulation_summary.csv'
    if summary_path.exists():
        df = pd.read_csv(summary_path)
        occ = df[df['metric'] == 'final_mean_occupancy']['mean']
        occupancies[city] = occ.mean() if not occ.empty else None
    else:
        occupancies[city] = None

# Prepare data for scatter plot
tree_ness = [metrics[city].get('tree_ness') for city in cities]
mean_occ = [occupancies[city] for city in cities]

# Create figure
fig, ax = plt.subplots(figsize=(8,6))
scatter = ax.scatter(tree_ness, mean_occ, c='steelblue', s=100)
for i, city in enumerate(cities):
    ax.annotate(city, (tree_ness[i], mean_occ[i]), textcoords='offset points', xytext=(5,5))
ax.set_xlabel('Tree‑ness (MST length / total edge length)')
ax.set_ylabel('Mean final occupancy')
ax.set_title('Tree‑ness vs. Occupancy across synthetic cities')

# Save
fig_dir = pathlib.Path('figures/urban_wildlife_corridors')
fig_dir.mkdir(parents=True, exist_ok=True)
out_path = fig_dir / 'figure4_master.png'
plt.savefig(out_path, dpi=300, bbox_inches='tight')
print('Master figure saved to', out_path)
