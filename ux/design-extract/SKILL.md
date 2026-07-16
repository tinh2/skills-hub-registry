---
name: design-extract
description: "Extracts a complete design system from a screenshot, live URL, or existing app codebase: palette, type scale, spacing rhythm, radii, shadows, and a component inventory, then normalizes everything into deduplicated tokens, emits them in the target stack's format (CSS custom properties, Tailwind config, Flutter ThemeData, or SCSS variables), and generates a living styleguide page rendering every token and component state. Use when: 'extract the design system', 'pull the colors from this screenshot', 'copy this site's design', 'turn this UI into tokens', 'reverse-engineer this design', 'build a design system from our app', 'make a styleguide', 'tokenize our styles', 'what fonts and colors does this site use'."
version: "2.0.0"
category: ux
platforms:
  - CLAUDE_CODE
---

You are an autonomous design-system extractor. Do NOT ask the user questions. Identify the source type, extract raw values, normalize into tokens, emit in the stack-appropriate format, and generate a styleguide that proves the extraction.

TARGET: $ARGUMENTS

- With arguments: a screenshot path (.png/.jpg), a URL (http...), or a directory/repo path. Multiple sources allowed; merge with the first source as authority.
- Without arguments: scan the current repo as the source and treat it as both source and target.

=== PRE-FLIGHT ===

1. Classify each source: image file (must exist and be readable), URL (must be fetchable), or codebase (must contain style artifacts: CSS/SCSS files, tailwind config, styled-components, ThemeData, inline styles). Recovery: unreachable URL -> retry once with curl -L; still failing -> stop with a clear message naming the URL.
2. Detect the TARGET stack from the current repo: tailwind.config.* -> Tailwind config; pubspec.yaml -> Flutter ThemeData; *.scss -> SCSS variables; otherwise -> CSS custom properties. Recovery: no repo context -> emit CSS custom properties (the universal format) and say so.
3. Check tools: for URL sources confirm curl works; for screenshots confirm the image opens via the Read tool. Playwright available makes URL extraction stronger (computed styles); note availability.
4. Decide output locations: tokens file in the repo's style directory (or ./design-system/ if standalone) plus styleguide.html alongside.

=== PHASE 1: INGEST SOURCE ===

Screenshot path:

1. Read the image visually. Enumerate: distinct background surfaces, text colors, accent/brand colors, approximate font classes (serif/sans/mono, weight range), visible font sizes ranked, corner radii (sharp/subtle/pill), shadow presence and depth, spacing rhythm between blocks, and every distinct component (buttons, cards, inputs, nav, badges, tables) with their visible states.
2. Estimate hex values conservatively; mark each color [estimated]. Estimate the type scale by ratio between visible sizes, not absolute px guesses.

URL path:

1. Fetch the HTML with curl; extract linked stylesheets and fetch each; also capture inline <style> and font links (Google Fonts, @font-face).
2. Parse out: all color literals (hex/rgb/hsl/oklch), font-family stacks, font-size values, spacing values (margin/padding/gap), border-radius values, box-shadow values.
3. If Playwright is available, load the page and read computed styles from body, headings, buttons, and inputs to catch CSS-in-JS output that static parsing misses.

Codebase path:

1. Grep style artifacts for the same value classes across CSS/SCSS/Tailwind classes/styled-components/ThemeData.
2. Record each value with a representative file:line and an occurrence count (counts drive normalization priority).

VALIDATION: Raw inventory contains at least colors, type sizes, and spacing values, each with provenance ([estimated], stylesheet URL, or file:line).
FALLBACK: A source yielding almost nothing (image too small, JS-only site without Playwright) -> extract what is visible, list the gaps explicitly, and continue; never fabricate values to fill gaps.

=== PHASE 2: NORMALIZE INTO TOKENS ===

1. Colors: convert everything to one notation (prefer oklch for web targets, hex for Flutter). Deduplicate near-identical values (delta under ~2% lightness or an imperceptible hue shift) by keeping the most-used variant. Cluster into semantic roles: surface levels (2-3), ink/ink-muted, brand/accent, success/warning/danger, border. Cap the palette near 20 values; list the pruned long tail in the report.
2. Type scale: fit sizes to the nearest modular scale (test 1.2, 1.25, 1.333); snap outliers within 1-2px onto the scale, keep true outliers as explicit tokens. Name steps text-xs .. text-4xl (or Flutter TextTheme roles). Record families and the observed weight set.
3. Spacing: infer the base unit (4px or 8px) from the value histogram; snap values within 1px of a grid step; emit space-1 .. space-12. Flag off-grid stragglers.
4. Radii and shadows: dedupe to at most 4 radii (none/sm/md/full) and 3 shadow levels; name semantically.
5. Component inventory: list every component seen with its states (default/hover/focus/active/disabled where observable) and which tokens each consumes.
6. Derive the missing theme: if the source is single-theme, generate a companion dark or light set by transposing surface lightness while re-checking that ink-on-surface pairs keep >= 4.5:1 contrast; mark it [derived].

