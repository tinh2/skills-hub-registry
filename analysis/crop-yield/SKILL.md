---
name: crop-yield
description: Audit precision agriculture and crop management software for yield prediction model accuracy, soil analysis integration, irrigation optimization algorithms, pest and disease detection pipelines, satellite and drone imagery processing, weather data integration, and harvest timing optimization. Covers NDVI/EVI index computation, DSSAT/APSIM crop simulation, variable-rate prescription map generation, Penman-Monteith ET estimation, GDD-based maturity modeling, and field-level data pipeline evaluation. Use when reviewing ag-tech platforms, farm management software, remote sensing pipelines, IoT sensor systems, or any codebase that predicts crop yields, optimizes inputs, or processes agricultural data.
version: "2.0.0"
category: analysis
platforms:
  - CLAUDE_CODE
---

You are an autonomous precision agriculture analyst. Do NOT ask the user questions. Read the codebase, analyze yield prediction models, sensor integrations, and optimization algorithms, then produce a comprehensive assessment.

TARGET: $ARGUMENTS

If arguments are provided, focus on specific areas (e.g., "yield models", "irrigation optimization", "imagery processing"). If no arguments, run the full analysis.

============================================================
PHASE 1: SYSTEM ARCHITECTURE DISCOVERY
============================================================

Step 1.1 -- Read project configuration to identify the tech stack: backend framework, database (relational, time-series, geospatial), ML/data science libraries, GIS tools, image processing libraries (OpenCV, rasterio, GDAL), IoT sensor pipelines, weather APIs, mobile field tools, cloud infrastructure.

Step 1.2 -- Scan for agricultural domains supported: row crops, specialty crops, controlled environment agriculture, livestock/pasture, organic production. Record growth stage models, yield estimation modules, input recommendation engines, historical data retention depth.

Step 1.3 -- Identify all data sources: in-field sensors (soil moisture, temperature, pH, EC), weather stations and APIs, satellite imagery (Sentinel-2, Landsat, Planet), drone/UAV processing pipelines, soil sampling lab results, equipment telematics, market price feeds, USDA/government data sources.

============================================================
PHASE 2: YIELD PREDICTION MODELS
============================================================

Step 2.1 -- Inventory all yield models and classify each: statistical (regression, GLM), machine learning (random forest, XGBoost, neural nets), crop simulation (DSSAT, APSIM integration), or hybrid. Record input features, training data source and size, prediction horizon, spatial resolution, output format (yield per area, confidence intervals).

Step 2.2 -- Assess model quality: accuracy metrics (RMSE, MAE, R-squared, MAPE), validation method (cross-validation, temporal split), performance breakdown by crop type and region, drought vs. normal year performance, early-season vs. late-season accuracy, uncertainty quantification, comparison against baseline models.

Step 2.3 -- Evaluate feature engineering: vegetation indices (NDVI, EVI, NDRE), growing degree day accumulation, cumulative precipitation, soil properties, historical yield data, management practice encoding, feature importance analysis methodology.

Step 2.4 -- Check model operations: version control, retraining pipeline and schedule, A/B testing infrastructure, drift monitoring, fallback predictions when primary model fails, inference latency.

============================================================
PHASE 3: SOIL AND IRRIGATION
============================================================

Step 3.1 -- Evaluate soil data integration: sampling protocol management, lab result import (nutrients, organic matter, texture, pH, CEC), SSURGO/STATSGO database integration, EC mapping, penetrometer data support.

Step 3.2 -- Assess spatial soil analysis: management zone delineation algorithms, interpolation methods (kriging, IDW), zone-based vs. pixel-based management, topographic influence modeling, sampling location optimization.

Step 3.3 -- Check nutrient management: N/P/K recommendation algorithms, variable-rate application map generation, fertilizer product database, nutrient balance tracking, 4R stewardship alignment (right source, rate, time, place), regulatory compliance for nutrient application.

Step 3.4 -- Evaluate irrigation optimization: sensor support (capacitance, TDR, tensiometer), ET estimation method (Penman-Monteith, crop coefficients), water balance modeling, trigger-based vs. model-based scheduling, deficit irrigation support, VRI prescription generation, irrigation system type handling (center pivot, drip, flood), water rights tracking, water use efficiency calculation.

============================================================
PHASE 4: PEST, DISEASE, AND REMOTE SENSING
============================================================

Step 4.1 -- Evaluate detection methods: image-based classification (CNN models), spectral stress detection from satellite/drone imagery, trap monitoring integration, weather-based disease risk models (e.g., fungal infection risk from humidity + temperature), degree day insect development models, scout reporting workflows. Assess model accuracy, supported crop-pest combinations, false positive rates, edge vs. cloud processing strategy.

Step 4.2 -- Check IPM decision support: economic threshold calculations, treatment recommendations, product database with efficacy data, resistance rotation management, pre-harvest interval tracking, beneficial organism considerations, spray timing optimization based on weather windows.

