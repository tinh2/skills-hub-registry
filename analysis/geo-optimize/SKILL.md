---
name: geo-optimize
description: Generative Engine Optimization (GEO) / Answer Engine Optimization (AEO) — make a site citable by ChatGPT, Perplexity, Claude, Gemini, and Google AI Overviews. Generates llms.txt and llms-full.txt, fills schema.org coverage gaps (Organization, Person/Author, Article, Product, FAQPage, HowTo, BreadcrumbList), audits entity density (target 15+ recognized entities per pillar page → 4.8x AI Overview selection rate), tests AI crawler parity (fetches as GPTBot / PerplexityBot / OAI-SearchBot / ClaudeBot and confirms content visibility without JS), audits E-E-A-T author entity signals (Person → Organization → topic graph), and produces a prioritized GEO punch list. TRIGGER on "GEO", "generative engine optimization", "AEO", "answer engine optimization", "AI search optimization", "get cited by ChatGPT", "Perplexity citations", "AI Overviews", "llms.txt", "schema markup", "entity SEO", "topical authority", "AI search visibility". GEO is distinct from traditional SEO — invoke this skill whenever a user wants to be discovered by AI search agents specifically.
version: "1.0.0"
category: analysis
platforms:
  - CLAUDE_CODE
---

# GEO / AEO Optimizer

You optimize a website for citation by AI search engines (ChatGPT browsing, Perplexity, Claude, Gemini, Google AI Overviews, Bing Copilot). The discipline is called **Generative Engine Optimization (GEO)** or **Answer Engine Optimization (AEO)** depending on the source — same thing.

This is not a 2024-style SEO audit. AI search ranks differently:

- **96% of AI Overview citations** come from sources with strong E-E-A-T signals.
- **Pages with 15+ recognized entities** have **4.8× higher probability** of AI Overview selection.
- **Pages ranking #6–#10 with strong EEAT are cited 2.3× more often** than #1-ranked pages with weak EEAT.
- **GPT-4 accuracy goes from 16% → 54%** when content has structured data.
- **AI crawlers don't execute JavaScript** — if content needs JS to render, AI engines can't see it.

============================================================
=== PRE-FLIGHT ===
============================================================

Before auditing, verify:

- [ ] **Site URL provided** (root domain, not just a single page).
- [ ] **Rendering strategy known.** SSR / SSG / CSR? AI crawlers do not run JS. CSR-only sites fail GEO before they start.
- [ ] **CMS / hosting access.** Some fixes (llms.txt, schema injection, robots.txt allow rules for AI bots) require write access.
- [ ] **Target topics defined.** What 5-10 queries do you want to be cited for? Without targets, "visibility" can't be measured.
- [ ] **Tooling available.** `curl` for user-agent tests, `playwright` or `puppeteer` for render diffs, `jq` for JSON-LD parsing.

Recovery:

- If site is purely client-rendered (Next.js SPA mode, React SPA, Vue SPA without SSR), the first deliverable is a switch-to-SSR recommendation. Do NOT generate downstream GEO fixes for content AI literally cannot see.
- If user can't provide target queries, generate a starter set from their main nav + top 10 pages by traffic (Google Search Console export accepted).

============================================================
=== PHASE 1: AI CRAWLER PARITY TEST ===
============================================================

The single most predictive test: can AI crawlers actually see your content?

Generate `geo/parity_test.sh`:

```bash
#!/usr/bin/env bash
# Fetch pages as each AI bot and verify content parity vs human browser

URL="$1"
USER_AGENTS=(
  "GPTBot/1.0 (+https://openai.com/gptbot)"
  "OAI-SearchBot/1.0 (+https://platform.openai.com/docs/bots)"
  "ChatGPT-User/1.0 (+https://openai.com/bot)"
  "PerplexityBot/1.0 (+https://perplexity.ai/perplexitybot)"
  "Perplexity-User/1.0 (+https://perplexity.ai/perplexity-user)"
  "ClaudeBot/1.0 (+https://anthropic.com/claudebot)"
  "Claude-Web/1.0 (+https://anthropic.com)"
  "Google-Extended/1.0"
  "GoogleOther/1.0"
  "Bingbot/2.0 (compatible; MSNBot/2.0; +http://search.msn.com/msnbot.htm)"
  "Applebot-Extended/1.0"
)

for ua in "${USER_AGENTS[@]}"; do
  echo "=== $ua ==="
  curl -sSL -A "$ua" "$URL" | grep -oE "(<title>.*</title>|<h1[^>]*>.*</h1>)" | head -3
  echo
done
```

Then run a JS-rendered fetch via Playwright and diff key content elements (title, H1, body length, structured data, target keywords). If non-trivial drift, flag as a P0 issue.

VALIDATION: At minimum, title + H1 + first 500 words of body must be identical between the no-JS GPTBot fetch and the rendered human view. Schema.org JSON-LD must be in the static HTML (not injected client-side).

FALLBACK: If the site fails parity, do NOT continue downstream phases. Generate a remediation plan first: move to SSR (Next.js, Astro, Nuxt SSR mode, Remix, SvelteKit SSR) or pre-render critical pages.

============================================================
=== PHASE 2: LLMS.TXT GENERATION ===
============================================================

`llms.txt` is the emerging standard for telling LLMs about your site at a high level. It's the AI-era cousin of `robots.txt` + `sitemap.xml` collapsed into a curated human-readable index.

Generate two files at the site root:

### `/llms.txt` (curated, terse)

```markdown
# {Site Name}

> {One-sentence value proposition that an LLM should learn about you}

## Core Pages

- [About](https://example.com/about): One-sentence summary
- [Products](https://example.com/products): What you sell, who it's for
- [Pricing](https://example.com/pricing): Tiers and starting prices

## Documentation

- [Getting Started](https://example.com/docs/start)
- [API Reference](https://example.com/docs/api)

## Trust & Authority

- [Customer Stories](https://example.com/customers)
- [Press & Recognition](https://example.com/press)

## Contact

- Support: support@example.com
- Sales: sales@example.com
```

### `/llms-full.txt` (full corpus, for LLMs that want depth)

Concatenate the markdown content of the 20-50 most important pages, with H1 headings and source URLs as anchors. Cap at ~200KB so it fits in typical context windows.

VALIDATION: Both files are publicly accessible at site root (HTTP 200, Content-Type text/plain or text/markdown). `llms.txt` is under 8KB. `llms-full.txt` is under 250KB. No JS required to view.

FALLBACK: If the user can't write to site root, generate as a static asset they can deploy via their static-site host (Netlify, Vercel, Cloudflare Pages all serve `/public/llms.txt`).

============================================================
=== PHASE 3: SCHEMA.ORG COVERAGE AUDIT & FILL ===
============================================================

Scan every important page for JSON-LD and report coverage. The schema types that move the needle for AI citations:

| Page Type           | Required Schema                                                    |
| ------------------- | ------------------------------------------------------------------ |
| Homepage            | Organization (with `sameAs` to social/Wikidata/Crunchbase)         |
| About / Team        | Person (each author/founder with `sameAs`, `jobTitle`, `worksFor`) |
| Article / Blog Post | Article + `author` (Person) + `publisher` (Organization)           |
| Product             | Product + Offer + AggregateRating (if reviews exist)               |
| Docs / Guides       | HowTo OR TechArticle, with `step` array                            |
| FAQ                 | FAQPage with `mainEntity` array                                    |
| Listing / Category  | ItemList + BreadcrumbList                                          |
| Local Business      | LocalBusiness with `geo`, `openingHoursSpecification`              |
| Reviews             | Review with `author`, `itemReviewed`, `reviewRating`               |
| Events              | Event with `startDate`, `location`, `offers`                       |
| Job Posting         | JobPosting                                                         |
| Video               | VideoObject with `transcript` (massive AI citation boost)          |

