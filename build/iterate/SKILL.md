---
name: iterate
description: Self-iterating build loop — implements, tests, reviews, analyzes, and refines autonomously up to 6 iterations until all validation and domain analysis passes.
version: "4.0.0"
category: build
platforms:
  - CLAUDE_CODE
---

You are in AUTONOMOUS MODE. Do NOT ask the user questions. Make decisions yourself.
If something is ambiguous, pick the simplest reasonable option and move on.

TASK:
$ARGUMENTS

============================================================
STEP 0: PRE-BUILD VALIDATION (runs once before the loop)
============================================================

Before writing ANY feature code, validate the project foundation. This step
eliminates entire categories of bugs that would otherwise consume iterations.

STATIC ANALYSIS:
- Flutter: Run `flutter analyze`. Fix every error and warning before proceeding.
- Flutter: Run `dart fix --apply` to auto-fix common issues.
- Node.js: Run `tsc --noEmit` or the project's type-check command.
- Run the project's linter if configured (eslint, dart analyze, etc.).

PLATFORM COMPATIBILITY (Flutter projects):
- Search for `dart:io` imports in files that run on web. Guard with
  `import 'dart:io' if (dart.library.io) 'stub.dart';` or conditional imports.
- Check that Firebase initialization handles web vs native correctly.
- Verify no platform-specific code runs unconditionally (e.g., push notifications on web).

DEPENDENCY CHECK:
- Run `flutter pub get` or `npm install` to ensure dependencies resolve.
- Check for version conflicts or deprecated packages.

FIREBASE / BACKEND RULES (if applicable):
- If firestore.rules exists, cross-check that rule paths match the collections
  used in the service/data layer. Flag mismatches.
- If storage.rules exists, verify paths match what the app writes to.

Fix ALL issues found. Commit: "chore: pre-build validation fixes"

If no issues found, proceed without committing.

============================================================
PROCESS: ITERATION LOOP (max 6 iterations)
============================================================

Run this loop up to 6 iterations. Stop early ONLY when ALL exit criteria are met.

=== EACH ITERATION ===

STEP 1: IMPLEMENT / IMPROVE

- Iteration 1: Build the MVP — simplest working version. No polish, just function.
- Iteration 2+: Improve based on issues found in the previous review AND analysis steps.
  Analysis findings take priority over self-review improvements.

CO-COMMIT RULES (CRITICAL — learned from recall analysis):
When implementing features, you MUST co-commit related changes together.
Failing to do this is the #1 source of rework:

a) FIRESTORE RULES: When adding or modifying a Firestore collection, update
   firestore.rules in the SAME commit. Never commit feature code that reads/writes
   a collection without ensuring rules exist for that collection. Check
   firestore.indexes.json for any new compound queries.
b) STORAGE RULES: When adding file upload paths, update storage.rules in the
   same commit.
c) SERVER-SIDE VALIDATION: When adding client-side business logic (credit checks,
   eligibility, permissions), wire up the corresponding server-side validation
   (Cloud Functions, callable functions) in the SAME iteration. Never rely on
   client-side-only enforcement for security-critical logic.
d) MODEL SERIALIZATION: When a Cloud Function writes new fields to a document,
   update the client-side model class (fields, constructor, copyWith, fromJson/
   fromMap, toJson/toMap) in the SAME commit. Missing fields are invisible bugs.
e) CLOUD FUNCTION TRIGGERS: When creating new collections or changing document
   structure, verify Cloud Function triggers still match. Update triggers in the
   same commit if needed.

STEP 2: VALIDATE

- Run the project's test suite. If no tests exist, write basic tests first.
- Run the build/compile step if applicable.
- Run the linter if configured.
- Record what passed and what failed.

STEP 3: FIX

- If anything from Step 2 failed, fix it NOW before moving on.
- Re-run validation until it passes.
- If stuck after 3 fix attempts on the same issue, note it and move on.

STEP 4: SELF-REVIEW

Score the current state on these dimensions (1-5):
- Works: Does it run without errors? Do tests pass?
- Correct: Does it actually do what was asked?
- Clean: Is the code readable and maintainable?
- Robust: Are edge cases handled? Is error handling adequate?
- Wired: Are all layers connected? (rules, server validation, model serialization)

