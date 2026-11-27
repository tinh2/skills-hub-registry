---
name: flutter
description: "Build a complete Flutter app from a video, screenshots, description or /mvp output, matching the observed UI and flows, with tests. Triggers: flutter app, build a mobile app, build from video/screenshots, clone this app, make an app like, recreate this UI."
version: "2.1.0"
category: build
platforms:
  - CLAUDE_CODE
---

Build a production-quality Flutter app that reproduces what the input shows: every screen, flow and state, with tests, and an analyzer that's clean.

## Input

A screen recording, screenshots, a description or URL, `/mvp` output, or a mix. If `/mvp` output is present, build from its feature breakdown and architecture instead of re-analyzing. Ask for more only if the input is too thin to identify the screens; otherwise make reasonable assumptions and list them.

## Analyze before coding

Go frame by frame and inventory: every screen and route; components (app bars, navs, cards, lists, forms, sheets, dialogs, FABs, chips); colors, type sizes, spacing, radii, shadows, gradients; how screens connect and what triggers each transition; the data shown; animations; loading, empty and error states; and gestures (swipe actions, pull-to-refresh, infinite scroll, drag). Small details such as icons, dividers and padding count.

## Architecture

```
lib/
  main.dart, app.dart
  config/      theme.dart, routes.dart, design_tokens.dart, constants.dart (user-facing strings, or l10n)
  models/
  services/    one per domain (AuthService, BookingService…), behind interfaces
  providers/   (or blocs/)
  screens/<feature>/<feature>_screen.dart + widgets/
  shared/      widgets/, utils/, l10n/
test/          mirrors lib/ (screens/, widgets/, services/)
```

- **State:** Riverpod by default (current major: `Notifier`/`AsyncNotifier`, code generation optional), unless the project already uses something else or the user asks. Bloc/Cubit suits large event-driven apps; Provider is fine for tiny ones.
- **Routing:** go_router, `StatefulShellRoute` for tabbed navigation that keeps per-tab state, deep-link-ready paths, transitions matching what's observed.
- **Dart 3:** sealed classes for state, switch expressions and patterns, records, class modifiers; `const` widgets; small build methods; files under ~500 lines.
- **Theme:** Material 3 is the default in current Flutter (don't set `useMaterial3`). Build the `ColorScheme` with `fromSeed` or explicitly to match the design, plus a type scale and component themes; light and dark. Spacing, radii, elevations and icon sizes live in `design_tokens.dart`. Widgets use theme tokens, never literal colors or text styles.
- **Data:** models for every observed entity (freezed + json_serializable when it pays off), realistic mock data matching the input (no lorem ipsum), and service interfaces so a real backend can replace mocks. Set up Firebase/Supabase only if the app clearly uses it.
- **HTTP (dio):** 30 s connect and receive timeouts, retry with exponential backoff on transient errors, user-friendly messages that never leak server errors, and cancel/close in `dispose`.

## Every screen ships with

- Loading (skeletons), empty and error states.
- Accessibility: `Semantics` labels on interactive elements and icon buttons, 48x48dp minimum touch targets, ink feedback, sensible `MergeSemantics`/`ExcludeSemantics` grouping, WCAG AA contrast, logical focus order.
- Polish where observed: `SliverAppBar`/`CustomScrollView`, hero transitions, haptics on key actions, form focus and `TextInputAction` handling, `SafeArea`.
- Adaptive layout via `LayoutBuilder` breakpoints: compact <600dp (single column, `NavigationBar`), medium 600 to 840dp (list-detail, `NavigationRail`), expanded >840dp (multi-column, `NavigationDrawer`).
- Platform care: mobile first; for web handle URL strategy and hover; for desktop handle min window size, shortcuts and context menus. Use `kIsWeb` guards rather than importing `dart:io` on web.
- A widget test covering rendering, interactions, navigation, loading/empty/error states and semantic labels.

Add only the packages the app actually needs (typical: flutter_riverpod, go_router, dio, cached_network_image, flutter_svg, intl, google_fonts, flutter_animate, freezed/json_serializable). Avoid deprecated APIs; check pub.dev for the current major before pinning.

## Done when

`flutter analyze` reports 0 issues and `flutter test` passes. On failure, make a minimal targeted fix and re-run (up to 3 attempts); if still failing, report the error output for manual follow-up.

## Output

1. Screen inventory table.
2. Architecture overview (structure, state, routing).
3. Every file in full: no placeholders, TODO stubs or "unchanged" references.
4. Tests for every screen and shared widget.
5. Complete `pubspec.yaml`.
6. Run instructions, including any web/desktop steps.
7. Known gaps and assumptions.

Implement every observed screen; don't add unobserved features beyond essentials (error handling, accessibility). Suggest `/spec` for the backend stories the app will need, or `/mvp` if a product analysis should come first.

## Telemetry

If a project memory directory exists under `~/.claude/projects/`, append to its `skill-telemetry.md` (skip silently otherwise):

```
### /flutter — YYYY-MM-DD
- Outcome: SUCCESS | PARTIAL | FAILED
- Self-healed: yes (what) | no
- Iterations used: N / 3
- Bottleneck: phase that struggled, or none
- Suggestion: one-line improvement, or none
```
