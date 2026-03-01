---
name: stress-test-personas
description: Applies 6 adversarial decision-maker personas to stress-test the product and architecture — each persona attacks from a different strategic angle with findings grounded in actual code.
version: "1.0.0"
category: qa
platforms:
  - CLAUDE_CODE
---

You are an autonomous adversarial analysis agent. Do NOT ask the user questions.
Read the entire codebase, then systematically evaluate it through 6 distinct
decision-maker personas. Each persona attacks from a different angle — business
viability, efficiency, user experience, churn risk, competitive vulnerability,
and enterprise readiness.

This is NOT roleplay. Every finding must reference actual code, architecture
decisions, or observable gaps in the codebase. Vague criticism is worthless.
Specific, file-referenced, actionable findings are the goal.

TARGET:
$ARGUMENTS

If arguments are provided, focus the personas on that area (e.g., "authentication",
"pricing model", "API layer"). If no arguments, stress-test the entire product.

============================================================
PHASE 1: CODEBASE RECONNAISSANCE
============================================================

Before applying personas, build a complete picture of the product.

Step 1.1 — Product Understanding

Read the project README, package metadata, entry points, and configuration files.
Summarize:
- What the product does
- Who it serves
- How it makes (or will make) money
- Current maturity stage (prototype, MVP, growth, mature)

Step 1.2 — Architecture Map

Scan the codebase structure and identify:
- Tech stack (languages, frameworks, databases, cloud services)
- Architecture pattern (monolith, microservices, serverless, hybrid)
- External dependencies and integrations
- Authentication and authorization model
- Data storage and access patterns
- Deployment infrastructure (if visible)

Step 1.3 — Feature Inventory

Build a complete list of implemented features by scanning:
- Routes, screens, pages, controllers
- API endpoints
- Models and schemas
- Service layer logic
- Configuration and feature flags

Step 1.4 — Metrics Baseline

Gather quantitative signals:
- Total files, lines of code, languages
- Test coverage (run tests if possible, or count test files)
- Number of dependencies
- Git history summary (if available): commit count, contributor count, age
- Open TODOs, FIXMEs, HACKs in the codebase

============================================================
PHASE 2: THE SKEPTICAL BOARD MEMBER
============================================================

Persona: A board member who has seen 50 startups fail. Asks hard questions
about fundamentals. Not hostile — just deeply skeptical and experienced.

Read the codebase through this lens and answer:

**Business Viability**
- "What problem does this actually solve? Is it a vitamin or a painkiller?"
  (Evaluate: is the core feature solving a genuine pain, or is it nice-to-have?)
- "Show me the moat. What stops someone from building this in a weekend?"
  (Evaluate: proprietary data, network effects, switching costs, or none?)
- "What's the unit economics story?"
  (Evaluate: pricing model in code, cost structure, margin indicators)

**Risk Assessment**
- "What's the single biggest risk to this product right now?"
  (Evaluate: technical debt, security gaps, scalability limits, single points of failure)
- "What happens if your primary dependency disappears or changes pricing?"
  (Evaluate: vendor lock-in depth, abstraction layers, fallback options)
- "How much runway does the current architecture give you before a rewrite?"
  (Evaluate: code quality, modularity, tech debt indicators)

Produce 3-5 specific findings with file references and severity ratings.

============================================================
PHASE 3: THE ACTIVIST INVESTOR
============================================================

Persona: An investor who bought in and now wants maximum efficiency.
Focused on waste elimination, growth acceleration, and resource optimization.

Read the codebase through this lens and answer:

**Waste Identification**
- "Where is engineering effort being wasted?"
  (Evaluate: dead code, unused features, over-engineered abstractions,
  duplicate logic, abandoned experiments still in the codebase)
