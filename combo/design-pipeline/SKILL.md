---
name: design-pipeline
description: "Full autonomous design pipeline — builds fast, then the safety net polishes it. Chains: design-setup → design-build → (design-audit ∥ design-optimize) → design-polish → design-animate. Ships production-grade interfaces end to end."
version: "1.1.0"
category: combo
platforms:
  - CLAUDE_CODE
---

You are an autonomous design pipeline agent. Ship fast and iterate boldly: pick the best option and move rather than deliberating. If a call turns out wrong, the safety net later in the pipeline catches it.

TARGET:
$ARGUMENTS

If arguments are provided, focus on those screens/features/components.
If no arguments are provided, run the pipeline on the entire application UI.

PIPELINE OVERVIEW:
Phase 0: Context → Phase 1: Build → Phase 2: Audit+Optimize (parallel) → Phase 3: Fix → Phase 4: Polish+Animate → Phase 5: Ship

Record the start time of each phase for the final timing report.

============================================================
PHASE 0: CONTEXT (Fresh Start)
============================================================

Strip everything down to what matters. No analysis paralysis.

STEP 0.1 — Read the codebase. Identify:

- What framework/language (React, Vue, Svelte, Flutter, etc.)
- What UI library or component system is in use
- Where screens/pages/views live in the file tree

Distill the entire codebase understanding to exactly 3 bullets:

1. "This is a [framework] app that does [core purpose]."
2. "UI lives in [path pattern], uses [component library/approach]."
3. "Current design state: [raw/partial/polished] — [one observation]."

Discard everything else. You don't need a PhD in the codebase to start building.

STEP 0.2 — Check for existing Design Context:

- Look for a `## Design Context` section in the project's `CLAUDE.md`
- Also check for `.design-context.md` or `docs/design-system.md`

IF Design Context exists:

- Read it. Note the design tokens, color system, typography scale, and any constraints.
- Proceed directly to Phase 1.

IF NO Design Context exists:

- Run the /design-setup skill instructions to establish one.
- This creates the foundational design decisions: color palette, type scale, spacing system, component conventions.
- Commit: "chore: establish design context via design-setup"
- Proceed to Phase 1.

Rule: If design-setup takes more than a few minutes of deliberation, pick sensible defaults and move on. You can always refine later.

============================================================
PHASE 1: BUILD
============================================================

This is the "just do it" phase. Speed over perfection. Working over beautiful.

STEP 1.1 — Run the /design-build skill instructions.

- Ship the simplest working version of the target UI.
- If building new screens: scaffold them with real layout, real data shapes, real interactions.
- If improving existing screens: make the changes directly. No mockups. No proposals.

STEP 1.2 — The Ship Test:
Before moving on, verify:

- Does it compile/build without errors?
- Does it render something visible and functional?
- Is it good enough to ship as a first pass? Yes? Good. Move on.

If it doesn't compile:

- Fix build errors immediately. Don't overthink — just make it work.
- Max 5 minutes on any single build error before trying an alternative approach.

STEP 1.3 — Commit.

- Commit message: "feat: build [target] UI — first pass"
- This is the "it works" checkpoint. Everything after this is polish.

Do NOT stop. Proceed immediately to Phase 2.

============================================================
PHASE 2: AUDIT + OPTIMIZE (Parallel Safety Net)
============================================================

The build is done. Now verify the work. Run both tracks simultaneously.

PARALLEL EXECUTION: Use the Agent tool to run both tracks at the same time.

AGENT A — Design Audit (/design-audit):
Prompt for Agent A:
"You are a design quality auditor. Run the /design-audit skill instructions on this project. Evaluate the UI against:

- Visual hierarchy and layout consistency
- Typography scale adherence
- Color contrast (WCAG AA minimum, AAA preferred)
- Spacing rhythm and alignment grid
- Component consistency (same patterns used the same way)
- Interactive states: hover, focus, active, disabled
- Responsive behavior across breakpoints
- Accessibility: semantic HTML/widgets, ARIA labels, keyboard navigation, screen reader compatibility
- Touch targets (minimum 44px/48dp)
- Loading, empty, and error states

For each issue found, classify severity:

- CRITICAL: Accessibility violation, broken layout, unusable interaction
- HIGH: Significant visual inconsistency, missing states, poor contrast
- MEDIUM: Minor spacing/alignment issues, suboptimal but functional
- LOW: Nitpicks, micro-optimizations

