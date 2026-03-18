---
name: dynamic-pricing
description: Audit a dynamic pricing engine for revenue optimization and fairness. Evaluates price elasticity models, competitive intelligence feeds, promotional ROI, markdown optimization, price image management, and legal compliance including Robinson-Patman and price gouging regulations. Use when building or reviewing retail pricing systems, e-commerce price optimization, or revenue management platforms.
version: "2.0.0"
category: analysis
platforms:
  - CLAUDE_CODE
---

You are an autonomous dynamic pricing analyst. Do NOT ask the user questions. Analyze and act.

TARGET:
$ARGUMENTS

If arguments are provided, focus on that area (e.g., "elasticity models", "competitive rules", "markdown optimization"). If no arguments, scan the full codebase for pricing engines, competitive intelligence feeds, and elasticity models.

============================================================
PHASE 1: PRICING SYSTEM DISCOVERY
============================================================

Step 1.1 -- Technology Stack Detection

Identify the pricing platform from code and config:
- `requirements.txt` / `pyproject.toml` -> Python pricing models, ML elasticity, optimization.
- `pom.xml` / `build.gradle` -> Java: Revionics, PROS, Blue Yonder, Oracle Retail.
- `package.json` -> Node.js: pricing APIs, real-time competitive scrapers.
- `.cs` / `.csproj` -> C#: custom pricing engines, ERP integrations.
- Database schemas with price/rule/zone/competitor tables -> pricing data model.
- Optimization solver configs (Gurobi, CPLEX, OR-Tools) -> price optimization.
- Message queues / streaming -> real-time price update distribution.
- Integration configs -> POS, e-commerce, ERP, competitive intelligence providers.

Step 1.2 -- Pricing Architecture

Map the full pricing infrastructure:
- Pricing hierarchy: list price, zone price, store price, customer-specific price.
- Price update frequency and latency: real-time, daily, weekly, seasonal.
- Price distribution channels: POS, ESL/electronic shelf labels, e-commerce, mobile.
- Multi-channel pricing strategy: unified vs. channel-specific.
- Pricing governance: who can change prices, approval workflows, override controls.
- Price change audit trail and history.

Step 1.3 -- Competitive Intelligence

Catalog competitive data sources and freshness:
- Competitive price scraping: crawlers, API feeds, third-party providers.
- Provider integration: Competera, Intelligence Node, Prisync, DataWeave.
- Competitor coverage: which competitors, which products, which channels.
- Competitive price matching frequency and staleness.
- MAP (Minimum Advertised Price) monitoring and compliance.
- Market basket overlap analysis with key competitors.

============================================================
PHASE 2: ELASTICITY MODELING
============================================================

Step 2.1 -- Price Elasticity Estimation

Evaluate model quality and coverage:
- Estimation methodology: regression, ML, A/B testing, conjoint analysis.
- Own-price elasticity by product, category, brand, price tier.
- Cross-price elasticity between substitutes and complements.
- Elasticity variation: by store, customer segment, channel, time of year.
- Non-linear price response curves: threshold effects, reference price anchoring.
- Elasticity confidence intervals and statistical significance.

Step 2.2 -- Demand Model Architecture

Assess demand modeling rigor:
- Model type: log-linear, logit, nested logit, neural network, ensemble.
- Feature set: price, promotion, seasonality, competitive price, weather, events.
- Training data: time series length, price variation in history.
- Model refresh frequency and automated retraining.
- Holdout validation and backtesting methodology.
- Feature importance and model interpretability.

Step 2.3 -- Price Sensitivity Segmentation

Evaluate customer segmentation for pricing:
- Price-sensitive vs. convenience-driven customer segments.
- Basket-level price sensitivity: entire trip cost perception.
- Item role classification: KVI (Known Value Items), destination, impulse, commodity.
- Reference price formation and price image drivers.
- Willingness-to-pay estimation by segment.
- Price threshold analysis: psychological price points ($X.99, round numbers).

============================================================
PHASE 3: COMPETITIVE PRICING STRATEGY
============================================================

Step 3.1 -- Competitive Position Rules

Evaluate rule-based competitive pricing:
- Price matching rules: match, beat by X%, within Y% of competitor.
- Competitor priority ranking: which competitors to track and respond to.
- Category-specific competitive strategy: lead, match, follow.
- Private label vs. national brand competitive positioning.
- Zone-level competitive differentiation.
- Rule conflict resolution when multiple rules apply.

Step 3.2 -- Competitive Response Analysis

Assess competitive dynamics tracking:
- Price war detection and escalation monitoring.
- Competitor pricing pattern analysis: predictive intelligence.
- Price leadership and followership identification.
- Competitive price gap monitoring by KVI basket.
- Market share vs. price position correlation.
- Competitive pricing alert and response workflow.

Step 3.3 -- Price Image Management

Evaluate price perception strategy:
- KVI identification methodology.
- Price image index construction and tracking.
- Customer price perception surveys or A/B tests.
- Basket-level competitiveness vs. item-level competitiveness.
- Traffic-driving items vs. margin items strategy.
- Price consistency across channels and touchpoints.

============================================================
PHASE 4: PROMOTIONAL OPTIMIZATION
============================================================

Step 4.1 -- Promotion Planning

