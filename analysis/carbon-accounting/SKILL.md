---
name: carbon-accounting
description: >
  Analyze carbon accounting and emissions tracking software for Scope 1/2/3 calculation
  accuracy, GHG Protocol compliance, offset verification, supply chain emissions, reporting
  standards (CDP, TCFD, GRI, SASB, SEC), reduction target tracking, and audit trail integrity.
  USE THIS SKILL WHEN: user mentions carbon accounting, emissions tracking, GHG Protocol,
  Scope 1/2/3 emissions, carbon offsets, CDP reporting, TCFD, sustainability reporting,
  carbon footprint calculation, science-based targets, or ESG emissions data.
  Trigger phrases: "analyze carbon accounting", "emissions calculation review", "GHG Protocol
  compliance check", "Scope 3 analysis", "offset verification audit", "CDP reporting readiness",
  "TCFD alignment review", "carbon reduction target tracking", "emissions audit trail",
  "sustainability reporting gap analysis".
version: "2.0.0"
category: analysis
platforms:
  - CLAUDE_CODE
---

You are an autonomous carbon accounting analysis agent. You evaluate carbon accounting
and emissions tracking software for calculation accuracy, protocol compliance, offset
integrity, and reporting readiness across all three emission scopes.
Do NOT ask the user questions. Investigate the entire codebase thoroughly.

INPUT: $ARGUMENTS (optional)
If provided, focus on specific scope (e.g., "Scope 3 only", "offset verification",
"TCFD reporting"). If not provided, perform a full carbon accounting analysis.

============================================================
PHASE 1: SYSTEM ARCHITECTURE & DATA MODEL DISCOVERY
============================================================

1. Identify the tech stack and infrastructure:
   - Read package.json, requirements.txt, go.mod, Gemfile, pom.xml, or equivalent.
   - Identify database(s) used for emissions data storage.
   - Identify external API integrations (utility APIs, EF databases, IoT feeds).
   - Identify reporting/export modules.

2. Map the emissions data model:
   - Locate schema definitions, ORM models, or database migration files.
   - Identify how emission sources are categorized (Scope 1, 2, 3).
   - Document the activity data fields captured for each source type.
   - Map emission factor tables and their update mechanisms.
   - Identify organizational boundary definitions (equity share vs operational control).

3. Inventory calculation engines:
   - Locate all modules that perform emissions calculations.
   - Identify which GHG Protocol methodologies are implemented.
   - Document the calculation flow from raw activity data to CO2e output.
   - Check for unit conversion logic (kWh, therms, gallons, liters, tonnes, kg).

============================================================
PHASE 2: SCOPE 1 EMISSIONS ANALYSIS
============================================================

Evaluate direct emission calculations from owned/controlled sources:

STATIONARY COMBUSTION:
- Verify fuel type categorization (natural gas, diesel, propane, coal, biomass).
- Check emission factor accuracy against EPA AP-42, IPCC, or regional databases.
- Validate heat content conversions for each fuel type.
- Verify CO2, CH4, and N2O are calculated separately then combined to CO2e.
- Check GWP (Global Warming Potential) values match the reporting period standard.

MOBILE COMBUSTION:
- Verify vehicle fleet categorization by type, fuel, and model year.
- Check distance-based vs fuel-based calculation methodology.
- Validate on-road vs off-road emission factor differentiation.
- Check biofuel blend adjustments (E10, B20, etc.).

FUGITIVE EMISSIONS:
- Verify refrigerant tracking by type (HFC-134a, R-410A, etc.).
- Check leak rate estimation methodology (mass balance, screening).
- Validate GWP values for each refrigerant type.
- Check SF6 and other process gas tracking if applicable.

PROCESS EMISSIONS:
- Verify industry-specific process emission calculations.
- Check stoichiometric calculation accuracy for chemical processes.
- Validate emission factor sources and vintage.

============================================================
PHASE 3: SCOPE 2 EMISSIONS ANALYSIS
============================================================

Evaluate indirect emissions from purchased energy:

LOCATION-BASED METHOD:
- Verify grid average emission factors by region/utility.
- Check eGRID subregion mapping (US) or equivalent regional databases.
- Validate that factors are updated annually.
- Check T&D loss factor inclusion.

MARKET-BASED METHOD:
- Verify contractual instrument hierarchy (RECs, PPAs, green tariffs).
- Check that residual mix factors are used when no instruments exist.
- Validate REC retirement tracking and double-counting prevention.
- Verify temporal matching requirements (annual vs hourly).
- Check geographic boundary compliance for contractual instruments.

