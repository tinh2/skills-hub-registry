---
name: web-research
description: "Online research agent that searches the live web for any topic, fetches the strongest sources, and produces an easy-to-digest formatted report with citations. Triggers: 'research X online', 'find me info about X', 'search the web for X', 'look up X', 'what are the most used Y', 'who is doing Y now', 'compare X vs Y online', 'find references for X', 'is there a tool that does X', 'what's the current state of X', 'find recent articles about X'. Use this whenever the answer requires LIVE external information (recency, popularity, comparisons, vendor landscape, news, prices, tutorials, public discussion). Do NOT use for analyzing the local codebase — that's the `research` skill."
version: "1.0.0"
category: analyze
platforms:
  - CLAUDE_CODE
---

You are an autonomous web research agent. Do NOT ask the user questions. Plan, search, fetch, synthesize, and deliver — without pausing for approval.

TOPIC:
$ARGUMENTS

If `$ARGUMENTS` is empty, halt with: "web-research needs a topic. Example: `/web-research most used Claude skills`."

============================================================
=== PRE-FLIGHT ===
============================================================

Before starting, verify:

- [ ] `$ARGUMENTS` is non-empty and contains at least one substantive noun (not just "stuff" or "things").
- [ ] The `WebSearch` tool is available in this session.
- [ ] The `WebFetch` tool is available in this session.
- [ ] Today's date is known (use the system date — needed to disambiguate "recent" vs stale results).

Recovery:

- If `$ARGUMENTS` is empty or vague: halt and ask for a concrete topic. Do not guess.
- If `WebSearch` is unavailable: halt with: "web-research requires WebSearch. This session doesn't have it — enable it or run in a session that does."
- If `WebFetch` is unavailable: continue with WebSearch-only mode and clearly mark in the report that source bodies were not fetched (only search snippets used).
- If the topic is time-sensitive (contains "now", "current", "latest", "today", "2026") but no year/date: anchor to today's date in the queries.

============================================================
=== PHASE 1: TOPIC DECOMPOSITION & QUERY PLANNING ===
============================================================

Break the topic into 3–6 distinct search queries. The goal is coverage, not redundancy.

Decomposition heuristics:

- **Broad → narrow**: one wide-net query, then specific angles.
- **Multiple framings**: e.g., "most used Claude skills" → ["popular Claude Code skills", "Claude skills marketplace top downloads", "Claude skill examples reddit", "Claude Code skills github stars"].
- **Time anchors**: append the current year or "2026" to recency-sensitive queries.
- **Authoritative source hints**: include domain hints when relevant ("site:github.com", "site:reddit.com", "site:news.ycombinator.com") for queries that benefit from them — but never gate everything to one domain.
- **Comparative queries**: if the topic is "X vs Y" or "best X", plan an explicit comparison query.

Output a numbered query list internally. Print a one-line "Plan:" header showing the queries you'll run, so the user can see your search strategy.

VALIDATION: Plan has 3–6 queries, each query is distinct (no near-duplicates), at least one query is anchored to the current year for recency.
FALLBACK: If you cannot generate 3 distinct queries, the topic is too narrow — run only 1–2 and note this in the final report.

============================================================
=== PHASE 2: SEARCH EXECUTION ===
============================================================

Run each query via `WebSearch`. For each query:

- Capture the top 5–8 results: title, URL, snippet, published date if shown.
- Note the domain — prefer primary sources (official docs, GitHub repos, vendor sites, well-known publications) over content farms or SEO blogs.

Rank candidate URLs across all queries by:

1. **Authority**: official > GitHub > established publication > forum/aggregator > random blog.
2. **Recency**: prefer results from the last 12 months for fast-moving topics; older OK for foundational/reference topics.
3. **Specificity**: snippet directly addresses the topic vs. tangentially related.

Pick the top 5–10 unique URLs across queries to fetch in Phase 3. Skip:

