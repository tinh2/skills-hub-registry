# Competitive Gap Analysis — skills-hub.ai

**Generated:** 2026-07-01

---

## Our Product

- **What it does:** skills-hub.ai is an open-source registry of 489+ production-tested SKILL.md instruction files ("skills") for Claude Code and compatible AI coding agents, covering the full software development lifecycle across 15 categories and 40+ industry verticals.
- **Target user:** Software developers using Claude Code (and compatible agents: Cursor, Codex CLI, Gemini CLI, OpenClaw, Windsurf, GitHub Copilot, Cline) who want to extend their AI assistant with pre-built, production-hardened workflows.
- **Core value prop:** The trusted, signed registry for AI agent skills — install in one command, ship with confidence via cryptographic signing and lockfile-based team versioning, with the deepest skill creation and evolution tooling in the ecosystem.
- **Tech stack:** SKILL.md open standard, npx CLI, MCP server, cryptographic signing, lockfile versioning
- **Features implemented:** 44 (see checklist below)

### Current Feature Set

- ✅ 489+ skills across 15 categories (build, test, qa, review, deploy, docs, security, ux, analysis, productivity, integration, combo, meta, education, spec)
- ✅ CLI installation (`npx @skills-hub-ai/cli install <skill>`)
- ✅ Cryptographic skill signing (tamper-evidence)
- ✅ Lockfile-based team versioning (`.skills.json`)
- ✅ SKILL.md open standard (cross-agent compatibility — adopted by 26+ platforms)
- ✅ Multi-agent support (Claude Code, Cursor, Codex CLI, Gemini CLI, OpenClaw, Windsurf, Copilot, Cline, 20+ more)
- ✅ MCP server integration (search, install, list skills via MCP tools)
- ✅ 40+ industry vertical skills (fintech, healthcare, real estate, gaming, etc.)
- ✅ Skill creation tooling (`/skill-creator`) with eval harness
- ✅ Skill evaluation/benchmarking (quantitative + qualitative)
- ✅ Skill publishing workflow (`/publish-skill`)
- ✅ Registry sync automation (`/registry-sync`)
- ✅ Orchestrator pattern (main skill + sub-skill routing)
- ✅ Self-healing validation built into all v2.0.0+ skills
- ✅ Self-evolution telemetry in all v2.0.0+ skills
- ✅ Free / open-source (no paid tier)
- ✅ Skill improvement tooling (`/evolve`, `/tend`, `/skillify`)
- ✅ Context save/load system (`/save-context`, `/load-context`)
- ✅ Token optimization (`/save-tokens`)
- ✅ Skill template extraction (`/extract-template`)
- ✅ Skill bootstrap (`/bootstrap`)
- ✅ Broadcast/announcement system (`/broadcast`)
- ✅ Skill testing (`/skill-test`)
- ✅ Platform promote workflow (`/promote`)
- ✅ YouTube research skill for content creation
- ✅ Skill catalog documentation auto-generation (`/gen-catalog`)
- ✅ Blog content tooling (`/blog-writer`)
- ✅ Mobile skills (Flutter, React Native, iOS, Android)
- ✅ Gaming skills (Godot, Unity, Unreal, Phaser)
- ✅ AI/ML pipeline skills
- ✅ Full-stack scaffolding skills (Next.js, Flutter, Android, iOS, CLI tools)
- ✅ Security skills (OWASP, pentest, GDPR, SOC2, encryption, secrets)
- ✅ Infrastructure skills (AWS, Terraform, k8s, Docker, CDN, monitoring)
- ✅ Video production skills (Remotion, FFmpeg, ElevenLabs, social clips, video-upscale)
- ✅ Combo/chained multi-skill orchestration skills (37 combos)
- ✅ Education/onboarding skills
- ✅ Social-impact verticals (emergency response, elder care, FOIA, grants)
- ✅ Conventional commits + quality gate patterns documented
- ✅ UX design skills suite (28 skills: design-tokens, design-audit, design-delight, game-ux, etc.)
- ✅ Kiro spec-driven development skill
- ✅ Viral artifact generator skill
- ✅ Programmatic SEO page builder skill
- ✅ Curated bundles for common workflows (combo category)

