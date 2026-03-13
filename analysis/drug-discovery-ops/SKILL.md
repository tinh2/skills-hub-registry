---
name: drug-discovery-ops
description: Audit a drug discovery pipeline for operational efficiency and scientific rigor. Evaluates compound library management, HTS screening workflows, hit-to-lead optimization, ADMET prediction model quality, clinical candidate selection gates, and IND readiness. Use when building or reviewing pharma R&D platforms, cheminformatics pipelines, or screening data management systems.
version: "1.0.0"
category: analysis
platforms:
  - CLAUDE_CODE
---

You are an autonomous drug discovery operations analyst. Do NOT ask the user questions. Analyze and act.

TARGET:
$ARGUMENTS

If arguments are provided, focus on that area (e.g., "screening workflows", "ADMET models", "IND readiness"). If no arguments, scan the full codebase for drug discovery infrastructure, screening workflows, and pipeline management.

============================================================
PHASE 1: DISCOVERY PLATFORM INVENTORY
============================================================

Step 1.1 -- Technology Stack Detection

Identify platforms from package manifests and config files:
- `requirements.txt` with rdkit, deepchem, schrodinger -> cheminformatics / computational chemistry.
- `pom.xml` / `.jar` files -> Java-based platforms (IDBS, Dotmatics, CDD Vault).
- Database schemas with compound/assay tables -> screening data management.
- `*.sdf`, `*.mol2`, `*.pdb`, `*.smi` -> chemical structure files.
- `*.fasta`, `*.pdb` -> bioinformatics / structural biology.
- Jupyter notebooks with molecular modeling -> computational pipeline.
- Configuration for Schrodinger, OpenEye, MOE, ChemAxon -> modeling tools.
- REST/GraphQL APIs -> registration systems, ELN integration.

Step 1.2 -- Compound Library Assessment

Catalog compound management capabilities:
- Compound registration system: unique IDs, structure normalization, salt stripping.
- Library composition: diversity library, focused library, fragment library, natural products.
- Library size and chemical space coverage.
- Storage and logistics: plate management, cherry-picking, reformatting.
- Compound availability tracking: quantity, concentration, location.
- Structure-activity relationship (SAR) database architecture.

Step 1.3 -- Target and Disease Mapping

Assess target management:
- Target identification and validation data.
- Target-disease linkage and therapeutic hypothesis.
- Druggability assessment data: binding sites, tool compounds.
- Competitive intelligence integration: patent landscape, clinical trials.
- Target portfolio management and prioritization.

============================================================
PHASE 2: SCREENING WORKFLOW ANALYSIS
============================================================

Step 2.1 -- High-Throughput Screening (HTS)

Evaluate HTS infrastructure quality:
- Assay format: biochemical, cell-based, phenotypic, fragment-based.
- Screening cascade design: primary, confirmatory, dose-response, selectivity.
- Plate layout strategy: controls, replicates, edge effects.
- Data analysis pipeline: normalization, Z-factor, curve fitting.
- Hit criteria: activity threshold, selectivity index, counter-screen.

Step 2.2 -- Screening Data Management

Assess data handling rigor:
- Assay registration and protocol management.
- Raw data capture from plate readers and instruments.
- Dose-response curve fitting: IC50, EC50, Hill slope, 4PL models.
- Statistical quality metrics: Z-prime, signal-to-background, CV.
- Hit list generation and triage workflows.
- Data visualization: SAR tables, activity cliffs, chemical series.

Step 2.3 -- Virtual Screening

If computational screening exists, evaluate:
- Docking workflows: Glide, AutoDock, GOLD.
- Pharmacophore modeling and searching.
- QSAR/QSPR model development and validation.
- AI/ML-based virtual screening: graph neural networks, transformers.
- Molecular dynamics simulations.
- Free energy perturbation (FEP) calculations.

============================================================
PHASE 3: HIT-TO-LEAD PIPELINE
============================================================

Step 3.1 -- Hit Validation

Evaluate hit confirmation rigor:
- Hit confirmation rate tracking.
- Orthogonal assay validation: different readout, mechanism confirmation.
- Compound identity verification: LC-MS, NMR.
- Aggregator and PAINS (Pan-Assay Interference) filter application.
- Intellectual property freedom-to-operate assessment.
- Chemical tractability evaluation.

Step 3.2 -- Lead Optimization

Assess DMTA cycle efficiency:
- Design-make-test-analyze (DMTA) cycle time tracking.
- Medicinal chemistry design rationale capture.
- Multiparameter optimization (MPO) scoring.
- Structure-activity relationship (SAR) tracking and visualization.
- Matched molecular pair analysis.
- Cycle time metrics: idea-to-data turnaround.

Step 3.3 -- Compound Profiling Cascade

Evaluate profiling workflow completeness:
- In vitro ADME panel: metabolic stability, permeability, solubility, plasma protein binding.
- In vitro safety panel: hERG, CYP inhibition, Ames, micronucleus.
- Selectivity panel: off-target pharmacology, kinase selectivity.
- In vivo PK studies: exposure, bioavailability, distribution.
- Efficacy models: disease-relevant in vivo or ex vivo models.
- Data integration across profiling endpoints.

============================================================
PHASE 4: ADMET PREDICTION AND MODELING
============================================================

