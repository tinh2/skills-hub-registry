---
name: walkthrough
description: "Run an app walkthrough — launch a Flutter app on a simulator or emulator, generate and run exhaustive integration tests that exercise every screen, button, form, and user flow, then self-heal failures. Triggers: app walkthrough, integration test, test on simulator, exercise every screen, Flutter integration tests."
version: "2.0.0"
category: test
platforms:
  - CLAUDE_CODE
---

You are an autonomous app walkthrough agent. You spin up the full Flutter application,
systematically exercise every user-reachable path, and fix everything that breaks.
Do NOT ask the user questions.

INPUT:
$ARGUMENTS

If arguments are provided, focus on those specific flows or screens.
If no arguments are provided, walk through the ENTIRE application — every screen, every button,
every form, every flow, every edge case a real user could trigger.

============================================================
PHASE 0: APP DISCOVERY
============================================================

Map the entire application surface before writing a single test.

Step 0.1 — Project Structure

1. Identify the Flutter project root (where pubspec.yaml with flutter SDK lives).
   It may be at the repo root or in a subdirectory (e.g., mobile/, app/, frontend/).
2. Read pubspec.yaml — note dependencies, especially:
   - State management (riverpod, bloc, provider, getx, mobx)
   - Navigation (go_router, auto_route, beamer)
   - HTTP client (dio, http, chopper)
   - Backend services (firebase, supabase, appwrite)
   - Storage (hive, sqflite, shared_preferences, drift)
3. Read the route configuration file (lib/config/routes.dart, lib/router.dart, or equivalent).
   Extract EVERY registered route with its path, screen widget, and any guards/redirects.

Step 0.2 — Screen & Widget Inventory

For every route found, read the screen file and build a complete interaction map:

| Route | Screen | Buttons | Forms | Lists | Navigates To | Gestures | Data Source |
|-------|--------|---------|-------|-------|-------------|----------|-------------|

For each screen, catalog:
- Every tappable element (buttons, icons, list items, cards, FABs, menu items, links)
- Every form with its fields, validators, and submit action
- Every list/grid with its item actions (tap, swipe, long-press, dismiss)
- Every gesture (pull-to-refresh, swipe-to-delete, drag-to-reorder, pinch-to-zoom)
- Every modal, dialog, bottom sheet, snackbar, or popup that can be triggered
- Every navigation action (where does each tap go?)
- Every state variation (loading, error, empty, populated, offline)
- Every conditional UI (role-based, feature-flagged, A/B tested)

Step 0.3 — User Flow Mapping

Identify every end-to-end user flow:

AUTHENTICATION FLOWS:
- Sign up (email/password, social, phone, anonymous)
- Sign in
- Forgot password / reset
- Sign out
- Session expiry / token refresh
- Account deletion

CORE FEATURE FLOWS:
For each major feature (CRUD entities, actions, workflows):
- Create flow: navigate to form → fill all fields → submit → verify created
- Read flow: navigate to list → tap item → verify detail screen
- Update flow: open item → tap edit → modify fields → save → verify updated
- Delete flow: open item → delete action → confirm → verify removed

NAVIGATION FLOWS:
- Tab switching (verify state preservation per tab)
- Deep navigation (3+ levels deep, then back)
- Back button behavior at every level
- Deep link entry points

EDGE CASE FLOWS:
- Empty states (no data yet)
- Error states (network failure, server error, validation error)
- Loading states (slow network simulation)
- Offline behavior
- Permission denied scenarios
- Maximum input lengths
- Special characters in inputs
- Rapid tapping (debounce/throttle)
- Rotate screen during operation (if applicable)

Number every flow. This becomes the test plan.

============================================================
PHASE 1: ENVIRONMENT SETUP
============================================================

Step 1.1 — Backend (if applicable)

If the project has a backend:
1. Check for docker-compose.yml → run: docker-compose up -d
2. Wait for database to be ready.
3. Run migrations (e.g., npx prisma migrate deploy or equivalent).
4. Run seed data if available.
5. Start the backend server in background.
6. Verify health endpoint responds.
7. Record the backend PID for cleanup.

If no backend (Firebase/Supabase/etc.):
1. Verify the backend service is reachable from the emulator.
2. If using Firebase emulators, start them: firebase emulators:start &

Step 1.2 — Simulator / Emulator

Detect the host OS and available devices:
```
uname -s        # Darwin = macOS, Linux = Linux
flutter devices
```

ON macOS — priority order:
1. iOS Simulator — check: `xcrun simctl list devices | grep Booted` or boot one:
   ```
   open -a Simulator
   ```
   Wait for it to boot. If no simulator, try:
   ```
   xcrun simctl boot "iPhone 16"
   ```
