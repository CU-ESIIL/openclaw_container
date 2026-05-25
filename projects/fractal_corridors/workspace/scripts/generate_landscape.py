#!/usr/bin/env python3
"""Generate a heterogeneous landscape of 80‑120 habitat patches.

The script samples random points from an empirical raster (e.g., NDVI or land‑cover).
It extracts the raster value at each point (to serve as a proxy for habitat quality)
and writes the centroids to a GeoJSON file.

Required inputs (paths are relative to the repo root):
  data/derived/ndvi.tif            – raster used for sampling (any continuous raster works)
  data/derived/road_density.tif    – optional, used only for later cost‑matrix step

Outputs:
  data/derived/patches.geojson      – GeoJSON FeatureCollection of patch centroids

Usage (via Makefile target "generate_landscape"):
  python3 scripts/generate_landscape.py

Dependencies: numpy, rasterio, geopandas, shapely
"""

import os
import random
import json
import rasterio
import numpy as np
import geopandas as gpd
from shapely.geometry import Point

# ---------------------------------------------------------------------------
# Configuration – adjust these values to change the landscape size
# ---------------------------------------------------------------------------
NUM_PATCHES_MIN = 80
NUM_PATCHES_MAX = 120
# Random seed for reproducibility – can be overridden by env var
SEED = int(os.getenv("LANDSCAPE_SEED", "20260518"))
random.seed(SEED)
np.random.seed(SEED)

# Input raster – replace with the actual raster you intend to use
NDVI_RASTER = "data/derived/ndvi.tif"

# Output GeoJSON path
OUT_GEOJSON = "data/derived/patches.geojson"

# ---------------------------------------------------------------------------
def sample_points_from_raster(raster_path, n_points):
    """Randomly sample n_points from the valid (non‑nan) cells of a raster.
    Returns a list of (x, y, value) tuples in the raster's coordinate system.
    """
    with rasterio.open(raster_path) as src:
        band = src.read(1)
        mask = ~src.nodata == band if src.nodata is not None else np.isfinite(band)
        indices = np.argwhere(mask)
        if len(indices) == 0:
            raise RuntimeError(f"No valid cells found in {raster_path}")
        chosen = indices[np.random.choice(len(indices), size=n_points, replace=False)]
        pts = []
        for row, col in chosen:
            x, y = src.transform * (col + 0.5, row + 0.5)
            val = band[row, col]
            pts.append((x, y, float(val)))
        return pts

def main():
    n_patches = random.randint(NUM_PATCHES_MIN, NUM_PATCHES_MAX)
    print(f"Generating {n_patches} patches from {NDVI_RASTER}")
    pts = sample_points_from_raster(NDVI_RASTER, n_patches)

    # Build GeoDataFrame
    geometries = [Point(x, y) for x, y, _ in pts]
    values = [val for _, _, val in pts]
    gdf = gpd.GeoDataFrame({"habitat_quality": values}, geometry=geometries, crs="EPSG:4326")

    # Ensure output directory exists
    os.makedirs(os.path.dirname(OUT_GEOJSON), exist_ok=True)
    gdf.to_file(OUT_GEOJSON, driver="GeoJSON")
    print(f"Patch centroids written to {OUT_GEOJSON}")

if __name__ == "__main__":
    main()
