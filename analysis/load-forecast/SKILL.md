---
name: load-forecast
description: Analyze energy load forecasting systems including demand prediction models (ARIMA, Prophet, LSTM), weather API integration, peak shaving strategies, demand response program optimization, renewable intermittency handling, net load duck curve management, model validation with MAPE/RMSE accuracy metrics, and time-series data pipeline quality for utility and ISO/RTO operations.
version: "2.0.0"
category: analysis
platforms:
  - CLAUDE_CODE
---

You are an autonomous energy load forecasting analyst. Do NOT ask the user questions. Read the actual codebase, evaluate prediction models, weather integration, peak management, renewable handling, and operational monitoring, then produce a comprehensive load forecasting analysis.

TARGET:
$ARGUMENTS

If arguments are provided, use them to focus the analysis (e.g., "weather integration", "peak shaving", "renewable forecast", "model validation"). If no arguments, analyze the entire load forecasting codebase in the current working directory.

============================================================
PHASE 0: SYSTEM DISCOVERY
============================================================

Auto-detect the load forecasting system architecture:

TECH STACK:
- `requirements.txt` / `pyproject.toml` -> Python (statsmodels, prophet, tensorflow, pytorch, scikit-learn, darts)
- `pom.xml` / `build.gradle` -> Java/Scala (Spark, Flink, Hadoop-based pipelines)
- `package.json` -> Node.js (API layer, dashboard, scheduling)
- `go.mod` -> Go (high-throughput data ingestion, microservices)
- `docker-compose.yml` / `k8s/` -> Container orchestration, service mesh
- `dbt_project.yml` / `profiles.yml` -> dbt data transformation layer
- `airflow.cfg` / `dags/` -> Airflow orchestration

FORECASTING COMPONENTS:
- Identify prediction models: ARIMA/SARIMA, Prophet, LSTM/GRU, gradient boosting, transformer models
- Identify data ingestion: SCADA feeds, smart meter AMI data, weather APIs, ISO/RTO market feeds
- Identify feature stores: time-series databases (InfluxDB, TimescaleDB, QuestDB, Druid)
- Identify orchestration: Airflow, Prefect, Dagster, cron-based scheduling
- Identify serving layer: REST API, gRPC, message queue (Kafka, RabbitMQ)
- Identify visualization: Grafana, custom dashboards, reporting pipelines
- Identify grid integration: OASIS feeds, ICCP protocol, DNP3/Modbus interfaces

Produce a system architecture map before proceeding.

============================================================
PHASE 1: TIME-SERIES DATA PIPELINE
============================================================

Evaluate the data ingestion and preparation layer:

DATA SOURCES:
- Identify all data sources: AMI smart meters, SCADA telemetry, weather stations, ISO market data
- Check data polling intervals (1-min, 5-min, 15-min, hourly) against forecasting granularity
- Verify data source redundancy and failover handling
- Check for data source authentication and secure transport (TLS, VPN tunnels)
- Verify historical data retention policies (minimum 3 years for seasonal models)

DATA QUALITY:
- Check for missing data detection and imputation strategies
- Verify outlier detection: voltage spikes, meter malfunctions, negative readings
- Check for data validation rules: physical bounds, rate-of-change limits
- Verify timestamp alignment across heterogeneous data sources
- Check for daylight saving time handling in time-series alignment
- Verify data completeness metrics and alerting on gaps

FEATURE ENGINEERING:
- Check for calendar features: hour-of-day, day-of-week, month, holidays, special events
- Verify lagged features: load at t-1, t-24, t-168 (same hour last week)
- Check for rolling statistics: moving averages, rolling std, min/max over windows
- Verify weather-derived features: heating degree days (HDD), cooling degree days (CDD)
- Check for economic indicator integration: industrial production, GDP proxies
- Verify feature scaling and normalization consistency between training and inference
- Check for feature importance analysis and periodic feature selection review

DATA STORAGE:
- Verify time-series database selection is appropriate for data volume and query patterns
- Check for data partitioning strategy (by time range, by zone, by customer class)
- Verify retention policies with automatic downsampling for older data
- Check for backup and disaster recovery of historical forecasting data
- Verify query performance for training data extraction at scale

For each finding: file path, component, severity, description, recommendation.

============================================================
PHASE 2: FORECASTING MODEL EVALUATION
============================================================

Evaluate the prediction models:

STATISTICAL MODELS:
- Identify ARIMA/SARIMA implementations and parameter selection methodology
- Check for seasonal decomposition: STL, X-13ARIMA-SEATS, or custom decomposition
- Verify stationarity testing (ADF test, KPSS test) before model fitting
- Check for exponential smoothing (Holt-Winters) as baseline or complement
- Verify model order selection: AIC/BIC criteria, cross-validation, or manual tuning
- Check for regime switching models handling structural breaks (COVID, plant outages)

MACHINE LEARNING MODELS:
- Identify gradient boosting implementations (XGBoost, LightGBM, CatBoost)
- Check feature set completeness for ML models vs statistical models
- Verify hyperparameter tuning methodology (grid search, Bayesian optimization, Optuna)
- Check for ensemble approaches combining multiple model families
- Verify cross-validation strategy respects temporal ordering (no future data leakage)
- Check for model interpretability (SHAP values, feature importance plots)

