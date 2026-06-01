# Competitive Gap Analysis — Skills Hub Registry

> Generated 2026-06-01 | Domain: AI coding agent skills/plugin registry and marketplace

---

## Our Product

- **What it does:** Skills Hub Registry is the official curated skill collection for skills-hub.ai — a marketplace of 430+ production-tested autonomous AI agent skills for Claude Code and 26+ other AI coding tools, organized into 15 categories covering the complete software development lifecycle, 40 industry verticals, gaming, and mobile development. The skills-hub.ai website aggregates 5,400+ skills from 60+ sources. Each skill is a self-contained SKILL.md instruction set that runs end-to-end without asking the user questions.
- **Target user:** Developers using Claude Code, Cursor, Codex CLI, Gemini CLI, Windsurf, OpenCode, and other AI coding tools who need turn-key autonomous task execution for any software or domain challenge.
- **Core value prop:** Zero-question autonomy with self-healing validation, self-evolution telemetry, and uniquely pre-built combo chains that orchestrate multiple skills into full pipelines — invoke once, get a complete outcome.
- **Features implemented:** 430 curated skills in registry; 5,400+ indexed on skills-hub.ai

### Current Feature Checklist

**Discovery & Installation**
- [✅] Skills catalog as README (sortable by category)
- [✅] Web browse UI at skills-hub.ai/browse with semantic search and filtering
- [✅] CLI installation via `npx @skills-hub-ai/cli install <skill-name>` (auto-detects AI tool)
- [✅] Cross-platform SKILL.md format (26+ platforms: Claude Code, Cursor, Codex, Gemini CLI, Windsurf, Cline, Copilot, OpenCode, and more)
- [✅] Community skill publishing
- [✅] Skill versioning (semver)
- [✅] Curated bundles for common workflows
- [❌] Leaderboard / trending by install count
- [❌] Occupation/persona-based browsing (e.g., "DevOps engineer," "frontend developer")
- [❌] Community ratings and reviews
- [❌] Newsletter / "this week in skills" digest

**Execution & Automation**
- [✅] Autonomous zero-question execution
- [✅] Multi-phase phased execution structure
- [✅] Orchestrator + sub-skill routing pattern
- [✅] Self-healing validation blocks
- [✅] Self-evolution telemetry
- [✅] Combo/pipeline chain skills (34 multi-skill chains) — **unique to Skills Hub**
- [✅] Scheduled/headless execution via `/loop` — **unique to Skills Hub**
- [✅] Parallel feature dispatch via `/parallel-features` — **unique to Skills Hub**
- [✅] Context save/load across sessions

**Quality & Security**
- [✅] Registry CI validation (`/registry-sync`)
- [✅] Internal quality scoring rubric (0-100)
- [❌] Automated security scanning on submitted skills
- [❌] Malicious intent detection (prompt injection, data exfiltration, dangerous commands)
- [❌] Per-skill security grade (A–F) visible to users

**Creator Ecosystem**
- [❌] Creator monetization (paid skills, revenue share)
- [❌] Creator analytics (install counts, usage telemetry per publisher)
- [❌] Skill bounty / enterprise custom skill tiers
- [❌] Creator profile pages

**Developer API**
- [❌] REST API with OpenAPI spec for programmatic skill discovery
- [❌] MCP server exposing skill registry as a tool
- [❌] Embed widget for third-party platform integration

**Domain Coverage (current strengths)**
- [✅] 40 industry verticals in analysis category (197 skills)
- [✅] Full SDLC coverage: build → test → QA → review → deploy → docs → security → UX
- [✅] Gaming-specific skills (Unity, Unreal, Godot, web game)
- [✅] Mobile-specific skills (Flutter, React Native, iOS, Android)
- [✅] Video production skills (ad video, tutorial video, social clip, wedding video)
- [✅] Meta-skills for skill lifecycle (creator, publisher, registry-sync, evolve, tend)
- [❌] Data/AI/ML category (RAG, feature stores, model evaluation, data pipelines)
- [❌] Language/framework pattern skills (TypeScript, Go, Rust, React, etc.)

---

## Competitive Landscape

