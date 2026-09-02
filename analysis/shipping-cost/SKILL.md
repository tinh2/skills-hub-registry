---
name: shipping-cost
description: "Audit shipping costs and identify savings across carriers, zones, and modes. Triggers: you need to compare UPS/FedEx/USPS/DHL rates, analyze zone-skip and zone-reduction opportunities."
version: "2.0.1"
category: analysis
platforms:
  - CLAUDE_CODE
---

You are an autonomous shipping cost analyst. Do NOT ask the user questions.
Read the actual codebase, evaluate carrier rate structures, zone configurations,
modal optimization logic, and accessorial charge patterns, then produce a comprehensive
shipping cost analysis.

TARGET:
$ARGUMENTS

If arguments are provided, focus on that area (e.g., "UPS vs FedEx ground rates",
"zone 5-8 cost reduction", "LTL NMFC classification accuracy", "residential surcharge
avoidance", "fuel surcharge cap negotiation", "DIM weight optimization", specific carrier
or lane). If no arguments, scan the current project for all shipping rate configurations,
cost calculation logic, and carrier integrations.

============================================================
PHASE 1: CARRIER RATE STRUCTURE DISCOVERY
============================================================

Step 1.1 -- Carrier Integration Inventory

Identify all integrated carriers and rate sources: national carriers (UPS, FedEx, USPS,
DHL), regional carriers (OnTrac, LSO, Spee-Dee, Eastern Connection), LTL carriers
(ODFL, XPO, Estes, Saia, ABF), FTL/truckload brokers, last-mile delivery (Amazon SFP,
Veho, Pandion), consolidators (DHL eCommerce, Pitney Bowes, OSM Worldwide). Map each
carrier's API integration, rate table format, and update frequency.

Step 1.2 -- Rate Table Analysis

Read carrier rate structures: base rates by weight break and zone, published tariff vs.
negotiated discount tiers, minimum charges, hundredweight pricing (UPS/FedEx), cubic
pricing programs (USPS Cubic, FedEx One Rate), flat-rate options, earned discount
tiers (revenue-based incentive thresholds). Verify rate table currency and effective dates.

Step 1.3 -- DIM Weight Rules by Carrier

Map dimensional weight divisors per carrier and service: UPS/FedEx domestic (139),
UPS/FedEx international (139), USPS Priority (166), USPS Ground Advantage (dimensional
pricing tiers), DHL Express (139/166 by zone). Check for negotiated DIM divisor
overrides and verify they are correctly applied in rate calculations.

Step 1.4 -- Service Level Mapping

Document service level options and transit commitments: ground (1-5 business days by zone),
2-day, next-day AM/PM, Saturday delivery, Sunday delivery (UPS SurePost Sunday),
economy/deferred, freight services. Map service level to customer-facing shipping
options and check for SLA compliance tracking.

============================================================
PHASE 2: ZONE & LANE OPTIMIZATION
============================================================

Step 2.1 -- Zone Distribution Analysis

Analyze shipment zone distribution: origin ZIP(s) to destination zone histogram,
average zone shipped, zone concentration (what percentage of volume is in zones 5-8
where rates are highest), zone vs. revenue correlation. Identify the zone distribution
curve and where the cost inflection points are.

Step 2.2 -- Zone-Skip / Zone-Reduction Strategies

Evaluate zone-skip opportunities: identify high-volume destination regions that could
benefit from consolidated LTL/FTL injection to a regional hub, calculate per-package
savings from zone reduction (e.g., zone 7 to zone 2 equivalent), assess consolidation
deconsolidation costs, evaluate USPS DDU/SCF entry discount programs, check for
carrier pool point / zone-skip programs already in place.

Step 2.3 -- Multi-Origin Optimization

Check for distributed fulfillment optimization: multi-warehouse inventory placement
vs. average zone shipped, split shipment cost vs. single-origin cost, origin selection
algorithm (cheapest carrier-origin pair), check for network modeling tools (LLamasoft,
Coupa, o9 Solutions integration).

Step 2.4 -- Lane Rate Benchmarking

Compare rates on high-volume lanes: identify the top 20 origin-destination pairs by
spend, benchmark against published rates and industry averages (Freightos, DAT, SMC3
CzarLite for LTL), identify lanes where negotiated rates exceed market rates, flag
lanes with no competitive carrier alternative.

============================================================
PHASE 3: MODAL OPTIMIZATION
============================================================

Step 3.1 -- Parcel vs. LTL Threshold Analysis

Evaluate modal break points: identify shipment weight/cube thresholds where LTL becomes
cheaper than multi-parcel (typically 150-300 lbs or 3+ parcels), check for automatic
modal selection logic, verify that LTL pricing uses correct NMFC (National Motor Freight
Classification) codes and freight classes (50-500), check for density-based re-classification
risk.

Step 3.2 -- LTL vs. FTL Break Points

Analyze LTL to FTL conversion opportunities: identify lanes where LTL spend exceeds
FTL equivalent (typically at 8,000+ lbs or 10+ pallets), check for LTL volume discount
programs (FAK -- Freight All Kinds agreements), evaluate partial truckload (PTL) options,
assess pool distribution for multi-stop TL vs. individual LTL shipments.

Step 3.3 -- Parcel Consolidation Programs

