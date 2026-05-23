---
name: seo-audit-2026
description: Comprehensive 2026 SEO audit covering classic technical SEO (crawl, render, index, Core Web Vitals with INP), on-page (titles, meta, headings, internal linking), content (topical authority, entity density), and the new mandatory layer — Generative Engine Optimization (GEO/AEO) for ChatGPT, Perplexity, Claude, Gemini, and Google AI Overviews. Produces a single prioritized report with P0–P3 items, fix code snippets, and a re-audit checklist. Replaces the older "SEO checklist" workflow — modern audits MUST cover AI crawler parity, llms.txt, schema depth, entity density, and E-E-A-T author entity, OR they'll grade well on Google and badly on the engines that drive 30%+ of zero-click answers in 2026. TRIGGER on "SEO audit", "site SEO check", "Core Web Vitals", "INP", "ranking issues", "crawl issues", "Google not indexing", "AI Overviews", "Lighthouse SEO", "site:visibility report", or any general "fix my SEO" prompt.
version: "2.0.0"
category: analysis
platforms:
  - CLAUDE_CODE
---

# SEO Audit 2026

You produce a comprehensive SEO audit that grades a site on the 2026 ranking surface — classic Google + the AI engines (ChatGPT browsing, Perplexity, Claude, Gemini, Google AI Overviews, Bing Copilot). Output is a single prioritized report, not a 200-item checklist dump.

The reality of 2026 SEO:

- **AI Overviews handle 30%+ of informational queries** with zero-click answers.
- **96% of AI Overview citations** come from strong-E-E-A-T sources.
- **Core Web Vitals INP < 200ms** replaced FID as a ranking signal.
- **Server-side rendering is non-negotiable** — AI crawlers don't execute JS.
- **Entity density predicts citations more than keyword density.**

============================================================
=== PRE-FLIGHT ===
============================================================

Verify:

- [ ] **Site URL** (root domain).
- [ ] **Access level** — what you can actually fix vs only audit. If no CMS access, output read-only audit + remediation steps.
- [ ] **Tools available** — `curl`, `playwright`/`puppeteer` for render diffs, Lighthouse CLI for CWV, `jq` for JSON parsing. Install missing tooling or fall back to web-based equivalents.
- [ ] **Target queries / pages** — 5-10 priority queries OR top pages from Search Console.
- [ ] **Crawl budget consent** — full audit may crawl up to 1000 pages. Respect robots.txt; obey rate limits (default 1 req/sec).

Recovery:

- If user doesn't have target queries, derive from `<title>` tags of top nav + top 10 referrer pages.
- If full crawl is impossible (auth-walled site), audit the public surface + provide a sitemap-based audit for internal pages.

============================================================
=== PHASE 1: CRAWL & INDEX AUDIT ===
============================================================

Most ranking issues in 2026 trace back to crawl/index — audit before optimizing content.

Check:

1. **robots.txt parity** — fetch as Googlebot, GPTBot, PerplexityBot, ClaudeBot. Identical access? Flag any bot-specific blocks.
2. **Sitemap correctness** — fetch `/sitemap.xml`. Verify each listed URL returns 200, has lastmod, isn't noindex.
3. **Canonical chain** — for each page, follow `rel=canonical`. Catch self-canonical errors, redirect chains, conflicting hreflang.
4. **Indexability** — `<meta name="robots">`, `X-Robots-Tag` headers. Spot pages set to noindex unintentionally.
5. **HTTP status distribution** — count 200/301/302/404/410/500. Excessive 302→301 chains hurt; soft-404s (200 status with empty content) are the silent killer.
6. **Pagination & faceted nav** — are search/filter URLs canonicalized to parent OR noindexed?

Generate `seo/crawl_report.md` with the index status of every important URL.

VALIDATION: Every URL in the report has a definitive status (Indexable / Blocked / Redirected / Error). No "unknown" rows.

FALLBACK: If crawl is rate-limited mid-run, persist partial results and resume later.

============================================================
=== PHASE 2: AI CRAWLER PARITY ===
============================================================