| Competitor | Positioning | Pricing | Market Position | Skill Count |
|-----------|-------------|---------|-----------------|-------------|
| [Skills.sh (Vercel)](https://skills.sh) | "npm for AI agents" — open CLI + leaderboard; official skills from Vercel, Prisma, Supabase, Stripe, Coinbase, Microsoft | Free | Leader | 90,000+ |
| [SkillsMP](https://skillsmp.com) | Largest aggregator, GitHub-scraped, minimal curation | Free | Volume leader | 800,000+ |
| [Agensi](https://agensi.io/skills) | Security-first curated marketplace with creator monetization (80/20 Stripe) | Free–$400 | Quality-tier niche leader | 500+ curated |
| [LobeHub Skills](https://lobehub.com/skills) | Polished marketplace within multi-agent ecosystem, community ratings | Free | Challenger | 169,739 |
| [AgentSkill.sh](https://agentskill.sh) | Directory + security scoring, 20+ AI tools coverage | Free | Mid-tier | 193,000–216,000 |
| [Agent Skills Hub](https://agentskillshub.dev) | Security-first, automated 45+ vulnerability pattern scanning, A–F grades | Free | New entrant (security niche) | N/A |
| [ClaudeMarketplaces.com](https://claudemarketplaces.com) | Community-curated Claude Code–specific directory | Free | Niche (Claude-specific) | 6,700+ |
| [ClaudeSkills.info](https://claudeskills.info) | Community-contributed, Anthropic skills + submissions | Free | Niche | 658+ |
| [Anthropic Official Plugins](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) | First-party skills curated by Anthropic | Free | Authority | 100+ |
| [PromptBase](https://promptbase.com) | World's largest general AI prompt marketplace | $1.99–$19.99/prompt | Leader (general prompts) | 500,000+ prompts |

### Source URLs

- Skills.sh: [Vercel announcement](https://vercel.com/changelog/introducing-skills-the-open-agent-skills-ecosystem); [InfoQ coverage](https://www.infoq.com/news/2026/02/vercel-agent-skills/)
- SkillsMP: [SkillsMP site](https://skillsmp.com); [SmartScope guide](https://smartscope.blog/en/blog/skillsmp-marketplace-guide/)
- Agensi: [Best Marketplaces 2026](https://www.agensi.io/learn/best-ai-agent-skills-marketplaces-2026); [Monetization guide](https://www.agensi.io/learn/agent-skills-marketplace-sell-your-skills)
- AgentSkill.sh: [Directory](https://agentskill.sh)
- Agent Skills Hub: [agentskillshub.dev](https://agentskillshub.dev)
- skills-hub.ai: [Homepage](https://skills-hub.ai); [Codex skills](https://skills-hub.ai/codex-skills)
- Market overview: [Digital Applied — AI Agent Marketplaces 2026](https://www.digitalapplied.com/blog/ai-agent-marketplaces-2026-discovery-distribution)
- MCP trends: [The New Stack — 5 Key Trends in Agentic Development 2026](https://thenewstack.io/5-key-trends-shaping-agentic-development-in-2026/)
- Security gap: [Snyk + Vercel](https://snyk.io/blog/snyk-vercel-securing-agent-skill-ecosystem/)

---

## Feature Matrix

| Feature | Skills Hub | Skills.sh | SkillsMP | Agensi | AgentSkill.sh | AgentSkillsHub |
|---------|:----------:|:---------:|:--------:|:------:|:-------------:|:--------------:|
| Web browse UI + semantic search | ✅ | 🔶 leaderboard | ✅ | ✅ | ✅ | ✅ |
| CLI installer (one command) | ✅ npx | ✅ npx skills add | ❌ manual | ✅ curl | ❌ | ❌ |
| Cross-platform (20+ agents) | ✅ 26+ | ✅ 17-19 | 🔶 4 | ✅ 20+ | ✅ 20+ | 🔶 3 |
| Community ratings / reviews | ❌ | ❌ | ❌ | 🔶 editorial | ❌ | ❌ |
| Leaderboard / trending | ❌ | ✅ (24h + all-time) | ❌ | ❌ | ❌ | ❌ |
| Install count tracking | ❌ | ✅ (579K top skill) | ❌ | ❌ | ❌ | ❌ |
| Creator monetization | ❌ | ❌ | ❌ | ✅ 80/20 | ❌ | ❌ |
| Automated security scanning | ❌ | 🔶 Snyk (post-launch) | ❌ | ✅ 8-point | 🔶 scoring | ✅ 45+ patterns, A–F |
| Per-skill security grade visible | ❌ | ❌ | ❌ | 🔶 editorial | 🔶 score | ✅ A–F badge |
| Combo / chaining skills | ⭐ 34 chains | ❌ | ❌ | ❌ | ❌ | ❌ |
| Scheduled / headless execution | ⭐ /loop | ❌ | ❌ | ❌ | ❌ | ❌ |
| Parallel dispatch | ⭐ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Self-evolution telemetry | ⭐ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Industry vertical depth (40+) | ⭐ 197 skills | ❌ | 🔶 categories | ❌ | ❌ | ❌ |
| Meta-skills (skill lifecycle) | ⭐ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Curated bundles / stacks | ✅ | ❌ | ❌ | ✅ ($149–400) | ❌ | ❌ |
| REST API access | ❌ | ❌ | ✅ OpenAPI 3.0 | ❌ | ❌ | ❌ |
| MCP server for registry | ❌ | ❌ | ✅ | 🔶 | ❌ | ❌ |
| Occupation-based browsing | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ |
| Creator profile pages | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| Official vendor skills | 🔶 Anthropic | ✅ Vercel, Stripe, Supabase, Prisma, Coinbase, Microsoft | ❌ | ❌ | ❌ | ❌ |
| Newsletter / community digest | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

Use: ✅ = has it, 🔶 = partial, ❌ = missing, ⭐ = our edge

---

## Critical Gaps (Build Now)

### 1. Automated Security Scanning + Per-Skill Grade

- **Who has it:** Agensi (8-point automated scan: prompt injection, data exfiltration, dangerous commands, secret detection, obfuscation, external fetches, credential access, privilege escalation + human review); Agent Skills Hub (45+ vulnerability patterns, A–F security grades visible on every skill page); agentskill.sh (scoring)
- **Why it matters:** SkillsMP's own data: 26.1% of community-sourced skills contain at least one vulnerability; 5.2% show patterns of malicious intent. Agent Skills Hub launched in 2026 specifically to fill this gap — if Skills Hub doesn't act, security-conscious developers will defect to agentskillshub.dev. Being the "audited, safe" registry is a durable differentiator.
- **Effort:** M
- **Implementation hint:** Extend `/registry-sync` (meta/registry-sync/SKILL.md) to include a security-scan phase. Check for: shell command injection patterns in instructions, external HTTP fetches to non-whitelisted domains, instructions to read/write credentials or `.env` files, obfuscated content. Generate a `security-score` (A–F) in each skill's frontmatter. Surface it in the web UI and README catalog.

### 2. Install Count / Usage Telemetry Surfaced to Users

- **Who has it:** Skills.sh (leaderboard, top skill has 579K installs, 235K weekly for find-skills utility); agentskill.sh (audit detail views)
- **Why it matters:** "Most used" sort is the single biggest trust signal in any marketplace. Without it, users can't distinguish battle-tested skills from untested ones. Skills.sh's leaderboard is cited in every comparison article as a key differentiator.
- **Effort:** S–M
- **Implementation hint:** The `tend` meta-skill already runs telemetry — extend it to report aggregate install counts back to a central privacy-preserving counter (skill-level only, no PII). Surface in web UI, README catalog, and as a `weekly_installs` field in SKILL.md frontmatter.

### 3. Creator Monetization

- **Who has it:** Agensi (Stripe Connect, 80/20 split, $5–$400 range); PromptBase ($1.99–$19.99, 80% creator share, 500K listings)
- **Why it matters:** Creator economics drive catalog growth. The current 430-skill registry requires all effort from the core team. PromptBase's 500K listings vs Agensi's 500 curated vs Skills Hub's 430 proves: incentives scale supply. Expert domain skills (HIPAA compliance audits, game economy balancing) could command $20–$100 each from professional studios. The market is showing that 80/20 splits are the standard.
- **Effort:** L
- **Implementation hint:** Extend `publish-skill` meta-skill to accept an optional `price` field in SKILL.md frontmatter. A Stripe checkout flow on skills-hub.ai generates a license token baked into the install command. CLI verifies the token. Creator dashboard shows earnings.

### 4. MCP Server for Registry Discovery

- **Who has it:** SkillsMP (MCP integration), MCPMarket.com, Anthropic Official (MCP plugin listings)
- **Why it matters:** MCP is the de facto "USB-C for AI" in 2026 — natively supported by Anthropic, OpenAI, Google, and Microsoft. An MCP server lets any MCP-compatible agent (Claude, Cursor, Windsurf) discover and install Skills Hub skills without leaving their IDE. MCP-based access changes the distribution model: agent connects once, searches live catalog, loads skills on demand.
- **Effort:** M
- **Implementation hint:** The `mcp__skills-hub__*` tools are already referenced in system prompts (list_installed_skills, search_skills, get_skill_detail, install_skill). Build the MCP server to match these existing tool signatures. Deploy as Cloudflare Worker or Vercel Edge Function wrapping the existing gen-catalog JSON export.

---

## Strategic Gaps (Plan & Schedule)

### 5. REST API with OpenAPI Spec

- **Who has it:** SkillsMP (free tier, no credit card required, REST + MCP server)
- **Why it matters:** Enables third parties to embed Skills Hub discovery in their own tools (IDE extensions, agent builders, onboarding wizards). Enables programmatic skill composition at runtime. Required foundation for the MCP server (Gap 4).
- **Effort:** M
- **Implementation hint:** `gen-catalog` meta-skill already generates a JSON catalog from SKILL.md frontmatter. Deploy as Cloudflare Worker or Vercel Edge Function. Add OpenAPI spec. Expose `GET /skills`, `GET /skills/{name}`, `GET /skills?category=build&q=nextjs`.

### 6. Leaderboard / Trending Rankings

- **Who has it:** Skills.sh (24h trending + all-time leaderboard, cited in InfoQ coverage as key feature); agentskill.sh (audit views)
- **Why it matters:** 235K weekly installs of `find-skills` shows developers actively seek discovery tools. A leaderboard provides social proof and surfaces what's actually working in production. Without it, Skills Hub's 430-skill catalog is undifferentiated from any skill list.
- **Effort:** S (once install telemetry from Gap 2 exists)
- **Implementation hint:** Build on top of install count telemetry. Add sort options to web UI: "Most Installed," "Trending This Week," "Newest," "Highest Rated." Surface top 10 in README hero section.

### 7. Official Vendor Skills

- **Who has it:** Skills.sh (Vercel, Prisma, Supabase, Stripe, Remotion, Coinbase, Microsoft all shipped official skills before Q1 2026 ended)
- **Why it matters:** Vendor-official skills are the highest-trust content in any marketplace. They drive developer adoption of the platform and give Skills Hub authority beyond community content. skills-hub.ai already aggregates from 60+ sources; the gap is officially co-branded skills from the vendors themselves.
- **Effort:** M (business development + integration)
- **Implementation hint:** Skills Hub already curates from many sources. Create a "Verified Vendor" tier with a badge, dedicated landing pages per vendor, and a vendor portal for direct publishing. Target initial vendors: Anthropic, Supabase, Expo, Cloudflare Workers AI.

### 8. Community Ratings and Reviews

- **Who has it:** LobeHub (community feedback), Agensi (editorial notes), PromptBase (creator ratings)
- **Why it matters:** The biggest trust-builder after install counts. Allows users to report broken skills, surface better alternatives, and reward quality creators.
- **Effort:** M
- **Implementation hint:** Each skill directory already exists on GitHub. Add a GitHub Discussions template per skill. Surface discussion thread count and latest feedback in web UI. Zero custom backend for v1.

---

## Differentiator Opportunities

### 9. Data/AI/ML Skills Category

No competitor has pre-built skills for data engineering, RAG systems, ML pipelines, LLM evaluation, or prompt engineering. This is the fastest-growing segment in developer tooling. Skills Hub's existing pattern (autonomous, zero-question, phased execution) would work exceptionally well for ML workflows which require careful setup steps.

- **Effort:** L (15–20 new skills)
- **Opportunity:** Cross-reference with 40 existing industry verticals (e.g., healthcare data pipelines with HIPAA, finance data with SOX) — a depth no data-tools competitor can match.

### 10. Language/Framework Pattern Skills

No skills marketplace has dedicated language-pattern skills (TypeScript strict mode, Go idioms, Rust ownership patterns, React hooks, etc.). These are the highest-frequency developer queries. A `language/` category with 25–30 skills would directly address the gap vs. Antigravity (which covers dozens of frameworks) and close a major SEO surface area.

- **Effort:** L (25–30 new skills)
- **SEO opportunity:** "Claude Code TypeScript skill" has zero dedicated results — entirely greenfield keyword territory.

### 11. Skill Stacks / Bundle Sales

Skills Hub is the only marketplace with combo/chaining skills (34 multi-skill pipelines). A "Mobile Launch Stack" ($29), "Compliance Bundle" ($49), "Game Studio Pack" ($79) would monetize this unique capability while providing high-value opinionated bundles that no raw prompt marketplace can replicate.

- **Effort:** M (pricing layer on top of creator monetization)
- **Competitors with this:** Agensi has $149–400 enterprise bundles, but without combo chains

### 12. Agent-Aware In-IDE Skill Recommendations

While coding in Claude Code, proactively suggest relevant skills based on what's currently open (e.g., "You're building a Next.js app — `/nextjs`, `/e2e`, `/secure` are available"). GitHub Copilot Extensions have context-aware suggestions. No skills marketplace does this.

- **Effort:** L
- **Competitors with this:** None in skills space; GitHub Copilot Extensions do context-aware suggestions

### 13. Enterprise Governance Tier

The iflytek SkillHub (GitHub) launched a self-hosted enterprise registry with RBAC and audit logs. No other skills marketplace offers RBAC, air-gapped installs, policy controls, or enterprise SSO. This is a first-mover opportunity in a wide-open segment, especially as enterprises require governance for AI-agent tool deployment.

- **Effort:** XL
- **Competitors with this:** iflytek/skillhub (GitHub, self-hosted only); TrueFoundry (MCP, not skills)

---

## Our Competitive Edges

### ⭐ Combo / Pipeline Chain Skills (34 chains)

No competitor has pre-built multi-skill orchestration chains. Skills Hub's `/launch-readiness`, `/mobile-launch`, `/compliance-gate`, `/secure-ship`, `/story`, `/research` etc. are the equivalent of a DevOps playbook encoded into a single invocation. This is the most defensible differentiation — it requires not just content but an architectural understanding of how skills should compose.

**Protect by:** building more chains, making chains the primary marketing message, documenting the chain pattern as the "Skills Hub way."

### ⭐ Scheduled / Headless Execution (`/loop`)

No other skills marketplace has a scheduling primitive. `/loop` combined with `/tend` creates a fully autonomous improvement cycle. As background agents become standard (Cursor Background Agents, Claude Code doubled limits), this capability is ahead of the curve.

**Protect by:** building more scheduled skills, documenting headless use cases, marketing to DevOps/SRE audiences.

### ⭐ Parallel Feature Dispatch (`/parallel-features`)

Parallel git worktree–based skill execution is unique. No competitor supports spawning multiple agents across isolated branches and merging results. This directly addresses the multi-agent trend (Gartner: 1,445% inquiry surge).

**Protect by:** building on this with more multi-agent skills, documenting the pattern prominently.

### ⭐ 40-Industry Vertical Depth (197 analysis skills)

No competitor comes close. Agensi has ~8 categories; SkillsMP has keyword search but no domain expertise baked in. Skills Hub's HIPAA audit, FedRAMP review, game economy balancing, clinical data review, energy compliance, permit compliance, etc. are unique professional-grade capabilities inaccessible elsewhere.

**Protect by:** treating industry verticals as a premium tier, pursuing enterprise licensing per vertical.

### ⭐ Self-Evolution Telemetry + Meta-Skills

The `/evolve`, `/tend`, `/skillify`, and `/skill-creator` meta-skills create a self-improving registry. No competitor has this. It's a compounding moat.

**Protect by:** publishing improvement metrics, making telemetry visible in release notes.

### ⭐ Zero-Question Autonomous Execution Philosophy

Every Skills Hub skill explicitly forbids asking the user questions. This is a product philosophy encoded at the format level. No competitor has codified this as a hard constraint.

---

## Industry Trends

| Trend | Adoption Stage | Competitors With It | Our Status | Recommendation |
|-------|---------------|--------------------|-----------:|----------------|
| MCP as primary discovery/delivery layer | Mainstream (natively supported by Anthropic, OpenAI, Google, Microsoft) | SkillsMP, Anthropic Official, MCPMarket | ❌ Registry not yet MCP-served | Build MCP server immediately — this is becoming table stakes |
| Official vendor-published skills | Early mainstream (Vercel, Stripe, Supabase, Coinbase all shipped in Q1 2026) | Skills.sh (6+ major vendors) | 🔶 Site aggregates but not co-branded | Pursue vendor partnerships, create "Verified Vendor" tier |
| Security-first distribution | Early mainstream (Agent Skills Hub launched; 26.1% community skills have vulnerabilities) | Agensi (8-point), AgentSkillsHub (A–F grades), agentskill.sh | ❌ No scanning | Build scanning urgently before community submissions scale |
| Context-aware in-IDE recommendations | Emerging | GitHub Copilot Extensions | ❌ Missing | High differentiation if built first in skills space |
| Enterprise governance (RBAC, audit logs, air-gapped) | Pre-mainstream | iflytek/skillhub (GitHub) | ❌ Missing | First-mover opportunity |
| Creator economics (80/20 marketplace splits) | Early (Agensi pioneering, PromptBase proven) | Agensi, PromptBase | ❌ Missing | Evaluate when catalog growth plateaus |
| Curated bundles / workflow packs | Emerging | Agensi ($149–400), skills-hub.ai (basic bundles) | 🔶 Basic | Expand with combo-chain bundles at multiple price points |
| Multi-agent orchestration skills | Mainstream | Cursor (Build in Parallel), Windsurf (Cascade) | ✅ Ahead — /parallel-features, combo chains | Promote heavily; build more multi-agent combos |
| SKILL.md standard (26+ platforms) | Mainstream | Skills.sh (17–19), Agensi (20+), skills-hub.ai (26+) | ✅ On par | Maintain and certify new platforms as they launch |

---

## Recommended Roadmap

### Sprint 1 — Quick Wins (next 2–4 weeks)

1. **Security scanning in registry-sync** — CRITICAL pressure, M effort. Extend `/registry-sync` to flag prompt injection, credential access, external fetch patterns. Display A–F security grade in web UI and README. Publish methodology publicly — this alone differentiates Skills Hub vs the growing security-focused competitors.
2. **Install count telemetry** — HIGH pressure, S effort. Extend `/tend` to report aggregate install counts. Add "Most Installed" sort to web UI and README catalog. Highest-trust signal in any marketplace.
3. **Leaderboard** — HIGH pressure, S effort (depends on telemetry). "Trending This Week" + "All-Time Top 10" in README hero and web UI.

### Next Quarter — Strategic

4. **MCP server for registry** — CRITICAL pressure, M effort. Match existing `mcp__skills-hub__*` tool signatures. Deploy as edge function. This is becoming table stakes as MCP achieves full standardization in 2026.
5. **REST API + OpenAPI spec** — HIGH pressure, M effort. Foundation for MCP server and third-party integrations. `gen-catalog` JSON is already generated.
6. **Data/AI/ML skills category** — HIGH opportunity, L effort. 15–20 new skills covering RAG, ML pipelines, LLM evaluation, data engineering. Zero competition in this niche with autonomous execution.
7. **Language/framework pattern skills** — HIGH opportunity, L effort. 25–30 skills for TypeScript, Go, Rust, React, Vue, Python patterns. Closes major SEO gap and count deficit.
8. **Vendor partnership program** — HIGH opportunity, M effort. Pursue Anthropic, Supabase, Expo, Cloudflare as initial official skill publishers. "Verified Vendor" badge creates a quality tier no competitor currently offers.

### Future — Differentiators

9. **Creator monetization** — L effort. Stripe Connect, 80/20 split. Only after catalog growth plateaus or when Agensi proves creator economics work at scale.
10. **Skill Stacks / Bundle pricing** — M effort. "Mobile Launch Stack," "Compliance Bundle," "Game Studio Pack" — leverage unique combo chain capability.
11. **Community ratings via GitHub Discussions** — M effort. Zero-backend v1 using native GitHub features per skill.
12. **Agent-aware in-IDE recommendations** — L effort. Hook into Claude Code session context; suggest skills based on open files/tasks.
13. **Enterprise governance tier** — XL effort. RBAC, audit logs, air-gapped installs. iflytek showed this is possible as a GitHub project; build as a hosted product.

---

## Summary

- **Total features across top 6 competitors:** ~52 distinct user-facing capabilities
- **We have:** 30 (58%) — weighted by our combo/scheduling/domain uniqueness
- **Partial:** 5 (10%)
- **Missing:** 17 (33%)
- **Our edges:** 6 distinct categories where we lead or are the only player
- **Critical gaps to close:** 4 (security scanning, install telemetry, creator monetization, MCP server)

**Biggest threat:** The security-first niche is now contested. Agent Skills Hub (agentskillshub.dev) launched in 2026 with A–F security grades for every skill, targeting the exact position Skills Hub could own. If Skills Hub doesn't build security scanning before community submissions scale, this niche gets taken.

**Biggest opportunity:** MCP server for registry discovery. MCP is the de facto integration layer for agentic AI in 2026, natively supported across all major platforms. Skills Hub already has the `mcp__skills-hub__*` tool signatures defined in system prompts. Shipping this first converts discovery from "visit a website" to "your agent finds and installs skills automatically while you work" — a step-change in distribution that no competitor has fully executed yet.
