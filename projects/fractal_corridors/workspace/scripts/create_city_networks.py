#!/usr/bin/env python3
"""Create synthetic city network data for demonstration.
We define three example cities with simple bounding boxes and generate
random green‑space patches and four corridor geometries (nearest‑web,
minimum‑spanning‑tree, dendritic, hybrid). The script also computes a
*tree‑ness* metric (MST length / total edge length) and writes it to
`city_metrics.json`.
"""
import json, pathlib, random
import networkx as nx
import geopandas as gpd
from shapely.geometry import Point, LineString

# Define three example cities (bbox in EPSG:4326)
cities = {
    "London": {"bbox": (-0.15, 51.48, -0.10, 51.52)},
    "Paris": {"bbox": (2.30, 48.85, 2.35, 48.90)},
    "Montreal": {"bbox": (-73.65, 45.45, -73.50, 45.60)}
}

out_dir = pathlib.Path('data/derived')
out_dir.mkdir(parents=True, exist_ok=True)
metrics = {}

for name, info in cities.items():
    minx, miny, maxx, maxy = info['bbox']
    # generate a variable number of random green‑space centroids (30 for demo cities, 2000 for Montreal)
    patches = []
    num_patches = 30
    if name == "Montreal":
        num_patches = 2000
    for i in range(num_patches):
        x = random.uniform(minx, maxx)
        y = random.uniform(miny, maxy)
        patches.append(Point(x, y))
    gdf = gpd.GeoDataFrame({'city':[name]*num_patches}, geometry=patches, crs='EPSG:4326')
    city_dir = out_dir / name
    city_dir.mkdir(parents=True, exist_ok=True)
    gdf.to_file(city_dir / 'patches.geojson', driver='GeoJSON')

    # build a fully connected graph (complete) with Euclidean distances
    G = nx.complete_graph(len(patches))
    pos = {i: (pt.x, pt.y) for i, pt in enumerate(patches)}
    for u, v in G.edges():
        x1, y1 = pos[u]
        x2, y2 = pos[v]
        dist = ((x1 - x2)**2 + (y1 - y2)**2) ** 0.5
        G.edges[u, v]['weight'] = dist

    # Minimum spanning tree
    mst = nx.minimum_spanning_tree(G, weight='weight')
    mst_len = sum(d['weight'] for _,_,d in mst.edges(data=True))
    total_len = sum(d['weight'] for _,_,d in G.edges(data=True))
    tree_ness = mst_len / total_len if total_len>0 else 0
    metrics[name] = {'tree_ness': tree_ness}

    # Save geometries as GeoJSON (edges only)
    def edges_to_gdf(graph, filename):
        lines = []
        for u, v in graph.edges():
            p1 = pos[u]
            p2 = pos[v]
            lines.append(LineString([p1, p2]))
        gdf_edges = gpd.GeoDataFrame(geometry=lines, crs='EPSG:4326')
        gdf_edges.to_file(city_dir / filename, driver='GeoJSON')
    edges_to_gdf(G, 'nearest_web.geojson')
    edges_to_gdf(mst, 'mst.geojson')
    # Dendritic: take MST and add a few random extra edges
    dend = mst.copy()
    extra = random.sample(list(G.edges()), k=10)
    dend.add_edges_from(extra)
    edges_to_gdf(dend, 'dendritic.geojson')
    # Hybrid: combine dendritic and a few shortcuts
    hybrid = dend.copy()
    shortcuts = random.sample(list(G.edges()), k=5)
    hybrid.add_edges_from(shortcuts)
    edges_to_gdf(hybrid, 'hybrid.geojson')

# write metrics json
with open('city_metrics.json', 'w') as f:
    json.dump(metrics, f, indent=2)
print('City networks and metrics generated.')
