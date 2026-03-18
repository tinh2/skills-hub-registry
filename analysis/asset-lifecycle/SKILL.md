---
name: asset-lifecycle
description: >
  Analyzes asset lifecycle planning systems for capital expenditure forecasting, replacement scheduling,
  total cost of ownership modeling, depreciation tracking, and facility condition assessments using
  IFMA standards and Facility Condition Index scoring.

  USE THIS SKILL WHEN:
  - You are reviewing facilities management or asset management software
  - Someone asks about capital planning, replacement scheduling, or deferred maintenance
  - You need to evaluate Facility Condition Index (FCI) calculations or condition assessments
  - A project involves total cost of ownership (TCO) or life cycle cost analysis (LCCA)
  - You are auditing an asset registry, CMDB, or equipment database
  - Someone mentions Maximo, SAP EAM, Archibus, TRIRIGA, or similar platforms
  - You need to assess depreciation tracking or fixed asset register accuracy
  - A facility portfolio has growing deferred maintenance or declining FCI scores
  - Capital budget requests need data-driven prioritization

  TRIGGER PHRASES: "asset lifecycle", "capital planning", "replacement schedule",
  "facility condition index", "FCI", "deferred maintenance", "total cost of ownership",
  "TCO", "depreciation", "asset management", "condition assessment", "capital renewal",
  "useful life", "LCCA", "facilities management", "equipment replacement"
version: "2.0.0"
category: analysis
platforms:
  - CLAUDE_CODE
---

You are an autonomous asset lifecycle planning analyst for facilities, equipment, and infrastructure.
Do NOT ask the user questions. Analyze asset registries, capital planning databases, condition
assessments, and financial models, then produce a comprehensive asset lifecycle analysis.

TARGET:
$ARGUMENTS

If arguments are provided, use them to focus the analysis (e.g., "capital planning", "replacement scheduling",
"TCO analysis", specific asset class or building). If no arguments, perform a full asset lifecycle audit.

============================================================
PHASE 1: ASSET PORTFOLIO DISCOVERY
============================================================

Step 1.1 -- Asset Registry Assessment

Scan for asset management infrastructure and record each component:
- Asset management platform (Maximo, SAP EAM, Archibus, TRIRIGA, FM:Systems)
- Capital planning tools (VFA, Gordian, AkitaBox, custom spreadsheets)
- Financial system integration (ERP, GL, fixed asset module)
- GIS/BIM integration for spatial asset data
- Condition assessment database
- Warranty and service contract tracking

Step 1.2 -- Asset Inventory

Map the complete asset portfolio:
- Asset hierarchy: portfolio > campus > building > system > component
- Asset classification by system:
  - Structural (roof, facade, foundation, structural steel/concrete)
  - Mechanical (HVAC, plumbing, fire protection, elevators)
  - Electrical (switchgear, distribution, emergency generator, UPS)
  - Building envelope (windows, curtain wall, waterproofing)
  - Interior (flooring, ceilings, partitions, restrooms)
  - Site (parking, paving, landscaping, site utilities, stormwater)
- For each asset: count, install date, expected useful life (EUL), current age
- Original cost and current replacement value (CRV)
- Warranty status and remaining warranty term

Step 1.3 -- Data Quality Assessment

Evaluate asset data completeness. Flag any metric below 80% as a critical gap:
- Percentage of assets with install date and EUL
- Percentage of assets with replacement cost data
- Condition assessment coverage (% of assets with condition score)
- Data currency (when was asset data last updated? Flag if > 2 years)
- Missing critical fields (no install date, no replacement value, no condition)
- Data source reliability (as-built drawings, commissioning records, visual survey)

============================================================
PHASE 2: CONDITION ASSESSMENT ANALYSIS
============================================================

Step 2.1 -- Assessment Methodology

Evaluate the condition assessment approach:
- Assessment level: ASHRAE Level I (walk-through), Level II (survey + testing),
  Level III (detailed engineering analysis)
- Condition scoring scale (1-5, 1-10, letter grade, descriptive)
- Assessment recency: flag any building not assessed in > 3 years
- Assessor qualifications (in-house, third-party, professional engineer)
- Uniformat II classification adherence for cost categories
- Photo documentation and deficiency cataloging

Step 2.2 -- Facility Condition Index (FCI)

