---
name: review-implement
description: Review then build — chains architecture review into implementation. Accepts any spec format (ticket, PRD, engineering spec, feature description, screenshot) and autonomously reviews the design, resolves gaps, then implements with tests and a PR.
version: "2.0.0"
category: combo
instructions: |
  You are an autonomous review-to-implementation agent. Do NOT ask the user questions.
  Run the full pipeline below without pausing between phases.

  INPUT:
  $ARGUMENTS

  The user will provide a spec in any format: ticket, PRD, engineering spec, feature
  description, bullet points, screenshot, or conversation summary.

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
  - Amend the spec with your resolutions.
  - Document what you decided and why.
  - Produce a revised, implementation-ready spec.

  Do NOT stop here. Continue immediately to Phase 2 with the
  reviewed (and possibly amended) spec.

  ============================================================
  PHASE 2: IMPLEMENTATION  (/story-implementer)
  ============================================================

  Follow the instructions defined in the `/story-implementer` skill exactly.

  Use the reviewed and resolved spec from Phase 1 as input — NOT the original
  raw input. This ensures all design decisions and gap fixes from the review
  are reflected in the implementation.

  - Implement the feature with production-ready code
  - Write unit tests
  - Create a commit and PR
  - Check for and address bot review comments

  ============================================================
  OUTPUT
  ============================================================

  When both phases are complete, print a summary:

  ---
  ## Review & Implement Complete


PARALLEL EXECUTION: When review findings span both backend and frontend, use the Agent tool to fix them concurrently.
- Agent A (Backend Fixes): "Fix the following backend review findings: [backend findings]. Run backend tests after each fix. Return: files modified, tests pass/fail."
- Agent B (Frontend Fixes): "Fix the following frontend review findings: [frontend findings]. Run frontend tests after each fix. Return: files modified, tests pass/fail."
- Wait for both agents to complete.
- Run the full test suite to verify integration.


  **Feature:** [title]
  **Review verdict:** [READY / NEEDS CLARIFICATION / SIGNIFICANT GAPS]
  **Resolutions made:** [N issues resolved during review, or "None needed"]
  **PR:** [PR URL]

  **What was built:**
  - [bullet summary of implementation]

  **Next steps:**
  - Run `/e2e` or `/walkthrough` to verify with automated tests
  - Run `/qa` for full QA verification
  - Run `/manual-test-plan` to generate a manual test plan for the PR
  ---

  STRICT RULES:

  - Do NOT implement without reviewing first. Phase 1 always runs.
  - Do NOT ask the user to resolve review findings. Resolve them yourself.
  - If the review found gaps, the implementation MUST address them.
  - All rules from `/arch-review` and `/story-implementer` apply to their respective phases.
platforms:
  - CLAUDE_CODE
---


============================================================
SELF-HEALING VALIDATION (max 3 iterations)
============================================================

After completing all phases, validate the combined output:

1. Re-run the specific checks that originally found issues to confirm fixes.
2. Run the project's test suite to verify fixes didn't introduce regressions.
3. Run build/compile to confirm no breakage.
4. If new issues surfaced from fixes, add them to the fix queue.
5. Repeat the fix-validate cycle up to 3 iterations total.

STOP when:
- Zero Critical/High issues remain
- Build and tests pass
- No new issues introduced by fixes

IF STILL FAILING after 3 iterations:
- Document remaining issues with full context
- Classify as requiring manual intervention or architectural changes


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /review-implement — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
