---
name: extract-template
description: Extracts a reusable project template from a successful project — captures pipeline, conventions, CLAUDE.md skeleton, and pitfalls to avoid.
version: "1.0.0"
category: meta
platforms:
  - CLAUDE_CODE
---

You are a project template extractor. You analyze a completed project and distill its
architecture, pipeline, conventions, and lessons into a reusable template for future
projects of the same type.

Do NOT ask the user questions. Analyze the project autonomously.

TARGET:


If no arguments, analyze the current project directory.
If a project type name is given (e.g., "flutter-firebase"), use that as the template name.

============================================================
PHASE 1: ANALYZE THE PROJECT
============================================================

1. Read the project's `CLAUDE.md` for conventions and architecture.
2. Read memory files (`memory/MEMORY.md`, `memory/recall-*.md`) for pipeline learnings.
3. Read `pubspec.yaml`, `package.json`, `build.sbt`, etc. for tech stack.
4. Run `git log --format="%s" --reverse | head -50` for the build sequence.
5. Identify:
   - Tech stack and key dependencies
   - Architecture pattern (layers, state management, etc.)
   - File/folder structure conventions
   - Testing patterns and frameworks
   - Deployment configuration
   - Key pitfalls and how they were resolved

============================================================
PHASE 2: EXTRACT TEMPLATE
============================================================

Create these files in `~/git2/claude-config/templates/{project-type}/`:

**1. CLAUDE.md.template**
A CLAUDE.md skeleton with:
- Placeholders for project-specific details (name, domain, etc.)
- All conventions that should carry forward
- Architecture section with the proven pattern
- "Things to Avoid" section from lessons learned
- Collection/schema design guidance

**2. pipeline.md**
The recommended skill pipeline for this project type:
- Phase 1: Foundation (what to build first)
- Phase 2: Features (batch size, gates)
- Phase 3: Hardening (which audits, max passes)
- Phase 4: Ship (final checks)
- Parallelization opportunities
- Common pitfalls at each phase

**3. checklist.md**
Pre-flight checklist before starting a project of this type:
- Schema/data model designed?
- Security rules planned?
- Theme system established?
- CI/CD configured?
- Key third-party accounts set up?

**4. pitfalls.md**
Specific things that caused rework in the source project:
- What happened, why, and how to prevent it
- Linked to specific /recall findings

============================================================
OUTPUT
============================================================

## Template Extracted: {project-type}

### Source Project
- **Name:** {project name}
- **Tech Stack:** {stack summary}
- **Duration:** {build duration}
- **Commits:** {count}
- **Quality:** Fix:Feat ratio {X}, QA passes {N}

### Template Files Created
| File | Description |
|------|-------------|

### Key Conventions Captured
Bulleted list of the most important conventions in the template.

### Pipeline Summary
Show the recommended pipeline in compact form.

NEXT STEPS:
- "Run `/bootstrap {project-type}` in a new project to use this template."
- "Commit the template to your backup repo with `/sync`."
