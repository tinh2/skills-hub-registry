# Feature Ideation: skills-hub-registry Expansion

**Date:** 2026-03-01
**Source:** Competitive gap analysis (10 competitors), recall analysis (359 skills, 4.3h build), existing skills-hub.ai feature docs
**Theme:** Closing the count gap, cross-platform reach, and new skill categories

---

## Context

The skills-hub-registry has 359 skills with 100% structural consistency, 40 industry verticals, 28 combo chains, and 7 meta skills — quality advantages no competitor matches. However, Antigravity Awesome Skills has 954+ skills (2.6x our count), and critical categories are missing: language-specific skills (0), Data/AI skills (0), and cross-platform compatibility (CLAUDE_CODE only). This report proposes 18 features to close gaps and extend advantages.

---

## Feature Catalog

### TIER 1: HIGH Priority — Close Critical Gaps

---

#### R-001: Language & Framework Skills Category

**Priority:** HIGH
**Effort:** L (25-35 new skills)
**Gap addressed:** GAP 3 (Language/Framework-Specific Skills), count deficit vs Antigravity

**Description:**
Add a new `language` category with skills that teach Claude Code language-specific patterns, testing conventions, and framework best practices. This is the #1 category gap — Everything Claude Code covers 6 languages; Antigravity covers dozens of frameworks; we cover zero.

**Proposed skills (30):**

| Skill | Description |
|-------|-------------|
| `language/typescript/` | TypeScript strict mode patterns, utility types, type guards, declaration files |
| `language/python/` | Python best practices — typing, dataclasses, async/await, project structure |
| `language/go/` | Go idioms — error handling, goroutines, channels, interface design |
| `language/rust/` | Rust ownership, lifetimes, traits, error handling, async patterns |
| `language/java/` | Java modern patterns — records, sealed classes, virtual threads, Spring Boot |
| `language/swift/` | Swift concurrency (async/await, actors), SwiftUI, protocol-oriented design |
| `language/kotlin/` | Kotlin coroutines, multiplatform, Compose, Ktor patterns |
| `language/csharp/` | C# modern — records, pattern matching, LINQ, ASP.NET Core minimal APIs |
| `language/ruby/` | Ruby idioms — blocks, metaprogramming, Rails conventions, RSpec patterns |
| `language/php/` | PHP modern — typed properties, enums, fibers, Laravel patterns |
| `language/react/` | React patterns — hooks, server components, Suspense, performance optimization |
| `language/nextjs/` | Next.js App Router — layouts, loading states, server actions, caching |
| `language/vue/` | Vue 3 Composition API, Pinia, Nuxt 3, TypeScript integration |
| `language/angular/` | Angular signals, standalone components, typed forms, SSR with Analog |
| `language/svelte/` | SvelteKit, runes, form actions, progressive enhancement |
| `language/django/` | Django patterns — models, views, serializers, async views, testing |
| `language/fastapi/` | FastAPI patterns — dependency injection, Pydantic v2, async, background tasks |
| `language/nestjs/` | NestJS patterns — modules, guards, interceptors, microservices, GraphQL |
| `language/spring-boot/` | Spring Boot 3 — WebFlux, security, data JPA, testing, native images |
| `language/rails/` | Rails 8 — Hotwire, Turbo, Stimulus, Action Cable, Solid Queue |
| `language/flutter/` | Flutter patterns — Riverpod, GoRouter, platform channels, testing |
| `language/react-native/` | React Native — Expo, navigation, native modules, Reanimated, Skia |
| `language/tailwind/` | Tailwind CSS — design tokens, component patterns, responsive, dark mode |
| `language/sql/` | SQL patterns — window functions, CTEs, query optimization, indexing |
| `language/graphql/` | GraphQL — schema design, resolvers, subscriptions, federation, Relay |
| `language/terraform/` | Terraform patterns — modules, state management, workspaces, testing |
| `language/docker/` | Dockerfile best practices — multi-stage, layer caching, security scanning |
| `language/bash/` | Shell scripting — portability, error handling, argument parsing, testing |
| `language/elixir/` | Elixir/Phoenix — GenServer, LiveView, Ecto, supervision trees |
| `language/zig/` | Zig patterns — comptime, allocators, error handling, C interop |

**Differentiator vs. competitors:**
- Each skill follows our quality template (autonomous mode, phased, NEXT STEPS, DO NOT)
- Skills focus on patterns + anti-patterns with code examples, not just reference docs
- Cross-references to our existing build/test/deploy skills per language

