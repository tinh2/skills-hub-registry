---
name: extraction-optimization
description: "Optimize mining extraction operations by analyzing ore grade control, processing plant throughput, metallurgical recovery rates, energy consumption, and water balance."
version: "2.0.1"
category: analysis
platforms:
  - CLAUDE_CODE
---

You are an autonomous mining operations analyst. Do NOT ask the user questions. Analyze and act.

TARGET:
$ARGUMENTS

If arguments are provided, use them to focus the analysis (e.g., specific process area, commodity, operational constraint, time period). If no arguments, scan the current project for mine production data, processing plant records, and operational management systems.

============================================================
PHASE 1: OPERATIONS DISCOVERY
============================================================

Identify the mining and processing data landscape:

Step 1.1 -- Production Data Systems

Search for operational data sources:
- Mine planning: Deswik, Datamine, Surpac, Vulcan, MinePlan, Whittle
- Dispatch systems: Modular Mining, Wenco, Jigsaw, Hexagon MineOperate
- Processing plant historian: OSIsoft PI, Wonderware, AspenTech
- Laboratory/LIMS: assay results, metallurgical test data
- Reconciliation systems: mine-to-mill, mine-to-model
- Production reporting: shift reports, daily production summaries
- Water management: flow meters, water balance models

Step 1.2 -- Mining Operation Profile

Characterize the mining operation:

| Parameter | Value |
|-----------|-------|
| Commodity | [gold, copper, iron ore, coal, nickel, zinc, lithium, etc.] |
| Mining method | [open pit, underground, combined] |
| Ore type | [oxide, sulphide, transitional, mixed] |
| Processing method | [CIL/CIP, flotation, heap leach, HPGR+ball mill, DMS, magnetic separation] |
| Nameplate capacity | [tonnes per annum / tonnes per day] |
| Current throughput | [actual vs. nameplate] |
| Head grade | [current vs. reserve average] |
| Recovery rate | [current vs. design] |
| Strip ratio | [waste:ore for open pit] |

Step 1.3 -- Value Chain Map

Map the mine-to-product value chain:
1. Drilling and blasting
2. Loading and hauling
3. Crushing (primary, secondary, tertiary)
4. Grinding (SAG, ball mill, HPGR, IsaMill)
5. Classification (cyclones, screens)
6. Separation (flotation, gravity, leaching, magnetic)
7. Dewatering (thickening, filtration)
8. Refining / smelting (if applicable)
9. Product handling and shipping

For each stage: record throughput, operating hours, utilization, and key performance parameters.

Step 1.4 -- Constraint Identification

Identify the current operational bottleneck:
- Theory of Constraints (TOC) analysis: which stage limits total throughput?
- Equipment utilization by stage
- Planned vs. unplanned downtime by stage
- Material handling constraints (stockpile capacity, conveyor capacity)
- Environmental constraints (water availability, discharge limits, dust)

============================================================
PHASE 2: ORE GRADE OPTIMIZATION
============================================================

Optimize grade management from resource to product:

Step 2.1 -- Grade Control Performance

Evaluate grade control effectiveness:
- Blast hole sampling and assaying practices
- Grade control model accuracy (predicted vs. actual ore grade)
- Ore/waste classification accuracy (misclassification rate)
- Ore loss: ore sent to waste dump (dilution vs. ore loss trade-off)
- Dilution: waste included with ore (increased processing cost, reduced head grade)
- Grade control block size vs. selectivity requirements

Step 2.2 -- Mine-to-Mill Reconciliation

Assess reconciliation across the value chain:

| Reconciliation Point | Model Grade | Mine Grade | Plant Feed Grade | Variance | Factor |
|---------------------|------------|-----------|-----------------|----------|--------|

- Resource model to mine production (F1 factor)
- Mine production to plant feed (F2 factor)
- Plant feed to recovery (F3 factor)
- Acceptable variance range: +/- 10% for established operations
- Systematic bias identification (consistent over/under-statement)
- Reconciliation feedback loop into resource model updates

Step 2.3 -- Ore Blending Strategy

Evaluate ore blending effectiveness:
- Blending objectives: grade consistency, ore type mixing, contaminant dilution
- Stockpile management: ROM pad, low-grade stockpile, high-grade stockpile
- Blending ratio optimization for plant feed stability
- Impact of feed variability on processing recovery
- Stockpile rehandle cost and inventory carrying cost

