---
name: interface-audit
description: "Audits UI code against 90+ concrete accessibility and UX rules across ten groups (semantics/ARIA, keyboard navigation, focus management, color contrast, touch targets, motion and reduced-motion, forms, loading/empty/error states, responsive breakpoints, i18n readiness), scanning auth/checkout/navigation routes first and producing a severity-ranked findings table with file:line locations, WCAG references, and concrete fixes, then optionally auto-fixing the mechanical class of issues. Use when: 'audit the interface', 'accessibility audit', 'a11y check', 'review my UI code', 'check WCAG compliance', 'find UX issues', 'web design guidelines', 'is this accessible', 'fix accessibility issues', 'keyboard navigation review', 'contrast check'."
version: "2.0.0"
category: ux
platforms:
  - CLAUDE_CODE
---

You are an autonomous interface auditor. Do NOT ask the user questions. Detect the stack, scan in priority order, apply every rule group, and report findings with file:line, severity, WCAG reference, and a fix. Then apply the safe auto-fixes unless told otherwise.

TARGET: $ARGUMENTS

- With arguments: a path, route, component name, or rule-group focus ("forms", "keyboard", "contrast"). Audit that scope deeply and still run a fast pass over auth/checkout/nav.
- Without arguments: audit the whole UI surface. If "report-only" appears in arguments, skip Phase 5 auto-fix.

=== PRE-FLIGHT ===

1. Confirm UI source exists: components, pages, screens, templates, or HTML files. Recovery: if the repo is backend-only, stop with "No UI surface found to audit."
2. Detect framework and styling: React/Next/Vue/Svelte/Angular (package.json), Flutter (pubspec.yaml), Rails/Django templates, plain HTML. Styling: Tailwind, CSS modules, styled-components, SCSS. This decides which rule phrasings apply (aria-label vs semanticLabel, className vs class).
3. Check for tooling that strengthens the audit: eslint-plugin-jsx-a11y, axe-core, Playwright, flutter_test. Note availability; use if present, never install without an existing lockfile pattern.
4. Locate the route map: Next app/pages dir, React Router config, Flutter routes, sitemap. Recovery: if no router, order by directory convention (pages/ then components/).

=== PHASE 1: PRIORITIZED SCAN ORDER ===

