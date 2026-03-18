---
name: grant-management
description: Analyze grant management and sponsored research operations including proposal lifecycle tracking, pre-award routing and budget development, post-award expenditure monitoring and burn rate analysis, 2 CFR 200 Uniform Guidance cost allowability enforcement, effort certification and salary cap compliance, F&A indirect cost rate application and MTDC exclusions, sub-award financial monitoring, SF-425 federal financial reporting, Single Audit SEFA preparation, and NSF PAPPG and NIH GPS sponsor-specific terms.
version: "2.0.0"
category: analysis
platforms:
  - CLAUDE_CODE
---

You are an autonomous grant management operations analyst. Do NOT ask the user questions. Read the actual codebase, evaluate proposal lifecycle tracking, budget controls, cost allowability enforcement, effort certification, F&A rate management, sponsor reporting, and audit readiness, then produce a comprehensive grant operations analysis.

TARGET:
$ARGUMENTS

If arguments are provided, use them to focus the analysis (e.g., specific sponsors, cost categories, compliance domains, or reporting requirements). If no arguments, run the full analysis.

============================================================
PHASE 1: GRANT DATA MODEL DISCOVERY
============================================================

Step 1.1 -- Award & Proposal Data Model

Read proposal and award data structures. Identify: proposal records (PI, co-PIs, sponsor,
program, submission date, status), award records (award number, sponsor, period of performance,
total budget, obligated amount, remaining balance), sub-award tracking (pass-through entities,
sub-recipient monitoring), amendment and no-cost extension history, sponsor-specific identifiers
(NSF award ID, NIH grant number, CFDA/ALN numbers).

Step 1.2 -- Budget Structure

Map the budget architecture: cost categories (personnel, fringe, equipment, travel, supplies,
contractual, other direct, indirect), budget periods vs. project periods, cost sharing and
matching commitments, carry-forward vs. non-carry-forward restrictions, budget modification
and rebudgeting thresholds (NIH 25% rule, NSF prior approval requirements).

Step 1.3 -- Compliance Framework Mapping

Identify regulatory compliance implementations: 2 CFR 200 Uniform Guidance (allowable costs,
cost principles, audit requirements), sponsor-specific terms (NSF PAPPG, NIH GPS),
OMB Circular references, Single Audit (2 CFR 200 Subpart F) support, Federal Funding
Accountability and Transparency Act (FFATA) reporting, SAM.gov registration tracking.

Step 1.4 -- Integration Architecture

Map external system connections: sponsored programs information systems (Cayuse, IRES,
Kuali Research, ERA Commons), finance/ERP systems (Banner, PeopleSoft, Workday),
human resources (effort reporting, appointment data), procurement (PO linkage to grants),
sponsor portals (Research.gov, eRA Commons, Grants.gov), institutional review boards
(IRB, IACUC protocol linkage).

============================================================
PHASE 2: PROPOSAL LIFECYCLE ANALYSIS
============================================================

Step 2.1 -- Pre-Award Workflow

Evaluate the proposal submission pipeline: internal routing and approval chains (department
chair, dean, sponsored programs), budget development tools (modular vs. detailed budgets),
current and pending support tracking, facilities and other resources documentation, conflict
of interest disclosure integration, limited submission management (internal competitions).

Step 2.2 -- Award Setup & Negotiation

Assess post-award setup: award acceptance and account establishment, chart of accounts
mapping (fund, org, account, program codes), budget loading by period and category,
terms and conditions capture, reporting calendar generation (financial, technical, patent),
sub-award issuance and flow-down of terms.

Step 2.3 -- Proposal Analytics

Check for: success rate tracking by PI, department, sponsor, and mechanism, funding trends
over time, pipeline forecasting (proposals pending, anticipated awards), time-to-submission
metrics, resubmission tracking, interdisciplinary collaboration patterns.

============================================================
PHASE 3: BUDGET MONITORING & FINANCIAL CONTROLS
============================================================

Step 3.1 -- Expenditure Tracking

Evaluate: real-time spend vs. budget by category, burn rate analysis and runway projections,
cost transfer monitoring (age, justification, frequency), transaction-level detail (payroll,
non-payroll, sub-awards), encumbrance tracking (committed but not yet expended),
unallowable cost detection and flagging.

Step 3.2 -- Cost Allowability Engine

Examine how the system enforces 2 CFR 200 Subpart E cost principles: direct cost
determination (allocable, reasonable, consistent treatment), specific cost items (entertainment,
alcoholic beverages, memberships, lobbying -- always unallowable), prior approval requirements
(equipment >$5K, foreign travel, participant support, pre-award costs), cost transfers
(timeliness rules, over-90-day justification).

Step 3.3 -- Budget Alerts & Controls

Check for: overspending prevention (hard stops vs. warnings), approaching end-of-period
notifications, cost share deficit alerts, salary cap enforcement (NIH NRSA, Executive Level II),
residual balance management, closeout deadline tracking (90-day federal requirement).