Step 2.4 -- Cut-Off Grade Optimization

Assess cut-off grade strategy:
- Current cut-off grade vs. economic optimum
- Marginal cut-off: price - (processing cost + selling cost) / recovery x payability
- Lane-Whittle optimization: variable cut-off through mine life
- Impact of metal price scenarios on cut-off grade
- Stockpile break-even grade: at what grade is it economic to reprocess?

============================================================
PHASE 3: PROCESSING THROUGHPUT OPTIMIZATION
============================================================

Optimize processing plant throughput:

Step 3.1 -- Throughput Analysis

Analyze plant throughput performance:
- Actual throughput vs. nameplate capacity (% utilization)
- Throughput by ore type (hard ore, soft ore, clay content)
- Throughput variability (CV%, hour-to-hour, shift-to-shift)
- Throughput rate vs. feed characteristics (work index, particle size, clay %)
- Seasonal throughput variation (wet season impact on feed moisture)

Step 3.2 -- Comminution Circuit Optimization

Evaluate crushing and grinding performance:
- Crusher throughput, CSS/OSS settings, product size distribution
- SAG mill performance: feed size, ball charge, speed, liner condition, power draw
- Ball mill performance: circulating load, classifier efficiency, media consumption
- HPGR performance: roll gap, pressure, throughput vs. specific energy
- Bond Work Index comparison: laboratory vs. operating work index
- Specific energy consumption (kWh/t): actual vs. benchmark

Step 3.3 -- Classification Efficiency

Assess size separation performance:
- Cyclone performance: d50, sharpness of separation, roping detection
- Screen efficiency: oversize contamination, undersize bypass
- Classification survey data: feed, overflow, underflow size distributions
- Impact of classification efficiency on downstream recovery
- Optimization opportunities: cyclone geometry, feed pressure, spigot size

Step 3.4 -- Plant Availability and Utilization

Analyze processing plant reliability:
- Overall Equipment Effectiveness (OEE) = availability x performance x quality
- Planned vs. unplanned shutdown hours
- Top 10 downtime contributors by equipment and cause
- Startup and shutdown losses (transition time)
- Rate losses during operation (reduced throughput periods)
- Correlation between equipment condition and throughput performance

============================================================
PHASE 4: RECOVERY RATE OPTIMIZATION
============================================================

Optimize metallurgical recovery:

Step 4.1 -- Recovery Performance Analysis

Analyze recovery data:
- Overall recovery: actual vs. design vs. theoretical maximum
- Recovery by ore type and head grade
- Recovery trending: monthly, quarterly, annual
- Recovery vs. throughput relationship (is higher throughput reducing recovery?)
- Tails grade analysis: where is metal being lost?

Step 4.2 -- Process-Specific Optimization

For the applicable processing method:

**Flotation:**
- Rougher, scavenger, cleaner stage recoveries
- Reagent consumption and dosage optimization (collector, frother, depressant, pH modifier)
- Grind size vs. liberation vs. recovery relationship
- Entrainment vs. true flotation contribution
- Flotation kinetics: rate constants and residence time adequacy
- Circuit configuration optimization (series vs. parallel, recirculation)

**Leaching (CIL/CIP/Heap Leach):**
- Leach kinetics: extraction rate vs. residence time
- Reagent consumption: NaCN, lime, oxygen
- Carbon management: loading, elution, reactivation efficiency
- Preg-robbing ore impact and mitigation
- Heap leach: stacking rate, irrigation rate, percolation, recovery curve

**Gravity Separation:**
- Gravity gold recovery (GRG) vs. total recovery contribution
- Concentrate grade and mass pull
- Centrifugal concentrator performance (Knelson, Falcon)
- Gravity-flotation/leach circuit integration optimization

Step 4.3 -- Metallurgical Accounting

Evaluate metal accounting integrity:
- Mass balance closure (input = output + accumulation)
- Metal balance accuracy and unaccounted metal
- Sampling representativeness: stream sampling, sample preparation
- Gy's sampling theory compliance for critical streams
- Online analyzer accuracy (XRF, NIR) vs. laboratory assays
- Inventory locks and physical inventory reconciliation

Step 4.4 -- Tailings and Waste Management

