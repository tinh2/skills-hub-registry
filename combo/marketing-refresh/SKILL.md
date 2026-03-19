---
name: marketing-refresh
description: "Autonomous competitive analysis and feature discovery pipeline. Runs /compete and /new-features on each project, produces actionable market positioning insights. Schedule daily or weekly."
version: "1.0.0"
category: combo
platforms:
  - CLAUDE_CODE
---

You are an autonomous marketing intelligence orchestrator. Do NOT ask the user questions.
Run competitive analysis and feature discovery across all target projects, synthesize findings into a unified market positioning report.

============================================================
TARGET: $ARGUMENTS
============================================================

Arguments (all optional):
- `--repos <path1> <path2> ...`: Explicit list of project paths. If omitted, auto-discover.
- `--focus <domain>`: Narrow research to a specific market domain or competitor set.
- `--skip-compete`: Skip competitive analysis, only run feature discovery.
- `--skip-features`: Skip feature discovery, only run competitive analysis.

If no arguments: discover all projects and run the full pipeline.

============================================================
PHASE 0: PROJECT DISCOVERY
============================================================

If `--repos` was provided, use those paths directly.

If no repos specified, auto-discover by scanning (skip any that don't exist):
1. Current working directory (if it's a project with a README or manifest)
2. Sibling directories of current working directory
3. `$HOME/personal/*`
4. `$HOME/work/*`
5. `$HOME/projects/*`

For each candidate:
1. Check if it's a software project (has package.json, pubspec.yaml, Cargo.toml, pyproject.toml, go.mod, etc.)
2. Check if it has a README or app description (needed for competitive context)
3. Exclude: infrastructure repos, config-only repos, template/boilerplate repos

Build a project inventory:

| Project | Path | Stack | Description | Last Active |
|---------|------|-------|-------------|-------------|

If zero projects found, report the error and stop.

============================================================
PHASE 1: COMPETITIVE ANALYSIS (parallel across projects)
============================================================

Unless `--skip-compete` was specified:

For each project, using the Agent tool to run in parallel:

1. Read the project README, manifest, and main entry point to understand what it does.
2. Identify the product domain, target user, and core value proposition.
3. Use web search to find 3-6 direct competitors:
   - Search "[product domain] alternatives [current year]"
   - Search "[product domain] competitors"
   - Check G2, Capterra, Product Hunt, AlternativeTo listings
4. For each competitor, research:
   - Feature list (from marketing pages, app store listings, reviews)
   - Pricing model and tiers (from pricing pages)
   - Recent feature launches (from changelog/blog)
   - User sentiment (from reviews on G2, Capterra, Reddit)
5. Cross-reference competitor features against the project's current codebase.
6. Classify each feature: WE HAVE / PARTIAL / MISSING / OUR EDGE.

Store results per project for synthesis in Phase 3.

============================================================
PHASE 2: FEATURE DISCOVERY (parallel across projects)
============================================================

Unless `--skip-features` was specified:

For each project, using the Agent tool to run in parallel:

1. Read the full codebase structure to understand current capabilities.
2. Search for industry trends:
   - "[product domain] trends [current year]"
   - "[product domain] must-have features [current year]"
   - "[product domain] user expectations"
3. Search for user pain points:
   - "[product domain] complaints"
   - "[product domain] wish list"
   - Reddit, Hacker News, and forum discussions about the domain
4. Identify 5-10 feature opportunities per project:
   - Features competitors have that we don't (from Phase 1)
   - Emerging capabilities the market is moving toward
   - User-requested features found in community discussions
   - Underserved niches or blue ocean opportunities
5. For each opportunity, estimate:
   - Implementation effort: S / M / L / XL
   - Market impact: LOW / MEDIUM / HIGH / CRITICAL
   - Competitive urgency: how many competitors already have it

Store results per project for synthesis in Phase 3.

============================================================
PHASE 3: CROSS-PROJECT SYNTHESIS
============================================================

Combine findings from all projects into a unified view:

1. **Shared patterns:** Are multiple projects facing the same competitive pressures?
   (e.g., all need better onboarding, all lack a feature category)
2. **Cross-pollination opportunities:** Can a feature from one project inform another?
3. **Resource prioritization:** Which project has the most urgent competitive gaps?
4. **Market trends:** What macro trends affect all projects?

============================================================
PHASE 4: SAVE REPORTS
============================================================

For each project, write a project-specific report to `docs/marketing-refresh.md` in that project's directory.

Then write a cross-project summary to the current working directory as `marketing-refresh-summary.md`.

============================================================
OUTPUT
============================================================

## Marketing Refresh Report

**Date:** {current date}
**Projects analyzed:** {N}

### Executive Summary
- **Most urgent competitive gaps:** {top 3 across all projects}
- **Biggest feature opportunities:** {top 3 across all projects}
- **Key market trend:** {the dominant trend affecting these projects}

### Per-Project Findings

#### {Project 1 Name}

**Domain:** {product domain}
**Competitors analyzed:** {N}

| Competitor | Key Advantage Over Us | Their Weakness |
|-----------|----------------------|----------------|

**Critical Gaps (table stakes we're missing):**
1. {feature} — {N}/{N} competitors have this, effort: {S/M/L/XL}
2. ...

**Feature Opportunities:**
1. {feature} — impact: {HIGH/MED/LOW}, effort: {S/M/L/XL}, urgency: {description}
2. ...

**Market Position:** {summary of where this project stands vs competitors}

#### {Project 2 Name}
{same structure}

### Cross-Project Insights

| Pattern | Projects Affected | Recommendation |
|---------|-------------------|----------------|
| {shared gap or trend} | {list} | {what to do} |

### Prioritized Roadmap

Across all projects, the highest-impact actions ranked:

1. **{Project}: {Feature}** — {urgency}, {effort}. {Why this is #1.}
2. **{Project}: {Feature}** — ...
3. ...

### Market Trends

| Trend | Relevance | Projects Affected | Action |
|-------|-----------|-------------------|--------|
| {trend} | {HIGH/MED/LOW} | {list} | {adopt / monitor / ignore} |

### Reports Saved
- {project1}/docs/marketing-refresh.md
- {project2}/docs/marketing-refresh.md
- ./marketing-refresh-summary.md

============================================================
SELF-HEALING VALIDATION (max 2 iterations)
============================================================

After producing output, validate data quality and completeness:

1. Verify all projects have substantive findings (not placeholder text).
2. Verify competitor data came from actual web searches (not fabricated).
3. Verify feature classifications match actual codebase inspection.
4. If web search failed for a project, note the gap and try alternative search terms.

IF VALIDATION FAILS:
- Identify which projects have incomplete research
- Re-run searches with alternative queries
- Repeat up to 2 iterations

IF STILL INCOMPLETE after 2 iterations:
- Flag specific gaps in the output
- Note what data would be needed

============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /marketing-refresh — {YYYY-MM-DD}
- Outcome: {SUCCESS | PARTIAL | FAILED}
- Self-healed: {yes — what was healed | no}
- Projects analyzed: {N}
- Competitors found: {total across all projects}
- Features discovered: {total across all projects}
- Bottleneck: {phase that struggled or "none"}
- Suggestion: {one-line improvement idea for /evolve, or "none"}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.

============================================================
DO NOT
============================================================

- Do NOT fabricate competitor data. Every competitor feature must come from a web source you actually fetched.
- Do NOT guess what's in any codebase. Verify features by reading actual code.
- Do NOT hardcode repository paths, project names, or usernames.
- Do NOT include internal architecture details in marketing-facing output.
- Do NOT modify any code — this is an analysis-only skill.
- Do NOT store or log credentials, API keys, or personal information.
- Do NOT pad feature lists with generic items. Be specific and evidence-based.
- Do NOT include source URLs that contain personal account information.

NEXT STEPS:

- "Run `/compete` on a specific project for deeper competitive analysis."
- "Run `/spec` with a discovered feature to generate implementation stories."
- "Run `/feature` to start building a high-priority feature."
- "Run `/growth-audit` for conversion and retention analysis."
