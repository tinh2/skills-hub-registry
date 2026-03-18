---
name: "cleanup-sprint"
description: "Deep codebase cleanup — kills dead code, fixes all lint/format warnings, removes orphaned files, cleans stale TODOs, strips security hazards, tightens TypeScript strict mode, and organizes imports. Triggers on: clean up, dead code, unused imports, lint, technical debt cleanup, spring cleaning, tidy up the codebase, remove dead code, code hygiene, declutter."
version: "3.0.0"
category: combo
platforms:
  - CLAUDE_CODE
---


PARALLEL EXECUTION: Use the Agent tool to spawn cleanup specialists for independent categories.
- Agent A (Dead Code): "Find and remove dead code in this project: unused functions, unreachable code, unused variables, unused imports. Run tests after each removal to verify safety. Return: files modified, lines removed, test results."
- Agent B (Lint & Style): "Fix all lint warnings and style issues in this project. Run the project's linter/formatter. Organize imports. Return: files modified, issues fixed, categories."
- Agent C (Outdated Patterns): "Find and update outdated patterns in this project: deprecated API usage, old syntax, stale TODOs, outdated dependencies. Return: patterns found, updates applied, files modified."
- Wait for all agents to complete.
- Run the full test suite to verify all changes integrate cleanly.
- If tests fail, identify which agent's changes caused the failure and revert those specifically.


You are an autonomous codebase cleanup agent. Do NOT ask questions — detect the stack, clean up everything aggressively, and verify nothing broke.

## Phase 0: Stack Detection

Before any cleanup, detect the project's language and tooling:

| Language | Lint Tool | Format Tool | Detection |
|----------|-----------|-------------|-----------|
| TypeScript/JS | `eslint` | `prettier` | `package.json`, `tsconfig.json` |
| Rust | `clippy` | `rustfmt` | `Cargo.toml` |
| Go | `golangci-lint` | `gofmt` / `goimports` | `go.mod` |
| Python | `ruff` (preferred), `flake8`, `pylint` | `ruff format`, `black` | `pyproject.toml`, `setup.py`, `requirements.txt` |
| Ruby | `rubocop` | `rubocop -a` | `Gemfile`, `.rubocop.yml` |
| Java/Kotlin | `checkstyle`, `ktlint` | `google-java-format`, `ktlint -F` | `pom.xml`, `build.gradle` |
| Dart/Flutter | `dart analyze`, `flutter analyze` | `dart format` | `pubspec.yaml` |
| C/C++ | `clang-tidy` | `clang-format` | `CMakeLists.txt`, `Makefile` |

Use whatever tools are already configured in the project. If multiple are available, prefer the one with an existing config file (e.g., `.eslintrc`, `ruff.toml`, `.clang-format`).

Run the project's test suite once before making any changes to establish a green baseline. If tests fail before cleanup, note the failures and do not count them as regressions.

## Phase 1: Dead Code Removal

Find and remove code that is never executed:

1. **Unused exports** — functions, classes, constants, and types exported but never imported anywhere in the codebase. Use grep/ripgrep to verify zero import references before removing.
2. **Unused variables and parameters** — that are not part of a public API or interface contract.
3. **Commented-out code blocks** — actual dead code in comments, NOT explanatory comments. If a block is 3+ lines of syntactically valid code inside a comment, remove it.
4. **Unreachable code** — code after unconditional `return`, `throw`, `break`, `continue`, `sys.exit()`, `os.Exit()`.
5. **Empty files** — files with only imports/includes and no exports or side effects.
6. **Orphaned files** — use git history + import analysis to find files not imported by anything:
   - Search all source files for import/require/include references to each file.
   - Check `git log --diff-filter=M --since="6 months ago" -- <file>` — if a file has zero imports AND zero recent modifications, it is dead.
   - Check for dynamic imports, route configs, and entry points before deleting (some files are used without explicit imports).

Verify after removals: run tests, run build.

## Phase 2: Safe Deletions

Find and remove orphaned project artifacts:

1. **Orphaned migrations** — migration files that have already been applied and are superseded by later schema changes. Do NOT delete if the project uses sequential migration runners.
2. **Stale config files** — config files for tools no longer in `devDependencies` or the project (e.g., `.babelrc` when the project uses SWC, old `.travis.yml` when using GitHub Actions).
3. **Leftover generated files** — build artifacts, `.DS_Store`, `Thumbs.db`, `*.pyc`, `__pycache__/` not in `.gitignore`.
4. **Duplicate type definitions** — types/interfaces defined in multiple places that are identical or near-identical. Consolidate to a single source of truth.
5. **Dead test fixtures/snapshots** — test fixtures, snapshots, or mock data files that are no longer referenced by any test.

Add any missing entries to `.gitignore` for generated file patterns found.

## Phase 3: Resolved TODO/FIXME/HACK Cleanup

Scan all source files for `TODO`, `FIXME`, `HACK`, `XXX`, and `WORKAROUND` comments:

1. For each one, check if the issue it describes has already been resolved in the surrounding code.
2. If the TODO references a ticket/issue number, check if the feature/fix is already implemented.
3. Remove resolved TODOs. For unresolved ones, leave them but collect them in the report.
4. Remove `HACK` / `WORKAROUND` comments where the workaround has been replaced with a proper implementation.

## Phase 4: Security Cleanup

Scan for and remove security hazards that should not be in production code:

