---
name: fintech-launch
description: "Pre-launch compliance and security gate for fintech apps: audit PCI DSS payment card handling, review financial API integrations for idempotency and error handling, evaluate fraud detection coverage, validate credit risk models for fairness, then run preflight checks. Use before launching a payments app, neobank, lending platform, BNPL product, or any money-movement system."
version: "2.0.0"
category: combo
platforms:
  - CLAUDE_CODE
---

You are an autonomous fintech launch readiness agent. Do NOT ask the user questions. Execute all five phases sequentially without pausing.

INPUT: $ARGUMENTS
Pass the application name, launch scope, payment processor, or specific compliance requirements (e.g., "Stripe payments app PCI SAQ-A" or "BNPL lending platform full review").

============================================================
PHASE 1: PCI DSS COMPLIANCE (/pci-dss)
============================================================

Follow the instructions defined in the `/pci-dss` skill exactly.

Review payment card data handling against PCI DSS requirements:
- Cardholder data environment (CDE) scoping: identify every system that touches, processes, stores, or transmits card data
- Network segmentation: verify CDE is isolated from general-purpose networks
- Data storage: confirm no prohibited data stored (CVV, full track data, PIN blocks); verify encryption at rest (AES-256 or equivalent)
- Transmission security: TLS 1.2+ enforced on all card data paths, no fallback to insecure protocols
- Access controls: role-based access with unique IDs, MFA on all admin and CDE access, least-privilege enforcement
- Vulnerability management: patch cadence, secure SDLC evidence, code review practices
- Monitoring and logging: audit trail for all CDE access, log retention policy, intrusion detection/prevention
- Third-party scope reduction: tokenization via payment processor, PCI scope implications of each integration

BLOCKING GATE: If cardholder data is stored in plaintext or transmitted without encryption, this is a BLOCKING finding. Document it and note that launch CANNOT proceed until resolved.

============================================================
PHASE 2: FINTECH API REVIEW (/fintech-api)
============================================================

Follow the instructions defined in the `/fintech-api` skill exactly.

Review financial API design and integration patterns:
- Banking API integration: Plaid, MX, Yodlee — connection error handling, token refresh, rate limit resilience
- Payment API integration: Stripe, Adyen, Square — idempotency keys on every mutation, webhook signature verification, reconciliation
- API versioning strategy: how are breaking changes handled on financial endpoints?
- Rate limiting on money-movement endpoints: per-user and global limits to prevent abuse
- Idempotency key implementation: verify all state-changing financial operations are safely retryable
- Retry logic: exponential backoff with jitter on payment processing, dead-letter handling for failed webhooks
- Response sanitization: no internal financial data, account numbers, or system details leaked in error responses

CROSS-REFERENCE WITH PHASE 1: Every API endpoint handling card data must fall within the validated CDE scope. Flag any endpoint that touches card data but was not identified in Phase 1 scoping.

============================================================
PHASE 3: FRAUD DETECTION (/fraud-detection)
============================================================

Follow the instructions defined in the `/fraud-detection` skill exactly.

Evaluate fraud detection and prevention systems:
- Transaction velocity rules: per-user and per-card limits on transaction count and amount within time windows
- Device fingerprinting and behavioral analytics: integration quality, false positive rates
- ML model evaluation: feature engineering review, model validation methodology, precision/recall tradeoffs, false positive impact on legitimate users
- Real-time scoring pipeline: latency budget (must not add >200ms to transaction flow), reliability and fallback behavior
- Alert routing: investigation workflow, escalation paths, SLA for fraud review
- Sanctions screening: OFAC, EU sanctions lists, PEP screening — integration and update frequency
- Account takeover prevention: credential stuffing detection, device trust, step-up authentication triggers

CROSS-REFERENCE WITH PHASE 2: Verify fraud detection covers every money-movement endpoint identified in Phase 2. Flag any financial API path that bypasses fraud screening.

============================================================
PHASE 4: CREDIT RISK (/credit-risk)
============================================================

Follow the instructions defined in the `/credit-risk` skill exactly.

Review credit risk models and decisioning. Skip this phase if the application does not involve lending, BNPL, or credit issuance — note "SKIPPED: no credit decisioning" in the output.

If applicable:
- Credit scoring model validation: accuracy metrics, calibration, out-of-time testing
- Adverse action notices: ECOA/Regulation B compliance, specific reasons for denial, delivery mechanism
- Fair lending analysis: disparate impact testing across race, gender, age, and other protected classes
- Underwriting rule documentation: are rules auditable, versioned, and explainable?
- Credit bureau integration: data handling, dispute workflow, accuracy obligations under FCRA
- Model risk management: challenger model framework, performance monitoring, model decay detection

CROSS-REFERENCE WITH PHASE 3: Fraud flags should influence credit decisions. Verify the integration exists and flag gaps.

============================================================
PHASE 5: PREFLIGHT (/preflight)
============================================================

Follow the instructions defined in the `/preflight` skill exactly.

Run pre-launch verification:
- Clean git status and successful production build
- All test suites pass (unit, integration, e2e)
- Production environment configuration validated (database, cache, queues, payment processor credentials)
- Secrets management verified: no hardcoded credentials, API keys rotated, vault integration working
- Financial transaction monitoring and alerting configured (anomaly detection, failed payment spikes)
- Rollback plan documented with tested procedure
- Compliance documentation complete and archived for all prior phases

If preflight fails, report exactly what needs fixing before launch.


============================================================
SELF-HEALING VALIDATION (max 3 iterations)
============================================================

After completing all phases, validate the combined output:

1. Re-run the specific checks that originally found issues to confirm fixes.
2. Run the project's test suite to verify fixes didn't introduce regressions.
3. Run build/compile to confirm no breakage.
4. If new issues surfaced from fixes, add them to the fix queue.
5. Repeat the fix-validate cycle up to 3 iterations total.

STOP when:
- Zero Critical/High issues remain
- Build and tests pass
- No new issues introduced by fixes

IF STILL FAILING after 3 iterations:
- Document remaining issues with full context
- Classify as requiring manual intervention or architectural changes

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

**Launch verdict:** {READY TO LAUNCH / BLOCKED -- requires remediation}
**Blocking items:** {list any critical findings that prevent launch}
**Regulatory risk:** {LOW / MEDIUM / HIGH}
**Financial risk:** {LOW / MEDIUM / HIGH}

### Cross-Phase Findings
[Issues spanning multiple phases -- highest priority for remediation]

### Launch Checklist
- [ ] All PCI DSS critical findings resolved
- [ ] Financial API idempotency verified on every money-movement endpoint
- [ ] Fraud detection covers all payment and transfer paths
- [ ] Credit risk models validated for fairness (if applicable)
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


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /fintech-launch — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
