---
name: git-hooks
description: "Set up pre-commit hooks for linting, formatting, and type-checking with commit message enforcement using conventional commits. Triggers: you want to enforce code quality on every commit, add conventional commits, prevent bad code from being committed."
version: "2.0.1"
category: productivity
platforms:
  - CLAUDE_CODE
---

You are in AUTONOMOUS MODE. Do NOT ask questions. Do NOT pause for confirmation.
Execute every phase below in sequence, making decisions based on what you find.

============================================================
PHASE 0 — INPUT
============================================================

$ARGUMENTS may contain:
- `--tool=TOOL` — force a specific hook manager: `husky`, `lefthook`, `pre-commit`
- `--no-commit-msg` — skip commit message hook setup
- `--no-lint-staged` — run full lint instead of staged-only
- `--ci` — also generate CI workflow to mirror hook checks

If no arguments, auto-detect the best hook tool for the stack.

============================================================
PHASE 1 — STACK DETECTION
============================================================

Detect the project stack and existing tooling:

**Language & Tooling**:
- `package.json` → Node/TS — prefer husky + lint-staged
- `pyproject.toml` / `requirements.txt` → Python — prefer pre-commit framework
- `go.mod` → Go — prefer lefthook or pre-commit
- `Cargo.toml` → Rust — prefer lefthook
- `pubspec.yaml` → Flutter/Dart — prefer lefthook
- `Gemfile` → Ruby — prefer lefthook or overcommit
- Multiple languages → prefer lefthook (polyglot native)

**Existing Hooks** (check and preserve):
- `.husky/` directory — existing husky setup
- `.lefthook.yml` or `lefthook.yml` — existing lefthook setup
- `.pre-commit-config.yaml` — existing pre-commit setup
- `.git/hooks/` — raw git hooks (will be replaced)

**Lint & Format Tools** (detect what to run in hooks):
- ESLint: `.eslintrc.*` / `eslint.config.*` / `biome.json`
- Prettier: `.prettierrc*` / `biome.json`
- TypeScript: `tsconfig.json` → run `tsc --noEmit`
- Ruff: `ruff.toml` / `pyproject.toml [tool.ruff]`
- Black: `pyproject.toml [tool.black]`
- mypy: `mypy.ini` / `pyproject.toml [tool.mypy]`
- golangci-lint: `.golangci.yml` / `.golangci.yaml`
- gofmt/goimports: always available with Go
- Clippy: always available with Rust
- rustfmt: always available with Rust
- dart analyze / dart format: always available with Flutter

Record: hook tool, lint commands, format commands, type-check command, test command.

============================================================
PHASE 2 — SET UP HOOK MANAGER
============================================================

**If Node.js (husky + lint-staged)**:

1. Install dependencies:
   ```
   npm install --save-dev husky lint-staged
   ```
2. Initialize husky:
   ```
   npx husky init
   ```
3. Create `.husky/pre-commit`:
   ```sh
   npx lint-staged
   ```
4. Add `lint-staged` config to `package.json`:
   ```json
   {
     "lint-staged": {
       "*.{js,jsx,ts,tsx}": ["eslint --fix", "prettier --write"],
       "*.{json,md,yml,yaml}": ["prettier --write"]
     }
   }
   ```
   Adjust glob patterns and commands based on detected linters.
   If Biome is detected instead of ESLint+Prettier:
   ```json
   {
     "lint-staged": {
       "*.{js,jsx,ts,tsx,json}": ["biome check --write"]
     }
   }
   ```
5. If TypeScript detected, add type-check to pre-commit (runs on all files, not staged):
   ```sh
   npx lint-staged
   npx tsc --noEmit
   ```

**If Python (pre-commit framework)**:

1. Install: `pip install pre-commit` (or add to dev dependencies)
2. Create `.pre-commit-config.yaml`:
   ```yaml
   repos:
     - repo: https://github.com/astral-sh/ruff-pre-commit
       rev: v0.8.0
       hooks:
         - id: ruff
           args: [--fix]
         - id: ruff-format
     - repo: https://github.com/pre-commit/mirrors-mypy
       rev: v1.13.0
       hooks:
         - id: mypy
   ```
   Adjust repos based on detected tools (Black instead of Ruff, pyright instead of mypy).
3. Install hooks: `pre-commit install`

**If Go / Rust / Flutter / Polyglot (lefthook)**:

1. Install lefthook (detect best method):
   - npm: `npm install --save-dev lefthook`
   - brew: `brew install lefthook`
   - go: `go install github.com/evilmartians/lefthook@latest`
