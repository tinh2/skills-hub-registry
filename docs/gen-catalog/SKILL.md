---
name: gen-catalog
description: Auto-generates README.md and skills-list from SKILL.md frontmatter across all skill directories, eliminating manual documentation updates.
version: "1.1.0"
category: docs
platforms:
  - CLAUDE_CODE
---

You are a catalog generation agent. Do NOT ask the user questions.

============================================================
TARGET: $ARGUMENTS
============================================================

- If $ARGUMENTS contains "readme", only regenerate README.md (skip skills-list).
- If $ARGUMENTS contains "skills-list", only regenerate skills-list/SKILL.md (skip README).
- If $ARGUMENTS contains a directory path, scan only that directory for SKILL.md files.
- If $ARGUMENTS is empty, scan all directories and regenerate both README.md and skills-list/SKILL.md.

============================================================
PHASE 1: DISCOVER ALL SKILLS
============================================================

1. Glob for all `*/SKILL.md` and `*/skill.md` files under `./`.
2. Also check `~/.claude/commands/*.md` for global commands (these are slash commands
   that exist outside the skills directory).
3. For each file found, parse the YAML frontmatter:
   - `name` (required)
   - `description` (required)
   - `version` (required)
   - `category` (optional — one of: discovery, spec, build, test, quality, docs, ops, combo)
   - If `category` is missing, infer from the instructions content:
     - "competitive" / "research" / "product analysis" → discovery
     - "spec" / "story" / "jira" / "design review" → spec
     - "implement" / "build" / "scaffold" / "iterate" / "ship" → build
     - "test" / "e2e" / "walkthrough" / "QA test plan" → test
     - "review" / "analyze" / "audit" / "consistency" / "UX" → quality
     - "README" / "documentation" / "catalog" → docs
     - "security" / "compliance" / "icon" / "image" / "infrastructure" → ops
     - "chain" / "combo" / "Follow the instructions defined in" → combo
4. Detect combo chains by scanning instructions for the pattern:
   "Follow the instructions defined in the `/X` skill"
   or "Chains /X → /Y" in the description.
   Record the chain sequence for each combo skill.

============================================================
PHASE 2: GENERATE README.md
============================================================

Read the existing `./README.md`.

Preserve everything ABOVE the line `<!-- AUTO-GENERATED-SKILLS-TABLE-START -->`.
Preserve everything BELOW the line `<!-- AUTO-GENERATED-SKILLS-TABLE-END -->`.

If these markers do not exist yet, add them. Place the start marker after the
first heading and intro paragraph. Place the end marker before the
"## Autonomous Build & Improve Chains" section (or at the end if that section
does not exist).

Between the markers, generate:

### Skills by Category

For each category (in this order: discovery, spec, build, test, quality, docs, ops, combo):

#### [Category Display Name]

| Skill | Description | Version |
|-------|------------|---------|
| `/name` | description | vN |

Category display names:
- discovery → "Product Discovery & Research"
- spec → "Spec & Design"
- build → "Build & Implement"
- test → "Testing & QA"
- quality → "Code Quality & Review"
- docs → "Documentation & Reporting"
- ops → "Operations & Security"
- combo → "Combo Chains"

For combo skills, add a "Chain" column:

| Skill | Chain | Description | Version |
|-------|-------|------------|---------|
| `/name` | `/a` → `/b` → `/c` | description | vN |

Also include global commands from `~/.claude/commands/` with a note:
> Global commands (available in any project):
| Command | Description |
|---------|------------|
| `/name` | description |

============================================================
PHASE 3: GENERATE skills-list/SKILL.md
============================================================

Read the existing `./skills-list/SKILL.md` (or `skill.md`).

Replace ONLY the hardcoded skills table (the content between the `instructions: |`
line's table section). Keep the YAML frontmatter. Keep any manually-written sections
after the table (pipeline diagrams, parallelization rules, development patterns).

The generated table should match the format already used in skills-list:

| Skill | Description |
|---|---|
| **name** | description |

Group by category with category headers.

============================================================
PHASE 4: VERIFY
============================================================

1. Count total skills discovered.
2. Count skills in generated README table.
3. Count skills in generated skills-list table.
4. All three counts must match. If not, flag the discrepancy.
5. Check for orphan directories (dirs under ./ with no SKILL.md).
6. Check for skills referenced in combo chains that don't exist.

============================================================
PHASE 5: COMMIT (optional)
============================================================

If changes were made, stage README.md and skills-list/SKILL.md (or skill.md).
Commit: "docs: auto-generate skills catalog (N skills)"

Do NOT include Co-Authored-By lines.
Push after committing.

============================================================
OUTPUT
============================================================

## Catalog Generated

| Metric | Value |
|--------|-------|
| Skills discovered | N |
| README.md updated | N skills in table |
| skills-list updated | N skills in table |
| Orphan directories | [list or "none"] |
| Missing chain targets | [list or "none"] |
| Global commands found | N |

============================================================
NEXT STEPS
============================================================

- Run `/skills-list` to view the updated catalog in the terminal.
- Run `/readme` to enhance the README beyond the auto-generated table.
- Run `/bootstrap` to scaffold a new project using skills from the catalog.
- Run `/recall` to analyze development patterns and feed insights back.

============================================================
DO NOT
============================================================

- Do NOT modify any SKILL.md files other than skills-list/SKILL.md — this skill only reads frontmatter.
- Do NOT invent skills that were not discovered — only catalog what exists.
- Do NOT remove manually-written sections from README.md outside the auto-generated markers.
- Do NOT delete orphan directories — only report them.
- Do NOT skip the verification phase — count mismatches indicate catalog drift.
