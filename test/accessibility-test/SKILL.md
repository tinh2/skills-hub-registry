---
name: accessibility-test
description: "Automated WCAG 2.1 AA accessibility testing with axe-core and Lighthouse CI. Auto-detects frontend framework (React, Next.js, Vue, Angular, Svelte, Astro, Flutter, React Native), discovers all routes and interactive components, installs Playwright + axe-core for page-level scanning and jest-axe/vitest-axe for component-level testing. Generates tests for color contrast (4.5:1), alt text, form labels, ARIA attributes, heading order, landmark regions, focus visibility, keyboard navigation (tab order, focus traps, modal focus management, skip-to-content), screen reader compatibility (aria-live regions, error announcements, toast notifications), and Flutter Semantics validation (48dp touch targets, semanticLabel). Reports violations by severity (critical, serious, moderate, minor) with WCAG criterion references. Use when adding a11y testing, auditing accessibility compliance, fixing contrast issues, or validating keyboard and screen reader support."
version: "2.0.0"
category: test
platforms:
  - CLAUDE_CODE
---

You are in AUTONOMOUS MODE. Do NOT ask questions. Detect the frontend framework, set up accessibility testing with axe-core and Lighthouse CI, generate a11y tests for all pages/routes, and produce a violations report organized by severity.

INPUT:
$ARGUMENTS

If arguments are provided, focus on those specific pages, components, or WCAG criteria. If no arguments are provided, test ALL pages and routes for WCAG 2.1 AA compliance.

============================================================
PHASE 1: FRONTEND DISCOVERY
============================================================

Step 1.1 -- Detect Frontend Framework

| Indicator | Framework |
|---|---|
| next.config.* | Next.js |
| nuxt.config.* | Nuxt |
| angular.json | Angular |
| svelte.config.* | SvelteKit |
| vite.config.* + React | React + Vite |
| vite.config.* + Vue | Vue + Vite |
| package.json with react-scripts | Create React App |
| pubspec.yaml with flutter | Flutter |
| package.json with expo | React Native (Expo) |
| astro.config.* | Astro |

Step 1.2 -- Detect Existing A11y Tools

| Indicator | Tool |
|---|---|
| jest-axe in package.json | jest-axe |
| @axe-core/playwright in package.json | Playwright axe |
| cypress-axe in package.json | Cypress axe |
| @axe-core/react in package.json | React axe (dev overlay) |
| pa11y in package.json | Pa11y |
| lighthouserc.* or @lhci/cli | Lighthouse CI |
| .a11yrc or a11y.config.* | Custom a11y config |
| Semantics widgets in Flutter | Flutter a11y (built-in) |

Step 1.3 -- Discover All Routes and Pages

Use the same route discovery method as `/e2e` Phase 0, Step 0.2.

Build the page inventory:

| # | Route | Page Name | Auth Required | Interactive Elements | Forms |
|---|-------|-----------|--------------|---------------------|-------|

Identify component-level testing targets:
- Reusable UI components (buttons, inputs, modals, navbars)
- Custom interactive widgets (date pickers, sliders, autocomplete)
- Dynamic content areas (accordions, tabs, carousels, tooltips)

============================================================
PHASE 2: TOOL SETUP
============================================================

Step 2.1 -- Install A11y Testing Tools

FOR WEB PROJECTS (React, Next.js, Vue, Angular, Svelte, Astro):

Primary tool -- Playwright + axe-core (page-level testing):
- Install: npm install -D @axe-core/playwright
- Provides: Full page a11y scanning with Playwright browser automation

Secondary tool -- jest-axe or vitest-axe (component-level testing):
- Install: npm install -D jest-axe (for Jest) or npm install -D vitest-axe (for Vitest)
- Provides: A11y checks on rendered components in unit tests

Reporting tool -- Lighthouse CI:
- Install: npm install -D @lhci/cli
- Provides: Automated Lighthouse scores including accessibility score
- Create lighthouserc.js config

FOR FLUTTER:

No extra installation needed. Flutter has built-in Semantics testing.
- Use WidgetTester to verify Semantics tree
- Use flutter test --test-semantics for semantic validation
- Use integration_test for full-app a11y flows

Step 2.2 -- Configure Lighthouse CI

Create lighthouserc.js (or .lighthouserc.json):

Configuration must include:
- URLs to test (all discovered routes)
- Assertions for accessibility score:
  - minScore: 0.9 (WCAG 2.1 AA target = 90%+)
- Number of runs: 3 (for stability)
- Preset: "lighthouse:no-pwa" (focus on accessibility, not PWA)
- Categories to audit: accessibility, best-practices

Step 2.3 -- Configure axe-core Rules

Set up axe-core with WCAG 2.1 AA as the baseline:

Rule tags to enable:
- wcag2a: WCAG 2.0 Level A
- wcag2aa: WCAG 2.0 Level AA
- wcag21a: WCAG 2.1 Level A
- wcag21aa: WCAG 2.1 Level AA
- best-practice: Additional best practice rules

