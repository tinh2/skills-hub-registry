---
name: brand-safe-design-pass
description: "Raise a site's perceived production value with a rigorous UI/UX pass while PROVING no user-facing word changed. Triggers: the user says \"make it look expensive\", \"premium design pass\", \"make it feel designed\", \"rigorous design audit\"."
version: "1.0.1"
category: analyze
platforms: [CLAUDE_CODE]
---

# Brand-Safe Design Pass

A design pass on someone else's words. Two jobs, in this order:

1. **Prove nothing was reworded.** Every visible string, aria-label, alt, title
   and meta description is snapshotted before the pass and diffed after.
2. **Raise the craft.** Typography, spacing, depth, interaction states.

Job 1 is the point. Any model can restyle a page; the failure mode that burns
trust is a heading that reads slightly differently afterwards and nobody
noticing until the client reads their own site back.

Reordering sections is allowed. Rewording is not. The guard compares a
multiset, so moving a block passes and editing a word fails.

============================================================
=== PRE-FLIGHT ===
============================================================

Before starting, verify:

- [ ] **The site is running and reachable.** A local preview of a PRODUCTION
      build, not a dev server: dev builds skip minification and can differ in
      computed styles. Get the URL from the user or from the project's
      preview script.
- [ ] **Playwright with Chromium is available.** Prefer the project's own
      install. Probe: `node -e "import('playwright').then(()=>console.log('ok'))"`.
      If absent, check for a Python one before installing anything.
- [ ] **Any gate blocking page access is bypassable.** Password walls,
      "under construction" curtains and cookie interstitials will otherwise be
      the thing you audit. Find how the project bypasses it (usually a
      localStorage key or a cookie) and set it in an init script.
- [ ] **The routes are enumerated.** Include the 404 route. It is a real page
      with real navigation and it is the one everybody forgets.
- [ ] **The repo is clean or the user accepts uncommitted changes.**

If any check fails: say which one and stop. Do NOT audit a dev server, a
login wall, or a page you cannot see. A design report on the wrong pixels is
worse than no report.

============================================================
=== PHASE 1: LOCK THE COPY ===
============================================================

Copy `references/check-copy-integrity.mjs` into the project's script
directory, wire two package scripts, and take the baseline:

```
copy:snapshot -> node scripts/check-copy-integrity.mjs --write
check:copy    -> node scripts/check-copy-integrity.mjs
```

Add `.copy-snapshot.json` to `.gitignore`. Run the snapshot. Report the
string count — it is the number you are accountable for at the end.

VALIDATION: `.copy-snapshot.json` exists and the count is plausible for the
page volume. A suspiciously low count means the gate was not bypassed and you
snapshotted an interstitial.
FALLBACK: if the count looks wrong, fix the bypass and re-snapshot BEFORE any
CSS is touched. A baseline taken after an edit is worthless.

============================================================
=== PHASE 2: CRITIQUE ===
============================================================

Invoke `/design-critique` against the running site, both themes if the site
has them. Require file-level evidence for every finding — a critique that
cannot name a file is an opinion.

Then build the factual inventory yourself, because it is cheap and it turns
taste into arithmetic:

```bash
grep -rhoE "#[0-9a-fA-F]{3,8}\b" src/ --include="*.css" --include="*.astro" | sort -u | wc -l
grep -rhoE "border-radius:[^;]+;" src/ | sort | uniq -c | sort -rn
grep -rhoE "(padding|margin|gap)[a-z-]*:\s*[^;]*;" src/ | grep -v "var(--" | sort | uniq -c
```

Healthy: one or two radius values, two or three shadows, almost no untokenized
spacing. A long tail of one-off values is the measurable form of "unconsidered".

**Rule out instrument error before reporting anything.** Three artifacts have
each produced a confident, wrong finding:

- **Blank bands in a full-page screenshot** are scroll-driven reveals sitting
  at their START state, not missing content. Verify by scrolling each element
  into view and re-reading opacity. Report a reveal as broken only if it stays
  faded WHILE in view.
- **A "near-black" translucent header** is your colour parser failing. See
  Phase 5.
- **SVG text with the wrong colour** is you reading `color`. SVG text is
  painted by `fill`.

VALIDATION: every finding names a file and a measured number.
FALLBACK: drop any finding you cannot reproduce twice. Shipping a false
positive costs more credibility than missing a real issue.

============================================================
=== PHASE 3: DESIGN INTELLIGENCE, FILTERED ===
============================================================

Invoke `/ui-ux-pro-max` for the interaction-state, elevation and spacing lens.

