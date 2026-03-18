# Competitive Gap Analysis: Skills Hub Registry

**Date:** 2026-03-17
**Previous:** 2026-03-01
**Scope:** AI coding agent skill/plugin marketplaces, curated registries, community aggregators

---

## Our Product

- **What it does:** Skills Hub Registry is a curated, open-source marketplace of 366 autonomous Claude Code agents covering the complete SDLC plus 40 industry verticals, 11 social-impact sectors, and 30 multi-skill orchestration chains. It powers the skills-hub.ai marketplace.
- **Target user:** Software engineers and development teams using Claude Code who need production-ready, autonomous workflow automation across build, test, deploy, security, compliance, and domain-specific operations.
- **Core value prop:** Deepest industry vertical coverage (40 sectors), fully autonomous execution (no questions asked), composable multi-skill chains, and self-improving meta-skills — all free and open source.
- **Tech stack:** YAML frontmatter + Markdown instructions (SKILL.md), Git distribution, GitHub Actions CI on self-hosted runners, validation scripts.
- **Features implemented:** 366 skills across 13 categories.

---

## Competitive Landscape

| Competitor | Positioning | Market Position | Skill/Plugin Count | Distribution |
|-----------|-------------|-----------------|-------------------|--------------|
| **Claude Code Plugins Plus** (BrightCoding/Intent Solutions) | Enterprise-grade plugin platform with CLI package manager and empirical validation | Challenger | 270+ plugins / 1,537 skills | CLI (`ccpi`), npm |
| **OpenClaw ClawHub** | Largest open community skill marketplace for AI agents | Leader (volume) | 5,700+ skills (3,500 community) | CLI + web marketplace |
| **Cursor Marketplace** | Curated enterprise plugin marketplace for Cursor IDE | Leader (enterprise) | 40+ curated plugins | One-click IDE install |
| **Anthropic Official Plugins** | Official, vetted Claude Code plugins | Leader (authority) | ~50-100 production-ready | GitHub, `/plugin install` |
| **MCP Server Directories** (mcp.so, mcpservers.org, mcpmarket.com) | Aggregated MCP server discovery | Adjacent/complementary | Tens of thousands | npm, Docker |

### Competitor Profiles

**Claude Code Plugins Plus** — Most direct competitor. 270+ plugins organized into 42 SaaS skill packs with 1,537 embedded agent skills. Key differentiator: CLI package manager (`ccpi`) with search, install, update, validate operations. Includes 11 Jupyter notebooks for interactive tutorials, schema compliance validation, tool permission declarations, and sandboxing. Open-source with optional $5/mo sponsorship for priority support.

**OpenClaw ClawHub** — Largest skill volume (5,700+) but significant quality/security problems. Snyk's ToxicSkills report found 13.4% of skills have critical security issues; Bitdefender found 17-20% contain malicious code. No manual review before listing. Growing at 120-180 new skills/week from ~1,400 publishers. Star-based rating system (top skill: GitHub Actions at 2,890 stars).

**Cursor Marketplace** — Enterprise-curated with major brand partners (AWS, Figma, Stripe, Linear, Datadog, Slack, GitLab, Amplitude). 40+ plugins bundling MCP servers, skills, subagents, hooks, and rules. One-click install in Cursor IDE. Team/Enterprise plans enable private marketplace distribution. Completely different ecosystem (Cursor, not Claude Code).

**Anthropic Official Plugins** — Small curated set from Anthropic themselves. Includes Code Review, Frontend Design, Context7 (live docs injection), Superpowers (TDD framework). High authority but limited scope. Distribution via official GitHub repo and `/plugin install` command.

**MCP Server Directories** — Adjacent market. Provide external tool connections (databases, APIs, services) rather than autonomous skill execution. Complementary to skills — skills *use* MCP servers. Growing rapidly with the 2026 MCP roadmap (Server Cards, stateless streaming HTTP).

---

## Pricing Comparison