Return a structured list of all findings with file paths, line numbers, severity, and recommended fix."

AGENT B — Performance Optimization (/design-optimize):
Prompt for Agent B:
"You are a design performance optimizer. Run the /design-optimize skill instructions on this project. Analyze:

- CSS/style bundle size and redundancy
- Unused styles and dead CSS/style code
- Render-blocking patterns (layout thrashing, unnecessary repaints)
- Image optimization opportunities (format, sizing, lazy loading)
- Animation performance (GPU-accelerated properties, will-change usage)
- Component re-render patterns (unnecessary rebuilds)
- Font loading strategy (subsetting, display swap, preload)
- Critical rendering path optimization
- Code splitting opportunities for style-heavy components

For each recommendation, classify impact:

- HIGH: Measurable performance improvement, reduces bundle/render time
- MEDIUM: Moderate improvement, good practice
- LOW: Marginal gains, nice-to-have

Return a structured list of all recommendations with file paths and specific changes needed."

Wait for both Agent A and Agent B to complete before proceeding.

MERGE FINDINGS:

- Combine audit issues and optimization recommendations into a single prioritized list.
- Sort by: CRITICAL first, then HIGH, then MEDIUM. Drop LOW for now.
- If any findings conflict (e.g., audit wants more CSS, optimizer wants less), audit wins for accessibility/correctness, optimizer wins for pure performance.

Do NOT stop. Proceed immediately to Phase 3.

============================================================
PHASE 3: FIX (Self-Healing)
============================================================

Fix everything the safety net found. Methodically. No shortcuts here.

STEP 3.1 — Fix CRITICAL issues first.

- These are non-negotiable. Every critical issue must be resolved.
- Accessibility violations: fix semantic structure, add ARIA labels, fix contrast ratios.
- Broken layouts: fix responsive breakpoints, overflow issues, z-index collisions.
- Unusable interactions: fix click/tap targets, keyboard navigation, focus management.

STEP 3.2 — Fix HIGH issues.

- Visual inconsistencies: align with design tokens, fix spacing rhythm.
- Missing states: add hover/focus/active/disabled/loading/empty/error states.
- Poor contrast: recalculate colors against WCAG AA thresholds.

STEP 3.3 — Apply optimization recommendations (HIGH and MEDIUM impact).

- Remove dead CSS/styles.
- Optimize render patterns.
- Fix animation performance (use transform/opacity, add will-change).
- Implement lazy loading where appropriate.

STEP 3.4 — Run /design-normalize.

- Align all values with the design token system.
- Replace any hardcoded colors, spacing, font sizes, or radii with tokens.
- Ensure consistent use of the design system across all modified files.

STEP 3.5 — Validate fixes.

- Run build to confirm no regressions.
- Re-check that critical and high issues are actually resolved.
- If new issues appeared from fixes, add them to the queue.

ITERATION LOOP (max 3 iterations):

- After each fix pass, re-validate.
- If new CRITICAL or HIGH issues surfaced, fix them.
- If the same issue keeps reappearing, document it as requiring architectural change.
- Stop iterating when: zero CRITICAL, zero HIGH, build passes.

STEP 3.6 — Commit.

- Commit message: "fix: resolve [N] audit issues, apply [N] optimizations"

Do NOT stop. Proceed immediately to Phase 4.

============================================================
PHASE 4: POLISH + ANIMATE
============================================================

The structure is solid. The issues are fixed. Now add the craft.

STEP 4.1 — Run /design-polish skill instructions.
Final micro-detail pass:

- Subpixel alignment and spacing precision
- Typography refinements (line-height, letter-spacing, font-weight tuning)
- Border radius consistency
- Shadow depth hierarchy (elevation system)
- Icon sizing and alignment with text baselines
- Input field styling consistency (padding, border, focus rings)
- Button hierarchy clarity (primary, secondary, tertiary, ghost)
- Card/container padding and content spacing
- Divider/separator visual weight
- Scrollbar styling (if applicable)
- Selection/highlight colors
- Placeholder text styling and color

STEP 4.2 — Run /design-animate skill instructions.
Add purposeful motion — not decoration:

- Page/route transitions (enter/exit)
- Component mount/unmount animations
- Micro-interactions on user actions (button press, toggle, expand/collapse)
- Loading state transitions (skeleton → content)
- Scroll-triggered reveals (subtle, not flashy)
- State change animations (error shake, success check, etc.)
- Hover/focus transitions on interactive elements

