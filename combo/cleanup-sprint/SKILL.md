---
name: "cleanup-sprint"
description: "Behavior-preserving codebase cleanup: dead code, orphaned files, resolved TODOs, security leftovers, lint/format, TS strictness, imports and unused deps, in atomic tested commits. Triggers: clean up, dead code, unused imports, lint, technical debt cleanup."
version: "3.1.0"
category: combo
platforms:
  - CLAUDE_CODE
---

Clean up the codebase without changing behavior. Work autonomously; the bar for every change is that tests and build stay as green as they were before you started.

## Baseline first

Detect the stack and use the lint/format tools the project already configures (prefer ones with a config file: `.eslintrc`, `ruff.toml`, `.rubocop.yml`, `.clang-format`, `analysis_options.yaml`...). Run tests and build once before touching anything; pre-existing failures are not regressions, but record them.

Independent categories (dead code, lint/style, outdated patterns) can run as parallel subagents if your harness supports it; afterward, run the full suite and revert whichever batch broke it.

## What to clean

1. **Dead code.** Unused exports (verify zero references with ripgrep, including dynamic imports, route configs, entry points, reflection/DI), unused non-public variables and parameters, unreachable code, commented-out code blocks (3+ lines of real code, not explanatory comments), empty files. Orphaned files: no importers and no edits in `git log --since="6 months ago"`.
2. **Safe deletions.** Config for tools no longer used (`.babelrc` under SWC, `.travis.yml` under Actions), committed generated files (`.DS_Store`, `__pycache__`, build output: also add them to `.gitignore`), duplicate type definitions (consolidate), fixtures and snapshots no test references. Leave applied migrations alone when the project uses a sequential migration runner.
3. **TODO / FIXME / HACK / XXX / WORKAROUND.** Remove ones the code or the referenced ticket already resolves; list the rest in the report.
4. **Security leftovers.** Logging of tokens, passwords, request bodies or user data; ungated debug/test endpoints; hardcoded credentials (move to env); `Access-Control-Allow-Origin: *` in prod config; disabled auth or unexplained security suppressions (`# nosec`, `eslint-disable` on security rules); test accounts in non-test code. Keep debug tooling that is properly gated.
5. **Lint and format.** Auto-fix first (`eslint --fix`, `ruff check --fix`, `cargo clippy --fix`, `rubocop -a`, `dart fix --apply`), fix the rest by hand, then format. Keep suppressions that carry an explanation; remove bare ones.
6. **TypeScript strictness** (TS only). Enable `noImplicitAny`, `strictNullChecks`, `noUnusedLocals/Parameters`, `strictPropertyInitialization` one at a time and fix the errors properly: `as any` and `@ts-ignore` don't count as fixes. If full `strict` would need 50+ changes, stop at the flags you finished and report the rest.
7. **Imports.** Remove unused, merge duplicates, order stdlib / external / internal (or the project's existing convention), replace star imports that pull fewer than 10 names. Use `goimports`, ruff/isort, etc. where available.
8. **Dependencies.** Remove manifest entries nothing references (scripts, tests and config count as references) and duplicates. Don't bump versions; that's a different task.

## Commits

One category per commit, each passing tests on its own:
`chore(dead-code)`, `chore(safe-delete)`, `chore(todo)`, `chore(security)`, `chore(lint)`, `chore(types)`, `chore(imports)`, `chore(deps)`. If a change breaks a test that passed at baseline, revert that change and note it.

Done means: no new test failures versus baseline, build passes, lint warnings at zero or below baseline. Iterate fix-and-verify up to three times; anything still failing goes in the report as needing manual work.

## Output

```
Cleanup Sprint Report
=====================
Stack: <language> | Lint: <tool> | Format: <tool>

Dead code:      files <N>, exports <N>, commented blocks <N>, unreachable <N>
Safe deletions: orphaned files <N>, stale configs <N>, dead fixtures <N>
TODOs:          resolved removed <N>, remaining <N>
Security:       debug logging <N>, credentials <N>, other <N>
Lint/format:    fixed <N>, remaining <N> (reasons)
TS strict:      enabled <flags>, errors fixed <N>, deferred <flags> (reasons)
Imports:        files <N>, unused removed <N>
Dependencies:   removed <N>

Verification: tests <pass/fail> | build <pass/fail> | lint <pass/fail>
Net lines removed: <N> | Commits: <N>

Unresolved TODOs:
- <file>:<line> <text>
```

## Telemetry

If a memory directory for this project exists under `~/.claude/projects/`, append to its `skill-telemetry.md`:

```
### /cleanup-sprint — YYYY-MM-DD
- Outcome: SUCCESS | PARTIAL | FAILED
- Bottleneck: <phase that struggled, or none>
- Suggestion: <one-line improvement for /evolve, or none>
```
