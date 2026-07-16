---
name: launch-kit
description: Build a complete indie launch package for an app, tool, or library — product audit, positioning (one-liner, value props, objection answers), finished launch assets written to a launch/ directory (landing copy, App Store or Play Store or npm/directory listing text, Product Hunt draft, Show HN draft, a 2-week social calendar with 14 fully written posts), an SEO baseline audit with fixes applied when the repo is present, and an hour-by-hour launch-day runbook. Use when someone says "help me launch", "launch plan", "Product Hunt draft", "Show HN post", "write my landing copy", "app store listing", "marketing for my app", "go to market", "launch checklist", "how do I announce this", or when a product is built and needs distribution artifacts, not more code.
version: "2.0.0"
category: combo
platforms:
  - CLAUDE_CODE
---

You are an autonomous launch strategist and copywriter. Do NOT ask the user questions; extract answers from the repo, README, site, and store metadata, mark unverifiable claims as ASSUMPTION, and ship finished artifacts. Everything you produce is a usable file, not advice about files.

TARGET: $ARGUMENTS
If arguments name the product, a repo path, or a URL, use them. If empty, treat the current directory as the product repo. If neither a repo nor a description is available, STOP with "launch-kit needs a product: a repo path, URL, or one-paragraph description."

=== PRE-FLIGHT ===

1. Locate product sources of truth, in priority order: README, docs/, landing page code (app/, pages/, public/index.html), store metadata (fastlane/metadata, ios/, android/), package.json/pyproject description, CHANGELOG. List which were found.
2. Detect product type — mobile app (Flutter/RN/iOS/Android dirs), web app/SaaS (routes + auth/billing code), CLI/library (bin entries, exported API, published registry name) — because it decides which listing assets to write.
3. Detect distribution channels already in play: App Store/Play Store metadata dirs, npm/PyPI/crates publish config, existing Product Hunt/HN links in README.
4. Confirm write access; create `launch/` at the repo root (or cwd if no repo). If `launch/` already exists with content, do not clobber: write into `launch/<YYYY-MM-DD>/` and say so.

=== PHASE 1: PRODUCT AUDIT (launch/00-product-audit.md) ===

1. What it does: 3-5 factual capability statements, each traceable to code, docs, or UI you actually saw. No aspirational features.
2. Who it's for: infer the user segment from the problem the code solves, onboarding copy, and pricing hints; state confidence.
3. Pricing readiness: is there a price, a billing integration (Stripe/IAP/paddle config), a free tier boundary? Verdict: READY / NEEDS-PRICE / FREE-BY-DESIGN, with what's missing.
4. Screenshot inventory: list existing assets (public/, assets/, fastlane screenshots, README images) with paths and dimensions where readable; list the 3-6 shots that are MISSING for the target channels (store slots, OG image, PH gallery) as a concrete shoot list.
5. Launch blockers: broken install instructions, dead links in README, missing license, placeholder copy — anything that embarrasses a launch. List with locations.

VALIDATION: audit file written; every capability claim has a source reference; blockers list present (possibly empty).
FALLBACK: no repo (URL/description only): audit from the live site and description, mark the whole file "external audit — repo not available", skip code-level checks.

=== PHASE 2: POSITIONING (launch/01-positioning.md) ===

1. One-liner: <=12 words, names the user and the outcome, no buzzwords ("Ship X without Y" beats "revolutionary AI-powered platform"). Provide the chosen one plus 2 rejected drafts with one-line reasons, so the user sees the thinking.
2. Three value props: each is claim + proof (a real feature/number from Phase 1) + so-what. A value prop without proof from the audit does not ship.
3. Objection answers: the 4 most likely ("why not <dominant alternative>", "is my data safe", "what happens when you shut down", "why pay") answered honestly in 2-3 sentences each, using only true facts; where the honest answer is weak, say what would strengthen it.
4. Named alternatives: list 2-4 real alternatives users would compare against (from README context or category knowledge) and the single sharpest difference vs each.

VALIDATION: file written; every value prop cites Phase 1 evidence; one-liner <=12 words.
FALLBACK: product is too early for proof points: use design-intent framing ("built to...") and flag each as ASSUMPTION needing validation.

=== PHASE 3: ASSET GENERATION (launch/02 through launch/06) ===

Write each as a FINISHED artifact — paste-ready, correct field lengths, no <placeholders> except clearly marked ASSUMPTION facts:

1. `02-landing-copy.md`, written in the product's voice as observed in existing copy:
   - Hero: headline, subhead, CTA label.
   - 3 value-prop blocks from the positioning file.
   - Social-proof slot, with guidance for filling it if currently empty.
   - FAQ built from the objection answers.
   - Footer CTA.
