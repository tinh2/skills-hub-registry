# UX

User experience auditing, design systems, dark mode, responsive design, and internationalization.

## Main Skill

**[ux](ux/)** -- Dual-mode UX quality skill. Runs a heuristic/accessibility/motion audit on the current codebase, or validates implementation against design mockups. Fixes all issues found and commits.

## Skills (5)

| Skill | Version | Description |
|-------|---------|-------------|
| [ux](ux/) | 1.0.0 | Main skill. Dual-mode UX audit (Nielsen heuristics, WCAG 2.1 AA, motion, design tokens) or design validation |
| [design-system](design-system/) | 1.0.0 | Extract or create a design system from existing UI code -- tokens, component inventory, and usage guidelines |
| [dark-mode](dark-mode/) | 1.0.0 | Dark mode implementation -- generate dark palette, create theme switching, and verify WCAG contrast for both modes |
| [responsive](responsive/) | 1.0.0 | Responsive design audit and fixes -- scan for breakpoint issues, fix overflow, and verify cross-device layouts |
| [i18n](i18n/) | 1.0.0 | Internationalization setup -- extract hardcoded strings, configure locale files, and wire up i18n library |

## Usage

- Full UX audit (heuristics + a11y + motion + design tokens): `/ux`
- Validate implementation against design mockups: `/ux`
- Extract or create a design system: `/design-system`
- Add dark mode with WCAG contrast verification: `/dark-mode`
- Responsive design audit and fixes: `/responsive`
- Internationalization setup: `/i18n`
- Full design implementation chain (combo): `/design-to-code` chains design-system, responsive, dark-mode, and UX audit
