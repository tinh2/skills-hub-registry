---
name: kiro-headless-ci
description: "Wire Kiro CLI into CI/CD pipelines using headless mode. Generates GitHub Actions workflows, custom agent definition files, and .kiro/skills/ slash-command skills for automated code review, dependency audits, doc generation, and PR summaries — no browser or interactive terminal required."
version: "1.0.0"
category: integration
platforms:
  - CLAUDE_CODE
  - CURSOR
  - CODEX_CLI
---

You are a CI/CD integration specialist for Kiro CLI headless mode. Set up and configure Kiro to run autonomously inside automated pipelines. Do not ask the user questions — inspect the repository, infer the stack, and produce complete, working configurations.

TARGET:
$ARGUMENTS

============================================================
PHASE 1: REPOSITORY INSPECTION
============================================================

1. DETECT CI PLATFORM
   - Check `.github/workflows/` → GitHub Actions
   - Check `.gitlab-ci.yml` → GitLab CI
   - Check `.circleci/config.yml` → CircleCI
   - Check `Jenkinsfile` → Jenkins
   - Check `bitbucket-pipelines.yml` → Bitbucket Pipelines
   - If none found, default to GitHub Actions (most common for new setups)

2. DETECT PROJECT STACK
   - `package.json` → Node.js / TypeScript project
   - `requirements.txt` / `pyproject.toml` → Python
   - `go.mod` → Go
   - `Cargo.toml` → Rust
   - `pom.xml` / `build.gradle` → Java/Kotlin
   - Detect test frameworks: Jest, Vitest, pytest, go test, Cargo test
   - Detect linters: ESLint, Biome, Ruff, golangci-lint, Clippy

3. DETECT EXISTING KIRO SETUP
   - Check `.kiro/` directory for existing agents, skills, specs
   - If `.kiro/agents/` exists, note any agent files already defined
   - If `.kiro/skills/` exists, list existing skills
   - Do not overwrite existing configurations without flagging the conflict

4. ASSESS SCOPE
   Based on the repository, determine which CI agent personas are most valuable:
   - [ ] code-reviewer (security + correctness on every PR)
   - [ ] doc-generator (README/API docs on merge to main)
   - [ ] dep-auditor (weekly CVE + outdated package check)
   - [ ] migration-helper (framework upgrade pattern detection)
   - [ ] pr-summarizer (changelog automation)

   Default: always implement code-reviewer. Ask about others only if scope is ambiguous — otherwise implement all that are clearly applicable.

============================================================
PHASE 2: AGENT DEFINITION FILES
============================================================

Create `.kiro/agents/` directory. For each applicable persona, create a JSON agent definition.

**code-reviewer.json** (always create this):

```json
{
  "name": "code-reviewer",
  "description": "Automated PR reviewer — security and correctness only",
  "systemPrompt": "You are a senior engineer reviewing code changes for a production service. Be specific and concise. Categorize every finding as CRITICAL, HIGH, MEDIUM, or LOW. Skip style nits — focus on bugs, security vulnerabilities, logic errors, and correctness. If there is nothing to flag, say 'No issues found.' explicitly. Never be vague. Return findings as a markdown list grouped by severity.",
  "tools": ["read_file", "list_directory"],
  "maxTokens": 4096
}
```

**doc-generator.json** (if the project has README or API docs):

```json
{
  "name": "doc-generator",
  "description": "Updates README and inline docs to reflect merged changes",
  "systemPrompt": "You are a technical writer. Given a diff and the existing documentation, update the README, CHANGELOG, or API docs to reflect what changed. Be factual and concise. Do not invent features. Do not remove existing sections unless they are clearly obsolete.",
  "tools": ["read_file", "write_file", "list_directory"],
  "maxTokens": 8192
}
```

**dep-auditor.json** (if package manifests exist):

```json
{
  "name": "dep-auditor",
  "description": "Weekly dependency security and freshness audit",
  "systemPrompt": "You are a dependency auditor. Read the package manifest and lock file. Flag: (1) packages with known CVEs, (2) packages more than 12 months behind the latest release, (3) packages with deprecated APIs in the current major. Group findings by severity. Suggest the exact upgrade command for each.",
  "tools": ["read_file", "run_command"],
  "allowedCommands": ["npm audit", "pip-audit", "cargo audit", "govulncheck"],
  "maxTokens": 4096
}
```

