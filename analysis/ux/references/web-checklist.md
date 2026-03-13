# Web Platform Checklist

Reference file for `/ux` skill — web-specific heuristics, accessibility patterns, and design system conventions.

## Project Detection

- `package.json` with React, Next.js, Vue, Angular, Svelte, or similar framework.
- CSS/design system: `src/styles/`, `tailwind.config.*`, CSS modules, styled-components, etc.
- Routes: file-based routing (Next.js `app/` or `pages/`), router config (React Router, Vue Router).
- Shared components: `src/components/`, `src/ui/`, `src/shared/`.

## Screen Discovery

Read the router config or page directory structure.
For file-based routing (Next.js), scan `app/` or `pages/` directories.
For config-based routing (React Router, Vue Router), read the route definitions.

## Accessibility (WCAG 2.1 AA)

### Semantic HTML
- Use semantic elements: `<nav>`, `<main>`, `<article>`, `<section>`, `<aside>`, `<header>`, `<footer>`.
- Every `<img>` must have an `alt` attribute. Decorative images use `alt=""`.
- Every `<button>` and `<a>` must have accessible text (visible label, `aria-label`, or `aria-labelledby`).
- Form inputs must have associated `<label>` elements or `aria-label`.
- Use ARIA roles, states, and properties only when native HTML semantics are insufficient.
- Heading hierarchy must be logical (`h1` > `h2` > `h3`, no skipped levels).

### Color & Contrast
- Normal text (below 18px or 14px bold): minimum 4.5:1 contrast ratio.
- Large text (18px+ or 14px+ bold): minimum 3:1 contrast ratio.
- Non-text elements (icons, borders, focus rings): minimum 3:1 against background.
- Do not rely on color alone to convey information.
- Check contrast in both light and dark mode if applicable.

### Touch/Click Targets
- Interactive elements: minimum 44x44 CSS pixels (WCAG 2.5.8).
- Adjacent targets: sufficient spacing to prevent mis-taps.
- Links within text: ensure sufficient padding or line-height for tap area.

### Keyboard Navigation
- All interactive elements reachable via Tab key.
- Focus order matches visual reading order.
- Focus indicators clearly visible (never `outline: none` without replacement).
- Escape key closes modals, dropdowns, and overlays.
- Skip-to-content link at top of page.
- No keyboard traps.

### Motion & Animation
- Respect `prefers-reduced-motion` media query.
- No content that flashes more than 3 times per second.
- Auto-playing animations must be pausable.
- Parallax and scroll-triggered animations must degrade gracefully.

### Screen Reader
- Dynamic content updates use `aria-live` regions.
- Loading states announced to assistive technology.
- Error messages associated with form fields via `aria-describedby`.
- Modal dialogs trap focus and use `role="dialog"` with `aria-modal="true"`.

## Design System Consistency

### CSS Custom Properties
- Every color reference must use CSS custom properties (variables) from the design system.
  Flag any hardcoded hex/rgb/hsl values in component stylesheets.
- Every font size, weight, and family must use design tokens.
  Flag any hardcoded font values not from the design system.
- Every spacing value must use the spacing scale (CSS variables or utility classes).
  Flag magic number padding/margin values.

### Component Conventions
- Consistent button hierarchy (primary, secondary, tertiary variants).
- Consistent card, input, modal, and navigation patterns across pages.
- Icons from a consistent library (do not mix icon sets arbitrarily).
- Loading/error/empty states using shared components.

### Motion Choreography
- Page transitions consistent (if using client-side routing).
- Hover/focus states on all interactive elements.
- Micro-interactions: button feedback, form validation feedback, toast notifications.
- Transition durations: small (100-200ms), medium (200-350ms), large (350-500ms).
- Easing: `ease-in-out` for most, `ease-out` for enter, `ease-in` for exit.

### Responsive Design
- Mobile-first or responsive breakpoints covering phone, tablet, desktop.
- No horizontal scrollbar at any supported viewport width.
- Touch-friendly on mobile (no hover-only interactions).
- Images use `srcset` or responsive sizing.
- Text wraps properly at all widths.

## Fix Commit Prefixes

- `fix(ux): [page] add missing loading state`
- `fix(a11y): [page] add alt text and aria labels`
- `fix(design): [page] replace hardcoded colors with CSS variables`
- `fix(motion): [page] add hover states and page transitions`

## Rules

- Use CSS custom properties from the design system. Never introduce hardcoded color or font values in component stylesheets.
- When adding ARIA labels, use concise descriptive text. Do not redundantly include the element role.
- When fixing contrast, prefer adjusting the foreground (text/icon) color over the background unless the background is the problem.
- When adding animations, keep durations 150-400ms. Use standard easing. Do not animate elements that are already on screen and static.
- Respect `prefers-reduced-motion` in all animation code.
