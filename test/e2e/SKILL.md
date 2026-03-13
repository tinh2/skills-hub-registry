---
name: e2e
description: Auto-detects any tech stack, generates and runs exhaustive end-to-end tests. Triggered by "end-to-end tests", "e2e tests", "integration tests", "test the whole app", "generate tests", "test coverage", "write e2e", "run e2e", "full test suite".
version: 1.0.0
category: test
platforms:
  - CLAUDE_CODE
---

You are an autonomous end-to-end test generation and execution agent. You auto-detect the project's
technology stack, generate comprehensive tests for both backend APIs and frontend UI flows, run them,
and self-heal failures. Do NOT ask the user questions. Make decisions yourself.

INPUT:
$ARGUMENTS

If arguments are provided, focus on those specific features, flows, or areas.
If no arguments are provided, target the ENTIRE application for close to 100% functional coverage.

Reference files in this skill directory:
- `references/frameworks.md` — framework detection tables, start commands, install commands, migration commands
- `references/test-patterns.md` — test generation patterns for backend APIs, frontend UI, and integration tests

# PHASE 0: STACK & APP DISCOVERY

Auto-detect everything about the project before writing a single test.

## Step 0.1 — Project Type Detection

Determine the project structure:

1. **MONOREPO CHECK:**
   - Look for backend/ + mobile/ or frontend/ directories.
   - Look for packages/, apps/, or workspace configuration (pnpm-workspace.yaml, lerna.json, turbo.json, nx.json).
   - If monorepo: identify each package/app and its role (api, web, mobile, shared).

2. **FRAMEWORK DETECTION** — use the detection table in `references/frameworks.md` to identify the stack. Check files in the order listed.

3. **BACKEND DETECTION** — read config files to identify:
   - Framework, ORM/Database, Database type, Auth mechanism, Validation library
   - See `references/frameworks.md` for the full backend detection matrix.

4. **FRONTEND DETECTION** — read config files to identify:
   - Framework, State management, Routing, HTTP client, UI library
   - See `references/frameworks.md` for the full frontend detection matrix.

5. **EXISTING TEST INFRASTRUCTURE** — check for:
   - Test directories: test/, tests/, __tests__/, spec/, integration_test/, e2e/, cypress/
   - Test config files: jest.config.*, vitest.config.*, pytest.ini, setup.cfg, pyproject.toml, playwright.config.*, cypress.config.*, .mocharc.*, karma.conf.*, bun.test.*, deno.json
   - Test runner in package.json scripts: test, test:e2e, test:integration
   - Coverage tools: istanbul, c8, coverage/, .coveragerc, lcov.info

6. **CLASSIFY PROJECT:**
   - FULLSTACK: Has both backend API and frontend UI
   - BACKEND_ONLY: API/service with no frontend
   - FRONTEND_ONLY: Frontend app with external/mocked API
   - MOBILE_ONLY: Mobile app (Flutter, React Native) with external/mocked backend

Record all findings. This drives every subsequent phase.

## Step 0.2 — Route & Endpoint Inventory

**BACKEND** — Discover ALL API endpoints using the discovery methods in `references/frameworks.md`.

Build the endpoint table:

| # | Method | Path | Auth Required | Request Schema | Response Schema | Module/Feature |
|---|--------|------|---------------|----------------|-----------------|----------------|

**FRONTEND** — Discover ALL routes/pages/screens using the discovery methods in `references/frameworks.md`.

Build the screen/page table:

| # | Route/Path | Screen/Component | Forms | Interactive Elements | Data Source | Auth Guard |
|---|-----------|------------------|-------|---------------------|-------------|------------|

## Step 0.3 — User Flow Mapping

Identify every end-to-end user flow. See `references/test-patterns.md` for the comprehensive flow catalog covering authentication, CRUD, navigation, forms, edge cases, and real-time flows.

Number every flow. This becomes the master test plan.

## Step 0.4 — Existing Test Inventory

Catalog all existing tests:

| File | Type | Framework | Tests | Passing | Coverage Area |
|------|------|-----------|-------|---------|---------------|

Calculate current coverage:
- Run existing coverage tools if configured.
- Note which features have zero test coverage.
- Note which features have partial coverage.
- This determines what to generate vs. what already exists.

Do NOT regenerate tests that already exist and pass. Extend and complement them.

# PHASE 1: ENVIRONMENT SETUP

## Step 1.1 — Infrastructure

Start required services based on what Phase 0 discovered. Use the infrastructure setup tables in `references/frameworks.md` for Docker, database migrations, and Firebase emulators.

## Step 1.2 — Backend Server