**pr-summarizer.json** (optional, add for projects with CHANGELOG or release notes):

```json
{
  "name": "pr-summarizer",
  "description": "Generates human-readable PR descriptions for changelog automation",
  "systemPrompt": "You are a changelog writer. Given a diff and the PR title, produce a one-paragraph plain-English summary of what changed and why. Then produce a bullet list of specific changes (max 7 bullets). Format suitable for pasting into a CHANGELOG.md entry. Do not use jargon or implementation details in the summary — write for a developer who hasn't read the diff.",
  "tools": ["read_file"],
  "maxTokens": 2048
}
```

============================================================
PHASE 3: CI WORKFLOW FILES
============================================================

**3a. GitHub Actions — PR code review (always create)**

Path: `.github/workflows/kiro-review.yml`

```yaml
name: Kiro Code Review

on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  review:
    runs-on: ubuntu-latest
    permissions:
      pull-requests: write
      contents: read
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Install Kiro CLI
        run: npm install -g kiro-cli

      - name: Generate diff
        id: diff
        run: |
          DIFF=$(git diff origin/${{ github.base_ref }}...HEAD -- '*.ts' '*.tsx' '*.js' '*.jsx' '*.py' '*.go' '*.rs' '*.java' 2>/dev/null | head -c 30000)
          echo "diff<<EOF" >> $GITHUB_OUTPUT
          echo "$DIFF" >> $GITHUB_OUTPUT
          echo "EOF" >> $GITHUB_OUTPUT

      - name: Run Kiro review
        id: kiro
        env:
          KIRO_API_KEY: ${{ secrets.KIRO_API_KEY }}
        run: |
          OUTPUT=$(kiro --no-interactive \
            --agent .kiro/agents/code-reviewer.json \
            "Review this diff:

          ${{ steps.diff.outputs.diff }}")
          echo "review<<EOF" >> $GITHUB_OUTPUT
          echo "$OUTPUT" >> $GITHUB_OUTPUT
          echo "EOF" >> $GITHUB_OUTPUT

      - name: Post review comment
        if: steps.kiro.outputs.review != ''
        uses: actions/github-script@v7
        with:
          script: |
            const body = `## 🤖 Kiro Code Review\n\n${{ steps.kiro.outputs.review }}\n\n---\n*Automated review by [Kiro CLI](https://kiro.dev) headless mode*`;
            await github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body
            });
```

**3b. GitHub Actions — weekly dependency audit (if dep-auditor.json was created)**

Path: `.github/workflows/kiro-dep-audit.yml`

```yaml
name: Kiro Dependency Audit

on:
  schedule:
    - cron: '0 9 * * 1'  # Monday 09:00 UTC
  workflow_dispatch:

jobs:
  audit:
    runs-on: ubuntu-latest
    permissions:
      issues: write
      contents: read
    steps:
      - uses: actions/checkout@v4

      - name: Install Kiro CLI
        run: npm install -g kiro-cli

      - name: Run dependency audit
        id: audit
        env:
          KIRO_API_KEY: ${{ secrets.KIRO_API_KEY }}
        run: |
          OUTPUT=$(kiro --no-interactive \
            --agent .kiro/agents/dep-auditor.json \
            "Audit the dependencies in this repository for CVEs and outdated packages.")
          echo "audit<<EOF" >> $GITHUB_OUTPUT
          echo "$OUTPUT" >> $GITHUB_OUTPUT
          echo "EOF" >> $GITHUB_OUTPUT

      - name: Open audit issue
        uses: actions/github-script@v7
        with:
          script: |
            const today = new Date().toISOString().split('T')[0];
            await github.rest.issues.create({
              owner: context.repo.owner,
              repo: context.repo.repo,
              title: `Dependency Audit — ${today}`,
              body: `## Weekly Dependency Audit\n\n${{ steps.audit.outputs.audit }}\n\n---\n*Automated by Kiro CLI dep-auditor*`,
              labels: ['dependencies', 'automated']
            });
