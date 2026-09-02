---
name: gsc-pull
description: "Pull and analyze Google Search Console data via the GSC API. Produces: weekly query × page performance with WoW/MoM/YoY deltas, top movers report (winners + losers ranked by absolute click change), click-loss attribution (lost rank? Triggers: \"GSC\", \"Google Search Console\"."
version: "1.0.1"
category: analysis
platforms:
  - CLAUDE_CODE
---

# GSC Pull & Analysis Pipeline

You generate a Google Search Console data pipeline + analyzer. The platform value of Semrush/Ahrefs/Visibly is mostly "we wrap the GSC API for you." You can do it better by giving the user the data + the queries + the analysis in their own stack.

============================================================
=== PRE-FLIGHT ===
============================================================

- [ ] **GSC property** verified and owned. Domain property preferred over URL prefix.
- [ ] **GSC API access**: enabled via Google Cloud Console (Webmasters API). Service account with owner-level access to the property.
- [ ] **Storage target**: SQLite (solo), Postgres (team), BigQuery (enterprise / longitudinal analysis past 16-month GSC retention).
- [ ] **Time range**: GSC API returns 16-month rolling window. For longitudinal trends, you must persist locally — start the pipeline NOW even if you don't analyze yet.
- [ ] **Brand list**: list of branded terms to split branded vs nonbranded traffic.

Recovery:
- If service account isn't set up: generate the gcloud + IAM commands; the user runs them once.
- If property is URL prefix only: warn user; data will be incomplete vs domain property.

============================================================
=== PHASE 1: API CLIENT + AUTH ===
============================================================

