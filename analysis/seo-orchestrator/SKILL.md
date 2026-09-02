---
name: seo-orchestrator
description: "The full open SEO suite for 2026 — a single orchestrator that composes 10+ specialized sub-skills into a daily, weekly, and on-demand workflow that owns the SEO + GEO surface for a site.."
version: "1.0.1"
category: analysis
platforms:
  - CLAUDE_CODE
---

# SEO Orchestrator (the open suite that beats Visibly / Semrush / Ahrefs)

You orchestrate the full SEO + GEO workflow. The pitch from incumbents (Semrush, Ahrefs, Visibly AI, Conductor, Moz, BrightEdge): pay $129-$999/month for a closed dashboard that wraps Google's data plus a handful of features they've bolted on. The pitch here: your own code, your own data, the same coverage plus the 2026 AI-search layer they're not yet covering.

This is the front door. Behind it sit 10 sub-skills, each doing one job extremely well. The orchestrator runs them in the right order, dedupes their findings, and presents a single ranked action list.

============================================================
=== HOW THIS BEATS VISIBLY AI HEAD-TO-HEAD ===
============================================================

| Capability | Visibly AI | This suite |
|---|---|---|
| Crawling agent (sitemap + JS-rendered) | ✅ | ✅ via `/seo-audit-2026` + `/internal-link-graph` |
| SEO analyst (GSC + GA4 integration) | ✅ | ✅ via `/gsc-pull` |
| Strategist (topical clusters + keyword plans) | ✅ | ✅ via `/internal-link-graph` cluster analysis + `/seo-content-brief` |
| Copywriter (drafts content) | ✅ | ✅ via `/wp-content-write` + `/seo-content-brief` |
| Chief Editor (E-E-A-T + quality checks) | ✅ | ✅ via `/seo-audit-2026` Phase 6 + `/geo-optimize` Phase 5 |
| Consultant (insights / advice) | ✅ | ✅ via this orchestrator's punch list |
| **AI search citation tracking** (ChatGPT / Perplexity / Claude / Gemini / AI Overviews) | ❌ | **✅ via `/ai-citation-tracker`** |
| **Cannibalization detection + resolution patches** | partial | ✅ via `/content-cannibalization` |
| **Semantic internal linking** (not keyword matching) | partial | ✅ via `/internal-link-graph` |
| **llms.txt + schema generation** | partial | ✅ via `/geo-optimize` |
| **AI crawler parity testing** (GPTBot / PerplexityBot / ClaudeBot) | ❌ | ✅ via `/seo-audit-2026` + `/geo-optimize` |
| **Entity density audit** (15+ entity threshold) | ❌ | ✅ via `/geo-optimize` |
| **E-E-A-T author entity** (Person + sameAs chain) | partial | ✅ via `/geo-optimize` + `/seo-audit-2026` |
| Open data (your DB, exportable) | ❌ | ✅ SQLite / Postgres / BigQuery — your choice |
| Open code (your repo, auditable, extensible) | ❌ | ✅ everything generated, nothing hidden |
| Composable with non-SEO agents | ❌ | ✅ chains with any skills-hub skill |
| Cost | €39-€399/month | API costs only (~$10-50/month for citation polling) |

============================================================
=== PRE-FLIGHT ===
============================================================

- [ ] **Site URL + property**: domain + GSC property + GA4 property (if available).
- [ ] **Brand list**: canonical brand name + aliases + key personnel.
- [ ] **Competitor list**: 5-15 brands for share-of-voice tracking.
- [ ] **Target query universe**: 50-500 priority queries. Bootstrap from GSC top queries if unsure.
- [ ] **API keys**:
  - Google Search Console API (service account)
  - Google Analytics 4 API (optional)
  - One of: OpenAI (ChatGPT), Anthropic (Claude), Perplexity API, Google AI Studio (Gemini)
  - SerpAPI / Bright Data SERP (for AI Overviews tracking — no first-party API)
- [ ] **CMS access** (WordPress, Hugo, Ghost, Next.js MDX, etc.) — needed for content publishing + redirect/canonical patches.
- [ ] **Storage**: SQLite for solo / Postgres for team / BigQuery for enterprise.
- [ ] **Cadence preference**: daily, weekly, or on-demand?

Recovery:
- Missing GA4: skill suite still functional — falls back to GSC clicks only.
- Missing AI engine APIs: degrades to Playwright headless polling for those engines (slower, more brittle).
- No competitor list: derive top 5 from AI citation polling after 1 week, then ask user to confirm.

============================================================
=== PHASE 1: ONE-TIME SETUP ===
============================================================

First run only. Bootstraps the data layer.

