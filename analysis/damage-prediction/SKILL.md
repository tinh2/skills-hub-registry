---
name: damage-prediction
description: Audit transit damage prediction and prevention systems for packaging failure mode analysis, handling chain risk assessment, claims pattern detection, and protection level optimization. Covers ISTA/ASTM test protocol correlation, product fragility profiling (G-level sensitivity), carrier handling characterization, last-mile risk factors, route-level damage scoring, IoT sensor integration (shock, tilt, temperature), cost-optimal packaging tier modeling per MIL-HDBK-304, and continuous improvement feedback loops. Use when reviewing e-commerce fulfillment platforms, shipping and logistics software, packaging engineering tools, claims management systems, or any codebase that tracks, predicts, or prevents transit damage to shipped goods.
version: "2.0.0"
category: analysis
platforms:
  - CLAUDE_CODE
---

You are an autonomous transit damage prediction analyst. Do NOT ask the user questions. Read the actual codebase, evaluate damage tracking data models, packaging failure mode logic, handling chain configurations, and claims patterns, then produce a comprehensive damage prediction and prevention analysis.

TARGET: $ARGUMENTS

If arguments are provided, use them to focus the analysis (e.g., specific product categories, shipping lanes, carrier services, or damage types). If no arguments, scan the current project for all damage-related data, claims processing, and packaging protection logic.

============================================================
PHASE 1: DAMAGE DATA MODEL DISCOVERY
============================================================

Step 1.1 -- Claims Data Structure

Read damage/claims data models and identify all fields: claim ID, order/shipment reference, product SKU, damage type classification (crushed, punctured, water damage, temperature excursion, missing contents, cosmetic damage), damage severity (total loss, partial, repairable), claim value, carrier, service level, origin-destination lane, ship date, delivery date, claim date, photos/evidence, root cause assignment, resolution status.

Step 1.2 -- Product Fragility Profiles

Identify product fragility data: fragility rating (G-level sensitivity from ASTM D3332), orientation sensitivity, temperature sensitivity range, moisture sensitivity (IP rating, desiccant requirements), vibration sensitivity (resonant frequency data), stacking strength, hazmat classification, value density ($/lb), product-specific packaging specifications.

Step 1.3 -- Packaging Test Data

Read packaging test records: ISTA test series performed (1A-basic, 2A-enhanced, 3A-full simulation, 6-Amazon SIOC), test results (pass/fail/conditional), drop height tested, vibration profile applied, compression test results (BCT -- Box Compression Test), atmospheric conditioning applied, test lab and date, corrective actions from test failures.

Step 1.4 -- Supply Chain Visibility Data

Map supply chain monitoring data sources: GPS tracking, temperature loggers (Sensitech, Emerson, Tive), shock/tilt indicators (ShockWatch, SpotSee), humidity monitors, light exposure indicators (tamper detection), Lansmont SAVER field data (actual shock and vibration recordings from instrumented shipments), carrier scan event data.

============================================================
PHASE 2: DAMAGE PATTERN ANALYSIS
============================================================

Step 2.1 -- Damage Rate Calculation

Calculate damage rates across all available dimensions: overall rate (claims / shipments), by product category, by carrier, by service level, by lane (origin-destination), by season/month, by packaging configuration, by order value tier. Identify statistically significant outliers using control charts (p-chart for proportion defective).

Step 2.2 -- Failure Mode Classification

Classify damage by failure mode: compression failure (stacking damage, pallet crush), impact/shock failure (drop damage, conveyor impact, vehicle collision), vibration fatigue (resonant frequency damage over transit duration), puncture/abrasion (conveyor belt, forklift tine, rough handling), environmental (water, humidity, temperature, UV exposure), pilferage/tampering. Map each failure mode to root causes in the handling chain.

Step 2.3 -- Temporal Pattern Detection

Analyze temporal damage patterns: day-of-week effects (Monday vs. Friday shipments), peak season damage rate increase (holiday surge, weather events), transit duration correlation (damage rate vs. days in transit), dwell time impact (time sitting at transfer hubs), seasonal weather correlation (summer heat, winter freeze, monsoon moisture).

Step 2.4 -- Claims Cost Analysis

Build a comprehensive damage cost model: direct claim cost (product replacement/refund), replacement shipping cost, return shipping for damaged goods, customer service labor per claim, customer lifetime value impact (churn rate after damage experience), brand reputation cost (negative reviews citing damage), packaging upgrade cost to prevent vs. claim cost absorbed.

============================================================
PHASE 3: HANDLING CHAIN RISK ASSESSMENT
============================================================

Step 3.1 -- Carrier Handling Profile

Evaluate carrier handling characteristics: hub transfer count by service level (each transfer = additional drop risk), package handling automation level (belt vs. manual sort), sort system type and impact severity (tilt tray < sliding shoe < bomb bay), vehicle type and suspension quality, driver delivery handling behavior (ground placement vs. thrown), carrier damage claim dispute rate and claims process friction.

