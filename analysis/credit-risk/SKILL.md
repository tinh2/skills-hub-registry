---
name: credit-risk
description: Analyze credit risk modeling software for fairness, accuracy, regulatory compliance, and model governance across scoring algorithms and decision engines.
version: "1.0.0"
category: analysis
platforms:
  - CLAUDE_CODE
---

You are in AUTONOMOUS MODE. Do NOT ask questions. Analyze every aspect of the credit risk system systematically.

TARGET:
$ARGUMENTS

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

MODEL COMPONENTS:
- Identify scoring models: logistic regression, gradient boosting, neural networks, ensemble
- Identify feature stores, feature engineering pipelines, preprocessing steps
- Identify decision engines: rule-based, model-based, hybrid
- Identify model serving: batch scoring, real-time API, embedded scoring
- Identify monitoring: model drift detection, performance tracking, alerting
- Identify data sources: credit bureaus, application data, alternative data

Produce a system inventory before proceeding.

============================================================
PHASE 1: MODEL ARCHITECTURE ANALYSIS
============================================================

Evaluate the scoring model architecture:

ALGORITHM REVIEW:
- Identify all scoring algorithms in use (logistic regression, GBM, neural net, etc.)
- Check model complexity vs interpretability tradeoff
- Verify model selection rationale is documented
- Check for ensemble methods and how sub-models are combined
- Verify hyperparameter tuning process (grid search, Bayesian optimization, cross-validation)

FEATURE SELECTION:
- List all input features used in scoring models
- Check for feature importance ranking (Gini, information value, chi-square)
- Identify correlated features that may cause multicollinearity
- Verify feature stability analysis across time periods
- Check for feature drift monitoring between training and production

MODEL VALIDATION:
- Verify out-of-sample testing methodology (train/test split, k-fold, time-based)
- Check model discrimination metrics: AUC-ROC, Gini coefficient, KS statistic
- Check calibration metrics: Hosmer-Lemeshow, calibration curves
- Verify population stability index (PSI) monitoring
- Check for stress testing and sensitivity analysis
- Verify backtesting against historical default data

For each finding: file path, model component, severity, description, recommendation.

============================================================
PHASE 2: DATA QUALITY ASSESSMENT
============================================================

Evaluate data pipelines feeding the credit risk models:

INPUT DATA VALIDATION:
- Check for schema validation on incoming data (bureau data, application data)
- Verify data type enforcement (numeric fields not accepting strings, date formats)
- Check for range validation (age > 0, income > 0, credit score 300-850)
- Verify referential integrity checks across data sources

MISSING VALUE HANDLING:
- Identify how missing values are detected and flagged
- Check imputation strategies (mean, median, model-based, flag-and-fill)
- Verify missing value rates are monitored and alerted on
- Check if missing-at-random assumption is validated
- Flag hardcoded magic values used as missing indicators (-999, 9999, etc.)

OUTLIER DETECTION:
- Check for outlier detection in continuous features
- Verify outlier treatment strategy (winsorization, capping, exclusion)
- Check if outlier thresholds are documented and justified
- Verify extreme value handling in production scoring

DATA LINEAGE:
- Verify data source documentation exists
- Check for data transformation audit trail
- Verify data versioning for model reproducibility
- Check that training data snapshots are archived

============================================================
PHASE 3: REGULATORY COMPLIANCE
============================================================

Audit against fair lending and consumer protection regulations:

FAIR LENDING (ECOA / Regulation B / FHA):
- Check if protected class variables are excluded from models:
  race, color, religion, national origin, sex, marital status, age (except as permitted)
- Scan for proxy variables that correlate with protected classes:
  zip code (race proxy), first name (ethnicity proxy), university attended (race proxy)
- Check if disparate impact analysis is performed and documented
- Verify adverse action notice generation meets Regulation B requirements
- Check that specific reasons for denial are provided (not generic)
- Verify adverse action reason codes map to FCRA/ECOA requirements

ADVERSE ACTION NOTICES:
- Verify the system generates specific reason codes for each denial
- Check that reason codes are ordered by impact (most impactful first)
- Verify reason code descriptions are consumer-friendly
- Check that up to 4 principal reasons are provided per ECOA requirements
- Verify adverse action notice templates include all required disclosures

MODEL DOCUMENTATION (SR 11-7 / OCC 2011-12):
- Check for model development documentation (methodology, assumptions, limitations)
- Verify model validation is performed by independent team
- Check for ongoing monitoring plan documentation
- Verify model inventory/registry exists with version tracking
- Check that model risk tier classification is documented

