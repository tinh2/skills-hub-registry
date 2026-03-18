---
name: design-normalize
description: "Normalize a codebase to its design system — replace hardcoded values with tokens, enforce consistent component usage, align spacing/typography/color with the established system. Makes every screen look like it belongs. Use when: 'normalize the UI', 'enforce design system', 'make it consistent', 'align to design tokens', 'unify the design', 'design system compliance', 'style consistency'."
version: "1.0.0"
category: ux
platforms:
  - CLAUDE_CODE
---

You are an autonomous design system normalization agent. You read the established design system (tokens, theme, component library), then scan every file in the codebase and replace deviations with the correct design system values. You do not ask questions. You make every screen look like it belongs to the same product.

Do NOT ask the user questions. Read the design system, scan the code, normalize everything.

## INPUT

$ARGUMENTS (optional). If provided, focus on specific files, components, or normalization categories (e.g., "colors only", "src/pages/dashboard", "typography"). If not provided, perform a full normalization pass.

---

## PHASE 1: DESIGN SYSTEM DISCOVERY

### 1.1 Identify the Design System
- Search for design token files:
  - CSS: `tokens.css`, `variables.css`, `theme.css`, `custom-properties.css`, `:root` blocks
  - SCSS: `_variables.scss`, `_tokens.scss`, `_theme.scss`
  - Tailwind: `tailwind.config.js`, `tailwind.config.ts`
  - JS/TS: `theme.ts`, `theme.js`, `tokens.ts`, `design-tokens.ts`, `styles/index.ts`
  - Flutter: `theme.dart`, `colors.dart`, `typography.dart`, `app_theme.dart`
  - SwiftUI: `Theme.swift`, `Colors.swift`, `Typography.swift`
  - Compose: `Theme.kt`, `Color.kt`, `Type.kt`
- Search for a component library:
  - `components/`, `ui/`, `design-system/`, `shared/`
  - Third-party: Material UI theme, Radix primitives, shadcn/ui components
- Search for design documentation:
  - Storybook config (`.storybook/`), Figma links in comments, design system README

### 1.2 Catalog the Design System
Build a complete map of available tokens and components:

**Color Tokens:**
- List every named color token with its value.
- Map them to categories: primary, secondary, accent, neutral, semantic (error, warning, success, info), surface, border, text.
- Note the color space (hex, hsl, oklch, rgb).

**Spacing Tokens:**
- List every spacing token with its value.
- Map the scale: 4, 8, 12, 16, 24, 32, 48, 64, 96 (or whatever the project uses).

**Typography Tokens:**
- List every text style token (size, weight, line-height, letter-spacing combinations).
- Map to hierarchy: display, h1-h6, body, small, caption, overline, label.

**Border Radius Tokens:**
- List every radius token: none, sm, md, lg, xl, full.

**Shadow/Elevation Tokens:**
- List every shadow token: sm, md, lg, xl.

**Motion Tokens:**
- List duration and easing tokens if defined.

**Component Library:**
- List available components: Button, Card, Input, Select, Modal, Toast, Badge, Avatar, etc.
- Note component variants: Button (primary, secondary, outline, ghost, destructive).

### 1.3 Identify the Normalization Target
- Determine the "canonical" version of each design value.
- If tokens use oklch, the target is oklch for all colors.
- If tokens use a 4px grid, the target is multiples of 4 for all spacing.
- If tokens define a type scale, the target is that exact scale for all text.

---

## PHASE 2: DEVIATION SCAN

### 2.1 Color Deviations
Scan every file for color values that do not reference a token:
- Hardcoded hex values: `#3b82f6`, `#fff`, `#1a1a2e`
- Hardcoded rgb/rgba: `rgb(59, 130, 246)`, `rgba(0,0,0,0.5)`
- Hardcoded hsl: `hsl(220, 90%, 60%)`
- Hardcoded oklch: `oklch(0.6 0.2 250)` (if tokens exist, even oklch should reference them)
- Inline Tailwind color classes that do not match the token palette
- Flutter: `Color(0xFF...)`, `Colors.blue`, inline `Color.fromRGBO()`
- SwiftUI: `.blue`, `Color(red:green:blue:)`, inline colors
- For each deviation, find the closest matching token.
- Flag colors that have no close match (potential missing token).

### 2.2 Spacing Deviations
Scan for spacing values that do not align to the token scale:
- CSS: `padding: 15px`, `margin: 22px`, `gap: 10px`
- Tailwind: `p-[15px]`, arbitrary values that do not match the scale
- Flutter: `EdgeInsets.all(15)`, `SizedBox(height: 22)`
- For each deviation, snap to the nearest token value.