Rules to explicitly verify:
- color-contrast: Text has sufficient contrast ratio (4.5:1 normal, 3:1 large)
- image-alt: All images have alt text
- label: All form inputs have labels
- link-name: All links have discernible text
- button-name: All buttons have discernible text
- document-title: Page has a title
- html-has-lang: HTML element has lang attribute
- landmark-one-main: Page has one main landmark
- region: All content is within landmarks
- aria-required-attr: ARIA elements have required attributes
- aria-valid-attr-value: ARIA attributes have valid values
- heading-order: Headings are in sequential order
- tabindex: No tabindex > 0 (disrupts tab order)
- focus-visible: Focused elements have visible focus indicator

============================================================
PHASE 3: TEST GENERATION
============================================================

Step 3.1 -- Page-Level A11y Tests (Playwright + axe)

FOR EACH page in the inventory, generate a test file:

```
test('[page-name] - accessibility', async ({ page }) => {
  // Navigate and wait for page to be fully loaded
  // Inject axe-core
  // Run full page scan with WCAG 2.1 AA tags
  // Assert zero violations
})
```

Each page test must:
1. Navigate to the page (with authentication if required)
2. Wait for all content to load (network idle, fonts, images)
3. Run axe-core scan with wcag2a, wcag2aa, wcag21a, wcag21aa tags
4. Capture all violations with:
   - Rule ID and description
   - Impact level (critical, serious, moderate, minor)
   - Affected HTML element
   - WCAG success criterion violated
   - Fix suggestion

Test interactive states for each page:
- Default state (page loaded)
- After opening a modal/dialog (check focus trap, aria attributes)
- After expanding an accordion/dropdown (check aria-expanded)
- After triggering an error state (check error messages are announced)
- After form validation failure (check error association with inputs)

Step 3.2 -- Keyboard Navigation Tests

FOR EACH page, generate keyboard navigation tests:

TAB ORDER:
1. Press Tab repeatedly from the top of the page
2. Verify focus moves in a logical reading order
3. Verify no element is skipped
4. Verify no focus trap (except intentional ones in modals)
5. Verify focus is visible on every focused element

KEYBOARD INTERACTIONS:
- Buttons: Enter and Space activate
- Links: Enter activates
- Checkboxes: Space toggles
- Radio buttons: Arrow keys move between options
- Dropdowns/Select: Arrow keys navigate options, Enter selects
- Modals: Escape closes, Tab stays within modal (focus trap)
- Menus: Arrow keys navigate, Escape closes
- Tabs: Arrow keys switch tabs
- Accordions: Enter/Space toggles

FOCUS MANAGEMENT:
- When a modal opens, focus moves to the first focusable element inside
- When a modal closes, focus returns to the trigger element
- After deleting an item, focus moves to a sensible element (next item or heading)
- Skip-to-content link works (first Tab stop, jumps to main content)

Step 3.3 -- Component-Level A11y Tests

FOR reusable components, generate unit-level a11y tests:

Using jest-axe or vitest-axe:
1. Render the component in isolation
2. Run axe on the rendered output
3. Assert zero violations

Test each component variant:
- Default state
- Disabled state
- Error state
- Loading state
- With different prop combinations

Verify semantic HTML:
- Buttons use <button>, not <div onclick>
- Links use <a href>, not <span onclick>
- Headings use <h1>-<h6> in order
- Lists use <ul>/<ol>/<li>
- Tables use <table>/<thead>/<tbody>/<th> with scope
- Forms use <form> with <label> elements linked to inputs

Step 3.4 -- Screen Reader Compatibility Tests

Generate tests to verify screen reader announcements:

ARIA LIVE REGIONS:
- Dynamic status messages use aria-live="polite"
- Error alerts use aria-live="assertive" or role="alert"
- Loading indicators announce state changes
- Toast/snackbar notifications are announced

ARIA LABELS:
- Icon-only buttons have aria-label
- Complex widgets have aria-labelledby or aria-describedby
- Decorative images have aria-hidden="true" or empty alt=""
- Navigation landmarks have aria-label when multiple exist

FORM ACCESSIBILITY:
- Each input has an associated <label> (htmlFor/for attribute)
- Required fields are marked with aria-required="true"
- Error messages are linked with aria-describedby
- Fieldsets group related inputs with <legend>
- Error state uses aria-invalid="true"

Step 3.5 -- Flutter-Specific A11y Tests (if Flutter)

Generate tests using Semantics finders:

- Verify every tappable widget has a Semantics label
- Verify images have semanticLabel property
- Verify custom widgets expose Semantics (onTap, label, value, hint)
- Verify text contrast meets 4.5:1 (check theme colors)
- Verify touch targets are at least 48x48dp
- Verify ExcludeSemantics is not hiding important content
- Test with semantics debugger enabled
- Run: flutter test --test-semantics

============================================================
PHASE 4: EXECUTION
============================================================

Step 4.1 -- Start the Application

Start the frontend dev server (same as `/e2e` Phase 1).
Wait for the server to be fully ready.

Step 4.2 -- Run axe-core Tests

Execute page-level a11y tests:

| Tool | Command |
|---|---|
| Playwright + axe | npx playwright test a11y-tests/ --reporter=list |
| Cypress + axe | npx cypress run --spec "cypress/e2e/a11y/**" |
| jest-axe | npx jest tests/a11y/ --verbose |
| Flutter | flutter test test/a11y/ |

Step 4.3 -- Run Lighthouse CI

Execute Lighthouse accessibility audits:

lhci autorun --config=lighthouserc.js

Or for individual pages:
lhci collect --url=http://localhost:PORT/page1 --url=http://localhost:PORT/page2
lhci assert

Record the accessibility score for each page.

Step 4.4 -- Compile Violations

Merge results from axe-core and Lighthouse into a unified violations list.
Deduplicate violations that appear in both tools.


============================================================
SELF-HEALING VALIDATION (max 3 iterations)
============================================================

After generating and running tests, validate:

1. All generated test files compile/parse without syntax errors.
2. Run the generated tests — capture pass/fail results.
3. If tests fail due to test code bugs (not application bugs), fix the test code.
4. Re-run to confirm tests pass or legitimately fail on application issues.
5. Repeat up to 3 iterations.

IF STILL FAILING after 3 iterations:
- Separate test failures into: test bugs vs application bugs
- Fix test bugs, document application bugs

============================================================
OUTPUT
============================================================

## Accessibility Test Report

### Setup
- **Framework:** [detected]
- **A11y tools:** [axe-core, Lighthouse CI, jest-axe, etc.]
- **WCAG level:** 2.1 AA (baseline)
- **Pages tested:** [count]
- **Components tested:** [count]

### Lighthouse Accessibility Scores

| Page | Score | Status |
|------|-------|--------|
| [page] | [0-100] | [PASS >= 90 / FAIL < 90] |
| **Average** | **N** | **[verdict]** |

### Violations by Severity

#### Critical (must fix immediately)
| # | Rule | WCAG Criterion | Page | Element | Description | Fix |
|---|------|---------------|------|---------|-------------|-----|

#### Serious (should fix before release)
| # | Rule | WCAG Criterion | Page | Element | Description | Fix |
|---|------|---------------|------|---------|-------------|-----|

#### Moderate (fix in next sprint)
| # | Rule | WCAG Criterion | Page | Element | Description | Fix |
|---|------|---------------|------|---------|-------------|-----|

#### Minor (improvement opportunity)
| # | Rule | WCAG Criterion | Page | Element | Description | Fix |
|---|------|---------------|------|---------|-------------|-----|

### Violation Summary
- Critical: N
- Serious: N
- Moderate: N
- Minor: N
- **Total violations:** N

### Keyboard Navigation Results

| Page | Tab Order | Focus Visible | Keyboard Operable | Focus Management |
|------|----------|--------------|-------------------|-----------------|

### WCAG 2.1 AA Compliance Checklist

| Criterion | Description | Status | Notes |
|-----------|------------|--------|-------|
| 1.1.1 | Non-text Content (alt text) | PASS/FAIL | |
| 1.3.1 | Info and Relationships (semantic HTML) | PASS/FAIL | |
| 1.4.3 | Contrast (Minimum) 4.5:1 | PASS/FAIL | |
| 1.4.11 | Non-text Contrast 3:1 | PASS/FAIL | |
| 2.1.1 | Keyboard accessible | PASS/FAIL | |
| 2.4.3 | Focus Order logical | PASS/FAIL | |
| 2.4.7 | Focus Visible | PASS/FAIL | |
| 3.3.1 | Error Identification | PASS/FAIL | |
| 3.3.2 | Labels or Instructions | PASS/FAIL | |
| 4.1.2 | Name, Role, Value (ARIA) | PASS/FAIL | |

### Accessibility Grade
- **AAA READY:** Zero violations, score 95+, all keyboard tests pass
- **AA COMPLIANT:** Zero critical/serious, score 90+, keyboard navigable
- **PARTIAL:** Some serious violations, score 70-89, keyboard issues
- **NON-COMPLIANT:** Critical violations, score < 70, keyboard broken

NEXT STEPS:

- "Critical violations found? Fix them immediately -- they block users with disabilities."
- "Run `/visual-regression` to verify fixes do not break the visual design."
- "Run `/e2e` to verify a11y fixes do not break functionality."
- "Run `/test-suite` to see overall test health with a11y coverage."
- "Add Lighthouse CI and axe checks to your CI pipeline to prevent regressions."
- "Consider manual testing with VoiceOver (macOS), NVDA (Windows), or TalkBack (Android)."

DO NOT:

- Do NOT lower the WCAG target below AA. AA is the legal and ethical minimum.
- Do NOT suppress axe-core rules without a documented justification.
- Do NOT skip keyboard navigation testing. Mouse-only interfaces exclude users.
- Do NOT add aria-label to elements that already have visible text labels.
- Do NOT use aria-hidden="true" on interactive or informative elements.
- Do NOT generate tests for non-visual projects (CLIs, APIs, backend services).
- Do NOT treat a passing Lighthouse score as complete a11y compliance. Automated tools catch ~30% of issues.
- Do NOT add role="presentation" or role="none" to meaningful content.
- Do NOT ignore color contrast. It is the most common a11y violation.


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /accessibility-test — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
