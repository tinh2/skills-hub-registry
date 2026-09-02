---
name: release
description: "Set up automated releases with semantic versioning, changelog generation, and package publishing. Triggers: you want automated versioning, need to publish packages, want changelogs from conventional commits."
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
- `--tool=TOOL` — force a specific release tool: `semantic-release`, `changesets`, `release-please`, `cargo-release`, `goreleaser`
- `--publish=TARGET` — where to publish: `npm`, `pypi`, `crates`, `ghcr`, `github` (GitHub Releases only)
- `--monorepo` — configure for monorepo with independent package versioning
- `--dry-run` — generate config files but do not create any CI workflows
- `--channel=CHANNEL` — set release channel: `latest` (default), `next`, `beta`, `alpha`

If no arguments, auto-detect the best tool and target.

============================================================
PHASE 1 — STACK DETECTION
============================================================

Detect the project stack and current release state:

**Language & Package Registry**:
- `package.json` → npm (check `publishConfig`, `private` field, `name` scope)
- `pyproject.toml` → PyPI (check `[project]` or `[tool.poetry]` section)
- `Cargo.toml` → crates.io (check `publish` field)
- `go.mod` → Go modules (tag-based releases)
- `pubspec.yaml` → pub.dev (check `publish_to`)

**Current Versioning**:
- Read current version from manifest file
- Check git tags: `git tag --list 'v*' --sort=-version:refname | head -5`
- Check if CHANGELOG.md exists and its format (Keep a Changelog, conventional, custom)
- Check existing release CI workflows in `.github/workflows/`

**Monorepo Detection**:
- `turbo.json` / `nx.json` / `pnpm-workspace.yaml` / `lerna.json`
- Multiple `package.json` files in subdirectories
- If monorepo detected, prefer changesets over semantic-release

**Existing Commit Convention**:
- Check if commitlint is configured (conventional commits already enforced)
- Sample recent commits: `git log --oneline -20` to see if they follow a pattern
- Check for `.husky/commit-msg` or equivalent hook

Record: language, registry, current version, monorepo status, commit convention.

============================================================
PHASE 2 — SELECT AND CONFIGURE RELEASE TOOL
============================================================

**If Node.js single-package → semantic-release**:

1. Install:
   ```
   npm install --save-dev semantic-release @semantic-release/changelog @semantic-release/git
   ```
2. Create `.releaserc.json`:
   ```json
   {
     "branches": ["main"],
     "plugins": [
       "@semantic-release/commit-analyzer",
       "@semantic-release/release-notes-generator",
       ["@semantic-release/changelog", { "changelogFile": "CHANGELOG.md" }],
       ["@semantic-release/npm", { "npmPublish": true }],
       ["@semantic-release/git", {
         "assets": ["CHANGELOG.md", "package.json"],
         "message": "chore(release): ${nextRelease.version}"
       }],
       "@semantic-release/github"
     ]
   }
   ```
   Adjust: set `"npmPublish": false` if `package.json` has `"private": true`.
   If `--channel` specified, add branch config for pre-release channels.

3. If commitlint is NOT already set up, install it:
   ```
   npm install --save-dev @commitlint/cli @commitlint/config-conventional
   ```
   Create `commitlint.config.js`:
   ```js
   export default { extends: ['@commitlint/config-conventional'] };
   ```

**If Node.js monorepo → changesets**:

1. Install:
   ```
   npm install --save-dev @changesets/cli @changesets/changelog-github
   ```
2. Initialize: `npx changeset init`
3. Configure `.changeset/config.json`:
   ```json
   {
     "$schema": "https://unpkg.com/@changesets/config@3.0.0/schema.json",
     "changelog": ["@changesets/changelog-github", { "repo": "{owner}/{repo}" }],
     "commit": false,
     "fixed": [],
     "linked": [],
     "access": "public",
     "baseBranch": "main",
     "updateInternalDependencies": "patch",
     "ignore": []
   }
   ```
   Detect repo name from `git remote get-url origin`.

**If Python → semantic-release (Python)**:

1. Install: `pip install python-semantic-release` (or add to dev dependencies)
2. Add to `pyproject.toml`:
   ```toml
   [tool.semantic_release]
   version_toml = ["pyproject.toml:project.version"]
   branch = "main"
   commit_message = "chore(release): {version}"
   build_command = "pip install build && python -m build"
   ```
   If publishing to PyPI, add:
   ```toml
   upload_to_pypi = true
   ```

**If Go → goreleaser**:

1. Install config: create `.goreleaser.yml`:
   ```yaml
   version: 2
   builds:
     - env: [CGO_ENABLED=0]
       goos: [linux, darwin, windows]
       goarch: [amd64, arm64]
   archives:
     - format: tar.gz
       name_template: "{{ .ProjectName }}_{{ .Version }}_{{ .Os }}_{{ .Arch }}"
       format_overrides:
         - goos: windows
           format: zip
   changelog:
     sort: asc
     filters:
       exclude: ["^docs:", "^test:", "^chore:"]
   ```