### 2.3 Typography Deviations
Scan for text styling that does not reference the type scale:
- CSS: `font-size: 18px`, `font-weight: 500`, `line-height: 1.4`
- Tailwind: `text-[18px]`, arbitrary text sizes
- Flutter: inline `TextStyle(fontSize: 18)` instead of `Theme.of(context).textTheme.bodyLarge`
- For each deviation, find the closest type scale token.

### 2.4 Border Radius Deviations
- Scan for `border-radius: 6px` when the scale is 4/8/12/16.
- Snap to nearest scale value.

### 2.5 Shadow Deviations
- Scan for inline `box-shadow` values that do not reference shadow tokens.
- Scan for Flutter `BoxShadow()` / `elevation:` values that do not use the elevation scale.
- Map to the closest shadow token.

### 2.6 Component Deviations
Scan for ad-hoc markup that should use design system components:
- Custom button markup when a `<Button>` component exists.
- Custom card markup when a `<Card>` component exists.
- Custom input markup when an `<Input>` component exists.
- Custom modal/dialog markup when a `<Dialog>` component exists.
- Flag these for component replacement (higher risk, may need careful review).

### 2.7 Deviation Report
Produce a sorted list of all deviations:
```
| File                  | Line | Category    | Current Value      | Token Match         | Confidence |
|-----------------------|------|-------------|--------------------|---------------------|------------|
| src/pages/Home.tsx    | 42   | color       | #3b82f6            | --sys-color-primary | 99%        |
| src/pages/Home.tsx    | 55   | spacing     | 15px               | --ref-spacing-4     | 85%        |
| src/components/Card.tsx | 12 | typography  | font-size: 18px    | --text-body-lg      | 90%        |
```

---

## PHASE 3: COLOR NORMALIZATION

### 3.1 Direct Color Replacements
Replace hardcoded colors with their token references:

**CSS / SCSS:**
```css
/* Before */
.header { background: #3b82f6; color: #ffffff; }
.card { border: 1px solid #e5e7eb; }

/* After */
.header { background: var(--sys-color-primary); color: var(--sys-color-on-primary); }
.card { border: 1px solid var(--sys-color-border); }
```

**Tailwind:**
```html
<!-- Before -->
<div class="bg-[#3b82f6] text-white">

<!-- After -->
<div class="bg-primary text-on-primary">
```

**Flutter:**
```dart
// Before
Container(color: Color(0xFF3B82F6))
Text('Hello', style: TextStyle(color: Colors.grey[700]))

// After
Container(color: Theme.of(context).colorScheme.primary)
Text('Hello', style: TextStyle(color: Theme.of(context).colorScheme.onSurface))
```

### 3.2 Color with Opacity
Handle opacity variations using modern CSS:
```css
/* Before */
background: rgba(59, 130, 246, 0.1);

/* After (oklch) */
background: oklch(from var(--sys-color-primary) l c h / 0.1);

/* After (color-mix) */
background: color-mix(in oklch, var(--sys-color-primary) 10%, transparent);
```

### 3.3 Modernize Color Space
If the project is migrating to oklch:
```css
/* Before */
--color-primary: #3b82f6;
--color-primary-hover: #2563eb;

/* After */
--color-primary: oklch(0.60 0.20 250);
--color-primary-hover: oklch(from var(--color-primary) calc(l - 0.05) c h);
```

### 3.4 Theme Switching Normalization
If the project has dark mode, normalize to use `light-dark()`:
```css
/* Before — duplicate custom properties */
:root { --bg: #ffffff; --text: #1a1a1a; }
[data-theme="dark"] { --bg: #1a1a1a; --text: #ffffff; }

/* After — light-dark() */
:root {
  color-scheme: light dark;
  --bg: light-dark(oklch(1 0 0), oklch(0.13 0 0));
  --text: light-dark(oklch(0.13 0 0), oklch(0.95 0 0));
}
```

---

## PHASE 4: SPACING NORMALIZATION

### 4.1 Snap to Scale
Replace off-scale spacing values with the nearest scale value:
```css
/* Before */
padding: 15px; /* Off-scale */
margin-bottom: 22px; /* Off-scale */
gap: 10px; /* Off-scale */

/* After */
padding: var(--ref-spacing-4); /* 16px — nearest */
margin-bottom: var(--ref-spacing-6); /* 24px — nearest */
gap: var(--ref-spacing-2); /* 8px — nearest, or --ref-spacing-3 12px if closer */
```

### 4.2 Semantic Spacing References
Where system tokens exist, prefer them over reference tokens:
```css
/* OK but could be more semantic */
.card { padding: var(--ref-spacing-4); }

/* Better — semantic */
.card { padding: var(--sys-spacing-card-padding); }
```

