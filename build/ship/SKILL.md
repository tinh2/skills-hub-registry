---
name: ship
description: "Fast autonomous build loop -- 4 iterations max. Ship it, quick build, fast implementation, just build it, ship fast."
version: 1.0.0
category: build
platforms:
  - CLAUDE_CODE
---

You are in FULLY AUTONOMOUS MODE. Zero questions. Just build.

TASK:
$ARGUMENTS

RULES:
- Do NOT ask the user anything. Decide and move.
- If you're unsure between two approaches, pick the simpler one.
- If a dependency is missing, install it.
- If tests don't exist, write them.
- If something breaks, fix it -- don't report it, fix it.

=== PRE-BUILD: VALIDATION GATE ===

Before writing any feature code, validate the project foundation.
This prevents wasting iterations on lint, platform, and config issues.

1. DETECT PROJECT TYPE:
   Identify the tech stack from project files (package.json, pubspec.yaml,
   Cargo.toml, go.mod, requirements.txt, pom.xml, Gemfile, etc.).
   Adapt all subsequent checks to the detected stack.

2. STATIC ANALYSIS:
   - Run the project's type checker (tsc --noEmit, flutter analyze, mypy, cargo check, etc.).
   - Run the project's linter if configured (eslint, dart fix --apply, ruff, clippy, etc.).
   - Fix all errors and warnings.

3. DEPENDENCY CHECK:
   - Run the project's dependency installer (npm install, flutter pub get, pip install, cargo build, etc.).
   - Fix version conflicts or missing packages.

4. PLATFORM/CONFIG CHECK:
   - If the project has platform-specific code, verify guards are in place (e.g., web vs native,
     OS-specific imports, conditional compilation).
   - If the project has database rules/migrations, cross-check them against code usage.
   - If the project has config files (env templates, schema files), verify they match code expectations.

5. CI/DEPLOY LOCAL VALIDATION:

   Before committing ANY CI workflow or deploy pipeline change:
   a) PLATFORM PLAN CHECK: Verify the feature works with the current GitHub plan/repo
      settings. Run `gh api repos/{owner}/{repo}` to check. Don't add features that
      require plan upgrades (e.g., CodeQL on private repos without Advanced Security).
   b) BUILD LOCALLY: Run the project's build command locally before adding to CI.
      Catch config, signing, and compilation issues before they hit CI.
   c) TIMEOUT DEFAULTS: Set CI test/build timeouts to 2-3x expected duration from the
      start. Never rely on default timeouts -- they cause multi-commit fix chains.
   d) USE `act` (GitHub Actions local runner) when available to validate workflow
      syntax and logic before pushing.

Fix everything found. Commit: "chore: pre-build validation fixes"
If clean, skip the commit and proceed.

=== CO-COMMIT RULES ===

These rules apply to EVERY iteration. Violating them is the #1 source of rework:

a) SCHEMA/RULES: When adding or modifying a data model, update corresponding
   database rules, migrations, or schemas in the SAME commit. Never commit
   feature code without its schema changes.
b) SERVER-SIDE VALIDATION: When adding client-side business logic (permission
   checks, eligibility, rate limits), wire up server-side enforcement in the
   SAME iteration. Client-only validation is not validation.
c) SERIALIZATION: When backend code writes new fields, update the client model
   (fields, serialization, deserialization) in the SAME commit.
d) EVENT HANDLERS: When changing data structures, verify triggers, webhooks,
   and event handlers still match in the same commit.
e) SHARED CONFIGURATION: When 2+ files reference the same configurable value
   (model name, base URL, API key, timeout, port), extract to a shared config
   module. Never hardcode the same default in multiple files.

=== ITERATION 1: MAKE IT EXIST ===

- Build the simplest version that works. No polish, just function.
- Co-commit schema changes, server validation, and model fields with features.
- Run tests/build to verify.
- Fix anything broken.
- Keep commits incremental -- if touching 15+ files, split into logical commits.
- Commit: "feat: initial implementation"

=== ITERATION 2: MAKE IT SOLID ===

- Add error handling for real failure modes (not hypotheticals).
- Add or fix tests for core behavior.
- Verify all server-side validation is wired (not just client-side checks).
- Run full validation -- fix until green.
- Commit: "fix: harden implementation"

=== ITERATION 3: DOMAIN ANALYSIS GATE ===

Run the `/analyze` skill scoped to everything you built or changed.
Include all analysis phases: consistency audit, validation wiring,
schema completeness, and platform compatibility.

Scope: All features/files touched across iterations 1-2.
Depth: Full analysis (all phases of /analyze).
Action: FIX everything rated Critical or Warning. Re-run affected checks to confirm.
Commit: "fix: resolve domain analysis issues"

=== ITERATION 4: FINAL PASS (only if needed) ===

- Only run if the analysis gate found issues that required fixes.
- Re-validate everything -- tests, build, re-check analysis.
- Clean up if genuinely messy, then done.
- Commit: "refactor: final cleanup"

=== POST-SHIP: DOCUMENTATION ===

After all iterations complete and validation passes:
- Run `/readme` to generate or update the project's README.md.

=== OUTPUT ===

One short summary:

  ## Shipped
  - What: [what you built]
  - Pre-validation: [issues found/fixed, or "clean"]
  - Status: [tests/build passing or not]
  - Analysis: [issues found / issues fixed / any remaining]
  - Server-side validation: [all wired / gaps found and fixed]
  - Schema/rules: [all data paths covered / gaps found and fixed]
  - Documentation: [README.md generated/updated]
  - Caveats: [any known issues, or "none"]

NEXT STEPS:

Recommended pipeline after `/ship`:
- "Run `/qa` to verify everything works end-to-end."
- "Run `/e2e` to generate automated end-to-end test coverage."
- "Run `/iterate-review` to harden with a focused review pass."
- "Run `/ux` to audit accessibility, design standards, and usability."
- "Run `/polish` for the full quality pipeline: `/ux` -> `/qa` -> `/analyze`."
