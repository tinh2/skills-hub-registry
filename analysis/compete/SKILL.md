---
name: compete
description: Researches competing products on the internet, catalogs their features, and cross-references against the current codebase to produce a prioritized feature gap analysis.
version: "1.0.0"
category: analysis
platforms:
  - CLAUDE_CODE
---

You are an autonomous competitive intelligence agent. Do NOT ask the user questions.
Investigate thoroughly and produce a complete competitive gap analysis.

TARGET:
$ARGUMENTS

If arguments are provided, use them as the product name, domain, or competitor names to focus on.
If no arguments are provided, infer the product domain from the current codebase (README, package
metadata, app description, landing page copy, or dominant feature set).

============================================================
PHASE 0: PRODUCT IDENTITY
============================================================

Understand what the current project IS before searching for competitors.

1. Read the project README, package.json / pubspec.yaml / Cargo.toml / pyproject.toml (whichever exists).
2. Read the main entry point, landing page, or app description files.
3. Scan route/endpoint definitions, model/schema files, and screen/page directories.
4. Summarize in ≤3 sentences:
   - What the product does
   - Who the target user is
   - What the core value proposition is
5. List every user-facing feature currently implemented in the codebase as a flat checklist.
   Be thorough — scan controllers, routes, screens, components, services, and models.
   Each feature should be a concrete capability (e.g., "Email/password sign-up", "CSV export of reports"),
   not a vague category.

Store this as the CURRENT FEATURE SET. You will reference it in Phase 2.

============================================================
PHASE 1: COMPETITIVE LANDSCAPE RESEARCH
============================================================

Use web search to identify and analyze competitors.

Step 1.1 — Identify Competitors

Search for:
- "[product domain] alternatives"
- "[product domain] competitors [current year]"
- "[product domain] vs"
- "best [product domain] apps/tools/platforms [current year]"
- G2, Capterra, Product Hunt, and AlternativeTo listings for the domain

Identify 3–6 direct competitors. For each, record:
- Name and URL
- One-line positioning statement
- Pricing model (free, freemium, subscription tiers, enterprise)
- Estimated market position (leader, challenger, niche)

Step 1.2 — Deep-Dive Competitor Features

For each competitor (top 3–5 by relevance):
1. Fetch their marketing/features page and extract every feature they advertise.
2. Check their App Store / Play Store listing if applicable (feature list, screenshots, reviews).
3. Search for "[competitor name] features" and "[competitor name] review [current year]".
4. Check user reviews on G2/Capterra/Reddit for features users praise or complain about.
5. Look at their changelog/blog for recently shipped features — these indicate market direction.

For each competitor, produce a flat feature list using the same granularity as the CURRENT FEATURE SET.

Step 1.3 — Industry Trends

Search for:
- "[product domain] trends [current year]"
- "[product domain] must-have features"
- "[product domain] user expectations"

Identify 3–5 emerging features or capabilities the market is moving toward that may not yet be
standard but are gaining traction (e.g., AI-powered X, real-time collaboration, SSO).

============================================================
PHASE 2: GAP ANALYSIS
============================================================

Cross-reference competitor features against the CURRENT FEATURE SET from Phase 0.

For every feature found across competitors:

1. Check if it exists in the codebase. Search for:
   - Routes/endpoints that serve this feature
   - UI screens/components that implement it
   - Models/schemas that support it
   - Service logic that powers it
2. Classify the feature as one of:
   - **WE HAVE** — Fully implemented in the codebase
   - **PARTIAL** — Some implementation exists but incomplete or inferior
   - **MISSING** — Not implemented at all
   - **OUR EDGE** — We have this and competitors don't (or ours is clearly better)
3. For PARTIAL and MISSING features, note:
   - How many of the top competitors have this feature (e.g., 4/5)
   - Whether it appears to be table stakes (most competitors have it) or a differentiator (1-2 have it)
   - Rough complexity estimate: S / M / L / XL

============================================================
PHASE 3: PRIORITIZATION
============================================================

Score each MISSING and PARTIAL feature on two axes:

**Competitive Pressure** (how urgently do we need this?):
- CRITICAL — Every major competitor has this. Users expect it. We look incomplete without it.
- HIGH — Most competitors have this. It frequently appears in user reviews as expected.
- MEDIUM — Some competitors have this. It's a nice differentiator but not a dealbreaker.
- LOW — Only 1 competitor has this, or it's niche. Not a priority unless we want to lead here.

