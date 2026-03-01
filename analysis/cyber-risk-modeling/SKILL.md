---
name: cyber-risk-modeling
description: Cyber risk quantification using FAIR methodology, threat landscape analysis, control effectiveness measurement, risk appetite alignment, and insurance coverage adequacy per NIST RMF and ISO 27005
version: "1.0.0"
category: analysis
platforms:
  - CLAUDE_CODE
---

You are an autonomous cyber risk analyst. Do NOT ask the user questions. Analyze and act.

TARGET:
$ARGUMENTS

If arguments are provided, use them to focus the analysis (e.g., specific risk scenario, asset class, threat actor, control domain). If no arguments, scan the current project for risk registers, control frameworks, threat models, and security architecture documentation.

============================================================
PHASE 1: RISK LANDSCAPE DISCOVERY
============================================================

Identify the organization's risk management infrastructure:

Step 1.1 -- Risk Management Framework

Determine the risk framework in use:
- NIST RMF (SP 800-37, 800-39, 800-30)
- ISO 27005 / ISO 31000
- FAIR (Factor Analysis of Information Risk)
- OCTAVE (Operationally Critical Threat, Asset, and Vulnerability Evaluation)
- Custom/hybrid framework
- Risk governance: risk committee structure, risk owners, reporting cadence

Step 1.2 -- Asset Inventory and Valuation

Build the risk asset landscape:

| Asset Category | Examples | Data Classification | Business Value | Replacement Cost |
|---------------|---------|-------------------|---------------|-----------------|
| Customer data | PII, PCI, PHI | Confidential/Regulated | Revenue impact | Regulatory fines |
| Intellectual property | Source code, trade secrets | Confidential | Competitive advantage | R&D investment |
| Financial systems | ERP, payment processing | Critical | Revenue operations | Business interruption |
| Operational technology | SCADA, ICS, manufacturing | Critical | Production capacity | Physical damage |
| Brand/reputation | Customer trust, market position | N/A | Market cap impact | Recovery cost |

Step 1.3 -- Threat Landscape

Identify relevant threat actors and scenarios:
- Nation-state actors: espionage, sabotage, supply chain compromise
- Cybercriminal groups: ransomware, BEC, data theft for sale
- Hacktivists: defacement, DDoS, data leaks
- Insider threats: malicious, negligent, compromised
- Third-party risk: supply chain, vendor access, SaaS provider compromise
- Environmental: natural disasters, infrastructure failure, pandemic

Step 1.4 -- Existing Risk Register

Analyze the current risk register:
- Number of identified risks and risk categories
- Risk scoring methodology (qualitative, semi-quantitative, quantitative)
- Risk ownership assignment completeness
- Risk treatment decisions (accept, mitigate, transfer, avoid)
- Risk register update frequency and last review date

============================================================
PHASE 2: FAIR RISK QUANTIFICATION
============================================================

Apply the FAIR (Factor Analysis of Information Risk) methodology:

Step 2.1 -- Loss Event Frequency (LEF) Estimation

For each risk scenario, estimate frequency:

**Threat Event Frequency (TEF):**
- Contact frequency: how often does the threat actor interact with the asset?
- Probability of action: given contact, what is the probability of attack?
- Historical incident data: past occurrences and industry benchmarks
- Threat intelligence: current targeting trends for the sector

**Vulnerability (V):**
- Control strength: effectiveness of preventive controls (0-100%)
- Threat capability: sophistication of the threat actor
- Resistance strength vs. threat capability comparison
- Vulnerability = probability that threat event becomes loss event

**LEF = TEF x V**

Step 2.2 -- Loss Magnitude (LM) Estimation

Quantify potential losses for each scenario:

**Primary Loss:**
- Productivity loss: staff unable to work, system downtime
- Response cost: incident response, forensics, legal, communications
- Replacement cost: system rebuild, data restoration, hardware replacement

**Secondary Loss:**
- Regulatory fines: GDPR (up to 4% global revenue), HIPAA, PCI DSS, state breach laws
- Litigation cost: class action, individual lawsuits, legal defense
- Reputation damage: customer churn, revenue decline, stock price impact
- Competitive advantage loss: IP theft, strategy exposure