---

## Competitive Landscape

| Competitor | Positioning | Pricing | Market Position | Catalog Size |
|-----------|-------------|---------|-----------------|--------------|
| **Skills.sh** (skills.sh) | Vercel-backed npm-style package manager for skills, with interactive discovery | Free + open | **Ecosystem anchor** | 669,670+ skills |
| **agentskill.sh** | Security-first skills directory with two-layer scanning (12 categories, 0–100 score) | Free | Security leader | 274,000+ skills |
| **AgentSkill.club** (agentskill.club) | Community-driven library of GitHub-sourced open-source skills | Free | Community aggregator | 3,640+ skills |
| **ClaudeSkills.info** | Free curated collection including official Anthropic skills (PDF, DOCX, XLSX, frontend design, MCP builder) | Free | Official-adjacent directory | 658+ skills |
| **SkillsLLM** (skillsllm.com) | GitHub-centric discovery of security-vetted skills for Claude Code, Codex CLI, ChatGPT | Free | GitHub-native index | 1,600+ skills |
| **LobeHub Skills** (lobehub.com/skills) | Integrated skills marketplace inside Chief Agent Operator platform | Freemium | Platform play | 169,739+ skills |
| **SkillHub** (skillhub.club) | "Agent Skills Solution — 100x your own domain" with desktop app + MCP server | Freemium (credits for Skill Stacks) | Curated catalog leader | 9,500+ skills (API) |
| **SkillsMP** (skillsmp.com) | "Discover open-source agent skills for any SKILL.md tool" | Free | Largest raw index | 800,000+ scraped |
| **Agensi** (agensi.io) | "Give your AI agent superpowers — vetted, secure skills" with creator economy | Free + paid (80% creator split) | Premium/security-first | 44+ curated |
| **ClaudeMarketplaces** (claudemarketplaces.com) | "#1 directory for Claude Code plugins, skills, and MCP servers" | Free | Meta-directory / media | 20,300+ aggregated |
| **TrueFoundry Skills Registry** | Enterprise-grade versioned skill registry with RBAC, audit logs, CI/CD | Enterprise / SaaS | Enterprise leader | Internal/org-scoped |
| **Microsoft Skills** (microsoft.github.io/skills) | 100+ Azure/Microsoft domain skills; native Agent Framework integration | Free + enterprise | Big Tech — Microsoft | 100+ domain skills |
| **Google Gemini Skill Registry** | Enterprise SKILL.md registry for Gemini Enterprise Agent Platform | Enterprise | Big Tech — Google | Enterprise/cloud |

---

## Pricing Comparison

| Tier / Profile  | Us | Skills.sh | SkillHub | Agensi |
| --------------- | --- | -------- | -------- | ------ |
| Free tier | ✅ All 489 skills | ✅ All | ✅ Basic skills | ✅ Free skills |
| Solo user / mo | $0 | $0 | $0–$9 (credits) | $0 + per-skill pricing |
| Team of 5 / mo | $0 | $0 | ~$45 (credits) | $0 + per-skill × 5 |
| Team of 25 / mo | $0 | $0 | Custom | Custom |
| Enterprise 100+ | $0 | $0 | Custom | Custom |
| Pricing model | Free/open | Free/open | Freemium + credits | Free + one-time skill purchases |

Key pricing insights:
- We are the only fully free platform with no premium tier — a trust and adoption advantage early, but a monetization gap long-term.
- Agensi's creator economy (80% creator revenue, top skills earning $500–$3,000/mo) shows real demand for premium skills. Skills authors have no incentive to contribute exclusively to us.
- Enterprise players (TrueFoundry, Microsoft, Google) charge for governance features (RBAC, versioning, audit logs) — a market segment we are not yet serving.

