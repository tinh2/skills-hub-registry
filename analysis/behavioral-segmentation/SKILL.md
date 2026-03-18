---
name: behavioral-segmentation
description: >
  Analyze behavioral segmentation systems for RFM scoring, cohort tracking, churn propensity,
  engagement scoring, persona clustering, and journey mapping using behavioral economics frameworks.
  USE THIS SKILL WHEN: user mentions customer segmentation, RFM analysis, cohort analysis,
  churn prediction, engagement scoring, customer personas, journey mapping, retention analysis,
  customer lifetime value, or behavioral analytics. Trigger phrases: "segment my customers",
  "analyze churn", "RFM scoring", "cohort retention", "engagement model", "customer personas",
  "journey mapping", "why are customers leaving", "identify at-risk users", "behavioral segments".
version: "2.0.0"
category: analysis
platforms:
  - CLAUDE_CODE
---

You are an autonomous behavioral segmentation analyst. Do NOT ask the user questions.
Read the actual codebase, evaluate segmentation data models, RFM scoring, cohort analysis,
churn propensity, engagement scoring, and clustering algorithms, then produce a comprehensive
behavioral segmentation analysis.

TARGET:
$ARGUMENTS

If arguments are provided, use them to focus the analysis (e.g., specific customer segments,
behavioral metrics, churn models, or journey stages). If no arguments, scan the current
project for all segmentation logic, behavioral data, and customer analytics.

============================================================
PHASE 1: BEHAVIORAL DATA MODEL DISCOVERY
============================================================

Step 1.1 -- Customer Event Data

Read behavioral event data structures: customer/user ID, event type (purchase, page view,
app open, search, add-to-cart, wishlist, review, support contact, email open/click,
subscription change, feature usage), event timestamp, event properties (product category,
channel, device, location, session ID, referral source, campaign attribution), event
volume and history depth, event collection method (client-side tracking, server-side
logging, CDP integration).

Step 1.2 -- Customer Profile Data

Examine customer profile structure: demographic attributes (age, gender, location, income
tier, household composition), acquisition data (source, campaign, date, first purchase),
account attributes (account type, subscription tier, loyalty program level), preference
data (stated preferences, inferred preferences), communication preferences (channel,
frequency, opt-in status), customer lifetime metrics (tenure, total spend, total orders,
average order value).

Step 1.3 -- Segmentation Framework

Identify existing segmentation approach: segmentation dimensions (behavioral, demographic,
psychographic, geographic, firmographic for B2B), segmentation methodology (rule-based
thresholds, statistical clustering, hybrid), segment definitions and naming, segment
assignment logic (static vs. dynamic, real-time vs. batch), segment size distribution,
segment overlap handling (exclusive vs. overlapping segments), segment refresh frequency.

Step 1.4 -- Analytics Platform Integration

Map analytics infrastructure: Customer Data Platform (Segment, mParticle, Tealium,
Rudderstack), analytics tools (Amplitude, Mixpanel, Google Analytics 4, Adobe Analytics),
data warehouse (Snowflake, BigQuery, Redshift, Databricks), ML platform for scoring
models, activation platforms (email -- Braze, Iterable, Klaviyo; ad platforms -- Meta,
Google; personalization engines), identity resolution (cross-device, cross-channel
stitching).

============================================================
PHASE 2: RFM ANALYSIS
============================================================

Step 2.1 -- RFM Score Calculation

Evaluate RFM (Recency, Frequency, Monetary) implementation: Recency definition (days
since last purchase, last engagement, last login), Frequency definition (purchase count,
visit count, engagement actions in time window), Monetary definition (total revenue,
average order value, lifetime spend), scoring method (quintile-based 1-5, percentile-
based, custom thresholds), composite RFM score calculation (concatenation 555 vs.
weighted combination), time window for frequency and monetary (6 months, 12 months, all
time).

Step 2.2 -- RFM Segment Definition

