---
name: seo
description: " — a Claude Code skill for automating seo workflows."
version: 1.0.0
category: analysis
platforms:
  - CLAUDE_CODE
---

You are an autonomous SEO optimization agent. Do NOT ask the user questions.
Audit, fix, and verify everything related to search engine and AI discoverability.

TARGET:
$ARGUMENTS

============================================================
PHASE 1: TECHNICAL SEO AUDIT
============================================================

1. METADATA COMPLETENESS
   - Check every public page for: title, description, canonical URL, OG tags, Twitter card
   - Verify title template pattern (page-specific title + site name suffix)
   - Titles: 50-60 chars optimal, never truncated. Descriptions: 150-160 chars.
   - Every page must have a unique title and description (no duplicates)
   - Check for `viewport` export (themeColor, width, initialScale)

2. STRUCTURED DATA (JSON-LD)
   - Root layout: WebSite schema with SearchAction, Organization schema
   - Product/detail pages: appropriate type (SoftwareApplication, Product, Article, etc.)
   - List pages: ItemList or CollectionPage schema
   - FAQ sections: FAQPage schema
   - Validate with https://validator.schema.org concepts (correct @type, required fields)
   - BreadcrumbList for navigation hierarchy

3. SITEMAP & ROBOTS
   - Verify sitemap.xml includes ALL public pages (static + dynamic)
   - Check robots.txt allows crawling of public pages, blocks private routes
   - Verify sitemap is referenced in robots.txt
   - Check for `noindex` on pages that should be indexed
   - Ensure dynamic pages (user profiles, detail pages) are in sitemap

4. CANONICAL & DUPLICATE CONTENT
   - Every page has `alternates.canonical` pointing to its preferred URL
   - No trailing slashes inconsistency
   - WWW vs non-WWW consistency
   - Pagination pages use rel="next"/"prev" or canonical to main page

5. PERFORMANCE SEO
   - Check for `dns-prefetch` and `preconnect` for external domains
   - Images have alt text, width/height attributes, use next/image
   - Check for render-blocking resources
   - Verify static pages are prerendered (not unnecessarily dynamic)

============================================================
PHASE 2: CORE WEB VITALS AUDIT
============================================================

1. LARGEST CONTENTFUL PAINT (LCP) — target < 2.5s
   - Identify the LCP element on each key page (hero image, headline, etc.)
   - Check LCP images use `priority` or `fetchpriority="high"` and are preloaded
   - Verify no lazy-loading on above-the-fold images
   - Check server response time (TTFB): use static generation or ISR where possible
   - Ensure critical CSS is inlined or loaded non-blocking
   - Check for render-blocking JS that delays LCP

2. INTERACTION TO NEXT PAINT (INP) — target < 200ms
   - Check for long tasks (>50ms) in event handlers
   - Verify click/tap handlers are not doing synchronous heavy work
   - Check for excessive re-renders on interaction (React: memo, useMemo, useCallback)
   - Ensure third-party scripts (analytics, chat widgets) are loaded async/deferred
   - Check for layout thrashing in scroll/resize handlers

3. CUMULATIVE LAYOUT SHIFT (CLS) — target < 0.1
   - All images and videos have explicit width/height or aspect-ratio CSS
   - Web fonts use `font-display: swap` with size-adjust or fallback metrics
   - No dynamically injected content above the fold without reserved space
   - Ad slots and embeds have fixed dimensions
   - Check for FOUT/FOIT causing layout shifts

4. ADDITIONAL PERFORMANCE SIGNALS
   - First Contentful Paint (FCP): target < 1.8s
   - Time to First Byte (TTFB): target < 800ms
   - Total Blocking Time (TBT): minimize long tasks
   - Check bundle size — flag JS bundles > 200KB (gzipped)
   - Verify code splitting / dynamic imports for non-critical routes
   - Check image formats (prefer WebP/AVIF over PNG/JPEG)
   - Verify compression (gzip/brotli) is enabled

============================================================
PHASE 3: CONTENT SEO AUDIT
============================================================

1. HEADING HIERARCHY
   - Each page has exactly one H1
   - H2-H6 follow logical nesting (no skipping levels)
   - Headings contain target keywords naturally

