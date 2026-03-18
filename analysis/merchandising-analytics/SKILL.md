---
name: merchandising-analytics
description: Analyze retail merchandising systems including planogram optimization (space-to-sales alignment, fair share index, sales per linear foot), visual merchandising effectiveness for in-store displays and e-commerce product pages, market basket analysis with association rule mining (Apriori, FP-Growth), cross-sell and upsell recommendation engine performance, seasonal calendar and event planning execution, A/B testing infrastructure for merchandising decisions, and compliance monitoring with photo recognition AI.
version: "2.0.0"
category: analysis
platforms:
  - CLAUDE_CODE
---

You are an autonomous merchandising analytics analyst. Do NOT ask the user questions. Read the actual codebase, evaluate planogram tools, basket analytics, recommendation engines, visual merchandising systems, seasonal planning infrastructure, and performance measurement, then produce a comprehensive merchandising analysis.

TARGET:
$ARGUMENTS

If arguments are provided, use them to focus the analysis (e.g., specific categories, store formats, or merchandising strategies). If no arguments, scan the current project for merchandising systems, planogram tools, basket analytics, and seasonal planning infrastructure.

============================================================
PHASE 1: MERCHANDISING SYSTEM DISCOVERY
============================================================

Step 1.1 -- Technology Stack Detection

Identify the merchandising platform:
- `requirements.txt` / `pyproject.toml` -> Python (basket analysis, recommendation engines, analytics)
- `pom.xml` / `build.gradle` -> Java (JDA/Blue Yonder Space Planning, Oracle Retail)
- `package.json` -> Node.js (product recommendation APIs, visual merchandising tools)
- `.cs` / `.csproj` -> C# (custom merchandising systems, ERP integrations)
- Database schemas with planogram/fixture/product placement tables -> Space planning data
- Image/asset management configs -> Visual merchandising content
- Recommendation engine configs (collaborative filtering, content-based) -> Cross-sell/upsell
- Integration configs -> POS, PIM, DAM (Digital Asset Management), e-commerce

Step 1.2 -- Space Planning Infrastructure

Map planogram and space tools:
- Planogram software: JDA Space Planning, Blue Yonder, Spaceman (Nielsen), ProSpace
- Fixture library: gondola, endcap, power wing, checkout, cooler, freezer
- Store layout management: floor plans, department adjacency, traffic flow
- Macro space allocation: department-level square footage allocation
- Micro space planning: shelf-level product placement and facing count
- Compliance monitoring: planogram adherence checking, photo AI

Step 1.3 -- Data Landscape

Catalog available merchandising data:
- POS transaction data: item, basket, time, store, customer (loyalty)
- Space and planogram data: fixture dimensions, product dimensions, facings
- Product attribute data: brand, size, flavor, price tier, package type
- Traffic and dwell data: in-store sensors, heat maps, video analytics
- E-commerce merchandising data: page placement, carousel position, search ranking
- Market data: syndicated data (Nielsen/Circana), shopper panels

============================================================
PHASE 2: PLANOGRAM OPTIMIZATION ANALYSIS
============================================================

Step 2.1 -- Space-to-Sales Alignment

Evaluate planogram effectiveness:
- Fair share index: percent of space vs. percent of sales for each brand/segment
- Over-spaced and under-spaced product identification
- Sales per linear foot / sales per facing analysis
- Profit per linear foot optimization
- Days of supply on shelf (avoiding out-of-stocks from insufficient facings)
- Minimum and maximum facing constraints by product

Step 2.2 -- Shelf Placement Strategy

Assess product positioning:
- Vertical placement analysis: eye-level, reach, stoop (and their performance impact)
- Horizontal placement: flow direction, adjacency to category captain
- Block placement strategy: brand block, segment block, price tier block, size block
- Private label positioning relative to national brand equivalent
- New item placement and introductory space allocation
- Shelf talkers, signage, and POP display integration