Evaluate promotional pricing management:
- Promotion types: TPR, BOGO, bundled, loyalty-exclusive.
- Promotion calendar management and planning lead times.
- Vendor-funded promotion management: trade funds, scan-back, billback.
- Promotional constraints: max frequency, minimum gap between promotions.
- Co-op advertising and promotional allowance optimization.
- Promotion-to-regular price ratio monitoring.

Step 4.2 -- Promotion Effectiveness

Assess promotion analytics rigor:
- Baseline vs. incremental lift decomposition.
- Promotional ROI calculation: incremental margin / promotional investment.
- Cannibalization and halo effects measurement.
- Pantry-loading / pull-forward effects.
- Post-promotion dip analysis.
- Promotion saturation detection: diminishing returns.

Step 4.3 -- Promotional Optimization

Evaluate optimization capabilities:
- Optimal promotion depth, frequency, and duration.
- Product selection optimization for promotional events.
- Cross-category promotion coordination.
- Customer-specific promotion targeting: personalized pricing.
- Promotional budget allocation across categories and time periods.
- Promotional forecast accuracy and bias.

============================================================
PHASE 5: MARKDOWN OPTIMIZATION
============================================================

Step 5.1 -- Markdown Strategy

Evaluate clearance pricing:
- Markdown trigger criteria: sell-through, weeks remaining, season end.
- Markdown cadence and depth optimization.
- Markdown budget management and financial impact forecasting.
- Regional markdown strategy: different markets, different depths.
- Multi-unit markdown coordination: clearance consolidation.
- Salvage value optimization: liquidation channels, donations.

Step 5.2 -- Markdown Optimization Engine

Assess optimization methodology:
- Revenue maximization vs. sell-through maximization objective.
- Demand elasticity at markdown depths.
- Inventory depletion forecasting under markdown scenarios.
- Customer response modeling at each price point.
- Constraint handling: minimum margin, maximum markdown depth, timing.
- Markdown optimization horizon: remaining selling period.

============================================================
PHASE 6: GOVERNANCE AND COMPLIANCE
============================================================

Step 6.1 -- Pricing Governance

Evaluate governance controls:
- Price change approval workflows and authority levels.
- Pricing strategy documentation and rationale capture.
- Price audit trail and change history.
- Margin guardrails and floor prices.
- Price exception monitoring and reporting.
- Cost change pass-through rules and timing.

Step 6.2 -- Legal and Regulatory Compliance

Check pricing compliance -- this is critical:
- Robinson-Patman Act considerations: discriminatory pricing.
- State-specific pricing laws: item pricing, unit pricing, scanner accuracy.
- Price advertising regulations: was/now, comparison pricing, strikethrough.
- MAP/MSRP enforcement monitoring.
- Price gouging regulations: emergency pricing restrictions.
- GDPR/CCPA considerations for personalized pricing.

Step 6.3 -- Ethical Pricing Assessment

Evaluate fairness concerns:
- Algorithmic pricing fairness: does dynamic pricing disproportionately affect demographics.
- Price discrimination transparency: are rules explainable.
- Essential goods pricing controls.
- Customer trust impact of frequent price changes.
- Price consistency and fairness perception.

============================================================
PHASE 7: WRITE REPORT
============================================================

Write analysis to `docs/dynamic-pricing-analysis.md` (create `docs/` if needed).

Include: Executive Summary, Pricing Architecture Assessment, Elasticity Model Evaluation,
Competitive Positioning Analysis, Promotional Optimization Review, Markdown Strategy
Assessment, Governance and Compliance Audit, Revenue Opportunity Quantification,
Prioritized Recommendations.


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

## Dynamic Pricing Analysis Complete

- Report: `docs/dynamic-pricing-analysis.md`
- Product categories analyzed: [count]
- Elasticity models reviewed: [count]
- Competitive rules assessed: [count]
- Revenue opportunities identified: [estimated value]

### Summary Table
| Area | Status | Priority |
|------|--------|----------|
| Elasticity Modeling | [PASS/WARN/FAIL] | [P1-P4] |
| Competitive Intelligence | [PASS/WARN/FAIL] | [P1-P4] |
| Competitive Rules | [PASS/WARN/FAIL] | [P1-P4] |
| Promotional Optimization | [PASS/WARN/FAIL] | [P1-P4] |
| Markdown Optimization | [PASS/WARN/FAIL] | [P1-P4] |
| Price Image Management | [PASS/WARN/FAIL] | [P1-P4] |
| Governance | [PASS/WARN/FAIL] | [P1-P4] |
| Legal Compliance | [PASS/WARN/FAIL] | [P1-P4] |

NEXT STEPS:

- "Run `/inventory-allocation` to align inventory positions with pricing strategy."
- "Run `/sku-optimization` to rationalize assortment and reduce pricing complexity."
- "Run `/merchandising-analytics` to evaluate cross-sell pricing and basket impact."

DO NOT:

- Do NOT modify any pricing rules, competitive matching logic, or price records.
- Do NOT trigger any price changes or promotional activations.
- Do NOT access or display competitor pricing data outside the analysis report.
- Do NOT assume elasticity models are accurate without checking validation metrics.
- Do NOT skip legal compliance review even for B2B or wholesale pricing systems.


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /dynamic-pricing — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
