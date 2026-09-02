---
name: content-cannibalization
description: "Detect content cannibalization on a site — multiple URLs ranking (or impressing) for the same query, splitting click-through, diluting authority, and confusing Google about which URL is canonical for the intent.."
version: "1.0.1"
category: analysis
platforms:
  - CLAUDE_CODE
---

# Content Cannibalization Detector & Resolver

You find cannibalization and recommend the specific fix. Cannibalization is the single most common cause of "we have lots of content but rankings are stuck" — and it's invisible without joining GSC query-level data with the site's page intents.

============================================================
=== PRE-FLIGHT ===
============================================================

- [ ] **GSC data**: from `/gsc-pull` skill (or direct connection).
- [ ] **Page-to-intent map**: for each URL, which target query is it written for? If unknown, derive from H1 + meta description.
- [ ] **Crawl data**: title, H1, canonical, noindex, content embedding (from `/internal-link-graph` if available).
- [ ] **Authority signal**: backlinks per page (from Ahrefs/Majestic if accessible; otherwise GSC referring domain proxy).
- [ ] **Action capacity**: how many redirects / consolidations / canonical edits can the team execute monthly? (Drives prioritization.)

Recovery:
- No backlink data: use internal PageRank from `/internal-link-graph` as authority proxy.
- No intent map: auto-derive via top GSC query per page (with a "MUST_VERIFY" flag on results).

============================================================
=== PHASE 1: CANNIBALIZATION DETECTION ===
============================================================

For each unique query in GSC (filter to impressions ≥ 50 in window):

```python
def detect_cannibalization(gsc_rows, min_impressions=50, position_max=50):
    """
    Returns clusters where a single query has 2+ URLs both within
    position 1-50 with non-trivial impressions.
    """
    by_query = defaultdict(list)
    for row in gsc_rows:
        if row.impressions >= min_impressions and row.position <= position_max:
            by_query[row.query].append(row)
    
    clusters = {}
    for query, rows in by_query.items():
        if len(rows) >= 2:
            clusters[query] = sorted(rows, key=lambda r: -r.clicks)
    return clusters
```

Output `cannibalization_clusters.csv`:

| Query | URL | Impressions | Clicks | Avg Position | CTR | Cluster Size |
|---|---|---|---|---|---|---|
| best CRM | /blog/best-crm | 8400 | 240 | 8.2 | 2.9% | 3 |
| best CRM | /pricing | 1100 | 12 | 22.4 | 1.1% | 3 |
| best CRM | /reviews | 600 | 5 | 31.8 | 0.8% | 3 |

VALIDATION: Detection produces non-zero clusters on any site with > 500 pages and > 100 ranking queries.

============================================================
=== PHASE 2: ROOT-CAUSE CLASSIFICATION ===
============================================================

For each cluster, classify the cannibalization type:

| Class | Signal | Typical fix |
|---|---|---|
| **True duplicate** | Embedding similarity > 0.95 between competing pages | Consolidate, 301 weaker → stronger, remove |
| **Intent overlap** | Same query, different intents (e.g., transactional + informational) | Differentiate H1 / content; canonical NOT same |
| **Template confusion** | Multiple variant/filter pages indexable, same query | Canonicalize to parent; or `noindex` variants |
| **Accidental same H1** | Different topics but same H1 / title | Rewrite the H1 / title of one |
| **Variant page leakage** | UTM / session ID / filter query strings indexed | Set `<link rel="canonical">` to clean URL; robots Disallow query strings |
| **Author overlap** | Same author bio repeated, body content overlaps in intro paragraphs | Update author template to be lighter |

Detection per class:
- **True duplicate**: embedding cosine ≥ 0.95 across competing URLs.
- **Intent overlap**: SERP intent signal (Google AI Overview vs ten blue links vs shopping ads) suggests one canonical intent; multiple pages target different but Google merges.
- **Template confusion**: URL pattern suggests filter/variant (`?color=`, `?sort=`, `/category/page/2/`).
- **Variant leakage**: URL has query string or session ID.

VALIDATION: Each cluster has a class label + confidence (0-1).

============================================================
=== PHASE 3: RESOLUTION RECOMMENDATIONS ===
============================================================

Per cluster, produce one of five resolutions:

