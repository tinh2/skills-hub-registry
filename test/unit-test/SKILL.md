---
name: unit-test
description: "Generate comprehensive unit tests with edge cases, error paths, and boundary values. Triggers: you need to add unit tests, increase code coverage, test edge cases, or verify error handling paths."
version: "2.0.1"
category: test
platforms:
  - CLAUDE_CODE
---

You are in AUTONOMOUS MODE. Do NOT ask questions. Detect the project's test framework,
find untested code, generate comprehensive unit tests, run them, and fix failures
in a self-healing loop.

INPUT:
$ARGUMENTS

If arguments are provided, focus on those specific files, modules, or functions.
If no arguments are provided, scan the ENTIRE project for untested code.

============================================================
PHASE 1: FRAMEWORK DETECTION
============================================================

Step 1.1 -- Detect Test Framework

Scan for configuration files and determine the test framework:

| Indicator | Framework | Language |
|---|---|---|
| vitest.config.* or "vitest" in package.json | Vitest | TypeScript/JavaScript |
| jest.config.* or "jest" in package.json | Jest | TypeScript/JavaScript |
| pytest.ini, pyproject.toml [tool.pytest], conftest.py | pytest | Python |
| go.mod + *_test.go files | go test | Go |
| pom.xml with junit or build.gradle with junit | JUnit | Java/Kotlin |
| Gemfile with rspec | RSpec | Ruby |
| pubspec.yaml with flutter_test | flutter_test | Dart/Flutter |
| Cargo.toml + #[cfg(test)] | cargo test | Rust |
| *.csproj with xunit or nunit | xUnit/NUnit | C#/.NET |
| .mocharc.* or "mocha" in package.json | Mocha | JavaScript |

If no test framework is detected, install the most appropriate one:
- Node.js projects: install Vitest (preferred) or Jest
- Python projects: install pytest
- Other stacks: use the built-in test runner

Record: framework name, config file path, test directory convention, test file naming pattern.

Step 1.2 -- Detect Test Conventions

Read existing test files (if any) to learn project conventions:

- File naming: *.test.ts, *.spec.ts, *_test.go, test_*.py, *_test.dart
- Directory structure: co-located with source, separate test/ directory, __tests__/
- Import patterns: relative imports, path aliases, barrel imports
- Mock patterns: jest.mock, vi.mock, unittest.mock, gomock, mockito
- Assertion style: expect().toBe(), assert, assertEqual, should
- Setup/teardown patterns: beforeEach, setUp, TestMain
- Describe/it vs test blocks
- Custom helpers or fixtures in use

Adopt ALL existing conventions. New tests must look like they were written by
the same developer who wrote the existing tests.

============================================================
PHASE 2: COVERAGE ANALYSIS
============================================================

Step 2.1 -- Run Existing Coverage

If coverage tools are configured, run them to get a baseline:

| Framework | Command |
|---|---|
| Vitest | npx vitest run --coverage |
| Jest | npx jest --coverage |
| pytest | pytest --cov=. --cov-report=term-missing |
| go test | go test -coverprofile=coverage.out ./... && go tool cover -func=coverage.out |
| flutter_test | flutter test --coverage |
| cargo test | cargo tarpaulin --out Stdout |

Parse the output to identify:
- Files with 0% coverage (highest priority)
- Files with < 50% coverage
- Specific uncovered lines/functions

Step 2.2 -- Scan for Untested Code

If no coverage data is available, scan manually:

1. List all source files (exclude test files, config, generated code, migrations).
2. For each source file, check if a corresponding test file exists.
3. For files without tests, read the file and catalog:
   - Exported functions/methods
   - Class methods (public and protected)
   - Business logic functions (anything with conditionals, loops, calculations)
   - Utility/helper functions
   - Error handling paths

Build the untested code inventory:

| Source File | Functions | Complexity | Test File Exists | Priority |
|------------|-----------|------------|-----------------|----------|

Priority ranking:
- CRITICAL: Business logic, auth, payment, data validation
- HIGH: API handlers, service layer, data access
- MEDIUM: Utilities, helpers, formatters
- LOW: Constants, types, simple getters/setters

============================================================
PHASE 3: TEST GENERATION
============================================================

Step 3.1 -- Generate Test Files

For each untested source file (ordered by priority), generate a test file.

FOLLOW THE PROJECT'S CONVENTIONS for file naming and location.

Each test file must include:

IMPORTS:
- Import the module under test
- Import test framework utilities
- Import mock libraries if needed
- Import types/interfaces used by the module

HAPPY PATH TESTS:
- Test each function with valid, typical inputs
- Verify return values match expected output
- Verify side effects (database writes, API calls, state changes)
- Test with multiple valid input variations

EDGE CASE TESTS:
- Null/undefined/nil inputs
- Empty strings, empty arrays, empty objects
- Zero values, negative numbers
- Maximum boundary values (MAX_INT, very long strings)
- Unicode and special characters
- Whitespace-only strings

ERROR PATH TESTS:
- Invalid input types
- Missing required parameters
- Out-of-range values
- Network/IO failure scenarios (with mocks)
- Timeout scenarios
- Permission/authorization failures
- Concurrent access conflicts

BOUNDARY VALUE TESTS:
- Minimum valid input
- Maximum valid input
- One below minimum (should fail)
- One above maximum (should fail)
- Exactly at boundary

Step 3.2 -- Mock Strategy

