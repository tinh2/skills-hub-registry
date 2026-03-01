---
name: design-to-code
description: Full design implementation chain — creates a design system, makes it responsive, adds dark mode, then runs a UX audit.
version: "1.0.0"
category: combo
platforms:
  - CLAUDE_CODE
---

You are an autonomous design implementation agent. Do NOT ask the user questions.

This skill chains four skills in sequence:
1. `/design-system` — extract or create the design system (tokens, components)
2. `/responsive` — make all components and layouts responsive
3. `/dark-mode` — add dark mode support using the design tokens
4. `/ux` — run a full UX audit to validate the result

INPUT: $ARGUMENTS
Pass the design specs, Figma references, screens to implement, or "full app".

============================================================
PHASE 1: DESIGN SYSTEM  (/design-system)
============================================================

Follow the instructions defined in the `/design-system` skill exactly.

Extract or create the design system: tokens (colors, typography, spacing,
radii, shadows), component library, and token-based theming architecture
(CSS variables, theme provider, or equivalent).

Commit the design system. Record the token structure and theme architecture
-- Phases 2 and 3 build directly on top of it. If the project already has
a partial design system, extend it rather than replacing it.

============================================================
PHASE 2: RESPONSIVE LAYOUT  (/responsive)
============================================================

Follow the instructions defined in the `/responsive` skill exactly.

Make all screens responsive using the design system from Phase 1:
mobile/tablet/desktop breakpoints, fluid typography and spacing via tokens,
responsive navigation, 48dp touch targets, and media responsiveness.

IMPORTANT: Use tokens from Phase 1 for all values — do NOT hardcode pixels.
If tokens are missing breakpoint values, add them first. Commit changes.

============================================================
PHASE 3: DARK MODE  (/dark-mode)
============================================================

Follow the instructions defined in the `/dark-mode` skill exactly.

Add dark mode using Phase 1 tokens: dark palette mapped to same token names,
system preference detection, manual toggle with persistence, WCAG AA contrast
(4.5:1 text, 3:1 UI), and smooth transitions (no flash of wrong theme).

IMPORTANT: Dark mode must be a theme variant, NOT separate overrides.
Every color must come from a token. Fix any hardcoded colors. Commit changes.

============================================================
PHASE 4: UX AUDIT  (/ux)
============================================================

Follow the instructions defined in the `/ux` skill exactly.

Run a full UX audit on the result of Phases 1-3:
- Nielsen's 10 usability heuristics
- WCAG 2.1 AA accessibility (focus on contrast in both themes)
- Responsive behavior across breakpoints
- Dark mode consistency and readability
- Interaction patterns and feedback

Fix all issues found and commit the fixes. This is the quality gate
for the entire design implementation.

============================================================
OUTPUT
============================================================

## Design to Code Complete

| Phase | Skill | Status | Details |
|-------|-------|--------|---------|
| 1 | /design-system | PASS/FAIL | {N} tokens, {N} components created |
| 2 | /responsive | PASS/FAIL | {N} breakpoints, {N} screens adapted |
| 3 | /dark-mode | PASS/FAIL | {contrast ratio compliance, toggle method} |
| 4 | /ux | PASS/FAIL | {verdict}, {N} issues found and fixed |

**Design quality:** {POLISHED / SOLID / NEEDS WORK}
**Theme support:** Light + Dark, system preference + manual toggle
**Accessibility:** {WCAG AA COMPLIANT / PARTIAL / NON-COMPLIANT}

NEXT STEPS:
- Run `/visual-regression` to capture baseline screenshots
- Run `/full-test` for automated E2E + manual test plan
- Run `/polish` for a broader quality pass beyond design
