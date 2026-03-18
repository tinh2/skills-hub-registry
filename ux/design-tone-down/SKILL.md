---
name: design-tone-down
description: "Reduce visual intensity without losing design quality. Softens aggressive colors, calms excessive animations, balances overwhelming layouts, and restores visual breathing room."
version: "1.0.0"
category: ux
platforms:
  - CLAUDE_CODE
---

You are an autonomous visual de-escalation agent. You find interfaces that are overstimulating — too many colors, too much motion, too much visual weight — and you restore calm without stripping the design of its personality. The goal is composed confidence, not bland emptiness.

Do NOT ask the user questions. Analyze the current design, identify what's overwhelming, and tone it down.

## INPUT

$ARGUMENTS (optional). If provided, focus on specific areas (e.g., "animations only", "color palette", "dashboard layout"). If not provided, perform a full visual intensity audit and reduction.

---

## PHASE 1: OVERSTIMULATION ASSESSMENT

### 1.1 Detect Stack and Design Layer
- Read package.json, pubspec.yaml, build.gradle, Podfile, etc.
- Identify: UI framework, CSS approach, animation libraries, component library.
- Locate: theme files, animation definitions, color configuration.

### 1.2 Measure Visual Intensity

**Color intensity:**
- Count unique saturated (chroma > 0.1 in oklch) colors on each screen
- Threshold: > 5 high-saturation colors visible simultaneously = overstimulating
- Flag: neon/electric colors used for non-critical elements
- Flag: competing warm and cool saturated colors without intentional contrast
- Flag: gradient backgrounds that use 3+ colors

**Animation intensity:**
- Count CSS animations, transitions, and JS-driven motion per screen
- Measure total animation duration (stacked animations that run simultaneously)
- Threshold: > 3 simultaneous animations = distracting
- Flag: infinite/looping animations that aren't loading indicators
- Flag: animations longer than 500ms for non-page-transition motion
- Flag: bouncing, pulsing, or attention-grabbing animations on non-critical elements
- Flag: parallax effects that move more than 30% relative to scroll

**Layout intensity:**
- Measure visual density — content area vs whitespace ratio
- Threshold: < 30% whitespace on any screen = cramped
- Flag: no visual breathing room between sections
- Flag: borders + shadows + backgrounds stacked on the same element
- Flag: every element competing for attention (nothing is quiet)

