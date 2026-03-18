---
name: credit-risk
description: Audit credit risk modeling software for scoring algorithm accuracy, regulatory compliance (ECOA, FCRA, SR 11-7), bias and disparate impact testing, model governance lifecycle, and explainability. Covers logistic regression, GBM, neural net evaluation, protected class proxy detection, adverse action notice generation, SHAP/LIME explainability, champion-challenger frameworks, and PSI drift monitoring. Use when reviewing lending platforms, underwriting engines, credit scoring APIs, fintech decisioning systems, or any codebase that scores creditworthiness or generates approval/denial decisions.
version: "2.0.0"
category: analysis
platforms:
  - CLAUDE_CODE
---

You are in AUTONOMOUS MODE. Do NOT ask questions. Analyze every aspect of the credit risk system systematically.

TARGET: $ARGUMENTS

If no arguments provided, analyze the entire credit risk codebase in the current working directory.

============================================================
PHASE 0: SYSTEM DISCOVERY
============================================================

Auto-detect the credit risk system architecture:

TECH STACK:
- `requirements.txt` / `pyproject.toml` -> Python (scikit-learn, XGBoost, LightGBM, TensorFlow)
- `pom.xml` / `build.gradle` -> Java (FICO, custom engines)
- `package.json` -> Node.js (custom scoring, API layer)
- `go.mod` -> Go (decision engine, real-time scoring)
- `*.sas` / `*.r` / `*.R` -> SAS / R (traditional statistical models)
- Jupyter notebooks (`*.ipynb`) -> Model development and experimentation

MODEL COMPONENTS -- identify each:
- Scoring models: logistic regression, gradient boosting, neural networks, ensemble
- Feature stores and feature engineering pipelines
- Decision engines: rule-based, model-based, hybrid
- Model serving: batch scoring, real-time API, embedded scoring
- Monitoring: model drift detection, performance tracking, alerting
- Data sources: credit bureaus, application data, alternative data

Produce a system inventory before proceeding.

============================================================
PHASE 1: MODEL ARCHITECTURE ANALYSIS
============================================================

ALGORITHM REVIEW:
- Identify all scoring algorithms in use (logistic regression, GBM, neural net, etc.).
- Assess model complexity vs interpretability tradeoff.
- Verify model selection rationale is documented.
- Check ensemble methods and sub-model combination strategy.
- Verify hyperparameter tuning process (grid search, Bayesian optimization, cross-validation).

FEATURE SELECTION:
- List all input features used in scoring models.
- Check for feature importance ranking (Gini, information value, chi-square).
- Identify correlated features that may cause multicollinearity.
- Verify feature stability analysis across time periods.
- Check for feature drift monitoring between training and production.

MODEL VALIDATION:
- Verify out-of-sample testing methodology (train/test split, k-fold, time-based).
- Check discrimination metrics: AUC-ROC, Gini coefficient, KS statistic.
- Check calibration metrics: Hosmer-Lemeshow, calibration curves.
- Verify PSI (Population Stability Index) monitoring.
- Check for stress testing and sensitivity analysis.
- Verify backtesting against historical default data.

For each finding: record file path, model component, severity, description, recommendation.

============================================================
PHASE 2: DATA QUALITY ASSESSMENT
============================================================

INPUT DATA VALIDATION:
- Schema validation on incoming data (bureau data, application data).
- Data type enforcement (numeric fields not accepting strings, date formats).
- Range validation (age > 0, income > 0, credit score 300-850).
- Referential integrity checks across data sources.

MISSING VALUE HANDLING:
- Detection and flagging of missing values.
- Imputation strategies (mean, median, model-based, flag-and-fill).
- Missing value rate monitoring and alerting.
- Missing-at-random assumption validation.
- Flag hardcoded magic values used as missing indicators (-999, 9999, etc.).

OUTLIER DETECTION:
- Outlier detection in continuous features.
- Treatment strategy (winsorization, capping, exclusion).
- Documented and justified outlier thresholds.
- Extreme value handling in production scoring.

DATA LINEAGE:
- Data source documentation.
- Data transformation audit trail.
- Data versioning for model reproducibility.
- Training data snapshot archival.

============================================================
PHASE 3: REGULATORY COMPLIANCE
============================================================

Audit against fair lending and consumer protection regulations.

FAIR LENDING (ECOA / Regulation B / FHA):
- Verify protected class variables are excluded from models: race, color, religion, national origin, sex, marital status, age (except as permitted).
- Scan for proxy variables that correlate with protected classes: zip code (race proxy), first name (ethnicity proxy), university attended (race proxy).
- Check disparate impact analysis documentation.
- Verify adverse action notice generation meets Regulation B requirements.
- Check that specific denial reasons are provided (not generic).
- Verify adverse action reason codes map to FCRA/ECOA requirements.

ADVERSE ACTION NOTICES:
- Verify specific reason codes generated for each denial.
- Check reason codes are ordered by impact (most impactful first).
- Verify reason code descriptions are consumer-friendly.
- Check that up to 4 principal reasons are provided per ECOA requirements.
- Verify adverse action notice templates include all required disclosures.

MODEL DOCUMENTATION (SR 11-7 / OCC 2011-12):
- Model development documentation (methodology, assumptions, limitations).
- Independent model validation.
- Ongoing monitoring plan documentation.
- Model inventory/registry with version tracking.
- Model risk tier classification documentation.

FCRA COMPLIANCE:
- Permissible purpose checks before pulling credit reports.
- Accurate furnishing logic for credit bureau reporting.
- Dispute resolution workflow.
- Consumer disclosure mechanisms.

============================================================
PHASE 4: BIAS DETECTION AND FAIRNESS
============================================================

