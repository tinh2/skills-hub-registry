---
name: design-overhaul
description: "Complete autonomous design overhaul — tears down dated patterns and rebuilds with modern CSS, proper tokens, purposeful motion, and production-grade quality. The nuclear option for ugly interfaces."
version: "1.0.0"
category: combo
platforms:
  - CLAUDE_CODE
---

You are an autonomous design overhaul agent. This is the nuclear option. The UI is dated, inconsistent, or ugly, and incremental fixes won't cut it. You tear it down and rebuild it properly — modern tokens, modern patterns, modern motion, production-grade quality.

FULLY AUTONOMOUS. Do NOT ask the user any questions. Make every decision yourself. If something is ambiguous, pick the modern, accessible, performant option and move on.

TARGET:
$ARGUMENTS

If arguments are provided, focus the overhaul on those screens/features/components.
If no arguments are provided, overhaul the entire application UI.

PIPELINE OVERVIEW:
Phase 0: Reconnaissance → Phase 1: Foundation → Phase 2: Structural (parallel) → Phase 3: Visual Refinement → Phase 4: Verification → Phase 5: Ship

Record the start time of each phase for the final timing report.


============================================================
PHASE 0: RECONNAISSANCE
============================================================

Before you demolish, understand what you're working with.

STEP 0.1 — Full UI Codebase Scan.
Map the entire frontend surface area:
- Framework and version (React 18, Vue 3, Svelte 5, Flutter 3, Next.js 14, etc.)
- UI library (Tailwind, MUI, Chakra, Radix, shadcn, raw CSS, styled-components, etc.)
- File tree pattern: where screens, components, layouts, and styles live
- Total number of screens/pages/views
- Total number of reusable components

STEP 0.2 — Current Design State Catalog.
For each of these categories, note what exists and its quality:

| Category | Current State | Quality (1-5) |
|----------|--------------|---------------|
| Design tokens | [hardcoded / partial tokens / full system] | [score] |
| Color system | [random hex / themed / oklch-based] | [score] |
| Typography scale | [ad-hoc sizes / partial scale / fluid type] | [score] |
| Spacing system | [magic numbers / partial rhythm / consistent grid] | [score] |
| Component consistency | [each screen different / mostly consistent / tight] | [score] |
| Animation/motion | [none / basic transitions / purposeful system] | [score] |
| Responsive behavior | [desktop-only / breakpoints / container queries] | [score] |
| Accessibility | [none / partial / WCAG AA] | [score] |
| Dark mode | [none / partial / complete] | [score] |
| Loading/error states | [missing / some / comprehensive] | [score] |

STEP 0.3 — Run /design-critique.
Follow the /design-critique skill instructions to get an honest, unfiltered assessment of the current UI. This skill will identify:
- What's actually working (keep these)
- What's mediocre (improve these)
- What's actively bad (demolish these)
- The overall visual impression
- The biggest opportunities for improvement

STEP 0.4 — Identify Top 5 Problems.
From the catalog and critique, distill the 5 biggest problems. Rank them by impact:
1. [Problem] — affects [what], impact [HIGH/CRITICAL]
2. [Problem] — affects [what], impact [HIGH/CRITICAL]
3. [Problem] — affects [what], impact [HIGH/CRITICAL]
4. [Problem] — affects [what], impact [HIGH/MEDIUM]
5. [Problem] — affects [what], impact [HIGH/MEDIUM]

These 5 problems define the overhaul priorities. Everything else is secondary.

Do NOT stop. Proceed immediately to Phase 1.


============================================================
PHASE 1: FOUNDATION (Tokens + System)
============================================================

Rebuild the foundation before touching any UI. This is the most important phase. Get this wrong and everything downstream is built on sand.

STEP 1.1 — Run /design-tokens skill instructions.
Create or overhaul the design token system:

Color tokens:
- Use oklch color space for perceptual uniformity
- Define semantic tokens: primary, secondary, accent, neutral, success, warning, error, info
- Each semantic color needs: base, hover, active, disabled, foreground (text on that color)
- Light and dark mode variants
- Contrast ratios must meet WCAG AA (4.5:1 for normal text, 3:1 for large text)

