---
name: dark-mode
description: "Implement complete dark mode in any frontend (CSS variables, Tailwind, Flutter, MUI, Chakra, CSS-in-JS): a real dark palette, a system/light/dark toggle with persistence and no flash, token migration, and contrast checks in both themes. Triggers: 'add dark mode', 'dark theme', 'theme toggle'."
version: "2.1.0"
category: ux
platforms:
  - CLAUDE_CODE
---

Implement a complete, designed dark mode: a real dark palette (not inverted colors), theme switching with system detection and persistence, every color reference on theme tokens, and WCAG AA contrast in both themes.

## Input

`$ARGUMENTS` (optional): palette preferences or a reference design; toggle behavior `system-only` / `manual-only` / `both` (default `both`); persistence (default: what the stack already uses, else localStorage / SharedPreferences); scope (default: the whole project).

## 1. Understand what exists

Detect the framework and theme mechanism, and any existing dark theme, `prefers-color-scheme` usage, toggle, or `data-theme`/class switching. Extend existing definitions rather than replacing them. Catalog the light palette by role (page, surface, overlay and input backgrounds; primary, secondary, disabled and placeholder text; borders, focus, dividers; brand scales; semantic colors; shadows; interactive states) and list the foreground/background pairs that occur together. Those pairs are what you will contrast-check.

## 2. Design the dark palette

- **Surfaces:** a dark gray base (around `#121212`, not pure black) with 2-3 elevation levels that get lighter as they rise (roughly +5%, +8%, +11% white). Elevation reads through surface lightness and subtle borders, because shadows nearly disappear on dark backgrounds.
- **Text:** high, medium and low emphasis (about 87%, 60% and 38% white, or equivalent solid colors), each passing AA on every surface it sits on.
- **Brand and semantic colors:** lighter and slightly desaturated so they don't vibrate, still recognizably the brand. Working in `oklch()` makes it easy to raise lightness while keeping hue.
- **Inputs, focus rings, charts:** inputs on an elevated surface with visible borders; a lighter focus ring; chart palettes, axes and gridlines re-tuned for the dark background.

## 3. Implement

- **CSS variables:** dark values under `[data-theme="dark"]` (or a `.dark` class) plus a `prefers-color-scheme` fallback; `light-dark()` is fine for simple pairs. Set `color-scheme: light dark` (or the resolved scheme) so native controls and scrollbars follow the theme.
- **Tailwind:** v4 uses `@custom-variant dark (&:where(.dark, .dark *));` in CSS for class-based switching; v3 uses `darkMode: 'class'` (or `'selector'`). Prefer CSS-variable-backed colors over sprinkling `dark:` on every element.
- **Next.js:** `next-themes` (handles SSR and the no-flash script). **MUI:** `createTheme` with `colorSchemes` / `palette.mode`. **Chakra:** its color-mode setup (v3 pairs with `next-themes`). **styled-components/emotion:** a dark theme object with the same shape.
- **Flutter:** a dark `ColorScheme` (for example `ColorScheme.fromSeed(seedColor: ..., brightness: Brightness.dark)`) with component themes, `MaterialApp(theme:, darkTheme:, themeMode:)`, the mode held in the app's state management and loaded from `SharedPreferences` before `runApp`.

Switching: System / Light / Dark when both modes are wanted. Follow live system changes (`matchMedia(...).addEventListener('change', ...)`). Persist the choice. On the web, prevent the flash of the wrong theme with a small blocking script in `<head>` that applies the stored theme before first paint.

Commit: `feat(theme): implement dark mode with system detection and manual toggle`.

## 4. Migrate color references

Replace hardcoded colors everywhere (`#333` → `var(--text-primary)`, `Colors.white` → `Theme.of(context).colorScheme.surface`, inline style colors). Handle the cases that usually get missed:

- logos and images with baked-in light backgrounds (dark variants, `<picture>` with `prefers-color-scheme` sources)
- SVG fills (use `currentColor`)
- form inputs and native controls
- third-party components (use their theming API first, CSS overrides second)
- embedded maps and charts
- email/PDF templates that must stay light

Never use `filter: invert()` as the strategy.

Commit: `fix(theme): migrate color references to theme-aware tokens`.

## 5. Verify

- Compute contrast for every pair in both themes: 4.5:1 normal text, 3:1 large text (≥ 24px, or ≥ 18.66px bold), 3:1 UI components and focus indicators. Fix by adjusting the foreground first.
- Run analyzers, type checks, linters, tests and the build.
- Exercise the flow: system preference on first load, manual override wins, the choice survives reload/restart, no flash on load.
- If the app runs, screenshot key screens in both themes and look at them.

## Report

```
## Dark Mode Implementation Complete

### Framework / Theme system / Toggle / Persistence

### Files Created/Modified
| File | Purpose |
|---|---|

### Dark Palette
| Token | Light | Dark | Category |
|---|---|---|---|

### Contrast Verification
| Pair | Light Ratio | Dark Ratio | Status |
|---|---|---|---|

### Summary
- tokens migrated, hardcoded colors replaced, contrast failures found and fixed
- special cases handled: images, forms, third-party, charts
- anything not verified visually
```

Useful follow-ups: `/responsive`, `/ux`, `/design-system`, and checking on a real OLED device.
