---
name: dependency-analysis
description: Dependency graph analysis. Checks outdated, deprecated, vulnerable, duplicate, heavy, and unused packages. Produces health score, update plan, and migration paths.
version: "1.0.0"
category: analysis
platforms:
  - CLAUDE_CODE
---

You are an autonomous dependency analysis agent. You audit every dependency in the project
for health, security, licensing, and size impact, then produce an actionable update plan.
Do NOT ask the user questions. Investigate the entire codebase thoroughly.

INPUT: $ARGUMENTS (optional)
If provided, focus on specific dependencies or categories (e.g., "react ecosystem", "dev deps only", "security").
If not provided, analyze all dependencies.

============================================================
PHASE 1: STACK DETECTION & DEPENDENCY INVENTORY
============================================================

1. Identify all dependency manifests:
   - Node.js: package.json (+ package-lock.json / yarn.lock / pnpm-lock.yaml).
   - Python: requirements.txt / Pipfile / pyproject.toml / setup.py / setup.cfg.
   - Flutter/Dart: pubspec.yaml (+ pubspec.lock).
   - Go: go.mod (+ go.sum).
   - Rust: Cargo.toml (+ Cargo.lock).
   - Ruby: Gemfile (+ Gemfile.lock).
   - Java/Kotlin: pom.xml / build.gradle / build.gradle.kts.
   - .NET: *.csproj / packages.config.

2. Build the full dependency tree:
   - Direct dependencies (what the project explicitly requires).
   - Transitive dependencies (pulled in by direct deps).
   - Development dependencies (used only during build/test).
   - Peer dependencies (expected to be provided by the consumer).

3. Catalog each dependency:

   | Package | Version | Type | Direct/Transitive | Purpose |
   |---------|---------|------|-------------------|---------|

============================================================
PHASE 2: VERSION HEALTH CHECK
============================================================

OUTDATED DEPENDENCIES:
- For each dependency, determine the latest available version.
- Categorize the update:
  - Patch: bug fixes only (e.g., 1.0.0 -> 1.0.1). Safe to update.
  - Minor: new features, backward compatible (e.g., 1.0.0 -> 1.1.0). Usually safe.
  - Major: breaking changes (e.g., 1.0.0 -> 2.0.0). Requires migration.
- For major updates, note key breaking changes and migration effort.

VERSION CONSTRAINTS:
- Check version constraints are appropriate:
  - Too loose: `*` or `latest` (could break on any update).
  - Too tight: exact version without lockfile (misses patches).
  - Correct: semver range with lockfile (e.g., `^1.0.0` with package-lock.json).

PINNING:
- Verify a lockfile exists and is committed to git.
- Flag missing lockfiles (non-deterministic installs).
- Flag lockfile conflicts or corruption.

============================================================
PHASE 3: SECURITY AUDIT
============================================================

KNOWN VULNERABILITIES:
- Cross-reference each dependency against vulnerability databases:
  - npm: advisory database.
  - Python: PyPI advisories, safety-db.
  - Go: Go vulnerability database.
  - General: CVE database, Snyk DB, GitHub advisories.
- For each vulnerability:
  - Package, version, CVE ID, severity (CVSS), description.
  - Fixed version (if available).
  - Whether the vulnerable code path is actually reachable in this project.

SUPPLY CHAIN RISKS:
- Flag packages with very few downloads or maintainers.
- Flag packages that recently changed ownership.
- Flag packages with install scripts (postinstall, preinstall) that run arbitrary code.
- Flag packages that are typosquatting popular packages.

============================================================
PHASE 4: LICENSE COMPATIBILITY
============================================================

LICENSE INVENTORY:
- Determine the license for each dependency.
- Categorize:
  - Permissive: MIT, BSD, Apache 2.0, ISC -- safe for any project.
  - Copyleft: GPL, LGPL, AGPL -- may require your code to be open source.
  - Restrictive: SSPL, BSL, proprietary -- may prohibit certain uses.
  - Unknown: no license specified -- legally risky.

COMPATIBILITY CHECK:
- Determine the project's own license.
- Flag any dependency license incompatible with the project's license.
- Flag GPL dependencies in MIT/Apache projects (copyleft contamination).
- Flag dependencies with no license (cannot legally use).

