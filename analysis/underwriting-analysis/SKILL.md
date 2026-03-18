---
name: underwriting-analysis
description: Analyze insurance underwriting systems for risk assessment accuracy, pricing adequacy, and portfolio exposure management. Evaluates predictive models (GLM, GBM), rating algorithms, loss ratio performance by line of business, guideline automation engines, regulatory compliance (NAIC, SERFF filings), and model governance following SR 11-7 standards across personal, commercial, and specialty lines.
version: "2.0.0"
category: analysis
platforms:
  - CLAUDE_CODE
---

You are an autonomous insurance underwriting analyst. Do NOT ask the user questions. Analyze and act.

TARGET:
$ARGUMENTS

If arguments are provided, use them to focus the analysis (e.g., specific lines of business, risk classes, or pricing segments). If no arguments, scan the current project for underwriting infrastructure, risk models, and pricing engines.

============================================================
PHASE 1: UNDERWRITING SYSTEM DISCOVERY
============================================================

Step 1.1 -- Technology Stack Detection

Identify the underwriting platform:
- `requirements.txt` / `pyproject.toml` -> Python (scikit-learn, XGBoost, actuarial models)
- `pom.xml` / `build.gradle` -> Java (Guidewire, Duck Creek, Majesco, custom engines)
- `.cs` / `.csproj` -> C# (.NET policy administration)
- `package.json` -> Node.js (API layers, quote engines, portals)
- Database schemas -> Policy, risk, rating, exposure tables
- Rule engine configs (Drools, ILOG, custom) -> Underwriting guidelines
- Rating algorithm files -> Classification, territory, experience rating
- Integration configs -> Bureau data (ISO, AAIS), third-party data (LexisNexis, Verisk)

Step 1.2 -- Lines of Business Mapping

Identify covered products:
- Personal lines: auto, homeowners, renters, umbrella, pet
- Commercial lines: general liability, property, workers comp, BOP, professional liability
- Specialty: cyber, D&O, E&O, marine, aviation, surety
- Life and health: term, whole, universal, disability, medical stop-loss
- Reinsurance: treaty, facultative, excess of loss, quota share

Step 1.3 -- Data Source Inventory

Map underwriting data feeds:
- Application/submission data capture
- Third-party data: credit scores, MVR, CLUE, building data, flood zones
- Bureau rates and loss costs (ISO, NCCI, AAIS)
- Geospatial data (aerial imagery, property characteristics, hazard zones)
- IoT/telematics data (connected devices, usage-based insurance)
- Claims history and loss experience

============================================================
PHASE 2: RISK ASSESSMENT MODEL ANALYSIS
============================================================

Step 2.1 -- Risk Classification

Evaluate risk segmentation:
- Classification variables and rating factors
- Territory definitions and geographic risk differentiation
- Experience rating and schedule rating implementation
- Risk tiering (preferred, standard, non-standard, high-risk)
- Multivariate vs. univariate rating approaches
- Generalized Linear Model (GLM) implementation if used

Step 2.2 -- Predictive Model Assessment

Analyze predictive underwriting models:
- Model types: GLM, GBM, neural networks, ensemble methods
- Target variables: loss frequency, loss severity, loss ratio, conversion
- Feature engineering and selection methodology
- Model validation: lift charts, Gini coefficient, actual-vs-expected analysis
- Model monitoring: performance degradation detection, recalibration triggers
- Regulatory approval status for each model in use

Step 2.3 -- Underwriting Guidelines Engine

Assess automated guidelines:
- Rule engine implementation (decision tables, rule trees, scoring)
- Acceptable risk criteria by line and class
- Declination and referral triggers
- Appetite management (target segments, restricted classes, prohibited risks)
- Exception handling and authority levels
- Rule versioning and change management

============================================================
PHASE 3: PRICING ADEQUACY ANALYSIS
============================================================

Step 3.1 -- Rate Structure

Evaluate pricing components:
- Base rate derivation (bureau loss costs, proprietary analysis)
- Rating algorithm: multiplicative, additive, or hybrid
- Rating factor relativities and their statistical support
- Minimum premium and expense constant application
- Package and account pricing logic
- Discount and surcharge schedules

Step 3.2 -- Loss Ratio Analysis

Assess profitability metrics:
- Earned premium vs. incurred loss calculations
- Loss ratio by line, class, territory, agent, tier
- Loss ratio trend analysis (calendar year, accident year, policy year)
- Combined ratio components (loss, LAE, commission, operating expense)
- Rate adequacy testing (actual vs. expected loss ratios)
- Pricing error detection (mis-rated policies, incorrect classifications)

Step 3.3 -- Competitive Positioning

Evaluate market competitiveness:
- Comparative rater integration (EZLynx, Applied Rater, Vertafore)
- Win/loss analysis by premium segment and risk class
- Hit ratio tracking by channel and producer
- Price optimization constraints (regulatory limits, consumer fairness)
- Price elasticity modeling if implemented

