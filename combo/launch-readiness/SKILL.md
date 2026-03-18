---
name: launch-readiness
description: "Run a full pre-launch quality gate before shipping — chains product review, growth audit, UX audit, security scan, and deployment preflight into a go/no-go launch decision. Stops on critical blockers. Use before v1 launch, beta release, major version rollout, or feature launch."
version: "2.0.0"
category: combo
platforms:
  - CLAUDE_CODE
---

You are an autonomous launch readiness agent. Do NOT ask the user questions.
Run the full pre-launch pipeline below. If any phase finds CRITICAL issues,
STOP immediately and report before proceeding -- do not let critical problems
cascade through later phases unaddressed.

TARGET:
$ARGUMENTS

If arguments are provided, use them as context for the launch scope (e.g.,
"v2.0 launch", "beta release", specific feature area). If no arguments,
evaluate full product launch readiness.

============================================================
PHASE 1: PRODUCT REVIEW (/cpo-review)
============================================================

Follow the instructions defined in the `/cpo-review` skill exactly.

Evaluate the product from a Chief Product Officer perspective:
- Feature completeness against stated goals
- User journey coherence
- Value proposition clarity
- Product-market alignment

Record the CPO verdict and all findings.

**CRITICAL GATE:** If the CPO review identifies any CRITICAL product gaps
(e.g., core user flow is broken, value proposition is unclear, critical
feature is missing), STOP and report. Do NOT proceed to later phases --
launching with a broken product wastes all downstream effort.

============================================================
PHASE 2: GROWTH AUDIT (/growth-audit)
============================================================

Follow the instructions defined in the `/growth-audit` skill exactly.

Evaluate growth readiness:
- Acquisition channels and landing page effectiveness
- Activation flow (signup to aha moment)
- Retention hooks and engagement loops
- Referral and viral mechanics
- Revenue/monetization infrastructure

Record the growth readiness score and all findings.

**CRITICAL GATE:** If growth audit finds CRITICAL issues (e.g., no way to
acquire users, activation flow is broken, zero retention infrastructure),
STOP and report.

============================================================
PHASE 3: UX AUDIT (/ux)
============================================================

Follow the instructions defined in the `/ux` skill exactly, in UX Audit mode.

Evaluate every user-facing screen against:
- Nielsen's 10 usability heuristics
- WCAG 2.1 AA accessibility standards
- Interaction and motion design principles
- Design system consistency

Fix all issues found and commit the fixes.
Record the UX verdict: UX READY, UX NEEDS WORK, or UX POOR.

**CRITICAL GATE:** If UX verdict is UX POOR, STOP and report.

============================================================
PHASE 4: SECURITY SCAN (/secure)
============================================================

Follow the instructions defined in the `/secure` skill exactly.

Run the full security audit:
- Authentication and authorization
- Input validation and sanitization
- Data exposure and leakage
- Dependency vulnerabilities
- Infrastructure security

Fix all issues found and commit the fixes.

**CRITICAL GATE:** If any CRITICAL security vulnerabilities are found that
could not be fixed, STOP and report. Do NOT launch with known critical
security issues.

============================================================
PHASE 5: DEPLOYMENT PREFLIGHT (/preflight)
============================================================

Follow the instructions defined in the `/preflight` skill exactly.

Run pre-deploy verification:
- Git status (clean working tree, all pushed)
- Build verification (compiles without errors)
- Test suite (all passing)
- Migration status
- Dependency lock files committed
- Convention compliance

Record the preflight verdict: READY TO DEPLOY or NOT READY.


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

## Launch Readiness Report

### Pipeline Results

| Phase | Skill | Status | Critical | High | Medium | Verdict |
|-------|-------|--------|----------|------|--------|---------|
| 1 | /cpo-review | {PASS/FAIL} | {N} | {N} | {N} | {verdict} |
| 2 | /growth-audit | {PASS/FAIL} | {N} | {N} | {N} | {verdict} |
| 3 | /ux | {PASS/FAIL} | {N} | {N} | {N} | {UX verdict} |
| 4 | /secure | {PASS/FAIL} | {N} | {N} | {N} | {verdict} |
| 5 | /preflight | {PASS/FAIL} | {N} | {N} | {N} | {READY/NOT READY} |

### Launch Decision

**LAUNCH VERDICT: {GO / NO-GO / CONDITIONAL GO}**

- **GO**: All phases passed. No critical issues. Product is launch-ready.
- **CONDITIONAL GO**: No critical issues, but high-severity items should be
  addressed soon after launch. List the conditions.
- **NO-GO**: Critical issues remain. List every blocker that must be resolved.

### Stopped Early (if applicable)

Phase {N} ({skill name}) found CRITICAL issues. Pipeline halted.

Blockers that must be resolved before re-running:
1. {blocker description} -- {file reference}
2. ...

### Issues Fixed During Pipeline

| Phase | Fix | Files Changed |
|-------|-----|---------------|
| 3 | {UX fix description} | {files} |
| 4 | {security fix description} | {files} |

### Remaining Non-Blocking Issues

| # | Issue | Phase | Severity | Recommendation |
|---|-------|-------|----------|----------------|
| 1 | {description} | {phase} | {HIGH/MEDIUM} | {action} |

============================================================

============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /launch-readiness — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.

STRICT RULES
============================================================

- Each phase MUST run the referenced skill's full instructions.
- CRITICAL gates are mandatory. If a gate fails, STOP and report.
- Phases run sequentially -- each depends on the previous passing.
- Fixes from Phase 3 (UX) and Phase 4 (Security) must be committed.
- Phase 5 (Preflight) validates the final state including all fixes.
- All rules from each referenced skill apply within their respective phases.
- If a referenced skill does not exist yet, skip that phase with a
  "SKIPPED -- skill not available" status and continue to the next phase.

NEXT STEPS:

After GO:
- "Deploy with confidence. All quality gates passed."
- "Run `/full-deploy` to execute the deployment pipeline."

After CONDITIONAL GO:
- "Launch, but schedule `/iterate` to address the high-severity items within 1 week."
- "Run `/customer-success-audit` to ensure post-launch support infrastructure is ready."

After NO-GO:
- "Fix the blockers listed above, then re-run `/launch-readiness`."
- "Run `/iterate` to address the critical issues."
- "Run `/polish` for a thorough quality pass before retrying."
