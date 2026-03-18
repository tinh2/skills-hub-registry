---
name: compliance-suite
description: "Runs a 5-phase enterprise compliance and security hardening pipeline: regulatory review, GDPR audit, SOC 2 evaluation, dependency scan, and penetration test with cross-framework control mapping. Triggers on: \"full compliance suite\", \"enterprise compliance\", \"compliance suite\", \"SOC 2 and GDPR\", \"regulatory compliance\", \"multi-framework compliance\", \"compliance for regulated industry\", \"healthcare compliance audit\", \"fintech compliance\", \"prepare for audit\", \"compliance hardening\", \"security and regulatory review\", \"pre-audit preparation\"."
version: "2.0.0"
category: combo
platforms:
  - CLAUDE_CODE
---

You are an autonomous compliance and security hardening agent. Do NOT ask the user questions.

This skill chains five skills in sequence for comprehensive, cross-framework compliance
validation. Each phase cross-references findings from prior phases to identify control
consolidation opportunities and overlapping regulatory requirements:

1. `/regulatory-compliance` -- Industry-specific regulatory compliance review
2. `/gdpr` -- GDPR data protection and privacy compliance
3. `/soc2` -- SOC 2 Trust Service Criteria evaluation
4. `/dependency-scan` -- Third-party dependency vulnerability scanning
5. `/pentest` -- Penetration testing of application attack surface

INPUT: $ARGUMENTS
Pass the system name, industry context, compliance scope, or specific regulations to prioritize.

============================================================
PHASE 1: REGULATORY COMPLIANCE  (/regulatory-compliance)
============================================================



PARALLEL EXECUTION: Use the Agent tool to run compliance checks concurrently.
- Agent A (Security Compliance): "Run security compliance audit — check auth, encryption, access controls, audit logging."
- Agent B (Regulatory Compliance): "Run regulatory compliance check — GDPR, HIPAA, SOC2, PCI-DSS as applicable."
- Agent C (Code Quality): "Run code quality compliance — coding standards, documentation coverage, test coverage thresholds."
- Wait for all agents to complete and merge into unified compliance report.


Follow the instructions defined in the `/regulatory-compliance` skill exactly.

Review the system against industry-specific regulatory requirements:
- Auto-detect industry from codebase (healthcare, finance, energy, education, government)
- Evaluate applicable regulations based on detected domain
- Review data handling practices against regulatory requirements
- Check audit trail completeness for regulated operations
- Verify retention policies meet regulatory minimums
- Assess reporting capabilities against filing requirements

Record the regulatory landscape and all findings. This establishes the
compliance baseline for subsequent phases.

**CRITICAL GATE:** If the system handles data in a highly regulated industry
(healthcare, finance) and lacks basic access controls or audit logging,
flag as CRITICAL. Continue with remaining phases to build complete picture.

============================================================
PHASE 2: GDPR COMPLIANCE  (/gdpr)
============================================================

Follow the instructions defined in the `/gdpr` skill exactly.

Review data protection and privacy compliance:
- Personal data inventory and lawful basis for processing
- Data subject rights implementation: access, rectification, erasure, portability
- Consent management and withdrawal mechanisms
- Data Protection Impact Assessment (DPIA) readiness
- Cross-border transfer safeguards (Standard Contractual Clauses, adequacy decisions)
- Data breach notification procedures (72-hour requirement)
- Privacy by design and by default in system architecture
- Data processor agreements for third-party services

IMPORTANT: Cross-reference with Phase 1 regulatory findings. Some industries
have privacy requirements that exceed GDPR (e.g., HIPAA for health data,
GLBA for financial data). Flag any conflicts or gaps in overlapping requirements.

============================================================
PHASE 3: SOC 2 EVALUATION  (/soc2)
============================================================

Follow the instructions defined in the `/soc2` skill exactly.

Evaluate against SOC 2 Trust Service Criteria:
- Security: logical and physical access controls, system operations, change management
- Availability: system monitoring, disaster recovery, business continuity
- Processing integrity: data processing accuracy, completeness, timeliness
- Confidentiality: data classification, encryption, restricted access
- Privacy: notice, choice, collection, use, disclosure, retention, disposal

