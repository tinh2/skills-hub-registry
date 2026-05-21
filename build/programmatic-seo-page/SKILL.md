---
name: programmatic-seo-page
description: "Generates production-ready programmatic SEO landing pages using the three winning 2026 templates ('Best X for Niche', '[Service] in [City]', '[A] vs [B] for [User Type]') with unique scraped data, Article + Product + FAQ schema, a viral artifact (custom score or grader), and editorial-review checklist. Avoids site-wide thin-content penalties. Use when scaling organic acquisition past 100 pages."
version: "1.0.0"
category: build
platforms:
  - CLAUDE_CODE
  - CURSOR
  - CODEX_CLI
---

You are a programmatic SEO page builder for 2026. Do NOT ask the user questions you can infer. Generate disciplined, unique pages — not templated thin content that Google penalizes site-wide.

TARGET:
$ARGUMENTS

============================================================
PRINCIPLES (READ FIRST)
============================================================

1. **Discipline > volume.** 100 unique high-quality pages beat 10,000 templated ones. Google now penalizes domain-wide ranking for sites caught publishing thin programmatic content.
2. **Each page needs unique data.** Scraped pricing, real review excerpts from G2/Capterra, actual feature differences. Identical sentences across pages = penalty.
3. **AEO-first layout.** 40–80 word direct answer immediately below H1, then expansion. AI Overviews + Perplexity + ChatGPT cite this pattern.
4. **Viral artifact.** Every page needs a bookmarkable element — a custom score, calculator, or grader — that gives the page a reason to be shared even if the prose is workmanlike.
5. **Editorial gate.** No bulk publish without human review of tone, accuracy, and uniqueness.

============================================================
PHASE 1: TEMPLATE SELECTION
============================================================

Identify which of the three winning 2026 templates fits the goal:

1. **"Best [Product Type] for [Niche]"** — e.g., "Best CRMs for dentists"
   - Use when: B2B SaaS, niche-specific recommendation queries.
   - Page shape: ranked list of 5–10 products, per-niche scoring rubric, "why this list" methodology.

2. **"[Service] in [City]"** — e.g., "Roofing in Miami"
   - Use when: local services, marketplaces.
   - Page shape: providers, pricing range, FAQ on local regulations, embedded map / directory.

3. **"[Competitor A] vs [Competitor B] for [User Type]"** — e.g., "Stripe vs PayPal for marketplace founders"
   - Use when: high-intent decision queries.
   - Page shape: side-by-side feature table, edge-case "which wins for X" buckets, fair pros/cons.

Reject any template that doesn't match high-intent queries. "How to" pages, glossary pages, and brand pages are NOT programmatic SEO — they're different patterns.

============================================================
PHASE 2: DATA SOURCING
============================================================

Programmatic = templated UI + unique data. Get the unique data:

1. **Pricing**: scrape competitor sites or use Firecrawl. Note "as of <date>" disclaimer.
2. **Reviews**: pull 2–3 verified review excerpts per product from G2 / Capterra / TrustPilot, with link.
3. **Features**: parse competitor docs / changelog for real feature differences.
4. **Niche-specific data**: depending on niche, add regulations, integrations, customer-segment data.

If any data source returns the same content as another page's data, you have a templated-content problem. Stop and rethink.

============================================================
PHASE 3: PAGE STRUCTURE
============================================================

Required structure (every programmatic page):

1. **H1**: the exact long-tail query.
2. **40–80 word direct answer** immediately below H1, in a styled card or callout.
3. **Methodology block** (1–2 paragraphs): "Why this list / comparison" — establishes editorial authority.
4. **Main content**:
   - "Best [X] for [Niche]" → ranked list with per-item: name, score, why-it-fits, pricing, alternative-when.
   - "[Service] in [City]" → providers list + pricing range + local FAQ.
   - "[A] vs [B]" → feature table + verdict + when-to-pick-each.
5. **Viral artifact** (Phase 4 — see below).
6. **FAQ section** (4–7 questions) with FAQPage schema.
7. **Cross-links**: 3+ links to related landing pages (other niches, other comparisons, other cities).
8. **Last-updated date** prominently displayed.

