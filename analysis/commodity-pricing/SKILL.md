---
name: commodity-pricing
description: "Analyze commodity pricing and trading systems including forward curves, option models, position management, risk metrics, and regulatory reporting. Use when: 'review pricing models', 'audit trading system', 'evaluate VaR implementation', 'check commodity risk management', 'assess ETRM system', 'review derivatives valuation', 'analyze energy trading platform', 'evaluate hedge accounting'."
version: "2.0.0"
category: analysis
platforms:
  - CLAUDE_CODE
---

You are in AUTONOMOUS MODE. Do NOT ask questions. Evaluate every component of the commodity pricing and trading system systematically.

## INPUT

$ARGUMENTS (optional). If no arguments provided, analyze the entire commodity pricing codebase in the current working directory.

---

## PHASE 0: SYSTEM DISCOVERY

Auto-detect the commodity trading system architecture.

### Tech Stack
- `requirements.txt` / `pyproject.toml` -> Python (QuantLib, NumPy, SciPy, pandas, arch)
- `pom.xml` / `build.gradle` -> Java/Scala (Spark, Flink, enterprise ETRM systems)
- `package.json` -> Node.js (API layer, dashboard, reporting frontend)
- `go.mod` / `Cargo.toml` -> Go/Rust (low-latency pricing engines, market data feeds)
- `docker-compose.yml` / `k8s/` -> Container orchestration
- `.proto` files -> gRPC for inter-service communication

### Trading Components
- Identify pricing models: Black-Scholes, Monte Carlo, binomial trees, finite difference.
- Identify market data: real-time feeds (ICE, CME, NYMEX), historical databases, curve construction.
- Identify position management: trade capture, portfolio aggregation, P&L calculation.
- Identify risk systems: VaR engines, stress testing, Greeks calculation, limit monitoring.
- Identify settlement: physical delivery tracking, financial settlement, netting, invoicing.
- Identify regulatory: EMIR/Dodd-Frank reporting, REMIT surveillance, position limits.
- Identify deal capture: trade entry, confirmation, lifecycle events (amendments, novations).

Produce a system architecture map before proceeding.

---

## PHASE 1: PRICING MODEL EVALUATION

### 1.1 Forward Curve Construction
- Check bootstrapping methodology (piecewise, spline, monotone convex).
- Verify curve input sources: exchange settlements, broker quotes, bilateral trades.
- Check for seasonal shaping in power and gas curves (monthly, daily, hourly granularity).
- Verify basis differential modeling between delivery points.
- Check curve storage and versioning (end-of-day, intraday, real-time).
- Verify curve staleness detection and fallback logic for missing market data.

### 1.2 Option Pricing
- Identify option models: Black-76, Bachelier, local volatility, stochastic volatility.
- Check implied volatility surface construction and interpolation.
- Verify smile/skew handling in energy options (mean-reverting models).
- Check Asian option pricing (arithmetic average, geometric approximation).
- Verify spread option pricing: Kirk approximation, Margrabe, or Monte Carlo.
- Check swing/storage option valuation: least-squares Monte Carlo, dynamic programming.
- Verify calendar spread and time spread option handling.

### 1.3 Monte Carlo Simulation
- Check variance reduction techniques: antithetic variates, control variates, stratification.
- Verify random number generation quality (Mersenne Twister, Sobol sequences).
- Check convergence monitoring and adaptive sample sizing.
- Verify correlation structure in multi-factor simulations (Cholesky decomposition).
- Check simulation performance: GPU acceleration, parallel processing.
- Verify path generation respects mean reversion and jump-diffusion if applicable.

### 1.4 Physical Asset Valuation
- Check real option valuation of physical assets (tolling agreements, storage, transport).
- Verify intrinsic vs extrinsic value decomposition.
- Check operational constraint modeling (ramp rates, minimum run times, efficiency curves).
- Verify seasonal storage optimization (injection/withdrawal scheduling).
- Check transportation and pipeline capacity valuation.

For each finding: file path, model component, severity, description, recommendation.

---

## PHASE 2: MARKET DATA MANAGEMENT

### 2.1 Real-Time Feeds
- Identify exchange feed handlers: CME MDP, ICE iMpact, NYMEX, EEX, NBP.
- Check feed redundancy and failover between primary and backup feeds.
- Verify message processing latency monitoring.
- Check sequence number gap detection and recovery.
- Verify time synchronization accuracy for market data timestamps.
- Check throttling and backpressure handling during high-volume periods.

