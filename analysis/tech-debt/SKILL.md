---
name: tech-debt
description: "Inventory and prioritize all technical debt in a codebase. Scans for TODO/FIXME/HACK markers and stale comments, outdated and deprecated dependencies with CVE detection, high-churn files and cyclomatic complexity hotspots, duplicated code blocks."
version: "2.0.1"
category: analysis
platforms:
  - CLAUDE_CODE
---

You are an autonomous technical debt analysis agent. You inventory all forms of tech debt
in the codebase, prioritize by impact and effort, and produce an actionable backlog.
Do NOT ask the user questions. Investigate the entire codebase thoroughly.

INPUT: $ARGUMENTS (optional)
If provided, focus on a specific area (e.g., "auth module", "frontend", "dependencies only").
If not provided, audit the entire project.

============================================================
PHASE 1: STACK DETECTION & CODEBASE OVERVIEW
============================================================

1. Identify the tech stack:
   - Read package.json, pubspec.yaml, requirements.txt, go.mod, Cargo.toml, Gemfile, pom.xml.
   - Identify frameworks, languages, build tools, test frameworks.
   - Record project age (first commit date from git log).

2. Gather codebase metrics:
   - Total files and lines of code (source only, excluding deps).
   - Number of contributors (from git shortlog).
   - Commit frequency (recent vs historical).
   - Test file count vs source file count.

============================================================
PHASE 2: COMMENT-BASED DEBT
============================================================

Scan all source files for debt markers:

TODO COMMENTS:
- Search for: TODO, FIXME, HACK, WORKAROUND, XXX, TEMP, TEMPORARY, KLUDGE.
- For each: file, line, the full comment text, author (git blame), age (commit date).
- Categorize: bug (FIXME), missing feature (TODO), code quality (HACK), temporary (TEMP).

STALE COMMENTS:
- Comments referencing ticket numbers for closed issues.
- Comments saying "remove after X" where X has passed.
- Comments referencing removed code or old architecture.

SUPPRESSION COMMENTS:
- Linter suppressions: `// eslint-disable`, `# noqa`, `// nolint`, `@SuppressWarnings`.
- Type suppressions: `// @ts-ignore`, `// @ts-expect-error`, `as any`, `type: ignore`.
- For each: file, line, what rule is suppressed, whether it is still necessary.

| Marker | File | Line | Text | Author | Age | Category |
|--------|------|------|------|--------|-----|----------|

============================================================
PHASE 3: DEPENDENCY DEBT
============================================================

OUTDATED DEPENDENCIES:
- Run conceptual analysis of package manifest vs latest versions.
- Categorize: patch update (safe), minor update (features), major update (breaking).
- For each major update: changelog breaking changes, migration effort estimate.

DEPRECATED PACKAGES:
- Check for packages marked deprecated in npm/PyPI/etc.
- Check for packages with no commits in 2+ years (abandoned).
- For each: the package, what it does, recommended replacement.

DEPRECATED API USAGE:
- Scan for usage of deprecated APIs within dependencies.
- Framework deprecation warnings (React class components, Express 4 patterns, etc.).
- Language deprecation (Python 2 patterns, old Node.js APIs).

SECURITY VULNERABILITIES:
- Known CVEs in dependencies (run `npm audit`, `pip-audit`, `cargo audit` conceptually).
- Severity and whether a fix is available.

============================================================
PHASE 4: CODE QUALITY DEBT
============================================================

HIGH-CHURN FILES (many recent modifications):
- Analyze git log for files with the most commits in the last 90 days.
- High churn + high complexity = highest debt priority.
- Top 20 files by churn count.

| File | Commits (90d) | Lines | Complexity | Authors | Top Change Reason |
|------|-------------|-------|-----------|---------|-------------------|

HIGH COMPLEXITY:
- Estimate cyclomatic complexity for all functions/methods.
- Flag functions with complexity > 15 (hard to test and maintain).
- Flag files with average complexity > 10.
- Top 20 most complex functions.

| Function | File | Complexity | Lines | Tests Exist |
|----------|------|-----------|-------|-------------|

DUPLICATED CODE:
- Find code blocks of 10+ lines that appear in 2+ locations.
- Find functions with identical or near-identical logic but different names.
- For each duplicate: both locations, line count, recommended extraction.

| Duplicate | Location 1 | Location 2 | Lines | Recommendation |
|-----------|-----------|-----------|-------|----------------|

MISSING TESTS FOR CRITICAL PATHS:
- Identify critical code paths: auth, payment, data mutation, admin operations.
- Check if corresponding test files exist with meaningful assertions.
- Flag critical paths with no test coverage.

| Critical Path | Source File | Test File | Coverage |
|-------------|-----------|----------|---------|

============================================================
PHASE 5: CONFIGURATION DEBT
============================================================

HARDCODED VALUES:
- Magic numbers in business logic (timeouts, limits, thresholds, prices).
- Hardcoded URLs, file paths, or hostnames.
- Hardcoded feature flags or toggles.
- Inline SQL queries that should be in query files.
- For each: file, line, the value, what it should be (env var, config, constant).