**If Rust → cargo-release**:

1. Install: `cargo install cargo-release`
2. Add to `Cargo.toml`:
   ```toml
   [workspace.metadata.release]
   sign-commit = false
   sign-tag = false
   push = true
   publish = true
   ```

**If release-please requested**:

1. Create `.release-please-manifest.json`:
   ```json
   { ".": "0.1.0" }
   ```
2. Create `release-please-config.json`:
   ```json
   {
     "packages": { ".": { "release-type": "{node|python|go|...}" } },
     "changelog-sections": [
       { "type": "feat", "section": "Features" },
       { "type": "fix", "section": "Bug Fixes" },
       { "type": "perf", "section": "Performance" },
       { "type": "docs", "section": "Documentation" }
     ]
   }
   ```

============================================================
PHASE 3 — GENERATE CI WORKFLOW
============================================================

Skip if `--dry-run` was passed.

Create `.github/workflows/release.yml`:

**For semantic-release**:
```yaml
name: Release
on:
  push:
    branches: [main]
permissions:
  contents: write
  issues: write
  pull-requests: write
  packages: write
jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
          persist-credentials: false
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: npm
      - run: npm ci
      - run: npx semantic-release
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          NPM_TOKEN: ${{ secrets.NPM_TOKEN }}
```

**For changesets**:
```yaml
name: Release
on:
  push:
    branches: [main]
permissions:
  contents: write
  pull-requests: write
jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: npm
      - run: npm ci
      - uses: changesets/action@v1
        with:
          publish: npm run release
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          NPM_TOKEN: ${{ secrets.NPM_TOKEN }}
```

**For release-please**:
```yaml
name: Release
on:
  push:
    branches: [main]
permissions:
  contents: write
  pull-requests: write
jobs:
  release-please:
    runs-on: ubuntu-latest
    steps:
      - uses: googleapis/release-please-action@v4
        with:
          release-type: node
```

**For goreleaser**:
```yaml
name: Release
on:
  push:
    tags: ['v*']
permissions:
  contents: write
jobs:
  goreleaser:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: actions/setup-go@v5
        with:
          go-version-file: go.mod
      - uses: goreleaser/goreleaser-action@v6
        with:
          args: release --clean
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

Adjust for Python/Rust equivalents as appropriate.

============================================================
PHASE 4 — VERIFY CONFIGURATION
============================================================

1. Validate the release config file is syntactically correct (parse JSON/YAML/TOML)
2. Verify conventional commits are being enforced (commitlint or equivalent is configured)
3. Dry-run the release tool if supported:
   - semantic-release: `npx semantic-release --dry-run`
   - changesets: `npx changeset status`
   - goreleaser: `goreleaser check`
4. Verify the CI workflow YAML is valid
5. Check that required secrets are documented


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
## Release Pipeline Setup Complete

### Tool: {semantic-release | changesets | release-please | goreleaser | cargo-release}
### Current Version: {version}
### Publish Target: {npm | pypi | crates.io | GitHub Releases}
### Release Channel: {latest | next | beta}

### How It Works
1. Write code using conventional commits (feat:, fix:, etc.)
2. Push/merge to main
3. {tool} analyzes commits since last release
4. Automatically: bumps version, generates changelog, creates git tag, publishes

### Commit → Release Mapping
- `feat:` → minor version bump (0.1.0 → 0.2.0)
- `fix:` → patch version bump (0.1.0 → 0.1.1)
- `feat!:` or `BREAKING CHANGE:` → major version bump (0.1.0 → 1.0.0)
- `docs:`, `chore:`, `ci:` → no release

### Files Created/Modified
- {list of files}

### Required Secrets
- GITHUB_TOKEN: automatic (provided by GitHub Actions)
- NPM_TOKEN: {required if publishing to npm — generate at npmjs.com}
- {other secrets as applicable}
```

============================================================
NEXT STEPS
============================================================

1. Add required secrets to GitHub repository settings (Settings → Secrets → Actions)
2. Run `/git-hooks` to enforce conventional commits locally if not already set up
3. Make a `feat:` commit and push to main to trigger the first release
4. For monorepos: run `npx changeset` before merging PRs to document changes


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /release — {{YYYY-MM-DD}}
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

- Do NOT configure publishing for private packages unless explicitly requested
- Do NOT use `GITHUB_TOKEN` for npm publishing — it requires a separate `NPM_TOKEN`
- Do NOT set up multiple release tools that conflict (e.g., semantic-release AND changesets)
- Do NOT skip conventional commit enforcement — releases depend on structured commit messages
- Do NOT use `fetch-depth: 1` in the release workflow — semantic-release needs full git history
- Do NOT overwrite existing CHANGELOG.md — the release tool will manage it going forward
- Do NOT use deprecated action versions (checkout@v2, setup-node@v3, etc.)
- Do NOT publish to registries during dry-run verification