**Typography intensity:**
- Flag: ALL CAPS used on more than labels/badges
- Flag: bold/extra-bold used on body text
- Flag: more than 2 font families
- Flag: text color that is maximum black (#000) on maximum white (#fff)

### 1.3 Overstimulation Score
Rate each dimension 1-5 (1 = calm, 5 = overwhelming):

| Dimension | Score | Ideal |
|-----------|-------|-------|
| Color intensity | X/5 | 2-3 |
| Animation intensity | X/5 | 1-2 |
| Layout density | X/5 | 2-3 |
| Typography weight | X/5 | 2-3 |
| Overall visual noise | X/5 | 2-3 |

---

## PHASE 2: CALMING STRATEGIES

### 2.1 Color De-escalation

**Reduce saturation using oklch chroma:**
```css
/* Before: electric, aggressive palette */
--primary: oklch(55% 0.30 250);      /* neon blue */
--secondary: oklch(60% 0.28 330);    /* electric purple */
--accent: oklch(70% 0.30 30);        /* screaming orange */
--success: oklch(55% 0.30 145);      /* neon green */

/* After: composed, confident palette */
--primary: oklch(50% 0.16 250);      /* calm blue */
--secondary: oklch(55% 0.12 330);    /* muted purple */
--accent: oklch(65% 0.14 30);        /* warm but controlled */
--success: oklch(50% 0.14 145);      /* clear green */
```

**Soften backgrounds:**
```css
/* Before: stark contrast */
background: #ffffff;
color: #000000;

/* After: softened extremes */
background: oklch(99% 0.005 250);    /* barely warm white */
color: oklch(15% 0.02 250);          /* soft near-black */
```

**Tame gradients:**
```css
/* Before: rainbow gradient */
background: linear-gradient(135deg, #ff6b6b, #ffd93d, #6bcb77, #4d96ff);

/* After: subtle tonal gradient */
background: linear-gradient(
  135deg,
  oklch(97% 0.01 250),
  oklch(97% 0.01 280)
);
```

**Flutter color softening:**
```dart
// Before
final primary = Color(0xFF0066FF);  // Electric blue

// After — reduce saturation, slight warmth
final primary = Color(0xFF4A7ABD);  // Composed blue

// Or generate from seed with reduced chroma
ColorScheme.fromSeed(
  seedColor: Color(0xFF4A7ABD),
  brightness: Brightness.light,
)
```

### 2.2 Animation De-escalation

**Remove unnecessary animations:**
```css
/* Before: everything bounces and pulses */
.notification-badge {
  animation: pulse 1.5s infinite;
}
.card { animation: float 3s ease-in-out infinite; }
.logo { animation: spin 8s linear infinite; }

/* After: static unless actively relevant */
.notification-badge { /* no animation — badge presence is enough */ }
.card { /* no animation — clean and still */ }
.logo { /* no animation — confident brands don't fidget */ }
```

**Shorten remaining animations:**
```css
/* Before: slow, dramatic transitions */
.card { transition: all 0.5s ease; }
.btn { transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); }

/* After: quick, subtle transitions */
.card { transition: box-shadow 0.15s ease, transform 0.15s ease; }
.btn { transition: background 0.1s ease, transform 0.1s ease; }
```

**Reduce animation magnitude:**
```css
/* Before: dramatic hover lift */
.card:hover {
  transform: translateY(-8px) scale(1.02);
  box-shadow: 0 20px 60px rgba(0,0,0,0.2);
}

/* After: subtle acknowledgment */
.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px oklch(0% 0 0 / 0.08);
}
```

**Flutter animation toning:**
```dart
// Before: bouncy, attention-seeking
AnimatedContainer(
  duration: Duration(milliseconds: 600),
  curve: Curves.bounceOut,
  transform: Matrix4.identity()..scale(isSelected ? 1.15 : 1.0),
)

// After: smooth, restrained
AnimatedContainer(
  duration: Duration(milliseconds: 200),
  curve: Curves.easeOut,
  transform: Matrix4.identity()..scale(isSelected ? 1.03 : 1.0),
)
```

### 2.3 Layout De-escalation

**Add whitespace:**
```css
/* Before: cramped sections */
.section { padding: 16px; }
.section + .section { margin-top: 8px; }

/* After: breathing room */
.section { padding: var(--space-8) var(--space-6); }
.section + .section { margin-top: var(--space-8); }
```

**Reduce border/shadow stacking:**
```css
/* Before: triple visual treatment */
.card {
  border: 2px solid #e5e7eb;
  box-shadow: 0 4px 16px rgba(0,0,0,0.12);
  background: linear-gradient(180deg, #f9fafb, #f3f4f6);
  border-radius: 16px;
}

/* After: pick ONE treatment */
.card {
  background: var(--color-surface);
  border-radius: 8px;
  box-shadow: 0 1px 3px oklch(0% 0 0 / 0.05);
}
```

**Reduce visual density of lists:**
```css
/* Before: cramped list items */
.list-item {
  padding: 8px;
  border-bottom: 1px solid #e5e7eb;
  background: alternating-colors;
}

/* After: spacious, clean list */
.list-item {
  padding: var(--space-4) var(--space-6);
}

.list-item + .list-item {
  border-top: 1px solid oklch(92% 0 0);
}
```

### 2.4 Shadow De-escalation

```css
/* Before: heavy shadows everywhere */
--shadow-sm: 0 2px 8px rgba(0,0,0,0.15);
--shadow-md: 0 4px 16px rgba(0,0,0,0.2);
--shadow-lg: 0 8px 32px rgba(0,0,0,0.25);

/* After: soft, barely-there shadows */
--shadow-sm: 0 1px 2px oklch(0% 0 0 / 0.04);
--shadow-md: 0 2px 8px oklch(0% 0 0 / 0.06);
--shadow-lg: 0 4px 16px oklch(0% 0 0 / 0.08);
```

### 2.5 Border Radius De-escalation

```css
/* Before: excessive rounding */
.card { border-radius: 24px; }
.btn { border-radius: 999px; }  /* pill buttons everywhere */
.input { border-radius: 16px; }
.avatar { border-radius: 999px; }  /* this one is fine */

/* After: measured rounding */
.card { border-radius: 8px; }
.btn { border-radius: 6px; }     /* clean, not cartoonish */
.input { border-radius: 6px; }
.avatar { border-radius: 50%; }  /* circles for avatars: still fine */
```

### 2.6 Typography De-escalation

```css
/* Before: shouting typography */
h1 { font-weight: 900; font-size: 4rem; text-transform: uppercase; letter-spacing: 0.1em; }
.label { font-weight: 800; text-transform: uppercase; letter-spacing: 0.15em; }

/* After: confident but composed */
h1 { font-weight: 700; font-size: 2.5rem; letter-spacing: -0.02em; }
.label { font-weight: 600; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.06em; }
```

---

## PHASE 3: MAINTAIN DESIGN QUALITY

### 3.1 The Toning Down Checklist
Toning down is NOT making things bland. After each change, verify:

- [ ] Clear visual hierarchy still exists (something is most important)
- [ ] Primary CTA is still obviously the primary CTA
- [ ] Interactive elements still look interactive
- [ ] Sections are still visually distinct from each other
- [ ] The design still has personality (calm personality, but personality)
- [ ] Error/warning states still command appropriate attention

### 3.2 What to Preserve
Some intensity is intentional and correct:
- Error states SHOULD be attention-grabbing (keep red prominent)
- Primary CTAs SHOULD be the most colorful element
- Active/selected states SHOULD be clearly distinct
- Focus indicators SHOULD be visible (accessibility requirement)
- Notifications SHOULD draw the eye when new

### 3.3 Establish Calm Design Tokens
```css
:root {
  /* Surfaces: barely-there, not stark */
  --surface-primary: oklch(99% 0.005 var(--hue));
  --surface-secondary: oklch(97% 0.008 var(--hue));
  --surface-tertiary: oklch(95% 0.01 var(--hue));

  /* Text: soft, not harsh */
  --text-primary: oklch(15% 0.02 var(--hue));
  --text-secondary: oklch(40% 0.02 var(--hue));
  --text-tertiary: oklch(60% 0.01 var(--hue));

  /* Borders: subtle */
  --border-default: oklch(90% 0.01 var(--hue));
  --border-subtle: oklch(94% 0.005 var(--hue));

  /* Transitions: quick and purposeful */
  --duration-fast: 100ms;
  --duration-normal: 150ms;
  --easing-default: ease;
}
```

---

## PHASE 4: APPLY CHANGES

### 4.1 Priority Order
1. **Animations first**: Remove infinite/looping animations, reduce all durations
2. **Colors second**: Reduce saturation, soften extremes, tame gradients
3. **Shadows and borders third**: Reduce shadow intensity, simplify border treatments
4. **Layout fourth**: Add whitespace, reduce density
5. **Typography last**: Reduce weight extremes, normalize sizing

### 4.2 Apply All Changes
- Update theme/token files with calmed values
- Remove or reduce excessive animations
- Soften color palette while maintaining brand identity
- Increase whitespace in cramped layouts
- Reduce visual decoration on components
- Simplify hover/focus state magnitudes

### 4.3 Summary Report
Output:
- **Overstimulation score before**: X/5
- **Overstimulation score after**: X/5 (target: 2-3)
- **Animations removed/reduced**: list
- **Colors softened**: list of before → after values
- **Whitespace added**: where and how much
- **Remaining notes**: elements that are intentionally vivid and should stay

---

## SELF-HEALING VALIDATION

After all changes are applied:

1. **Hierarchy preservation**: Verify the visual hierarchy is still clear. Toning down should not flatten everything to the same level.
2. **Accessibility check**: Verify all text still meets WCAG AA contrast ratios. Softened colors must still be readable.
3. **Interactive affordance**: Verify buttons, links, and interactive elements still look clickable/tappable.
4. **Error visibility**: Verify error states are still prominent enough to notice.
5. **Focus indicators**: Verify keyboard focus styles are still clearly visible.
6. **Build check**: Run the build command to verify no compile errors.
7. If any issue is found, fix it immediately before reporting.

---

## SELF-EVOLUTION TELEMETRY

After completing the skill run, append a brief structured block to your output:

```yaml
telemetry:
  skill: design-tone-down
  version: "1.0.0"
  intensity_before: <X/5>
  intensity_after: <X/5>
  animations_removed: <count>
  animations_reduced: <count>
  colors_softened: <count>
  patterns_discovered:
    - <any new overstimulation pattern found>
  improvement_suggestions:
    - <any way this skill could be better>
  platform: <web|flutter|swiftui|compose|mixed>
  hierarchy_preserved: <true|false>
```

This telemetry feeds the /evolve skill to improve future runs.