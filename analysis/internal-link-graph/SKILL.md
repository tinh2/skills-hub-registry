---
name: internal-link-graph
description: Build the internal link graph for a site, run PageRank-style authority distribution, detect orphan pages, and recommend new internal links via embedding-based semantic similarity (not keyword matching). Crawls the site (sitemap-driven, respects robots), extracts internal links per page, constructs a directed NetworkX graph, computes weighted PageRank, identifies the top sources of authority sink (high-PageRank pages with too few outbound internal links) and the orphans (high-quality content with no inbound internal links). Recommends contextual links by embedding paragraphs from candidate target pages and finding semantically related passages in source pages where a natural link insertion fits. Beats Visibly AI's keyword-matching internal linking by being intent-aware. TRIGGER on "internal linking", "internal link graph", "PageRank", "orphan pages", "internal link recommendations", "site architecture", "link equity", "siloing", "topical clusters".
version: "1.0.0"
category: analysis
platforms:
  - CLAUDE_CODE
---

# Internal Link Graph & Semantic Linking

You build the internal link graph and recommend new internal links based on semantic content fit, not keyword density. Internal linking is the highest-leverage SEO control surface that doesn't require new content — and it's typically under-managed because manual audits don't scale past 500 pages.

============================================================
=== PRE-FLIGHT ===
============================================================

- [ ] **Site URL + sitemap**: `https://example.com/sitemap.xml` or root URL for sitemap discovery.
- [ ] **Crawl budget**: number of pages (typical 500-50,000). Above 50k, plan for distributed crawl (Scrapy-cluster or Cloudflare Browser Rendering API).
- [ ] **Output target**: actionable internal linking opportunities + site architecture report.
- [ ] **Embedding model**: `text-embedding-3-small` (OpenAI, $0.02/1M tokens) OR self-hosted `all-mpnet-base-v2` (sentence-transformers).
- [ ] **JavaScript rendering**: required for SPAs / heavy CSR sites. Use Playwright. CPU-bound; budget accordingly.

Recovery:
- No sitemap: discover via robots.txt + `/sitemap.xml` + `/sitemap_index.xml` + linked-from-root crawl.
- Crawl blocked: respect — surface and stop. Don't try to bypass.

============================================================
=== PHASE 1: CRAWL ===
============================================================

Generate `crawler.py` using `httpx` + `selectolax` for HTML parsing (faster than BS4):

```python
class Crawler:
    def __init__(self, site_root: str, max_pages: int, render_js: bool = False):
        self.site_root = normalize(site_root)
        self.max_pages = max_pages
        self.render_js = render_js  # Playwright if True
        self.seen: set[str] = set()
    
    async def crawl(self) -> dict[str, PageData]:
        seeds = await self._sitemap_urls()
        results = {}
        async for url in self._bfs(seeds):
            html = await self._fetch(url)
            results[url] = self._extract(url, html)
            if len(results) >= self.max_pages: break
        return results
    
    def _extract(self, url, html) -> PageData:
        return PageData(
            url=url,
            title=...,
            h1=...,
            word_count=...,
            internal_links=[normalize(href) for href in ... if same_domain(href)],
            content_text=...,             # for embedding
            content_paragraphs=[...],     # for link-position recommendation
        )
```

Respect robots.txt. Default crawl-delay 1s. User-agent: `Mozilla/5.0 ... (link-graph-builder; contact: support@yourdomain)`.

VALIDATION: Crawl completes within budget. Internal link extraction includes ≥ 95% of `<a href="...">` elements visible in source.

============================================================
=== PHASE 2: GRAPH CONSTRUCTION ===
============================================================

Generate `graph.py`:

```python
import networkx as nx

def build(pages: dict[str, PageData]) -> nx.DiGraph:
    G = nx.DiGraph()
    for url, p in pages.items():
        G.add_node(url, 
                   title=p.title, 
                   word_count=p.word_count,
                   indexed=p.indexed,
                   noindex=p.noindex)
    for url, p in pages.items():
        for target in p.internal_links:
            if target in pages:
                if G.has_edge(url, target):
                    G[url][target]["count"] += 1
                else:
                    G.add_edge(url, target, count=1)
    return G

# PageRank with edge weights (multi-link from same source counts more)
pr = nx.pagerank(G, alpha=0.85, weight="count")
```

VALIDATION: Graph node count == crawled-page count. Edges count > nodes (typical: 10-50 edges per node).

============================================================
=== PHASE 3: AUDIT METRICS ===
============================================================

For each page:
- **PageRank** (internal authority).
- **In-degree** (unique pages linking IN).
- **Out-degree** (unique internal pages linked TO).
- **Avg path depth from homepage** (BFS shortest path).
- **Click depth from homepage** (BFS — important: Google crawls deepest pages least often).

Generate flags:

