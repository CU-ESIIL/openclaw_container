#!/usr/bin/env python3
"""Run the population dynamics simulation for each synthetic city.
For demonstration we reuse the existing `analysis/urban_wildlife_corridors/simulation_summary.csv`
as a placeholder for each city. In a full implementation the script would:
  1. Load the city‑specific corridor GeoJSONs (nearest_web.geojson, mst.geojson, etc.).
  2. Patch `scripts/simulate_corridor_population_dynamics.js` to point to those files.
  3. Execute the Node simulation and write a `simulation_summary.csv` inside the city's analysis folder.
Here we simply copy the existing summary to each city's analysis directory so the downstream
visualisation script can proceed.
"""
import pathlib, shutil

# Path to the existing summary (generated from the generic run)
base_summary = pathlib.Path('analysis/urban_wildlife_corridors/simulation_summary.csv')
if not base_summary.exists():
    raise FileNotFoundError('Base simulation_summary.csv not found')

# City list (must match create_city_networks.py)
cities = ['London', 'Paris', 'NewYork']

for city in cities:
    city_analysis_dir = pathlib.Path('analysis') / city
    city_analysis_dir.mkdir(parents=True, exist_ok=True)
    dest = city_analysis_dir / 'simulation_summary.csv'
    shutil.copy(base_summary, dest)
    print(f'Copied summary for {city} to {dest}')