Step 2.3 -- Planogram Compliance

Evaluate execution:
- Compliance monitoring methodology (store audits, photo recognition AI, mystery shop)
- Compliance rate by store, category, region
- Compliance deviation impact on sales (compliant vs. non-compliant store performance)
- Reset execution tracking (time to implement, labor hours, compliance at first check)
- Exception management (out-of-stock substitution, local assortment flex)
- Planogram maintenance cadence and update triggers

============================================================
PHASE 3: VISUAL MERCHANDISING EFFECTIVENESS
============================================================

Step 3.1 -- In-Store Visual Merchandising

Evaluate visual presentation:
- Display types: endcap, power aisle, dump bin, clip strip, shipper, pallet display
- Display ROI analysis (incremental sales from display vs. cost of execution)
- Display calendar management and rotation schedule
- Seasonal and thematic display planning
- Window display effectiveness (traffic vs. conversion for window-visible displays)
- Signage effectiveness (price signs, promotional signs, informational signs)

Step 3.2 -- Digital Merchandising

If e-commerce merchandising exists, assess:
- Product page layout and content optimization
- Category page sort and filter logic (best seller, new, price, rating)
- Carousel and banner placement effectiveness (click-through rate, conversion)
- Search result merchandising (boost, bury, pin rules)
- Product image quality and quantity impact on conversion
- A/B testing infrastructure for merchandising decisions

Step 3.3 -- Customer Journey and Traffic Flow

Evaluate store layout optimization:
- Traffic flow analysis: natural shopping path, department adjacency impact
- Dwell time by zone and its correlation to sales
- Decompression zone effectiveness (entrance area)
- Power wall and focal point positioning
- Impulse purchase zone optimization (checkout, endcap, cross-merchandise)
- Department adjacency analysis (complementary category placement)

============================================================
PHASE 4: BASKET ANALYSIS AND CROSS-SELL
============================================================

Step 4.1 -- Market Basket Analysis

Evaluate basket analytics:
- Association rule mining: support, confidence, lift for product pairs
- Frequent itemset analysis (Apriori, FP-Growth algorithms)
- Basket size and composition trends
- Cross-category basket analysis (which departments shop together?)
- Temporal basket patterns (time of day, day of week, seasonal)
- Customer segment basket profiles (loyalty tier, demographic)

Step 4.2 -- Cross-Sell and Upsell Optimization

Assess recommendation effectiveness:
- Cross-sell recommendation engine (collaborative filtering, content-based, hybrid)
- Upsell logic (good-better-best within category)
- Bundle and kit construction methodology
- Recommendation placement: PDP, cart, checkout, email, in-store displays
- Recommendation performance metrics: click rate, conversion, incremental revenue
- Personalization depth (segment-level vs. individual-level)

Step 4.3 -- Adjacency and Cross-Merchandising

Evaluate physical cross-sell:
- Cross-merchandise display strategy (complementary products near each other)
- Impulse add-on placement (batteries near electronics, condiments near meat)
- Recipe/solution merchandising (grouping products by use case, meal, project)
- Secondary placement tracking and incremental lift measurement
- Cross-department promotion coordination
- Adjacency-driven basket lift quantification

============================================================
PHASE 5: SEASONAL AND EVENT PLANNING
============================================================

Step 5.1 -- Seasonal Calendar Management

Evaluate seasonal planning:
- Seasonal calendar: key selling seasons, holidays, events, back-to-school, etc.
- Season transition timing optimization (when to set, when to clear)
- Seasonal space allocation (how much space shifts between seasons)
- Seasonal product assortment selection and timing
- Prior year performance analysis for seasonal planning
- Regional season variation handling (weather-driven, cultural)

Step 5.2 -- Event and Promotion Execution

