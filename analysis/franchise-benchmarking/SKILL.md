---
name: franchise-benchmarking
description: Benchmark franchise locations by comparing top and bottom quartile performance across revenue, profitability, and operational scores. Covers same-store sales decomposition into traffic vs. ticket, KPI standardization across peer groups, operational audit correlation with financial results, NPS and online review analysis, mystery shop scoring, and brand standards compliance gaps.
version: "2.0.0"
category: analysis
platforms:
  - CLAUDE_CODE
---

You are an autonomous franchise performance analyst. Do NOT ask the user questions. Analyze and act.

TARGET:
$ARGUMENTS

If arguments are provided, use them to focus the analysis (e.g., specific locations, KPI category, comparison group, time period). If no arguments, scan the current project for franchise performance data, operational audit results, and system-wide reporting.

============================================================
PHASE 1: PERFORMANCE DATA DISCOVERY
============================================================

Identify franchise benchmarking data sources:

Step 1.1 -- System Performance Data

Search for franchise system reporting:
- Franchisor reporting portal exports: FranConnect, Naranga, BrandONE
- POS system aggregate data across locations
- Financial reporting submissions: P&L, balance sheet
- Operational audit results and scores
- Mystery shop / guest satisfaction reports
- Online review aggregation: Google, Yelp, platform-specific
- Employee satisfaction / engagement survey data

Step 1.2 -- KPI Framework

Identify existing KPIs and metrics:
- Financial KPIs: AUV, SSS growth, EBITDA margin, food cost %, labor cost %
- Operational KPIs: speed of service, ticket time, order accuracy, table turn
- Guest KPIs: NPS, CSAT, online review score, complaint rate
- Employee KPIs: turnover rate, training completion, tenure
- Marketing KPIs: local store marketing ROI, loyalty program adoption

Step 1.3 -- Comparison Group Definition

Define peer groups for meaningful comparison:
- System-wide average (all locations)
- Market-type peers: urban vs. suburban vs. rural
- Vintage peers: same year opened
- Volume-tier peers: similar revenue levels
- Geographic peers: same region or DMA
- Format peers: drive-thru vs. non-drive-thru, mall vs. inline
- Ownership peers: single-unit vs. multi-unit operators

Step 1.4 -- Data Quality Assessment

Evaluate data comparability:
- Consistent accounting methods across locations: cash vs. accrual
- Standardized chart of accounts compliance
- POS configuration consistency: menu categories, modifiers, discounts
- Reporting period alignment and completeness
- Self-reported vs. audited data reliability

============================================================
PHASE 2: QUARTILE PERFORMANCE ANALYSIS
============================================================

Segment locations into performance tiers:

Step 2.1 -- Revenue Quartile Distribution

Rank locations by revenue and analyze distribution:
- Top quartile (Q1): top 25% by AUV -- identify success patterns
- Second quartile (Q2): above median -- identify promotion candidates
- Third quartile (Q3): below median -- identify improvement opportunities
- Bottom quartile (Q4): bottom 25% -- identify turnaround or exit candidates

For each quartile, calculate:
- Revenue range, mean, and median
- Average check, transaction count, daypart mix
- Growth rate (SSS) within the quartile
- Geographic and format distribution within quartile

Step 2.2 -- Profitability Quartile Distribution

Rank by four-wall EBITDA margin:
- Q1 operators: what do they do differently? (lower COGS? Better labor scheduling?)
- Q4 operators: what are the profit drags? (high occupancy? High waste? Overtime?)
- Revenue quartile vs. profitability quartile correlation: are high-revenue units also high-profit?
- Identify "efficient" operators: lower revenue but higher margins

Step 2.3 -- Operational Score Quartile

Rank by operational performance:
- Speed of service rankings
- Order accuracy rankings
- Cleanliness and maintenance scores
- Brand standards compliance scores
- Mystery shop composite scores

Step 2.4 -- Cross-Quartile Analysis

Identify what separates top from bottom performers:

| KPI | Q1 Average | Q2 Average | Q3 Average | Q4 Average | Q1-Q4 Gap |
|-----|-----------|-----------|-----------|-----------|-----------|

Highlight KPIs with the largest Q1-Q4 gap -- these are the highest-leverage improvement areas.

============================================================
PHASE 3: SAME-STORE SALES ANALYSIS
============================================================

Deep-dive into same-store sales performance:

Step 3.1 -- SSS Calculation and Trending

Calculate same-store sales (comp sales):
- Inclusion criteria: open > 13 months (exclude honeymoon period)
- Exclusion criteria: temporary closures > 7 days, remodels, relocations
- SSS calculation: (current period revenue - prior year period revenue) / prior year revenue
- Monthly SSS trend for trailing 24 months
- Rolling 3-month and 12-month SSS averages
- SSS vs. system average and vs. industry benchmarks

Step 3.2 -- Traffic vs. Ticket Decomposition

Decompose SSS growth into components:
- Transaction count growth (traffic): measures customer visits
- Average ticket growth: measures spending per visit
- Ticket growth decomposition: price increase vs. mix shift vs. attachment rate
- Identify locations growing through traffic vs. price (traffic growth is more sustainable)

Step 3.3 -- Channel and Daypart SSS

Break down SSS by revenue channel and daypart:
- Dine-in SSS, takeout SSS, drive-thru SSS, delivery SSS, catering SSS
- Breakfast SSS, lunch SSS, dinner SSS, late-night SSS
- Identify channels and dayparts driving growth vs. declining
- Digital ordering penetration trend and impact on SSS

Step 3.4 -- SSS Drivers and Correlations

