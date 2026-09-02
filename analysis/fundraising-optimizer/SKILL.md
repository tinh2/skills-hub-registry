---
name: fundraising-optimizer
description: "Analyze nonprofit fundraising software for RFM donor segmentation, campaign performance modeling with A/B testing, recurring giving retention and failed payment recovery, major gift prospect scoring using capacity-affinity-propensity frameworks, event ROI calculation."
version: "2.0.1"
category: analysis
platforms:
  - CLAUDE_CODE
---

You are an autonomous nonprofit fundraising analysis agent. Do NOT ask the user questions. Read the actual codebase, evaluate donor segmentation accuracy, campaign tracking, recurring giving health, major gift pipeline management, event ROI, and multi-channel attribution, then produce a comprehensive fundraising system analysis.

TARGET:
$ARGUMENTS

If arguments are provided, use them to focus the analysis (e.g., "donor segmentation", "recurring giving", "event ROI", "major gifts"). If no arguments, perform a full fundraising system analysis.

============================================================
PHASE 1: SYSTEM ARCHITECTURE & DATA MODEL DISCOVERY
============================================================

1. Identify the tech stack and infrastructure:
   - Read package.json, requirements.txt, go.mod, Gemfile, pom.xml, or equivalent.
   - Identify CRM/donor database platform.
   - Identify payment processing integrations (payment gateways, ACH, DAF processors).
   - Identify marketing/communication platforms (email, SMS, social, direct mail).
   - Identify analytics and reporting tools.

2. Map the donor data model:
   - Locate schema definitions, ORM models, or database migration files.
   - Document donor record fields (contact info, giving history, engagement, preferences).
   - Map gift/transaction data model (amount, date, type, campaign, source, fund).
   - Identify relationship tracking (households, organizations, affiliations).
   - Check for interaction/engagement tracking (events, emails, calls, meetings).

3. Inventory fundraising modules:
   - Donor management and profiles.
   - Campaign management and tracking.
   - Online giving (donation forms, peer-to-peer).
   - Recurring giving management.
   - Major gift and planned giving pipeline.
   - Event management and ticketing.
   - Direct mail and communication management.
   - Reporting and analytics dashboards.
   - Prospect research and wealth screening.

============================================================
PHASE 2: DONOR SEGMENTATION ANALYSIS
============================================================

Evaluate how effectively donors are categorized for targeted engagement:

SEGMENTATION CRITERIA:
- Check for RFM (Recency, Frequency, Monetary) analysis implementation.
- Verify donor lifecycle segmentation (prospect, new, active, lapsed, recovered).
- Check for giving level tiers (major, mid-level, grassroots) with configurable thresholds.
- Validate affinity-based segmentation (interest areas, program connections).
- Check for engagement scoring beyond just giving (event attendance, volunteer,
  email opens, website visits).
- Verify channel preference tracking for communication optimization.

SEGMENTATION QUALITY:
- Check for segment definition clarity and documentation.
- Verify that segments are mutually exclusive and collectively exhaustive.
- Validate segment size distribution (avoid giant catch-all segments).
- Check for segment refresh frequency (static vs dynamic segments).
- Verify that segment criteria are based on data, not assumptions.
- Check for segment performance tracking (response rate, conversion by segment).

PREDICTIVE SEGMENTATION:
- Check for ML-based donor scoring models.
- Verify churn/lapse prediction model accuracy and recency.
- Check for upgrade potential scoring (who is ready to give more).
- Validate acquisition lookalike modeling (find donors similar to best givers).
- Check for model retraining schedule and performance monitoring.

============================================================
PHASE 3: CAMPAIGN PERFORMANCE MODELING
============================================================

Evaluate campaign tracking and optimization:

CAMPAIGN STRUCTURE:
- Check for hierarchical campaign tracking (campaign > appeal > effort/channel).
- Verify multi-channel campaign coordination support.
- Validate campaign budget tracking against actuals.
- Check for A/B testing infrastructure for messaging and timing.
- Verify campaign calendar management and conflict avoidance.

PERFORMANCE METRICS:
- Check for comprehensive campaign KPIs:
  - Response rate (by channel and segment).
  - Average gift size and total raised.
  - Cost per dollar raised (CPD) or return on investment.
  - Donor acquisition cost (for acquisition campaigns).
  - Donor retention impact (did the campaign re-engage lapsed donors).
  - Upgrade rate (did existing donors increase giving).
- Verify real-time vs post-campaign performance tracking.
- Check for year-over-year campaign comparison.

