---
name: test-suite
description: Analyze and score test coverage across all testing dimensions -- unit, integration, E2E, load, visual regression, contract, and accessibility. Auto-detects tech stack and test infrastructure, runs existing coverage tools, identifies gaps by category, scores each on a 0-10 scale with weighted overall health, and produces a prioritized remediation plan routing to the right testing sub-skill. Use when you need a test health overview, want to find coverage gaps, need to prioritize which tests to write next, or want to assess test quality before a release.
version: "2.0.0"
category: test
platforms:
  - CLAUDE_CODE
---

You are in AUTONOMOUS MODE. Do NOT ask questions. Analyze the project's test coverage
across all testing dimensions, identify gaps, and produce an actionable health report.

INPUT:
$ARGUMENTS

If arguments are provided, focus analysis on those specific areas or modules.
If no arguments are provided, analyze the ENTIRE project.

============================================================
PHASE 1: PROJECT DISCOVERY
============================================================

Step 1.1 -- Tech Stack Detection

Auto-detect the project's technology stack by scanning for configuration files:

| File/Pattern | Stack |
|---|---|
| pubspec.yaml with flutter SDK | Flutter / Dart |
| package.json + tsconfig.json | TypeScript / Node.js |
| package.json (no TS) | JavaScript / Node.js |
| requirements.txt or pyproject.toml | Python |
| go.mod | Go |
| Cargo.toml | Rust |
| Gemfile | Ruby |
| pom.xml or build.gradle | Java / Kotlin |
| *.csproj or *.sln | C# / .NET |

Detect the application type:
- BACKEND_ONLY: API/service with no frontend
- FRONTEND_ONLY: Frontend app with external API
- FULLSTACK: Both backend and frontend
- MOBILE: Mobile app (Flutter, React Native, SwiftUI)
- LIBRARY: Reusable package or SDK

Record: language, framework, application type, entry points, source directories.

Step 1.2 -- Test Infrastructure Inventory

Scan the project for ALL existing test-related files and configuration:

DIRECTORIES to check:
- test/, tests/, __tests__/, spec/, e2e/, cypress/, integration_test/
- playwright/, .storybook/, k6/, locust/, artillery/, load-test/
- contract/, pact/, snapshots/, __snapshots__/

CONFIG FILES to check:
- jest.config.*, vitest.config.*, pytest.ini, pyproject.toml [tool.pytest]
- playwright.config.*, cypress.config.*, .mocharc.*
- .nycrc, .coveragerc, codecov.yml, lcov.info, coverage/
- backstop.json, .percy.yml, chromatic.config.*
- pact-config.*, dredd.yml, .spectral.yaml
- lighthouserc.*, .axe.json, pa11y.json

TEST SCRIPTS in package.json (or equivalent):
- test, test:unit, test:integration, test:e2e, test:load, test:visual, test:a11y
- coverage, lint, typecheck

Build a complete inventory table:

| Category | Framework | Config File | Test Directory | Test Count | Last Modified |
|----------|-----------|-------------|----------------|------------|---------------|

Step 1.3 -- Source Code Analysis

Count source files and estimate testable surface area:

- Total source files (exclude node_modules, vendor, build, dist)
- Total functions/methods exported or public
- Total API endpoints (routes, controllers)
- Total UI components or screens
- Total data models or entities

============================================================
PHASE 2: TEST COVERAGE ANALYSIS
============================================================

Step 2.1 -- Run Existing Coverage Tools

If coverage tools are configured, run them:

| Stack | Command |
|---|---|
| Node.js (Vitest) | npx vitest run --coverage --reporter=json |
| Node.js (Jest) | npx jest --coverage --json |
| Python | pytest --cov=. --cov-report=json |
| Go | go test -coverprofile=coverage.out ./... |
| Flutter | flutter test --coverage |
| Ruby | bundle exec rspec --format json |

Parse the coverage output to extract:
- Line coverage percentage
- Branch coverage percentage
- Function coverage percentage
- Files with 0% coverage
- Files with < 50% coverage

Step 2.2 -- Categorize Existing Tests

Read every test file and classify each test into a category:

| Category | Indicators |
|----------|-----------|
| Unit | Tests a single function/method in isolation, uses mocks/stubs |
| Integration | Tests multiple components together, may use real DB or services |
| E2E | Tests full user flows, uses browser/simulator, hits real endpoints |
| Load/Performance | Uses k6, Locust, Artillery, or measures response times |
| Visual Regression | Captures screenshots, compares images, uses Percy/Chromatic |
| Contract | Validates API schemas, uses Pact/OpenAPI/Dredd |
| Accessibility | Uses axe-core, pa11y, Lighthouse, checks WCAG compliance |
| Snapshot | Jest/Vitest snapshot tests |
| Smoke | Basic health checks, minimal coverage |

Build the categorized test count:

| Category | Test Files | Test Cases | Coverage Area |
|----------|-----------|------------|---------------|

Step 2.3 -- Gap Identification

For each testing category, assess whether coverage exists and rate it:

UNIT TESTS:
- Are business logic functions covered?
- Are utility/helper functions covered?
- Are edge cases tested (null, empty, boundary values)?
- Are error paths tested?

INTEGRATION TESTS:
- Are API endpoints tested end-to-end?
- Are database operations tested (CRUD, transactions)?
- Are external service integrations tested (with mocks)?
- Are authentication/authorization flows tested?

E2E TESTS:
- Are critical user flows covered?
- Are form submissions tested?
- Are navigation flows tested?
- Are error states tested?

LOAD TESTS:
- Are performance baselines established?
- Are critical endpoints load-tested?
- Are spike/stress scenarios defined?