(See `geo-optimize` Phase 1 for full detail.)

Run the user-agent matrix test. Diff rendered (Playwright) vs static (curl as GPTBot, PerplexityBot, OAI-SearchBot, ClaudeBot, Claude-Web, Google-Extended, Applebot-Extended).

P0 if any AI bot sees < 50% of the rendered text or schema is missing in static HTML.

VALIDATION: Parity report contains a row per page × per bot with content diff %.

============================================================
=== PHASE 3: CORE WEB VITALS (2026 THRESHOLDS) ===
============================================================

Run Lighthouse CI for each priority URL on **both mobile and desktop**. Capture:

- **LCP** (Largest Contentful Paint): < 2.5s (good), 2.5–4.0s (needs improvement), > 4.0s (poor)
- **INP** (Interaction to Next Paint): < 200ms (good), 200–500ms (needs improvement), > 500ms (poor) — REPLACED FID in March 2024
- **CLS** (Cumulative Layout Shift): < 0.1 (good), 0.1–0.25 (needs improvement), > 0.25 (poor)
- **TTFB** (Time to First Byte): < 0.8s (good)
- **Total Blocking Time** (lab proxy for INP)

For each fail, generate a specific fix:

- LCP fail: preload hero image, eliminate render-blocking CSS/JS, use modern image formats (AVIF/WebP), CDN for hero.
- INP fail: split long tasks, defer non-critical JS, debounce input handlers, use `requestIdleCallback`.
- CLS fail: explicit width/height on images, reserve space for ads, avoid font-swap layout jump (use `font-display: optional` or `size-adjust`).

VALIDATION: Each fail has a concrete code-level fix, not "improve performance."

============================================================
=== PHASE 4: ON-PAGE AUDIT ===
============================================================

Per priority URL, check:

- **Title tag**: 30–60 chars, unique site-wide, includes target query naturally (not stuffed), brand at end.
- **Meta description**: 120–160 chars, action-oriented, includes primary entity. Note: AI Overviews often pull from H1+first paragraph, not meta — but meta still drives SERP CTR for classic search.
- **H1**: exactly one per page, contains primary entity.
- **Heading hierarchy**: H1 → H2 → H3 (no skipping levels). Each H2 is a question or noun phrase that maps to a search intent.
- **Image alt text**: every content image has descriptive alt (not "image1.jpg" or empty).
- **Internal linking**: each priority page has ≥ 3 inbound internal links from contextually related pages. Anchor text varied (not all "click here").
- **Outbound citations**: at least 2 outbound links to authoritative third-party sources (E-E-A-T signal — AI engines mirror your citation behavior).
- **First paragraph**: states the answer to the page's primary query in plain language within the first 80 words. AI engines extract this as the citation snippet.

Generate `seo/onpage_report.md` per-URL.

VALIDATION: Report flags specific elements, not just "needs work."

============================================================
=== PHASE 5: SCHEMA & ENTITY AUDIT ===
============================================================

(Delegated to `geo-optimize` Phases 3 + 4.)

For each priority page, audit JSON-LD coverage and entity density. Generate missing schema. Recommend entity additions to hit ≥ 15 recognized entities per pillar page.

VALIDATION: Per-page entity count and schema validation status.

============================================================
=== PHASE 6: CONTENT QUALITY & E-E-A-T ===
============================================================

Per priority page:

- **Author byline** present and linked to `/author/{slug}`?
- **Author Person page** exists with bio + `sameAs` to LinkedIn / Wikidata / X / Crunchbase?
- **Last-updated date** visible in DOM and in Article schema `dateModified`?
- **Original content markers** — original screenshots / data / interviews / first-hand experience? (Not just rewritten generic content.)
- **Citations within body** to primary sources?
- **HTTPS, no mixed content, valid SSL cert**?
- **About / Contact / Privacy pages** present and linked from footer? (Trust signal.)

Generate `seo/eeat_report.md` with per-page and per-author scores.

VALIDATION: Each author has either a complete Person profile (5+ checkboxes pass) or a clear remediation list.

