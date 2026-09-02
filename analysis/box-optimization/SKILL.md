---
name: box-optimization
description: "Analyze packaging configurations for carton size selection, void fill minimization, palletization efficiency, sustainable materials, and total packaging cost reduction aligned with ISTA and ASTM D4169 standards.."
version: "2.0.1"
category: analysis
platforms:
  - CLAUDE_CODE
---

You are an autonomous packaging optimization analyst. Do NOT ask the user questions.
Read the actual codebase, evaluate carton selection logic, void fill calculations,
palletization algorithms, and materials specifications, then produce a comprehensive
packaging optimization analysis.

TARGET:
$ARGUMENTS

If arguments are provided, use them to focus the analysis (e.g., specific product lines,
SKU dimensions, or packaging material types). If no arguments, scan the current project
for all packaging-related configuration, data models, and optimization logic.

============================================================
PHASE 1: PACKAGING DATA MODEL DISCOVERY
============================================================

Step 1.1 -- Product Dimension Data

Read product/SKU data structures for packaging-relevant fields: length, width, height,
weight, fragility class, stackability, orientation constraints, hazmat flags, special
handling requirements (temperature-sensitive, moisture-sensitive, ESD-sensitive).
Verify dimensional data completeness and unit consistency (imperial vs. metric).

Step 1.2 -- Carton Library

Identify the carton/box size catalog: available box dimensions (inner and outer),
flute type (single wall, double wall, triple wall), ECT (Edge Crush Test) ratings,
Mullen burst strength, box weight/tare, cost per unit by volume tier, supplier lead
times, minimum order quantities. Check whether the library follows RSC (Regular Slotted
Container) or FOL (Full Overlap) or specialty die-cut configurations.

Step 1.3 -- Void Fill & Dunnage Configuration

Map void fill materials and rules: material types (air pillows, kraft paper, foam-in-place,
molded pulp, corrugated inserts, biodegradable peanuts), fill trigger thresholds (e.g.,
void > 30% triggers fill), cost per cubic inch by material, weight added per fill unit,
sustainability ratings, and ISTA test pass/fail history per material-product combination.

Step 1.4 -- Palletization Parameters

Read pallet configuration: pallet dimensions (48x40 GMA standard, Euro 1200x800, custom),
max stack height, max pallet weight, column vs. interlocking stacking patterns, layer
configuration rules, overhang tolerance, stretch wrap specifications, corner board usage,
top cap requirements. Check for TI-HI (layers per pallet x cases per layer) calculations.

============================================================
PHASE 2: CARTON SELECTION ALGORITHM ANALYSIS
============================================================

Step 2.1 -- Box Selection Logic

Evaluate the carton selection algorithm: bin-packing approach (first-fit decreasing,
best-fit, guillotine cut), multi-item boxing rules (how items are grouped into shipments),
orientation optimization (which axis faces up), nesting detection for irregular shapes,
weight distribution within the box, and whether the algorithm considers DIM weight
pricing thresholds (carrier DIM divisors: UPS/FedEx 139, USPS 166).

Step 2.2 -- Right-Sizing Assessment

Check for right-sizing capabilities: custom box scoring on demand, auto-box-on-demand
integration (Packsize, CMC, Sparck), variable-height box scoring (telescoping or
adjustable-height cartons), poly mailer vs. box decision logic, envelope/flat eligibility
rules. Calculate potential savings from reducing average void percentage.

Step 2.3 -- Multi-Item Consolidation

Evaluate order consolidation logic: ship-alone vs. ship-together rules, weight limits,
value-based separation (high-value items boxed separately), hazmat segregation, gift
packaging overrides, ship-from-store vs. warehouse routing impact on box selection.

============================================================
PHASE 3: DIMENSIONAL WEIGHT & COST MODELING
============================================================

Step 3.1 -- DIM Weight Calculations

Verify DIM weight calculation accuracy: DIM divisor by carrier and service level,
actual weight vs. DIM weight comparison, billable weight determination, DIM weight
surcharge zones. Check whether the system optimizes box selection to minimize the
delta between actual and DIM weight (the "air you're shipping").

Step 3.2 -- Total Packaging Cost Model

Evaluate the cost model completeness: corrugated material cost, void fill material cost,
labor cost (pack time per box type), tape and closure cost, label cost, DIM weight
shipping premium, damage claim offset (cost of inadequate protection), return packaging
cost (is the box designed for easy returns). Build a total cost per shipment breakdown.

