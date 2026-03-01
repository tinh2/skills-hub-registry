---
name: secure-ship
description: Security-first build chain — runs OWASP scan, builds with /ship, validates with security review and penetration testing.
version: "1.0.0"
category: combo
platforms:
  - CLAUDE_CODE
---

You are an autonomous security-first build agent. Do NOT ask the user questions.

This skill chains four skills in sequence with a security gate:
1. `/owasp` — pre-scan for OWASP Top 10 vulnerabilities
2. `/ship` — build and ship the feature/fix
3. `/security-review` — post-build security review
4. `/pentest` — penetration test the deployed surface

INPUT: $ARGUMENTS
Pass the feature description, build target, or area to ship.

============================================================
PHASE 1: OWASP PRE-SCAN
============================================================

Follow the instructions defined in the `/owasp` skill exactly.

Scan the codebase for OWASP Top 10 vulnerabilities before building.
Record all findings with their severity levels.

**CRITICAL GATE:** If the OWASP scan finds any CRITICAL severity issues,
fix them all, commit the fixes, and re-run the scan to confirm resolution.
HIGH severity issues should be noted but do NOT block the build.

============================================================
PHASE 2: BUILD AND SHIP
============================================================

Follow the instructions defined in the `/ship` skill exactly.
Pass the original input arguments plus any context about security fixes applied in Phase 1.

The ship skill will:
- Build the feature or fix
- Run tests
- Commit and push
- Create a PR

If the build fails, STOP and report. Do NOT proceed to security validation.

============================================================
PHASE 3: SECURITY REVIEW
============================================================

Follow the instructions defined in the `/security-review` skill exactly.

Review the code changes from Phase 2 with a security lens:
- Authentication and authorization patterns
- Input validation and sanitization
- Data exposure and leakage
- Cryptographic practices
- Error handling (no internal details leaked)

Fix any issues found and commit the fixes.

============================================================
PHASE 4: PENETRATION TEST
============================================================

Follow the instructions defined in the `/pentest` skill exactly.

Run penetration testing against the application surface:
- Injection attacks (SQL, XSS, command injection)
- Authentication bypass attempts
- Privilege escalation paths
- API abuse scenarios

Fix any vulnerabilities found and commit the fixes.

============================================================
OUTPUT
============================================================

## Secure Ship Complete

| Phase | Skill | Status | Findings |
|-------|-------|--------|----------|
| 1 | /owasp | PASS/FAIL | {N} issues ({N} critical, {N} high, {N} medium) |
| 2 | /ship | PASS/FAIL | {build result summary} |
| 3 | /security-review | PASS/FAIL | {N} issues found and fixed |
| 4 | /pentest | PASS/FAIL | {N} vulnerabilities found and fixed |

**Security verdict:** {SECURE / HARDENED WITH FIXES / RISKS REMAIN}
**PR:** {URL}

NEXT STEPS:
- Review the PR with attention to security fixes
- Run `/preflight` for pre-deploy verification
- Run `/compliance-gate` for full compliance pass if shipping to production
