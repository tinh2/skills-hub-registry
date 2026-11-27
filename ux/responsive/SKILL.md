---
name: responsive
description: "Audit and fix responsive design across breakpoints: fixed widths, overflow and horizontal scroll, non-responsive images, small touch targets, unreadable type, layouts that don't adapt. Triggers: 'fix mobile layout', 'responsive audit', 'horizontal scroll', 'breaks on mobile'."
version: "2.1.0"
category: ux
platforms:
  - CLAUDE_CODE
---

Find and fix responsive layout problems so every screen works from a small phone to an ultra-wide monitor with no page-level horizontal scroll.

## Input

`$ARGUMENTS` (optional): screens or components to focus on, custom breakpoints, or a direction (`mobile-first`, `tablet`, `desktop-down`). Default breakpoints: 375, 428, 768, 1024, 1280, 1920. Without arguments, audit the whole project.

## Find the problems

Identify the framework and its existing responsive system (Tailwind prefixes, breakpoint constants, `useMediaQuery` hooks, layout components, Flutter `LayoutBuilder`/`MediaQuery`). Fix within that system rather than adding a parallel one.

**Measure, don't only read.** If the app can run, load each screen in a headless browser at each breakpoint and check `document.documentElement.scrollWidth > clientWidth`, then find the offending element (the one whose right edge exceeds the viewport). Screenshot the changed screens. Code reading misses most overflow caused by long strings, images and third-party widgets.

In code, look for:

- **Fixed widths** wider than a small phone with no flexible or scrolling parent: CSS `width: Npx`, Tailwind `w-[Npx]`/`w-96` without responsive variants, Flutter `SizedBox`/`Container` widths, inline styles. Classify each as breaking, risky or safe.
- **Layouts that don't adapt:** grids that never collapse to one column, flex rows that don't wrap, heavy horizontal padding on mobile (> 32px), headings that don't scale.
- **Images** without `max-width: 100%`/`height: auto`, `aspect-ratio`, `srcset`/`sizes` or the framework image component; Flutter images without `fit` or constraints.
- **Overflow sources:** `white-space: nowrap` on dynamic text, tables and code blocks without a scroll wrapper, long URLs or IDs without `overflow-wrap: anywhere`, `100vh` (use `dvh`/`svh`), Flutter `Row` children without `Expanded`/`Flexible`.
- **Touch targets** under 48x48px (44pt iOS) or closer than 8px apart, especially icon buttons.
- **Typography:** body under 16px on mobile, form inputs under 16px (iOS Safari zooms on focus), lines over ~75ch on wide screens, body line-height under 1.4, truncation that hides essential content, text ignoring the user's text scale.

## Fix

Fix in shared layouts and components first so every page benefits. Typical fixes:

- `width: 100%; max-width: ...` (or `w-full max-w-*`); Flutter `Expanded`/`Flexible`/`ConstrainedBox`.
- `grid-template-columns: repeat(auto-fit, minmax(min(280px, 100%), 1fr))` or `grid-cols-1 md:grid-cols-2 lg:grid-cols-3`; Flutter `LayoutBuilder` to switch column counts.
- Container queries for components that live in containers of varying width.
- Fluid type and spacing with `clamp()`, always with rem bounds, never bare `vw`.
- Horizontally scrollable wrappers for intentionally wide content (tables, code, carousels), never on the page body.
- Desktop navigation collapsing to a menu or bottom bar on small screens.
- `min-width`/`min-height` or padding to reach 48px targets.

Constraints: don't hide content on mobile unless it is truly optional and reachable another way; never disable zoom (`user-scalable=no`, `maximum-scale=1`); keep reading order logical when layout reflows; fix the cascade rather than adding `!important`.

Commit per category with messages like `fix(responsive): replace fixed widths with responsive layouts`.

## Verify

Re-run the breakpoint measurement on every screen; no screen may have page-level horizontal scroll. Run the type checker, linters (Stylelint/ESLint), `flutter analyze` where relevant, the test suite and the build. Repeat fix and verify until no breaking issues remain, then document anything left.

## Report

```
## Responsive Audit Complete

### Framework: detected
### Breakpoints Tested: 375, 428, 768, 1024, 1280, 1920

### Issues Found and Fixed
| Category | Found | Fixed | Remaining |
|---|---|---|---|
| Fixed widths (breaking) | | | |
| Missing responsive variants | | | |
| Non-responsive images | | | |
| Overflow / horizontal scroll | | | |
| Touch targets < 48px | | | |
| Typography scaling | | | |

### Breakpoint Matrix
| Screen | Mobile | Tablet | Desktop | Wide |
|---|---|---|---|---|

### Files Modified
| File | Changes |
|---|---|

### Verdict
RESPONSIVE READY, or NEEDS WORK: N screens at which breakpoints, and why.
```

State whether the matrix came from real rendering or code reading. Useful follow-ups: `/dark-mode`, `/ux`, `/qa`, and testing on a real device.