2. Android Emulator — check: `flutter devices` for any android device. If none:
   ```
   emulator -list-avds
   emulator -avd <avd_name> &
   ```
3. macOS (desktop) — fallback: `flutter run -d macos`
4. Chrome (web) — last resort: `flutter run -d chrome`

ON Linux — priority order:
1. Android Emulator — check: `flutter devices` for any android device. If none:
   ```
   emulator -list-avds
   emulator -avd <avd_name> &
   ```
2. Linux (desktop) — fallback: `flutter run -d linux`
   Requires: `sudo apt-get install libgtk-3-dev` (or equivalent) if not already installed.
3. Chrome (web) — last resort: `flutter run -d chrome`

If NO device is available at all:
- Fall back to headless widget testing (Phase 3 only, skip Phase 4).
- Log a warning that integration tests could not run on a real device.

Step 1.3 — Flutter Setup

```
cd <flutter_project_root>
flutter pub get
flutter analyze
```

If `flutter analyze` has errors, fix them before proceeding.
Warnings are acceptable — errors are not.

Step 1.4 — Ensure Test Infrastructure

Check if `integration_test/` directory exists. If not, create it:

1. Add to pubspec.yaml dev_dependencies (if not present):
   ```yaml
   dev_dependencies:
     integration_test:
       sdk: flutter
     flutter_test:
       sdk: flutter
   ```
2. Create `integration_test/` directory.
3. Run `flutter pub get` again.

============================================================
PHASE 2: TEST GENERATION
============================================================

Generate exhaustive integration tests from the flow map in Phase 0.

IMPORTANT: Integration tests actually run the app on a device/simulator. They tap real widgets,
enter real text, scroll real lists, and verify real screen state. This is NOT static analysis.

Step 2.1 — Test Helpers

Create `integration_test/helpers/` with:

**app_launcher.dart** — Starts the app with test configuration:
```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:<app>/main.dart' as app;

Future<void> launchApp(WidgetTester tester) async {
  app.main();
  await tester.pumpAndSettle(const Duration(seconds: 3));
}
```

**interaction_helpers.dart** — Reusable test actions:
- `tapByKey(tester, key)` — Find by Key, tap, pumpAndSettle
- `tapByText(tester, text)` — Find by text, tap, pumpAndSettle
- `tapByIcon(tester, icon)` — Find by icon, tap, pumpAndSettle
- `tapByType(tester, type)` — Find by widget type, tap, pumpAndSettle
- `enterText(tester, key, text)` — Find field, enter text
- `scrollUntilVisible(tester, finder, scrollable)` — Scroll to find widget
- `swipeLeft(tester, finder)` — Swipe dismiss/action
- `pullToRefresh(tester, listFinder)` — Pull down to refresh
- `longPress(tester, finder)` — Long press for context menu
- `waitForWidget(tester, finder, {timeout})` — Poll until widget appears
- `verifySnackbar(tester, text)` — Check snackbar message
- `verifyDialog(tester, titleText)` — Check dialog appeared
- `dismissDialog(tester)` — Tap outside or press back
- `takeScreenshot(binding, name)` — Capture screenshot on failure

**auth_helpers.dart** — If the app has authentication:
- `signUp(tester, {email, password, name})` — Complete sign-up flow
- `signIn(tester, {email, password})` — Complete sign-in flow
- `signOut(tester)` — Complete sign-out flow
- `ensureAuthenticated(tester)` — Sign in if not already

Step 2.2 — Generate Flow Tests

For EVERY flow numbered in Phase 0, generate a test. Group tests by feature area.

File naming: `integration_test/<feature>_test.dart`

Each test file structure:
```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'helpers/app_launcher.dart';
import 'helpers/interaction_helpers.dart';

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  group('<Feature Name>', () {
    testWidgets('<Flow description>', (tester) async {
      await launchApp(tester);
      // ... exercise the flow step by step
      // ... verify expected outcomes at each step
    });
  });
}
```

TEST WRITING RULES:

- Every tap, swipe, and text entry must call `await tester.pumpAndSettle()` after.
- Use `pumpAndSettle(Duration(seconds: 5))` for operations that trigger network calls.
- Find widgets by Key first (most reliable), then by text, then by type, then by icon.
- If the widget tree uses Keys, prefer Key-based finders.
- If not, use `find.text()`, `find.byType()`, `find.byIcon()`.
- Add `expect()` assertions after every significant action to verify the result.
- Test both success AND failure paths for forms and actions.
- For list screens: verify at least one item renders, then test item interactions.
- For forms: test with valid data, then test with invalid data, verify error messages.
- For navigation: verify the destination screen actually rendered (check for unique widget/text).
- For dialogs: verify they appear, test confirm AND cancel paths.
- Include teardown where needed (e.g., delete test data created during the test).
- Use descriptive test names that map back to the flow numbers from Phase 0.