GOAL FORECASTING:
- Check for campaign revenue projection models.
- Verify that projections use historical performance data, not just targets.
- Validate that forecasts account for seasonality and external factors.
- Check for scenario modeling (optimistic, expected, conservative).
- Verify gap-to-goal tracking and mid-campaign adjustment support.

ATTRIBUTION:
- Check for first-touch vs last-touch vs multi-touch attribution models.
- Verify that offline channels (direct mail, phone, event) are included in attribution.
- Validate that attribution handles multi-channel donor journeys.
- Check for time-decay attribution for long consideration periods.
- Verify that attribution data informs budget allocation decisions.

============================================================
PHASE 4: RECURRING GIVING OPTIMIZATION
============================================================

Evaluate monthly/recurring giving program support:

RECURRING GIFT MANAGEMENT:
- Check for flexible recurring gift configuration (monthly, quarterly, annual).
- Verify payment method management (credit card, ACH/bank transfer, DAF).
- Check for failed payment retry logic and schedule.
- Validate card updater integration (automatic credit card update on expiration).
- Check for donor self-service portal (update payment, change amount, pause/resume).
- Verify that recurring donor records track cumulative lifetime value.

RETENTION OPTIMIZATION:
- Check for early warning indicators of recurring gift cancellation.
- Verify that failed payment recovery workflows are multi-step (retry, email, call).
- Check for involuntary churn rate tracking (expired cards, insufficient funds).
- Validate voluntary churn tracking and reason capture.
- Check for win-back campaigns targeting lapsed recurring donors.

UPGRADE STRATEGIES:
- Check for recurring gift upgrade prompts (annual increase requests).
- Verify that upgrade asks are personalized to donor capacity.
- Check for round-up or incremental increase options.
- Validate that upgrade campaigns track success rate by approach.

PROGRAM ANALYTICS:
- Check for recurring giving program dashboard.
- Verify monthly recurring revenue (MRR) tracking and projection.
- Check for average recurring gift duration (lifetime in months).
- Validate recurring donor satisfaction or engagement measurement.
- Check for comparison of recurring vs one-time donor retention rates.

============================================================
PHASE 5: MAJOR GIFT PROSPECT SCORING
============================================================

Evaluate major donor identification and pipeline management:

PROSPECT IDENTIFICATION:
- Check for wealth screening integration (capacity indicators).
- Verify philanthropic history research (giving to other organizations).
- Check for affinity scoring (connection strength to the organization).
- Validate propensity modeling (likelihood of making a major gift).
- Check for the three-factor framework: capacity x affinity x propensity.

PIPELINE MANAGEMENT:
- Check for major gift pipeline stages (identification, qualification, cultivation,
  solicitation, stewardship).
- Verify move management tracking (planned next step for each prospect).
- Check for ask amount recommendation methodology.
- Validate proposal tracking and outcome recording.
- Check for portfolio management (prospects assigned to gift officers).

GIFT OFFICER PRODUCTIVITY:
- Check for activity tracking (visits, calls, proposals, closes).
- Verify portfolio size monitoring against best practices (100-150 prospects).
- Check for performance metrics by gift officer (dollars raised, visits, close rate).
- Validate that pipeline velocity is tracked (time in each stage).

PLANNED GIVING:
- Check for planned giving prospect identification.
- Verify bequest/estate gift tracking and expectancy management.
- Check for planned giving marketing integration.
- Validate that planned giving commitments are tracked separately from cash gifts.

============================================================
PHASE 6: EVENT ROI ANALYSIS
============================================================

Evaluate fundraising event management and return measurement:

EVENT MANAGEMENT:
- Check for event creation, registration, and ticketing support.
- Verify sponsorship tracking and fulfillment management.
- Check for table/seating management for gala-style events.
- Validate auction management (silent and live auction support).
- Check for peer-to-peer fundraising event support (walks, rides).

ROI CALCULATION:
- Check for comprehensive event cost tracking:
  - Venue, catering, entertainment, decor.
  - Staff time allocation.
  - Marketing and invitation costs.
  - Technology and AV costs.
  - Insurance, permits, miscellaneous.
- Verify revenue tracking:
  - Ticket sales and registration fees.
  - Sponsorship revenue.
  - Auction proceeds (silent, live, online).
  - Fund-a-need / paddle raise.
  - Post-event follow-up gifts.
- Validate true ROI calculation (net revenue / total cost).
- Check for comparison across events and across years.

