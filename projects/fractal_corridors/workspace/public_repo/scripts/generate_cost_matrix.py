#!/usr/bin/env python3
"""Generate an effective-cost matrix for the landscape.

The matrix combines:
  1. Euclidean distance between patch centroids.
  2. Road‑density resistance (from a raster layer).
  3. Species‑specific crossing penalties (provided as a JSON lookup).

Outputs a NumPy ``.npy`` file ``data/derived/cost_matrix.npy`` that can be
read by the JavaScript simulation (or any downstream Python model).

Dependencies: numpy, rasterio, geopandas, shapely
"""

import os
import json
import numpy as np
import rasterio
import geopandas as gpd
from shapely.geometry import Point
from scipy.spatial import distance_matrix

# ---------------------------------------------------------------------------
# Configuration – adjust paths as needed
# ---------------------------------------------------------------------------
PATCH_GEOJSON = "data/derived/patches.geojson"
ROAD_DENSITY_RASTER = "data/derived/road_density.tif"  # raster of km per km^2
SPECIES_PENALTIES_JSON = "data/derived/species_penalties.json"  # e.g., {"amphibian": 1.5, "bird": 0.8}
OUT_NPY = "data/derived/cost_matrix.npy"

# Parameters for weighting the components (tune as needed)
ALPHA_EUCLIDEAN = 1.0
ALPHA_ROAD = 0.5  # scaling factor for road resistance
ALPHA_SPECIES = 1.0  # will be applied later per species

# ---------------------------------------------------------------------------
def load_patches():
    gdf = gpd.read_file(PATCH_GEOJSON)
    # Ensure geometries are points; if polygons, take centroids
    if not all(gdf.geometry.type == "Point"):
        gdf["geometry"] = gdf.geometry.centroid
    return gdf

def compute_euclidean(patch_gdf):
    coords = np.stack([patch_gdf.geometry.x, patch_gdf.geometry.y], axis=1)
    return distance_matrix(coords, coords)

def sample_road_resistance(patch_gdf, raster_path):
    # Sample the raster value at each patch location (average over a small window)
    with rasterio.open(raster_path) as src:
        values = []
        for geom in patch_gdf.geometry:
            x, y = geom.x, geom.y
            row, col = src.index(x, y)
            # read a 3x3 window around the point to smooth out noise
            window = src.read(1, window=((max(row-1,0), min(row+2, src.height)),
                                         (max(col-1,0), min(col+2, src.width))))
            # ignore nodata
            valid = window[window != src.nodata]
            values.append(float(valid.mean()) if valid.size > 0 else 0.0)
    return np.array(values)

def build_cost_matrix(euc, road_resist):
    # Euclidean component scaled
    cost = ALPHA_EUCLIDEAN * euc
    # Add road resistance as an additive term proportional to the average
    # resistance of the two endpoints.
    road_mat = (road_resist[:, None] + road_resist[None, :]) / 2.0
    cost += ALPHA_ROAD * road_mat
    return cost

def main():
    if not os.path.exists(PATCH_GEOJSON):
        raise FileNotFoundError(f"Patch file not found: {PATCH_GEOJSON}")
    patches = load_patches()
    euclid = compute_euclidean(patches)
    road_resist = sample_road_resistance(patches, ROAD_DENSITY_RASTER)
    cost_mat = build_cost_matrix(euclid, road_resist)
    # Save the matrix
    os.makedirs(os.path.dirname(OUT_NPY), exist_ok=True)
    np.save(OUT_NPY, cost_mat)
    print(f"Effective cost matrix written to {OUT_NPY}")

if __name__ == "__main__":
    main()
