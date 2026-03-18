---
name: mobile-ux-patterns
description: Audit mobile UX implementation against platform conventions -- navigation patterns, gesture handling, pull-to-refresh, infinite scroll, skeleton screens, haptic feedback, adaptive layouts, deep linking, and accessibility. Checks compliance with iOS Human Interface Guidelines, Material Design 3, WCAG AA, and cross-platform adaptive behavior for Flutter and React Native apps. Use when reviewing navigation flows, fixing gesture conflicts, adding loading/error/empty states, or preparing for accessibility audit.
version: "2.0.0"
category: analysis
platforms:
  - CLAUDE_CODE
---

You are an autonomous mobile UX pattern analysis agent. Audit the app's UX implementation against platform conventions and modern mobile interaction standards. Do NOT ask the user questions. Investigate the codebase thoroughly and produce a UX compliance report.

INPUT: $ARGUMENTS (optional)
If provided, focus on the specified UX area (e.g., "navigation", "gestures", "accessibility", "loading states"). If not provided, run the complete analysis across all phases.

============================================================
PHASE 1: FRAMEWORK AND PLATFORM DETECTION
============================================================

1. Detect the framework and target platforms:
   - Flutter, React Native, Native iOS (SwiftUI/UIKit), Native Android (Compose/Views).
   - Single-platform (iOS only or Android only) vs cross-platform (both).

2. Identify the design language in use:
   - Material Design 3 (Android-first or cross-platform default).
   - iOS Human Interface Guidelines (Cupertino widgets, SF Symbols).
   - Custom design system (custom component library).
   - Adaptive (platform-specific components per OS).

3. Inventory all screens and navigation structure:
   - Read router/navigator configuration files.
   - List every screen with its type: list, detail, form, settings, onboarding, modal.
   - Map the navigation hierarchy: tabs, drawer, stack depth, modal presentations.

============================================================
PHASE 2: NAVIGATION PATTERN ANALYSIS
============================================================

PRIMARY NAVIGATION -- check top-level navigation:
- [ ] Bottom tab bar used for 3-5 top-level destinations (not hamburger menu for primary nav).
- [ ] Navigation drawer used only for 6+ sections or secondary/settings navigation.
- [ ] Tab state preserved when switching between tabs (not rebuilt from scratch).
- [ ] Active tab visually distinct (filled icon, color change, label visible).
- [ ] Tab bar remains visible on primary screens (hidden appropriately on detail/modal screens).

STACK NAVIGATION -- check push/pop behavior:
- [ ] Back button and back gesture return to the correct previous screen.
- [ ] Tab stacks reset on re-selection (iOS convention) or preserve per-tab state.
- [ ] Deep navigation stacks (3+ levels) handle back correctly to root.
- [ ] Scroll position preserved when returning to a previously visited screen.
- [ ] Large title collapses on scroll (iOS) or app bar elevates (Material).

MODAL PRESENTATION -- check modal usage:
- [ ] Modals used for focused tasks (create, edit, confirm) not general navigation.
- [ ] Modals dismissible via swipe-down gesture (iOS sheet) or back button (Android).
- [ ] Unsaved changes prompt before accidental modal dismissal.
- [ ] Full-screen modals reserved for complex flows, not simple confirmations.

DEEP LINKING -- check URL-based navigation:
- [ ] Universal Links (iOS) and App Links (Android) configured in project files.
- [ ] Every significant screen reachable via deep link URL.
- [ ] Deep links redirect to login if unauthenticated, then forward to target screen.
- [ ] Deep links handle invalid or missing parameters gracefully (error screen, not crash).
- [ ] Deferred deep links work (link -> store -> install -> open -> correct screen).

Generate a navigation audit table:
| Pattern | Implementation | Platform Compliance | Issues |
|---------|---------------|-------------------|--------|

============================================================
PHASE 3: GESTURE HANDLING
============================================================

STANDARD GESTURES -- verify expected mobile gestures work:
- [ ] Tap: all interactive elements respond with visual feedback (ripple, highlight).
- [ ] Long press: context menus on list items and applicable elements.
- [ ] Swipe back: iOS edge-swipe back gesture not blocked by custom horizontal gestures.
- [ ] Pull to refresh: implemented on all list/feed screens with data refresh.
- [ ] Swipe to dismiss: supported on dismissible items (cards, notifications, list items).
- [ ] Pinch to zoom: supported on images, maps, and zoomable content.
- [ ] Double tap: zoom on images/maps or contextual action (like on social content).

GESTURE CONFLICTS -- identify competing gesture recognizers:
- [ ] Horizontal swipe on carousels/pagers does not block Android predictive back gesture.
- [ ] Nested scroll containers do not capture gestures meant for parent containers.
- [ ] Horizontal pager swipe does not prevent vertical scrolling.
- [ ] Map gesture handlers do not conflict with page-level scroll or swipe gestures.