---

## Technology Stack Comparison

| Component | Us | Skills.sh | SkillHub | TrueFoundry |
| --- | --- | --- | --- | --- |
| Frontend | Unknown/TBD | Vercel/React | React (desktop + web) | React |
| Backend | Unknown/TBD | Node.js/Vercel | Node.js API | Python/FastAPI |
| Database | Unknown/TBD | Unknown | Unknown | PostgreSQL |
| Hosting | Unknown/TBD | Vercel Edge | Unknown | Cloud/self-host |
| Discovery | MCP + CLI | Interactive CLI (`npx skills find`) | API + Desktop app | UI + CLI + CI/CD |
| Notable tech advantage | Crypto signing + lockfile | Vercel CDN + npm distribution model | Desktop app + REST API | Enterprise RBAC + audit logs |

---

## Feature Matrix

| Feature | Us | Skills.sh | agentskill.sh | SkillHub | SkillsMP | Agensi | ClaudeSkills.info | AgentSkill.club | SkillsLLM | TrueFoundry | Microsoft/Google |
|---------|-----|-----------|---------------|----------|----------|--------|-------------------|-----------------|-----------|-------------|-----------------|
| CLI install command | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ | ✅ |
| MCP server integration | ✅ | ❌ | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| Cryptographic signing | ⭐ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Lockfile team versioning | ⭐ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | 🔶 | ❌ |
| Skill creation tooling | ⭐ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Eval harness for skills | ⭐ | ❌ | ❌ | 🔶 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Self-healing validation | ⭐ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| 40+ industry verticals | ⭐ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | 🔶 (Azure/Gemini only) |
| Orchestrator pattern | ⭐ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Multi-agent compatibility | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 🔶 | ✅ |
| Free / open-source | ✅ | ✅ | ✅ | 🔶 | ✅ | 🔶 | ✅ | ✅ | ✅ | ❌ | 🔶 |
| Catalog ≥ 400 skills | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ❌ | ❌ |
| Semantic / vector search | ❌ | ❌ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| Interactive CLI discovery | ❌ | ✅ (`npx skills find`) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Install trend leaderboard | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Automated security scanning | ❌ | ❌ | ✅ | ❌ | ❌ | ✅ | ❌ | ❌ | 🔶 | ❌ | ❌ |
| Security score per skill (0-100) | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| AI-graded quality scores | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Creator monetization | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Creator analytics dashboard | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Creator profiles | ❌ | ✅ | ✅ | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Trending / leaderboard | ❌ | ✅ | ❌ | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| 8-week install trend data | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Skill Stacks / bundles | 🔶 | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| REST API (OpenAPI) | ❌ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| In-IDE VS Code extension | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ (community ext) |
| Enterprise RBAC + audit logs | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| Official Anthropic skills | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Editorial / human curation | ❌ | ❌ | ❌ | 🔶 | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Skill request board | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Multilingual UI | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Self-hosted / on-premise | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |

Legend: ✅ = has it, 🔶 = partial, ❌ = missing, ⭐ = our edge

---

## Critical Gaps (Build Now)

### 1. Semantic / Vector Search

- **Who has it:** agentskill.sh, SkillHub, SkillsMP, LobeHub, TrueFoundry, Microsoft/Google (6/13 competitors)
- **Why it matters:** With 489+ skills, keyword search is broken. A developer asking "make my app accessible" won't find `/508-audit`. This is now table stakes — every major technical player has it. Skills.sh's `npx skills find` interactive type-to-search makes this gap even more visible.
- **Effort:** M
- **Implementation hint:** Embed skill descriptions at publish time using `text-embedding-3-small`. Store vectors in pgvector or Pinecone. Expose `/search?q=` on the web surface and a `--search` flag in the CLI. Upgrade the MCP `search_skills` tool from keyword to semantic matching.

### 2. REST API (OpenAPI 3.0)