**A. Consolidate-and-301** (best for true duplicates):
- Identify "winner" (highest authority + best historical clicks + best target intent fit).
- All losers 301-redirect → winner.
- Merge unique content from losers into winner (don't lose value).
- Update internal links to point to winner.

**B. Canonicalize** (best for variant leakage):
- Set `<link rel="canonical" href="https://example.com/canonical">` on variants.
- Don't 301 (preserve UX for filtered nav).

**C. Differentiate-intent** (best for intent overlap):
- Keep both pages. Rewrite each to target distinct intent.
- Page A → transactional ("buy X"); Page B → informational ("what is X").
- Update internal links to disambiguate.

**D. Noindex-the-weaker** (best for template / pagination):
- `<meta name="robots" content="noindex,follow">` on weaker pages.
- Or use `rel="next/prev"` pagination semantics where applicable.

**E. Update-internal-links-only** (lightest touch, valid when both pages should stay live):
- Reroute internal links so the intended page gets all the link equity.
- Don't change URL structure.

Per cluster, output `resolution_{cluster_id}.md` with:
- Recommended resolution (A-E)
- Reasoning (which signals drove it)
- Exact code/redirects/canonical tags to add
- Internal link updates needed
- Expected click recovery (sum of cluster clicks × consolidation multiplier 1.2-1.8)

VALIDATION: Recommendation per cluster is concrete and tied to evidence.

============================================================
=== PHASE 4: REDIRECT RULES & CANONICAL PATCHES ===
============================================================

Generate platform-specific implementation:

**Nginx**:
```
location = /blog/old-url { return 301 /blog/winner-url; }
```

**Apache (.htaccess)**:
```
RewriteRule ^blog/old-url$ /blog/winner-url [R=301,L]
```

**Next.js (`next.config.js`)**:
```js
async redirects() {
  return [
    { source: '/blog/old-url', destination: '/blog/winner-url', permanent: true },
    ...
  ]
}
```

**Cloudflare Workers** / **Vercel `vercel.json`** / **Netlify `_redirects`**:
```
/blog/old-url  /blog/winner-url  301
```

**WordPress** (Redirection plugin export):
```csv
source,target,type
/blog/old-url,/blog/winner-url,301
```

**Canonical tag patches** for "B. Canonicalize":
```html
<link rel="canonical" href="https://example.com/canonical-url">
```

VALIDATION: Generated redirects parse correctly in their target stack.

============================================================
=== PHASE 5: RECOVERY MODEL ===
============================================================

Estimate post-fix click recovery:

```
Expected clicks per cluster after fix =
  (sum of impressions in cluster) × (CTR at winner's new expected position)

Position lift from consolidation:
  if total cluster clicks > 100 and lift ~ -1 to -3 positions (closer to top)
  use CTR-by-position curve (Google avg: pos 1=27%, pos 2=15%, pos 3=11%, pos 4=8%, pos 5=7%, etc.)
```

For each cluster:
- Current cluster total clicks/week
- Expected clicks/week after fix
- Net gain
- Confidence (high if true duplicate, medium for intent split, low for soft variants)

Aggregate: total expected click gain across all cannibalization fixes. Prioritize highest-gain × lowest-effort first.

VALIDATION: Recovery model uses real CTR-by-position curves, not made-up multipliers.

============================================================
=== PHASE 6: ACTION QUEUE ===
============================================================

Generate `action_queue.md` ordered by impact × inverse effort:

```markdown
# Cannibalization Action Queue — {site}

## P0 — High impact, low effort
1. [Consolidate] "best CRM" cluster: 301 /blog/reviews + /pricing → /blog/best-crm. Expected: +180 clicks/week. Effort: 30 min. Risk: low.

## P1 — High impact, medium effort
2. [Differentiate] "API rate limits" cluster: rewrite /docs/api-limits to focus on technical reference vs /blog/api-rate-limits which keeps tutorial focus. Expected: +90 clicks/week. Effort: 4 hours.

## P2 — Polish
3. [Canonicalize] "/?utm_source=*" variants: add canonical pointing to clean URL. Expected: +5 clicks/week (de-duped indexing). Effort: 1 hour.
```

VALIDATION: Action queue has per-item expected gain + effort.

============================================================
=== SELF-REVIEW ===
============================================================

- **Complete**: Detection + classification + 5 resolution types + redirect patches + recovery model?
- **Robust**: Handles variant leakage with query strings? Avoids over-consolidating (some pairs SHOULD stay separate)?
- **Clean**: Recommendations are platform-specific (Nginx / Next.js / WordPress)?
- **SEO-credible**: Would an Ahrefs power-user accept the analysis as production-ready?

Common gap: recommending 301 on a page that's still gaining traffic. Always check trend before consolidating — growing-but-second-best may overtake.

============================================================
=== LEARNINGS CAPTURE ===
============================================================

`~/.claude/skills/content-cannibalization/LEARNINGS.md`.

============================================================
=== STRICT RULES ===
============================================================

- Never recommend a 301 without first checking that both pages have the same primary intent. Intent splits don't consolidate, they differentiate.
- Never propose a redirect that creates a chain (A→B→C). Always squash to A→C directly.
- Never assume cluster sizes > 2 = always bad. Sometimes Google legitimately surfaces multiple URLs (e.g., subdirectory + a sub-page).
- Always update internal links AFTER 301-ing. Otherwise the redirects hop forever and crawl budget burns.
- Always re-pull GSC after 4-8 weeks to verify recovery model was correct. Refine assumptions over time.
