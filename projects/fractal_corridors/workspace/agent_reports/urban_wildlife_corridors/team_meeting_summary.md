# Team Meeting – Fractal Corridor Results Review (2026‑05‑21)

**Participants**: Quantitative Modeler, Domain Scientist, Deputy Integrator, Scientific Director, Skeptic, Societal Impact.

---

## 1. Quantitative Modeler Summary

- **Simulation vs. Theory**: The side‑by‑side table from `compare_fractal_theory_vs_simulation.py` shows that the MST (pure tree) design yields the highest simulated mean final population (30 843) and the highest theoretical persistence (0.051). The hierarchical (branch‑trunk‑ring) layout performs worst in both metrics (simulation 30 227, theory 0.014).
- **Discrepancies**: Theory predicts a monotonic decline of persistence with increasing fractal dimension, which matches the simulation ranking (MST > nearest > dendritic > hierarchical). However, the absolute values differ: theoretical persistence is an order of magnitude lower than what the simulation suggests for all designs, likely because the theoretical model assumes a single, static mortality factor while the simulation includes stochastic disturbance events.
- **Immediate Next‑Step Analyses**:
  1. **Sensitivity checks** on road mortality (`ROAD_MORTALITY`) and dispersal kernel (`DISPERSAL_KERNEL`). Use the newly added environment variables to run a focused sweep (already implemented in `parameter_sweep_fractal.py`).
  2. **Parameter sweep** across stochastic disturbance probability (`DISTURBANCE_PROB`). The current runs only cover `p = 0.0` and `p = 0.1` for the nearest design; we should extend to `p = 0.2–0.5`.
  3. **Calibration**: Fit the allometric exponent `b` and viscosity exponent `γ` to species‑specific telemetry data (see Domain Scientist notes).
  4. **Uncertainty quantification**: Monte‑Carlo replicate the simulation for each design to obtain confidence intervals on the mean final population.

---

## 2. Domain Scientist Summary

- **Ecological Implications**: The lack of advantage for the hierarchical network suggests that redundancy alone does not compensate for high road‑mortality and frequent disturbances in a dense urban matrix. Edge effects and habitat quality variations (not captured in the current model) are likely driving the lower persistence of the hierarchical design.
- **Biological Concerns**: 
  - The model treats all species with a single dispersal kernel; real communities (e.g., coyotes vs. hedgehogs) will respond differently to corridor geometry.
  - Disturbance events are modeled as a simple probability; temporal clustering (e.g., traffic rush hour) could create critical bottlenecks.
- **Next Ecological Analyses**:
  1. **Species‑specific calibration**: Incorporate empirical movement parameters for at least three functional groups (small mammals, medium carnivores, avian dispersers).
  2. **Edge‑effect mapping**: Add GIS layers for road width, traffic volume, and lighting to weight corridor mortality spatially.
  3. **Dynamic land‑use scenarios**: Run the simulation on projected 2030/2040 urban growth maps to test robustness of each design over time.
  4. **Connectivity metrics**: Compute circuit‑theory resistance and compare with the flow‑law flux to validate the analytical assumptions.

---

## 3. Deputy Integrator Summary

- All data products (Parquet files, sensitivity tables) are now stored under `analysis/`. The manuscript pipeline can ingest the new `simulation_summary.parquet` without conversion steps.
- No remaining integration blockers; next step is to embed the updated results table into `documents/urban_wildlife_corridors/manuscript_draft.md` once the parameter‑sweep analysis is finalized.

---

## 4. Scientific Director Summary

- The hierarchical layout does **not** outperform the baseline designs; therefore no conditional manuscript paragraph is needed at this stage.
- Emphasise in the Discussion that the streaming workflow enables rapid evaluation of many design scenarios and that the current evidence points to simple cost‑matched networks being at least as effective as more complex fractal hierarchies.

---

## 5. Skeptic Summary

- Risks identified earlier (deterministic scaling, static mortality, homogeneous species response) are confirmed by the present results.
- Recommend a formal **null‑model** comparison (randomized network geometry) to ensure the observed ranking is not an artifact of the specific network generation algorithm.

---

## 6. Societal Impact Summary

- No immediate public‑facing claim about hierarchical superiority is warranted.
- Prepare a broader‑impact paragraph that highlights the methodological advance (streaming‑first simulation) and the practical implication that simple, cost‑matched corridors can be effective in dense cities.

---

**Action Items**
1. Quantitative Modeler to run full parameter sweep (σ ∈ {0.05,0.07,0.09}, m ∈ {0.2,0.3,0.4}, p ∈ {0.0,0.1,0.2,0.3}).
2. Domain Scientist to gather species‑specific movement data and produce calibration tables.
3. Deputy Integrator to update the manuscript table with the upcoming sweep results.
4. Scientific Director to draft the revised Discussion section reflecting the lack of hierarchical advantage.
5. Skeptic to design a randomized‑network null model for robustness testing.
6. Societal Impact to draft the broader‑impact paragraph.

*Prepared by the PI Liaison after consolidating sub‑agent inputs.*