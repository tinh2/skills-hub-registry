---
name: parallax-pain
description: "Finds why users of an existing product would switch: reads public reviews, forums and feature-request boards by hand or via official feeds, records each complaint verbatim with its link, clusters them into ranked pain themes, and turns the top themes into differentiation obligations for your own product. Never invents quotes or counts. Triggers: 'what do users hate about X', 'read X's reviews', 'find the gap', 'how do I make mine better', 'positioning against X', 'parallax pain'."
version: "1.0.0"
category: analyze
platforms:
  - CLAUDE_CODE
tags: [user-research, reviews, positioning, differentiation, parallax]
---

# Parallax Pain

A behavioral copy has no reason to exist. This skill finds the reason, in the
users' own words, and makes it a requirement rather than a slogan.

Requires `parallax/gate.md` (PASS*). Reads `parallax/study.md` if present.

## Rules

- **Nothing invented.** Every quote verbatim, every row with a URL and date.
  If a source is unreachable, say so. Report the real counts, even if small.
- **Read, don't scrape.** One page at a time, as a person would. Official
  feeds and APIs within their terms are fine (for example Apple's public
  customer-reviews RSS feed, the Hacker News Algolia search API, Reddit's
  official API). No scraping libraries against sites that forbid it.
- **Research, not marketing.** Reviewers' words never appear on your site, and
  no fake reviews for anyone, ever.
- Do not store reviewers' usernames beyond what the link already shows.

## Step 1: collect

Target at least 60 items across 3+ source types, newest first, including 3-4
star reviews ("love it, but..."): app stores, G2/Capterra/Trustpilot, Reddit
and HN threads ("X alternative", "switched from X", "X vs"), the target's
public roadmap or request board with vote counts, and its changelog (so you do
not "fix" what shipped last month).

`parallax/pain/reviews.csv`: `id,source,url,date,rating,quote`.

## Step 2: cluster and rank

Group into themes (pricing, performance, missing feature, reliability, support,
lock-in, UX, privacy...). Score each theme:

`score = count x recency weight (last 12 months 1.0, older 0.5) x severity (1-3 star 1.5, else 1.0)`,
and mark **thin** when it has < 3 items or a single source. Show the
arithmetic in the table. Read the unclustered low ratings by hand.

## Step 3: cross-check against evidence

For each top theme, check `study.md`: is the complaint consistent with what
was observed? Cite the E-id, or open a U-id ("does the export really drop
attachments? probe: capture export on own account"). Complaints about things
the study cannot see stay labelled "reported, unverified".

## Step 4: three lists and an angle

In `parallax/pain.md`:

1. **Fix**: things users hate that you will do better (theme, score, sources,
   1-2 linked quotes, the concrete behavior you will ship instead).
2. **Add**: requested and still missing.
3. **Skip**: what users do not value, so you can leave it out.
4. **Angle**: one sentence for who switches and why, built from list 1 only.

Each Fix/Add item gets a proposed obligation `P01..` with a testable
acceptance criterion ("import a 10k-row CSV in under 5 s"), which
parallax-spec turns into ledger rows of kind `differentiator`.

Credit: inspired by replica-entrepreneur in the Replica pack by Jake
Schincariol (MIT). Independent text.
