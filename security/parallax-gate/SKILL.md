---
name: parallax-gate
description: "Legal and ethics gate for building your own product inspired by an existing app. Writes a signed-off gate record: allowed sources, the target's ToS and robots.txt findings, the clean-room rules, and hard stops (no auth, paywall or DRM bypass, no copied code, copy, assets, trademarks or logos). Every other Parallax skill refuses to run until it passes. Not legal advice. Triggers: 'can I clone this app', 'is it legal to copy X', 'clean room rules', 'before we reverse engineer X', 'parallax gate', or the first step of any Parallax study."
version: "1.0.0"
category: security
platforms:
  - CLAUDE_CODE
tags: [clean-room, legal, ethics, reverse-engineering, ip, parallax]
---

# Parallax Gate

Parallax is a pack for studying an existing product's behavior and building an
original product that does the job better. This skill runs first. It writes
`parallax/gate.md`, and every other Parallax skill reads it and stops if it is
missing, failed, or older than the target's current terms.

This is a practical checklist, not legal advice. When a finding is unclear,
say so and tell the user to ask a lawyer before going further.

## The pack

| step | skill | writes |
| --- | --- | --- |
| 0 | parallax-gate | `parallax/gate.md` |
| 1 | parallax-study | `parallax/evidence/`, `evidence.md`, `unknowns.md`, `study.md` |
| 2 | parallax-pain | `parallax/pain.md` |
| 3 | parallax-spec | `parallax/obligations.csv`, `spec.md` |
| 4 | (build, your normal workflow) | your code, tracked against obligations |
| 5 | parallax-verify | `parallax/verify.md` |
| 6 | parallax-ship | `parallax/ship.md` |

## Step 1: identify the target and the user's standing

Ask, or propose and confirm:

1. Target product, platform(s), and the slice being studied (one core loop, not
   "all of it").
2. Does the user have their own legitimate account? Free or paid? Personal or
   employer-provided?
3. Is the user an employee, contractor or former employee of the target, or
   bound by an NDA with it? If yes: STOP and tell them to get legal advice.
   Confidential knowledge cannot enter a clean room.

## Step 2: read the rules the target published

Fetch and read (as a person would, one page at a time):

- Terms of service / EULA. Search it for: "reverse engineer", "decompile",
  "disassemble", "competing product", "benchmark", "scrape", "automated",
  "robot", "crawl". Quote each hit verbatim with its URL and section.
- `robots.txt` on every domain you plan to read. Record disallowed paths.
- API terms, if a public API exists.

Classify each technique below as **allowed**, **restricted** (allowed only on
public pages, not with the account) or **forbidden**:

| technique | default | downgrade when |
| --- | --- | --- |
| reading public pages, docs, help center, pricing, changelog | allowed | robots.txt disallows the path |
| using the user's own account by hand | allowed | ToS bans using accounts to build competing products |
| automated browser capture of the user's own session (REA `capture_browser_scenario`) at human pace | allowed | ToS bans automation or bots |
| reading network traffic of the user's own session (HAR / REA `inspect_web_network_capture`) | allowed | ToS bans reverse engineering or automation |
| static analysis of publicly served JS bundles (REA `analyze_web_bundle`) to learn routes and behavior | restricted | ToS bans reverse engineering; then forbidden |
| inspecting a desktop or mobile package the user lawfully installed | restricted | EULA bans reverse engineering, unless the user's jurisdiction grants an interoperability exception and a lawyer confirms |
| bulk crawling, scraping review sites, loops over pages | forbidden | never allowed |

When in doubt, choose the stricter row. A forbidden technique is not used, and
the gap it leaves goes in the unknowns ledger instead.

## Step 3: the hard stops (never negotiable)

Write these into `gate.md` verbatim. Any Parallax skill that is about to cross
one stops and tells the user.

1. **Only public information and the user's own account.** Never use someone
   else's credentials, shared logins, leaked data, or insider information.
2. **No circumvention.** Never bypass authentication, paywalls, rate limits,
   licence checks, DRM, certificate pinning, obfuscation-as-protection, or
   anti-bot measures. Never replay, forge or tamper with tokens.
3. **No copying of expression.** No source code (minified or recovered), HTML,
   CSS, SVG, images, icons, fonts, sounds, UI copy, help text, email text,
   sample data, trademarks, logos, product names or distinctive trade dress.
4. **Clean-room separation.** Evidence describes *behavior* (what happens, what
   shape data has, which states exist). Specs are written in your own words
   from evidence. Code is written from specs only, never with a recovered
   source file, bundle excerpt or screenshot open as a template.
5. **No private APIs in the product.** Your product never calls the target's
   undocumented endpoints. Observed API shapes inform your own design only.
6. **Privacy.** Captures from the user's session contain their personal data.
   Redact tokens, cookies, emails, names and IDs before anything is saved
   under `parallax/evidence/`, and never commit raw captures.
7. **No fake reviews or impersonation**, ever.

## Step 4: write the gate record

`parallax/gate.md`:

```
# Parallax gate: <target> / <slice>
date: <YYYY-MM-DD>   status: PASS | PASS-RESTRICTED | FAIL
terms reviewed: <URL> (retrieved <date>), robots.txt: <URLs>
user standing: own account <yes/no, plan>, insider/NDA <no>
## ToS findings (verbatim, with section)
## Technique table (allowed / restricted / forbidden, with reason)
## Hard stops (copied from parallax-gate)
## Open legal questions (for a lawyer)
```

Status rules: FAIL if the user is an insider, if the only route to the slice
requires a forbidden technique, or if the goal is a counterfeit (same name,
logo or look, meant to be mistaken for the original). PASS-RESTRICTED when
some techniques are downgraded. Show the user the record and get a yes.

Add `parallax/evidence/raw/` to `.gitignore` now.

## Re-checks

Re-run this gate when the target's terms change, before launch (parallax-ship
does it), and whenever a skill wants a technique the table does not allow.

## Credit

Parallax was inspired by the Replica skill pack by Jake Schincariol
(github.com/Jakeschincariol/replica-skill, MIT). Parallax is an independent
rewrite with an evidence-first design; no Replica text is reused.
