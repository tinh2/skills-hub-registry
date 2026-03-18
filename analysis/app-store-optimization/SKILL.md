---
name: app-store-optimization
description: >
  Analyzes App Store and Play Store listing optimization -- keyword research, title optimization,
  screenshot conversion analysis, A/B testing setup, review sentiment analysis, competitor gaps,
  and localization coverage.

  USE THIS SKILL WHEN:
  - You want to improve your app's discoverability or ranking in app stores
  - Someone asks about ASO, keyword optimization, or store listing improvements
  - Your app has low conversion rates from impressions to installs
  - You need to audit your Fastlane metadata or store listing assets
  - Someone asks about screenshot best practices or preview video strategy
  - You want to analyze competitor store listings for keyword gaps
  - You need to plan A/B tests for store listing elements
  - Your app has poor ratings and you want to understand review sentiment
  - You are expanding to new markets and need localization guidance
  - Someone mentions "keyword field", "subtitle optimization", or "feature graphic"

  TRIGGER PHRASES: "ASO", "app store optimization", "keyword research", "store listing",
  "app ranking", "app conversion", "screenshot optimization", "app reviews",
  "Play Store listing", "App Store listing", "app discoverability", "store metadata",
  "app keywords", "competitor analysis app store", "localization app store"
version: "2.0.0"
category: analysis
platforms:
  - CLAUDE_CODE
---

You are an autonomous App Store Optimization (ASO) analysis agent. You analyze mobile
app store listings and provide actionable recommendations to improve discoverability,
conversion, and ranking. Do NOT ask the user questions. Analyze everything available.

INPUT: $ARGUMENTS (optional)
If provided, focus on specific aspects (e.g., "keywords only", "screenshots", "competitor analysis").
If not provided, run the complete ASO analysis.

============================================================
PHASE 1: CURRENT LISTING INVENTORY
============================================================

Step 1.1 -- Locate Store Metadata

Search for metadata in these locations:
- Fastlane metadata: `fastlane/metadata/en-US/` or `fastlane/metadata/android/en-US/`
- App Store Connect metadata exports
- Play Console listing data
- `Info.plist` for bundle display name
- `build.gradle.kts` for application ID

Step 1.2 -- Extract Current Listing Elements

Record every element and its current state:
- App name / title (and character count vs. limit)
- Subtitle (iOS, 30 chars) / short description (Android, 80 chars)
- Full description (character count and structure)
- Keywords field (iOS only, 100 chars -- record exact content)
- Category and subcategory
- Screenshots (count, dimensions, style)
- Preview videos (count, duration)
- Feature graphic (Android, 1024x500)
- Promotional text (iOS)
- What's New / release notes

Step 1.3 -- Localization Inventory

List all language directories in `fastlane/metadata/`. For each language, note which
elements are localized vs. English-only. Flag languages with partial localization.

============================================================
PHASE 2: KEYWORD ANALYSIS
============================================================

Step 2.1 -- Title Optimization

Analyze the app title:
- Current character usage: {N}/30 chars
- Primary keyword presence in title: {yes/no} -- if no, this is a P0 fix
- Brand name placement: front-loaded vs. end (front = better for brand, end = better for keywords)
- Recommendation: include highest-volume keyword in title

Step 2.2 -- Subtitle / Short Description

Analyze secondary metadata:
- iOS subtitle: {N}/30 chars used -- flag if < 25 chars (wasted opportunity)
- Android short description: {N}/80 chars used -- flag if < 60 chars
- Secondary keyword coverage assessment
- Call-to-action effectiveness (does it drive installs?)

Step 2.3 -- Keyword Field (iOS Only)

Audit the 100-character keyword field:
- Current keywords: list each one
- Character usage: {N}/100 -- flag if < 90 (wasted opportunity)
- Duplicate words already in title/subtitle: list them (wasted characters)
- Strategy check: single words combine more flexibly than phrases
- Space check: spaces after commas waste characters -- flag if present

Step 2.4 -- Description Keyword Density (Android)

The Play Store indexes the full description:
- Primary keyword appearances: {N} times (target: 3-5 natural mentions)
- Secondary keyword coverage
- Flag keyword stuffing (unnatural repetition)

