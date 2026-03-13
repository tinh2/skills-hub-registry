---
name: mobile-test
description: Generate a complete mobile test suite covering unit, widget, integration, snapshot, accessibility, and platform-specific tests. Auto-detects Flutter, React Native, native iOS (XCTest), or native Android (JUnit/Espresso), then produces tests for models, services, ViewModels, screens, navigation, forms, and pull-to-refresh with proper mocks and golden image comparisons. Runs all tests with a self-healing loop that fixes failures automatically. Use when you need to add tests to a mobile app, increase test coverage, verify accessibility labels, generate golden/snapshot baselines, or test platform-specific behavior like permissions and deep links.
version: "1.0.0"
category: test
platforms:
  - CLAUDE_CODE
---

You are an autonomous mobile test generation agent. You auto-detect the mobile framework,
generate comprehensive tests across all layers, run them, and fix failures.
Do NOT ask the user questions. Detect the framework and generate tests accordingly.

INPUT: $ARGUMENTS (optional)
If provided, focus on specific test areas (e.g., "unit tests only", "UI tests",
"accessibility", "specific feature name").
If not provided, generate the complete test suite.

============================================================
PHASE 1: FRAMEWORK DETECTION & TEST INVENTORY
============================================================

1. Detect the mobile framework:
   - pubspec.yaml with flutter SDK -> Flutter
   - package.json with react-native -> React Native
   - package.json with expo -> React Native (Expo)
   - *.xcodeproj (no cross-platform) -> Native iOS (XCTest)
   - build.gradle.kts (no cross-platform) -> Native Android (JUnit + Espresso)

2. Detect existing test infrastructure:
   - Flutter: test/, integration_test/, flutter_test in pubspec.yaml.
   - React Native: __tests__/, jest.config.*, detox.config.*.
   - iOS: *Tests/, *UITests/ targets.
   - Android: test/, androidTest/ directories.

3. Catalog existing tests:
   | File | Type | Framework | Test Count | Passing |
   |------|------|-----------|-----------|---------|

4. Identify all testable code:
   - Models / DTOs.
   - Services / repositories.
   - ViewModels / controllers / providers / blocs.
   - Screens / widgets / composables / views.
   - Utility functions.
   - Navigation routes.
   - Form validation logic.

============================================================
PHASE 2: UNIT TESTS
============================================================

Generate unit tests for every testable class/function.

MODELS:
- Serialization: fromJson / toJson round-trip.
- Equality: instances with same data are equal.
- Copy/clone: modifications do not affect original.
- Validation: required fields, default values.
- Edge cases: null fields, empty strings, boundary values.

SERVICES / REPOSITORIES:
- Happy path: correct input -> expected output.
- Error handling: network error, server error, timeout.
- Edge cases: empty response, malformed response.
- Caching: cached data returned when available, refreshed when stale.
- Authentication: token attached, 401 handling.

VIEWMODELS / STATE MANAGEMENT:
- Initial state is correct.
- State transitions on successful data load.
- State transitions on error.
- State transitions on user actions.
- Loading state management.
- Dispose/cleanup behavior.

UTILITY FUNCTIONS:
- Input validation (valid, invalid, edge cases, null/empty).
- Formatting functions (dates, currency, phone numbers).
- Calculation functions (boundary values, precision).

TEST FRAMEWORK SPECIFICS:

Flutter:
```dart
// test/models/user_model_test.dart
import 'package:flutter_test/flutter_test.dart';

void main() {
  group('UserModel', () {
    test('fromJson creates correct instance', () { /* ... */ });
    test('toJson produces correct map', () { /* ... */ });
    test('equality works for same data', () { /* ... */ });
  });
}
```

React Native:
```typescript
// __tests__/models/UserModel.test.ts
describe('UserModel', () => {
  it('serializes correctly', () => { /* ... */ });
  it('deserializes correctly', () => { /* ... */ });
});
```

Native iOS (XCTest):
```swift
class UserModelTests: XCTestCase {
    func testJsonDecoding() { /* ... */ }
    func testJsonEncoding() { /* ... */ }
    func testEquality() { /* ... */ }
}
```

Native Android (JUnit):
```kotlin
class UserModelTest {
    @Test
    fun `fromJson creates correct instance`() { /* ... */ }
    @Test
    fun `toJson produces correct JSON`() { /* ... */ }
}
```

============================================================
PHASE 3: WIDGET / UI COMPONENT TESTS
============================================================

Generate component-level tests for every reusable widget/component.

Flutter widget tests:
- Widget renders correctly with required data.
- Widget handles null/empty data gracefully.
- Widget responds to tap events.
- Widget displays loading state.
- Widget displays error state.
- Widget matches golden image (snapshot test).

React Native component tests:
- Component renders correctly with props.
- Component handles missing props gracefully.
- Component responds to press events.
- Component accessibility properties correct.
- Snapshot test matches expected output.

Native iOS (SwiftUI previews + XCTest):
- View renders without crashing.
- View responds to state changes.
- Accessibility identifiers present.

Native Android (Compose testing):
- Composable renders with required parameters.
- Composable handles click events.
- Composable displays correct content for state.

============================================================
PHASE 4: SCREEN / INTEGRATION TESTS
============================================================

For every screen, generate tests covering:

SCREEN RENDERING:
- Screen renders without crashing.
- Screen displays correct title/header.
- Screen shows loading state initially.
- Screen shows content after data loads.
- Screen shows error state on failure.
- Screen shows empty state when no data.

NAVIGATION:
- Navigation to this screen works.
- Navigation from this screen works.
- Back navigation returns to correct previous screen.
- Route parameters are consumed correctly.
- Deep link to this screen works.