Generate `gsc_client.py` (Python preferred — Google's `google-api-python-client` is mature):

```python
from google.oauth2 import service_account
from googleapiclient.discovery import build

class GSCClient:
    SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]
    
    def __init__(self, service_account_path: str, site_url: str):
        creds = service_account.Credentials.from_service_account_file(
            service_account_path, scopes=self.SCOPES
        )
        self.service = build("searchconsole", "v1", credentials=creds)
        self.site = site_url  # "sc-domain:example.com" or "https://example.com/"
    
    def search_analytics(self, start, end, dimensions, filters=None, row_limit=25000):
        """
        dimensions: ["date", "query", "page", "country", "device", "searchAppearance"]
        Returns up to 25k rows per call. Use date partitioning for full coverage.
        """
        body = {
            "startDate": start.isoformat(),
            "endDate": end.isoformat(),
            "dimensions": dimensions,
            "rowLimit": row_limit,
            "dataState": "final",  # vs "all" which includes fresh (estimated) data
        }
        if filters: body["dimensionFilterGroups"] = filters
        # paginate via startRow up to 50k total per (start, end) range
        ...
    
    def inspect_url(self, inspection_url: str, language_code="en-US"):
        """URL Inspection API — 2k requests per day per site. Use sparingly."""
        return self.service.urlInspection().index().inspect(body={
            "inspectionUrl": inspection_url,
            "siteUrl": self.site,
            "languageCode": language_code,
        }).execute()
```

VALIDATION: Smoke test fetches recent 7-day query data. URL inspection returns IndexStatusResult for a known indexed page.

============================================================
=== PHASE 2: DATA SCHEMA ===
============================================================

```sql
CREATE TABLE gsc_daily (
  date DATE NOT NULL,
  query TEXT,
  page TEXT,
  country TEXT,
  device TEXT,
  search_appearance TEXT,
  impressions INTEGER,
  clicks INTEGER,
  position REAL,
  ctr REAL GENERATED ALWAYS AS (CASE WHEN impressions > 0 THEN clicks * 1.0 / impressions ELSE 0 END),
  PRIMARY KEY (date, query, page, country, device, search_appearance)
);
CREATE INDEX idx_gsc_query ON gsc_daily(query);
CREATE INDEX idx_gsc_page ON gsc_daily(page);
CREATE INDEX idx_gsc_date ON gsc_daily(date);

CREATE TABLE gsc_url_inspection (
  url TEXT PRIMARY KEY,
  last_inspected DATETIME,
  index_status TEXT,        -- "PASS" / "FAIL" / "NEUTRAL"
  coverage_state TEXT,
  google_canonical TEXT,
  user_canonical TEXT,
  mobile_usable BOOLEAN,
  rich_results_eligible BOOLEAN,
  last_crawl DATETIME,
  crawled_as TEXT,          -- DESKTOP / MOBILE
  page_fetch_state TEXT,
  raw_response JSON
);
```

VALIDATION: 16-month backfill loads without primary-key conflicts. Storage size estimate matches expectation (~10MB per 1k unique queries per month).

============================================================
=== PHASE 3: WEEKLY PULL JOB ===
============================================================

Schedule (cron or scheduled skill):

```
daily 02:00 → pull yesterday's data, idempotent upsert
weekly Mon 03:00 → reconcile last 7 days, compute deltas
monthly 1st 04:00 → 16-month backfill check, fill gaps
```

Per pull:
1. Fetch `[date, query, page, country, device]` daily.
2. Fetch `[date, query]` and `[date, page]` separately (deduplicated rollups, smaller payload).
3. Sample 50 URLs/day for URL Inspection (respect 2k/day cap).

VALIDATION: Daily cron runs without manual intervention for 30 days. No duplicate-key errors.

============================================================
=== PHASE 4: ANALYSIS — TOP MOVERS ===
============================================================

Generate `top_movers.py`:

For each (query, page) pair appearing in either of two windows (current week vs comparison week), compute:

```python
@dataclass
class Mover:
    query: str
    page: str
    clicks_current: int
    clicks_prior: int
    clicks_delta: int            # current - prior
    clicks_pct_change: float     # (current - prior) / prior
    impressions_delta: int
    position_delta: float        # negative = position improved
    ctr_delta: float
    is_winner: bool              # clicks_delta > 0 AND magnitude meaningful
```

**Winners**: top 25 by `clicks_delta` (filter `impressions_prior > 100` to filter noise).

**Losers**: bottom 25 by `clicks_delta` (same filter).

**Click-loss attribution**: for each loser, classify:
- `RANK_LOSS`: position_delta > 1.0 and clicks_delta < 0
- `IMPRESSION_LOSS`: position stable, impressions down (Google reduced surfacing)
- `CTR_LOSS`: position stable, impressions stable, CTR down (SERP feature ate clicks)
- `SEASONAL`: matches a YoY pattern at the same query

VALIDATION: Movers report identifies a known win/loss from a fixture.

============================================================
=== PHASE 5: ANALYSIS — QUERY-PAGE MISMATCH ===
============================================================

A query-page mismatch happens when:
- A query ranks via the WRONG page on your site (target page is buried, intent page underperforms).
- Multiple pages compete for the same query (= cannibalization — chain to `/content-cannibalization`).

Detect: for each query with > 100 impressions in the window, list all (page, impressions, clicks, avg position). Flag where the top-impression page differs from the page you intended to rank.

Output `query_page_mismatch.csv` with recommended action (consolidate, canonicalize, redirect, differentiate, or update internal links).

VALIDATION: Mismatches show concrete page paths + actionable recommendation.

============================================================
=== PHASE 6: BRANDED-VS-NONBRANDED SPLIT ===
============================================================

For each query, classify branded or nonbranded based on the brand alias list:

```python
def classify(query: str, brand_aliases: list[str]) -> str:
    q = query.lower()
    return "branded" if any(a.lower() in q for a in brand_aliases) else "nonbranded"
```

Compute weekly totals: `branded_clicks`, `nonbranded_clicks`, `branded_share`. Track trend over time.

Healthy growth profile: nonbranded growing faster than branded (you're acquiring new users, not just being searched for by existing ones).

VALIDATION: Branded/nonbranded sums equal total clicks. Trend chart renders.

============================================================
=== PHASE 7: REPORTS ===
============================================================

```
gsc-pull/
├── README.md
├── data/
│   └── gsc.db                 # SQLite (or pointer to Postgres)
├── reports/
│   ├── weekly_summary.md
│   ├── top_movers.csv         # winners + losers
│   ├── click_loss_attribution.md
│   ├── query_page_mismatch.csv
│   ├── branded_vs_nonbranded.csv
│   ├── position_bucket_analysis.csv  # % of clicks from top 3 / 4-10 / 11-20 / 21+
│   └── url_inspection_findings.md
└── cron/
    └── daily_pull.sh
```

Weekly summary structure:

```markdown
# GSC Weekly — {site} — {week}

## TL;DR
- Total clicks: X (+/- Y vs prior week, +/- Z YoY)
- Total impressions: X
- Avg position: X
- Branded share: X%
- Top winner: {query} — {page} (+N clicks)
- Top loser: {query} — {page} (-N clicks)

## Top 5 Winners
{table}

## Top 5 Losers + Attribution
{table with rank-loss / impression-loss / CTR-loss labels}

## Query-Page Mismatches
{N detected — see csv}

## Recommended Actions
{ordered by impact}
```

VALIDATION: Summary fits one screen. Recommended actions reference specific queries + pages.

============================================================
=== SELF-REVIEW ===
============================================================

- **Complete**: API client + schema + cron + 4 analyses + reports?
- **Robust**: Handles 2k/day URL inspection cap? Survives API rate limits?
- **Clean**: SQLite/Postgres choice transparent? CSVs Excel-friendly?
- **GSC-credible**: Would an SEO consultant who lives in GSC daily accept the analyses?

Common gap: forgetting `dataState=final` vs `all` and getting estimated data that shifts next day. Confirm which is used in each query.

============================================================
=== LEARNINGS CAPTURE ===
============================================================

`~/.claude/skills/gsc-pull/LEARNINGS.md`.

============================================================
=== STRICT RULES ===
============================================================

- Never query `dataState="all"` and then declare the data stable. Use `final` for analytical work.
- Never hit URL Inspection > 2,000/day per property — it's a hard cap.
- Never lose history. Start persisting NOW even if the user isn't analyzing yet.
- Never analyze without WoW/MoM/YoY context. Absolute numbers without comparison are vanity.
- Always classify click loss into the four root-cause buckets. "Clicks down" without attribution is useless.
