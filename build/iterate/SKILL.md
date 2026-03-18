---
name: iterate
description: Autonomous build loop -- build iteratively, implement features, add capabilities. Default 6 iterations (thorough) or --fast for 4 iterations (ship it quick).
version: "2.0.0"
category: build
instructions: |
  You are in FULLY AUTONOMOUS MODE. Zero questions. Just build.

  TASK:
  $ARGUMENTS

  MODE DETECTION:
  - If $ARGUMENTS starts with "--fast" (e.g., "/iterate --fast add search bar"):
    MAX_ITERATIONS = 4 (fast mode -- build it, harden it, analyze it, ship it)
    Remove "--fast" from the task description before proceeding.
  - Otherwise: MAX_ITERATIONS = 6 (thorough mode -- full iterative refinement)

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

  5. DOCKER/INFRASTRUCTURE CHECK (if docker-compose.yml or Dockerfile exists):
     - Verify image references use full registry paths where needed.
     - Verify volume mounts: target paths exist in container, writable dirs have correct permissions.
     - Verify config files are mounted where the application actually reads them.
     - Run `bash -n` on all .sh scripts to catch syntax errors.
     - Check for cross-platform portability issues (sed, readlink, date flags, etc.).

  Fix everything found. Commit: "chore: pre-build validation fixes"
  If clean, skip the commit and proceed.

  === PER-COMPONENT QUALITY CHECKLIST ===

  Every component (screen, page, module, endpoint) you create or modify MUST
  satisfy these before committing. Applying these at creation time prevents
  dozens of retrofit commits later.

  a) ACCESSIBILITY:
     - Web: ARIA labels on interactive elements, focus management, keyboard navigation.
     - Mobile (Flutter): semanticLabel on icons/images, Semantics wrappers, 48dp touch targets.
     - Mobile (native): accessibilityLabel, accessibilityHint on interactive elements.
     - All: meaningful alt text, sufficient color contrast, screen-reader-friendly structure.

  b) DESIGN TOKENS:
     - Web: CSS custom properties or theme variables -- zero hardcoded hex colors or magic numbers.
     - Flutter: Colors from ColorScheme, TextStyles from TextTheme, spacing from constants.
     - Native: Style resources, design system tokens -- not inline literal values.
     - All: configurable values (rates, limits, feature flags) from config, not hardcoded.

  c) ASYNC SAFETY:
     - React: cleanup in useEffect return, abort controllers for fetch, check component mounted state.
     - Flutter: `if (!mounted) return;` before setState after every await.
     - General: cancellation tokens for long-running operations, cleanup on component unmount/dispose.
     - All: proper error handling on every async call, timeout on network requests.

  d) SCALABILITY:
     - Database queries have limits and pagination (no unbounded fetches).
     - Batch operations for multi-record writes.
     - Idempotent background jobs and event handlers.
     - Index coverage for compound/filtered queries.

  e) STRUCTURAL HEALTH: If any file exceeds 500 lines, decompose it into
     domain-specific modules. Do not let monolithic files grow across iterations.

  MONOLITH DECOMPOSITION GATE:

  Before adding ANY feature code to a file that exceeds 500 lines:
  1. STOP. Do not add the feature to the monolithic file.
  2. Extract the relevant section into its own file first (component, service, module, utility).
  3. Verify the extraction works (tests pass, build succeeds).
  4. Commit the extraction: "refactor: extract [component] from [monolith]"
  5. THEN implement the feature in the newly extracted file.

  This is NOT optional. Flagging a file for future decomposition does not work --
  monoliths that get flagged but not split accumulate modifications and high fix-commit
  rates. Decompose BEFORE building, not after.

  MINIMUM TEST REQUIREMENT:

  Every iteration that adds new functionality must include:
  - Backend: At least 2 tests per new endpoint/function (happy path + error case).
  - Frontend: At least 1 component/integration test per new screen or major component.
  - If ZERO tests exist: set up test framework + 3-5 smoke tests first.
  A feature is not complete until its tests exist and pass.

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
     module. Never hardcode the same default in multiple files. Duplicated config
     is the #1 source of co-change rework in backend projects.

  ============================================================
  PROCESS: ITERATION LOOP (max MAX_ITERATIONS iterations)
  ============================================================

  Run this loop up to MAX_ITERATIONS iterations. Stop early ONLY when ALL exit
  criteria are met.

  === PRE-IMPLEMENTATION: EXTERNAL SERVICE CONTRACT VERIFICATION ===

  Before writing ANY code that integrates with an external service, STOP and verify:

  1. API/TEMPLATE CONTRACTS: If integrating with any external API (payment, email,
     auth, etc.) -- read the actual API field names, webhook payload shapes, and
     response formats FIRST. List them explicitly. Do NOT guess from memory.
  2. PLATFORM REQUIREMENTS: If adding CI/CD workflows, deploy pipelines, or
     platform-specific config -- verify platform constraints before committing
     (plan tier requirements, signing identities, required environment variables).
  3. TIMEOUT/LIMITS: When adding test steps or CI jobs, set timeouts to 2-3x the
     expected duration from the start. Never use the default.

  If you cannot verify locally, document the assumptions explicitly in a code
  comment and flag them for manual verification.

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
  - Run domain analysis (see DOMAIN ANALYSIS section below).
  - Commit: "fix: harden implementation"

  === ITERATION 3: DOMAIN ANALYSIS GATE ===

  Run the `/analyze` skill scoped to everything you built or changed.
  Include all analysis phases: consistency audit, validation wiring,
  schema completeness, and platform compatibility.

  Scope: All features/files touched across iterations 1-2.
  Depth: Full analysis (all phases of /analyze).
  Action: FIX everything rated Critical or Warning. Re-run affected checks to confirm.
  Commit: "fix: resolve domain analysis issues"

  === ITERATION 4: CLEANUP / FINAL PASS (fast mode stops here) ===

  - Re-validate everything -- tests, build, re-check analysis.
  - Clean up code quality, naming, structure. Address remaining warnings.
  - If fast mode (4 iterations): this is the final pass. Ship it.
  - Commit: "refactor: cleanup"

  === ITERATION 5 (thorough mode only): HARDENING ===

  - Only run if analysis still finds issues or self-review scores < 4.
  - Re-run domain analysis to confirm previous fixes.
  - Address any remaining warnings.
  - Commit: "fix: hardening pass"

  === ITERATION 6 (thorough mode only): FINAL PASS ===

  - Only run if something still isn't right.
  - Final validation and polish.
  - Commit: "refactor: final pass"

  === SELF-REVIEW (run at end of each iteration) ===

  Score the current state on these dimensions (1-5):
  - Works: Does it run without errors? Do tests pass?
  - Correct: Does it actually do what was asked?
  - Clean: Is the code readable and maintainable?
  - Robust: Are edge cases handled? Is error handling adequate?
  - Wired: Are all layers connected? (schemas, server validation, serialization)

  Output the scores and a brief assessment of what to improve next iteration:

    ## Iteration N Self-Review
    - Works: X/5
    - Correct: X/5
    - Clean: X/5
    - Robust: X/5
    - Wired: X/5
    - Next focus: [what to improve]

  === DOMAIN ANALYSIS (runs on iteration 2 and on the final iteration) ===

  Run the `/analyze` skill scoped to the features you built or changed.
  Include all analysis phases: consistency audit, validation wiring,
  schema completeness, and platform compatibility.

  Scope: Only the features/files touched -- not the full project.
  Depth: Full analysis (all phases of /analyze).
  Action: If analysis finds Critical or Warning issues, feed them into the NEXT
  iteration's improvements as top-priority targets.

  === INTERMEDIATE QUALITY GATE ===

  When implementing MULTIPLE features (e.g., a list from a spec or backlog):
  - After every 3-4 features, run a mini domain analysis even if it's
    not iteration 2 yet. This catches cross-feature issues early.
  - Do NOT batch 8+ features into one iteration without a quality check.
  - If implementing 5+ features, split into batches of 3-4 and run validation
    between batches. This prevents mega-fix-commits later.

  === EXIT CRITERIA (ALL must be true to stop early) ===

  - All tests pass
  - Build succeeds (if applicable)
  - No lint errors (if linter exists)
  - Self-review scores are all 4+
  - Domain analysis shows zero Critical issues and zero Warning issues
  - Server-side validation is wired for all security-critical client logic
  - Schema/rules exist for all data the app reads/writes
  - The feature does what was requested

  === SCREEN/COMPONENT SIGN-OFF TABLE ===

  Before committing ANY screen or major component (new or modified), fill out
  this sign-off table:

  | Component | A11y | Tokens | Async | Scale | Structure | PASS? |
  |-----------|------|--------|-------|-------|-----------|-------|
  | {name}    | Y/N  | Y/N    | Y/N   | Y/N   | Y/N       | ALL Y |

  Rules:
  - Every column must be Y before committing. Any N = fix first, then re-check.
  - Include the checklist in commit messages: "feat: add profile page [A11y:Y Tokens:Y Async:Y Scale:Y Structure:Y]"
  - If implementing multiple components in one iteration, each gets its own row.
  - Do NOT batch components and "come back to fix a11y/tokens later" -- this is
    the #1 source of rework. Fix at creation time, not as a retrofit pass.

  Column definitions (quick reference):
  - A11y: ARIA/semantic labels, touch/click targets, keyboard navigation
  - Tokens: zero hardcoded colors or styles -- all from theme/design system
  - Async: cleanup on unmount, error handling on all async calls, timeouts
  - Scale: query limits, pagination, batch operations
  - Structure: file under 500 LOC, domain-split modules

  === COMMIT DISCIPLINE ===

  - Commit after each iteration with descriptive messages.
  - Keep commits focused. If an iteration touches 20+ files, split into logical commits.
  - NEVER batch all fixes into a single mega-commit like "lots of bug fixes".
    Each fix should be independently reviewable and revertable.
  - NEVER commit feature code without its corresponding schema/rules update.
  - Use conventional commits: feat:, fix:, chore:, test:, docs:

  === POST-LOOP: DOCUMENTATION ===

  After all iterations complete and validation passes:
  - Run `/readme` to generate or update the project's README.md.

  === OUTPUT ===

  One short summary:

    ## Build Summary
    - Mode: [thorough (6 iter) / fast (4 iter)]
    - What was built: [description]
    - Pre-validation: [issues found/fixed, or "clean"]
    - Iterations completed: N/MAX_ITERATIONS
    - Final validation: [tests/build/lint status]
    - Final scores: Works X/5, Correct X/5, Clean X/5, Robust X/5, Wired X/5
    - Domain analysis: [issues found / issues fixed / any remaining]
    - Server-side validation: [all wired / gaps found and fixed]
    - Schema/rules: [all data paths covered / gaps found and fixed]
    - Documentation: [README.md generated/updated]
    - Known limitations: [any trade-offs or deferred items]

  NEXT STEPS:

  Recommended pipeline after `/iterate`:
  - "Run `/qa` to verify everything works end-to-end."
  - "Run `/e2e` to generate automated end-to-end test coverage."
  - "Run `/iterate-review` to harden with a focused review pass."
  - "Run `/ux` to audit accessibility, design standards, and usability."
  - "Run `/polish` for the full quality pipeline: `/ux` -> `/qa` -> `/audit`."
platforms:
  - CLAUDE_CODE
---


============================================================
SELF-HEALING VALIDATION (max 3 iterations)
============================================================

After completing the main phases, validate your work:

1. Run the project's test suite (auto-detect: flutter test, npm test, vitest run, cargo test, pytest, go test, sbt test).
2. Run the project's build/compile step (flutter analyze, npm run build, tsc --noEmit, cargo build, go build).
3. If either fails, diagnose the failure from error output.
4. Apply a minimal targeted fix — do NOT refactor unrelated code.
5. Re-run the failing validation.
6. Repeat up to 3 iterations total.

IF STILL FAILING after 3 iterations:
- Document what was attempted and what failed
- Include the error output in the final report
- Flag for manual intervention


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /iterate — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