### 2.2 Historical Data
- Check tick data storage and retrieval performance.
- Verify end-of-day settlement price capture and validation.
- Check corporate action and contract rollover handling.
- Verify data quality validation: price bounds, stale data detection, outlier filtering.
- Check gap filling methodology for illiquid products.
- Verify historical data retention meets regulatory requirements (5-7 years minimum).

### 2.3 Curve Management
- Check official end-of-day curve publication workflow.
- Verify curve approval and sign-off process.
- Check curve override capability with audit trail.
- Verify multi-curve support: bid, ask, mid, settlement, internal marks.
- Check curve comparison and variance reporting.
- Verify curve data distribution to downstream consumers (risk, P&L, settlement).

### 2.4 Reference Data
- Check contract specification management (lot sizes, delivery points, expiry dates).
- Verify product master data consistency across systems.
- Check calendar management (exchange holidays, delivery calendars).
- Verify counterparty and broker reference data management.

---

## PHASE 3: POSITION MANAGEMENT AND P&L

### 3.1 Trade Capture
- Check trade entry validation (limit checks, product eligibility, counterparty credit).
- Verify trade lifecycle event handling: new, amend, cancel, novation, exercise, assignment.
- Check trade confirmation matching and exception handling.
- Verify deal ticket completeness (all required fields populated).
- Check bulk trade import capability and validation.
- Verify trade audit trail (every change tracked with user, timestamp, before/after).

### 3.2 Position Aggregation
- Check real-time position aggregation by: book, trader, desk, commodity, delivery period.
- Verify netting logic: delivery point, counterparty, product type.
- Check physical vs financial position separation.
- Verify time-bucketed position reporting (daily, monthly, quarterly, annual).
- Check position limit monitoring against regulatory and internal limits.
- Verify position reconciliation between front-office and back-office systems.

### 3.3 P&L Calculation
- Check mark-to-market P&L methodology (daily revaluation against curves).
- Verify realized vs unrealized P&L separation.
- Check P&L attribution: price change, volume change, new deals, curve roll.
- Verify P&L explain capability (breakdown of daily P&L movement drivers).
- Check accounting P&L vs trading P&L reconciliation.
- Verify multi-currency P&L with FX rate handling.
- Check accrual accounting treatment where required (hedge accounting, ASC 815).

### 3.4 Hedge Accounting
- Check hedge designation and documentation workflow.
- Verify hedge effectiveness testing: prospective and retrospective.
- Check fair value vs cash flow hedge classification.
- Verify de-designation and reclassification handling.
- Check ASC 815 / IFRS 9 compliance in hedge accounting logic.

---

## PHASE 4: RISK MANAGEMENT

### 4.1 Value at Risk (VaR)
- Identify VaR methodology: historical simulation, parametric, Monte Carlo.
- Check VaR confidence levels and holding periods (95%/99%, 1-day/10-day).
- Verify VaR backtesting: exceptions tracking, Kupiec test, Christoffersen test.
- Check conditional VaR (CVaR / Expected Shortfall) calculation.
- Verify component VaR and incremental VaR for portfolio decomposition.
- Check VaR limit monitoring and breach notification.

### 4.2 Greeks Calculation
- Check delta, gamma, vega, theta, rho calculation on all derivative positions.
- Verify Greeks are computed using appropriate bump sizes (1% price, 1% vol, 1 day).
- Check cross-gamma and correlation sensitivity.
- Verify Greeks aggregation across portfolios.
- Check Greeks-based hedging recommendations.

### 4.3 Stress Testing
- Check historical stress scenarios (energy crises, weather events, geopolitical shocks).
- Verify hypothetical stress scenario construction capability.
- Check reverse stress testing (what scenario causes a given loss threshold).
- Verify stress test coverage of all material risk factors.
- Check stress test reporting and governance workflow.

### 4.4 Credit Risk
- Check counterparty credit exposure calculation (current and potential future exposure).
- Verify credit limit monitoring and breach alerting.
- Check collateral management: margin calls, ISDA CSA threshold tracking.
- Verify netting agreement application in exposure calculation.
- Check credit valuation adjustment (CVA) computation.

### 4.5 Limit Management
- Check multi-level limit framework: VaR, position, Greeks, notional, tenor.
- Verify limit breach detection is real-time or near-real-time.
- Check pre-trade limit checking capability.
- Verify limit override workflow with approval and audit trail.
- Check limit utilization reporting and trending.

---

## PHASE 5: REGULATORY REPORTING AND COMPLIANCE

### 5.1 EMIR / Dodd-Frank Reporting
- Check trade reporting to registered trade repositories.
- Verify Unique Transaction Identifier (UTI) generation and sharing.
- Check Legal Entity Identifier (LEI) management.
- Verify reporting field completeness against regulatory technical standards.
- Check lifecycle event reporting (modifications, terminations, valuations).
- Verify daily valuation reporting for outstanding derivatives.
- Check reporting reconciliation and error correction workflow.

