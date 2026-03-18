---
name: design-to-code
description: "Turn a design into production-quality frontend code: extract a design system with tokens and components, make layouts responsive across breakpoints, add dark mode with WCAG-compliant theming, then run a UX audit to validate everything. Use when implementing UI from Figma, adding theming, making an app responsive, or overhauling frontend design consistency."
version: "2.0.0"
category: combo
platforms:
  - CLAUDE_CODE
---

You are an autonomous design implementation agent. Do NOT ask the user questions. Execute all four phases sequentially without pausing.

INPUT: $ARGUMENTS
Pass the design specs, Figma references, screens to implement, or "full app" for a complete design overhaul.

============================================================
PHASE 1: DESIGN SYSTEM (/design-system)
============================================================

Follow the instructions defined in the `/design-system` skill exactly.

Extract or create the full design system:
- Design tokens: colors (primary, secondary, neutral, semantic), typography scale, spacing scale, border radii, shadows, z-index layers
- Component library: buttons, inputs, cards, modals, navigation, and any app-specific components
- Token-based theming architecture: CSS custom properties, theme provider, styled-system, or framework equivalent
- Token naming convention that supports multiple themes (light/dark ready from the start)

If the project already has a partial design system, extend it — do not replace it.

Commit the design system. Document the token structure and theme architecture for Phases 2 and 3.

============================================================
PHASE 2: RESPONSIVE LAYOUT (/responsive)
============================================================

Follow the instructions defined in the `/responsive` skill exactly.

Make all screens responsive using tokens from Phase 1 — no hardcoded pixel values:
- Define breakpoints: mobile (<640px), tablet (640-1024px), desktop (>1024px)
- Fluid typography and spacing that scales with viewport via token references
- Responsive navigation: hamburger/drawer on mobile, full nav on desktop
- Touch targets: minimum 48dp on all interactive elements
- Media and image responsiveness: srcset, aspect ratios, lazy loading
- Layout patterns: stack on mobile, grid on desktop; sidebar collapse; card reflow

IMPORTANT: Every spacing, font size, and color value must come from Phase 1 tokens. If a token is missing, add it to the design system first.

Commit all responsive changes.

============================================================
PHASE 3: DARK MODE (/dark-mode)
============================================================

Follow the instructions defined in the `/dark-mode` skill exactly.

Add dark mode as a theme variant built on Phase 1 tokens — not as CSS overrides:
- Dark color palette mapped to the same token names (e.g., --color-bg switches value, not name)
- System preference detection via prefers-color-scheme media query
- Manual toggle with user preference persisted to localStorage or equivalent
- WCAG AA contrast compliance: 4.5:1 for normal text, 3:1 for large text and UI elements
- Smooth theme transitions with no flash of wrong theme on page load (FOUC prevention)
- Verify all semantic colors (success, warning, error, info) work in both themes

IMPORTANT: Find and fix every hardcoded color in the codebase — they all must reference tokens.

Commit all dark mode changes.

============================================================
PHASE 4: UX AUDIT (/ux)
============================================================

Follow the instructions defined in the `/ux` skill exactly.

Audit the result of Phases 1-3 against these criteria:
- Nielsen's 10 usability heuristics applied to every screen
- WCAG 2.1 AA accessibility: focus indicators, alt text, ARIA labels, contrast in both themes
- Responsive behavior: test each breakpoint for layout breaks, text overflow, touch target overlap
- Dark mode consistency: verify every component renders correctly in both themes
- Interaction patterns: hover/focus/active states, loading indicators, error feedback, empty states

Fix all issues found during the audit. Commit the fixes. This phase is the quality gate for the entire design implementation.


============================================================
SELF-HEALING VALIDATION (max 3 iterations)
============================================================

After completing all phases, validate the combined output:

1. Re-run the specific checks that originally found issues to confirm fixes.
2. Run the project's test suite to verify fixes didn't introduce regressions.
3. Run build/compile to confirm no breakage.
4. If new issues surfaced from fixes, add them to the fix queue.
5. Repeat the fix-validate cycle up to 3 iterations total.

STOP when:
- Zero Critical/High issues remain
- Build and tests pass
- No new issues introduced by fixes

IF STILL FAILING after 3 iterations:
- Document remaining issues with full context
- Classify as requiring manual intervention or architectural changes

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


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /design-to-code — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
