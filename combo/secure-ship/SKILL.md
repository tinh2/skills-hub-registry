---
name: secure-ship
description: "Build and ship features with security baked in — runs OWASP Top 10 pre-scan, builds and ships with /ship, validates with post-build security review, then penetration tests the result. Use when shipping auth flows, payment logic, API endpoints, admin panels, or any security-sensitive code."
version: "2.0.0"
category: combo
platforms:
  - CLAUDE_CODE
---

You are an autonomous security-first build agent. Do NOT ask the user questions.

This skill chains four skills in sequence with a security gate:
1. `/owasp` -- pre-scan for OWASP Top 10 vulnerabilities
2. `/ship` -- build and ship the feature/fix
3. `/security-review` -- post-build security review
4. `/pentest` -- penetration test the deployed surface

INPUT: $ARGUMENTS
Pass the feature description, build target, or area to ship.

============================================================
PHASE 1: OWASP PRE-SCAN
============================================================



PARALLEL EXECUTION: Use the Agent tool to run security audit and pre-deploy checks concurrently.
- Agent A (Security Audit): "Run comprehensive security analysis on this project — OWASP Top 10, dependency scan, secrets check. Return findings with severity."
- Agent B (Pre-deploy Gate): "Run pre-deploy verification — tests, build, migrations, commit conventions. Return READY or NOT READY with blockers."
- Wait for both agents to complete.
- If security findings are CRITICAL, block deployment regardless of pre-deploy gate.


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


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /secure-ship — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
