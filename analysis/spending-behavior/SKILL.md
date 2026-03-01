---
name: spending-behavior
description: Analyzes personal finance apps for spending categorization accuracy, budget adherence tracking, behavioral nudge effectiveness, savings goal optimization, subscription detection, and financial health scoring models.
version: "1.0.0"
category: analysis
platforms:
  - CLAUDE_CODE
---

You are an autonomous spending behavior analyst. Do NOT ask the user questions.
Read the actual codebase, evaluate spending categorization, budget tracking,
behavioral nudges, savings optimization, subscription detection, and financial
health scoring, then produce a comprehensive analysis.

TARGET:
$ARGUMENTS

If arguments are provided, use them to focus the analysis (e.g., "categorization"
or "savings goals"). If no arguments, run the full analysis.

============================================================
PHASE 1: SYSTEM DISCOVERY
============================================================

Step 1.1 -- Technology Stack

Identify from package manifests: platform type (web, mobile, API), backend framework,
database engine, bank aggregation provider (Plaid, Yodlee, MX, Finicity), ML/analytics
libraries, charting/visualization, notification services, data export capabilities.

Step 1.2 -- Transaction Data Model

Read core data structures: transactions (amount, date, merchant, category, subcategory,
account, type -- debit, credit, transfer, refund), accounts (checking, savings, credit
card, investment, loan), budgets (category, allocated amount, period, rollover rules),
goals (target amount, target date, contribution schedule, funding source), recurring
items (bills, subscriptions, income, detected frequency).

Step 1.3 -- Data Ingestion Pipeline

Map how transaction data enters the system: bank feed connection (real-time vs. batch),
manual entry, receipt scanning/OCR, CSV import, transaction deduplication logic,
pending transaction handling, transaction enrichment pipeline (merchant name cleaning,
logo matching, category assignment).

============================================================
PHASE 2: SPENDING CATEGORIZATION
============================================================

Step 2.1 -- Category Taxonomy

Evaluate: category hierarchy (top-level and subcategories), number and granularity
of categories, customizable vs. fixed categories, category mapping to standard
taxonomies (MCC codes, Plaid categories), handling of ambiguous merchants (is a
gas station purchase fuel or a snack), split transaction support (single purchase
across multiple categories).

Step 2.2 -- Categorization Engine

Evaluate: initial categorization method (merchant name matching, MCC code mapping,
ML classification, rules engine), categorization accuracy for common merchants,
handling of generic merchants (POS terminal, payment processor names), user
correction workflow (recategorize and learn), recategorization propagation (apply
correction to past and future transactions from same merchant), confidence scoring
(high confidence auto-assign, low confidence prompt user).

Step 2.3 -- Categorization Edge Cases

Evaluate: handling of transfers between own accounts (not spending), credit card
payments (not double-counting), refunds and returns (offset original category),
cash withdrawals (unknown category), peer-to-peer payments (Venmo, Zelle -- purpose
unknown), international transactions (currency and merchant name), business vs.
personal expense separation.

============================================================
PHASE 3: BUDGET ADHERENCE TRACKING
============================================================

Step 3.1 -- Budget Configuration

Evaluate: budget creation workflow (category-level, envelope-style, zero-based),
budget period options (monthly, bi-weekly, weekly, custom), income-based budget
suggestions, budget templates for common scenarios, multi-account budget consolidation,
shared household budgets, seasonal budget adjustments.

Step 3.2 -- Real-Time Tracking

Evaluate: spending pace visualization (on track, ahead, behind), remaining budget
calculation accuracy, daily spending rate vs. daily budget rate, category-level
burn-down, rollover handling (unused budget carries forward or resets), over-budget
detection and alerting, mid-period budget adjustment.

Step 3.3 -- Budget Alerts and Notifications

Evaluate: threshold alerts (50%, 75%, 90%, 100% of budget), frequency capping
(avoid alert fatigue), delivery channels (push, email, SMS, in-app), alert
customization (per category thresholds), predictive alerts (projected to exceed
budget based on current pace), positive reinforcement alerts (under budget).

============================================================
PHASE 4: BEHAVIORAL NUDGE SYSTEM
============================================================

Step 4.1 -- Nudge Types

Evaluate: pre-purchase nudges (spending approaching budget limit), post-purchase
nudges (large or unusual transaction alerts), comparative nudges (spending more
than usual in this category), social comparison nudges (spend less than X% of
similar users -- privacy considerations), goal-linked nudges (this purchase delays
your savings goal by N days), positive reinforcement (streak maintenance, savings
milestones).

Step 4.2 -- Nudge Timing and Delivery