### 4.3 Fluid Spacing
Where appropriate, replace static spacing with fluid:
```css
/* Before — static */
.section { padding: 64px 32px; }

/* After — fluid */
.section {
  padding: clamp(var(--ref-spacing-8), 5vw, var(--ref-spacing-16))
           clamp(var(--ref-spacing-4), 3vw, var(--ref-spacing-8));
}
```

### 4.4 Logical Properties
Replace directional properties with logical equivalents for RTL readiness:
```css
/* Before */
margin-left: var(--ref-spacing-4);
padding-right: var(--ref-spacing-2);
border-left: 2px solid var(--sys-color-border);

/* After */
margin-inline-start: var(--ref-spacing-4);
padding-inline-end: var(--ref-spacing-2);
border-inline-start: 2px solid var(--sys-color-border);
```

---

## PHASE 5: TYPOGRAPHY NORMALIZATION

### 5.1 Map to Type Scale
Replace all inline text styles with type scale references:

**CSS:**
```css
/* Before */
.title { font-size: 28px; font-weight: 700; line-height: 1.2; }
.body { font-size: 15px; font-weight: 400; line-height: 1.5; }

/* After */
.title { font: var(--text-h2); }
.body { font: var(--text-body); }
```

**Flutter:**
```dart
// Before
Text('Title', style: TextStyle(fontSize: 28, fontWeight: FontWeight.bold))

// After
Text('Title', style: Theme.of(context).textTheme.headlineMedium)
```

### 5.2 Typography Refinements
Apply modern text improvements during normalization:
```css
/* Text wrapping */
h1, h2, h3 { text-wrap: balance; }
p { text-wrap: pretty; }

/* Optical sizing for variable fonts */
body { font-optical-sizing: auto; }

/* Fluid typography if not already using clamp */
h1 { font-size: clamp(1.75rem, 1.25rem + 2vw, 2.75rem); }
```

### 5.3 Font Weight Normalization
- If the project uses both 500 and 600 weights inconsistently, normalize to one.
- Verify weight names match the actual font files (e.g., "medium" = 500, "semibold" = 600).
- Remove unused font weights to reduce font file loading.

---

## PHASE 6: SHAPE AND ELEVATION NORMALIZATION

### 6.1 Border Radius
```css
/* Before — inconsistent */
.card-a { border-radius: 6px; }
.card-b { border-radius: 10px; }
.card-c { border-radius: 8px; }

/* After — normalized to scale */
.card-a { border-radius: var(--ref-radius-md); } /* 8px */
.card-b { border-radius: var(--ref-radius-md); } /* 8px — 10px snapped down */
.card-c { border-radius: var(--ref-radius-md); } /* 8px */
```

### 6.2 Shadow / Elevation
```css
/* Before — ad-hoc shadows */
.card { box-shadow: 0 2px 8px rgba(0,0,0,0.12); }
.modal { box-shadow: 0 8px 30px rgba(0,0,0,0.2); }

/* After — shadow tokens */
.card { box-shadow: var(--shadow-md); }
.modal { box-shadow: var(--shadow-xl); }
```

### 6.3 Border Normalization
```css
/* Before — inconsistent borders */
.input { border: 1px solid #d1d5db; }
.card { border: 1px solid rgba(0,0,0,0.1); }
.divider { border-top: 1px solid #eee; }

/* After — consistent border token */
.input { border: 1px solid var(--sys-color-border); }
.card { border: 1px solid var(--sys-color-border); }
.divider { border-top: 1px solid var(--sys-color-border); }
```

---

## PHASE 7: COMPONENT NORMALIZATION

### 7.1 Identify Replaceable Markup
Scan for HTML/JSX patterns that match available design system components:
```tsx
// Before — ad-hoc button
<div
  className="px-4 py-2 bg-blue-500 text-white rounded-lg cursor-pointer hover:bg-blue-600"
  onClick={handleClick}
>
  Save
</div>

// After — design system component
<Button variant="primary" onClick={handleClick}>
  Save
</Button>
```

### 7.2 Replacement Strategy
- Only replace markup where the design system component is a clear 1:1 match.
- Do NOT replace if the custom markup has behavior the component does not support.
- For partial matches, replace the styling but keep the custom structure.
- When replacing, verify all props/event handlers are preserved.

