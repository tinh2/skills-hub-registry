# Flutter Platform Checklist

Reference file for `/ux` skill — Flutter-specific heuristics, accessibility patterns, and design system conventions.

## Project Detection

- `pubspec.yaml` exists: Flutter project (mobile — iOS + Android, possibly web/desktop).
- Theme file: `lib/config/theme.dart` or `lib/theme/` directory.
- Routes: `lib/config/routes.dart`, `lib/app.dart` (GoRouter, auto_route, etc.).
- Shared widgets: `lib/core/widgets/`, `lib/shared/widgets/`, `lib/common/`.

## Screen Discovery

Read routes from GoRouter config (lib/app.dart or lib/config/routes.dart).
For each route, identify the screen widget file.

## Accessibility (WCAG 2.1 AA)

### Semantic Structure
- Every `Icon` widget must have a `semanticLabel` or be wrapped in `Semantics`.
- Every `Image`/`Image.network` must have a `semanticLabel`.
- Decorative images must use `excludeFromSemantics: true`.
- Use `MergeSemantics` where a group of widgets represents one concept.
- Logical reading order must match visual order.

### Touch Targets
- Every tappable element: minimum 48x48 dp (Material minimum).
- Adjacent touch targets: minimum 8dp spacing.
- Small icons used as buttons must have padding to expand hit area.
- Check `IconButton`, `GestureDetector`, `InkWell` tap areas.

### Text Scaling
- Text must scale with system font size (use sp / theme text styles).
- No fixed pixel sizes that prevent scaling.
- Layout must not break at 200% text scale factor.
- `TextOverflow` handling must work at larger text sizes.

### Motion & Animation
- Animations must respect `MediaQuery.disableAnimations`.
- No content that flashes more than 3 times per second.
- Auto-playing animations must be pausable or respect reduced motion preferences.

### Focus & Navigation
- Tab/focus order for forms must be logical (top to bottom, left to right).
- Focus indicators must be visible.
- Keyboard/switch access navigation must work on all interactive elements.

## Design System Consistency

### Theme Token Usage
- Every color reference must use `ColorScheme` or the app's named color constants.
  Flag any hardcoded `Color(0xFF...)` values in screen or widget files.
- Every text style must use `TextTheme` from the theme or app text style constants.
  Flag any hardcoded `TextStyle(fontSize: ...)` not from the theme.
- Every spacing value must use app spacing constants or consistent multiples of a base unit (4dp or 8dp grid).
  Flag magic number padding/margin values that deviate from the grid.
- Every border radius must use the app's standard radii.
  Flag inconsistent border radius values across similar components.

### Component Conventions
- Primary actions: `FilledButton`. Secondary: `OutlinedButton`. Tertiary: `TextButton`.
- Icons from a consistent family (do not mix Material Icons, Cupertino Icons, and custom SVGs arbitrarily).
- Loading/error/empty states using shared widgets consistently.
- Use Material 3 components (`FilledButton`, `NavigationBar`, `SearchBar`) rather than Material 2 predecessors.

### Motion Choreography
- Page transitions consistent across all push routes.
- Transitions match platform conventions (slide from right on iOS, fade on Android).
- Transition duration: 200-350ms for page transitions.
- Modal routes: slide up for bottom sheets, fade for dialogs.
- Micro-interactions: ink splash on buttons, shimmer for content loading, spinner for actions.
- List items: staggered fade/slide on first load, `AnimatedList` on add/remove.
- Hero animation between list items and detail screens.
- Duration ranges: small (100-200ms), medium (200-350ms), large (350-500ms).
- Easing: `Curves.easeInOut` for most, `Curves.easeOut` for enter, `Curves.easeIn` for exit.

### Responsive Design
- `LayoutBuilder` or `MediaQuery` checks for tablet vs phone.
- Landscape orientation support or explicit portrait lock.
- Text handles different screen widths (no overflow, proper wrapping).

## Fix Commit Prefixes

- `fix(ux): [screen] add missing loading state`
- `fix(a11y): [screen] add semantic labels to interactive elements`
- `fix(design): [screen] replace hardcoded colors with theme tokens`
- `fix(motion): [screen] add page transition and list entrance animation`

## Rules

- Always use theme tokens from `ThemeData`. Never introduce new hardcoded `Color` or `TextStyle` values in screen files.
- When adding semantic labels, use concise descriptive text. Do not include "button" or "icon" in the label — the widget role is announced automatically.
- When fixing contrast, prefer adjusting the foreground (text/icon) color over the background unless the background is the problem.
- When adding animations, keep durations 150-400ms. Use standard curves. Do not animate elements that are already on screen and static.