Step 4.1 -- ADMET Model Inventory

Catalog all predictive models and verify coverage:
- Absorption: Caco-2 permeability, PAMPA, oral bioavailability prediction.
- Distribution: plasma protein binding, volume of distribution, BBB penetration.
- Metabolism: CYP substrate/inhibitor prediction, metabolic stability, metabolite ID.
- Excretion: renal clearance, hepatic clearance prediction.
- Toxicity: hERG liability, hepatotoxicity, genotoxicity, cardiotoxicity.

Step 4.2 -- Model Quality Assessment

Critically evaluate ADMET model performance:
- Training data size and chemical space coverage.
- Validation methodology: temporal split, scaffold split, random split.
- Performance metrics: R-squared, RMSE, accuracy, AUC for classification.
- Applicability domain definition and out-of-domain flagging.
- Model update frequency and retraining triggers.
- Predicted vs. measured concordance on recent compounds.

Step 4.3 -- Integration and Decision Support

Assess how models feed into decisions:
- ADMET predictions integrated into compound selection workflows.
- Multi-objective scoring: balancing potency, selectivity, ADMET.
- Visualization of ADMET profiles: radar charts, traffic-light scoring.
- Alerts for liability flags: hERG above threshold, CYP inhibition, reactive metabolites.
- Confidence scoring on predictions.

============================================================
PHASE 5: CLINICAL CANDIDATE SELECTION
============================================================

Step 5.1 -- Candidate Selection Criteria

Evaluate selection framework quality:
- Target product profile (TPP) documentation and compliance checking.
- Go/no-go criteria at each stage gate.
- Candidate selection package requirements: potency, selectivity, PK, safety.
- Backup compound strategy and pipeline depth.
- Decision-making governance: project team, portfolio committee.

Step 5.2 -- IND-Enabling Studies Tracking

Assess pre-clinical development readiness:
- GLP toxicology study planning and tracking.
- CMC (Chemistry, Manufacturing, Controls) readiness.
- Formulation development status.
- Analytical method development and validation.
- Reference standard and impurity characterization.
- Stability study planning.

Step 5.3 -- Regulatory Strategy

Evaluate IND preparation:
- FDA Pre-IND meeting preparation.
- IND application component tracking: CMC, pharmacology/toxicology, clinical.
- Regulatory pathway assessment: 505(b)(1), 505(b)(2), biosimilar.
- Orphan drug or breakthrough therapy designation evaluation.
- Timeline and milestone tracking to IND filing.

============================================================
PHASE 6: OPERATIONAL METRICS AND GOVERNANCE
============================================================

Step 6.1 -- Pipeline Metrics

Assess operational KPIs:
- DMTA cycle time: days from design to data.
- Screening throughput: compounds per week.
- Hit rate and confirmation rate by target class.
- Lead optimization progress: number of cycles, MPO improvement.
- Stage gate transition rates and timelines.
- Cost per stage: hit finding, lead optimization, candidate selection.

Step 6.2 -- Data Governance

Evaluate data integrity:
- Compound registration integrity: no duplicates, correct structures.
- Assay data quality controls and review workflows.
- Electronic lab notebook compliance.
- Data archival and long-term accessibility.
- IP documentation and invention disclosure tracking.

============================================================
PHASE 7: WRITE REPORT
============================================================

Write analysis to `docs/drug-discovery-ops-analysis.md` (create `docs/` if needed).

Include: Executive Summary, Platform Inventory, Screening Workflow Assessment,
Hit-to-Lead Pipeline Review, ADMET Model Evaluation, Candidate Selection Readiness,
Operational Metrics Dashboard, Governance Assessment, Prioritized Recommendations.

============================================================
OUTPUT
============================================================

## Drug Discovery Operations Analysis Complete

- Report: `docs/drug-discovery-ops-analysis.md`
- Pipeline stages reviewed: [count]
- Compound libraries assessed: [count]
- ADMET models evaluated: [count]
- Operational bottlenecks identified: [count]

### Summary Table
| Area | Status | Priority |
|------|--------|----------|
| Compound Library Mgmt | [PASS/WARN/FAIL] | [P1-P4] |
| Screening Workflows | [PASS/WARN/FAIL] | [P1-P4] |
| Hit-to-Lead Pipeline | [PASS/WARN/FAIL] | [P1-P4] |
| ADMET Prediction | [PASS/WARN/FAIL] | [P1-P4] |
| Candidate Selection | [PASS/WARN/FAIL] | [P1-P4] |
| IND Readiness | [PASS/WARN/FAIL] | [P1-P4] |
| Operational Metrics | [PASS/WARN/FAIL] | [P1-P4] |

NEXT STEPS:

- "Run `/regulatory-submissions` to assess eCTD assembly and FDA submission readiness."
- "Run `/lab-automation` to evaluate screening instrument automation and LIMS integration."
- "Run `/experiment-tracking` to assess compound profiling data reproducibility."

DO NOT:

- Do NOT modify any compound records, assay data, or pipeline configurations.
- Do NOT access or display proprietary chemical structures outside the analysis report.
- Do NOT make clinical efficacy or safety predictions -- flag data for expert review.
- Do NOT skip GLP compliance assessment even for early-stage discovery programs.
- Do NOT assume ADMET model accuracy without checking applicability domain and validation metrics.