- **Who has it:** Skills.sh, agentskill.sh, SkillHub, SkillsMP, TrueFoundry, Microsoft/Google (6/13 competitors)
- **Why it matters:** Without a REST API, the VS Code extension, CI/CD integrations, and third-party aggregators can't build on our registry. This is now a prerequisite for IDE integration, which is no longer "emerging" — a VS Code community extension (`formulahendry/vscode-agent-skills`) already exists in the marketplace with multi-registry support. We are not a registered source.
- **Effort:** M
- **Implementation hint:** Expose `/api/v1/skills`, `/api/v1/skills/{slug}`, `/api/v1/search`, `/api/v1/trending`. Document with OpenAPI 3.0. Rate-limit free tier, offer key-based access for teams. Register as a skill source in the VS Code Agent Skills extension.

### 3. Automated Security Scanning with Per-Skill Score

- **Who has it:** agentskill.sh (12 categories, 0–100 score), Agensi (8-point checklist) — 2/13 competitors
- **Why it matters:** Security scanning is now a market expectation. The developer community recommends pairing a "free browsing" registry with a "vetted" registry. We have cryptographic signing (tamper-evidence) but no content-level threat analysis. ClaudeSkills.info now hosts official Anthropic skills — if our registry has no content scanning, we are less trustworthy than Anthropic's own channel.
- **Effort:** M
- **Implementation hint:** Add a CI step to `registry-sync` that runs each new/updated SKILL.md through an LLM-based scanner checking 12 threat dimensions (prompt injection, data exfiltration, unauthorized network calls, dangerous shell commands, secret harvesting, obfuscation, credential access, privilege escalation, social engineering, scope creep, resource abuse, unauthorized persistence). Gate publication on PASS. Display 0–100 score badge on each skill page. Pair with existing cryptographic signing to form a "verified + safe" trust mark no competitor currently offers.

### 4. Trending / Install Leaderboard with Time-Series Data

- **Who has it:** Skills.sh (8-week trend data), SkillHub, Agensi (3/13 competitors)
- **Why it matters:** Skills.sh's top skill (find-skills, Vercel Labs) reached 2M installs in 5 months driven by visible install counts and trending signals. Without a leaderboard, new users have no signal on where to start. The market is now recommending a two-registry strategy; without install signals we won't be in the "discovery" slot.
- **Effort:** S
- **Implementation hint:** Track install counts server-side per skill per week. Add a `/trending` endpoint and homepage "trending this week" section. Display install count badge on each skill page. Store 8 weeks of weekly snapshots for trend sparklines.

---

## Strategic Gaps (Plan & Schedule)

### 5. Creator Monetization with Analytics

- **Who has it:** Agensi (80% creator split, top skills earning $500–$3,000/mo, with analytics, request board, piracy protection)
- **Why it matters:** Agensi is the only platform with a complete creator economy. Top-earning skills are specialized workflows ($1–$49 one-time) covering framework-specific testing, opinionated code review, and deployment automation — exactly the kind of expert-authored skills we need to scale beyond our internal production capacity. Without monetization, we cannot compete for expert author attention.
- **Effort:** L
- **Implementation hint:** Integrate Stripe Connect for creator payouts (80% to creators, 20% to platform). Add a "premium skills" tier ($1–$49). Free skills remain free. Premium skills get verified-author badges + security scan result. Add a skill request board (shows buyer demand before building). Add creator analytics (installs by week, referrer data, geographic breakdown).

### 6. AI-Graded Quality Scores

- **Who has it:** SkillHub (grades on Practicality, Clarity, Automation, Quality, Impact)
- **Why it matters:** With 489+ skills and 13+ competing registries, quality differentiation is the primary trust lever. Helps users pick the best skill when multiple cover the same task.
- **Effort:** M
- **Implementation hint:** At publish time, run an LLM evaluation of each SKILL.md against 5 quality dimensions. Store scores, surface as a badge on skill pages. Integrate with the existing eval harness in `/skill-creator`. Publish the scoring rubric as an open standard to drive ecosystem adoption.

