---
name: hotfix
description: Emergency bug fix pipeline — diagnose, fix, test, commit, push, and PR in 2 iterations max. Speed over perfection.
version: "1.0.0"
category: build
platforms:
  - CLAUDE_CODE
---

You are in EMERGENCY MODE. Fix the bug and ship. Do NOT ask questions.

Maximum 2 iterations. Do NOT refactor surrounding code. Do NOT improve anything
beyond the bug. Apply the minimal correct fix.

INPUT: $ARGUMENTS
Bug description, error message, stack trace, or area that's broken.

============================================================
BRANCH SAFETY
============================================================

Before making any changes:
1. Check the current branch: `git branch --show-current`
2. If on main, master, or develop: create a hotfix branch first:
   `git checkout -b hotfix/{short-description}`
   Use a slugified version of the bug description (e.g., hotfix/null-pointer-user-login).
3. If already on a feature or hotfix branch: stay on it.

============================================================
ITERATION 1: DIAGNOSE AND FIX
============================================================

1. DIAGNOSE:
   - Parse the error message, stack trace, or bug description.
   - Search the codebase for the failing code path (grep class names, method names, error strings).
   - Read the relevant files. Trace the execution path.
   - Identify the root cause.

2. FIX:
   - Apply the minimal fix. Change as few lines as possible.
   - Do NOT refactor. Do NOT clean up. Do NOT add comments.
   - If the fix requires a database change, create a migration (follow /db-migrate conventions).

3. TEST:
   Auto-detect the project type and run the appropriate test suite:
   - Scala (build.sbt): `ENVIRONMENT=test sbt "testOnly *AffectedSpec*"`
     If no specific test identified: `ENVIRONMENT=test sbt test`
   - Flutter (pubspec.yaml): `flutter test`
   - Node.js (package.json): `npx vitest run` or `npm test`
   - If tests pass → go to SHIP.
   - If tests fail → go to ITERATION 2.

============================================================
ITERATION 2: REFINE (only if iteration 1 tests failed)
============================================================

1. Analyze the test failures from iteration 1.
2. Adjust the fix based on what the tests revealed.
3. Re-run the test suite.
4. If still failing → STOP. Report what you found and what you tried.

============================================================
SHIP
============================================================

1. Stage ONLY the files you changed (no unrelated files).
2. Commit:
   ```
   fix: {brief description of what was broken and fixed}

   deploy:tho
   ```
   Do NOT include Co-Authored-By lines.
3. Push immediately.
4. Create PR with `gh pr create`:
   - Title: `fix: {brief description}` (under 70 chars)
   - Body:
     ```
     ## Summary
     - **Bug:** {what was broken}
     - **Cause:** {root cause}
     - **Fix:** {what was changed}

     ## Test Plan
     - [ ] {relevant test verification}
     - [ ] All existing tests pass
     ```
   - Do NOT reference Claude, AI, or include any AI attribution.
   - Extract story number from branch name if present and link Jira.

OUTPUT:
## Hotfix Shipped
- **Bug:** {what was broken}
- **Cause:** {root cause}
- **Fix:** {file:line — what changed}
- **Tests:** {pass/fail, count}
- **PR:** {URL}
- **Iterations:** {1 or 2}/2
