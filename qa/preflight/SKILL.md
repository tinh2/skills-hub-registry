---
name: preflight
description: "Read-only pre-deploy gate: git state, build, tests, migrations, lock files, secrets and commit conventions, ending in READY or NOT READY. Triggers: preflight, pre-deploy check, ready to deploy, deployment checklist."
version: "2.1.0"
category: qa
platforms:
  - CLAUDE_CODE
---

Verify the current branch is safe to deploy and report. This is read-only: change nothing, including "quick fixes". Run the checks without stopping to ask; note anything you could not run.

## Configuration

A deploy flag (e.g. `deploy:prod`, `ship-it`) is required in the last commit message only if the project configures one: `deployFlag` in CLAUDE.md, or `preflight.deployFlag` in package.json / pyproject.toml. Otherwise that check is N/A.

## Checks

1. **Git state**
   - Uncommitted changes: `git status --porcelain` must be empty.
   - Unpushed commits: `git log origin/<branch>..HEAD --oneline` must be empty (list them if not).
   - Behind remote: `git fetch origin` then compare; WARN if the remote has commits you lack.
   - Conflict markers: `git diff --check`.
   - Branch exists on the remote.
2. **Build / static check.** Detect the stack and use its standard check: `sbt compile`, `flutter analyze` (warnings = WARN), `npx tsc --noEmit` or `npm run build`, `mypy`/`ruff`, `go build ./...`, `cargo check`, `mvn compile -q` / `./gradlew compileJava`, Rails `bin/rails assets:precompile` (skip if it needs a DB). Prefer the project's own script if one exists.
3. **Tests.** Run the project's suite (`vitest run`, `jest`, `pytest`, `go test ./...`, `cargo test`, `flutter test`, `ENVIRONMENT=test sbt test`, `rspec`, `mvn test`...). List failures.
4. **Pending migrations** (WARN, not FAIL; N/A if none detected): Prisma `npx prisma migrate status`, Django `showmigrations --plan | grep '\[ \]'`, Flyway / Alembic / Rails / Knex / Sequelize migration files new on this branch.
5. **Lock files.** WARN if any of `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`, `pubspec.lock`, `Gemfile.lock`, `poetry.lock`, `uv.lock`, `Pipfile.lock`, `Cargo.lock`, `go.sum` have uncommitted changes.
6. **Secrets in tracked files** (FAIL with file:line): `AKIA[0-9A-Z]{16}`, `sk-[a-zA-Z0-9]{20,}`, `-----BEGIN ... PRIVATE KEY-----`, `ghp_`/`gho_`/`github_pat_`, `xoxb-`/`xoxp-`, and `(password|secret|token|api_key)\s*[:=]\s*['"][^'"]{8,}` unless the value is an env/variable reference. Tracked `.env` files (except `.env.example` / `.env.sample`).
7. **Conventions**
   - Deploy flag present in the last commit (if configured).
   - No `Co-Authored-By` lines on branch commits: `git log <base>..HEAD --format=%b | grep -i co-authored-by`.
   - No AI attribution in the PR body: `gh pr view --json body`.

## Output

```
## Preflight Check Results

| # | Check | Status | Details |
|---|-------|--------|---------|
| 1 | Uncommitted changes | PASS/FAIL | |
| 2 | Unpushed commits | PASS/FAIL | |
| 3 | Branch up to date | PASS/WARN | |
| 4 | Merge conflicts | PASS/FAIL | |
| 5 | Build | PASS/FAIL | <stack detected> |
| 6 | Tests | PASS/FAIL | X passed, Y failed |
| 7 | Pending migrations | PASS/WARN/N/A | |
| 8 | Lock files | PASS/WARN | |
| 9 | Secrets scan | PASS/FAIL | |
| 10 | Deploy flag | PASS/FAIL/N/A | |
| 11 | No Co-Authored-By | PASS/FAIL | |
| 12 | No AI attribution | PASS/FAIL | |
| 13 | Branch pushed | PASS/FAIL | |

**VERDICT: READY TO DEPLOY | NOT READY**
```

If NOT READY, list each fix needed as a concrete action (e.g. "commit and push", "run `/hotfix` for the failing tests").

## Telemetry

If a memory directory for this project exists under `~/.claude/projects/`, append to its `skill-telemetry.md`:

```
### /preflight — YYYY-MM-DD
- Outcome: SUCCESS | PARTIAL | FAILED
- Bottleneck: <check that struggled, or none>
- Suggestion: <one-line improvement for /evolve, or none>
```

Skip silently if the directory does not exist.