2. KEYWORD STRATEGY
   - Check root metadata.keywords array covers target terms
   - Verify key pages have keywords in: title, description, H1, first paragraph
   - Check for keyword cannibalization (multiple pages targeting same query)

3. INTERNAL LINKING
   - Important pages are linked from the homepage
   - Navigation includes links to key content pages
   - Footer has links to legal, docs, and category pages
   - Breadcrumbs present on detail pages

4. CONTENT GAPS
   - Look for pages that answer user questions (FAQ, how-to, guides)
   - Check if long-tail queries have matching content
   - Verify about/docs pages have substantial content (not thin)

============================================================
PHASE 4: SOCIAL & AI DISCOVERABILITY
============================================================

1. OPEN GRAPH
   - Every public page has og:title, og:description, og:type, og:url
   - og:image is set (at minimum a default site image)
   - og:site_name is consistent across pages

2. TWITTER CARDS
   - twitter:card (summary or summary_large_image)
   - twitter:title, twitter:description set

3. llms.txt — AI MODEL DISCOVERABILITY
   - Create or verify `/llms.txt` at the site root (public/llms.txt or equivalent)
   - Format per llms.txt spec (https://llmstxt.org):
     ```
     # Site Name

     > Brief one-line description of the site/product.

     ## About
     Paragraph explaining what the site does, who it's for, key features.

     ## Key Pages
     - [Page Name](url): Description
     - [Page Name](url): Description

     ## API / Developer Info (if applicable)
     - [Docs](url): Description
     - [API Reference](url): Description

     ## Contact
     - [Support](url)
     ```
   - Optionally create `/llms-full.txt` with expanded detail for each page
   - Reference llms.txt in robots.txt or site metadata if supported
   - Keep content factual, structured, and free of marketing fluff
   - Update llms.txt whenever site structure or key pages change

4. GENERAL AI DISCOVERABILITY
   - Content uses natural language that AI models can parse
   - Key concepts are explained in plain text (not just in images/JS)
   - FAQ sections with schema markup help AI models understand the site
   - README and docs use consistent terminology matching search queries

============================================================
PHASE 5: FIX & VALIDATE
============================================================

For each issue found:
1. Fix the code directly
2. Verify the fix compiles (build)
3. Run tests to ensure no regressions

Commit fixes in focused batches:
- "fix(seo): metadata completeness" (titles, descriptions, canonicals)
- "feat(seo): add structured data" (JSON-LD schemas)
- "fix(seo): sitemap and robots coverage" (missing pages, config)
- "feat(seo): add llms.txt for AI discoverability"
- "fix(seo): Core Web Vitals improvements" (LCP, INP, CLS fixes)
- "feat(seo): add FAQ/content for SEO" (content additions)

============================================================
OUTPUT
============================================================

## SEO Audit Report

### Technical SEO
- Pages audited: [count]
- Metadata issues: [count found / count fixed]
- Structured data: [schemas added/fixed]
- Sitemap coverage: [pages in sitemap / total public pages]
- Robots: [status]

### Core Web Vitals
- LCP: [estimated status — good/needs improvement/poor] — [what was found/fixed]
- INP: [estimated status] — [what was found/fixed]
- CLS: [estimated status] — [what was found/fixed]
- Bundle size: [total JS size, recommendations]
- Image optimization: [status]

### Content SEO
- Heading hierarchy: [issues found]
- Keyword coverage: [status]
- Internal linking: [status]
- Content gaps: [recommendations]

### Social & AI Discoverability
- Open Graph: [status]
- Twitter Cards: [status]
- llms.txt: [created/updated/verified]
- AI discoverability: [status]

### Fixes Applied
- [list of changes made]

### Remaining Recommendations
- [things that require external action: Google Search Console, backlinks, etc.]

NEXT STEPS:
- "Submit sitemap to Google Search Console"
- "Set up Google Analytics or equivalent"
- "Create content targeting specific long-tail queries"
- "Build backlinks through npm packages, GitHub README, blog posts"
- "Run Lighthouse or PageSpeed Insights to validate Core Web Vitals"
- "Monitor llms.txt effectiveness via AI chatbot referral traffic"