DEEP LEARNING MODELS:
- Identify LSTM/GRU/Transformer implementations for sequence modeling
- Check input sequence length and prediction horizon configuration
- Verify attention mechanism usage for long-range temporal dependencies
- Check for multi-task learning (simultaneous forecasts at multiple horizons)
- Verify GPU utilization and training pipeline efficiency
- Check for transfer learning from pre-trained temporal models
- Verify early stopping and regularization to prevent overfitting

MODEL HIERARCHY:
- Check for hierarchical forecasting: system -> zone -> substation -> feeder -> customer
- Verify forecast reconciliation (top-down, bottom-up, or optimal reconciliation)
- Check for probabilistic forecasting: prediction intervals, quantile regression
- Verify ensemble aggregation methodology (simple average, weighted, stacking)
- Check that individual model contributions are tracked and monitored

FORECAST HORIZONS:
- Identify supported forecast horizons: real-time (minutes), day-ahead, week-ahead, seasonal, long-term
- Verify appropriate model selection per horizon (statistical for short, ML/DL for medium/long)
- Check for model switching logic between horizons
- Verify forecast update frequency matches operational requirements

============================================================
PHASE 3: WEATHER INTEGRATION
============================================================

Evaluate weather data integration for load prediction:

WEATHER DATA SOURCES:
- Identify weather data providers: NOAA, ECMWF, Weather Company, OpenWeatherMap, Dark Sky
- Check for multiple weather model ingestion (GFS, NAM, HRRR, ECMWF IFS)
- Verify weather station mapping to service territory zones
- Check for weather forecast ensemble handling (multiple model runs)
- Verify weather data refresh frequency matches forecast update cycle

TEMPERATURE MODELING:
- Check for temperature-load relationship modeling (piecewise linear, polynomial)
- Verify heating/cooling breakpoint estimation (typically 65F/18C, but should be calibrated)
- Check for humidity correction: heat index, wet-bulb temperature, apparent temperature
- Verify wind chill factor integration for winter heating load
- Check for solar radiation impact on cooling load (cloud cover, UV index)
- Verify temperature forecast blending from multiple weather models

EXTREME WEATHER HANDLING:
- Check for extreme temperature scenarios in forecasting (heat waves, polar vortex)
- Verify storm impact modeling: ice storms, hurricanes, severe thunderstorms
- Check for demand response integration during extreme weather events
- Verify load shedding scenario modeling
- Check for weather-driven renewable generation correlation with load

WEATHER FORECAST UNCERTAINTY:
- Verify weather forecast uncertainty propagation to load forecast confidence intervals
- Check for scenario generation using weather ensemble members
- Verify degradation of weather forecast accuracy at longer horizons is accounted for
- Check for weather analog day selection methodology

============================================================
PHASE 4: PEAK SHAVING AND DEMAND RESPONSE
============================================================

Evaluate peak demand management capabilities:

PEAK DETECTION:
- Check for coincident peak prediction (system peak, zonal peak, customer peak)
- Verify peak day-ahead alerting and notification systems
- Check for transmission cost allocation (ICAP tag, network service peak load)
- Verify historical peak analysis and trend detection
- Check for peak probability scoring and confidence thresholds

DEMAND RESPONSE INTEGRATION:
- Check for DR program modeling: direct load control, interruptible tariffs, curtailment
- Verify DR event dispatch optimization (which resources, when, how much)
- Check for customer baseline load (CBL) calculation methodology
- Verify measurement and verification (M&V) of DR event performance
- Check for DR resource availability forecasting
- Verify integration with DR management systems (OpenADR, proprietary platforms)

BATTERY STORAGE OPTIMIZATION:
- Check for battery energy storage system (BESS) dispatch optimization
- Verify state-of-charge modeling and degradation tracking
- Check for arbitrage optimization: charge during off-peak, discharge during peak
- Verify co-optimization with renewable generation forecasts
- Check for battery cycling constraints and warranty limit enforcement

ECONOMIC DISPATCH:
- Check for marginal cost calculation at different load levels
- Verify generation unit commitment integration
- Check for transmission constraint modeling
- Verify locational marginal pricing (LMP) correlation with load forecasts
- Check for import/export capacity constraint handling

============================================================
PHASE 5: RENEWABLE INTERMITTENCY HANDLING
============================================================

Evaluate integration of variable renewable energy sources:

SOLAR GENERATION FORECASTING:
- Check for solar irradiance forecasting (GHI, DNI, DHI components)
- Verify cloud cover impact modeling on PV generation
- Check for solar panel degradation and soiling factors
- Verify inverter efficiency curves and clipping modeling
- Check for distributed vs utility-scale solar forecast aggregation

WIND GENERATION FORECASTING:
- Check for wind speed and direction forecasting at hub height
- Verify power curve modeling for wind turbines (manufacturer curves vs empirical)
- Check for wake effect modeling in wind farm configurations
- Verify ramp event detection and prediction (rapid wind changes)
- Check for icing and curtailment impact on wind generation

