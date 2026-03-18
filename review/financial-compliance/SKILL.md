---
name: financial-compliance
description: "Audit fintech and financial services code for KYC/AML (CIP, CDD, EDD, sanctions screening, transaction monitoring), BSA (SAR/CTR filing, FinCEN reporting, Travel Rule), Reg E (EFT error resolution, unauthorized transfer liability, provisional credit), SOX (audit trails, segregation of duties, financial controls), GLBA (privacy notices, Safeguards Rule, data sharing), and state money transmitter licensing. Use when reviewing banking, payments, lending, crypto, neobank, BNPL, or embedded finance codebases."
version: "2.0.0"
category: review
platforms:
  - CLAUDE_CODE
---

You are in AUTONOMOUS MODE. Do NOT ask questions. Review every regulatory domain systematically.

TARGET:
$ARGUMENTS

If no arguments provided, review the entire financial services codebase in the current
working directory against all applicable regulations.

============================================================
PHASE 0: REGULATORY SCOPE DETECTION
============================================================

Auto-detect the financial services scope:

BUSINESS MODEL DETECTION:
- Identify the type of financial service: banking, lending, payments, money transfer,
  investment, insurance, cryptocurrency, BNPL, neobank, embedded finance
- Detect regulated activities: fund transfers, credit issuance, securities trading,
  money transmission, deposit taking, insurance underwriting
- Identify jurisdictions from configuration, legal entities, or licensing references
- Determine applicable regulatory framework based on business model

TECH STACK:
- Identify web framework, database, ORM, message queues, third-party integrations
- Identify identity verification services (Jumio, Onfido, Alloy, Persona, Plaid Identity)
- Identify sanctions screening services (Dow Jones, Refinitiv, ComplyAdvantage, Chainalysis)
- Identify transaction monitoring systems (custom, Actimize, Featurespace, Unit21)
- Identify reporting systems (FinCEN filings, state reports, SAR/CTR generation)

Produce a regulatory applicability matrix before proceeding.

============================================================
PHASE 1: KYC / AML COMPLIANCE
============================================================

Review Know Your Customer and Anti-Money Laundering implementation:

CUSTOMER IDENTIFICATION PROGRAM (CIP):
- Verify collection of required identification: name, date of birth, address, ID number
- Check identity verification against government databases or document verification
- Verify ID document validation (expiration, format, authenticity checks)
- Check for beneficial ownership collection for legal entities (25% threshold)
- Verify recordkeeping of identification information and verification methods
- Check for CIP exceptions handling (existing customers, regulated entities)

CUSTOMER DUE DILIGENCE (CDD):
- Verify risk rating assignment during onboarding (low, medium, high, prohibited)
- Check risk scoring factors: geography, product type, transaction volume, industry
- Verify ongoing monitoring adjusts risk rating based on activity
- Check for periodic re-verification schedules based on risk tier
- Verify CDD documentation retention (5-year minimum after account closure)

ENHANCED DUE DILIGENCE (EDD):
- Check for EDD triggers: high-risk customers, PEPs, high-risk jurisdictions
- Verify additional information collection for high-risk customers
- Check for source of funds / source of wealth verification
- Verify senior management approval for high-risk relationships
- Check for ongoing enhanced monitoring for EDD customers

SANCTIONS SCREENING:
- Verify OFAC SDN list screening on customer onboarding
- Check for ongoing sanctions screening (not just onboarding)
- Verify screening against all applicable lists (OFAC SDN, EU, UN, UK HMT)
- Check fuzzy matching logic and threshold configuration
- Verify match review workflow and false positive disposition
- Check for real-time screening on transactions (not just customer screening)
- Verify sanctions screening on counterparties and beneficiaries

TRANSACTION MONITORING:
- Check for suspicious activity detection rules
- Verify monitoring covers: structuring, rapid movement, unusual patterns, layering
- Check threshold calibration and tuning documentation
- Verify alert investigation workflow and escalation procedures
- Check for typology coverage (trade-based laundering, funnel accounts, etc.)
- Verify retroactive monitoring when customer risk changes

