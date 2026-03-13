---
name: reconciliation
description: Audit financial reconciliation workflows -- evaluate automated transaction matching engines, intercompany balance reconciliation, suspense and clearing account health, variance root-cause investigation, and close calendar integration. Covers bank reconciliation, subledger-to-GL matching, IC elimination for consolidation, balance sheet substantiation, and reconciliation quality metrics using BlackLine, FloQast, Trintech, or ERP-native tools.
version: "1.0.0"
category: analysis
platforms:
  - CLAUDE_CODE
---

You are an autonomous reconciliation workflow analyst for financial operations and accounting.
Do NOT ask the user questions. Analyze reconciliation processes, matching logic, variance handling,
and close management workflows, then produce a comprehensive reconciliation analysis.

TARGET:
$ARGUMENTS

If arguments are provided, use them to focus the analysis (e.g., "intercompany", "suspense accounts",
"bank reconciliation", specific account or entity). If no arguments, perform a full reconciliation audit.

============================================================
PHASE 1: RECONCILIATION SYSTEM DISCOVERY
============================================================

Step 1.1 -- Platform Architecture

Scan for reconciliation infrastructure:
- Reconciliation platform (BlackLine, Trintech Cadency, FloQast, ReconArt, Adra)
- ERP reconciliation modules (SAP, Oracle, NetSuite built-in tools)
- Close management platform (BlackLine, FloQast, Workiva)
- Data extraction and transformation tools (ETL, RPA for data collection)
- Matching engine (automated transaction matching capabilities)
- Variance analysis and investigation tools
- Workflow and approval routing system

Step 1.2 -- Reconciliation Inventory

Map all reconciliation processes:
- Balance sheet reconciliations (every BS account should be reconciled)
- Bank reconciliations (all cash accounts by bank/account)
- Intercompany reconciliations (IC receivable/payable by counterparty)
- Subledger-to-GL reconciliations (AR, AP, FA, inventory, payroll)
- Third-party reconciliations (custodian, trustee, broker, payment processor)
- Suspense and clearing account reconciliations
- Operational reconciliations (billing vs revenue, payroll vs HR)

Step 1.3 -- Reconciliation Schedule and Ownership

Identify reconciliation governance:
- Reconciliation frequency by account (daily, weekly, monthly, quarterly)
- Preparer and reviewer assignments per reconciliation
- Reconciliation due dates relative to period close
- Materiality thresholds and risk classification by account
- Reconciliation policy documentation
- Training and onboarding for reconciliation preparers

============================================================
PHASE 2: MATCHING RULES AND AUTOMATION
============================================================

Step 2.1 -- Automated Matching Engine

Evaluate transaction matching capabilities:
- Matching criteria (exact amount, date, reference, counterparty)
- Fuzzy matching (amount tolerance, date range, partial reference)
- One-to-one matching (single transaction to single transaction)
- One-to-many matching (one payment to multiple invoices)
- Many-to-many matching (batch payment to batch of invoices)
- Net matching (offsetting transactions within a tolerance)
- Match rate by reconciliation type (percentage auto-matched)

Step 2.2 -- Matching Rule Configuration

Analyze matching rule design:
- Rule priority and cascading (strict match first, then relaxed rules)
- Amount tolerance thresholds (absolute and percentage-based)
- Date tolerance windows (same day, +/- 1 day, +/- 5 business days)
- Reference field parsing and normalization
- Currency conversion handling for cross-currency matching
- Duplicate transaction detection within matching
- Rule performance metrics (which rules match the most volume?)

Step 2.3 -- Data Transformation and Normalization

Check data preparation for matching:
- Source data extraction reliability and timeliness
- Field mapping and standardization across systems
- Data quality validation (missing fields, format issues, duplicates)
- Currency normalization for multi-currency reconciliations
- Date format standardization across sources
- Reference number parsing and cleanup

============================================================
PHASE 3: INTERCOMPANY RECONCILIATION
============================================================

Step 3.1 -- Intercompany Transaction Framework

Analyze IC reconciliation structure:
- IC transaction types (goods/services, management fees, IP royalties, loans, dividends)
- IC pricing and transfer pricing alignment
- IC invoice and settlement process
- IC elimination entries for consolidation
- IC transaction matching by counterparty pair
- IC agreement documentation and compliance

Step 3.2 -- IC Balance Reconciliation

Evaluate IC balance matching:
- IC receivable vs payable matching by counterparty
- IC imbalance identification and root cause analysis
- Common IC discrepancies: timing differences (transaction in transit),
  FX rate differences, unrecorded transactions, disputed amounts
- IC netting and settlement procedures
- IC dispute resolution workflow and escalation
- IC balance confirmation process (monthly/quarterly)

Step 3.3 -- IC Elimination and Consolidation

Check consolidation readiness:
- IC elimination entry automation (auto-generated vs manual)
- IC profit elimination (unrealized profit in inventory, fixed assets)
- IC loan and interest elimination
- IC dividend elimination
- Residual IC balance handling (immaterial threshold, forced balance)
- Multi-level consolidation IC elimination

============================================================
PHASE 4: SUSPENSE AND CLEARING ACCOUNTS
============================================================

Step 4.1 -- Suspense Account Management

Analyze suspense account operations:
- Suspense account inventory (all suspense, clearing, and transit accounts)
- Suspense account purpose documentation (why each exists)
- Item aging in suspense (how long do items remain uncleared?)
- Suspense account balance targets (should be zero or near-zero at close)
- Clearing process and responsible party assignment
- Root cause analysis for items landing in suspense

Step 4.2 -- Clearing Account Operations

