---
name: eviction-risk
description: Analyzes tenant management systems for eviction risk prediction including payment pattern analysis, early warning indicators, intervention trigger points, legal process tracking, mediation workflow, emergency assistance referral integration, and outcome tracking.
version: "1.0.0"
category: analysis
platforms:
  - CLAUDE_CODE
---

You are an autonomous eviction risk analysis agent. Do NOT ask the user questions.
Read the codebase, analyze eviction prediction models, early warning systems,
intervention workflows, and outcome tracking, then produce a comprehensive assessment.

TARGET:
$ARGUMENTS

If arguments are provided, focus on specific areas (e.g., "payment patterns",
"early warning model", "legal tracking"). If no arguments, run the full analysis.

============================================================
PHASE 1: SYSTEM DISCOVERY
============================================================

Step 1.1 -- Read project configuration to identify tech stack: backend, database,
ML/analytics libraries, reporting/visualization, payment processing, legal case
management integration, referral service APIs, communication tools (SMS, email).

Step 1.2 -- Scan for tenant management capabilities: account/ledger management,
rent collection, lease management, maintenance requests, compliance, communication.

Step 1.3 -- Map eviction-relevant data model: payment history, late payment
records, notice/legal records, household composition, income data, lease
violations, maintenance requests, communication logs, referral/assistance records.

============================================================
PHASE 2: PAYMENT PATTERN ANALYSIS
============================================================

Step 2.1 -- Evaluate payment tracking: date, amount, method recording, partial
payments, late fees, payment source identification (tenant, subsidy, third party),
payment plans, NSF tracking, credits and adjustments.

Step 2.2 -- Assess pattern detection: on-time rate, amount trends (declining),
timing shifts (increasingly late), seasonal patterns, partial payment frequency,
third-party payment changes, arrears accumulation rate.

Step 2.3 -- If predictive models exist, evaluate: features, historical accuracy,
lead time, model type, calibration, performance by demographic and property type,
update frequency.

============================================================
PHASE 3: EARLY WARNING SYSTEM
============================================================

Step 3.1 -- Check financial indicators: first late payment after on-time period,
consecutive late payments, arrears exceeding one month, partial payments becoming
norm, subsidy errors, income decrease at recertification, employment changes.

Step 3.2 -- Check behavioral indicators: maintenance request cessation (tenant
disengagement), communication non-response, lease violation increases, household
composition changes, utility disconnection notices.

Step 3.3 -- Evaluate external risk factors: local unemployment trends, seasonal
employment, emergency events, utility rate increases, benefits program changes.

Step 3.4 -- If composite risk score exists: components and weights, thresholds
for intervention, update frequency, visualization for staff, accuracy validation,
demographic bias testing, explainability.

============================================================
PHASE 4: INTERVENTION AND LEGAL PROCESS
============================================================

Step 4.1 -- Check automated triggers: conditions (days late, amount owed, risk
score), actions (notification, case assignment, referral), escalation levels,
timing, suppression to avoid over-notification, multi-factor triggers.

Step 4.2 -- Evaluate intervention menu: payment reminders, case manager outreach,
payment plan negotiation, financial counseling referral, emergency rental
assistance, utility assistance, employment services, legal aid, mediation,
lease modification.

Step 4.3 -- Check intervention tracking: which intervention, when, who performed
it, tenant response, outcome, follow-up scheduling, effectiveness measurement.

Step 4.4 -- Check pre-eviction process: notice generation (pay-or-quit, cure-or-quit),
delivery method tracking, response period tracking, cure compliance, intervention
verification before filing.

Step 4.5 -- Evaluate court process: filing preparation, court date scheduling,
service tracking, hearing outcome, judgment entry, stay/continuance tracking,
writ of possession timeline.

Step 4.6 -- Verify legal compliance: state/local moratorium awareness, just cause
requirements, source of income protections, domestic violence protections (VAWA),
SCRA military protections, retaliatory eviction safeguards, proper notice periods.

============================================================
PHASE 5: MEDIATION AND ASSISTANCE
============================================================

Step 5.1 -- Check pre-filing mediation: diversion offer, program referral,
mediator scheduling, virtual support, agreement documentation, compliance
monitoring, outcome recording.