For each finding: regulatory reference, file path, severity, description, remediation.

============================================================
PHASE 2: BSA (BANK SECRECY ACT) COMPLIANCE
============================================================

Review BSA-specific requirements:

SUSPICIOUS ACTIVITY REPORTING:
- Verify SAR filing workflow exists for transactions > $5,000
- Check SAR narrative generation includes required elements (5 W's)
- Verify 30-day filing deadline tracking from initial detection
- Check for continuing activity SAR filing (90-day reviews)
- Verify SAR confidentiality (no tipping off)
- Check SAR data retention (5 years from filing)

CURRENCY TRANSACTION REPORTING:
- Verify CTR generation for cash transactions > $10,000
- Check for aggregate same-day cash transaction calculation
- Verify CTR e-filing integration with FinCEN BSA E-Filing
- Check for multiple transaction aggregation by customer
- Verify CTR exemption management for eligible businesses

RECORDKEEPING:
- Check that records of transactions > $3,000 are maintained
- Verify funds transfer recordkeeping (Travel Rule for transfers > $3,000)
- Check for 5-year retention of BSA records
- Verify records are retrievable within reasonable timeframe
- Check for purchase of monetary instruments > $3,000 records

BSA/AML PROGRAM ELEMENTS:
- Verify internal controls implementation in code
- Check for compliance officer designation references
- Verify training program references or requirements
- Check for independent audit/testing references

============================================================
PHASE 3: REGULATION E COMPLIANCE
============================================================

Review electronic fund transfer compliance:

DISCLOSURE REQUIREMENTS:
- Check for initial disclosures on EFT service enrollment
- Verify terms and conditions include required Reg E disclosures
- Check for change-in-terms notification implementation
- Verify periodic statement generation with required elements
- Check for receipt generation on electronic transfers

ERROR RESOLUTION:
- Verify error resolution workflow exists with required timelines:
  - 10 business days to investigate (20 for new accounts)
  - Provisional credit within 10 days if investigation extends
  - 45 calendar days maximum resolution (90 for certain transactions)
- Check that error reports trigger investigation workflow
- Verify consumer notification of investigation results
- Check for error correction and credit application logic

UNAUTHORIZED TRANSFERS:
- Verify unauthorized transfer liability limits:
  - $0 if reported before transfer
  - $50 if reported within 2 business days
  - $500 if reported within 60 days of statement
  - Unlimited after 60 days
- Check that liability calculation logic matches regulatory requirements
- Verify provisional credit implementation during investigation
- Check for fraud detection on consumer accounts

PREAUTHORIZED TRANSFERS:
- Check for consumer authorization requirements
- Verify stop payment capability and processing
- Check for notification of varying amount preauthorized transfers
- Verify right to stop payment is communicated

============================================================
PHASE 4: SOX (SARBANES-OXLEY) COMPLIANCE
============================================================

Review financial reporting controls in code:

FINANCIAL REPORTING CONTROLS:
- Check for data validation on financial calculations and reports
- Verify calculation accuracy (rounding, currency conversion, accrual logic)
- Check for reconciliation processes between systems
- Verify financial data cannot be modified without audit trail
- Check for approval workflows on financial adjustments

AUDIT TRAIL:
- Verify all financial data changes are logged with actor, timestamp, before/after values
- Check for immutable audit logs (append-only, no deletion)
- Verify audit log retention meets requirements (7-year minimum for SOX)
- Check that audit logs capture both successful and failed operations
- Verify audit log integrity protection (hashing, tamper detection)

SEGREGATION OF DUTIES:
- Check for role separation in financial workflows:
  - Initiator cannot approve their own transactions
  - Administrator cannot process financial transactions
  - Developers cannot deploy to production without approval
- Verify dual authorization for high-value operations
- Check for separation between transaction recording and reconciliation
- Verify access control enforces segregation in code

INTERNAL CONTROLS:
- Check for automated control points in financial processes
- Verify exception reporting when controls are bypassed
- Check for management override logging
- Verify control testing automation or hooks

============================================================
PHASE 5: GLBA (GRAMM-LEACH-BLILEY ACT) COMPLIANCE
============================================================

Review privacy and data protection:

PRIVACY NOTICES:
- Check for initial privacy notice delivery on account opening
- Verify annual privacy notice distribution mechanism
- Check that privacy notice content includes required elements:
  - Categories of information collected
  - Categories of information disclosed
  - Third parties receiving information
  - Consumer opt-out rights
- Verify opt-out mechanism implementation and processing
- Check for revised privacy notice when practices change

DATA SHARING CONTROLS:
- Verify data sharing with third parties respects opt-out elections
- Check for data sharing agreements referenced in code
- Verify exceptions to opt-out requirements (joint marketing, service providers)
- Check for third-party data use restrictions enforcement
- Verify data sharing logging and tracking

SAFEGUARDS RULE:
- Check for access controls protecting customer financial information
- Verify encryption of customer data at rest and in transit
- Check for data loss prevention measures
- Verify employee access is limited to business need
- Check for security incident response procedures
- Verify vendor management for third-party access to customer data

============================================================
PHASE 6: STATE MONEY TRANSMITTER COMPLIANCE
============================================================

Review state-level requirements:

LICENSE TRACKING:
- Check for state license tracking system or configuration
- Verify multi-state compliance (each state has different requirements)
- Check for license renewal tracking and alerting
- Verify surety bond amount tracking per state

STATE REPORTING:
- Check for state-specific reporting generation (quarterly, annual)
- Verify transaction volume reporting by state
- Check for complaint tracking and reporting mechanisms
- Verify state examination support (data export, record retrieval)

STATE-SPECIFIC REQUIREMENTS:
- Check for state-specific transaction limits
- Verify state-specific disclosure requirements
- Check for state-specific refund policies (California, New York have specific rules)
- Verify state-specific record retention requirements


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

## Financial Regulatory Compliance Review

**System:** [name/description]
**Business Model:** [detected financial service type]
**Stack:** [detected technologies]

### Regulatory Applicability

| Regulation | Applicable | Reason |
|------------|-----------|--------|
| KYC/AML | [YES/NO/PARTIAL] | [reason] |
| BSA | [YES/NO/PARTIAL] | [reason] |
| Reg E | [YES/NO/PARTIAL] | [reason] |
| SOX | [YES/NO/PARTIAL] | [reason] |
| GLBA | [YES/NO/PARTIAL] | [reason] |
| State MTL | [YES/NO/PARTIAL] | [reason] |

### Summary

| Regulation | Status | Findings | Critical |
|------------|--------|----------|----------|
| KYC/AML | [PASS/WARN/FAIL] | N | N |
| BSA | [PASS/WARN/FAIL] | N | N |
| Reg E | [PASS/WARN/FAIL] | N | N |
| SOX | [PASS/WARN/FAIL] | N | N |
| GLBA | [PASS/WARN/FAIL] | N | N |
| State MTL | [PASS/WARN/FAIL] | N | N |

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
[Ordered list by regulatory enforcement risk — KYC/AML and BSA first, then consumer protection]

============================================================
NEXT STEPS
============================================================

After reviewing the compliance findings:
- "Run `/credit-risk` to analyze credit decisioning models for fair lending compliance."
- "Run `/fraud-detection` to evaluate transaction monitoring and SAR processes."
- "Run `/pci-dss` to audit payment card data handling."
- "Run `/owasp` to check security posture of financial APIs."
- "Run `/analyze` to trace regulatory workflows end-to-end across the system."


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /financial-compliance — {{YYYY-MM-DD}}
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
- Do NOT make definitive legal or compliance determinations — flag issues for legal review.
- Do NOT access or display actual customer data (PII, financial records, account numbers).
- Do NOT skip any regulatory domain — review all applicable regulations.
- Do NOT assume compliance based on the presence of a library — verify implementation.
- Do NOT conflate best practices with legal requirements — clearly label each.
- Do NOT provide jurisdiction-specific legal advice — note requirements and recommend legal counsel.
