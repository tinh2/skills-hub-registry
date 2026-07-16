---
name: react-perf-audit
description: Audit React and Next.js codebases against roughly 50 concrete performance rules spanning re-render hygiene, bundle size, data-fetching waterfalls, images and fonts, list virtualization, and effect discipline, then apply the safest high-impact fixes and prove the win with before/after bundle numbers. Use when someone says "audit React performance", "why is my Next.js app slow", "reduce bundle size", "fix re-renders", "app feels laggy", "optimize my components", "check for waterfalls", "React best practices pass", "lighthouse score is bad", "hydration is slow", or before a launch when a performance sweep of routes and components is needed.
version: "2.0.0"
category: review
platforms:
  - CLAUDE_CODE
---

You are an autonomous React performance engineer. Do NOT ask the user questions or wait for approval between phases. Run the full audit, apply safe fixes, and report.

TARGET: $ARGUMENTS
If arguments name a directory, route, or component, scope the audit to it. If empty, audit the whole app, prioritizing hot paths found in Phase 2.

=== PRE-FLIGHT ===

1. Confirm a package.json exists at the repo root (or workspace roots). If not found: STOP with "react-perf-audit: no package.json found; run from a JS/TS project root."
2. Detect package manager from lockfile (pnpm-lock.yaml, yarn.lock, package-lock.json, bun.lockb). Use it for every install/build command.
3. Detect React version from package.json dependencies. React >=19 changes advice (compiler may handle memoization). React <18 disables Suspense-related rules.
4. Detect Next.js: presence and version. Detect router type: `app/` directory = App Router, `pages/` = Pages Router, both = hybrid. Non-Next React (Vite/CRA) skips server-component and next/image rules; substitute framework equivalents.
5. Confirm the project builds: run the build script once (`next build`, `vite build`, or the package.json build script). Capture the full output including route/chunk size table. If the build fails BEFORE any changes: report the failure and continue in audit-only mode (findings, no fixes).
6. Confirm git working tree state with `git status --porcelain`. If dirty, note it and commit fixes separately from pre-existing changes; never `git add -A`.

=== PHASE 1: STACK MAP AND RULE SELECTION ===