Output the scores and a brief assessment of what to improve next iteration:

  ## Iteration N Self-Review
  - Works: X/5
  - Correct: X/5
  - Clean: X/5
  - Robust: X/5
  - Wired: X/5
  - Next focus: [what to improve]

STEP 5: DOMAIN ANALYSIS (runs on iteration 2 and on the final iteration)

Run the `/analyze` skill scoped to the features you built or changed in this iteration.
Include all analysis phases: consistency audit, server-side validation wiring,
model-to-Cloud-Function field completeness, Firebase rules, and platform compatibility.

Scope: Only the features/files touched in this iteration — not the full project.
Depth: Full analysis (all phases of /analyze).
Action: If analysis finds Critical or Warning issues, feed them into the NEXT
iteration's Step 1 as the top-priority improvement targets.

=== INTERMEDIATE QUALITY GATE (learned from recall) ===

When implementing MULTIPLE features (e.g., a list from docs/NewFeatures.md):
- After every 3-4 features, run a mini domain analysis (Step 5) even if it's
  not iteration 2 yet. This catches cross-feature issues early.
- Do NOT batch 8+ features into one iteration without a quality check.
- If implementing 5+ features, split into batches of 3-4 and run validation
  between batches. This prevents "lots of bug fixes" mega-commits later.

=== EXIT CRITERIA (ALL must be true to stop early) ===

- All tests pass
- Build succeeds (if applicable)
- No lint errors (if linter exists)
- Self-review scores are all 4+
- Domain analysis shows zero Critical issues and zero Warning issues
- Server-side validation is wired for all security-critical client logic
- Firestore rules exist for all collections the app reads/writes
- The feature does what was requested

=== ITERATION FOCUS ===

- Iteration 1: Focus ONLY on making it work. Ugly code is fine. But DO co-commit
  rules, server validation, and model fields — these are not polish, they are wiring.
- Iteration 2: Run domain analysis. Fix consistency issues + error handling + tests.
- Iteration 3: Clean up code quality, naming, structure. Address remaining warnings.
- Iteration 4: Re-run analysis to confirm. Polish if needed.
- Iteration 5: Only if analysis still finds issues.
- Iteration 6: Final pass — only if something still isn't right.

=== COMMIT DISCIPLINE ===

- Commit after each iteration: "feat: iteration N — [what changed]"
- Keep commits focused. If an iteration touches 20+ files, split into logical commits.
- NEVER batch all fixes into a single mega-commit like "lots of bug fixes".
  Each fix should be independently reviewable and revertable.
- NEVER commit feature code without its corresponding Firestore rules update.
- Use conventional commits: feat:, fix:, chore:, test:, docs:

=== AFTER THE LOOP ===

STEP 6: UPDATE DOCUMENTATION

After the build loop completes and all validation passes:
- Run `/readme` to generate or update the project's README.md.
- This ensures documentation stays in sync with what was just built.

Output a summary:

  ## Build Summary
  - What was built: [description]
  - Pre-validation: [issues found and fixed, or "clean"]
  - Iterations completed: N/6
  - Final validation: [tests/build/lint status]
  - Final scores: Works X/5, Correct X/5, Clean X/5, Robust X/5, Wired X/5
  - Domain analysis: [issues found / issues fixed / any remaining]
  - Server-side validation: [all wired / gaps found and fixed]
  - Firestore rules: [all collections covered / gaps found and fixed]
  - Documentation: [README.md generated/updated]
  - Known limitations: [any trade-offs or deferred items]

=== STRICT RULES ===

- Do NOT ask the user anything. Decide and move.
- If you're unsure between two approaches, pick the simpler one.
- If a dependency is missing, install it.
- If tests don't exist, write them.
- If something breaks, fix it — don't report it, fix it.
- Do not add features beyond what was requested. No scope creep.
- Pre-validation is NOT optional. Always run Step 0 before the loop.
- Co-commit rules are NOT optional. Firestore rules, server validation,
  and model serialization must ship with the feature, not as an afterthought.

NEXT STEPS:

Recommended pipeline after `/iterate`:
- "Run `/qa` to verify everything works end-to-end (domain analysis + integration flows)."
- "Run `/e2e` to generate automated end-to-end test coverage."
- "Run `/iterate-review` to harden the code with a focused review pass."
- "Run `/ux` to audit accessibility, design standards, and usability."
- "Run `/polish` for the full quality pipeline: `/ux` → `/qa` → `/analyze`."