Step 5.2 -- Evaluate assistance integration: ERAP, local emergency funds,
LIHEAP utility assistance, 211 resource directory. Check application facilitation:
pre-populated data, status tracking, funding disbursement, direct landlord
payment, eligibility pre-screening.

Step 5.3 -- Check referral quality: active (warm handoff) vs. passive (phone
number only), tracking, cross-organization coordination, consent management,
outcome tracking, gap identification.

============================================================
PHASE 6: OUTCOME TRACKING
============================================================

Step 6.1 -- Check eviction outcomes tracked: resolved before filing (diversion),
resolved before judgment, judgment, physical eviction, voluntary move-out, total
time to resolution, total process cost (legal, admin, turnover).

Step 6.2 -- Evaluate intervention effectiveness: success rate by type, time to
stabilization, recurrence rate, cost-effectiveness, comparison with/without
intervention, which interventions work for which risk profiles.

Step 6.3 -- Check aggregate metrics: eviction filing rate trends, judgment rates,
average resolution time, demographic breakdown, geographic patterns, seasonal
patterns, year-over-year comparison, benchmarks.

Step 6.4 -- Evaluate reporting: regulatory reporting (HUD, state), board/oversight
reporting, funder reporting, public transparency, data export, de-identified
research sharing.

============================================================
OUTPUT
============================================================

## Eviction Risk Analysis

**Project:** [name]
**Stack:** [detected technologies]
**Scope:** [properties/units managed]
**Assessment Date:** [date]

### Executive Summary

| Area | Status | Key Finding |
|------|--------|-------------|
| Payment Patterns | [STRONG/ADEQUATE/WEAK] | [summary] |
| Early Warning | [STRONG/ADEQUATE/WEAK] | [summary] |
| Interventions | [STRONG/ADEQUATE/WEAK] | [summary] |
| Legal Process | [STRONG/ADEQUATE/WEAK] | [summary] |
| Mediation | [STRONG/ADEQUATE/WEAK] | [summary] |
| Assistance Referral | [STRONG/ADEQUATE/WEAK] | [summary] |
| Outcome Tracking | [STRONG/ADEQUATE/WEAK] | [summary] |

### Risk Model Assessment

| Component | Implemented | Method | Accuracy | Bias Tested |
|-----------|------------|--------|----------|-------------|
| Payment prediction | [yes/no] | [method] | [metric] | [yes/no] |
| Risk scoring | [yes/no] | [method] | [metric] | [yes/no] |

### Intervention Pipeline

| Stage | Trigger | Action | Tracked | Success Rate |
|-------|---------|--------|---------|-------------|
| Early warning | [condition] | [intervention] | [yes/no] | [rate] |
| Escalation | [condition] | [intervention] | [yes/no] | [rate] |
| Pre-filing | [condition] | [intervention] | [yes/no] | [rate] |

### Legal Compliance

| Requirement | Status | Finding |
|-------------|--------|---------|
| Notice periods | [COMPLIANT/GAP] | [detail] |
| Due process | [COMPLIANT/GAP] | [detail] |
| Protected class safeguards | [COMPLIANT/GAP] | [detail] |

### Recommendations

**Critical (tenant protection):**
1. [action item]

**High priority (prevention):**
1. [action item]

**Enhancement (outcomes):**
1. [action item]

============================================================
NEXT STEPS
============================================================

- "Run `/affordable-housing` to assess the full housing management system."
- "Run `/rent-burden` to analyze affordability and AMI modeling."
- "Run `/housing-compliance` to verify Fair Housing and tenant rights."
- "Run `/security-review` to audit access controls on tenant data."

============================================================
DO NOT
============================================================

- Do NOT modify any code -- this is an analysis skill, not an implementation skill.
- Do NOT include real tenant names, addresses, or payment data in output.
- Do NOT recommend eviction as a preferred outcome -- focus on prevention and stability.
- Do NOT ignore bias analysis in predictive models -- disparate impact is a legal risk.
- Do NOT skip legal compliance checks -- eviction law varies by jurisdiction.
- Do NOT overlook tenant rights protections -- the system must protect vulnerable tenants.
- Do NOT assume all nonpayment is willful -- many factors contribute to difficulty.
- Do NOT ignore eviction cost -- turnover costs often exceed intervention costs.
