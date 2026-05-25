# Urban Wildlife Corridors Source Inventory

Status: working source inventory, 2026-05-18.

## User-supplied prior work

Ty provided three files in Slack on 2026-05-18 as prior work to build on. Direct Slack download was blocked by `missing_scope`, but Ty added local copies under `/workspace/documents/source_materials` on 2026-05-18.

| File | Slack file ID | Type | Size | Intended use | Access status |
| --- | --- | --- | ---: | --- | --- |
| Design principles for fitting cities and ecosystems into the same footprint 14 April 2021.docx | F0B4JCTQ666 | Word document | 1,283,357 bytes | Conceptual/design principles for city-ecosystem footprint integration; manuscript framing and design rules. | Available locally |
| population dynamics on a network.qmd | F0B4GB09CCE | Quarto/plain text snippet | 22,527 bytes, 608 lines | Existing population-dynamics network model; should guide equations, state variables, diagnostics, and simulation architecture. | Available locally |
| Greenspace scaling.Rmd | F0B4GB1P7NJ | R Markdown | 9,862 bytes | Existing scaling analysis; relevant to corridor/greenspace geometry, allometry, and urban design constraints. | Available locally |

## Immediate integration plan

1. Extract the conceptual claims and design principles from the DOCX.
2. Compare the Quarto network model against the current JavaScript scaffold:
   - state variables
   - network construction
   - dispersal operator
   - density dependence
   - stochasticity or disturbance
   - equilibrium versus transient diagnostics
3. Compare the R Markdown scaling analysis against the corridor-geometry hypotheses:
   - scaling exponents
   - area or length constraints
   - branching/fractal geometry assumptions
   - city footprint/ecosystem footprint tradeoffs
4. Replace or revise `scripts/simulate_corridor_population_dynamics.js` where Ty's prior equations are more appropriate.
5. Update `documents/urban_wildlife_corridors/manuscript_draft.md` so the manuscript builds from Ty's prior theory rather than from the temporary scaffold.

Initial synthesis is in `documents/urban_wildlife_corridors/prior_work_synthesis.md`.