---

#### R-002: Data & AI Skills Category

**Priority:** HIGH
**Effort:** L (15-20 new skills)
**Gap addressed:** Strategic GAP 3 (No Data/AI/ML Category), fastest-growing demand segment

**Description:**
Add a new `data` category covering ML pipelines, data engineering, prompt engineering, LLM evaluation, and RAG systems. Antigravity has a full "Data & AI" category. We have zero.

**Proposed skills (18):**

| Skill | Description |
|-------|-------------|
| `data/data-pipeline/` | Main orchestrator — scans for data stack, routes to sub-skills |
| `data/etl/` | ETL pipeline — extract, transform, load with Apache Airflow, Dagster, or Prefect |
| `data/data-modeling/` | Dimensional modeling — star schema, snowflake, slowly changing dimensions |
| `data/data-quality/` | Data quality checks — Great Expectations, Soda, dbt tests |
| `data/dbt/` | dbt project — models, tests, macros, documentation, CI/CD |
| `data/spark/` | Apache Spark — PySpark, Spark SQL, streaming, optimization |
| `data/ml-pipeline/` | ML pipeline — feature engineering, training, evaluation, serving |
| `data/model-evaluation/` | ML model evaluation — metrics, cross-validation, bias detection |
| `data/feature-store/` | Feature store setup — Feast, Tecton, or custom with Redis/BigQuery |
| `data/prompt-engineering/` | Prompt engineering — techniques, templates, evaluation, versioning |
| `data/rag/` | RAG system — chunking, embedding, vector store, retrieval, generation |
| `data/llm-evaluation/` | LLM output evaluation — benchmarks, human eval, automated scoring |
| `data/vector-db/` | Vector database setup — Pinecone, Weaviate, Qdrant, pgvector |
| `data/data-lakehouse/` | Lakehouse architecture — Delta Lake, Iceberg, Hudi |
| `data/streaming/` | Event streaming — Kafka, Kinesis, Pulsar, schema registry |
| `data/observability-data/` | Data observability — Monte Carlo, Elementary, lineage tracking |
| `data/notebook/` | Jupyter notebook patterns — reproducibility, testing, parameterization |
| `data/data-governance/` | Data governance — catalog, lineage, access control, PII detection |

**Differentiator vs. competitors:**
- Industry-specific data skills can cross-reference our 40 verticals (e.g., healthcare data pipelines with HIPAA, finance data with SOX)
- Autonomous mode — skills analyze existing data stack and generate pipelines, not just docs

---

#### R-003: Cross-Platform Compatibility Update

**Priority:** HIGH
**Effort:** S (metadata update on 359 skills)
**Gap addressed:** GAP 2 (Cross-Platform), competitive parity with Antigravity/SkillHub

**Description:**
Update the `platforms` field on all 359 skills to include compatible platforms beyond CLAUDE_CODE. Most SKILL.md-format skills work across tools without modification.

**Key Requirements:**
- Update platforms to `[CLAUDE_CODE, CURSOR, CODEX_CLI]` on all skills that use standard SKILL.md features
- Add `WINDSURF`, `OPENCODE`, `GEMINI_CLI` where applicable
- Test a sample of 10 skills on Cursor and Codex CLI to validate cross-platform behavior
- Add a `compatibility.md` doc explaining platform differences

**Impact:**
- Makes the registry discoverable by Cursor, Codex, and Windsurf users
- Matches Antigravity's 8-platform claim
- Opens the skills-hub.ai marketplace to a much larger user base

---

#### R-004: Expand Core Dev Categories (Reach 500+ Skills)

**Priority:** HIGH
**Effort:** XL (100-140 new skills across existing categories)
**Gap addressed:** GAP 1 (Raw Count Deficit)

**Description:**
Add skills to existing underpopulated categories to close the count gap with Antigravity (954+). Target: 500+ total skills.

**Category expansion plan:**