Evaluate: nudge trigger conditions (amount thresholds, pattern detection, goal
proximity), delivery timing (real-time vs. daily digest vs. weekly summary),
nudge suppression rules (don't nudge during known bill payment periods), A/B
testing infrastructure for nudge effectiveness, user preference respect (nudge
frequency settings, opt-out per category).

Step 4.3 -- Nudge Effectiveness Measurement

Evaluate: whether the system tracks behavior change after nudges, nudge-to-action
conversion rates, spending reduction attribution, nudge fatigue detection (declining
response rates), user satisfaction with nudge frequency, long-term behavioral change
vs. short-term compliance.

============================================================
PHASE 5: SAVINGS GOAL OPTIMIZATION
============================================================

Step 5.1 -- Goal Configuration

Evaluate: goal types supported (emergency fund, vacation, down payment, education,
custom), target amount and date setting, automatic contribution scheduling, funding
source selection (specific account, round-ups, percentage of income), multiple
concurrent goal prioritization, goal sharing (household members).

Step 5.2 -- Goal Progress Tracking

Evaluate: progress visualization (progress bar, projected completion date), on-track
vs. behind-schedule detection, automatic adjustment recommendations when behind,
contribution history tracking, interest/growth inclusion in projections, milestone
celebrations, goal completion workflows (funds transfer, goal archival).

Step 5.3 -- Savings Optimization

Evaluate: round-up savings (transaction round-up to nearest dollar), found money
detection (lower-than-usual bills, refunds, windfalls), savings rate recommendations
based on income and expenses, idle cash detection (excess in checking), optimal
savings allocation across goals, emergency fund priority (recommend building before
other goals), high-yield savings account integration.

============================================================
PHASE 6: SUBSCRIPTION DETECTION
============================================================

Step 6.1 -- Detection Algorithm

Evaluate: recurring transaction identification (same merchant, similar amount,
regular interval), frequency detection accuracy (monthly, annual, weekly, quarterly),
amount variation tolerance (subscriptions with taxes or small price changes),
free trial to paid conversion detection, new subscription alerts, cancelled
subscription confirmation, merchant name normalization for subscription grouping.

Step 6.2 -- Subscription Management

Evaluate: subscription inventory dashboard (all detected subscriptions), total
monthly subscription cost calculation, category breakdown (streaming, software,
fitness, news, etc.), unused subscription detection (subscriptions without associated
usage data), price increase alerts, renewal date reminders, cancellation workflow
assistance (links, instructions).

Step 6.3 -- Subscription Optimization

Evaluate: duplicate service detection (multiple streaming services), downgrade
recommendations based on usage, annual vs. monthly pricing comparison, bundle
opportunity identification, total subscription cost trending over time, subscription
cost as percentage of income.

============================================================
PHASE 7: FINANCIAL HEALTH SCORING
============================================================

Step 7.1 -- Score Components

Evaluate: which factors feed the health score (savings rate, debt-to-income ratio,
emergency fund adequacy, spending vs. income, bill payment timeliness, credit
utilization, net worth trend, insurance coverage), component weighting methodology,
score range and granularity, benchmark definition (what constitutes healthy).

Step 7.2 -- Score Calculation

Evaluate: calculation methodology transparency (can users see what drives their
score), update frequency (real-time, daily, monthly), historical score tracking,
score change attribution (which factor caused the change), peer comparison
(anonymized cohort benchmarks), score projection (if you maintain current behavior,
score will be X in 6 months).

Step 7.3 -- Actionable Insights

Evaluate: personalized recommendations based on score components, priority ordering
(which action would most improve score), estimated score improvement per action,
progress tracking on recommendations, link between health score and specific
financial behaviors, educational content tied to low-scoring areas.

Write analysis to `docs/spending-behavior-analysis.md` (create `docs/` if needed).

============================================================
OUTPUT
============================================================

## Spending Behavior Analysis Complete

- Report: `docs/spending-behavior-analysis.md`
- Categorization methods evaluated: [count]
- Budget tracking features assessed: [count]
- Behavioral nudge types analyzed: [count]
- Savings goal features reviewed: [count]
- Subscription detection capabilities: [count]
- Health score components assessed: [count]

**Critical findings:**
1. [finding] -- [user financial impact]
2. [finding] -- [categorization accuracy concern]
3. [finding] -- [behavioral nudge effectiveness gap]

**Top recommendations:**
1. [recommendation] -- [expected improvement in spending awareness]
2. [recommendation] -- [expected improvement in savings outcomes]
3. [recommendation] -- [expected improvement in user engagement]

NEXT STEPS:
- "Run `/debt-payoff` to analyze how spending insights feed into debt reduction strategy."
- "Run `/retirement-optimizer` to evaluate long-term financial planning integration."
- "Run `/security-review` to audit access controls on bank aggregation credentials."

DO NOT:
- Do NOT modify any code -- this is an analysis skill, not an implementation skill.
- Do NOT include real transaction data, account numbers, or personally identifiable information in output.
- Do NOT evaluate the financial advice quality -- evaluate the software's ability to surface actionable insights.
- Do NOT ignore categorization edge cases -- miscategorized transactions erode user trust and budget accuracy.
- Do NOT assess nudges without considering fatigue -- excessive notifications cause users to disable them entirely.
- Do NOT overlook privacy implications of social comparison features -- peer benchmarking requires careful anonymization.
- Do NOT treat all users as having stable, predictable income -- variable income users need different budget models.
- Do NOT assume bank aggregation data is always accurate -- pending transactions, delayed postings, and merchant name variations cause errors.
