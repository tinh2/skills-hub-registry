---
name: portfolio-optimizer
description: Analyze investment portfolio management software for allocation models, risk metrics, rebalancing logic, and performance attribution accuracy.
version: "1.0.0"
category: analysis
platforms:
  - CLAUDE_CODE
---

You are in AUTONOMOUS MODE. Do NOT ask questions. Analyze every component of the portfolio management system systematically.

TARGET:
$ARGUMENTS

If no arguments provided, analyze the entire portfolio management codebase in the current working directory.

============================================================
PHASE 0: SYSTEM DISCOVERY
============================================================

Auto-detect the portfolio management system architecture:

TECH STACK:
- `requirements.txt` / `pyproject.toml` -> Python (NumPy, SciPy, pandas, cvxpy, PyPortfolioOpt)
- `pom.xml` / `build.gradle` -> Java (QuantLib, custom engines)
- `package.json` -> Node.js (API layer, dashboard, client portal)
- `go.mod` -> Go (high-performance calculation engines)
- `*.r` / `*.R` -> R (statistical modeling, PerformanceAnalytics)
- `*.m` / `*.mat` -> MATLAB (quantitative finance, optimization)
- Jupyter notebooks (`*.ipynb`) -> Research and backtesting

SYSTEM COMPONENTS:
- Identify optimization engines: mean-variance, risk parity, factor models
- Identify risk calculation modules: VaR, CVaR, stress testing
- Identify rebalancing logic: triggers, constraints, execution
- Identify market data integrations: pricing feeds, reference data, corporate actions
- Identify performance measurement: return calculation, attribution, benchmarking
- Identify reporting: client statements, regulatory reports, compliance reports
- Identify order management: trade generation, execution, settlement

Produce a component inventory before proceeding.

============================================================
PHASE 1: ALLOCATION MODEL ANALYSIS
============================================================

Evaluate portfolio construction and optimization algorithms:

MODERN PORTFOLIO THEORY (MPT):
- Check mean-variance optimization implementation
- Verify efficient frontier calculation methodology
- Check covariance matrix estimation (sample, shrinkage, Ledoit-Wolf, factor-based)
- Verify expected return estimation method (historical, CAPM, Black-Litterman)
- Check for numerical stability in optimization (near-singular matrices, convergence)
- Verify optimization solver selection and configuration (cvxpy, scipy, quadprog)

BLACK-LITTERMAN MODEL:
- Check if prior (equilibrium) returns are derived from market capitalization
- Verify investor views incorporation methodology
- Check confidence level (tau, omega) parameterization
- Verify posterior distribution calculation accuracy
- Check for view consistency validation

RISK PARITY:
- Check equal risk contribution calculation methodology
- Verify risk budgeting implementation (if non-equal risk targets)
- Check for convergence of iterative risk parity algorithms
- Verify that risk parity respects portfolio constraints

CONSTRAINTS HANDLING:
- Check for regulatory constraints: concentration limits, asset class limits, sector limits
- Verify client-specific constraints: ESG exclusions, tax-lot restrictions, liquidity needs
- Check for turnover constraints to limit trading costs
- Verify cardinality constraints (min/max number of holdings)
- Check constraint feasibility validation before optimization
- Verify soft vs hard constraint distinction and penalty functions

NUMERICAL ACCURACY:
- Check floating-point precision handling in portfolio weights
- Verify weights sum to 1.0 (or target allocation) within tolerance
- Check for negative weight handling (short-selling constraints)
- Verify rounding logic for share-based portfolios
- Check for cash residual handling after rounding

For each finding: file path, model component, severity, description, recommendation.

============================================================
PHASE 2: RISK METRICS EVALUATION
============================================================

Evaluate risk calculation accuracy and methodology:

VALUE AT RISK (VaR):
- Identify VaR methodology: historical simulation, parametric, Monte Carlo
- Check confidence level configuration (95%, 99%)
- Verify holding period specification and scaling
- Check for fat-tail handling (Student-t, Cornish-Fisher expansion)
- Verify backtesting of VaR predictions against actual losses
- Check for VaR exceptions tracking and reporting

