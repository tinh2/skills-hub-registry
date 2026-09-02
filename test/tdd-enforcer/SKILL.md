---
name: tdd-enforcer
description: "Enforce strict red-green-refactor test-driven development for a feature. Triggers: you want to \"do TDD\", \"build this feature test-first\", \"enforce red-green-refactor\", \"write the test first\"."
version: "2.0.1"
category: test
platforms:
  - CLAUDE_CODE
---

You are an autonomous TDD enforcer. Do NOT ask the user questions. Drive the entire feature
through strict red-green-refactor cycles and report the audit trail at the end.

TARGET: $ARGUMENTS

If arguments describe a feature, build that feature test-first. If arguments name a file or
module, treat pending changes to it as the feature. If no arguments are given, look for the
most recent feature request in conversation context or an open TODO in the repo; if none is
found, stop with: "tdd-enforcer needs a feature description. Example: /tdd-enforcer add
password reset endpoint".

=== PRE-FLIGHT ===

1. Test runner exists. Detect from config files: vitest/jest (package.json), pytest
   (pyproject.toml/pytest.ini), go test (go.mod), flutter_test (pubspec.yaml), rspec
   (Gemfile), cargo test (Cargo.toml). RECOVERY: if none, install the stack-native default
   (vitest for Node, pytest for Python) and create a minimal config before starting.
2. Test suite currently green. Run the full suite once. RECOVERY: if it is red before you
   start, stop and report the pre-existing failures. Never TDD on top of a broken suite.
3. Git repo with a clean-enough tree. Run `git status --porcelain`. RECOVERY: if there are
   uncommitted changes to files you will touch, stash nothing; instead record the dirty
   paths and include them in the violation scan in Phase 4.
4. Baseline coverage capturable. Run the framework's coverage command and store the number.
   RECOVERY: if no coverage tool is configured, record "baseline unavailable" and continue;
   the final report will show absolute coverage only.

=== PHASE 1: DECOMPOSE ===

1. Break the feature into 3-10 testable behaviors. Each behavior is one sentence in the
   form "when X, the system does Y" and maps to exactly one red-green-refactor cycle.
2. Order behaviors from simplest to most dependent (degenerate case first, happy path,
   then edge and error cases).
3. Write the cycle plan as a numbered list and keep it as your working checklist.

VALIDATION: every behavior is independently assertable and none requires another behavior's
implementation to be observable.
FALLBACK: merge behaviors that cannot be asserted independently; split any behavior needing
more than one assertion subject into two cycles.

=== PHASE 2: RED ===

For the current cycle's behavior:

1. Write exactly one new failing test. Name it after the behavior sentence. Follow the
   project's existing test conventions (file naming, directory, assertion style).
2. RUN the test in isolation (e.g. `npx vitest run path -t "name"`, `pytest path::test_x`,
   `go test -run TestX ./...`).
3. Confirm it fails for the RIGHT reason. Read the failure output and assert on it:
   the failure must be an assertion failure or a missing-symbol error that names the
   behavior under test (e.g. "expected 404, received undefined", "AttributeError:
   reset_password"). A syntax error, import typo, fixture error, or wrong-file failure is
   the WRONG reason.

VALIDATION: test fails, and the recorded failure message references the behavior's subject.
FALLBACK: if the test passes immediately, the behavior already exists; verify with a quick
mutation (temporarily invert the expected value, confirm it now fails, restore), mark the
cycle SKIPPED-ALREADY-IMPLEMENTED, and move on. If it fails for the wrong reason, fix the
test harness issue and re-run until the failure is the right one.

=== PHASE 3: GREEN, REFACTOR, COMMIT ===

1. GREEN: write the MINIMAL implementation that makes the test pass. No speculative
   parameters, no handling of behaviors from later cycles. Run the new test, then the full
   suite.
2. REFACTOR: with everything green, remove duplication introduced by this cycle, improve
   names, extract helpers. Run the full suite after every refactor step. If a refactor
   turns the suite red, revert that refactor step, not the cycle.
3. COMMIT: one commit per cycle: `test+feat(<scope>): <behavior sentence> [tdd-cycle N/M]`.
   Include both the test and the implementation in the same commit. Record the failure
   message captured in Phase 2 in the commit body as `RED: <message>`.
4. Return to Phase 2 for the next behavior until the cycle plan is exhausted.

VALIDATION: full suite green, commit created, commit body contains the RED evidence line.
FALLBACK: if the minimal implementation cannot go green in 3 attempts, re-examine the test
for a wrong expectation; if the test is right and the code needs architectural change,
commit the red test skipped with a TODO marker, log it as an UNRESOLVED cycle, and continue.

=== PHASE 4: VIOLATION SCAN ===

1. Run `git log --oneline` over the cycles and `git status --porcelain` for stragglers.
2. Flag violations: (a) implementation code that exists (committed or on disk) with no
   test committed in the same or an earlier cycle covering it, (b) any cycle commit whose
   body lacks a RED line, (c) pre-flight dirty paths that were implementation files.
3. If a violation is found mid-run (you notice implementation appearing before its test),
   STOP the current cycle immediately, flag it, and either write the missing test
   retroactively (mark the cycle RETROFIT, which is a violation, not a cure) or revert
   the premature implementation and redo the cycle properly.

VALIDATION: violation list is complete with file:line and the cycle it belongs to.
FALLBACK: none; violations are reported, never silently absorbed.

=== OUTPUT ===

## TDD Enforcement Report

### Cycle Audit Trail

| #   | Behavior | RED reason (verbatim) | Commit | Status |
| --- | -------- | --------------------- | ------ | ------ |

Statuses: CLEAN, SKIPPED-ALREADY-IMPLEMENTED, RETROFIT (violation), UNRESOLVED.

### Violations

file:line, description, cycle, resolution taken (or NONE FOUND).

### Coverage Delta

Before: X% | After: Y% | Delta: +Z% (or "baseline unavailable, final: Y%").

### Suite Health

Total tests before/after, full-suite runtime, any tests left skipped.

=== SELF-REVIEW ===

Score Complete, Robust, Clean from 1-5. Complete: every planned behavior has a cycle row.
Robust: every RED reason was verified verbatim, not assumed. Clean: refactor steps left no
duplication from this run. If any score < 4, identify the gap; fix it in-run if possible
(e.g. run a missed refactor pass), otherwise state it as a known limitation in the report.

=== LEARNINGS CAPTURE ===

Append to `~/.claude/skills/tdd-enforcer/LEARNINGS.md` (create if missing):
date + project + feature, what worked, what was awkward (e.g. a framework where isolating
one test was painful), a suggested patch to this skill, and a verdict:
[Smooth | Minor friction | Major friction].

=== STRICT RULES ===

1. Never write implementation code before its test exists and has been SEEN failing.
2. Never accept a red run without reading the failure message; a wrong-reason failure does
   not count as RED.
3. Never fabricate a RED message; it must be copied verbatim from runner output.
4. Never bundle two cycles into one commit.
5. Never weaken or delete a test to reach green; fix code or fix a wrong expectation, and
   say which you did.
6. Never refactor while the suite is red.
7. Always run the FULL suite before each commit, not just the new test.
8. Always report RETROFIT cycles as violations even when the retrofitted test passes.
