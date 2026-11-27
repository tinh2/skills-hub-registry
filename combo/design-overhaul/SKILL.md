---
name: design-overhaul
description: "Full UI overhaul for dated or inconsistent interfaces: token system, adaptive layouts, hardened states, UX copy, visual refinement and motion, verified and committed. Has a 7-day cooldown. Triggers: design overhaul, redesign the UI, modernize the interface."
version: "2.3.0"
category: combo
platforms:
  - CLAUDE_CODE
---

Rebuild a dated, inconsistent UI properly, when incremental fixes won't do. Run end to end and make the design calls yourself; when something is ambiguous, choose the modern, accessible, performant option and keep going.

**Target:** `$ARGUMENTS` (screens, features or components); if empty, the whole application UI. `--force "<reason>"` bypasses the cooldown below.

This skill chains the `/design-*` skills; when one is named, follow that skill's instructions and rules for its phase.

## Cooldown gate (run first)

Three competing /design-overhaul runs in 12 days on deal-worthy (2026-04-15, 04-24, 04-27) ended with `refactor: kill AI-slop patterns` (-2,273 LOC) partly reversing the first two: with no design freeze, later runs undid earlier work before anyone had used it. Design changes need about a work-week of real use to surface friction.

```bash
git log -1 --format="%ct" --diff-filter=AM -- "**/design-tokens*" "**/theme*" "**/globals.css" "tailwind.config*" "**/styles/**"
git log --format="%ct %s" --all | grep -iE "design[- ]overhaul|refactor.*design|refactor.*ai[- ]slop" | head -3
```

If either shows a commit within the last 7 days, stop without changes and say: "Cooldown gate: previous design pass landed {N}d ago, within the 7-day cooldown. Use `--force \"<reason>\"` to override." Accept `--force` only with a reason, and put that reason in the commit bodies.

## Phase 0: Understand before demolishing

Map the frontend: framework and version, UI library, where screens/components/styles live, counts of screens and shared components. Score the current state 1-5 for: tokens, color system, type scale, spacing, component consistency, motion, responsive behavior, accessibility, dark mode, loading/error states. Run `/design-critique` (what works and should stay, what's mediocre, what's actively bad). Distill the **top 5 problems** by impact; they set the priorities.

## Phase 1: Foundation

Get this right first; everything else builds on it.

- `/design-tokens`: semantic colors in oklch (primary, secondary, accent, neutral, success, warning, error, info, each with hover/active/disabled/foreground), light and dark, WCAG AA contrast (4.5:1 text, 3:1 large). Spacing scale on a consistent ratio, fluid type scale with `clamp()` (size, line-height, tracking, weight), radius, elevation, durations (~150/250/400ms), easings, z-index layers.
- `/design-normalize`: replace hardcoded colors, sizes, spacing, radii, shadows, durations and z-indexes with tokens. Track found / replaced / intentionally skipped and the adoption rate; aim for 95%+.
- `/design-color` if color was a top-5 problem or scored 3 or below.
- Commit: `refactor: modernize design token system`.

## Phase 2: Structure (three parallel tracks)

These touch mostly separate files, so run them as parallel subagents when your harness supports it. Each returns a count summary.

- **Layouts (`/design-adapt`).** Grid/flex with gap spacing; media queries for page grids, container queries for components; mobile-first at 320/768/1024/1440+. No horizontal scroll, no meaning-hiding truncation, touch targets intact.
- **Hardening (`/design-harden`).** Skeletons shaped like the content for every fetch; empty states that explain and offer the next action; errors in plain language with retry, distinguishing network, server and validation; long text, missing images and missing optional data degrade gracefully; buttons disabled during async work; debounce where rapid input causes trouble.
- **Copy (`/design-copy`).** Specific verb labels ("Save changes", "Delete project"), one capitalization style, labels not placeholders, helper text before errors, errors that say what happened and how to fix it without blame, confirmations that state consequences.

Resolve conflicts with priority structure > content > style. Commit each track separately: `refactor: implement adaptive layouts and container queries`, `feat: add loading, empty, and error states`, `copy: rewrite UX copy for clarity and consistency`.

## Phase 3: Visual refinement

Pick from the critique, in this order when several apply: too noisy → `/design-tone-down` then `/design-simplify`; too bland → `/design-amplify`; lifeless → `/design-delight`; color still weak → `/design-color`. Tone down before amplifying, simplify before adding delight.

Always finish with `/design-polish` (alignment, type tuning, radius and elevation consistency, icon alignment, input and button hierarchy, visible on-brand focus rings) and `/design-animate`: 150-300ms micro-interactions, 300-500ms page transitions, ease-out in / ease-in out, transform and opacity only, `prefers-reduced-motion` respected, every animation earning its place.

Commit: `style: visual refinement (<skills applied>)`.

## Phase 4: Verify

Run `/design-audit` over hierarchy, type, contrast, spacing, consistency, interactive states, responsive, accessibility (semantics, keyboard, screen reader), touch targets, states, motion and token adoption. Fix every CRITICAL and HIGH, re-audit the affected files, up to 2 rounds; fix MEDIUMs that are quick and document the rest as architectural, framework-bound, or needing a human design decision. Build and run tests; update snapshots only for intentional changes. Commit `fix: resolve N post-overhaul audit issues` if needed, then commit anything left and push the branch.

Before reporting, confirm: every phase ran, all three Phase 2 tracks returned, the critique actually ran, nothing is uncommitted, build and tests pass (report honestly if not), token adoption is above 90% (otherwise say Phase 1 is incomplete).

## Output

```
## Design Overhaul Complete
Target: ... | Visual skills applied and why: ...

| Phase | Duration | Status |  (0 Recon ... 5 Ship, total)

| Category | Before (score/5) | After (score/5) | Delta |  (the 9 Phase 0 categories)

Token adoption N% | Container queries N | oklch yes/partial/no | est. WCAG level
Hardened: N loading + N empty + N error states

Top 5 problems: problem -> fix -> result
Issues: found N (C/H/M), fixed N, deferred N (reasons)
Commits: hash message
```

Next: a fresh `/design-critique`, `/design-audit` again in a week, and real user feedback.

## Telemetry

If a memory directory for this project exists under `~/.claude/projects/`, append to its `skill-telemetry.md`:

```
### /design-overhaul — YYYY-MM-DD
- Outcome: SUCCESS | PARTIAL | FAILED
- Target / Phases completed N/6 / Skills chained
- Token adoption: before% -> after%
- Audit issues: found, fixed; quality delta: avg before -> after
- Bottleneck / Suggestion for /evolve
```