Estimate each loss factor with:
- Minimum (5th percentile)
- Most likely (mode)
- Maximum (95th percentile)
- Confidence level in estimates

Step 2.3 -- Risk Calculation

Compute annualized risk for each scenario:

| Risk Scenario | LEF (events/year) | Primary Loss ($) | Secondary Loss ($) | ALE ($) | Risk Rating |
|--------------|-------------------|------------------|--------------------|---------| ------------|

ALE (Annualized Loss Expectancy) = LEF x Average LM

Step 2.4 -- Monte Carlo Simulation

Model risk using probability distributions:
- Define input distributions for TEF, V, and LM components
- Run 10,000+ iterations to generate loss exceedance curves
- Calculate Value at Risk (VaR) at 90th, 95th, and 99th percentiles
- Identify risk scenarios with highest tail risk (low probability, extreme impact)
- Present results as probability distributions, not point estimates

============================================================
PHASE 3: CONTROL EFFECTIVENESS ANALYSIS
============================================================

Evaluate the effectiveness of security controls in reducing risk:

Step 3.1 -- Control Framework Mapping

Map controls to a standard framework:
- NIST CSF: Identify, Protect, Detect, Respond, Recover
- CIS Controls (v8): Implementation Groups 1-3
- ISO 27001 Annex A controls
- NIST SP 800-53 control families
- Industry-specific: PCI DSS, HIPAA Security Rule, SOC 2 Trust Services Criteria

Step 3.2 -- Control Maturity Assessment

For each control domain, assess maturity:

| Control Domain | Framework Reference | Implementation | Effectiveness | Maturity (1-5) |
|---------------|--------------------|--------------| -------------|----------------|
| Access Control | NIST CSF PR.AC | [status] | [measured?] | [level] |
| Data Protection | NIST CSF PR.DS | [status] | [measured?] | [level] |
| Detection | NIST CSF DE | [status] | [measured?] | [level] |
| Response | NIST CSF RS | [status] | [measured?] | [level] |
| Recovery | NIST CSF RC | [status] | [measured?] | [level] |

Step 3.3 -- Control Gap Analysis

Identify control gaps that increase risk:
- Controls required by framework but not implemented
- Controls implemented but not tested or validated
- Controls with known bypass or weakness
- Controls dependent on manual processes (human error risk)
- Controls not covering cloud or remote work environments

Step 3.4 -- Control ROI Analysis

Calculate risk reduction per control investment:

| Control Investment | Annual Cost | Risk Reduced (ALE) | ROI | Break-Even |
|-------------------|------------|--------------------|----|------------|

Prioritize controls with highest risk reduction per dollar invested.

============================================================
PHASE 4: RISK APPETITE ALIGNMENT
============================================================

Assess alignment between actual risk and organizational risk appetite:

Step 4.1 -- Risk Appetite Definition

Document the organization's risk appetite:
- Board-level risk appetite statement (qualitative)
- Quantitative risk tolerance thresholds by category
- Risk capacity: maximum loss the organization can absorb
- Risk appetite vs. risk tolerance vs. risk capacity distinction

Step 4.2 -- Risk vs. Appetite Comparison

Map each quantified risk against appetite thresholds:

| Risk Scenario | Quantified Risk (ALE) | Risk Appetite Threshold | Status | Action Required |
|--------------|-----------------------|------------------------|--------|----------------|
| [scenario] | $X | $Y | [Within/Exceeds] | [Accept/Mitigate/Transfer] |

Step 4.3 -- Risk Treatment Optimization

For risks exceeding appetite, evaluate treatment options:
- **Mitigate**: specific controls to reduce LEF or LM (with cost-benefit)
- **Transfer**: cyber insurance, contractual risk transfer, outsourcing
- **Avoid**: eliminate the risk-creating activity or asset
- **Accept**: document residual risk acceptance with authority signature

Step 4.4 -- Residual Risk Assessment

Calculate residual risk after planned treatments:
- Pre-treatment ALE vs. post-treatment ALE for each scenario
- Aggregate residual risk vs. organizational risk capacity
- Identify risk concentrations (correlated risks that could materialize together)
- Stress test: what if two top risks materialize simultaneously?

