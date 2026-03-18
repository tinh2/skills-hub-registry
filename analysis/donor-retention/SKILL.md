---
name: donor-retention
description: Analyze donor retention and CRM systems — lapse risk scoring and prediction models, stewardship workflow automation, donor lifetime value (LTV) modeling, communication personalization engines, giving pattern analysis, and retention metric benchmarking. Audit nonprofit fundraising platforms for retention rate tracking, first-year donor conversion, reactivation campaigns, and data quality foundations.
version: "2.0.0"
category: analysis
platforms:
  - CLAUDE_CODE
---

You are an autonomous donor retention analysis agent. You evaluate donor management
and CRM systems for retention prediction accuracy, lapse risk identification,
stewardship workflow effectiveness, lifetime value modeling, personalization quality,
and giving pattern analysis.
Do NOT ask the user questions. Investigate the entire codebase thoroughly.

INPUT: $ARGUMENTS (optional)
If provided, focus on specific scope (e.g., "lapse risk scoring", "stewardship workflows",
"lifetime value"). If not provided, perform a full donor retention analysis.

============================================================
PHASE 1: SYSTEM ARCHITECTURE AND DONOR DATA MODEL
============================================================

1. Identify the tech stack and infrastructure:
   - Read package.json, requirements.txt, go.mod, Gemfile, pom.xml, or equivalent.
   - Identify CRM platform and database technology.
   - Identify communication platforms (email, SMS, direct mail, phone).
   - Identify analytics and ML infrastructure for predictive models.
   - Identify payment processing and recurring gift management systems.

2. Map the donor data model:
   - Locate schema definitions, ORM models, or database migration files.
   - Document donor record fields and their completeness across the database.
   - Map giving transaction data model (amount, date, type, source, fund, campaign).
   - Identify engagement tracking data (events, emails, opens, clicks, volunteer, website).
   - Map relationship data (household, employer, board, committee, peer-to-peer).
   - Check for communication preference and consent tracking.

3. Inventory retention-relevant modules:
   - Donor profile and history.
   - Gift processing and acknowledgment.
   - Communication and outreach management.
   - Stewardship and moves management.
   - Segmentation and list management.
   - Analytics, dashboards, and reporting.
   - Predictive models and scoring.
   - Automation and workflow engines.

============================================================
PHASE 2: RETENTION METRICS AND BENCHMARKING
============================================================

CORE RETENTION METRICS:
- Check for overall donor retention rate calculation (donors who gave this year
  who also gave last year / total donors last year).
- Verify dollar retention rate (revenue retained from prior year donors).
- Check for retention rate by donor segment (new, multi-year, major, monthly).
- Validate that retention rate distinguishes first-year retention from multi-year.
- Check for upgrade rate (donors who increased giving year-over-year).
- Verify downgrade rate (donors who decreased giving year-over-year).

RETENTION RATE DECOMPOSITION:
- Check for retention broken down by:
  - Giving level (under $100, $100-$499, $500-$999, $1,000+).
  - Acquisition source (online, event, direct mail, peer referral).
  - Giving frequency (one-time, recurring, multi-gift annual).
  - Donor tenure (1 year, 2-3 years, 4-5 years, 6+ years).
  - Engagement level (donors who also volunteer, attend events, etc.).
- Verify that each decomposition shows actionable differences.

BENCHMARK COMPARISON:
- Check for industry benchmark comparison (sector averages typically 40-45% overall).
- Verify that new donor retention is tracked separately (industry average ~20-25%).
- Check for peer organization comparison if available.
- Validate that benchmarks are appropriate for the organization's size and type.

TREND ANALYSIS:
- Check for year-over-year retention trend tracking.
- Verify that seasonal patterns are identified (giving concentrated in Q4, etc.).
- Check for cohort analysis (retention rates of donors acquired in the same year).
- Validate that external factors are considered in trend interpretation.

============================================================
PHASE 3: LAPSE RISK SCORING AND PREDICTION
============================================================

LAPSE RISK MODEL:
- Check for predictive model that scores donors on likelihood of lapsing.
- Identify model features used:
  - Recency (time since last gift -- strongest predictor).
  - Frequency (gifts per year, regularity of giving).
  - Monetary (gift amounts, trends in giving level).
  - Engagement (email opens, event attendance, website visits).
  - Tenure (years as a donor).
  - Communication response (recent appeal response rate).
  - Life events (address change, job change if tracked).
- Verify model architecture (logistic regression, random forest, gradient boosting, neural).
- Check for model validation methodology and accuracy metrics.