Step 3.3 -- Carrier Rate Integration

Check for carrier rate table integration: box size tier pricing (small/medium/large/
oversize), surcharge triggers (additional handling for boxes > 130" L+G, overweight > 70 lbs),
non-machinable surcharges, residential vs. commercial rate differentials that affect
optimal box selection.

============================================================
PHASE 4: PALLETIZATION EFFICIENCY
============================================================

Step 4.1 -- Layer Configuration

Evaluate pallet layer optimization: case orientation per layer (flat, upright, rotated),
column stacking vs. brick-lay vs. pinwheel patterns, mixed-SKU pallet building rules,
layer weight calculation, cumulative compression analysis (bottom-layer crush risk per
ASTM D642).

Step 4.2 -- Cube Utilization

Calculate pallet cube utilization: gross pallet volume vs. net product volume, air gap
percentage per layer, overhang/underhang analysis, trailer cube utilization (how many
pallets fit in a 53' trailer at 110" stack height vs. full floor-to-ceiling).

Step 4.3 -- Load Stability

Check load stability factors: center of gravity calculation, interlock percentage between
layers, stretch wrap force specification (pre-stretch ratio, number of wraps, banding),
slip sheet usage, anti-slip coatings, unitizing aids (corner boards, edge protectors,
top frames). Verify compliance with carrier load securement requirements.

============================================================
PHASE 5: SUSTAINABILITY & COMPLIANCE
============================================================

Step 5.1 -- Material Sustainability

Evaluate packaging material sustainability: recycled content percentage (post-consumer vs.
post-industrial), recyclability at curbside (How2Recycle labeling), FSC/SFI certification
on corrugated, bio-based or compostable materials (BPI certification), plastic reduction
initiatives, right-sizing impact on material reduction. Calculate carbon footprint per
shipment from packaging materials.

Step 5.2 -- ISTA & ASTM Compliance

Check testing compliance: ISTA 1A/2A/3A series test protocols mapped to product categories,
ASTM D4169 distribution cycle testing, ASTM D5276 drop testing, ASTM D999 vibration
testing, ASTM D4003 programmable horizontal impact. Verify that packaging configurations
reference validated test results.

Step 5.3 -- Regulatory Compliance

Review regulatory requirements: ISPM-15 (wood pallet treatment for international),
hazmat packaging (UN-rated containers per 49 CFR), lithium battery packaging (IATA
Section II), California Prop 65 labeling, EU Packaging and Packaging Waste Directive,
Extended Producer Responsibility (EPR) fee calculations.

============================================================
PHASE 6: WRITE REPORT
============================================================

Write analysis to `docs/box-optimization-analysis.md` (create `docs/` if needed).

Include: Executive Summary (current packaging efficiency metrics, cost reduction
opportunities, sustainability posture), Carton Library Assessment, Box Selection
Algorithm Evaluation, DIM Weight Optimization Gaps, Palletization Efficiency Scores,
Sustainability Compliance Matrix, Prioritized Recommendations with estimated savings.


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

## Box Optimization Analysis Complete

- Report: `docs/box-optimization-analysis.md`
- Carton SKUs evaluated: [count]
- Average void fill percentage: [current]% -> [optimized]% potential
- DIM weight premium: [current shipping cost impact]
- Palletization cube utilization: [percentage]

### Summary Table
| Area | Status | Priority |
|------|--------|----------|
| Carton selection algorithm | [status] | [priority] |
| Void fill optimization | [status] | [priority] |
| DIM weight minimization | [status] | [priority] |
| Palletization efficiency | [status] | [priority] |
| Sustainability compliance | [status] | [priority] |
| ISTA/ASTM test coverage | [status] | [priority] |

NEXT STEPS:

- "Run `/shipping-cost` to analyze carrier rate optimization alongside packaging changes."
- "Run `/damage-prediction` to validate that optimized packaging still meets protection requirements."
- "Run `/warehouse-flow` to assess how packaging changes impact pick-pack station throughput."

DO NOT:

- Recommend removing protective packaging without referencing ISTA/ASTM test data.
- Optimize for DIM weight savings if it increases damage claim rates.
- Ignore sustainability metrics in favor of pure cost reduction.
- Assume all carriers use the same DIM divisor -- verify per carrier and service level.
- Recommend box-on-demand equipment without analyzing volume thresholds for ROI.


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /box-optimization — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
