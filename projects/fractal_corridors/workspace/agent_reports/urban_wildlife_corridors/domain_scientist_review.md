# Domain Scientist Review – Urban Wildlife Corridors Manuscript Draft

**Overall Assessment**: The draft offers a coherent conceptual framing of urban ecological corridors as transport networks and presents a substantial simulation effort. The ecological logic is sound, but several aspects need strengthening before the work can robustly inform urban wildlife conservation.

## 1. Ecological Plausibility
- **Movement Cost Modeling** – The incorporation of effective travel‑time, road‑mortality, and crossing penalties reflects real‑world constraints on wildlife movement and is a strong point.
- **Species‑Specific Dispersal** – Heterogeneous dispersal kernels for functional groups are included, yet the parameter values are not calibrated against empirical data (e.g., radio‑telemetry or citizen‑science movement tracks). This limits confidence that the model captures realistic scale‑dependent movement.
- **Habitat Quality Layer** – Habitat nodes are derived from OpenStreetMap footprints without validation of habitat suitability. OSM tags alone cannot guarantee the presence of vegetative structure, food resources, or shelter needed by target taxa.
- **Disturbance & Recovery** – The disturbance timers and road‑mortality layer add realism, but the disturbance regimes (e.g., intensity, frequency) are generic and not tied to observed urban stressors such as construction cycles or traffic fluctuations.
- **Genetic Connectivity** – The model tracks abundances only; gene flow and inbreeding depression, which are critical for long‑term persistence in fragmented cities, are not considered.

## 2. Interpretation of Results
- The finding that dendritic (hierarchical) geometries do not reliably outperform cost‑matched controls aligns with theoretical expectations that total corridor length and connectivity dominate persistence outcomes.
- However, the manuscript sometimes overstates the generality of this result. It should emphasize that the conclusion is conditional on the current model structure, parameterizations, and synthetic landscapes.
- The discussion could benefit from clearer linkage between specific response variables (e.g., recovery time, rescue‑effect frequency) and the ecological mechanisms they represent.
- The provisional conclusion wisely tempers claims, but the language should avoid implying that hierarchical designs are ineffective; rather, they are not a *silver bullet* without complementary design considerations (e.g., crossing mitigation, redundancy).

## 3. Relevance to Urban Wildlife Conservation
- **Actionable Insights** – The emphasis on minimizing high‑risk human infrastructure crossings and ensuring network redundancy is directly relevant to city planners and conservation practitioners.
- **Transferability** – Current simulations use synthetic city footprints. Before advising real‑world implementation, the workflow should be demonstrated on at least one empirically derived urban landscape, with documented OSM tag validation and species‑specific movement data.
- **Stakeholder Considerations** – The manuscript could integrate discussion of socio‑ecological trade‑offs (e.g., green space allocation, equity of access) which are essential for adoption of corridor projects.

## 4. Recommendations for Revision
1. **Empirical Calibration** – Incorporate field‑derived movement parameters for at least two focal taxa (e.g., small mammal and pollinator) to ground the dispersal kernels.
2. **Habitat Validation** – Perform a brief validation of OSM‑derived habitat nodes against an independent land‑cover dataset (e.g., high‑resolution satellite or city GIS layers).
3. **Genetic Dimension** – Discuss, even qualitatively, how corridor design may affect gene flow and propose how future model extensions could incorporate genetic metrics.
4. **Scenario Diversity** – Run the model on two contrasting city typologies (e.g., dense high‑rise vs. sprawling low‑density) to test the robustness of the conclusions.
5. **Clarify Limitations** – Strengthen the limitations section to explicitly note the lack of empirical calibration, the synthetic nature of the landscapes, and the exclusion of socio‑economic factors.
6. **Conservation Recommendations** – Frame practical guidance around (a) reducing high‑risk crossings, (b) maintaining redundant pathways, and (c) prioritizing cost‑effective connectivity over strict hierarchical geometry.

## 5. Minor Comments
- Ensure consistent use of terminology (“hierarchical”, “dendritic”, “branch‑trunk‑ring”).
- Check reference formatting (e.g., missing DOIs).
- Add a data‑availability statement linking to the repository and raw OSM extracts.

**Conclusion**: The draft is a solid foundation for advancing urban corridor science. Addressing the above ecological realism gaps will greatly increase its impact and suitability for informing urban wildlife conservation policy.