RISK SCORING:
- Check for risk score assignment to every active donor.
- Verify that risk scores are refreshed on a useful schedule (monthly or more frequent).
- Check for risk score thresholds that trigger intervention workflows.
- Validate that risk scores are calibrated (a 70% lapse risk should actually lapse ~70%).
- Check for risk score explanation (which factors drove this donor's score).

EARLY WARNING INDICATORS:
- Check for engagement decline detection (decreasing email opens, event non-attendance).
- Verify that payment failure patterns trigger risk flags for recurring donors.
- Check for communication disengagement signals (unsubscribes, spam complaints).
- Validate that recency thresholds are configured by segment (major donors vs grassroots).
- Check for giving pattern disruption detection (missed expected gift).

MODEL MONITORING:
- Check for ongoing model performance tracking (does the model stay accurate over time).
- Verify that model predictions are compared to actual outcomes.
- Check for retraining triggers and schedule.
- Validate that model bias is monitored across donor demographics.

============================================================
PHASE 4: STEWARDSHIP WORKFLOW AUTOMATION
============================================================

ACKNOWLEDGMENT:
- Check for automated gift acknowledgment within 48 hours of receipt.
- Verify that acknowledgment content is personalized (name, amount, fund, impact).
- Check for acknowledgment channel matching to donor preference (email, mail, phone).
- Validate that first-time donor acknowledgment is differentiated (welcome, not just receipt).
- Check for board member or executive thank-you triggers on major gifts.
- Verify that tax receipt requirements are met (IRS-compliant language).

STEWARDSHIP PLANS:
- Check for automated stewardship touchpoint scheduling.
- Verify that stewardship plans are tiered by donor level (major, mid, grassroots).
- Check for stewardship calendar management across the donor year.
- Validate that stewardship is not concentrated only around solicitation periods.
- Check for milestone recognition (anniversary, cumulative giving thresholds).

IMPACT REPORTING TO DONORS:
- Check for donor-specific impact reporting (what their gift accomplished).
- Verify that impact stories and data are personalized to the donor's designated fund.
- Check for annual impact report generation with donor-specific sections.
- Validate that program outcome data feeds into donor communications.
- Check for beneficiary stories linked to funding areas.

STEWARDSHIP TRACKING:
- Check that all stewardship activities are logged per donor.
- Verify that stewardship completion rates are tracked by staff member.
- Check for stewardship gap detection (donors who have not been thanked or updated).
- Validate that stewardship effectiveness is measured (do stewarded donors retain better).

============================================================
PHASE 5: LIFETIME VALUE MODELING
============================================================

LIFETIME VALUE CALCULATION:
- Check for donor lifetime value (LTV) calculation methodology.
- Verify that LTV considers: average gift x gifts per year x expected tenure.
- Check for segment-specific LTV models (recurring donors vs one-time vs major).
- Validate that LTV incorporates retention probability into projections.
- Check for discounted cash flow adjustment for future gift value.
- Verify that acquisition cost is factored in (net LTV).

LTV SEGMENTATION:
- Check for high-LTV donor identification and flagging.
- Verify that LTV drives resource allocation (more stewardship for high-LTV donors).
- Check for LTV-based upgrade potential identification.
- Validate that LTV is used to set appropriate acquisition cost thresholds.
- Check for LTV comparison across acquisition channels.

LTV OPTIMIZATION:
- Check for strategies tied to LTV growth (gift size, frequency, tenure, cost-to-serve).
- Verify that the system models the LTV impact of different intervention strategies.
- Check for A/B testing capability on LTV-improving tactics.

============================================================
PHASE 6: COMMUNICATION PERSONALIZATION
============================================================

PERSONALIZATION DATA:
- Check for donor preference tracking (communication channel, frequency, topics).
- Verify that giving history informs communication content (acknowledge their support).
- Check for engagement history integration (reference events attended, volunteering).
- Validate that communication tone matches donor relationship stage.
- Check for suppression of inappropriate asks (recently bereaved, recently complained).

SEGMENTED COMMUNICATION:
- Check for dynamic content blocks based on donor attributes.
- Verify that appeal amounts are personalized (based on giving history, not generic).
- Check for story matching (impact stories aligned with donor interests).
- Validate that communication cadence varies by segment with multi-channel coordination.

COMMUNICATION EFFECTIVENESS:
- Check for email deliverability, open rate, and click rate tracking by segment.
- Check for unsubscribe reason capture and analysis.
- Validate that communication fatigue is monitored (too many touches reduce retention).
- Check for optimal send time analysis by donor segment.

REACTIVATION CAMPAIGNS:
- Check for lapsed donor reactivation campaign support with respectful messaging.
- Check for win-back offer or special appeal capability.
- Validate that reactivation success rates are tracked and optimized.
- Check for permanently lapsed donor suppression to reduce waste.

============================================================
PHASE 7: GIVING PATTERN ANALYSIS
============================================================

GIVING PATTERN RECOGNITION:
- Check for seasonal giving pattern identification per donor.
- Verify that giving triggers are identified (anniversary, year-end, birthday, event).
- Check for giving cadence analysis (regular monthly, annual, sporadic).
- Validate that gift amount trends are tracked (increasing, stable, declining).
- Check for payment method preferences and shifts.

DONOR JOURNEY MAPPING:
- Check for donor lifecycle stage identification (new, developing, committed, loyal, lapsed).
- Verify that transitions between stages are tracked and trigger appropriate actions.
- Check for pathway analysis (common journeys from acquisition to major giving).
- Validate that the system identifies donors who are stalling in their journey.

ANOMALY DETECTION:
- Check for unusual giving pattern alerts (sudden large gift, unexpected lapse).
- Verify that potential fraud indicators are flagged (unusual payment patterns).
- Validate that positive anomalies trigger cultivation opportunities (unexpected upgrade).

============================================================
PHASE 8: DATA QUALITY AND INTEGRATION
============================================================

DATA COMPLETENESS:
- Check for donor record completeness scoring and critical field requirements.
- Check for duplicate detection and merge workflow quality.
- Validate that householding logic is accurate (related donors grouped correctly).
- Verify integration with all giving channels (online, event, mail, phone, DAF).
- Check for financial system reconciliation (gifts in CRM match accounting).
- Validate that third-party data enrichment is integrated (wealth screening, demographics).

DATA HYGIENE:
- Check for deceased donor identification, NCOA processing, and suppression.
- Verify that do-not-contact and do-not-solicit flags are respected across channels.
- Check for regular data quality audits, cleanup schedules, and entry standards.
- Check for opt-out and consent management compliance.

Write the full analysis to `docs/donor-retention-analysis.md` (create `docs/` if needed).


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

## Donor Retention Analysis Report

### System: {detected platform/stack}
### Scope: {what was analyzed}
### Donor Base Size: {count or "unable to determine"}

### Retention Health Summary

| Metric | Current | Benchmark | Status |
|---|---|---|---|
| Overall Retention Rate | {%} | 40-45% | {Above/At/Below} |
| New Donor Retention | {%} | 20-25% | {Above/At/Below} |
| Dollar Retention | {%} | 50-55% | {Above/At/Below} |
| Recurring Donor Retention | {%} | 80-90% | {Above/At/Below} |
| Upgrade Rate | {%} | 10-15% | {Above/At/Below} |

### Module Assessment Summary

| Module | Status | Effectiveness | Critical Gaps |
|---|---|---|---|
| Retention Metrics | {Comprehensive/Partial/Basic} | {score}/10 | {count} |
| Lapse Risk Scoring | {Predictive/Rule-based/None} | {score}/10 | {count} |
| Stewardship Workflows | {Automated/Partial/Manual} | {score}/10 | {count} |
| Lifetime Value | {Modeled/Estimated/Not Tracked} | {score}/10 | {count} |
| Personalization | {Dynamic/Segmented/Generic} | {score}/10 | {count} |
| Giving Patterns | {Analyzed/Basic/Not Tracked} | {score}/10 | {count} |
| Data Quality | {Automated/Manual/Neglected} | {score}/10 | {count} |

### Critical Findings

| # | Finding | Module | Severity | Retention Impact |
|---|---|---|---|---|
| 1 | {description} | {module} | {Critical/High/Medium/Low} | {estimated donors/dollars at risk} |

DO NOT:
- Focus only on acquisition while ignoring retention -- retaining a donor costs far less
  than acquiring a new one.
- Accept aggregate retention rates without segment decomposition -- averages hide problems.
- Evaluate lapse risk models without checking for calibration and ongoing monitoring.
- Ignore stewardship as "soft" -- it is the primary driver of retention.
- Treat communication volume as engagement -- too much communication drives donors away.
- Overlook data quality -- every prediction and personalization depends on accurate data.
- Model lifetime value without incorporating retention probability -- it inflates projections.
- Skip reactivation analysis -- lapsed donors who return are often highly loyal.

NEXT STEPS:
- "Implement lapse risk scoring if not currently predictive."
- "Run `/fundraising-optimizer` to evaluate retention alongside other fundraising metrics."
- "Run `/impact-measurement` to strengthen impact reporting to donors."
- "Automate stewardship workflows to close gaps in donor acknowledgment and cultivation."
- "Improve first-year donor retention -- it has the greatest impact on long-term revenue."


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /donor-retention — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
