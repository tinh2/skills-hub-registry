---
name: iterate-review
description: "Autonomously review and improve code through iterative analysis, wiring verification, fixing, and validation. Works with any tech stack."
version: 1.0.0
category: analysis
platforms:
  - CLAUDE_CODE
---

You are in AUTONOMOUS MODE. Do NOT ask questions. Analyze and fix.

TARGET:
$ARGUMENTS

============================================================
PRE-REVIEW: STATIC VALIDATION
============================================================

Before reviewing code, run automated checks to clear the noise.
Detect the project's tech stack and run the appropriate checks:

1. Language/framework linting:
   - Detect the project type from config files (package.json, pubspec.yaml,
     Cargo.toml, pyproject.toml, go.mod, Gemfile, pom.xml, etc.).
   - Run the project's standard linter/analyzer (e.g., `npm run lint`,
     `flutter analyze`, `cargo clippy`, `ruff check`, `go vet`).
   - Run any available auto-fix tool (e.g., `dart fix --apply`, `eslint --fix`,
     `ruff --fix`, `cargo fix`).
   - If a Makefile or task runner defines a `lint` or `check` target, use it.
2. Type checking (if applicable):
   - Run type checker (`tsc --noEmit`, `mypy`, `pyright`, etc.).
3. Shell scripts & infrastructure:
   - Run `bash -n` on all .sh files to catch syntax errors.
   - Check `sed -i` usage for portability (macOS vs Linux).
   - Verify docker-compose.yml image refs and volume mount paths.
   - After any directory reorganization, verify relative path references
     still resolve correctly.
4. Schema/config validation (if applicable):
   - Cross-check database rules/policies against code.
   - Verify queries have matching indexes if required.

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
3. CHECK WIRING COMPLETENESS:
   - API/service gaps: Are there endpoints, functions, or service methods that
     are defined but never called from the client? Or client code that calls
     endpoints that don't exist or have mismatched signatures?
   - Model/schema gaps: Are there fields written by the backend that are missing
     from the client-side model (serialization/deserialization)? Or vice versa?
   - Auth/permission gaps: Are there routes or operations that should require
     authentication or authorization but don't enforce it?
   - Config propagation: Are configurable values (limits, thresholds, feature
     flags) actually threaded through to where they're used, or are hardcoded
     defaults silently overriding them?
4. CHECK EXTERNAL SERVICE CONTRACTS:
   - For each external service integration (APIs, email providers, payment
     processors, CI/CD tools): verify that field names, payload shapes, and
     config values in the code match the actual API contracts.
   - Flag hardcoded assumptions about external service behavior that aren't
     verified by tests or documented.
   - Check for "yo-yo" patterns: values that were changed, reverted, then
     changed again in recent history.
5. CHECK STRUCTURAL HEALTH:
   - Monolithic files: Flag any single file exceeding 500 lines or modified
     in >20% of recent commits. Recommend splitting into domain-specific modules.
   - Error handling coverage: Every user-facing action that calls an async
     service should be wrapped in try/catch with user-visible error feedback.
   - Dead code: Flag unreachable code, unused imports, and commented-out blocks.
6. FIX all identified issues.
7. VALIDATE — run tests, build, lint. Fix until green.
8. DOMAIN ANALYSIS (runs on iteration 2 and on the final iteration):
   Run the `/analyze` skill scoped to the code under review.
   If analysis finds Critical or Warning issues, add them to the fix list for
   the next iteration. Critical issues take priority over code review issues.
9. REASSESS — stop if: all code issues resolved AND validation passes AND
   domain analysis shows zero Critical/Warning issues.

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

=== COMMIT DISCIPLINE ===

- NEVER batch all fixes into a single "lots of bug fixes" mega-commit.
- Each commit should be focused and independently reviewable.
- Tag fix commits with a category prefix (e.g., fix(auth), fix(wiring), fix(perf)).
- When fixing schema/permission gaps, include the fix in the same commit
  as the related code fix.

=== OUTPUT ===

Brief summary after each iteration:

  ## Iteration N
  - Found: [issues identified]
  - Wiring: [API gaps / model gaps / auth gaps found, if any]
  - Analysis: [Critical/Warning/Info counts, if analysis ran this iteration]
  - Fixed: [what was changed]
  - Validation: [pass/fail status]

Final summary:

  ## Review Complete
  - Pre-validation: [issues found and fixed, or "clean"]
  - Iterations completed: N/5
  - Issues found and fixed: [total count]
  - Wiring completeness: [API / model / auth / config status]
  - Domain analysis: [issues found / issues fixed / any remaining]
  - Structural health: [monolithic files flagged, if any]
  - Final validation: [tests/build/lint status]
  - Remaining concerns: [any trade-offs, or "none"]

NEXT STEPS:

- "Run `/qa` to verify everything works end-to-end."
- "Run `/arch-review` for architect-level structural review."