| Tier / Profile | Us | Plugins Plus | OpenClaw ClawHub | Cursor Marketplace | Anthropic Official |
|---------------|-----|-------------|-----------------|-------------------|-------------------|
| Skills/plugins | Free | Free (OSS) | Free | Free (with plan) | Free |
| Platform cost | Claude Pro $20/mo | Claude Pro $20/mo | API costs $5-30/mo | Cursor Pro $20/mo | Claude Pro $20/mo |
| Premium support | None | $5/mo sponsor | Cloud $39/mo | Business $40/seat/mo | N/A |
| Enterprise | None | Custom dev available | N/A | Enterprise (custom) | N/A |
| Pricing model | Fully free/OSS | Freemium + sponsorship | Free + BYOK API | Bundled with IDE sub | Free |

**Key pricing insights:**
- All skill registries are free — the cost is in the underlying AI platform subscription
- We are price-competitive (free) but lack premium support or enterprise tiers that could generate revenue
- Cursor's enterprise play (private marketplaces, team management) is a model we don't address
- OpenClaw's managed cloud ($39/mo) shows demand for hosted skill execution

---

## Technology Stack Comparison

| Component | Us | Plugins Plus | OpenClaw ClawHub | Cursor Marketplace | Anthropic Official |
|----------|-----|-------------|-----------------|-------------------|-------------------|
| Skill format | SKILL.md (YAML+MD) | SKILL.md (YAML+MD) | SKILL.md (YAML+MD) | Plugin manifest (JSON+MD) | Plugin manifest |
| Distribution | Git clone | CLI (`ccpi`) + npm | CLI + web marketplace | One-click IDE install | GitHub + `/plugin install` |
| Package manager | None | Yes (`ccpi`) | Yes (`openclaw skill`) | Built into Cursor | Built into Claude Code |
| Search/discovery | Manual (README) | CLI search + web catalog | Semantic search + web | IDE marketplace UI | GitHub browse |
| Validation | Shell script CI | Schema validation + empirical verification | Community reports | Curated review | Manual curation |
| Quality assurance | YAML frontmatter checks | 4,300+ lines of issue detection | Auto-hide after 3 reports | Verified partners only | Anthropic review |
| Sandboxing | None | Tool permission declarations | None (security issues) | IDE sandbox | Claude Code sandbox |
| Tutorials | None | 11 Jupyter notebooks | None | Plugin docs | Official docs |
| Ratings/metrics | None | None | Stars (community) | None visible | None |
| Private/team distribution | None | None | None | Team marketplace (Enterprise) | None |

**Tech stack assessment:** Behind on distribution infrastructure. We have the deepest skill content but the weakest delivery mechanism. Every competitor except us has a CLI or one-click install path.

---

## Feature Matrix

### Distribution & Developer Experience

| Feature | Us | Plugins Plus | OpenClaw | Cursor Mkt | Pressure | Effort |
|---------|-----|-------------|----------|------------|----------|--------|
| CLI install command | N | Y | Y | Y (IDE) | CRITICAL | M |
| Semantic search | N | N | Y | Y (IDE) | HIGH | L |
| One-click install | N | N | N | Y | MEDIUM | L |
| Web marketplace UI | N (separate) | Y | Y | Y | HIGH | XL |
| Package versioning/pinning | ~ | Y | Y | Y | HIGH | M |
| Hot-reload skills | N | N | Y | N | LOW | M |
| Interactive tutorials | N | Y | N | N | LOW | M |
| Private/team distribution | N | N | N | Y | MEDIUM | L |
| Adoption metrics/ratings | N | N | Y | N | MEDIUM | M |
| Schema validation | Y | Y | N | Y | — | — |
| CI/CD validation pipeline | Y | Y | N | Y | — | — |

### Content & Coverage

