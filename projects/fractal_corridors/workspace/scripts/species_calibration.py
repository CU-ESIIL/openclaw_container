#!/usr/bin/env python3
"""Placeholder for species‑specific movement parameter calibration.

This script is intended to:
1. Load species trait data (e.g., from GBIF or a local JSON/CSV).
2. Extract dispersal distance estimates for a set of representative taxa (small mammals, medium carnivores, birds).
3. Fit a simple allometric relationship between body mass and median dispersal distance.
4. Write a calibration table (`species_movement_calibration.csv`) that can be consumed by the simulation pipeline.

The actual implementation will require domain‑specific data sources; for now the script generates a dummy CSV with example values.
"""
import csv
import os
from pathlib import Path

# Output path – placed under analysis for easy downstream access
output_dir = Path('analysis') / 'species_calibration'
output_dir.mkdir(parents=True, exist_ok=True)
output_file = output_dir / 'species_movement_calibration.csv'

# Dummy data – replace with real trait extraction later
rows = [
    ['species','body_mass_g','median_dispersal_km','dispersal_sigma_km'],
    ['Eastern Cottontail','1200','2.5','0.8'],
    ['Red Fox','6000','5.0','1.5'],
    ['American Robin','120','1.2','0.4'],
]

with open(output_file, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(rows)

print(f"Species calibration table written to {output_file}")
