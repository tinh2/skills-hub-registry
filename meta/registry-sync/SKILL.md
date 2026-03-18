---
name: registry-sync
description: "Validate the entire skills registry — scan all SKILL.md files for frontmatter correctness, check category READMEs are current, detect duplicate skill names, find broken cross-references, compute per-skill quality scores, and optionally auto-fix mismatches and missing READMEs"
version: "2.0.0"
category: meta
platforms:
  - CLAUDE_CODE
---

You are in AUTONOMOUS MODE. Do NOT ask questions. Scan, validate, and report.

You are the registry sync and validation engine. You scan the entire skills
registry, validate every SKILL.md file, check structural integrity, ensure
READMEs are current, and produce a comprehensive health report.

INPUT:
$ARGUMENTS

The user may provide:
1. No arguments — run full registry sync.
2. `--fix` — automatically fix issues that can be auto-corrected (missing READMEs, outdated lists).
3. `--category [name]` — validate only a specific category.
4. `--report-only` — skip fixes, only produce the report.

Default behavior (no arguments): validate everything, report issues, do not auto-fix.

============================================================
PHASE 1: REGISTRY SCAN
============================================================

1. Identify the registry root directory (current working directory or $ARGUMENTS path).
2. Scan all top-level directories to discover categories.
   Expected categories: build, meta, analysis, deploy, test, qa, review, security,
   docs, ux, combo, productivity, integration.
3. Within each category, scan for subdirectories containing `SKILL.md` files.
4. Build a registry index:
   ```
   {
     category: string,
     skills: [
       {
         name: string,
         path: string,
         frontmatter: { name, description, version, category, platforms },
         instructionLength: number,
         lineCount: number
       }
     ]
   }
   ```
5. Report any directories that lack a SKILL.md file.
6. Report any SKILL.md files found outside of category directories.

============================================================
PHASE 2: FRONTMATTER VALIDATION
============================================================

For each SKILL.md, validate the frontmatter:

1. **name** — Present, string, lowercase, alphanumeric + hyphens only, no spaces.
   MUST match the directory name it lives in.
2. **description** — Present, string, >= 50 characters.
3. **version** — Present, string, valid semver format (X.Y.Z).
4. **category** — Present, string, must be a valid category name.
   MUST match the parent directory name.
5. **platforms** — Present, array, must include "CLAUDE_CODE".

Record each validation as PASS, WARN, or FAIL with the specific issue.

============================================================
PHASE 3: INSTRUCTION VALIDATION
============================================================

For each SKILL.md, validate the instruction body:

1. **Minimum Length**: Instructions (after frontmatter) >= 500 characters.
2. **Autonomous Mode**: Contains "Do NOT ask questions" or "AUTONOMOUS MODE".
3. **Input Section**: Has an INPUT or $ARGUMENTS section defining what the skill accepts.
4. **Phase Structure**: Has 3+ phases separated by `============` lines.
5. **Output Section**: Has a structured OUTPUT section.
6. **Guardrails**: Has a "DO NOT" section with prohibitions.
7. **Next Steps**: Has a "NEXT STEPS" section with follow-up suggestions.

Compute the quality score for each skill using the rubric:
- Schema: 0-25 points (5 per frontmatter field).
- Instructions: 0-75 points (length 10, autonomous 5, input 10, phases 15, output 10, guardrails 10, next steps 5, actionability 10).
- Total: 0-100 points.

============================================================
PHASE 4: CROSS-REGISTRY CHECKS
============================================================

1. **Duplicate Names**: No two skills across any category should share the same `name`.
   Flag duplicates with their paths.

2. **Cross-References**: Scan all skills for references to other skills (pattern: `/skill-name`).
   For each reference, verify the target skill exists in the registry.
   Flag broken references.

3. **Category Distribution**: Count skills per category. Flag categories with:
   - 0 skills (empty category directory with no skills).
   - 1 skill (underdeveloped category).
   - 15+ skills (potentially needs subcategories).

4. **Version Consistency**: Flag skills still at version "0.x.x" (should be >= 1.0.0).
   Flag skills with unusually high versions (> 10.0.0) — may indicate version inflation.

5. **Description Uniqueness**: Flag skills with near-identical descriptions (> 80% similarity).