| Category | Current | Target | Add | Focus Areas |
|----------|---------|--------|-----|-------------|
| build | 21 | 30 | +9 | Monolith-to-microservice migration, serverless scaffold, Remix, Astro, SolidJS |
| test | 11 | 20 | +9 | Mutation testing, property-based testing, snapshot testing, test data factories, chaos |
| qa | 13 | 18 | +5 | Performance profiling, memory leak detection, race condition detection |
| review | 26 | 30 | +4 | Cost review, migration review, dependency review, config review |
| deploy | 15 | 22 | +7 | Blue-green deploy, canary releases, feature flags, edge functions, serverless |
| security | 12 | 18 | +6 | Supply chain security, SBOM, secrets rotation, zero-trust, API security |
| ux | 6 | 12 | +6 | Motion design, micro-interactions, loading states, error UX, onboarding UX |
| docs | 10 | 14 | +4 | Storybook docs, migration guides, troubleshooting guides, release notes |
| productivity | 8 | 12 | +4 | Task automation, code generation templates, snippet library, workspace |
| integration | 9 | 15 | +6 | Database (Supabase, PlanetScale), AI (OpenAI, Anthropic SDK), payments (LemonSqueezy) |

**Total: +60 skills → 419 + language (30) + data (18) = 467 skills minimum → 500+ with combo chains**

---

### TIER 2: MEDIUM Priority — Extend Advantages

---

#### R-005: Sample Inputs & Expected Outputs

**Priority:** MEDIUM
**Effort:** XL (add to all 359+ skills)
**Gap addressed:** GAP 4 (No Interactive Experience), feeds skills-hub.ai playground

**Description:**
Add a `## Examples` section to every skill with 2-3 sample invocations and their expected output summaries. This feeds the skills-hub.ai playground (F-025: Skill Sandbox) and helps users understand what each skill does before installing.

**Key Requirements:**
- Each skill gets 2-3 example blocks showing input → expected output format
- Examples are realistic (not "hello world")
- Examples reference common project types (React app, Python API, Flutter app)
- Examples are parseable by the marketplace app for playground pre-population

**Format:**
```markdown
## Examples

**Example 1:** `/skill-name my-react-app`
- Input: React 18 + TypeScript + Vite project with 12 components
- Output: Analysis report with 5 findings, 3 recommendations, 2 action items

**Example 2:** `/skill-name --focus security`
- Input: Node.js API with Express + Prisma
- Output: Security audit report with OWASP Top 10 coverage, 8 vulnerabilities found
```

---

#### R-006: Plugin Manifest & Installation

**Priority:** MEDIUM
**Effort:** M
**Gap addressed:** GAP 6 (No Installation Mechanism)

**Description:**
Create a `.claude-plugin/` manifest that makes the entire registry installable as a Claude Code plugin via the official plugin system.

**Key Requirements:**
- `.claude-plugin/manifest.json` with plugin metadata
- Install via: `/plugin marketplace add your-org/skills-hub-registry`
- Bundle selection: install all 500+ skills or choose by category
- Category-based bundles: `skills-hub-dev-tools`, `skills-hub-industry`, `skills-hub-social-impact`
- Version management via plugin system

**Differentiator:**
- Nobody offers category-selective plugin installation
- One command installs 500+ production-quality skills

---

#### R-007: Role-Based Skill Bundles

**Priority:** MEDIUM
**Effort:** M (15-20 new combo skills)
**Gap addressed:** Competitive parity with Antigravity bundles, user onboarding

**Description:**
Create role-based bundles that package skills by developer persona. Antigravity has "Web Wizard", "Security Engineer" bundles. We should have equivalent but backed by our higher-quality skills.

**Proposed bundles (15):**

| Bundle | Skills Included | Target User |
|--------|----------------|-------------|
| `combo/frontend-lead/` | /react + /nextjs + /tailwind + /responsive + /dark-mode + /design-system + /a11y | Frontend team lead |
| `combo/backend-lead/` | /api-scaffold + /db-migrate + /load-test + /api-review + /monitoring | Backend engineer |
| `combo/devops-engineer/` | /docker + /k8s + /terraform + /github-actions + /monitoring + /secrets | Platform/DevOps |
| `combo/security-engineer/` | /secure + /owasp + /pentest + /dependency-scan + /soc2 + /gdpr | Security team |
| `combo/data-engineer/` | /data-pipeline + /etl + /dbt + /data-quality + /streaming | Data engineering |
| `combo/ml-engineer/` | /ml-pipeline + /model-evaluation + /feature-store + /rag + /llm-evaluation | ML/AI team |
| `combo/mobile-developer/` | /flutter + /react-native + /ios-app + /android-app + /mobile-ci-cd | Mobile dev |
| `combo/game-developer/` | /unity-scaffold + /godot-scaffold + /game-design-audit + /game-launch | Game dev |
| `combo/startup-founder/` | /mvp + /build + /ship + /preflight + /landing-page | Solo founder |
| `combo/tech-lead/` | /arch-review + /tech-debt + /codebase-health + /iterate-review + /recall | Engineering lead |
| `combo/qa-engineer/` | /qa + /test-suite + /e2e + /load-test + /visual-regression + /manual-test-plan | QA team |
| `combo/documentation/` | /document + /readme + /api-docs + /adr + /changelog + /diagram | Technical writer |
| `combo/compliance-officer/` | /gdpr + /soc2 + /hipaa + /check-vanta + /encryption | Compliance |
| `combo/open-source/` | /readme + /changelog + /pr + /git-hooks + /linter + /release | OSS maintainer |
| `combo/fullstack/` | /build + /ship + /qa + /deploy + /monitor | Fullstack generalist |

