---
name: energy-compliance
description: "Audit energy utility software for NERC CIP cybersecurity, FERC market and tariff compliance, EPA emissions and CEMS reporting, renewable portfolio standards (RPS/REC tracking), pipeline safety (49 CFR 192/195), SCADA security, carbon market compliance, and state PUC/ISO/RTO requirements. Use when reviewing power generation, transmission, distribution, pipeline, renewable, EV charging, or energy trading codebases."
version: "2.0.0"
category: review
platforms:
  - CLAUDE_CODE
---

You are in AUTONOMOUS MODE. Do NOT ask questions. Review every regulatory domain systematically.

TARGET:
$ARGUMENTS

If no arguments provided, review the entire energy sector codebase in the current
working directory against all applicable regulations.

============================================================
PHASE 0: REGULATORY SCOPE DETECTION
============================================================

Auto-detect the energy sector scope:

BUSINESS MODEL DETECTION:
- Identify the type of energy operation: generation, transmission, distribution, retail,
  trading, pipeline, renewable development, energy storage, EV charging
- Detect regulated activities: bulk electric system operation, natural gas transmission,
  emissions monitoring, renewable energy credits, wholesale market participation
- Identify jurisdictions from configuration, licensing references, or NERC region identifiers
- Determine applicable regulatory framework based on business model

TECH STACK:
- Identify web framework, database, ORM, message queues, SCADA integration
- Identify NERC CIP compliance tools (asset management, access control, vulnerability scanning)
- Identify emissions monitoring systems (CEMS, emissions calculators, EPA reporting)
- Identify market systems (ISO/RTO interfaces, OASIS, eTariff)
- Identify pipeline SCADA and safety systems (leak detection, cathodic protection)

Produce a regulatory applicability matrix before proceeding.

============================================================
PHASE 1: NERC CIP CYBERSECURITY COMPLIANCE
============================================================

Review Critical Infrastructure Protection standards:

CIP-002: BES CYBER SYSTEM CATEGORIZATION:
- Check for BES Cyber System inventory and categorization (High, Medium, Low impact)
- Verify categorization criteria match NERC bright-line criteria
- Check for Electronic Access Control or Monitoring Systems (EACMS) identification
- Verify Physical Access Control Systems (PACS) identification
- Check for Protected Cyber Asset (PCA) identification
- Verify categorization review schedule (at least every 15 months)

CIP-005: ELECTRONIC SECURITY PERIMETERS:
- Check for Electronic Security Perimeter (ESP) definition and enforcement
- Verify all external routable connectivity passes through Electronic Access Points (EAPs)
- Check for inbound and outbound access permissions documentation
- Verify Interactive Remote Access requires multi-factor authentication
- Check for vendor remote access controls and session monitoring
- Verify ESP boundary protection for cloud-hosted BES Cyber Systems

CIP-007: SYSTEM SECURITY MANAGEMENT:
- Check for ports and services documentation (only required ports enabled)
- Verify security patch management process: evaluate within 35 days, apply or mitigate
- Check for malicious code prevention (antivirus, application whitelisting)
- Verify security event logging: login attempts, access control changes, detected malware
- Check for log retention (minimum 90 days online)
- Verify system access controls: unique user accounts, password complexity, account management

CIP-010: CONFIGURATION CHANGE MANAGEMENT:
- Check for baseline configuration documentation (OS, firmware, ports, patches, custom software)
- Verify change management process: test, approve, document before deployment
- Check for vulnerability assessment within 35 days of configuration change
- Verify active baseline comparison and drift detection
- Check for transient cyber asset and removable media management

CIP-011: INFORMATION PROTECTION:
- Check for BES Cyber System Information (BCSI) identification and protection
- Verify access authorization for BCSI
- Check for BCSI handling procedures (storage, transit, disposal)
- Verify data sanitization before device reuse or disposal

CIP-013: SUPPLY CHAIN RISK MANAGEMENT:
- Check for vendor risk assessment process in code/configuration
- Verify software integrity verification (hash validation, signature checking)
- Check for vendor remote access security controls
- Verify supply chain incident response procedures

For each finding: CIP standard reference, file path, severity, description, remediation.

============================================================
PHASE 2: FERC COMPLIANCE AND REPORTING
============================================================

Review Federal Energy Regulatory Commission requirements:

MARKET RULES AND TARIFFS:
- Check for tariff compliance in wholesale market participation logic
- Verify Open Access Same-Time Information System (OASIS) posting automation
- Check for Available Transfer Capability (ATC) calculation compliance
- Verify market manipulation prevention controls (anti-gaming provisions)
- Check for Electric Quarterly Report (EQR) data generation

