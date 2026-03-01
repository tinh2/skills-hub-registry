---
name: ship
description: Fast autonomous build loop — 4 iterations max. Build it, make it work, analyze it, ship it.
version: "8.1.0"
category: build
platforms:
  - CLAUDE_CODE
---

You are in FULLY AUTONOMOUS MODE. Zero questions. Just build. Do NOT ask the user anything. Decide and move.

============================================================
TARGET: $ARGUMENTS
============================================================

$ARGUMENTS contains the task description — what to build, fix, or ship.

If $ARGUMENTS is empty:
1. Check conversation context for a pending task or feature request.
2. Check recent git log for incomplete work or failing tests.
3. If nothing is found, run `flutter analyze` or `tsc --noEmit` (whichever applies) and fix all issues found.
4. If the project is clean, report that and suggest what to work on next.

RULES:
- If you're unsure between two approaches, pick the simpler one.
- If a dependency is missing, install it.
- If tests don't exist, write them.
- If something breaks, fix it — don't report it, fix it.

============================================================
PHASE 1: PRE-BUILD VALIDATION GATE
============================================================

Before writing any feature code, validate the project foundation.
This prevents wasting iterations on lint, platform, and config issues.

1. STATIC ANALYSIS:
   - Flutter: Run `flutter analyze` and `dart fix --apply`. Fix all errors/warnings.
   - Node.js: Run `tsc --noEmit` or the project's type-check command.
   - Run the project's linter if configured.

2. PLATFORM CHECKS (Flutter):
   - Scan for unguarded `dart:io` imports in web-reachable code.
   - Verify Firebase init handles web vs native.
   - Verify push notification setup is platform-guarded.

3. DEPENDENCY CHECK:
   - Run `flutter pub get` or `npm install`.
   - Fix version conflicts or missing packages.

4. RULES/CONFIG CHECK (if Firebase):
   - Cross-check firestore.rules paths against collections used in code.
   - Cross-check storage.rules against upload paths.
   - Verify indexes exist for compound queries.

5. DOCKER/INFRASTRUCTURE CHECK (if docker-compose.yml or Dockerfile exists):
   - Verify image references use full registry paths (e.g., `ghcr.io/org/image`, not bare `org/image`)
   - Verify volume mounts: target paths exist in container, writable dirs have correct permissions
   - Verify config files are mounted where the application actually reads them (check default paths, not just env vars)
   - Run `bash -n` on all .sh scripts to catch syntax errors
   - Check for macOS vs Linux portability issues: `sed -i` (needs '' on macOS), `readlink -f` (not on macOS), `date` flags
   - Verify `$SCRIPT_DIR` / path references still resolve correctly after any directory reorganization

Fix everything found. Commit: "chore: pre-build validation fixes"
If clean, skip the commit and proceed.

============================================================
PHASE 2: QUALITY CHECKLIST (apply to every screen/module)
============================================================

Every screen you create or modify MUST satisfy these before committing.
Applying these at creation time prevents 46+ retrofit commits later:

a) A11Y: Every Icon/Image has semanticLabel. Every interactive element has
   tooltip or Semantics label. All tap targets >= 48x48dp. Text uses theme styles.
b) DESIGN TOKENS: Colors from ColorScheme only (zero hardcoded Color(0xFF...)).
   TextStyles from TextTheme only. Border radii from constants. Spacing on grid.
   Fees/rates/limits from admin config, not hardcoded.
c) ASYNC SAFETY: Every async operation in StatefulWidget checks
   `if (!mounted) return;` before calling setState.
d) SCALABILITY: Every Firestore query has .limit(). Batch writes for multi-doc
   operations. Idempotent Cloud Function triggers.
e) STRUCTURAL HEALTH: If any file exceeds 500 lines, decompose it into
   domain-specific modules. Do not let monolithic services grow across iterations.

MONOLITH DECOMPOSITION GATE (learned from recall analysis — 69 modifications to 3 monolithic files):

Before adding ANY feature code to a file that exceeds 500 lines:
1. STOP. Do not add the feature to the monolithic file.
2. Extract the relevant section into its own file first (widget, service, mixin, module).
3. Verify the extraction works (tests pass, build succeeds).
4. Commit the extraction: "refactor: extract [component] from [monolith]"
5. THEN implement the feature in the newly extracted file.

This is NOT optional. "Flag and plan" does not work — one project flagged
a monolithic screen file (6,732 lines) but never decomposed it, resulting in 21 modifications
and a 62% fix-commit rate. Decompose BEFORE building, not after.

