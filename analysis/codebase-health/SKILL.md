---
name: codebase-health
description: "Score your codebase 0-100 across complexity, coupling, cohesion, test coverage, documentation, churn hotspots, dependency health, and lint/type safety. Triggers: 'how healthy is this codebase', 'check code quality', 'score my project', 'find tech debt hotspots'."
version: "2.0.1"
category: analysis
platforms:
  - CLAUDE_CODE
---

You are an autonomous codebase health assessment agent. You measure the codebase across multiple quality dimensions, produce a composite health score (0-100), and identify the areas most in need of attention.

Do NOT ask the user questions. Investigate the entire codebase thoroughly.

## INPUT

$ARGUMENTS (optional). If provided, focus on specific dimensions or modules (e.g., "complexity only", "src/services", "trends"). If not provided, perform a full health assessment.

---

## PHASE 1: STACK DETECTION AND BASELINE

### 1.1 Identify Tech Stack
- Read package.json, pubspec.yaml, requirements.txt, go.mod, Cargo.toml, Gemfile, pom.xml.
- Identify language(s), framework(s), build tool(s), test framework(s), linter(s).
- Determine if TypeScript/Flow (typed) or JavaScript (untyped).

### 1.2 Gather Baseline Metrics
- Total source files (exclude node_modules, build, dist, vendor, generated).
- Total lines of code (source only).
- Total test files and test lines.
- Project age (first commit date).
- Number of contributors.
- Total commits.

### 1.3 Check for Previous Reports
- Look in MEMORY.md, docs/, or project root for prior scores.
- If found, use as baseline for trend comparison.

---

## PHASE 2: COMPLEXITY ANALYSIS (Weight: 15%)

### Cyclomatic Complexity
- Estimate cyclomatic complexity for every function/method.
- Count decision points: if, else if, case, while, for, &&, ||, catch, ternary.
- Compute: average complexity per function, median, 90th percentile.
- Flag functions with complexity > 15 (hard to test).
- Flag files with average function complexity > 10.

### Cognitive Complexity
- Beyond cyclomatic: account for nesting depth, breaks in linear flow.
- Deeply nested conditionals score higher than flat conditionals.

**Scoring:** 100 if avg < 5. 80 if avg < 8. 60 if avg < 12. 40 if avg < 15. 20 otherwise.

---

## PHASE 3: COUPLING ANALYSIS (Weight: 15%)

### Import Dependencies
- Build the import graph (which files import which).
- Compute fan-in (how many files import this file) and fan-out (how many files this file imports).
- Flag files with fan-in > 15 (central dependency -- high change impact).
- Flag files with fan-out > 15 (depends on everything -- fragile).

### Circular Dependencies
- Detect import cycles (A imports B imports C imports A).
- Count the number of cycles and their lengths.

### Layer Violations
- Detect architectural layers (UI, service, data, util).
- Flag imports that skip layers (UI directly importing data layer).

**Scoring:** 100 if no cycles and clean layers. 80 if < 3 cycles. 60 if < 10 cycles. 40 if 10+ cycles. 20 if pervasive coupling.

---

## PHASE 4: COHESION ANALYSIS (Weight: 10%)

### File Cohesion
- Does each file have a single clear purpose?
- Flag files with multiple unrelated classes/functions.
- Flag files > 500 lines (likely multiple responsibilities).

### Directory Cohesion
- Are related files in the same directory?
- Flag features scattered across unrelated directories.
- Check for "feature" vs "layer" organization consistency.

### Module Boundaries
- Are module boundaries clear (index files, barrel exports)?
- Do modules expose minimal public API?

**Scoring:** 100 if all files < 300 lines with clean boundaries. 80 if < 5% over 500 lines. 60 if < 10%. 40 if > 10%. 20 if god classes and no boundaries.

---

## PHASE 5: TEST COVERAGE (Weight: 20%)

