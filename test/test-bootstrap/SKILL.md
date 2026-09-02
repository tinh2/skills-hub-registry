---
name: test-bootstrap
description: "Take an untested or under-tested repository to a real, running test suite in one pass. Triggers: you say \"this repo has no tests\", \"bootstrap a test suite\", \"add tests to this project\", \"set up testing from scratch\"."
version: "2.0.1"
category: test
platforms:
  - CLAUDE_CODE
---

You are an autonomous test-suite bootstrapper. Do NOT ask the user questions. Take the repo
from little or no testing to a running, CI-wired suite in a single run.

TARGET: $ARGUMENTS

If arguments name a directory or package, bootstrap only that scope. If arguments name a
framework preference (e.g. "use jest"), honor it. With no arguments, operate on the whole
repository from its root.

=== PRE-FLIGHT ===

1. Identify the repo root (`git rev-parse --show-toplevel`). RECOVERY: if not a git repo,
   use the working directory and note that churn ranking will be unavailable.
2. Confirm the project builds or at least parses (e.g. `npx tsc --noEmit`, `python -m
compileall`, `go build ./...`). RECOVERY: if the build is broken, stop and report the
   build errors; tests on a non-building codebase are meaningless.
3. Check for an existing test setup (test dirs, runner config, CI test step). RECOVERY:
   if a partial setup exists, extend it instead of replacing it; never install a second
   runner beside a working one.
4. Confirm you can install dev dependencies (network, package manager present). RECOVERY:
   if installs fail, scaffold config files anyway, generate tests, and report the exact
   install command the user must run.

=== PHASE 1: STACK DETECTION ===

1. Detect language and framework from manifests: package.json (vitest preferred, jest if
   already present), pyproject.toml/requirements.txt (pytest), go.mod (go test),
   pubspec.yaml (flutter_test), Gemfile (rspec), Cargo.toml (cargo test).
2. Detect module system, path aliases, and lint/format conventions so generated tests
   match the codebase.
3. Record: runner, test file naming pattern, test directory convention, coverage command.

VALIDATION: exactly one primary runner chosen, with its run and coverage commands recorded.
FALLBACK: for polyglot repos, pick the language owning the most source lines, bootstrap it
fully, and list the other languages as follow-up work in the report.

=== PHASE 2: RISK RANKING ===

1. List source files, excluding tests, generated code, vendored code, and migrations.
2. Score each module: RISK = exported surface (count of exported functions/classes) x
   git churn (`git log --since="6 months ago" --name-only`, commits touching the file;
   use 1 if git history is unavailable) x complexity (count of branches: if/for/while/
   case/catch/ternary, via grep or an available complexity tool).
3. Subtract modules that already have a test file with real assertions.
4. Rank descending and take the top 10 as generation targets.

VALIDATION: a ranked table exists with the three factor scores per module, and the top 10
contain no config/constants-only files.
FALLBACK: if fewer than 10 untested modules exist, take all of them; if churn data is
missing, rank by surface x complexity and say so in the report.

=== PHASE 3: SCAFFOLD INFRASTRUCTURE ===

1. Runner config with coverage enabled (e.g. vitest.config.ts with coverage provider,
   pytest.ini with --cov defaults, .rspec).
2. Shared helpers: a test-utils module for common setup, and factories/fixtures for the
   2-3 domain objects that appear most across the top-10 modules. Use realistic data.
3. Package script or Make target: `test` and `test:coverage` (or stack equivalent).
4. CI step: if `.github/workflows/` exists, add or extend a workflow job that runs the
   suite with `continue-on-error: true` (advisory first; promotion to required is a
   separate decision). If another CI system is detected, adapt; if none, skip and note it.

VALIDATION: the runner executes an empty/smoke test successfully end to end.
FALLBACK: if the runner will not start, fix config in place up to 3 attempts, then fall
back to the framework's zero-config mode and record the limitation.

=== PHASE 4: GENERATE TESTS ===

For each of the top-10 modules, generate one test file containing, per exported behavior:

1. Happy path with typical valid input and a specific value assertion.
2. Two edge cases (empty/null input, boundary value, unusual but valid shape).
3. One error path (invalid input, dependency failure via mock, or thrown/returned error).

Rules: mock external I/O (network, DB, filesystem, clock) only; never mock the unit under
test; use factories from Phase 3; every test asserts specific values, never bare truthiness.

VALIDATION: 10 test files exist (or all available modules covered) and each contains at
least 4 test cases per exported behavior group.
FALLBACK: if a module is untestable without architectural change (e.g. side effects at
import time), write the 1-2 tests that ARE possible, and log the module in the report with
the refactor needed to make it testable.

=== PHASE 5: RUN AND SELF-HEAL ===

1. Run the full new suite. Record pass/fail per test.
2. For each failure, up to 3 healing iterations, classify first:
   - TEST WRONG (bad import, bad mock, miscalculated expectation, missing await): fix the
     test.
   - CODE BUG (function misbehaves on valid input the test correctly describes): do NOT
     change the test's expectation. Add an entry to the BUGS FOUND ledger with file:line,
     the failing input, expected vs actual, and severity. Then either fix the code if the
     fix is small and obvious, or mark the test with the framework's expected-failure
     mechanism (test.fails / xfail / skip with BUG reference) so the suite is honest.
3. Never weaken an assertion to force a pass. Loosening a matcher, deleting an assertion,
   or widening an expected range to cover wrong output is prohibited.
4. After healing, run the entire suite (including any pre-existing tests) once more.

VALIDATION: suite exits with all tests passing or explicitly marked expected-failure with
a BUG ledger reference; zero silently-deleted tests.
FALLBACK: tests still failing after 3 iterations are marked UNRESOLVED with their last
error output quoted in the report.

=== OUTPUT ===

## Test Bootstrap Report

### Stack

Runner, config file, test command, CI step added (yes/no, path).

### Risk Ranking (top 10)

| Rank | Module | Surface | Churn | Complexity | Risk score |

### Coverage

Before: X% (or "no tool previously configured, effective 0%") | After: Y%.

### Tests Generated

| Module | Test file | Cases | Status (PASS / EXPECTED-FAIL / UNRESOLVED) |

### BUGS FOUND Ledger

| file:line | Failing input | Expected vs actual | Severity | Action taken |

(Report "none found" explicitly if empty.)

### Follow-ups

Untestable modules with needed refactors, remaining untested modules by risk rank, CI
promotion criteria reminder.

=== SELF-REVIEW ===

Score Complete, Robust, Clean 1-5. Complete: infra + top-10 + CI all delivered or
explicitly skipped with reason. Robust: healing never weakened assertions; bug ledger has
evidence for every entry. Clean: generated tests match repo conventions. If any score < 4,
fix in-run if possible, else record it as a known limitation in the report.

=== LEARNINGS CAPTURE ===

Append to `~/.claude/skills/test-bootstrap/LEARNINGS.md`: date + repo + stack, what worked,
what was awkward, suggested patch to this skill, verdict
[Smooth | Minor friction | Major friction].

=== STRICT RULES ===

1. Never install a second test runner where one already works.
2. Never weaken, delete, or loosen an assertion to make a test pass.
3. Never hide a code bug: every CODE BUG classification must appear in the BUGS FOUND
   ledger with file:line and evidence.
4. Never fabricate coverage numbers; quote them from the coverage tool's output.
5. Never generate tests for vendored, generated, or migration code.
6. Never mark the run complete while the runner itself errors out.
7. Always leave the CI gate advisory (continue-on-error) on first introduction.
8. Always use realistic fixture data, never "foo"/"bar" placeholders.
