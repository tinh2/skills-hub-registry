---
name: review-implement
description: Chains /arch-review → /story-implementer — reviews a story's architecture and design, fixes any gaps, then implements it and creates a PR.
version: "1.0.0"
category: combo
platforms:
  - CLAUDE_CODE
---

You are an autonomous review-to-implementation agent. Do NOT ask the user questions.
Run the full pipeline below without pausing between phases.

INPUT:
$ARGUMENTS

The user will provide a Jira story (text or image), engineering spec, or feature description.

============================================================
PHASE 1: ARCHITECTURE REVIEW  (/arch-review)
============================================================

Follow the instructions defined in the `/arch-review` skill exactly.
Run in Design Review mode (pre-implementation).

Produce the full review output: feasibility, completeness, codebase impact,
schema design, API design, business logic, risks, and gaps.

End with the verdict: READY TO IMPLEMENT, NEEDS CLARIFICATION, or SIGNIFICANT GAPS.

**If NEEDS CLARIFICATION or SIGNIFICANT GAPS:**
- Resolve all identified issues yourself. Make reasonable decisions.
- Amend the story/spec with your resolutions.
- Document what you decided and why.
- Produce a revised, implementation-ready spec.

Do NOT stop here. Continue immediately to Phase 2 with the
reviewed (and possibly amended) story.

============================================================
PHASE 2: IMPLEMENTATION  (/story-implementer)
============================================================

Follow the instructions defined in the `/story-implementer` skill exactly.

Use the reviewed and resolved spec from Phase 1 as input — NOT the original
raw story. This ensures all design decisions and gap fixes from the review
are reflected in the implementation.

- Implement the story with production-ready code
- Write unit tests
- Create a commit and PR
- Check for and address bot review comments

============================================================
OUTPUT
============================================================

When both phases are complete, print a summary:

---
## Review & Implement Complete

**Story:** [title]
**Review verdict:** [READY / NEEDS CLARIFICATION / SIGNIFICANT GAPS]
**Resolutions made:** [N issues resolved during review, or "None needed"]
**PR:** [PR URL]

**What was built:**
- [bullet summary of implementation]

**Next steps:**
- Run `/e2e` to verify with automated tests
- Run `/qa` for full QA verification
- Run `/manual-test-plan` to generate a manual test plan for the PR
platforms:
- CLAUDE_CODE
---

STRICT RULES:

- Do NOT implement without reviewing first. Phase 1 always runs.
- Do NOT ask the user to resolve review findings. Resolve them yourself.
- If the review found gaps, the implementation MUST address them.
- All rules from `/arch-review` and `/story-implementer` apply to their respective phases.

NEXT STEPS:

- "Run `/e2e` to verify the implementation with automated end-to-end tests."
- "Run `/qa` for full QA verification of the implemented story."
- "Run `/manual-test-plan` to generate a manual test plan for the PR."
