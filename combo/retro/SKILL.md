---
name: retro
description: Chains /recall → /new-features — reconstructs the dev cycle from git history, extracts patterns and insights, then synthesizes feature ideas from the learnings.
version: "1.0.0"
category: combo
platforms:
  - CLAUDE_CODE
---

You are an autonomous retrospective-to-ideation agent. Do NOT ask the user questions.
Run the full pipeline below without pausing between phases.

TARGET:
$ARGUMENTS

If arguments are provided, use them to scope the retrospective (branch name, date range, feature).
If no arguments are provided, analyze the full git history.

============================================================
PHASE 1: DEVELOPMENT RETROSPECTIVE  (/recall)
============================================================

Follow the instructions defined in the `/recall` skill exactly.

Produce the full retrospective output: Timeline Reconstruction, Pattern Extraction,
Dependency Mapping, and Insight Distillation.

Save the retrospective output to `docs/dev-retrospective.md` (create the `docs/` directory if it doesn't exist).

Key outputs to preserve for Phase 2:
- What caused rework (indicates areas needing better features/tooling)
- Where bottlenecks were (indicates areas needing improvement)
- Patterns of late discovery (indicates missing validation/features)
- Recommended improvements for the next cycle

Do NOT stop here. Continue immediately to Phase 2.

============================================================
PHASE 2: FEATURE IDEATION  (/new-features)
============================================================

Now follow the instructions defined in the `/new-features` skill exactly.

Read ALL `.md` files in the `docs/` directory — this includes
the `docs/dev-retrospective.md` you just wrote plus any other markdown files
that already existed in the folder.

Extract learnings from every file, synthesize feature ideas, and write
the report to `docs/NewFeatures-X.md` (where X is a 3-word kebab-case theme).

IMPORTANT: Features should directly address the pain points and
inefficiencies discovered in the retrospective:
- Rework hotspots → features that prevent those issues
- Bottlenecks → features that eliminate or reduce them
- Late discoveries → features that catch issues earlier
- Process gaps → features or tooling that fill them

============================================================
OUTPUT
============================================================

When both phases are complete, print a summary:

---
## Retro Complete

**Files generated:**
1. `docs/dev-retrospective.md` — Full development cycle analysis
2. `docs/NewFeatures-[X].md` — Feature ideas derived from retrospective learnings

**Key stats:**
- Commits analyzed: [N]
- Rework hotspots identified: [N]
- Feature ideas generated: [N] (HIGH: [N], MEDIUM: [N], LOW: [N])

**Top insight:** [single most impactful finding from the retrospective]

**Next steps:**
- Run `/backend-spec [feature name]` to generate implementation stories
- Run `/iterate` or `/ship` to start building a feature
- Run `/research` to validate features against competitors
platforms:
- CLAUDE_CODE
---

STRICT RULES:

- Do NOT skip Phase 1 and go straight to Phase 2.
- Do NOT ask the user for input between phases.
- Phase 1 MUST save its output to `docs/dev-retrospective.md` so Phase 2 can read it.
- Phase 2 MUST read the file written by Phase 1 from the `docs/` directory.
- All rules from `/recall` and `/new-features` apply to their respective phases.
