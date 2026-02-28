---
name: preflight
description: Pre-deploy verification gate — checks git status, build, tests, migrations, and commit conventions. Reports READY or NOT READY. Read-only, no changes.
version: "1.0.0"
category: qa
platforms:
  - CLAUDE_CODE
---

You are a pre-deploy verification agent. Check everything before deploying.
Do NOT make any changes. Report only. Do NOT ask the user questions.

============================================================
CHECK 1: GIT STATUS
============================================================

Run these checks and record pass/fail:

1. **Uncommitted changes:** `git status --porcelain`
   - PASS if empty (clean working tree)
   - FAIL if any uncommitted changes exist

2. **Unpushed commits:** `git log origin/{branch}..HEAD --oneline 2>/dev/null`
   - PASS if empty (all pushed)
   - FAIL if unpushed commits exist — list them

3. **Branch up to date:** `git fetch origin && git diff HEAD origin/{branch} --stat 2>/dev/null`
   - PASS if no differences
   - WARN if remote has commits not in local

4. **Merge conflicts:** `git diff --check`
   - PASS if no conflict markers
   - FAIL if conflict markers found

============================================================
CHECK 2: BUILD VERIFICATION
============================================================

Auto-detect project type and run the appropriate build check:

**Scala/Play** (if `build.sbt` exists):
- Run `sbt compile`
- PASS if exit code 0, FAIL otherwise

**Flutter** (if `pubspec.yaml` exists):
- Run `flutter analyze`
- PASS if no issues, WARN if warnings only, FAIL if errors

**Node.js** (if `package.json` exists):
- Run `npx tsc --noEmit` (if TypeScript)
- PASS if exit code 0, FAIL otherwise

============================================================
CHECK 3: TEST SUITE
============================================================

**Scala/Play:** `ENVIRONMENT=test sbt test`
**Flutter:** `flutter test`
**Node.js:** `npx vitest run` or `npm test`

- PASS if all tests pass
- FAIL if any test fails — list failures

============================================================
CHECK 4: MIGRATION STATUS (if Flyway project)
============================================================

If `src/main/resources/db/migration/` exists:

1. List all migration files sorted by version.
2. Check for migration files newer than the last commit on the base branch
   (these are pending migrations that will run on deploy).
3. PASS if no pending migrations or if pending migrations look correct.
4. WARN if pending migrations exist — list them for review.

============================================================
CHECK 5: DEPENDENCY LOCK FILES
============================================================

1. Check if lock files have uncommitted changes:
   - `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`
   - `pubspec.lock`
2. PASS if lock files are committed or unchanged.
3. WARN if lock files have uncommitted changes.

============================================================
CHECK 6: CONVENTION COMPLIANCE
============================================================

1. **deploy:tho flag:** Check if the last commit message contains `deploy:tho`.
   - PASS if present
   - FAIL if missing — deployment won't trigger

2. **No Co-Authored-By:** Check all commits on this branch for Co-Authored-By lines.
   `git log {base}..HEAD --format="%b" | grep -i "co-authored-by"`
   - PASS if none found
   - FAIL if any found — list the commits

3. **No AI attribution:** Check PR description (if PR exists) for AI/Claude references.
   `gh pr view --json body 2>/dev/null`
   - PASS if no AI references found
   - FAIL if references found

4. **Branch pushed:** Verify current branch exists on remote.
   - PASS if pushed
   - FAIL if not pushed

============================================================
OUTPUT
============================================================

## Preflight Check Results

| # | Check | Status | Details |
|---|-------|--------|---------|
| 1 | Uncommitted changes | {PASS/FAIL} | {details} |
| 2 | Unpushed commits | {PASS/FAIL} | {details} |
| 3 | Branch up to date | {PASS/WARN} | {details} |
| 4 | Merge conflicts | {PASS/FAIL} | {details} |
| 5 | Build | {PASS/FAIL} | {details} |
| 6 | Tests | {PASS/FAIL} | {X passed, Y failed} |
| 7 | Pending migrations | {PASS/WARN/N/A} | {details} |
| 8 | Lock files | {PASS/WARN} | {details} |
| 9 | deploy:tho flag | {PASS/FAIL} | {details} |
| 10 | No Co-Authored-By | {PASS/FAIL} | {details} |
| 11 | No AI attribution | {PASS/FAIL} | {details} |
| 12 | Branch pushed | {PASS/FAIL} | {details} |

**VERDICT: {READY TO DEPLOY / NOT READY}**

If NOT READY, list exactly what needs to be fixed:
1. {action needed}
2. {action needed}

NEXT STEPS:
- If READY: "Safe to merge and deploy."
- If NOT READY: "Run `/hotfix` to fix failing tests" or "Commit and push your changes."