VISUAL REGRESSION TESTS:
- Are critical pages captured at multiple breakpoints?
- Is there a baseline for comparison?
- Are dynamic content areas handled?

CONTRACT TESTS:
- Are API schemas validated?
- Is backward compatibility verified?
- Are consumer-driven contracts in place?

ACCESSIBILITY TESTS:
- Are WCAG 2.1 AA standards checked?
- Is keyboard navigation tested?
- Are all routes/pages scanned?
- Is Lighthouse CI configured?

============================================================
PHASE 3: SCORING AND HEALTH REPORT
============================================================

Step 3.1 -- Score Each Category

Rate each testing category on a 0-10 scale:

| Score | Meaning |
|-------|---------|
| 0 | No tests exist |
| 1-2 | Minimal: fewer than 5 tests, only happy paths |
| 3-4 | Basic: some coverage but major gaps in edge cases or error paths |
| 5-6 | Moderate: reasonable coverage, some categories of tests missing |
| 7-8 | Good: comprehensive coverage with minor gaps |
| 9-10 | Excellent: thorough coverage including edge cases, errors, boundaries |

Calculate an overall health score as a weighted average:
- Unit tests: 30% weight
- Integration tests: 25% weight
- E2E tests: 20% weight
- Load tests: 5% weight
- Visual regression: 5% weight
- Contract tests: 5% weight
- Accessibility: 10% weight

Step 3.2 -- Priority Ranking

Rank gaps by impact. Consider:
- What breaks production most often? (usually integration + unit gaps)
- What blocks releases? (usually E2E + contract gaps)
- What causes user complaints? (usually a11y + visual gaps)
- What causes incidents? (usually load + integration gaps)

============================================================
PHASE 4: REMEDIATION ROUTING
============================================================

For each identified gap, recommend which sub-skill to run:

| Gap | Skill to Run | Priority |
|-----|-------------|----------|
| No unit tests or < 50% coverage | `/unit-test` | CRITICAL |
| No integration tests | `/integration-test` | CRITICAL |
| No E2E tests | `/e2e` | HIGH |
| No load tests for API projects | `/load-test` | MEDIUM |
| No visual regression (frontend) | `/visual-regression` | MEDIUM |
| No contract tests (API projects) | `/contract-test` | MEDIUM |
| No a11y tests (frontend) | `/accessibility-test` | HIGH |


============================================================
SELF-HEALING VALIDATION (max 3 iterations)
============================================================

After generating and running tests, validate:

1. All generated test files compile/parse without syntax errors.
2. Run the generated tests — capture pass/fail results.
3. If tests fail due to test code bugs (not application bugs), fix the test code.
4. Re-run to confirm tests pass or legitimately fail on application issues.
5. Repeat up to 3 iterations.

IF STILL FAILING after 3 iterations:
- Separate test failures into: test bugs vs application bugs
- Fix test bugs, document application bugs

============================================================
OUTPUT
============================================================

Print the full health report:

## Test Coverage Health Report

### Project Summary
- **Project:** [name from package.json, pubspec.yaml, etc.]
- **Stack:** [language + framework]
- **Type:** [BACKEND_ONLY / FRONTEND_ONLY / FULLSTACK / MOBILE / LIBRARY]
- **Source files:** [count]
- **Testable surface:** [endpoints, components, functions count]

### Coverage Scores

| Category | Score (0-10) | Tests | Status |
|----------|-------------|-------|--------|
| Unit Tests | N | N tests | [MISSING / WEAK / MODERATE / STRONG / EXCELLENT] |
| Integration Tests | N | N tests | [status] |
| E2E Tests | N | N tests | [status] |
| Load Tests | N | N tests | [status] |
| Visual Regression | N | N tests | [status] |
| Contract Tests | N | N tests | [status] |
| Accessibility | N | N tests | [status] |
| **Overall Health** | **N/10** | **N total** | **[verdict]** |

### Line Coverage (if available)
- Overall: X%
- Files with 0% coverage: [list top 10]

### Critical Gaps (prioritized)

1. **[Gap]** -- [why it matters] -- Run: `/[skill]`
2. **[Gap]** -- [why it matters] -- Run: `/[skill]`
3. ...

### Existing Test Quality Notes
- [observations about test quality, naming, organization, flakiness]

### Recommended Test Plan

Run these skills in order to achieve comprehensive coverage:
1. `/[skill]` -- [what it will add]
2. `/[skill]` -- [what it will add]
3. ...

Estimated improvement: current N/10 -> projected N/10 after remediation.

NEXT STEPS:

- "Critical unit test gaps? Run `/unit-test` to generate missing unit tests."
- "No integration tests? Run `/integration-test` to cover API and database operations."
- "Frontend with no visual regression? Run `/visual-regression` to set up baseline screenshots."
- "API without contract tests? Run `/contract-test` to validate schemas."
- "Accessibility gaps? Run `/accessibility-test` to check WCAG 2.1 AA compliance."
- "Need load testing? Run `/load-test` to establish performance baselines."
- "Want full E2E coverage? Run `/e2e` for comprehensive end-to-end testing."

DO NOT:

- Do NOT generate or run tests in this skill. This is analysis and routing only.
- Do NOT modify any source code or test files.
- Do NOT install any packages or frameworks.
- Do NOT skip any testing category in the analysis, even if it seems irrelevant.
- Do NOT inflate scores. A category with zero tests gets a zero score.
- Do NOT recommend skills that are irrelevant to the project type (e.g., no visual regression for a CLI tool, no load tests for a static library).


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /test-suite — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