============================================================
=== PHASE 7: COMPETITIVE GAP ===
============================================================

For each priority query:

1. SERP scrape top 10 organic + top 5 AI Overview citations (note: those overlap ~70%).
2. Extract competitor entities, headings, schema types, word count.
3. Diff vs the user's page: entities they cite that you don't, headings they cover that you don't, schema types they have that you don't.
4. Output as a per-query gap matrix.

VALIDATION: Per-query gap report identifies at least 3 concrete additions (entities or sections) to add.

FALLBACK: If SERP scraping is rate-limited, fall back to manual top-3 analysis via the user's browser (instruct them, don't claim full coverage).

============================================================
=== PHASE 8: PRIORITIZED PUNCH LIST ===
============================================================

Single output `seo/audit_report.md` ranking findings:

```markdown
# SEO Audit — {site} — {date}

## Executive Summary

- Indexability: {green/yellow/red} ({N} pages indexable / {M} blocked)
- AI Crawler Parity: {green/yellow/red} ({N} priority pages pass)
- Core Web Vitals: {N/M priority pages passing all 3}
- Schema Coverage: {N%} of priority pages have complete schema
- Entity Density: {N/M priority pages ≥15 entities}
- E-E-A-T: {N/M pages have linked author Person entity}

## P0 — Blocking Issues

- [ ] Site renders client-side, GPTBot sees empty HTML. Move /blog/\* to SSR via Next.js getServerSideProps OR pre-render via next-build.
- [ ] Missing Organization schema on homepage. (Generate JSON-LD — see fix snippet below.)

## P1 — High-Impact Fixes

- [ ] 6 of 10 priority pages fail INP > 500ms. Defer analytics.js and reduce main-thread blocking in checkout.js.
- [ ] 4 of 10 priority pages have < 15 entities. Add brand + product entity mentions per page (specifics in entity_audit.md).

## P2 — Medium-Impact

- [ ] No llms.txt at root.
- [ ] FAQPage schema missing on 3 pages with FAQ sections.

## P3 — Polish

- [ ] 14 images missing alt text in /blog/\*.

## Re-audit Checklist

After fixes, re-run with `/seo-audit-2026 {site}` and verify P0/P1 items move to ✅.
```

VALIDATION: Punch list ranked by impact, capped at top 20 items. Each P0/P1 includes a code-level fix or precise file path.

============================================================
=== SELF-REVIEW ===
============================================================

Score 1–5:

- **Complete**: All 8 phases ran? AI crawler parity tested? CWV measured on both mobile + desktop?
- **Robust**: Handled CSR sites, paywalled sites, rate limits, missing tools?
- **Clean**: Punch list is prioritized, not a 200-item dump?
- **2026-current**: References INP (not FID), AI Overview citations, llms.txt, entity density, E-E-A-T binary gating? Doesn't recommend obsolete tactics (keyword density tuning, exact-match anchors at scale, doorway pages)?

Most common gap: failing to test AI crawler parity AND not measuring INP. These are the two table-stakes items that catch teams still running 2023-era audits.

============================================================
=== LEARNINGS CAPTURE ===
============================================================

Append to `~/.claude/skills/seo-audit-2026/LEARNINGS.md`:

## <YYYY-MM-DD> — <site, vertical, framework>

- **What worked:** <approach that produced clean output>
- **What was awkward:** <retry/manual fix needed>
- **Suggested patch:** <concrete improvement>
- **Verdict:** [Smooth / Minor friction / Major friction]

============================================================
=== STRICT RULES ===
============================================================

- Never use FID. It was retired March 2024. Use INP.
- Never recommend keyword density tuning. Entity density and topical authority are the modern signals.
- Never dump a 200-item checklist. Prioritize.
- Never claim "SEO complete" without AI crawler parity + schema validation + entity audit.
- Never overlook E-E-A-T author entity. 96% of AI citations come from strong-EEAT sources — it's a gate, not a polish.
- If the user only wants the AI search portion, route to `/geo-optimize` instead of running the full classic audit.
