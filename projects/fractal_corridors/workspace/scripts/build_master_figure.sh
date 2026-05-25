#!/usr/bin/env bash
# Build the full master figure pipeline
set -e

echo "--- Creating city networks ---"
python3 scripts/create_city_networks.py

echo "--- Running city simulations (placeholder) ---"
python3 scripts/run_city_simulations.py

echo "--- Visualizing results and creating master figure ---"
python3 scripts/visualize_city_results.py

echo "Pipeline completed. Master figure is at figures/urban_wildlife_corridors/figure4_master.png"