For EACH missing schema, generate valid JSON-LD with required + recommended properties filled. Use the user's actual data, not placeholders.

The `sameAs` property on Organization and Person is the single highest-leverage entity-graph signal — link to Wikidata QID, LinkedIn, Crunchbase, Google Knowledge Panel, X, Wikipedia.

VALIDATION: Every generated JSON-LD passes Google Rich Results Test (schema.org validator) with zero errors. `sameAs` arrays exist on at least Organization and the top 3 author/founder Person nodes.

============================================================
=== PHASE 4: ENTITY DENSITY AUDIT ===
============================================================

For each pillar page (high-traffic, high-conversion, or strategic content), count "recognized entities" — proper nouns that map to a Knowledge Graph node (companies, products, people, places, technologies, standards).

Target: **≥ 15 recognized entities per pillar page** (the 4.8× selection threshold from 2026 ranking factor research).

Process per page:

1. Extract proper nouns.
2. Cross-check each against a knowledge base (Wikidata QIDs preferred; fallback to Google KG via `Google-Extended` searches).
3. Count entities that resolve. Report:
   - Entity count
   - Entity diversity (different entity TYPES — Person, Org, Product, Place — better than 15 of one type)
   - Missing co-occurring entities a competitor cites for the same topic (gap analysis)

Output `geo/entity_audit.md` with per-page recommendations.

VALIDATION: Each pillar page either meets the ≥15 threshold OR has a specific list of entities to add, with where they should be inserted naturally.

FALLBACK: If knowledge-graph lookups are rate-limited, fall back to a static curated entity list per industry (industries.yaml) — coverage is partial but report explicitly notes the gap.

============================================================
=== PHASE 5: E-E-A-T & AUTHOR ENTITY ===
============================================================

E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness) is a **binary citation gate** for AI search in 2026, not a ranking nudge.

Check:

- [ ] **Author bylines** on every article. Author name links to `/author/{slug}` page.
- [ ] **`/author/{slug}` page exists** with bio, photo, credentials, social `sameAs` links.
- [ ] **Person schema** on author pages, with `worksFor`, `knowsAbout`, `alumniOf`, social `sameAs`.
- [ ] **Organization schema** on homepage with `founder`, `foundingDate`, `numberOfEmployees`, address, `sameAs`.
- [ ] **Press / mentions page** linking out to third-party coverage (off-domain authority signals).
- [ ] **Last-updated dates** visible on all articles (Google added Authors documentation 2026-02-01 making this a direct quality signal).
- [ ] **Citations within content** linking to primary sources (academic, government, established publications). AI engines mirror your citation behavior — sites that cite get cited.
- [ ] **First-party data / experience markers**: original screenshots, original case studies, dated metrics. Generic content without first-hand experience signals fails E-E-A-T.

Output `geo/eeat_report.md` per author and per content section.

VALIDATION: Each pillar page has a named author with a linked Person page. Person page has at least 3 `sameAs` entries linking to verifiable third-party profiles.

============================================================
=== PHASE 6: AI BOT ALLOW RULES & RATE LIMITS ===
============================================================

Update `robots.txt` to explicitly allow AI bots you want to index you. Default policy:

```
User-agent: *
Allow: /

User-agent: GPTBot
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Perplexity-User
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Claude-Web
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: Applebot-Extended
Allow: /

User-agent: anthropic-ai
Allow: /

Sitemap: https://example.com/sitemap.xml
```

If the site is behind Cloudflare's AI bot blocker (now default-on for many tenants), surface that and recommend disabling for the bots above.

VALIDATION: `curl -A "GPTBot" https://yourdomain.com/robots.txt` returns the file. `curl -A "GPTBot" https://yourdomain.com/some-pillar-page` returns 200 with full content.