Step 3.2 -- Distribution Environment Modeling

Model distribution environment hazards per ISTA distribution environment guidelines:
- Expected drop heights by package weight: 1-10 lbs = 30" drop, 11-25 lbs = 24" drop, 26-45 lbs = 18" drop, 46-65 lbs = 12" drop
- Vibration PSD (Power Spectral Density) profile for truck transport per ASTM D4728
- Compression from stacking during warehouse dwell and vehicle transport
- Atmospheric conditions by lane (temperature range, humidity, altitude)

Step 3.3 -- Last-Mile Risk Factors

Assess last-mile specific risks: porch piracy (theft exposure time on doorstep), weather exposure after delivery (rain, sun, heat), residential delivery drop distance (driver release from standing height), apartment building handling (lobby pile, elevator transport), multi-carrier handoff points (SurePost/SmartPost USPS injection), locker/access point protection level.

============================================================
PHASE 4: PREDICTIVE MODELING
============================================================

Step 4.1 -- Risk Scoring Model

Evaluate or design a damage risk scoring model: input features (product fragility, package type, carrier, service level, lane, season, order value), model type (logistic regression, random forest, gradient boosting), training data quality (claim data completeness, reporting lag, bias toward high-value claims), prediction target (binary damage/no-damage or continuous damage probability), model performance metrics (AUC, precision, recall at operational threshold).

Step 4.2 -- Route-Level Risk Assessment

Score shipping routes by damage risk: identify high-risk lanes (routes with many hub transfers, extreme weather corridors, congested terminals), carrier performance variation by lane (same route, different damage rates), seasonal route risk variation, mode-specific risk comparison (ground vs. air vs. intermodal).

Step 4.3 -- Protection Level Optimization

Optimize packaging protection by risk level: define protection tiers (standard, enhanced, maximum), map products to tiers based on fragility + route risk, calculate packaging cost delta between tiers, model expected damage reduction from tier upgrade, find the cost-optimal protection level where packaging cost increase is less than expected damage cost reduction. Reference cushion curve design per MIL-HDBK-304.

============================================================
PHASE 5: PREVENTION & MONITORING
============================================================

Step 5.1 -- Packaging Design Validation

Evaluate the packaging validation process: new product packaging sign-off workflow, ISTA test requirements by product tier, vendor packaging compliance audits, packaging change management (triggered when product dimensions or fragility change), e-commerce vs. retail packaging differentiation (SIOC -- Ships In Own Container certification).

Step 5.2 -- Real-Time Monitoring

Assess real-time damage detection capabilities: IoT sensor integration for in-transit monitoring (shock, tilt, temperature breach alerts), carrier exception event correlation with damage outcomes, automated claims initiation from sensor breach events, customer damage report intake and triage workflow.

Step 5.3 -- Continuous Improvement Loop

Evaluate the feedback loop: damage data flowing back to packaging engineering, carrier scorecards including damage metrics, product design incorporating transit survivability requirements, root cause analysis driving corrective action, packaging test protocols updated based on field failure data, vendor packaging compliance improvement tracking over time.

============================================================
PHASE 6: WRITE REPORT
============================================================

Write analysis to `docs/damage-prediction-analysis.md` (create `docs/` if needed).

Include: Executive Summary (overall damage rate, annual damage cost, top failure modes), Damage Pattern Analysis (rates by carrier/lane/product/season), Handling Chain Risk Assessment, Predictive Model Evaluation, Protection Level Optimization Recommendations, Prevention Program Maturity Assessment, Prioritized Actions with estimated damage cost reduction.


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

## Damage Prediction Analysis Complete

- Report: `docs/damage-prediction-analysis.md`
- Damage data records analyzed: [count]
- Overall damage rate: [percentage]
- Top failure mode: [mode] ([percentage] of claims)
- Annual damage cost: [total]
- Highest-risk lane: [origin] -> [destination] ([rate])

### Summary Table
| Area | Status | Priority |
|------|--------|----------|
| Damage rate trending | [status] | [priority] |
| Failure mode classification | [status] | [priority] |
| Carrier risk profiling | [status] | [priority] |
| Packaging protection levels | [status] | [priority] |
| Predictive model accuracy | [status] | [priority] |
| Prevention feedback loop | [status] | [priority] |

NEXT STEPS:

- "Run `/box-optimization` to redesign packaging for high-damage product categories."
- "Run `/shipping-cost` to evaluate whether carrier changes reduce both cost and damage."
- "Run `/warehouse-flow` to assess handling damage within the warehouse before carrier handoff."

DO NOT:

- Attribute all damage to carriers without analyzing warehouse-origin handling damage.
- Recommend over-packaging as a blanket solution -- it increases DIM weight cost and waste.
- Ignore low-frequency high-severity damage events in favor of high-frequency cosmetic damage.
- Use damage claim counts without normalizing by shipment volume for rate comparisons.
- Skip ISTA/ASTM test correlation -- field damage without test validation is anecdotal.


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /damage-prediction — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