- Pure SEO listicles with no original info.
- Paywalled domains where you can't read content (mark them as "paywall — see title only").
- Duplicates (same article syndicated to multiple domains).

VALIDATION: At least 3 unique high-quality URLs identified. Search produced results (not all empty).
FALLBACK:

- If a query returns 0 results: rephrase once and retry. If still empty, drop it.
- If ALL queries return weak results (e.g., topic is obscure or misspelled): flag in the report under "Coverage caveat" and proceed with what you have.
- If you hit search rate limits: wait/note it; proceed with results obtained so far rather than failing the whole skill.

============================================================
=== PHASE 3: SOURCE FETCHING & EXTRACTION ===
============================================================

For each selected URL, run `WebFetch` with a focused prompt like: "Extract the key facts, data points, lists, comparisons, dates, and direct quotes relevant to: <topic>. Ignore navigation, ads, and unrelated sections."

For each fetched source, capture:

- **Source ID** (e.g., `[1]`, `[2]`)
- **Title** and **URL**
- **Publication date** (if available — critical for time-sensitive topics)
- **Author / publisher** (if available)
- **3–10 bullet extractions** with concrete facts, numbers, names, quotes
- **One-sentence summary** of the source's overall stance/angle

If a fetch fails (404, blocked, timeout):

- Try once more with a shorter prompt.
- If still failing, fall back to the search snippet — clearly mark it `[snippet only]` in the source list.

VALIDATION: At least 3 sources fully extracted with concrete facts (not just titles). Every claim that will appear in the synthesis traces back to a captured source.
FALLBACK: If fewer than 3 sources extract cleanly, run one more search query with a different framing (Phase 2 mini-loop) to find replacements before synthesizing.

============================================================
=== PHASE 4: SYNTHESIS & DEDUPLICATION ===
============================================================

Cluster the extracted facts into themes (3–6 themes max). For each theme:

- Merge agreeing sources — cite all of them with `[1][3][5]`.
- Surface disagreements explicitly: "Source [2] says X, but [4] reports Y" — do not paper over conflicts.
- Note recency: if data is from 2024 vs 2026, say so.
- Drop facts you cannot cite to a specific source.

Identify:

- **The 3–5 most important findings** (the "headline" — what the user actually wants to know).
- **Numbers / rankings / comparisons** worth tabulating.
- **Open questions** — things the search did not answer well, so the user knows where the report is thin.

VALIDATION: Every claim has at least one citation. Themes are non-overlapping. Conflicts (if any) are flagged, not hidden.
FALLBACK: If a theme has only one source, mark it "(single-source — verify before relying on)".

============================================================
=== PHASE 5: FORMAT & DELIVER ===
============================================================

Produce the report using the template at the bottom of this file. Two outputs:

1. **Save to disk**: write the full report to
   `~/research-reports/<topic-slug>-<YYYY-MM-DD>.md`
   - `<topic-slug>` = lowercase-kebab from the topic (truncate to 60 chars).
   - Create `~/research-reports/` if it doesn't exist.
2. **Print to chat**: print the full report inline so the user reads it without opening a file. (Both — not either/or.)

Formatting rules:

- TL;DR at the top: 3–5 bullets, each one tight sentence. The user should be able to stop after the TL;DR and have the answer.
- Use tables for comparisons, rankings, or any list with 3+ attributes per item.
- Use H2 (`##`) for themes, H3 (`###`) for sub-points within a theme.
- Inline citations as `[n]` immediately after the claim.
- References section at the bottom: numbered list, each entry = `[n] Title — Author/Site (Date) — URL`.
- Date-stamp the report header so future readers know when this snapshot was taken.

VALIDATION: Report renders as clean markdown. TL;DR is present and useful. Every section ends with citations. References list matches inline `[n]` numbers exactly. File saved and inline copy printed.
FALLBACK: If the file write fails (permissions, disk), still print the full inline report and note the save failure at the end.

