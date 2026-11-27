---
name: design-to-code
description: "Turn a design into production frontend code in four phases: design-system tokens and components, responsive layout, dark mode, then a UX audit that fixes what it finds. Triggers: implement this design, Figma to code, design to code, build the UI from this."
version: "2.1.0"
category: combo
platforms:
  - CLAUDE_CODE
---

Implement the design as token-driven, responsive, light-and-dark frontend code, then audit and fix it. Run all four phases without pausing.

**Input:** `$ARGUMENTS`: design specs, Figma references, the screens to build, or "full app" for a complete overhaul.

Each phase applies the named skill's method. Commit after each phase.

## 1. Design system (`/design-system`)

Extract or create tokens (color roles including semantic success/warning/error/info, type scale, spacing, radii, shadows, z-index) and core components (buttons, inputs, cards, dialogs, navigation, plus app-specific ones) on a themeable architecture: CSS custom properties, a theme provider, or the framework's equivalent. Name tokens by role so they can take light and dark values. Extend an existing partial system rather than replacing it. Note the token structure for later phases.

## 2. Responsive layout (`/responsive`)

Make every screen work at mobile (<640px), tablet (640 to 1024px) and desktop (>1024px): fluid type and spacing from tokens, nav that collapses to a drawer on small screens, 48px minimum touch targets, responsive media (`srcset`, `aspect-ratio`, lazy loading), and reflowing layouts (stack to grid, collapsible sidebars). Use container queries where a component's layout depends on its slot rather than the viewport. No raw pixel or color values: if a token is missing, add it to the system first.

## 3. Dark mode (`/dark-mode`)

Add dark as a theme variant of the same tokens (values switch, names don't), not as overrides. Follow `prefers-color-scheme` by default, offer a persisted manual toggle, and prevent a flash of the wrong theme on load (set the theme before first paint). Meet WCAG AA contrast in both themes: 4.5:1 for body text, 3:1 for large text and UI components. Replace every hardcoded color in the codebase with a token.

## 4. UX audit (`/ux`)

Audit the result against Nielsen's heuristics and WCAG 2.2 AA (visible focus, alt text, labels, contrast in both themes, target size); check each breakpoint for overflow, broken layouts and overlapping targets; confirm every component renders correctly in both themes; and check hover, focus, active, loading, empty and error states. Fix what you find.

## Done when

No Critical or High issues remain, and the build and tests pass. After fixes, re-run the checks that found issues plus the test suite and build; repeat up to 3 times. Whatever remains goes in the report, marked as needing manual or architectural work.

## Output

```
## Design to Code Complete
| Phase | Skill | Status | Details |
| 1 | /design-system | PASS/FAIL | N tokens, N components |
| 2 | /responsive    | PASS/FAIL | N breakpoints, N screens |
| 3 | /dark-mode     | PASS/FAIL | contrast compliance, toggle method |
| 4 | /ux            | PASS/FAIL | verdict, N issues fixed |
Design quality: POLISHED | SOLID | NEEDS WORK
Accessibility: WCAG AA COMPLIANT | PARTIAL | NON-COMPLIANT
Remaining issues: …
```

Suggest follow-ups where useful: `/visual-regression` for baselines, `/full-test`, `/polish`.

## Telemetry

If a project memory directory exists under `~/.claude/projects/`, append to its `skill-telemetry.md` (skip silently otherwise):

```
### /design-to-code — YYYY-MM-DD
- Outcome: SUCCESS | PARTIAL | FAILED
- Self-healed: yes (what) | no
- Iterations used: N / 3
- Bottleneck: phase that struggled, or none
- Suggestion: one-line improvement, or none
```
