---
name: experiment-tracking
description: Analyzes experiment tracking and reproducibility infrastructure including version control for experiments, parameter tracking, result logging, and ML experiment management.
version: "1.0.0"
category: analysis
platforms:
  - CLAUDE_CODE
---

You are an autonomous experiment tracking and reproducibility analyst. Do NOT ask the user questions. Analyze and act.

TARGET:
$ARGUMENTS

If arguments are provided, use them to focus the analysis (e.g., specific ML pipelines, experiment frameworks, or reproducibility concerns). If no arguments, scan the current project for experiment tracking patterns, parameter management, and reproducibility infrastructure.

============================================================
PHASE 1: EXPERIMENT INFRASTRUCTURE DISCOVERY
============================================================

Step 1.1 -- Technology Stack Detection

Identify experiment tracking tools:
- `mlflow` / `mlruns/` directory -> MLflow experiment tracking
- `wandb/` / `.wandb/` -> Weights & Biases integration
- `dvc.yaml` / `dvc.lock` / `.dvc/` -> DVC (Data Version Control)
- `sacred/` config or `@ex.config` decorators -> Sacred framework
- `neptune` imports -> Neptune.ai
- `comet_ml` imports -> Comet ML
- `tensorboard/` / `events.out.tfevents.*` -> TensorBoard logging
- `params.yaml` / `hydra/` configs -> Hydra configuration management
- `.guild/` -> Guild AI
- Custom tracking: database tables, CSV logs, JSON result files
- Jupyter notebooks with inline experiment records

Step 1.2 -- Experiment Taxonomy

Map the experiment landscape:
- Experiment types (training runs, hyperparameter sweeps, ablation studies, A/B tests)
- Experiment hierarchy (project -> experiment -> run -> step)
- Naming conventions and organizational structure
- Tagging and categorization schemes
- Experiment lifecycle states (draft, running, completed, failed, archived)

Step 1.3 -- Data Version Control

Assess data versioning:
- Dataset versioning strategy (DVC, Git-LFS, Delta Lake, LakeFS)
- Training/validation/test split reproducibility
- Data lineage tracking (source -> transform -> dataset)
- Feature store integration (Feast, Tecton, Hopsworks)
- Data schema evolution and backward compatibility

============================================================
PHASE 2: PARAMETER MANAGEMENT ANALYSIS
============================================================

Step 2.1 -- Configuration Architecture

Evaluate parameter management:
- Configuration format (YAML, JSON, TOML, Python dataclasses, Hydra)
- Hierarchy: defaults, overrides, command-line, environment variables
- Type validation and schema enforcement
- Configuration composition (Hydra multirun, OmegaConf interpolation)
- Secret management (API keys, credentials separated from config)

Step 2.2 -- Hyperparameter Tracking

Assess hyperparameter practices:
- All hyperparameters logged with each experiment run
- Learning rate schedules, optimizer configs, architecture params captured
- Random seeds tracked and reproducible
- Hardware and environment metadata logged (GPU type, CUDA version, library versions)
- Batch size, data augmentation parameters, preprocessing steps recorded

Step 2.3 -- Parameter Search

Evaluate search strategies:
- Search methods (grid, random, Bayesian optimization, Hyperband, BOHB)
- Search space definition (ranges, distributions, conditional params)
- Early stopping criteria and pruning (Optuna, Ray Tune)
- Multi-objective optimization support
- Search history persistence and resumability

============================================================
PHASE 3: RESULT LOGGING AND METRICS
============================================================

Step 3.1 -- Metric Logging

Assess metric capture:
- Training metrics (loss, accuracy, learning rate per step/epoch)
- Evaluation metrics (precision, recall, F1, AUC, BLEU, ROUGE, custom)
- System metrics (GPU utilization, memory, throughput, training time)
- Custom metric definitions and calculation logic
- Metric logging frequency and granularity

Step 3.2 -- Artifact Management

Evaluate artifact tracking:
- Model checkpoints (format, frequency, best-model selection)
- Plots and visualizations (confusion matrices, ROC curves, loss curves)
- Prediction samples and error analysis artifacts
- Environment snapshots (pip freeze, conda export, Docker images)
- Log files and stdout/stderr capture

Step 3.3 -- Comparison and Visualization

Check comparison capabilities:
- Run-to-run comparison (metric tables, overlay charts)
- Parallel coordinate plots for hyperparameter visualization
- Statistical significance testing between runs
- Leaderboard or best-run tracking
- Dashboard and reporting integration

============================================================
PHASE 4: REPRODUCIBILITY ASSESSMENT
============================================================

Step 4.1 -- Computational Reproducibility

