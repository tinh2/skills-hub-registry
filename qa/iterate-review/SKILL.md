---
name: iterate-review
description: Autonomously review and improve existing code through up to 5 iterations of analysis, domain verification, fixing, and validation.
version: "5.0.0"
category: qa
platforms:
  - CLAUDE_CODE
---

You are in AUTONOMOUS MODE. Do NOT ask questions. Analyze and fix.

TARGET:
$ARGUMENTS

============================================================
PRE-REVIEW: STATIC VALIDATION
============================================================

Before reviewing code, run automated checks to clear the noise:

1. Flutter (if pubspec.yaml exists):
   - Run `flutter analyze`. Fix all errors and warnings.
   - Run `dart fix --apply`.
2. Node.js (if package.json exists):
   - Run `tsc --noEmit`. Fix type errors.
3. Platform checks (Flutter):
   - Scan for unguarded `dart:io` imports in web-reachable code.
   - Fix platform compatibility issues.
4. Firebase (if applicable):
   - Cross-check firestore.rules paths against code.
   - Verify compound queries have matching indexes.
5. Shell scripts & infrastructure (learned from OpenClaw recall — stray syntax,
   sed portability, path breakage after reorg):
   - Run `bash -n` on all .sh files to catch syntax errors (stray `fi`, unmatched brackets).
   - Check `sed -i` usage — needs `''` arg on macOS, not on Linux. Flag unportable usage.
   - Verify docker-compose.yml image refs use full registry paths (not bare names).
   - Verify volume mount targets match where the app actually reads config/data.
   - After any directory reorganization, verify `$SCRIPT_DIR`, `../`, `./` path references
     still resolve correctly.
   - Check variable names reference the correct entity (e.g., `$CALLER_ID` vs `$AGENT_ID`).

Fix all issues. Commit: "fix: pre-review static validation"
If clean, skip commit.

============================================================
PROCESS (max 5 iterations)
============================================================

=== EACH ITERATION ===

1. READ the target code thoroughly.
2. IDENTIFY the top 3 most impactful issues:
   - Bugs or incorrect behavior
   - Missing error handling that would cause real failures
   - Code that's confusing or poorly structured
3. CHECK WIRING COMPLETENESS (learned from recall analysis):
   - Server-side validation gaps: Are there callable Cloud Functions that exist
     but are never called from the client? (e.g., validateCreditSpend exists but
     client does client-only checks.) This is a CRITICAL issue.
   - Model serialization gaps: Are there fields written by Cloud Functions that
     are missing from the client model's fromMap/toMap? (e.g., Cloud Function
     writes offPlatformWarningCount but model doesn't deserialize it.)
   - Firestore rules lag: Are there collections the app reads/writes that have
     no matching rule in firestore.rules? Or rules that are too permissive?
   - Config propagation: Are admin-configurable settings (e.g., CSF monthly cap,
     pending period) actually passed through to the functions that use them, or
     are hardcoded defaults used instead?
4. CHECK STRUCTURAL HEALTH (learned from recall analysis):
   - Monolithic files: Flag any single file modified in >20% of recent commits
     or exceeding 600 lines. Recommend splitting into domain-specific modules.
   - Error handling coverage: Every user-facing action that calls an async service
     should be wrapped in try/catch with user-visible error feedback.
5. FIX all identified issues.
6. VALIDATE — run tests, build, lint. Fix until green.
7. DOMAIN ANALYSIS (runs on iteration 2 and on the final iteration):
   Run the `/analyze` skill scoped to the code under review.
   Include all analysis phases: consistency audit, server-side validation wiring,
   model-to-Cloud-Function field completeness, Firebase rules, and platform compatibility.
   If analysis finds Critical or Warning issues, add them to the fix list for the
   next iteration. Critical issues take priority over code review issues.
8. REASSESS — stop if: all code issues resolved AND validation passes AND domain
   analysis shows zero Critical/Warning issues.

=== ITERATION FOCUS ===

- Iteration 1: Correctness bugs, missing tests, AND wiring completeness checks
- Iteration 2: Run domain analysis. Fix consistency issues + error handling + edge cases.
- Iteration 3: Address remaining analysis warnings + code clarity + structural health.
- Iteration 4: Re-run analysis to confirm. Polish if needed.
- Iteration 5: Only if analysis still finds issues.

=== DO NOT ===

- Add features that weren't asked for
- Refactor code that works fine and is readable
- Add comments to obvious code
- Over-engineer simple logic
- Ask the user any questions — just decide and fix

=== COMMIT DISCIPLINE (learned from recall analysis) ===

- NEVER batch all fixes into a single "lots of bug fixes" mega-commit.
- Each commit should be focused and independently reviewable.
- When fixing Firestore rules gaps, include the rule fix in the same commit
  as the related code fix.

=== OUTPUT ===

Brief summary after each iteration:

  ## Iteration N
  - Found: [issues identified]
  - Wiring: [server-side gaps / model gaps / rules gaps found, if any]
  - Analysis: [Critical/Warning/Info counts, if analysis ran this iteration]
  - Fixed: [what was changed]
  - Validation: [pass/fail status]

Final summary:

  ## Review Complete
  - Pre-validation: [issues found and fixed, or "clean"]
  - Iterations completed: N/5
  - Issues found and fixed: [total count]
  - Wiring completeness: [server validation / model serialization / rules status]
  - Domain analysis: [issues found / issues fixed / any remaining]
  - Structural health: [monolithic files flagged, if any]
  - Final validation: [tests/build/lint status]
  - Remaining concerns: [any trade-offs, or "none"]

NEXT STEPS:

- "Run `/qa` to verify everything works end-to-end."
- "Run `/arch-review` for architect-level structural review."
- "Run `/readme` to update project documentation with the current state."
- "Run `/ux` to audit accessibility and design standards."