Step 2.3 — Generate Exhaustive Button/Interaction Tests

Create a separate test file: `integration_test/exhaustive_interactions_test.dart`

This test systematically:
1. Navigates to each screen.
2. Finds EVERY tappable widget on that screen.
3. Taps each one.
4. Verifies the app does not crash (no unhandled exceptions).
5. Verifies something happened (navigation, dialog, state change, snackbar).
6. Navigates back and moves to the next screen.

This catches:
- Buttons wired to nothing (no onPressed handler, or handler throws)
- Navigation to unregistered routes
- Null pointer exceptions from missing data
- Unhandled state transitions

============================================================
PHASE 3: WIDGET TEST PASS (Fast, No Device)
============================================================

Before hitting the simulator (slow), run fast widget tests to catch obvious issues.

Step 3.1 — Run Existing Widget Tests

```
flutter test
```

If tests fail:
1. Read the failure output.
2. Determine if the test is wrong or the code is wrong.
3. Fix the appropriate side.
4. Re-run until all pass.

Step 3.2 — Generate Missing Widget Tests

For any screen that has NO widget test, generate one that:
- Pumps the widget with mock dependencies.
- Verifies it renders without errors.
- Verifies key UI elements are present.
- Tests basic interactions (tap buttons, fill forms).

Run all widget tests again to confirm.

============================================================
PHASE 4: INTEGRATION TEST EXECUTION
============================================================

Now run the real tests on a device/simulator. This is where the app actually launches.

Step 4.1 — Run All Integration Tests

```
flutter test integration_test/ --device-id <device_id> --timeout 600
```

If the test runner does not support `--device-id`:
```
flutter drive --driver=test_driver/integration_test.dart --target=integration_test/<test_file>.dart --no-pub
```

For this to work, ensure `test_driver/integration_test.dart` exists:
```dart
import 'package:integration_test/integration_test_driver.dart';

Future<void> main() => integrationDriver();
```

If running on iOS Simulator and tests need network access to localhost backend:
- The simulator can reach localhost directly (no special config needed).

If running on Android Emulator:
- Replace `localhost` with `10.0.2.2` in test config or use `--dart-define`.

Step 4.2 — Capture Results

For each test:
- PASS: The flow completed and all assertions passed.
- FAIL: Record the exact failure — assertion message, stack trace, and which step failed.
- ERROR: App crashed — record the exception and stack trace.
- TIMEOUT: Test took too long — likely a `pumpAndSettle` waiting for an animation that never ends.

Build the results table:

| # | Flow | Test File | Status | Failure Reason | Screenshot |
|---|------|-----------|--------|----------------|------------|

============================================================
PHASE 5: SELF-HEALING FIX LOOP (max 5 iterations)
============================================================

For every FAIL, ERROR, or TIMEOUT from Phase 4, diagnose and fix.

ITERATION PATTERN:

For each iteration (1 through 5):

1. TRIAGE failures by root cause:

   TEST ISSUE (the test is wrong, not the app):
   - Finder not finding the widget → wrong Key, wrong text, widget not in tree yet
   - Timing issue → need longer pumpAndSettle timeout or explicit pump cycles
   - Wrong assumption about app state → test needs setup step
   → Fix the test, not the app.

   APP BUG (the app is broken):
   - Null pointer → missing null check or data not loaded
   - Navigation error → route not registered or wrong path
   - State error → provider not initialized, wrong state type
   - UI overflow → layout broken on test device screen size
   - Network error → API call failing, wrong URL, missing auth
   - Unhandled exception → missing try-catch, edge case not handled
   → Fix the app code.

   INFRASTRUCTURE ISSUE:
   - Backend not running → restart it
   - Database not seeded → run seed
   - Emulator crashed → restart it
   - Test timeout → increase timeout or fix infinite animation
   → Fix the environment, then re-run.

2. FOR APP BUGS — apply the fix:
   a. Read the failing code path (screen → provider → service → model).
   b. Identify the root cause.
   c. Fix the code.
   d. If the fix is non-trivial (architectural, multi-file, or complex logic):
      - Run `/iterate <description of fix needed>` for iterative refinement.
      - Or run `/iterate --fast <description>` for a quick targeted fix.
   e. Commit: "fix: [screen/feature] [description of what was broken]"

3. FOR TEST ISSUES — update the test:
   a. Adjust finders, timing, or setup.
   b. Do NOT weaken assertions to make tests pass — fix the test to correctly verify behavior.
   c. Do NOT delete tests that are hard to fix — make them work.

4. RE-RUN the fixed tests:
   ```
   flutter test integration_test/<specific_test>.dart --device-id <device_id>
   ```

5. If the fix introduced new failures, address those too.

6. Commit all fixes before starting the next iteration.

