# Scientific Director Review

**Manuscript:** `documents/urban_wildlife_corridors/manuscript_draft.md`

## Summary
The draft presents a well‑structured framework for evaluating hierarchical urban ecological corridors using stochastic metacommunity simulations. The narrative is coherent, the objectives are clearly linked to the broader project goal of testing whether hierarchical network geometry can improve biodiversity outcomes in fragmented urban landscapes.

## Strengths
- **Clear motivation** – The introduction convincingly explains why traditional nearest‑distance designs may be insufficient and frames the scientific question around movement function rather than mere distance.
- **Comprehensive prediction set** – Table 1 (Predictions P1‑P6) articulates explicit, testable hypotheses with required controls and response variables.
- **Methodological depth** – The draft outlines a multi‑species stochastic graph model with realistic movement costs (effective travel time, crossing risk, road‑mortality) and disturbance dynamics, which aligns with state‑of‑the‑art metacommunity modeling.
- **Iterative development** – Recent sections (5.5‑5.6) incorporate heterogeneous dispersal kernels, road‑mortality layers, and longer simulation horizons, demonstrating responsiveness to earlier reviewer feedback.
- **Transparency** – The manuscript lists data sources, code repositories, and provides a reproducible workflow (Parquet output, `scripts/generate_figures.py`).

## Major Concerns & Recommendations
1. **Empirical grounding of habitat layers** – The OSM‐derived greenspace and building‑footprint layers are still described as “placeholders.” Before any claim about urban planning relevance, the manuscript should include a validation section showing that the habitat quality indices correlate with independent field or remote‑sensing data (e.g., NDVI, land‑cover maps).
2. **Functional‑group parameterisation** – The current functional‐group kernels are described qualitatively. Provide a table with the specific parameter values (kernel scale, mortality sensitivity) and justification (literature or expert elicitation).
3. **Cost‑matching controls** – While cost‑matched rewired networks are mentioned, the method for preserving total corridor length and degree distribution needs explicit description (e.g., algorithmic steps, random seed handling) to ensure reproducibility.
4. **Statistical analysis** – The manuscript reports qualitative trends (e.g., “no inherent biodiversity advantage”). Include quantitative effect sizes with confidence intervals or Bayesian credible intervals for each prediction, and clarify the statistical tests used across the 30 replicates per configuration.
5. **Scope of conclusions** – The final “Provisional Conclusion” still hints at broader urban planning implications. Temper these statements until the model has been validated against empirical biodiversity data or a real‑city case study, as already noted in the “Limitations” section.
6. **Figure completeness** – Figure 4 has been regenerated, but the manuscript still references Figures 1 and 2 (now removed). Ensure that all figure cross‑references are accurate and that the figure captions fully describe the visualised metrics.
7. **Human‑network conflict quantification** – The manuscript mentions a “human‑network conflict layer” but does not detail how crossing penalties are derived (traffic volume, road classification). Include a brief methods subsection describing the data source and scaling for these penalties.

## Alignment with Project Goals
The draft stays tightly aligned with the project’s overarching aim to test hierarchical corridor designs. The inclusion of disturbance scenarios, heterogeneous dispersal, and cost‑matched controls directly addresses the hypothesis that hierarchy may improve metacommunity persistence and recovery. Addressing the concerns above will strengthen the manuscript’s scientific rigor and prepare it for the upcoming Skeptic review.

## Action Items for the Team
- Add a **Habitat Validation** subsection (methods + results).
- Provide a **Functional‑Group Parameter Table** (Appendix A).
- Expand the **Cost‑Matching Algorithm** description (pseudocode or reference).
- Incorporate **Statistical Summary Tables** for each prediction (e.g., mean ± SD, p‑values).
- Revise all figure references and ensure captions are complete.
- Detail the **Human‑Network Conflict Data** source and calculation.
- Once revisions are made, circulate the updated manuscript for the Quantitative Modeler and Domain Scientist reviews before the Skeptic’s formal assessment.

*Prepared by the Scientific Director (subagent).*