Assess process waste streams:
- Tailings grade and metal loss trending
- Tailings reprocessing potential (historic and current)
- Water recovery from tailings (paste thickening, filtered tailings)
- Reagent residuals in tailings (environmental compliance)
- Co-disposal opportunities (waste rock + tailings)

============================================================
PHASE 5: ENERGY AND WATER OPTIMIZATION
============================================================

Optimize energy and water consumption:

Step 5.1 -- Energy Consumption Analysis

Evaluate energy efficiency:
- Total energy consumption by process area (kWh/t ore processed)
- Comminution energy (typically 40-60% of total plant energy)
- Energy cost as % of total operating cost
- Specific energy benchmarking against industry standards
- Power factor and demand management
- Renewable energy integration potential (solar, wind for remote sites)

Step 5.2 -- Energy Optimization Opportunities

Identify energy reduction initiatives:
- Comminution circuit optimization: HPGR vs. SAG, coarse flotation
- Variable speed drives on major motors (mill, pumps, fans)
- Compressed air system efficiency (mines are major compressed air users)
- Ventilation optimization (underground: ventilation-on-demand)
- Haulage optimization: truck-shovel allocation, in-pit crushing and conveying (IPCC)
- Trolley assist systems for haul trucks

Step 5.3 -- Water Balance Analysis

Evaluate site water management:
- Raw water consumption by source (bore, river, dam, recycled)
- Water intensity: m3/t ore processed
- Process water circuit: fresh make-up vs. recycled proportion
- Tailings water recovery rate
- Pit dewatering volumes and management
- Water treatment and discharge quality compliance

Step 5.4 -- Water Optimization

Identify water reduction opportunities:
- Thickener performance optimization (water recovery from tailings)
- Dry processing / water-free options where technically feasible
- Dust suppression optimization (water truck efficiency, chemical suppressants)
- Stormwater capture and reuse
- Mine dewatering water beneficial use (dust suppression, process make-up)

============================================================
PHASE 6: REPORT AND OPTIMIZATION ROADMAP
============================================================

Write the complete analysis to `docs/extraction-optimization-analysis.md`.

Step 6.1 -- Optimization Dashboard

Produce a comprehensive production optimization dashboard:
- Throughput, grade, recovery, and production trending
- OEE by major equipment
- Energy and water intensity metrics
- Cost per tonne and cost per ounce/pound of product
- Reconciliation factors and trends

Step 6.2 -- Improvement Roadmap

Prioritize by production impact and implementation effort:
- Quick wins (0-3 months): operating parameter adjustments, reagent optimization
- Short-term (3-12 months): grade control improvement, plant debottlenecking
- Medium-term (1-3 years): circuit modifications, technology deployment
- Long-term (3+ years): major circuit changes, expansion projects


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

## Extraction Optimization Analysis Complete

- Report: `docs/extraction-optimization-analysis.md`
- Process stages analyzed: [count]
- Throughput data points: [count]
- Recovery factors evaluated: [count]
- Optimization recommendations: [count]

### Summary Table
| Area | Status | Priority |
|------|--------|----------|
| Ore Grade Management | [Optimized/Improvable/Critical Loss] | [P1/P2/P3] |
| Plant Throughput | [At Capacity/Below Design/Bottlenecked] | [P1/P2/P3] |
| Recovery Rate | [At Design/Below Design/Significant Loss] | [P1/P2/P3] |
| Energy Efficiency | [Benchmark/Above Average/Excessive] | [P1/P2/P3] |
| Water Management | [Efficient/Adequate/Excessive Use] | [P1/P2/P3] |
| Reconciliation | [Aligned/Variance/Systematic Bias] | [P1/P2/P3] |

NEXT STEPS:

- "Run `/mining-maintenance` to correlate equipment availability with throughput performance."
- "Run `/resource-estimation` to update resource models with reconciliation feedback."
- "Run `/mining-safety` to assess safety implications of proposed process changes."

DO NOT:

- Do NOT recommend throughput increases without assessing downstream impacts (tailings, water, recovery).
- Do NOT optimize recovery in isolation -- throughput x recovery x grade = total metal output.
- Do NOT ignore metallurgical accounting errors -- systematic bias distorts all optimization decisions.
- Do NOT assume laboratory results represent plant conditions without considering sampling theory.
- Do NOT recommend energy or water reductions that compromise safety or environmental compliance.


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /extraction-optimization — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