---

#### R-008: Workflow Playbooks

**Priority:** MEDIUM
**Effort:** M (10-15 new skills)
**Gap addressed:** Competitive parity with Antigravity workflows, user guidance

**Description:**
Create step-by-step workflow playbooks that guide users through multi-skill processes for specific goals. These are like combo skills but with more narrative guidance and decision points.

**Proposed playbooks:**

| Playbook | Goal | Skills Used |
|----------|------|-------------|
| `combo/ship-saas/` | Ship a SaaS MVP in a weekend | /mvp → /build → /ship → /stripe → /auth → /deploy |
| `combo/audit-codebase/` | Full codebase audit | /analyze → /tech-debt → /codebase-health → /security-review |
| `combo/go-to-production/` | Production readiness | /preflight → /monitoring → /secrets → /cdn → /dns → /runbook |
| `combo/migrate-stack/` | Technology migration | /tech-debt → /api-surface → /db-migrate → /integration-test |
| `combo/onboard-team/` | Team onboarding setup | /onboarding → /devcontainer → /env-setup → /linter → /git-hooks |
| `combo/incident-drill/` | Incident response prep | /runbook → /chaos → /monitoring → /incident-response |
| `combo/quarterly-review/` | Quarterly codebase review | /recall → /metrics → /tech-debt → /dependency-analysis → /codebase-health |

---

#### R-009: Hooks & Commands Package

**Priority:** MEDIUM
**Effort:** L
**Gap addressed:** GAP 5 (No Agent/Hook/Command Ecosystem)

**Description:**
Add supporting hooks and commands that complement the skill collection. Ship as a separate directory that users can optionally install.

**Proposed hooks:**

| Hook | Trigger | Action |
|------|---------|--------|
| `hooks/pre-commit-lint/` | Pre-commit | Auto-run linter before commit |
| `hooks/post-commit-test/` | Post-commit | Run relevant tests after commit |
| `hooks/pre-push-security/` | Pre-push | Quick security scan before push |
| `hooks/pr-review/` | PR creation | Auto-generate PR description |
| `hooks/deploy-preflight/` | Pre-deploy | Run preflight checks before deploy |

**Proposed commands:**

| Command | Action |
|---------|--------|
| `commands/health/` | Quick codebase health check (subset of /analyze) |
| `commands/coverage/` | Show test coverage summary |
| `commands/deps/` | Show dependency health (outdated, vulnerable) |
| `commands/todo/` | Show TODO/FIXME/HACK comments across codebase |

---

### TIER 3: LOW Priority — Future Growth

---

#### R-010: Certification & Badging System

**Priority:** LOW
**Effort:** S
**Description:** Add quality tier badges to skills (Bronze/Silver/Gold/Platinum) based on structural completeness, instruction depth, example coverage, and production usage validation.

---

#### R-011: Skill Dependency Declarations

**Priority:** LOW
**Effort:** M
**Description:** Add `depends_on` field to SKILL.md frontmatter so combo skills and main skills formally declare their sub-skill dependencies. Enables automated dependency resolution in the marketplace.

---

#### R-012: Localized Skill Variants

**Priority:** LOW
**Effort:** XL
**Description:** Create locale-specific variants of industry skills for different regulatory environments (EU GDPR vs US CCPA, NHS vs FDA, etc.).

---

#### R-013: Skill Difficulty Levels