### 5.2 REMIT (EU Energy Market)
- Check REMIT transaction reporting (standard and non-standard contracts).
- Verify fundamental data reporting (generation outages, capacity availability).
- Check inside information disclosure procedures.
- Verify market manipulation surveillance (wash trades, spoofing detection).
- Check ACER reporting format compliance.

### 5.3 Position Limits
- Check exchange position limit monitoring (CFTC, ESMA).
- Verify position aggregation across accounts and entities for limit purposes.
- Check large trader reporting threshold monitoring.
- Verify exemption tracking (bona fide hedging, risk management).
- Check speculative position limit compliance.

### 5.4 Settlement and Delivery
- Check physical delivery scheduling and nomination.
- Verify financial settlement calculation and netting.
- Check invoice generation and reconciliation.
- Verify settlement calendar management per exchange and jurisdiction.
- Check settlement dispute handling and resolution workflow.

---

## PHASE 6: SYSTEM OPERATIONS AND DATA INTEGRITY

### 6.1 End-of-Day Processing
- Check EOD batch processing pipeline: curve publication, P&L, risk, reporting.
- Verify batch job dependency management and failure handling.
- Check EOD reconciliation checkpoints.
- Verify EOD completion monitoring and SLA tracking.
- Check month-end and year-end close processing.

### 6.2 Data Integrity
- Check trade data reconciliation between systems (front/mid/back office).
- Verify position reconciliation with exchange clearing statements.
- Check cash reconciliation with bank statements.
- Verify data lineage tracking from source to report.
- Check data quality monitoring and alerting.

### 6.3 Audit and Controls
- Check segregation of duties: trading vs risk vs settlement vs IT.
- Verify four-eyes principle on trade amendments and limit changes.
- Check system access controls and role-based permissions.
- Verify regulatory audit trail retention (7 years for CFTC, 5 years for EMIR).
- Check change management controls on pricing models and risk parameters.

---


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

## OUTPUT FORMAT

```
## Commodity Pricing and Trading System Analysis Report

**System:** [name/description]
**Stack:** [detected technologies]
**Commodity Markets:** [detected: power, gas, oil, metals, agricultural]
**Trading Types:** [physical, financial, derivatives]

### Summary

| Category | Status | Findings | Critical |
|----------|--------|----------|----------|
| Pricing Models | [PASS/WARN/FAIL] | N | N |
| Market Data | [PASS/WARN/FAIL] | N | N |
| Position/P&L | [PASS/WARN/FAIL] | N | N |
| Risk Management | [PASS/WARN/FAIL] | N | N |
| Regulatory Reporting | [PASS/WARN/FAIL] | N | N |
| Operations/Integrity | [PASS/WARN/FAIL] | N | N |

### Pricing Model Coverage

| Product Type | Model | Validation | Greeks | Status |
|-------------|-------|------------|--------|--------|
| Forwards/Futures | | | | |
| European options | | | | |
| Asian options | | | | |
| Spread options | | | | |
| Swing/storage | | | | |

### Risk Coverage Matrix

| Risk Metric | Implemented | Validated | Monitored | Gap |
|-------------|-------------|-----------|-----------|-----|
| VaR (historical) | | | | |
| VaR (Monte Carlo) | | | | |
| CVaR / ES | | | | |
| Greeks | | | | |
| Stress testing | | | | |
| Credit exposure | | | | |

### Detailed Findings

For each category with WARN or FAIL:

| # | Severity | File | Description | Impact | Recommendation |
|---|----------|------|-------------|--------|----------------|

### Remediation Priority
[Ordered list by financial exposure and regulatory risk]
```

---

## RULES

- Do NOT modify any pricing models, risk parameters, or trading limits.
- Do NOT execute trades, submit orders, or interact with exchange APIs.
- Do NOT access or display actual trade data, counterparty names, or portfolio positions.
- Do NOT expose pricing model parameters, VaR figures, or limit thresholds that are commercially sensitive.
- Do NOT skip regulatory reporting analysis even for internal or proprietary trading systems.
- Do NOT assume model accuracy without checking backtesting and validation results.
- Do NOT conflate theoretical model outputs with production calibrated results -- verify calibration.

---

## NEXT STEPS

- "Run `/fraud-detection` to evaluate trade surveillance and market manipulation detection."
- "Run `/security-review` to audit trading platform APIs and access controls."
- "Run `/compliance-ops` to review broader financial regulatory requirements."


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /commodity-pricing — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
