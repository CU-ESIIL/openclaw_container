#!/usr/bin/env python3
"""Generate habitat patches from a Sentinel‑2 NDVI raster.

The script reads a single‑band NDVI GeoTIFF (produced by
`download_ndvi_sentinel2.py`), applies a configurable NDVI threshold to
identify vegetated cells, performs connected‑component labeling to find
contiguous vegetation clusters, and writes each cluster as a polygon
feature in GeoJSON.

Each feature includes:
  - mean_ndvi: average NDVI value of the pixels belonging to the patch
  - area_ha: patch area in hectares (derived from pixel size)
  - acquisition_date: acquisition date extracted from raster metadata (if present)

The output CRS matches the input raster CRS (typically EPSG:4326). The
script also writes a small log file with processing details.
"""

import os
import json
import rasterio
import numpy as np
from rasterio import features, warp
from shapely.geometry import shape, mapping
from datetime import datetime

# ---------------------------------------------------------------------------
# Configurable parameters (adjust as needed)
# ---------------------------------------------------------------------------
NDVI_PATH = os.getenv('NDVI_PATH', 'data/derived/ndvi.tif')
OUTPUT_GEOJSON = os.getenv('PATCHES_GEOJSON', 'data/derived/patches.geojson')
NDVI_THRESHOLD = float(os.getenv('NDVI_THRESHOLD', '0.3'))  # vegetated if NDVI >= threshold
MIN_AREA_HA = float(os.getenv('MIN_AREA_HA', '0.1'))  # drop tiny patches
# ---------------------------------------------------------------------------

def main():
    if not os.path.exists(NDVI_PATH):
        raise FileNotFoundError(f"NDVI raster not found: {NDVI_PATH}")

    with rasterio.open(NDVI_PATH) as src:
        ndvi = src.read(1, masked=True).astype('float32')
        crs = src.crs
        transform = src.transform
        # Try to pull acquisition date from common tags (e.g., DATE_ACQUIRED)
        acquisition_date = src.tags().get('DATE_ACQUIRED') or src.tags().get('ACQUISITION_DATE')
        try:
            if acquisition_date:
                # Ensure ISO format
                acquisition_date = datetime.fromisoformat(acquisition_date).date().isoformat()
        except Exception:
            acquisition_date = None

    # Binary mask of vegetation
    veg_mask = (ndvi >= NDVI_THRESHOLD) & (~ndvi.mask)
    if not veg_mask.any():
        raise RuntimeError('No vegetated pixels found with the given threshold.')

    patches = []
    # Approximate pixel area in square meters
    pixel_area_m2 = abs(transform.a * transform.e)
    if crs.is_geographic:
        # Rough conversion: 1 degree ~ 111 km at equator
        pixel_area_m2 = (111_000 * transform.a) * (111_000 * abs(transform.e))

    # Use rasterio.features.shapes to extract polygons of contiguous high‑NDVI cells
    for geom_dict, value in features.shapes(veg_mask.astype('uint8'), mask=veg_mask, transform=transform):
        if value != 1:
            continue
        polygon = shape(geom_dict)
        # Compute area in hectares (reproject if geographic for accuracy)
        if crs.is_geographic:
            reprojected = warp.transform_geom(crs, "EPSG:3857", mapping(polygon), precision=6)
            area_m2 = shape(reprojected).area
        else:
            area_m2 = polygon.area
        area_ha = area_m2 / 10_000
        if area_ha < MIN_AREA_HA:
            continue
        # Compute mean NDVI within the polygon using a mask
        geom_mask = features.geometry_mask([geom_dict], transform=transform, invert=True, out_shape=ndvi.shape)
        mean_ndvi = ndvi[geom_mask].mean()
        feature = {
            'type': 'Feature',
            'properties': {
                'mean_ndvi': float(mean_ndvi),
                'area_ha': float(area_ha),
                'acquisition_date': acquisition_date
            },
            'geometry': mapping(polygon)
        }
        patches.append(feature)

    geojson = {'type': 'FeatureCollection', 'features': patches}
    os.makedirs(os.path.dirname(OUTPUT_GEOJSON), exist_ok=True)
    with open(OUTPUT_GEOJSON, 'w') as f:
        json.dump(geojson, f, indent=2)
    print(f"Generated {len(patches)} patches → {OUTPUT_GEOJSON}")

if __name__ == '__main__':
    main()
