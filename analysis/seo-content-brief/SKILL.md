---
name: seo-content-brief
description: Generate a 2026-grade content brief for a target query — combines classic SERP analysis with AI Overview / Perplexity / ChatGPT citation analysis, entity recommendations (target ≥15 recognized entities), topical authority gap map, intent-mapped heading structure, internal linking targets, FAQ from PAA + Reddit + AI prompt mining, and explicit E-E-A-T requirements (author entity profile, first-party data needed, primary source citations). Replaces older keyword-density-focused briefs. The brief tells a writer EXACTLY what to include for both Google ranking AND AI citation. TRIGGER on "content brief", "SEO brief", "article outline", "blog post brief", "topic outline", "write a brief for [keyword]", "content strategy for [topic]", "what should we write about [X]". Skip if user just wants a content idea — this skill is for the page-level brief, not the editorial calendar.
version: "1.0.0"
category: analysis
platforms:
  - CLAUDE_CODE
---

# SEO Content Brief Generator (2026)

You generate a content brief that ranks AND gets cited by AI. Modern briefs are no longer "keyword + word count + headings." They are entity-aware, intent-mapped, E-E-A-T-aware, and AI-citation-targeted.

Why this differs from a 2023-era brief:

- AI engines synthesize from MANY sources, weighting entity relationships and citation depth → a brief must list entities to mention, not just keywords.
- AI Overviews pull from the first 80 words of pages with strong structure → the brief must specify the answer-first opener.
- Entity density > keyword density. 15+ recognized entities ≈ 4.8× AI citation probability.
- Topical authority compounds — a brief is also a vote on which existing pages to internal-link to/from.

============================================================
=== PRE-FLIGHT ===
============================================================

Verify:

- [ ] **Target query** explicit ("best CRM for small business", "how to file 1099-NEC", etc.).
- [ ] **Intent classification**: informational / transactional / navigational / commercial-investigation. Different briefs per intent.
- [ ] **Site context**: domain URL + existing top 10 pages (so internal linking suggestions are real, not generic).
- [ ] **Author available**: at least one person with credible Author Entity setup (or note that author setup is a prerequisite — without it, the content won't get cited regardless of quality).
- [ ] **Output format**: markdown brief (default), Notion-flavored markdown, or Google Doc upload (export as .docx via pandoc).

Recovery:

- If query intent is ambiguous, default to informational (most common) and surface the disambiguation in the brief header.
- If existing site pages aren't accessible, generate a brief without internal linking suggestions and flag this gap.

============================================================
=== PHASE 1: SERP + AI CITATION ANALYSIS ===
============================================================

For the target query, gather signals from THREE surfaces:

### Classic SERP (Google top 10)

- Title, URL, content type (article/listicle/tool/video/forum), word count, last-updated date.
- People Also Ask (PAA) questions.
- Featured snippet structure (paragraph / list / table) — note: AI Overviews are eating featured snippet territory.

### AI Overview / Generative results

- Capture the AI Overview / Gemini answer for the query if available.
- List the 3–10 URLs cited by the AI Overview.
- Note which citations overlap with the organic top 10 (typically 60–80% overlap).

### Conversational AI engines

- Run the query through ChatGPT (with browsing), Perplexity, Claude (with search).
- Capture: which sources each engine cited, recurring entities mentioned, any consensus claims.

Output `brief/01_competitive_landscape.md` with side-by-side citation tables.

VALIDATION: Per-engine citation list has ≥ 3 URLs. Overlap with organic top-10 noted.

FALLBACK: Without Perplexity/ChatGPT API access, capture manually via the user's browser (provide them a copy-paste prompt). Less precise but unblocks the brief.

============================================================
=== PHASE 2: ENTITY EXTRACTION ===
============================================================

From the top 10 organic + AI-cited sources, extract every recognized entity (proper noun mapped to a Knowledge Graph node).

Bucket entities by type:

- **People**: founders, authors, public figures
- **Organizations**: companies, agencies, certifying bodies
- **Products / Tools**: named software, hardware, services
- **Places**: countries, cities, regions, neighborhoods
- **Concepts / Standards**: ISO numbers, frameworks, methodologies, laws
- **Events**: conferences, releases, historical milestones
- **Times / Dates**: years, eras, quarters

Output `brief/02_entities.md` ranked by co-occurrence frequency across sources.

Identify:

- **Must-mention entities** (in ≥ 50% of top 10 sources) — the brief MUST include these.
- **Differentiator entities** (in top 3 only, or unique to AI Overview citations) — the brief SHOULD include if relevant.
- **Stale entities** (in top 10 from 2022 sources but not in fresh AI citations) — likely safe to omit; flag for review.

VALIDATION: Entity list has ≥ 25 candidates. Must-mention list has ≥ 10 entities.

============================================================
=== PHASE 3: INTENT-MAPPED HEADING STRUCTURE ===
============================================================

Generate the H2/H3 outline. Each heading is a question the reader (or AI engine) is trying to answer.

Default outline patterns by intent:

**Informational ("what is X", "how does X work")**:

1. H1: {Definitive query phrasing}
2. Lead paragraph (answer in first 60 words — AI Overview target)
3. H2: What is {X}? (definition with key entity)
4. H2: How {X} works (mechanism, 3-5 steps)
5. H2: Types of {X} (taxonomy)
6. H2: When to use {X} (decision criteria)
7. H2: Common mistakes / misconceptions
8. H2: Tools / examples (entity-rich)
9. H2: FAQ (from PAA + Reddit + AI engines)

**Commercial-investigation ("best X", "X vs Y", "X review")**:

1. H1: {Best X for Y} or {X vs Y}
2. Lead paragraph (top recommendation in first 60 words)
3. H2: Quick comparison table (entity-dense)
4. H2: {Tool 1} — pros/cons/best-for
5. H2: {Tool 2} — pros/cons/best-for
6. ...
7. H2: How we evaluated (E-E-A-T signal)
8. H2: Decision framework (which to pick when)
9. H2: FAQ

**Transactional ("buy X", "X pricing", "X near me")**:

1. H1: Direct match
2. Lead with offer / pricing / availability
3. H2: Features
4. H2: Pricing tiers
5. H2: How to get started
6. H2: Customer outcomes / case studies (E-E-A-T)
7. H2: FAQ

Output `brief/03_outline.md`.

VALIDATION: Outline is intent-matched. Each H2 maps to a specific user question or buyer-journey stage.

============================================================
=== PHASE 4: FAQ MINING ===
============================================================

Compile the FAQ section from multiple sources:

1. **Google People Also Ask** — top 5 from SERP scrape.
2. **Reddit / forums** — search for the target query + "reddit" / "stackoverflow" / "quora"; extract recurring questions.
3. **AI engine outputs** — note any follow-up suggestions ChatGPT/Perplexity/Claude offer after the main answer.
4. **Comments / reviews** — if the user has G2 / Trustpilot / Amazon reviews on the product/topic, mine for unanswered questions.

Dedupe, rank by frequency, output as a 5–10 question FAQ section with answer drafts (1–3 sentences each).

VALIDATION: FAQ has ≥ 5 questions, each with a draft answer ≤ 60 words.

============================================================
=== PHASE 5: INTERNAL LINKING TARGETS ===
============================================================

From the user's existing top pages, identify:

- **3–5 pages to link TO from this new content** (topically relevant, higher in funnel).
- **3–5 pages to link FROM (back to this content)** (existing high-traffic pages where this new content would be a natural reference).

Format each as:

```markdown
- [{Anchor text}](https://example.com/path) — Why: {one-sentence rationale}
```

VALIDATION: Each suggested link has a specific anchor text and rationale, not just a URL.

FALLBACK: Without site access, suggest internal-link templates ("link to your pillar page on {X} topic") and let the writer fill specifics.

============================================================
=== PHASE 6: E-E-A-T REQUIREMENTS ===
============================================================

Specify what makes this content citable, not just rankable:

- [ ] **Author**: Named, byline links to `/author/{slug}`, Person schema, ≥ 3 `sameAs`.
- [ ] **First-party data**: original screenshot / chart / quote / experiment / dated metric.
- [ ] **Primary source citations**: ≥ 2 outbound links to authoritative sources (gov, academic, established trade publication).
- [ ] **Last-updated discipline**: page must include `dateModified` schema and visible "Updated YYYY-MM-DD" in DOM.
- [ ] **Original quote / interview**: if topic warrants, include a quote from a recognized practitioner or vendor.

Mark each as REQUIRED or RECOMMENDED based on competitiveness of the query (high-competition → all REQUIRED).

VALIDATION: List is specific to this brief's topic, not generic boilerplate.

============================================================
=== PHASE 7: THE FINAL BRIEF ===
============================================================

Combine all phases into `brief/{slug}.md`:

```markdown
# Content Brief — {Target Query}

**Generated:** {date}  
**Intent:** {informational / commercial-investigation / transactional}  
**Target length:** {word count based on competitor median ±10%}  
**Author requirement:** {Person entity profile complete: yes/no — must be yes to publish}

## TL;DR for the writer

- Lead with the direct answer in the first 60 words.
- Cover these MUST-MENTION entities: {list of 10}
- Hit ≥ 15 total recognized entities (see entities.md for the full pool).
- Internal-link to: {3 pages}
- FAQ section is required (5+ questions from FAQ.md).
- Author must be {Name}; if not, set up the Person entity first.

## Outline

{from Phase 3}

## Entities to include

{from Phase 2, must-mention bucket}

## FAQ section

{from Phase 4}

## Internal Linking

{from Phase 5}

## E-E-A-T requirements

{from Phase 6}

## Competitor benchmarks

- Median word count: {N}
- Median entity count: {N}
- Median schema types: {Article, FAQPage, ...}

## Schema to ship with the page

- Article (required)
- FAQPage (if FAQ section is present)
- BreadcrumbList
- {anything else specific to this topic — HowTo, Product, etc.}
```

VALIDATION: Brief is ≤ 6 pages of markdown. A competent writer should be able to produce the article from the brief alone without further research.

FALLBACK: If brief is too thin (insufficient SERP signal — emerging topic), say so explicitly and recommend supplementing with subject-matter-expert interview.

============================================================
=== SELF-REVIEW ===
============================================================

Score 1–5:

- **Complete**: All 7 phases? Entity list ≥ 25 candidates? Outline intent-matched? E-E-A-T section specific?
- **Robust**: Handled missing API access? Internal linking targets defaulted gracefully when site context unavailable?
- **Clean**: Brief is ≤ 6 pages, scannable, actionable?
- **AI-citation-ready**: A writer following this brief produces content that hits ≥ 15 entities, lead-with-answer structure, schema-ready, and has named-author E-E-A-T?

Common gap: brief loses entity discipline at writing time. Cap the brief by reminding the writer in the TL;DR to count entities before publishing.

============================================================
=== LEARNINGS CAPTURE ===
============================================================

Append to `~/.claude/skills/seo-content-brief/LEARNINGS.md`:

## <YYYY-MM-DD> — <target query, intent, vertical>

- **What worked:** <approach that produced a tight brief>
- **What was awkward:** <retry/manual fix needed>
- **Suggested patch:** <concrete improvement>
- **Verdict:** [Smooth / Minor friction / Major friction]

============================================================
=== STRICT RULES ===
============================================================

- Never produce a brief with only keywords and word count. That's a 2018 brief.
- Never recommend exact-match keyword stuffing. Modern engines penalize and AI engines ignore.
- Never omit the entity must-mention list. It's the highest-leverage section.
- Never skip the E-E-A-T requirements. A brief that gets published without author entity setup will not get cited.
- If the brief is for a YMYL topic (health, finance, legal), upgrade E-E-A-T REQUIRED items to include credentialed author + primary medical/legal/financial source citations.