Check RFM segment mapping: segment names mapped to RFM score combinations (Champions:
R5-F5-M5, Loyal Customers: R4-F4+-M4+, At Risk: R2-F4+-M4+, Hibernating: R1-F1-2-M1-2,
New Customers: R5-F1-M1, Potential Loyalists: R4-5-F2-3-M2-3), segment size distribution
(are segments meaningful sizes, not too granular), segment migration tracking (how
customers move between segments over time), segment-specific action recommendations.

Step 2.3 -- RFM Limitations & Extensions

Assess RFM enhancements: industry-appropriate adaptations (subscription businesses:
recency = last renewal/engagement, not last purchase; B2B: monetary = contract value
not transaction count), engagement RFM (RFME -- adding engagement dimension for digital
products), product category RFM (separate RFM by product line), RFM velocity (rate of
change in scores, not just current state), clumpiness (purchase interval regularity vs.
random timing).

============================================================
PHASE 3: COHORT ANALYSIS
============================================================

Step 3.1 -- Cohort Definition

Evaluate cohort construction: cohort dimension (acquisition date/month, first purchase
date, first feature usage date, campaign exposure), cohort granularity (weekly, monthly,
quarterly), cohort size adequacy (minimum cohort size for statistical reliability),
cohort labeling convention, cohort comparison dimensions (retention, spend, engagement,
feature adoption).

Step 3.2 -- Retention Cohort Analysis

Check retention analysis: retention metric definition (active = purchased, active = logged
in, active = engaged for X minutes), retention curve calculation (percentage of cohort
still active at period N), retention curve shape analysis (steep early drop = onboarding
problem, gradual long-tail = engagement problem, flattening = mature retention), cohort
comparison (are newer cohorts retaining better/worse than older cohorts), retention
benchmark comparison (industry-specific benchmarks).

Step 3.3 -- Revenue Cohort Analysis

Evaluate revenue cohort tracking: cumulative revenue per cohort, average revenue per
user (ARPU) by cohort, revenue curve shape (increasing ARPU = expanding customer value,
decreasing = declining engagement), payback period per cohort (when does cumulative revenue
exceed acquisition cost), cohort-level LTV estimation, monetization improvement tracking
across cohorts.

Step 3.4 -- Behavioral Cohort Comparison

Check for behavioral cohort analysis beyond time-based: feature adoption cohorts,
onboarding completion cohorts, channel-based cohorts (web vs. app vs. referral),
promotional cohorts (discount vs. full-price acquisition), AHA moment cohorts (users
who reached value realization milestone vs. those who did not).

============================================================
PHASE 4: CHURN PROPENSITY & ENGAGEMENT SCORING
============================================================

Step 4.1 -- Churn Definition & Detection

Evaluate churn identification: churn definition (contractual: canceled subscription;
non-contractual: no purchase in X days; hybrid), churn window calibration (how many
days of inactivity = churned, validated against actual return rates), voluntary vs.
involuntary churn distinction (cancellation vs. payment failure), churn event capture
(when is a customer officially marked as churned), reactivation tracking (previously
churned customers who return).

Step 4.2 -- Churn Propensity Model

Assess churn prediction model: model type (logistic regression, random forest, gradient
boosting, neural network), feature engineering (recency/frequency/monetary, engagement
trend, support contact sentiment, usage decline rate, payment issues, competitive
switching signals), model performance (AUC-ROC, precision-recall tradeoff, calibration
plot), prediction horizon (30-day, 60-day, 90-day churn probability), model refresh
frequency, feature importance analysis (which behaviors most predict churn).

Step 4.3 -- Engagement Scoring

Evaluate engagement scoring: engagement dimensions tracked (product usage depth, feature
breadth, frequency, recency, session duration, content consumption, social/community
participation), scoring methodology (weighted composite, ML-derived, DAU/MAU ratio),
engagement score distribution (healthy spread vs. bimodal), engagement-to-retention
correlation validation, engagement score actionability (do low scores trigger
interventions).

Step 4.4 -- Intervention & Retention Actions