| Feature | Us | Plugins Plus | OpenClaw | Cursor Mkt | Pressure | Effort |
|---------|-----|-------------|----------|------------|----------|--------|
| Build/scaffold skills | Y (22) | Y | Y | ~ | — | — |
| Test generation skills | Y (13) | Y | Y | N | — | — |
| Security/compliance audit | Y (13) | ~ | N | ~ (Snyk, Semgrep) | — | — |
| Industry verticals (40+) | Y (40) | N | N | N | — | — |
| Social impact sectors | Y (11) | N | N | N | — | — |
| Multi-skill chains | Y (30) | ~ | N | ~ | — | — |
| Meta/self-improving skills | Y (9) | N | N | N | — | — |
| Gaming skills | Y (15+) | N | ~ | N | — | — |
| Mobile skills | Y (10+) | N | ~ | N | — | — |
| UX/design skills | Y (6) | N | ~ | Y (Figma) | — | — |
| Integration skills (auth, pay) | Y (9) | ~ | Y | Y (Stripe, etc.) | — | — |
| External tool connections (MCP) | N | ~ | Y | Y | HIGH | M |
| Third-party API plugins | N | Y | Y | Y | HIGH | L |
| Community-contributed skills | N | ~ | Y | N | MEDIUM | M |

### Quality & Security

| Feature | Us | Plugins Plus | OpenClaw | Cursor Mkt | Pressure | Effort |
|---------|-----|-------------|----------|------------|----------|--------|
| Curated quality control | Y | Y | N (13-20% malicious) | Y | — | — |
| Empirical verification | N | Y | N | N | MEDIUM | L |
| Tool permission declarations | N | Y | N | Y | HIGH | M |
| Security scanning of skills | N | ~ | N (community reports) | Y | HIGH | M |
| Contribution guidelines | N | Y | Y | Y | HIGH | S |
| Sandboxed execution | N | Y | N | Y | HIGH | L |

---

## Critical Gaps (Build Now)

### 1. CLI Install / Package Manager
- **Who has it:** Plugins Plus (`ccpi`), OpenClaw (`openclaw skill install`), Cursor (IDE-native)
- **Why it matters:** Without a CLI, users must manually clone repos and copy files. This is the #1 friction point for adoption. Every other marketplace has solved this.
- **Effort:** M
- **Implementation hint:** Build a `skills-hub` CLI (Node.js or shell) that reads from a catalog index file, supports `search`, `install`, `update`, `list`. Publish to npm. Alternatively, integrate with Claude Code's native `/plugin install` mechanism.

### 2. Contribution Guidelines (CONTRIBUTING.md)
- **Who has it:** Plugins Plus, OpenClaw, Cursor, Anthropic Official
- **Why it matters:** Without contribution docs, the registry appears closed/unmaintained. Community contribution is table stakes for any open-source marketplace.
- **Effort:** S
- **Implementation hint:** Add `CONTRIBUTING.md` with skill submission format, quality checklist, PR template, and review process.

### 3. Tool Permission Declarations
- **Who has it:** Plugins Plus, Cursor Marketplace
- **Why it matters:** Users need to know what file/network/system access a skill requires before installing. Trust is the #1 concern (see OpenClaw's 13-20% malicious rate).
- **Effort:** M
- **Implementation hint:** Add `permissions` field to SKILL.md frontmatter (e.g., `permissions: [file_read, file_write, network, bash]`). Update validation script to enforce.

### 4. MCP Server Integration
- **Who has it:** OpenClaw (bridge pattern), Cursor (bundled), Plugins Plus (partial)
- **Why it matters:** MCP is the emerging standard for connecting AI agents to external tools. Skills that can leverage MCP servers (databases, APIs, services) are far more powerful. The 2026 MCP roadmap is accelerating adoption.
- **Effort:** M
- **Implementation hint:** Add MCP bridge skills or document how to compose skills with MCP servers. Add `mcp_servers` field to SKILL.md for declaring MCP dependencies.

---

## Strategic Gaps (Plan & Schedule)

### 1. Web Marketplace / Search API
- **Pressure:** HIGH
- **Effort:** XL
- **Who has it:** OpenClaw (ClawHub), Cursor (IDE marketplace), Plugins Plus (web catalog)
- **Why it matters:** Discovery is impossible without search. README browsing doesn't scale at 366 skills. The skills-hub.ai frontend exists separately but the registry itself has no search infrastructure.
- **Implementation hint:** Generate a `catalog.json` index from SKILL.md frontmatter (name, description, category, tags, version). Serve via GitHub Pages or API. Frontend reads this index.

