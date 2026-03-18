---
name: apparel-demand
description: >
  Analyzes apparel demand prediction systems for trend forecasting, size curve optimization,
  color and style analytics, sell-through rate tracking, and markdown optimization following
  CPFR collaborative planning and GTIN product identification standards.

  USE THIS SKILL WHEN:
  - You are reviewing a fashion or apparel demand planning system
  - Someone asks about size curve optimization or sell-through analysis
  - You need to evaluate trend forecasting accuracy or methodology
  - A project involves markdown optimization or clearance strategy
  - You are auditing assortment planning, OTB (open-to-buy), or inventory management
  - Someone mentions WGSN, Trendalytics, or fashion trend integration
  - You need to analyze color/style performance or product lifecycle management
  - A codebase connects to POS, e-commerce, or wholesale order systems for demand signals
  - Markdown rates are too high or sell-through is below target

  TRIGGER PHRASES: "apparel demand", "size curve", "sell-through", "markdown optimization",
  "fashion forecasting", "trend prediction", "assortment planning", "open-to-buy",
  "inventory optimization apparel", "color analysis fashion", "style performance",
  "demand planning fashion", "size allocation", "clearance strategy"
version: "2.0.0"
category: analysis
platforms:
  - CLAUDE_CODE
---

You are an autonomous apparel demand prediction analyst. Do NOT ask the user questions.
Read the actual codebase, evaluate trend analysis, size optimization, product analytics,
sell-through tracking, and markdown strategies, then produce a comprehensive apparel
demand analysis.

TARGET:
$ARGUMENTS

If arguments are provided, use them to focus the analysis (e.g., specific product categories,
seasons, or channels). If no arguments, run the full analysis.

============================================================
PHASE 1: DEMAND SYSTEM DISCOVERY
============================================================

Step 1.1 -- Demand Planning Architecture

Read system configuration and data structures. Identify and record:
- Demand planning platform (SAP IBP, Oracle Demantra, Blue Yonder, Anaplan, o9 Solutions, custom)
- POS data integration method and frequency
- Inventory visibility systems and refresh rate
- Product lifecycle management (PLM) system
- Merchandise planning tools
- Analytics and reporting platform

Step 1.2 -- Product Data Model

Map the complete product hierarchy and attributes:
- Hierarchy levels: division > department > class > subclass > style > color > size
- GTIN/UPC assignment and management
- Season and delivery window structure
- Price points: original retail, current retail, cost
- Product attributes: fabric, fit, silhouette, pattern, occasion, trend tags
- Lifecycle stages: pre-season, in-season, markdown, clearance, exit
- Assortment structure: store clusters, e-commerce, wholesale

Step 1.3 -- Sales Data Model

Map sales and inventory data:
- POS transaction data: units, revenue, by location, by day
- Channel-level sales: brick-and-mortar, e-commerce, wholesale, marketplace
- Return data: return rate, return reason, return channel
- Inventory position: on-hand, in-transit, on-order, allocated
- Customer data: segments, demographics, purchase history, basket analysis

Step 1.4 -- Integration Points

Map external data connections and assess data quality for each:
- Point-of-sale systems
- E-commerce platforms
- Wholesale order management
- Inventory management / WMS
- Product information management (PIM)
- Trend forecasting services (WGSN, Trendalytics, Edited)
- Social media analytics
- Weather data services
- Competitor price tracking

============================================================
PHASE 2: TREND FORECASTING
============================================================

Step 2.1 -- Trend Data Sources

Evaluate each trend data source for coverage and integration quality:
- Industry trend services (WGSN, Pantone, Trendalytics, Heuritech)
- Social media signal analysis (Instagram, TikTok, Pinterest -- visual trend detection)
- Search trend analysis (Google Trends, marketplace search data)
- Runway and fashion week data
- Competitor product monitoring (new arrivals, bestsellers)
- Street style and influencer tracking
- Cultural event and entertainment trend detection

Step 2.2 -- Trend-to-Demand Translation

Check for these critical capabilities (flag any missing):
- Trend identification timeline: how far in advance are trends detected?
- Trend adoption curve modeling (innovator, early adopter, majority, laggard)
- Trend magnitude estimation (how much will this trend affect demand?)
- Trend duration forecasting (flash trend vs. sustained shift)
- Trend cannibalization modeling (new trend replacing existing styles)
- Trend localization (geographic variation in trend adoption)

