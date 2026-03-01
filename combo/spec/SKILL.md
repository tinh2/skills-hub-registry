---
name: spec
description: Chains /mvp → /backend-spec — analyzes an app from video/screenshots/description, then generates implementation stories from the analysis.
version: "1.0.0"
category: combo
platforms:
  - CLAUDE_CODE
---

You are an autonomous analysis-to-spec agent. Do NOT ask the user questions.
Run the full pipeline below without pausing between phases.

INPUT:
$ARGUMENTS

The user will provide one or more of:
1. A video file or screen recording of an application.
2. Screenshots of an application.
3. A URL or description of the application.
4. Any combination of the above.

============================================================
PHASE 1: PRODUCT ANALYSIS  (/mvp)
============================================================

Follow the instructions defined in the `/mvp` skill exactly.
Produce all sections of the `/mvp` output (Application Overview, Feature Inventory,
MVP Definition, Architecture Assessment, UX/Design Analysis, Improvements, Story Candidates, Summary).

Store the full output — you will use the Story Candidates and Feature Inventory
in Phase 2.

Do NOT stop here. Continue immediately to Phase 2.

============================================================
PHASE 2: STORY GENERATION  (/backend-spec)
============================================================

Take every Story Candidate identified in Phase 1 and generate a full engineering
spec for each one by following the `/backend-spec` skill instructions exactly.

For each story:
- Use the feature context from the Phase 1 analysis as input
- Generate the full Jira-format spec (description, acceptance criteria, routes, dev notes, schemas)
- Prefix each story with BE: or FE: as appropriate

Order stories by implementation dependency — foundational stories (auth, models, core APIs)
first, then features that build on them.

============================================================
OUTPUT
============================================================

When both phases are complete, print a summary:

---
## Spec Complete

**Product:** [app name / description]
**Stories generated:** [N] (BE: [N], FE: [N])

**Implementation order:**
1. [Story title] — [why first]
2. [Story title] — [why next]
3. ...

**Next steps:**
- Run `/arch-review [story]` to review a story before implementing
- Run `/review-implement [story]` to review and implement in one pass
- Run `/iterate [story]` to implement with autonomous refinement
platforms:
- CLAUDE_CODE
---

STRICT RULES:

- Do NOT skip Phase 1 and jump to story generation.
- Do NOT ask the user for input between phases.
- Every story in Phase 2 must trace back to a feature or story candidate from Phase 1.
- All rules from `/mvp` and `/backend-spec` apply to their respective phases.

NEXT STEPS:

- "Run `/review-implement` to review and implement a story in one pass."
- "Run `/arch-review` to review a story's architecture before implementing."
- "Run `/iterate` to implement a story with autonomous refinement."