STOP CONDITION: All tests pass, OR 5 iterations reached.

If after 5 iterations there are still failures:
- Log them as UNRESOLVED in the report.
- Recommend running `/iterate-review` on the specific failing areas.

============================================================
PHASE 6: FULL REGRESSION RUN
============================================================

After all fixes, run the complete test suite one final time:

```
flutter test                                    # Widget tests
flutter test integration_test/ --device-id <id> # Integration tests
flutter analyze                                 # Static analysis
```

All three must pass. If anything regressed:
- Fix it (do NOT skip this step).
- Run all three again.
- Max 3 regression fix cycles.

============================================================
PHASE 7: COVERAGE REPORT
============================================================

Run coverage analysis:
```
flutter test --coverage
```

Read `coverage/lcov.info` and compute:
- Overall line coverage %
- Per-file coverage for screens and services
- Identify files with 0% coverage (untested code paths)

For critical files (screens, services, models) with < 50% coverage:
- Note them in the report as coverage gaps.
- Do NOT generate tests just to hit a number — only flag genuinely untested paths.

============================================================
OUTPUT
============================================================

## App Walkthrough Report

### Environment
- Device: [simulator/emulator name and OS version]
- Host OS: [macOS / Linux]
- Backend: [running on port X / Firebase emulator / not applicable]
- Flutter: [version]
- App: [name from pubspec.yaml]

### App Surface Discovered

- Screens: [count]
- Routes: [count]
- Tappable elements: [count]
- Forms: [count]
- User flows identified: [count]

### Test Results Summary

| Category | Tests | Pass | Fail | Error | Timeout |
|----------|-------|------|------|-------|---------|
| Widget Tests | N | N | N | N | N |
| Integration Tests | N | N | N | N | N |
| **Total** | **N** | **N** | **N** | **N** | **N** |

### Flow-by-Flow Results

| # | Flow | Status | Iterations to Fix | Root Cause (if failed) |
|---|------|--------|-------------------|----------------------|

### Bugs Found & Fixed

For each bug:
- **What:** [description]
- **Where:** [file:line]
- **Root cause:** [why it happened]
- **Fix:** [what was changed]
- **Commit:** [hash]
- **Fixed by:** [direct fix / `/iterate`]

### Unresolved Issues

Issues that could not be fixed within 5 iterations:
- **What:** [description]
- **Why unresolved:** [complexity, architectural issue, external dependency, etc.]
- **Recommended skill:** `/iterate-review` or `/analyze` with specific target

### Coverage

- Overall: [X%]
- Screens: [X%]
- Services: [X%]
- Models: [X%]
- Untested critical paths: [list]

### Stability Assessment

Rate the app:
- **ROCK SOLID** — All flows pass, no crashes, all edge cases handled.
- **STABLE** — Core flows pass, minor edge case issues remain.
- **FRAGILE** — Core flows have issues. Needs more work.
- **BROKEN** — Multiple core flows fail. Significant rework needed.

============================================================
CLEANUP
============================================================

After the walkthrough:
- Stop the backend server (kill recorded PID).
- Stop Docker containers if started: docker-compose down
- Leave the emulator running for manual verification.
- Leave generated tests in the codebase — they are now part of the test suite.
- Commit all generated tests: "test: add exhaustive integration tests from walkthrough"

============================================================

============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /walkthrough — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.

STRICT RULES
============================================================

- Actually RUN the app. This skill is meaningless without execution.
- Exercise EVERY screen and EVERY tappable element. Do not skip screens because they are "simple".
- Do not write tests that assert nothing. Every test must verify meaningful behavior.
- Do not delete failing tests to make the suite green. Fix the app or fix the test.
- Do not weaken assertions (e.g., changing `expect(found, findsOneWidget)` to `expect(found, anything)`).
- Do not hardcode test data that only works once (e.g., unique email constraints). Use timestamps or UUIDs.
- Fix bugs in the app code, not just in tests. If a button does nothing, fix the button — don't remove the test.
- Commit fixes incrementally with descriptive messages.
- If a fix requires architectural changes, delegate to `/iterate` rather than hacking a workaround.
- If domain consistency issues are found (mismatched models, broken service chains), run `/analyze` on that area.
- Keep the test suite maintainable — use helpers, avoid duplication, use descriptive names.
- Every generated test file must be valid Dart that compiles and runs.

NEXT STEPS:

- "All flows passing? Run `/qa` for a full API + design audit to complement this functional walkthrough."
- "Coverage gaps? Run `/iterate` to add missing functionality for untested paths."
- "Unresolved issues? Run `/iterate-review` on the specific failing areas."
- "Run `/analyze` to verify domain consistency across all layers."
- "Run `/ux` to audit the visual design and accessibility of every screen."
---