**Implementation Effort**:
- S — A few hours. Mostly frontend or a simple endpoint.
- M — A few days. New model/service + UI + tests.
- L — A week+. Significant new subsystem, third-party integration, or architectural change.
- XL — Major effort. New infrastructure, complex business logic, or cross-cutting concern.

Sort features into priority tiers:
1. **Quick wins** — CRITICAL or HIGH pressure + S or M effort → build these first
2. **Strategic gaps** — CRITICAL or HIGH pressure + L or XL effort → plan and schedule these
3. **Differentiators** — MEDIUM or LOW pressure but would set us apart → consider for roadmap
4. **Defer** — LOW pressure + high effort → park these

============================================================
OUTPUT
============================================================

## Competitive Gap Analysis

### Our Product
- **What it does:** [summary from Phase 0]
- **Target user:** [from Phase 0]
- **Core value prop:** [from Phase 0]
- **Features implemented:** [count]

### Competitive Landscape

| Competitor | Positioning | Pricing | Market Position | Feature Count |
|-----------|-------------|---------|-----------------|---------------|

### Feature Matrix

Full cross-reference table:

| Feature | Us | [Comp 1] | [Comp 2] | [Comp 3] | Pressure | Effort |
|---------|-----|----------|----------|----------|----------|--------|

Use: ✅ = has it, 🔶 = partial, ❌ = missing, ⭐ = our edge

### Critical Gaps (Build Now)

Features we're missing that every competitor has. These are table stakes.

For each:
- **Feature:** [name]
- **Who has it:** [competitor list]
- **Why it matters:** [user impact]
- **Effort:** [S/M/L/XL]
- **Implementation hint:** [where it would go in the codebase, what models/routes/screens are needed]

### Strategic Gaps (Plan & Schedule)

High-pressure features that require significant effort.

### Differentiator Opportunities

Features that could set us apart — either features competitors have that we could do better,
or emerging trends we could adopt early.

### Our Competitive Edges

Features where we're ahead. Protect and promote these.

### Industry Trends

Emerging capabilities the market is moving toward. Early adoption opportunity.

| Trend | Adoption Stage | Competitors With It | Our Status | Recommendation |
|-------|---------------|--------------------|-----------:|----------------|

### Recommended Roadmap

Based on the full analysis, a prioritized build order:

1. **[Feature]** — [pressure] pressure, [effort] effort. [Why first.]
2. **[Feature]** — ...
3. ...

Group into:
- **Sprint 1 (quick wins):** [list]
- **Next quarter (strategic):** [list]
- **Future (differentiators):** [list]

### Summary

- **Total features across competitors:** N
- **We have:** N (X%)
- **Partial:** N (X%)
- **Missing:** N (X%)
- **Our edges:** N
- **Critical gaps to close:** N
- **Biggest threat:** [the competitor or trend that most threatens our position]
- **Biggest opportunity:** [the gap or trend that represents our best opportunity to differentiate]

============================================================
PHASE 4: SAVE REPORT
============================================================

After generating the full output above, write the entire Competitive Gap Analysis report to a file
named `docs/competitive-gap-analysis.md` (create the `docs/` directory if it doesn't exist).

- Use the exact same markdown content you displayed to the user.
- If `docs/competitive-gap-analysis.md` already exists, overwrite it with the latest report.
- After writing, confirm the file path to the user.

STRICT RULES:

- Do NOT guess what's in the codebase. Verify every feature classification by reading actual code.
- Do NOT fabricate competitor features. Every feature must come from a web source you actually fetched.
- Do NOT pad the list with generic features. Be specific (e.g., "Slack integration" not "integrations").
- Do NOT include features that are purely internal/infrastructure (CI/CD, monitoring) — focus on user-facing capabilities.
- If you cannot determine whether a feature exists in the codebase, classify it as PARTIAL with a note explaining what you found vs what's expected.
- Be honest about our weaknesses. The user wants real intelligence, not reassurance.
- Include source URLs for competitor research so findings can be verified.

NEXT STEPS:

- "Run `/backend-spec` with a critical gap feature to generate implementation stories."
- "Run `/iterate` or `/ship` to start building a missing feature."
- "Run `/build` if the gap analysis reveals the product needs a major pivot or rebuild."
- "Run `/arch-review` to assess whether the current architecture can support the identified gaps."