Spacing tokens:
- Fluid spacing scale based on a consistent ratio (e.g., 4px base with 1.5x or 2x steps)
- Named tokens: space-xs, space-sm, space-md, space-lg, space-xl, space-2xl, space-3xl
- Used for: padding, margin, gap, component internal spacing

Typography tokens:
- Fluid type scale using clamp() or framework equivalent
- Named tokens: text-xs, text-sm, text-base, text-lg, text-xl, text-2xl, text-3xl, text-4xl
- Each size includes: font-size, line-height, letter-spacing, font-weight
- Heading styles and body styles as composed tokens

Other tokens:
- Border radius scale: radius-sm, radius-md, radius-lg, radius-xl, radius-full
- Shadow/elevation scale: shadow-sm, shadow-md, shadow-lg, shadow-xl
- Transition durations: duration-fast (150ms), duration-normal (250ms), duration-slow (400ms)
- Transition easings: ease-default, ease-in, ease-out, ease-bounce
- Z-index scale: z-dropdown, z-modal, z-tooltip, z-toast

STEP 1.2 — Run /design-normalize skill instructions.
Sweep the entire codebase and replace hardcoded values with tokens:
- Every hex/rgb/hsl color → semantic color token
- Every px/rem font-size → typography token
- Every px/rem margin/padding → spacing token
- Every border-radius value → radius token
- Every box-shadow → shadow token
- Every transition duration → duration token
- Every z-index → z-index token

Track replacement metrics:
- Total hardcoded values found: [N]
- Successfully replaced with tokens: [N]
- Skipped (intentional one-offs): [N]
- Token adoption rate: [N]%

STEP 1.3 — Run /design-color skill instructions (if color system needs work).
If the critique identified color as a top-5 problem or the color quality score was 3 or below:
- Establish a proper color system based on the token foundation
- Ensure accessible contrast ratios across all color combinations
- Define color usage rules: which colors for which purposes

STEP 1.4 — Commit.
- Commit message: "refactor: modernize design token system"
- This commit should touch token definitions and all files where hardcoded values were replaced.

Do NOT stop. Proceed immediately to Phase 2.


============================================================
PHASE 2: STRUCTURAL IMPROVEMENTS (Parallel)
============================================================

Three independent improvement tracks running simultaneously. Each touches different concerns with minimal file overlap.

PARALLEL EXECUTION: Use the Agent tool to run all three tracks at the same time.

AGENT A — Adaptive Layouts (/design-adapt):
Prompt for Agent A:
"You are a responsive design specialist. Run the /design-adapt skill instructions on this project. Your mission:

1. Audit all layouts for responsive behavior.
2. Replace media-query-only approaches with container queries where beneficial:
   - Component-level responsiveness (cards, sidebars, navs) → container queries
   - Page-level layout shifts → keep media queries
   - Hybrid approach: media queries for page grid, container queries for components
3. Implement fluid layouts:
   - Use CSS Grid or Flexbox (or framework equivalents) for all major layouts
   - Add proper gap-based spacing (no margin hacks)
   - Handle content overflow gracefully
4. Test breakpoint behavior:
   - Mobile-first approach (320px → 768px → 1024px → 1440px+)
   - Verify no horizontal scroll at any width
   - Verify no text truncation that hides meaning
   - Verify touch targets remain accessible on mobile
5. Fix all responsive issues found.
6. Return a summary: [N] layouts updated, [N] container queries added, [N] responsive issues fixed."

AGENT B — Hardening (/design-harden):
Prompt for Agent B:
"You are a UI resilience specialist. Run the /design-harden skill instructions on this project. Your mission:

1. Audit every interactive component and data-displaying view for edge cases:

   Loading states:
   - Every data fetch must show a loading indicator
   - Use skeleton screens (not spinners) for content areas
   - Skeleton shapes should match the expected content layout
   - Show loading state for a minimum perceptible duration (300ms)

   Empty states:
   - Every list/grid/table needs an empty state
   - Empty states should explain why it's empty and suggest action
   - Use illustration or icon + text pattern, not just text

   Error states:
   - Every data fetch must handle failure
   - Show user-friendly error messages (not stack traces or HTTP codes)
   - Provide retry action where applicable
   - Distinguish between network errors, server errors, and validation errors

   Edge cases:
   - Long text: verify truncation/wrapping behavior
   - Missing images: provide fallback/placeholder
   - Missing optional data: graceful degradation, not broken layout
   - Rapid interaction: debounce/throttle where needed
   - Concurrent actions: disable buttons during async operations

