---
name: visual-regression
description: Set up visual regression testing with baseline screenshots across breakpoints. Auto-detects frontend framework (Next.js, React, Vue, Angular, Flutter, Storybook), configures Playwright screenshot comparison, BackstopJS, or Flutter golden tests, captures every page at mobile/tablet/desktop/wide viewports plus interactive states (hover, focus, error, empty, loading), stabilizes dynamic content to prevent false positives, and reports pixel-level diffs. Use when you need to catch unintended UI changes, set up screenshot baselines, prevent CSS regressions, or verify layouts across screen sizes after refactoring.
version: "1.0.0"
category: test
platforms:
  - CLAUDE_CODE
---

You are in AUTONOMOUS MODE. Do NOT ask questions. Detect the frontend framework,
set up visual regression testing with baseline screenshots, configure comparison
tools, and report any visual diffs.

INPUT:
$ARGUMENTS

If arguments are provided, focus on those specific pages, components, or breakpoints.
If no arguments are provided, capture ALL pages/routes in the application.

============================================================
PHASE 1: FRONTEND DISCOVERY
============================================================

Step 1.1 -- Detect Frontend Framework

| Indicator | Framework |
|---|---|
| next.config.* or app/ with page.tsx | Next.js |
| nuxt.config.* or pages/*.vue | Nuxt |
| angular.json | Angular |
| svelte.config.* | SvelteKit |
| vite.config.* + src/App.tsx | React + Vite |
| vite.config.* + src/App.vue | Vue + Vite |
| package.json with react-scripts | Create React App |
| pubspec.yaml with flutter | Flutter |
| package.json with expo | React Native (Expo) |
| .storybook/ directory | Storybook (component library) |
| astro.config.* | Astro |

Step 1.2 -- Detect Existing Visual Testing Tools

| Indicator | Tool |
|---|---|
| .percy.yml or percy in package.json | Percy |
| chromatic in package.json | Chromatic |
| backstop.json or backstop/ directory | BackstopJS |
| playwright.config.* with toHaveScreenshot | Playwright screenshots |
| cypress/ with matchImageSnapshot | Cypress image snapshot |
| .loki/ or loki in package.json | Loki |
| reg-suit.json or reg-suit in package.json | reg-suit |

If no visual testing tool exists, select based on stack:
- Projects with Playwright already: Use Playwright screenshot comparison (built-in)
- Projects with Storybook: Use Chromatic or Storybook test-runner
- Any web project: Use Playwright (most capable, no third-party dependency)
- Flutter: Use golden tests (flutter_test matchesGoldenFile)

Step 1.3 -- Discover All Pages and Routes

Build the page inventory by scanning route definitions, page components, and navigation config.

| # | Route | Page Name | Auth Required | Dynamic Content | Priority |
|---|-------|-----------|--------------|----------------|----------|

Priority classification:
- CRITICAL: Landing page, login, signup, dashboard, main feature pages
- HIGH: Settings, profile, list views, detail views
- MEDIUM: Secondary features, about, help
- LOW: Error pages, empty states, loading states (still capture them)

============================================================
PHASE 2: TOOL SETUP
============================================================

Step 2.1 -- Install and Configure

FOR PLAYWRIGHT (preferred for web):

Install if needed: npm init playwright@latest

Create or update playwright.config.ts to include:
- projects for each browser: chromium, firefox, webkit
- viewport sizes for breakpoints:
  - mobile: { width: 375, height: 812 }
  - tablet: { width: 768, height: 1024 }
  - desktop: { width: 1280, height: 720 }
  - wide: { width: 1920, height: 1080 }
- screenshot comparison settings:
  - maxDiffPixels or maxDiffPixelRatio threshold
  - animations: "disabled" (prevent flaky diffs)
  - snapshotPathTemplate for organized output

FOR BACKSTOPJS:

Install: npm install -D backstopjs && npx backstop init

Configure backstop.json:
- viewports: mobile (375), tablet (768), desktop (1280)
- scenarios for each page
- misMatchThreshold: 0.1 (very strict) to 5 (lenient)
- delay and readySelector for dynamic content

FOR FLUTTER GOLDEN TESTS:

No extra installation needed. Uses flutter_test matchesGoldenFile.

Configure test/golden/ directory for baseline images.

FOR CHROMATIC (Storybook projects):

Install: npm install -D chromatic
Configure: add chromatic script to package.json
Set up: CHROMATIC_PROJECT_TOKEN environment variable

Step 2.2 -- Handle Dynamic Content

Dynamic content causes false positive diffs. Set up stabilization:

FREEZE TIME:
- JavaScript: Mock Date.now() to return a fixed timestamp
- Playwright: page.addInitScript to override Date constructor
- Flutter: Use clock package with fixed time

MOCK DATA:
- Use consistent seed data for all screenshots
- Mock API responses with deterministic data
- Use fixed user avatars (no gravatar or random avatars)

HIDE DYNAMIC ELEMENTS:
- Mask elements that change every render (timestamps, counters, ads)
- Use CSS to hide cursor blink, animations, transitions
- Disable video/gif playback
- Replace dynamic images with placeholders

WAIT FOR STABILITY:
- Wait for network idle (no pending requests)
- Wait for fonts to load (document.fonts.ready)
- Wait for images to load (all img elements complete)
- Wait for animations to finish (use page.evaluate to check)
- Add explicit wait for lazy-loaded content

============================================================
PHASE 3: TEST GENERATION
============================================================

Step 3.1 -- Generate Screenshot Tests

FOR PLAYWRIGHT:

Create visual-tests/ directory with one test file per page group:

For each page in the inventory, generate a test that:
1. Navigates to the page (with auth if required)
2. Waits for stability (network idle, fonts loaded, images loaded)
3. Hides dynamic elements (timestamps, avatars)
4. Takes a full-page screenshot
5. Compares against baseline with toHaveScreenshot()

Generate tests for EACH breakpoint:
- test('page-name - mobile', ...) with mobile viewport
- test('page-name - tablet', ...) with tablet viewport
- test('page-name - desktop', ...) with desktop viewport

Generate tests for interactive states:
- Hover states on buttons/links
- Focused form fields
- Open dropdown menus
- Expanded accordions
- Modal/dialog open states
- Error states (form validation)
- Empty states (no data)
- Loading states (skeleton screens)

FOR FLUTTER GOLDEN TESTS:

Create test/golden/ directory:

For each widget/screen, generate a test that:
1. Pumps the widget with fixed size and test data
2. Calls expectLater(find.byType(Widget), matchesGoldenFile('path.png'))
3. Tests at multiple sizes using WidgetTester.view.physicalSize

FOR BACKSTOPJS:

Add scenarios to backstop.json for each page with:
- url and label
- readySelector (element that confirms page loaded)
- delay (ms to wait)
- hideSelectors for dynamic content
- clickSelector for interactive states
- viewports for each breakpoint

Step 3.2 -- Generate Baseline

Run the tests in update mode to create baseline screenshots:

| Tool | Command |
|---|---|
| Playwright | npx playwright test --update-snapshots |
| BackstopJS | npx backstop reference |
| Flutter | flutter test --update-goldens test/golden/ |
| Chromatic | npx chromatic (first run creates baseline) |

Verify baselines are created and look correct. Commit baseline images.

============================================================
PHASE 4: EXECUTION AND COMPARISON
============================================================

Step 4.1 -- Run Comparison Tests

Execute the visual tests against the baselines:

| Tool | Command |
|---|---|
| Playwright | npx playwright test visual-tests/ --reporter=html |
| BackstopJS | npx backstop test |
| Flutter | flutter test test/golden/ |
| Chromatic | npx chromatic |

Step 4.2 -- Analyze Diffs

For each failed comparison:

1. Identify the page and breakpoint
2. Measure the diff percentage
3. Categorize the diff:
   - INTENTIONAL: Layout or design change that should update the baseline
   - REGRESSION: Unintended visual change that needs fixing
   - FALSE POSITIVE: Dynamic content not properly stabilized
   - BROWSER RENDERING: Sub-pixel differences across browsers

Step 4.3 -- Handle Results

FOR REGRESSIONS: Note the file and visual difference for the developer to fix.
FOR FALSE POSITIVES: Improve stabilization (add masks, increase thresholds).
FOR INTENTIONAL CHANGES: Update baselines.

============================================================
OUTPUT
============================================================

## Visual Regression Test Report

### Setup
- **Framework:** [detected]
- **Visual testing tool:** [selected]
- **Breakpoints:** mobile (375px), tablet (768px), desktop (1280px), wide (1920px)
- **Baseline images:** [count] created

### Pages Captured

| Page | Route | Mobile | Tablet | Desktop | States Captured |
|------|-------|--------|--------|---------|----------------|
| [name] | [route] | PASS/FAIL | PASS/FAIL | PASS/FAIL | [hover, error, empty, etc.] |

### Results Summary
- Total screenshots: N
- Matching baseline: N
- Diffs detected: N
  - Regressions: N
  - False positives: N (stabilization improved)
  - Intentional changes: N (baselines updated)

### Visual Diffs Found

| Page | Breakpoint | Diff % | Category | Description |
|------|-----------|--------|----------|------------|

### Dynamic Content Handling
- Elements masked: [list]
- Time frozen to: [timestamp]
- APIs mocked: [list]

### CI Integration

Add to your CI pipeline:
```
[generated CI config snippet for the detected CI system]
```

NEXT STEPS:

- "Visual regressions found? Fix the UI and re-run `/visual-regression` to update baselines."
- "Run `/accessibility-test` to check WCAG compliance on the same pages."
- "Run `/e2e` to verify functional correctness alongside visual correctness."
- "Run `/test-suite` to see overall test health with visual regression coverage."
- "Commit baseline images and add visual tests to your CI pipeline."

DO NOT:

- Do NOT run visual tests without stabilizing dynamic content first.
- Do NOT set diff thresholds to zero. Sub-pixel rendering differences are normal.
- Do NOT capture screenshots without waiting for fonts and images to load.
- Do NOT skip mobile breakpoints. Most visual regressions appear on small screens.
- Do NOT compare screenshots across different operating systems (rendering differs).
- Do NOT include timestamps, live data, or user-specific content in screenshots.
- Do NOT delete baseline images. They are the source of truth for comparison.
- Do NOT generate visual tests for non-visual projects (CLIs, APIs, libraries).
