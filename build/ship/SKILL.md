---
name: ship
description: "Fast autonomous build loop -- 4 iterations max. Ship it, quick build, fast implementation, just build it, ship fast."
version: 2.0.0
category: build
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

=== PRE-BUILD: SECURITY-BY-DEFAULT CHECKLIST ===

Before writing feature code, apply these to every new endpoint/service/screen:
- Rate limiting on all new endpoints (or confirm global rate limiter covers it)
- Input validation via schema (Zod, Joi, etc.) — not manual checks
- Error responses sanitized — no stack traces or internal paths leaked
- Auth/ownership checks — users can only access their own resources (prevent IDOR)
- Timeouts on all external calls (30s default)
- DB queries use select/projection (not include/fetch-all), have pagination/limit
Do NOT defer these to a later "security hardening" pass. This caused 5-38 reactive
security fix commits per project across all 6 codebases.

=== PRE-COMMIT LOCAL VALIDATION ===

Before EVERY commit, run the project's format/lint/test suite locally:
- Flutter: `dart format --set-exit-if-changed . && flutter analyze && flutter test`
- Node.js: `npm run lint && npm run format:check && npm test` (or equivalent)
- Python: `ruff check . && ruff format --check . && pytest`
- Go: `gofmt -l . && go vet ./... && go test ./...`
- Rust: `cargo fmt --check && cargo clippy && cargo test`
If ANY check fails, fix it BEFORE committing. CI pass rates are 23-67% across
all projects because this step was skipped. Every format/lint fix commit is waste.

=== TEST CO-COMMIT ENFORCEMENT ===

Tests MUST be in the SAME commit as the feature they test. Do NOT batch-write
tests in a separate commit/session. The commit pattern is: `feat: add X [includes
tests]` — not `feat: add X` followed by `test: add tests for X, Y, Z`.
M8 (test co-commit ratio) is 0.00-0.32 across all projects. Batch tests find
stale interfaces and miss wiring bugs.

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

=== POST-SHIP: RELEASE TAGGING ===

After all iterations complete and validation passes, create a release tag:
1. Check existing tags: `git tag --sort=-v:refname | head -5`
2. Determine next version (v0.1.0 if no tags, bump patch/minor as appropriate)
3. Create: `git tag -a v{X.Y.Z} -m "feat: {description}"`
4. Push: `git push origin v{X.Y.Z}`
Why: D1 (Deployment Frequency) = 0/week across all projects.

=== POST-SHIP: DEAD CODE CLEANUP ===

Before documenting, scan for dead code:
1. If you REPLACED a file: delete the old file in the same commit.
2. If you RENAMED a file: verify no imports reference the old name. Delete old file.
3. If you EXTRACTED code from a monolith: verify extracted code removed from original.
4. Run: `git diff --name-status HEAD~{N}..HEAD` to review all file changes.

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