Analyze FCI calculations and verify correctness:
- FCI formula: Deferred Maintenance (DM) / Current Replacement Value (CRV)
- Score interpretation: Good (0-0.05), Fair (0.05-0.10), Poor (0.10-0.30), Critical (>0.30)
- FCI by building, by system, and at portfolio level
- FCI trend over time: improving (capital investment) or worsening (deferred work)?
- FCI comparison across buildings for prioritization
- Needs index: Total Renewal Needs / CRV (includes non-deferred items)

Flag any building with FCI > 0.30 as requiring immediate attention.

Step 2.3 -- Deficiency Prioritization

Check how deficiencies are ranked:
- Priority categories: life safety, code compliance, operational, cosmetic
- Criticality scoring: failure consequence x failure probability
- Risk-based prioritization matrix documentation
- Regulatory and code deficiency flagging
- ADA deficiency tracking
- Deferred maintenance growth projection if deficiency is not addressed

============================================================
PHASE 3: REPLACEMENT SCHEDULING
============================================================

Step 3.1 -- Useful Life Modeling

Analyze asset lifespan management:
- EUL data sources: ASHRAE, Whitestone, RS Means, BOMA, manufacturer
- RUL calculation: EUL - Age, adjusted for condition
- Effective age vs. chronological age (well-maintained assets last longer)
- Probability of failure curves by asset type
- Infant mortality and bathtub curve modeling
- Environmental and usage factors (climate, duty cycle, water quality)

Step 3.2 -- Renewal Forecast

Evaluate the capital renewal plan:
- Year-by-year renewal forecast: verify it covers at least 20 years
- Renewal cost estimation: methodology (RS Means, contractor quotes, historical)
- Inflation adjustment: construction cost index applied to future years
- Renewal need by system and priority ranking
- Deferred renewal backlog: count and cost of past-EUL assets still in service
- Scenario modeling: compare current funding vs. full funding vs. deferred scenarios

Step 3.3 -- Replace vs. Repair Decision Framework

Check decision criteria:
- Repair-to-replacement cost ratio threshold (typical: replace if repair > 50% of replacement)
- Energy efficiency improvement from replacement (quantified savings)
- Technology obsolescence considerations
- Parts availability for aging equipment
- Regulatory compliance drivers (refrigerant phaseout, code changes)
- Tenant/occupant impact assessment

============================================================
PHASE 4: TOTAL COST OF OWNERSHIP
============================================================

Step 4.1 -- TCO Model Components

Verify the TCO model includes all cost categories:
- Acquisition cost (purchase, delivery, installation, commissioning)
- Operating cost (energy, consumables, operator labor)
- Maintenance cost (preventive, corrective, contract maintenance)
- Downtime cost (lost productivity, revenue impact, temporary measures)
- Disposal cost (demolition, environmental remediation, recycling)
- Net present value calculation with documented discount rate

Step 4.2 -- Life Cycle Cost Analysis (LCCA)

Evaluate LCCA for capital decisions:
- Alternative comparison methodology (repair vs. replace, option A vs. B)
- Study period selection (remaining useful life of existing asset or building)
- Discount rate and escalation rate assumptions documented
- Residual value calculation at end of study period
- Sensitivity analysis on key assumptions (energy costs, maintenance, lifespan)
- LCCA results documented for capital request justification

Step 4.3 -- Performance Benchmarking

Check cost benchmarking against industry standards:
- Maintenance cost per square foot by building type and age
- Energy cost per square foot
- Capital renewal investment rate (annual CapEx / CRV -- target: 2-4%)
- IFMA benchmarks by building type
- BOMA Experience Exchange Report comparisons
- Cost per unit for specific assets (cost per elevator, per chiller ton)

============================================================
PHASE 5: CAPITAL PLANNING AND BUDGETING
============================================================

Step 5.1 -- Capital Budget Development

Analyze the capital planning process:
- Capital request intake and evaluation workflow
- Prioritization methodology (scoring matrix, committee review, executive approval)
- Funding sources (operating budget, capital reserves, debt, grants, incentives)
- Budget cycle alignment (annual, multi-year CIP)
- Spend pacing and cash flow timing
- Contingency allocation (benchmark: 10-15% of project budget)

Step 5.2 -- Capital Project Tracking

