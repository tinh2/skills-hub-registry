---
name: skills-list
description: " — a Claude Code skill for automating skills-list workflows."
version: 1.0.0
category: analysis
platforms:
  - CLAUDE_CODE
---

Dynamically discover and display all installed skills.

## How to discover skills

1. List all directories under `~/.claude/skills/`
2. For each directory, read its `SKILL.md` file
3. Extract the `name` and `description` from the YAML frontmatter
4. Sort alphabetically by name

## Output format

Print a markdown table with two columns: **Skill** and **Description**.
- Skill column: bold skill name as a slash command (e.g., **`/iterate`**)
- Description column: first sentence or line of the description (keep it concise, max ~120 chars, trim trailing whitespace)
- Skip any directory that does not contain a SKILL.md or has no parseable frontmatter
- At the end, print a total count: "**N skills available.**"

## Important

- Do NOT use a hardcoded list. Always read from disk at runtime so the catalog stays current.
- Do NOT invoke any skills. This is a read-only catalog display.
- If a description spans multiple lines in YAML (using `>` or `|`), join them into one line and take the first sentence.