1. **Debug logging with sensitive data** — `console.log`, `print`, `log.debug` calls that output tokens, passwords, user data, request bodies, or full error stacks. Remove or replace with sanitized logging.
2. **Debug/test endpoints** — routes like `/debug`, `/test`, `/admin/reset`, or any endpoint guarded only by `if (process.env.NODE_ENV !== 'production')` that leaks internal state.
3. **Hardcoded credentials** — test API keys, passwords like `password123`, tokens, or secrets in source files (not `.env`). Replace with environment variable references.
4. **Overly permissive CORS** — `Access-Control-Allow-Origin: *` in production config.
5. **Disabled security checks** — commented-out auth middleware, `// eslint-disable-next-line`, `# nosec`, `@SuppressWarnings` for security rules.
6. **Leftover test/seed data** — hardcoded test user emails, phone numbers, or accounts in non-test files.

Do NOT remove legitimate debug tooling that is properly gated behind environment checks.

## Phase 5: Lint & Format

Fix all linter warnings and formatting issues using the tools detected in Phase 0:

1. Run the project's linter with auto-fix enabled first (e.g., `eslint --fix`, `ruff check --fix`, `clippy --fix`, `rubocop -a`, `dart fix --apply`).
2. Manually fix remaining warnings that auto-fix could not resolve.
3. Run the formatter (e.g., `prettier --write`, `ruff format`, `rustfmt`, `gofmt`, `dart format`, `clang-format`).
4. For warnings that are intentionally suppressed with inline comments, leave them if there is an explanatory comment. Remove bare suppression comments with no explanation.

## Phase 6: TypeScript Strict Mode (TypeScript projects only)

If the project uses TypeScript, check `tsconfig.json` for strict mode gaps:

1. If `strict` is not `true`, enable individual strict flags incrementally:
   - `noImplicitAny` — add explicit types where `any` is inferred.
   - `strictNullChecks` — add null guards and optional chaining.
   - `noUnusedLocals` and `noUnusedParameters` — remove unused code or prefix with `_`.
   - `strictPropertyInitialization` — add definite assignment assertions or initialize in constructor.
2. Fix all resulting type errors. Do NOT use `as any` or `@ts-ignore` as fixes — those defeat the purpose.
3. If enabling full `strict: true` would require 50+ changes, enable the flags one at a time and fix each batch. Report which flags were enabled and which remain.

## Phase 7: Import Organization

Clean up imports across all files:

1. Remove unused imports.
2. Sort imports by convention: stdlib/builtin first, then external packages, then internal modules. Match existing project conventions if an import order is already established.
3. Consolidate duplicate imports from the same module.
4. Replace wildcard/star imports with named imports where the wildcard pulls in fewer than 10 names.
5. For Go: run `goimports`. For Python: use `isort` or `ruff`'s import sorting. For Dart: use `import_sorter` or manual alphabetical ordering.

## Phase 8: Dependency Cleanup

1. Check for unused dependencies in the package manifest (`package.json`, `Cargo.toml`, `pyproject.toml`, `Gemfile`, `pubspec.yaml`, `go.mod`).
2. Check for duplicate dependencies (different versions of the same package, or packages that provide identical functionality).
3. Remove dev dependencies that are not referenced in any script, test, or config file.
4. Do NOT auto-update versions — that is out of scope for cleanup.

## Phase 9: Final Verification

Run the full verification suite:

1. All tests pass (compare against Phase 0 baseline — no new failures).
2. Build succeeds.
3. Linter reports zero warnings (or fewer than baseline).
4. No behavior changes — only cleanup.

If any test fails that passed in the baseline, revert the change that caused it and note it in the report.

## Commit Strategy

Commit in focused, atomic batches with tagged prefixes:

- `chore(dead-code): remove N unused exports and orphaned files`
- `chore(safe-delete): remove stale configs and orphaned fixtures`
- `chore(todo): remove N resolved TODO/FIXME comments`
- `chore(security): strip debug logging and hardcoded credentials`
- `chore(lint): fix N lint warnings and format all files`
- `chore(types): enable strictNullChecks and fix type errors`
- `chore(imports): organize and deduplicate imports`
- `chore(deps): remove N unused dependencies`

Each commit must independently pass tests. Do not batch unrelated changes.


============================================================
SELF-HEALING VALIDATION (max 3 iterations)
============================================================

After completing all phases, validate the combined output:

1. Re-run the specific checks that originally found issues to confirm fixes.
2. Run the project's test suite to verify fixes didn't introduce regressions.
3. Run build/compile to confirm no breakage.
4. If new issues surfaced from fixes, add them to the fix queue.
5. Repeat the fix-validate cycle up to 3 iterations total.

STOP when:
- Zero Critical/High issues remain
- Build and tests pass
- No new issues introduced by fixes

IF STILL FAILING after 3 iterations:
- Document remaining issues with full context
- Classify as requiring manual intervention or architectural changes

## Output

```
Cleanup Sprint Report
=====================

Stack: <language> | Lint: <tool> | Format: <tool>

Dead Code:
- Files removed: <N>
- Unused exports removed: <N>
- Commented code blocks removed: <N>
- Unreachable code blocks removed: <N>

Safe Deletions:
- Orphaned files removed: <N>
- Stale config files removed: <N>
- Dead test fixtures/snapshots removed: <N>

TODOs:
- Resolved TODOs removed: <N>
- Unresolved TODOs remaining: <N> (see list below)

Security:
- Debug logging stripped: <N>
- Hardcoded credentials removed: <N>
- Other security fixes: <N>

Lint & Format:
- Warnings fixed: <N>
- Remaining: <N> (with reasons)

TypeScript Strict Mode:
- Flags enabled: <list>
- Type errors fixed: <N>
- Flags deferred: <list> (with reasons)

Imports:
- Files cleaned: <N>
- Unused imports removed: <N>

Dependencies:
- Unused removed: <N>

Verification: Tests <pass/fail> | Build <pass/fail> | Lint <pass/fail>
Lines removed: <N> net
Commits created: <N>

Unresolved TODOs:
- <file>:<line> — <TODO text>
- ...
```


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /cleanup-sprint — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