============================================================
PHASE 5: README VALIDATION
============================================================

For each category directory, check for `README.md`:

1. **Existence**: Does `category/README.md` exist?
2. **Skill Listing**: Does it list ALL skills in the category?
   Compare README skill list against discovered SKILL.md files.
   Flag: skills in directory but missing from README, skills in README but not in directory.
3. **Format**: Does the README follow a consistent format?
   Expected: category description, skill table (name, description, version), usage examples.

Check the root `README.md`:
1. Does it list all categories?
2. Does it show the total skill count?
3. Is the count accurate?

If `--fix` is specified:
- Create missing category READMEs with a standard template.
- Update existing READMEs to include missing skills.
- Update root README skill count.

============================================================
PHASE 6: FIXES (only with --fix flag)
============================================================

If `--fix` was specified, apply auto-corrections:

1. **Missing Category READMEs**: Generate from template:
   ```markdown
   # [Category Name]

   [Category description]

   ## Skills

   | Skill | Description | Version |
   |-------|-------------|---------|
   | [name] | [description] | [version] |
   ```

2. **Outdated README Skill Lists**: Add missing skills, remove deleted skills.

3. **Root README Count**: Update the total skill count.

4. **Category Mismatch**: If a skill's `category` frontmatter does not match its
   directory, update the frontmatter (directory is the source of truth).

5. **Name Mismatch**: If a skill's `name` frontmatter does not match its directory
   name, update the frontmatter (directory name is the source of truth).

Do NOT auto-fix: descriptions, versions, instruction content, or structural issues.
Those require human judgment.


============================================================
SELF-HEALING VALIDATION (max 2 iterations)
============================================================

After producing output, validate data quality and completeness:

1. Verify the analysis consumed sufficient data.
2. Verify all output sections have substantive content (not just headers).
3. Verify recommendations are actionable and reference specific evidence.

IF VALIDATION FAILS:
- Identify data gaps and attempt alternative data sources
- Re-generate incomplete sections with expanded analysis
- Repeat up to 2 iterations

============================================================
OUTPUT
============================================================

## Registry Health Report

### Summary
| Metric | Value |
|--------|-------|
| Total categories | [N] |
| Total skills | [N] |
| Average quality score | [X/100] |
| Skills passing (>= 60) | [N] ([%]) |
| Skills needing work (40-59) | [N] ([%]) |
| Skills failing (< 40) | [N] ([%]) |
| Validation errors | [N] |
| Validation warnings | [N] |

### Per-Category Breakdown
| Category | Skills | Avg Score | Errors | Warnings |
|----------|--------|-----------|--------|----------|
| build | [N] | [X] | [N] | [N] |
| meta | [N] | [X] | [N] | [N] |
| ... | | | | |

### All Skills
| Skill | Category | Version | Score | Verdict |
|-------|----------|---------|-------|---------|
| [name] | [cat] | [ver] | [X/100] | [PASS/WARN/FAIL] |

### Validation Errors (must fix)
| # | Skill | Issue |
|---|-------|-------|

### Validation Warnings (should fix)
| # | Skill | Issue |
|---|-------|-------|

### Cross-Reference Check
| Skill | References | Broken References |
|-------|-----------|-------------------|

### README Status
| Location | Status | Issues |
|----------|--------|--------|
| Root README.md | [current/outdated/missing] | [details] |
| build/README.md | [current/outdated/missing] | [details] |
| ... | | |

### Fixes Applied (if --fix was specified)
| # | Fix | File |
|---|-----|------|

DO NOT:
- Modify SKILL.md instruction content. Only fix frontmatter mismatches and READMEs.
- Delete any files. Only create or update.
- Change version numbers. Versions are the skill author's responsibility.
- Fix structural issues in instructions (missing phases, weak guardrails). Flag them only.
- Run without scanning ALL categories. A partial scan produces misleading metrics.

NEXT STEPS:

After sync:
- "Fix skills with FAIL verdict using the issues listed in the report."
- "Run `/skill-test [skill-name]` for a deep analysis of specific failing skills."
- "Run `/skill-creator` to create skills for underdeveloped categories."
- "Commit updated READMEs: `git add */README.md README.md`."


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /registry-sync — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
