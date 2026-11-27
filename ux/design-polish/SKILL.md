---
name: design-polish
description: "Final quality pass before shipping: fixes alignment, spacing, type hierarchy, color consistency, interactive states and motion timing to match the existing design language. Triggers: 'polish the UI', 'make it pixel perfect', 'final design pass'."
version: "1.1.0"
category: ux
platforms:
  - CLAUDE_CODE
---

Find and fix the visual imperfections in this UI, making it consistent with the design language it already has. Infer intent from the existing code; this is a polish pass, not a redesign.

## Input

`$ARGUMENTS` (optional): components or pages to focus on ("dashboard only", "mobile nav", "card components"). Without it, polish the whole UI.

## 1. Extract the implicit design system

Identify the stack, styling approach and component library. Then catalog every value used for spacing, color, type (size/weight/line-height/letter-spacing), radius, shadow/elevation and motion (duration/easing). The most-used values per category are the canonical scale; everything else is a deviation (a lone `padding: 15px` on a 4/8/12/16/24 scale, one card at 6px radius when the rest use 8px). Rank deviations by frequency and visibility. If there is already a token file or theme, that is the source of truth.

## 2. Fix, in this order

**Spacing and alignment.** Snap off-scale values to the scale. Consistent section padding, max-widths and card padding; nested containers shouldn't double up padding. Icons vertically centered with adjacent text; labels, inputs and helper text aligned across form rows; list bullets/icons and text aligned. Use container queries for component-level spacing changes and `clamp()` for fluid spacing where the codebase supports them.

**Typography.** Each heading level is the same size/weight/line-height everywhere; one body size; one caption size. Body measure ≤ ~75ch. `text-wrap: balance` on headings, `text-wrap: pretty` on paragraphs. Uppercase labels get 0.05-0.1em letter-spacing. Collapse near-duplicate weights (500 vs 600). Fluid heading sizes with `clamp()`; tighter line-height for large type; body never below 14px (16px preferred on mobile).

**Color.** One value per role (no near-miss primaries), semantic colors used consistently, no mixed warm and cool grays, hover/active derived the same way everywhere (`color-mix(in oklch, ...)` works well). Check contrast at every surface boundary, including placeholders (4.5:1), icons and focus rings (3:1), and disabled states (muted but legible).

**Interactive states.** Every clickable element has hover, `:focus-visible`, active and disabled states, consistent across components. Prefer outline-based focus rings (`outline: 2px solid var(--focus-ring); outline-offset: 2px`) and never remove an outline without a replacement. Hover must not shift layout. Press feedback is immediate. Touch targets ≥ 44px (48 preferred).

**Motion.** A small duration scale (~100-150ms micro, 200-300ms state changes, 300-500ms page), one standard easing curve, `linear` only for progress. Transition named properties, not `all`. Entrances move from a natural direction; stagger at a consistent 50-100ms step. Everything respects `prefers-reduced-motion`. Use CSS scroll-driven animations (`animation-timeline: scroll()/view()`) instead of JS scroll listeners where supported.

**Native mobile.**

- Flutter: `EdgeInsets`/`BorderRadius` from theme constants, `Theme.of(context).textTheme` instead of inline `TextStyle`, `SafeArea` on root screens, sensible `resizeToAvoidBottomInset`.
- SwiftUI: spacing scale, Dynamic Type support, consistent `symbolRenderingMode`, `safeAreaInset`.
- Compose: `MaterialTheme.typography`, spacing tokens in `Modifier.padding`, `WindowInsets` for edge-to-edge.

**Micro-details.** Subpixel gaps in flex layouts, stretched images (use `aspect-ratio`/`object-fit`), text clipped without ellipsis, inconsistent icon sizes, leftover lorem ipsum, inconsistent button verbs ("Save" vs "Submit" vs "Confirm"), generic empty states, inconsistent error formatting. In dark mode: borders visible, shadows adjusted, image overlays adapted.

Make minimal edits in the existing code style; don't refactor unrelated code. Apply every clear fix; apply pure enhancements only where they can't regress anything. Anything needing a design decision or new assets goes in the report, not the code.

## 3. Verify

Run the build and linters (including a11y lint such as `eslint-plugin-jsx-a11y` if configured) and any visual tests (Storybook/Chromatic/Percy/golden tests). Revert any change that breaks the build. Confirm focus indicators survived and no color change lowered contrast. If you can run the app, look at the changed screens.

## Report

```
## Polish Pass Summary

| Category | Found | Fixed | Skipped (risk) |
|---|---|---|---|
| Spacing | | | |
| Alignment | | | |
| Typography | | | |
| Color | | | |
| Motion | | | |
| Hover/Focus | | | |
| Mobile | | | |
| Micro-details | | | |
| **Total** | | | |
```

Then: files modified with a one-line summary each; before/after for the 3 most impactful fixes; remaining items that need a decision; and systemic causes (for example "cards have five paddings, so a spacing token is missing"), suggesting `/design-system` when hardcoded values are widespread.