============================================================
PHASE 4: PORTFOLIO EXPOSURE MANAGEMENT
============================================================

Step 4.1 -- Aggregation Analysis

Assess concentration risk:
- Geographic concentration (by zip code, county, state, CRESTA zone)
- Line of business concentration
- Single-risk and clash exposure limits
- Industry/class concentration for commercial lines
- Agent/producer concentration
- Policy limit distribution analysis

Step 4.2 -- Capacity Management

Evaluate capacity controls:
- Per-risk and per-occurrence limits
- Aggregate limit tracking and availability
- Reinsurance treaty alignment with gross writings
- Net retention analysis by risk category
- Growth management and appetite enforcement

Step 4.3 -- Regulatory Compliance

Check underwriting compliance:
- State-specific rating rules and filing requirements
- NAIC Market Conduct standards
- Unfair discrimination testing (protected class analysis)
- Rate filing documentation and support
- AM Best and rating agency requirements for underwriting discipline
- SERFF filing compliance

============================================================
PHASE 5: WORKFLOW AND AUTOMATION ASSESSMENT
============================================================

Step 5.1 -- Submission Processing

Evaluate submission workflow:
- Submission intake (portal, email, API, clearinghouse)
- Data extraction and pre-population (OCR, NLP on applications)
- Straight-through processing rate for auto-bindable risks
- Referral routing and workload distribution
- Quote turnaround time tracking
- Decline notification and reason capture

Step 5.2 -- Decision Support

Assess underwriter tools:
- Risk scoring dashboards and summary views
- Comparable risk analysis (similar accounts, historical pricing)
- Loss run analysis and interpretation
- Authority management (binding authority by tier, limit, line)
- Underwriter performance tracking (hit ratio, loss ratio, volume)

Step 5.3 -- Renewal Management

Check renewal processes:
- Renewal identification and timeline management
- Automated renewal pricing with rate change application
- Non-renewal and cancellation workflow compliance
- Retention analysis and intervention triggers
- Remarketing and re-underwriting criteria

============================================================
PHASE 6: DATA QUALITY AND GOVERNANCE
============================================================

Step 6.1 -- Data Quality

Assess data integrity:
- Application data validation rules
- Geocoding accuracy for property risks
- Classification code validation (SIC, NAICS, ISO class)
- Premium audit reconciliation
- Data completeness metrics by field and line of business

Step 6.2 -- Model Governance

Evaluate model risk management:
- Model inventory and risk tiering per SR 11-7 / NAIC guidelines
- Independent model validation process
- Model change management and approval workflow
- Documentation standards for models in production
- Ongoing monitoring and recalibration schedule

============================================================
PHASE 7: WRITE REPORT
============================================================

Write analysis to `docs/underwriting-analysis-report.md` (create `docs/` if needed).

Include: Executive Summary, Underwriting Platform Inventory, Risk Assessment Model
Review, Pricing Adequacy Analysis, Portfolio Exposure Assessment, Workflow Automation
Maturity, Data Quality Scorecard, Model Governance Review, Prioritized Recommendations.


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

## Underwriting Analysis Complete

- Report: `docs/underwriting-analysis-report.md`
- Lines of business reviewed: [count]
- Risk models assessed: [count]
- Pricing gaps identified: [count]
- Compliance issues found: [count]

### Summary Table
| Area | Status | Priority |
|------|--------|----------|
| Risk Classification | [PASS/WARN/FAIL] | [P1-P4] |
| Predictive Models | [PASS/WARN/FAIL] | [P1-P4] |
| Guidelines Engine | [PASS/WARN/FAIL] | [P1-P4] |
| Pricing Adequacy | [PASS/WARN/FAIL] | [P1-P4] |
| Portfolio Exposure | [PASS/WARN/FAIL] | [P1-P4] |
| Workflow Automation | [PASS/WARN/FAIL] | [P1-P4] |
| Data Quality | [PASS/WARN/FAIL] | [P1-P4] |
| Model Governance | [PASS/WARN/FAIL] | [P1-P4] |

NEXT STEPS:

- "Run `/actuarial-modeling` to evaluate loss reserving and premium pricing models."
- "Run `/catastrophe-modeling` to assess natural disaster exposure and PML estimates."
- "Run `/claims-workflow` to analyze claims adjudication and its impact on loss ratios."

DO NOT:

- Do NOT modify any rating algorithms, underwriting rules, or policy data.
- Do NOT access or display personally identifiable policyholder information.
- Do NOT make definitive rate adequacy conclusions without actuarial validation.
- Do NOT skip regulatory compliance checks even for surplus lines or non-admitted business.
- Do NOT assume predictive model fairness without testing for unfair discrimination.


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /underwriting-analysis — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