2. Create `lefthook.yml`:
   ```yaml
   pre-commit:
     parallel: true
     commands:
       lint:
         glob: "*.go"
         run: golangci-lint run --fix {staged_files}
       format:
         glob: "*.go"
         run: gofmt -w {staged_files}
   ```
   Adjust commands per detected language.
3. Install hooks: `lefthook install`

============================================================
PHASE 3 — COMMIT MESSAGE HOOK
============================================================

Skip if `--no-commit-msg` was passed.

Set up conventional commit enforcement:

**For husky (Node.js)**:
1. Install: `npm install --save-dev @commitlint/cli @commitlint/config-conventional`
2. Create `commitlint.config.js`:
   ```js
   export default { extends: ['@commitlint/config-conventional'] };
   ```
3. Create `.husky/commit-msg`:
   ```sh
   npx --no -- commitlint --edit $1
   ```

**For pre-commit (Python)**:
Add to `.pre-commit-config.yaml`:
```yaml
  - repo: https://github.com/compilerla/conventional-pre-commit
    rev: v3.6.0
    hooks:
      - id: conventional-pre-commit
        stages: [commit-msg]
```
Run: `pre-commit install --hook-type commit-msg`

**For lefthook**:
Add to `lefthook.yml`:
```yaml
commit-msg:
  commands:
    conventional:
      run: |
        MSG=$(head -1 {1})
        if ! echo "$MSG" | grep -qE '^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\(.+\))?!?: .+'; then
          echo "Commit message must follow Conventional Commits format"
          echo "Examples: feat: add login, fix(auth): token expiry"
          exit 1
        fi
```

============================================================
PHASE 4 — VERIFY HOOKS WORK
============================================================

1. Run the pre-commit hook manually to verify it works:
   - Husky: `npx lint-staged`
   - Pre-commit: `pre-commit run --all-files`
   - Lefthook: `lefthook run pre-commit`

2. If the hook fails on existing code:
   - Auto-fix what can be auto-fixed (formatting, simple lint rules)
   - Commit the fixes: `fix: auto-fix lint and format violations`
   - Re-run to verify hooks pass

3. Test the commit-msg hook with an invalid message to confirm it rejects it,
   then test with a valid conventional commit message.

============================================================
PHASE 5 — CI MIRROR (IF --ci)
============================================================

If `--ci` was passed, generate a GitHub Actions workflow that mirrors the hook checks:

Create `.github/workflows/lint.yml`:
```yaml
name: Lint
on:
  pull_request:
    branches: [main, master]
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - # setup language runtime
      - # run same lint/format/typecheck commands as hooks
```

This ensures hooks cannot be bypassed with `--no-verify`.


============================================================
SELF-HEALING VALIDATION (max 2 iterations)
============================================================

After completing, validate the output was produced correctly:

1. Verify generated files exist and are syntactically valid.
2. Run any available validation (lint, type-check, dry-run).
3. If the skill produces configuration, verify it parses without errors.

IF VALIDATION FAILS:
- Diagnose from error context and re-generate the failing artifact
- Repeat up to 2 iterations

============================================================
OUTPUT
============================================================

Print a summary:

```
## Git Hooks Setup Complete

### Hook Manager: {husky|lefthook|pre-commit}

### Pre-Commit Hooks
- Lint: {eslint --fix | ruff --fix | golangci-lint run}
- Format: {prettier --write | ruff-format | gofmt}
- Type Check: {tsc --noEmit | mypy | N/A}
- Scope: {staged files only | all files}

### Commit-Msg Hook
- Enforcing: Conventional Commits (feat|fix|docs|...)

### Files Created/Modified
- {list of files created or modified}

### Existing Violations Fixed
- {N auto-fixable issues fixed, or "none"}
```

============================================================
NEXT STEPS
============================================================

1. Make a test commit to verify hooks run correctly
2. Run `/linter` if lint configuration needs improvement
3. Run `/release` to set up automated releases that consume conventional commits
4. Consider adding `--no-verify` to your CI push commands if hooks run in CI separately


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /git-hooks — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.

============================================================
DO NOT
============================================================

- Do NOT install multiple hook managers — pick one and use it consistently
- Do NOT configure hooks that take longer than 10 seconds on staged files
- Do NOT run full test suites in pre-commit — only lint, format, and type-check
- Do NOT silently swallow hook errors — hooks must fail loudly with clear messages
- Do NOT overwrite existing hook configurations without reading them first
- Do NOT use deprecated commitlint configs (e.g., `.commitlintrc` without module type)
- Do NOT add hooks for tools that are not installed or configured in the project
