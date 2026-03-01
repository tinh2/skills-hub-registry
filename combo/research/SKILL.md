---
name: research
description: Chains /compete → /new-features — runs competitive gap analysis, saves the report, then synthesizes actionable feature ideas from all markdown findings in the folder.
version: "1.0.0"
category: combo
platforms:
  - CLAUDE_CODE
---

You are an autonomous research-to-ideation agent. Do NOT ask the user questions.
Run the full pipeline below without pausing between phases.

TARGET:
$ARGUMENTS

============================================================
PHASE 1: COMPETITIVE GAP ANALYSIS  (/compete)
============================================================

Follow the instructions defined in the `/compete` skill exactly.
Produce the full Competitive Gap Analysis output including all sections
(Product Identity, Competitive Landscape, Feature Matrix, Critical Gaps,
Strategic Gaps, Differentiators, Our Edges, Industry Trends, Recommended Roadmap, Summary).

Save the report to `docs/competitive-gap-analysis.md`
as specified by the `/compete` skill (create the `docs/` directory if it doesn't exist).

Do NOT stop here. Continue immediately to Phase 2.

============================================================
PHASE 2: FEATURE IDEATION  (/new-features)
============================================================

Now follow the instructions defined in the `/new-features` skill exactly.

Read ALL `.md` files in the `docs/` directory — this includes
the `docs/competitive-gap-analysis.md` you just wrote plus any other markdown
files that already existed in the folder.

Extract learnings from every file, synthesize feature ideas, and write
the report to `docs/NewFeatures-X.md` (where X is a 3-word kebab-case theme).

IMPORTANT: Features should heavily draw from the competitive gap analysis
just produced. Critical gaps and strategic gaps from Phase 1 should become
HIGH priority features. Differentiator opportunities should become MEDIUM.

============================================================
OUTPUT
============================================================

When both phases are complete, print a summary:

---
## Research Complete

**Files generated:**
1. `docs/competitive-gap-analysis.md` — Full competitive landscape + gap analysis
2. `docs/NewFeatures-[X].md` — Actionable feature ideas derived from findings

**Key stats:**
- Competitors analyzed: [N]
- Total gaps found: [N]
- Feature ideas generated: [N] (HIGH: [N], MEDIUM: [N], LOW: [N])

**Next steps:**
- Run `/backend-spec [feature name]` to generate implementation stories
- Run `/iterate` or `/ship` to start building a feature
- Run `/arch-review` to assess architecture readiness for the proposed features
platforms:
- CLAUDE_CODE
---

STRICT RULES:

- Do NOT skip Phase 1 and go straight to Phase 2.
- Do NOT ask the user for input between phases.
- Phase 2 MUST read the file written by Phase 1 — that's the whole point of the chain.
- All rules from `/compete` and `/new-features` apply to their respective phases.

NEXT STEPS:

- "Run `/backend-spec` to generate implementation stories from the features identified."
- "Run `/arch-review` to assess architecture readiness for the proposed features."
