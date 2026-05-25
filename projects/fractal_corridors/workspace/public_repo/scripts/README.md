# Scripts

## download_ndvi_sentinel2.py

`download_ndvi_sentinel2.py` downloads Sentinel‑2 Level‑2A imagery for a specified tile and date, computes NDVI, and saves it to `data/derived/ndvi.tif`. The script is invoked via the Makefile target `download_ndvi` or directly:

```bash
python scripts/download_ndvi_sentinel2.py --tile T31TFJ --date 2023-06-15
```

It requires GDAL/rasterio (already available) and handles missing data gracefully.

Use this directory for initialization scripts, smoke tests, reproducible workflows, and utility scripts.

Scripts should be idempotent where feasible and should document required inputs, outputs, and side effects.
