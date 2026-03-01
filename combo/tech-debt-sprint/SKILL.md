---
name: tech-debt-sprint
description: Debt reduction sprint chain — inventories tech debt, detects code smells, removes dead code, then hardens with a review pass.
version: "1.0.0"
category: combo
platforms:
  - CLAUDE_CODE
---

You are an autonomous tech debt reduction agent. Do NOT ask the user questions.

This skill chains four skills in sequence:
1. `/tech-debt` — inventory all technical debt in the codebase
2. `/code-smell` — detect and fix code smells
3. `/dead-code` — find and remove dead code
4. `/iterate-review` — full review pass to harden the cleaned codebase

INPUT: $ARGUMENTS
Pass a specific area to focus on, or leave empty for a full codebase sprint.

============================================================
PHASE 1: DEBT INVENTORY  (/tech-debt)
============================================================

Follow the instructions defined in the `/tech-debt` skill exactly.

Inventory all technical debt: TODO/FIXME/HACK comments, outdated dependencies,
missing tests, architectural violations (god objects, circular deps),
hardcoded values, and duplicated logic.

Record findings with severity (CRITICAL, HIGH, MEDIUM, LOW).
This inventory drives Phases 2 and 3. Do NOT fix anything yet.

============================================================
PHASE 2: CODE SMELL FIXES  (/code-smell)
============================================================

Follow the instructions defined in the `/code-smell` skill exactly.

Detect and fix code smells, prioritizing items from Phase 1: long methods,
god classes, duplicated code, deep nesting, primitive obsession, and
feature envy. Commit each fix with a descriptive refactor message.

IMPORTANT: Run tests after each fix. If a refactor breaks tests, fix the
tests if the refactor is correct, or revert if it introduced a bug.

============================================================
PHASE 3: DEAD CODE REMOVAL  (/dead-code)
============================================================

Follow the instructions defined in the `/dead-code` skill exactly.

Find and remove dead code: unused functions/classes, unreachable paths,
unused imports/variables, commented-out blocks, stale feature flags,
and orphaned test files.

IMPORTANT: Verify each removal (check dynamic refs, reflection) before
deleting. Run tests after removals. Commit with clear messages.

============================================================
PHASE 4: HARDENING REVIEW  (/iterate-review)
============================================================

Follow the instructions defined in the `/iterate-review` skill exactly.

Run a full iterative review pass on the now-cleaned codebase:
- Verify refactors from Phase 2 maintained correctness
- Verify removals from Phase 3 did not break anything
- Check for new issues introduced during the sprint
- Validate that architecture is cleaner post-sprint
- Run all tests and verify full pass

Fix any issues found during the review. This is the final quality gate.

============================================================
OUTPUT
============================================================

## Tech Debt Sprint Complete

| Phase | Skill | Status | Details |
|-------|-------|--------|---------|
| 1 | /tech-debt | DONE | {N} items inventoried ({N} critical, {N} high) |
| 2 | /code-smell | PASS/FAIL | {N} smells fixed, {N} files refactored |
| 3 | /dead-code | PASS/FAIL | {N} dead items removed, {N} lines deleted |
| 4 | /iterate-review | PASS/FAIL | {verdict}, {N} issues caught and fixed |

**Debt reduction:** {N} items resolved out of {N} inventoried
**Lines removed:** {N} (dead code + refactor simplifications)
**Test status:** {ALL PASS / FAILURES REMAIN}

NEXT STEPS:
- Commit and push the debt reduction branch
- Run `/preflight` before merging to main
- Schedule another `/tech-debt-sprint` in 2-4 weeks
- Track remaining debt items in the backlog
