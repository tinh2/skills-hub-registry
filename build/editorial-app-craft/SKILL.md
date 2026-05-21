---
name: editorial-app-craft
description: |
  Build a considered, cozy, editorial single-file web app (Firebase backend optional).
  Use when the user asks for a personal/family/couple/journaling/cozy app: "build a family board",
  "shared list app for me and my partner", "create a household app", "single-file Firebase app",
  "warm cream sage design", "Playfair editorial UI", "apply Field Notes aesthetic", "cozy productivity",
  "small considered web app". NOT for marketing landing pages, dashboards, or generic SaaS.
  Bundles a tuned design token system (sage + cream + terracotta + honey), Playfair Display + Source Sans 3
  typography, multi-layer paper shadows, Apple-style easing, and a set of considered detail patterns:
  daily rotating ornament + palette + quote, time-of-day greeting, editorial cards with byline metadata,
  Field Notes detail modal with italic serif numerals, day-varying empty states, toast personality variants,
  page-load orchestration, streak milestone ornaments, iOS-aware voice input, mobile touch targets.
version: "1.0.0"
category: build
platforms: [CLAUDE_CODE]
---

# editorial-app-craft

You build a single-file HTML web app with a cozy editorial aesthetic — sage + cream + terracotta,
Playfair Display + Source Sans 3, with a curated set of "considered detail" patterns layered in.
Optional Firebase backend (Auth + Firestore + Hosting + custom domain).

This is for **personal / family / cozy / journaling / shared-with-loved-ones** apps. It is NOT
for marketing pages, dashboards, or generic SaaS. The aesthetic is "Field Notes meets a quiet
weekend morning at home."

============================================================
=== PRE-FLIGHT ===
============================================================

Before starting, verify:

- [ ] User has described the kind of app they want, OR is iterating on an existing one.
- [ ] The app is small/personal/family-scale (not a marketing site or dashboard).
- [ ] If Firebase backend is requested: `firebase --version` works and the user has run `firebase login`.
- [ ] If a custom domain is requested: confirm DNS provider (Route 53? Cloudflare? GoDaddy?).

If any check fails:

- Aesthetic mismatch (marketing landing page, dashboard, etc.) → say so and decline. This skill
  has strong opinions; using it on the wrong target produces strange output.
- Firebase CLI not installed → `brew install firebase-cli` or skip the deploy phase entirely
  and produce a static single-file app instead.
- DNS unclear → produce the app and stop before custom-domain wiring; tell user to come back
  once they know.

============================================================
=== PHASE 1: UNDERSTAND THE APP ===
============================================================

Ask (in ONE message, then proceed):

1. What is the app for, in one sentence?
2. Who's it for? (just you, you + partner, family of N, etc.)
3. What are the 2–4 main "things" the app needs to hold? (tasks, lists, notes, photos, journal entries...)
4. Does it need to sync across devices / multiple users? (yes → Firebase; no → localStorage only)

If the user already gave enough signal in their prompt, skip the questions and proceed.

VALIDATION: You can describe the app in one paragraph and name its core data model.
FALLBACK: If still unclear, propose a small default and let the user redirect.

============================================================
=== PHASE 2: SCAFFOLD ===
============================================================

Create the project at `~/git/<app-name>/`:

```
~/git/<app-name>/
├── index.html              # single-file app
├── icon.svg                # favicon SVG (small fleuron in brand gradient)
├── apple-touch-icon.png    # 180×180 PNG (render via Playwright screenshot of icon.svg)
├── firebase.json           # if Firebase
├── firestore.rules         # if Firestore
└── .firebaserc             # if Firebase
```

The `index.html` skeleton has these sections in this order:

1. `<head>` with theme-color meta, favicon link, apple-touch-icon link, Google Fonts (Playfair
   Display + Source Sans 3), inline `<style>`.
2. The full design tokens block from `assets/design-tokens.css`.
3. The component patterns block from `assets/patterns.css`.
4. `<body>` with: welcome-modal, family-setup-modal (if multi-user), app shell, content modals.
5. `<script type="module">` with Firebase imports (if needed), state, render, the detail-patterns
   functions from `assets/detail-patterns.js`.

VALIDATION: index.html opens directly in a browser without a server and renders the empty welcome
modal with daily ornament + time-of-day greeting.
FALLBACK: If something blocks rendering, fix it before adding features.

============================================================
=== PHASE 3: APPLY DETAIL PATTERNS ===
============================================================

Layer these in. Each is described in `assets/detail-patterns.js`:

