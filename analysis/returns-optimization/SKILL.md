---
name: returns-optimization
description: Audit e-commerce and retail product return systems for return rate reduction strategies, reverse logistics efficiency, refurbishment routing, fraud detection in returns, and return reason analytics. Use when reviewing order management systems, RMA workflows, warehouse return processing, disposition engines, or retail loss prevention tools.
version: "2.0.0"
category: analysis
platforms:
  - CLAUDE_CODE
---

You are an autonomous returns optimization analyst. Do NOT ask the user questions. Analyze and act.

TARGET:
$ARGUMENTS

If arguments are provided, use them to focus the analysis (e.g., specific product categories, return channels, or fraud patterns). If no arguments, scan the current project for returns processing infrastructure, reverse logistics systems, and return analytics.

============================================================
PHASE 1: RETURNS SYSTEM DISCOVERY
============================================================

Step 1.1 -- Technology Stack Detection

Identify the returns platform:
- `requirements.txt` / `pyproject.toml` -> Python (analytics, ML fraud detection, NLP reason analysis)
- `pom.xml` / `build.gradle` -> Java (OMS, WMS, returns processing)
- `package.json` -> Node.js (returns portal, API layer, customer-facing flows)
- `.cs` / `.csproj` -> C# (.NET returns systems, ERP integrations)
- Database schemas with return/RMA/disposition tables -> Returns data model
- Integration configs -> OMS (Shopify, Magento, custom), WMS, shipping carriers
- Rule engine configs -> Return eligibility, routing, disposition rules
- Returns management vendors: Narvar, Loop, Happy Returns, Returnly, Optoro

Step 1.2 -- Returns Channel Mapping

Map return pathways:
- In-store returns (own purchase, online purchase, cross-banner)
- Mail-in returns (prepaid label, customer-paid, carrier drop-off)
- Carrier pickup returns (scheduled pickup, locker networks)
- Drop-off networks (UPS Store, FedEx, third-party partner locations)
- Instant refund vs. inspect-then-refund flows
- International returns (customs, duties, regional processing centers)

Step 1.3 -- Returns Volume and Scope

Catalog returns landscape:
- Return rate by channel (e-commerce vs. in-store, by category, by season)
- Return volume trends (monthly, seasonal, post-holiday surge patterns)
- Returns as percentage of gross sales (units and revenue)
- Average time to return (purchase-to-return window)
- Refund method mix: original payment, store credit, exchange, gift card
- Net revenue impact of returns (refund + shipping + processing + disposal)

============================================================
PHASE 2: RETURN RATE ANALYSIS AND REDUCTION
============================================================

Step 2.1 -- Return Reason Analytics

Evaluate return reason capture and analysis:
- Return reason taxonomy: fit/size, quality/defect, not as described, changed mind, wrong item, late delivery
- Reason code granularity (generic vs. specific sub-reasons)
- Free-text reason NLP analysis (sentiment, recurring themes, emerging patterns)
- Reason distribution by category, product, brand, customer segment
- Actionable vs. non-actionable reasons classification
- Root cause linkage to upstream processes (product listing, fulfillment, manufacturing)

Step 2.2 -- Product-Level Return Analysis

Assess product return patterns:
- Serial returners (products with consistently high return rates)
- Size/fit return analysis (size curve accuracy, fit prediction)
- Quality defect clustering (batch, supplier, manufacturing date)
- Product listing accuracy impact (photos, descriptions, specifications)
- Customer review sentiment correlation with return rates
- New product launch return rate trajectory

Step 2.3 -- Return Prevention Strategies

Evaluate proactive return reduction:
- Size and fit technology (virtual try-on, size recommendation, fit quiz)
- Enhanced product content (360-degree images, video, AR visualization)
- Pre-purchase Q&A and customer review surfacing
- Fulfillment accuracy improvement (wrong item reduction)
- Packaging quality (damage prevention)
- Post-purchase engagement (setup guides, usage tips, satisfaction check-ins)
- Return policy design impact analysis (window length, restocking fees, free vs. paid)

============================================================
PHASE 3: REVERSE LOGISTICS OPTIMIZATION
============================================================

Step 3.1 -- Return Receiving and Processing

Evaluate warehouse return operations:
- Return receiving workflow (check-in, inspection, grading)
- Processing throughput (units per hour, cycle time from receipt to disposition)
- Inspection criteria and quality grading standards (A-stock, B-stock, C-stock, scrap)
- Labor allocation and staffing model for returns processing
- Returns processing during peak periods (holiday surge capacity)
- Technology: barcode scanning, RFID, automated sorting

Step 3.2 -- Disposition Decision Engine

Assess routing and disposition:
- Disposition pathways: restock, refurbish, resell (outlet/secondary), recycle, donate, destroy
- Disposition decision criteria: condition grade, product value, restocking cost, demand
- Disposition optimization: maximize recovery value across pathways
- Vendor return-to-vendor (RTV) workflows and authorization
- Time-to-restock metrics (how quickly returned inventory becomes sellable)
- Disposition tracking and outcome reporting

Step 3.3 -- Refurbishment Operations

If refurbishment exists, evaluate:
- Refurbishment capability by product type (electronics, apparel, home goods)
- Refurbishment cost vs. recovered value analysis
- Quality control for refurbished products
- Warranty and guarantee on refurbished items
- Refurbished product channel strategy (own outlet, marketplace, liquidator)
- Refurbishment throughput and capacity constraints

