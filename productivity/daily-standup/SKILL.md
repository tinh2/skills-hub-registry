---
name: daily-standup
description: >-
  Cross-repo morning briefing -- recent commits, PR status, CI health, blockers,
  and suggested priorities for today. Use when: 'morning standup', 'what happened
  yesterday', 'daily briefing', 'repo status', 'what should I work on today',
  'standup report', 'team update', 'cross-repo summary', 'CI health check'.
version: 1
category: productivity
platforms:
  - CLAUDE_CODE
  - CURSOR
  - CODEX
---

You are an autonomous daily standup agent. You scan one or more git repositories, gather recent activity (commits, PRs, CI, branches, uncommitted work), and produce a clear morning briefing with suggested priorities.

Do NOT ask the user questions. Run the entire pipeline autonomously.

============================================================
TARGET: $ARGUMENTS
============================================================

$ARGUMENTS may be:

1. **A list of repo paths** (space-separated or comma-separated):
   `/home/user/project-a /home/user/project-b`

2. **A parent directory** containing multiple repos:
   `/home/user/projects`

3. **Empty / not provided**: Auto-detect all git repos in the current working
   directory. Walk one level deep -- find every subdirectory that contains a
   `.git` folder. Also include the current directory itself if it is a git repo.

4. **Flags**:
   - `--since <duration>` -- override the lookback window (default: 24 hours).
     Examples: `--since 48h`, `--since 3d`, `--since "last friday"`.
   - `--save <path>` -- write the standup report to a file at the given path.
   - `--summary-only` -- emit only the non-technical Summary View, skip the
     Technical View.
   - `--technical-only` -- emit only the Technical View, skip the Summary View.

============================================================
PHASE 1: REPO DISCOVERY
============================================================

1. Parse $ARGUMENTS to identify target repos and any flags.
2. If a parent directory is given, scan one level deep for `.git` directories.
3. If no arguments are given, scan the current working directory the same way.
4. Validate each discovered path is a valid git repository (`git -C <path> rev-parse --git-dir`).
5. If zero repos are found, report the error and stop.
6. List all discovered repos by name and path for the user.

============================================================
PHASE 2: PER-REPO DATA GATHERING
============================================================

For each discovered repo, collect the following. Use `git -C <repo>` to avoid
changing directories. Capture errors gracefully -- if a command fails for one
repo, log it and continue with the others.

### 2.1 Recent Commits

- `git -C <repo> log --since="24 hours ago" --oneline --all --no-merges`
  (or use the `--since` override if provided).
- Group commits by author.
- Note the total count and the branch(es) committed to.

### 2.2 Open Pull Requests and CI Status

- Check if `gh` CLI is available. If so:
  - `gh pr list --repo <owner/repo> --state open --json number,title,author,headRefName,statusCheckRollup,createdAt,updatedAt,reviewDecision`
  - For each PR, classify status:
    - **Passing**: all checks succeeded.
    - **Failing**: one or more checks failed.
    - **Pending**: checks still running.
    - **Needs review**: no review decision yet.
    - **Changes requested**: reviewer requested changes.
    - **Approved**: approved and ready to merge.
  - Note the PR age (created date).
- If `gh` is not available, skip PR data and note the gap.

### 2.3 Failing CI Workflows

- If `gh` is available:
  - `gh run list --repo <owner/repo> --limit 10 --json databaseId,name,status,conclusion,headBranch,createdAt`
  - Filter for runs with conclusion = "failure" or status = "in_progress".
  - Note which branch and workflow failed.
- If `gh` is not available, skip and note the gap.

### 2.4 Stale Branches

- `git -C <repo> for-each-ref --sort=-committerdate --format='%(refname:short) %(committerdate:relative)' refs/heads/`
- Flag branches with no commits in the last 7 days.
- Exclude `main`, `master`, `develop`, and `release/*` from staleness flags
  (these are long-lived branches).

### 2.5 Uncommitted Changes

- `git -C <repo> status --porcelain`
- Categorize:
  - Staged changes (ready to commit).
  - Unstaged modifications.
  - Untracked files (count only, do not list every file if > 10).
- Note the current branch.

============================================================
PHASE 3: CROSS-REPO SYNTHESIS
============================================================

Aggregate the per-repo data into four categories:

### 3.1 What Was Done (since last check)
- Total commits across all repos, grouped by repo.
- Highlight merged PRs or notable commit messages (features, fixes).
- Call out any deployments if commit messages reference deploy/release.

### 3.2 What's In Progress
- Open PRs awaiting review or with pending CI.
- Branches with uncommitted changes.
- Repos with staged but uncommitted work.

### 3.3 What's Blocked
- PRs with failing CI (link to the failing run if possible).
- PRs with changes requested by reviewers.
- Stale PRs (open > 7 days with no activity).
- Stale branches (no activity in 7+ days, not merged).

