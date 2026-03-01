---
name: linter
description: "Auto-detect stack and configure linting, formatting, and editor integration with auto-fix for existing violations"
version: "1.0.0"
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
- `--tool=TOOL` — force a specific linter: `eslint`, `biome`, `ruff`, `golangci-lint`, `rubocop`, `clippy`
- `--fix` — auto-fix all fixable violations after setup (default: setup only)
- `--strict` — enable stricter rule sets (recommended for new projects)
- `--no-format` — skip formatter setup, configure linter only
- `--migrate` — migrate from one tool to another (e.g., ESLint → Biome, flake8 → Ruff)

If no arguments, auto-detect the stack and set up the appropriate tools.

============================================================
PHASE 1 — STACK DETECTION
============================================================

Detect the language and existing lint/format tooling:

**JavaScript / TypeScript**:
- Existing: `.eslintrc.*`, `eslint.config.*` (flat config), `biome.json`, `biome.jsonc`
- Formatter: `.prettierrc*`, `.prettierignore`, `biome.json`
- Framework: React (`jsx`), Vue (`.vue`), Svelte (`.svelte`), Angular
- TypeScript: `tsconfig.json` present → enable type-aware lint rules

**Python**:
- Existing: `ruff.toml`, `pyproject.toml [tool.ruff]`, `.flake8`, `setup.cfg [flake8]`, `pylintrc`
- Formatter: `pyproject.toml [tool.black]`, `ruff.toml [format]`
- Type checker: `mypy.ini`, `pyproject.toml [tool.mypy]`, `pyrightconfig.json`

**Go**:
- Existing: `.golangci.yml`, `.golangci.yaml`
- Formatter: `gofmt` / `goimports` (built-in)

**Rust**:
- Existing: `clippy.toml`, `.clippy.toml`
- Formatter: `rustfmt.toml`, `.rustfmt.toml`

**Ruby**:
- Existing: `.rubocop.yml`
- Formatter: same tool (RuboCop handles both)

**Flutter / Dart**:
- Existing: `analysis_options.yaml`
- Formatter: `dart format` (built-in)

Record: language, existing tools, missing tools, framework-specific needs.

============================================================
PHASE 2 — CONFIGURE LINTER
============================================================

**2.1 — JavaScript / TypeScript**:

If no linter exists OR `--migrate` from legacy ESLint:

Prefer **ESLint 9 flat config** for new setups:
1. Install:
   ```
   npm install --save-dev eslint @eslint/js typescript-eslint globals
   ```
   Add framework plugins:
   - React: `eslint-plugin-react`, `eslint-plugin-react-hooks`
   - Next.js: `@next/eslint-plugin-next`
   - Vue: `eslint-plugin-vue`
2. Create `eslint.config.js`:
   ```js
   import js from '@eslint/js';
   import tseslint from 'typescript-eslint';
   import globals from 'globals';

   export default tseslint.config(
     js.configs.recommended,
     ...tseslint.configs.recommended,
     {
       languageOptions: {
         globals: { ...globals.node }
       },
       rules: {
         '@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
         '@typescript-eslint/no-explicit-any': 'warn',
       }
     },
     { ignores: ['dist/', 'node_modules/', 'coverage/'] }
   );
   ```
3. Add lint script to `package.json`: `"lint": "eslint ."`

If **Biome** is preferred or requested:
1. Install: `npm install --save-dev --exact @biomejs/biome`
2. Create `biome.json`:
   ```json
   {
     "$schema": "https://biomejs.dev/schemas/1.9.0/schema.json",
     "organizeImports": { "enabled": true },
     "linter": {
       "enabled": true,
       "rules": { "recommended": true }
     },
     "formatter": {
       "enabled": true,
       "indentStyle": "space",
       "indentWidth": 2
     }
   }
   ```
3. Add scripts: `"lint": "biome check ."`, `"lint:fix": "biome check --write ."`

If `--strict`: enable `tseslint.configs.strictTypeChecked` or Biome `"all"` rules with selected disables.

**2.2 — Python**:

Prefer **Ruff** (replaces flake8, isort, black, pyflakes, pycodestyle):
1. Add to `pyproject.toml`:
   ```toml
   [tool.ruff]
   target-version = "py312"
   line-length = 88

   [tool.ruff.lint]
   select = ["E", "F", "W", "I", "N", "UP", "B", "A", "SIM", "TCH"]
   ignore = []

   [tool.ruff.format]
   quote-style = "double"
   ```
   If `--strict`: add `"S"` (bandit security), `"D"` (docstrings), `"ANN"` (type annotations).

If migrating from flake8/pylint/isort:
- Read existing config, map rules to Ruff equivalents
- Remove old tool configs and dependencies

**2.3 — Go**:

Configure **golangci-lint**:
1. Create `.golangci.yml`:
   ```yaml
   linters:
     enable:
       - errcheck
       - gosimple
       - govet
       - ineffassign
       - staticcheck
       - unused
       - gocritic
       - gofumpt
       - misspell
       - revive
   linters-settings:
     gocritic:
       enabled-tags: [diagnostic, style, performance]
     gofumpt:
       extra-rules: true
   issues:
     max-issues-per-linter: 0
     max-same-issues: 0
   ```
   If `--strict`: add `exhaustive`, `nilnil`, `wrapcheck`, `errorlint`.

**2.4 — Rust**:

Clippy is built-in. Create `clippy.toml` for custom config if needed:
```toml
cognitive-complexity-threshold = 25
```
Add to CI: `cargo clippy -- -D warnings`

