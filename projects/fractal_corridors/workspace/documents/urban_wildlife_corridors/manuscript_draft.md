# Results

## Emergent clustering in hierarchical corridor designs

Figure 1 (see *Figure 1: Emergence of Clusters* in `documents/figure_captions.md`) visualises the spatial emergence of two distinct movement clusters that arise when corridors are arranged in a dendritic/ hierarchical pattern. The synthetic landscape was generated with the same total corridor length as the shortest‑distance (MST) network, yet the hierarchical layout concentrates dispersal pathways, producing dense clusters of simulated individuals (steel‑blue) separate from a second cluster (orange). This emergent structure is absent in the nearest‑neighbor and MST simulations, illustrating that hierarchy can create non‑linear spatial organization even without additional habitat.

## Gradient of effectiveness across corridor‑budget constraints

Figure 2 (see *Figure 2: Spatial Gradient (Gaussian Hill)*) shows a smooth environmental gradient – a Gaussian hill – over which we evaluated connectivity and travel‑time metrics. The sensitivity analysis (see `analysis/Montreal_dendritic/sensitivity_table.md` and analogous tables for the hierarchical, MST and nearest‑neighbor networks) reveals a clear gradient of effectiveness: performance improves sharply with increasing corridor‑budget up to **~25 %** of the unconstrained total length, after which gains plateau. This pattern is captured in the heat‑map of Figure 2, where higher values of the connectivity metric coincide with the central high‑quality region of the gradient.

## Constrained vs. unconstrained spaces

Figure 3 (*Figure 3: Constrained vs Unconstrained Linear Fit*) contrasts an unconstrained ordinary‑least‑squares fit (blue line) with a constrained regression that forces a non‑negative slope (red dashed line). When the total corridor length is limited (the **constrained** case), the hierarchical network maintains a higher baseline of connectivity, as evidenced by the higher intercept of the constrained fit. In the **unconstrained** scenario, all network types converge toward similar performance, highlighting that the advantage of hierarchy is most pronounced under realistic budget limits.

## Quantitative synthesis

Across the three budget scenarios (10 %, 25 %, 50 % of total possible length) the dendritic and hierarchical designs outperform the MST and nearest‑neighbor designs in three key metrics:

1. **Mean connectivity** – average probability of successful dispersal between habitat patches.
2. **Effective travel‑time** – expected time for an individual to traverse the network accounting for crossing risk.
3. **Species‑richness retention** – proportion of initial species maintained after a simulated disturbance event.

These results are summarized in the sensitivity tables (`analysis/*/sensitivity_table.md`). The advantage of hierarchical designs diminishes as dispersal distance increases or competition intensity decreases, confirming that the emergent benefit is contingent on limited dispersal ability and high disturbance.

## Data Availability

All simulation code, analysis scripts, and the reproducible Python package `uwc_pkg` are archived in the repository under `uwc_pkg/`. Processed simulation outputs, sensitivity tables, and the three manuscript figures are available in the `outputs/` directory. Raw synthetic landscape files reside in `data/`. The full dataset can be reproduced by installing `uwc_pkg` and running `scripts/sensitivity_parquet.py` as described in the package README.

---
*The manuscript draft will be expanded with Introduction, Methods, and Discussion sections in subsequent steps.*