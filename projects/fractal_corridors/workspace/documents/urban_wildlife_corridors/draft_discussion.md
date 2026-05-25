# Draft Discussion (Update after Parameter Sweep)

## Overview
The recent large‑scale simulations across multiple corridor designs (nearest‑neighbor, minimum‑spanning‑tree, dendritic, hierarchical, and hybrid) consistently show that **simple cost‑matched networks perform at least as well as, and often better than, more complex hierarchical designs** in terms of species persistence and occupancy metrics. This aligns with the analytical flow‑law model, which predicts a monotonic decline in persistence with increasing fractal dimension under the current parameter regime.

## Interpretation of Discrepancies
While the ranking of designs matches the theoretical expectation, the **absolute values of simulated persistence are an order of magnitude higher** than those predicted by the analytical model. The likely drivers are:
1. **Stochastic disturbance** (`DISTURBANCE_PROB`) is incorporated in the simulation but not in the static analytical formulation.
2. The analytical model assumes a single, uniform mortality factor, whereas the simulation includes heterogeneous road‑mortality and edge‑effects.
3. Species‑specific dispersal kernels are homogenized in the current runs, inflating persistence for taxa that would otherwise be more limited.

## Immediate Next‑Step Analyses
1. **Full Parameter Sweep** – already completed, results are stored in `analysis/urban_wildlife_corridors/occupancy_sweep.csv`.  We will integrate these results into the manuscript table.
2. **Species‑Specific Calibration** – we need to obtain empirical dispersal parameters for representative taxa and incorporate them into the simulation (see `scripts/species_calibration.py`).
3. **Edge‑Effect GIS Mapping** – spatially varying road width, traffic volume, and lighting will be added as mortality modifiers (see `scripts/edge_effect_mapping.py`).
4. **Null‑Model Robustness** – beyond the placeholder random geometric graph, a degree‑preserving edge‑rewiring null model will be implemented to confirm that the observed ranking is not an artifact of network generation.
5. **Uncertainty Quantification** – Monte‑Carlo replicates will produce confidence intervals for all metrics.

## Revised Narrative
Given the lack of a clear advantage for hierarchical designs under realistic urban disturbance regimes, the manuscript will emphasize the **methodological contribution** (streaming‑first simulation workflow) and **practical guidance** that simple, cost‑matched corridors can be effective. The broader‑impact statement will be updated accordingly (see `broader_impact_draft.md`).

*Prepared by the Scientific Director and Quantitative Modeler after the team meeting.*