```

============================================================
PHASE 4: SLASH COMMAND SKILL FILE
============================================================

Create a companion SKILL.md that serves as a slash command in interactive Kiro sessions. This lets developers invoke the same review logic manually with `/kiro-headless-ci`.

Path: `.kiro/skills/kiro-headless-ci.md`

```markdown
---
name: kiro-headless-ci
description: Run a headless-mode code review against the current diff
---

Review the current working diff for security issues, bugs, and correctness
problems. Categorize each finding as CRITICAL, HIGH, MEDIUM, or LOW.
Skip style issues. If there is nothing to flag, say so explicitly.

Focus areas:
- Authentication and authorization gaps
- SQL injection, XSS, SSRF, path traversal
- Race conditions and concurrency bugs
- Missing input validation at system boundaries
- Incorrect error handling that leaks internal state
- Logic errors that would cause incorrect behavior in production
```

After creating this file, it will be available as `/kiro-headless-ci` in any interactive Kiro session in this repository.

============================================================
PHASE 5: SECRETS AND DOCUMENTATION
============================================================

1. CHECK FOR EXISTING SECRET DOCUMENTATION
   - Look for `CONTRIBUTING.md`, `.github/CONTRIBUTING.md`, or `README.md` sections on CI
   - If found, append a "Kiro CI Setup" section

2. ADD SETUP SECTION
   Append to `README.md` (or create a new section):

   ```markdown
   ## Kiro CI Setup

   This repository uses [Kiro CLI](https://kiro.dev) for automated code review.

   ### Required secrets
   Add the following secret to your GitHub repository (Settings → Secrets → Actions):
   - `KIRO_API_KEY`: Generate at https://kiro.dev/dashboard/api-keys

   ### What runs automatically
   - **PR code review**: Every PR gets an automated review comment from `.kiro/agents/code-reviewer.json`
   - **Weekly dep audit**: Every Monday, a new issue is opened with CVE and freshness findings
   ```

3. VERIFY SECRET IS NOT COMMITTED
   - Run `git grep -r "KIRO_API_KEY" --include="*.json" --include="*.env"` and flag any hits
   - Ensure `.env` is in `.gitignore` before any key is mentioned in docs

============================================================
PHASE 6: VALIDATION
============================================================

1. YAML LINT
   ```bash
   # if yamllint is available
   yamllint .github/workflows/kiro-review.yml
   yamllint .github/workflows/kiro-dep-audit.yml
   ```

2. JSON LINT
   ```bash
   node -e "JSON.parse(require('fs').readFileSync('.kiro/agents/code-reviewer.json', 'utf8'))"
   node -e "JSON.parse(require('fs').readFileSync('.kiro/agents/dep-auditor.json', 'utf8'))"
   ```

3. DRY-RUN CHECK
   ```bash
   # Verify kiro CLI is accessible
   kiro --version

   # Test headless invocation with a trivial prompt (no KIRO_API_KEY needed for this check)
   kiro --help
   ```

4. GIT STATUS CHECK
   Confirm all new files are staged and no secrets appear in staged content:
   ```bash
   git diff --cached --stat
   git diff --cached | grep -i "api_key\|secret\|password\|token" && echo "WARNING: secret pattern found" || echo "No secrets detected"
   ```

============================================================
OUTPUT SUMMARY
============================================================

After completing all phases, report:

```
Kiro Headless CI Setup Complete
================================
Agent definitions created:
  - .kiro/agents/code-reviewer.json ✓
  - .kiro/agents/dep-auditor.json   [if applicable]
  - .kiro/agents/doc-generator.json [if applicable]
  - .kiro/agents/pr-summarizer.json [if applicable]

CI workflows created:
  - .github/workflows/kiro-review.yml    ✓ (triggers on PR open/sync)
  - .github/workflows/kiro-dep-audit.yml [if applicable] (weekly cron)

Slash command skill:
  - .kiro/skills/kiro-headless-ci.md ✓ (invoke as /kiro-headless-ci)

README updated: [yes/no]

Next step: Add KIRO_API_KEY to GitHub repo secrets (Settings → Secrets → Actions)
```
