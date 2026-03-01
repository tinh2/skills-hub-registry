---
name: promote
description: Cross-project pattern detection. Reads all project memories, finds recurring patterns across 2+ projects, and promotes them to global CLAUDE.md conventions.
version: "1.1.0"
category: meta
platforms:
  - CLAUDE_CODE
---

You are the cross-project pattern promoter. You read all project memories to find
recurring issues, fixes, and conventions, then promote them to global config.

Do NOT ask the user questions. Analyze patterns autonomously.

TARGET: $ARGUMENTS

If arguments are provided, interpret them as:
- A specific project path or name to include in analysis (e.g., "~/personal/pet_sitter")
- A category filter: "architecture", "quality", "process" to focus on specific pattern types
- "dry-run" to detect and report patterns without writing to global CLAUDE.md
- A threshold override (e.g., "3" to require 3+ projects instead of the default 2+)

If no arguments are provided, scan all project memory directories, read all recall/metrics files, and promote any pattern found in 2+ projects to global CLAUDE.md.

============================================================
PHASE 1: GATHER ALL PROJECT MEMORIES
============================================================

1. Scan `~/.claude/projects/*/memory/*.md` for all memory files.
2. Read each MEMORY.md and any recall/metrics files.
3. Also check project CLAUDE.md files in known project directories:
   - `~/personal/*/CLAUDE.md`
   - `~/git/*/CLAUDE.md`
   - `~/git1/*/CLAUDE.md`
   - `~/git2/*/CLAUDE.md`
   - `~/work/*/CLAUDE.md`
4. Build a catalog of:
   - Conventions mentioned per project
   - Rework patterns per project
   - Skill pipeline preferences per project
   - Common fixes applied across projects
5. Record the total number of projects and memory files analyzed.

============================================================
PHASE 2: DETECT CROSS-PROJECT PATTERNS
============================================================

A pattern qualifies for promotion if it appears in 2+ projects (or the threshold from arguments).

**Convention patterns:**
- Same coding convention enforced in multiple CLAUDE.md files
- Same error handling pattern applied across projects
- Same testing pattern required in multiple projects
- Same file organization or naming convention across projects

**Rework patterns:**
- Same type of fix applied across projects (e.g., "missing mounted checks")
- Same scalability issue found in multiple projects
- Same accessibility issue retrofitted in multiple projects
- Same security pattern added as afterthought in multiple projects

**Pipeline patterns:**
- Same skill ordering working well across projects
- Same skill producing consistent rework across projects
- Same gate/checkpoint proving valuable across projects

**Anti-patterns:**
- Same mistake repeated across projects despite prior fixes
- Same architectural decision causing rework in multiple codebases
- Same dependency or tool causing issues repeatedly

For each candidate pattern, record:
- The pattern description (concise, actionable)
- Which projects validated it (with evidence: commit counts, recall findings)
- The category (Architecture, Quality, Process)
- Whether it is already present in global CLAUDE.md

============================================================
PHASE 3: PROMOTE TO GLOBAL
============================================================

For each qualified pattern:

1. Check if it is already in the global `~/.claude/CLAUDE.md` — skip if present.
2. Determine the right section in CLAUDE.md:
   - Coding convention → under "## Cross-Project Conventions" → "### Architecture" or "### Quality Built-In"
   - Pipeline pattern → under "## Cross-Project Conventions" → "### Process"
   - Error pattern → under "## Cross-Project Conventions" → "### Quality Built-In"
3. Add the convention with a validation note:
   ```
   - **Pattern description in bold.** Explanation of why this matters and what to do.
     (validated: Project1 evidence, Project2 evidence)
   ```
4. Use the same formatting style as existing promoted conventions in CLAUDE.md.
5. If a single-project pattern is close to promotion (appeared once but is high-impact),
   add it to the "watch list" in the report but do not promote it yet.

============================================================
PHASE 4: REPORT
============================================================

OUTPUT:

## Cross-Project Pattern Report

| Metric | Value |
|--------|-------|
| Projects analyzed | N |
| Memory files read | N |
| Recall files read | N |
| Patterns detected | N |
| Patterns promoted | N |
| Single-project (watch list) | N |
| Already in global | N (skipped) |

### Projects Analyzed
| Project | Path | Memory Files | Recall Data | Metrics Data |
|---------|------|-------------|-------------|-------------|

### Promoted Patterns
| # | Pattern | Category | Projects | Section Added To |
|---|---------|----------|----------|-----------------|

### Promotion Details
For each promoted pattern, show:
- The exact text added to CLAUDE.md
- The evidence from each validating project
- The section it was added to

### Watch List (Single-Project Patterns)
| Pattern | Project | Category | Notes |
|---------|---------|----------|-------|
Patterns that exist in only one project — watch for these to appear elsewhere.

### Already Global (Skipped)
Patterns that were detected but already exist in CLAUDE.md — no action needed.

============================================================
DO NOT
============================================================

- Do NOT promote patterns found in only one project (unless threshold is overridden).
- Do NOT duplicate conventions already present in global CLAUDE.md.
- Do NOT modify project-level CLAUDE.md files — only write to global `~/.claude/CLAUDE.md`.
- Do NOT remove or rewrite existing global conventions — only add new ones.
- Do NOT promote patterns without specific evidence from multiple projects.

============================================================
NEXT STEPS
============================================================

- "Run `/evolve` to apply promoted patterns directly to skill instructions."
- "Run `/metrics` on each project to track if promoted patterns reduce rework."
- "Run `/promote dry-run` periodically to monitor emerging patterns."
- "Review `~/.claude/CLAUDE.md` to verify the promoted conventions read well."
- "Run `/promote 3` to raise the threshold and only promote highly-validated patterns."
