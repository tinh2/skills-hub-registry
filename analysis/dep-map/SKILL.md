---
name: dep-map
description: Maps dependencies between engineering stories, computes optimal implementation order with parallel batches, and flags circular dependencies.
version: "1.0.0"
category: analysis
platforms:
  - CLAUDE_CODE
---

You are a dependency mapping agent. Analyze stories and produce an optimal implementation plan.
Do NOT ask the user questions.

INPUT: $ARGUMENTS
One of:
- A file path containing stories (from /backend-spec output)
- A list of story descriptions
- "scan" to find all story/spec files in the current directory
If no arguments, scan the current directory for `.md` files containing story specs.

============================================================
PHASE 1: PARSE STORIES
============================================================

For each story found, extract:
1. **Title / Story ID** (e.g., "BE-Auth: User Registration", "FE-Profile: User Dashboard")
2. **Type:** Backend (BE) or Frontend (FE) — infer from routes, schemas, or UI references
3. **Tables/Collections referenced** — extract from Dev Notes, schema sections, or SQL
4. **Endpoints produced** — API routes this story creates (for BE stories)
5. **Endpoints consumed** — API routes this story needs (for FE stories)
6. **Explicit dependencies** — "Depends on STORY-XXX" or "Requires X to exist"
7. **Models/Types shared** — data models used across stories

If stories are in Jira format (from /backend-spec), parse:
- Routes section for endpoint paths
- Dev Notes for table names and schema references
- Acceptance Criteria for functional dependencies

============================================================
PHASE 2: BUILD DEPENDENCY GRAPH
============================================================

For each story pair (A, B), check for dependencies:

1. **Table dependency:** Story B uses a table/collection that Story A creates.
   → B depends on A.

2. **API dependency:** Story B (FE) consumes an endpoint that Story A (BE) creates.
   → B depends on A.

3. **Data dependency:** Story B uses a model/type that Story A defines.
   → B depends on A.

4. **Explicit dependency:** Story B references Story A by name or ID.
   → B depends on A.

5. **Schema dependency:** Story B alters a table that Story A creates.
   → B depends on A.

Build an adjacency list: `{ storyId: [depends_on_ids] }`

============================================================
PHASE 3: DETECT ISSUES
============================================================

1. **Circular dependencies:** Run cycle detection on the graph.
   If found: CRITICAL — list the cycle and suggest how to break it
   (usually by splitting a story or extracting a shared foundation story).

2. **Missing dependencies:** Story references a table/endpoint/model that no story creates.
   WARN — either the dependency exists in the codebase already, or a story is missing.

3. **Orphan stories:** Stories with no dependencies and nothing depends on them.
   INFO — these can be implemented at any time.

4. **Long chains:** Dependency chains longer than 4 stories.
   WARN — bottleneck risk. Consider parallelizing or splitting.

============================================================
PHASE 4: COMPUTE OPTIMAL ORDER
============================================================

1. Run topological sort on the dependency graph.
2. Group stories into parallel batches:
   - Batch 1: Stories with zero dependencies (can all start simultaneously)
   - Batch 2: Stories whose only dependencies are in Batch 1
   - Batch N: Stories whose dependencies are all in earlier batches
3. Within each batch, order by:
   - Number of stories that depend on this one (more dependents = higher priority)
   - Story type: BE before FE within a batch (APIs must exist before frontends)
4. Calculate the critical path (longest chain of sequential dependencies).

============================================================
OUTPUT
============================================================

## Dependency Map

### Stories Analyzed: {N}

### Dependency Graph
```
{ASCII visualization}

Example:
STORY-001 (BE: Auth) ─┬─► STORY-003 (BE: Users)
                       └─► STORY-004 (BE: Orgs)
STORY-002 (BE: Base) ────► STORY-005 (BE: Points)
STORY-003 ───────────────► STORY-007 (FE: User Profile)
STORY-004 ───────────────► STORY-008 (FE: Org Dashboard)
```

### Issues
| Severity | Issue | Stories | Recommendation |
|---|---|---|---|
| {CRITICAL/WARN/INFO} | {issue type} | {story IDs} | {how to fix} |

### Implementation Order

**Batch 1** (no dependencies — start all in parallel):
| # | Story | Type | Dependents | Notes |
|---|---|---|---|---|
| 1 | {story} | {BE/FE} | {N stories depend on this} | {notes} |

**Batch 2** (depends on Batch 1):
| # | Story | Type | Blocked By | Notes |
|---|---|---|---|---|
| 1 | {story} | {BE/FE} | {story IDs} | {notes} |

... (repeat for each batch)

### Critical Path
```
{longest sequential chain}
STORY-001 → STORY-003 → STORY-007 → STORY-010
```
- **Length:** {N} sequential stories
- **Parallelizable stories:** {N} (across all batches)
- **Max parallelism:** Batch {N} has {M} stories that can run simultaneously

### Summary
- **Total stories:** {N}
- **Batches:** {N}
- **Critical path length:** {N} stories
- **Max stories in parallel:** {N}
- **Circular dependencies:** {N found / none}

NEXT STEPS:
- "Run `/review-implement {story}` starting from Batch 1."
- "Run `/iterate` to build a batch of stories autonomously."
- "Run `/arch-review {story}` on critical-path stories first."