MINIMUM TEST REQUIREMENT (learned from recall analysis — M8: Test Coverage = 0.00):

Every iteration that adds new functionality must include:
- Backend: At least 2 tests per new API endpoint (happy path + error case).
- Frontend: At least 1 widget/component test per new screen.
- If ZERO tests exist: set up test framework + 3-5 smoke tests first.
A feature is not complete until its tests exist and pass.

============================================================
PHASE 3: CO-COMMIT RULES (apply to every commit)
============================================================

These rules apply to EVERY iteration. Violating them is the #1 source of rework:

a) FIRESTORE RULES: When adding or modifying a Firestore collection, update
   firestore.rules in the SAME commit. Never commit feature code without rules.
b) SERVER-SIDE VALIDATION: When adding client-side business logic (credit checks,
   eligibility, permissions), wire up server-side enforcement in the SAME iteration.
c) MODEL SERIALIZATION: When a Cloud Function writes new fields, update the
   client model (fields, fromMap/toMap, copyWith) in the SAME commit.
d) CLOUD FUNCTION TRIGGERS: When changing document structure, verify triggers
   still match in the same commit.
e) SHARED CONFIGURATION (learned from recall analysis — 3 rework commits from
   duplicated defaults): When 2+ files reference the same configurable value (model
   name, base URL, API key, timeout, port), extract to a shared config module.
   Never hardcode the same default in multiple files. Create `src/config.ts` (or
   equivalent) with all shared defaults and env variable overrides centralized.
   Duplicated config is the #1 source of co-change rework in backend projects.

============================================================
PHASE 4: ITERATION 1 — MAKE IT EXIST
============================================================

- Build the simplest version that works.
- Co-commit Firestore rules, server validation, and model fields with features.
- Run tests/build to verify.
- Fix anything broken.
- Keep commits incremental — if touching 15+ files, split into logical commits.
- Commit: "feat: initial implementation"

============================================================
PHASE 5: ITERATION 2 — MAKE IT SOLID
============================================================

- Add error handling for real failure modes (not hypotheticals).
- Add or fix tests for core behavior.
- Verify all server-side validation is wired (not just client-side checks).
- Run full validation — fix until green.
- Commit: "fix: harden implementation"

============================================================
PHASE 6: ITERATION 3 — DOMAIN ANALYSIS GATE
============================================================

Run the `/analyze` skill scoped to everything you built or changed.
Include all analysis phases: consistency audit, server-side validation wiring,
model-to-Cloud-Function field completeness, Firebase rules, and platform compatibility.

Scope: All features/files touched across iterations 1-2.
Depth: Full analysis (all phases of /analyze).
Action: FIX everything rated Critical or Warning. Re-run affected checks to confirm.
Commit: "fix: resolve domain analysis issues"

============================================================
PHASE 7: ITERATION 4 — FINAL PASS (only if needed)
============================================================

- Only run if the analysis gate found issues that required fixes.
- Re-validate everything — tests, build, re-check analysis.
- Clean up if genuinely messy, then done.
- Commit: "refactor: final cleanup"

============================================================
POST-SHIP: DOCUMENTATION
============================================================

After all iterations complete and validation passes:
- Run `/readme` to generate or update the project's README.md.

============================================================
OUTPUT
============================================================

One short summary:

| Section | Detail |
|---------|--------|
| What | {what you built} |
| Pre-validation | {issues found/fixed, or "clean"} |
| Status | {tests/build passing or not} |
| Analysis | {issues found / issues fixed / any remaining} |
| Server-side validation | {all wired / gaps found and fixed} |
| Firestore rules | {all collections covered / gaps found and fixed} |
| Documentation | {README.md generated/updated} |
| Caveats | {any known issues, or "none"} |

============================================================
NEXT STEPS
============================================================

Recommended pipeline after `/ship`:
- "Run `/qa` to verify everything works end-to-end."
- "Run `/e2e` to generate automated end-to-end test coverage."
- "Run `/iterate-review` to harden with a focused review pass."
- "Run `/ux` to audit accessibility, design standards, and usability."
- "Run `/polish` for the full quality pipeline: `/ux` -> `/qa` -> `/analyze`."

============================================================
DO NOT
============================================================

- Do NOT ask the user anything — decide and move autonomously.
- Do NOT spend more than 4 iterations — if it is not working after 4, stop and report.
- Do NOT refactor code unrelated to the task — stay scoped.
- Do NOT skip the pre-build validation gate — it prevents cascading failures.
- Do NOT commit without running tests first — every commit must have a green build.
