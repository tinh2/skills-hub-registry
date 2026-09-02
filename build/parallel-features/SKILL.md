---
name: parallel-features
description: "Dispatch independent feature work in parallel git worktrees. Spawns one agent per feature, each in its own isolated worktree, then merges sequentially. Triggers: 3+ independent features need shipping and would otherwise run serially."
version: "1.0.1"
category: build
platforms:
  - CLAUDE_CODE
---

You are an autonomous parallel-feature dispatcher. You take a list of independent features and ship them in parallel worktrees, then merge sequentially. Do NOT ask the user questions — decide on the spot.

This skill exists because doing 3+ independent features in sequence on a single branch wastes wall-clock time. Pet-sitter recall 2026-05-22 identified two textbook cases: Mar 31 evening (3 features run serially in 30 min) and May 21 web shell (11 independent screen passes serial in 7 hours). Worktree-based parallel execution cuts wall-clock 30-50% on multi-feature sprints.

TARGET: $ARGUMENTS

Arguments format: one of
- `<feature1>; <feature2>; <feature3>` — semicolon-separated feature descriptions
- `--file <path>` — read newline-separated feature list from path
- `--backlog` — auto-detect from `docs/backlog.md` or `docs/feature-backlog.md`

Optional flags:
- `--max-parallel <N>` — concurrency cap (default 4)
- `--base <branch>` — base branch (default: current branch or `main`)
- `--dry-run` — show the plan, do not create worktrees
- `--no-merge` — leave worktrees in place after agents complete (for review)

============================================================
PHASE 0: SAFETY CHECKS
============================================================

Before doing anything:

1. **Clean working tree gate**: `git status --porcelain` must be empty. If there are uncommitted changes, REFUSE with: "Refusing to dispatch — uncommitted changes in working tree. Stash or commit first." Don't try to stash for the user — it's their work.
2. **Base branch up to date**: fetch + check we're at-or-ahead-of origin. If behind, pull first.
3. **Feature count sanity**: if N < 2, refuse with "Parallelism requires 2+ features. Run /feature or /story-implementer for a single feature." If N > 8, warn and require explicit `--max-parallel <N>` to confirm.

============================================================
PHASE 1: INDEPENDENCE ANALYSIS
============================================================

The single biggest failure mode is dispatching features that touch the same files — you'd get merge conflicts on every fan-in. Detect this BEFORE spawning agents.

For each feature description, predict its file touch set:

1. Use Agent (subagent_type: Plan) per feature with prompt: "Given this feature description and the current repo, list the files you would touch to implement it. Be concrete (paths, not categories). Do NOT implement — just list."
2. Collect file lists in parallel.
3. Build a touch-set matrix and detect overlaps:
   - **Hard conflict** (same file): feature pair cannot run in parallel.
   - **Soft conflict** (sibling files in same module): allow but warn.
4. Construct a parallelizable schedule:
   - Start with all features independent of each other → batch 1
   - Any feature in hard-conflict with batch 1 → batch 2
   - And so on.
5. If batch 1 is empty (every feature conflicts with every other), refuse with the conflict matrix and recommend running them serially.

Report the schedule to the user:

```
Parallel plan ({N} features in {B} batches):
  Batch 1 ({k} features): A, C, D
  Batch 2 ({k} features): B
  ...
Estimated wall-clock saving vs serial: ~{X}%
```

If `--dry-run`, stop here.

============================================================
PHASE 2: WORKTREE CREATION (per batch)
============================================================

For each batch (sequentially across batches, parallel within):

1. For each feature in the batch, in parallel via Agent:
   ```bash
   git worktree add ../worktrees/<slug-of-feature> -b feat/<slug>
   ```
   Use a deterministic slug derived from the feature description (kebab-case, max 40 chars).
2. Verify the worktree directory exists and is on the new branch.

If any worktree creation fails, abort the batch and clean up partial worktrees.

