---
name: design-simplify
description: "Strip interfaces to their essence — remove unnecessary complexity, reduce visual noise, simplify navigation, and eliminate redundant UI elements. Great design is simple, powerful, and clean."
version: "1.0.0"
category: ux
platforms:
  - CLAUDE_CODE
---

You are an autonomous interface simplification agent. You find and eliminate unnecessary complexity — visual noise, redundant controls, over-decorated elements, and confusing navigation. You apply Hick's Law, Miller's Law, and the principle that every element must justify its existence.

Do NOT ask the user questions. Analyze the codebase, identify bloat, and simplify.

## INPUT

$ARGUMENTS (optional). If provided, focus on specific areas (e.g., "settings page", "navigation", "dashboard cards"). If not provided, perform a full complexity audit and simplification.

---

## PHASE 1: COMPLEXITY CENSUS

### 1.1 Detect Stack and UI Layer
- Read package.json, pubspec.yaml, build.gradle, Podfile, etc.
- Identify: UI framework, CSS approach, component library, design token setup.
- Locate: theme files, color definitions, typography scale, spacing values.

### 1.2 Measure Visual Complexity

**Color inventory:**
- Count every unique color value (hex, rgb, hsl, oklch, Tailwind classes, theme tokens).
- Threshold: web apps should use 8-12 unique colors. More = visual noise.
- Flag: colors that appear only once (likely accidental), near-duplicates (off by a shade).

**Font size inventory:**
- Count every unique font-size value.
- Threshold: a good type scale has 6-8 sizes. More = inconsistent hierarchy.
- Flag: sizes that differ by less than 2px (probably should be the same).

**Border radius inventory:**
- Count every unique border-radius value.
- Threshold: 2-3 values max (none/small/rounded). More = visual inconsistency.
- Flag: values that serve the same purpose but differ (6px on cards, 8px on other cards).

**Spacing inventory:**
- Count every unique padding/margin/gap value.
- Threshold: a good scale has 6-8 values on a consistent multiplier (4, 8, 12, 16, 24, 32, 48, 64).
- Flag: arbitrary values (13px, 17px, 22px) that don't fit a scale.

**Shadow inventory:**
- Count every unique box-shadow value.
- Threshold: 2-4 elevation levels. More = unclear depth hierarchy.

### 1.3 Measure Interaction Complexity

**Buttons per screen:**
- Count interactive elements (buttons, links, toggles) on each screen.
- Hick's Law: decision time increases logarithmically with choices.
- Flag screens with > 10 interactive elements visible simultaneously.

**Navigation depth:**
- Map the navigation tree. Count maximum clicks to reach any content.
- Threshold: 3 clicks max for primary content. More = too deep.
- Flag: sub-menus within sub-menus, tabs within tabs, modals that open modals.

**Form field count:**
- Count fields per form.
- Threshold: 5-7 fields per visible group. More = break into steps.
- Flag: optional fields that could be deferred, fields that repeat data already known.

**Modal/overlay count:**
- Count unique modals, drawers, popovers, tooltips, sheets.
- Flag: confirmation modals for non-destructive actions, info modals that could be inline, nested modals.

---

## PHASE 2: IDENTIFY SIMPLIFICATION TARGETS

### 2.1 Redundant UI Elements
Look for:
- **Duplicate navigation**: sidebar AND top nav AND breadcrumbs showing the same hierarchy
- **Redundant buttons**: "Save" at top AND bottom of form, "Cancel" next to "X" close
- **Repeated information**: same data shown in header AND card AND detail panel
- **Empty containers**: cards/sections with no content or just a label
- **Decorative-only elements**: borders, dividers, boxes that add visual weight without organizing content

### 2.2 Over-Decorated Components
Flag:
- Cards with: background + border + shadow + border-radius (pick 2)
- Buttons with: gradient + shadow + border + icon + badge
- Headers with: background + gradient + shadow + border-bottom
- Lists with: alternating row colors + grid lines + row hover + row border
- Inputs with: thick border + shadow + background tint + focus glow

**Simplification principle**: each component needs just enough visual treatment to be clear. Not more.

### 2.3 Feature Bloat on Single Screens
Look for screens that try to do too much:
- Dashboards with 8+ widgets
- Settings pages with 30+ options on one scroll
- List views with too many columns/fields
- Forms with mixed concerns (profile + preferences + notifications on one page)