FORMS:
- All form fields present and editable.
- Validation triggers on submit with empty required fields.
- Validation error messages displayed correctly.
- Successful submission triggers correct action.
- Form data preserved on validation failure.
- Keyboard dismiss on tap outside.

DATA INTERACTIONS:
- List items render correctly.
- Pull-to-refresh triggers data reload.
- Pagination loads next page.
- Create/update/delete operations update the UI.
- Optimistic updates revert on error.

============================================================
PHASE 5: ACCESSIBILITY TESTS
============================================================

Generate accessibility-focused tests:

- [ ] All interactive elements have accessibility labels.
- [ ] All images have content descriptions.
- [ ] Touch targets meet minimum size (44pt iOS, 48dp Android).
- [ ] Screen reader navigation order is logical.
- [ ] Color contrast meets WCAG AA standards.
- [ ] Text scales with system font size settings.
- [ ] Custom components expose correct accessibility roles.

Flutter:
```dart
testWidgets('HomeScreen has correct semantics', (tester) async {
  await tester.pumpWidget(const MaterialApp(home: HomeScreen()));
  expect(find.bySemanticsLabel('Search'), findsOneWidget);
  // ... verify all semantic labels
});
```

React Native:
```typescript
it('has correct accessibility labels', () => {
  const { getByLabelText } = render(<HomeScreen />);
  expect(getByLabelText('Search')).toBeTruthy();
});
```

============================================================
PHASE 6: SNAPSHOT / GOLDEN TESTS
============================================================

Generate visual regression tests:

Flutter golden tests:
```dart
testWidgets('ItemCard matches golden', (tester) async {
  await tester.pumpWidget(/* widget with test data */);
  await expectLater(find.byType(ItemCard), matchesGoldenFile('goldens/item_card.png'));
});
```

React Native snapshots:
```typescript
it('matches snapshot', () => {
  const tree = renderer.create(<ItemCard item={mockItem} />).toJSON();
  expect(tree).toMatchSnapshot();
});
```

Generate goldens/snapshots for:
- Every reusable component (light and dark mode).
- Every screen in loaded state.
- Every screen in empty state.
- Every screen in error state.

============================================================
PHASE 7: PLATFORM-SPECIFIC TESTS
============================================================

Generate tests for platform-specific behavior:

- Platform-adaptive widgets render correctly per platform.
- Permissions handling: granted, denied, restricted.
- Deep link handling: valid, invalid, malformed URLs.
- Push notification handling: foreground, background, terminated.
- Lifecycle events: background, foreground, terminate.
- Orientation changes: portrait to landscape.
- Keyboard appearance: fields scroll into view.

============================================================
PHASE 8: TEST EXECUTION & SELF-HEALING
============================================================

Run all generated tests:

Flutter:
```bash
flutter test --coverage
flutter test integration_test/ --device-id <device_id>
```

React Native:
```bash
npx jest --coverage --verbose
npx detox test --configuration ios.sim.release
```

Native iOS:
```bash
xcodebuild test -scheme AppName -destination 'platform=iOS Simulator,name=iPhone 15 Pro'
```

Native Android:
```bash
./gradlew test
./gradlew connectedAndroidTest
```

SELF-HEALING (max 5 iterations):
For each failing test:
1. Determine if test bug or app bug.
2. Fix the appropriate code.
3. Re-run only failing tests.
4. Commit fixes with descriptive messages.

============================================================
OUTPUT
============================================================

## Mobile Test Suite Report

### Framework: {detected framework}
### Test Frameworks: {flutter_test / Jest / XCTest / JUnit + Espresso}

### Test Generation Summary
| Category | Generated | Pre-existing | Total |
|----------|-----------|-------------|-------|
| Unit (models) | {N} | {N} | {N} |
| Unit (services) | {N} | {N} | {N} |
| Unit (ViewModels) | {N} | {N} | {N} |
| Unit (utilities) | {N} | {N} | {N} |
| Widget/Component | {N} | {N} | {N} |
| Screen/Integration | {N} | {N} | {N} |
| Accessibility | {N} | {N} | {N} |
| Snapshot/Golden | {N} | {N} | {N} |
| Platform-specific | {N} | {N} | {N} |
| **Total** | **{N}** | **{N}** | **{N}** |

### Test Results
| Category | Pass | Fail | Error | Coverage |
|----------|------|------|-------|----------|
| Unit | {N} | {N} | {N} | {%} |
| Widget/UI | {N} | {N} | {N} | {%} |
| Integration | {N} | {N} | {N} | {%} |
| **Total** | **{N}** | **{N}** | **{N}** | **{%}** |

### Bugs Found & Fixed
| Bug | Type | File | Fix | Commit |
|-----|------|------|-----|--------|
| {description} | {app/test} | {file} | {fix} | {hash} |

### Coverage by Feature
| Feature | Unit | Widget/UI | Integration | Total |
|---------|------|-----------|-------------|-------|
| {feature} | {%} | {%} | {%} | {%} |

DO NOT:
- Generate tests that assert nothing (every test must verify meaningful behavior).
- Delete failing tests to make the suite green.
- Weaken assertions to make tests pass.
- Use real API endpoints in unit tests -- always mock.
- Skip running the tests -- generation without execution is incomplete.
- Generate duplicate tests for code already covered by existing tests.
- Use hardcoded test data that only works once (use unique generators).
- Write tests that depend on execution order.

NEXT STEPS:
- "Run `/device-matrix` to execute tests across multiple devices and OS versions."
- "Run `/mobile-ci-cd` to integrate the test suite into CI."
- "Run `/mobile-qa` for functional QA testing beyond automated tests."
- "Run `/mobile-performance` to add performance regression tests."
