#!/usr/bin/env python3
"""Create a NDVI raster for a given bounding box.
If internet access to Sentinel‑2 is available, the script will download the
required Level‑2A tiles from the AWS public bucket, compute NDVI and write
`data/derived/ndvi.tif`.  If the download fails (e.g., no network), a synthetic
NDVI raster is generated instead so downstream steps can still run.
"""
import os, sys, pathlib, subprocess, json
import numpy as np
import rasterio
from rasterio.transform import from_bounds

# ---------------------------------------------------------------------
# Configuration – adjust the bounding box (EPSG:4326) for your study area.
# Example: small area around central London.
# ---------------------------------------------------------------------
BBOX = (-0.15, 51.48, -0.10, 51.52)  # (min_lon, min_lat, max_lon, max_lat)
RESOLUTION = 0.0001  # approx 10 m in degrees (very coarse for demo)
OUT_PATH = pathlib.Path('data/derived/ndvi.tif')

def download_sentinel_tile(bbox, dest_dir):
    """Attempt to download a Sentinel‑2 tile that intersects the bbox.
    Returns a list of local .tif paths for the red (B04) and NIR (B08) bands.
    Uses the AWS public HTTP endpoint.
    """
    # Simple heuristic: use a known tile that covers the bbox – here we pick
    # tile "31UFS" which contains London. In a real implementation you would
    # search the Sentinel tiling grid.
    tile = '31UFS'
    date = '2022-06-01'  # arbitrary recent date with Level‑2A data
    # Construct AWS URLs – the bucket layout is:
    # s3://sentinel-s2-l2a/tiles/{utm}/{grid}/{date}/0/\
    #   {band}_{resolution}.tif
    base = f'https://sentinel-s2-l2a.s3.amazonaws.com/tiles/{tile[:2]}/{tile[2:4]}/{tile[4:]}/{date}/0'
    urls = {
        'red': f'{base}/B04_10m.tif',
        'nir': f'{base}/B08_10m.tif',
    }
    local_paths = {}
    os.makedirs(dest_dir, exist_ok=True)
    for name, url in urls.items():
        fp = pathlib.Path(dest_dir) / f'{name}.tif'
        try:
            subprocess.run(['curl', '-fLs', url, '-o', str(fp)], check=True, timeout=30)
            local_paths[name] = fp
        except Exception as e:
            print(f'Failed to download {name} band: {e}', file=sys.stderr)
            return None
    return local_paths

def compute_ndvi(red_path, nir_path, out_path, bbox, res):
    with rasterio.open(red_path) as red_src, rasterio.open(nir_path) as nir_src:
        red = red_src.read(1).astype('float32')
        nir = nir_src.read(1).astype('float32')
        ndvi = (nir - red) / (nir + red + 1e-6)
        # Clip to bbox
        transform = from_bounds(*bbox, ndvi.shape[1], ndvi.shape[0])
        profile = red_src.profile.copy()
        profile.update({
            'dtype': 'float32',
            'count': 1,
            'compress': 'lzw',
            'transform': transform,
        })
        with rasterio.open(out_path, 'w', **profile) as dst:
            dst.write(ndvi, 1)

def generate_synthetic_ndvi(out_path, bbox, res):
    # Create a simple gradient + noise raster
    width = int((bbox[2] - bbox[0]) / res)
    height = int((bbox[3] - bbox[1]) / res)
    transform = from_bounds(*bbox, width, height)
    x = np.linspace(0, 1, width)
    y = np.linspace(0, 1, height)[:, None]
    ndvi = 0.4 + 0.2 * np.outer(y[:,0], x) + 0.1 * np.random.rand(height, width)
    profile = {
        'driver': 'GTiff',
        'dtype': 'float32',
        'count': 1,
        'height': height,
        'width': width,
        'crs': 'EPSG:4326',
        'transform': transform,
        'compress': 'lzw',
    }
    with rasterio.open(out_path, 'w', **profile) as dst:
        dst.write(ndvi.astype('float32'), 1)
    print(f'Synthetic NDVI written to {out_path}')

def main():
    tile_dir = pathlib.Path('tmp/sentinel_tiles')
    paths = download_sentinel_tile(BBOX, tile_dir)
    if paths:
        compute_ndvi(paths['red'], paths['nir'], OUT_PATH, BBOX, RESOLUTION)
        print(f'NDVI raster created at {OUT_PATH}')
    else:
        generate_synthetic_ndvi(OUT_PATH, BBOX, RESOLUTION)

if __name__ == '__main__':
    main()