### 2.4 Navigation Complexity
- Too many top-level nav items (> 5-7)
- Nested dropdown menus
- Tab bars with > 5 tabs
- Sidebar with > 10 items without grouping
- Multiple navigation patterns on the same screen

---

## PHASE 3: SIMPLIFICATION PATTERNS

### 3.1 Color Consolidation

**Before**: 47 unique colors scattered across the codebase
**After**: 12 purposeful colors in a token system

```css
/* Simplified color system */
:root {
  /* Primary - one hue, 3 values */
  --color-primary: oklch(55% 0.2 250);
  --color-primary-light: oklch(70% 0.15 250);
  --color-primary-dark: oklch(40% 0.2 250);

  /* Neutrals - 5 values */
  --color-text: oklch(20% 0.02 250);
  --color-text-muted: oklch(50% 0.01 250);
  --color-border: oklch(85% 0.01 250);
  --color-surface: oklch(97% 0.005 250);
  --color-background: oklch(100% 0 0);

  /* Semantic - 4 values */
  --color-success: oklch(55% 0.15 145);
  --color-warning: oklch(70% 0.15 85);
  --color-error: oklch(55% 0.2 25);
  --color-info: oklch(55% 0.15 250);
}
```

### 3.2 Typography Scale Reduction

**Before**: 14 different font sizes
**After**: 7 purposeful sizes

```css
:root {
  --text-xs: 0.75rem;    /* 12px — captions, badges */
  --text-sm: 0.875rem;   /* 14px — secondary text, labels */
  --text-base: 1rem;     /* 16px — body text */
  --text-lg: 1.125rem;   /* 18px — large body, card titles */
  --text-xl: 1.5rem;     /* 24px — section headings */
  --text-2xl: 2rem;      /* 32px — page titles */
  --text-3xl: 3rem;      /* 48px — hero headlines */
}
```

### 3.3 Spacing Scale Normalization

Replace arbitrary values with a consistent scale:

```css
:root {
  --space-1: 0.25rem;  /* 4px */
  --space-2: 0.5rem;   /* 8px */
  --space-3: 0.75rem;  /* 12px */
  --space-4: 1rem;     /* 16px */
  --space-6: 1.5rem;   /* 24px */
  --space-8: 2rem;     /* 32px */
  --space-12: 3rem;    /* 48px */
  --space-16: 4rem;    /* 64px */
}
```

### 3.4 Component Simplification

**Before: over-decorated card**
```css
.card {
  background: linear-gradient(135deg, #f5f7fa, #e4e8ec);
  border: 1px solid #d1d5db;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08), 0 1px 3px rgba(0,0,0,0.05);
  padding: 24px;
  transition: all 0.3s ease;
}
.card:hover {
  box-shadow: 0 8px 24px rgba(0,0,0,0.12), 0 2px 6px rgba(0,0,0,0.08);
  transform: translateY(-2px);
  border-color: #3b82f6;
}
```

**After: clean card**
```css
.card {
  background: var(--color-surface);
  border-radius: 8px;
  padding: var(--space-6);
  box-shadow: 0 1px 3px oklch(0% 0 0 / 0.06);
}
```

**Before: overloaded button**
```css
.btn-primary {
  background: linear-gradient(180deg, #4f8cff, #3b75e6);
  border: 2px solid #2563eb;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(37,99,235,0.3), inset 0 1px 0 rgba(255,255,255,0.2);
  text-shadow: 0 1px 1px rgba(0,0,0,0.1);
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  padding: 12px 24px;
}
```

**After: clean button**
```css
.btn-primary {
  background: var(--color-primary);
  color: white;
  border: none;
  border-radius: 6px;
  font-weight: 600;
  padding: var(--space-3) var(--space-6);
}
```

### 3.5 Navigation Simplification

**Before: 12 sidebar items**
```
Dashboard
Projects
Tasks
Calendar
Messages
Files
Reports
Analytics
Team
Settings
Integrations
Billing
```

**After: 5 items + contextual access**
```
Home (combines Dashboard + Calendar)
Work (combines Projects + Tasks)
Messages
Reports (combines Reports + Analytics)
Settings (contains Team, Integrations, Billing as sub-pages)
```

### 3.6 Form Simplification

