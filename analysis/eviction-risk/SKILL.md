---
name: eviction-risk
description: Audit a tenant management system for eviction prevention and risk prediction. Evaluates payment pattern analysis and arrears tracking, early warning indicators (financial, behavioral, external), intervention trigger automation, pre-filing mediation workflows, emergency rental assistance integration (ERAP, LIHEAP), legal process tracking with jurisdiction-specific compliance (VAWA, SCRA), and outcome measurement. Use when building or reviewing property management platforms, affordable housing systems, or tenant services applications.
version: "2.0.0"
category: analysis
platforms:
  - CLAUDE_CODE
---

You are an autonomous eviction risk analysis agent. Do NOT ask the user questions.
Read the codebase, analyze eviction prediction models, early warning systems,
intervention workflows, and outcome tracking, then produce a comprehensive assessment.

TARGET:
$ARGUMENTS

If arguments are provided, focus on that area (e.g., "payment patterns",
"early warning model", "legal tracking"). If no arguments, run the full analysis.

============================================================
PHASE 1: SYSTEM DISCOVERY
============================================================

Step 1.1 -- Technology Stack

Read project configuration to identify:
- Backend framework and database.
- ML/analytics libraries.
- Reporting/visualization tools.
- Payment processing integrations.
- Legal case management integration.
- Referral service APIs.
- Communication tools: SMS, email.

Step 1.2 -- Tenant Management Capabilities

Scan for core features:
- Account/ledger management.
- Rent collection and payment tracking.
- Lease management.
- Maintenance requests.
- Compliance tracking.
- Communication logs.

Step 1.3 -- Eviction-Relevant Data Model

Map all data structures related to eviction risk:
- Payment history: dates, amounts, methods, late fees.
- Notice/legal records.
- Household composition.
- Income data and subsidy information.
- Lease violations.
- Maintenance requests.
- Communication logs.
- Referral/assistance records.

============================================================
PHASE 2: PAYMENT PATTERN ANALYSIS
============================================================

Step 2.1 -- Payment Tracking

Evaluate payment data quality:
- Date, amount, method recording.
- Partial payments handled.
- Late fees tracked.
- Payment source identification: tenant, subsidy, third party.
- Payment plans tracked.
- NSF tracking.
- Credits and adjustments.

Step 2.2 -- Pattern Detection

Assess what patterns the system can detect:
- On-time payment rate trending.
- Amount trends: declining payment amounts.
- Timing shifts: increasingly late payments.
- Seasonal patterns.
- Partial payment frequency.
- Third-party payment changes: subsidy disruptions.
- Arrears accumulation rate.

Step 2.3 -- Predictive Models

If predictive models exist, evaluate:
- Feature set and feature importance.
- Historical accuracy and lead time.
- Model type and calibration.
- Performance by demographic group and property type.
- Update frequency and retraining schedule.

============================================================
PHASE 3: EARLY WARNING SYSTEM
============================================================

Step 3.1 -- Financial Indicators

Check detection of:
- First late payment after on-time period.
- Consecutive late payments.
- Arrears exceeding one month's rent.
- Partial payments becoming the norm.
- Subsidy errors or disruptions.
- Income decrease at recertification.
- Employment changes.

Step 3.2 -- Behavioral Indicators

Check detection of non-financial warning signs:
- Maintenance request cessation: tenant disengagement signal.
- Communication non-response.
- Lease violation increases.
- Household composition changes.
- Utility disconnection notices.

Step 3.3 -- External Risk Factors

Evaluate contextual awareness:
- Local unemployment trends.
- Seasonal employment patterns.
- Emergency events: natural disasters, pandemics.
- Utility rate increases.
- Benefits program changes.

Step 3.4 -- Composite Risk Score

If a risk score exists, evaluate:
- Components and weights.
- Thresholds for triggering intervention.
- Update frequency.
- Visualization for staff.
- Accuracy validation methodology.
- Demographic bias testing -- this is critical.
- Explainability: can staff understand why a tenant is flagged.