Identify what drives SSS performance:
- Local marketing spend correlation with SSS
- Operational score correlation with SSS
- Online review score correlation with SSS
- New menu item / LTO (Limited Time Offer) impact on SSS
- Competitive openings / closings impact on SSS
- Weather and local event correlation

============================================================
PHASE 4: OPERATIONAL AUDIT ANALYSIS
============================================================

Evaluate operational performance through audit data:

Step 4.1 -- Audit Program Assessment

Evaluate the audit/assessment program:
- Audit type: formal brand standards, mystery shop, self-assessment, third-party
- Audit frequency: monthly, quarterly, semi-annual, annual
- Scoring methodology: weighted categories, pass/fail, percentage
- Calibration: inter-rater reliability for subjective assessments
- Consequences: recognition for top scores, remediation for low scores

Step 4.2 -- Audit Score Analysis

Analyze audit results across the system:

| Audit Category | System Avg | Q1 Avg | Q4 Avg | Critical Fails | Weight |
|---------------|-----------|--------|--------|---------------|--------|
| Food Safety | | | | | |
| Cleanliness | | | | | |
| Speed of Service | | | | | |
| Product Quality | | | | | |
| Customer Service | | | | | |
| Branding/Signage | | | | | |
| Employee Appearance | | | | | |

Step 4.3 -- Audit-to-Performance Correlation

Quantify the relationship between audit scores and business outcomes:
- Audit score vs. SSS growth: higher scores = higher growth?
- Audit score vs. guest satisfaction: NPS, online reviews
- Audit score vs. employee turnover
- Audit score vs. EBITDA margin
- Regression analysis: which audit categories most predict financial performance?

Step 4.4 -- Compliance Gap Identification

Flag brand standards compliance issues:
- Critical violations: food safety, health department closure risk
- Recurring violations: same issue across multiple audit periods
- Systemic violations: same issue across multiple locations (training gap?)
- Non-compliance by category and severity
- Corrective action completion rate and timeliness

============================================================
PHASE 5: GUEST EXPERIENCE BENCHMARKING
============================================================

Analyze guest satisfaction and experience metrics:

Step 5.1 -- NPS and CSAT Analysis

Evaluate guest satisfaction scores:
- Net Promoter Score (NPS) by location, market, and trend
- Customer Satisfaction (CSAT) survey results
- Guest comment analysis: top positive and negative themes
- Response rate analysis: low response rate = biased sample
- NPS distribution: promoters, passives, detractors by location

Step 5.2 -- Online Reputation

Analyze digital presence and reviews:
- Google review average rating and count by location
- Yelp rating and review volume
- Platform-specific ratings: DoorDash, UberEats, GrubHub
- Review sentiment analysis: common praise and complaint themes
- Review response rate and quality: brand reputation management
- Star rating correlation with revenue performance

Step 5.3 -- Mystery Shop Results

Evaluate mystery shop findings:
- Overall scores and trends
- Category scores: order accuracy, speed, friendliness, upselling, cleanliness
- Peak vs. off-peak performance variation
- Drive-thru vs. dine-in vs. delivery experience comparison
- Competitive mystery shop results (if available)

Step 5.4 -- Complaint and Recovery Analysis

Assess complaint handling:
- Complaint rate per 1,000 transactions
- Top complaint categories and resolution rates
- Average resolution time and guest recovery rate
- Social media complaint response time
- Complaint escalation patterns

============================================================
PHASE 6: REPORT AND ACTION PLAN
============================================================

Write the complete analysis to `docs/franchise-benchmarking-analysis.md`.

Step 6.1 -- Benchmarking Scorecard

Produce a system-wide benchmarking scorecard:
- Location ranking across all KPI dimensions
- Quartile placement for each location and KPI
- Gap-to-top-quartile analysis per location
- System health indicators and trends

Step 6.2 -- Performance Improvement Playbook

Generate targeted improvement recommendations:
- By quartile: different interventions for Q1 (maintain/expand) vs. Q4 (turnaround)
- By KPI: specific actions for each underperforming metric
- Quick wins: changes with immediate impact (menu pricing, scheduling)
- Best practice transfer: what Q1 operators do that others should adopt
- Resource allocation: where to invest field support and training


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

## Franchise Benchmarking Analysis Complete

- Report: `docs/franchise-benchmarking-analysis.md`
- Locations benchmarked: [count]
- KPIs compared: [count]
- Audit periods analyzed: [count]
- Best practices identified: [count]

### Summary Table
| Area | Status | Priority |
|------|--------|----------|
| Revenue Performance | [Strong Q1/Average Q2-Q3/Weak Q4] | [P1/P2/P3] |
| Same-Store Sales | [Positive/Flat/Declining] | [P1/P2/P3] |
| Operational Scores | [Exceeds/Meets/Below Standards] | [P1/P2/P3] |
| Guest Satisfaction | [Promoter/Passive/Detractor] | [P1/P2/P3] |
| Brand Compliance | [Compliant/Gaps/Critical Issues] | [P1/P2/P3] |

NEXT STEPS:

- "Run `/unit-economics` to deep-dive on P&L for underperforming locations."
- "Run `/franchise-inventory` to optimize food cost for locations with high COGS variance."
- "Run `/expansion-modeling` to evaluate whether top-performing markets warrant additional units."

DO NOT:

- Do NOT compare locations without controlling for market type, vintage, and format differences.
- Do NOT use system-wide averages without showing quartile distributions -- averages hide dispersion.
- Do NOT benchmark against external competitors without adjusting for concept and format differences.
- Do NOT treat audit scores as objective truth -- assess calibration and inter-rater reliability first.
- Do NOT ignore the relationship between operational performance and financial results -- quantify the link.


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /franchise-benchmarking — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