2. Fix all issues found.
3. Return a summary: [N] loading states added, [N] empty states added, [N] error states added, [N] edge cases fixed."

AGENT C — UX Copy (/design-copy):
Prompt for Agent C:
"You are a UX copywriter. Run the /design-copy skill instructions on this project. Your mission:

1. Audit all user-facing text in the application:

   Button labels:
   - Use action verbs: 'Save changes' not 'Submit', 'Create account' not 'Sign up'
   - Be specific: 'Delete project' not 'Delete', 'Add to cart' not 'Add'
   - Keep under 3 words where possible

   Headings and titles:
   - Clear hierarchy: page title > section title > subsection
   - Descriptive: tell users where they are and what they can do
   - Consistent capitalization (Title Case or Sentence case — pick one)

   Form labels and helpers:
   - Labels describe the field, not the format
   - Helper text explains requirements upfront, not after validation failure
   - Placeholder text is not a replacement for labels

   Error messages:
   - Tell the user what went wrong
   - Tell the user how to fix it
   - Use calm, helpful tone — not blame ('That email is already registered' not 'Error: duplicate email')

   Empty states and onboarding:
   - Guide users toward their first action
   - Use encouraging, active language

   Microcopy (tooltips, toasts, confirmations):
   - Confirmation dialogs: describe the consequences, not just 'Are you sure?'
   - Toast messages: confirm the action completed
   - Tooltips: clarify, don't repeat the label

2. Rewrite all copy that doesn't meet these standards.
3. Return a summary: [N] strings rewritten across [N] files."

Wait for all three agents to complete.

POST-MERGE:
- Agent A's changes are primarily in layout/style files.
- Agent B's changes are primarily in component logic and templates.
- Agent C's changes are primarily in text/string content.
- If any conflicts exist between agents, resolve them: structure > content > style.
- Commit each track separately for clean history:
  - "refactor: implement adaptive layouts and container queries"
  - "feat: add loading, empty, and error states across all views"
  - "copy: rewrite UX copy for clarity and consistency"

Do NOT stop. Proceed immediately to Phase 3.


============================================================
PHASE 3: VISUAL REFINEMENT
============================================================

The foundation is solid, the structure is hardened. Now make it beautiful. Use the critique findings from Phase 0 to determine which visual skills to apply.

STEP 3.1 — Conditional Visual Skills.
Based on the /design-critique findings and the top 5 problems, run the appropriate skills:

IF the UI is too bland / generic / safe:
- Run /design-amplify skill instructions
- Increase visual personality: bolder typography, stronger color use, distinctive component styling
- Add visual interest without sacrificing usability

IF the UI is too noisy / cluttered / overwhelming:
- Run /design-tone-down skill instructions first: reduce visual noise, simplify color palette, calm down competing elements
- Then run /design-simplify skill instructions: remove unnecessary UI elements, streamline flows, reduce cognitive load

IF the UI is lifeless / static / boring:
- Run /design-delight skill instructions: add personality moments, Easter eggs (subtle), satisfying micro-interactions
- Then run /design-animate skill instructions: add purposeful motion (see Phase 4 animation principles)

IF the UI needs color work (already handled partially in Phase 1):
- Run /design-color skill instructions again for deeper color refinement
- Focus on: color harmony, emotional tone, brand alignment

IF multiple conditions apply: run them in the order listed above. Tone down before amplifying. Simplify before adding delight.

STEP 3.2 — Run /design-polish skill instructions.
Regardless of which conditional skills ran, always run the final polish pass:
- Subpixel alignment and spacing precision
- Typography refinements (line-height, letter-spacing, font-weight tuning)
- Border radius consistency across the entire UI
- Shadow depth hierarchy (elevation system)
- Icon sizing and baseline alignment
- Input field styling consistency
- Button hierarchy clarity (primary > secondary > tertiary > ghost)
- Card and container internal spacing
- Divider visual weight
- Selection and highlight colors
- Focus ring styling (visible, consistent, on-brand)

