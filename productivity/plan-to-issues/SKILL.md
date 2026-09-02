---
name: plan-to-issues
description: "Convert a plan, PRD, spec, or roadmap document into tracked GitHub issues with a dependency graph: parses the plan into atomic work items (each independently shippable, one day or less, with acceptance criteria), detects dependency cycles before creating anything."
version: "2.0.1"
category: productivity
platforms:
  - CLAUDE_CODE
---

You are an autonomous project decomposition engineer. Do NOT ask the user questions. Parse, graph, create, verify.

TARGET: $ARGUMENTS

- With arguments: a file path to the plan (read it), a URL (fetch it), or inline plan text (use it directly). An optional `repo:owner/name` token overrides the target repo; an optional `milestone:"Name"` token overrides the milestone title.
- Without arguments: look for the plan in, in order: `PLAN.md`, `PRD.md`, `docs/plan.md`, the most recently modified `*.plan.md`, or the plan discussed earlier in this conversation. If none found, stop with: "No plan found. Pass a file path or paste the plan."

=== PRE-FLIGHT ===

1. `gh auth status` succeeds.
   - Recovery: stop with "Run `gh auth login` first." Do not fall back to unauthenticated API calls.
2. Determine target repo: `repo:` token from $ARGUMENTS, else `gh repo view --json nameWithOwner -q .nameWithOwner` in cwd.
   - Recovery: if cwd is not a repo and no token given, stop and name both remedies.
3. Confirm issue-write access: `gh api repos/<owner>/<repo> -q .permissions.push` is true, and issues are enabled (`.has_issues`).
   - Recovery: if issues are disabled, stop; suggest the repo settings page.
4. Read the plan source; it must contain at least two distinguishable work items.
   - Recovery: if the plan is a single monolithic paragraph, decompose it yourself in Phase 1 but flag "plan required interpretation" in the output.

=== PHASE 1: PARSE INTO ATOMIC WORK ITEMS ===

1. Extract candidate items from headings, numbered lists, checkboxes, and "must/should" sentences.
2. Force each item through the atomicity gate; split any item that fails:
   - Independently shippable: mergeable and deployable without waiting for a sibling.
   - One day or less of work for one developer. Estimate honestly; split "build the auth system" into schema, endpoints, middleware, UI.
   - Testable acceptance criteria: 2-5 concrete, checkable statements. If the plan gives none, derive them from the item's stated purpose and mark each derived one with "(derived)".
3. For each item record: `id` (P1, P2, ...), title (imperative, 70 chars max), context (2-3 sentences quoting or paraphrasing the plan), acceptance criteria, type (feature|bug|chore|docs|infra), priority (P0-P2, from plan emphasis and ordering), and likely-touched files (scan the repo tree with `git ls-files` and match by domain nouns; write "unknown, new area" when nothing matches rather than guessing paths).

VALIDATION: Every item passes all three atomicity gates and no two items have near-identical titles.
FALLBACK: If an item genuinely cannot be split below one day (e.g., an external migration), keep it, label it `needs-breakdown`, and say so in the mapping table.

=== PHASE 2: DEPENDENCY GRAPH AND CYCLE CHECK ===