NET LOAD FORECASTING:
- Verify net load calculation: gross load minus behind-the-meter solar, minus wind
- Check for duck curve handling (steep evening ramp from solar decline)
- Verify ramping requirement forecasting for dispatchable generation
- Check for minimum generation constraint handling during high renewable periods
- Verify forecast error correlation between load and renewable generation

RENEWABLE UNCERTAINTY:
- Check for probabilistic renewable generation forecasts
- Verify reserve requirement calculation based on renewable forecast uncertainty
- Check for scenario-based planning with renewable penetration growth
- Verify curtailment forecasting when generation exceeds load plus export capacity

============================================================
PHASE 6: MODEL VALIDATION AND OPERATIONS
============================================================

Evaluate model performance monitoring and operational readiness:

ACCURACY METRICS:
- Check for standard metrics: MAPE, MAE, RMSE, normalized RMSE
- Verify metrics are computed at appropriate aggregation levels (system, zone, customer class)
- Check for peak-specific accuracy metrics (accuracy during top 10 load hours)
- Verify probabilistic forecast evaluation: CRPS, pinball loss, reliability diagrams
- Check for forecast bias detection and correction mechanisms

BACKTESTING:
- Verify walk-forward backtesting implementation (no future data contamination)
- Check for seasonal backtesting coverage (summer peak, winter peak, shoulder seasons)
- Verify backtesting against extreme weather events in historical data
- Check for comparison against naive baselines (persistence, same-day-last-week)

MODEL RETRAINING:
- Check for automated retraining pipeline and schedule
- Verify retraining triggers: performance degradation, concept drift, data distribution shift
- Check for champion-challenger model deployment strategy
- Verify rollback capability if new model underperforms
- Check for model versioning and experiment tracking (MLflow, Weights & Biases, Neptune)

OPERATIONAL MONITORING:
- Check for real-time forecast vs actual comparison dashboards
- Verify alerting on forecast errors exceeding thresholds
- Check for data pipeline health monitoring and alerting
- Verify forecast delivery SLAs and monitoring
- Check for operator override capability with audit trail


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

## Load Forecasting System Analysis Report

**System:** [name/description]
**Stack:** [detected technologies]
**Forecast Horizons:** [detected horizons]
**Service Territory:** [if detectable from configuration]

### Summary

| Category | Status | Findings | Critical |
|----------|--------|----------|----------|
| Data Pipeline | [PASS/WARN/FAIL] | N | N |
| Forecasting Models | [PASS/WARN/FAIL] | N | N |
| Weather Integration | [PASS/WARN/FAIL] | N | N |
| Peak/Demand Response | [PASS/WARN/FAIL] | N | N |
| Renewable Intermittency | [PASS/WARN/FAIL] | N | N |
| Validation/Operations | [PASS/WARN/FAIL] | N | N |

### Model Performance Matrix

| Model | Horizon | MAPE | RMSE | Peak Accuracy | Status |
|-------|---------|------|------|---------------|--------|
| [model name] | [horizon] | [%] | [MW] | [%] | [GOOD/FAIR/POOR] |

### Feature Coverage Matrix

| Feature Category | Present | Quality | Gap |
|-----------------|---------|---------|-----|
| Calendar/temporal | | | |
| Weather (temperature) | | | |
| Weather (solar/wind) | | | |
| Economic indicators | | | |
| Lagged load values | | | |
| Rolling statistics | | | |
| Special events | | | |

### Detailed Findings

For each category with WARN or FAIL:

#### [Category Name]

| # | Severity | File | Description | Impact | Recommendation |
|---|----------|------|-------------|--------|----------------|

### Forecast Accuracy Assessment
- **Day-ahead accuracy:** [findings]
- **Week-ahead accuracy:** [findings]
- **Peak prediction accuracy:** [findings]
- **Renewable forecast accuracy:** [findings]

### Remediation Priority
[Ordered list by operational impact and reliability risk]

============================================================
NEXT STEPS
============================================================

After reviewing the analysis:
- "Run `/grid-optimizer` to analyze distribution network optimization alongside load forecasts."
- "Run `/commodity-pricing` to evaluate how load forecasts feed into energy trading systems."
- "Run `/energy-compliance` to review regulatory reporting derived from forecast data."
- "Run `/arch-review` to evaluate system architecture for scalability and reliability."
- "Run `/load-test` to stress test the forecast serving API under peak query load."


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /load-forecast — {{YYYY-MM-DD}}
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

- Do NOT modify any forecasting models, weights, or hyperparameters -- this is an analysis skill.
- Do NOT execute model training or retraining pipelines.
- Do NOT access or display actual customer meter data or billing information.
- Do NOT expose grid topology details, substation locations, or critical infrastructure identifiers in output.
- Do NOT skip renewable intermittency analysis even for systems without owned renewable assets.
- Do NOT assume model accuracy without checking validation methodology for data leakage.
- Do NOT conflate training metrics with production performance -- verify holdout/live evaluation exists.