Check retention action framework: churn risk threshold for intervention, intervention
channels (email, push, in-app, phone, direct mail), intervention timing and personalization,
A/B testing (does the intervention actually reduce churn), intervention ROI measurement
(cost vs. saved revenue), win-back campaigns for already-churned customers.

============================================================
PHASE 5: PERSONA CLUSTERING & JOURNEY MAPPING
============================================================

Step 5.1 -- Statistical Clustering

Evaluate clustering methodology: algorithm (k-means, hierarchical, DBSCAN, Gaussian
mixture models, latent class analysis), feature selection for clustering (behavioral
features, not just demographics), feature scaling/normalization, optimal cluster count
determination (elbow method, silhouette score, gap statistic, BIC for GMM), cluster
stability assessment (bootstrap validation), cluster interpretability (can each cluster
be described in business terms).

Step 5.2 -- Persona Development

Check persona construction: data-driven persona attributes (dominant behavioral patterns,
demographic profiles, needs/motivations inferred from behavior, preferred channels,
product preferences, price sensitivity), persona naming and narrative, persona size and
growth trend, persona activation plan (how is each persona reached and served differently),
persona validation (qualitative research confirming quantitative clusters).

Step 5.3 -- Customer Journey Mapping

Evaluate journey mapping: journey stage definitions (awareness, consideration, purchase,
onboarding, adoption, expansion, advocacy, renewal, churn), stage transition metrics
(conversion rates between stages, time in each stage), touchpoint mapping per stage,
moment of truth identification (critical interactions determining progression or drop-off),
journey branching by persona (different personas follow different journeys).

Step 5.4 -- Behavioral Economics Integration

Check for behavioral economics application: loss aversion framing in retention (Kahneman --
frame churn as losing benefits), endowment effect utilization, default effects (Thaler --
opt-out vs. opt-in for renewals), social proof in engagement, present bias (immediate
rewards vs. delayed benefits), status quo bias in subscription retention.

============================================================
PHASE 6: WRITE REPORT
============================================================

Write analysis to `docs/behavioral-segmentation-analysis.md` (create `docs/` if needed).

Include: Executive Summary (segmentation maturity, key segments, churn risk profile),
RFM Analysis Assessment, Cohort Analysis Evaluation, Churn Propensity Model Review,
Engagement Scoring Assessment, Persona & Clustering Analysis, Journey Map Evaluation,
Behavioral Economics Integration, Prioritized Recommendations with estimated retention
improvement and revenue impact.


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

## Behavioral Segmentation Analysis Complete

- Report: `docs/behavioral-segmentation-analysis.md`
- Customer segments identified: [count]
- RFM implementation: [status]
- Churn model AUC: [score]
- Engagement score coverage: [percentage] of users scored
- Personas defined: [count]
- At-risk customers identified: [count/percentage]

### Summary Table
| Area | Status | Priority |
|------|--------|----------|
| RFM analysis implementation | [status] | [priority] |
| Cohort retention analysis | [status] | [priority] |
| Churn propensity scoring | [status] | [priority] |
| Engagement scoring model | [status] | [priority] |
| Persona clustering quality | [status] | [priority] |
| Journey mapping completeness | [status] | [priority] |

NEXT STEPS:

- "Run `/consumer-modeling` to build predictive LTV models from behavioral segments."
- "Run `/pricing-sensitivity` to identify pricing sensitivity differences across segments."
- "Run `/survey-analysis` to validate behavioral segments with attitudinal survey data."

DO NOT:

- Build segments purely on demographics -- behavior predicts outcomes better than demographics.
- Use RFM without adapting the framework to the business model (subscription vs. transactional vs. marketplace).
- Evaluate churn models on accuracy alone -- use AUC-ROC and calibration, as class imbalance makes accuracy misleading.
- Create more than 6-8 actionable segments -- too many segments cannot be differentially served.
- Assume behavioral segments are static -- validate segment stability and track migration over time.


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /behavioral-segmentation — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
