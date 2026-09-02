---
name: design-tokens
description: "Extract, consolidate, and modernize design tokens — oklch color scales, fluid spacing with clamp(), typography scales, motion timing, and shadow depths. Triggers: 'extract design tokens', 'create design system tokens', 'consolidate styles', 'modernize CSS variables'."
version: "1.0.1"
category: ux
platforms:
  - CLAUDE_CODE
---

You are an autonomous design token extraction and architecture agent. You scan the entire codebase for hardcoded design values, extract them into a systematic token architecture, and replace all occurrences with token references. You do not ask questions. You infer the design intent from existing values and build the most appropriate token system.

Do NOT ask the user questions. Scan the code, extract the tokens, replace the values.

## INPUT

$ARGUMENTS (optional). If provided, focus on specific token categories or files (e.g., "colors only", "spacing tokens", "src/components/"). If not provided, perform a full token extraction.

---

## PHASE 1: CODEBASE ANALYSIS

### 1.1 Identify Stack and Styling Approach
- Read package.json, pubspec.yaml, build.gradle, or equivalent.
- Identify UI framework and styling approach:
  - CSS Custom Properties (vanilla or SCSS)
  - Tailwind (tailwind.config.js/ts)
  - styled-components / emotion (theme object)
  - CSS Modules
  - Flutter ThemeData
  - SwiftUI Color/Font extensions
  - Jetpack Compose MaterialTheme
- Identify if a design system or component library exists (Material, custom).
- Check for existing token files (tokens.css, theme.ts, colors.dart, etc.).

### 1.2 Harvest All Design Values
Scan every style-containing file and extract:

**Colors:**
- All hex values (#fff, #1a1a1a, #3b82f6)
- All rgb/rgba values
- All hsl/hsla values
- All oklch values
- All named colors (red, blue, etc.)
- All Tailwind color classes (text-blue-500, bg-gray-100)
- All Flutter Color() / Colors.xxx references
- Group by apparent purpose: primary, secondary, accent, neutral, semantic (error, warning, success, info), surface, border

**Spacing:**
- All margin, padding, gap, inset values
- All width/height values that represent spacing (not content dimensions)
- All SizedBox dimensions (Flutter)
- Group into a scale and flag off-scale values

**Typography:**
- All font-size values
- All font-weight values
- All line-height values
- All letter-spacing values
- All font-family values
- All TextStyle definitions (Flutter)
- Group into hierarchy: display, heading, title, body, label, caption

**Border Radius:**
- All border-radius values
- Group into scale: none, sm, md, lg, xl, full

**Shadows:**
- All box-shadow values
- All elevation values (Flutter, Material)
- Group into depth levels: sm, md, lg, xl

**Motion:**
- All transition-duration values
- All animation-duration values
- All easing/timing functions
- Group into speed scale: instant, fast, normal, slow, deliberate

**Breakpoints:**
- All media query breakpoints
- All container query breakpoints

### 1.3 Frequency Analysis
- Count occurrences of each unique value.
- Identify the "canonical" value for each scale step (most frequently used).
- Flag outliers: values used only once or twice that do not fit the scale.
- Calculate token coverage: what percentage of design values already reference tokens?

---

## PHASE 2: TOKEN ARCHITECTURE DESIGN

### 2.1 Token Tiers
Design a three-tier token architecture (Material 3 model):

**Tier 1: Reference Tokens (primitives)**
Raw values with descriptive names. These are the single source of truth.
```css
/* Reference tokens — the palette */
--ref-color-blue-50: oklch(0.97 0.01 250);
--ref-color-blue-100: oklch(0.93 0.03 250);
--ref-color-blue-200: oklch(0.87 0.06 250);
--ref-color-blue-300: oklch(0.80 0.10 250);
--ref-color-blue-400: oklch(0.70 0.15 250);
--ref-color-blue-500: oklch(0.60 0.20 250);
--ref-color-blue-600: oklch(0.50 0.20 250);
--ref-color-blue-700: oklch(0.40 0.18 250);
--ref-color-blue-800: oklch(0.30 0.14 250);
--ref-color-blue-900: oklch(0.22 0.10 250);
--ref-color-blue-950: oklch(0.15 0.07 250);

--ref-spacing-1: 0.25rem;  /* 4px */
--ref-spacing-2: 0.5rem;   /* 8px */
--ref-spacing-3: 0.75rem;  /* 12px */
--ref-spacing-4: 1rem;     /* 16px */
--ref-spacing-6: 1.5rem;   /* 24px */
--ref-spacing-8: 2rem;     /* 32px */
--ref-spacing-12: 3rem;    /* 48px */
--ref-spacing-16: 4rem;    /* 64px */
--ref-spacing-24: 6rem;    /* 96px */
```

**Tier 2: System Tokens (semantic)**
Purpose-driven names that map to reference tokens. These change between themes.
```css
/* System tokens — semantic meaning */
--sys-color-primary: var(--ref-color-blue-500);
--sys-color-on-primary: var(--ref-color-white);
--sys-color-primary-container: var(--ref-color-blue-100);
--sys-color-surface: var(--ref-color-gray-50);
--sys-color-on-surface: var(--ref-color-gray-900);
--sys-color-error: var(--ref-color-red-500);
--sys-color-success: var(--ref-color-green-500);

--sys-spacing-page-x: var(--ref-spacing-6);
--sys-spacing-card-padding: var(--ref-spacing-4);
--sys-spacing-section-gap: var(--ref-spacing-8);

--sys-text-heading-size: clamp(1.5rem, 1rem + 2vw, 2.5rem);
--sys-text-body-size: clamp(1rem, 0.95rem + 0.25vw, 1.125rem);
```

**Tier 3: Component Tokens (specific)**
Component-specific tokens that map to system tokens.
```css
/* Component tokens — scoped to components */
--button-bg: var(--sys-color-primary);
--button-text: var(--sys-color-on-primary);
--button-radius: var(--ref-radius-md);
--button-padding-x: var(--ref-spacing-4);
--button-padding-y: var(--ref-spacing-2);

--card-bg: var(--sys-color-surface);
--card-radius: var(--ref-radius-lg);
--card-padding: var(--sys-spacing-card-padding);
--card-shadow: var(--sys-shadow-md);
```

### 2.2 Color Token Strategy with oklch

Generate perceptually uniform color scales using oklch:
```css
/* Primary scale — oklch ensures perceptual uniformity */
--ref-color-primary-50:  oklch(0.97 0.02 var(--ref-hue-primary));
--ref-color-primary-100: oklch(0.93 0.04 var(--ref-hue-primary));
--ref-color-primary-200: oklch(0.87 0.08 var(--ref-hue-primary));
--ref-color-primary-300: oklch(0.78 0.12 var(--ref-hue-primary));
--ref-color-primary-400: oklch(0.68 0.17 var(--ref-hue-primary));
--ref-color-primary-500: oklch(0.58 0.21 var(--ref-hue-primary));
--ref-color-primary-600: oklch(0.48 0.20 var(--ref-hue-primary));
--ref-color-primary-700: oklch(0.38 0.17 var(--ref-hue-primary));
--ref-color-primary-800: oklch(0.28 0.13 var(--ref-hue-primary));
--ref-color-primary-900: oklch(0.20 0.09 var(--ref-hue-primary));

/* Relative color syntax for dynamic variations */
--primary-hover: oklch(from var(--sys-color-primary) calc(l + 0.08) c h);
--primary-active: oklch(from var(--sys-color-primary) calc(l - 0.05) c h);
--primary-muted: oklch(from var(--sys-color-primary) l calc(c * 0.3) h);
```

Use `color-mix()` for overlays and state layers:
```css
--state-hover: color-mix(in oklch, var(--sys-color-primary) 8%, transparent);
--state-pressed: color-mix(in oklch, var(--sys-color-primary) 12%, transparent);
--state-focus: color-mix(in oklch, var(--sys-color-primary) 12%, transparent);
```

### 2.3 Theme Switching with light-dark()
```css
:root {
  color-scheme: light dark;

  --sys-color-surface: light-dark(
    var(--ref-color-gray-50),
    var(--ref-color-gray-900)
  );
  --sys-color-on-surface: light-dark(
    var(--ref-color-gray-900),
    var(--ref-color-gray-100)
  );
  --sys-color-border: light-dark(
    var(--ref-color-gray-200),
    var(--ref-color-gray-700)
  );
  --sys-shadow-md: light-dark(
    0 4px 6px oklch(0 0 0 / 0.1),
    0 4px 6px oklch(0 0 0 / 0.4)
  );
}
```

### 2.4 @property Registration for Animatable Tokens
Register custom properties so they can be animated:
```css
@property --sys-color-primary {
  syntax: '<color>';
  inherits: true;
  initial-value: oklch(0.58 0.21 250);
}

@property --button-bg {
  syntax: '<color>';
  inherits: false;
  initial-value: oklch(0.58 0.21 250);
}
```
This enables smooth color transitions that interpolate in oklch space.

### 2.5 Fluid Spacing and Typography
```css
/* Fluid spacing using clamp */
--space-fluid-sm: clamp(var(--ref-spacing-2), 1.5vw, var(--ref-spacing-4));
--space-fluid-md: clamp(var(--ref-spacing-4), 3vw, var(--ref-spacing-8));
--space-fluid-lg: clamp(var(--ref-spacing-8), 5vw, var(--ref-spacing-16));

/* Fluid typography using clamp */
--text-display: clamp(2.5rem, 2rem + 2.5vw, 4.5rem);
--text-h1: clamp(2rem, 1.5rem + 2vw, 3rem);
--text-h2: clamp(1.5rem, 1.25rem + 1.5vw, 2.25rem);
--text-h3: clamp(1.25rem, 1.1rem + 0.75vw, 1.75rem);
--text-body: clamp(1rem, 0.95rem + 0.25vw, 1.125rem);
--text-sm: clamp(0.875rem, 0.85rem + 0.125vw, 0.9375rem);
--text-xs: 0.75rem; /* Fixed — never goes smaller */
```

### 2.6 Motion Tokens
```css
/* Duration scale */
--duration-instant: 0ms;
--duration-fast: 100ms;
--duration-normal: 200ms;
--duration-slow: 300ms;
--duration-deliberate: 500ms;
--duration-page: 400ms;

/* Easing curves */
--ease-default: cubic-bezier(0.4, 0, 0.2, 1);      /* Material standard */
--ease-in: cubic-bezier(0.4, 0, 1, 1);               /* Entering screen */
--ease-out: cubic-bezier(0, 0, 0.2, 1);               /* Leaving screen */
--ease-bounce: cubic-bezier(0.34, 1.56, 0.64, 1);     /* Playful */
--ease-spring: linear(0, 0.009, ..., 1);               /* Spring physics */

/* Composite motion tokens */
--transition-colors: color var(--duration-fast) var(--ease-default),
                     background-color var(--duration-fast) var(--ease-default),
                     border-color var(--duration-fast) var(--ease-default);
--transition-transform: transform var(--duration-normal) var(--ease-out);
--transition-opacity: opacity var(--duration-normal) var(--ease-default);
```

### 2.7 Shadow Tokens with oklch
```css
/* Layered shadows for more natural depth */
--shadow-sm: 0 1px 2px oklch(0 0 0 / 0.05);
--shadow-md: 0 1px 3px oklch(0 0 0 / 0.1),
             0 1px 2px oklch(0 0 0 / 0.06);
--shadow-lg: 0 4px 6px oklch(0 0 0 / 0.07),
             0 2px 4px oklch(0 0 0 / 0.06);
--shadow-xl: 0 10px 15px oklch(0 0 0 / 0.1),
             0 4px 6px oklch(0 0 0 / 0.05);
--shadow-2xl: 0 20px 25px oklch(0 0 0 / 0.15),
              0 8px 10px oklch(0 0 0 / 0.05);

/* Colored shadows for interactive elements */
--shadow-primary: 0 4px 14px oklch(from var(--sys-color-primary) l c h / 0.25);
--shadow-error: 0 4px 14px oklch(from var(--sys-color-error) l c h / 0.25);
```

---

## PHASE 3: FLUTTER TOKEN ARCHITECTURE (if applicable)

### 3.1 ThemeData Token Structure
```dart
// tokens/colors.dart
class AppColors {
  // Reference tokens
  static const primaryHue = 250.0;

  // Generate scale programmatically
  static Color primary(int shade) => Color.fromOKLCH(
    lightness: _lightnessScale[shade]!,
    chroma: _chromaScale[shade]!,
    hue: primaryHue,
  );

  // System tokens
  static ColorScheme lightScheme = ColorScheme(
    primary: primary(500),
    onPrimary: Colors.white,
    primaryContainer: primary(100),
    surface: neutral(50),
    onSurface: neutral(900),
    // ...
  );
}

// tokens/spacing.dart
class AppSpacing {
  static const double xs = 4;
  static const double sm = 8;
  static const double md = 16;
  static const double lg = 24;
  static const double xl = 32;
  static const double xxl = 48;

  // Semantic spacing
  static const double cardPadding = md;
  static const double pagePadding = lg;
  static const double sectionGap = xl;
}

// tokens/typography.dart
class AppTypography {
  static TextTheme textTheme = TextTheme(
    displayLarge: TextStyle(fontSize: 57, fontWeight: FontWeight.w400, height: 1.12),
    headlineLarge: TextStyle(fontSize: 32, fontWeight: FontWeight.w600, height: 1.25),
    titleLarge: TextStyle(fontSize: 22, fontWeight: FontWeight.w500, height: 1.27),
    bodyLarge: TextStyle(fontSize: 16, fontWeight: FontWeight.w400, height: 1.5),
    labelLarge: TextStyle(fontSize: 14, fontWeight: FontWeight.w500, height: 1.43, letterSpacing: 0.1),
  );
}
```

### 3.2 Extension Methods for Token Access
```dart
extension ThemeExtensions on BuildContext {
  AppColors get colors => Theme.of(this).extension<AppColors>()!;
  AppSpacing get spacing => Theme.of(this).extension<AppSpacing>()!;
}
```

---

## PHASE 4: TAILWIND TOKEN MAPPING (if applicable)

### 4.1 tailwind.config Tokens
```javascript
// tailwind.config.js
export default {
  theme: {
    colors: {
      primary: {
        50:  'oklch(0.97 0.02 250)',
        100: 'oklch(0.93 0.04 250)',
        // ... full scale
        DEFAULT: 'oklch(0.58 0.21 250)',
      },
      surface: {
        DEFAULT: 'light-dark(oklch(0.99 0 0), oklch(0.15 0 0))',
        raised: 'light-dark(oklch(1 0 0), oklch(0.18 0 0))',
      },
    },
    spacing: {
      // Map to 4px grid
      '0.5': '0.125rem', // 2px
      '1': '0.25rem',    // 4px
      '2': '0.5rem',     // 8px
      '3': '0.75rem',    // 12px
      '4': '1rem',       // 16px
      '6': '1.5rem',     // 24px
      '8': '2rem',       // 32px
      '12': '3rem',      // 48px
      '16': '4rem',      // 64px
    },
    fontSize: {
      xs: ['0.75rem', { lineHeight: '1rem' }],
      sm: ['0.875rem', { lineHeight: '1.25rem' }],
      base: ['1rem', { lineHeight: '1.5rem' }],
      lg: ['1.125rem', { lineHeight: '1.75rem' }],
      xl: ['1.25rem', { lineHeight: '1.75rem' }],
      '2xl': ['clamp(1.5rem, 1.25rem + 1.5vw, 2.25rem)', { lineHeight: '1.3' }],
      '3xl': ['clamp(2rem, 1.5rem + 2vw, 3rem)', { lineHeight: '1.2' }],
    },
    boxShadow: {
      sm: '0 1px 2px oklch(0 0 0 / 0.05)',
      DEFAULT: '0 1px 3px oklch(0 0 0 / 0.1), 0 1px 2px oklch(0 0 0 / 0.06)',
      lg: '0 4px 6px oklch(0 0 0 / 0.07), 0 2px 4px oklch(0 0 0 / 0.06)',
    },
    transitionDuration: {
      fast: '100ms',
      DEFAULT: '200ms',
      slow: '300ms',
      deliberate: '500ms',
    },
    transitionTimingFunction: {
      DEFAULT: 'cubic-bezier(0.4, 0, 0.2, 1)',
      'ease-out': 'cubic-bezier(0, 0, 0.2, 1)',
      bounce: 'cubic-bezier(0.34, 1.56, 0.64, 1)',
    },
  },
};
```

---

## PHASE 5: TOKEN REPLACEMENT

### 5.1 Replacement Strategy
- Process files in dependency order: token definitions first, then consumers.
- Replace hardcoded values with the appropriate token tier:
  - Component-internal values → component tokens
  - Shared across components → system tokens
  - Only if no system token fits → reference tokens
- Never skip a tier: components should reference system tokens, not reference tokens directly.

### 5.2 Replacement Rules

**Colors:**
```css
/* Before */
.button { background: #3b82f6; }
.card { background: #ffffff; border: 1px solid #e5e7eb; }

/* After */
.button { background: var(--sys-color-primary); }
.card { background: var(--sys-color-surface); border: 1px solid var(--sys-color-border); }
```

**Spacing:**
```css
/* Before */
.card { padding: 20px; margin-bottom: 15px; }

/* After — snapped to nearest scale value */
.card { padding: var(--sys-spacing-card-padding); margin-bottom: var(--ref-spacing-4); }
```

**Typography:**
```css
/* Before */
h1 { font-size: 28px; font-weight: 700; line-height: 1.2; }

/* After */
h1 { font-size: var(--text-h1); font-weight: var(--weight-bold); line-height: var(--leading-tight); }
```

**Shadows:**
```css
/* Before */
.card { box-shadow: 0 2px 4px rgba(0,0,0,0.1); }

/* After */
.card { box-shadow: var(--shadow-md); }
```

### 5.3 Flutter Replacement
```dart
// Before
Container(
  padding: EdgeInsets.all(16),
  decoration: BoxDecoration(
    color: Color(0xFF3B82F6),
    borderRadius: BorderRadius.circular(8),
  ),
)

// After
Container(
  padding: EdgeInsets.all(AppSpacing.md),
  decoration: BoxDecoration(
    color: Theme.of(context).colorScheme.primary,
    borderRadius: BorderRadius.circular(AppRadius.md),
  ),
)
```

### 5.4 Handle Edge Cases
- Colors with opacity: use `oklch(from var(--token) l c h / 0.5)` or `color-mix()`.
- Calc-based spacing: keep calc but use tokens inside: `calc(var(--ref-spacing-4) + var(--ref-spacing-2))`.
- One-off values: if a value is truly unique and intentional, leave it but add a comment explaining why.
- Gradients: extract gradient stops as tokens, keep gradient direction as-is.

---

## PHASE 6: VALIDATION AND COVERAGE

### 6.1 Token Coverage Audit
After replacement, scan the codebase again and calculate:
- Total design values in codebase.
- Values now using tokens.
- Token coverage percentage.
- Target: 90%+ coverage for colors, spacing, and typography.

### 6.2 Consistency Check
- Verify no circular token references.
- Verify all token references resolve to valid values.
- Verify token naming is consistent (no mixing of camelCase and kebab-case).
- Verify tier discipline: components reference system tokens, system tokens reference reference tokens.

### 6.3 Build Verification
- Run the project build command.
- If build fails, identify the broken token reference and fix it.
- Run linter and fix any new warnings.

---

## PHASE 7: SELF-HEALING VALIDATION

### 7.1 Comprehensive Checks
- Build passes with zero errors.
- No hardcoded color values remain in component files (only in token definitions).
- All token references resolve correctly.
- Light/dark theme switching works if applicable.
- No visual regressions in existing components.

### 7.2 Test Existing Tests
- Run all existing tests. Fix any that reference hardcoded values that were replaced.
- Verify snapshot tests are updated (not broken).

---

## PHASE 8: TELEMETRY AND REPORT

### 8.1 Token Extraction Summary

```
## Token Extraction Summary

| Category     | Values Found | Unique | Tokens Created | Coverage |
|--------------|-------------|--------|----------------|----------|
| Colors       |             |        |                |          |
| Spacing      |             |        |                |          |
| Typography   |             |        |                |          |
| Radius       |             |        |                |          |
| Shadows      |             |        |                |          |
| Motion       |             |        |                |          |
| **Total**    |             |        |                |          |
```

### 8.2 Token Architecture
- Token file(s) created/modified.
- Tier breakdown: X reference tokens, Y system tokens, Z component tokens.
- Theme support: light/dark, custom themes.

### 8.3 Modernization Applied
- Hex/RGB to oklch conversions.
- Static to fluid (clamp) conversions.
- @property registrations added.
- light-dark() usage.
- color-mix() usage.

### 8.4 Remaining Hardcoded Values
List any values intentionally left hardcoded with justification.

### 8.5 Self-Evolution Notes
- What percentage of the codebase was already using tokens? (Baseline for future runs.)
- Which categories had the most scattered values? (Suggest conventions to prevent regression.)
- Are there component libraries that should adopt these tokens? (Integration opportunities.)
- Recommend running `/design-normalize` to enforce token usage across all components.
- Recommend running `/design-polish` to verify visual consistency after token migration.