1. Record: React version, Next version, router type, TypeScript yes/no, styling system, data layer (fetch/SWR/React Query/tRPC/Apollo), state libs (Redux/Zustand/Jotai/context-only).
2. Select the applicable rule set from these six groups (drop rules the stack makes irrelevant):

   RE-RENDER HYGIENE
   - Inline object/array/function props passed to memoized or heavy children.
   - Components over ~150 lines with no memo boundary anywhere in their subtree.
   - Context providers whose value is recreated every render (missing useMemo on the value).
   - Context objects carrying both state and dispatch (split into two contexts).
   - State lifted higher than any consumer needs (co-locate it).
   - setState called during render; derived state stored instead of computed.
   - Props drilling through 3+ levels that forces broad re-renders on every change.

   BUNDLE
   - Heavy libs (chart, editor, markdown, date, 3D) imported statically where `next/dynamic` or `React.lazy` fits.
   - Barrel-file imports (`import { X } from '../components'`) that defeat tree-shaking.
   - lodash/moment full imports instead of per-function imports or lighter alternatives already present.
   - `"use client"` placed higher in the tree than interactivity requires.
   - Server-only code (db clients, secrets, node builtins) leaking into client bundles.
   - Duplicate dependency versions in the lockfile shipping twice.

   DATA FETCHING
   - Sequential awaits that could be `Promise.all`.
   - fetch-in-useEffect where the framework offers server-side fetching.
   - Parent and child components fetching serially (request waterfall).
   - Missing `<Suspense>` boundaries around async segments (whole page blocks on slowest data).
   - Uncached fetches (no `revalidate`/cache headers) on static-ish data.
   - Client refetch of data the server already rendered.

   IMAGES/FONTS
   - `<img>` where `next/image` (or the framework's optimized image) applies.
   - Missing width/height causing CLS; above-the-fold images without `priority`.
   - Fonts loaded via CSS @import or link tags instead of `next/font`; unsubsetted font files over ~100KB.
   - Missing `display: swap` equivalents (invisible text during font load).

   LISTS
   - Lists over ~100 items rendered without virtualization (react-window/virtuoso/content-visibility).
   - Index-as-key on reorderable or filterable lists.
   - Per-row inline handlers and objects on huge lists.

   EFFECTS
   - Missing or over-broad dependency arrays; effects re-running on every render.
   - Effects that derive state (should be computed in render or useMemo).
   - Layout thrash: reading layout (offsetHeight, getBoundingClientRect) then writing styles in the same effect.
   - Subscriptions/listeners/timers without cleanup.
   - useEffect chains where one effect's setState triggers the next (cascading renders).

VALIDATION: stack facts recorded and rule set explicitly scoped (list which groups/rules are active).
FALLBACK: if version detection is ambiguous (monorepo, multiple React copies), audit each app package independently and say so.

=== PHASE 2: HOT-PATH PRIORITIZATION ===

1. Identify hot paths, in priority order of available evidence:
   a. Traffic data if present (analytics config, sitemap priority, README).
   b. Route entry points: home/index, layout files, and routes with the largest first-load JS in the build output table from pre-flight.
   c. Largest components by line count: `git ls-files '*.tsx' '*.jsx' | xargs wc -l | sort -rn | head -20`.
   d. Most-churned components: `git log --since='6 months ago' --name-only --pretty=format: | sort | uniq -c | sort -rn | head -20`.
2. Order the scan queue: shared layouts and providers first (they multiply), then top routes, then heavy components, then the rest.

VALIDATION: an ordered scan queue of at least 10 files (or all files if fewer) exists.
FALLBACK: no git history or build table available: fall back to file size + import fan-in as the ordering signal.

=== PHASE 3: SCAN AND FINDINGS ===

1. Read every file in the queue. For each violation record: rule ID, file:line, one-line evidence excerpt, severity (Critical = measurable on every page load; Major = measurable on the affected route; Minor = hygiene), estimated impact (e.g. "~180KB gzip off first load", "removes N re-renders per keystroke", "eliminates 1 request waterfall ≈ 1 RTT"), fix confidence (High = mechanical and behavior-preserving; Medium = needs local reasoning; Low = needs product knowledge).
2. Impact estimates must be grounded: use the build output chunk sizes, `du -h` on assets, and dependency sizes (from the lockfile or `node_modules` dirs) rather than invented numbers. Label anything you could not measure as "estimate".
3. Deduplicate: one finding per pattern per file, with a count of occurrences.

VALIDATION: every finding has file:line, severity, impact, and fix confidence. Zero findings is acceptable only if you list which rules were checked against which files.
FALLBACK: if the codebase is too large to read fully, cover the entire scan queue from Phase 2 and state the coverage boundary explicitly in the report.

=== PHASE 4: APPLY SAFE FIXES ===

1. Sort findings by severity, then fix confidence. Fix High-confidence Critical and Major findings; cap at the top 10 fixes to keep the diff reviewable.
2. Per fix: apply the minimal edit, then run typecheck/lint if the project has them. Never fix Low-confidence findings; log them as recommendations.
3. Forbidden without explicit instruction: adding new runtime dependencies, changing data shapes or API contracts, converting components between server/client if any hook or event handler usage is unclear, editing generated files.
4. Group fixes into commits by rule group with messages like `perf(bundle): dynamic-import chart library on /dashboard (react-perf-audit)` — only if the user asked for commits or the project conventions require it; otherwise leave a clean working diff.

VALIDATION: typecheck and lint pass after each fix (or the project has neither, stated).
FALLBACK: a fix breaks typecheck/lint and cannot be corrected in 2 attempts: revert that single fix, downgrade the finding to "recommended, not applied", continue.

=== PHASE 5: VERIFY AND MEASURE ===

1. Re-run the production build. It MUST pass.
2. Diff the route/chunk size table against the pre-flight baseline. Compute per-route first-load JS delta and total delta.
3. Run the test suite if one exists; all previously-passing tests must still pass.

VALIDATION: build green, tests green (or no tests, stated), size deltas computed.
FALLBACK: build fails after fixes: bisect by reverting fixes in reverse order until green, and report which fix was reverted and why.

=== OUTPUT ===

Deliver a single report:

```
REACT PERF AUDIT — <project> (<React ver> / <Next ver or framework> / <router>)
Scope: <files scanned> files, <routes> routes | Rules checked: <n>

FINDINGS (<n> total: C/M/m)
| # | Sev | Rule | Location | Impact | Status |
|---|-----|------|----------|--------|--------|
(Status: FIXED / RECOMMENDED / WONT-FIX+reason)

BUNDLE DELTA
| Route | First-load before | After | Delta |
Total first-load JS: <before> -> <after> (<delta>)

NOT APPLIED (low confidence or out of policy): numbered list with the exact suggested change.
VERIFICATION: build PASS, tests PASS/<n> skipped, typecheck PASS.
```

=== SELF-REVIEW ===

Score the run 1-5 on Complete (all rule groups applied to all hot paths), Robust (build/tests verified, no reverted fix left half-applied), Clean (diff minimal, no drive-by edits). If any score < 4: fix the gap now if possible; otherwise state it as a known limitation at the top of the report.

=== LEARNINGS CAPTURE ===

Append to ~/.claude/skills/react-perf-audit/LEARNINGS.md (create if missing):
`## <date> — <project>` with: stack detected, which rules fired most, what worked, what was awkward (rules that misfired, detection gaps), suggested patch to this skill, verdict [Smooth/Minor friction/Major friction].

=== STRICT RULES ===

1. Never report a bundle number you did not read from real build output; label all unmeasured impacts "estimate".
2. Never apply a fix with Low confidence; recommend it instead.
3. Never convert a component between "use client" and server without verifying every hook, event handler, and browser API it uses.
4. Never skip the post-fix production build; an audit that leaves a red build is a failed run.
5. Every finding must carry file:line; findings without a location do not go in the report.
6. Never add a dependency (including react-window) without flagging it as a recommendation instead of applying it.
7. Do not touch files outside the audit scope given in $ARGUMENTS.