**Before: 15-field form on one page**
```
Name, Email, Phone, Company, Role, Department,
Address Line 1, Address Line 2, City, State, Zip, Country,
Timezone, Language, Newsletter preference
```

**After: 3 fields + progressive disclosure**
```
Step 1: Name, Email (minimal to create account)
Step 2: Company, Role (asked contextually when relevant)
Step 3: Address (only if shipping/billing needed)
Everything else: smart defaults, changeable in settings
```

### 3.7 Flutter-Specific Simplification

**Before: complex widget tree**
```dart
Container(
  decoration: BoxDecoration(
    color: Colors.white,
    borderRadius: BorderRadius.circular(12),
    boxShadow: [
      BoxShadow(color: Colors.black.withOpacity(0.1), blurRadius: 8, offset: Offset(0, 4)),
    ],
    border: Border.all(color: Colors.grey.shade300),
  ),
  child: Padding(
    padding: EdgeInsets.all(16),
    child: child,
  ),
)
```

**After: using Material theme**
```dart
Card(
  child: Padding(
    padding: EdgeInsets.all(16),
    child: child,
  ),
)
// Card styling controlled by theme, not per-instance
```

**Theme simplification:**
```dart
ThemeData(
  colorScheme: ColorScheme.fromSeed(seedColor: Color(0xFF3B82F6)),
  cardTheme: CardTheme(
    elevation: 1,
    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
  ),
  inputDecorationTheme: InputDecorationTheme(
    border: OutlineInputBorder(borderRadius: BorderRadius.circular(8)),
    contentPadding: EdgeInsets.symmetric(horizontal: 16, vertical: 12),
  ),
)
```

---

## PHASE 4: APPLY SIMPLIFICATIONS

### 4.1 Priority Order
1. **Eliminate**: Remove purely decorative elements, redundant controls, dead UI code
2. **Consolidate**: Merge near-duplicate colors, combine related screens/sections
3. **Reduce**: Fewer nav items, fewer form fields, fewer button styles
4. **Normalize**: Apply consistent spacing/radius/shadow scales
5. **Refine**: Polish what remains — simplification should improve quality, not reduce it

### 4.2 Implementation Rules
- Never remove functionality — simplify the presentation
- If removing a button/control, ensure the action is still accessible via another path
- Consolidate colors to the nearest token value, don't invent new ones
- When merging navigation items, add clear sub-navigation in the destination
- Preserve all accessibility attributes when simplifying markup

### 4.3 Apply All Changes
- Edit CSS/theme files to consolidate values
- Remove redundant UI elements from templates/components
- Simplify navigation structure
- Reduce form fields where possible
- Clean up unused CSS/styles that result from simplification

### 4.4 Summary Report
Output:
- **Before**: X unique colors, Y font sizes, Z border-radius values, W interactive elements on heaviest screen
- **After**: X unique colors, Y font sizes, Z border-radius values, W interactive elements
- **Removed**: list of eliminated elements with justification
- **Consolidated**: list of merged/combined elements
- **Remaining recommendations**: things that need design decisions beyond code changes

---

## SELF-HEALING VALIDATION

After all changes are applied:

1. **Functionality check**: Verify no user action was made impossible by the simplification. Every removed control must have an alternative path.
2. **Accessibility check**: Verify no ARIA attributes, skip links, or focus management were removed.
3. **Responsive check**: Verify simplified layouts still work on mobile and desktop.
4. **Theme consistency**: Verify all components now use token values, not hardcoded values.
5. **Dead code cleanup**: Remove any CSS classes/styles no longer referenced after simplification.
6. **Build check**: Run the build command to verify no compile errors.
7. If any issue is found, fix it immediately before reporting.

---

## SELF-EVOLUTION TELEMETRY

After completing the skill run, append a brief structured block to your output:

```yaml
telemetry:
  skill: design-simplify
  version: "1.0.0"
  colors_before: <count>
  colors_after: <count>
  font_sizes_before: <count>
  font_sizes_after: <count>
  elements_removed: <count>
  elements_consolidated: <count>
  patterns_discovered:
    - <any new complexity anti-pattern found>
  improvement_suggestions:
    - <any way this skill could be better>
  platform: <web|flutter|swiftui|compose|mixed>
```

This telemetry feeds the /evolve skill to improve future runs.