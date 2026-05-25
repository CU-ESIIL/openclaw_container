# Risk & Uncertainty Memo: Fractal Theory Assumptions

**Prepared for:** Urban Wildlife Corridors Working Group
**Author:** Skeptic Sub‑agent (depth 1)
**Date:** 2026‑05‑21

---

## 1. Overview
The fractal‐based framework for designing urban wildlife corridors assumes that habitat connectivity can be captured by scale‑invariant patterns and deterministic geometry. While elegant, several key theoretical assumptions introduce risk and uncertainty that could undermine the validity of model outcomes and subsequent policy recommendations.

---

## 2. Core Assumptions & Identified Weaknesses
| # | Assumption | Potential Weakness / Source of Uncertainty | Implications |
|---|------------|--------------------------------------------|--------------|
| 1 | **Deterministic spatial scaling** – The model treats habitat patches as perfect fractal objects with exact self‑similarity across scales. | Real urban landscapes exhibit irregular, non‑self‑similar patch shapes (e.g., irregular park boundaries, roof gardens). Stochastic variation in patch size and shape breaks the scaling law. | Over‑estimates connectivity at fine scales; may miss critical bottlenecks.
| 2 | **Neglect of stochastic disturbances** – Disturbance processes (traffic noise, light pollution, intermittent flooding) are omitted or treated as static. | Disturbances are inherently random in time and space; their probability distribution can shift with climate change or development. | Underestimates corridor degradation risk; leads to overly optimistic movement probabilities.
| 3 | **Edge effects ignored or simplified** – Edge influences on mortality, predation, and resource availability are assumed negligible or modeled with a constant buffer. | Edge effects are highly context‑dependent (e.g., road width, traffic volume, vegetation buffer quality). A single buffer cannot capture this variability. | May mis‑classify high‑risk edge zones as suitable, compromising corridor safety.
| 4 | **Homogeneous species response** – The theory assumes a single, scale‑invariant dispersal kernel for all focal species. | Species differ in movement ecology, tolerance to urban matrix, and perception of scale. Stochastic variation in individual behaviour is also ignored. | Policy derived from the model may protect species with low sensitivity while leaving vulnerable taxa unprotected.
| 5 | **Static land‑use background** – Future land‑use change is not incorporated; the fractal geometry is projected onto a fixed map. | Urban development is stochastic and policy‑driven; land‑use trajectories can alter corridor topology dramatically. | Corridor designs become rapidly obsolete; mitigation investments may be wasted.
| 6 | **Scale selection bias** – The chosen fractal dimension is calibrated on a limited spatial extent (e.g., a single watershed). | Scaling relationships may not hold across the broader metropolitan region, leading to extrapolation error. | Uncertainty in model transferability; risk of over‑generalisation.

---

## 3. Risk Assessment
| Risk | Likelihood | Severity | Mitigation Strategy |
|------|------------|----------|-------------------|
| **Over‑optimistic connectivity predictions** due to deterministic scaling. | Medium | High (misallocation of conservation resources). | Conduct empirical validation with GPS telemetry; incorporate stochastic perturbations into connectivity kernels.
| **Under‑estimated corridor failure** from stochastic disturbances. | High | Medium‑High (loss of functional corridors). | Model disturbance regimes probabilistically (e.g., Poisson traffic events, seasonal flooding) and perform sensitivity analyses.
| **Edge‑related mortality spikes** not captured. | Medium | High (potential population declines). | Use high‑resolution edge‑effect layers (traffic volume, lighting) and apply species‑specific mortality functions.
| **Species‑specific bias** from a single dispersal kernel. | High | Medium (bias against less mobile taxa). | Develop a suite of species‑specific kernels; adopt a multi‑species ensemble approach.
| **Obsolescence from static land‑use** assumptions. | High | Medium‑High (future‑proofing failure). | Integrate scenario‑based land‑use projections (e.g., from urban growth models) into the fractal framework.
| **Scale‑transfer error** when applying a locally‑derived fractal dimension region‑wide. | Medium | Medium | Re‑estimate fractal parameters across multiple sub‑regions; apply hierarchical scaling.

---

## 4. Recommendations for Immediate Action
1. **Empirical Calibration** – Gather movement data (e.g., radio‑tracking, camera traps) across representative urban habitats to fit stochastic dispersal kernels.
2. **Disturbance Modeling** – Incorporate probabilistic disturbance layers (traffic, noise, flood risk) and run Monte‑Carlo simulations to quantify uncertainty bounds.
3. **Edge‑Effect Mapping** – Create high‑resolution edge‑risk rasters using GIS layers (road class, illumination) and apply species‑specific mortality coefficients.
4. **Multi‑Species Framework** – Extend the fractal model to a suite of kernels reflecting functional groups (e.g., small mammals, birds, reptiles).
5. **Dynamic Land‑Use Scenarios** – Couple the fractal geometry with projected urban growth models (e.g., SLEUTH, cellular automata) to test corridor robustness under future development.
6. **Cross‑Scale Validation** – Estimate fractal dimensions in multiple sub‑regions and assess consistency; adjust the model to allow region‑specific scaling factors.

---

## 5. Conclusions
While the fractal theory offers a compelling analytical lens, the current set of assumptions introduces considerable risk of over‑estimation of connectivity and under‑estimation of corridor vulnerability. Addressing stochastic disturbances, edge effects, species heterogeneity, and dynamic land‑use will substantially improve the robustness of the framework and ensure that policy recommendations are defensible under uncertainty.

---

*Prepared by the Skeptic sub‑agent (fractal_skeptic).*