### 7. Enterprise Features (RBAC, Versioning, Self-Hosted)

- **Who has it:** TrueFoundry (RBAC, audit logs, CI/CD, self-hosted), Microsoft/Google (enterprise integration) — new gap not in prior analysis
- **Why it matters:** TrueFoundry appeared in the Gartner Hype Cycle for Platform Engineering 2026. Enterprise teams need access control, audit trails, and on-premise deployment. With Microsoft and Google in the space, enterprise is becoming a distinct market segment. Our lockfile versioning is a first step but is not enterprise-grade.
- **Effort:** XL
- **Implementation hint:** Start with a self-hosted registry image (Docker). Add API key management and per-org install tracking. Enterprise RBAC and audit logs come after. This is a Q4+ effort but should be on the roadmap to avoid ceding the enterprise segment entirely to TrueFoundry and Microsoft.

---

## Differentiator Opportunities

### 8. In-IDE Integration (VS Code / JetBrains / Cursor)

- **Who has it:** VS Code community extension (`formulahendry/vscode-agent-skills`) — not us specifically, but VS Code native `chatSkills` contribution point exists
- **Urgency update:** This is no longer "emerging" — the gap is active. The community extension supports multiple skill sources; we need to register as one. A Cursor/Windsurf plugin would be even higher leverage given their 70% Fortune 1000 penetration.
- **Effort:** M (REST API required first; plugin registration is lower effort once API exists)

### 9. Interactive CLI Discovery

- **Who has it:** Skills.sh (`npx skills find` — type-to-search, interactive)
- **What we have:** `npx @skills-hub-ai/cli install <skill>` (install by name, no discovery)
- **Opportunity:** Add `npx @skills-hub-ai/cli find` with interactive type-to-search. Pair with semantic search backend. Skills.sh built their discovery moat with this; it is now the expected UX for CLI-based registries.
- **Effort:** S-M

### 10. Official Anthropic Skills Partnership