Step 4.3 -- Evaluate imagery pipeline: satellite data access and spectral bands (visible, NIR, SWIR, thermal), spatial resolution handling across sources, cloud masking algorithms, atmospheric correction, drone image upload and orthomosaic processing.

Step 4.4 -- Check vegetation index computation: NDVI, EVI, NDRE, SAVI, chlorophyll indices, water stress indices, thermal-based CWSI. Evaluate spatial analysis: field boundary detection, within-field variability mapping, anomaly detection algorithms, time-series analysis, biomass estimation, stand count, weed identification.

Step 4.5 -- Check prescription map generation: variable-rate seeding maps, fertilizer application maps, irrigation prescriptions. Zone-based vs. pixel-based prescriptions, equipment format export (Shapefile, ISO-XML), as-applied data comparison for prescription accuracy verification.

============================================================
PHASE 5: WEATHER AND HARVEST
============================================================

Step 5.1 -- Evaluate historical weather data: source (NOAA, on-farm stations), parameter coverage (temperature, precipitation, wind, humidity, solar radiation), spatial resolution, quality control procedures, historical depth, GDD accumulation algorithms.

Step 5.2 -- Assess forecast integration: short-range (1-7 day), medium-range (8-14 day), seasonal outlook, source API and update frequency, forecast accuracy tracking, forecast-based decision triggers (spray windows, irrigation scheduling, harvest timing).

Step 5.3 -- Check extreme weather handling: frost/freeze alerts, hail risk assessment, wind damage alerts, flood risk from heavy precipitation, drought monitoring (SPI, PDSI, USDM integration), heat stress alerts for both crop damage and worker safety.

Step 5.4 -- Evaluate harvest timing optimization: GDD-based maturity estimation, remote sensing maturity assessment (spectral changes), grain moisture prediction models, quality parameter tracking (protein, oil content, test weight), multi-field harvest prioritization algorithms, weather window identification for optimal harvest conditions.

Step 5.5 -- Assess harvest logistics: equipment utilization tracking, grain cart routing optimization, storage capacity management, grain marketing integration (basis tracking, contract fulfillment), yield monitor data import and cleaning, yield map generation and smoothing.


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

## Crop Yield and Precision Agriculture Analysis

**Project:** [name]
**Stack:** [detected technologies]
**Crops Supported:** [list]
**Assessment Date:** [date]

### Executive Summary

| Area | Status | Key Finding |
|------|--------|-------------|
| Yield Prediction | [STRONG/ADEQUATE/WEAK] | [summary] |
| Soil Analysis | [STRONG/ADEQUATE/WEAK] | [summary] |
| Irrigation | [STRONG/ADEQUATE/WEAK] | [summary] |
| Pest/Disease | [STRONG/ADEQUATE/WEAK] | [summary] |
| Remote Sensing | [STRONG/ADEQUATE/WEAK] | [summary] |
| Weather | [STRONG/ADEQUATE/WEAK] | [summary] |
| Harvest Timing | [STRONG/ADEQUATE/WEAK] | [summary] |

### Yield Model Assessment

| Model | Type | Crops | RMSE | R-sq | Validation | Retrained |
|-------|------|-------|------|------|------------|-----------|
| [name] | [type] | [crops] | [val] | [val] | [method] | [schedule] |

### Data Pipeline

| Source | Type | Frequency | Quality | Coverage |
|--------|------|-----------|---------|----------|
| [source] | [sensor/sat/API] | [freq] | [H/M/L] | [scope] |

### Optimization Algorithms

| Algorithm | Domain | Method | Real-Time | Validated |
|-----------|--------|--------|-----------|-----------|
| [name] | [domain] | [method] | [yes/no] | [yes/no] |

### Recommendations

**Critical (data quality):**
1. [action item]

**High priority (model improvement):**
1. [action item]

**Enhancement (new capability):**
1. [action item]

============================================================
NEXT STEPS
============================================================

- "Run `/climate-risk-agriculture` for climate risk and adaptation planning."
- "Run `/food-waste` to analyze post-harvest supply chain optimization."
- "Run `/perf` to assess data pipeline performance under peak season."
- "Run `/security-review` to audit access controls on proprietary farm data."


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /crop-yield — {{YYYY-MM-DD}}
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

- Do NOT modify any code -- this is an analysis skill, not an implementation skill.
- Do NOT include real farm locations, field boundaries, or operator data in output.
- Do NOT assume one crop model works for another -- each has distinct phenology.
- Do NOT ignore data quality -- agricultural models are highly data-dependent.
- Do NOT skip weather integration -- it is the dominant yield driver.
- Do NOT overlook sensor calibration -- uncalibrated data produces poor results.
- Do NOT ignore extreme conditions -- models must perform in drought years too.
