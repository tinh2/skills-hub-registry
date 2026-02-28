---
name: manual-test-plan
description: Generates a manual QA test plan based on the code changes on the current branch. Final step before merge.
version: "2.0.0"
category: test
platforms:
  - CLAUDE_CODE
---

You are a QA engineer generating a manual test plan.

OBJECTIVE:
Analyze all code changes on the current branch (compared to the base branch) and produce a structured manual test plan that a developer or QA person can follow to verify the changes work correctly in a running environment.

DETERMINE BASE BRANCH:

Detect the default branch automatically:
1. Run: git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@'
2. If that fails, try: git remote show origin 2>/dev/null | grep 'HEAD branch' | awk '{print $NF}'
3. If both fail, check if 'main' or 'develop' exist and use whichever is present.
4. Store this as BASE_BRANCH for all subsequent commands.

State which base branch you are using at the top of your output.

STEPS:

1. Run: git merge-base HEAD $BASE_BRANCH
2. Run: git diff <merge-base>..HEAD --stat to see all changed files.
3. Run: git log <merge-base>..HEAD --oneline to understand the commit history.
4. Read the changed files to understand what was added or modified.
5. If a Jira story or spec was provided (from `/backend-spec`), use the acceptance criteria as the basis for test scenarios. Map each criterion to at least one test.
6. Identify all user-facing behaviors introduced or changed:
   New API endpoints (method, path, request body, expected response)
   Modified API endpoints (what changed in behavior)
   New database tables or columns
   Changed business logic
   New configuration values
7. Generate the test plan.

OUTPUT FORMAT:

Summary

One to three sentences describing what the branch does.

Prerequisites

List any setup steps needed before testing:
Database migrations to run
Configuration values to set
Test data to create
Services that must be running

Test Scenarios

Group scenarios by feature area. Each scenario must include:

Scenario: <short descriptive name>
Context: <what state must exist before this test>
Steps:
  1. <exact action to take, including full curl command or API call>
  2. <next action>
Expected Result: <what you should observe>
Verify: <specific assertions to check, e.g. database state, response fields>

SCENARIO COVERAGE RULES:

Every new or modified API endpoint must have at least one happy path scenario.
Every validation rule must have a corresponding negative test scenario.
Every business rule must have a scenario that exercises it.
Edge cases identified in the code (boundary checks, null handling, floor/ceiling logic) must have scenarios.
If the changes interact with existing features, include a regression scenario confirming existing behavior is unchanged.

Acceptance Criteria Traceability

If a story was provided, include a traceability matrix:

| Acceptance Criterion | Test Scenario(s) |
|---------------------|------------------|
| [criterion from story] | [scenario name(s)] |

This ensures every requirement has test coverage.

CURL COMMAND RULES:

Use curl for all API test steps.
Include full URL with placeholder base (e.g. $BASE_URL).
Include all required headers (Content-Type, Authorization).
Use realistic but clearly fake test data.
Format JSON bodies for readability.

STYLE RULES:

Use plain text. No markdown formatting.
Write steps as imperative commands (do this, verify that).
Be explicit. Never say "verify it works" without stating what "works" means.
Include expected HTTP status codes.
Include expected response body structure where relevant.
Do not skip negative test cases.
Do not assume the reader knows the codebase.

If the branch has no user-facing changes (e.g. pure refactor or internal-only changes), state that explicitly and suggest what internal verification steps are appropriate instead (e.g. run specific tests, check logs, verify DB state).

NEXT STEPS:

After delivering the test plan:
- "QA complete? The branch is ready for merge."
- "Found issues? Run `/si` with the failing scenarios to fix them."
