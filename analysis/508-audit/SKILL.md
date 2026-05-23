---
name: 508-audit
description: Run a full Section 508 + WCAG 2.2 Level AA accessibility audit on a federal / .gov / public-sector website or ICT product. Section 508 incorporates WCAG 2.0 AA as the binding federal standard, but most modern federal procurements now test against WCAG 2.2 AA (the 2024-incorporated update). Outputs the official compliance trio agencies require: (1) Voluntary Product Accessibility Template (VPAT® 2.5 Rev 508) covering all 508 chapters, (2) Accessibility Conformance Report (ACR) with each criterion marked Supports / Partially Supports / Does Not Support / Not Applicable + explanation, (3) Remediation plan with prioritized fixes (P0 blockers like keyboard traps, P1 perceivability fails, P2 cosmetic). Combines axe-core automated scan + manual keyboard / screen-reader / cognitive walkthrough findings. TRIGGER on "Section 508", "508 audit", "WCAG", "VPAT", "ACR", "federal accessibility", ".gov accessibility", "ADA Title II", "ICT accessibility", "accessibility audit for government", "GSA accessibility".
version: "1.0.0"
category: analysis
platforms:
  - CLAUDE_CODE
---

# Section 508 + WCAG 2.2 Accessibility Audit

You run a federal-grade accessibility audit and produce the deliverable trio agencies require (VPAT 2.5 + ACR + remediation plan). Federal procurement is increasingly contingent on these — failure to provide credible 508 documentation eliminates vendors from competition.

**Standards landscape (2026)**:

- **Section 508 (Revised 2017)**: binding for federal procurement. Incorporates **WCAG 2.0 AA** technical criteria.
- **WCAG 2.2 AA** (W3C, October 2023): adds 9 new success criteria (focus appearance, dragging movements, target size, etc.). Many agencies test against 2.2 even though 508 floor is still 2.0. Testing higher is fine.
- **ADA Title II** (April 2024 final rule): public entities (state, local governments) must conform to WCAG 2.1 AA by April 2026 (large entities) or 2027 (small).
- **Section 504** (federal grantees): similar requirements via funding agreements.

============================================================
=== PRE-FLIGHT ===
============================================================

Verify:

- [ ] **Site URL** + scope (pages to audit). Federal audit baseline: every "key" template + ≥ 25 sampled pages.
- [ ] **Site rendering**: static HTML / SSR / CSR? Pure CSR can't be audited by lightweight tools without rendering.
- [ ] **Stack**: identify frontend framework + UI library (React + MUI, Vue + Vuetify, etc.). Different defaults.
- [ ] **Documentation deliverable target**: VPAT 2.5 Rev 508, VPAT 2.5 Int (international), or VPAT 2.5 INT/EU (with EN 301 549).
- [ ] **Test tools available**: axe-core, Lighthouse, WAVE, screen reader (NVDA / JAWS / VoiceOver), keyboard.

Recovery:

- If site is CSR-only, render via Playwright before scanning — axe-core needs DOM, not raw HTML.
- If user can't provide screen-reader access, output manual test cases for them to run + capture results.

============================================================
=== PHASE 1: AUTOMATED SCAN ===
============================================================

Run axe-core (`@axe-core/cli` or via Playwright `@axe-core/playwright`) against every priority URL:

```bash
npx @axe-core/cli --rules wcag22aa,best-practice https://example.gov \
  --save axe-report.json \
  --tags wcag2a,wcag2aa,wcag21a,wcag21aa,wcag22a,wcag22aa
```

Also run Lighthouse accessibility category for each URL. Persist both as `automated_findings.json`.

Caveats explicit to the user:

