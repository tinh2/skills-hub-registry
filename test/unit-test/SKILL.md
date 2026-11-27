---
name: unit-test
description: "Find untested code, write unit tests covering edge cases, error paths and boundaries in the project's own style, run them and fix failures. Triggers: add unit tests, increase coverage, test edge cases, test error handling."
version: "2.1.0"
category: test
platforms:
  - CLAUDE_CODE
---

Find the code that most needs tests, write unit tests that would catch real regressions, run them, and get them green without weakening anything. Work autonomously.

**Scope:** `$ARGUMENTS` (files, modules or functions) if given; otherwise the whole project.

## 1. Learn the setup

- Detect the framework from config (Vitest, Jest, pytest, go test, JUnit, RSpec, flutter_test, cargo test, xUnit/NUnit, Mocha). Use the one that's configured; if none is, add Vitest for Node, pytest for Python, or the language's built-in runner.
- Read existing tests and copy their conventions exactly: file naming and location, import style and aliases, mocking library, assertion style, fixtures and helpers. New tests should look like the same person wrote them.

## 2. Find the gaps

Get a baseline from the coverage tool if one is configured (`vitest run --coverage`, `jest --coverage`, `pytest --cov=. --cov-report=term-missing`, `go test -coverprofile=c.out ./... && go tool cover -func=c.out`, `flutter test --coverage`, `cargo tarpaulin`). Otherwise, pair source files with test files and read the untested ones.

Prioritize: business logic, auth, payments and validation first; then handlers, services and data access; then utilities. Skip constants, types, trivial getters and generated code (migrations, build output, declarations).

## 3. Write the tests

For each target, cover:

- **Happy paths** with realistic inputs, checking return values and side effects.
- **Edge cases:** null/undefined, empty strings/collections, zero and negatives, very large or long values, unicode, whitespace-only.
- **Error paths:** invalid types, missing params, I/O or network failure, timeouts, permission failures.
- **Boundaries:** min, max, and one past each.

Mock external dependencies (DB, HTTP, filesystem, clock, randomness, env, third-party SDKs) with realistic return values; reset them between tests. Don't mock the unit under test or pure logic it relies on.

Each test checks one behavior, has a name that states the expected outcome, asserts specific values (not just truthiness), and is independent and deterministic.

## 4. Run and heal (up to 3 passes per failing test)

Run the new tests, then diagnose each failure:

- **Test bug** (wrong import, bad mock, wrong expected value, missing `await`, leaking state): fix the test.
- **App bug** (throws on valid input, wrong result, unhandled edge case): fix the code, and call it out in the report.

Never delete a test, skip it, or loosen an assertion to get green. After 3 passes, mark it UNRESOLVED with the reason; if a fix needs an architectural change, note it and move on. Finish by running the full suite to confirm nothing existing broke, then measure coverage again.

## Output

```
## Unit Test Generation Report
### Stack: language, framework, conventions followed
### Coverage Before: X% line (or "no coverage tool"), N untested files / functions

| Source File | Test File | Tests Added | Priority | Status |

### Self-Healing: fixed per pass; Unresolved: N (reasons)
### App bugs found and fixed: list
### Coverage After: X% line (+N), X% branch; remaining uncovered files
### Breakdown: happy N / edge N / error N / boundary N; total N
```

Suggest follow-ups where useful: `/integration-test`, `/e2e`, `/test-suite`, `/qa`.

## Telemetry

If a project memory directory exists under `~/.claude/projects/`, append to its `skill-telemetry.md` (skip silently otherwise):

```
### /unit-test — YYYY-MM-DD
- Outcome: SUCCESS | PARTIAL | FAILED
- Self-healed: yes (what) | no
- Iterations used: N / 3
- Bottleneck: phase that struggled, or none
- Suggestion: one-line improvement, or none
```