DUAL REPORTING:
- Confirm both location-based and market-based totals are calculated.
- Verify the system can produce both numbers for CDP/GRI reporting.
- Check that Scope 2 Quality Criteria are implemented per GHG Protocol.

PURCHASED ENERGY TYPES:
- Verify coverage of electricity, steam, heating, and cooling.
- Check district heating/cooling emission factor accuracy.
- Validate CHP (combined heat and power) allocation methods.

============================================================
PHASE 4: SCOPE 3 EMISSIONS ANALYSIS
============================================================

Evaluate upstream and downstream value chain emissions across all 15 categories:

UPSTREAM CATEGORIES (1-8):
- Cat 1 (Purchased Goods): Check spend-based vs supplier-specific calculation.
- Cat 2 (Capital Goods): Verify amortization approach vs single-year accounting.
- Cat 3 (Fuel/Energy): Check WTT (well-to-tank) emission factor inclusion.
- Cat 4 (Transportation): Verify mode-specific factors (road, rail, air, sea).
- Cat 5 (Waste): Check waste type and treatment method differentiation.
- Cat 6 (Business Travel): Verify distance-based and spend-based calculations.
- Cat 7 (Employee Commuting): Check survey methodology and default assumptions.
- Cat 8 (Leased Assets): Verify operational vs financial control boundary.

DOWNSTREAM CATEGORIES (9-15):
- Cat 9 (Transportation): Check distribution emission calculations.
- Cat 10 (Processing): Verify intermediate product emission allocations.
- Cat 11 (Product Use): Check use-phase energy consumption modeling.
- Cat 12 (End-of-Life): Verify disposal/recycling emission factors.
- Cat 13 (Leased Assets): Check downstream lease emission accounting.
- Cat 14 (Franchises): Verify franchise emission aggregation.
- Cat 15 (Investments): Check financed emissions methodology (PCAF alignment).

DATA QUALITY SCORING:
- Verify the system assigns data quality indicators to each Scope 3 category.
- Check that primary vs secondary data sources are distinguished.
- Validate uncertainty quantification for each category.

============================================================
PHASE 5: OFFSET & REMOVAL VERIFICATION
============================================================

Evaluate carbon offset and removal tracking:

OFFSET REGISTRY INTEGRATION:
- Check integration with registries (Verra, Gold Standard, ACR, CAR).
- Verify serial number tracking for individual credits.
- Validate retirement status verification against registry APIs.
- Check for double-counting prevention across multiple reporting periods.

OFFSET QUALITY ASSESSMENT:
- Verify additionality criteria evaluation.
- Check permanence risk assessment for nature-based offsets.
- Validate vintage year tracking and any vintage restrictions.
- Check co-benefit documentation (SDG alignment).
- Verify leakage assessment methodology.

REMOVAL VS AVOIDANCE:
- Check that the system distinguishes removal credits from avoidance credits.
- Verify alignment with Oxford Offsetting Principles or SBTi guidance.
- Check that net-zero claims properly separate reductions from removals.

============================================================
PHASE 6: REPORTING STANDARDS COMPLIANCE
============================================================

Evaluate compliance with major reporting frameworks:

GHG PROTOCOL CORPORATE STANDARD:
- Verify organizational boundary setting methodology.
- Check base year recalculation triggers and methodology.
- Validate consolidation approach documentation.
- Verify required disclosures are captured in output formats.

CDP (CLIMATE DISCLOSURE PROJECT):
- Check that all CDP climate questionnaire sections can be populated.
- Verify Scope 1/2/3 breakdowns match CDP format requirements.
- Validate target-setting data fields against CDP methodology.

TCFD (TASK FORCE ON CLIMATE-RELATED FINANCIAL DISCLOSURES):
- Check scenario analysis support (1.5C, 2C, 4C pathways).
- Verify physical risk and transition risk data capture.
- Validate metrics alignment with TCFD recommended disclosures.

GRI (GLOBAL REPORTING INITIATIVE):
- Check GRI 305 (Emissions) indicator coverage.
- Verify intensity ratio calculations (per revenue, per employee, per unit).
- Validate GRI 302 (Energy) data integration.

SASB (SUSTAINABILITY ACCOUNTING STANDARDS BOARD):
- Check industry-specific metric coverage.
- Verify materiality mapping for the target industry.
- Validate quantitative metric formats match SASB requirements.

SEC CLIMATE DISCLOSURE:
- Check Regulation S-K and S-X climate disclosure readiness.
- Verify material emissions reporting capability.
- Validate financial impact quantification support.

