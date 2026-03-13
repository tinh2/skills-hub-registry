---
name: hotfix
description: >
version: 1.0.0
category: deploy
  Emergency hotfix pipeline — diagnose, fix, test, commit, push, and PR
  in 2 iterations max. Triggers: "emergency fix", "hotfix", "quick bug fix",
  "fix and push", "critical bug", "urgent fix".
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
LOG ANALYSIS
============================================================

Before diving into code, check for recent evidence:
1. Look for error/crash logs in common locations:
   - `log/`, `logs/`, `tmp/`, `.log` files in the project root
   - CI artifacts: check `gh run list --limit 3` for recent failures,
     then `gh run view {id} --log-failed` for details
   - Docker logs if applicable: `docker compose logs --tail=50`
2. Parse any stack traces or error messages from logs to narrow the search.
3. If the user provided a stack trace, skip this step and use that directly.

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
   - If the fix requires a database change, create a migration following project conventions.

3. TEST:
   Auto-detect the project type and run the appropriate test suite.
   Check for these files in order and run the first match:

   | Marker file          | Framework    | Command                                              |
   |----------------------|--------------|------------------------------------------------------|
   | `build.sbt`          | Scala/sbt    | `ENVIRONMENT=test sbt "testOnly *AffectedSpec*"` (or `sbt test` if no specific test) |
   | `Cargo.toml`         | Rust         | `cargo test`                                         |
   | `go.mod`             | Go           | `go test ./...`                                      |
   | `pubspec.yaml`       | Flutter/Dart | `flutter test`                                       |
   | `Gemfile`            | Ruby         | `bundle exec rspec` (or `bundle exec rake test`)     |
   | `build.gradle*`      | Java/Kotlin  | `./gradlew test`                                     |
   | `pom.xml`            | Java/Maven   | `mvn test`                                           |
   | `pyproject.toml`     | Python       | `pytest` (or `python -m pytest`)                     |
   | `setup.py`/`setup.cfg` | Python     | `pytest` (or `python -m pytest`)                     |
   | `requirements.txt`   | Python       | `pytest`                                             |
   | `Makefile`           | Make         | `make test`                                          |
   | `package.json`       | Node.js      | Check scripts: prefer `vitest`, then `jest`, then `npm test` |
   | `mix.exs`            | Elixir       | `mix test`                                           |
   | `CMakeLists.txt`     | C/C++        | `cmake --build build && ctest --test-dir build`      |
   | `*.sln` / `*.csproj` | .NET         | `dotnet test`                                        |
   | `Package.swift`      | Swift        | `swift test`                                         |

   If multiple markers exist, use the one most relevant to the changed files.
   If no marker is found, check for a `Makefile` with a `test` target, or skip tests and warn.

   - If tests pass -> go to SHIP.
   - If tests fail -> go to ITERATION 2.

============================================================
ITERATION 2: REFINE (only if iteration 1 tests failed)
============================================================

1. Analyze the test failures from iteration 1.
2. Adjust the fix based on what the tests revealed.
3. Re-run the test suite.
4. If still failing -> STOP. Report what you found and what you tried.
   Include the ROLLBACK PLAN in your output.

============================================================
ROLLBACK PLAN
============================================================

If the fix does not work after 2 iterations, provide a rollback plan:
1. `git diff HEAD~1` — show exactly what changed.
2. `git revert HEAD` — command to revert the fix commit.
3. If a migration was created, provide the reverse migration or rollback command.
4. Note any side effects (caches to clear, services to restart, etc.).

============================================================
SHIP
============================================================

1. Stage ONLY the files you changed (no unrelated files).
2. Detect commit message conventions from the project:
   - Run `git log --oneline -10` to check for patterns (conventional commits,
     Jira ticket prefixes, deploy tags, etc.).
   - Follow whatever convention the project uses.
   - Default format if no convention detected:
     ```
     fix: {brief description of what was broken and fixed}
     ```
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
   - Extract story/ticket number from branch name if present and link it.

OUTPUT:
## Hotfix Shipped
- **Bug:** {what was broken}
- **Cause:** {root cause}
- **Fix:** {file:line — what changed}
- **Tests:** {pass/fail, count}
- **PR:** {URL}
- **Iterations:** {1 or 2}/2
- **Rollback:** `git revert {commit-sha}` if needed