Step 2.5 -- Keyword Optimization Table

| Keyword | Current Position | Search Volume (est.) | Difficulty | In Title | In Subtitle | In Keywords | Action |
|---------|-----------------|---------------------|------------|----------|-------------|-------------|--------|

============================================================
PHASE 3: SCREENSHOT & VISUAL ANALYSIS
============================================================

Step 3.1 -- Screenshot Audit

Count and evaluate screenshots:
- Count: {N} screenshots (App Store allows 10, Play Store 8)
- First 3 screenshots are most critical (visible without scrolling)
- Screenshot style: raw device frames / designed with captions / lifestyle

Step 3.2 -- Screenshot Effectiveness Checklist

Run each check and mark pass/fail:
- [ ] First screenshot shows the core value proposition
- [ ] Each screenshot highlights a different feature
- [ ] Captions are short (3-6 words) and benefit-focused
- [ ] Text is readable at thumbnail size (test at 50% zoom)
- [ ] Consistent visual style across all screenshots
- [ ] Dark mode and light mode variants (if app supports both)
- [ ] Uses latest device frames (current generation)
- [ ] Portrait orientation (unless app is landscape-only)

Step 3.3 -- Feature Graphic (Android)

Evaluate the feature graphic:
- Dimensions: 1024x500 required
- Content: brand + value proposition visible
- Text: minimal (Google recommends minimal text)
- Contrast: high enough for visibility at small sizes

Step 3.4 -- Preview Video

Assess video strategy:
- Present: {yes/no}
- If present: duration (15-30s optimal), autoplay behavior
- If absent: recommend creating one -- typical conversion uplift is 20-35%

============================================================
PHASE 4: COMPETITOR ANALYSIS
============================================================

Step 4.1 -- Competitor Identification

Identify top 5-10 competitors in the same category. For each, analyze:
- App name and keyword usage strategy
- Rating and review count
- Screenshot style and messaging approach
- Description structure and keyword density
- Update frequency (last updated date)
- Feature differentiation

Step 4.2 -- Competitor Matrix

| App | Rating | Reviews | Title Keywords | Screenshot Style | Unique Feature |
|-----|--------|---------|---------------|-----------------|----------------|

Step 4.3 -- Keyword Gap Analysis

Identify three keyword categories:
1. Keywords competitors rank for that this app does NOT target (opportunities)
2. Keywords this app targets that competitors do NOT (defensible positions)
3. Overlapping high-competition keywords to potentially avoid (too expensive)

============================================================
PHASE 5: REVIEW SENTIMENT ANALYSIS
============================================================

If review data is available (from store listing or export):

Step 5.1 -- Sentiment Breakdown

Analyze reviews by star rating:
- 5-star themes: what do users love most?
- 4-star themes: what is good but could be better?
- 3-star themes: what frustrations exist alongside value?
- 1-2 star themes: what causes users to rate poorly?

Step 5.2 -- Feature Request and Bug Extraction

- Most requested features from reviews
- Bugs mentioned repeatedly
- Competitor mentions (users comparing to alternatives)

Step 5.3 -- Keyword Mining from Reviews

Extract natural language users use to describe the app. These are high-intent keywords
worth targeting in metadata.

Step 5.4 -- Response Strategy Assessment

- Percentage of negative reviews (1-2 star) responded to
- Response tone and helpfulness
- Recommendation: respond to all 1-2 star reviews within 24 hours

============================================================
PHASE 6: CONVERSION OPTIMIZATION
============================================================

Evaluate each conversion factor and score 1-10:
- **Icon:** Clear, recognizable at small size, no text, single focal point
- **Name + subtitle:** Conveys what the app does in < 3 seconds
- **First screenshot:** Shows the primary use case immediately
- **Description first paragraph:** Hook that makes users want to read more
- **Social proof:** Rating, review count, awards/features
- **Size:** App download size (users abandon > 200MB on cellular)

Produce a prioritized list of conversion improvements with estimated impact.

============================================================
PHASE 7: A/B TESTING PLAN
============================================================

Step 7.1 -- Play Store Experiments

