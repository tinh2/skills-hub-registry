---
name: dependency-scan
description: Scan project dependencies for known vulnerabilities (CVEs), auto-fix safe patches, and generate SBOM. Auto-detects all package managers in monorepos — npm (npm audit), yarn (yarn audit), pnpm (pnpm audit), pip/poetry (pip-audit), Cargo (cargo audit), Go modules (govulncheck), Maven (dependency-check), Gradle, Bundler (bundle audit), and Composer. Categorizes findings by severity (Critical/High/Medium/Low), dependency type (direct vs transitive), and fix availability. Applies safe patch-level fixes automatically, adds npm overrides or yarn resolutions for transitive vulnerabilities, flags major version bumps for manual review, and generates CycloneDX SBOM with license compliance checks (GPL, AGPL, LGPL flagging). Verifies fixes by re-scanning and running tests before committing.
version: "2.0.0"
category: security
platforms:
  - CLAUDE_CODE
---

You are in AUTONOMOUS MODE. Do NOT ask questions. Detect, scan, fix, and report.

TARGET:
$ARGUMENTS

If arguments contain "sbom" or "SBOM", generate a Software Bill of Materials in
addition to the vulnerability scan. If no arguments provided, scan the entire
project in the current working directory.

IMPORTANT: Scan ALL detected package managers — monorepos often have multiple (e.g., npm frontend + Python backend). For each vulnerability, record: package name, current version, patched version, severity, CVE/advisory URL, and whether it is direct or transitive. Apply safe fixes (patch-level bumps) automatically, but never apply major version bumps without flagging them. After applying fixes, always re-run the scan to verify resolution and run the project test suite to check for regressions. Do not commit if tests fail.

============================================================
PHASE 0: PACKAGE MANAGER DETECTION
============================================================

Scan the project root and subdirectories to detect all package managers in use:

| File | Package Manager | Scan Command |
|------|----------------|--------------|
| `package-lock.json` | npm | `npm audit --json` |
| `yarn.lock` | yarn | `yarn audit --json` |
| `pnpm-lock.yaml` | pnpm | `pnpm audit --json` |
| `requirements.txt` / `pyproject.toml` / `Pipfile` | pip | `pip-audit --format=json` |
| `poetry.lock` | poetry | `poetry audit` or `pip-audit` |
| `Cargo.lock` | cargo | `cargo audit --json` |
| `go.sum` | go mod | `govulncheck -json ./...` |
| `pom.xml` | Maven | `mvn dependency-check:check` |
| `build.gradle` / `build.gradle.kts` | Gradle | `gradle dependencyCheckAnalyze` |
| `Gemfile.lock` | bundler | `bundle audit check --format=json` |
| `composer.lock` | composer | `composer audit --format=json` |

A project may have multiple package managers (e.g., monorepo with frontend npm
and backend Python). Detect and scan ALL of them.

============================================================
PHASE 1: VULNERABILITY SCAN
============================================================

For each detected package manager, run the appropriate audit command.

NPM:
```bash
npm audit --json 2>/dev/null
```
Parse the JSON output. Extract: package name, severity, CVE/advisory URL,
current version, patched version, whether it is a direct or transitive dependency.

YARN (Classic v1):
```bash
yarn audit --json 2>/dev/null
```
Note: Yarn audit outputs newline-delimited JSON, not a single JSON object.
Parse each line as a separate JSON advisory.

YARN (Berry v2+):
```bash
yarn npm audit --json 2>/dev/null
```

PNPM:
```bash
pnpm audit --json 2>/dev/null
```

PIP:
```bash
pip-audit --format=json 2>/dev/null || pip-audit --format=columns 2>/dev/null
```
If `pip-audit` is not installed, scan `requirements.txt` manually and check
versions against known CVE databases using web search.

CARGO:
```bash
cargo audit --json 2>/dev/null || cargo audit 2>/dev/null
```

GO:
```bash
govulncheck -json ./... 2>/dev/null || govulncheck ./... 2>/dev/null
```

BUNDLER:
```bash
bundle audit check --format=json 2>/dev/null || bundle audit check 2>/dev/null
```

If the scan tool is not installed, note it in the output and fall back to
manual analysis of the lock file against known CVEs.

============================================================
PHASE 2: CATEGORIZE FINDINGS
============================================================

For each vulnerability found, classify:

1. **Severity:** Critical / High / Medium / Low
2. **Dependency type:** Direct (in package.json/requirements.txt) or Transitive
3. **Fix available:** Yes (patch version exists) / No (no fix yet)
4. **Auto-fixable:** Can be fixed by version bump without breaking changes
5. **Breaking change risk:** Major version bump required / minor / patch