CONDITIONAL VALUE AT RISK (CVaR / Expected Shortfall):
- Verify CVaR calculation methodology
- Check that CVaR is computed from the full loss distribution (not approximated)
- Verify CVaR is used as optimization objective where appropriate (subadditivity)
- Check for stress CVaR under adverse scenarios

PORTFOLIO RISK METRICS:
- Check Sharpe ratio calculation (risk-free rate source, annualization)
- Verify Sortino ratio implementation (downside deviation, MAR)
- Check maximum drawdown calculation (peak-to-trough, recovery tracking)
- Verify beta calculation (benchmark selection, regression methodology)
- Check tracking error calculation against benchmark
- Verify information ratio computation

STRESS TESTING:
- Check for historical stress scenario library (2008 GFC, COVID, rate shocks)
- Verify scenario application methodology (factor shocks, historical replay)
- Check for custom scenario creation capability
- Verify stress test results integration into risk reporting
- Check for reverse stress testing (what breaks the portfolio)

CORRELATION AND FACTOR ANALYSIS:
- Check correlation matrix estimation and updating frequency
- Verify factor model implementation (Fama-French, Barra, custom)
- Check for regime-dependent correlation handling
- Verify factor exposure calculation accuracy
- Check for tail dependence estimation beyond linear correlation

============================================================
PHASE 3: REBALANCING LOGIC REVIEW
============================================================

Evaluate portfolio rebalancing implementation:

THRESHOLD-BASED REBALANCING:
- Check drift calculation methodology (absolute vs relative)
- Verify threshold configuration per asset class or security
- Check for band-based rebalancing (inner/outer thresholds)
- Verify partial rebalancing logic (rebalance only drifted positions)
- Check for cascade effects (rebalancing one position triggers others)

CALENDAR-BASED REBALANCING:
- Check rebalancing schedule implementation (daily, monthly, quarterly)
- Verify trade date vs settlement date handling
- Check for market holiday awareness in scheduling
- Verify end-of-period vs start-of-period rebalancing logic

TAX-LOSS HARVESTING:
- Check for loss identification and harvesting triggers
- Verify wash sale rule compliance (30-day window, substantially identical)
- Check for replacement security selection logic
- Verify short-term vs long-term loss tracking
- Check for tax lot selection methodology (specific identification, FIFO, HIFO)
- Verify year-end tax-loss harvesting sweeps

EXECUTION OPTIMIZATION:
- Check for transaction cost modeling in rebalancing decisions
- Verify minimum trade size thresholds (avoid dust trades)
- Check for market impact estimation on large trades
- Verify trade netting across accounts (household-level optimization)
- Check for trade staging and prioritization logic

CONSTRAINTS DURING REBALANCING:
- Verify liquidity constraints are respected (illiquid positions not force-sold)
- Check for cash reserve maintenance during rebalancing
- Verify client restriction enforcement during trade generation
- Check for regulatory holding period requirements

============================================================
PHASE 4: PERFORMANCE ATTRIBUTION
============================================================

Evaluate performance measurement and attribution:

RETURN CALCULATION:
- Check time-weighted return (TWR) calculation methodology
- Verify money-weighted return (MWR/IRR) calculation for applicable contexts
- Check for cash flow timing handling (beginning vs end of period)
- Verify daily return chaining methodology
- Check for fee impact calculation (gross vs net returns)
- Verify currency return decomposition for international portfolios

BRINSON ATTRIBUTION:
- Check allocation effect calculation (sector/asset class weight differences)
- Verify selection effect calculation (security selection within sectors)
- Check interaction effect handling (combined allocation + selection)
- Verify arithmetic vs geometric attribution methodology
- Check for multi-period attribution compounding

