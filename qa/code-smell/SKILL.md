---
name: code-smell
description: "Scan a codebase for Fowler's code smells (god classes, long methods, feature envy, data clumps, primitive obsession, shotgun surgery, message chains) and rank refactorings by impact. Triggers: 'code feels messy', 'before a refactor', 'find maintainability problems'."
version: "2.1.0"
category: qa
platforms:
  - CLAUDE_CODE
---

Find the code smells that actually hurt maintainability in this codebase, report each with location and severity, and recommend a specific refactoring. This is a report; don't change code.

## Input

`$ARGUMENTS` (optional): files or directories to focus on. Default: the whole project, excluding tests, generated code, vendored code and config.

## Approach

Identify the languages and frameworks, then inventory source files by size and import count. The largest and most-imported files are where smells concentrate. Git history is strong evidence: files with high churn (`git log --format= --name-only | sort | uniq -c | sort -rn | head -30`) that also have many smells are the priority, and files that always change together point to shotgun surgery.

Count logic lines only (no blanks, comments or imports). Don't flag idiomatic framework shapes (a Flutter `build` method, a React component's JSX, a Django settings file) unless they are smelly by that framework's own standards.

## Smells and thresholds

| Category          | Smell                             | Flag when                                                                            | Severity                                            | Refactoring                            |
| ----------------- | --------------------------------- | ------------------------------------------------------------------------------------ | --------------------------------------------------- | -------------------------------------- |
| Bloaters          | Long method                       | > 50 lines                                                                           | Med 50-100, High 100-200, Crit > 200                | Extract Function                       |
|                   | God class/module                  | > 500 lines or many unrelated responsibilities                                       | Med 500-800, High 800-1200, Crit > 1200             | Extract Class/Module                   |
|                   | Long parameter list               | > 4 params                                                                           | Low 5, Med 6-7, High > 7                            | Parameter Object                       |
|                   | Data clumps                       | same 3+ fields together in several places                                            | Med 3-4 places, High 5+                             | Extract Class                          |
|                   | Primitive obsession               | strings for emails/URLs/IDs/money, boolean flag params, string type codes            | Low internal, Med in API/models, High in validation | Value Object, Enum                     |
| OO abusers        | Repeated switch                   | same type discriminator switched in 2+ places                                        | Med 2, High 3+                                      | Polymorphism / Strategy / lookup table |
|                   | Parallel hierarchies              | adding a subclass forces one elsewhere                                               | Med                                                 | Move Method, collapse one              |
|                   | Temporary field                   | field set only in some code paths                                                    | Low                                                 | Extract Class                          |
| Change preventers | Divergent change                  | one module changes for unrelated reasons (3+ external concerns, mixed commit topics) | Med 2, High 3+                                      | Split by responsibility                |
|                   | Shotgun surgery                   | one concept scattered across 5+ files/layers                                         | Med 5-8, High > 8                                   | Consolidate                            |
| Dispensables      | Lazy class / pass-through wrapper | < 3 methods, little logic                                                            | Low                                                 | Inline                                 |
|                   | Speculative generality            | one-implementation interfaces, unused "future" params                                | Low-Med                                             | Collapse, Remove Parameter             |
|                   | Dead code (light check)           | unreachable code, commented-out blocks > 5 lines                                     | Low                                                 | delete; deeper pass via `/dead-code`   |
| Couplers          | Feature envy                      | uses another module's data 2x+ more than its own                                     | Med 2x, High 3x+                                    | Move Function                          |
|                   | Message chains                    | `a.b().c().d()` 3+ links                                                             | Low 3, Med 4, High 5+                               | Hide Delegate                          |
|                   | Middle man                        | > 50% of methods only delegate                                                       | Med                                                 | Remove Middle Man                      |
|                   | Inappropriate intimacy            | reaching into another module's internals, bidirectional deps                         | Med, High if bidirectional                          | Move, Extract, hide internals          |

Thresholds are starting points. Raise severity when the smell sits in hot, frequently changed code and lower it in stable code nobody touches.

## Report

```
## Code Smell Report

### Stack: ...
### Files scanned: N | Smells found: N

### Summary by Category
| Category | Critical | High | Medium | Low | Total |
|---|---|---|---|---|---|
| Bloaters | | | | | |
| OO Abusers | | | | | |
| Change Preventers | | | | | |
| Dispensables | | | | | |
| Couplers | | | | | |

### Critical & High Smells (ranked by impact)
1. **Smell: location** (Severity)
   - File: `file:line`
   - Detail: what specifically is wrong
   - Impact: maintenance or bug risk, and churn if known
   - Refactoring: the concrete approach
   - Effort: S / M / L

### Top 10 Worst Files
| File | Lines | Smells | Worst Smell | Recommendation |
|---|---|---|---|---|

### Refactoring Priority Queue
1. Action: fixes N smells, effort S/M/L

### Metrics
- Average method length, average class length
- Longest method and largest class (name, lines, file)
- Deepest message chain (file:line)
```

Useful follow-ups: `/dead-code`, `/refactor` to carry out the top items, `/tech-debt-sprint`, `/perf` for smelly code on hot paths.