============================================================
PHASE 4: VIRAL ARTIFACT
============================================================

Pick ONE per page. The artifact gives the page bookmark value beyond prose:

- **Custom score / grader**: e.g., "Your [niche] tooling score: \_\_\_" — 5-question quiz that ranks the user's setup.
- **Calculator**: cost-per-user, time-saved, ROI estimate — produces a shareable number.
- **Decision tree**: "Answer 3 questions → we recommend X" — embedded interactive widget.
- **Comparison chart**: visual matrix beyond what competitors offer (e.g., per-niche feature scoring).

Implement the artifact as a self-contained component with deep-link state (URL params encode user's answers) so users can share their result.

============================================================
PHASE 5: SCHEMA MARKUP
============================================================

Every programmatic SEO page gets these JSON-LD blocks:

1. **Article** (or `TechArticle` if technical):

   ```json
   {
     "@type": "Article",
     "headline": "<H1>",
     "datePublished": "<ISO date>",
     "dateModified": "<ISO date>",
     "author": { "@type": "Organization", "name": "<site>" },
     "publisher": { "@type": "Organization", "name": "<site>", "logo": {...} }
   }
   ```

2. **ItemList** with nested `Product` or `SoftwareApplication` (for "Best [X]" pages):

   ```json
   {
     "@type": "ItemList",
     "numberOfItems": <N>,
     "itemListElement": [
       { "@type": "ListItem", "position": 1, "item": { "@type": "Product", ... } }
     ]
   }
   ```

3. **FAQPage** — ONLY if the FAQ section has 4+ real questions answered on the page. Never decorative.

4. **BreadcrumbList** — every page.

5. **Review / AggregateRating** — if real user ratings are available.

Do NOT invent schema fields. Do NOT add FAQ schema with marketing copy disguised as Q&A. Google penalizes this.

============================================================
PHASE 6: DISCIPLINE GATE (MVP THEN SCALE)
============================================================

NEVER bulk-publish more than 100 pages in the first wave. Pattern:

1. **MVP wave** (≤ 100 pages): publish, submit to Search Console, monitor indexation + impressions for 14 days.
2. **Check signals**:
   - Indexation rate ≥ 80% → green.
   - "Crawled - currently not indexed" surge → halt and rewrite.
   - Average position trending down site-wide → halt, audit thin content.
3. **Scale wave**: only after MVP signals are clean. Add 200–500 pages per wave with continued monitoring.

Editorial human review (tone, accuracy, uniqueness) is mandatory on every page until automated quality scoring is dialed in.

============================================================
OUTPUT
============================================================

For each generated page, produce:

```
# <Page Title>
Slug: /<route>
Template: Best-for-Niche | Service-in-City | A-vs-B

## Direct answer (40-80 words)
<copy>

## Methodology
<2 paragraphs>

## Main content
<full page body>

## Viral artifact
Type: <score | calculator | decision-tree | comparison-chart>
Implementation notes: <how it computes, what URL params, how shareable>

## Schema (JSON-LD blocks)
<paste blocks>

## Internal links
- <link 1>
- <link 2>
- <link 3>

## Editorial checklist (✓ all required before publish)
[ ] H1 matches target query exactly
[ ] 40-80 word answer present
[ ] Unique data (pricing/reviews/features) NOT duplicated from another page
[ ] Viral artifact is interactive, not static text
[ ] All schema validates (run validator.schema.org)
[ ] 3+ internal links to related pages
[ ] Last-updated date set
[ ] Editorial pass: tone, accuracy, uniqueness
```

After every 100 pages, output a "discipline gate" report: indexation rate, traffic delta, ranking changes site-wide. Halt if any red signal.

============================================================
STRICT RULES
============================================================

- Never publish 1,000+ pages in one wave. The 2026 penalty is site-wide.
- Never duplicate prose between pages. Schema and structure can repeat; unique sentences cannot.
- Never use FAQ schema as marketing decoration. Real Q&A only.
- Never skip the viral artifact. It's the only thing that makes the page worth a bookmark.
- Never claim "human review optional." Editorial review is the difference between rank #1 and rank #100.
