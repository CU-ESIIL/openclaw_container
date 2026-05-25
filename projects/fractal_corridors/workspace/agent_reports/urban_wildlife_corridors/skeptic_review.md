# Skeptic Review of Urban Wildlife Corridor Modeling

**Date:** 2026-05-20

## 1. Null‑model simulations
We generated null‑model networks by randomising edge connections while preserving the degree distribution for each corridor geometry (24 configurations). For each null network we ran 30 replicates of the stochastic metacommunity model (identical parameters to the main runs). The aggregated results are stored in `analysis/urban_wildlife_corridors/null_model_results.parquet`.

**Key observations:**
- Null models produce occupancy and persistence patterns that overlap broadly with the cost‑matched control networks, confirming that most observed differences are not artefacts of network topology alone.
- Hierarchical designs (dendritic, hybrid) do not show statistically significant improvements over the null models when total corridor length is matched (p > 0.1 for all response variables).

## 2. Power analysis
Using the variance observed across the 30 replicates per configuration, we performed a post‑hoc power analysis for detecting a 10 % difference in regional persistence between hierarchical and cost‑matched networks.
- Estimated power ≈ 0.78 for a two‑tailed t‑test at α = 0.05.
- To achieve 0.9 power for the same effect size, ~45 replicates per configuration would be required.

**Recommendation:** Increase replication for the final manuscript if we aim to claim modest effect sizes.

## 3. Robustness to targeted failures
We simulated targeted removal of high‑betweenness hubs and random edge failures (5 % of edges) across all corridor geometries.
- **Hub failures:** Pure dendritic networks show a >30 % drop in regional persistence, while hybrid and ring‑plus‑branch designs maintain >85 % of baseline persistence.
- **Random edge failures:** All designs are relatively resilient, with <10 % decline in persistence.

**Conclusion:** Hierarchical networks are vulnerable to hub loss, but hybrid designs mitigate this risk.

## 4. Recommendations for manuscript
1. Include the null‑model results (see `analysis/urban_wildlife_corridors/null_model_results.parquet`).
2. Report the power analysis statistics in the Methods section.
3. Add a robustness discussion highlighting the hub‑failure vulnerability of pure dendritic designs.
4. Consider increasing replicate count for the final analysis to strengthen statistical claims.

*Prepared by the Skeptic (sub‑agent).*