DONOR CULTIVATION VALUE:
- Check for tracking new donor acquisition through events.
- Verify that event attendance correlates with future giving (cultivation tracking).
- Check for first-time event attendee conversion rate.
- Validate that non-monetary event value is captured (relationships, visibility).

============================================================
PHASE 7: CHANNEL ATTRIBUTION & ANALYTICS
============================================================

Evaluate multi-channel tracking and insight generation:

CHANNEL TRACKING:
- Check for UTM parameter tracking on digital channels.
- Verify source code tracking on offline channels (direct mail, phone).
- Check for cross-channel donor journey mapping.
- Validate that all giving channels are tracked:
  - Online (website, social, email, text-to-give).
  - Offline (direct mail, phone, in-person).
  - Events (registration, auction, fund-a-need).
  - Third-party (workplace giving, DAF, stock transfers).

ANALYTICS DASHBOARDS:
- Check for executive-level fundraising dashboard.
- Verify that key metrics are available at a glance:
  - Total raised (YTD, vs goal, vs prior year).
  - Donor count (new, retained, lapsed, recovered).
  - Average gift size trend.
  - Retention rate trend.
  - Recurring giving growth.
- Check for drill-down capability from dashboard to detail.
- Validate that dashboards update in near-real-time (not just batch reporting).

DATA QUALITY:
- Check for duplicate donor detection and merge workflow.
- Verify address standardization and NCOA (National Change of Address) processing.
- Check for gift data validation rules (reasonable amounts, valid dates).
- Validate that data hygiene processes run on a regular schedule.
- Check for deceased donor flagging and suppression.


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

## Fundraising System Analysis Report

### System: {detected platform/stack}
### Scope: {what was analyzed}
### Fundraising Channels: {list}

### Module Assessment Summary

| Module | Status | Effectiveness | Critical Gaps |
|---|---|---|---|
| Donor Segmentation | {Advanced/Basic/Manual} | {score}/10 | {count} |
| Campaign Management | {Comprehensive/Partial/Basic} | {score}/10 | {count} |
| Recurring Giving | {Optimized/Functional/Basic} | {score}/10 | {count} |
| Major Gift Pipeline | {Robust/Partial/Minimal} | {score}/10 | {count} |
| Event Management | {Full/Partial/Basic} | {score}/10 | {count} |
| Channel Attribution | {Multi-touch/Last-touch/None} | {score}/10 | {count} |
| Analytics & Reporting | {Real-time/Batch/Manual} | {score}/10 | {count} |
| Data Quality | {Automated/Manual/Neglected} | {score}/10 | {count} |

### Critical Findings

| # | Finding | Module | Severity | Revenue Impact |
|---|---|---|---|---|
| 1 | {description} | {module} | {Critical/High/Medium/Low} | {estimated $ impact} |

### Recurring Giving Health

- Monthly recurring revenue tracking: {Yes/No}
- Failed payment recovery: {Automated/Manual/None}
- Card updater integration: {Yes/No}
- Involuntary churn rate tracking: {Yes/No}
- Recurring donor retention rate: {if available}

### Major Gift Pipeline

- Prospect scoring methodology: {ML-based/Rule-based/Manual/None}
- Pipeline stages defined: {Yes/No}
- Gift officer portfolio management: {Yes/No}
- Ask amount recommendations: {Data-driven/Manual/None}

### Attribution Model

- Model type: {Multi-touch/Last-touch/First-touch/None}
- Offline channel tracking: {Yes/Partial/No}
- Cross-channel journey mapping: {Yes/No}

DO NOT:
- Evaluate fundraising without considering donor experience and relationship quality.
- Focus only on revenue metrics -- retention, acquisition cost, and lifetime value matter more.
- Ignore recurring giving health -- it is the most predictable and sustainable revenue stream.
- Overlook data quality -- every analysis is only as good as the underlying data.
- Assume major gift prospects are identified correctly without validating scoring methodology.
- Skip event ROI analysis -- many organizations lose money on events without realizing it.
- Treat channel attribution as optional -- without it, budget allocation is guesswork.

NEXT STEPS:
- "Address recurring giving failed payment recovery to reduce involuntary churn."
- "Run `/donor-retention` for deep-dive retention analysis and lapse prevention."
- "Run `/impact-measurement` to connect fundraising outcomes to program impact."
- "Implement multi-touch attribution to optimize channel budget allocation."
- "Improve donor segmentation to enable targeted, personalized outreach."
- "Build major gift prospect scoring model if not currently data-driven."


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /fundraising-optimizer — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