Use mocks appropriately:

MOCK THESE (external dependencies):
- Database queries and connections
- HTTP/API calls to external services
- File system operations
- Time/date functions (use deterministic values)
- Random number generators
- Environment variables
- Third-party SDK calls

DO NOT MOCK THESE (test the real thing):
- The function under test
- Pure utility functions
- Data transformation logic
- Validation logic
- Business rule calculations

Mock setup pattern (adapt to detected framework):
- Create mocks in beforeEach/setUp
- Reset mocks in afterEach/tearDown
- Verify mock call counts and arguments where relevant
- Use realistic mock return values, not empty objects

Step 3.3 -- Test Quality Rules

Every generated test must:

- Have a descriptive name explaining what is tested and expected outcome
- Test exactly ONE behavior per test case
- Be independent (no test depends on another test's state)
- Be deterministic (no random values, no time-dependent assertions)
- Clean up after itself (reset mocks, clear state)
- Use realistic test data (not "foo", "bar", "test123")
- Assert specific values, not just truthiness
- Include both positive and negative assertions where appropriate

============================================================
PHASE 4: EXECUTION AND SELF-HEALING
============================================================

Step 4.1 -- Run Generated Tests

Execute the new tests:

| Framework | Command |
|---|---|
| Vitest | npx vitest run [test-files] --reporter=verbose |
| Jest | npx jest [test-files] --verbose --forceExit |
| pytest | pytest [test-files] -v --tb=short |
| go test | go test -v -run [TestPattern] ./... |
| flutter_test | flutter test [test-files] |
| RSpec | bundle exec rspec [test-files] --format documentation |
| cargo test | cargo test [test-names] -- --nocapture |
| JUnit | mvn test -Dtest=[TestClass] or gradle test --tests [TestClass] |

Record results for each test: PASS, FAIL (with error), or ERROR.

Step 4.2 -- Self-Healing Loop (max 3 iterations)

For each failing test, diagnose the failure:

CATEGORY A -- TEST BUG (fix the test):
- Wrong import path or module name
- Incorrect mock setup (wrong return type, missing mock)
- Wrong assertion value (expected output calculated incorrectly)
- Async handling missing (missing await, missing done callback)
- Setup/teardown not cleaning state properly
- Type mismatch in mock or assertion

CATEGORY B -- APP BUG (fix the application):
- Function throws on valid input (missing null check)
- Function returns wrong value (logic error)
- Function does not handle edge case (no validation)
- Error message is wrong or missing

FIX: Apply the appropriate fix, re-run ONLY the previously failing tests.

ITERATION RULES:
- Maximum 3 iterations per failing test
- If a test still fails after 3 iterations, mark it UNRESOLVED
- Never delete a test to make the suite green
- Never weaken an assertion (removing checks, loosening matchers)
- If the fix requires architectural changes, note it and skip

Step 4.3 -- Full Suite Verification

After the healing loop, run the ENTIRE test suite (existing + new tests):

Verify:
- All new tests pass
- No existing tests were broken by new code
- No regressions introduced

If existing tests broke, fix the regression before continuing.

============================================================
PHASE 5: COVERAGE MEASUREMENT
============================================================

Run coverage again with all tests (existing + new):

| Framework | Command |
|---|---|
| Vitest | npx vitest run --coverage |
| Jest | npx jest --coverage |
| pytest | pytest --cov=. --cov-report=term-missing |
| go test | go test -coverprofile=coverage.out ./... |
| flutter_test | flutter test --coverage |

Record the improvement: before vs. after coverage percentage.

============================================================
OUTPUT
============================================================

## Unit Test Generation Report

### Stack
- **Language:** [detected]
- **Framework:** [detected test framework]
- **Conventions:** [file naming, directory structure, assertion style]

### Coverage Before
- Line coverage: X% (or "no coverage tool configured")
- Untested files: N
- Untested functions: N

### Tests Generated

| Source File | Test File | Tests Added | Category | Status |
|------------|-----------|-------------|----------|--------|
| [source] | [test] | N | [CRITICAL/HIGH/MEDIUM/LOW] | [ALL PASS / N UNRESOLVED] |

### Self-Healing Summary
- Iteration 1: N fixed
- Iteration 2: N fixed
- Iteration 3: N fixed
- Unresolved: N (with reasons)

### Coverage After
- Line coverage: X% (+N% improvement)
- Branch coverage: X%
- Remaining uncovered files: [list]

### Test Breakdown
- Happy path tests: N
- Edge case tests: N
- Error path tests: N
- Boundary value tests: N
- **Total new tests:** N

NEXT STEPS:

- "Unit tests solid? Run `/integration-test` to test component interactions."
- "Want full E2E coverage? Run `/e2e` for end-to-end user flow testing."
- "Run `/test-suite` to see the overall test health score after adding unit tests."
- "Run `/qa` for a full quality audit beyond just test coverage."

DO NOT:

- Do NOT generate tests that assert nothing (empty test bodies, toBeTruthy on everything).
- Do NOT delete or skip existing tests.
- Do NOT mock the function under test.
- Do NOT generate tests for generated code (migrations, build output, type declarations).
- Do NOT use random or time-dependent values in assertions.
- Do NOT generate tests that depend on execution order.
- Do NOT install a different test framework if one is already configured.
- Do NOT weaken assertions to make tests pass. Fix the code or fix the test logic.


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /unit-test — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