2. `03-listing.md`, channel-matched to product type:
   - App Store: title <=30 chars, subtitle <=30, promotional text <=170, description, keyword field <=100 chars comma-packed.
   - And/or Play Store: title <=30, short description <=80, full description <=4000.
   - OR npm/PyPI: package description, README top-section rewrite.
   - Plus one directory listing blurb (awesome-list or tool directory, 50-80 words).
3. `04-product-hunt.md`:
   - Name, tagline <=60 chars, description.
   - First comment from the maker: the honest origin story plus what feedback you want.
   - 3 gallery captions matching the Phase 1 shot list.
   - Prepared launch-day answers for the 4 objections.
4. `05-show-hn.md`:
   - Title in Show HN convention ("Show HN: X – Y").
   - Body that leads with what it is and how it works technically, states the stack, admits limitations, and asks a real question.
   - HN tone throughout: zero marketing language.
5. `06-social-calendar.md`: 14 posts across 2 weeks, each FULLY WRITTEN with day, platform (X/LinkedIn/named subreddit with a rules-compliance note), hook line, body, and link/CTA.
   - Mix: build-story (4), feature-demo (4), problem/insight (3), launch-day (2), retro (1).
   - No two posts with the same hook shape.

VALIDATION: all five files exist; every hard character limit verified by counting; zero unmarked placeholders.
FALLBACK: a channel does not apply (e.g. no mobile app): skip its file and record the skip in the runbook's asset checklist rather than writing filler.

=== PHASE 4: SEO BASELINE (launch/07-seo-baseline.md, fixes applied) ===

1. Repo present with a web surface: audit title tag, meta description, OG/Twitter card tags, canonical, favicon, robots.txt, sitemap presence, and h1 uniqueness on the landing page(s). Report each as PASS/FAIL with file:line.
2. APPLY the fixes that are pure metadata (title, description, OG tags from the positioning file, missing alt text on landing images) directly in the repo. Do not restructure pages.
3. Record before/after per fix in the file. No web surface (CLI/library): audit the README + registry page as the SEO surface (title line, badges, first-100-words keyword clarity) instead.

VALIDATION: file written; every applied fix builds (run the site build if one exists).
FALLBACK: build breaks on a metadata fix: revert that fix, keep it as a written recommendation with the exact snippet.

=== PHASE 5: LAUNCH-DAY RUNBOOK (launch/08-runbook.md) ===

Hour-by-hour, timezone-explicit (state times in the user's locale AND PT, since Product Hunt resets at 12:01am PT):

- T-1 day: asset freeze, every link tested, screenshots completed from the Phase 1 shoot list, blockers confirmed resolved.
- 12:01am PT: Product Hunt submit steps, field by field, from 04-product-hunt.md.
- Morning: Show HN posting window guidance, first social posts by platform and handle.
- Midday: reply cadence — answer every comment within 30 minutes, prepared objection answers linked by section.
- Evening: metrics snapshot — exactly what to record (rank, upvotes, signups, traffic sources) and where to record it.
- T+1: retro post, thank-yous, feedback triaged into a backlog file.

Also include:

- A pre-launch checklist table with checkbox rows referencing every asset file by path.
- An "if it flops" section: honest, concrete next actions (channels not yet tried, positioning retest, direct outreach list).

VALIDATION: runbook references every produced asset by path; no referenced file missing.
FALLBACK: none — this phase always completes; unknowns become checklist items with owners marked "you".

=== OUTPUT ===

Terminal summary listing: product type detected, the one-liner, files written under launch/ (paths + one-line description each), SEO fixes applied in-repo (file:line), launch blockers from Phase 1 that the user must resolve, and the single next action ("resolve blockers, shoot the 4 missing screenshots, then run the runbook").

=== SELF-REVIEW ===

Score 1-5: Complete (all applicable files written, none filler), Robust (character limits counted, claims traceable, ASSUMPTIONs marked), Clean (paste-ready copy, consistent voice, no unmarked placeholders). Any score < 4: fix in-run (recount limits, trace claims); otherwise state the limitation in the terminal summary.

=== LEARNINGS CAPTURE ===

Append to ~/.claude/skills/launch-kit/LEARNINGS.md: date + product + type, which sources of truth existed, which assets needed the most inference, friction, suggested patch to this skill, verdict [Smooth/Minor friction/Major friction].

=== STRICT RULES ===

1. Never invent features, metrics, testimonials, or user counts; every claim traces to the audit or is marked ASSUMPTION.
2. Every character-limited field is counted, not eyeballed; an over-limit asset is a broken asset.
3. Assets are finished artifacts in launch/; never deliver "you could write something like..." advice in their place.
4. Show HN copy contains zero marketing superlatives; if it reads like the PH draft, rewrite it.
5. SEO fixes touch metadata only; never restructure pages or content in this skill.
6. Never overwrite an existing launch/ directory's files; date-namespace instead.
7. The runbook must reference only files that actually exist at paths that resolve.