Create `rustfmt.toml`:
```toml
edition = "2021"
max_width = 100
use_field_init_shorthand = true
```

**2.5 — Ruby**:

Configure **RuboCop**:
1. Install: `gem install rubocop` (or add to Gemfile)
2. Create `.rubocop.yml` with project-appropriate rules

**2.6 — Flutter / Dart**:

Configure or update `analysis_options.yaml`:
```yaml
include: package:flutter_lints/flutter.yaml
linter:
  rules:
    prefer_const_constructors: true
    prefer_const_declarations: true
    avoid_print: true
    prefer_single_quotes: true
```

============================================================
PHASE 3 — CONFIGURE FORMATTER
============================================================

Skip if `--no-format`.

**JavaScript / TypeScript** (if not using Biome):
1. Install: `npm install --save-dev prettier`
2. Create `.prettierrc`:
   ```json
   {
     "semi": true,
     "singleQuote": true,
     "trailingComma": "all",
     "printWidth": 100,
     "tabWidth": 2
   }
   ```
3. Create `.prettierignore`:
   ```
   dist
   node_modules
   coverage
   pnpm-lock.yaml
   ```
4. Add script: `"format": "prettier --write .", "format:check": "prettier --check ."`

**Python** (if not using Ruff format):
- Black is included if Ruff is not used
- Ruff format handles formatting when Ruff is the linter

**Go**: `gofmt` / `goimports` — no config needed, built into Go toolchain.

**Rust**: `rustfmt` — configured via `rustfmt.toml` in Phase 2.

Create `.editorconfig` if it does not exist:
```ini
root = true

[*]
indent_style = space
indent_size = 2
end_of_line = lf
charset = utf-8
trim_trailing_whitespace = true
insert_final_newline = true

[*.{py,rs}]
indent_size = 4

[*.go]
indent_style = tab

[Makefile]
indent_style = tab
```

============================================================
PHASE 4 — EDITOR INTEGRATION
============================================================

Create or update `.vscode/settings.json` (merge with existing):

```json
{
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll": "explicit",
    "source.organizeImports": "explicit"
  }
}
```

Add language-specific settings:
- ESLint: `"editor.defaultFormatter": "dbaeumer.vscode-eslint"` for JS/TS files
- Biome: `"editor.defaultFormatter": "biomejs.biome"` for JS/TS files
- Prettier: `"editor.defaultFormatter": "esbenp.prettier-vscode"` for JS/TS/JSON/MD
- Ruff: `"[python]": { "editor.defaultFormatter": "charliermarsh.ruff" }`
- Go: `"[go]": { "editor.defaultFormatter": "golang.go" }`
- Rust: `"[rust]": { "editor.defaultFormatter": "rust-lang.rust-analyzer" }`

Create or update `.vscode/extensions.json` with recommended extensions:
```json
{
  "recommendations": [
    "dbaeumer.vscode-eslint",
    "esbenp.prettier-vscode",
    "EditorConfig.EditorConfig"
  ]
}
```

============================================================
PHASE 5 — FIX EXISTING VIOLATIONS
============================================================

If `--fix` was passed:

1. Run the auto-fixer:
   - ESLint: `npx eslint . --fix`
   - Biome: `npx biome check --write .`
   - Prettier: `npx prettier --write .`
   - Ruff: `ruff check --fix . && ruff format .`
   - golangci-lint: `golangci-lint run --fix`
   - Clippy: `cargo clippy --fix --allow-dirty`
   - dart: `dart fix --apply && dart format .`

2. Count remaining (non-auto-fixable) violations:
   - Run lint again without `--fix`
   - Report count by rule/category

3. Commit auto-fixes: `style: auto-fix lint and format violations`

If `--fix` was NOT passed, still report the violation count so the user knows the current state.

============================================================
OUTPUT
============================================================

Print a summary:

```
## Linter Setup Complete

### Stack: {language} / {framework}

### Tools Configured
- Linter: {ESLint 9 | Biome | Ruff | golangci-lint | Clippy | RuboCop}
- Formatter: {Prettier | Biome | Ruff | gofmt | rustfmt}
- Editor: VS Code format-on-save enabled

### Current State
- Auto-fixable violations: {N} (fixed with --fix)
- Remaining violations: {N} (require manual review)
- Clean files: {N}/{total}

### Files Created/Modified
- {list of files}
```

============================================================
NEXT STEPS
============================================================

1. Run `/git-hooks` to enforce lint on every commit
2. Run the linter to see remaining violations: `npm run lint` / `ruff check .`
3. Add lint step to CI: run `/github-actions` to generate CI workflow
4. Review and adjust rule severity in the config file as needed

============================================================
DO NOT
============================================================

- Do NOT install both ESLint and Biome — they serve the same purpose, pick one
- Do NOT install both Prettier and Biome — Biome includes formatting
- Do NOT install deprecated tools (TSLint, flake8 for new projects, prettier-eslint)
- Do NOT use ESLint legacy config format (`.eslintrc.json`) for new setups — use flat config (`eslint.config.js`)
- Do NOT enable every available rule — start with recommended and add incrementally
- Do NOT auto-fix violations that change semantics (e.g., `no-unused-vars` removing code)
- Do NOT modify files outside the project root
- Do NOT overwrite existing lint configs without reading them first and preserving custom rules
- Do NOT configure formatters with conflicting settings (e.g., Prettier tabs + EditorConfig spaces)