### 2. Security Scanning / Sandboxing
- **Pressure:** HIGH
- **Effort:** L
- **Who has it:** Plugins Plus (empirical verification), Cursor (partner vetting)
- **Why it matters:** As the registry grows beyond curated content, trust becomes critical. OpenClaw's cautionary tale (13-20% malicious) shows what happens without quality gates.

### 3. Package Versioning & Dependency Resolution
- **Pressure:** HIGH
- **Effort:** L
- **Who has it:** Plugins Plus, OpenClaw (semver), Cursor
- **Why it matters:** Skills reference sub-skills by name but not version. Breaking changes in a sub-skill can cascade through combo chains.

---

## Differentiator Opportunities

### 1. Industry Vertical Depth (MEDIUM pressure, already built)
No competitor comes close to 40 industry verticals + 11 social-impact sectors. This is unique positioning. Plugins Plus, OpenClaw, and Cursor focus on generic dev tools — none have healthcare compliance, fintech launch pipelines, or agricultural risk modeling.

### 2. Multi-Skill Orchestration Chains (MEDIUM pressure, already built)
30 combo chains that orchestrate 2-6 skills in sequence/parallel. No competitor has this level of workflow composition. Cursor plugins can bundle components but don't have pre-built orchestration pipelines.

### 3. Self-Improving Meta Skills (LOW pressure, already built)
`/evolve`, `/recall`, `/metrics`, `/promote` — no competitor has skills that analyze their own performance and patch themselves. This is genuinely novel.

### 4. Compliance-Ready Industry Pipelines (MEDIUM pressure, already built)
HIPAA, SOC2, GDPR, PCI-DSS, FDA, NERC CIP — pre-built compliance audit skills with regulatory section mappings. No competitor offers this depth.

---

## Our Competitive Edges

| Edge | Description | Competitors With Similar |
|------|-------------|------------------------|
| **Industry vertical depth** | 40 sectors with domain-specific regulatory, operational, and analytical skills | 0/4 |
| **Social impact coverage** | 11 sectors (education, housing, mental health, elder care, etc.) | 0/4 |
| **Multi-skill chains** | 30 orchestrated pipelines (e.g., `/fintech-launch`, `/game-launch`, `/mobile-publish`) | 0/4 (Cursor has plugin bundles but no pre-built chains) |
| **Self-improving system** | Meta skills that analyze performance and patch regressions | 0/4 |
| **Compliance depth** | HIPAA, SOC2, GDPR, PCI-DSS, FDA with CFR-level mapping | 0/4 (some have basic security scans) |
| **Fully autonomous execution** | Every skill runs without asking questions | 1/4 (some Plugins Plus skills) |
| **Curated quality** | All 366 skills author-reviewed, no community-submitted malware risk | 2/4 (Cursor, Anthropic Official) |

---

## Market Positioning (Blue Ocean Analysis)

| Strategy | Features | Rationale |
|----------|----------|-----------|
| **ELIMINATE** | Interactive tutorials, Jupyter notebooks | Not core to the value prop. Skills are self-documenting. Tutorials add maintenance burden for low user demand in a power-user market. |
| **REDUCE** | Web marketplace complexity | Don't build a full marketplace platform. A searchable catalog index (`catalog.json` + static site) covers 90% of discovery needs at 10% of the cost. |
| **RAISE** | Industry vertical depth, compliance rigor, orchestration chains | Go deeper where no competitor plays. Add more verticals, more compliance frameworks, more complex multi-skill pipelines. This is uncontested space. |
| **CREATE** | "Compliance-as-Skills" positioning — pre-built regulatory audit pipelines that enterprises can drop into any codebase | No competitor offers domain-specific compliance automation at this depth. Position as the enterprise compliance automation layer for AI-assisted development. |

**Recommended positioning:** *"The deepest AI coding automation library — 40 industry verticals, regulatory compliance built-in, and self-improving orchestration chains that no general-purpose plugin marketplace can match."*

---

## Industry Trends