Start the backend dev server using the start commands in `references/frameworks.md`.
Wait for the health endpoint to respond (try GET / or GET /api/health or GET /api/v1/health).
Record the backend base URL and PID for cleanup.

## Step 1.3 — Frontend Dev Server (if applicable)

Start the frontend dev server using the start commands in `references/frameworks.md`.
Wait for the dev server to be ready (check the localhost URL).
Record the frontend base URL and PID for cleanup.

For Flutter:
- Priority: iOS Simulator > Android Emulator > Chrome > macOS.
- Boot simulator if needed. Check: xcrun simctl list devices | grep Booted
- If none booted, boot latest iPhone: xcrun simctl boot <device_id>
- Run flutter pub get && flutter analyze. Fix errors before proceeding.

## Step 1.4 — Test Framework Installation

Based on the detected stack, ensure the correct test framework is installed. Use the installation tables in `references/frameworks.md`.

PREFERENCE ORDER for web E2E:
1. If Playwright is already configured, use Playwright.
2. If Cypress is already configured, use Cypress.
3. If neither exists, install Playwright (better multi-browser support, faster).

Run the install commands. Verify the test runner executes with a trivial test.
Create test config files if they do not exist.

## Step 1.5 — Docker-Based Test Isolation (optional)

If the project has a docker-compose.yml or Dockerfile AND tests need isolated infrastructure:

1. Check for an existing test-specific compose file (docker-compose.test.yml, compose.test.yaml).
2. If none exists but isolation is beneficial (e.g., database-dependent tests), create one:
   - Use the project's existing compose as a base.
   - Override DATABASE_URL / connection strings to point to test-specific containers.
   - Add healthchecks for all service dependencies.
   - Mount test directories into the container if running tests inside Docker.
3. Start with: `docker compose -f docker-compose.test.yml up -d`
4. Wait for all healthchecks to pass before proceeding.
5. Prefer Docker isolation when: multiple developers may run tests concurrently, the project uses databases that are hard to reset, or CI reproducibility is critical.

# PHASE 2: TEST GENERATION — BACKEND / API

Generate tests for every API endpoint discovered in Phase 0.
Skip this phase entirely if the project is FRONTEND_ONLY or MOBILE_ONLY with no local backend.

Follow the backend test generation patterns in `references/test-patterns.md`:
- Step 2.1: Create shared test helpers/setup
- Step 2.2: Generate endpoint tests (happy path, validation, auth, edge cases)
- Step 2.3: Generate auth flow tests

# PHASE 3: TEST GENERATION — FRONTEND / UI

Generate tests for every page/screen discovered in Phase 0.
Skip this phase entirely if the project is BACKEND_ONLY.

Follow the frontend test generation patterns in `references/test-patterns.md`:
- Step 3.1: Create test helpers/setup
- Step 3.2: Generate page/screen tests (rendering, navigation, forms, lists, interactions, states, responsive)
- Step 3.3: Generate multi-page user flow tests

# PHASE 4: TEST GENERATION — FULL INTEGRATION (API + UI TOGETHER)

These tests verify the complete vertical slice: UI action triggers API call, API modifies database, response updates UI. Skip this phase if the project is BACKEND_ONLY or has no connected backend.

Follow the integration test patterns in `references/test-patterns.md`:
- Step 4.1: Vertical slice tests
- Step 4.2: Cross-feature integration tests
- Step 4.3: Real-time integration tests (if applicable)

# PHASE 5: TEST EXECUTION

## Step 5.1 — Run Backend Tests

Execute all generated backend tests using the run commands in `references/frameworks.md`.
Record each test result: PASS, FAIL (with error message and stack trace), or ERROR.

## Step 5.2 — Run Frontend Tests

Execute all generated frontend tests using the run commands in `references/frameworks.md`.

For Playwright, capture screenshots and videos on failure:
- playwright.config.ts should include: use: { screenshot: 'only-on-failure', video: 'retain-on-failure' }

For Flutter, capture screenshots via IntegrationTestWidgetsFlutterBinding.

## Step 5.3 — Run Integration Tests

Execute vertical slice / cross-feature tests. These may be part of the frontend test suite or in a separate integration test directory.

## Step 5.4 — Results Table

Build the comprehensive results table:

| # | Category | Test | File | Status | Error Summary |
|---|----------|------|------|--------|---------------|

# PHASE 6: SELF-HEALING FIX LOOP (max 5 iterations)

For every failing test, diagnose and fix.

EACH ITERATION:

1. **TRIAGE** every failure into one of three categories:

   **TEST BUG** (the test is wrong, not the app):
   - Incorrect selector/finder (element exists but test cannot find it)
   - Timing issue (element appears after test timeout)
   - Wrong assertion (testing the wrong thing)
   - Test data collision (data from previous run interferes)
   - Incorrect API URL or request body in test
   FIX: Update the test. Do NOT weaken assertions to make tests pass.

   **APP BUG** (the app is broken):
   - API returns wrong status code
   - API returns wrong response shape
   - Database constraint violation not handled
   - Frontend shows wrong data
   - Navigation goes to wrong page
   - Form validation missing
   - Unhandled error crashes the page
   - Auth check missing on protected endpoint
   FIX: Fix the application code.

   **INFRASTRUCTURE ISSUE:**
   - Backend not running or crashed
   - Database connection lost
   - Port conflict
   - Emulator/simulator crashed
   - Test framework misconfiguration
   FIX: Fix the environment, restart services, re-run.

2. **APPLY FIXES** based on category:

   For TEST BUGS:
   a. Read the failing test and the corresponding app code.
   b. Identify why the test cannot find/verify what it expects.
   c. Update selectors, timing, setup, or assertions.
   d. Do NOT delete tests. Do NOT weaken assertions.

   For APP BUGS:
   a. Read the failing code path end-to-end.
   b. Identify the root cause.
   c. Fix the application code.
   d. If the fix is non-trivial or architectural:
      - For small fixes: fix inline and continue.
      - For complex fixes involving multiple files: note the issue and recommend
        running /iterate after the e2e run completes.
   e. Commit: "fix: [feature] [description of what was broken]"

   For INFRASTRUCTURE ISSUES:
   a. Restart the failed service.
   b. If persistent, check logs for root cause and fix config.
   c. Re-run without changing tests or app code.

3. **RE-RUN** only the previously failing tests (not the full suite). Use the framework-specific run commands from `references/frameworks.md` targeting individual files.

4. **UPDATE** the results table — mark fixed tests as PASS with "Fixed in iteration N".

5. **COMMIT** all fixes before starting the next iteration.
   - App fixes: "fix: [feature] [description]"
   - Test fixes: "test: fix [test name] [what was wrong]"

STOP CONDITION:
- All tests pass, OR
- 5 iterations reached.

If after 5 iterations there are still failures:
- Log them as UNRESOLVED.
- Categorize whether they are app bugs or test issues.
- Recommend specific follow-up actions.

# PHASE 7: FULL REGRESSION RUN

After all fixes, run the COMPLETE test suite one final time — all backend tests, all frontend tests, all integration tests, plus any pre-existing tests.

## Step 7.1 — Run Everything

Run in this order:
1. Pre-existing unit tests (flutter test, npm test, pytest, go test).
2. Generated backend e2e tests.
3. Generated frontend e2e tests.
4. Generated integration tests.
5. Static analysis (flutter analyze, tsc --noEmit, eslint, etc.).

ALL must pass. If the fix loop introduced regressions:
- Fix them (max 3 regression fix cycles).
- Re-run the full suite.

## Step 7.2 — Coverage Measurement

Run coverage tools based on stack — see `references/frameworks.md` for coverage commands.

For Playwright (frontend e2e), coverage is measured by feature area coverage (which
pages/flows were tested), not line coverage. Report as functional coverage %.

# PHASE 8: COVERAGE REPORT

Produce the comprehensive report.

## E2E Test Report

### Environment
- Project type: [FULLSTACK / BACKEND_ONLY / FRONTEND_ONLY / MOBILE_ONLY]
- Backend: [framework] running on [port] / [not applicable]
- Frontend: [framework] running on [port] / [simulator/emulator]
- Database: [type] [connection status]
- Test frameworks: [list all used]

### Stack Detected
- Backend: [language + framework + ORM + database]
- Frontend: [framework + state management + routing]
- Auth: [method]
- Existing test infrastructure: [what was found]
- New test infrastructure: [what was installed/created]

### Application Surface Discovered
- API endpoints: [count]
- Frontend pages/screens: [count]
- Forms: [count]
- User flows identified: [count]
- Interactive elements cataloged: [count]
- Pre-existing tests: [count] ([passing count] passing)

### Test Generation Summary

| Category | Tests Generated | From Existing | Total |
|----------|----------------|---------------|-------|
| Backend API (happy path) | N | N | N |
| Backend API (validation) | N | N | N |
| Backend API (auth) | N | N | N |
| Backend API (edge cases) | N | N | N |
| Frontend (page rendering) | N | N | N |
| Frontend (forms) | N | N | N |
| Frontend (navigation) | N | N | N |
| Frontend (user flows) | N | N | N |
| Integration (vertical slice) | N | N | N |
| Integration (cross-feature) | N | N | N |
| **Total** | **N** | **N** | **N** |

