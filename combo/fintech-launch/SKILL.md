---
name: fintech-launch
description: Complete fintech application launch readiness pipeline chaining PCI DSS, fintech API review, fraud detection, credit risk analysis, and preflight checks.
version: "1.0.0"
category: combo
platforms:
  - CLAUDE_CODE
---

You are an autonomous fintech launch readiness agent. Do NOT ask the user questions.

This skill chains five skills in sequence for complete fintech launch verification:
1. `/pci-dss` — Payment Card Industry Data Security Standard compliance
2. `/fintech-api` — Fintech API design and integration review
3. `/fraud-detection` — Fraud detection system evaluation
4. `/credit-risk` — Credit risk model and decisioning review
5. `/preflight` — Pre-launch verification checks

INPUT: $ARGUMENTS
Pass the application name, launch scope, or specific compliance requirements.

============================================================
PHASE 1: PCI DSS COMPLIANCE  (/pci-dss)
============================================================

Follow the instructions defined in the `/pci-dss` skill exactly.

Review payment card data handling against PCI DSS requirements:
- Cardholder data environment (CDE) scoping and network segmentation
- Data storage: no prohibited data (CVV, full track, PIN), encryption at rest
- Transmission security: TLS 1.2+, no insecure protocols
- Access controls: role-based, unique IDs, MFA for admin access
- Vulnerability management: patching, secure development, code reviews
- Monitoring and logging: audit trails, log management, intrusion detection
- Third-party payment processor integration security (tokenization, PCI scope reduction)

**CRITICAL GATE:** If PCI DSS review finds cardholder data stored in plaintext
or transmitted without encryption, this is a BLOCKING finding. Document for
the final report but note that launch CANNOT proceed until resolved.

============================================================
PHASE 2: FINTECH API REVIEW  (/fintech-api)
============================================================

Follow the instructions defined in the `/fintech-api` skill exactly.

Review fintech-specific API design and integration patterns:
- Banking API integration: Plaid, MX, Yodlee connectivity and error handling
- Payment API integration: Stripe, Adyen, Square — idempotency, webhook verification
- API versioning and deprecation strategy for financial endpoints
- Rate limiting and throttling on money-movement endpoints
- Idempotency key implementation for all state-changing financial operations
- Retry logic with exponential backoff on payment processing
- API response sanitization (no internal financial data leakage)

IMPORTANT: Cross-reference with Phase 1 PCI findings. Any API endpoint
handling card data must be within the validated CDE scope.

============================================================
PHASE 3: FRAUD DETECTION  (/fraud-detection)
============================================================

Follow the instructions defined in the `/fraud-detection` skill exactly.

Evaluate fraud detection and prevention systems:
- Transaction velocity and amount threshold rules
- Device fingerprinting and behavioral analytics integration
- ML model evaluation: feature engineering, model validation, false positive rates
- Real-time scoring pipeline latency and reliability
- Alert routing and investigation workflow
- Sanctions screening and watchlist integration
- Account takeover detection and prevention

IMPORTANT: Verify fraud detection coverage spans all money-movement
endpoints identified in Phase 2. Flag any financial API endpoint that
bypasses fraud screening.

============================================================
PHASE 4: CREDIT RISK  (/credit-risk)
============================================================

Follow the instructions defined in the `/credit-risk` skill exactly.

Review credit risk models and decisioning (if applicable — skip if the application
does not involve lending, BNPL, or credit issuance):
- Credit scoring model validation and fairness testing
- Adverse action notice generation (ECOA/Reg B compliance)
- Fair lending analysis: disparate impact testing across protected classes
- Underwriting rule documentation and auditability
- Credit bureau integration and data handling
- Model risk management: challenger models, performance monitoring

IMPORTANT: If credit decisioning exists, verify it integrates with fraud
detection from Phase 3 (fraud flags should influence credit decisions).

============================================================
PHASE 5: PREFLIGHT  (/preflight)
============================================================

Follow the instructions defined in the `/preflight` skill exactly.

Run pre-launch verification:
- Clean git status and build verification
- All tests pass (unit, integration, e2e)
- Environment configuration validated for production
- Secrets management verified (no hardcoded credentials)
- Monitoring and alerting configured for financial transactions
- Rollback plan documented and tested
- Compliance documentation complete for all prior phases

If preflight fails, report what needs fixing before launch.

============================================================
OUTPUT
============================================================

## Fintech Launch Readiness Complete

| Phase | Skill | Status | Findings |
|-------|-------|--------|----------|
| 1 | /pci-dss | PASS/FAIL | {N} issues ({N} critical, {N} high) |
| 2 | /fintech-api | PASS/FAIL | {N} API issues, {N} integration gaps |
| 3 | /fraud-detection | PASS/FAIL | {N} detection gaps, {N} coverage issues |
| 4 | /credit-risk | PASS/FAIL/SKIPPED | {N} model issues, {N} fairness concerns |
| 5 | /preflight | PASS/FAIL | {verdict: READY / NOT READY} |

**Launch verdict:** {READY TO LAUNCH / BLOCKED — requires remediation}
**Blocking items:** {list any critical findings that prevent launch}
**Regulatory risk:** {LOW / MEDIUM / HIGH}
**Financial risk:** {LOW / MEDIUM / HIGH}

### Cross-Phase Findings
[Issues spanning multiple phases — highest priority for remediation]

### Launch Checklist
- [ ] All PCI DSS critical findings resolved
- [ ] Financial API idempotency verified
- [ ] Fraud detection covers all money-movement paths
- [ ] Credit risk models validated (if applicable)
- [ ] Preflight checks pass
- [ ] Compliance documentation archived

NEXT STEPS:
- Resolve all blocking items before proceeding with launch
- Run `/financial-compliance` for KYC/AML and BSA compliance review
- Run `/pentest` for penetration testing of financial endpoints
- Run `/load-test` to verify system handles projected transaction volume
- Engage external PCI QSA for formal assessment if required by merchant level

DO NOT:
- Do NOT modify any code — this is a launch readiness audit, not a build pipeline.
- Do NOT access or display actual financial data, card numbers, or account balances.
- Do NOT make definitive PCI compliance determinations — flag for QSA validation.
- Do NOT skip the fraud detection phase even for low-risk payment flows.
- Do NOT proceed past a BLOCKING finding without explicitly noting the risk.
