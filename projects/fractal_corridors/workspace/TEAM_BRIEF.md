# TEAM_BRIEF.md - Working Group Brief

This document is written and maintained by the PI Liaison for the scientific working group. It translates the user's answers into a structured internal brief without inventing goals, facts, data sources, or approvals.

## Project summary

The project tests whether urban wildlife corridors should be designed as hierarchical ecological transport networks rather than shortest-distance webs among habitat fragments. Ty's prior work frames cities and ecosystems as co-located metabolic/transport networks, so Phase 1 should evaluate flow, time, crossing risk, disturbance recovery, and metacommunity persistence together. All claims remain preliminary until literature, domain, and skeptic review are complete.

## Key scientific question

Do dendritic, ringed, or fractal corridor geometries improve multi-species flow, dispersal, persistence, recovery, or coexistence relative to shortest-distance corridor webs under city transport constraints?

## User intent

The PI wants a manuscript draft grounded in real simulations, not just a conceptual essay. The theory is that transport-network-like hierarchy may organize ecological movement better than locally shortest paths, especially when movement is measured as effective time/risk and when human and non-human networks occupy the same footprint.

## Known constraints

- Use Ty's source materials in `documents/source_materials/` as the theoretical and modeling base.
- Use synthetic simulations until empirical sites, species, and data are selected or explicitly approved.
- Do not treat preliminary simulation outputs as validated ecological claims.
- Human approval is required before policy, community, public-facing, or empirical-site claims.
- The current JavaScript simulation is a diagnostic scaffold, not the manuscript-scale model.

## Expected outputs

- Reproducible simulation script.
- Simulation output tables and figure.
- Manuscript draft with methods, preliminary results, limitations, and next tests.
- Question queue for PI choices that affect Phase 1.

## Initial task assignments

| Role | Initial task | Expected output | Due or review point |
| --- | --- | --- | --- |
| Scientific Director | Review whether the current model directly tests the corridor hierarchy hypothesis or mostly tests corridor-length efficiency. | Phase 0 scientific review memo | Before claims are promoted beyond draft |
| Deputy Director / Integrator | Maintain artifact map across manuscript, simulation code, outputs, figures, assumptions, and questions. | Integration memo in agent_reports/urban_wildlife_corridors/ | Before Phase 1 sensitivity expansion |
| Quantitative Modeler | Extend the simulation to sensitivity analyses over dispersal, competition, corridor resistance, and disturbance. | Sensitivity script and diagnostics | Phase 1 |
| Domain Scientist | Review species dynamics, corridor assumptions, and plausibility for urban taxa. | Domain plausibility memo | Before manuscript interpretation hardens |
| Skeptic / Adversarial Reviewer | Test whether dendritic benefit is assumed rather than emergent. | Skeptic review memo | Required before any major claim |

## Assumptions to test

- Synthetic habitat fragments and niche gradients are sufficient for a Phase 0 model test.
- Corridor geometry can be usefully compared by both absolute biodiversity outcomes and biodiversity per corridor length.
- The first model is a scaffold; it does not include behavior, predation, mortality from roads, matrix permeability, human-network crossing costs, ring/trunk/branch flow motifs, or empirical calibration.

## Issues requiring skeptic review

- The initial run shows little absolute difference in coexistence among geometries, so the manuscript should not claim dendritic corridors increase coexistence without further model development.
- The apparent dendritic advantage is currently corridor-length efficiency, not stronger persistence.
- The stronger Ty-derived hypothesis is about maintaining flow through co-located city/ecosystem transport systems; the model must not reduce that to a simple edge-length comparison.

## Issues requiring impact review

- Urban corridor recommendations affect communities, land access, governance, and planning priorities; public-facing guidance requires later impact review.

## Unresolved questions for the user

- Which target species groups should Phase 1 emphasize?
- Should the empirical path use Montreal first, given the source materials, or remain synthetic until the model is stable?

## Follow‑on Experiments (Constrained Space)

## Figure Development Tasks

The team will design a concise set of Python‑generated figures that communicate:
1. **Emergence of hierarchical benefit** – visualizing how dendritic/Fractal networks produce non‑linear gains in flow, persistence, or species richness compared to shortest‑distance webs.
2. **Gradient of effectiveness** – a heat‑map or line plot showing performance metrics (e.g., connectivity, time‑risk) across a gradient of corridor length budgets or fragmentation levels.
3. **Constrained vs. Unconstrained spaces** – side‑by‑side comparisons of the same metrics when total corridor length is limited versus unlimited, highlighting trade‑offs.

### Assigned roles
- **Quantitative Modeler** – extend simulation scripts (`scripts/analysis/...`) to output the required metrics and generate the figures using Matplotlib/Seaborn.
- **Technical Communicator / Diagram‑maker** – draft figure captions, layout suggestions, and ensure visual clarity (color‑blind friendly palettes, consistent axis limits).
- **Domain Scientist** – verify ecological plausibility of the visualized patterns and suggest any additional annotations.
- **Skeptic Reviewer** – assess whether the figures over‑state the results; propose neutral ways to present uncertainty.

### Deliverables
- Three polished PNG/SVG figures placed in `figures/` with accompanying caption markdown in `documents/figure_captions.md`.
- A short report (`agent_reports/figure_development.md`) summarizing the design rationale and any residual ambiguities.


1. **Length‑budget sweep** – Impose a fixed total corridor length (e.g., 10 %, 25 %, 50 % of the unconstrained network) and compare dendritic vs. shortest‑distance designs on persistence, species richness, and flow efficiency. *Lead:* Quantitative Modeler to add a budget constraint to the Node.js simulation (or migrate to Python for easier parameter sweeps).
2. **Fragment density gradient** – Vary the number and spatial clustering of habitat patches while keeping the length budget constant, testing how hierarchical networks adapt to sparse vs. dense urban matrices. *Lead:* Data Engineer to generate synthetic landscape ensembles and provide them to the modeler.
3. **Multi‑species interaction test** – Introduce two‑species (competitor‑colonizer) dynamics with differing dispersal kernels to see if dendritic layouts preferentially support coexistence under space limits. *Lead:* Domain Scientist to define realistic parameter sets; Quantitative Modeler to implement the interaction module.

**Required updates** – Extend `scripts/` with a `budget_constraints.js` (or Python) module, add synthetic landscape generators in `data/`, and update `agent_reports/` with new reproducibility notes.