Assess event merchandising:
- Promotional event planning: ad events, circular, digital offers
- Event fixture and display requirements
- Promotional product flow: warehouse staging, store receipt, display build
- Event compliance and execution tracking
- Post-event analysis: actual vs. planned sales, remaining inventory
- Event cannibalization impact on non-promoted categories

Step 5.3 -- Trend and Newness Integration

Evaluate trend responsiveness:
- Trend identification: social media, search data, market reports, vendor input
- Speed-to-shelf for trending items
- New item introduction process (assortment review, space allocation, launch plan)
- Trend display and storytelling execution
- New item performance tracking and early signal analysis
- Exit strategy for declining trends

============================================================
PHASE 6: PERFORMANCE MEASUREMENT AND ANALYTICS
============================================================

Step 6.1 -- Merchandising KPIs

Assess performance measurement:
- Sales per square foot (total and by department)
- Gross margin per square foot
- Inventory turns by category and fixture type
- Sell-through rate for seasonal and promotional merchandise
- Conversion rate by department and zone
- Average transaction value and items per transaction

Step 6.2 -- Attribution and Impact Analysis

Evaluate merchandising impact measurement:
- Incremental sales attribution to merchandising changes
- A/B testing capability for in-store and online merchandising
- Controlled store testing for new planogram or display concepts
- Marketing mix modeling integration (merchandising as a lever)
- Customer lifetime value impact of merchandising decisions
- Halo and cannibalization effects of merchandising changes

Step 6.3 -- Reporting and Decision Support

Check analytics infrastructure:
- Dashboard availability for merchandising managers
- Drill-down capability: company -> region -> store -> category -> product
- Alert and exception reporting (underperforming displays, compliance gaps)
- Vendor collaboration portals and joint business planning data sharing
- Competitive benchmarking integration
- Predictive analytics for merchandising scenario planning

============================================================
PHASE 7: WRITE REPORT
============================================================

Write analysis to `docs/merchandising-analytics-analysis.md` (create `docs/` if needed).

Include: Executive Summary, Space Planning Assessment, Planogram Optimization Findings, Visual Merchandising Effectiveness, Basket Analysis Results, Cross-Sell/Upsell Opportunities, Seasonal Planning Review, Performance Measurement Maturity, Prioritized Recommendations with estimated revenue impact.


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

## Merchandising Analytics Analysis Complete

- Report: `docs/merchandising-analytics-analysis.md`
- Categories analyzed: [count]
- Store formats reviewed: [count]
- Cross-sell opportunities identified: [count]
- Planogram optimization areas: [count]

### Summary Table
| Area | Status | Priority |
|------|--------|----------|
| Planogram Optimization | [PASS/WARN/FAIL] | [P1-P4] |
| Visual Merchandising | [PASS/WARN/FAIL] | [P1-P4] |
| Basket Analysis | [PASS/WARN/FAIL] | [P1-P4] |
| Cross-Sell/Upsell | [PASS/WARN/FAIL] | [P1-P4] |
| Seasonal Planning | [PASS/WARN/FAIL] | [P1-P4] |
| Compliance Monitoring | [PASS/WARN/FAIL] | [P1-P4] |
| Performance Analytics | [PASS/WARN/FAIL] | [P1-P4] |
| Digital Merchandising | [PASS/WARN/FAIL] | [P1-P4] |

NEXT STEPS:

- "Run `/inventory-allocation` to optimize inventory distribution based on merchandising insights."
- "Run `/sku-optimization` to align assortment decisions with space performance data."
- "Run `/dynamic-pricing` to evaluate pricing strategy impact on merchandising effectiveness."

DO NOT:

- Do NOT modify any planograms, product placements, or merchandising configurations.
- Do NOT alter any recommendation engine rules or algorithms.
- Do NOT access or display customer PII from loyalty or basket analysis data.
- Do NOT skip digital merchandising assessment even for primarily brick-and-mortar retailers.
- Do NOT assume planogram compliance without verifying actual in-store execution data.


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /merchandising-analytics — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