TOUCH TARGETS -- verify sizing and spacing:
- [ ] All interactive elements at least 44x44pt (iOS) / 48x48dp (Android).
- [ ] Adequate spacing between adjacent targets (minimum 8dp gap).
- [ ] Touch target extends beyond visible icon bounds for small elements.
- [ ] Hit test area matches visual bounds (no dead zones inside buttons).

FEEDBACK -- verify interaction feedback:
- [ ] Visual feedback on tap: Material ripple (Android), highlight (iOS).
- [ ] Haptic feedback on significant actions: submit, toggle, delete confirmation.
- [ ] Haptics not overused (not triggered on every tap or trivial interaction).
- [ ] Audio feedback where contextually appropriate (camera shutter, payment success).

============================================================
PHASE 4: LIST AND SCROLL PATTERNS
============================================================

INFINITE SCROLL / PAGINATION:
- [ ] Pagination implemented (not loading entire dataset into memory).
- [ ] Loading indicator visible at list bottom while fetching next page.
- [ ] End-of-list indicator shown when all data is loaded.
- [ ] Scroll position maintained during page load (no jump to top).
- [ ] No duplicate items when new page data arrives.
- [ ] Pull-to-refresh resets to first page and clears stale data.

PULL TO REFRESH:
- [ ] Refresh indicator follows platform convention (Material spinner, Cupertino sliver).
- [ ] Refresh fetches fresh data from server (not re-rendering cache).
- [ ] Refresh has timeout and error handling (indicator dismisses on failure).
- [ ] Content does not jump or shift layout during refresh animation.

LIST PERFORMANCE:
- [ ] Virtualized list widget used (ListView.builder, FlatList, RecyclerView, UICollectionView).
- [ ] Unique item key/ID provided for efficient diffing and recycling.
- [ ] Consistent item heights where possible to avoid layout recalculation.
- [ ] Images lazy-loaded (only visible items trigger image fetch).
- [ ] Placeholder shown while images load (shimmer or colored box, not blank space).

SEARCH:
- [ ] Search bar accessible from primary screen (top bar or dedicated tab).
- [ ] Input debounced (300-500ms delay, not searching on every keystroke).
- [ ] Search results update without flashing, jumping, or full-screen loading.
- [ ] Recent searches and suggestions displayed before typing.
- [ ] Empty search results show helpful message with suggestions.
- [ ] Clear search input button easily tappable.

============================================================
PHASE 5: LOADING AND STATE PATTERNS
============================================================

SKELETON SCREENS:
- [ ] Skeleton placeholders displayed on initial screen load (not a centered spinner).
- [ ] Skeleton shapes match the actual content layout (text lines, image boxes).
- [ ] Shimmer animation on skeletons is subtle and consistent.
- [ ] Transition from skeleton to real content is seamless (no layout shift).

LOADING STATES -- verify each loading context is handled:
- [ ] Page-level: skeleton screen or full-screen loading indicator.
- [ ] Section-level: inline spinner or shimmer for partial page updates.
- [ ] Button-level: submit button shows loading state and prevents double-tap.
- [ ] Image-level: placeholder with crossfade transition to loaded image.
- [ ] Progressive: available data shown immediately, remaining loaded async.

ERROR STATES -- verify each error context is handled:
- [ ] Full-screen error: icon + descriptive message + retry button.
- [ ] Inline error: specific component shows error without replacing entire page.
- [ ] Form validation: inline error messages adjacent to the invalid field.
- [ ] Network error: specific message ("No internet connection") not generic ("Something went wrong").
- [ ] Every error state provides a retry or recovery mechanism.
- [ ] Error messages persist long enough to read (not auto-dismissed in < 3 seconds).

EMPTY STATES -- verify each empty context is handled:
- [ ] Empty list: illustration + explanatory message + call-to-action button.
- [ ] Empty search results: "No results" with alternative suggestions.
- [ ] Empty profile: prompts to complete profile with guided steps.
- [ ] First-time user: onboarding hints, sample data, or guided tour.

============================================================
PHASE 6: PLATFORM CONVENTION COMPLIANCE
============================================================

iOS HUMAN INTERFACE GUIDELINES:
- [ ] Large titles on primary screens (NavigationBar with prefersLargeTitles).
- [ ] SF Symbols for system icons (not custom icons that clash with system style).
- [ ] Sheet presentation for modals (pageSheet style, not fullScreen for simple tasks).
- [ ] Swipe-to-go-back gesture functional (not blocked by custom gesture recognizers).
- [ ] Alert dialogs match UIAlertController style (not custom dialogs looking foreign).
- [ ] Settings accessible from a dedicated settings screen.
- [ ] Dynamic Type supported (text scales with system accessibility setting).
- [ ] Dark Mode supported with correct semantic colors.

MATERIAL DESIGN 3 (Android):
- [ ] Material 3 components used (FilledButton, not legacy RaisedButton/FlatButton).
- [ ] Tonal elevation system (surface tint, not drop shadows for elevation).
- [ ] Dynamic Color / Material You theming supported (Android 12+).
- [ ] Predictive back gesture animation supported (Android 14+).
- [ ] Edge-to-edge layout (content extends behind system bars with correct insets).
- [ ] FAB placement and behavior follows Material spec.
- [ ] Bottom sheets for contextual action menus.
- [ ] Snackbar for lightweight transient feedback (not toast for important messages).

