---
name: fix-and-ship
description: Emergency pipeline — chains /hotfix then /preflight to fix a bug and verify it's safe to deploy.
version: "1.0.0"
category: combo
platforms:
  - CLAUDE_CODE
---

You are an autonomous emergency fix-and-deploy agent. Do NOT ask the user questions.

This skill chains two skills in sequence:
1. `/hotfix` — diagnose and fix the bug
2. `/preflight` — verify everything is safe to deploy

INPUT: $ARGUMENTS
Pass the bug description, error message, or area that's broken.

============================================================
PHASE 1: HOTFIX
============================================================

Follow the instructions defined in the `/hotfix` skill.
Pass the input arguments to the hotfix skill.

The hotfix skill will:
- Diagnose the bug (max 2 iterations)
- Apply the minimal fix
- Run tests
- Commit with conventional commit format
- Push and create a PR

If the hotfix skill reports failure (couldn't fix in 2 iterations),
STOP and report the findings. Do NOT proceed to preflight.

============================================================
PHASE 2: PREFLIGHT
============================================================

Follow the instructions defined in the `/preflight` skill.

The preflight skill will verify:
- Clean git status
- Build passes
- All tests pass
- Conventions enforced (conventional commits)
- Migration status

============================================================
OUTPUT
============================================================

## Fix and Ship Complete

### Hotfix
- **Bug:** {what was broken}
- **Cause:** {root cause}
- **Fix:** {file:line — what changed}
- **PR:** {URL}

### Preflight
- **Verdict:** {READY / NOT READY}
- **Issues:** {list any, or "none"}

### Status: {SHIPPED / BLOCKED}
{If SHIPPED: "PR is ready for review and merge."}
{If BLOCKED: "Preflight failed. Fix the issues listed above before deploying."}

NEXT STEPS:

- "Run `/qa` to verify the fix didn't introduce regressions."
- "Run `/e2e` to run automated end-to-end tests against the patched build."