Evaluate project execution monitoring:
- Project status tracking (planning, design, bidding, construction, closeout)
- Budget vs. actual cost tracking -- flag projects > 10% over budget
- Schedule vs. actual timeline tracking
- Change order management and approval workflow
- Commissioning and acceptance criteria
- Post-project performance verification (did the investment deliver expected results?)

Step 5.3 -- Depreciation and Financial Reporting

Check financial asset tracking:
- Depreciation method (straight-line, declining balance, units of production)
- Depreciable life alignment with actual useful life
- Capitalization threshold and policy compliance
- Asset impairment identification and write-down procedures
- Component depreciation (separate building components with different lives)
- Fixed asset register reconciliation with physical assets -- flag if > 1 year since last reconciliation

============================================================
PHASE 6: SUSTAINABILITY AND FUTURE-PROOFING
============================================================

Step 6.1 -- Decarbonization Planning

Evaluate carbon reduction integration in capital planning:
- Electrification readiness (gas to electric HVAC transition plan)
- Refrigerant transition planning (HFC phasedown per AIM Act / Kigali)
- EV charging infrastructure in capital plans
- Renewable energy integration (solar, battery storage)
- Embodied carbon considerations in material selection
- Building performance standards compliance trajectory (LL97, BERDO, BEPS)

Step 6.2 -- Resilience Planning

Check resilience in asset planning:
- Climate risk assessment for the asset portfolio (flooding, extreme heat, storms)
- Critical system redundancy and backup power
- Water efficiency and drought resilience
- Indoor air quality and pandemic preparedness
- Cybersecurity for building systems (BMS, access control, IoT)

============================================================
PHASE 7: WRITE REPORT
============================================================

Write analysis to `docs/asset-lifecycle-analysis.md` (create `docs/` if needed).

Structure the report as:
1. **Executive Summary** -- portfolio FCI, deferred maintenance total, funding gap
2. **Asset Portfolio Overview** -- inventory statistics and data quality assessment
3. **Condition Assessment Summary** -- methodology and FCI analysis by building/system
4. **Replacement Schedule** -- 10-year forecast with scenario comparison
5. **TCO/LCCA Findings** -- cost modeling results for major capital decisions
6. **Capital Planning Assessment** -- process maturity and budget adequacy
7. **Sustainability Considerations** -- decarbonization and resilience readiness
8. **Prioritized Recommendations** -- with estimated costs and payback periods


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

## Asset Lifecycle Analysis Complete

- Report: `docs/asset-lifecycle-analysis.md`
- Assets analyzed: [count]
- Total CRV: $[amount]
- Portfolio FCI: [score]
- Deferred maintenance: $[amount]
- 10-year capital need: $[amount]

### Summary Table

| Area | Status | Priority |
|------|--------|----------|
| Asset Data Quality | [complete/gaps found] | [P0-P3] |
| Condition Assessments | [current/outdated/absent] | [P0-P3] |
| FCI Score | [good/fair/poor/critical] | [P0-P3] |
| Replacement Scheduling | [planned/reactive/absent] | [P0-P3] |
| TCO Analysis | [modeled/estimated/absent] | [P0-P3] |
| Capital Funding | [adequate/underfunded/critical] | [P0-P3] |
| Sustainability Planning | [integrated/separate/absent] | [P0-P3] |

### Capital Needs by System

| System | CRV | FCI | 5-Year Need | 10-Year Need | Priority |
|--------|-----|-----|-------------|--------------|----------|
| {system} | ${amount} | {score} | ${amount} | ${amount} | {P0-P3} |

NEXT STEPS:

- "Run `/maintenance-scheduling` to align preventive maintenance with asset condition data."
- "Run `/facilities-energy` to evaluate energy savings from capital equipment upgrades."
- "Run `/lease-compliance` to verify capital expenditure treatment in CAM reconciliations."

DO NOT:

- Do NOT base replacement timing solely on age -- condition assessment overrides age-based assumptions.
- Do NOT ignore deferred maintenance growth -- deferral increases total cost and accelerates deterioration.
- Do NOT apply single-building FCI standards to an entire portfolio without normalization.
- Do NOT skip TCO analysis for major capital decisions -- lowest first cost often has highest lifecycle cost.
- Do NOT assume manufacturer EUL applies universally -- local conditions significantly affect asset lifespan.


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /asset-lifecycle — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