| Pattern                        | Where it goes                                                                                                                                      |
| ------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Daily rotating ornament**    | Brand mark (top-left) + welcome-modal mark. Call `applyDailyOrnament()` on boot + `setInterval(60_000)`.                                           |
| **Time-of-day greeting**       | Italic Playfair line above the welcome-modal headline.                                                                                             |
| **Daily quote**                | Below the sign-in button or somewhere persistent the user sees on each visit (footer ribbon, settings panel).                                      |
| **Editorial cards**            | Title in Playfair italic, metadata as inline byline with `·` separators, no pill backgrounds. Sage rail on hover, terracotta rail on "meaningful". |
| **Field Notes detail modal**   | Italic serif numerals 01/02/03 for sub-items, hairline dividers, memo-line input.                                                                  |
| **Day-varying empty states**   | Pull a line from `EMPTY_STATES[zoneKey]` by `dayIndex()`.                                                                                          |
| **Toast personality variants** | Use `celebrationLine({...})` instead of generic "+1 pt for X".                                                                                     |
| **Page-load orchestration**    | Add `.first-paint` class to the board on first render, strip after 900ms.                                                                          |
| **Streak milestones**          | If the app has any streak/count, use `streakOrnament(n)` and `isStreakMilestone(n)`.                                                               |
| **iOS-aware voice**            | Use `setupVoiceInput({...})` — auto-hides the mic on iOS WebKit.                                                                                   |
| **Mobile touch targets**       | Wrap icon-button styles in `@media (hover: none) { min-width: 40px; min-height: 40px; }`.                                                          |

For each pattern: write it, then verify it renders + works.

VALIDATION: Open the running app at 1400px AND 390px. Check that the editorial details actually
show. Touch targets must be ≥40px on mobile.
FALLBACK: If a pattern doesn't fit the app's data model (e.g., no "meaningful" concept), skip
it rather than forcing it.

============================================================
=== PHASE 4: FIREBASE WIRING (optional) ===
============================================================

If the user wants sync, follow `assets/firebase-deploy.md`:

1. `firebase projects:create` + register a Web app + grab SDK config
2. Enable Firestore + Identity Toolkit APIs (refresh CLI token if needed)
3. Create Firestore database
4. User enables Google sign-in via Console (one click — unavoidable)
5. Write `firebase.json`, `firestore.rules`, `.firebaserc`
6. `firebase deploy --only hosting,firestore:rules`

VALIDATION: Live URL works, sign-in flow completes, a test write to Firestore succeeds.
FALLBACK: If any step blocks, write a static localStorage-only version first and ship that.
Firebase can be added later without disturbing the UI.

============================================================
=== PHASE 5: CUSTOM DOMAIN (optional) ===
============================================================

Only proceed if user confirmed DNS provider in pre-flight.

1. Call `customDomains` API to register the subdomain
2. Read `requiredDnsUpdates.desired` — extract CNAME + TXT records
3. If user authorized AWS access: write Route 53 records via `aws route53` CLI
4. Otherwise: print the exact records and instruct user to paste at their registrar
5. Poll cert status until `HOST_ACTIVE` + `CERT_ACTIVE`
6. Add the new hostname to Auth's `authorizedDomains` list

VALIDATION: `https://<custom.domain>` loads with a green padlock.
FALLBACK: If cert provisioning takes >40 min, hand off to the user with a watch command and
the current status; don't block.

============================================================
=== SELF-REVIEW ===
============================================================

Score the output (1–5):

- **Complete**: All requested core features built and live?
- **Detail-rich**: Did you layer in at least 6 of the 11 detail patterns from Phase 3?
- **Brand-faithful**: Sage + cream + terracotta palette intact? Playfair + Source Sans? Multi-layer
  shadows? No purple gradients / emoji icons / pill-cluster cards?
- **Mobile-honest**: Verified at 360px or 390px? Touch targets ≥40px? Mic hidden on iOS?
- **Cozy, not clinical**: Empty states warm, copy human, italic Playfair used where it earns?

If any score < 4:

- Identify the specific gap and fix it.
- If unfixable in this run, note it explicitly as a known limitation in the final message.

============================================================
=== LEARNINGS CAPTURE ===
============================================================

After completing, append one entry to `~/.claude/skills/editorial-app-craft/LEARNINGS.md`:

```markdown
## <YYYY-MM-DD> — <app name + key decisions>

- **What worked:** <pattern that landed especially well, or a setup step that was smooth>
- **What was awkward:** <step that needed retries — Firebase auth provider, iOS Safari quirk, DNS, etc.>
- **Suggested patch:** <one concrete improvement — e.g., "default to Route 53 path detection",
  "add explicit step for custom-domain authorizedDomains", "include a default 30-quote list">
- **Verdict:** [Smooth / Minor friction / Major friction]
```

---

## Anti-patterns this skill refuses

- Purple gradients of any kind
- Pill clusters on cards (use editorial byline with dot separators instead)
- "B" letter on the brand mark (use the daily fleuron)
- Em-dashes in user-facing copy (commas / colons / sentence breaks instead)
- Emoji as decorative icons (only as content-bearing characters: ❤ for meaningful, 🔥/✦/🏆 for streak tiers)
- Cards with left-color-border + flat shadow (the 2020–2024 Material/Tailwind look)
- Inter/Roboto/system fonts as display (always Playfair Display for headings)
- "Add family members and kids" → say "Add family members". The app doesn't draw an adult/child line.