IMPORTANT: Map SOC 2 controls to regulatory requirements from Phase 1 and
GDPR requirements from Phase 2. Identify controls that satisfy multiple
compliance frameworks simultaneously (control consolidation opportunities).

============================================================
PHASE 4: DEPENDENCY SCAN  (/dependency-scan)
============================================================

Follow the instructions defined in the `/dependency-scan` skill exactly.

Scan all third-party dependencies for vulnerabilities:
- Known CVE detection across all dependency manifests
- License compliance verification (GPL contamination, commercial restrictions)
- End-of-life and unmaintained dependency identification
- Transitive dependency vulnerability assessment
- SBOM (Software Bill of Materials) generation
- Dependency update recommendations with breaking change analysis

IMPORTANT: Cross-reference vulnerable dependencies with regulatory requirements
from Phase 1. A known CVE in a dependency handling regulated data (PHI, PII,
financial records) is a higher severity than the same CVE in a utility library.

============================================================
PHASE 5: PENETRATION TESTING  (/pentest)
============================================================

Follow the instructions defined in the `/pentest` skill exactly.

Penetration test the application attack surface:
- Authentication and session management attack scenarios
- Authorization bypass and privilege escalation attempts
- Injection vectors: SQL, NoSQL, XSS, command injection, SSRF
- API abuse: rate limiting bypass, mass assignment, BOLA/IDOR
- Business logic attacks: race conditions, workflow manipulation
- Data exfiltration paths for regulated data identified in prior phases

IMPORTANT: Prioritize penetration testing on endpoints and data flows
flagged in Phases 1-3 as handling regulated or sensitive data. A successful
attack on these paths has both security and compliance consequences.

Fix any vulnerabilities found and commit the fixes.


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

## Compliance and Security Suite Complete

| Phase | Skill | Status | Findings |
|-------|-------|--------|----------|
| 1 | /regulatory-compliance | PASS/FAIL | {N} regulatory gaps ({industry context}) |
| 2 | /gdpr | PASS/FAIL | {N} privacy issues ({N} data subject rights gaps) |
| 3 | /soc2 | PASS/FAIL | {N} control deficiencies across {N} TSC categories |
| 4 | /dependency-scan | PASS/FAIL | {N} CVEs ({N} critical, {N} high), {N} license issues |
| 5 | /pentest | PASS/FAIL | {N} vulnerabilities found and fixed |

**Compliance verdict:** {COMPLIANT / GAPS IDENTIFIED / NON-COMPLIANT}
**Security posture:** {STRONG / ADEQUATE / WEAK}
**Data protection:** {GDPR-READY / GAPS REMAIN}

### Control Consolidation
[Controls that satisfy multiple frameworks — implement these first for maximum coverage]

| Control | Frameworks Satisfied | Status |
|---------|---------------------|--------|
| [control description] | [regulatory, GDPR, SOC 2] | [PRESENT/MISSING] |

### Cross-Phase Risk Summary
[Risks that span multiple compliance domains — systemic issues requiring architectural attention]

### Remediation Priority
1. [Critical items ordered by regulatory enforcement risk and data exposure severity]
2. [...]

NEXT STEPS:
- Address critical findings across all phases before production deployment
- Engage compliance counsel for regulatory gap remediation planning
- Run `/security-review` for deeper code-level security analysis
- Run `/owasp` for comprehensive OWASP Top 10 assessment
- Schedule periodic re-runs of this suite (quarterly recommended)
- Prepare compliance documentation package for auditor review

DO NOT:
- Do NOT make definitive compliance certifications — flag findings for qualified assessors.
- Do NOT access or display actual regulated data (PII, PHI, financial records) during the audit.
- Do NOT skip any phase — partial compliance assessment creates false confidence.
- Do NOT assume framework overlap eliminates the need for individual framework review.
- Do NOT execute penetration tests against production without explicit authorization.


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /compliance-suite — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
