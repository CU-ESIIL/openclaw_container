#!/usr/bin/env python3
"""Download Sentinel‑2 Level‑2A tiles and compute NDVI.

This script prefers streaming remote JPEG2000 bands via GDAL/VSICURL when the
``--stream`` flag is set.  If streaming is not requested, the bands are
temporarily downloaded to disk.

Typical usage:
  python scripts/download_ndvi_sentinel2.py \
        --tile T31TFJ \
        --date 2023-06-15 \
        --output data/derived/ndvi.tif \
        [--stream] [--crs EPSG:4326] [--metadata]

The resulting GeoTIFF contains a single NDVI band with nodata handling and
optional CRS reprojection and acquisition‑date metadata.
"""

import argparse
import os
import sys
import rasterio
import rasterio.warp
import numpy as np
import tempfile
import urllib.request

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def build_band_url(tile: str, date: str, band: str) -> str:
    """Construct the AWS URL for a Sentinel‑2 band.
    ``tile`` should be in the form ``T31TFJ`` (UTM zone 31, grid T, subgrid FJ).
    ``band`` is ``B04`` (red) or ``B08`` (NIR).
    """
    if not tile.startswith('T') or len(tile) < 5:
        raise ValueError('Tile must be like T31TFJ (e.g., T31TFJ)')
    zone = tile[1:3]
    grid = tile[3]
    subgrid = tile[4:]
    base_url = f"https://sentinel-s2-l2a.s3.amazonaws.com/tiles/{zone}/{grid}/{subgrid}/{date}/0"
    return f"{base_url}/{band}.jp2"

def download_band(url: str, out_path: str):
    """Download a band from ``url`` to ``out_path`` using urllib."""
    urllib.request.urlretrieve(url, out_path)

def compute_ndvi(red_src_path: str, nir_src_path: str, out_path: str,
                target_crs: str = None, add_metadata: bool = False):
    """Read red and NIR bands, compute NDVI, and write to ``out_path``.
    ``target_crs`` – EPSG code (e.g., ``EPSG:4326``) to reproject the output.
    ``add_metadata`` – if True, include ``ACQUISITION_DATE`` tag if present.
    """
    with rasterio.open(red_src_path) as red_src, rasterio.open(nir_src_path) as nir_src:
        red = red_src.read(1).astype('float32')
        nir = nir_src.read(1).astype('float32')
        # Mask nodata values
        mask = np.ones_like(red, dtype=bool)
        if red_src.nodata is not None:
            mask &= red != red_src.nodata
        if nir_src.nodata is not None:
            mask &= nir != nir_src.nodata
        ndvi = np.full(red.shape, np.nan, dtype='float32')
        ndvi[mask] = (nir[mask] - red[mask]) / (nir[mask] + red[mask] + 1e-6)

        profile = red_src.profile
        profile.update(
            dtype=rasterio.float32,
            count=1,
            compress='lzw',
            nodata=np.nan,
        )
        if target_crs:
            profile.update(crs=target_crs)
        else:
            profile.update(crs=red_src.crs)

        with rasterio.open(out_path, 'w', **profile) as dst:
            dst.write(ndvi, 1)
            if add_metadata:
                # Try to copy acquisition date from source tags if available.
                acq_date = red_src.tags().get('DATE_ACQUIRED') or red_src.tags().get('ACQUISITION_DATE')
                if acq_date:
                    dst.update_tags(ACQUISITION_DATE=acq_date)

# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description='Download Sentinel‑2 bands and compute NDVI')
    parser.add_argument('--tile', required=True, help='Sentinel‑2 tile identifier, e.g., T31TFJ')
    parser.add_argument('--date', required=True, help='Acquisition date YYYY-MM-DD')
    parser.add_argument('--output', required=True, help='Output NDVI GeoTIFF path')
    parser.add_argument('--stream', action='store_true', help='Stream remote bands via GDAL/VSICURL instead of downloading')
    parser.add_argument('--crs', default=None, help='Target CRS for output (e.g., EPSG:4326). If omitted, keeps source CRS.')
    parser.add_argument('--metadata', action='store_true', help='Include acquisition date as metadata tag')
    args = parser.parse_args()

    os.makedirs(os.path.dirname(args.output), exist_ok=True)

    red_url = build_band_url(args.tile, args.date, 'B04')
    nir_url = build_band_url(args.tile, args.date, 'B08')

    if args.stream:
        # Rasterio can open remote URLs via VSICURL if GDAL is compiled with it.
        compute_ndvi(red_url, nir_url, args.output, target_crs=args.crs, add_metadata=args.metadata)
        print(f'NDVI streamed and written to {args.output}')
        return

    # Fallback: download to temporary files first.
    with tempfile.TemporaryDirectory() as tmpdir:
        red_path = os.path.join(tmpdir, 'B04.jp2')
        nir_path = os.path.join(tmpdir, 'B08.jp2')
        try:
            download_band(red_url, red_path)
            download_band(nir_url, nir_path)
        except Exception as e:
            sys.stderr.write(f'Failed to download bands: {e}\n')
            sys.exit(1)
        compute_ndvi(red_path, nir_path, args.output, target_crs=args.crs, add_metadata=args.metadata)
        print(f'NDVI written to {args.output}')

if __name__ == '__main__':
    main()