```bash
# 1. Initialize storage
mkdir seo/ && cd seo/
sqlite3 seo.db < schema.sql   # composed schema from all sub-skills

# 2. Wire credentials (env file)
cat > .env <<EOF
GSC_SERVICE_ACCOUNT_PATH=./creds/gsc-sa.json
GSC_SITE_URL=sc-domain:example.com
GA4_PROPERTY_ID=...
OPENAI_API_KEY=...
ANTHROPIC_API_KEY=...
PERPLEXITY_API_KEY=...
GOOGLE_AI_API_KEY=...
SERPAPI_KEY=...
EOF

# 3. Initial backfill (one-time, ~30 min)
/gsc-pull --backfill 16months
/internal-link-graph --crawl
/ai-citation-tracker --backfill 4weeks    # seeds historical baseline
/seo-audit-2026 --full
```

VALIDATION: Setup completes; all integrations green; baseline data in DB.

============================================================
=== PHASE 2: DAILY WORKFLOW (cron) ===
============================================================

Runs every day at 02:00. Generated cron:

```bash
# Cron: 0 2 * * *
cd /path/to/seo

# Pull yesterday's GSC data
/gsc-pull --daily

# Poll top 25 priority queries across all engines
/ai-citation-tracker --priority-queries

# Detect critical regressions
/seo-orchestrator --daily-deltas
```

Daily output: `daily_alert_{date}.md` — sent to Slack if any of:
- Top-10 query lost > 30% clicks
- Top-10 query lost > 3 positions
- Newly cited competitor on tracked query
- Brand mention sentiment swing > 0.3

VALIDATION: Daily run finishes in < 5 minutes. Alert fires only on genuine regressions.

============================================================
=== PHASE 3: WEEKLY WORKFLOW ===
============================================================

Runs Monday 03:00. The "Monday morning intel briefing."

```bash
# 1. Refresh data
/gsc-pull --weekly                   # 7-day rollup + WoW delta
/internal-link-graph --recrawl       # weekly fresh crawl
/ai-citation-tracker --full-universe # all priority queries

# 2. Run analyses
/seo-audit-2026 --priority-pages     # focus on movers + cannibalized clusters
/geo-optimize --punch-list           # GEO findings
/content-cannibalization              # cluster analysis
/internal-link-graph --recommendations # new semantic link recs

# 3. Compose
/seo-orchestrator --weekly-report
```

Generates `weekly_report.md`:

```markdown
# SEO Weekly — {site} — {week}

## Headline
- Total clicks WoW: +X (+Y%)
- AI Overview citations: gained N, lost M
- ChatGPT citations: gained N, lost M  
- Perplexity citations: gained N, lost M
- Cannibalization clusters: N detected, M resolved this week
- New orphan pages: N (from /internal-link-graph)
- Audit P0 issues: N open (from /seo-audit-2026)

## P0 — Do this week
1. [Cannibalization] "best CRM" cluster → 301 /blog/reviews to /blog/best-crm. Expected: +180 clicks/week. Effort: 30 min.
2. [GEO] Add Organization + Person schema to homepage. Expected: +AI Overview eligibility. Effort: 1 hour.
3. [Citation gap] "API rate limits" — competitor X cited in ChatGPT + Perplexity. Run /seo-content-brief to plan response. Effort: 4 hours content.

## P1 — Do this month
{ordered list}

## Trends
- Branded vs nonbranded split: {chart}
- AI search share-of-voice trajectory: {chart}
- Position distribution: top-3 vs 4-10 vs 11+ {chart}
```

VALIDATION: Weekly report under 2 pages, every P0/P1 has expected impact + effort.

============================================================
=== PHASE 4: ON-DEMAND WORKFLOWS ===
============================================================

Common explicit asks:

**"Write content for query X"**:
```bash
/ai-citation-tracker --query "X" --inspect    # what's already cited
/seo-content-brief --query "X"                 # 2026 brief w/ entities + intent
/wp-content-write --brief brief_X.md           # if WordPress
```

**"Fix our checkout page rankings"**:
```bash
/gsc-pull --page /checkout
/seo-audit-2026 --url /checkout
/internal-link-graph --target /checkout       # find link gaps
```

**"Competitor X just launched a new pillar — analyze"**:
```bash
/ai-citation-tracker --competitor X
/content-cannibalization --against X
```

**"Site migration — minimize SEO damage"**:
```bash
/seo-audit-2026 --pre-migration       # baseline
# ... migrate ...
/seo-audit-2026 --post-migration --diff
/gsc-pull --post-migration-monitoring
```

VALIDATION: Each on-demand workflow chains the right sub-skills with the right inputs.

============================================================
=== PHASE 5: PUNCH LIST PRIORITIZATION ===
============================================================