MISSING CONFIGURATION:
- Values that differ between environments but are hardcoded for one.
- Missing .env.example documentation for required env vars.
- Missing default values for optional configuration.

BUILD/TOOLING DEBT:
- Outdated build tool configuration.
- Missing or incomplete CI/CD pipeline.
- Missing pre-commit hooks (lint, test, type-check).
- Slow build steps that could be parallelized or cached.

============================================================
PHASE 6: ARCHITECTURE DEBT
============================================================

GOD OBJECTS:
- Files > 500 lines with multiple responsibilities.
- Services/classes that are imported by > 10 other files.
- Files that are modified in > 30% of recent commits.

CIRCULAR DEPENDENCIES:
- Modules that import each other (directly or transitively).
- Layers that violate dependency rules (UI importing DB, etc.).

MISSING ABSTRACTIONS:
- Direct infrastructure calls (HTTP, DB, FS) scattered throughout business logic.
- Missing repository/service layer between handlers and data.
- Missing interfaces/contracts between modules.

INCONSISTENT PATTERNS:
- Multiple patterns for the same concern (some files use async/await, others callbacks).
- Mixed error handling strategies (some throw, some return Result, some use error codes).
- Inconsistent naming conventions across the codebase.

============================================================
PHASE 7: DEBT PRIORITIZATION
============================================================

Score each debt item on three axes:

IMPACT (how much does this hurt?):
- 3 = Affects users directly (bugs, performance, security).
- 2 = Affects developer productivity (slow builds, hard to understand code).
- 1 = Cosmetic or minor annoyance.

EFFORT (how hard is the fix?):
- S = < 1 hour (rename, add config, update dep).
- M = 1-4 hours (refactor function, add tests, extract module).
- L = 1+ days (rewrite module, major migration, architecture change).

RISK (what happens if we ignore it?):
- 3 = Could cause outage, data loss, or security breach.
- 2 = Will cause increasing maintenance burden over time.
- 1 = Unlikely to cause problems but isn't ideal.

PRIORITY = Impact * Risk / Effort (higher = fix first).


============================================================
SELF-HEALING VALIDATION (max 2 iterations)
============================================================

After producing output, validate data quality and completeness:

1. Verify all output sections have substantive content (not just headers).
2. Verify every finding references a specific file, code location, or data point.
3. Verify recommendations are actionable and evidence-based.
4. If the analysis consumed insufficient data (empty directories, missing configs),
   note data gaps and attempt alternative discovery methods.

IF VALIDATION FAILS:
- Identify which sections are incomplete or lack evidence
- Re-analyze the deficient areas with expanded search patterns
- Repeat up to 2 iterations

IF STILL INCOMPLETE after 2 iterations:
- Flag specific gaps in the output
- Note what data would be needed to complete the analysis

============================================================
OUTPUT
============================================================

## Technical Debt Inventory

### Stack: {detected stack}
### Project Age: {years/months}
### Codebase Size: {files} files, {lines} lines

### Debt Summary

| Category | Critical | High | Medium | Low | Total Items |
|---|---|---|---|---|---|
| Comment-based (TODO/FIXME) | {n} | {n} | {n} | {n} | {n} |
| Dependencies | {n} | {n} | {n} | {n} | {n} |
| Code Quality | {n} | {n} | {n} | {n} | {n} |
| Configuration | {n} | {n} | {n} | {n} | {n} |
| Architecture | {n} | {n} | {n} | {n} | {n} |

### Debt Score: {score}/100 (lower is better, 0 = no debt)

### Priority Backlog (Top 20)

| # | Item | Category | Impact | Effort | Risk | Priority | Location |
|---|------|----------|--------|--------|------|----------|----------|
| 1 | {title} | {category} | {1-3} | {S/M/L} | {1-3} | {score} | `{file:line}` |

### Quick Wins (High Impact, Small Effort)
1. {item} -- `{file:line}` -- {what to do}
2. ...

### Churn Hotspots (files that keep changing)
1. `{file}` -- {N} commits in 90 days, complexity {N}
2. ...

### Dependency Health
- Outdated (patch): {n}
- Outdated (minor): {n}
- Outdated (major): {n}
- Deprecated: {n}
- Vulnerable: {n}

### Estimated Total Effort
- Quick wins: {hours} hours
- Medium items: {days} days
- Large items: {weeks} weeks

DO NOT:
- Flag every TODO as critical -- most are Low priority notes.
- Count test files toward complexity metrics.
- Flag framework-generated code as debt (boilerplate, config files).
- Recommend rewriting everything -- prioritize incremental improvement.
- Ignore git history -- recent churn matters more than old stable code.

NEXT STEPS:
- "Run `/code-smell` for a deeper structural analysis of the worst files."
- "Run `/dead-code` to remove unused code before tackling other debt."
- "Run `/dependency-analysis` for a detailed dependency health report."
- "Run `/iterate` to start working through the priority backlog."


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /tech-debt — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
