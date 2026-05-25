# Public AI‑Based Earth‑Observation Embeddings (No API Key Required)

## Overview
The following open‑data collections provide high‑dimensional, AI‑generated embeddings of satellite imagery. All can be accessed without authentication (no API keys) and are released under permissive licenses.

| Dataset | Embedding type / size | Data format | Direct access URL | License | Quick‑start usage note |
|---------|----------------------|------------|-------------------|---------|------------------------|
| **Google Satellite Embedding V1 (AlphaEarth Foundations)** | 64‑dimensional vectors, 10 m pixel resolution, annual snapshots (2017‑2025) | Cloud‑Optimized GeoTIFF (COG) – one file per year, each band = one embedding dimension (A00‑A63) | `s3://us-west-2.opendata.source.coop/tge‑labs/aef/` – list files with `aws s3 ls --no‑sign‑request s3://us-west-2.opendata.source.coop/tge‑labs/aef/` and download any year via `aws s3 cp --no‑sign‑request … <local>` | CC‑BY 4.0 (credit Google/DeepMind) | Load with `rasterio` or `xarray.open_rasterio`. Vectors are unit‑length; compute dot‑products or cosine similarity directly. No extra normalisation needed. |
| **ML4Sustain / EarthEmbeddings (Hugging Face)** | 300‑dimensional embedding per 384 × 384 pixel Sentinel‑2 patch | Parquet files (each row stores a patch and its embedding vector) | https://huggingface.co/datasets/ML4Sustain/EarthEmbeddings (click *Download* → “Download all files”) | Apache 2.0 (free for commercial and research) | Read via `pandas.read_parquet` or `pyarrow`. The `embedding` column holds a list of floats; spatial fields (`grid_cell`, `centre_lat`, `centre_lon`, `crs`) let you index patches. |
| **Earth‑Genome / Earth Index Embeddings** | Global embeddings for selected dates, typical size 128‑D | Cloud‑Optimized GeoTIFF or Zarr (chunked array) on Source Coop S3 bucket | https://source.coop/earthgenome/earthindexembeddings → browse to `s3://us-west-2.opendata.source.coop/earthgenome/earthindexembeddings/` (list with `aws s3 ls --no‑sign‑request …`) | CC‑BY 4.0 | Open Zarr stores with `xarray.open_zarr` or `zarr.open_consolidated`. Because data is chunked you can stream only the tiles needed for your patch, keeping I/O low. |

## How to plug these embeddings into the NDVI‑based patch workflow
1. **Define the spatial extent** of each NDVI patch (e.g., the bounding box of a connected component).
2. **Read the matching region** from the embedding collection using the same CRS/extent. For COGs use `rasterio`/`xarray`; for Zarr use `xarray.open_zarr` with a slice.
3. **Aggregate** the embedding vectors across the patch (e.g., mean across pixels). Since vectors are unit‑length, renormalise after averaging if you need a unit vector.
4. **Combine** the NDVI statistics (`mean_ndvi`, `area_ha`) with the aggregated embedding to form a richer descriptor for each patch.
5. **Cache** the downloaded files locally (they are static) to avoid repeated network calls; the buckets support unauthenticated HTTP or `aws s3`‐style access.

## Next steps for the team
- **Select a dataset** (Google AlphaEarth, ML4Sustain, or Earth‑Genome) based on desired dimensionality and storage format.
- **Add a download step** to the `Makefile` (e.g., `download_embeddings`) that pulls the needed year(s) or Zarr store.
- **Extend `scripts/generate_patches_from_ndvi.py`** to load the embeddings for each patch, compute the mean vector, and store it as a new property (e.g., `embedding_mean`).
- **Update the cost‑matrix** script to optionally weight edges using embedding similarity if that fits the scientific question.
- **Document the new dependencies** in `scripts/README.md` and cite the dataset according to the license.

These resources give the project a powerful, high‑level representation of the landscape that goes beyond a single NDVI band, while still respecting the “no API key” constraint.
