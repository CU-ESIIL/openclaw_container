# Urban Wildlife Corridors – Project Presentation

---

## Slide 1 – Title
- **Title:** *Testing Hierarchical Ecological Transport Networks for Urban Metacommunity Flow and Recovery*
- **Team:** PI Liaison, Scientific Director, Deputy Integrator, Data Engineer, Quantitative Modeler, Domain Scientist, Skeptic, Societal Impact Agent
- **Date:** Tue 2026‑05‑19

---

## Slide 2 – Project Motivation
- Cities fragment habitats; corridors aim to reconnect.
- Traditional designs use shortest‑distance webs.
- Hypothesis: *Hierarchical (dendritic) networks* may improve biodiversity flow, efficiency, and resilience.
- Need quantitative, reproducible simulation evidence across realistic urban landscapes.

---

## Slide 3 – Data Sources & Landscape Generation
- **Sentinel‑2 NDVI** (Level‑2A) streamed from AWS → `data/derived/ndvi.tif`.
- **OpenStreetMap** roads & greenspace → road‑density raster & patch centroids.
- **Synthetic city patches** for London, Paris, New York (30 patches each).
- **Tree‑ness metric** = MST length ÷ total edge length (stored in `city_metrics.json`).

*Figure: Example NDVI background with OSM roads and green‑space patches* (placeholder – see generated maps).

---

## Slide 4 – Corridor Geometries
| Geometry | Construction |
|----------|--------------|
| Nearest‑Web | Connect each patch to its nearest neighbor |
| Minimum‑Spanning‑Tree (MST) | Kruskal’s algorithm on full graph |
| Dendritic | MST + a few random extra edges |
| Hybrid Dendritic | Dendritic + a handful of long shortcuts |

*Visuals:*  
- `figures/urban_wildlife_corridors/total_corridor_length.png` – total length per geometry.
- `figures/urban_wildlife_corridors/species_per_length.png` – biodiversity per unit length.
- `figures/urban_wildlife_corridors/final_mean_occupancy.png` – mean occupancy.

---

## Slide 5 – Population‑Dynamics Model (Core)
- Multi‑species logistic growth (12 species) with species‑specific traits (`species_traits.json`).
- Dispersal: rate & kernel (fraction of edge length).  
- Competition matrix and stochastic extinction.
- Scenarios: benign, costly movement, edge disturbance, high mortality.
- 100 replicates, 20 000 steps, burn‑in 5 000.

---

## Slide 6 – Sensitivity Sweep – Dispersal Distance
- Vary **kernel** from 0.01 to 0.12 (fraction of edge length).
- Keep dispersal rates very low & distance mortality high.
- Result: occupancy stays flat until a threshold is reached.

*Figure:* `figures/urban_wildlife_corridors/occupancy_vs_kernel.png`

---

## Slide 7 – Master Figure – Integrated Insights
- **Panel A:** World map with our three test cities.
- **Panel B:** Spatial layout of each city’s NDVI, roads, patches, and the four corridor designs.
- **Panel C:** Scatter of **Tree‑ness** vs. **Mean Final Occupancy** across cities.

*Figure:* `figures/urban_wildlife_corridors/figure4_master.png`

---

## Slide 8 – Key Findings
1. **Efficiency:** MST achieves the highest species‑per‑length, confirming length matters.
2. **Occupancy:** With current dispersal settings, geometry has little effect – individuals can traverse even the longest networks.
3. **Tree‑ness trend:** Higher tree‑ness correlates with slightly higher occupancy in the synthetic cities (see Master Figure).
4. **Sensitivity:** Only when dispersal kernels become very small does corridor length start to limit occupancy.

---

## Slide 9 – Implications & Next Steps
- **Data upgrade:** Replace synthetic NDVI/patches with real Sentinel‑2 derived raster and OSM‑derived patches.
- **Full‑scale cloud simulation:** Stream data, run on a Spark/Dask cluster (Quantitative Modeler).
- **Cost‑matched controls:** Generate corridor networks with equal total length for fair comparison.
- **Theory‑driven sweeps:** Percolation thresholds, network fragmentation (Domain Scientist).
- **Skeptic review:** Statistical tests for tree‑ness advantage.
- **Societal impact:** Open‑source repository, plain‑language summary for stakeholders.

---

## Slide 10 – Thank You & Contact
- **PI Liaison:** [email@example.com]
- **GitHub Repository:** https://github.com/openclaw/urban-wildlife-corridors
- **Open data sources:** Sentinel‑2 (AWS), OpenStreetMap (Overpass API)

*All figures are available in the `figures/urban_wildlife_corridors/` folder.*