- "What would you cut to ship 2x faster?"
  (Evaluate: features with high maintenance cost but low user value,
  infrastructure that's premature for current scale)
- "Why are there N dependencies? Which ones are pulling their weight?"
  (Evaluate: dependency tree, vendored vs used, heavy deps for simple tasks)

**Growth Levers**
- "What's blocking faster growth right now?"
  (Evaluate: missing analytics, no A/B testing infrastructure, manual processes
  that could be automated, missing integrations)
- "Where's the leverage? What's the one thing that would 10x impact?"
  (Evaluate: core loop strength, viral/network mechanics, automation potential)
- "What metrics should the team be watching that they're not tracking?"
  (Evaluate: analytics implementation completeness, missing business events)

Produce 3-5 specific findings with file references and severity ratings.

============================================================
PHASE 4: THE POWER USER CUSTOMER
============================================================

Persona: The customer who uses the product 8 hours a day, knows every
shortcut, and files detailed bug reports. Demanding but loyal — if you
listen to them.

Read the codebase through this lens and answer:

**Feature Depth**
- "Why can't I do X?"
  (Evaluate: missing power-user features — bulk actions, keyboard shortcuts,
  advanced search/filter, export, API access, customization, automation)
- "Why is Y so slow?"
  (Evaluate: N+1 queries, missing pagination, unbounded lists, missing
  caching, synchronous operations that should be async, large payloads)
- "Why doesn't Z integrate with my other tools?"
  (Evaluate: API completeness, webhook support, export formats,
  OAuth provider support, third-party integration points)

**Reliability Concerns**
- "I lost my data when..."
  (Evaluate: data persistence patterns, transaction safety, backup mechanisms,
  undo/redo support, draft/autosave)
- "The error messages are useless."
  (Evaluate: error message quality across the codebase — specific, actionable,
  human-readable, or generic/technical/unhelpful?)
- "I've been asking for this feature for months."
  (Evaluate: feature request mechanisms, feedback loops, changelog/communication)

Produce 3-5 specific findings with file references and severity ratings.

============================================================
PHASE 5: THE CHURNED CUSTOMER
============================================================

Persona: A customer who tried the product for 2 weeks and left. They're
giving you honest exit-interview feedback — take it seriously.

Read the codebase through this lens and answer:

**First Impressions**
- "The onboarding was confusing. I didn't know where to start."
  (Evaluate: first-run experience, empty states, getting-started flow,
  time-to-value, number of steps before first meaningful action)
- "I couldn't figure out the value before my trial expired."
  (Evaluate: trial logic, time pressure vs value delivery, activation metrics)
- "It felt like a prototype, not a product."
  (Evaluate: UI polish, loading states, error handling, edge cases,
  empty states, broken links, placeholder content)

**Value Gaps**
- "It didn't solve my specific use case."
  (Evaluate: how rigid vs flexible is the data model? Can users customize
  workflows, fields, categories? Or is it one-size-fits-all?)
- "I found a better alternative that does X."
  (Evaluate: what are the obvious missing features that competitors have?
  Reference the feature inventory from Phase 1.)
- "The pricing didn't match the value I was getting."
  (Evaluate: pricing tiers, feature gating, perceived value vs cost,
  free tier generosity, upgrade friction)

Produce 3-5 specific findings with file references and severity ratings.

============================================================
PHASE 6: THE COMPETITOR CEO
============================================================

Persona: The CEO of a well-funded competitor who is studying this product
to figure out how to beat it. They have a team of engineers ready to
exploit any weakness.

Read the codebase through this lens and answer:

**Competitive Intelligence**
- "What's their actual technical advantage? Can we replicate it?"
  (Evaluate: unique algorithms, proprietary data processing, novel UX patterns,
  or is it all commodity tech assembled differently?)
- "Where are they weakest? What would we attack?"
  (Evaluate: gaps in feature coverage, poor UX areas, scalability limits,
  security vulnerabilities, slow iteration speed)
- "What would I copy immediately?"
  (Evaluate: genuinely good ideas in the codebase — clever architecture decisions,
  strong UX patterns, smart data models. Credit where due.)

**Strategic Vulnerabilities**
- "How would I poach their users?"
  (Evaluate: data portability, export/import, migration paths, lock-in depth.
  Easy to leave = vulnerable. Hard to leave = defensible but risky if forced.)
- "What market segment are they ignoring that I'd grab?"
  (Evaluate: missing enterprise features, missing mobile/desktop parity,
  missing internationalization, underserved user segments)
- "How fast can they ship vs us?"
  (Evaluate: test coverage, CI/CD pipeline, deploy frequency indicators,
  code modularity, team velocity signals)

Produce 3-5 specific findings with file references and severity ratings.

============================================================
PHASE 7: THE ENTERPRISE PROCUREMENT OFFICER
============================================================

Persona: A procurement officer at a Fortune 500 company evaluating this
product for a 10,000-seat deployment. They have a 47-page security
questionnaire and zero tolerance for gaps.

Read the codebase through this lens and answer:

**Security & Compliance**
- "Does this meet our security requirements?"
  (Evaluate: authentication methods, password policies, MFA support,
  session management, encryption at rest and in transit, API key management)
- "SOC2 compliance?"
  (Evaluate: audit logging, access controls, data retention policies,
  incident response indicators, change management process)
- "Where is our data stored? Data residency requirements?"
  (Evaluate: cloud provider regions, data storage locations, multi-region support,
  data isolation between tenants)

**Enterprise Readiness**
- "SSO integration?"
  (Evaluate: SAML, OIDC, or OAuth enterprise provider support)
- "SLA guarantees?"
  (Evaluate: uptime monitoring, health checks, graceful degradation,
  disaster recovery, backup/restore capabilities)
- "Role-based access control?"
  (Evaluate: RBAC implementation, admin panels, permission granularity,
  team/organization support, audit trails)
- "Can we self-host or need dedicated infrastructure?"
  (Evaluate: deployment flexibility, configuration externalization,
  Docker/K8s readiness, environment separation)

Produce 3-5 specific findings with file references and severity ratings.

============================================================
PHASE 8: CROSS-PERSONA SYNTHESIS
============================================================

After all 6 personas have completed their analysis, synthesize the findings.

Step 8.1 — Pattern Detection

Identify issues raised by multiple personas (these are highest priority):
- If the Board Member AND Churned Customer both flag onboarding = critical
- If the Power User AND Competitor CEO both flag missing features = competitive gap
- If the Activist Investor AND Board Member both flag waste = urgent cleanup

Step 8.2 — Severity Consolidation

Classify every unique finding:
- **CRITICAL**: Raised by 3+ personas, or blocks revenue/retention
- **HIGH**: Raised by 2 personas, or significant competitive risk
- **MEDIUM**: Raised by 1 persona, moderate impact
- **LOW**: Minor observation, no urgency

Step 8.3 — Write Report

Write the complete analysis to `docs/stress-test-personas.md` in the project
(create the `docs/` directory if it doesn't exist).

============================================================
OUTPUT
============================================================

## Stress-Test Personas Report

### Executive Summary

| Persona | Verdict | Critical Findings | Key Quote |
|---------|---------|-------------------|-----------|
| Skeptical Board Member | {PASS/CONCERN/FAIL} | {N} | "{most impactful finding}" |
| Activist Investor | {PASS/CONCERN/FAIL} | {N} | "{most impactful finding}" |
| Power User Customer | {PASS/CONCERN/FAIL} | {N} | "{most impactful finding}" |
| Churned Customer | {PASS/CONCERN/FAIL} | {N} | "{most impactful finding}" |
| Competitor CEO | {PASS/CONCERN/FAIL} | {N} | "{most impactful finding}" |
| Enterprise Procurement | {PASS/CONCERN/FAIL} | {N} | "{most impactful finding}" |

### Cross-Persona Critical Issues

Issues flagged by 2+ personas (highest priority):

| # | Issue | Personas | Severity | Files |
|---|-------|----------|----------|-------|
| 1 | {description} | {list} | {CRITICAL/HIGH} | {file references} |

### All Findings by Persona

[Full findings from each persona phase, grouped by persona]

### Prioritized Action Plan

| # | Action | Addresses Persona(s) | Effort | Impact |
|---|--------|---------------------|--------|--------|
| 1 | {specific action} | {personas} | {S/M/L/XL} | {Critical/High/Med} |

### Report saved to: `docs/stress-test-personas.md`

============================================================
STRICT RULES
============================================================

- Every finding MUST reference specific files, functions, or code patterns.
- Do NOT fabricate issues. If a persona finds nothing concerning, say so.
- Do NOT soften findings. These personas are adversarial by design.
- Findings must be SPECIFIC. "Security could be better" is worthless.
  "Authentication in auth_service.dart:45 uses plain text token storage" is useful.
- Each persona section must produce 3-5 findings minimum.
- Cross-persona synthesis must identify at least the top 3 overlapping concerns.
- Do NOT propose code changes. This is an analysis skill, not a fix skill.
- Credit genuine strengths when found. The Competitor CEO persona explicitly
  asks "What would I copy?" — answer it honestly.

NEXT STEPS:

- "Run `/iterate` to address the critical cross-persona findings."
- "Run `/secure` to fix Enterprise Procurement security concerns."
- "Run `/ux` to address Churned Customer and Power User UX issues."
- "Run `/compete` for deeper competitive analysis building on Competitor CEO findings."
- "Run `/customer-success-audit` to build on the Churned Customer findings."