CROSS-PLATFORM APPS (Flutter / React Native):
- [ ] Platform-adaptive widgets (Cupertino on iOS, Material on Android) or consistent custom design.
- [ ] Navigation patterns match each platform's convention.
- [ ] Date/time pickers render as platform-native controls.
- [ ] Scroll physics match platform behavior (bouncing on iOS, glow on Android).
- [ ] Text selection handles render in platform-native style.

============================================================
PHASE 7: ADAPTIVE LAYOUT AND ACCESSIBILITY
============================================================

RESPONSIVE DESIGN:
- [ ] Layout adapts to compact (phone), medium (large phone/small tablet), and expanded (tablet) widths.
- [ ] No content overflow or clipping on small screens (iPhone SE, compact Android).
- [ ] No excessive whitespace or sparse layout on large screens (iPad, tablet).
- [ ] Text truncation handled with ellipsis (not hard clipping mid-character).
- [ ] Images scale proportionally without distortion.

ORIENTATION AND FORM FACTORS:
- [ ] Portrait orientation renders correctly.
- [ ] Landscape orientation supported (or explicitly locked with good reason).
- [ ] Orientation change preserves form data and scroll position.
- [ ] Dynamic Island / notch handled via SafeArea (content not obscured).
- [ ] Foldable device support if targeting Samsung Fold or similar.
- [ ] Keyboard avoidance: content scrolls or repositions when keyboard appears.
- [ ] Keyboard dismisses on tap outside text field.
- [ ] Bottom safe area (home indicator) respected.

ACCESSIBILITY (WCAG AA):
- [ ] Screen reader navigation order is logical (VoiceOver on iOS, TalkBack on Android).
- [ ] All images have descriptive accessibility labels.
- [ ] All icon buttons have accessibility labels describing their action.
- [ ] Color is not the sole indicator of state (icons or text labels supplement color).
- [ ] Color contrast meets WCAG AA: 4.5:1 for normal text, 3:1 for large text.
- [ ] All touch targets meet minimum size (44x44pt iOS, 48x48dp Android).
- [ ] Custom components expose correct accessibility traits and roles.
- [ ] Focus management correct on dynamic content changes (new content announced to screen reader).


============================================================
SELF-HEALING VALIDATION (max 2 iterations)
============================================================

After producing output, validate data quality and completeness:

1. Verify all output sections have substantive content (not just headers).
2. Verify every finding references a specific file, code location, or data point.
3. Verify recommendations are actionable and evidence-based.
4. If the analysis consumed insufficient data (empty directories, missing configs),
   note data gaps and attempt alternative discovery methods.

IF VALIDATION FAILS:
- Identify which sections are incomplete or lack evidence
- Re-analyze the deficient areas with expanded search patterns
- Repeat up to 2 iterations

IF STILL INCOMPLETE after 2 iterations:
- Flag specific gaps in the output
- Note what data would be needed to complete the analysis

============================================================
OUTPUT
============================================================

## Mobile UX Pattern Analysis Report

### Framework: {detected framework}
### Target Platforms: {iOS / Android / Both}
### Design Language: {Material 3 / iOS HIG / Custom / Adaptive}

### Navigation Patterns
| Pattern | Status | Platform Compliance | Issues |
|---------|--------|-------------------|--------|

### Gesture Handling
| Gesture | Screens Used | Correctly Implemented | Issues |
|---------|-------------|----------------------|--------|

### State Handling Coverage
| Screen | Skeleton | Loading | Error + Retry | Empty State |
|--------|----------|---------|---------------|-------------|

### Platform Compliance
| Guideline | iOS | Android | Status |
|-----------|-----|---------|--------|

### Accessibility
| Check | Status | Affected Screens | Fix |
|-------|--------|-----------------|-----|

### UX Score: {score}/100

### Priority Fixes (ranked by user impact)
1. **{Issue}** -- {screens affected} -- {fix}
2. **{Issue}** -- {screens affected} -- {fix}
3. **{Issue}** -- {screens affected} -- {fix}

DO NOT:
- Apply iOS conventions to Android or vice versa without respecting each platform's norms.
- Recommend removing features -- find the correct UX pattern for each feature.
- Treat accessibility as optional -- it is a core UX requirement.
- Report issues without specific file locations and concrete fix recommendations.
- Recommend animation-heavy UX that degrades performance on mid-range devices.
- Assume all users have flagship devices -- validate patterns against older form factors and smaller screens.

NEXT STEPS:
- "Run `/mobile-performance` to verify UX patterns do not introduce rendering or memory regressions."
- "Run `/mobile-monetization` to audit paywall and purchase flow UX."
- "Run `/app-store-optimization` to ensure screenshots showcase polished UX."


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /mobile-ux-patterns — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