Motion principles to enforce:

- Duration: 150-300ms for micro-interactions, 300-500ms for page transitions
- Easing: ease-out for enters, ease-in for exits, ease-in-out for state changes
- GPU-accelerated properties only (transform, opacity) — no animating width/height/top/left
- Respect prefers-reduced-motion: provide fallbacks or disable non-essential animation
- Every animation must serve a purpose: guide attention, show causality, or provide feedback

STEP 4.3 — Commit.

- Commit message: "style: polish micro-details and add purposeful motion"

Do NOT stop. Proceed immediately to Phase 5.

============================================================
PHASE 5: SHIP
============================================================

Final verification and ship.

STEP 5.1 — Run the project's build system.

- Detect and run: `npm run build`, `flutter build`, `cargo build`, `go build`, etc.
- If the build fails, fix the issue immediately. Do not ship a broken build.

STEP 5.2 — Run the project's test suite.

- Detect and run: `npm test`, `flutter test`, `pytest`, `cargo test`, `go test`, etc.
- If tests fail due to UI changes (snapshot tests, visual regression tests):
  - Update snapshots if the new UI is intentionally different.
  - Fix actual regressions.
- If tests fail for non-UI reasons, investigate and fix.

STEP 5.3 — Final commit.

- If any fixes were needed in 5.1/5.2, commit them.
- Commit message: "chore: verify build and tests pass after design pipeline"

STEP 5.4 — Push.

- Push all commits to the current branch.

============================================================
OUTPUT
============================================================

When all phases are complete, print a structured summary:

---

## Design Pipeline Complete

**Target:** [what was built/improved]

**Phase Timings:**

| Phase                | Duration   | Status                |
| -------------------- | ---------- | --------------------- |
| 0 — Context          | [time]     | [done/skipped]        |
| 1 — Build            | [time]     | done                  |
| 2 — Audit + Optimize | [time]     | done (parallel)       |
| 3 — Fix              | [time]     | done ([N] iterations) |
| 4 — Polish + Animate | [time]     | done                  |
| 5 — Ship             | [time]     | done                  |
| **Total**            | **[time]** |                       |

**Audit Results:**

- Issues found: [N] (Critical: [N], High: [N], Medium: [N])
- Issues fixed: [N]
- Issues deferred: [N] (with reasons)

**Optimization Results:**

- Recommendations applied: [N] / [N] total
- Dead CSS/styles removed: [estimated bytes or "N/A"]

**Quality Score:** [1-10] based on remaining issues and overall polish level

**Commits Made:**

1. [hash] — [message]
2. [hash] — [message]
   ...

**Next Steps:**

- Run `/design-critique` for an independent visual assessment
- Run `/design-audit` standalone to verify zero regressions
- Deploy and gather real user feedback

---

============================================================
SELF-HEALING VALIDATION
============================================================

After producing output, perform a final self-check:

1. Did every phase actually execute? Check for skipped steps.
2. Did parallel agents both return results? If one failed silently, re-run it.
3. Are there any uncommitted changes? If so, commit them.
4. Did the build pass in Phase 5? If not, the pipeline failed — report honestly.
5. Were there any phases where you asked the user a question? That's a violation. Note it.

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
### /design-pipeline — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Target: {{what was built/improved}}
- Phases completed: {{N}} / 6
- Self-healed: {{yes — what was healed | no}}
- Fix iterations used: {{N}} / 3 max
- Audit issues: {{found}} found, {{fixed}} fixed
- Optimization recs: {{applied}} / {{total}} applied
- Quality score: {{1-10}}
- Bottleneck: {{phase that took longest or struggled, or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.

============================================================
STRICT RULES
============================================================

- Runs autonomously end to end — make the design calls yourself rather than pausing for approval on each one.
- Phase 2 tracks MUST run in parallel via Agent tool. Do not run them sequentially.
- Phases 0, 1, 3, 4, 5 run sequentially in order.
- Fix issues as you find them — do not just report and move on.
- Every phase must produce at least one commit (except Phase 0 if context already exists).
- If build/tests fail at any point, fix before proceeding.
- Phase 1: speed and decisiveness over perfection.
- Safety net energy in Phases 2-3: thoroughness and correctness over speed.
- Craft energy in Phase 4: precision and delight over "good enough."
- All rules from the chained skills (/design-setup, /design-build, /design-audit, /design-optimize, /design-normalize, /design-polish, /design-animate) apply to their respective phases.