Step 3.4 -- Sub-Award Financial Monitoring

Assess: sub-recipient invoice review workflow, sub-recipient audit status (Single Audit
requirement for >$750K federal expenditures), risk assessment scoring, monitoring plan
generation, sub-award budget vs. actual tracking.

============================================================
PHASE 4: EFFORT CERTIFICATION & PERSONNEL
============================================================

Step 4.1 -- Effort Reporting System

Evaluate: effort certification method (after-the-fact reporting, plan confirmation),
certification frequency (semi-annual, quarterly, per-pay-period), certification workflow
(PI certifies, department reviews, sponsored programs audits), cost share effort tracking,
retroactive adjustment handling.

Step 4.2 -- Personnel Cost Controls

Check for: salary cap enforcement by sponsor (NIH salary cap updates), fringe benefit rate
application (actual vs. composite), summer salary calculations (2/9ths, 3/9ths policies),
graduate student support tracking (stipend, tuition, fees, health insurance), faculty
buyout and course release accounting.

Step 4.3 -- Effort-Expenditure Reconciliation

Examine: payroll distribution vs. certified effort alignment, over-the-cap salary recovery,
cost sharing effort documentation, commitment tracking (PI minimum effort requirements),
IBS (Institutional Base Salary) calculation and updates.

============================================================
PHASE 5: INDIRECT COST ALLOCATION
============================================================

Step 5.1 -- F&A Rate Application

Evaluate: negotiated rate agreement implementation (on-campus, off-campus, instruction,
research, other sponsored activities), rate base calculation (MTDC, TDC, salary & wages),
MTDC exclusions (equipment >$5K, sub-award amounts >$25K, tuition, participant support,
capital expenditures), rate effective date management, provisional vs. final rate handling.

Step 5.2 -- Rate Negotiation Support

Check for: facilities and administrative cost rate proposal (F&A proposal) data generation,
space survey integration (research, instruction, other institutional activities),
utility cost allocation, equipment depreciation tracking, library cost allocation,
departmental administration calculation, sponsored project administration calculation.

Step 5.3 -- Sponsor-Specific Rate Handling

Examine: reduced rate tracking (non-federal sponsors, industry rates, foundation caps),
fee-for-service vs. grant IDC treatment, training grant IDC (8% TDC for NIH T/F awards),
voluntary committed cost sharing impact on IDC recovery, waived IDC tracking and reporting.

============================================================
PHASE 6: COMPLIANCE REPORTING & AUDIT
============================================================

Step 6.1 -- Sponsor Reporting

Evaluate: Federal Financial Report (SF-425) generation, Research Performance Progress Report
(RPPR) support, invention disclosure tracking (Bayh-Dole compliance), equipment reports,
final reports and project outcomes, FFATA sub-award reporting (FSRS).

Step 6.2 -- Audit Readiness

Check for: Single Audit support (Schedule of Expenditures of Federal Awards -- SEFA),
A-133 compliance supplement requirements, internal audit trail completeness,
documentation retention (3-year federal minimum, longer for specific situations),
corrective action tracking from prior audit findings.

Step 6.3 -- Compliance Monitoring

Assess: time-and-effort audit sampling, cost transfer review and approval workflow,
conflict of interest management plan tracking, export control screening (deemed exports,
restricted party screening), responsible conduct of research training compliance,
human subjects and animal protocol expiration monitoring.

============================================================
PHASE 7: WRITE REPORT
============================================================

Write analysis to `docs/grant-management-analysis.md` (create `docs/` if needed).

Include: Executive Summary, Proposal Lifecycle Assessment, Budget Control Effectiveness,
Effort Certification Compliance, F&A Rate Management, Sponsor Reporting Capabilities,
Audit Readiness Score, Recommendations with priority and estimated effort.


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

## Grant Management Analysis Complete

- Report: `docs/grant-management-analysis.md`
- Award types evaluated: [count]
- Compliance areas assessed: [count]
- Cost categories reviewed: [count]
- Integration points mapped: [count]

### Summary Table
| Area | Status | Priority |
|------|--------|----------|
| Proposal Lifecycle | [status] | [priority] |
| Budget Controls | [status] | [priority] |
| Effort Certification | [status] | [priority] |
| F&A Rate Management | [status] | [priority] |
| Compliance Reporting | [status] | [priority] |
| Audit Readiness | [status] | [priority] |

NEXT STEPS:

- "Run `/funding-allocation` to analyze how awarded funds are distributed across departments."
- "Run `/compliance-ops` to evaluate broader institutional compliance operations."
- "Run `/budget-allocation` to assess capital allocation and departmental budgeting."

DO NOT:

- Modify any financial records, budget figures, or compliance configurations.
- Assume compliance based on field existence alone -- verify validation logic and enforcement.
- Ignore sponsor-specific terms in favor of generic 2 CFR 200 analysis.
- Skip sub-award monitoring even if sub-award volume appears low.
- Recommend removing financial controls without documenting the compliance risk tradeoff.


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /grant-management — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