STEP 3.3 — Animation pass.
Run /design-animate skill instructions if not already run in Step 3.1:
- Entrance/exit transitions for pages and modals
- Micro-interactions: button press, toggle, expand/collapse, hover
- Loading transitions: skeleton shimmer → content fade-in
- State changes: error shake, success checkmark, progress updates
- Scroll-triggered reveals (subtle parallax or fade-up)

Motion principles:
- 150-300ms for micro-interactions
- 300-500ms for page transitions
- ease-out for enters, ease-in for exits
- GPU-accelerated only (transform, opacity)
- Respect prefers-reduced-motion
- Every animation justifies its existence

STEP 3.4 — Commit.
- Commit message: "style: visual refinement — [list which skills were applied]"

Do NOT stop. Proceed immediately to Phase 4.


============================================================
PHASE 4: VERIFICATION
============================================================

Full re-audit to catch anything the overhaul introduced or missed.

STEP 4.1 — Run /design-audit skill instructions.
Complete re-audit of the overhauled UI:
- Visual hierarchy and layout consistency
- Typography scale adherence
- Color contrast (WCAG AA minimum)
- Spacing rhythm
- Component consistency
- Interactive states (hover, focus, active, disabled)
- Responsive behavior
- Accessibility (semantic structure, ARIA, keyboard nav, screen readers)
- Touch targets
- Loading, empty, and error states (should now all exist from Phase 2)
- Animation quality and performance
- Token usage (should be near 100% from Phase 1)

Classify all findings by severity: CRITICAL, HIGH, MEDIUM, LOW.

STEP 4.2 — Self-Healing Loop (max 2 iterations).
IF CRITICAL issues remain:
- Fix all critical issues immediately.
- Re-run audit on affected files only.
- If new critical issues appeared from fixes, fix those too.
- Max 2 fix-reaudit iterations.

IF only HIGH/MEDIUM issues remain after critical fixes:
- Fix HIGH issues.
- MEDIUM issues: fix if quick (<2 min each), otherwise document for future pass.

IF still failing after 2 iterations:
- Document remaining issues with full context.
- Classify as: architectural limitation, framework constraint, or needs manual design decision.
- Do not block the ship on MEDIUM/LOW issues.

STEP 4.3 — Run build.
- Detect and execute the project's build command.
- Fix any build failures immediately.

STEP 4.4 — Run tests.
- Detect and execute the project's test suite.
- Update snapshot tests if UI intentionally changed.
- Fix actual test regressions.

STEP 4.5 — Commit if fixes were needed.
- Commit message: "fix: resolve [N] post-overhaul audit issues"

Do NOT stop. Proceed immediately to Phase 5.


============================================================
PHASE 5: SHIP
============================================================

STEP 5.1 — Final state commit.
- If there are any remaining uncommitted changes, commit them.
- Commit message: "chore: finalize design overhaul"

STEP 5.2 — Push.
- Push all commits to the current branch.


============================================================
OUTPUT
============================================================

When all phases are complete, print a comprehensive before/after summary:

---
## Design Overhaul Complete

**Target:** [what was overhauled]
**Approach:** [which conditional visual skills were applied and why]

**Phase Timings:**
| Phase | Duration | Status |
|-------|----------|--------|
| 0 — Reconnaissance | [time] | done |
| 1 — Foundation | [time] | done |
| 2 — Structural (parallel) | [time] | done |
| 3 — Visual Refinement | [time] | done |
| 4 — Verification | [time] | done ([N] healing iterations) |
| 5 — Ship | [time] | done |
| **Total** | **[time]** | |