- Automated tools catch ~30-40% of real WCAG issues. The remaining 60-70% require manual testing.
- Common false positives: color-contrast on text in images (axe can't read), aria misuse in WAI-ARIA patterns.
- Auto-scan is the FLOOR, not the ceiling.

VALIDATION: Automated scan completes on every priority URL with no exit-1. Findings deduplicated.

============================================================
=== PHASE 2: KEYBOARD AUDIT ===
============================================================

Manual keyboard walkthrough. For each priority page:

- [ ] **Skip link** present and functional (first Tab focus).
- [ ] **Tab order** logical (matches visual reading order).
- [ ] **Focus visible** at every interactive element (WCAG 2.4.7).
- [ ] **No keyboard traps** (WCAG 2.1.2).
- [ ] **Custom widgets** (combobox, menu, tabs, dialog) operable via expected keys per WAI-ARIA Authoring Practices.
- [ ] **Modal dialogs** trap focus correctly AND restore focus on close.
- [ ] **WCAG 2.2 SC 2.4.11 Focus Not Obscured**: focused element not hidden by sticky header / cookie banner.
- [ ] **WCAG 2.2 SC 2.5.7 Dragging Movements**: every drag operation has a non-drag alternative (e.g., click buttons).
- [ ] **WCAG 2.2 SC 2.5.8 Target Size**: interactive targets ≥ 24×24 CSS pixels (exceptions noted).

Generate `keyboard_findings.md` with per-page checklist and violations.

VALIDATION: Every interactive element tested. Findings reference specific WCAG SC.

============================================================
=== PHASE 3: SCREEN READER AUDIT ===
============================================================

Test priority pages with NVDA (Windows + Chrome/Firefox) and VoiceOver (Mac/iOS). Report per page:

- [ ] **Page title** announced and meaningful (not "untitled").
- [ ] **Heading hierarchy** (h1 → h6) maps to visual structure.
- [ ] **Landmarks** (`<header>`, `<nav>`, `<main>`, `<aside>`, `<footer>`) present.
- [ ] **Form labels** associated via `<label for>` or `aria-labelledby`.
- [ ] **Error messages** announced (aria-live or focus-shift).
- [ ] **Images**: meaningful images have alt; decorative use `alt=""` or `role="presentation"`.
- [ ] **SVG**: `<title>` + `aria-labelledby` or hidden via `aria-hidden`.
- [ ] **Tables**: `<th>` + `scope` for data tables; layout tables avoided.
- [ ] **Live regions** for dynamic updates (`aria-live="polite"` or `"assertive"`).
- [ ] **Custom widgets**: announce role, state (expanded/collapsed), value.

Generate `sr_findings.md` per page with screen-reader-specific issues.

VALIDATION: Findings cite specific SC + reproducer steps.

============================================================
=== PHASE 4: COGNITIVE / READABILITY AUDIT ===
============================================================

WCAG 2.2 added several cognitive-load SC:

- [ ] **3.2.6 Consistent Help** — help mechanism (contact, FAQ, chat) at consistent position across pages.
- [ ] **3.3.7 Redundant Entry** — info previously entered is auto-populated or selectable.
- [ ] **3.3.8 Accessible Authentication (Minimum)** — no cognitive function test (typing CAPTCHA, recalling password from memory) unless alternative provided.
- [ ] **Plain language** — Flesch Reading Ease ≥ 60 for civic content (state/federal guideline).
- [ ] **Forms** — autocomplete attributes set (`autocomplete="email"`, `autocomplete="given-name"`).
- [ ] **Session timeout** warning + extension UI.
- [ ] **Errors** explain WHAT and HOW TO FIX, not just "invalid input."

VALIDATION: Each page has cognitive checklist run with findings.

============================================================
=== PHASE 5: VPAT 2.5 GENERATION ===
============================================================

Generate `vpat.docx` (or `vpat.md` if user prefers) following the **VPAT® 2.5 Rev 508** template from ITI / Section508.gov:

Sections required:

- Cover sheet (product, version, contact, evaluation method, date)
- **Chapter 1**: Application of Revised 508 Standards (which chapters apply)
- **Chapter 2**: 36 CFR Part 1194 Appendix A (Functional Performance Criteria)
- **Chapter 3**: WCAG 2.0 Level A & AA criteria (incorporated into 508)
- **Chapter 4**: Hardware (if applicable, often N/A for web)
- **Chapter 5**: Software (web applications fall here mostly)
- **Chapter 6**: Support Documentation and Services
- Conformance terms per criterion: **Supports** / **Partially Supports** / **Does Not Support** / **Not Applicable** + **Remarks and Explanations**

Per criterion remarks must be specific. "Supports" without explanation is suspect to procurement officers.

VALIDATION: VPAT covers ALL applicable WCAG 2.0 A/AA criteria + all 508 chapters. Every "Partially Supports" / "Does Not Support" has a remarks explanation.

============================================================
=== PHASE 6: ACCESSIBILITY CONFORMANCE REPORT (ACR) ===
============================================================

The ACR is the VPAT-formatted document signed and dated, typically delivered with the procurement response. Generate as `acr.pdf` (via `pandoc` + `wkhtmltopdf` or `weasyprint`) with:

- Signed conformance attestation
- Evaluation methodology summary (tools used, manual testing scope, sample size)
- Known issues with severity + planned remediation
- Roadmap dates for in-progress fixes
- Contact for accessibility questions

VALIDATION: ACR is a single PDF, signed, dated.

============================================================
=== PHASE 7: REMEDIATION PLAN ===
============================================================

Generate `remediation_plan.md` with findings ranked:

| Priority | Finding                                   | WCAG SC | Sample URL | Estimated effort | Suggested fix                                                      |
| -------- | ----------------------------------------- | ------- | ---------- | ---------------- | ------------------------------------------------------------------ |
| P0       | Keyboard trap in date picker              | 2.1.2   | /apply     | 4 hr             | Use `<input type="date">` or trap-aware Floating UI                |
| P0       | No skip link                              | 2.4.1   | All pages  | 1 hr             | Add `<a href="#main" class="skip-link">Skip to main</a>` in layout |
| P1       | Insufficient color contrast on link hover | 1.4.3   | All pages  | 2 hr             | Update `--color-link-hover` to ≥ 4.5:1                             |
| P2       | Missing lang attribute                    | 3.1.1   | /es/\*     | 1 hr             | Set `<html lang="es">` for Spanish pages                           |

P0 = WCAG fail that prevents access entirely. P1 = fail that hinders. P2 = polish.

Output also as JIRA / GitHub Issues import CSV.

VALIDATION: Every finding from phases 1-4 appears in the plan. P0 items have effort estimates.

============================================================
=== SELF-REVIEW ===
============================================================

Score 1–5:

- **Complete**: All 7 phases delivered? VPAT + ACR + remediation plan present?
- **Robust**: Automated + manual + screen reader + cognitive covered?
- **Clean**: VPAT criterion remarks are specific (not "supports — no issues")?
- **Federal-credible**: Would a federal accessibility officer (or Section508.gov reviewer) accept this trio as procurement-ready?

Common gap: VPAT with vague "Supports" remarks. Each must reference specific testing evidence.

============================================================
=== LEARNINGS CAPTURE ===
============================================================

Append to `~/.claude/skills/508-audit/LEARNINGS.md`:

## <YYYY-MM-DD> — <site, framework, scope>

- **What worked:**
- **What was awkward:**
- **Suggested patch:**
- **Verdict:** [Smooth / Minor friction / Major friction]

============================================================
=== STRICT RULES ===
============================================================

- Never deliver a VPAT with only automated-scan findings. 60-70% of real issues require manual testing.
- Never claim "Supports" on a criterion without explaining the testing evidence.
- Never silently overlook WCAG 2.2 SCs. Even though 508 floor is 2.0 AA, agencies increasingly test against 2.2.
- Never sign an ACR without management review. The conformance attestation has legal weight.
- Always flag CSR-only sites as requiring rendering before audit. Bare-bones HTML scans miss the entire SPA.
