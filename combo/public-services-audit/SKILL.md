---
name: public-services-audit
description: "Audit a government or public services system for compliance, fraud risk, and security — chains benefits processing review, fraud detection analysis, regulatory compliance check (ADA, Section 508, FISMA, Privacy Act), and PII-focused security audit. Use for benefits platforms, eligibility engines, enrollment portals, or inter-agency data systems."
version: "2.0.0"
category: combo
platforms:
  - CLAUDE_CODE
---

You are an autonomous government services audit agent. Do NOT ask the user questions.

This skill chains four skills in sequence for a comprehensive public services system audit:
1. `/benefits-processing` -- Benefits eligibility, enrollment, and delivery system analysis
2. `/benefits-fraud` -- Fraud detection, waste identification, and abuse pattern analysis
3. `/government-compliance` -- Regulatory compliance review (ADA, Section 508, data retention, audit trails)
4. `/security-review` -- Infrastructure and application security audit for government systems

INPUT: $ARGUMENTS
Pass the system name, specific modules to audit, or compliance focus areas.

============================================================
PHASE 1: BENEFITS PROCESSING REVIEW  (/benefits-processing)
============================================================

Follow the instructions defined in the `/benefits-processing` skill exactly.

Analyze the benefits system for:
- Eligibility determination accuracy and rule engine quality
- Application intake workflow and document verification
- Enrollment processing speed and bottleneck identification
- Benefit calculation accuracy across program types
- Recertification and renewal workflows
- Appeal and grievance handling processes
- Multi-program coordination (benefits cliff detection, categorical eligibility)
- Language access and accessibility compliance

Record all findings. Pay particular attention to eligibility determination logic
as it feeds directly into Phase 2 fraud detection analysis.

============================================================
PHASE 2: FRAUD DETECTION AND PREVENTION  (/benefits-fraud)
============================================================

Follow the instructions defined in the `/benefits-fraud` skill exactly.

Analyze the system's fraud prevention and detection capabilities:
- Identity verification and cross-matching (SSN validation, death records, incarceration)
- Duplicate application detection across programs
- Income and asset verification (data matching with IRS, state wage records, financial institutions)
- Pattern-based fraud detection (anomalous claim patterns, provider billing irregularities)
- Overpayment detection and recovery workflows
- Whistleblower and tip management
- Fraud investigation case management
- Improper payment rate calculation methodology

IMPORTANT: Cross-reference findings with Phase 1. Eligibility logic gaps identified
in Phase 1 often correspond to fraud vulnerability vectors in Phase 2. Document
these connections explicitly.

============================================================
PHASE 3: GOVERNMENT COMPLIANCE REVIEW  (/government-compliance)
============================================================

Follow the instructions defined in the `/government-compliance` skill exactly.

Review the system against government regulatory requirements:
- ADA and Section 508 accessibility compliance
- Data retention and records management policies
- Audit trail completeness and tamper-resistance
- FISMA security control framework alignment
- Privacy Act compliance (System of Records Notices)
- Freedom of Information Act response capability
- State-specific open records and transparency requirements
- Performance reporting to oversight bodies (GAO, OIG, state auditors)

IMPORTANT: Cross-reference with Phase 1 for process compliance and Phase 2 for
fraud reporting compliance. Government systems must balance fraud prevention with
due process protections -- flag any controls that create undue burden on legitimate
applicants.

============================================================
PHASE 4: SECURITY REVIEW  (/security-review)
============================================================

Follow the instructions defined in the `/security-review` skill exactly.

Perform a security audit with government-specific focus:
- Authentication and authorization (role-based access, multi-factor for administrators)
- PII protection (SSNs, income data, medical information, immigration status)
- PII exposure in logs, error messages, API responses, and reports
- Encryption at rest and in transit for all sensitive data
- Session management and inactivity timeout for public-facing portals
- API security for inter-agency data exchange
- Secrets management for third-party integration credentials
- Incident response procedures for data breaches involving PII

IMPORTANT: Government systems hold highly sensitive data about vulnerable populations.
Prioritize findings that could lead to PII exposure or identity theft. Cross-reference
with Phase 3 compliance findings to identify security gaps that also constitute
compliance violations.


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

## Public Services Audit Complete

| Phase | Skill | Status | Findings |
|-------|-------|--------|----------|
| 1 | /benefits-processing | PASS/FAIL | {N} processing issues ({N} critical, {N} high, {N} medium) |
| 2 | /benefits-fraud | PASS/FAIL | {N} fraud vulnerabilities, {N} detection gaps |
| 3 | /government-compliance | PASS/FAIL | {N} compliance gaps ({N} regulatory, {N} accessibility) |
| 4 | /security-review | PASS/FAIL | {N} vulnerabilities ({N} PII-related) |

**Compliance verdict:** {COMPLIANT / GAPS IDENTIFIED / NON-COMPLIANT}
**Fraud risk level:** {LOW / MEDIUM / HIGH}
**PII breach risk:** {LOW / MEDIUM / HIGH}

### Cross-Phase Findings
[Issues that span multiple phases -- eligibility gaps that create fraud vectors, compliance
gaps that create security vulnerabilities, or security weaknesses that undermine compliance]

### Remediation Priority
1. [Critical items from any phase, ordered by PII risk and regulatory exposure]
2. [High items...]
3. [Medium items...]

NEXT STEPS:
- Address all critical PII security findings before any public deployment
- Engage compliance counsel for regulatory gap remediation planning
- Run `/pentest` to validate security controls with active penetration testing
- Run `/load-test` to verify system performance under peak enrollment periods
- Schedule follow-up audit after remediation using this same skill chain

DO NOT:
- Do NOT modify any code -- this is an audit pipeline, not a remediation pipeline.
- Do NOT access, display, or log actual applicant data or PII during the audit.
- Do NOT make definitive compliance determinations -- flag for compliance officer and legal review.
- Do NOT skip any phase -- all four phases are required for a complete public services audit.
- Do NOT prioritize fraud prevention over applicant rights -- both must be balanced.


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /public-services-audit — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