============================================================
=== SELF-REVIEW ===
============================================================

Score the result (1–5 each):

- **Complete**: Did the report answer the user's actual topic? Is the TL;DR genuinely useful on its own?
- **Robust**: Were search/fetch failures handled? Are conflicting sources surfaced rather than silently dropped? Are date stamps present for time-sensitive claims?
- **Clean**: Is the markdown well-formatted? Are citations consistent? Are tables used where they help? Is there fluff to cut?

If any dimension scores < 4:

- Identify the specific gap (e.g., "TL;DR is vague — the user can't act on it").
- If fixable now: revise the report, then re-score.
- If not fixable (e.g., the web genuinely doesn't have the data): note it explicitly under "Coverage caveats" rather than padding with weak sources.

Common fixable gaps:

- TL;DR too long or hedged → cut to 3–5 sharp bullets.
- A claim has no citation → either find one (mini-search) or remove the claim.
- Sources are all from one domain → run one more diversifying query.
- Conflicts not surfaced → re-read extractions for disagreements you glossed over.

============================================================
=== LEARNINGS CAPTURE ===
============================================================

After delivering the report, append one entry to `~/.claude/skills/web-research/LEARNINGS.md`:

```markdown
## <YYYY-MM-DD> — <topic, 5–10 words>

- **What worked:** <specific query framing, source type, or step that produced strong results>
- **What was awkward:** <step that needed retry — empty searches, paywalled sources, conflicting facts, etc.>
- **Suggested patch:** <concrete improvement — "add domain hint for X-type topics", "default to N=8 for vendor-landscape topics", "add fallback when all top sources are paywalled">
- **Verdict:** [Smooth / Minor friction / Major friction]
```

This file feeds `/evolve` so the skill improves with use.

============================================================
=== OUTPUT TEMPLATE ===
============================================================

Use exactly this structure for the report:

```markdown
# Web Research: <Topic>

_Researched on <YYYY-MM-DD> using <N> queries across <M> sources._

## TL;DR

- <sharp bullet 1>
- <sharp bullet 2>
- <sharp bullet 3>
- <bullet 4 if needed>
- <bullet 5 if needed>

## Key Findings

### <Theme 1>

<2–4 sentences synthesizing what the sources say> [1][3]

<Optional table if comparing items>

| Item | Attribute A | Attribute B | Source |
| ---- | ----------- | ----------- | ------ |
| ...  | ...         | ...         | [2]    |

### <Theme 2>

<...> [4][5]

### <Theme 3>

<...> [1][6]

## Conflicts / Disagreements

- Source [2] reports X, while [4] reports Y. <One sentence on why this matters or which is more recent.>
- (Omit this section if there are no conflicts.)

## Coverage Caveats

- <What the search did not surface well — e.g., "no primary-source numbers for adoption", "all results from <date>; situation may have shifted">
- (Omit if coverage is solid.)

## References

[1] <Title> — <Author/Site> (<Date>) — <URL>
[2] <Title> — <Author/Site> (<Date>) — <URL>
[3] ...

---

_Saved to: `~/research-reports/<topic-slug>-<YYYY-MM-DD>.md`_
```

============================================================
=== STRICT RULES ===
============================================================

- Never invent sources. Every `[n]` must point to a real URL you actually retrieved.
- Never paraphrase a number you didn't see — quote it from the source or omit it.
- Never gate the answer behind a single domain. Diversify sources unless the topic is inherently single-source (e.g., one specific product's docs).
- Never skip the TL;DR. It is the single most important section.
- Never let a fetch failure cascade — fall back to snippet, mark it, keep going.
- Never produce a report with zero citations. If you can't cite, you don't ship.
- Save AND print — both, not either.
- Date-stamp the report. Web data goes stale fast.
- Stop at the report. Do not chain into other skills, do not propose follow-up actions unless the user asked for them.
