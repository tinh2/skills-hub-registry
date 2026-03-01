---
name: commodity-pricing
description: Analyze commodity pricing and trading systems including pricing models, market data feeds, position management, risk metrics, regulatory reporting, and settlement processing.
version: "1.0.0"
category: analysis
platforms:
  - CLAUDE_CODE
---

You are in AUTONOMOUS MODE. Do NOT ask questions. Evaluate every component of the commodity pricing and trading system systematically.

TARGET:
$ARGUMENTS

If no arguments provided, analyze the entire commodity pricing codebase in the current working directory.

============================================================
PHASE 0: SYSTEM DISCOVERY
============================================================

Auto-detect the commodity trading system architecture:

TECH STACK:
- `requirements.txt` / `pyproject.toml` -> Python (QuantLib, NumPy, SciPy, pandas, arch)
- `pom.xml` / `build.gradle` -> Java/Scala (Spark, Flink, enterprise ETRM systems)
- `package.json` -> Node.js (API layer, dashboard, reporting frontend)
- `go.mod` / `Cargo.toml` -> Go/Rust (low-latency pricing engines, market data feeds)
- `docker-compose.yml` / `k8s/` -> Container orchestration
- `.proto` files -> gRPC for inter-service communication

TRADING COMPONENTS:
- Identify pricing models: Black-Scholes, Monte Carlo, binomial trees, finite difference
- Identify market data: real-time feeds (ICE, CME, NYMEX), historical databases, curve construction
- Identify position management: trade capture, portfolio aggregation, P&L calculation
- Identify risk systems: VaR engines, stress testing, Greeks calculation, limit monitoring
- Identify settlement: physical delivery tracking, financial settlement, netting, invoicing
- Identify regulatory: EMIR/Dodd-Frank reporting, REMIT surveillance, position limits
- Identify deal capture: trade entry, confirmation, lifecycle events (amendments, novations)

Produce a system architecture map before proceeding.

============================================================
PHASE 1: PRICING MODEL EVALUATION
============================================================

Evaluate the derivatives pricing and valuation layer:

FORWARD CURVE CONSTRUCTION:
- Check for forward curve bootstrapping methodology (piecewise, spline, monotone convex)
- Verify curve input sources: exchange settlements, broker quotes, bilateral trades
- Check for seasonal shaping in power and gas curves (monthly, daily, hourly granularity)
- Verify basis differential modeling between delivery points
- Check for curve storage and versioning (end-of-day, intraday, real-time)
- Verify curve staleness detection and fallback logic for missing market data

OPTION PRICING:
- Identify option models: Black-76, Bachelier, local volatility, stochastic volatility
- Check for implied volatility surface construction and interpolation
- Verify smile/skew handling in energy options (mean-reverting models)
- Check for Asian option pricing (arithmetic average, geometric approximation)
- Verify spread option pricing: Kirk approximation, Margrabe, or Monte Carlo
- Check for swing/storage option valuation: least-squares Monte Carlo, dynamic programming
- Verify calendar spread and time spread option handling

MONTE CARLO SIMULATION:
- Check for variance reduction techniques: antithetic variates, control variates, stratification
- Verify random number generation quality (Mersenne Twister, Sobol sequences)
- Check for convergence monitoring and adaptive sample sizing
- Verify correlation structure in multi-factor simulations (Cholesky decomposition)
- Check for simulation performance: GPU acceleration, parallel processing
- Verify path generation respects mean reversion and jump-diffusion if applicable

PHYSICAL ASSET VALUATION:
- Check for real option valuation of physical assets (tolling agreements, storage, transport)
- Verify intrinsic vs extrinsic value decomposition
- Check for operational constraint modeling (ramp rates, minimum run times, efficiency curves)
- Verify seasonal storage optimization (injection/withdrawal scheduling)
- Check for transportation and pipeline capacity valuation

For each finding: file path, model component, severity, description, recommendation.

============================================================
PHASE 2: MARKET DATA MANAGEMENT
============================================================

Evaluate the market data infrastructure:

REAL-TIME FEEDS:
- Identify exchange feed handlers: CME MDP, ICE iMpact, NYMEX, EEX, NBP
- Check for feed redundancy and failover between primary and backup feeds
- Verify message processing latency monitoring
- Check for sequence number gap detection and recovery
- Verify time synchronization accuracy for market data timestamps
- Check for throttling and backpressure handling during high-volume periods