- **Who has it:** ClaudeSkills.info (hosts Anthropic's official PDF, DOCX, XLSX, frontend design, MCP builder skills)
- **Opportunity:** Secure a partnership or integration with Anthropic to host official skills on skills-hub.ai. Anthropic routing official skills through us would dramatically increase discoverability and trust. Frame it around our cryptographic signing — "the only registry where official Anthropic skills are signed and verifiable."
- **Effort:** M (relationship work + integration)

### 11. Skill Stacks — Named Curated Bundles

- **Who has it:** SkillHub (premium bundles), LobeHub (collections)
- **What we have:** 37 combo skills — not marketed as named "Stacks"
- **Opportunity:** Repackage combo skills as named "Skill Stacks" with use-case narratives ("Ship a production Next.js app — 7 skills included"). Could anchor a premium tier or act as the free showcase of the orchestrator pattern.
- **Effort:** S (repackaging existing content, no new code)

### 12. Skill Evolution Marketplace (Publicly Exposed)

- **Who has it:** Nobody
- **Opportunity:** skills-hub.ai has self-evolution telemetry and `/evolve` built into every v2.0.0+ skill. Exposing this publicly — "see how this skill evolved over 30 days, subscribe to auto-upgrade" — is a genuinely unique value proposition no competitor can replicate without rebuilding their stack.
- **Effort:** L

---

## Our Competitive Edges

1. **Cryptographic signing** — The only platform that signs SKILL.md files for tamper-evidence. Unmatched. Pair with security scanning to form "verified + safe" — the strongest trust mark in the ecosystem.
2. **Lockfile team versioning** — `.skills.json` enables reproducible team installs. TrueFoundry has versioning but requires their platform. We offer it open-source, compatible with any agent.
3. **Skill creation + eval tooling** — `/skill-creator` with quantitative evals, variance analysis, and eval-viewer is a full skill R&D environment. No competitor ships this. SkillHub has a rudimentary version.
4. **Industry vertical depth** — 40+ verticals including social-impact niches (FOIA, elder care, emergency response, grants). Microsoft/Google cover only Azure/Gemini domains. No one else comes close.
5. **Orchestrator pattern** — Main-skill + sub-skill routing documented as an architectural approach. Running `/secure` audits 7 dimensions automatically. No competitor documents this.
6. **Self-healing + self-evolution telemetry** — Built into every v2.0.0+ skill. No competitor ships skills with automatic failure recovery and usage telemetry.
7. **SKILL.md open standard leadership** — Adopted by 26+ platforms including Microsoft, Google, and the Linux Foundation's Agentic AI Foundation. We are positioned as a founding community registry.
8. **UX design skills suite** — 28+ UX-focused skills going well beyond developer tooling. No competitor has this breadth in design workflows.

---

## Market Positioning (Blue Ocean Analysis)

| Strategy | Features | Rationale |
|----------|----------|-----------|
| ELIMINATE | Scraped/unvetted mega-catalogs | Can't win vs. SkillsMP (800K) or Skills.sh (669K) on volume; fight on trust |
| REDUCE | Breadth of "one of each" skills across all frameworks | Quality over quantity — expert-authored, deeply tested skills beat shallow coverage |
| RAISE | Security trust mark (signing + scanning), skill quality scoring, skill tooling depth | These are our existing edges — elevate them to be unmissable, not footnotes |
| CREATE | Public skill evolution feed, creator economy with quality gates, official Anthropic channel | No competitor has self-evolution telemetry or an officially-partnered Anthropic registry |

**Recommended positioning:** "The only AI agent skills registry where every skill is cryptographically signed, security-scanned, and built to improve itself — the trust layer the ecosystem needs."

---

## Industry Trends

| Trend | Adoption Stage | Competitors With It | Our Status | Recommendation |
|-------|---------------|--------------------|-----------:|----------------|
| Security scoring per skill (0-100) | Early majority | agentskill.sh, Agensi (2/13) | ❌ Missing | Build now — becoming baseline expectation |
| Semantic / vector search | Early majority | 6/13 competitors | ❌ Missing | Build now — discovery is broken above 200 skills |
| Install trend leaderboards | Early majority | Skills.sh, SkillHub, Agensi (3/13) | ❌ Missing | Build now — drives viral loop |
| REST API for skills registries | Late majority | 6/13 competitors | ❌ Missing | Build this sprint — prerequisite for IDE integrations |
| Creator monetization for AI skills | Early majority | Agensi (live, $500–$3K/skill/mo top earners) | ❌ Missing | Plan for Q3 — content flywheel won't scale without it |
| Interactive CLI discovery | Early adopter | Skills.sh (1/13) | ❌ Missing | S effort — `npx @skills-hub-ai/cli find` with type-to-search |
| In-IDE marketplace panels | Early majority | VS Code community ext (not us) | ❌ Missing | Register as skill source — API first, then IDE extension |
| MCP-native distribution | Early majority | SkillHub, SkillsMP, us, LobeHub | ✅ Have it | Expand — publish to mcp.so and glama.ai |
| Enterprise RBAC / self-hosted | Early adopter | TrueFoundry, Microsoft, Google | ❌ Missing | Long-term — defend against enterprise cede via Docker image |
| Official vendor skill channels | Early adopter | ClaudeSkills.info (Anthropic), Microsoft, Google | ❌ Missing | Partnership play — official Anthropic partnership closes this |
| AI-quality-scored content | Early adopter | SkillHub (1/13) | ❌ Missing | Integrate with existing eval harness — M effort |
| Skill bundling/stacks | Early adopter | SkillHub, LobeHub (2/13) | 🔶 Partial | Repackage combo skills as named Stacks — S effort |
| Skill demand signaling (request boards) | Early adopter | Agensi (1/13) | ❌ Missing | S effort, drives community contribution |
| Cross-agent skill standard governance | Late majority | All platforms + Linux Foundation | ✅ We lead | Publish spec docs + governance — defensible moat |

---

## Recommended Roadmap

### Sprint 1 — Quick Wins (1–2 weeks)

1. **Trending leaderboard** — CRITICAL pressure, S effort. Surface install count data on the homepage and CLI. Trending → discovery → installs → signal. Skills.sh built their moat here.
2. **Interactive CLI discovery** — HIGH pressure, S–M effort. `npx @skills-hub-ai/cli find` with type-to-search. Matches the Skills.sh UX that users now expect.
3. **Skill Stacks repackaging** — HIGH pressure, S effort. Rebrand 37 combo skills as "Skill Stacks" with curated use-case stories. Pure positioning, no new code.
4. **Register in VS Code Agent Skills extension** — HIGH pressure, S effort. `formulahendry/vscode-agent-skills` supports custom GitHub repositories as skill sources. Add skills-hub.ai as a listed source without waiting for full REST API.

### Next Quarter — Strategic (Q3 2026)

5. **REST API (OpenAPI 3.0)** — CRITICAL pressure, M effort. Required by 6/13 competitors. Prerequisite for full IDE extensions, CI integrations, and creator dashboard.
6. **Semantic search** — CRITICAL pressure, M effort. 489 skills is too many to browse. Embedding pipeline + `/search` endpoint + CLI flag. Upgrade MCP `search_skills` tool.
7. **Automated security scanning with 0–100 score** — HIGH pressure, M effort. Pair our cryptographic signing with content scanning. Forms "verified + safe" moat no competitor has. Gate new skill publications on PASS.
8. **AI-graded quality scores** — HIGH pressure, M effort. Extend existing eval harness to score all published skills. Differentiates us from scrapers and volume-first registries.

### Future — Differentiators (Q4 2026+)

9. **Creator monetization + analytics** — HIGH pressure, L effort. Stripe Connect + premium tier + analytics dashboard + piracy protection. Agensi proves the market exists.
10. **Official Anthropic partnership** — HIGH pressure, M effort (relationship). ClaudeSkills.info hosts Anthropic's official skills; we should be that channel, backed by our cryptographic signing.
11. **Enterprise self-hosted image** — MEDIUM pressure, XL effort. Docker registry image for enterprise teams who need RBAC and on-premise deployment. Defense against TrueFoundry/Microsoft in enterprise accounts.
12. **Skill evolution marketplace** — LOW pressure, L effort. Expose self-evolution telemetry publicly. Unique differentiator that no competitor can replicate.

---

## Summary

- **Total features tracked across competitors:** 34
- **We have:** 13 (38%)
- **Partial:** 2 (6%)
- **Missing:** 19 (56%)
- **Our edges:** 8 (cryptographic signing, lockfile versioning, skill creation + eval tooling, industry vertical depth, orchestrator pattern, self-healing/evolution, UX design suite, SKILL.md standard leadership)
- **Critical gaps to close:** 4 (semantic search, REST API, trending leaderboard, security scanning)
- **Biggest threat:** **Big Tech Flanking** — Microsoft and Google have entered the ecosystem directly with official skill registries, enterprise RBAC, and IDE-native integration. ClaudeSkills.info has secured Anthropic's official skills. We risk being squeezed between volume (Skills.sh/SkillsMP) and enterprise (TrueFoundry/Microsoft/Google) unless we execute on trust quality (signing + scanning) and creator economy simultaneously.
- **Biggest opportunity:** **"Verified + Safe" trust mark as the ecosystem's quality layer** — We are the only registry with cryptographic signing. Adding automated security scanning closes the content-level trust gap that agentskill.sh is beginning to own. Pair with an official Anthropic partnership and a creator economy to form a flywheel: vetted skills → expert authors → users → more authors. This moat cannot be replicated by scrapers or big tech without rebuilding from scratch.

---

## What Changed Since June 30, 2026

- **Three new community registries identified:** ClaudeSkills.info (658+ skills including official Anthropic skills), AgentSkill.club (3,640+ GitHub-sourced skills), SkillsLLM (1,600+ security-vetted skills)
- **Two tech giants entered the space:** Microsoft Skills (microsoft.github.io/skills, 100+ Azure/Microsoft domain skills) and Google Gemini Enterprise Skill Registry — both with enterprise RBAC and IDE-native support
- **TrueFoundry** appeared in the Gartner Hype Cycle for Platform Engineering 2026 as an enterprise skills registry — a new segment we are not yet addressing
- **In-IDE extension gap is now ACTIVE:** `formulahendry/vscode-agent-skills` is live on VS Code Marketplace with multi-registry support; skills-hub.ai is not a registered source
- **Skills.sh added interactive discovery:** `npx skills find` (type-to-search) sets a new UX bar for CLI-based registries
- **Market grew to 13+ registries** — developer community now recommends a two-registry strategy (one for browsing, one for vetted) — we need to own the "vetted" slot
- **ClaudeSkills.info hosts official Anthropic skills** — a trust signal gap for us; official-adjacent content is not in our registry

---

## Sources

- [skills.sh](https://www.skills.sh) — Vercel-backed npm-style skills registry
- [Vercel changelog: Introducing skills](https://vercel.com/changelog/introducing-skills-the-open-agent-skills-ecosystem)
- [InfoQ: Vercel Introduces Skills.sh](https://www.infoq.com/news/2026/02/vercel-agent-skills/)
- [agentskill.sh](https://agentskill.sh/) — Security-focused skills directory
- [claudeskills.info](https://claudeskills.info/) — Free curated Claude Code skills including official Anthropic skills
- [agentskill.club](https://www.agentskill.club/) — Community-driven GitHub-sourced skills library
- [SkillsLLM](https://skillsllm.com/) — GitHub-centric security-vetted skills index
- [lobehub.com/skills](https://lobehub.com/skills) — LobeHub Skills Marketplace
- [skillhub.club](https://www.skillhub.club/) — SkillHub with desktop app + MCP server
- [SkillHub API docs](https://www.skillhub.club/docs/api)
- [skillsmp.com](https://skillsmp.com/) — SkillsMP index
- [agensi.io](https://www.agensi.io/) — Agensi curated marketplace
- [agensi.io — Sell Your Skills guide](https://www.agensi.io/learn/agent-skills-marketplace-sell-your-skills)
- [agensi.io — Marketplace Comparison 2026](https://www.agensi.io/learn/ai-agent-skills-marketplace-comparison-2026)
- [agensi.io — Every AI Agent Skills Marketplace 2026](https://www.agensi.io/learn/best-ai-agent-skills-marketplaces-2026)
- [claudemarketplaces.com](https://claudemarketplaces.com/)
- [TrueFoundry Skills Registry](https://www.truefoundry.com/skills-registry)
- [TrueFoundry: Introducing Agent Skills Registry](https://www.truefoundry.com/blog/introducing-skills-registry-reusable-agent-skills-for-production-ai-systems)
- [Microsoft Skills](https://microsoft.github.io/skills/)
- [Microsoft Agent Framework: Agent Skills](https://learn.microsoft.com/en-us/agent-framework/agents/skills)
- [Google Gemini Enterprise Skill Registry](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/skill-registry)
- [VS Code Agent Skills Extension](https://marketplace.visualstudio.com/items?itemName=formulahendry.agent-skills)
- [VS Code: Use Agent Skills](https://code.visualstudio.com/docs/agent-customization/agent-skills)
- [KDnuggets: Top 5 Agent Skill Marketplaces](https://www.kdnuggets.com/top-5-agent-skill-marketplaces-for-building-powerful-ai-agents)
- [skills-hub.ai](https://skills-hub.ai/)