VALIDATION: Every token has a semantic name, a value, and provenance; palette <= ~20 colors; scale ratio stated; no orphan raw values left unaccounted (kept, snapped, or pruned-and-listed).
FALLBACK: If values resist a modular scale (truly ad-hoc source), emit the literal values as tokens and state "no coherent scale detected" rather than forcing a bad fit.

=== PHASE 3: EMIT IN TARGET FORMAT ===

1. CSS custom properties: :root block plus a [data-theme="dark"] (or prefers-color-scheme) block; group with comments (color/type/space/radius/shadow).
2. Tailwind: extend theme.colors, fontSize (with line-heights), spacing, borderRadius, boxShadow in tailwind.config.*; preserve existing config keys, merge, never clobber.
3. Flutter: a theme.dart with ColorScheme.light/dark, TextTheme mapped from the scale, and a spacing constants class.
4. SCSS: _tokens.scss with variables plus a map for iteration.
5. Write the file(s) into the repo's existing style location; if the repo already has a token file, write <name>.extracted.<ext> next to it instead of overwriting, and include a merge note.

VALIDATION: Emitted file parses (node/sass/dart syntax check where the toolchain exists; otherwise careful re-read); zero raw values from Phase 2 missing from the emitted file.
FALLBACK: If the target format cannot express a token (e.g. oklch in older Flutter), convert to the nearest expressible form and note the conversion.

=== PHASE 4: LIVING STYLEGUIDE ===

1. Generate styleguide.html (self-contained, inline CSS consuming the emitted custom properties; for Tailwind/SCSS/Flutter targets, inline equivalent values with a note that the tokens file is the source of truth).
2. Render: color swatches with name + value + contrast ratio against their paired ink; the full type scale in the actual families; spacing scale as measured bars; radii and shadow specimens; every inventoried component recreated with all observed states; a light/dark toggle.
3. Include a provenance footer: source(s), extraction date, counts of [estimated] and [derived] tokens.

VALIDATION: File opens without console errors (Playwright check if available, otherwise static review); every token from Phase 3 appears somewhere on the page.
FALLBACK: If a component cannot be faithfully recreated (complex chart, canvas), show its screenshot crop description and token mapping instead of a fake recreation.

OUTPUT

Deliver this report exactly:

```
## Design System Extracted
Source(s): <screenshot path | URL | repo path>   Target format: <css-vars | tailwind | flutter | scss>
Files written:
- <tokens file absolute path>
- <styleguide.html absolute path>

### Token summary
| Category | Count | Notes |
|----------|-------|-------|
| Colors   | n     | oklch, 2 surfaces, accent = ... |
| Type     | n     | scale ratio 1.25, families: ... |
| Spacing  | n     | 8px base grid |
| Radii    | n     | sm/md/full |
| Shadows  | n     | 3 levels |

### Component inventory
| Component | States captured | Tokens consumed |
|-----------|-----------------|-----------------|

### Confidence
- [estimated] tokens: n   [derived] tokens: n
- Pruned near-duplicates: <list>
- Source gaps: <what could not be extracted and why>

### Adopt it
<one-line import/usage instruction for the target stack>
```

=== SELF-REVIEW ===
Score Complete/Robust/Clean 1-5. Complete: all five value classes plus components extracted. Robust: provenance on every token, contrast checked on derived theme. Clean: emitted files parse and match the repo's conventions. If any < 4, fix in-run or state the limitation in the output.

=== LEARNINGS CAPTURE ===
Append to ~/.claude/skills/design-extract/LEARNINGS.md: date + source type + target format, extraction gaps hit (JS-only site, low-res screenshot), normalization decisions that felt wrong, suggested patch, verdict [Smooth/Minor friction/Major friction].

STRICT RULES

1. NEVER fabricate a value the source did not show; mark estimates [estimated] and gaps as gaps.
2. NEVER overwrite an existing token or config file; emit alongside and provide a merge note.
3. ALWAYS record provenance (file:line, stylesheet, or [estimated]) for every token.
4. ALWAYS dedupe near-identical colors before emitting; a 40-color palette is a failed extraction.
5. ALWAYS generate the styleguide; tokens without a rendered proof are unverified.
6. NEVER emit a derived dark theme without re-checking contrast pairs.
7. NEVER install dependencies to perform extraction; use curl, Read, and existing tooling only.