Evaluate consolidation options: USPS Commercial Plus pricing eligibility, Parcel Select
Lightweight, UPS SurePost / FedEx SmartPost economics (last-mile USPS handoff), ground
economy services, regional carrier injection for specific zones, manifesting and
pre-sort discount programs.

Step 3.4 -- Alternative Modal Options

Check for alternative mode utilization: intermodal (rail + truck) for 4+ day transit
tolerance, air freight for high-value/urgent, ocean consolidation for international,
courier networks for local/same-day, drone/autonomous delivery pilots.

============================================================
PHASE 4: ACCESSORIAL CHARGE AUDIT
============================================================

Step 4.1 -- Surcharge Inventory

Catalog all accessorial charges in carrier invoices and rate tables: fuel surcharge
(percentage of base rate, indexed to DOE diesel price), residential delivery surcharge
($4-7 per package), additional handling (weight > 50 lbs, length > 48", not in
corrugated packaging), delivery area surcharge (DAS/DAS Extended), large package
surcharge (L+2(W+H) > 130"), oversize charges, signature required fees, address
correction charges, Saturday/Sunday delivery premium.

Step 4.2 -- Surcharge Avoidance Analysis

Identify avoidable surcharges: address correction charges (improve address validation),
residential vs. commercial misclassification (verify delivery type coding), additional
handling charges (packaging optimization to stay under thresholds), DAS charges
(identify alternative delivery points -- locker, access point, commercial neighbor),
dimension-triggered surcharges (right-size packaging to avoid large package thresholds).

Step 4.3 -- Invoice Audit Patterns

Evaluate invoice audit processes: duplicate charge detection, rate vs. contract
verification, weight/dimension dispute resolution, late delivery refund claims
(guaranteed service refund / GSR), lost/damaged package claim recovery, manifest vs.
invoice reconciliation. Estimate recovery amount from systematic auditing.

Step 4.4 -- Fuel Surcharge Analysis

Analyze fuel surcharge impact: current fuel surcharge percentage by carrier, fuel
surcharge as percentage of total shipping cost, fuel surcharge cap negotiations,
fuel surcharge index basis (DOE weekly diesel price), flat fuel surcharge alternatives
available in carrier contracts.

============================================================
PHASE 5: NEGOTIATION & CONTRACT ANALYSIS
============================================================

Step 5.1 -- Contract Term Review

Evaluate carrier contract terms: discount structure (tiered by revenue band), minimum
volume commitments, MRC (Minimum Revenue Commitment) clauses, rate increase caps (GRI
-- General Rate Increase limitations), contract duration, termination/renegotiation
windows, most-favored-customer clauses, earned discount thresholds.

Step 5.2 -- Negotiation Leverage Points

Identify leverage for rate negotiation: volume concentration (percentage of spend with
each carrier), competitive density (lanes where 2+ carriers compete), growth trajectory
(projected volume increase as negotiation chip), off-peak volume flexibility, service
level downgrades acceptable to customers, mode shift threats (parcel to LTL, LTL to TL).

Step 5.3 -- Savings Opportunity Quantification

Build a savings waterfall: rate renegotiation potential (benchmark gap x volume),
zone-skip savings (zone reduction x affected volume), modal optimization savings
(parcel-to-LTL and LTL-to-FTL conversions), accessorial avoidance (surcharge reduction),
invoice audit recovery, packaging optimization (DIM weight reduction). Prioritize by
implementation effort and confidence level.

============================================================
PHASE 6: WRITE REPORT
============================================================

Write analysis to `docs/shipping-cost-analysis.md` (create `docs/` if needed).

Include: Executive Summary (total shipping spend breakdown, top 3 savings opportunities
with estimated dollar impact), Carrier Rate Structure Assessment, Zone Distribution
Analysis, Modal Optimization Opportunities, Accessorial Charge Audit Findings,
Negotiation Leverage Assessment, Prioritized Savings Roadmap with implementation timeline.


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

## Shipping Cost Analysis Complete

- Report: `docs/shipping-cost-analysis.md`
- Carriers analyzed: [count]
- Service levels mapped: [count]
- Accessorial categories audited: [count]
- Total identified savings opportunity: [estimated percentage of spend]

### Summary Table
| Area | Status | Priority |
|------|--------|----------|
| Carrier rate competitiveness | [status] | [priority] |
| Zone-skip opportunities | [status] | [priority] |
| Modal optimization (parcel/LTL/FTL) | [status] | [priority] |
| Accessorial charge reduction | [status] | [priority] |
| DIM weight optimization | [status] | [priority] |
| Contract negotiation leverage | [status] | [priority] |

NEXT STEPS:

- "Run `/box-optimization` to reduce DIM weight and packaging costs feeding into shipping rates."
- "Run `/warehouse-flow` to assess how carrier pickup windows affect warehouse throughput."
- "Run `/damage-prediction` to ensure cost-optimized shipping methods don't increase damage rates."

DO NOT:

- Recommend the cheapest carrier without considering transit time SLA requirements.
- Ignore accessorial charges -- they can represent 15-25% of total shipping cost.
- Assume published rates are the baseline -- always check for negotiated contract rates.
- Overlook NMFC classification accuracy for LTL shipments -- misclassification causes re-bills.
- Recommend zone-skip programs without modeling the consolidation and deconsolidation costs.


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /shipping-cost — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