FACTOR ATTRIBUTION:
- Check factor model specification for return decomposition
- Verify factor return estimation methodology
- Check for specific (idiosyncratic) return calculation
- Verify factor exposure stability over attribution period
- Check for attribution residual analysis

BENCHMARK HANDLING:
- Verify benchmark return calculation accuracy
- Check for benchmark composition tracking (rebalancing, reconstitution)
- Verify custom benchmark creation and blending
- Check for benchmark selection documentation and appropriateness
- Verify benchmark-relative statistics (alpha, tracking error, information ratio)

DATA FEED INTEGRATION:
- Check market data source reliability and redundancy
- Verify pricing methodology (close, mid, bid, ask)
- Check for corporate action handling (splits, dividends, mergers)
- Verify stale price detection and handling
- Check for market data validation and outlier detection

============================================================
PHASE 5: REGULATORY AND REPORTING
============================================================

Evaluate compliance and reporting accuracy:

REGULATORY LIMITS:
- Check for investment company concentration limits (40 Act for US funds)
- Verify diversification requirements enforcement
- Check for leverage limits and margin requirements
- Verify derivative exposure calculation and limits
- Check for UCITS/AIFMD constraints if applicable (EU funds)

CLIENT REPORTING:
- Check portfolio statement generation accuracy
- Verify performance reporting against GIPS standards where applicable
- Check for composite construction methodology
- Verify fee disclosure in client reports
- Check for risk disclosure adequacy

COMPLIANCE MONITORING:
- Check for pre-trade compliance checks
- Verify post-trade compliance monitoring
- Check for breach detection and alerting
- Verify compliance cure period handling
- Check for compliance reporting to regulators

============================================================
OUTPUT
============================================================

## Portfolio Optimization Analysis Report

**System:** [name/description]
**Stack:** [detected technologies]
**Portfolio Types:** [equity, fixed income, multi-asset, alternatives]

### Summary

| Category | Status | Findings | Critical |
|----------|--------|----------|----------|
| Allocation Models | [PASS/WARN/FAIL] | N | N |
| Risk Metrics | [PASS/WARN/FAIL] | N | N |
| Rebalancing Logic | [PASS/WARN/FAIL] | N | N |
| Performance Attribution | [PASS/WARN/FAIL] | N | N |
| Regulatory/Reporting | [PASS/WARN/FAIL] | N | N |

### Model Inventory

| Model | Type | Methodology | Constraints | Validation Status |
|-------|------|-------------|-------------|-------------------|

### Numerical Accuracy Findings

| Calculation | Expected | Implementation | Deviation | Impact |
|-------------|----------|----------------|-----------|--------|

### Detailed Findings

For each category with WARN or FAIL:

#### [Category Name]

| # | Severity | File | Description | Financial Impact | Recommendation |
|---|----------|------|-------------|------------------|----------------|

### Risk Metric Validation
- **VaR backtesting:** [results]
- **Return calculation accuracy:** [results]
- **Attribution residuals:** [results]

### Remediation Priority
[Ordered list by financial impact — calculation errors first, then compliance, then reporting]

============================================================
NEXT STEPS
============================================================

After reviewing the analysis:
- "Run `/financial-compliance` to review regulatory compliance for investment management."
- "Run `/credit-risk` to analyze fixed-income credit risk models in the portfolio."
- "Run `/owasp` to audit the portfolio management API and client portal."
- "Run `/arch-review` to evaluate system architecture for calculation performance."
- "Run `/qa` to verify calculation accuracy with test portfolios."

============================================================
DO NOT
============================================================

- Do NOT modify any model code, weights, or parameters — this is an analysis skill.
- Do NOT execute trades or modify portfolio positions.
- Do NOT access or display actual client portfolio data or account details.
- Do NOT provide investment advice or recommend specific portfolio allocations.
- Do NOT skip numerical accuracy checks — verify calculations against known formulas.
- Do NOT assume optimization convergence without checking solver output.
- Do NOT ignore edge cases in financial calculations (zero positions, negative prices, corporate actions).
