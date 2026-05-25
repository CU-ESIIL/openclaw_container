# Cubedynamics – Data Scientist Notes

## Overview
- **Cubedynamics** is a Python library that provides a *composable grammar* for working with **spatiotemporal data cubes**.  It builds on the **xarray** data model, allowing us to treat raster time‑series (e.g., satellite NDVI, climate variables) as a single, multi‑dimensional array.
- The library is intentionally **modular**: it composes low‑level operations (reprojection, resampling, masking, aggregation) into higher‑level pipelines using the pipe operator (`|`).  This mirrors functional programming styles and makes complex workflows easier to read and reproduce.

## Core Concepts
1. **Data Cube** – An `xarray.DataArray` or `xarray.Dataset` with at least three dimensions: `time`, `x` (longitude), and `y` (latitude).  Cubedynamics treats the cube as the fundamental object.
2. **Operations (Grammar Elements)** – Functions such as `reproject`, `resample`, `mask`, `apply`, `groupby`, etc., that accept a cube and return a transformed cube.  Operators can be chained:
   ```python
   cube = (cube
           | reproject("EPSG:3857")
           | mask(band="NDVI", threshold=0.3)
           | temporal_mean())
   ```
3. **Lazy Execution** – By default Cubedynamics works with **Dask** arrays, so operations are lazy; computation only occurs when you call `.compute()` or write to disk.  This enables processing of very large datasets (e.g., whole‑Earth Sentinel‑2 time series) without holding everything in memory.
4. **STAC Integration** – The library can ingest STAC collections via `stackstac` or `pystac-client`, allowing us to pull remote assets directly (streaming) and avoid full downloads.  This is the mechanism we intend to use for NDVI streaming.

## Typical Workflow for NDVI Patch Generation
```
# 1. Load Sentinel‑2 NDVI tiles as a virtual cube (no download)
from cubedynamics import Cube
from cubedynamics.sources import StacSource

source = StacSource(collection="sentinel-2-l2a",
                    bounds=[lon_min, lat_min, lon_max, lat_max],
                    datetime="2023-06-15/2023-06-15",
                    assets=["B04", "B08"])  # Red & NIR

cube = Cube.from_source(source)

# 2. Compute NDVI on‑the‑fly using lazy arithmetic
ndvi = (cube.select(bands=["B04", "B08"]).apply(
          lambda red, nir: (nir - red) / (nir + red + 1e-6),
          dims=["band"],
          name="NDVI"))

# 3. Apply a threshold and label connected components
vegetation = ndvi > 0.3
labeled = vegetation.label(connectivity=2)   # 8‑connectivity

# 4. Vectorize patches (still lazy) – returns a GeoDataFrame
patches = labeled.vectorize(min_area=0.1)   # ha

# 5. Write output (trigger compute)
patches.to_file("data/derived/patches.geojson")
```

## Why It Helps Our Project
- **Streaming** – No intermediate `.jp2` files; data is read directly from the public AWS Sentinel‑2 bucket via VSICURL (handled internally by `stackstac`).
- **Scalability** – Dask chunks the cube by spatial tiles and time, which means we can process whole regions or multi‑date mosaics on modest hardware.
- **Reproducibility** – The entire workflow is a pure function of input parameters (tile, date, threshold).  Saving the script together with the environment (the `.venv` we created) gives a self‑contained pipeline.
- **Extensibility** – Once NDVI patches are available, we can easily plug in further analyses (e.g., time‑series extraction per patch, landscape metrics) using the same grammar.

## Open Questions / Action Items
- **Environment** – The current virtual environment is missing `rasterio`.  Install it (`.venv/bin/pip install rasterio`) to enable fallback local‑file handling for any non‑STAC assets.
- **Parameterisation** – Expose the NDVI threshold, minimum patch area, and target CRS as CLI arguments or environment variables (already done in `scripts/generate_patches_from_ndvi.py`).
- **Testing** – Run a quick sanity check on a small tile (e.g., `T31TFJ`) to ensure the `Cube` pipeline produces the expected number of patches.
- **Documentation** – Add a short section to `scripts/README.md` summarising the Cubedynamics‑based approach and linking to the official repo.

---
*These notes are intended for the Data Scientist role.  Keep them up‑to‑date as we iterate on the NDVI streaming workflow.*