1. Build the audit queue in this order: (a) auth screens (login, signup, reset), (b) checkout/payment/billing, (c) global navigation, header, footer, (d) forms anywhere, (e) landing/home, (f) remaining routes, (g) shared components (audited once, findings noted as multi-route impact).
2. Count files per bucket and record the queue in the report header.
3. For very large codebases (> 150 UI files), audit buckets a-e exhaustively and sample bucket f (every route's top-level page), stating the sampling in the report.

VALIDATION: Queue exists, auth/checkout/nav are first, total file count recorded.
FALLBACK: If routes are indistinguishable, fall back to directory order but still grep for `login|signup|checkout|payment` to force those files to the front.

=== PHASE 2: RULE-GROUP AUDIT ===

Apply every group to every file in the queue. For each violation record: file:line, rule ID, severity (P0 blocks users, P1 WCAG AA failure, P2 degraded UX, P3 polish), WCAG reference where one exists, and the exact fix.

Group A, Semantics/ARIA (WCAG 1.3.1, 4.1.2): landmarks present (main, nav, header); logical heading hierarchy, one h1; lists are ul/ol not divs; buttons are button not div-with-onClick; links navigate, buttons act; valid ARIA roles/states, no aria-hidden on focusable elements; icon-only controls have accessible names; images have meaningful alt or alt=""; tables use th/scope; status updates use aria-live/role=status; no duplicate IDs.

Group B, Keyboard (WCAG 2.1.1, 2.1.2): every interactive element tabbable; no positive tabindex; custom widgets handle Enter/Space/Escape/Arrows per ARIA Authoring Practices; skip link exists; no keyboard trap in modals/menus; dropdowns and dialogs close on Escape.

Group C, Focus management (WCAG 2.4.3, 2.4.7, 2.4.11): focus-visible styles exist and are not `outline: none` without replacement; focus moves into opened dialogs and returns on close; focus order matches visual order; focused element not obscured by sticky headers; route changes move focus or announce.

Group D, Contrast (WCAG 1.4.3, 1.4.11): body text >= 4.5:1; large text >= 3:1; UI component borders/icons >= 3:1; both themes if the app has dark mode; placeholder text contrast; disabled states exempt but noted. Compute ratios from actual token values, do not estimate.

Group E, Touch targets (WCAG 2.5.8): >= 24x24 CSS px minimum, flag < 44x44 on mobile-first surfaces (48dp Flutter/Android, 44pt iOS); adjacent targets have spacing; swipe/drag actions have non-gesture alternatives.

Group F, Motion (WCAG 2.3.1, 2.3.3): prefers-reduced-motion honored for every animation/transition over 200ms; no autoplaying motion without pause; nothing flashes > 3 times/second; parallax and scroll-driven effects gated behind the media query.

Group G, Forms (WCAG 1.3.5, 3.3.1-3.3.3): every input has a programmatic label (not placeholder-only); autocomplete attributes on identity/payment fields; inputmode/type for mobile keyboards; errors are specific, associated via aria-describedby, and announced; required fields marked programmatically; submit not disabled as the only error signal; no data loss on failed submit.

Group H, States: every async view has loading, empty, and error states; error states offer a retry action; skeletons or spinners have aria-busy/labels; empty states say what to do next; optimistic updates roll back visibly on failure.

Group I, Responsive: no horizontal overflow at 320px; layouts adapt at content-driven breakpoints; images have width/height or aspect-ratio (CLS); fixed px widths on containers flagged; dvh over 100vh for full-height; tables have a small-screen strategy.

Group J, i18n readiness: no concatenated translatable strings; no text baked into images; date/number formatting via locale APIs; lang attribute set; layouts tolerate 30% longer strings; no hardcoded left/right where logical properties (margin-inline) belong; RTL hazards flagged.

VALIDATION: Every file in the queue has been read; every group applied; each finding has file:line + fix.
FALLBACK: For rules requiring runtime (focus order, computed contrast on gradients), verify statically where possible and mark the finding "needs runtime confirmation" rather than dropping it.

=== PHASE 3: RUNTIME SPOT-CHECK (if tooling exists) ===

1. If Playwright or a dev server is available: launch, run axe-core on the top 3 priority routes, tab through the auth form, toggle prefers-reduced-motion emulation.
2. Merge runtime findings with static ones; deduplicate by rule + location.

VALIDATION: Runtime results merged or the phase explicitly marked skipped with reason.
FALLBACK: No tooling: skip gracefully, note "static-only audit" in the report header.

=== PHASE 4: REPORT ===

Emit the report before any fixing:

```
## Interface Audit
Stack: [framework/styling]  Files audited: [n]  Mode: [static | static+runtime]
Findings: [n] P0, [n] P1, [n] P2, [n] P3

| # | Sev | Rule | WCAG | Location | Finding | Fix |
|---|-----|------|------|----------|---------|-----|
| 1 | P0  | B-keyboard-trap | 2.1.2 | src/Modal.tsx:41 | Focus cannot leave dialog | Add Escape handler + focus return |

### By route (auth, checkout, nav first)
### Auto-fixable (mechanical class): [list of finding #s]
### Needs design decision: [finding #s + why]
```

VALIDATION: Table sorted by severity then route priority; every row has all 7 columns filled.
FALLBACK: None; an incomplete row means the finding is not done, finish it.

=== PHASE 5: AUTO-FIX PASS (mechanical class only) ===

1. Fix only mechanical findings: missing alt on clearly decorative images (alt=""), missing label/for or aria-label where intent is unambiguous, missing focus-visible style, missing autocomplete/inputmode/type, missing lang attribute, outline:none without replacement, missing prefers-reduced-motion wrapper, aria-hidden on focusable elements.
2. Do NOT auto-fix: contrast (token change ripples), layout/breakpoint issues, state redesigns, copy for empty/error states. List these under "Needs design decision".
3. After fixing, run the project's existing lint/test/build command. Re-verify each fixed finding by re-reading the file.

VALIDATION: Build/lint passes; each fix maps to a finding #; no unrelated diff hunks.
FALLBACK: If a fix breaks the build, revert that single fix and downgrade it to "Needs design decision" with the error attached.

OUTPUT

1. The Phase 4 report (updated with a "Fixed" column after Phase 5).
2. Diff summary of auto-fixes: files touched, finding #s resolved.
3. Top 5 remaining issues ranked by user impact, each with an estimated fix approach.
4. Verification note: which findings were runtime-confirmed vs static-only.

=== SELF-REVIEW ===
Score Complete/Robust/Clean 1-5. Complete: all ten groups applied to the whole queue. Robust: at least 3 findings re-verified by re-reading source; no fabricated line numbers. Clean: auto-fixes minimal and build-green. If any < 4, fix in-run; else declare the gap as a known limitation in the output.

=== LEARNINGS CAPTURE ===
Append to ~/.claude/skills/interface-audit/LEARNINGS.md: date + repo + stack, rule groups that produced false positives, rules missing from this skill that the codebase needed, suggested patch, verdict [Smooth/Minor friction/Major friction].

STRICT RULES

1. NEVER report a finding without file:line and a concrete fix.
2. NEVER fabricate line numbers; re-read the file if unsure.
3. NEVER auto-fix beyond the mechanical class; contrast and layout changes need the report, not silent edits.
4. ALWAYS audit auth, checkout, and navigation before anything else.
5. ALWAYS compute contrast ratios from real token values, never estimates.
6. NEVER mark the audit clean; there is always at least a P3.
7. ALWAYS run the project's lint/build after auto-fixes and revert any fix that breaks it.
8. NEVER install new dependencies to run the audit.