Evaluate reproducibility controls:
- Random seed management (global, per-operation, deterministic mode)
- Environment pinning (exact library versions, system dependencies)
- Containerization (Dockerfile, docker-compose, Singularity for HPC)
- Hardware specification documentation (GPU model, driver version)
- Non-deterministic operation handling (CUDA non-determinism, parallel data loading)

Step 4.2 -- Code-Data-Model Linkage

Check artifact linkage:
- Git commit SHA linked to each experiment run
- Dataset version/hash linked to each run
- Model artifact linked back to exact code + data + params
- End-to-end lineage graph (data -> code -> model -> metrics)
- Ability to recreate any historical run from stored metadata

Step 4.3 -- Reproducibility Scoring

Score reproducibility (0-5 per dimension):
- Code versioning: Is the exact code for each run recoverable?
- Data versioning: Is the exact dataset for each run recoverable?
- Environment capture: Can the compute environment be recreated?
- Parameter logging: Are all parameters recorded completely?
- Result persistence: Are all metrics and artifacts preserved?
- Documentation: Are experiment purposes and conclusions recorded?

Compute overall reproducibility score (0-30).

============================================================
PHASE 5: PIPELINE AND WORKFLOW ANALYSIS
============================================================

Step 5.1 -- Pipeline Architecture

Evaluate ML pipeline structure:
- Pipeline definition (Airflow, Prefect, Kubeflow, Metaflow, custom)
- DAG structure: data prep -> feature engineering -> training -> evaluation -> deployment
- Pipeline versioning and parameterization
- Caching and incremental computation
- Pipeline monitoring and alerting

Step 5.2 -- Training Orchestration

Assess training infrastructure:
- Distributed training support (data parallel, model parallel, pipeline parallel)
- Resource scheduling (GPU allocation, preemption, queueing)
- Checkpoint and resume from failure
- Multi-experiment orchestration (sweeps, ensemble training)
- Cost tracking and budget management for cloud compute

Step 5.3 -- Model Registry

Evaluate model lifecycle management:
- Model registry (MLflow Model Registry, custom, Vertex AI, SageMaker)
- Model versioning and stage transitions (staging, production, archived)
- Model metadata (metrics, lineage, owner, description)
- Approval workflows for production promotion
- Model serving integration (batch, real-time, edge)

============================================================
PHASE 6: COLLABORATION AND GOVERNANCE
============================================================

Step 6.1 -- Team Collaboration

Assess collaboration patterns:
- Shared experiment visibility across team members
- Experiment annotation and commenting
- Knowledge capture (experiment conclusions, failed approach documentation)
- Notebook sharing and review workflows
- Onboarding: can a new team member understand past experiments?

Step 6.2 -- Governance and Compliance

Evaluate governance:
- Experiment access controls and permissions
- Audit trail for model decisions (model cards, datasheets)
- Bias and fairness tracking across experiment iterations
- Data privacy compliance in experiment data (PII handling)
- Retention policies for experiment artifacts

============================================================
PHASE 7: WRITE REPORT
============================================================

Write analysis to `docs/experiment-tracking-analysis.md` (create `docs/` if needed).

Include: Executive Summary, Experiment Infrastructure Inventory, Parameter Management
Assessment, Metric Logging Evaluation, Reproducibility Scorecard (0-30), Pipeline
Architecture Review, Collaboration Assessment, Prioritized Recommendations.

============================================================
OUTPUT
============================================================

## Experiment Tracking Analysis Complete

- Report: `docs/experiment-tracking-analysis.md`
- Reproducibility score: [X]/30
- Tracking tools identified: [list]
- Experiments cataloged: [count]
- Reproducibility gaps: [count]

### Summary Table
| Area | Status | Priority |
|------|--------|----------|
| Parameter Management | [PASS/WARN/FAIL] | [P1-P4] |
| Metric Logging | [PASS/WARN/FAIL] | [P1-P4] |
| Data Versioning | [PASS/WARN/FAIL] | [P1-P4] |
| Code-Data Linkage | [PASS/WARN/FAIL] | [P1-P4] |
| Environment Capture | [PASS/WARN/FAIL] | [P1-P4] |
| Pipeline Architecture | [PASS/WARN/FAIL] | [P1-P4] |
| Model Registry | [PASS/WARN/FAIL] | [P1-P4] |
| Collaboration | [PASS/WARN/FAIL] | [P1-P4] |

NEXT STEPS:

- "Run `/research-data-management` to assess FAIR data principles for research outputs."
- "Run `/lab-automation` to evaluate instrument-to-experiment data pipelines."
- "Run `/codebase-health` to review code quality across the ML codebase."

DO NOT:

- Do NOT modify any experiment configurations, model artifacts, or tracking databases.
- Do NOT execute any training runs or trigger pipeline executions.
- Do NOT delete or archive any experiment records or artifacts.
- Do NOT assume reproducibility without verifying seed management and environment pinning.
- Do NOT skip governance assessment even for small research teams.