### Test Ratio
- Test files / source files.
- Test lines / source lines.
- Tests per public function/endpoint.

### Test Quality
- Do tests have meaningful assertions (not just "runs without error")?
- Are there integration tests, not just unit tests?
- Are critical paths tested (auth, payment, data mutation)?
- Are edge cases tested (null, empty, boundary, error)?

### Missing Coverage
- Source files with no corresponding test file.
- Public functions with no test.
- Critical paths (identified by naming: auth, pay, order, user, admin) without tests.

**Scoring:** 100 if > 80% files tested with edge cases. 80 if > 60%. 60 if > 40%. 40 if > 20%. 20 if < 20% tested.

---

## PHASE 6: DOCUMENTATION COVERAGE (Weight: 10%)

### Inline Documentation
- Public functions with JSDoc/docstrings/comments explaining purpose.
- Complex functions (complexity > 10) with explanatory comments.
- API endpoints with documented request/response types.

### Project Documentation
- README.md exists and is current (not a boilerplate template).
- Setup/installation instructions.
- Architecture documentation.
- API documentation.
- Contributing guide (for open source).

**Scoring:** 100 if > 80% documented with complete project docs. 80 if > 60%. 60 if > 40%. 40 if < 40%. 20 if no documentation.

---

## PHASE 7: CODE CHURN HOTSPOTS (Weight: 10%)

### Churn Analysis
- Files with the most commits in the last 90 days.
- Files with the most lines changed in the last 90 days.
- Correlation: high churn + high complexity = rework magnet.

### Fix Ratio
- Percentage of commits that are fixes (message contains "fix", "bug", "patch", "revert").
- High fix ratio = code is unstable.

### Hotspot Map
- Top 20 files by churn * complexity score.

**Scoring:** 100 if fix ratio < 20% and no hotspots. 80 if < 30%. 60 if < 40%. 40 if < 50%. 20 if >= 50% fixes.

---

## PHASE 8: DEPENDENCY HEALTH (Weight: 10%)

Brief dependency check (defer to `/dependency-analysis` for full audit):
- Total dependency count (flag > 100 for Node, > 50 for others).
- Known vulnerabilities (any critical/high?).
- Outdated major versions (> 2 major versions behind).
- Deprecated packages (still depending on abandoned packages?).

**Scoring:** 100 if no vulns and all current. 80 if no critical vulns. 60 if some high vulns. 40 if critical vulns. 20 if multiple critical vulns.

---

## PHASE 9: LINT AND TYPE SAFETY (Weight: 10%)

### Lint Violations
- Run linter if configured (eslint, flake8, clippy, dart analyze, golint).
- Count errors vs warnings.
- Categorize: style, correctness, performance, security.

### Type Safety
- TypeScript: strict mode enabled? `any` count? `ts-ignore` count?
- Python: type hints coverage? mypy clean?
- Dart: strong mode? dynamic usage?
- Go/Rust: inherently typed -- check for unsafe/reflect usage.

**Scoring:** 100 if zero lint errors and strict types. 80 if < 10 warnings. 60 if < 50 warnings. 40 if > 50 warnings. 20 if no linting configured.

---


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

## OUTPUT FORMAT

```
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
```

---

## RULES

- Do NOT count generated/vendored code toward any metric.
- Do NOT penalize small projects for missing documentation that is not needed yet.
- Do NOT compare scores across different languages (complexity norms vary).
- Do NOT weight all dimensions equally -- test coverage and complexity matter most.
- Do NOT report a trend without a previous baseline to compare against.
- Do NOT modify any code -- this is an analysis-only skill.

---

## NEXT STEPS

- "Run `/tech-debt` to get a detailed inventory of all debt items."
- "Run `/dependency-analysis` for a deep dive on dependency health."
- "Run `/dead-code` to reduce codebase size before re-scoring."
- "Run `/perf` to add runtime performance data to the health picture."


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /codebase-health — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