HISTORICAL DATA:
- Check for tick data storage and retrieval performance
- Verify end-of-day settlement price capture and validation
- Check for corporate action and contract rollover handling
- Verify data quality validation: price bounds, stale data detection, outlier filtering
- Check for gap filling methodology for illiquid products
- Verify historical data retention meets regulatory requirements (5-7 years minimum)

CURVE MANAGEMENT:
- Check for official end-of-day curve publication workflow
- Verify curve approval and sign-off process
- Check for curve override capability with audit trail
- Verify multi-curve support: bid, ask, mid, settlement, internal marks
- Check for curve comparison and variance reporting
- Verify curve data distribution to downstream consumers (risk, P&L, settlement)

REFERENCE DATA:
- Check for contract specification management (lot sizes, delivery points, expiry dates)
- Verify product master data consistency across systems
- Check for calendar management (exchange holidays, delivery calendars)
- Verify counterparty and broker reference data management

============================================================
PHASE 3: POSITION MANAGEMENT AND P&L
============================================================

Evaluate trade capture and position management:

TRADE CAPTURE:
- Check for trade entry validation (limit checks, product eligibility, counterparty credit)
- Verify trade lifecycle event handling: new, amend, cancel, novation, exercise, assignment
- Check for trade confirmation matching and exception handling
- Verify deal ticket completeness (all required fields populated)
- Check for bulk trade import capability and validation
- Verify trade audit trail (every change tracked with user, timestamp, before/after)

POSITION AGGREGATION:
- Check for real-time position aggregation by: book, trader, desk, commodity, delivery period
- Verify netting logic: delivery point, counterparty, product type
- Check for physical vs financial position separation
- Verify time-bucketed position reporting (daily, monthly, quarterly, annual)
- Check for position limit monitoring against regulatory and internal limits
- Verify position reconciliation between front-office and back-office systems

P&L CALCULATION:
- Check for mark-to-market P&L methodology (daily revaluation against curves)
- Verify realized vs unrealized P&L separation
- Check for P&L attribution: price change, volume change, new deals, curve roll
- Verify P&L explain capability (breakdown of daily P&L movement drivers)
- Check for accounting P&L vs trading P&L reconciliation
- Verify multi-currency P&L with FX rate handling
- Check for accrual accounting treatment where required (hedge accounting, ASC 815)

HEDGE ACCOUNTING:
- Check for hedge designation and documentation workflow
- Verify hedge effectiveness testing: prospective and retrospective
- Check for fair value vs cash flow hedge classification
- Verify de-designation and reclassification handling
- Check for ASC 815 / IFRS 9 compliance in hedge accounting logic

============================================================
PHASE 4: RISK MANAGEMENT
============================================================

Evaluate risk measurement and monitoring:

VALUE AT RISK (VaR):
- Identify VaR methodology: historical simulation, parametric, Monte Carlo
- Check VaR confidence levels and holding periods (95%/99%, 1-day/10-day)
- Verify VaR backtesting: exceptions tracking, Kupiec test, Christoffersen test
- Check for conditional VaR (CVaR / Expected Shortfall) calculation
- Verify component VaR and incremental VaR for portfolio decomposition
- Check for VaR limit monitoring and breach notification

GREEKS CALCULATION:
- Check for delta, gamma, vega, theta, rho calculation on all derivative positions
- Verify Greeks are computed using appropriate bump sizes (1% price, 1% vol, 1 day)
- Check for cross-gamma and correlation sensitivity
- Verify Greeks aggregation across portfolios
- Check for Greeks-based hedging recommendations

STRESS TESTING:
- Check for historical stress scenarios (energy crises, weather events, geopolitical shocks)
- Verify hypothetical stress scenario construction capability
- Check for reverse stress testing (what scenario causes a given loss threshold)
- Verify stress test coverage of all material risk factors
- Check for stress test reporting and governance workflow

CREDIT RISK:
- Check for counterparty credit exposure calculation (current and potential future exposure)
- Verify credit limit monitoring and breach alerting
- Check for collateral management: margin calls, ISDA CSA threshold tracking
- Verify netting agreement application in exposure calculation
- Check for credit valuation adjustment (CVA) computation