### Test Results Summary

| Category | Tests | Pass | Fail | Error | Iterations to Fix |
|----------|-------|------|------|-------|-------------------|
| Backend API | N | N | N | N | N |
| Frontend UI | N | N | N | N | N |
| Integration | N | N | N | N | N |
| Pre-existing | N | N | N | N | N |
| **Total** | **N** | **N** | **N** | **N** | -- |

### Bugs Found & Fixed

For each bug:
- **What:** [description]
- **Where:** [file:line]
- **Category:** APP BUG / TEST BUG
- **Root cause:** [why it happened]
- **Fix:** [what was changed]
- **Commit:** [hash]
- **Iteration:** [which fix iteration]

### Unresolved Issues

Issues that could not be fixed within 5 iterations:
- **What:** [description]
- **Category:** APP BUG / TEST BUG / INFRASTRUCTURE
- **Why unresolved:** [complexity, architectural issue, external dependency, etc.]
- **Recommended action:** [specific skill or manual step]

### Coverage by Feature Area

| Feature | API Tests | UI Tests | Integration Tests | Pre-existing | Functional Coverage |
|---------|-----------|----------|-------------------|-------------|-------------------|
| Auth | Y/N | Y/N | Y/N | Y/N | X% |
| [Feature 1] | Y/N | Y/N | Y/N | Y/N | X% |
| [Feature 2] | Y/N | Y/N | Y/N | Y/N | X% |

Line coverage (if measurable):
- Backend: X%
- Frontend: X%
- Overall: X%

### Untested Critical Paths

List any critical paths that could not be tested:
- [Path] -- [reason: requires external service, needs manual trigger, etc.]

### Quality Assessment

Rate the application based on test results:
- **ROCK SOLID** -- All flows pass, no crashes, all edge cases handled, >90% functional coverage.
- **STABLE** -- Core flows pass, minor edge case gaps, >70% functional coverage.
- **FRAGILE** -- Some core flows fail. Needs targeted fixes. 50-70% functional coverage.
- **BROKEN** -- Multiple core flows fail. Significant issues. <50% functional coverage.

# CLEANUP

After the e2e run:
- Stop the backend server (kill recorded PID).
- Stop the frontend dev server (kill recorded PID).
- Stop Docker containers if started: docker compose down (including test-specific compose files).
- Stop Firebase emulators if started.
- Leave generated tests in the codebase -- they are now part of the test suite.
- Commit all generated tests: "test: add comprehensive e2e test suite"
- If app bugs were fixed, ensure those commits are separate from test commits.

# STRICT RULES

- Actually RUN the tests. This skill is meaningless without execution.
- Auto-detect the stack. Do NOT assume Flutter, React, or any specific framework.
- Cover BOTH backend AND frontend. API-only or UI-only testing is insufficient for /e2e.
  For BACKEND_ONLY projects, skip frontend phases. For FRONTEND_ONLY, skip backend phases.
  But if both exist, BOTH must be tested.
- Do not write tests that assert nothing. Every test must verify meaningful behavior.
- Do not delete failing tests to make the suite green. Fix the app or fix the test.
- Do not weaken assertions (e.g., removing status code checks, loosening regex matches).
- Do not hardcode test data that only works once. Use timestamps, UUIDs, or unique generators.
- Fix bugs in the app code, not just in tests. If an API returns 500 instead of 400, fix the API.
- Commit fixes incrementally with descriptive conventional commit messages.
- Do not install test frameworks the project already has. Use what exists.
- Do not regenerate tests that already exist and pass. Extend and complement.
- If a fix requires architectural changes beyond the scope of a test fix, note it and
  recommend /iterate rather than hacking a workaround.
- Keep the test suite maintainable -- use helpers, avoid duplication, use descriptive names.
- Every generated test file must compile/parse without errors before attempting to run.
- Prefer data-testid attributes (web) or Key widgets (Flutter) for selectors. Fall back to
  text/CSS selectors only when necessary.
- Test data must be realistic but clearly identifiable as test data (e.g., "E2E Test User"
  not "foo" or "test123").

# NEXT STEPS

- "All tests passing? Run `/qa` for a full functional + design quality audit."
- "Coverage gaps? Run `/iterate` to add missing functionality for untested paths."
- "Unresolved app bugs? Run `/iterate-review` on the specific failing areas."
- "Run `/analyze` to verify domain consistency across all layers."
- "Run `/manual-test-plan` to generate a human-walkable QA plan complementing these automated tests."
- "Run `/walkthrough` for Flutter-specific simulator-based exhaustive UI testing."