TRANSMISSION PLANNING:
- Check for Order 1000 transmission planning process compliance
- Verify interconnection queue management against Order 2023 requirements
- Check for generator interconnection study automation (feasibility, system impact, facilities)
- Verify cost allocation methodology compliance
- Check for regional transmission planning data exchange

RELIABILITY STANDARDS:
- Check for mandatory reliability standard compliance tracking
- Verify event reporting automation (disturbance reports, system events)
- Check for compliance evidence generation and retention
- Verify self-assessment and internal compliance monitoring
- Check for mitigation plan tracking and implementation monitoring

RATE FILINGS:
- Check for rate schedule data management
- Verify formula rate update automation
- Check for cost-of-service calculation methodology
- Verify rate case data preparation and filing support

============================================================
PHASE 3: EPA EMISSIONS TRACKING
============================================================

Review environmental compliance for emissions:

CONTINUOUS EMISSIONS MONITORING (CEMS):
- Check for CEMS data acquisition and quality assurance (40 CFR Part 75)
- Verify calibration error test tracking (daily, quarterly, annual)
- Check for relative accuracy test audit (RATA) scheduling
- Verify missing data substitution procedures (Part 75 Subpart D)
- Check for hourly emissions data record completeness
- Verify heat input calculation methodology (fuel flow, stack flow)

EMISSIONS REPORTING:
- Check for Clean Air Markets Division (CAMD) electronic reporting
- Verify quarterly emissions report generation (Part 75)
- Check for annual compliance certification
- Verify Greenhouse Gas Reporting Program (40 CFR Part 98) data collection
- Check for criteria pollutant tracking: NOx, SO2, CO2, particulate matter
- Verify emissions allowance tracking and compliance demonstration

CLEAN AIR ACT COMPLIANCE:
- Check for Title IV Acid Rain Program allowance tracking
- Verify Cross-State Air Pollution Rule (CSAPR) compliance
- Check for Mercury and Air Toxics Standards (MATS) monitoring
- Verify New Source Review (NSR) / Prevention of Significant Deterioration (PSD) tracking
- Check for state implementation plan (SIP) requirement integration

CARBON MARKET COMPLIANCE:
- Check for carbon credit/offset tracking and verification
- Verify Regional Greenhouse Gas Initiative (RGGI) or state cap-and-trade compliance
- Check for carbon intensity calculation methodology
- Verify emissions verification and third-party audit support
- Check for voluntary carbon market reporting (CDP, SBTi alignment)

============================================================
PHASE 4: RENEWABLE PORTFOLIO STANDARDS AND CLEAN ENERGY
============================================================

Review renewable energy compliance:

RPS COMPLIANCE:
- Check for Renewable Portfolio Standard tracking by jurisdiction
- Verify Renewable Energy Certificate (REC) tracking and retirement
- Check for REC vintage and eligibility verification
- Verify compliance period calculations and banking/borrowing rules
- Check for Alternative Compliance Payment (ACP) calculation
- Verify RPS tier/class requirements (e.g., Class I solar, Class II renewable)

NET METERING:
- Check for net metering customer enrollment and tracking
- Verify net energy calculation methodology (monthly, annual true-up)
- Check for virtual net metering and community solar allocation
- Verify excess generation compensation calculation
- Check for net metering cap monitoring by program and jurisdiction

CLEAN ENERGY STANDARD:
- Check for clean energy percentage tracking
- Verify zero-emission credit (ZEC) program compliance
- Check for clean energy standard reporting generation
- Verify renewable energy procurement tracking
- Check for Inflation Reduction Act (IRA) tax credit qualification tracking

INTERCONNECTION COMPLIANCE:
- Check for DER interconnection application processing per state rules
- Verify IEEE 1547-2018 compliance verification in interconnection studies
- Check for hosting capacity analysis publication requirements
- Verify interconnection agreement management and milestone tracking

============================================================
PHASE 5: PIPELINE SAFETY (49 CFR 192/195)
============================================================

Review natural gas and hazardous liquid pipeline compliance:

INTEGRITY MANAGEMENT (49 CFR 192 Subpart O):
- Check for High Consequence Area (HCA) identification and documentation
- Verify integrity assessment method implementation (ILI, pressure testing, direct assessment)
- Check for assessment interval tracking (maximum 7 years for gas, 5 years for hazardous liquid)
- Verify threat identification and risk assessment methodology
- Check for remediation scheduling based on assessment findings
- Verify performance metrics tracking and trending

PIPELINE SAFETY MANAGEMENT (API RP 1173):
- Check for safety culture indicators and reporting
- Verify management of change (MOC) process in control system modifications
- Check for incident investigation and corrective action tracking
- Verify emergency response procedure management
- Check for stakeholder engagement documentation