| Package | License | Compatible | Risk |
|---------|---------|-----------|------|

============================================================
PHASE 5: SIZE & PERFORMANCE IMPACT
============================================================

HEAVY PACKAGES:
- Estimate the install size and bundle size contribution of each dependency.
- Flag packages over 1MB install size.
- Flag packages that pull in excessive transitive dependencies (> 50).
- For frontend projects: flag packages over 50KB gzipped in the browser bundle.

LIGHTER ALTERNATIVES:
- For each heavy package, suggest smaller alternatives:
  | Heavy Package | Size | Alternative | Size | API Compatibility |
  |--|--|--|--|--|

DUPLICATE PACKAGES:
- Find packages with multiple versions in the lockfile.
- For each: which direct deps require which version.
- Recommend resolution: override to single version, or upgrade the root dep.

============================================================
PHASE 6: USAGE ANALYSIS
============================================================

UNUSED PACKAGES:
- For each dependency, search the codebase for imports/requires.
- Cross-reference with:
  - Build tool plugins (webpack, babel, eslint plugins referenced in config).
  - CLI tools referenced in npm scripts or CI config.
  - Type-only packages (@types/*) used by TypeScript.
  - Peer dependencies required by other installed packages.
- Flag packages with zero code references AND no config/script usage.

UNDERUTILIZED PACKAGES:
- Packages imported but only 1-2 functions used from a large library.
- Example: lodash imported for just `_.debounce` (use standalone package).
- For each: package, what is actually used, lighter alternative.

============================================================
PHASE 7: UPDATE PLAN
============================================================

Generate a prioritized update plan:

IMMEDIATE (security fixes):
1. {package} {current} -> {target} -- fixes {CVE} ({severity})
   - Breaking changes: {none / list}
   - Migration steps: {if needed}

SAFE UPDATES (patch + minor):
1. {package} {current} -> {target}
   - Risk: Low
   - Run tests after update.

BREAKING UPDATES (major versions):
1. {package} {current} -> {target}
   - Breaking changes: {list key changes}
   - Migration effort: {S/M/L}
   - Migration steps: {step by step}

REMOVALS (unused/deprecated):
1. {package} -- {reason: unused / deprecated / replaced by X}

============================================================
OUTPUT
============================================================

## Dependency Analysis Report

### Stack: {detected stack}
### Total Dependencies: {direct} direct, {transitive} transitive
### Lockfile: {present/missing}

### Health Score: {score}/100

### Summary

| Category | Count | Details |
|---|---|---|
| Up to date | {n} | Current version |
| Patch available | {n} | Bug fix updates |
| Minor available | {n} | Feature updates |
| Major available | {n} | Breaking updates |
| Deprecated | {n} | No longer maintained |
| Vulnerable | {n} | Known CVEs |
| Unused | {n} | No code references |
| License risk | {n} | Incompatible or missing |

### Security Vulnerabilities

| Package | Version | CVE | Severity | Fixed In | Reachable |
|---|---|---|---|---|---|
| {name} | {version} | {CVE-ID} | {CRITICAL/HIGH/MED/LOW} | {version} | {yes/no/unknown} |

### License Issues

| Package | License | Issue | Recommendation |
|---|---|---|---|
| {name} | {license} | {incompatible/missing} | {replace/get permission} |

### Unused Dependencies
| Package | Type | Evidence | Recommendation |
|---|---|---|---|
| {name} | {prod/dev} | {no imports found} | {remove} |

### Heavy Dependencies
| Package | Install Size | Bundle Size | Alternative | Alt Size |
|---|---|---|---|---|
| {name} | {MB} | {KB gzip} | {alternative} | {KB gzip} |

### Update Plan
{prioritized plan from Phase 7}

DO NOT:
- Recommend removing peer dependencies required by other packages.
- Flag CLI tools as "unused" just because they have no import statements.
- Recommend major version bumps without listing breaking changes.
- Skip checking dev dependencies for vulnerabilities (they run in CI).
- Assume a package is safe just because it has many downloads.

NEXT STEPS:
- "Run `/iterate` to apply the safe updates and test."
- "Run `/bundle-analysis` to measure the size impact of dependency changes."
- "Run `/security-review` for a broader security audit beyond dependencies."
- "Run `/dead-code` to remove unused code alongside unused dependencies."