LIMIT MANAGEMENT:
- Check for multi-level limit framework: VaR, position, Greeks, notional, tenor
- Verify limit breach detection is real-time or near-real-time
- Check for pre-trade limit checking capability
- Verify limit override workflow with approval and audit trail
- Check for limit utilization reporting and trending

============================================================
PHASE 5: REGULATORY REPORTING AND COMPLIANCE
============================================================

Evaluate regulatory reporting capabilities:

EMIR / DODD-FRANK REPORTING:
- Check for trade reporting to registered trade repositories
- Verify Unique Transaction Identifier (UTI) generation and sharing
- Check for Legal Entity Identifier (LEI) management
- Verify reporting field completeness against regulatory technical standards
- Check for lifecycle event reporting (modifications, terminations, valuations)
- Verify daily valuation reporting for outstanding derivatives
- Check for reporting reconciliation and error correction workflow

REMIT (EU ENERGY MARKET):
- Check for REMIT transaction reporting (standard and non-standard contracts)
- Verify fundamental data reporting (generation outages, capacity availability)
- Check for inside information disclosure procedures
- Verify market manipulation surveillance (wash trades, spoofing detection)
- Check for ACER reporting format compliance

POSITION LIMITS:
- Check for exchange position limit monitoring (CFTC, ESMA)
- Verify position aggregation across accounts and entities for limit purposes
- Check for large trader reporting threshold monitoring
- Verify exemption tracking (bona fide hedging, risk management)
- Check for speculative position limit compliance

SETTLEMENT AND DELIVERY:
- Check for physical delivery scheduling and nomination
- Verify financial settlement calculation and netting
- Check for invoice generation and reconciliation
- Verify settlement calendar management per exchange and jurisdiction
- Check for settlement dispute handling and resolution workflow

============================================================
PHASE 6: SYSTEM OPERATIONS AND DATA INTEGRITY
============================================================

Evaluate operational controls and data governance:

END-OF-DAY PROCESSING:
- Check for EOD batch processing pipeline: curve publication, P&L, risk, reporting
- Verify batch job dependency management and failure handling
- Check for EOD reconciliation checkpoints
- Verify EOD completion monitoring and SLA tracking
- Check for month-end and year-end close processing

DATA INTEGRITY:
- Check for trade data reconciliation between systems (front/mid/back office)
- Verify position reconciliation with exchange clearing statements
- Check for cash reconciliation with bank statements
- Verify data lineage tracking from source to report
- Check for data quality monitoring and alerting

AUDIT AND CONTROLS:
- Check for segregation of duties: trading vs risk vs settlement vs IT
- Verify four-eyes principle on trade amendments and limit changes
- Check for system access controls and role-based permissions
- Verify regulatory audit trail retention (7 years for CFTC, 5 years for EMIR)
- Check for change management controls on pricing models and risk parameters

============================================================
OUTPUT
============================================================

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

#### [Category Name]

| # | Severity | File | Description | Impact | Recommendation |
|---|----------|------|-------------|--------|----------------|

### Remediation Priority
[Ordered list by financial exposure and regulatory risk]

============================================================
NEXT STEPS
============================================================

After reviewing the analysis:
- "Run `/load-forecast` to analyze demand prediction models feeding pricing decisions."
- "Run `/energy-compliance` to review FERC/NERC regulatory compliance for energy trading."
- "Run `/fraud-detection` to evaluate trade surveillance and market manipulation detection."
- "Run `/security-review` to audit trading platform APIs and access controls."
- "Run `/financial-compliance` to review broader financial regulatory requirements."

============================================================
DO NOT
============================================================

- Do NOT modify any pricing models, risk parameters, or trading limits — this is an analysis skill.
- Do NOT execute trades, submit orders, or interact with exchange APIs.
- Do NOT access or display actual trade data, counterparty names, or portfolio positions.
- Do NOT expose pricing model parameters, VaR figures, or limit thresholds that are commercially sensitive.
- Do NOT skip regulatory reporting analysis even for internal or proprietary trading systems.
- Do NOT assume model accuracy without checking backtesting and validation results.
- Do NOT conflate theoretical model outputs with production calibrated results — verify calibration.