PROTECTED CLASS PROXY ANALYSIS:
- Compute correlation between each input feature and known protected attributes.
- Flag features with correlation > 0.3 to race, gender, age, or national origin.
- Check if zip code, education institution, or employer are used (common proxies).
- Verify alternative data sources (rent payments, utility data) are tested for bias.

DISPARATE IMPACT TESTING:
- Approval rate comparison across demographic groups.
- Four-fifths (80%) rule analysis.
- Marginal effect analysis on protected classes.
- Statistical significance testing on outcome differences.
- Disparate impact testing at multiple score thresholds.

FAIRNESS METRICS:
- Demographic parity measurement.
- Equalized odds / equal opportunity metrics.
- Predictive parity across groups.
- Calibration fairness (equal calibration across groups).
- Fairness-accuracy tradeoff documentation.

BIAS MITIGATION:
- Pre-processing techniques (reweighting, resampling).
- In-processing techniques (adversarial debiasing, fairness constraints).
- Post-processing adjustments (threshold optimization per group).
- Mitigation step documentation with impact analysis.

============================================================
PHASE 5: MODEL GOVERNANCE
============================================================

VERSION CONTROL:
- Model version control with reproducibility artifacts.
- Training data, code, hyperparameters, and outputs versioned together.
- Model registry (MLflow, Weights & Biases, custom).
- Rollback capability to previous model versions.

CHAMPION-CHALLENGER FRAMEWORK:
- Challenger models tested alongside production champion.
- A/B testing or shadow scoring infrastructure.
- Defined and documented champion replacement criteria.
- Performance comparison methodology.

MONITORING AND ALERTING:
- Model performance degradation detection.
- PSI monitoring on input features.
- Concept drift detection on target variable.
- Automated alerting when metrics breach thresholds.
- Regular model performance reporting cadence.

APPROVAL AND AUDIT:
- Model approval workflow (development -> validation -> approval -> deployment).
- Audit trail on model changes and approvals.
- Segregation of duties between model developers and validators.
- Documented model risk assessments.

============================================================
PHASE 6: EXPLAINABILITY AND TRANSPARENCY
============================================================

GLOBAL EXPLAINABILITY:
- Feature importance calculations (Gini, permutation, SHAP).
- Partial dependence plots or accumulated local effects.
- Global surrogate model documentation.
- Model behavior documentation for edge cases.

LOCAL EXPLAINABILITY:
- Individual prediction explanations (SHAP values, LIME).
- Reason code generation from model explanations.
- Explanation magnitudes mapped to adverse action reasons.
- Explanation consistency across similar applicants.

DOCUMENTATION:
- Model cards or model factsheets.
- Intended use and limitations documented.
- Performance metrics broken down by relevant segments.
- Known failure modes documented.


============================================================
SELF-HEALING VALIDATION (max 2 iterations)
============================================================

After producing output, validate data quality and completeness:

1. Verify all output sections have substantive content (not just headers).
2. Verify every finding references a specific file, code location, or data point.
3. Verify recommendations are actionable and evidence-based.
4. If the analysis consumed insufficient data (empty directories, missing configs),
   note data gaps and attempt alternative discovery methods.

IF VALIDATION FAILS:
- Identify which sections are incomplete or lack evidence
- Re-analyze the deficient areas with expanded search patterns
- Repeat up to 2 iterations

IF STILL INCOMPLETE after 2 iterations:
- Flag specific gaps in the output
- Note what data would be needed to complete the analysis

============================================================
OUTPUT
============================================================

## Credit Risk Model Analysis Report

**System:** [name/description]
**Stack:** [detected technologies]
**Models Found:** [count and types]

### Summary

| Category | Status | Findings | Critical |
|----------|--------|----------|----------|
| Model Architecture | [PASS/WARN/FAIL] | N | N |
| Data Quality | [PASS/WARN/FAIL] | N | N |
| Regulatory Compliance | [PASS/WARN/FAIL] | N | N |
| Bias & Fairness | [PASS/WARN/FAIL] | N | N |
| Model Governance | [PASS/WARN/FAIL] | N | N |
| Explainability | [PASS/WARN/FAIL] | N | N |

### Model Inventory

| Model | Type | Features | AUC | Last Validated | Status |
|-------|------|----------|-----|----------------|--------|

### Detailed Findings

For each category with WARN or FAIL:

#### [Category Name]

| # | Severity | File | Description | Regulation | Recommendation |
|---|----------|------|-------------|------------|----------------|

### Regulatory Risk Assessment
- **Fair Lending violations:** [count and summary]
- **Documentation gaps:** [count and summary]
- **Adverse action deficiencies:** [count and summary]
- **Model governance gaps:** [count and summary]

### Bias Analysis Summary
- **Proxy variables identified:** [list]
- **Disparate impact findings:** [summary by protected class]
- **Fairness metric results:** [summary table]

### Remediation Priority
[Ordered list by regulatory risk and severity -- compliance issues first]

============================================================
NEXT STEPS
============================================================

- "Run `/fraud-detection` to analyze fraud detection components in the lending pipeline."
- "Run `/financial-compliance` to review broader regulatory compliance (KYC/AML, BSA)."
- "Run `/owasp` to audit the scoring API for security vulnerabilities."
- "Run `/analyze` to trace data flows end-to-end across the system."


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /credit-risk — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.

============================================================
DO NOT
============================================================

- Do NOT modify any model code or scoring logic -- this is an analysis skill.
- Do NOT retrain or re-score any models.
- Do NOT access or display actual customer PII from training data or production.
- Do NOT make definitive legal conclusions -- flag issues for legal/compliance review.
- Do NOT skip regulatory compliance phases even if the system appears small.
- Do NOT assume fair lending compliance without testing -- always check for proxy variables.
- Do NOT conflate statistical correlation with confirmed disparate impact -- note confidence levels.
