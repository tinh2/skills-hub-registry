---
name: design-audit
description: "Read-only design quality audit (WCAG 2.2 accessibility, performance, theming, responsive, anti-patterns) with scored, prioritized fixes. Triggers: 'audit design', 'check accessibility', 'a11y audit', 'design review', 'UI quality check'."
version: "1.1.0"
category: ux
platforms:
  - CLAUDE_CODE
---

Audit the UI of this codebase and produce a scored, prioritized report. This is read-only: don't modify source files.

## Input

`$ARGUMENTS` (optional): a focus area (`accessibility`/`a11y`, `performance`, `theming`, `responsive`/`mobile`, `anti-patterns`, `modern`) or a file/directory path. With a focus, go deep there and still do a lighter pass on the other categories. Without one, audit everything.

## Approach

Identify the stack (web framework and CSS approach, Flutter, SwiftUI, Compose, React Native) and any design system or `CLAUDE.md` design context. Spend effort where users spend time: route-level pages and shared components first, then the landing, auth and primary flows. Run real tools when available (axe, Lighthouse, `flutter analyze`) and prefer their output over inspection.

## What to check

**Accessibility (WCAG 2.2 AA, note AAA where cheap).** Beyond the familiar basics (alt text, labels, semantic landmarks, heading order, 4.5:1 / 3:1 contrast, keyboard reachability, visible focus, `lang`), check the criteria teams usually miss:

- 1.4.10 Reflow: no horizontal scroll at 320px. 1.4.12 Text spacing overrides don't break layout.
- 1.4.11 Non-text contrast ≥ 3:1 for controls, focus rings and meaningful icons.
- 2.4.11 Focus Not Obscured (AA): sticky headers, cookie bars and drawers don't hide the focused element.
- 2.5.7 Dragging: every drag has a single-pointer alternative.
- 2.5.8 Target Size Minimum (AA): 24x24 CSS px or enough spacing. 2.5.5 (AAA) is 44x44. Mobile platforms want 48dp Android / 44pt iOS.
- 3.3.7 Redundant Entry and 3.3.8 Accessible Authentication (AA): no re-asking for entered data, no cognitive test or puzzle-only CAPTCHA at login, paste allowed in password fields.
- Custom widgets follow ARIA APG patterns (dialog, combobox, tabs) with correct keyboard behavior; status messages use `role="status"`/`aria-live`.
- Flutter: `Semantics`, `semanticLabel` on images, tooltips on icon buttons.

**Performance.** Animations only on `transform`/`opacity`/`filter`; images with explicit dimensions, modern formats and lazy loading below the fold; `font-display`; deferred third-party scripts; code splitting at routes; `content-visibility` on long off-screen content; no read-then-write layout thrash. Flutter: `const` constructors, `RepaintBoundary` on heavy subtrees, builder lists for long content.

**Theming.** Colors, type sizes and spacing come from tokens, not magic values; semantic token names; a small palette and 2-3 surface levels; 2-3 font weights. Dark mode is complete (not inverted), keeps contrast, adapts images/icons and reduces shadows. Note adoption of current platform features as opportunities: `oklch()`, `color-mix()`, `light-dark()`, container queries, `:has()`, `@starting-style`, View Transitions, Popover API, scroll-driven animations; Material 3 / dynamic color on Flutter.

**Responsive.** Reason through 320, 375, 768, 1024, 1440 and 1920+ widths. Components adapt to their container; navigation adapts across sizes; tables have a small-screen strategy; forms stack; `dvh` instead of `100vh` hacks; hover-only interactions have touch equivalents; inputs set `inputmode`/`type`; long strings wrap or truncate; viewport meta present and zoom not disabled.

**Anti-patterns.**

- Generic AI-template look: cyan-on-dark, purple-to-blue gradient headings, gradient text, glassmorphism everywhere, hero metrics grids ("10K+ users"), blob decorations, shadows on everything, a single characterless font.
- Dated CSS: float layouts, `!important` chains outside resets/vendor overrides, unneeded vendor prefixes, bounce easing, z-index values in the hundreds or thousands.
- Structure: div soup, nested interactive elements (`<a>` in `<button>`), click handlers on non-interactive elements, duplicate component implementations, inline styles that should be tokens, fixed modals without scroll lock.

Judge in context: `!important` in a reset is fine, a gradient used once with intent is fine.

## Scoring

Severity per finding: **P0** blocks users (WCAG A failure, keyboard trap, broken layout); **P1** WCAG AA failure or serious usability issue; **P2** degraded experience (dated patterns, token drift, no reduced motion); **P3** enhancement (modern CSS, AAA, polish).

Score each category 0-100. Anti-patterns = 100 − (10×P0 + 5×P1 + 2×P2). Overall is weighted: Accessibility 35%, Performance 20%, Responsive 20%, Theming 15%, Anti-patterns 10%. Don't award 100.

## Report

```
## Design Audit Report

**Overall Score**: X/100 (Excellent / Good / Fair / Needs Work / Critical)
**Files Audited**: N
**Findings**: N P0, N P1, N P2, N P3

### Category Scores
| Category | Score | Key Issue |
|---|---|---|
| Accessibility | X/100 | ... |
| Performance | X/100 | ... |
| Theming | X/100 | ... |
| Responsive | X/100 | ... |
| Anti-patterns | X/100 | ... |

### P0 / P1 Findings
1. **Title**: file:line. What is wrong. **Fix**: the specific change.

### P2 / P3 Findings
(grouped by category, same format)

### Quick Wins (< 30 min each)
### Modernization Opportunities
### Comparison to Previous Audit (if scores exist in MEMORY.md)
```

Every finding needs a file:line where possible and a concrete fix. Before finalizing, re-open the source for a few findings to confirm they are real, and check the score arithmetic.

If `MEMORY.md` exists, append the scores with today's date under `## Design Audit Scores` so later audits can show the trend.