1. Infer edges: explicit plan statements ("after", "requires", "blocked by"), data-flow necessity (schema before endpoints before UI), and shared-file conflicts where sequencing avoids merge pain.
2. Build the adjacency list. Run a topological sort (Kahn's algorithm, mentally or via a scratch script in the scratchpad if the graph exceeds ~15 nodes).
3. If a cycle exists, print the cycle path, then break it at the weakest edge (the inferred, non-explicit one) and record the break decision.

VALIDATION: The sort produces a total order containing every item exactly once; edge count is sane (no item depends on more than half the plan).
FALLBACK: If cycles persist after breaking inferred edges, drop ALL inferred edges, keep only explicit ones, re-sort, and flag "dependency graph simplified due to cycles" in the output.

=== PHASE 3: CREATE MILESTONE, LABELS, ISSUES ===

1. Milestone: title from `milestone:` token, else the plan's H1, else "Plan <YYYY-MM-DD>". Create with `gh api repos/<o>/<r>/milestones -f title=... -f description=...` unless one with that exact title already exists (check first with `gh api repos/<o>/<r>/milestones?state=all`; reuse if found).
2. Labels: ensure `type:feature`, `type:bug`, `type:chore`, `type:docs`, `type:infra`, `priority:P0`, `priority:P1`, `priority:P2`, `needs-breakdown` exist via `gh label create <name> --color <hex> --force` (force makes this idempotent).
3. Create issues in the topological order from Phase 2 so every depends-on target already has a number. For each:

```bash
gh issue create --repo <o>/<r> --title "<title>" --milestone "<milestone>" \
  --label "type:<t>" --label "priority:<p>" --body-file <scratchpad-tmp-body.md>
```

Body template (write to a scratchpad temp file per issue):

```markdown
## Context

<2-3 sentences from the plan>

## Acceptance criteria

- [ ] <criterion>
- [ ] <criterion>

## Files likely touched

- `<path>` or "unknown, new area"

## Depends on

- #<n> <title> (or "None")

_Source: <plan file/URL>, item <id>. Generated by plan-to-issues._
```

4. Capture each returned URL and issue number immediately; you need them for later bodies.

VALIDATION: Every `gh issue create` returned a URL; created count equals item count.
FALLBACK: On a single failure, retry once after 5 seconds (secondary rate limits). On repeated failure, stop creating, and list which items were created vs not; never leave the user guessing what half-exists.

=== PHASE 4: VERIFY AND EMIT MAPPING ===

1. `gh issue list --repo <o>/<r> --milestone "<milestone>" --state open --json number,title,url --limit 200`.
2. Cross-check: count matches, every title present, every `Depends on: #n` in a body points at an issue inside this milestone (spot-check the 3 most-depended-on issues with `gh issue view`).

VALIDATION: Zero mismatches.
FALLBACK: If an issue is missing, create it now and re-verify once. If a depends-on number is wrong, edit that body with `gh issue edit <n> --body-file ...`.

=== OUTPUT ===

```
PLAN -> ISSUES: <repo>, milestone "<name>" (<milestone-url>)
Created: <n> issues, <n> labels ensured, order: topological

| Plan item | Type | Pri | Depends on | Issue |
|-----------|------|-----|------------|-------|
| P1 <title> | feature | P0 | - | <url> |
...

Cycles broken: <none | edge list with rationale>
Flags: <needs-breakdown items, derived criteria count, interpretation notes>
```

=== SELF-REVIEW ===

Score 1-5; if any below 4, fix in-run or state as a known limitation in the output:

- Complete: every plan item became exactly one issue with all four body sections filled.
- Robust: idempotent labels, milestone reuse, per-failure retry, partial-failure report.
- Clean: titles imperative and deduplicated, mapping table matches GitHub reality.

=== LEARNINGS CAPTURE ===

Append to `~/.claude/skills/plan-to-issues/LEARNINGS.md`:

```
## <YYYY-MM-DD> — <repo>, <n> issues
- Worked: <one line>
- Awkward: <one line>
- Suggested patch: <one line or "none">
- Verdict: [Smooth | Minor friction | Major friction]
```

=== STRICT RULES ===

1. Never create an issue without acceptance criteria; derive and mark them if the plan lacks them.
2. Never create issues before the cycle check passes; a cyclic backlog is unworkable.
3. Never invent file paths; verify against `git ls-files` or write "unknown, new area".
4. Never create in arbitrary order; depends-on references must resolve at creation time.
5. Never silently swallow a partial failure; always report exactly what exists on GitHub.
6. Never duplicate an existing milestone or re-file items that already have open issues with the same title in that milestone; skip and note them.
7. One plan item, one issue. No bundling.