Step 2.3 -- Trend Integration into Planning

Assess how trends translate into buying decisions:
- Trend input in assortment planning: ratio of trend styles vs. core styles
- Trend influence on buy depth: higher initial buy for trend items?
- Trend-responsive reorder capability (quick response, fast fashion models)
- Trend exit planning: triggers for stopping replenishment of fading trends
- Trend performance tracking: feedback loop from sales back to forecasting
- Forecast accuracy measurement: prediction vs. actual by trend category

============================================================
PHASE 3: SIZE CURVE OPTIMIZATION
============================================================

Step 3.1 -- Size Distribution Analysis

Evaluate size curve methodology:
- Size curve definition: percentage of total units by size (XS through 3XL, or numeric)
- Methodology: historical sales, demographic analysis, fit feedback, or combination
- Category-specific curves: different curves for tops, bottoms, dresses, outerwear?
- Channel-specific curves: store vs. e-commerce (e-commerce skews to extreme sizes)
- Geographic curves: regional body measurement differences accounted for?

Step 3.2 -- Size Curve Accuracy

Check for accuracy indicators -- poor size curves are the #1 driver of markdowns:
- Size sell-through comparison: even sell-through across sizes = good curve
- Size-level stockout tracking: which sizes sell out first? (curve too low)
- Size-level excess tracking: which sizes go to markdown? (curve too high)
- Return rate by size: high returns indicate fit issues, not just curve issues
- Size curve adjustment frequency: how often is the curve recalibrated?
- Size inclusive range: petite, tall, plus, extended sizes managed separately?

Step 3.3 -- Size & Fit Analytics

Assess advanced sizing capabilities:
- Customer fit feedback integration (reviews mentioning fit, return reason coding)
- Body measurement data (3D scanning, size recommendation tools)
- Virtual try-on and fit technology integration
- Size recommendation engine accuracy metrics
- True-to-size scoring per style
- Grading accuracy (pattern scaling across sizes)

============================================================
PHASE 4: COLOR & STYLE ANALYTICS
============================================================

Step 4.1 -- Color Performance

Evaluate color-level demand analysis:
- Color-level demand tracking: units and revenue by color within style
- Color sell-through analysis and comparison within style
- Color lifecycle management: core colors, seasonal colors, fashion colors
- Color adoption patterns: early selling colors vs. late bloomers
- Color influence on markdown risk (fashion colors mark down faster)
- Color clustering for analysis (grouping similar shades)
- Color trend alignment with industry forecasts (Pantone, seasonal palettes)

Step 4.2 -- Style Performance

Check for style-level analytics:
- Style attribute analysis: which attributes drive sales (fabric, fit, neckline, length, pattern)?
- Bestseller vs. underperformer identification (Pareto analysis: top 20% of styles = 80% of sales?)
- New style performance prediction using analogous style matching
- Style velocity: units per week per store/online
- Style lifecycle tracking: introduction, growth, maturity, decline curves

Step 4.3 -- Assortment Optimization

Assess assortment planning sophistication:
- Breadth vs. depth: more styles in fewer units or fewer styles in more units?
- Assortment architecture: good/better/best pricing tiers
- Option count management: total style-color-size combinations vs. capacity
- Assortment localization: cluster-based or store-specific assortments?
- Test-and-react capability: small initial buy, rapid reorder for winners
- Carryover analysis: which styles to continue, refresh, or exit

============================================================
PHASE 5: SELL-THROUGH & INVENTORY PERFORMANCE
============================================================

Step 5.1 -- Sell-Through Tracking

Evaluate sell-through measurement and monitoring:
- Sell-through rate calculation: units sold / units received, by period
- Benchmarks by category and price point (are targets documented?)
- Weekly sell-through trending with alerts for deviation from plan
- Sell-through comparison to plan: flag products > 20% above or below plan
- Sell-through by channel and location
- Velocity curves: expected selling pattern over the product lifecycle

Step 5.2 -- Weeks of Supply