Sort findings: Critical first, then by fix availability (fixable first).

============================================================
PHASE 3: AUTO-FIX
============================================================

Apply fixes in order of safety. Always commit after each fix category.

SAFE FIXES (apply automatically):

For npm:
```bash
# Patch-level fixes for direct dependencies
npm audit fix

# If audit fix resolves issues, verify with:
npm audit --json
```

For yarn (classic):
```bash
# Upgrade direct dependencies to patched versions
yarn upgrade <package>@<safe-version>
```

For pip:
```bash
# Update requirements.txt with patched versions
pip install <package>==<safe-version>
pip freeze > requirements.txt  # or update pyproject.toml
```

For cargo:
```bash
cargo update <package>
```

For go:
```bash
go get <package>@<safe-version>
go mod tidy
```

OVERRIDE FIXES (transitive dependencies):

For npm — add `overrides` in `package.json`:
```json
{
  "overrides": {
    "<vulnerable-package>": "<safe-version>"
  }
}
```

For yarn — add `resolutions` in `package.json`:
```json
{
  "resolutions": {
    "<vulnerable-package>": "<safe-version>"
  }
}
```

For pip — pin transitive dependency in requirements:
```
<vulnerable-package>>=<safe-version>
```

After applying overrides:
- Reinstall dependencies
- Verify the vulnerable version is gone from the lock file
- Run the project's test suite to check for regressions

Commit fixes: "fix: resolve N vulnerable dependencies"

RISKY FIXES (major version bumps — flag but do not auto-apply):

If a fix requires a major version bump:
- Document the required change
- Note potential breaking changes from the changelog
- Flag for manual review

============================================================
PHASE 4: SBOM GENERATION (if requested)
============================================================

If the user requested SBOM generation, produce a Software Bill of Materials:

For npm:
```bash
npm sbom --sbom-format=cyclonedx 2>/dev/null || npm ls --json --all
```

For other managers, generate a dependency tree and format as:

```
## Software Bill of Materials

| Package | Version | License | Direct/Transitive | Source |
|---------|---------|---------|-------------------|--------|
| express | 4.18.2  | MIT     | Direct            | npm    |
| lodash  | 4.17.21 | MIT     | Transitive        | npm    |
```

Include license information where available. Flag any copyleft licenses
(GPL, AGPL, LGPL) that may have compliance implications.


============================================================
SELF-HEALING VALIDATION (max 2 iterations)
============================================================

After producing the security analysis, validate thoroughness:

1. Verify every category in the audit was actually checked (not skipped).
2. Verify every finding has a specific file:line location.
3. Verify severity ratings are justified by impact assessment.
4. Verify no false positives by re-reading flagged code in context.

IF VALIDATION FAILS:
- Re-audit skipped categories or vague findings
- Verify or remove false positives
- Repeat up to 2 iterations

============================================================
OUTPUT
============================================================

## Dependency Vulnerability Report

**Project:** [name]
**Package Managers:** [list detected]
**Scan Date:** [date]

### Summary

| Severity | Total | Fixed | Remaining | Auto-Fixable |
|----------|-------|-------|-----------|-------------|
| Critical | N     | N     | N         | N           |
| High     | N     | N     | N         | N           |
| Medium   | N     | N     | N         | N           |
| Low      | N     | N     | N         | N           |

### Fixed Vulnerabilities
[List of packages upgraded/overridden with old → new version]

### Remaining Vulnerabilities (no fix available)

| Package | Version | Severity | CVE | Description | Workaround |
|---------|---------|----------|-----|-------------|-----------|
| pkg-name | 1.2.3 | High | CVE-XXXX-XXXX | Description | Suggested workaround |

### Breaking Changes Required
[List of major version bumps needed with migration notes]

### SBOM
[If requested, include the full SBOM table]

============================================================
NEXT STEPS
============================================================

After fixing dependencies:
- "Run the test suite to verify no regressions from dependency updates."
- "Run `/secure` for a full security posture assessment."
- "Run `/owasp` to check A06 (Vulnerable Components) compliance."
- "Schedule recurring dependency scans (weekly recommended)."


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /dependency-scan — {{YYYY-MM-DD}}
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

- Do NOT apply major version bumps automatically — flag them for review.
- Do NOT remove dependencies to fix vulnerabilities — only upgrade or override.
- Do NOT skip scanning any detected package manager.
- Do NOT ignore transitive dependencies — they are the most common attack vector.
- Do NOT commit changes if the test suite fails after fixes.
- Do NOT install global scanning tools — use project-local tools or manual analysis.
- Do NOT expose CVE details that could aid exploitation — focus on fix guidance.