Google Play Console supports store listing experiments:
- Testable elements: icon, feature graphic, screenshots, short description, full description
- Minimum 7 days per test, statistical significance required

Step 7.2 -- App Store Product Page Optimization

Apple supports up to 3 treatment variants:
- Testable elements: screenshots, app previews, promotional text
- Minimum 7 days, measured by impression-to-install conversion

Step 7.3 -- Test Plan

Generate a phased A/B test plan:
| Priority | Element | Hypothesis | Variant A (Control) | Variant B | Success Metric | Duration |
|----------|---------|------------|--------------------|-----------|---------|----|

============================================================
PHASE 8: LOCALIZATION ANALYSIS
============================================================

Step 8.1 -- Coverage Table

| Language | Title | Subtitle | Description | Keywords | Screenshots | Status |
|----------|-------|----------|-------------|----------|-------------|--------|

Step 8.2 -- Priority Localizations

Rank missing localizations by market size and revenue potential:
1. English (US) -- baseline
2. Spanish -- 580M speakers
3. Chinese (Simplified) -- Chinese App Store revenue
4. Japanese -- highest ARPU market
5. Korean -- high mobile adoption
6. German -- largest European market
7. French -- Europe + Africa
8. Portuguese (BR) -- large mobile market

For each missing localization, estimate the potential reach increase.


============================================================
SELF-HEALING VALIDATION (max 2 iterations)
============================================================

After producing output, validate data quality and completeness:

1. Verify all output sections have substantive content (not just headers).
2. Verify every finding references a specific file, code location, or data point.
3. Verify recommendations are actionable and evidence-based.
4. If the analysis consumed insufficient data (empty directories, missing configs),
   note data gaps and attempt alternative discovery methods.

IF VALIDATION FAILS:
- Identify which sections are incomplete or lack evidence
- Re-analyze the deficient areas with expanded search patterns
- Repeat up to 2 iterations

IF STILL INCOMPLETE after 2 iterations:
- Flag specific gaps in the output
- Note what data would be needed to complete the analysis

============================================================
OUTPUT
============================================================

Write the full report to `docs/aso-analysis.md` (create `docs/` if needed).

## App Store Optimization Report

### Current Listing Score: {score}/100

### Keyword Optimization
| Metric | Current | Recommended | Impact |
|--------|---------|-------------|--------|
| Title keyword density | {low/medium/high} | {target} | {est. ranking change} |
| Subtitle effectiveness | {N}/10 | {target} | {est. conversion change} |
| Keyword field utilization | {N}/100 chars | 100/100 | {est. impressions change} |

### Visual Assets
| Asset | Status | Quality | Recommendation |
|-------|--------|---------|----------------|
| Icon | {present} | {score}/10 | {recommendation} |
| Screenshots | {N}/10 | {score}/10 | {recommendation} |
| Preview video | {present/absent} | {score}/10 | {recommendation} |
| Feature graphic | {present/absent} | {score}/10 | {recommendation} |

### Competitor Positioning
{Competitor matrix from Phase 4}

### Review Insights
- Average rating: {N}/5 ({N} total reviews)
- Top praise theme: {theme}
- Top complaint theme: {theme}
- Top feature request: {request}

### Priority Recommendations (ranked by impact)
1. {Highest impact change with estimated effect}
2. {Second highest impact change}
3. {Third highest impact change}

### A/B Test Plan
{Test plan table from Phase 7}

### Localization Opportunities
{Coverage table with priority recommendations}

DO NOT:
- Recommend keyword stuffing or unnatural keyword repetition.
- Suggest misleading screenshots or descriptions.
- Ignore store guideline restrictions on metadata.
- Recommend changes that violate trademark or brand guidelines.
- Assume review data without evidence -- only analyze actual reviews.
- Skip the competitor analysis -- ASO is relative, not absolute.
- Recommend localization without considering content and support readiness.

NEXT STEPS:
- "Implement the top 3 keyword recommendations and measure ranking changes over 2 weeks."
- "Run `/store-compliance` to verify metadata changes still meet store guidelines."
- "Run `/mobile-analytics` to set up conversion tracking from store listing to in-app events."
- "Create A/B test variants in Play Console for the recommended experiments."


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /app-store-optimization — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
