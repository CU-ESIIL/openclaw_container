## Quantitative Modeler Review – Urban Wildlife Corridors Manuscript Draft

**Overall assessment**: The draft presents a compelling conceptual framework and a reasonable initial implementation. However, several modeling assumptions, data‑handling choices, and workflow integrations need clarification and tightening to meet the streaming‑first Parquet pipeline goals and to ensure reproducibility.

### 1. Modeling assumptions
- **Discrete seasonal/annual timesteps** – appropriate for large‑scale, long‑term dynamics, but the manuscript should explicitly justify why continuous ODE integration was not retained and how stochasticity is introduced at each step (e.g., demographic noise, disturbance events).
- **Metacommunity formulation** – the state‑equation `dN_is/dt = …` correctly includes growth, competition, emigration, immigration, and mortality, yet the current JavaScript scaffold does not yet implement full graph‑mediated dispersal; emigration is computed but the subsequent redistribution across the network is only approximated. This gap should be acknowledged and a plan to incorporate explicit dispersal kernels over the effective cost matrix described in §5.4 be added.
- **Functional‑group heterogeneity** – the extended model adds short/medium/long dispersal kernels, which is a major improvement. However, the manuscript still refers to “generic species” in several places (e.g., Table 2). The review should replace those references with the functional‑group terminology and ensure all response variables are reported per group.
- **Disturbance handling** – patch‑recovery timers are a good addition, but the implementation of edge/hub failures appears asymmetric across network geometries (trees cannot lose edges without disconnecting). The manuscript should note this limitation and possibly include a topology‑preserving edge‑removal scheme for fair comparison.
- **Cost‑matched controls** – the design includes cost‑matched rewired networks, but the draft does not describe how total corridor cost is quantified (e.g., sum of effective travel‑time plus crossing penalties). A brief methods note on the matching algorithm is required for reproducibility.

### 2. Data handling & streaming workflow
- **Streaming‑first data acquisition** – Sentinel‑2, embeddings, Zarr arrays, and GBIF records are correctly streamed via VSICURL/HTTP. The manuscript should cite the specific libraries (e.g., `rasterio`, `pyarrow.dataset`) that enable true streaming reads.
- **Parquet conversion** – the current pipeline still generates an intermediate CSV (`simulation_summary.csv`) and then converts it to Parquet. For a truly streaming workflow the simulation should write directly to Parquet (or Zarr) using `pyarrow` or `fastparquet` with batch flushing. The review recommends removing the CSV step and documenting the batch size and compression used.
- **Data provenance** – each external source (Sentinel‑2, GBIF, OSM) should have a provenance manifest (timestamp, version/tag, retrieval URL). The draft mentions storage under `data/derived/` but does not provide a manifest; adding a `data/manifest.yaml` would satisfy reproducibility standards.
- **Memory footprint** – the manuscript claims “continent‑scale” data handling; a brief note on memory management (e.g., use of Dask or lazy loading) would reassure reviewers that the workflow can operate on modest hardware.

### 3. Consistency with streaming‑first Parquet workflow
- The **scripts/generate_figures.py** now prefers Parquet, which is a positive step. However, the manuscript still describes a CSV‑based workflow in the Methods section. Update the text to reflect the current Parquet‑first approach and the planned future direct‑Parquet simulation output.
- The **validation report** should be generated from the Parquet dataset rather than a converted CSV; ensure the report reads directly from `simulation_summary.parquet`.
- All **figures** (including the regenerated Figure 4) must be produced from Parquet‑derived data frames; the caption should note that the underlying data are streamed Parquet records.

### 4. Recommendations (action items)
1. **Add explicit statement** that the simulation writes directly to Parquet in future runs; remove any references to CSV in Methods.
2. **Document the cost‑matching algorithm** (objective function, constraints) in a new subsection of Methods.
3. **Clarify the dispersal implementation** – either include a brief description of the current approximation or note that a full graph‑mediated dispersal kernel will be added in the next iteration.\F **Include functional‑group terminology** throughout the Results and tables; replace “generic species” where applicable.
4. **Provide a data provenance manifest** (e.g., `data/manifest.yaml`) and reference it in the manuscript.
5. **Address edge‑failure asymmetry** by describing a topology‑preserving edge‑removal protocol for the robustness tests.
6. **Mention memory/streaming considerations** (lazy loading, Dask, chunked Parquet reads) to support the streaming‑first claim.
7. **Update Figure 4 caption** to indicate that the raster was derived from streamed Parquet outputs.
8. **Add a short Data Availability statement** that points to the open‑source repository and describes how the Parquet dataset can be accessed via the streaming pipeline.

**Conclusion**: The manuscript is nearing readiness but requires the above clarifications to align modeling assumptions, data handling, and the streaming‑first Parquet workflow. Implementing these changes will strengthen reproducibility, satisfy the Quantitative Modeler’s standards, and streamline downstream integration.
