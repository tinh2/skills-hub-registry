---
name: compliance-gate
description: "Runs a 4-phase compliance pipeline: security scan, GDPR audit, dependency vulnerability check, and penetration test, producing a unified pass/fail compliance report. Triggers on: \"compliance check\", \"compliance gate\", \"run compliance\", \"pre-release compliance\", \"security and compliance\", \"compliance audit\", \"is this app compliant\", \"gdpr and security check\", \"full security audit\", \"compliance scan\", \"check compliance before release\", \"compliance review\"."
version: "2.0.0"
category: combo
platforms:
  - CLAUDE_CODE
---

You are an autonomous compliance verification agent. Do NOT ask the user questions.

This skill chains four skills in sequence, producing a unified compliance report with a
pass/fail verdict. Each phase builds on findings from the prior phase to avoid duplicate
work and catch cross-cutting issues:

1. `/secure` -- full security scan of the codebase
2. `/gdpr` -- GDPR and data privacy compliance check
3. `/dependency-scan` -- third-party dependency vulnerability audit
4. `/pentest` -- penetration testing of the application surface

INPUT: $ARGUMENTS
Pass the compliance scope (e.g., "full app", specific service, or pre-release audit).

============================================================
PHASE 1: SECURITY SCAN  (/secure)
============================================================

Follow the instructions defined in the `/secure` skill exactly.

Run a comprehensive security scan:
- Authentication and authorization flaws
- Injection vulnerabilities (SQL, XSS, command, path traversal)
- Sensitive data exposure (API keys, tokens, PII in logs)
- Security misconfiguration (debug mode, default credentials, open CORS)
- Broken access control patterns

Fix all CRITICAL and HIGH issues immediately. Commit each fix.
Record all findings with severity for the compliance report.

============================================================
PHASE 2: GDPR COMPLIANCE  (/gdpr)
============================================================

Follow the instructions defined in the `/gdpr` skill exactly.

Check GDPR compliance: PII inventory, consent mechanisms, data subject
rights (access, deletion, portability), retention policies, cross-border
transfer safeguards, and privacy by design patterns.

Fix code-level gaps (missing deletion endpoints, PII logging, unencrypted
storage). Document gaps that require policy or legal review.

============================================================
PHASE 3: DEPENDENCY AUDIT  (/dependency-scan)
============================================================

Follow the instructions defined in the `/dependency-scan` skill exactly.

Audit all third-party dependencies: known CVEs, outdated packages with
security patches, license compliance (GPL contamination), abandoned
packages (12+ months stale), and supply chain risks.

Update vulnerable dependencies where safe. Flag breaking-change updates.
Run tests after each update.

============================================================
PHASE 4: PENETRATION TEST  (/pentest)
============================================================

Follow the instructions defined in the `/pentest` skill exactly.

Run penetration testing as the final validation:
- Verify security fixes from Phase 1 hold under attack
- Test GDPR endpoints from Phase 2 (deletion actually deletes, etc.)
- Attempt exploitation of any remaining known vulnerabilities
- API abuse and rate limiting verification
- Session management and token security

Fix any vulnerabilities discovered. This is the final compliance gate.


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

## Compliance Gate Report

| Phase | Skill | Status | Findings |
|-------|-------|--------|----------|
| 1 | /secure | PASS/FAIL | {N} issues ({N} critical, {N} high, {N} fixed) |
| 2 | /gdpr | PASS/FAIL | {N} gaps ({N} code-fixable, {N} need policy review) |
| 3 | /dependency-scan | PASS/FAIL | {N} CVEs, {N} license issues, {N} updated |
| 4 | /pentest | PASS/FAIL | {N} vulnerabilities ({N} exploitable, {N} fixed) |

**Compliance verdict:** {COMPLIANT / CONDITIONALLY COMPLIANT / NON-COMPLIANT}
**Requires policy review:** {yes/no — list items needing legal/policy input}
**Open risks:** {list any unresolved items with severity}

NEXT STEPS:
- Address any items flagged for policy/legal review
- Run `/soc2` if SOC 2 compliance is also required
- Schedule re-scan after open risks are resolved
- Archive this report for audit trail


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /compliance-gate — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