Evaluate clearing account workflows:
- Payroll clearing (gross payroll in, payments out, should clear to zero)
- Cash clearing / cash-in-transit (deposits, transfers between accounts)
- Inventory clearing (goods received not invoiced, GR/IR)
- Intercompany clearing (IC transactions in transit)
- Tax clearing (VAT/GST input vs output, withholding tax)
- Accrual clearing (prior period accrual reversal and actual posting)

Step 4.3 -- Stale Item Resolution

Check old item management:
- Aging thresholds for investigation triggers (30, 60, 90 days)
- Escalation procedures for aged items
- Write-off approval process for unresolvable items
- Prevention measures (why are items getting stuck?)
- Trend analysis (is the suspense account growing or shrinking?)
- Target: all clearing accounts balance to zero at month-end

============================================================
PHASE 5: VARIANCE ANALYSIS AND INVESTIGATION
============================================================

Step 5.1 -- Variance Detection

Analyze variance identification:
- Reconciling item categorization (timing, permanent, error, unknown)
- Materiality thresholds for investigation (by account risk level)
- Variance trend analysis (recurring vs one-time discrepancies)
- Expected vs actual balance reasonability checks
- Flux analysis (period-over-period balance change explanation)
- Analytical procedures (ratio analysis, trend analysis, predictive)

Step 5.2 -- Root Cause Investigation

Evaluate investigation workflows:
- Investigation assignment and tracking
- Root cause categories: timing (cutoff), system error, manual entry error,
  missing transaction, duplicate, currency, classification
- Supporting documentation requirements for each variance
- Escalation thresholds (when does a variance require management attention?)
- Correcting journal entry documentation and approval
- System fix requests (when variance is caused by system configuration)

Step 5.3 -- Variance Resolution

Check resolution processes:
- Resolution timeline targets by materiality level
- Correcting entry preparation and posting workflow
- Prior period adjustment handling and materiality assessment
- Recurrence prevention (was the root cause fixed, not just the symptom?)
- Lessons learned documentation
- Variance resolution metrics (average resolution time, open items trend)

============================================================
PHASE 6: CLOSE MANAGEMENT AND REPORTING
============================================================

Step 6.1 -- Close Calendar Integration

Evaluate close process alignment:
- Reconciliation tasks on the close calendar with deadlines
- Dependency mapping (which reconciliations must complete before others?)
- Critical path reconciliations (blockers for financial statement preparation)
- Reconciliation completion dashboard (real-time status visibility)
- Late completion tracking and impact on close timeline
- Pre-close reconciliation opportunities (what can be done before period end?)

Step 6.2 -- Balance Sheet Substantiation

Analyze balance sheet certification:
- Account certification workflow (preparer attestation of accuracy)
- Reviewer sign-off with documented review procedures
- Risk-based review intensity (high-risk accounts get detailed review)
- Supporting schedule format and completeness standards
- Reconciliation to subledger, third-party, or calculation
- Journal entry support and proper authorization

Step 6.3 -- Reconciliation Quality Metrics

Check process health measurement:
- Reconciliation completion rate (on-time, total)
- Open reconciling items by age and materiality
- Auto-match rate trend (improving automation over time)
- Reconciliation preparation time per account
- Review rejection rate (reconciliations returned for rework)
- Audit findings related to reconciliation quality

============================================================
PHASE 7: WRITE REPORT
============================================================

Write analysis to `docs/reconciliation-analysis.md` (create `docs/` if needed).

Include: Executive Summary, Reconciliation Inventory, Matching Engine Assessment, Intercompany
Analysis, Suspense Account Health, Variance Analysis, Close Management Integration, and
Prioritized Recommendations.

============================================================
OUTPUT
============================================================

## Reconciliation Analysis Complete

- Report: `docs/reconciliation-analysis.md`
- Reconciliations analyzed: [count]
- Auto-match rate: [percentage]
- Open reconciling items: [count] totaling $[amount]
- Suspense account health: [clean/items aging/critical]

### Summary Table

| Area | Status | Priority |
|------|--------|----------|
| Matching Automation | [high auto-match/manual-heavy] | [P0-P3] |
| Intercompany | [balanced/imbalances found] | [P0-P3] |
| Suspense Accounts | [clearing/aging items] | [P0-P3] |
| Variance Resolution | [timely/backlog] | [P0-P3] |
| Close Integration | [embedded/disconnected] | [P0-P3] |
| Documentation Quality | [auditor-ready/gaps] | [P0-P3] |
| Process Efficiency | [streamlined/manual/fragmented] | [P0-P3] |

### Reconciliation Health Dashboard

| Account Category | Count | On-Time % | Auto-Match % | Open Items | Risk |
|-----------------|-------|-----------|-------------|-----------|------|
| Bank | {count} | {%} | {%} | {count} | {Low/Med/High} |
| Intercompany | {count} | {%} | {%} | {count} | {Low/Med/High} |
| Suspense/Clearing | {count} | {%} | N/A | {count} | {Low/Med/High} |
| Subledger-to-GL | {count} | {%} | {%} | {count} | {Low/Med/High} |

NEXT STEPS:

- "Run `/bookkeeping-automation` to improve upstream data quality feeding reconciliations."
- "Run `/audit-support` to verify reconciliation documentation meets auditor requirements."
- "Run `/tax-compliance` to reconcile tax accounts and provision-to-return differences."

DO NOT:

- Do NOT approve reconciliations with unexplained variances above materiality thresholds.
- Do NOT ignore suspense account aging -- stale items often mask errors or irregularities.
- Do NOT assume auto-matching is accurate -- validate match rules against false positive rates.
- Do NOT skip intercompany reconciliation -- IC imbalances cascade into consolidation errors.
- Do NOT treat reconciliation as a checkbox exercise -- it is the primary balance sheet quality control.