**Priority:** LOW
**Effort:** S
**Description:** Add `difficulty: beginner|intermediate|advanced` to frontmatter. Helps users find skills appropriate to their experience level.

---

#### R-014: Interactive Skill Builder

**Priority:** LOW
**Effort:** L
**Description:** A meta-skill that interviews users about their project and generates a custom skill tailored to their specific workflow. Builds on the existing `/skill-creator` but adds project analysis.

---

#### R-015: Changelog per Skill

**Priority:** LOW
**Effort:** M
**Description:** Add `CHANGELOG.md` to each skill directory documenting version history. Currently only the version field exists — no history of what changed between versions.

---

#### R-016: Automated Skill Testing Suite

**Priority:** LOW
**Effort:** XL
**Description:** GitHub Actions workflow that runs each skill against sample projects and validates the output meets quality criteria. Feeds into the certification system (R-010).

---

#### R-017: Community Contribution Guide

**Priority:** LOW
**Effort:** S
**Description:** Create CONTRIBUTING.md with guidelines for community skill submissions. Define quality standards, review process, and template requirements. Enables community growth while maintaining quality.

---

#### R-018: Skill Analytics Instrumentation

**Priority:** LOW
**Effort:** M
**Description:** Add optional telemetry integration so skills can report anonymized usage data back to the marketplace. Enables "most used" rankings and usage-based recommendations.

---

## Recommended Build Order

### Phase 1: Close the Count Gap (Week 1-2)
1. R-003: Cross-platform compatibility update (S — metadata batch update)
2. R-001: Language & Framework skills (L — 30 new skills)
3. R-002: Data & AI skills (L — 18 new skills)
4. R-004: Expand core dev categories (partial — 30 highest-impact skills)

**Result: ~440 skills, cross-platform, two new categories**

### Phase 2: Strengthen Moat (Week 3-4)
5. R-007: Role-based bundles (M — 15 combo skills)
6. R-008: Workflow playbooks (M — 7 combo skills)
7. R-004: Remaining core expansion (30 more skills)
8. R-006: Plugin manifest (M — distribution mechanism)

**Result: ~500+ skills, role-based bundles, installable as plugin**

### Phase 3: Ecosystem (Week 5-6)
9. R-005: Sample inputs/outputs (XL — enrich existing skills)
10. R-009: Hooks & commands package (L)
11. R-017: Community contribution guide (S)
12. R-011: Skill dependency declarations (M)

**Result: Complete ecosystem with playground support, automation, and community readiness**

---

## Impact Projections

| Metric | Current | After Phase 1 | After Phase 2 | After Phase 3 |
|--------|---------|---------------|---------------|---------------|
| Total skills | 359 | ~440 | ~500+ | ~520+ |
| Categories | 13 | 15 (+language, +data) | 15 | 15 |
| Industry verticals | 40 | 40 | 40 | 40 |
| Platform support | 1 | 5+ | 5+ | 5+ |
| Combo/bundle skills | 28 | 28 | 50+ | 50+ |
| Role bundles | 0 | 0 | 15 | 15 |
| Hooks/commands | 0 | 0 | 0 | 14 |
| Plugin installable | No | No | Yes | Yes |
| Sample I/O coverage | 0% | 0% | 0% | 100% |

---

## Summary

| Metric | Count |
|--------|-------|
| Total features proposed | 18 |
| HIGH priority | 4 |
| MEDIUM priority | 5 |
| LOW priority | 9 |
| New skills proposed | ~180 (30 language + 18 data + 60 core + 22 bundles/playbooks + hooks/commands) |
| Target total skills | 500+ |
| Estimated timeline | 6 weeks (3 phases of 2 weeks) |

**Top 5 features to build (in order):**
1. **R-003: Cross-Platform Compatibility** — fastest win, metadata update on existing skills
2. **R-001: Language & Framework Skills** — closes biggest category gap vs Antigravity
3. **R-002: Data & AI Skills** — fastest-growing demand segment, zero current coverage
4. **R-004: Core Category Expansion** — reach 500+ skills, close count gap
5. **R-007: Role-Based Bundles** — user onboarding, competitive parity with Antigravity bundles

**The thesis:** Quality beats quantity, but 359 vs 954+ is too large a gap to ignore. Reach 500+ while maintaining 100% structural validation, then let industry verticals (40), combo chains (50+), and cross-platform support (5+) be the differentiators that matter. Nobody else has curated quality + industry depth + skill composition.
