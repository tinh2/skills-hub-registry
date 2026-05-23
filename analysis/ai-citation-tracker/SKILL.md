---
name: ai-citation-tracker
description: Track brand mentions, URL citations, and share-of-voice across the 2026 AI search surface — ChatGPT (with browsing), Perplexity, Claude (with search), Google Gemini, Google AI Overviews, Bing Copilot, You.com, Phind, and Microsoft Copilot. Polls a configurable query set per engine on a schedule; logs whether your brand was mentioned, whether your URL was cited, who your competitors were, and how all of that moved week over week. Outputs share-of-voice dashboards, weekly delta reports, competitor matrices, and citation-gap analysis (queries where you SHOULD be cited but aren't). Closes the single biggest gap in legacy SEO platforms — Visibly AI / Semrush / Ahrefs / Moz / Conductor all under-cover this surface in 2026, even though AI Overviews now answer 30%+ of informational queries with zero clicks. TRIGGER on "AI citation tracking", "share of voice AI", "ChatGPT citations", "Perplexity citations", "AI Overview tracking", "brand mentions in AI", "LLM visibility", "GEO tracking", "AEO measurement", "AI search analytics", "track Claude citations".
version: "1.0.0"
category: analysis
platforms:
  - CLAUDE_CODE
---

# AI Citation Tracker (the 2026 GEO measurement surface)

You build a multi-engine AI citation tracker. Modern SEO platforms still optimize for Google's blue links. Meanwhile, generative engines deliver 30%+ of informational answers without a click — and those engines DO cite sources, just not in a place Search Console can see. Your job is to make that surface measurable.

============================================================
=== PRE-FLIGHT ===
============================================================

- [ ] **Brand name(s)**: canonical + variants (e.g., "Stripe" + "stripe.com" + product names + key personnel).
- [ ] **Domain(s)**: your URL(s) to detect in citations.
- [ ] **Competitor list**: 5-15 brands you track share of voice against. Without competitors, you have a vanity-metric tracker.
- [ ] **Query universe**: 25-200 priority queries. From: GSC top queries, internal taxonomy, sales objection list, support tickets, customer interviews.
- [ ] **API access**: At least one of — OpenAI API (ChatGPT with browsing), Anthropic API (Claude), Perplexity API, Google AI Studio API (Gemini), Bing Custom Search. Without APIs, fall back to headless browser polling (slower, more brittle).
- [ ] **Storage**: SQLite for solo / Postgres for team / BigQuery for enterprise.

Recovery:
- No competitor list → auto-derive top 5 from cited URLs after 1 week of polling, then prompt user to confirm.
- No API keys → generate Playwright-based engine adapters that hit the consumer UIs (with explicit fragility warning + need-for-residential-proxy notice).

============================================================
=== PHASE 1: ENGINE ADAPTERS ===
============================================================

One adapter per engine. Each adapter answers: "given query Q, what answer was generated and which URLs were cited?"

```python
class EngineAdapter(Protocol):
    name: str  # "chatgpt" | "perplexity" | "claude" | "gemini" | "ai_overviews" | "bing_copilot"

    async def query(self, query: str) -> EngineResult: ...

@dataclass
class EngineResult:
    engine: str
    query: str
    asked_at: datetime
    answer_text: str           # the synthesized answer
    citations: list[Citation]  # ordered as cited
    sources_attribution: str | None  # raw sources HTML/markup if returned
    raw_response: dict          # for replay/debug
    cost_usd: Decimal

@dataclass
class Citation:
    rank: int                  # 1-indexed position in the answer
    url: str
    title: str | None
    snippet: str | None
```

**Engine-specific notes**:

| Engine | Auth | Key URL | Cost ballpark | Notes |
|---|---|---|---|---|
| **ChatGPT (browsing)** | OpenAI API | `/v1/responses` w/ web_search_preview tool | $5-15 per 1k queries | Returns annotations[] with citation URLs |
| **Perplexity** | Perplexity API | `/chat/completions` with `model=sonar-pro` | $5/1M input + $15/1M output | Returns `citations` array natively |
| **Claude (with search)** | Anthropic API | `/v1/messages` w/ `tools=[web_search_20250305]` | $3/1M input + $15/1M output + $10 per 1k searches | Returns citations as part of content |
| **Gemini** | Google AI Studio API | `gemini-2.5-pro` w/ Google Search grounding | $1.25/1M + $5/1M | Returns grounding metadata with URLs |
| **AI Overviews** | SerpAPI / Bright Data SERP | n/a (no first-party API) | $5-20 per 1k queries | Scrape Google SERP, extract AI Overview block + sources |
| **Bing Copilot** | Bing Custom Search + Copilot scraper | n/a (no API) | $5-20 per 1k queries | Headless or SerpAPI |
| **You.com** | You.com API (free tier) | `/api/search` | Free / metered | Returns sources |
| **Phind** | scrape only | n/a | proxy cost | Headless |

VALIDATION: At least 3 engines wired and returning citations end-to-end against a smoke-test query.

FALLBACK: If an engine API is down/rate-limited, the polling job continues other engines + retries the failed one with exp backoff. Single-engine failure never blocks the run.

============================================================
=== PHASE 2: STORAGE SCHEMA ===
============================================================

SQLite/Postgres schema (Prisma-style):

```sql
CREATE TABLE Query (
  id INTEGER PRIMARY KEY,
  text TEXT NOT NULL UNIQUE,
  intent TEXT,                -- informational | commercial | transactional
  priority INTEGER DEFAULT 5, -- 1=critical, 10=long-tail
  added_at DATETIME
);

CREATE TABLE Brand (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,         -- canonical
  aliases TEXT,               -- JSON array
  domain TEXT,                -- if applicable
  is_self BOOLEAN DEFAULT FALSE,  -- our brand vs competitor
  added_at DATETIME
);

CREATE TABLE Poll (
  id INTEGER PRIMARY KEY,
  query_id INTEGER REFERENCES Query(id),
  engine TEXT NOT NULL,
  polled_at DATETIME NOT NULL,
  answer_text TEXT,
  cost_usd DECIMAL,
  raw_response JSON
);

CREATE TABLE Citation (
  id INTEGER PRIMARY KEY,
  poll_id INTEGER REFERENCES Poll(id),
  rank INTEGER,
  url TEXT NOT NULL,
  domain TEXT,                -- derived
  title TEXT,
  snippet TEXT,
  brand_matched INTEGER REFERENCES Brand(id)  -- nullable
);

CREATE TABLE BrandMention (
  id INTEGER PRIMARY KEY,
  poll_id INTEGER REFERENCES Poll(id),
  brand_id INTEGER REFERENCES Brand(id),
  mention_count INTEGER,      -- in answer_text
  cited BOOLEAN,              -- did a URL of theirs appear in citations
  sentiment REAL              -- -1 to 1, optional
);

CREATE INDEX idx_poll_query_engine_date ON Poll(query_id, engine, polled_at DESC);
```

VALIDATION: Schema migrates cleanly. Sample query inserts + reads.

============================================================
=== PHASE 3: POLLING ENGINE ===
============================================================

Generate the polling worker (Python / Node). Schedule:

- **Daily**: top 25 queries × all engines (≈ $5-15/day for ~150 calls).
- **Weekly**: full universe (100-200 queries) × all engines.
- **On-demand**: ad-hoc query investigation.

For each poll:
1. Call engine adapter.
2. Persist `Poll` row + `Citation` rows.
3. Run brand-mention detection on `answer_text`:
   - Match canonical + aliases (case-insensitive, word-boundary regex).
   - Count occurrences.
   - Optional: sentiment via small LLM call on the mention context.
4. Run domain-matching on citations against `Brand.domain`.

Rate-limit aware: respect each provider's RPM. Built-in token-bucket. Exponential backoff on 429.

VALIDATION: Daily run completes within window. Cost stays under budget (configurable, default $20/day cap).

============================================================
=== PHASE 4: METRICS & DELTAS ===
============================================================

Computed per (engine, query, week):

| Metric | Definition |
|---|---|
| **Cited** | Boolean — did our URL appear in citations? |
| **Mentioned** | Boolean — did our brand name appear in answer text? |
| **Citation rank** | If cited, what position (1 = first)? |
| **Share of voice** | (our brand mentions) / (total brand mentions in answer) |
| **Citation share** | (our citations) / (total citations) |
| **Competitor cited count** | Distinct competitor brands cited in answer |
| **Answer length** | Word count of synthesized answer |
| **WoW citation delta** | Cited this week minus cited last week, by query |
| **Top movers** | Queries with largest WoW citation gain/loss |
| **Citation gaps** | Queries where competitors are cited but you aren't |
| **Win-back queue** | Queries where you WERE cited 4 weeks ago but no longer are |

Persist daily; aggregate weekly. Generate `metrics_weekly.csv`.

VALIDATION: Metrics reconcile (per-query sums match aggregates). Weekly delta is non-empty after 2+ weeks of polling.

============================================================
=== PHASE 5: REPORTING ===
============================================================

Generate three reports:

**`weekly_report.md`** — for the team / boss:
- TL;DR: citations gained, lost, share-of-voice movement.
- Top 5 winners (queries newly citing you).
- Top 5 losers (queries no longer citing you).
- Top 5 citation gaps (where competitor X is cited 5+ engines, you're cited 0).
- Recommended content actions (per query, what to write/update to get cited).

**`competitor_matrix.csv`** — engine × competitor matrix of citations:

| Query | ChatGPT | Perplexity | Claude | Gemini | AI Overview | Bing Copilot |
|---|---|---|---|---|---|---|
| "best CRM" | Us, Hubspot, Salesforce | Hubspot, Salesforce | Us | Hubspot | Salesforce, Us | Hubspot |

**`citation_gap_actions.md`** — prescriptive:
For each citation gap, output: target query + which engines miss us + competitor URLs cited + a content brief stub (chain into `/seo-content-brief`).

VALIDATION: Reports render. CSV imports cleanly into Excel/Sheets.

============================================================
=== PHASE 6: ALERTING & DASHBOARD ===
============================================================

Push-style alerts:
- **Brand mention sentiment swing** (sentiment drops > 0.3 in any engine) → Slack/email.
- **Citation loss on top-10 query** → Slack/email same-day.
- **Competitor newly cited on tracked query** → daily digest.
- **Cost over budget** → throttle + alert.

Optional dashboard: Streamlit or Next.js + Prisma. Tabs: Overview, Per-Engine, Per-Query, Competitor Drill, Cost.

VALIDATION: Alerts fire on simulated event in test. Dashboard renders against the SQLite DB.

============================================================
=== PHASE 7: HOW THIS BEATS LEGACY SEO TOOLS ===
============================================================

| Capability | Semrush / Ahrefs | Visibly AI | This skill |
|---|---|---|---|
| Google rank tracking | ✅ | ✅ (via GSC) | (separate skill: gsc-pull) |
| AI Overview citation tracking | partial | ❌ | ✅ |
| ChatGPT citation tracking | ❌ | ❌ | ✅ |
| Perplexity citation tracking | ❌ | ❌ | ✅ |
| Claude / Gemini tracking | ❌ | ❌ | ✅ |
| Share-of-voice across all AI engines | ❌ | ❌ | ✅ |
| Citation-gap → content brief chain | ❌ | partial | ✅ (→ seo-content-brief) |
| Open data (your DB, no vendor lock) | ❌ | ❌ | ✅ |
| Composable with other agents | ❌ | partial | ✅ |
| Cost: per-month | $129-$499 | €39-€399 | API costs only (~$10-50/mo) |

VALIDATION: This positioning resonates with users who already pay for one of the above.

============================================================
=== SELF-REVIEW ===
============================================================

Score 1-5:
- **Complete**: 6+ engine adapters, schema, polling, metrics, reports, alerts?
- **Robust**: Single-engine failure doesn't break the pipeline? Rate-limit / budget controls?
- **Clean**: Citations dedupe? Brand matching handles aliases/case?
- **GEO-credible**: Would a CMO who's seen Visibly / Profound / Otterly / Brand24's AI module recognize this as production-grade?

Common gap: matching only canonical brand name, missing variants. Generate the alias seed list from the user's marketing site + Wikipedia + Crunchbase.

============================================================
=== LEARNINGS CAPTURE ===
============================================================

`~/.claude/skills/ai-citation-tracker/LEARNINGS.md`.

============================================================
=== STRICT RULES ===
============================================================

- Never poll without rate-limit / budget caps. AI engine APIs are billed; runaway loops are expensive.
- Never silently drop a failed engine. Surface the failure in the run report.
- Never use brand matching by canonical name alone. Aliases + variants are required.
- Always include competitor tracking. Share-of-voice without comparison is a vanity number.
- Always preserve raw_response. New citation patterns emerge; you'll want to replay.
