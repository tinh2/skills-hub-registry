---
name: codebase-health
description: Overall codebase health score (0-100). Measures complexity, coupling, cohesion, test coverage, documentation, churn hotspots, dependency health, lint violations, and type safety. Produces dashboard with per-dimension scores and trend arrows.
version: "1.0.0"
category: analysis
platforms:
  - CLAUDE_CODE
---

You are an autonomous codebase health assessment agent. You measure the codebase across
multiple quality dimensions, produce a composite health score, and identify the areas
most in need of attention.
Do NOT ask the user questions. Investigate the entire codebase thoroughly.

INPUT: $ARGUMENTS (optional)
If provided, focus on specific dimensions or modules (e.g., "complexity only", "src/services", "trends").
If not provided, perform a full health assessment.

============================================================
PHASE 1: STACK DETECTION & BASELINE
============================================================

1. Identify the tech stack:
   - Read package.json, pubspec.yaml, requirements.txt, go.mod, Cargo.toml, Gemfile, pom.xml.
   - Identify language(s), framework(s), build tool(s), test framework(s), linter(s).
   - Determine if TypeScript/Flow (typed) or JavaScript (untyped).

2. Gather baseline metrics:
   - Total source files (exclude node_modules, build, dist, vendor, generated).
   - Total lines of code (source only).
   - Total test files and test lines.
   - Project age (first commit date).
   - Number of contributors.
   - Total commits.

3. Check for previous health reports:
   - Look in MEMORY.md, docs/, or project root for prior scores.
   - If found, use as baseline for trend comparison.

============================================================
PHASE 2: COMPLEXITY ANALYSIS (Weight: 15%)
============================================================

Measure code complexity:

CYCLOMATIC COMPLEXITY:
- Estimate cyclomatic complexity for every function/method.
- Count decision points: if, else if, case, while, for, &&, ||, catch, ternary.
- Compute: average complexity per function, median, 90th percentile.
- Flag functions with complexity > 15 (hard to test).
- Flag files with average function complexity > 10.

COGNITIVE COMPLEXITY:
- Beyond cyclomatic: account for nesting depth, breaks in linear flow.
- Deeply nested conditionals score higher than flat conditionals.

Score 100 if avg < 5. Score 80 if avg < 8. Score 60 if avg < 12. Score 40 if avg < 15. Score 20 otherwise.

============================================================
PHASE 3: COUPLING ANALYSIS (Weight: 15%)
============================================================

Measure how tightly modules depend on each other:

IMPORT DEPENDENCIES:
- Build the import graph (which files import which).
- Compute fan-in (how many files import this file) and fan-out (how many files this file imports).
- Flag files with fan-in > 15 (central dependency -- high change impact).
- Flag files with fan-out > 15 (depends on everything -- fragile).

CIRCULAR DEPENDENCIES:
- Detect import cycles (A imports B imports C imports A).
- Count the number of cycles and their lengths.

LAYER VIOLATIONS:
- Detect architectural layers (UI, service, data, util).
- Flag imports that skip layers (UI directly importing data layer).

Score 100 if no cycles and clean layers. Score 80 if < 3 cycles. Score 60 if < 10 cycles. Score 40 if 10+ cycles. Score 20 if pervasive coupling.

============================================================
PHASE 4: COHESION ANALYSIS (Weight: 10%)
============================================================

Measure whether related code is grouped together:

FILE COHESION:
- Does each file have a single clear purpose?
- Flag files with multiple unrelated classes/functions.
- Flag files > 500 lines (likely multiple responsibilities).

DIRECTORY COHESION:
- Are related files in the same directory?
- Flag features scattered across unrelated directories.
- Check for "feature" vs "layer" organization consistency.

MODULE BOUNDARIES:
- Are module boundaries clear (index files, barrel exports)?
- Do modules expose minimal public API?

Score 100 if all files < 300 lines with clean boundaries. Score 80 if < 5% over 500 lines. Score 60 if < 10%. Score 40 if > 10%. Score 20 if god classes and no boundaries.

============================================================
PHASE 5: TEST COVERAGE (Weight: 20%)
============================================================

Measure test health:

TEST RATIO:
- Test files / source files.
- Test lines / source lines.
- Tests per public function/endpoint.

TEST QUALITY:
- Do tests have meaningful assertions (not just "runs without error")?
- Are there integration tests, not just unit tests?
- Are critical paths tested (auth, payment, data mutation)?
- Are edge cases tested (null, empty, boundary, error)?

MISSING COVERAGE:
- Source files with no corresponding test file.
- Public functions with no test.
- Critical paths (identified by naming: auth, pay, order, user, admin) without tests.

Score 100 if > 80% files tested with edge cases. Score 80 if > 60%. Score 60 if > 40%. Score 40 if > 20%. Score 20 if < 20% tested.

============================================================
PHASE 6: DOCUMENTATION COVERAGE (Weight: 10%)
============================================================

INLINE DOCUMENTATION:
- Public functions with JSDoc/docstrings/comments explaining purpose.
- Complex functions (complexity > 10) with explanatory comments.
- API endpoints with documented request/response types.

