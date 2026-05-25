# Hierarchical Advantage Experiment Report

**Parameters** (used for all runs)
- Dispersal kernel: very short (≈ 0.02 km⁻¹) – simulated via the `HIERARCHY_TYPE` label only as a placeholder.
- Road mortality: high (≈30 %).
- Disturbance: frequent, patch‑level, recovery timer 30 steps.
- Functional groups: 70 % short‑disperser, 30 % long‑disperser.

**Mean final population (higher = better persistence)**
| Design | Mean Final Population |
|-------|-----------------------|
| nearest | 30308.73 |
| dendritic | 30425.12 |
| hierarchical | 30227.28 |
| mst | 30843.46 |

**Result:** The hierarchical layout was *not* the top performer (best was `mst`).