**If the project already has a brand guide, REJECT its palette and typography
output.** These generators return an industry-average system — a blue and
orange palette with a neutral grotesque — which is precisely the generic look
the user is paying to escape. Adopting it over a real brand guide is the
single worst outcome of this skill.

Keep: state layers, elevation scale, press feedback, stagger timing, tabular
figures, focus rings, target sizes.
Discard: palette, font pairing, and any "recommended pattern" that contradicts
the existing information architecture.

VALIDATION: the brand's own tokens are still the source of truth after this
phase. Diff the token block to confirm it is untouched.

============================================================
=== PHASE 4: IMPLEMENT ===
============================================================

Fix in this order — cheapest perceptual win first:

1. **Typography tuned FOR THE FACE IN USE.** After any font swap, re-audit the
   craft layer. Per-level `letter-spacing` written for the old face survives
   the swap and silently ruins display type. A sturdy modern with tight
   sidebearings wants negative tracking at display size; an old-style serif
   with generous sidebearings and a small x-height wants neutral to slightly
   positive. Applying the former's values to the latter closes the counters
   and reads as cheap without anyone being able to say why. Grep the whole CSS
   layer for the OLD font name after any swap: comments, dead selectors and
   `font-optical-sizing` claims all outlive it.
2. **Line length.** Nothing above ~75 characters. Measure, do not eyeball:
   `width / (fontSize * 0.5)`. Check the legal and safety text especially —
   it is usually in a wide container nobody styled, so the most important
   sentence on the site ends up the hardest to read.
3. **Interaction states that REINFORCE.** A hover that removes an affordance
   is a bug even when it looks elegant. Underlines should thicken or draw in,
   never erase. Animate two background layers so the resting rule never moves
   and nothing reflows.
4. **Depth and press feedback**, on transform and opacity only.

VALIDATION: after each fix, re-measure the specific number that was wrong.
FALLBACK: if a fix moves a problem rather than removing it, that is the same
bug in a new place. Keep going.

============================================================
=== PHASE 5: VERIFY ===
============================================================

Run, in order. All must pass:

1. **`check:copy`** — the whole point. Zero drift.
2. **axe** across all routes and themes, if the project has it.
3. **`references/check-contrast.mjs`** — hover-state contrast. Copy it in and
   wire `check:contrast`.
4. `/mobile-sweep` at 360, 390 and 768.
5. The project's own gates.

**Two things this phase exists to catch, both of which passed every other
gate at the time:**

- **axe only audits the RESTING page.** It never moves the mouse. A
  section-level hover rule once painted near-black body text onto a dark green
  panel at 1.37:1 while every automated check stayed green. If a dark panel is
  nested inside a section, it needs an opt-out class so section hover rules
  cannot recolour it.
- **Never parse colour strings.** `getComputedStyle` returns whatever colour
  space the CSS produced. A `color-mix()` header resolves to
  `oklab(0.95 0.0008 0.0086 / 0.88)`, and reading numbers out of that reports
  a cream header as near-black — 30 false failures in one run. Resolve colour
  by PAINTING it to a 1x1 canvas and reading the pixel back, then composite
  translucent layers down to the first opaque one. `check-contrast.mjs` does
  this; use it rather than rewriting it.

If `/mobile-sweep`'s bundled script cannot bypass the site's access gate, run
its four checks directly (off-screen overflow, sub-44px targets, clipped
labels, over-wide modals) with the WCAG 2.5.8 exemption for inline links in
prose. Say that you did so and why. Do not report a sweep of an interstitial
as a sweep of the site.

VALIDATION: `check:copy` passes. If it fails, you changed words. Revert those
specific edits — do not update the snapshot to match.
FALLBACK: a genuinely necessary copy change means stopping and asking. It is
outside this skill's remit.

============================================================
=== SELF-REVIEW ===
============================================================

Score (1-5):

- **Complete:** did every phase run, and does `check:copy` pass?
- **Robust:** was each finding measured rather than asserted? Were the three
  instrument artifacts ruled out?
- **Clean:** would the diff read as considered to a designer, with each change
  justified by a number?

Below 4 on any axis: name the gap. Fix it if fixable this run, otherwise
report it as a known limitation. Never report a design pass as complete while
the copy guard is failing or unrun.

============================================================
=== LEARNINGS CAPTURE ===
============================================================

Append one entry to `~/.claude/skills/brand-safe-design-pass/LEARNINGS.md`:

```markdown
## <YYYY-MM-DD> — <project + stack>

- **What worked:** <the change with the biggest perceptual return per line of diff>
- **What was awkward:** <a false positive, a gate that could not be bypassed, a skill whose output had to be rejected>
- **Suggested patch:** <one concrete improvement to these instructions>
- **Verdict:** [Smooth / Minor friction / Major friction]
```
