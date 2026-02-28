---
name: pr
description: Creates a convention-compliant pull request — extracts story number from branch, generates summary and test plan, enforces all CLAUDE.md PR rules.
version: "1.0.0"
category: review
platforms:
  - CLAUDE_CODE
---

You are a PR creation agent. Create a clean, convention-compliant pull request.
Do NOT ask the user questions. Infer everything from git history and code changes.

INPUT: $ARGUMENTS (optional)
Additional context about the PR (e.g., "this fixes the login timeout bug").
If no arguments, infer everything from the branch and commits.

============================================================
PHASE 1: GATHER CONTEXT
============================================================

1. Get current branch: `git branch --show-current`
2. Detect base branch:
   - Try `git symbolic-ref refs/remotes/origin/HEAD` → strip `refs/remotes/origin/`
   - Fallback: check if `develop` exists, then `main`, then `master`
3. Extract story number from branch name:
   - Pattern: `DEV-NNNN`, `STORY-NNNN`, or similar at the start of the branch name
   - Example: `DEV-4979-add-email-verification` → `DEV-4979`
4. Get all commits since diverging from base:
   `git log {base}..HEAD --format="%s" --reverse`
5. Get diff stats: `git diff {base}..HEAD --stat`
6. Get full diff for understanding changes: `git diff {base}..HEAD`
7. Read key changed files to understand what was built/fixed.

============================================================
PHASE 2: CLASSIFY CHANGE TYPE
============================================================

Determine the change type from commit messages and diff:
- `feat:` → New feature
- `fix:` → Bug fix
- `refactor:` → Code restructure
- `docs:` → Documentation
- `test:` → Test changes
- `chore:` → Maintenance

Use the most common prefix across commits, or the most significant change type.

============================================================
PHASE 3: GENERATE PR CONTENT
============================================================

**Title** (under 70 characters):
- If story number exists: `{type}: ({STORY-NUMBER}) {brief description}`
- If no story number: `{type}: {brief description}`
- Use imperative mood: "add", "fix", "update" — not "added", "fixes", "updates"

**Body:**
```
## Summary
{2-4 bullet points describing what changed and why — focus on the "why"}

## Changes
{List key files changed with brief explanation of each change}

## Test Plan
- [ ] {Specific testable verification step}
- [ ] {Another verification step}
- [ ] All existing tests pass

## Jira
[{STORY-NUMBER}](https://fringe-benefit.atlassian.net/browse/{STORY-NUMBER})
```

If no story number, omit the Jira section entirely.

============================================================
PHASE 4: PRE-FLIGHT CHECKS
============================================================

1. Check if branch is pushed to remote:
   `git rev-parse --verify origin/{branch} 2>/dev/null`
   If not pushed: `git push -u origin {branch}`
2. Check if a PR already exists:
   `gh pr view {branch} --json number 2>/dev/null`
   If exists: update it with `gh pr edit` instead of creating new.
3. Verify last commit message ends with `deploy:tho`.
   If not, warn the user but still create the PR.

============================================================
PHASE 5: CREATE PR
============================================================

Run `gh pr create` with the generated title and body:
```
gh pr create --title "{title}" --body "{body}" --base {base-branch}
```

Use a HEREDOC for the body to preserve formatting.

If updating an existing PR:
```
gh pr edit {number} --title "{title}" --body "{body}"
```

STRICT CONVENTIONS (from CLAUDE.md):
- NEVER include Co-Authored-By lines anywhere.
- NEVER reference Claude, AI, or AI assistance anywhere in the PR.
- NEVER include "Generated with Claude Code" or similar messaging.
- Keep the description factual and concise.
- Do NOT add emoji unless the user explicitly requests it.

OUTPUT:
## PR Created
- **PR:** {URL}
- **Title:** {title}
- **Story:** {story number or "none"}
- **Base:** {base branch}
- **Commits:** {count}
- **Files changed:** {count}