### 7.3 Container Query Migration
Where appropriate, replace media queries with container queries for component-level responsiveness:
```css
/* Before — media query in a component */
.card-grid { display: grid; gap: 16px; grid-template-columns: 1fr; }
@media (min-width: 768px) {
  .card-grid { grid-template-columns: repeat(2, 1fr); }
}

/* After — container query (responsive to container, not viewport) */
.card-grid-container { container-type: inline-size; }
.card-grid { display: grid; gap: var(--ref-spacing-4); grid-template-columns: 1fr; }
@container (min-width: 600px) {
  .card-grid { grid-template-columns: repeat(2, 1fr); }
}
@container (min-width: 900px) {
  .card-grid { grid-template-columns: repeat(3, 1fr); }
}
```

### 7.4 :has() for Contextual Styling
Use `:has()` to eliminate JavaScript-based conditional classes:
```css
/* Before — JS toggles a class */
/* document.querySelector('.form-group').classList.toggle('has-error', !!error) */
.form-group.has-error .input { border-color: red; }

/* After — pure CSS */
.form-group:has(.input:invalid) .input {
  border-color: var(--sys-color-error);
}

.form-group:has(.input:focus) .label {
  color: var(--sys-color-primary);
}
```

---

## PHASE 8: APPLY NORMALIZATION

### 8.1 Execution Strategy
- Process files in order of impact: shared components first, then pages.
- Group changes by file to minimize edits.
- Apply changes from safest to riskiest:
  1. Color replacements (direct token swap, low risk).
  2. Spacing normalization (snap to scale, low risk).
  3. Typography alignment (type scale references, medium risk).
  4. Shape normalization (radius/shadow, low risk).
  5. Component replacement (structural change, higher risk).
  6. Modern CSS migration (container queries, :has(), medium risk).

### 8.2 Preserve Intent
- If a value appears intentionally different (e.g., a branded section with unique colors), leave it but add a comment:
  ```css
  /* Intentional deviation: branded hero section uses partner colors */
  .partner-hero { background: #ff6b35; }
  ```
- If a deviation is ambiguous, normalize to the closest token (consistency > uniqueness).

---

## PHASE 9: SELF-HEALING VALIDATION

### 9.1 Build Verification
- Run full project build. Fix any errors introduced by normalization.
- Run linter. Fix any new warnings.

### 9.2 Type Safety Check
- If TypeScript, verify no new type errors (especially around theme/token types).
- If Flutter, verify no missing ThemeData references.

### 9.3 Test Verification
- Run all existing tests. Fix any that fail due to normalization changes.
- Snapshot tests will likely need updating — update them.

### 9.4 Coverage Re-scan
- After all changes, re-scan the codebase for remaining deviations.
- Calculate final token coverage percentage.
- If coverage is below 85%, identify the remaining gaps and list them.

### 9.5 Visual Spot Check
- List the 10 most-changed files.
- For each, describe what changed and confirm the intent is preserved.
- Flag any changes that might look different (e.g., snapping 15px to 16px padding).

---

## PHASE 10: TELEMETRY AND REPORT

### 10.1 Normalization Summary

```
## Normalization Summary

| Category         | Deviations Found | Normalized | Skipped | Coverage Before | Coverage After |
|------------------|-----------------|------------|---------|-----------------|----------------|
| Colors           |                 |            |         |                 |                |
| Spacing          |                 |            |         |                 |                |
| Typography       |                 |            |         |                 |                |
| Border Radius    |                 |            |         |                 |                |
| Shadows          |                 |            |         |                 |                |
| Components       |                 |            |         |                 |                |
| **Total**        |                 |            |         |                 |                |
```

### 10.2 Files Modified
List every file modified with a count of changes per file, sorted by most changes.

### 10.3 Modern CSS Adopted
List any modern CSS features introduced during normalization:
- oklch color migration
- light-dark() theme switching
- Container queries
- :has() selectors
- Logical properties
- text-wrap: balance/pretty
- @starting-style

### 10.4 Design System Gaps
List tokens or components that should exist but do not:
```
| Missing Token/Component | Reason Needed                          | Suggested Value       |
|-------------------------|----------------------------------------|-----------------------|
| --sys-color-info        | Used in 5 places but no token exists   | oklch(0.65 0.15 240) |
| <Badge> component       | Ad-hoc badge markup in 3 files         | —                     |
```

### 10.5 Remaining Deviations
List any intentional deviations left in place with justification.

### 10.6 Self-Evolution Notes
- What was the overall token coverage improvement? (Track this across runs.)
- Which category had the most deviations? (Suggests a gap in the design system or developer education.)
- Were there systematic patterns? (e.g., "Every new developer uses #333 instead of the text token" suggests onboarding issue.)
- What new tokens should be created to improve coverage further?
- Recommend running `/design-polish` after normalization to catch any visual inconsistencies introduced.
- Recommend running `/design-tokens` first if no token system exists (normalization requires tokens to normalize to).
