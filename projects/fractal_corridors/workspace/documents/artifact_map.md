# Artifact Registry

| Artifact ID | Owner | Type | Location | Version/Commit | Dependencies | Description |
|------------|-------|------|----------|----------------|--------------|-------------|
| SIM‑v1.0 | Quantitative Modeler | Simulation code | scripts/sim/ | N/A | None | Baseline stochastic metacommunity model |
| PIPE‑ingest‑v0.1 | Data Engineer | Ingestion script | scripts/pipeline/ingest_sim.py | N/A | None | Downloads simulation output into `data/raw/` |
| PIPE‑clean‑v0.3 | Data Engineer | Cleaning script | scripts/pipeline/clean.py | N/A | SIM‑v1.0 output | Validates and transforms raw data to `data/processed/` |
| HYP‑v1.0 | Domain Scientist | Hypothesis document | documents/hypothesis_v1.md | N/A | None | Primary research question and testable predictions |
| ANAL‑v1.0 | Quantitative Modeler | Validation notebook | analysis/validation_v1.ipynb | N/A | PIPE‑clean‑v0.3 output | Computes metrics, generates figures |
| FIG‑persistence | Technical Communicator | Figure | figures/persistence_curve.png | N/A | ANAL‑v1.0 results | Persistence over time with confidence bands |
| MANU‑draft‑v0.1 | Scientific Narrative Lead | Draft manuscript | documents/draft.md | N/A | HYP‑v1.0, ANAL‑v1.0, FIG‑* | Provisional manuscript text |
| REVIEW‑skeptic‑v0.1 | Skeptic | Review report | agent_reports/skeptic_review.md | N/A | All artifacts | Confounder and robustness assessment |
| IMPACT‑checklist | Societal Impact | Checklist | documents/impact_checklist.md | N/A | MANU‑draft‑v0.1 | Flags policy‑relevant language |

The registry will be updated each time a new deliverable is produced.
