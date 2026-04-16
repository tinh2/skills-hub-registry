# Competitive Gap Analysis — Skills Hub Registry

> Generated 2026-04-09 | Domain: AI coding agent skills/plugin registry and marketplace

---

## Our Product

- **What it does:** Skills Hub Registry is a curated collection of 425+ production-tested autonomous AI agent skills organized into 13 categories covering the full software development lifecycle — from project scaffolding through deployment, security audits, domain-specific analysis across 40+ industry verticals, video production, and game development.
- **Target user:** Developers using Claude Code (and increasingly Cursor, Codex CLI, Gemini CLI) who need turn-key AI-driven assistance for any software task.
- **Core value prop:** Zero-question autonomy with self-healing validation and self-evolution telemetry — invoke a single skill (or a pre-built combo chain) and it runs end-to-end, retries on failure, and logs execution telemetry so a meta-skill can patch underperforming skills over time.
- **Features implemented:** 425+ skills across 13 categories, 34 combo pipeline chains, 195+ domain-specific analysis skills, quality scoring rubric (0-100), CI validation, self-healing blocks, self-evolution telemetry, meta-skills for skill lifecycle management.

---

## Competitive Landscape

| Competitor | Positioning | Pricing | Market Position | Feature Count |
|-----------|-------------|---------|-----------------|---------------|
| [Skills.sh (Vercel)](https://skills.sh) | "npm for AI agents" — open CLI + registry/leaderboard | Free / Open Source | Leader | 350,000+ packages |
| [SkillsMP](https://skillsmp.com) | Largest search/discovery layer aggregating GitHub skills | Free | Leader | 700,000+ indexed |
| [LobeHub Skills](https://lobehub.com/skills) | Polished marketplace with multi-agent collaboration | Free / Freemium | Challenger | 110,000+ skills |
| [Tons of Skills](https://tonsofskills.com) | CI-validated plugins with fuzzy search and CLI | Free | Challenger | 416 plugins / 2,787 skills |
| [Cursor Directory](https://cursor.directory) | Community rules, MCP servers, and plugins for Cursor | Free / Team tiers | Niche (Cursor-specific) | 76.8k+ developers |
| [Vibe Rules](https://viberules.app) | Cross-agent sync tool — write once, deploy to 18+ agents | Free (VSCode ext) | Niche (sync tool) | N/A (sync layer) |
| [Anthropic Official](https://github.com/anthropics/skills) | First-party reference skills for Claude | Free | Reference | 17 skills |

### Source URLs

- Skills.sh: [Vercel announcement](https://vercel.com/changelog/introducing-skills-the-open-agent-skills-ecosystem), [InfoQ coverage](https://www.infoq.com/news/2026/02/vercel-agent-skills/), [GitHub](https://github.com/vercel-labs/skills)
- SkillsMP: [SmartScope review](https://smartscope.blog/en/blog/skillsmp-marketplace-guide/), [skillsmp.com](https://skillsmp.com/)
- LobeHub: [lobehub.com/skills](https://lobehub.com/skills), [GitHub](https://github.com/lobehub/lobehub)
- Tons of Skills: [tonsofskills.com](https://tonsofskills.com/compare-marketplaces/)
- Cursor Directory: [cursor.directory](https://cursor.directory/)
- Vibe Rules: [viberules.app](https://viberules.app/en)
- Anthropic Official: [github.com/anthropics/skills](https://github.com/anthropics/skills)

---

## Feature Matrix

| Feature | Us | Skills.sh | SkillsMP | LobeHub | Tons of Skills | Cursor Dir | Vibe Rules |
|---------|-----|-----------|----------|---------|----------------|------------|------------|
| **Discovery & Distribution** | | | | | | | |
| Web-based searchable directory | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ |
| CLI installer (`npx skills add` or equiv.) | ❌ | ✅ | ❌ | ❌ | ✅ | ❌ | ❌ |
| One-click install from web/app | ❌ | ❌ | ❌ | ✅ | ❌ | ✅ | ✅ |
| Download/install count tracking | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Trending/leaderboard | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| User reviews/ratings | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Fuzzy/intelligent search | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ |
| Category-based browsing | 🔶 | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ |
| Dedicated skill detail pages | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ |
| **Quality & Security** | | | | | | | |
| CI validation pipeline | ✅ | ✅ | ❌ | ❌ | ✅ | ❌ | ❌ |
| Frontmatter schema validation | ✅ | ✅ | ❌ | ❌ | ✅ | ❌ | ❌ |
| Quality scoring rubric | ⭐ | ❌ | 🔶 | 🔶 | ❌ | ❌ | ❌ |
| Secret scanning | ❌ | ✅ | ❌ | ❌ | ✅ | ❌ | ❌ |
| Dangerous pattern detection | ❌ | ✅ | ❌ | ✅ | ✅ | ❌ | ❌ |
| Security vetting before install | ❌ | ✅ | ❌ | ✅ | ✅ | ❌ | ❌ |
| **Cross-Platform** | | | | | | | |
| Multi-agent support (18+ agents) | 🔶 | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ |
| Automatic format conversion | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Cross-agent sync tool | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| **Developer Experience** | | | | | | | |
| VSCode extension | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Skill creator/authoring tools | ⭐ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Self-healing validation in skills | ⭐ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Self-evolution telemetry | ⭐ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Skill versioning (semver) | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Skill dependency management | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Permissions sandboxing (runtime) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Skill bundle packaging | 🔶 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Community & Enterprise** | | | | | | | |
| Community skill submissions | 🔶 | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ |
| Team/private marketplace | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| Multi-agent collaboration | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ |
| User accounts/auth | ❌ | ❌ | ❌ | ✅ | ❌ | ✅ | ❌ |
| **Content Depth** | | | | | | | |
| SDLC coverage (build→deploy) | ⭐ | 🔶 | 🔶 | 🔶 | 🔶 | ❌ | ❌ |
| Combo/pipeline chains | ⭐ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Domain-specific analysis (40+ verticals) | ⭐ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Enterprise compliance (HIPAA, SOC2, etc.) | ⭐ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Video production pipeline | ⭐ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Game development skills | ⭐ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Meta-skills (skill lifecycle mgmt) | ⭐ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Progressive token loading | ✅ | ✅ | N/A | N/A | N/A | N/A | N/A |

Legend: ✅ = has it, 🔶 = partial, ❌ = missing, ⭐ = our edge

---

## Critical Gaps (Build Now)

Features we're missing that every major competitor has. These are table stakes.

### 1. Web-Based Searchable Directory

- **Feature:** A hosted website where users can browse, search, and discover skills
- **Who has it:** Skills.sh, SkillsMP, LobeHub, Tons of Skills, Cursor Directory (5/6 competitors)
- **Why it matters:** Without a web presence, we are invisible to the 99% of developers who discover tools via web search, not GitHub repo browsing. Every competitor has this. We are the only registry that exists exclusively as a GitHub repo with a README.
- **Effort:** L
- **Implementation hint:** Build a static site (Astro/Next.js) that reads SKILL.md files at build time, generates category pages, skill detail pages, and a search index. Deploy to Vercel/Cloudflare Pages. Could use `scripts/` tooling to generate JSON catalog at CI time. Consider `docs/` as the source for site content.

### 2. CLI Installer

- **Feature:** A command-line tool for installing skills (e.g., `npx skills-hub add <skill>`)
- **Who has it:** Skills.sh (`npx skills add`), Tons of Skills (`ccpi`)
- **Why it matters:** The `npx skills add` pattern from Vercel has set the standard. Without a CLI, users must manually copy SKILL.md files — friction that discourages adoption. Skills.sh hit 350,000 packages in 2 months largely because of frictionless install.
- **Effort:** M
- **Implementation hint:** Create an npm package that reads from the GitHub repo (or a registry API), downloads the skill folder to `~/.claude/skills/`, and handles versioning. Could extend `scripts/package_skill.py` logic. Entry point: `npx @skills-hub/cli add <skill-name>`.

### 3. Security Scanning

- **Feature:** Automated scanning of skill content for secrets, dangerous patterns, and supply-chain risks
- **Who has it:** Skills.sh (Snyk partnership), LobeHub (security-first vetting), Tons of Skills (secret scanning + dangerous pattern detection)
- **Why it matters:** The agent skills security crisis is real — 41.93% of marketplace skills flagged by scanners, supply-chain attacks via abandoned repo hijacking documented. Without security scanning, our registry risks hosting malicious content and losing trust. This is a market-wide concern highlighted by the Agent Skills Security Index launch.
- **Effort:** M
- **Implementation hint:** Add to `scripts/validate-skills.sh` or create a new `scripts/security-scan.sh`: grep for API keys/tokens/secrets patterns, detect `eval()` / `exec()` / shell injection patterns, check for data exfiltration URLs. Add as a CI step in `.github/workflows/validate.yml`. Consider integrating Snyk or Semgrep.

### 4. Intelligent Search & Skill Detail Pages

- **Feature:** Fuzzy search across skill names, descriptions, and categories + dedicated detail pages per skill
- **Who has it:** Skills.sh, SkillsMP, LobeHub, Tons of Skills, Cursor Directory (5/6 competitors)
- **Why it matters:** Our README lists skills but offers no way to search, filter, or deep-dive. Users looking for "HIPAA compliance" or "Flutter testing" can't find what we offer without scrolling a massive README.
- **Effort:** M (if paired with web directory)
- **Implementation hint:** Generate a JSON index from SKILL.md frontmatter at CI time. Build search with Fuse.js or Pagefind (for static sites). Each skill gets a page with: description, category, version, permissions, full instructions, related skills.

---

## Strategic Gaps (Plan & Schedule)

High-pressure features that require significant effort.

### 5. Cross-Platform Format Conversion

- **Feature:** Automatically convert SKILL.md to `.cursorrules`, Codex format, Copilot instructions, etc.
- **Who has it:** Vibe Rules (automatic format conversion for 18+ agents)
- **Why it matters:** We declare `platforms: [CLAUDE_CODE, CURSOR, CODEX_CLI]` in frontmatter but don't actually produce output for those platforms. As the market standardizes on SKILL.md, this becomes less urgent — but users on Cursor or Windsurf still need adapted formats today.
- **Competitive pressure:** MEDIUM — the SKILL.md standard is gaining universal adoption (30+ agents), making conversion less necessary over time.
- **Effort:** L
- **Implementation hint:** Create `scripts/convert.py` with adapters per target format. Map SKILL.md sections to `.cursorrules` structure, Copilot instructions, etc. Run at CI time to generate platform-specific versions alongside each SKILL.md.

### 6. Install Count & Trending/Leaderboard

- **Feature:** Track how many times each skill is installed; surface popular/trending skills
- **Who has it:** Skills.sh (install counts + leaderboard)
- **Why it matters:** Install counts are the strongest quality signal in package ecosystems (npm, PyPI). Skills.sh uses this to surface top skills. Without it, we can't tell users which of our 425+ skills are battle-tested.
- **Competitive pressure:** MEDIUM — only Skills.sh has this. But it's a powerful discovery mechanism.
- **Effort:** L (requires infrastructure: analytics endpoint, database or counter service)
- **Implementation hint:** If building a web directory, add a lightweight analytics ping on install (via CLI) or page view. Store counts in a simple KV store (Cloudflare KV, Vercel KV). Display on skill detail pages and a trending page.

### 7. Skill Dependency Management

- **Feature:** Skills can declare dependencies on other skills; installer resolves the graph
- **Who has it:** No competitor has this yet
- **Why it matters:** Our combo/pipeline chains already reference other skills by name in instruction text, but there's no machine-parseable dependency graph. As skills grow more interconnected, this becomes important for installation and version management.
- **Competitive pressure:** LOW — no one has it yet. First-mover opportunity.
- **Effort:** L
- **Implementation hint:** Add `depends: [skill-name@^1.0]` to frontmatter schema. Build a resolver in the CLI installer. Update `scripts/validate-skills.sh` to validate dependency references.

---

## Differentiator Opportunities

Features that could set us apart or where we could lead the market.

### 8. VSCode / IDE Extension

- **Feature:** Browse and install skills directly from VS Code sidebar
- **Who has it:** Vibe Rules (VSCode extension for sync)
- **Why it matters:** Most developers live in their IDE. A sidebar panel for browsing/installing skills removes the context switch of going to a website or CLI.
- **Competitive pressure:** LOW — only Vibe Rules has this, and it's a sync tool, not a full marketplace.
- **Effort:** L
- **Implementation hint:** VS Code extension with a tree view of categories → skills. Install action copies SKILL.md to `~/.claude/skills/`. Could reuse the JSON catalog from the web directory.

### 9. Team / Private Marketplace

- **Feature:** Organizations can curate a private set of approved skills for their team
- **Who has it:** Cursor Directory (Teams/Enterprise plans)
- **Why it matters:** Enterprise adoption requires governance — teams need to control which skills their developers use. This is the monetization path.
- **Competitive pressure:** LOW — only Cursor Directory has this (for Cursor users only).
- **Effort:** XL
- **Implementation hint:** Would require user accounts, org management, access control. Defer until core platform (web + CLI) is solid. Could start simple: a `team.yml` config that whitelists approved skills.

### 10. Multi-Agent Collaboration

- **Feature:** Skills that coordinate multiple AI agents working together
- **Who has it:** LobeHub (Agent Groups with intelligent assembly)
- **Why it matters:** Multi-agent workflows are an emerging trend. Our combo chains are sequential; true multi-agent collaboration would be parallel.
- **Competitive pressure:** LOW — emerging feature, only LobeHub has it.
- **Effort:** XL

---

## Our Competitive Edges

Features where we're ahead. Protect and promote these.

### 1. Self-Evolution Telemetry (Unique)
Skills log execution metadata to `~/.claude/projects/*/skill-telemetry.md`. The `/evolve` meta-skill reads this telemetry, maps findings to skills, generates additive patches, and bumps versions. **No competitor has anything like this.** This is genuine AI-improving-AI capability.

### 2. Self-Healing Validation (Unique)
Every skill includes self-healing blocks with up to 2 retry iterations. Skills can detect their own failures and attempt corrective action. **No competitor has this.**

### 3. Combo/Pipeline Chains (Unique)
34 pre-built multi-skill workflows (e.g., `/polish` = parallel UX + scalability audit → QA → analyze). Competitors offer individual skills only. **Our chains are the equivalent of npm scripts vs individual packages.**

### 4. Domain Depth — 40+ Industry Verticals (Unmatched)
195+ domain-specific analysis skills covering healthcare, fintech, manufacturing, logistics, government, nonprofits, gaming, real estate, and more. **No competitor comes close to this breadth.** SkillsMP and LobeHub have community-contributed skills but nothing curated at this depth.

### 5. Enterprise Compliance Suite (Unmatched)
HIPAA, GDPR, SOC2, PCI-DSS, OWASP, manufacturing (ISO 9001/13485), government (FedRAMP, FISMA), and more — with dedicated review skills for each. **This is a defensible moat for enterprise adoption.**

### 6. Full SDLC Coverage (Best-in-Class)
From `/build` (scaffolding) through `/test-suite`, `/qa`, `/secure`, `/deploy`, `/pr`, to `/preflight` — we cover the entire software development lifecycle in a single registry. Competitors have fragmented coverage.

### 7. Video Production Pipeline (Unique)
8 video skills covering Remotion, ElevenLabs, FFmpeg, tutorial videos, ad videos, social clips, and wedding videos. **No competitor touches video production.**

### 8. Meta-Skills for Skill Lifecycle (Unique)
`/skill-creator`, `/skill-test`, `/registry-sync`, `/evolve`, `/promote` — tools for building, testing, validating, improving, and promoting skills. **We are the only registry that is self-improving.**

### 9. Quality Scoring Rubric (Best-in-Class)
0-100 scoring system (Schema 0-25 + Instruction Quality 0-75). SkillsMP and LobeHub have basic quality filtering; ours is a structured, transparent rubric.

---

## Industry Trends

Emerging capabilities the market is moving toward. Early adoption opportunity.

| Trend | Adoption Stage | Competitors With It | Our Status | Recommendation |
|-------|---------------|--------------------|-----------:|----------------|
| SKILL.md as universal standard | Mainstream (30+ agents) | All | ✅ Already using | Promote our early adoption; ensure full spec compliance |
| CLI-based skill installation | Early mainstream | Skills.sh, Tons of Skills | ❌ Missing | **Build CLI installer — this is the distribution standard** |
| Security scanning / vetting | Early adopter | Skills.sh, LobeHub, Tons of Skills | ❌ Missing | **Add to CI pipeline — trust is a prerequisite for adoption** |
| Skill installer meta-skill | Trending (142k installs) | Skills.sh, community | ❌ Missing | Build a `/skill-install` skill that fetches from our registry |
| Browser-use skills | Emerging | LobeHub, community | ❌ Missing | Lower priority — let the standard mature |
| Multi-agent coordination | Emerging | LobeHub | ❌ Missing | Monitor; our combo chains are a related pattern |
| Agent Skills Security Index | Emerging | Independent initiative | ❌ Missing | Contribute and align with the security index |
| Private/team marketplaces | Early adopter | Cursor Directory | ❌ Missing | Defer until core platform is solid — then target enterprises |
| Monetization / paid skills | Nascent | PromptBase (prompts only) | ❌ N/A | Monitor; not yet proven in the skills market |

---

## Recommended Roadmap

Based on the full analysis, a prioritized build order:

### Sprint 1 — Quick Wins (1-2 weeks)

1. **Security scanning in CI** — CRITICAL pressure, M effort. Add secret/pattern scanning to `validate.yml`. Immediate trust signal. We already have the CI pipeline; extend it.
2. **JSON skill catalog generator** — HIGH pressure, S effort. Script to produce `skills.json` from all SKILL.md frontmatter. Foundation for web directory, CLI, and search.
3. **Skill installer meta-skill** — HIGH pressure, S effort. A `/skill-install` skill that downloads from our GitHub repo to `~/.claude/skills/`. Zero infrastructure needed.

### Sprint 2 — Core Platform (2-4 weeks)

4. **Static web directory** — CRITICAL pressure, L effort. Astro/Next.js site consuming `skills.json`. Category pages, skill detail pages, Pagefind search. Deploy to Vercel.
5. **CLI installer (npm package)** — CRITICAL pressure, M effort. `npx @skills-hub/cli add <skill>`. Downloads from GitHub. Handles versioning. The distribution standard.
6. **Install count tracking** — MEDIUM pressure, M effort. Lightweight analytics via CLI ping. Surface on web directory.

### Next Quarter — Strategic

7. **Cross-platform format conversion** — MEDIUM pressure, L effort. Auto-generate .cursorrules / Copilot versions.
8. **VSCode extension** — LOW pressure, L effort. Sidebar browser + installer.
9. **Skill dependency management** — LOW pressure, L effort. First-mover advantage; no competitor has this.

### Future — Differentiators

10. **Team/private marketplace** — LOW pressure, XL effort. Enterprise monetization path.
11. **Multi-agent collaboration** — LOW pressure, XL effort. Wait for patterns to mature.

---

## Summary

| Metric | Count |
|--------|-------|
| **Total features across competitors** | 34 |
| **We have** | 12 (35%) |
| **Partial** | 5 (15%) |
| **Missing** | 13 (38%) |
| **Our edges** | 9 unique advantages |
| **Critical gaps to close** | 4 (web directory, CLI installer, security scanning, search) |
| **Biggest threat** | **Skills.sh (Vercel)** — with 350k packages, CLI installer, and Snyk security, they are becoming the npm of AI agent skills. Their distribution infrastructure makes content depth (our advantage) harder to discover. If developers default to `npx skills add`, we need to be in that ecosystem or build a competing install path. |
| **Biggest opportunity** | **Our content depth + self-evolution system is unmatched and defensible.** No competitor has 40+ industry verticals, combo chains, or self-improving skills. If we add distribution infrastructure (web + CLI + security scanning), we become the "enterprise-grade, curated" alternative to Skills.sh's "npm-like, anything goes" model. The positioning is: **Skills.sh is npm; we are the standard library.** |
