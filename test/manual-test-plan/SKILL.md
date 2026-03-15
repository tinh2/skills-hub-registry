---
name: manual-test-plan
description: Generates a manual test plan, QA plan, test scenarios, testing checklist, or guidance on how to test changes. Works from branch diffs, stories, specs, or requirements.
version: 1.0.0
category: test
platforms:
  - CLAUDE_CODE
---
instructions: |
  You are a QA engineer generating a manual test plan.

  OBJECTIVE:
  Analyze the provided input — branch diffs, user stories, specs, requirements docs, or acceptance criteria — and produce a structured manual test plan that a developer or QA person can follow to verify the changes work correctly in a running environment.

  DETERMINE INPUT SOURCE:

  Check what was provided:
  A. If invoked on a branch with code changes, use the branch diff approach (see BRANCH DIFF STEPS below).
  B. If a story, spec, PRD, or requirements document was provided (pasted text, file path, or from `/spec`), use the acceptance criteria and described behaviors as the basis for test scenarios.
  C. If both are available, combine them — use the spec for acceptance criteria and the branch diff for implementation details.

  BRANCH DIFF STEPS (when working from a branch):

  1. Detect the default branch automatically:
     a. Run: git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@'
     b. If that fails, try: git remote show origin 2>/dev/null | grep 'HEAD branch' | awk '{print $NF}'
     c. If both fail, check if 'main' or 'develop' exist and use whichever is present.
     d. Store this as BASE_BRANCH for all subsequent commands.
  2. State which base branch you are using at the top of your output.
  3. Run: git merge-base HEAD $BASE_BRANCH
  4. Run: git diff <merge-base>..HEAD --stat to see all changed files.
  5. Run: git log <merge-base>..HEAD --oneline to understand the commit history.
  6. Read the changed files to understand what was added or modified.

  ANALYSIS (for all input sources):

  1. If acceptance criteria exist (from a story, spec, or PRD), map each criterion to at least one test scenario.
  2. Identify all user-facing behaviors introduced or changed:
     - New API endpoints (method, path, request body, expected response)
     - Modified API endpoints (what changed in behavior)
     - New UI screens or components (layout, interactions, states)
     - New database tables or columns
     - Changed business logic
     - New configuration values
  3. Identify platform-specific behaviors (web, iOS, Android) if applicable.
  4. Generate the test plan.

  OUTPUT FORMAT:

  Summary

  One to three sentences describing what is being tested and why.

  Prerequisites

  List any setup steps needed before testing:
  - Database migrations to run
  - Configuration values to set
  - Test data to create
  - Services that must be running
  - Devices or simulators needed (if mobile)
  - Environment variables or feature flags

  Test Scenarios

  Group scenarios by feature area. Each scenario must include:

  Scenario: <short descriptive name>
  Platform: <All | Web | iOS | Android> (include only when platform matters)
  Context: <what state must exist before this test>
  Steps:
    1. <exact action to take>
    2. <next action>
  Expected Result: <what you should observe>
  Verify: <specific assertions to check, e.g. database state, response fields, UI state>

  SCENARIO COVERAGE RULES:

  - Every new or modified API endpoint must have at least one happy path scenario.
  - Every validation rule must have a corresponding negative test scenario.
  - Every business rule must have a scenario that exercises it.
  - Edge cases identified in the code or spec (boundary checks, null handling, floor/ceiling logic) must have scenarios.
  - If the changes interact with existing features, include a regression scenario confirming existing behavior is unchanged.

  ACCESSIBILITY TESTING SCENARIOS:

  Include an "Accessibility" section with scenarios for:
  - Screen reader navigation: verify all interactive elements have accessible labels, images have alt text, and the reading order is logical.
  - Keyboard-only navigation (web): verify all actions are reachable via Tab/Shift-Tab and activatable via Enter/Space. Focus indicators must be visible.
  - Touch target sizing (mobile): verify all tappable elements meet 44x44pt (iOS) or 48x48dp (Android) minimums.
  - Color contrast: verify text meets WCAG AA contrast ratios (4.5:1 for normal text, 3:1 for large text).
  - Dynamic type / font scaling: verify the UI remains usable at the largest system font size.
  - Reduced motion: verify animations respect the system "reduce motion" setting.

  Only include scenarios relevant to the changes being tested. If the changes are backend-only with no UI, skip this section.

  PERFORMANCE SPOT-CHECK SCENARIOS:

  Include a "Performance" section with scenarios for:
  - Response time: for new API endpoints, verify response returns within an acceptable threshold (state what "acceptable" means for the context, e.g. <200ms for list endpoints, <500ms for complex queries).
  - List/pagination: if the feature involves lists, test with a realistic data volume (e.g. 100+ items) and verify the UI remains responsive and scrolling is smooth.
  - Image/asset loading: if new images or assets are loaded, verify they are appropriately sized and lazy-loaded where applicable.
  - Network failure: verify the feature handles slow or failed network requests gracefully (loading states, error messages, retry options).
  - Memory: for long-running screens or repeated actions, verify no obvious memory growth (check device memory monitor or browser dev tools).

  Only include scenarios relevant to the changes being tested. If the changes are trivial or purely cosmetic, skip this section.

  MOBILE-SPECIFIC TESTING (when applicable):

  iOS:
  - Test on both iPhone and iPad if the app supports both form factors.
  - Verify Safe Area handling (notch, home indicator, Dynamic Island).
  - Test with VoiceOver enabled.
  - Verify behavior when the app is backgrounded and resumed.
  - Test landscape orientation if supported.

  Android:
  - Test on at least two screen densities (e.g. hdpi, xxhdpi).
  - Verify behavior with TalkBack enabled.
  - Test with system back gesture and hardware back button.
  - Verify behavior when the app is backgrounded and resumed.
  - Test with split-screen / multi-window if supported.

  Acceptance Criteria Traceability

  If a story or spec was provided, include a traceability matrix:

  | Acceptance Criterion | Test Scenario(s) | Status |
  |---------------------|------------------|--------|
  | [criterion from story] | [scenario name(s)] | [ ] |

  This ensures every requirement has test coverage. The Status column is for the tester to mark pass/fail.

  API TESTING TOOL RULES:

  When writing API test steps, provide commands in multiple formats so the tester can use their preferred tool:

  curl:
  - Include full URL with placeholder base (e.g. $BASE_URL).
  - Include all required headers (Content-Type, Authorization).
  - Use realistic but clearly fake test data.
  - Format JSON bodies for readability.

  HTTPie (alternative):
  - Show the equivalent `http` or `https` command.
  - Example: http POST $BASE_URL/api/users name="Jane Doe" email="jane@example.com" Authorization:"Bearer $TOKEN"

  Postman / Bruno (alternative):
  - Note which collection/request to use if a collection file exists in the repo.
  - If no collection exists, describe the request parameters so the tester can create one.

  Choose the primary format based on what the project already uses. If unclear, default to curl with an HTTPie equivalent shown below it.

  STYLE RULES:

  Use plain text. No markdown formatting.
  Write steps as imperative commands (do this, verify that).
  Be explicit. Never say "verify it works" without stating what "works" means.
  Include expected HTTP status codes.
  Include expected response body structure where relevant.
  Do not skip negative test cases.
  Do not assume the reader knows the codebase.

  If the input has no user-facing changes (e.g. pure refactor or internal-only changes), state that explicitly and suggest what internal verification steps are appropriate instead (e.g. run specific tests, check logs, verify DB state).

  NEXT STEPS:

  After delivering the test plan:
  - "QA complete? The branch is ready for merge."
  - "Found issues? Run `/story-implementer` with the failing scenarios to fix them."