| Trend | Adoption Stage | Competitors With It | Our Status | Recommendation |
|-------|---------------|---------------------|------------|----------------|
| CLI package managers for skills | Mainstream | Plugins Plus, OpenClaw, Cursor | MISSING | **Build now** — table stakes |
| MCP server integration | Early mainstream | OpenClaw, Cursor, Plugins Plus | MISSING | **Build now** — emerging standard |
| Multi-agent orchestration | Early adopter | Cursor (subagents), Plugins Plus | PARTIAL (combo chains) | **Raise** — deepen our orchestration |
| Skill permission/security declarations | Early mainstream | Plugins Plus, Cursor | MISSING | **Build now** — trust is critical |
| Private/team skill distribution | Early adopter | Cursor (Enterprise) | MISSING | **Defer** — enterprise play, not our market yet |
| AI-generated skills | Bleeding edge | None fully | PARTIAL (skill-creator) | **Watch** — our skill-creator meta-skill is ahead |
| Skill analytics/telemetry | Early adopter | OpenClaw (stars) | MISSING | **Plan** — adoption data drives prioritization |
| Cross-platform skills (Claude + Cursor + Copilot) | Bleeding edge | None | MISSING | **Watch** — standards not settled |

---

## Recommended Roadmap

### Sprint 1 — Quick Wins (close critical gaps)

1. **CONTRIBUTING.md + PR template** — CRITICAL pressure, S effort. Unblocks community contributions and signals project health. Half a day.
2. **Permission declarations in SKILL.md** — HIGH pressure, M effort. Add `permissions` field to frontmatter, update validation script, update template. 1-2 days.
3. **Catalog index generation** — HIGH pressure, M effort. Script to generate `catalog.json` from all SKILL.md files. Enables search, enables future CLI. 1 day.
4. **MCP dependency declarations** — HIGH pressure, S effort. Add `mcp_servers` field to SKILL.md frontmatter for skills that should work with MCP servers. 1 day.

### Next Quarter — Strategic

5. **CLI package manager** — CRITICAL pressure, M-L effort. `npx skills-hub install <skill>` or `npx skills-hub search <query>`. Reads from catalog.json. 1-2 weeks.
6. **Searchable web catalog** — HIGH pressure, L effort. Static site (GitHub Pages) reading catalog.json with category filters, keyword search, skill detail pages. 1 week.
7. **Security scanning pipeline** — HIGH pressure, L effort. Static analysis of skill instructions for dangerous patterns (unrestricted bash, network access without declaration, credential handling). 1 week.
8. **Versioned dependency resolution** — HIGH pressure, L effort. Combo chains reference sub-skills by name + version range. Breaking change detection. 1 week.

### Future — Differentiators

9. **More industry verticals** — Expand into education technology, legal technology, proptech, insurtech with deeper skill chains.
10. **Cross-platform skill format** — Investigate compatibility with Cursor plugin format and OpenClaw skill format. Publish skills that work across platforms.
11. **Skill analytics** — Track installs, usage patterns, and success rates to prioritize maintenance and evolution.
12. **Enterprise private catalogs** — Allow teams to host internal skill registries with the same tooling.

---

## Summary

| Metric | Value |
|--------|-------|
| **Total features across competitors** | 28 (distribution, content, quality categories) |
| **We have** | 14 (50%) |
| **Partial** | 4 (14%) |
| **Missing** | 10 (36%) |
| **Our edges** | 7 (industry depth, social impact, chains, meta-skills, compliance, autonomous, curated quality) |
| **Critical gaps to close** | 4 (CLI install, CONTRIBUTING.md, permissions, MCP integration) |
| **Pricing position** | Competitive (free, same as most competitors) |
| **Tech stack assessment** | Behind on distribution infrastructure, ahead on content depth |
| **Biggest threat** | **Claude Code Plugins Plus** — same ecosystem, has CLI package manager, empirical validation, and growing fast. If they add industry verticals, our main differentiator narrows. |
| **Biggest opportunity** | **"Compliance-as-Skills" positioning** — no competitor offers domain-specific regulatory automation. Enterprises need HIPAA, SOC2, GDPR, PCI-DSS compliance baked into their development workflow. We have 13 security/compliance skills + 40 industry verticals. Position as the enterprise compliance layer. |