The orchestrator's core job: dedupe findings across sub-skills and rank by impact × confidence × inverse effort.

Each finding has shape:

```json
{
  "id": "uuid",
  "source_skill": "geo-optimize | seo-audit-2026 | ...",
  "category": "P0_BLOCKING | P1_HIGH | P2_MEDIUM | P3_POLISH",
  "title": "...",
  "description": "...",
  "expected_impact": {"metric": "clicks_weekly", "delta": 180, "confidence": 0.8},
  "effort_hours": 0.5,
  "blocked_by": [],
  "files_to_change": ["..."],
  "fix_snippet": "..."
}
```

Dedup rules:
- If two sub-skills flag the same URL with similar fix, merge into one finding with both sources cited.
- If a fix is blocked by another (e.g., cannibalization 301 depends on internal link audit), respect `blocked_by` order.

Rank: `score = expected_impact.delta * confidence / effort_hours`. Surface top 20.

VALIDATION: Top 20 has no duplicates. Score reasoning is auditable per finding.

============================================================
=== PHASE 6: CMS PUBLISHING INTEGRATION ===
============================================================

For each fix that touches a page, generate a CMS-specific patch:

| CMS | Patch format |
|---|---|
| **WordPress** | REST API call OR migration .sql OR Redirection plugin CSV |
| **Hugo / Jekyll / Astro / Next.js MDX** | git diff (markdown) committed to repo |
| **Webflow** | CMS export JSON + Designer notes |
| **Squarespace** | Manual step (CMS doesn't have a programmatic write API for blocks) — generate exact text + screenshot of where to paste |
| **Shopify** | Admin API call OR theme.liquid patch |
| **Ghost** | Admin API call |

Generate `publish_queue/` with one patch file per pending fix. Optionally chain `/wp-publish` to push WordPress.

VALIDATION: Each patch is syntactically valid for its CMS.

============================================================
=== PHASE 7: COST DASHBOARD ===
============================================================

Track API spend across sub-skills:

```markdown
## SEO Suite — Monthly Cost — {month}

| Source | Calls | Cost |
|---|---|---|
| GSC API | 2,400 | $0 (free) |
| GA4 API | 600 | $0 (free) |
| OpenAI (ChatGPT browsing) | 750 polls | $4.20 |
| Anthropic Claude | 750 polls | $3.80 |
| Perplexity | 750 polls | $2.10 |
| Gemini | 750 polls | $1.30 |
| SerpAPI (AI Overviews) | 1500 calls | $7.50 |
| OpenAI embeddings | 5M tokens | $0.10 |
| **Total** | | **$19.00** |

Compare to: Visibly AI Pro €119/mo, Semrush $129/mo, Ahrefs Lite $129/mo, Conductor $$$$
```

VALIDATION: Cost summary matches actual API billing.

============================================================
=== SELF-REVIEW ===
============================================================

Score 1-5:
- **Complete**: All sub-skills wired? Daily + weekly + on-demand workflows working?
- **Robust**: Single sub-skill failure doesn't break orchestration?
- **Clean**: One ranked punch list, no duplicates?
- **Competitive**: Side-by-side with Visibly / Semrush, does this win on the AI-search dimension AND match on classic SEO?

Common gap: data freshness inconsistency — citation data from Monday but GSC data from Sunday makes the report incoherent. Pin all weekly sub-skills to the same `as_of` timestamp.

============================================================
=== LEARNINGS CAPTURE ===
============================================================

`~/.claude/skills/seo-orchestrator/LEARNINGS.md`.

============================================================
=== STRICT RULES ===
============================================================

- Never run sub-skills in parallel without explicit data-freshness coordination. Pin the `as_of` to a single timestamp per run.
- Never run the full weekly pipeline more than once per week. Daily deltas vs weekly trends — different cadences, different intent.
- Never publish CMS patches autonomously without human review for the first 30 days. Trust takes time; one bad 301 hurts.
- Never skip the cost dashboard. AI engine polling adds up; budget visibility is a feature, not optional.
- Always preserve the punch list history. Month-over-month resolution counts are how you prove value.

============================================================
=== INSTALL & QUICKSTART ===
============================================================

```bash
# 1. Install via skills-hub CLI
npx @skills-hub-ai/cli install seo-orchestrator
npx @skills-hub-ai/cli install ai-citation-tracker gsc-pull internal-link-graph content-cannibalization
npx @skills-hub-ai/cli install seo-audit-2026 geo-optimize seo-content-brief

# 2. Initial run
/seo-orchestrator --setup

# 3. Schedule daily + weekly via cron (or use /schedule)
/seo-orchestrator --schedule daily weekly
```

You now have a production SEO suite running on your data, your code, your stack — for ~$20/month in API costs.
