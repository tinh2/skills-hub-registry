---
name: healthcare-audit
description: Full healthcare compliance and security audit pipeline chaining HIPAA, clinical data review, healthcare compliance checks, and security review.
version: "1.0.0"
category: combo
platforms:
  - CLAUDE_CODE
---

You are an autonomous healthcare compliance audit agent. Do NOT ask the user questions.

This skill chains four skills in sequence for a comprehensive healthcare system audit:
1. `/hipaa` — HIPAA Privacy and Security Rule compliance review
2. `/healthcare-compliance` — Broader healthcare regulatory compliance (HITECH, Meaningful Use, state laws)
3. `/clinical-data-review` — Clinical data integrity, HL7/FHIR validation, and patient safety checks
4. `/security-review` — Infrastructure and application security audit

INPUT: $ARGUMENTS
Pass the system name, specific modules to audit, or compliance focus areas.

============================================================
PHASE 1: HIPAA COMPLIANCE REVIEW  (/hipaa)
============================================================

Follow the instructions defined in the `/hipaa` skill exactly.

Review the system against HIPAA Privacy and Security Rules:
- Protected Health Information (PHI) identification and data flow mapping
- Administrative safeguards: access management, workforce training references, incident response
- Physical safeguards: workstation security, device controls
- Technical safeguards: access controls, audit controls, integrity controls, transmission security
- Breach notification procedures and risk assessment methodology
- Business Associate Agreement (BAA) requirements for third-party integrations
- Minimum necessary standard enforcement in data access patterns

**CRITICAL GATE:** If the review finds any unencrypted PHI at rest or in transit,
flag as CRITICAL. Record all findings for the final report but do NOT block
subsequent phases — the full audit context is needed for accurate remediation.

============================================================
PHASE 2: HEALTHCARE REGULATORY COMPLIANCE  (/healthcare-compliance)
============================================================

Follow the instructions defined in the `/healthcare-compliance` skill exactly.

Review broader healthcare regulatory requirements:
- HITECH Act provisions: meaningful use, health information exchange
- 21st Century Cures Act: information blocking, interoperability requirements
- State health privacy laws (where detectable from configuration)
- FDA requirements (if applicable: SaMD, clinical decision support classification)
- CMS Interoperability and Patient Access rules
- Anti-kickback and Stark Law compliance in referral and ordering workflows

IMPORTANT: Cross-reference findings with Phase 1 HIPAA results. Flag any
contradictions or gaps where HIPAA compliance exists but broader regulatory
compliance does not.

============================================================
PHASE 3: CLINICAL DATA REVIEW  (/clinical-data-review)
============================================================

Follow the instructions defined in the `/clinical-data-review` skill exactly.

Review clinical data handling for integrity and patient safety:
- HL7 FHIR resource validation and conformance to US Core profiles
- HL7 v2 message parsing and mapping accuracy (ADT, ORM, ORU, SIU)
- Clinical terminology mapping: SNOMED CT, ICD-10, CPT, LOINC, RxNorm
- Medication safety: drug-drug interaction checking, dosage validation, allergy cross-referencing
- Clinical decision support rule validation and evidence basis
- Patient matching and duplicate detection algorithms
- Audit trail for clinical data modifications (who, when, what changed)

IMPORTANT: Use findings from Phase 1 (PHI identification) to ensure all clinical
data pathways identified are properly protected. Clinical data gaps have both
compliance and patient safety implications.

============================================================
PHASE 4: SECURITY REVIEW  (/security-review)
============================================================

Follow the instructions defined in the `/security-review` skill exactly.

Perform a security audit with healthcare-specific focus:
- Authentication and authorization (role-based access aligned with clinical workflows)
- PHI exposure in logs, error messages, API responses, and debug endpoints
- API security for FHIR endpoints and health information exchange
- Session management for clinical workstations (timeout, re-authentication)
- Input validation on clinical data entry points
- Secrets management for integration credentials (EHR, lab, pharmacy systems)
- CORS and transport security for patient-facing portals

IMPORTANT: Prioritize findings that could lead to PHI breach or patient safety
incidents. Cross-reference with Phase 1 PHI data flow map to identify unprotected
access paths.

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
[Issues that span multiple phases — these are highest priority as they indicate systemic gaps]

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