---

## New Entrants & Aggregators (identified 2026-03-17)

| Competitor | Positioning | Skill Count | Differentiator |
|-----------|-------------|-------------|----------------|
| **claude-skill-registry** (majiayu000) | Crawled skill aggregator | 82,569 deduplicated (162K+ crawled) | Volume play — auto-scraped SKILL.md files from GitHub. No curation or quality control. |
| **SkillHub.club** | AI-evaluated skills marketplace | Unknown | AI quality ranking (S/A/B-rank system). Differentiating on automated skill scoring. |
| **claudeskills.info** | Official-focused marketplace | Unknown | Focuses on Anthropic official skills. Curated, narrow scope. |
| **SkillsMP.com** | Multi-agent skill marketplace | 500,000+ claimed | Cross-platform (Claude, Codex, ChatGPT, Gemini). Broadest agent coverage but quality unverified. |

**Key signals:**
- A HackerNoon article documents a developer building a "visual workbench" for managing Claude Code skills — discovery/management is a real pain point users are actively trying to solve.
- Multiple editorial roundups exist (Medium, Composio, Firecrawl) covering "best Claude Code skills" — **Skills Hub Registry does not appear in any of them yet**.
- The `github.com/topics/claude-skills-hub` topic exists on GitHub.
- claude-skill-registry's 82K deduplicated entries dwarf our 366 but are uncurated scrapes with no quality assurance.

**Action items:**
1. Submit Skills Hub Registry to editorial roundup authors (Medium/@unicodeveloper, Composio, Firecrawl) for inclusion.
2. Create a GitHub topic listing under `claude-skills-hub`.
3. Consider publishing a `catalog.json` that aggregators and visual tools can consume.

---

## Sources

- [Claude Code Plugins Plus (BrightCoding)](https://www.blog.brightcoding.dev/2026/02/07/claude-code-plugins-plus-270-ai-agent-tools-that-transform-development)
- [OpenClaw Skills Guide (AI Tools Kit)](https://www.aitoolskit.io/agents/openclaw-plugins-extensions-guide-2026)
- [Claude Code Plugins Review (AI Tool Analysis)](https://aitoolanalysis.com/claude-code-plugins/)
- [Cursor Marketplace](https://cursor.com/marketplace)
- [Cursor Marketplace Launch Blog](https://cursor.com/blog/marketplace)
- [Anthropic Official Plugins (GitHub)](https://github.com/anthropics/claude-plugins-official)
- [MCP Servers Directory](https://mcpservers.org/)
- [MCP 2026 Roadmap](http://blog.modelcontextprotocol.io/posts/2026-mcp-roadmap/)
- [Claude Code Alternatives (DigitalOcean)](https://www.digitalocean.com/resources/articles/claude-code-alternatives)
- [OpenClaw vs Claude Code (DataCamp)](https://www.datacamp.com/blog/openclaw-vs-claude-code)
- [Cursor vs GitHub Copilot 2026 (Morphllm)](https://www.morphllm.com/comparisons/cursor-vs-copilot)
- [AI Agent Skills Boom 2026 (SoloBusinessHub)](https://www.solobusinesshub.com/trend-watch/ai-agent-skills-boom-2026/)
- [claude-skill-registry (GitHub)](https://github.com/majiayu000/claude-skill-registry)
- [SkillHub.club — AI Skills Marketplace](https://www.skillhub.club/)
- [10 Must-Have Skills for Claude in 2026 (Medium)](https://medium.com/@unicodeveloper/10-must-have-skills-for-claude-and-any-coding-agent-in-2026-b5451b013051)
- [Top 10 Claude Code Skills (Composio)](https://composio.dev/content/top-claude-skills)
- [Best Claude Code Skills 2026 (Firecrawl)](https://www.firecrawl.dev/blog/best-claude-code-skills)
- [Visual Workbench for Claude Code Skills (HackerNoon)](https://hackernoon.com/i-built-a-visual-workbench-because-managing-claude-code-skills-was-driving-me-crazy)