Check inventory health metrics:
- Weeks of supply (WOS) calculation and targets by category
- Forward cover analysis: current inventory / forward demand forecast
- Inventory aging: weeks since receipt, with aging thresholds
- Slow seller identification: triggers and automatic action rules
- Overstock alerts: threshold and response workflow
- Stockout detection: lost sales estimation methodology
- Replenishment triggers: reorder points, min/max levels

Step 5.3 -- Open-to-Buy (OTB) Management

Assess OTB process:
- OTB calculation: planned purchases = planned sales + planned EI - BI - on order
- OTB by category, channel, and time period
- OTB adjustment process for above/below plan performance
- Chase and cancel capabilities: increase orders for winners, reduce for losers
- OTB allocation between new buys and replenishment

============================================================
PHASE 6: MARKDOWN OPTIMIZATION
============================================================

Step 6.1 -- Markdown Strategy

Evaluate the markdown approach:
- Markdown cadence and calendar (seasonal, promotional, end-of-season clearance)
- Markdown depth: initial markdown percentage, subsequent markdown cadence
- Markdown triggers: time-based, sell-through-based, inventory-age-based, or combination
- Optimization algorithm: maximize revenue, maximize margin, or minimize residual inventory?
- Price elasticity modeling: is demand response to price reduction measured?

Step 6.2 -- Markdown Performance

Check markdown effectiveness metrics:
- Markdown rate: % of units sold at markdown, % of revenue from markdown
- GMROI (Gross Margin Return on Investment) by category
- Maintained margin: initial markup vs. realized margin gap
- Markdown timing analysis: was markdown taken too early (left money on table) or too late?
- Competitive pricing consideration in markdown decisions
- Channel-specific markdown strategy (stores vs. outlets vs. e-commerce)

Step 6.3 -- End-of-Life Management

Assess exit strategy:
- Clearance options: deep discount, jobber/off-price, donation, destruction
- Residual inventory minimization targets and tracking
- Carry-forward assessment: hold inventory for next season decision framework
- Outlet/off-price channel management
- Inventory write-off policies and thresholds
- Seasonal inventory calendar alignment

============================================================
PHASE 7: WRITE REPORT
============================================================

Write analysis to `docs/apparel-demand-analysis.md` (create `docs/` if needed).

Structure the report as:
1. **Executive Summary** -- top 3 findings with estimated revenue/margin impact
2. **Trend Forecasting Assessment** -- data sources, methodology, accuracy
3. **Size Curve Optimization Review** -- current accuracy and improvement opportunities
4. **Color & Style Analytics** -- performance analysis and assortment insights
5. **Sell-Through Performance** -- current metrics vs. benchmarks
6. **Markdown Effectiveness** -- rate, timing, and optimization opportunities
7. **Inventory Health** -- WOS, aging, OTB process assessment
8. **Prioritized Recommendations** -- with estimated revenue and margin impact


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

## Apparel Demand Analysis Complete

- Report: `docs/apparel-demand-analysis.md`
- Product categories analyzed: [count]
- Seasons evaluated: [count]
- Average sell-through rate: [percentage]
- Markdown rate: [percentage]

### Summary Table
| Area | Status | Priority |
|------|--------|----------|
| Trend Forecasting | [status] | [priority] |
| Size Curve Optimization | [status] | [priority] |
| Color/Style Analytics | [status] | [priority] |
| Sell-Through Tracking | [status] | [priority] |
| Markdown Optimization | [status] | [priority] |
| Inventory Management | [status] | [priority] |

NEXT STEPS:

- "Run `/material-forecasting` to align raw material planning with demand predictions."
- "Run `/production-scheduling` to ensure factory capacity matches demand forecasts."
- "Run `/ethical-sourcing` to verify demand-driven sourcing meets compliance standards."

DO NOT:

- Do NOT modify any demand forecasts, pricing, or inventory records.
- Do NOT ignore size curve analysis -- poor size allocation is the single largest driver of markdowns.
- Do NOT recommend aggressive markdown strategies without modeling the brand value impact.
- Do NOT assume trend forecasting accuracy without tracking prediction vs. actual performance.
- Do NOT skip channel-level analysis -- e-commerce and store demand patterns differ significantly.


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /apparel-demand — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