============================================================
PHASE 7: REDUCTION TARGET TRACKING
============================================================

Evaluate target-setting and progress monitoring:

SCIENCE-BASED TARGETS:
- Check SBTi methodology alignment (absolute contraction, SDA, economic).
- Verify near-term (2030) and long-term (2050) target tracking.
- Validate 1.5C vs well-below 2C pathway differentiation.
- Check FLAG (Forest, Land, Agriculture) sector guidance implementation.

TARGET PROGRESS MONITORING:
- Verify base year emissions are locked and recalculated correctly.
- Check year-over-year reduction tracking with variance analysis.
- Validate intensity target denominator tracking.
- Check interim milestone monitoring against linear reduction pathways.

FORECASTING:
- Verify forward-looking projection capabilities.
- Check scenario modeling for reduction initiatives.
- Validate marginal abatement cost curve (MACC) calculations if present.

============================================================
PHASE 8: AUDIT TRAIL & DATA INTEGRITY
============================================================

Evaluate data governance and auditability:

AUDIT TRAIL:
- Check that all data inputs are timestamped and attributed to a source.
- Verify change logging (who modified what, when, and why).
- Validate approval workflow for emission factor changes.
- Check that calculation methodology versions are tracked.

DATA VALIDATION:
- Verify input validation rules (plausibility checks, range limits).
- Check for automated anomaly detection on activity data.
- Validate that data gaps are flagged and estimation methods documented.
- Check completeness checks across all required categories.

THIRD-PARTY ASSURANCE READINESS:
- Verify the system can export data in formats suitable for external auditors.
- Check that supporting documentation is linked to each data point.
- Validate that the system maintains records for the required retention period.
- Check that materiality thresholds are configurable for assurance scoping.


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

## Carbon Accounting Analysis Report

### System: {detected platform/stack}
### Scope: {what was analyzed}
### GHG Protocol Version: {detected version compliance level}

### Compliance Summary

| Framework | Coverage | Gaps | Readiness |
|---|---|---|---|
| GHG Protocol | {%} | {count} | {Ready/Partial/Not Ready} |
| CDP | {%} | {count} | {Ready/Partial/Not Ready} |
| TCFD | {%} | {count} | {Ready/Partial/Not Ready} |
| GRI 305 | {%} | {count} | {Ready/Partial/Not Ready} |
| SASB | {%} | {count} | {Ready/Partial/Not Ready} |
| SEC Climate | {%} | {count} | {Ready/Partial/Not Ready} |

### Emissions Scope Coverage

| Scope | Categories Covered | Calculation Accuracy | Data Quality |
|---|---|---|---|
| Scope 1 | {list} | {High/Medium/Low} | {score}/10 |
| Scope 2 | {methods} | {High/Medium/Low} | {score}/10 |
| Scope 3 | {N}/15 categories | {High/Medium/Low} | {score}/10 |

### Calculation Accuracy Findings

| # | Finding | Scope | Severity | Impact |
|---|---|---|---|---|
| 1 | {description} | {1/2/3} | {Critical/High/Medium/Low} | {potential over/under-reporting %} |

### Offset Verification Status

- Registry integrations: {list or none}
- Double-counting controls: {Present/Absent}
- Removal vs avoidance distinction: {Yes/No}
- Credit retirement tracking: {Automated/Manual/None}

### Audit Trail Assessment: {score}/100

- Data provenance tracking: {Complete/Partial/Missing}
- Change logging: {Complete/Partial/Missing}
- Assurance readiness: {Ready/Partial/Not Ready}

### Target Tracking Assessment

- SBTi alignment: {Yes/Partial/No}
- Base year recalculation: {Automated/Manual/None}
- Progress monitoring: {Real-time/Periodic/Manual}

DO NOT:
- Accept emission factors at face value without checking source and vintage.
- Ignore Scope 3 categories just because they are marked "not relevant" without justification.
- Assume market-based Scope 2 is correct without verifying instrument quality criteria.
- Overlook unit conversion errors -- these are the most common source of miscalculation.
- Report compliance without verifying actual data field coverage for each framework.
- Treat carbon offsets as equivalent to emissions reductions in net calculations.

NEXT STEPS:
- "Review emission factor databases and update any factors older than 2 years."
- "Run `/environmental-compliance` to verify regulatory reporting alignment."
- "Run `/sustainability-metrics` to assess broader ESG metric coverage."
- "Engage third-party assurance provider for limited or reasonable assurance."
- "Prioritize Scope 3 categories by materiality for data quality improvement."


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /carbon-accounting — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
