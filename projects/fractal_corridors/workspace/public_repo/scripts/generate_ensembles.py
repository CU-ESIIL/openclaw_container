#!/usr/bin/env python3
"""Generate stochastic network ensembles preserving total effective cost or degree distribution.

Workflow:
  1. Load patch centroids from ``data/derived/patches.geojson``.
  2. Load the effective‑cost matrix from ``data/derived/cost_matrix.npy``.
  3. Build a full graph (NetworkX) where edge weights are the effective costs.
  4. For each ensemble member:
       a. Copy the graph.
       b. Apply ``networkx.double_edge_swap`` to preserve the degree sequence
          (or a custom swap that preserves total cost). The number of swaps
          is set to 10 × |E| by default.
       c. Export the resulting adjacency list (nodes + edges with weights)
          as a JSON file ``data/derived/networks/ensemble_<id>.json``.

The script creates a ``networks`` subdirectory if it does not exist.

Dependencies: networkx, numpy, geopandas, json
"""

import os
import json
import numpy as np
import geopandas as gpd
import networkx as nx

# ---------------------------------------------------------------------------
# Configuration – adjust as needed
# ---------------------------------------------------------------------------
PATCH_GEOJSON = "data/derived/patches.geojson"
COST_MATRIX_NPY = "data/derived/cost_matrix.npy"
OUTPUT_DIR = "data/derived/networks"
NUM_ENSEMBLES = 30  # number of stochastic realizations per treatment
SWAPS_PER_EDGE = 10  # multiplier for number of double_edge_swap operations

# ---------------------------------------------------------------------------
def load_patches():
    gdf = gpd.read_file(PATCH_GEOJSON)
    # Ensure point geometry
    if not all(gdf.geometry.type == "Point"):
        gdf["geometry"] = gdf.geometry.centroid
    return gdf

def build_base_graph(cost_mat):
    n = cost_mat.shape[0]
    G = nx.Graph()
    G.add_nodes_from(range(n))
    # Add edges for all finite costs (avoid self‑loops)
    for i in range(n):
        for j in range(i+1, n):
            weight = float(cost_mat[i, j])
            if np.isfinite(weight):
                G.add_edge(i, j, weight=weight)
    return G

def export_graph(G, path):
    data = {
        "nodes": list(G.nodes()),
        "edges": [
            {"source": u, "target": v, "weight": d["weight"]}
            for u, v, d in G.edges(data=True)
        ]
    }
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    patches = load_patches()
    cost_mat = np.load(COST_MATRIX_NPY)
    base_G = build_base_graph(cost_mat)

    for idx in range(1, NUM_ENSEMBLES + 1):
        # Preserve degree distribution (default double_edge_swap)
        G = base_G.copy()
        num_swaps = SWAPS_PER_EDGE * G.number_of_edges()
        nx.double_edge_swap(G, nswap=num_swaps, max_tries=num_swaps * 10)
        out_path = os.path.join(OUTPUT_DIR, f"ensemble_{idx:02d}.json")
        export_graph(G, out_path)
        print(f"Ensemble {idx}/{NUM_ENSEMBLES} written to {out_path}")

if __name__ == "__main__":
    main()
