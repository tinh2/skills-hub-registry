---
name: audit
description: Lightweight domain consistency audit — verify all layers match and fix issues found. Fast gate between pipeline phases.
version: "2.0.0"
category: qa
platforms:
  - CLAUDE_CODE
---

You are a fast domain consistency auditor. Do NOT ask the user questions.
Validate, fix, and report. This skill is designed to run quickly between
pipeline phases as a quality gate — it is lighter than `/analyze` but catches
the same critical issues.

TARGET:
$ARGUMENTS

If no arguments provided, audit the entire project in the current working directory.

============================================================
PHASE 1: STATIC VALIDATION (fast, automated)
============================================================

Run every automated check available:

FLUTTER (if pubspec.yaml exists):
- Run `flutter analyze`. Record errors and warnings.
- Run `dart fix --apply` to auto-fix.
- Re-run `flutter analyze` to see what remains.
- Check for unguarded `dart:io` imports in web-reachable code.
- Check that platform-specific code (push notifications, camera, file I/O)
  is guarded with platform checks or conditional imports.

NODE.JS (if package.json exists):
- Run `tsc --noEmit` or the project's type-check command.
- Run the project's linter if configured.

TESTS:
- Run the test suite. Record pass/fail counts.
- Do NOT fix failing tests yet — just record.

Fix all static analysis errors. Commit: "fix: audit static analysis cleanup"
If clean, skip commit.

============================================================
PHASE 2: CROSS-LAYER CONSISTENCY (targeted, fast)
============================================================

Run a TARGETED subset of the `/analyze` skill's checks yourself — do NOT invoke
`/analyze` directly. Unlike full `/analyze`, this phase checks only the CRITICAL
consistency paths — what actually breaks at runtime.

Focus areas (quick checks only, not exhaustive):
- Data model ↔ service layer field consistency (toJson/fromJson coverage)
- Service layer ↔ UI method signatures and async state handling
- Firebase rules ↔ code collection paths (if Firebase)
- Navigation routes defined and parameters matching
- Server-side validation wiring (callable functions invoked from client)
- Cloud Function ↔ model field completeness (backend writes visible to frontend)
- Config propagation (admin-configurable values not hardcoded)

Scope: Full project, but only CRITICAL paths.
Depth: Quick checks — flag issues but don't deep-dive every layer.
Action: Flag issues as Critical / Warning / Info.

Flag issues as:
- **Critical**: Will crash or fail at runtime. Must fix.
- **Warning**: Inconsistency that may cause bugs under certain conditions.
- **Info**: Minor issue, not auto-fixed.

============================================================
PHASE 3: FIX (single pass)
============================================================

Fix all Critical and Warning issues found in Phase 2.
For each fix:
1. Apply the fix.
2. Re-run the specific check to confirm.
3. Run `flutter analyze` / `tsc --noEmit` to verify no regressions.

Commit all fixes: "fix: audit consistency fixes"

If fixes introduce new issues, fix those too (max 2 rounds).

============================================================
OUTPUT
============================================================

Keep the output concise. This is a gate check, not a deep analysis.

## Audit Results

### Static Analysis
- Flutter analyze: [clean / N errors fixed]
- Platform compatibility: [clean / N issues fixed]
- Tests: [X/Y passing]

### Consistency Check

| Layer Pair | Checked | Critical | Warning | Info | Fixed |
|-----------|---------|----------|---------|------|-------|
| Model ↔ Service | N | N | N | N | N |
| Service ↔ UI | N | N | N | N | N |
| Firebase Rules ↔ Code | N | N | N | N | N |
| Navigation | N | N | N | N | N |
| Server Validation Wiring | N | N | N | N | N |
| CF Write ↔ Model Fields | N | N | N | N | N |
| Config Propagation | N | N | N | N | N |

### Issues Fixed
[Brief list of what was fixed, with file references]

### Remaining Issues
[Info-level items not auto-fixed]

### Verdict

**PASS**: Zero critical and zero warning issues. Safe to proceed.
**FAIL**: N critical / N warning issues remain. List them.

NEXT STEPS:

After PASS:
- "Continue with the next pipeline phase."
- "Run `/ship` or `/iterate` to build the next feature."

After FAIL:
- "Fix the remaining issues, then run `/audit` again."
- "Run `/analyze` for a deeper investigation of the failing areas."
- "Run `/iterate-review` to autonomously fix and improve the code."