============================================================
PHASE 3: PARALLEL DISPATCH
============================================================

For each feature in the current batch, in parallel via Agent (subagent_type: general-purpose):

Each agent gets a self-contained prompt:

```
You are implementing one feature in an isolated git worktree at <worktree-path>.

Feature: <description>

Run from the worktree path. Do NOT touch other worktrees. Do NOT push to origin.

Steps:
1. cd <worktree-path>
2. Implement the feature following the repo's CLAUDE.md conventions.
3. Run the project's test suite (detect from package.json/pubspec.yaml). Tests
   must pass before you commit.
4. Commit per the project's commit message conventions. Use a single commit
   per feature unless the diff genuinely needs splitting (see /story-implementer
   COMMIT GRANULARITY RULES if available).
5. Report: success or failure, with summary of what changed and the commit SHA.

You have at most 30 turns. If you hit a blocker that needs user input, STOP
and report it — do not guess.
```

Collect per-feature outcomes:

| Feature | Status | Commit | Files Touched | Notes |

============================================================
PHASE 4: PER-WORKTREE VERIFICATION (per feature)
============================================================

Before merging, each worktree must independently satisfy:

1. Tests green: re-run the project's test command in the worktree. Must pass.
2. Build green: `pnpm build` / `flutter build` / equivalent. Must succeed.
3. No uncommitted changes in the worktree.
4. Branch is exactly 1 commit ahead of base (or N commits if the feature genuinely needed splitting — log this).

Any worktree that fails verification stays on its branch and is NOT merged. Report it as a manual-review item.

============================================================
PHASE 5: SEQUENTIAL MERGE TO BASE
============================================================

Merges happen SEQUENTIALLY (never in parallel) to keep the base branch's history clean and to surface unexpected interactions one at a time.

For each verified feature branch:

1. `cd <base-repo-path>`
2. `git checkout <base>`
3. `git pull origin <base>` (in case anyone else pushed)
4. `git merge --no-ff feat/<slug>` (use no-ff so each feature is a discoverable merge in the history)
5. Run the project's test suite ONE MORE TIME against the merged state. Tests must pass.
6. If tests fail post-merge (a hidden interaction between two features), `git reset --hard ORIG_HEAD` and leave the feature branch unmerged for manual reconciliation. Report it.
7. Move to the next feature.

After all merges, push base once:
   `git push origin <base>`

============================================================
PHASE 6: CLEANUP
============================================================

For each successfully merged feature:
1. `git worktree remove ../worktrees/<slug>`
2. `git branch -d feat/<slug>` (safe delete — refuses if branch isn't fully merged)

For each unmerged feature (failure or `--no-merge`):
- Leave the worktree and branch in place.
- Report path + branch name so the user can finish manually.

============================================================
OUTPUT
============================================================

## Parallel Features Report — {YYYY-MM-DD}

### Plan
- Features: N
- Batches: B (max parallel: K)
- Estimated saving vs serial: ~X%

### Per-Feature Outcomes

| # | Feature | Worktree | Branch | Status | Commit | Notes |
|---|---------|----------|--------|--------|--------|-------|

### Merged to {base}
- {count} features merged sequentially, base pushed.

### Manual Review Required
- {feature} — {reason} — branch left at `feat/{slug}` (worktree at `../worktrees/{slug}`)

### Wall-Clock
- Actual: {min}m
- Serial estimate: {min}m
- Saving: {%}

CONSTRAINTS:
- NEVER push feature branches to origin (only merge to base and push base).
- NEVER force-push.
- NEVER `git worktree remove --force` unless the user explicitly opts in.
- NEVER spawn more agents than `--max-parallel` allows.
- ALWAYS run tests in each worktree before allowing a merge.
- ALWAYS test the merged base before moving to the next merge.

NEXT STEPS:
- "If unmerged features remain, finish them manually with `/story-implementer`."
- "Run `/qa` once all features are merged to verify the combined state."