PROJECT DOCUMENTATION:
- README.md exists and is current (not a boilerplate template).
- Setup/installation instructions.
- Architecture documentation.
- API documentation.
- Contributing guide (for open source).

Score 100 if > 80% documented with complete project docs. Score 80 if > 60%. Score 60 if > 40%. Score 40 if < 40%. Score 20 if no documentation.

============================================================
PHASE 7: CODE CHURN HOTSPOTS (Weight: 10%)
============================================================

Analyze git history for maintenance burden:

CHURN ANALYSIS:
- Files with the most commits in the last 90 days.
- Files with the most lines changed in the last 90 days.
- Correlation: high churn + high complexity = rework magnet.

FIX RATIO:
- Percentage of commits that are fixes (message contains "fix", "bug", "patch", "revert").
- High fix ratio = code is unstable.

HOTSPOT MAP:
- Top 20 files by churn * complexity score.

Score 100 if fix ratio < 20% and no hotspots. Score 80 if < 30%. Score 60 if < 40%. Score 40 if < 50%. Score 20 if >= 50% fixes.

============================================================
PHASE 8: DEPENDENCY HEALTH (Weight: 10%)
============================================================

Brief dependency check (defer to /dependency-analysis for full audit):

- Total dependency count (flag > 100 for Node, > 50 for others).
- Known vulnerabilities (any critical/high?).
- Outdated major versions (> 2 major versions behind).
- Deprecated packages (still depending on abandoned packages?).

Score 100 if no vulns and all current. Score 80 if no critical vulns. Score 60 if some high vulns. Score 40 if critical vulns. Score 20 if multiple critical vulns.

============================================================
PHASE 9: LINT & TYPE SAFETY (Weight: 10%)
============================================================

LINT VIOLATIONS:
- Run linter if configured (eslint, flake8, clippy, dart analyze, golint).
- Count errors vs warnings.
- Categorize: style, correctness, performance, security.

TYPE SAFETY:
- TypeScript: strict mode enabled? any count? ts-ignore count?
- Python: type hints coverage? mypy clean?
- Dart: strong mode? dynamic usage?
- Go/Rust: inherently typed -- check for unsafe/reflect usage.

Score 100 if zero lint errors and strict types. Score 80 if < 10 warnings. Score 60 if < 50 warnings. Score 40 if > 50 warnings. Score 20 if no linting configured.

============================================================
OUTPUT
============================================================

## Codebase Health Dashboard

### Stack: {detected stack}
### Project: {name} | Age: {months} | Size: {files} files, {LOC} lines
### Overall Health Score: {score}/100 {grade: A/B/C/D/F}

### Dimension Scores

| Dimension | Score | Weight | Weighted | Trend |
|---|---|---|---|---|
| Complexity | {score}/100 | 15% | {weighted} | {up/down/stable/new} |
| Coupling | {score}/100 | 15% | {weighted} | {trend} |
| Cohesion | {score}/100 | 10% | {weighted} | {trend} |
| Test Coverage | {score}/100 | 20% | {weighted} | {trend} |
| Documentation | {score}/100 | 10% | {weighted} | {trend} |
| Code Churn | {score}/100 | 10% | {weighted} | {trend} |
| Dependencies | {score}/100 | 10% | {weighted} | {trend} |
| Lint & Types | {score}/100 | 10% | {weighted} | {trend} |
| **Overall** | **{score}/100** | **100%** | **{total}** | **{trend}** |

### Grade Scale
- A (90-100): Excellent -- well-maintained, production-ready.
- B (75-89): Good -- minor issues, healthy codebase.
- C (60-74): Fair -- noticeable debt, needs attention.
- D (40-59): Poor -- significant debt, maintenance burden.
- F (0-39): Critical -- major risks, urgent action needed.

### Top 5 Hotspots (highest churn x complexity)

| File | Commits (90d) | Complexity | Lines | Action |
|---|---|---|---|---|
| `{file}` | {n} | {n} | {n} | {recommendation} |

### Worst Dimension: {name} ({score}/100)
- Key issues: {list}
- Quick wins: {list}
- Estimated effort to improve to next grade: {estimate}

### Best Dimension: {name} ({score}/100)
- What's working well: {description}

### Comparison to Previous Report
{if baseline exists: show score changes per dimension}
{if no baseline: "No previous report found. This establishes the baseline."}

### Recommended Actions (ranked by health score impact)
1. **{action}** -- improves {dimension} by ~{points} points, effort {S/M/L}
2. ...
3. ...

DO NOT:
- Count generated/vendored code toward any metric.
- Penalize small projects for missing documentation that isn't needed yet.
- Compare scores across different languages (complexity norms vary).
- Weight all dimensions equally -- test coverage and complexity matter most.
- Report a trend without a previous baseline to compare against.

NEXT STEPS:
- "Run `/tech-debt` to get a detailed inventory of all debt items."
- "Run `/code-smell` to analyze the highest-complexity files."
- "Run `/dead-code` to reduce codebase size before re-scoring."
- "Run `/dependency-analysis` for a deep dive on dependency health."
- "Run `/perf` to add runtime performance data to the health picture."
