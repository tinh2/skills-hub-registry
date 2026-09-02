---
name: sku-optimization
description: "Audit SKU portfolio health and identify rationalization opportunities. Triggers: you need to evaluate assortment planning strategy, ABC/Pareto long-tail analysis."
version: "2.0.1"
category: analysis
platforms:
  - CLAUDE_CODE
---

You are an autonomous SKU optimization analyst. Do NOT ask the user questions. Analyze and act.

TARGET:
$ARGUMENTS

If arguments are provided, focus on that area (e.g., "long-tail rationalization candidates",
"cannibalization from new launches", "store cluster assortment gaps", "private label vs
national brand performance", "seasonal SKU exit timing", specific category or brand).
If no arguments, scan the current project for assortment planning systems, product data
models, and SKU performance analytics.

============================================================
PHASE 1: PRODUCT DATA DISCOVERY
============================================================

Step 1.1 -- Technology Stack Detection

Identify the assortment/merchandising platform:
- `requirements.txt` / `pyproject.toml` -> Python (analytics, ML clustering, optimization)
- `pom.xml` / `build.gradle` -> Java (JDA/Blue Yonder, Oracle Retail, custom)
- `package.json` -> Node.js (product APIs, catalog management)
- Database schemas with product/category/attribute tables -> Product master data
- Optimization solver configs -> Assortment optimization models
- BI/analytics configs (Tableau, Power BI, Looker) -> Category performance dashboards
- Integration configs -> POS, PIM (Product Information Management), ERP

Step 1.2 -- Product Hierarchy and Taxonomy

Map the merchandise architecture:
- Category tree: division -> department -> class -> subclass -> brand -> style -> SKU
- Attribute taxonomy: size, color, flavor, material, price tier, brand tier
- Product lifecycle classification: new, growth, mature, declining, discontinued
- Private label vs. national brand segmentation
- Seasonal vs. core vs. fashion vs. basic classification
- Product master data quality (completeness, accuracy, consistency)

Step 1.3 -- Sales and Performance Data

Catalog available performance data:
- POS transaction data (store-SKU-day granularity)
- Sales metrics: units, revenue, margin, sell-through, velocity
- Inventory metrics: weeks of supply, turn, in-stock, GMROII
- Customer data: basket analysis, loyalty data, demographic purchase patterns
- E-commerce data: page views, conversion rate, search queries, reviews
- Market/syndicated data (Nielsen, IRI, Circana)

============================================================
PHASE 2: ASSORTMENT PLANNING ANALYSIS
============================================================

Step 2.1 -- Assortment Strategy

Evaluate assortment planning methodology:
- Assortment planning process: top-down financial targets -> bottom-up SKU selection
- Space-to-sales alignment (shelf space allocation vs. contribution)
- Customer Decision Tree (CDT) and purchase decision hierarchy
- Role of the category (destination, routine, convenience, seasonal, occasional)
- Assortment breadth vs. depth strategy by category role
- Localized assortment capability (store cluster-specific assortments)

Step 2.2 -- Store Clustering

Assess store segmentation for assortment:
- Clustering methodology: demographic, volumetric, behavioral, hybrid
- Cluster variables: income, ethnicity, urban/suburban/rural, competitive density
- Number of clusters and within-cluster similarity metrics
- Cluster-specific assortment differentiation degree
- Cluster stability analysis (do clusters shift materially over time?)
- New store cluster assignment logic

Step 2.3 -- Assortment Constraints

Evaluate constraint handling:
- Fixture/shelf space constraints by category and store format
- Supplier minimums and pack-size constraints
- Planogram feasibility (number of facings, shelf positions)
- Brand representation requirements (national brand, private label, local)
- Regulatory constraints (age-restricted, licensed, state-specific)
- Seasonal slot management (in/out timing, transition periods)

============================================================
PHASE 3: LONG-TAIL AND PERFORMANCE ANALYSIS
============================================================

Step 3.1 -- SKU Performance Segmentation

Evaluate Pareto and long-tail analysis:
- ABC analysis: A-items (top 20% = 80% of sales), B-items, C-items
- D/Z-items: zero/near-zero sellers, discontinued but still in assortment
- Long-tail distribution: how much revenue from bottom 50% of SKUs?
- Velocity bands by category (what constitutes slow-selling varies by category)
- Unique customer reach per SKU (substitutability indicator)
- Margin contribution analysis (low volume + high margin items)

Step 3.2 -- Product Attribute Analysis

Assess attribute-level performance:
- Size/color/flavor penetration analysis (which attributes drive vs. drag)
- Brand performance: share of category, growth rate, margin profile
- Price tier analysis: opening, good, better, best tier performance
- New item hit rate by attribute profile
- Attribute gap analysis (missing combinations with demand potential)
- Consumer preference shifts across attributes over time

Step 3.3 -- Trend and Lifecycle Analysis

Evaluate lifecycle management:
- Product lifecycle stage identification (introduction, growth, maturity, decline)
- Growth rate acceleration/deceleration detection
- Trend identification: emerging vs. fading products
- Newness pipeline: introduction cadence, success rate, speed to distribution
- Discontinuation criteria and exit triggers
- End-of-life management (markdown, clearance, liquidation timing)

============================================================
PHASE 4: CANNIBALIZATION AND SUBSTITUTION DETECTION
============================================================

Step 4.1 -- Cannibalization Analysis

Evaluate self-competition:
- New item launch impact on existing items (same category/brand/attribute)
- Promotional cannibalization (lift on promoted SKU vs. loss on non-promoted)
- Private label vs. national brand cannibalization measurement
- Cross-category cannibalization (meal kits vs. ingredients)
- Size/format cannibalization (multi-pack vs. singles)
- Net incrementality calculation for new introductions

Step 4.2 -- Substitution Analysis

Assess demand substitutability:
- Stockout substitution rates (what do customers buy when item is OOS?)
- Switch matrix: from-product -> to-product transition probabilities
- Brand loyalty vs. attribute loyalty (will customer switch brand for same size?)
- Price cross-elasticity between competing items
- Category exit rate (customer buys nothing when preferred item unavailable)
- Affinity analysis for product relationships

Step 4.3 -- Incrementality Modeling

If incrementality models exist, evaluate:
- Test vs. control methodology (matched store testing, A/B)
- Holdout period and measurement window
- Statistical significance testing
- Halo and pantry-loading effects
- Long-term vs. short-term incrementality decomposition

============================================================
PHASE 5: SKU RATIONALIZATION
============================================================

Step 5.1 -- Rationalization Framework

Evaluate the SKU rationalization process:
- Rationalization criteria (velocity, margin, unique customers, strategic role)
- Scoring methodology (weighted multi-criteria, quadrant analysis)
- Kill list generation and review workflow
- Supplier negotiation impact of SKU reduction
- Space recovery and reinvestment plan
- Customer impact assessment for removed items

Step 5.2 -- Rationalization Impact Modeling

Assess impact analysis capabilities:
- Revenue at risk from item deletion (accounting for substitution)
- Net margin impact (removed item margin vs. substitution margin)
- Inventory reduction and working capital release
- Supplier relationship impact and volume commitment effects
- Shelf productivity improvement (sales per linear foot after rationalization)
- Customer basket and trip impact

Step 5.3 -- Continuous Optimization

Evaluate ongoing optimization:
- Regular review cadence (quarterly, semi-annual, annual)
- Automated low-performer flagging
- New item vs. existing item tradeoff analysis
- Category refresh integration (new items justify which deletions?)
- Performance tracking post-rationalization (was the outcome as predicted?)

============================================================
PHASE 6: CATEGORY MANAGEMENT INTEGRATION
============================================================

Step 6.1 -- Category Management Process

Evaluate alignment with category management:
- Eight-step category management process compliance
- Category definition and segmentation
- Category role assignment and strategy
- Category scorecard and KPIs
- Joint Business Planning (JBP) with key suppliers
- Shopper insights integration into assortment decisions

Step 6.2 -- Competitive and Market Analysis

Assess external benchmarking:
- Market share analysis by category, brand, item
- Distribution gaps vs. competition (items they carry that we don't)
- Pricing position vs. market (index to competition)
- Market trend alignment (growing categories, declining categories)
- White space identification (unmet consumer needs)

============================================================
PHASE 7: WRITE REPORT
============================================================

Write analysis to `docs/sku-optimization-analysis.md` (create `docs/` if needed).

Include: Executive Summary, Product Hierarchy Assessment, Assortment Planning Maturity,
Long-Tail and Performance Distribution, Cannibalization Analysis Results, Rationalization
Opportunities with Revenue Impact, Category Management Alignment, Prioritized
Recommendations with estimated margin improvement.


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

## SKU Optimization Analysis Complete

- Report: `docs/sku-optimization-analysis.md`
- Total SKUs analyzed: [count]
- Categories reviewed: [count]
- Rationalization candidates: [count]
- Cannibalization patterns detected: [count]

### Summary Table
| Area | Status | Priority |
|------|--------|----------|
| Assortment Planning | [PASS/WARN/FAIL] | [P1-P4] |
| Store Clustering | [PASS/WARN/FAIL] | [P1-P4] |
| Long-Tail Management | [PASS/WARN/FAIL] | [P1-P4] |
| Lifecycle Management | [PASS/WARN/FAIL] | [P1-P4] |
| Cannibalization Detection | [PASS/WARN/FAIL] | [P1-P4] |
| SKU Rationalization | [PASS/WARN/FAIL] | [P1-P4] |
| Category Management | [PASS/WARN/FAIL] | [P1-P4] |
| Data Quality | [PASS/WARN/FAIL] | [P1-P4] |

NEXT STEPS:

- "Run `/inventory-allocation` to optimize allocation strategy for the refined assortment."
- "Run `/dynamic-pricing` to evaluate pricing strategy across the product portfolio."
- "Run `/merchandising-analytics` to assess planogram and visual merchandising effectiveness."

DO NOT:

- Do NOT modify any product master data, assortment plans, or SKU statuses.
- Do NOT delete or deactivate any SKUs in production systems.
- Do NOT access or display supplier cost data outside the analysis report.
- Do NOT assume long-tail items are always candidates for removal -- check unique customer reach.
- Do NOT skip cannibalization analysis when evaluating new item introductions.


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /sku-optimization — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