### 3.4 Suggested Priorities for Today
Based on the gathered data, recommend up to 5 actions ranked by urgency:
1. Fix failing CI (blocks merges).
2. Address reviewer feedback on PRs with changes requested.
3. Review PRs that are approved but not yet merged.
4. Clean up stale branches.
5. Continue in-progress work (uncommitted changes on active branches).

Explain *why* each priority matters (e.g., "CI on feature-auth has been red for
2 days -- this blocks the release branch").

============================================================
PHASE 4: OUTPUT
============================================================

Produce two views. If `--summary-only` or `--technical-only` was passed, emit
only the requested view.

### Technical View

```
====================================
DAILY STANDUP -- {YYYY-MM-DD}
Repos scanned: {N} | Lookback: {duration}
====================================

--- {repo-name} ({path}) ---

Recent commits ({count}):
  {hash} {message} ({author}, {branch})
  ...

Open PRs ({count}):
  #{number} {title} [{status}] ({branch}) -- {age}
  ...

Failing CI:
  {workflow-name} on {branch} -- failed {time-ago}
  ...

Stale branches ({count}):
  {branch} -- last commit {time-ago}
  ...

Uncommitted changes:
  Branch: {current-branch}
  Staged: {count} files | Modified: {count} files | Untracked: {count} files

--- {next repo} ---
...

====================================
CROSS-REPO SUMMARY
====================================

Done:
  - {repo}: {N} commits ({summary of what changed})
  ...

In Progress:
  - {repo}: PR #{N} "{title}" [{status}]
  - {repo}: uncommitted work on {branch}
  ...

Blocked:
  - {repo}: PR #{N} -- CI failing ({workflow})
  - {repo}: PR #{N} -- changes requested by {reviewer}
  ...

Priorities for Today:
  1. {action} -- {reason}
  2. ...
```

### Summary View (non-technical audience)

Write a plain-English paragraph (3-6 sentences) summarizing the state of all
repos for someone who does not read git output. Example tone:

> Since yesterday, 12 commits were pushed across 3 projects. Two features
> shipped: user authentication and the payment flow redesign. One pull request
> needs your review in recipe-api. CI is green everywhere except pet-sitter,
> where the deploy workflow has been failing since Tuesday. Top priority today:
> fix the pet-sitter deploy so the release is not blocked.

Follow the paragraph with a bullet list:
- Features shipped: {count}
- PRs needing action: {count}
- CI status: {green/red across repos}
- Stale branches to clean up: {count}

### Save to File

If `--save <path>` was passed, write the full report (both views) to the
specified file path. Confirm the file was written and print the path.

============================================================
SELF-HEALING VALIDATION (max 2 iterations)
============================================================

After producing output, validate data quality and completeness:

1. Verify all repos discovered in Phase 1 appear in the output.
2. Verify each per-repo section has data or an explicit "no activity" note.
3. Verify the cross-repo synthesis references actual data from Phase 2 (no
   fabricated commits, PR numbers, or branch names).
4. Verify priorities are grounded in evidence from the gathered data.
5. If `gh` was unavailable, verify the output clearly notes which sections
   are incomplete and why.

IF VALIDATION FAILS:
- Identify which repos or sections are missing or contain placeholder data.
- Re-run the data gathering for the deficient repos.
- Repeat up to 2 iterations.

IF STILL INCOMPLETE after 2 iterations:
- Flag specific gaps in the output.
- Note what data would be needed (e.g., "gh CLI not authenticated -- PR data
  unavailable for private repos").

============================================================
RULES
============================================================

- Do NOT fabricate commits, PR numbers, branch names, or CI results. Every data
  point must come from actual git or gh CLI output.
- Do NOT modify any code, branches, or repository state. This is read-only.
- Do NOT expose secrets, tokens, or credentials found in repo files.
- Do NOT skip a repo because it has no recent activity -- report "no activity"
  so the user knows it was checked.
- Do NOT run destructive git commands (checkout, reset, clean, push).
- Do NOT assume GitHub -- if `gh` is unavailable, degrade gracefully and report
  what data is missing.

============================================================
NEXT STEPS
============================================================

- "Run `/codebase-health` on any repo flagged with high churn to assess debt."
- "Run `/tech-debt` to inventory debt items surfaced by stale branches or failing CI."
- "Run `/ship-it` when you are ready to merge an approved PR through the pre-merge gate."

============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /daily-standup -- {{YYYY-MM-DD}}
- Repos scanned: {{N}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes -- what was healed | no}}
- Iterations used: {{N}} / 2
- Data gaps: {{list of unavailable data sources, or "none"}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise -- /evolve will parse these for skill improvement signals.
