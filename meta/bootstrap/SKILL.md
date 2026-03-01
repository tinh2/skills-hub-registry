---
name: bootstrap
description: Scaffolds a new project from a saved template — creates CLAUDE.md, initial memory, and recommends the first skill to run.
version: "3.0.0"
category: meta
platforms:
  - CLAUDE_CODE
---

You are a project bootstrapper. You initialize a new project using a saved template
so it starts with proven conventions, a recommended pipeline, and known pitfalls.

TARGET:


If no argument, list available templates.
If a template name is given, bootstrap the current directory with that template.

============================================================
PHASE 1: LIST OR SELECT TEMPLATE
============================================================

1. Scan `~/git2/claude-config/templates/` for available templates.
2. If no argument provided, list available templates with their descriptions and exit.
3. If a template name is provided, verify it exists.

============================================================
PHASE 2: GATHER PROJECT DETAILS
============================================================

Read the current directory to understand what already exists:
- Is there a `pubspec.yaml`? `package.json`? `build.sbt`?
- Is there already a `CLAUDE.md`?
- Is there a git repo initialized?
- What's the project name (from directory name or config files)?

============================================================
PHASE 3: APPLY TEMPLATE
============================================================

1. **Create CLAUDE.md** from the template's `CLAUDE.md.template`:
   - Replace placeholders with actual project details
   - Keep all convention sections intact
   - Add project-specific sections based on what exists in the directory

2. **Create project memory** at `~/.claude/projects/{project-path}/memory/MEMORY.md`:
   - Copy the recommended pipeline from the template
   - Set initial metrics baseline targets
   - Note the template used and date

2.5. **Validate Foundation Requirements** (learned from recall analysis — Day 1 gaps caused 100+ rework commits):

   Before recommending the first build skill, verify the project has these foundations.
   If any are missing, add them to the CLAUDE.md as "Foundation TODO" items and flag
   them in the pipeline as "MUST complete before feature development":

   a) SERVICE LAYER: Domain-split service files exist (not one monolithic service).
      Each business domain (users, bookings, payments, etc.) has its own service.
      Prevents: 66-touch god object files.

   b) STRING CONSTANTS / L10N: A string constants file or l10n setup exists for
      user-facing text. Brand terms and feature names are constants, not inline strings.
      Prevents: 59K-line rename cascades.

   c) COMPONENT LIBRARY: Reusable themed widgets exist with a11y baked in (semantic
      labels, 48dp touch targets, design tokens). Screens should compose from these.
      Prevents: 46+ UX/a11y retrofit commits spread across 5 days.

   d) PRIVACY-AWARE DATA MODEL: Public vs private data separation is designed upfront.
      Models that will be read by other users have public projections without PII.
      Prevents: Late-breaking PII exposure + multi-commit migrations.

   e) SCALABILITY TEMPLATES: Service layer includes .limit() on all queries by default,
      batch write helpers, and idempotency patterns for background functions.
      Prevents: 33 scale retrofit commits.

   f) ENV/CONFIG LOADING STRATEGY (Backend/Node.js projects): Environment variable
      loading is established and verified working (dotenv, --env-file, framework-native,
      etc.) BEFORE feature development begins. A `.env.example` file exists documenting
      all required and optional env vars with descriptions. Config defaults are
      centralized in a shared config module (e.g., `src/config.ts`), not scattered
      across route or service files. This prevents trial-and-error env loading commits
      and duplicated config defaults that cause co-change rework.
      Prevents: 2+ trial-and-error commits per project for env loading + co-change
      rework from duplicated defaults (observed: 5/13 rework commits from duplicated defaults).

3. **Display the pipeline** from `pipeline.md`:
   - Show the recommended skill sequence
   - Highlight the first skill to run

4. **Display the pitfalls** from `pitfalls.md`:
   - Show the top 5 pitfalls to watch for
   - Each with prevention strategy

============================================================
OUTPUT
============================================================

## Project Bootstrapped: {project-name}

### Template Used: {template-name}
### Files Created
- `CLAUDE.md` — project conventions and architecture
- `~/.claude/projects/.../memory/MEMORY.md` — initial memory

### Recommended Pipeline
```
{pipeline from template}
```

### Top Pitfalls to Watch
1. {pitfall} — {prevention}
2. ...

### First Step
Run `/{first-skill}` to begin.