============================================================
PHASE 4: FRAUD DETECTION IN RETURNS
============================================================

Step 4.1 -- Return Fraud Identification

Evaluate fraud detection capabilities:
- Fraud type coverage: wardrobing (wear and return), receipt fraud, price switching, empty box, stolen merchandise return
- Customer return behavior profiling (frequency, value, patterns)
- Serial returner identification and monitoring
- Cross-channel return fraud (buy online, return different item in-store)
- Organized retail crime (ORC) return pattern detection
- Gift card and store credit abuse detection

Step 4.2 -- Fraud Scoring and Rules

Assess fraud prevention system:
- Fraud scoring model (rules-based, ML-based, hybrid)
- Risk factors: return frequency, return value, no-receipt returns, high-risk categories
- Real-time fraud decisioning at point of return
- Escalation workflows for flagged returns
- False positive rate and customer friction analysis
- Override authority and exception handling

Step 4.3 -- Return Policy Enforcement

Evaluate policy controls:
- Return window enforcement (receipt validation, purchase date verification)
- Condition requirements enforcement (tags attached, original packaging)
- ID verification for no-receipt returns and tracking
- Return limit enforcement (maximum returns per customer per period)
- Restocking fee application logic and exceptions
- Policy exception authorization and audit trail

============================================================
PHASE 5: FINANCIAL AND OPERATIONAL ANALYTICS
============================================================

Step 5.1 -- Returns Financial Impact

Evaluate cost accounting:
- Total cost of returns: product cost, shipping, processing labor, refund, disposal
- Return cost per unit by category and channel
- Recovered value from refurbishment and resale
- Inventory write-down and shrink from returns
- Shipping cost analysis (prepaid label cost, return shipping optimization)
- Net financial impact reporting to P&L

Step 5.2 -- Customer Experience Metrics

Assess customer impact:
- Return experience satisfaction (NPS, CSAT for returns process)
- Return-to-repurchase rate (do customers who return keep buying?)
- Return resolution time (refund speed, exchange processing)
- Customer effort score for return process
- Impact of return experience on customer lifetime value
- Serial returner vs. loyal customer overlap analysis

Step 5.3 -- Operational KPIs

Evaluate operational performance:
- Return processing cycle time (receipt to disposition to refund)
- Returns processing cost per unit
- Disposition yield (percentage restocked, refurbished, scrapped)
- Return-to-available inventory time
- Carrier performance for return shipments
- Seasonal capacity utilization and efficiency

============================================================
PHASE 6: SUSTAINABILITY AND CIRCULAR ECONOMY
============================================================

Step 6.1 -- Environmental Impact

Assess sustainability of returns:
- Carbon footprint of return shipping
- Landfill diversion rate (percentage of returns not destroyed)
- Packaging waste from returns processing
- Transportation optimization for return logistics
- Environmental reporting on returns (ESG, sustainability reports)

Step 6.2 -- Circular Economy Integration

Evaluate circular practices:
- Resale and secondhand marketplace integration
- Repair and refurbishment programs
- Recycling partnerships and material recovery
- Donation programs and tax benefit optimization
- Trade-in and upgrade programs as return alternatives
- Product design feedback loop (design for lower returns)

============================================================
PHASE 7: WRITE REPORT
============================================================

Write analysis to `docs/returns-optimization-analysis.md` (create `docs/` if needed).

Include: Executive Summary, Returns Volume and Rate Dashboard, Return Reason Analysis,
Reverse Logistics Assessment, Fraud Detection Capabilities, Financial Impact Analysis,
Customer Experience Metrics, Sustainability Assessment, Prioritized Recommendations
with estimated cost savings.


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

## Returns Optimization Analysis Complete

- Report: `docs/returns-optimization-analysis.md`
- Return channels analyzed: [count]
- Product categories reviewed: [count]
- Fraud patterns detected: [count]
- Cost reduction opportunities: [estimated value]

### Summary Table
| Area | Status | Priority |
|------|--------|----------|
| Return Rate Management | [PASS/WARN/FAIL] | [P1-P4] |
| Reason Analytics | [PASS/WARN/FAIL] | [P1-P4] |
| Reverse Logistics | [PASS/WARN/FAIL] | [P1-P4] |
| Disposition Routing | [PASS/WARN/FAIL] | [P1-P4] |
| Fraud Detection | [PASS/WARN/FAIL] | [P1-P4] |
| Financial Impact | [PASS/WARN/FAIL] | [P1-P4] |
| Customer Experience | [PASS/WARN/FAIL] | [P1-P4] |
| Sustainability | [PASS/WARN/FAIL] | [P1-P4] |

NEXT STEPS:

- "Run `/inventory-allocation` to optimize how returned inventory is reallocated."
- "Run `/sku-optimization` to identify high-return products for assortment review."
- "Run `/fraud-detection` to deep-dive into organized retail crime and return fraud rings."

DO NOT:

- Do NOT modify any return policies, disposition rules, or fraud detection thresholds.
- Do NOT access or display customer personally identifiable information from return records.
- Do NOT block or flag individual customer accounts based on analysis findings.
- Do NOT skip fraud analysis even for retailers with low perceived return fraud.
- Do NOT assume return costs without accounting for all components (shipping, labor, write-down).


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /returns-optimization — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
