---
name: merchant-feed
description: Generate and maintain a multi-channel product feed across Google Merchant Center, Meta Catalog (Instagram + Facebook Shops), TikTok Shop, Pinterest Catalogs, Bing Shopping, and Snapchat Catalogs from a single product source of truth (Shopify, BigCommerce, WooCommerce, custom DB). Enforces 2026 platform requirements: Google's new 500×500 image minimum (warnings Apr 14 2026, enforcement Jan 31 2027), title structure that wins matching (Google heavily weights title), required GTIN/MPN/brand triplet, GPC + condition + availability + price/sale_price accuracy, Meta dynamic-ad-eligibility constraints, TikTok's video-asset preference, Pinterest rich pin merchant-verification. Generates: feed file (XML / JSON / TSV per platform spec), validation report (catches disapprovals before submission), title-A/B-test harness, custom_label rotation calendar, weekly feed-audit cron, and disapproval-recovery playbook (48-hour SLA per platform best practice). TRIGGER on "product feed", "Google Shopping feed", "Merchant Center", "Meta catalog", "TikTok Shop", "Pinterest catalog", "Bing Shopping", "feed optimization", "shopping ads", "Performance Max feed", "Advantage+ Shopping", "DPA", "DSA", "catalog disapproval".
version: "1.0.0"
category: analysis
platforms:
  - CLAUDE_CODE
---

# Multi-Channel Merchant Feed Pipeline

You build a feed-as-product-data discipline. In 2026, feed management is less about producing "a feed" and more about running a data product: continuously modifying attributes, enriching missing fields, validating quality, and tying changes to performance.

============================================================
=== PRE-FLIGHT ===
============================================================

- [ ] **Product source of truth**: Shopify, BigCommerce, WooCommerce, Magento, custom DB, ERP (NetSuite, SAP).
- [ ] **Target channels**: which of GMC / Meta / TikTok Shop / Pinterest / Bing / Snap?
- [ ] **Catalog size**: < 500 SKUs → single feed file is fine. 5k+ SKUs → use Content API / Commerce API for incremental updates.
- [ ] **Product types**: physical goods, digital, services, software, age-restricted (alcohol/tobacco/cannabis — extra scrutiny). Subscription products require additional Google attributes (`subscription_cost`).
- [ ] **Brand assets**: high-res images, GTINs, MPNs. Without GTIN, disapprovals climb 30-50%.
- [ ] **Localization**: feed per country / language? Currency? Local tax/shipping?

Recovery:

- Missing GTINs: flag SKUs with `identifier_exists=false` (Google allows this for niche brands) but expect lower performance.
- Image quality issues: route through a transform CDN (Cloudinary, imgix, Vercel Image Optimization) to auto-meet 500×500 minimum + AVIF/WebP output.

============================================================
=== PHASE 1: CANONICAL PRODUCT SCHEMA ===
============================================================

Build the single source of truth. Every channel feed projects from this:

```json
{
  "id": "SKU-12345",
  "title": "...", // primary attribute for Google match
  "description": "...",
  "link": "https://...",
  "mobile_link": "https://...", // optional but recommended
  "image_link": "https://.../primary.jpg", // ≥ 500×500 (2026 requirement)
  "additional_image_link": ["...", "..."], // up to 10
  "availability": "in_stock|out_of_stock|preorder|backorder",
  "availability_date": "2026-08-15", // if preorder
  "price": "29.99 USD",
  "sale_price": "24.99 USD",
  "sale_price_effective_date": "2026-05-23T00:00-07:00/2026-06-30T23:59-07:00",
  "brand": "...",
  "gtin": "00012345678905",
  "mpn": "...",
  "identifier_exists": true,
  "condition": "new|refurbished|used",
  "google_product_category": "Apparel & Accessories > Clothing > Shirts & Tops",
  "product_type": "Mens > Shirts > T-Shirts",
  "color": "navy",
  "size": "L",
  "material": "100% cotton",
  "gender": "male|female|unisex",
  "age_group": "adult|kids|toddler|infant|newborn",
  "item_group_id": "TSHIRT-001", // for variant grouping
  "shipping": [{ "country": "US", "service": "Standard", "price": "4.99 USD" }],
  "tax": [{ "country": "US", "region": "CA", "rate": 9.0, "tax_ship": true }],
  "custom_label_0": "high_margin", // for ad bidding strategy
  "custom_label_1": "summer_collection",
  "custom_label_2": "best_seller",
  "custom_label_3": "new_arrival",
  "custom_label_4": "low_inventory",
  "video": "https://.../product.mp4" // critical for TikTok Shop
}
```