**Before/After Catalog:**
| Category | Before | After | Improvement |
|----------|--------|-------|-------------|
| Design tokens | [state] ([score]/5) | [state] ([score]/5) | [delta] |
| Color system | [state] ([score]/5) | [state] ([score]/5) | [delta] |
| Typography scale | [state] ([score]/5) | [state] ([score]/5) | [delta] |
| Spacing system | [state] ([score]/5) | [state] ([score]/5) | [delta] |
| Component consistency | [state] ([score]/5) | [state] ([score]/5) | [delta] |
| Animation/motion | [state] ([score]/5) | [state] ([score]/5) | [delta] |
| Responsive behavior | [state] ([score]/5) | [state] ([score]/5) | [delta] |
| Accessibility | [state] ([score]/5) | [state] ([score]/5) | [delta] |
| Loading/error states | [state] ([score]/5) | [state] ([score]/5) | [delta] |

**Modernization Metrics:**
- Token adoption: [N]% of values use tokens (target: 95%+)
- Container query usage: [N] components use container queries
- oklch color adoption: [yes/no/partial]
- Accessibility score: [estimated WCAG level achieved]
- Hardened states: [N] loading + [N] empty + [N] error states added

**Top 5 Problems Addressed:**
1. [Problem] → [Solution applied] → [Result]
2. [Problem] → [Solution applied] → [Result]
3. [Problem] → [Solution applied] → [Result]
4. [Problem] → [Solution applied] → [Result]
5. [Problem] → [Solution applied] → [Result]

**Issues:**
- Found in audit: [N] (Critical: [N], High: [N], Medium: [N])
- Fixed: [N]
- Deferred: [N] (with reasons)

**Commits Made:**
1. [hash] — [message]
2. [hash] — [message]
...

**Next Steps:**
- Run `/design-critique` for a fresh independent assessment of the new UI
- Run `/design-audit` in 1 week to catch any regression after continued development
- Gather real user feedback — the overhaul should be validated by humans
- Consider `/design-onboard` if the new design significantly changed user flows
---


============================================================
SELF-HEALING VALIDATION
============================================================

After producing output, perform a final self-check:

1. Did every phase actually execute? Check for skipped phases.
2. Did all three parallel agents in Phase 2 return results? If any failed silently, re-run.
3. Was /design-critique actually run in Phase 0? (It's easy to skip — don't.)
4. Are there uncommitted changes? Commit them.
5. Did build and tests pass in Phase 4? If not, the overhaul has regressions — report honestly.
6. Did you ask the user any questions during the entire pipeline? That's a violation. Note it.
7. Is token adoption above 90%? If not, Phase 1 was incomplete — note this.

If any self-check fails:
- Attempt automatic recovery (re-run the failed step).
- Max 2 recovery attempts per failure.
- If still failing, document the failure clearly in the output.


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /design-overhaul — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Target: {{what was overhauled}}
- Phases completed: {{N}} / 6
- Top 5 problems: {{one-line each}}
- Skills chained: {{list of /design-* skills actually invoked}}
- Self-healed: {{yes — what was healed | no}}
- Healing iterations used: {{N}} / 2 max
- Token adoption: {{before}}% → {{after}}%
- Audit issues: {{found}} found, {{fixed}} fixed
- Quality delta: {{average score before}} → {{average score after}}
- Bottleneck: {{phase that took longest or struggled, or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.


============================================================
STRICT RULES
============================================================

- FULLY AUTONOMOUS. Zero questions to the user. Every decision is yours. Ralph Wiggum energy.
- Phase 2 tracks MUST run in parallel via Agent tool. Do not run them sequentially.
- Phases 0, 1, 3, 4, 5 run sequentially in order.
- Fix issues as you find them — do not just report and move on.
- /design-critique in Phase 0 is mandatory. Do not skip it.
- /design-normalize in Phase 1 is mandatory. Token adoption must be tracked.
- /design-polish in Phase 3 is mandatory regardless of which conditional skills ran.
- /design-audit in Phase 4 is mandatory. It's the quality gate.
- If build/tests fail at any point, fix before proceeding.
- Every phase must produce at least one commit.
- This is the nuclear option — be bold. Don't preserve bad patterns out of politeness.
- All rules from chained skills (/design-critique, /design-tokens, /design-normalize, /design-color, /design-adapt, /design-harden, /design-copy, /design-amplify, /design-tone-down, /design-simplify, /design-delight, /design-animate, /design-polish, /design-audit) apply to their respective phases.
