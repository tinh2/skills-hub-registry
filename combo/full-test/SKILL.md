---
name: full-test
description: Chains /e2e → /manual-test-plan — runs exhaustive automated E2E tests with self-healing, then generates a manual test plan for remaining edge cases.
version: "1.0.0"
category: combo
platforms:
  - CLAUDE_CODE
---

You are an autonomous testing agent. Do NOT ask the user questions.
Run the full pipeline below without pausing between phases.

TARGET:
$ARGUMENTS

If arguments are provided, focus testing on those features/flows.
If no arguments are provided, test the entire application.

============================================================
PHASE 1: AUTOMATED E2E TESTS  (/e2e)
============================================================

Follow the instructions defined in the `/e2e` skill exactly.
Run all 9 phases: Stack Discovery → Environment Setup → Backend API Tests →
Frontend UI Tests → Integration Tests → Test Execution → Self-Healing Fix Loop →
Full Regression → Coverage Report.

Record the final test results and coverage report. Note which areas have
strong automated coverage and which areas are harder to test automatically
(complex user flows, visual regressions, edge cases requiring human judgment).

Do NOT stop here. Continue immediately to Phase 2.

============================================================
PHASE 2: MANUAL TEST PLAN  (/manual-test-plan)
============================================================

Follow the instructions defined in the `/manual-test-plan` skill exactly.

IMPORTANT: When generating the manual test plan, factor in the automated
test coverage from Phase 1:

- Do NOT duplicate scenarios that are already well-covered by automated tests.
- FOCUS manual test scenarios on:
  1. Areas where automated tests found bugs (verify fixes manually)
  2. Flows that are hard to automate (multi-step UX, visual layout, real device behavior)
  3. Edge cases the automated suite couldn't cover (network conditions, permissions, etc.)
  4. Exploratory testing suggestions for areas with low automated coverage
- Reference the automated test results: "Automated tests cover X; manually verify Y."

============================================================
OUTPUT
============================================================

When both phases are complete, print a summary:

---
## Full Test Pass Complete

**Automated E2E Results:**
- Tests run: [N]
- Passed: [N] | Failed: [N] | Fixed: [N]
- Quality verdict: [ROCK SOLID / STABLE / FRAGILE / BROKEN]

**Manual Test Plan:**
- Manual scenarios generated: [N]
- Focus areas: [list areas needing manual verification]

**Coverage assessment:**
- Strong automated coverage: [list areas]
- Needs manual verification: [list areas]
- Gaps (no coverage): [list areas, if any]

**Next steps:**
- Execute the manual test plan before merging
- Run `/polish` for UX audit + QA verification + domain analysis
- Run `/qa` for additional functional verification
platforms:
- CLAUDE_CODE
---

STRICT RULES:

- Do NOT skip Phase 1 and only generate a manual test plan.
- Do NOT duplicate automated test coverage in the manual plan.
- Phase 2 must reference Phase 1 results to produce a complementary (not redundant) plan.
- All rules from `/e2e` and `/manual-test-plan` apply to their respective phases.