Persist as `products.json` with versioning (so feed history is auditable).

VALIDATION: 100% of products have id, title, description, link, image_link, availability, price, brand. ≥ 90% have GTIN.

============================================================
=== PHASE 2: TITLE OPTIMIZATION ===
============================================================

Title is the highest-leverage attribute for Google matching. Use this structure:

`[Brand] [Product Type] [Key Attribute] [Variant] [Size/Quantity]`

Examples:

- ❌ "Awesome T-Shirt"
- ✅ "Nike Dri-FIT Men's Running T-Shirt — Navy, Large"
- ✅ "Apple AirPods Pro (2nd Gen) — USB-C, Active Noise Cancellation"

Title cap: 150 chars (Google), 65 chars displayed in shopping results. Front-load the most important info.

Maintain a per-product title A/B test queue: rotate one new variant per category per month, measure CTR + ROAS at the keyword level via Search Terms Report.

VALIDATION: Median title length 60-120 chars. No "AAA-promo" stuffing or all-caps.

============================================================
=== PHASE 3: PER-CHANNEL FEED PROJECTION ===
============================================================

Project the canonical product into each channel's format:

**Google Merchant Center** (XML or TSV):

- Full canonical schema. Required: id, title, description, link, image_link, availability, price, brand, gtin (if available), condition, google_product_category.
- Sale price requires `sale_price_effective_date` to qualify as a deal.
- Feeds via Content API for Shopping (real-time) or scheduled fetch (8-24 hour cadence).

**Meta Catalog** (CSV or Catalog Batch API):

- Similar fields; uses `availability` (lowercase: in stock / out of stock).
- `inventory` (numeric count) for ads with low-stock urgency.
- Additional Meta-specific: `applinks` for app-deep-link, `rich_text_description` for Shops.
- `home_listing` for real estate variant, `flight` for travel variant.

**TikTok Shop** (TSV or Commerce API):

- Video required for top placements. Map to `tiktok_video_url` field.
- Stricter content moderation: no medical claims, no age-restricted products in many regions.
- Stricter image requirements (white background preferred for product imagery).

**Pinterest Catalogs**:

- Image quality matters most (Pinterest is image-first).
- `additional_image_link` (5+) outperforms single-image listings.
- Pin link landing must match feed link exactly.

**Bing Shopping** (close to GMC format):

- Reuses Google product feed mostly; small differences in attribute names.

**Snap Catalogs**:

- Use Snap's tags (`age_group`, `gender`) for AR try-on eligibility.

Generate per-channel projection in `feeds/{channel}/{date}.{ext}`.

VALIDATION: Each channel feed validates against the platform's spec (use vendor schema validators / spec linters).

============================================================
=== PHASE 4: VALIDATION & DISAPPROVAL PREVENTION ===
============================================================

Before submission, run pre-flight checks:

| Check                                | Failure mode                                            | Fix                                 |
| ------------------------------------ | ------------------------------------------------------- | ----------------------------------- |
| Image ≥ 500×500 (Google 2026)        | Disapproval warning Apr→reject Jan 2027                 | Auto-upscale via CDN transform      |
| Title length 30-150                  | Truncation in SERP                                      | Tighten to 60-90 chars              |
| Description ≥ 30 words               | Low relevance score                                     | Auto-augment with attribute join    |
| Price > 0 and matches landing page   | Price mismatch disapproval                              | Verify scrape of landing page price |
| GTIN valid checksum                  | Invalid GTIN disapproval                                | Validate UPC/EAN/ISBN checksum      |
| Availability matches landing         | "Out of stock" mismatch                                 | Scrape landing inventory status     |
| Brand present                        | Limited performance                                     | Default to store brand if missing   |
| Required GPC category for restricted | Disapproval (apparel needs color+size+age_group+gender) | Enforce per category rules          |
| Restricted content                   | Disapproval (e.g., drug-related claims)                 | Run vocab filter                    |
| Landing page returns 200             | Broken landing disapproval                              | Crawl + verify before submit        |

Output `feed_validation_{date}.md` with per-SKU issues.

VALIDATION: Pre-submission validation catches > 95% of issues that would otherwise be caught downstream.

============================================================
=== PHASE 5: WEEKLY FEED AUDIT CRON ===
============================================================

Schedule a weekly task (Mondays, post-weekend sales data):

1. Fetch disapproval reports from GMC, Meta Commerce Manager, TikTok Shop, Pinterest.
2. Map each disapproval to the underlying canonical product issue.
3. Auto-fix the deterministic ones (image upscale, title tightening, category mapping).
4. Surface non-deterministic ones (policy violations, restricted content claims) for human review.
5. Track 48-hour SLA: every new disapproval must be addressed within 48h.
6. Track custom_label rotation: quarterly review of which custom labels are working (e.g., high-margin label producing top ROAS).

Generate `weekly_audit_{date}.md` digest.

VALIDATION: SLA met for ≥ 95% of disapprovals.

============================================================
=== PHASE 6: PERFORMANCE FEEDBACK LOOP ===
============================================================

Tie feed changes back to performance:

- Pull `impressions`, `clicks`, `conversions`, `cost`, `revenue` per SKU per channel.
- Compute: CTR, conversion rate, ROAS, CPA.
- Flag underperformers (bottom 20% by ROAS) for title test or image refresh.
- Flag overperformers (top 5%) for custom_label tagging → push to higher-priority campaigns.

VALIDATION: Performance attribution joins canonical product ID to channel SKU ID without drift.

============================================================
=== PHASE 7: OUTPUT PACKAGE ===
============================================================

```
merchant-feed/
├── README.md
├── products.json                # canonical
├── feeds/
│   ├── google/products.xml
│   ├── meta/products.csv
│   ├── tiktok/products.tsv
│   ├── pinterest/products.csv
│   ├── bing/products.xml
│   └── snap/products.csv
├── validation/
│   └── feed_validation_{date}.md
├── audit/
│   └── weekly_audit_{date}.md
├── tests/
│   └── title_ab_tests.csv       # active title variants per SKU
└── perf/
    └── sku_performance_{date}.csv
```

VALIDATION: Every channel feed validates and submits without disapproval.

============================================================
=== SELF-REVIEW ===
============================================================

- **Complete**: All 7 phases run. Canonical schema → 6 channel projections + validation + audit + perf loop.
- **Robust**: Handles missing GTINs, image upscaling, channel-specific edge cases?
- **Clean**: Disapproval SLA tracking, no feed drift between channels?
- **Ecommerce-credible**: Would a feed manager at a $100k+/month Shopping spend accept the system?

Common gap: image upscale missing → silent quality degradation. Verify CDN transform pipeline.

============================================================
=== LEARNINGS CAPTURE ===
============================================================

`~/.claude/skills/merchant-feed/LEARNINGS.md`.

============================================================
=== STRICT RULES ===
============================================================

- Never submit images below 500×500 for Google after Jan 2027. Auto-upscale or omit.
- Never silently drop attributes a channel requires. Surface in validation report.
- Never let disapprovals sit > 48 hours. Compound spend loss.
- Never reuse one feed across channels without per-channel projection. Each platform has unique requirements.
- Always preserve canonical → channel ID mapping for performance attribution.