LEAK DETECTION AND REPAIR:
- Check for computational pipeline monitoring (CPM) system implementation
- Verify leak detection sensitivity thresholds and alarm management
- Check for PHMSA reporting automation (incident, annual, safety-related condition)
- Verify cathodic protection monitoring data collection and compliance
- Check for excavation damage prevention (811/one-call) system integration

CONTROL ROOM MANAGEMENT (49 CFR 192.631):
- Check for SCADA alarm management and rationalization
- Verify controller fatigue management controls
- Check for operating procedure documentation and accessibility
- Verify shift handover documentation requirements
- Check for controller training and qualification tracking

============================================================
PHASE 6: STATE AND REGIONAL REQUIREMENTS
============================================================

Review state-specific energy regulatory requirements:

STATE PUC/PSC COMPLIANCE:
- Check for state public utility commission reporting requirements
- Verify rate case data preparation and filing automation
- Check for quality of service reporting (reliability metrics, customer complaints)
- Verify integrated resource planning (IRP) data management
- Check for energy efficiency program tracking and reporting

REGIONAL MARKET COMPLIANCE:
- Check for ISO/RTO market rule compliance (PJM, MISO, CAISO, ERCOT, ISO-NE, NYISO, SPP)
- Verify market settlement data reconciliation
- Check for demand response program compliance tracking
- Verify capacity market obligation tracking and reporting
- Check for ancillary services compliance documentation


============================================================
SELF-HEALING VALIDATION (max 2 iterations)
============================================================

After producing the review, validate completeness and consistency:

1. Verify all required output sections are present and non-empty.
2. Verify every finding references a specific file or code location.
3. Verify recommendations are actionable (not vague).
4. Verify severity ratings are justified by evidence.

IF VALIDATION FAILS:
- Identify which sections are incomplete or lack specificity
- Re-analyze the deficient areas
- Repeat up to 2 iterations

============================================================
OUTPUT
============================================================

## Energy Sector Regulatory Compliance Review

**System:** [name/description]
**Business Model:** [detected energy sector type]
**Stack:** [detected technologies]

### Regulatory Applicability

| Regulation | Applicable | Reason |
|------------|-----------|--------|
| NERC CIP | [YES/NO/PARTIAL] | [reason] |
| FERC | [YES/NO/PARTIAL] | [reason] |
| EPA Emissions | [YES/NO/PARTIAL] | [reason] |
| RPS/Clean Energy | [YES/NO/PARTIAL] | [reason] |
| Pipeline Safety | [YES/NO/PARTIAL] | [reason] |
| State PUC/PSC | [YES/NO/PARTIAL] | [reason] |

### Summary

| Regulation | Status | Findings | Critical |
|------------|--------|----------|----------|
| NERC CIP | [PASS/WARN/FAIL] | N | N |
| FERC | [PASS/WARN/FAIL] | N | N |
| EPA Emissions | [PASS/WARN/FAIL] | N | N |
| RPS/Clean Energy | [PASS/WARN/FAIL] | N | N |
| Pipeline Safety | [PASS/WARN/FAIL] | N | N |
| State PUC/PSC | [PASS/WARN/FAIL] | N | N |

### Detailed Findings

For each regulation with WARN or FAIL:

#### [Regulation Name]

| # | Severity | Reg Reference | File | Description | Remediation |
|---|----------|---------------|------|-------------|-------------|

### Compliance Gap Analysis
- **Missing workflows:** [list of required but unimplemented regulatory workflows]
- **Incomplete implementations:** [list of partially implemented requirements]
- **Documentation gaps:** [list of missing required documentation]

### Remediation Priority
[Ordered list by enforcement risk — NERC CIP penalties first, then FERC, EPA, pipeline safety]

============================================================
NEXT STEPS
============================================================

After reviewing the compliance findings:
- "Run `/grid-optimizer` to analyze grid operation systems referenced in compliance findings."
- "Run `/load-forecast` to evaluate forecasting accuracy for regulatory reporting."
- "Run `/commodity-pricing` to review energy trading compliance requirements."
- "Run `/security-review` to audit SCADA and control system cybersecurity."
- "Run `/pentest` to test critical infrastructure system defenses."


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /energy-compliance — {{YYYY-MM-DD}}
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

- Do NOT modify any code — this is a review skill, not a remediation skill.
- Do NOT make definitive legal or regulatory compliance determinations — flag issues for compliance review.
- Do NOT access or display actual operational data (SCADA values, meter readings, pipeline pressures).
- Do NOT expose critical infrastructure details (substation names, pipeline routes, control system IPs).
- Do NOT skip any regulatory domain — review all applicable regulations for the detected business model.
- Do NOT assume compliance based on the presence of a library or tool — verify implementation completeness.
- Do NOT provide jurisdiction-specific legal advice — note requirements and recommend regulatory counsel.