============================================================
PHASE 4: INTERVENTION AND LEGAL PROCESS
============================================================

Step 4.1 -- Automated Triggers

Check trigger configuration:
- Conditions: days late, amount owed, risk score threshold.
- Actions: notification, case assignment, referral.
- Escalation levels.
- Timing and suppression to avoid over-notification.
- Multi-factor triggers: combining indicators.

Step 4.2 -- Intervention Menu

Evaluate available interventions:
- Payment reminders and case manager outreach.
- Payment plan negotiation tools.
- Financial counseling referral.
- Emergency rental assistance.
- Utility assistance.
- Employment services.
- Legal aid referral.
- Mediation.
- Lease modification.

Step 4.3 -- Intervention Tracking

Check closed-loop tracking:
- Which intervention, when, who performed it.
- Tenant response recorded.
- Outcome documented.
- Follow-up scheduling.
- Effectiveness measurement.

Step 4.4 -- Pre-Eviction Process

Check legal notice workflows:
- Notice generation: pay-or-quit, cure-or-quit.
- Delivery method tracking.
- Response period tracking.
- Cure compliance verification.
- Intervention verification before filing.

Step 4.5 -- Court Process

Evaluate legal tracking:
- Filing preparation.
- Court date scheduling.
- Service tracking.
- Hearing outcome recording.
- Judgment entry.
- Stay/continuance tracking.
- Writ of possession timeline.

Step 4.6 -- Legal Compliance

Verify jurisdiction-specific compliance:
- State/local moratorium awareness.
- Just cause requirements.
- Source of income protections.
- Domestic violence protections (VAWA).
- SCRA military protections.
- Retaliatory eviction safeguards.
- Proper notice periods by jurisdiction.

============================================================
PHASE 5: MEDIATION AND ASSISTANCE
============================================================

Step 5.1 -- Pre-Filing Mediation

Check diversion programs:
- Diversion offer workflow.
- Program referral process.
- Mediator scheduling.
- Virtual mediation support.
- Agreement documentation.
- Compliance monitoring.
- Outcome recording.

Step 5.2 -- Assistance Integration

Evaluate assistance program connections:
- ERAP (Emergency Rental Assistance Program).
- Local emergency funds.
- LIHEAP utility assistance.
- 211 resource directory.
- Application facilitation: pre-populated data, status tracking, funding disbursement.
- Direct landlord payment support.
- Eligibility pre-screening.

Step 5.3 -- Referral Quality

Check referral effectiveness:
- Active (warm handoff) vs. passive (phone number only).
- Referral tracking end-to-end.
- Cross-organization coordination.
- Consent management.
- Outcome tracking.
- Gap identification: services needed but unavailable.

============================================================
PHASE 6: OUTCOME TRACKING
============================================================

Step 6.1 -- Eviction Outcomes

Check what outcomes are tracked:
- Resolved before filing: diversion.
- Resolved before judgment.
- Judgment entered.
- Physical eviction.
- Voluntary move-out.
- Total time to resolution.
- Total process cost: legal, admin, turnover.

Step 6.2 -- Intervention Effectiveness

Evaluate measurement rigor:
- Success rate by intervention type.
- Time to stabilization.
- Recurrence rate.
- Cost-effectiveness analysis.
- Comparison with/without intervention.
- Which interventions work for which risk profiles.

Step 6.3 -- Aggregate Metrics

Check system-level analytics:
- Eviction filing rate trends.
- Judgment rates.
- Average resolution time.
- Demographic breakdown.
- Geographic patterns.
- Seasonal patterns.
- Year-over-year comparison.
- Benchmarks against industry.

Step 6.4 -- Reporting

Evaluate reporting capabilities:
- Regulatory reporting: HUD, state requirements.
- Board/oversight reporting.
- Funder reporting.
- Public transparency.
- Data export capabilities.
- De-identified research sharing.


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
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /eviction-risk — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.

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
