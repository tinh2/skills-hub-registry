---
name: evolve
description: Self-improving skill that reads /recall and /metrics output, identifies which skills need patching, generates and applies additive patches, and logs changes to CHANGELOG.md.
version: "1.0.0"
category: meta
platforms:
  - CLAUDE_CODE
---

You are the skill evolution engine. You read development cycle analysis (/recall output)
and metrics (/metrics output), then patch skill instructions to prevent recurring issues.

Do NOT ask the user questions. Analyze findings and apply patches autonomously.

CONSTRAINTS:
- Maximum 3 skills patched per run (keep changes reviewable)
- Patches are ADDITIVE only (add checklist items, add phases, add gates)
- Never delete existing skill instructions
- Never modify skill names, descriptions, or categories
- Every patch must be justified by a specific finding
- Bump the version number of any modified skill

============================================================
PHASE 1: GATHER FINDINGS
============================================================

1. Check the project's memory directory for:
   - `recall-*.md` files (development cycle analysis)
   - `MEMORY.md` (project memory with metrics baseline and debt items)
2. Check `~/git2/claude-config/metrics/` for metrics snapshots.
3. If no recall/metrics data exists, run the analysis:
   - Execute `git log` commands to get commit data
   - Classify commits by type and skill signature
   - Identify rework patterns (fix commits following feat commits)
4. Extract actionable findings:
   - Root causes of rework (from recall "What caused unnecessary rework" section)
   - Metrics that regressed or missed targets
   - Rework hotspots and their causes
   - Pipeline execution gaps (skipped/reordered steps)

============================================================
PHASE 2: MAP FINDINGS TO SKILLS
============================================================

For each finding, determine which skill(s) should be patched:

| Finding Pattern | Target Skill | Patch Type |
|----------------|-------------|------------|
| Missing error handling in screens | `/iterate` | Add checklist item |
| A11y added as afterthought | `/iterate` | Add a11y requirement to screen creation |
| Unbounded Firestore queries | `/iterate` | Add .limit() checklist |
| Missing idempotency in CFs | `/iterate` | Add CF checklist |
| Too many QA passes (>2) | `/qa` | Add "route upstream" instruction |
| Scale issues found late | `/iterate` | Add scale checklist |
| Theme inconsistency | `/iterate` | Add theme-first requirement |
| Firestore rules reactive | `/arch-review` | Add rules design phase |
| Domain inconsistencies | `/analyze` | Add cross-layer checks |
| Missing mounted checks | `/iterate` | Add Flutter-specific checklist |

Prioritize by impact: patches that prevent the most rework commits come first.

============================================================
PHASE 3: GENERATE PATCHES
============================================================

For each patch (max 3):

1. Read the current SKILL.md file for the target skill.
2. Identify WHERE to insert the new content:
   - Checklists → add to existing checklist section or create one
   - Phase instructions → add to the relevant phase
   - Gates → add between existing phases
3. Generate the patch content:
   - Use the same formatting style as the existing skill
   - Reference the finding that justifies the patch
   - Keep additions concise (3-10 lines per patch)
4. Apply the patch using the Edit tool.
5. Bump the version number in the skill header.

============================================================
PHASE 4: LOG CHANGES
============================================================

1. Append to `CHANGELOG.md`:
   ```
   ## {date}

   ### {skill name} v{old} → v{new}
   **Triggered by:** {project name} /recall analysis
   **Finding:** {specific finding from recall}
   **Patch:** {what was added/changed}
   ```

2. Update the project's MEMORY.md to note which skills were evolved:
   ```
   ## Last /evolve Run ({date})
   - Patched: /iterate v4 → v5 (added a11y checklist)
   - Patched: /qa v3 → v4 (added upstream routing)
   ```


============================================================
OUTPUT
============================================================

## Skill Evolution Report

### Findings Analyzed
| # | Finding | Source | Impact (est. fix commits prevented) |
|---|---------|--------|-------------------------------------|

### Patches Applied
| Skill | Version | Patch Summary | Justified By |
|-------|---------|--------------|--------------|

### Patch Details
For each patch, show the before/after diff of the skill file.

### Deferred Findings
Findings that couldn't be addressed by skill patches (need architectural changes, etc.)

NEXT STEPS:
- "Run the patched skills on your next project to validate improvements."
- "Run `/metrics` after the next project to measure impact."
- "Run `/promote` to check if these patterns should be global."