FALLBACK: If the user explicitly wants to block training (vs indexing for citation), they can allow `*-User` and `*-SearchBot` (live retrieval) while blocking `GPTBot` and `ClaudeBot` (training). Document the trade-off — blocking training also tends to reduce indexing.

============================================================
=== PHASE 7: CITATION TRACKING SETUP ===
============================================================

GEO success requires measuring what was cited and where.

Generate `geo/track_citations.py` — a recurring polling job that:

1. For each target query, prompts ChatGPT (via API), Perplexity (via API), Claude (via API), and Gemini.
2. Captures the answer + any URL citations.
3. Logs to a SQLite DB: `query`, `engine`, `date`, `cited_urls[]`, `our_brand_mentioned (bool)`, `our_url_cited (bool)`, `competitors_cited[]`.
4. Generates a weekly report: share-of-voice per engine per query, week-over-week deltas.

Set up via cron or as a scheduled skill (`/schedule` weekly).

VALIDATION: First run produces a baseline. Second run a week later produces a delta report. Both runs persist to `geo/citations.db`.

FALLBACK: Without API keys for Perplexity/ChatGPT, fall back to manual logging via a Google Sheet template (less precise but still actionable).

============================================================
=== PHASE 8: PRIORITIZED PUNCH LIST ===
============================================================

Output `geo/punch_list.md` with findings ranked by impact:

| Priority | Issue                                       | Impact                     | Effort |
| -------- | ------------------------------------------- | -------------------------- | ------ |
| P0       | Site uses CSR, AI bots see empty HTML       | Blocks ALL citations       | High   |
| P0       | Missing Organization schema on homepage     | No entity grounding        | Low    |
| P1       | 8 of 12 pillar pages have < 15 entities     | -4.8× citation probability | Medium |
| P1       | No author Person pages                      | EEAT gatekeeper fails      | Medium |
| P2       | llms.txt missing                            | Lost soft signal           | Low    |
| P3       | Schema FAQPage missing on 4 pages with FAQs | Lost rich result           | Low    |

Each item links to the specific phase output explaining the fix.

VALIDATION: Punch list is non-empty AND non-overwhelming (top 20 items max). P0 items are unambiguous, not stylistic preferences.

============================================================
=== SELF-REVIEW ===
============================================================

Score 1–5:

- **Complete**: All 8 phases run? Crawler parity tested? Schema generated and validated? Entity density measured?
- **Robust**: Handled CSR sites? Cloudflare blocks? Missing API keys for tracking?
- **Clean**: Punch list is prioritized, not a dump? JSON-LD validates? llms.txt under size cap?
- **GEO-credible**: Would an SEO consultant familiar with AI search engines (Perplexity, AI Overviews) sign off on the recommendations as 2026-current?

============================================================
=== LEARNINGS CAPTURE ===
============================================================

Append to `~/.claude/skills/geo-optimize/LEARNINGS.md`:

## <YYYY-MM-DD> — <site, vertical, framework>

- **What worked:** <approach/tool that produced clean output>
- **What was awkward:** <retry/manual fix needed>
- **Suggested patch:** <concrete improvement>
- **Verdict:** [Smooth / Minor friction / Major friction]

============================================================
=== STRICT RULES ===
============================================================

- Never generate schema with placeholder values like "Your Company Name". Use real values or skip.
- Never skip the crawler parity test. CSR sites fail GEO before anything else matters — diagnose this first.
- Never recommend blocking all AI bots without surfacing the trade-off (blocking training often reduces indexing too).
- Never claim a page is "GEO-ready" without ≥15 entities AND validated schema AND author Person entity.
- llms.txt is a soft signal — don't oversell it. Schema and SSR are the load-bearing fixes.
- If the user is on a no-code platform (Squarespace, Wix, Shopify base theme) that limits schema injection, output the JSON-LD they can paste into header/footer settings — don't hand-wave.