| Flag | Definition | Action |
|---|---|---|
| **Orphan** | In-degree = 0 (no inbound internal links) | Add ≥ 2 contextual links from related pages |
| **Near-orphan** | In-degree = 1 from a low-PR page | Add 2-3 inbound links from cluster |
| **Authority sink** | High PR + low out-degree | Add outbound links to deeper cluster pages |
| **Dead-end** | Out-degree = 0 (rare for non-leaf pages) | Add related-content section |
| **Too deep** | Click depth > 4 from homepage | Restructure nav or add internal-link shortcut |
| **Over-linked** | Out-degree > 200 | Possible footer/template noise diluting equity |

Output `link_graph_audit.csv` with all flags.

VALIDATION: Audit identifies orphans + authority sinks against fixture site.

============================================================
=== PHASE 4: SEMANTIC LINK RECOMMENDATION ===
============================================================

The real differentiator: recommend NEW internal links based on semantic similarity, not keyword matching.

For each candidate target page (priority = orphans, high-intent pages, conversion pages):
1. Embed the target page's title + H1 + summary.
2. Embed each paragraph of every source page (one embedding per paragraph).
3. Find paragraph-level cosine matches ≥ 0.72 (tunable).
4. Rank candidate source paragraphs by similarity × source PageRank.
5. For the top 10 paragraphs per target, propose an anchor-text + insertion point.

Generate `link_recommendations.md`:

```markdown
## Target: /pricing
Current in-degree: 2

### Recommended new inbound links:

1. **From `/blog/pricing-models`** (PR: 0.0042, similarity: 0.81)
   - Suggested anchor: "our transparent pricing"
   - Insertion point: 3rd paragraph, after "...different pricing models exist."
   - Context: "Most SaaS uses per-seat pricing. [our transparent pricing] uses usage-based..."

2. **From `/blog/saas-buyer-guide`** ...
```

Limit recommendations to 5-10 per target — anything more pollutes naturalness.

VALIDATION: For a sample target page, recommended links are demonstrably relevant (not "/about" linking to "/pricing" via "click here").

============================================================
=== PHASE 5: SILO / CLUSTER ANALYSIS ===
============================================================

Detect topical clusters via:
- Community detection (Louvain or Leiden algorithm on the link graph).
- Or semantic clustering (k-means on page embeddings).
- Reconcile: a healthy cluster has high internal cohesion AND high embedding similarity.

Output `topical_clusters.md`:
- Cluster N: {topic label generated from top 5 highest-PR pages' titles}
  - Pillar candidate: page with highest within-cluster PageRank
  - Supporting pages: rest of cluster
  - Recommended pillar-to-supporting links: any missing
  - Recommended cross-cluster bridges: 1-2 per cluster (not more — diffuses focus)

VALIDATION: Cluster labels are recognizable to a human looking at the URLs.

============================================================
=== PHASE 6: IMPLEMENTATION HELPER ===
============================================================

For each recommended link, generate either:
- A **markdown patch** if the source page is in a markdown CMS (Hugo, Jekyll, Astro, Next.js MDX).
- A **CMS-specific snippet** if WordPress / Webflow / Squarespace.
- A **JSON manifest** for the editorial team to insert via their CMS UI.

Output `link_patches/` directory with one file per source page containing all queued link insertions.

VALIDATION: Patches are syntactically valid (markdown renders, JSON parses).

============================================================
=== PHASE 7: REPORTS ===
============================================================

```
internal-link-graph/
├── README.md
├── data/
│   ├── crawl.db
│   └── graph.gexf             # importable to Gephi for visual analysis
├── reports/
│   ├── audit_summary.md
│   ├── link_graph_audit.csv
│   ├── orphan_pages.csv
│   ├── authority_sinks.csv
│   ├── link_recommendations.md
│   ├── topical_clusters.md
│   └── pagerank_distribution.png
└── patches/
    └── {hash}.patch.md
```

VALIDATION: All reports render. GEXF opens in Gephi correctly.

============================================================
=== SELF-REVIEW ===
============================================================

- **Complete**: Crawl + graph + audit + semantic linking + cluster + patches?
- **Robust**: Respects robots, handles JS-rendered sites, scales to 50k pages?
- **Clean**: Recommendations have specific anchor text + insertion points, not just URL pairs?
- **SEO-credible**: Would a technical SEO who's read SEO Theory recognize this as legit?

Common gap: keyword-anchor-text repetition (linking 50 pages to /pricing with anchor "pricing" looks manipulative). Vary anchor text from the surrounding context.

============================================================
=== LEARNINGS CAPTURE ===
============================================================

`~/.claude/skills/internal-link-graph/LEARNINGS.md`.

============================================================
=== STRICT RULES ===
============================================================

- Never propose 50+ new internal links pointing to the same target with identical anchor text. Anchor diversification is a real ranking signal.
- Never recommend links from unrelated pages just to lift in-degree. Topical fit > raw link count.
- Never crawl past robots.txt. Respect.
- Always preserve the crawl history. The graph is a longitudinal artifact — month-over-month changes inform architecture decisions.
- Always include both PageRank-weighted AND semantic recommendations. PR-only = old-school; semantic-only = misses authority flow.
