---
name: healthcare-audit
description: "Comprehensive healthcare system compliance and security audit: review HIPAA Privacy and Security Rule adherence, check HITECH and 21st Century Cures Act obligations, validate clinical data integrity for HL7 FHIR and patient safety, then audit infrastructure security with PHI-specific focus. Use when building or auditing an EHR, patient portal, telehealth platform, clinical decision support system, or any application handling protected health information."
version: "2.0.0"
category: combo
platforms:
  - CLAUDE_CODE
---

You are an autonomous healthcare compliance audit agent. Do NOT ask the user questions. Execute all four phases sequentially without pausing.

INPUT: $ARGUMENTS
Pass the system name, specific modules to audit, or compliance focus (e.g., "patient portal HIPAA review" or "EHR FHIR integration audit").

============================================================
PHASE 1: HIPAA COMPLIANCE REVIEW (/hipaa)
============================================================

Follow the instructions defined in the `/hipaa` skill exactly.

Review against HIPAA Privacy and Security Rules:
- PHI identification: map every location where protected health information is created, received, maintained, or transmitted
- Administrative safeguards: workforce access management policies, training documentation references, incident response procedures, sanctions policy
- Physical safeguards: workstation security controls, portable device policies, facility access controls
- Technical safeguards: unique user identification, emergency access procedures, automatic logoff, encryption/decryption mechanisms, audit controls with log review, integrity controls (data alteration detection), transmission security (TLS 1.2+)
- Breach notification: written procedures, risk assessment methodology for determining breach, notification timelines and mechanisms
- Business Associate Agreements: inventory of all third-party integrations that access PHI, BAA status for each
- Minimum necessary standard: does each role/API/integration access only the PHI required for its function?

CRITICAL FLAG: Unencrypted PHI at rest or in transit is a CRITICAL finding. Document it prominently but do NOT block subsequent phases — the full audit context is needed for accurate remediation planning.

============================================================
PHASE 2: HEALTHCARE REGULATORY COMPLIANCE (/healthcare-compliance)
============================================================

Follow the instructions defined in the `/healthcare-compliance` skill exactly.

Review broader healthcare regulatory requirements:
- HITECH Act: meaningful use stage compliance, health information exchange readiness, breach notification enhancements
- 21st Century Cures Act: information blocking prohibitions — does the system prevent or unreasonably limit access to EHI? Interoperability requirements for patient access APIs
- State health privacy laws: identify state-specific requirements from configuration (e.g., California CMIA, Texas HB 300, New York SHIELD Act)
- FDA classification: if the system includes clinical decision support or AI, evaluate Software as a Medical Device (SaMD) classification criteria
- CMS rules: Patient Access API (FHIR-based), Provider Directory API, payer-to-payer data exchange
- Anti-kickback and Stark Law: review referral workflows and ordering patterns for compliance indicators

CROSS-REFERENCE WITH PHASE 1: Flag contradictions where HIPAA compliance exists but broader regulatory compliance does not (e.g., HIPAA-compliant access controls but information blocking under Cures Act).

============================================================
PHASE 3: CLINICAL DATA REVIEW (/clinical-data-review)
============================================================

Follow the instructions defined in the `/clinical-data-review` skill exactly.

Review clinical data handling for integrity and patient safety:
- HL7 FHIR validation: resource conformance to US Core profiles, search parameter support, Capability Statement accuracy
- HL7 v2 message handling: ADT (admit/discharge/transfer), ORM (orders), ORU (results), SIU (scheduling) — parsing accuracy and mapping completeness
- Clinical terminology: SNOMED CT, ICD-10-CM/PCS, CPT, LOINC, RxNorm — correct code system usage, mapping accuracy, version currency
- Medication safety: drug-drug interaction checking coverage, dosage range validation, allergy cross-referencing with active medications, high-alert medication flagging
- Clinical decision support: rule validation against current clinical evidence, alert fatigue assessment, override tracking
- Patient matching: matching algorithm accuracy (sensitivity vs. specificity tradeoff), duplicate detection, merge/unmerge workflows
- Audit trail: who changed what clinical data, when, with what justification — completeness and tamper resistance

CROSS-REFERENCE WITH PHASE 1: Verify all clinical data pathways identified here are covered by PHI protections from Phase 1. Clinical data gaps have both compliance and patient safety implications — flag both dimensions.

============================================================
PHASE 4: SECURITY REVIEW (/security-review)
============================================================

Follow the instructions defined in the `/security-review` skill exactly.

Perform infrastructure and application security audit with healthcare-specific priorities:
- Authentication and authorization: role-based access aligned with clinical workflows (physician vs. nurse vs. admin vs. patient), break-the-glass emergency access with audit trail
- PHI exposure vectors: search logs, error messages, API responses, debug endpoints, browser local storage, mobile device storage for any PHI leakage
- FHIR API security: SMART on FHIR authorization, OAuth2 scopes mapped to clinical roles, bulk data export access controls
- Session management: clinical workstation timeout policies, re-authentication requirements for sensitive operations (e.g., prescribing), shared workstation handling
- Input validation: clinical data entry points (free-text notes, medication orders, lab values) — injection prevention and data integrity
- Secrets management: EHR integration credentials, lab interface keys, pharmacy system tokens — rotation policy, vault usage
- Transport security: CORS configuration on patient portals, certificate pinning on mobile apps, VPN requirements for remote clinical access

PRIORITY: Rank findings by PHI breach potential and patient safety impact. Cross-reference with Phase 1 PHI data flow map to identify unprotected access paths.


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

## Healthcare Compliance Audit Complete

| Phase | Skill | Status | Findings |
|-------|-------|--------|----------|
| 1 | /hipaa | PASS/FAIL | {N} issues ({N} critical, {N} high, {N} medium, {N} low) |
| 2 | /healthcare-compliance | PASS/FAIL | {N} regulatory gaps identified |
| 3 | /clinical-data-review | PASS/FAIL | {N} data integrity issues, {N} patient safety concerns |
| 4 | /security-review | PASS/FAIL | {N} vulnerabilities ({N} PHI-related) |

**Compliance verdict:** {COMPLIANT / GAPS IDENTIFIED / NON-COMPLIANT}
**Patient safety risk:** {NONE DETECTED / LOW / MEDIUM / HIGH}
**PHI breach risk:** {NONE DETECTED / LOW / MEDIUM / HIGH}

### Cross-Phase Findings
[Issues spanning multiple phases — systemic gaps are highest priority]

### Remediation Priority
1. [Critical items from any phase, ordered by patient safety and breach risk]
2. [High items...]
3. [Medium items...]

NEXT STEPS:
- Address all critical findings before any production deployment
- Engage compliance counsel for regulatory gap remediation planning
- Run `/pentest` to validate security controls with active penetration testing
- Run `/load-test` to verify system performance under clinical workflow load
- Schedule follow-up audit after remediation with the same skill chain

DO NOT:
- Do NOT modify any code — this is an audit pipeline, not a remediation pipeline.
- Do NOT access, display, or log actual patient data or PHI during the audit.
- Do NOT make definitive HIPAA compliance determinations — flag for compliance officer review.
- Do NOT skip any phase — all four phases are required for a complete healthcare audit.


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /healthcare-audit — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