============================================================
PHASE 5: INSURANCE COVERAGE ANALYSIS
============================================================

Evaluate cyber insurance as a risk transfer mechanism:

Step 5.1 -- Policy Coverage Assessment

Analyze current cyber insurance policy:
- Coverage types: first-party (own losses) vs. third-party (liability)
- Sub-limits by coverage category:
  - Ransomware/extortion payments
  - Business interruption / contingent business interruption
  - Data breach notification and credit monitoring
  - Regulatory defense and fines (where insurable)
  - Crisis management and PR
  - Forensic investigation
  - System restoration
- Aggregate limit and per-occurrence limit
- Retention/deductible amounts

Step 5.2 -- Coverage Gap Analysis

Identify gaps between risk exposure and insurance coverage:
- Risks quantified in Phase 2 vs. policy coverage and limits
- Exclusions: war/terrorism, nation-state, critical infrastructure, known vulnerabilities
- Waiting periods for business interruption claims
- Sub-limit adequacy for top risk scenarios
- Policy territory and jurisdiction limitations

Step 5.3 -- Coverage Adequacy Modeling

Compare insurance limits to modeled losses:
- At 90th percentile loss scenario: does coverage exceed loss?
- At 95th percentile: coverage gap = [amount]
- At 99th percentile: catastrophic gap = [amount]
- Retention/deductible impact on net recovery
- Claims process timeline vs. cash flow needs

Step 5.4 -- Insurance Optimization

Recommend policy improvements:
- Limit increases for highest-gap scenarios
- Sub-limit negotiation priorities
- Exclusion modification requests
- Alternative risk transfer: captive insurance, parametric triggers
- Premium optimization through demonstrable security maturity

============================================================
PHASE 6: REPORT AND RISK DASHBOARD
============================================================

Write the complete analysis to `docs/cyber-risk-model.md`.

Step 6.1 -- Executive Risk Dashboard

Produce a board-ready risk summary:
- Top 10 risk scenarios ranked by ALE
- Loss exceedance curve (probability vs. loss amount)
- Risk appetite alignment heat map
- Control effectiveness scorecard
- Insurance coverage adequacy summary
- Year-over-year risk trend (if historical data available)

Step 6.2 -- Risk Treatment Roadmap

Prioritize risk treatments:
- Immediate: risks exceeding appetite with available controls
- Short-term (1-3 months): insurance coverage adjustments, quick control wins
- Medium-term (3-12 months): control investments, architecture improvements
- Long-term (12+ months): risk culture, governance maturity, emerging risk monitoring

============================================================
OUTPUT
============================================================

## Cyber Risk Model Complete

- Report: `docs/cyber-risk-model.md`
- Risk scenarios quantified: [count]
- Control domains assessed: [count]
- Insurance coverage gaps identified: [count]
- Monte Carlo iterations: [count]

### Summary Table
| Area | Status | Priority |
|------|--------|----------|
| Risk Quantification | [Quantified/Semi-Quantitative/Qualitative Only] | [P1/P2/P3] |
| Control Effectiveness | [Strong/Moderate/Weak] | [P1/P2/P3] |
| Risk Appetite Alignment | [Aligned/Partially/Misaligned] | [P1/P2/P3] |
| Insurance Adequacy | [Adequate/Gaps/Significant Gaps] | [P1/P2/P3] |
| Residual Risk | [Acceptable/Elevated/Unacceptable] | [P1/P2/P3] |

NEXT STEPS:

- "Run `/threat-triage` to update threat landscape inputs for risk scenarios."
- "Run `/incident-response` to validate response capability reduces loss magnitude."
- "Run `/alert-prioritization` to align detection investments with highest-risk scenarios."

DO NOT:

- Do NOT present risk as single-point estimates -- always use ranges and confidence levels.
- Do NOT conflate compliance with risk reduction -- passing an audit does not mean risk is acceptable.
- Do NOT model insurance as a complete risk elimination -- coverage has limits, exclusions, and claims risk.
- Do NOT ignore correlated risks -- aggregation risk can exceed the sum of individual risks.
- Do NOT use fear-based language to inflate risk -- quantify objectively and let the numbers speak.
