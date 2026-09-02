---
name: pdp-builder
description: "Generate a production-grade Product Detail Page (PDP) optimized for the 2026 conversion benchmarks — 4-8% target vs 1.5-3% average. Triggers: \"product page\", \"PDP\", \"product detail page\", \"Shopify product page\", \"ecommerce conversion\"."
version: "1.0.1"
category: analysis
platforms:
  - CLAUDE_CODE
---

# Product Detail Page (PDP) Generator

You generate a complete, conversion-optimized PDP. The 2026 benchmark is clear: average sites convert at 1.5-3%, top performers at 4-8% — a 2-3× gap explained by measurable elements, not magic. Your job is to ship those elements.

The single biggest gap-closer: image quality + social proof + page speed. Walmart found each 1-second-faster page delivered +2% conversion. Page loading in 2.4s converts at 1.9%; 5.7s converts at 0.6%.

============================================================
=== PRE-FLIGHT ===
============================================================

Verify before building:

- [ ] **Platform identified.** Shopify (Liquid / Hydrogen), Next.js Commerce, BigCommerce Catalyst, WooCommerce, custom React/Vue/Svelte.
- [ ] **Product data source.** Shopify Admin API, Stripe Products, BigCommerce Storefront API, CSV import, headless CMS (Contentful/Sanity/Strapi).
- [ ] **Image assets.** Minimum: 1 hero + 3 alt angles + 1 lifestyle. Ideal: + product video (autoplay muted on desktop, click-to-play mobile).
- [ ] **Reviews data.** Yotpo, Judge.me, Loox, Stamped, Trustpilot, or first-party. Without reviews, social proof block falls back to "trust badges" only — significantly weaker.
- [ ] **Brand tokens.** Colors, fonts, button radius. Without these, generated CSS uses neutral defaults.

Recovery:

- If image assets are weak (single product shot only), output the PDP with a "MISSING:" placeholder per slot and add a TODO to capture alt angles, lifestyle, and video — flag the conversion impact clearly.
- If platform is unknown, default to Next.js + Tailwind + headless commerce-agnostic structure that maps to any backend.

============================================================
=== PHASE 1: VISUAL HIERARCHY (F-PATTERN) ===
============================================================

Eye-tracking shows users scan PDPs in F-pattern. The viewport-above-fold zones (in priority order):

1. **Top-left**: Hero image (largest, sharpest, fills 50%+ of mobile width).
2. **Top-right**: Title + price + reviews snippet (X stars, N reviews).
3. **Second row left**: Variant selectors (size, color) + add-to-cart CTA.
4. **Below fold**: Detailed description, full reviews, related products, FAQ.

Generate the layout as semantic HTML with proper landmarks (`<main>`, `<section>`, `<aside>`). Mobile-first CSS (default styles for ≤768px, media queries for tablet/desktop). Touch targets ≥44px.

VALIDATION: Lighthouse mobile Best Practices ≥ 90. CLS < 0.1 (every image has explicit width/height). LCP image preloaded.

============================================================
=== PHASE 2: IMAGE PIPELINE ===
============================================================

93% of consumers cite visual appearance as the top purchase factor. The image system MUST:

- **Multiple angles**: hero + 3-4 alternate angles + lifestyle context.
- **AVIF first, WebP fallback, JPG legacy** with `<picture><source type="image/avif">...`.
- **Responsive `srcset`** at 320w/640w/1024w/1600w/2560w.
- **Explicit width/height** to reserve space (CLS prevention).
- **Hero image preloaded** in `<head>`: `<link rel="preload" as="image" href="..." imagesrcset="..." imagesizes="...">`.
- **Zoom on hover/tap** (lightbox or in-place pan).
- **Video** as `<video autoplay muted loop playsinline poster>` on desktop, click-to-play on mobile (battery).
- **CDN with image transformation** (Cloudinary, imgix, Shopify CDN, Vercel Image Optimization).

VALIDATION: Hero image LCP < 2.5s on Slow 4G. Image markup passes Lighthouse Image best practices.

============================================================
=== PHASE 3: SOCIAL PROOF BLOCK ===
============================================================

Products with 5+ reviews convert 270% better. Build the proof block as:

1. **Aggregate rating** (X.X stars, Y reviews) — top-right of hero, schema.org AggregateRating.
2. **Review excerpts** — 3 verified reviews above the fold (rotate top-rated).
3. **Photo reviews** — UGC from buyers; massively trust-boosting.
4. **Trust signals** — returns policy, shipping speed, security badges, payment methods, "X people bought today" (only if true — fake urgency erodes trust).
5. **Press / endorsements** — if applicable, "As seen in" logo strip with `nofollow` outbound links.
6. **Q&A section** — buyer questions + answers (or store-curated FAQ).

VALIDATION: Above-fold area on mobile shows at least one social proof element. AggregateRating schema validates.

============================================================
=== PHASE 4: CTA & VARIANT SELECTOR ===
============================================================

Critical CTAs:

- **Primary**: "Add to cart" — high contrast, ≥48px tall, full-width on mobile, sticky on scroll (mobile bottom bar).
- **Secondary**: "Buy now" → checkout (Shop Pay / Apple Pay / Google Pay express).
- **Tertiary**: Save / Wishlist (heart icon).

Variant selectors:

- Color: swatches with `aria-label`, current-state styling, "out of stock" greyed not hidden.
- Size: pills with size guide modal link.
- Quantity: stepper (- / number / +), default 1.

Inventory urgency (only if accurate):

- "Only N left" message at quantities ≤ 5.
- "Selling fast" pill if velocity > X/day.

VALIDATION: CTA is keyboard-focusable, has visible focus ring, `aria-disabled` when out-of-stock.

============================================================
=== PHASE 5: SCHEMA.ORG MARKUP ===
============================================================

Generate JSON-LD for the product:

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "...",
  "image": ["..."],
  "description": "...",
  "sku": "...",
  "brand": { "@type": "Brand", "name": "..." },
  "offers": {
    "@type": "Offer",
    "url": "...",
    "priceCurrency": "USD",
    "price": 49.99,
    "availability": "https://schema.org/InStock",
    "itemCondition": "https://schema.org/NewCondition",
    "shippingDetails": { "@type": "OfferShippingDetails", ... },
    "hasMerchantReturnPolicy": { "@type": "MerchantReturnPolicy", ... }
  },
  "aggregateRating": { "@type": "AggregateRating", "ratingValue": 4.7, "reviewCount": 128 },
  "review": [ ... top 3 reviews ... ]
}
```

Include `shippingDetails` and `hasMerchantReturnPolicy` — these unlock Google Shopping rich results in 2026.

VALIDATION: Passes Google Rich Results Test for Product. AggregateRating has a real value (not 0/0).

============================================================
=== PHASE 6: CRO EXPERIMENTATION HARNESS ===
============================================================

Top performers run disciplined experiments and read the data honestly. Generate:

- **Variant config file** (`pdp.experiments.json`) compatible with Optimizely, VWO, Statsig, GrowthBook, or LaunchDarkly.
- **At minimum, three experiments scaffolded**:
  1. Hero image: lifestyle vs studio
  2. CTA copy: "Add to cart" vs "Add to bag" vs "Buy now"
  3. Social proof position: above-fold vs below-fold
- **Sample size calculator** stub: takes baseline CR + MDE + α=0.05 + power=0.8, returns required N per variant. Refuse to call experiments early.
- **Event tracking spec**: `pdp_view`, `pdp_image_zoom`, `pdp_variant_select`, `pdp_add_to_cart`, `pdp_buy_now`, `pdp_exit`.

VALIDATION: Sample-size calculator does the math (not just emits a TODO). Experiment config maps to user's chosen platform.

============================================================
=== PHASE 7: OUTPUT PACKAGE ===
============================================================

```
pdp/
├── README.md                    # Where to drop files in each platform
├── components/
│   ├── ProductHero.{tsx|liquid|vue}
│   ├── ProductGallery.{tsx|liquid|vue}
│   ├── ProductVariants.{tsx|liquid|vue}
│   ├── ProductSocialProof.{tsx|liquid|vue}
│   ├── ProductSchema.{tsx|liquid|vue}
│   └── ProductCTA.{tsx|liquid|vue}
├── styles/
│   └── pdp.css                  # Mobile-first responsive
├── schema/
│   └── product-jsonld.example.json
├── experiments/
│   └── pdp.experiments.json
├── tracking/
│   └── events.spec.md
└── perf/
    └── lighthouse-budget.json   # CI gate: LCP<2.5s, INP<200ms, CLS<0.1
```

============================================================
=== SELF-REVIEW ===
============================================================

Score 1–5:

- **Complete**: All 7 phases delivered? Schema validates? Mobile-first?
- **Robust**: Handles missing images / reviews gracefully? Sticky CTA on mobile?
- **Clean**: No inline styles, no hardcoded colors outside tokens, no console.log?
- **Conversion-credible**: Would a CRO consultant recognize this as 2026-current? F-pattern hierarchy + social proof above fold + schema + perf budget all present?

Most common gap: forgetting LCP image preload → hero takes 4s on Slow 4G → conversion craters. Verify the `<link rel="preload">` is in the head, not just `<img loading="eager">`.

============================================================
=== LEARNINGS CAPTURE ===
============================================================

Append to `~/.claude/skills/pdp-builder/LEARNINGS.md`:

## <YYYY-MM-DD> — <platform, vertical>

- **What worked:** <pattern that produced clean output>
- **What was awkward:** <retry/manual fix needed>
- **Suggested patch:** <concrete improvement>
- **Verdict:** [Smooth / Minor friction / Major friction]

============================================================
=== STRICT RULES ===
============================================================

- Never skip image preload. LCP > 2.5s tanks conversion regardless of other quality.
- Never fabricate review counts. AggregateRating must be real or absent.
- Never use fake urgency ("only 2 left" when there are 50). FTC enforces this and shoppers detect it.
- Never block the CTA with a full-screen popup. Exit intent OK, blocking on load not.
- Mobile-first or fail. 73% of traffic, 58% of purchases.