FCRA COMPLIANCE:
- Verify permissible purpose checks before pulling credit reports
- Check that furnishing logic accurately reports to credit bureaus
- Verify dispute resolution workflow exists
- Check consumer disclosure mechanisms

============================================================
PHASE 4: BIAS DETECTION AND FAIRNESS
============================================================

Analyze for discriminatory patterns:

PROTECTED CLASS PROXY ANALYSIS:
- Compute correlation between each input feature and known protected attributes
- Flag features with correlation > 0.3 to race, gender, age, or national origin
- Check if zip code, education institution, or employer are used (common proxies)
- Verify alternative data sources (rent payments, utility data) are tested for bias

DISPARATE IMPACT TESTING:
- Check if approval rates are compared across demographic groups
- Verify four-fifths (80%) rule analysis is performed
- Check for marginal effect analysis on protected classes
- Verify statistical significance testing on outcome differences
- Check if disparate impact is tested at multiple score thresholds

FAIRNESS METRICS:
- Check for demographic parity measurement
- Verify equalized odds / equal opportunity metrics
- Check predictive parity across groups
- Verify calibration fairness (equal calibration across groups)
- Check if fairness-accuracy tradeoff is documented

BIAS MITIGATION:
- Check for pre-processing bias mitigation (reweighting, resampling)
- Verify in-processing techniques (adversarial debiasing, fairness constraints)
- Check post-processing adjustments (threshold optimization per group)
- Verify that mitigation steps are documented with impact analysis

============================================================
PHASE 5: MODEL GOVERNANCE
============================================================

Evaluate the model lifecycle and governance framework:

VERSION CONTROL:
- Check if models are version-controlled with reproducibility artifacts
- Verify training data, code, hyperparameters, and outputs are versioned together
- Check for model registry (MLflow, Weights & Biases, custom)
- Verify rollback capability to previous model versions

CHAMPION-CHALLENGER FRAMEWORK:
- Check if challenger models are tested alongside production champion
- Verify A/B testing or shadow scoring infrastructure exists
- Check that champion replacement criteria are defined and documented
- Verify performance comparison methodology

MONITORING AND ALERTING:
- Check for model performance degradation detection
- Verify PSI (Population Stability Index) monitoring on input features
- Check for concept drift detection on target variable
- Verify automated alerting when metrics breach thresholds
- Check for regular model performance reporting cadence

APPROVAL AND AUDIT:
- Verify model approval workflow exists (development -> validation -> approval -> deployment)
- Check for audit trail on model changes and approvals
- Verify segregation of duties between model developers and validators
- Check that model risk assessments are documented

============================================================
PHASE 6: EXPLAINABILITY AND TRANSPARENCY
============================================================

Evaluate model interpretability:

GLOBAL EXPLAINABILITY:
- Check for feature importance calculations (Gini, permutation, SHAP)
- Verify partial dependence plots or accumulated local effects
- Check for global surrogate model documentation
- Verify model behavior documentation for edge cases

LOCAL EXPLAINABILITY:
- Check for individual prediction explanations (SHAP values, LIME)
- Verify reason code generation from model explanations
- Check that explanation magnitudes map to adverse action reasons
- Verify explanations are consistent across similar applicants

DOCUMENTATION:
- Check for model cards or model factsheets
- Verify intended use and limitations are documented
- Check that performance metrics are broken down by relevant segments
- Verify that known failure modes are documented

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
[Ordered list by regulatory risk and severity — compliance issues first]

============================================================
NEXT STEPS
============================================================

After reviewing the analysis:
- "Run `/fraud-detection` to analyze fraud detection components in the lending pipeline."
- "Run `/financial-compliance` to review broader regulatory compliance (KYC/AML, BSA)."
- "Run `/owasp` to audit the scoring API for security vulnerabilities."
- "Run `/analyze` to trace data flows end-to-end across the system."

============================================================
DO NOT
============================================================

- Do NOT modify any model code or scoring logic — this is an analysis skill.
- Do NOT retrain or re-score any models.
- Do NOT access or display actual customer PII from training data or production.
- Do NOT make definitive legal conclusions — flag issues for legal/compliance review.
- Do NOT skip regulatory compliance phases even if the system appears small.
- Do NOT assume fair lending compliance without testing — always check for proxy variables.
- Do NOT conflate statistical correlation with confirmed disparate impact — note confidence levels.
