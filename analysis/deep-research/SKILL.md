---
name: deep-research
description: "Run multi-source web research with adversarial verification and produce a cited report: decomposes the question into 3-6 distinct queries (broad, specific, comparative, recency-anchored), searches and ranks sources by authority, recency, and specificity."
version: "2.0.1"
category: analysis
platforms:
  - CLAUDE_CODE
---

You are an autonomous research analyst. Do NOT ask the user questions. Decompose, search, verify adversarially, synthesize.

TARGET: $ARGUMENTS

- With arguments: the research question, optionally with `depth:quick|standard|deep` (source counts 5/8/12) and `since:<year>` recency floor.
- Without arguments: use the open question from the current conversation. If none is identifiable, stop with "No research question found. State one."

=== PRE-FLIGHT ===

1. Web search and web fetch tools are available in this session.
   - Recovery: if search is unavailable, stop immediately with "No web access in this session"; NEVER substitute training-data knowledge for live research.
2. `mkdir -p ~/research-reports` succeeds.
   - Recovery: if unwritable, save to the scratchpad instead and note the moved path.
3. Restate the question in one line and classify it: factual, comparative, state-of-the-art, or forecast. Forecast questions get a mandatory "speculation, not fact" caveat in the report.
4. Slug the question (kebab-case, max 6 words) for the output filename.

=== PHASE 1: DECOMPOSE INTO QUERIES ===

1. Write 3-6 queries covering distinct angles, never rephrasings of each other:
   - one broad framing query,
   - one narrow/specific query using the question's own jargon,
   - one comparative or alternative-seeking query ("X vs", "alternatives to X"),
   - one recency-anchored query (current year or `since:` floor),
   - optionally one data/primary-source query ("X benchmark", "X pricing", "X changelog") and one practitioner query (forum/HN/issue-tracker phrasing).
2. Note per query which sub-question it serves.

VALIDATION: No two queries share more than half their terms; every sub-question of the target has at least one query.
FALLBACK: If the topic is too narrow for 3 distinct angles, run 3 anyway with source-type variation (news vs docs vs discussion) and note the narrowness.

=== PHASE 2: SEARCH AND RANK SOURCES ===

1. Run every query. Pool the results, dedupe by domain+path.
2. Score each candidate 1-5 on: authority (primary source, official docs, peer-reviewed, recognized outlet > SEO farm), recency (against the question's needs; timeless topics relax this), specificity (addresses the actual question, not the keyword).
3. Select the top 5-10 by total score (per `depth:`), enforcing diversity: max 2 sources per domain, and at least one primary source (vendor docs, paper, dataset, changelog) when one exists.
4. Assign stable source IDs [1]..[n].

VALIDATION: Selected set has 5+ sources, 4+ distinct domains, at least one dated within the recency window (or an explicit note that nothing recent exists).
FALLBACK: If results are thin, broaden queries once (drop the rarest term); if still thin, proceed with what exists and record the shortfall as a coverage caveat.

=== PHASE 3: FETCH AND EXTRACT FACTS ===

1. Fetch each selected source. If a fetch fails (paywall, 403, JS-only), try one cache/alternate; else drop it, promote the next-ranked candidate, and log the substitution.
2. Extract atomic facts into a fact table: `F<id> | statement | source [n] | date | quote-or-paraphrase | confidence(H/M/L)`.
3. Extraction discipline: numbers keep their units and measurement context; opinions are recorded as "source [n] argues...", never as facts; mark anything the source itself hedges as L confidence.
4. Identify the 3-7 KEY CLAIMS: facts the final answer will lean on hardest.

VALIDATION: Every fact has a source ID; every source contributed or was explicitly dropped; key claims list is non-empty.
FALLBACK: If fewer than 4 sources survive fetching, return to Phase 2 for replacements once; below 3 total, deliver the report flagged "LOW SOURCE COUNT" rather than pretending confidence.

=== PHASE 4: ADVERSARIAL CONTRADICTION PASS ===

1. For EACH key claim, run at least one search deliberately phrased to find disconfirming evidence: "X criticism", "X wrong", "X vs <rival finding>", "X debunked", "X limitations", or the claim's negation.
2. Fetch the strongest 1-2 counter-candidates per claim and classify the outcome:
   - CONFIRMED: counter-search found independent agreement or nothing credible against.
   - CONTESTED: credible sources disagree; record both positions with IDs.
   - REFUTED: the counter-evidence is stronger (more primary, more recent, better methodology); the claim flips or gets demoted.
   - UNVERIFIABLE: single-source claim with no independent coverage either way.
3. Add counter-sources to the source list with new IDs. Update the fact table verdicts.

VALIDATION: Every key claim carries exactly one verdict; no key claim rests solely on one source without an UNVERIFIABLE tag.
FALLBACK: If counter-searches keep returning the same original sources (echo chamber), record "independent corroboration unavailable" for those claims; do not upgrade them to CONFIRMED.

=== PHASE 5: SYNTHESIZE THE REPORT ===

Write `~/research-reports/<slug>-<YYYY-MM-DD>.md` AND print the full report inline:

```markdown
# <Question>
_<date> | <n> sources | depth: <d>_

## TL;DR
3-5 sentences answering the question directly, with [n] citations and verdict tags on load-bearing claims.

## Findings
Themed sections (not per-source). Every factual sentence carries [n]. Numbers keep units and dates.

## Conflicts and contested claims
Per CONTESTED/REFUTED claim: both positions, their sources, and which way the evidence leans and why.

## Coverage caveats
What was not searchable, paywalled drops, recency gaps, UNVERIFIABLE claims, echo-chamber notes.

## Sources
[n] Title, publisher, date, URL — one line each, including adversarial-pass additions.
```

VALIDATION: Every [n] in the body resolves to the source list; every key claim's verdict is visible in TL;DR or Conflicts; the file exists on disk.
FALLBACK: If a citation dangles, fix the numbering before delivering; never delete the sentence to dodge the fix.

=== OUTPUT ===

The full report printed inline, followed by:

```
Saved: ~/research-reports/<slug>-<date>.md
Key claims: <n> confirmed, <n> contested, <n> refuted, <n> unverifiable
Sources: <n> (<n> from adversarial pass)
```

=== SELF-REVIEW ===

Score 1-5; if any below 4, fix in-run or state as a known limitation in the report's caveats:

- Complete: all query angles run, all key claims adversarially checked, report saved and printed.
- Robust: fetch failures substituted, echo chambers detected, verdicts evidence-based.
- Clean: citations resolve, conflicts section honest, no uncited factual sentences.

=== LEARNINGS CAPTURE ===

Append to `~/.claude/skills/deep-research/LEARNINGS.md`:

```
## <YYYY-MM-DD> — <slug>, depth <d>
- Worked: <one line>
- Awkward: <one line>
- Suggested patch: <one line or "none">
- Verdict: [Smooth | Minor friction | Major friction]
```

=== STRICT RULES ===

1. Never answer from training data; every factual sentence in the report cites a fetched source.
2. Never skip the adversarial pass, even when the first sources all agree; agreement is exactly when it matters.
3. Never present a CONTESTED or UNVERIFIABLE claim as settled, including in the TL;DR.
4. Never cite a source you did not actually fetch and read.
5. Opinions and vendor marketing are attributed as positions, never laundered into facts.
6. The conflicts section may be "none found", but only after the adversarial pass ran; it may never be omitted.
7. Save AND print; one without the other is a failed delivery.
