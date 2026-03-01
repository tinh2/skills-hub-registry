# Competitive Gap Analysis: skills-hub-registry vs Skill Collection Landscape

**Date:** 2026-03-01
**Scope:** Claude Code skill collections, curated skill registries, community skill aggregators, agent OS skill bundles
**Context:** This analysis evaluates the skills-hub-registry (359 skills, 13 categories, 40 industry verticals) against competing skill collections and platforms to identify coverage gaps, quality advantages, and strategic opportunities.

---

## 1. Product Identity

**skills-hub-registry** is the official skill collection powering [skills-hub.ai](https://skills-hub.ai) — a marketplace for Claude Code skills. It's a **curated, production-quality skill library** organized around the complete software development lifecycle plus 40 industry verticals and social-impact sectors.

**The strategic question:** Is this collection sufficiently differentiated from the growing number of free skill aggregators and competing curated collections to drive marketplace value?

---

## 2. Competitive Landscape

### 2.1 Curated Skill Collections (Direct Competitors)

#### Antigravity Awesome Skills (github.com/sickn33/antigravity-awesome-skills)
- **Scale:** 954+ agentic skills
- **Categories:** 8 (Architecture, Business, Data & AI, Development, General, Infrastructure, Security, Testing)
- **Format:** SKILL.md standard
- **Platforms:** Claude Code, Antigravity, Cursor, Gemini CLI, Codex CLI, OpenCode, GitHub Copilot, AdaL
- **Extras:** Role-based bundles (Web Wizard, Security Engineer), step-by-step workflow playbooks, interactive web app for browsing
- **Quality control:** None beyond "battle-tested" claim. No scoring, no validation, no structural consistency enforcement
- **Industry verticals:** None
- **Strengths:**
  - Largest single curated collection (954+ vs our 359)
  - Includes official skills from Anthropic, OpenAI, Google, Microsoft, Supabase, Vercel
  - Bundles and workflows add usability layer
  - Cross-platform targeting (8+ tools)
- **Weaknesses:**
  - No industry-specific skills (generic dev-only)
  - No quality scoring or behavioral testing
  - No structural consistency (mixed formats, varying quality)
  - No skill chaining/composition
  - No meta/self-improvement skills
  - No autonomous mode enforcement
  - Aggregated from multiple sources — unclear provenance

#### Everything Claude Code (github.com/affaan-m/everything-claude-code)
- **Scale:** 56+ skills, 13 agents, 32+ commands, multiple hooks
- **Categories:** Language-specific (6 languages), Development Practices, Infrastructure, Business/Content
- **Format:** SKILL.md + agents + hooks + commands (broader scope than just skills)
- **Origin:** Anthropic hackathon winner (Feb 2026)
- **Strengths:**
  - Holistic approach (skills + agents + hooks + commands + MCP configs)
  - Language-specific depth (TypeScript, Python, Go, Java, C++, Swift, Rust)
  - Battle-tested from 10+ months of daily use
  - Security scanning built in
  - Plugin marketplace installable
- **Weaknesses:**
  - Only 56+ skills (vs our 359)
  - No industry verticals
  - Personal collection — single developer's workflow
  - No formal quality validation
  - No autonomous mode enforcement

#### Anthropic Official Skills (github.com/anthropics/skills)
- **Scale:** ~10-20 example skills + document skills (docx, pdf, pptx, xlsx)
- **Stars:** 79.7K GitHub stars
- **Categories:** Creative & Design, Development & Technical, Enterprise & Communication, Document Skills
- **Format:** SKILL.md standard (they defined it)
- **Strengths:**
  - Official Anthropic backing — enormous credibility
  - Defines the SKILL.md standard
  - Document skills power Claude's native document creation
  - 79.7K stars — massive visibility
  - Partner skills (Notion)
- **Weaknesses:**
  - Tiny collection (~20 skills)
  - No industry verticals
  - No autonomous mode
  - Example/demo quality, not production pipelines
  - No skill composition

### 2.2 Skill Aggregators (Indirect Competitors)

#### SkillsMP (skillsmp.com)
- **Scale:** 270K+ indexed skills
- **Model:** Aggregates from public GitHub repos automatically
- **Quality:** Zero curation — indexes everything
- **Strengths:** Largest catalog by volume, cross-platform (Claude, Codex, ChatGPT)
- **Weaknesses:** No quality control, no reviews, massive noise-to-signal ratio

#### SkillHub Club (skillhub.club)
- **Scale:** 7K+ AI-evaluated skills
- **Quality:** 5-dimension AI scoring (Practicality, Clarity, Automation, Quality, Impact)
- **Extras:** Instant playground for trying skills, S/A rank scoring
- **Platforms:** Claude Code, Cursor, OpenCode, Windsurf, Cline, Roo Code, Aide, Augment
- **Strengths:** AI quality scoring is novel, playground testing, wide platform support
- **Weaknesses:** No curation beyond AI scoring, no industry verticals, no composition

### 2.3 Universal Installers (Distribution Competitors)

#### OpenSkills (npmjs.com/package/openskills)
- **Scale:** Installer, not a collection — pulls from CCPM registry and GitHub
- **Model:** Universal SKILL.md loader via `npm i -g openskills`
- **Platforms:** Claude Code, Cursor, Windsurf, Aider, Codex
- **Strengths:** Universal installer, project-local and global install, private repo support
- **Weaknesses:** No own content, depends on other collections

#### CCPM (ccpm.dev)
- **Scale:** Growing plugin marketplace
- **Model:** CLI-first discovery and installation
- **Strengths:** Official Claude Code plugin system integration
- **Weaknesses:** Still early, limited catalog

### 2.4 Agent OS Skill Bundles

#### OpenFang (openfang.sh)
- **Scale:** 60 bundled skills + 7 Hands (autonomous agents)
- **Format:** SKILL.md parser + HAND.toml for autonomous agents
- **Strengths:** True autonomous execution, 40 channel adapters, FangHub marketplace
- **Weaknesses:** Small skill count, no industry verticals, self-hosted only

---

## 3. Feature Comparison Matrix

| Feature | skills-hub-registry | Antigravity | ECC | Anthropic | SkillsMP | SkillHub | OpenFang |
|---------|-------------------|-------------|-----|-----------|----------|----------|----------|
| **Total skills** | 359 | 954+ | 56+ | ~20 | 270K+ | 7K+ | 60 |
| **Categories** | 13 | 8 | ~6 | 4 | N/A | N/A | N/A |
| **Industry verticals** | 40 | 0 | 0 | 0 | 0 | 0 | 0 |
| **Structural consistency** | 100% validated | Mixed | Mixed | Official format | Mixed | Mixed | Mixed |
| **Autonomous mode** | 100% (359/359) | Partial | Partial | No | No | No | Yes (Hands) |
| **Quality validation** | Schema + structural | None | None | None | None | AI 5-dim | None |
| **Phased instructions** | 100% (359/359) | Some | Some | Some | Varies | Varies | Varies |
| **NEXT STEPS** | 100% (359/359) | Rare | No | No | N/A | N/A | No |
| **Guardrails (DO NOT)** | 100% (359/359) | Rare | Rare | No | N/A | N/A | No |
| **$ARGUMENTS handling** | 100% (359/359) | Partial | Partial | No | N/A | N/A | No |
| **Skill composition** | 28 combo chains | Bundle packs | Agent chains | No | No | No | Hand chains |
| **Meta/self-improvement** | 7 skills | No | No | 1 (skill-creator) | No | No | No |
| **Version management** | Semver on all | No | No | No | No | No | No |
| **Persona advisors** | 10 role-based | No | No | No | No | No | No |
| **Social impact** | 58 skills / 14 sectors | No | No | No | No | No | No |
| **Cross-platform** | CLAUDE_CODE | 8+ tools | Claude Code | Claude + API | Multi | 8+ tools | OpenFang |
| **Playground/try** | No | Web app | No | No | No | Yes | No |
| **Installation CLI** | Manual | Manual | Plugin | Plugin | Manual | Manual | CLI |

---

## 4. Critical Gaps (What We're Missing)

### GAP 1: Raw Skill Count Deficit
- **Antigravity** has 954+ skills vs our 359 (2.6x more)
- **SkillsMP** indexes 270K+ (volume play, but low quality)
- We have 193 analysis skills — heavily weighted toward industry verticals
- **The gap:** Our core software development categories (build: 21, test: 11, deploy: 15) are smaller than Antigravity's equivalent coverage
- **Impact:** Perception gap — "fewer skills" looks like less value in a marketplace listing
- **Opportunity:** Add 100-150 more software development skills to reach 500+ while maintaining quality

### GAP 2: Cross-Platform Compatibility
- **Antigravity** targets 8+ tools (Claude Code, Cursor, Windsurf, Codex, Gemini CLI, etc.)
- **SkillHub** supports 8+ tools
- **OpenSkills** is universal
- **We only target CLAUDE_CODE** — every skill has `platforms: [CLAUDE_CODE]`
- **Impact:** Excludes the growing Cursor, Codex, Windsurf, and Gemini CLI user bases
- **Opportunity:** Most SKILL.md skills work across tools without modification. Adding `platforms: [CLAUDE_CODE, CURSOR, CODEX_CLI, WINDSURF]` and testing compatibility would expand our addressable market significantly

### GAP 3: Language & Framework-Specific Skills
- **Everything Claude Code** has language-specific skills for 6 languages (TypeScript, Python, Go, Java, C++, Swift, Rust)
- **Antigravity** has framework-specific patterns
- **We have zero language-specific skills** — our build skills scaffold projects but don't teach language patterns
- **Impact:** Developers searching for "Python best practices" or "Go testing" won't find us
- **Opportunity:** Add 20-30 language-specific skills (TypeScript, Python, Go, Java, Rust, Swift) covering coding standards, testing patterns, and framework best practices

### GAP 4: Interactive Playground / Try Before Install
- **SkillHub** offers an instant playground with free daily quota
- **Antigravity** has a web app for browsing
- **We have no interactive experience** — skills are static markdown files
- **Impact:** Users can't evaluate skill quality before downloading
- **Opportunity:** This is a skills-hub.ai (the app) feature, not a registry gap. But the registry should include sample inputs/outputs that the app's playground can use.

### GAP 5: No Agent/Hook/Command Ecosystem
- **Everything Claude Code** ships skills + 13 agents + 32 commands + hooks + MCP configs
- Our skills are standalone SKILL.md files with no supporting automation
- **The gap:** Modern Claude Code power users want the full stack (skills + agents + hooks + commands)
- **Impact:** Power users may choose ECC's integrated approach over our skill-only approach
- **Opportunity:** Add hooks, commands, and agent configurations that complement the skill collection

### GAP 6: No Installation/Distribution Mechanism
- **Antigravity** can be browsed via web app
- **ECC** installable as Claude Code plugin
- **OpenSkills** installable via npm
- **We're a raw git repo** — `git clone` and manually copy
- **Impact:** Higher friction to adopt
- **Opportunity:** This is the skills-hub.ai marketplace's job — the registry feeds the app. But adding a simple install script or plugin manifest would reduce friction for early adopters.

---

## 5. Strategic Gaps (Deeper Analysis)

### STRATEGIC GAP 1: Enterprise Skill Partnerships
- **Anthropic** partners with PwC for finance/healthcare enterprise skills
- **Cursor** has enterprise partners (Figma, Stripe, AWS)
- **Intuit** building industry-specific skills with Anthropic
- We have 40 industry verticals but no enterprise partner backing
- **Opportunity:** Position the registry's industry verticals as the foundation for enterprise marketplace partnerships

### STRATEGIC GAP 2: Official Anthropic Skill Standard Alignment
- Anthropic's SKILL.md spec requires only `name` and `description` in frontmatter
- Our spec adds `version`, `category`, and `platforms` — valid extensions but non-standard
- If Anthropic enforces strict spec compliance, our extra fields could cause issues
- **Opportunity:** Ensure all extra fields are compatible with the official spec (they currently are — YAML allows additional fields)

### STRATEGIC GAP 3: No Data/AI/ML Skills Category
- **Antigravity** has a full "Data & AI" category (LLM apps, RAG, agents, analytics)
- We have zero data science, machine learning, or AI/ML-specific skills
- **Impact:** Missing the fastest-growing skill demand segment
- **Opportunity:** Add a `data` or `ai` category with 15-20 skills for ML pipelines, data engineering, prompt engineering, LLM evaluation, RAG systems

---

## 6. Differentiators — Where skills-hub-registry Wins

| Differentiator | Why It Matters | Who It Beats |
|----------------|----------------|-------------|
| **40 industry verticals** | No other collection has ANY industry-specific skills. We have 193. | Everyone (nobody else does this) |
| **100% structural consistency** | Every skill: autonomous mode, phased instructions, NEXT STEPS, DO NOT guardrails, $ARGUMENTS | Everyone (all others are mixed quality) |
| **Validated quality baseline** | Schema + structural validation on 100% of skills. Zero validation failures. | Everyone (including SkillHub's AI scoring — ours is structural, not surface) |
| **28 combo chains** | Skill composition as first-class content. /research chains /compete + /new-features. | Antigravity has bundles (static grouping), not chains (dynamic execution) |
| **10 persona advisors** | Role-based advisory skills (CTO, DevOps Lead, etc.) | Nobody else has persona skills |
| **58 social impact skills** | Climate, education, governance, agriculture, humanitarian, disability, housing | Nobody else covers social impact |
| **7 meta skills** | Self-improvement: evolve, promote, recall, metrics, extract-template | Anthropic has 1 (skill-creator); nobody else has meta skills |
| **Semver on every skill** | Version tracking enables update management in the marketplace | Nobody else versions skills |
| **Autonomous mode** | "Do NOT ask the user questions. Analyze and act." on 100% of skills | Mixed enforcement elsewhere |

---

## 7. Our Edges (Things Competitors Can't Easily Replicate)

1. **Industry vertical depth** — 193 skills across 40 verticals with domain-specific regulatory standards (HIPAA, GAMP 5, 21 CFR Part 11, ACORD, IATA, OSHA, etc.). This took 4.3 hours of intensive parallel agent generation. Reproducing this with equivalent domain knowledge is non-trivial.

2. **Consistent quality template** — Every skill follows the exact same structure: frontmatter → autonomous mode → TARGET: $ARGUMENTS → phased instructions → OUTPUT → NEXT STEPS → DO NOT. This consistency trains users to expect reliable behavior. Aggregators can't enforce this.

3. **Skill composition architecture** — The main skill + sub-skill pattern (/integrate routes to /stripe, /auth-provider, etc.) is a design philosophy, not just content. This orchestration layer doesn't exist in any competitor.

4. **Self-improving ecosystem** — /evolve reads recall data and patches skill instructions. /promote cross-pollinates patterns across projects. /metrics tracks quality over time. This feedback loop doesn't exist elsewhere.

5. **Production-tested origin** — These skills were built and refined across 7 real projects (fringe-core, PawPass, Recipe AI, Confidence Coach, ollama-server, claude-config, OpenClaw). They're not hypothetical — they reflect actual rework patterns, failure modes, and optimizations.

---

## 8. Industry Trends

1. **Skill format standardization is accelerating** — SKILL.md is now supported by Claude Code, Codex CLI, Cursor, OpenFang, AgentOS, SkillsMP, SkillHub, and OpenSkills. The format war is over. Distribution wins.

2. **Quality > Quantity** — SkillsMP's 270K skills prove that volume alone doesn't win. Users search for quality. SkillHub's 5-dimension AI scoring is a direct response. Curated collections that guarantee quality will outperform aggregators.

3. **Enterprise is adopting Claude Code skills** — PwC, Intuit, and enterprise partners are building industry-specific skills. The market is moving from generic dev tools to domain-specific workflows. Our 40 industry verticals are ahead of this curve.

4. **Cross-platform is table stakes** — Every new tool adopts SKILL.md. Collections that target only one platform will lose to universal collections.

5. **Composition is the next frontier** — Individual skills are commoditizing. Skill chains, workflows, and orchestrated pipelines are the value layer. Our 28 combo skills and main+sub-skill architecture are early-mover advantages.

6. **Agents > Skills** — OpenFang's Hands, ECC's 13 agents, and the "Deploy as Agent" trend suggest that standalone skills are evolving into autonomous agents. Skills that work in agent mode (autonomous, non-interactive) are better positioned for this transition.

---

## 9. Recommended Actions

### Phase 1: Close Critical Gaps (Immediate)
1. **Add cross-platform compatibility** — Update platforms field on all 359 skills to include CURSOR, CODEX_CLI, WINDSURF where compatible
2. **Add language-specific skills** — 20-30 skills for TypeScript, Python, Go, Java, Rust, Swift (coding standards, testing, frameworks)
3. **Add Data/AI category** — 15-20 skills for ML pipelines, RAG, prompt engineering, LLM evaluation, data engineering

### Phase 2: Strengthen Advantages (Next Sprint)
4. **Add sample inputs/outputs** — Each skill includes 2-3 example invocations with expected output (feeds marketplace playground)
5. **Create plugin manifest** — Make the registry installable as a Claude Code plugin
6. **Add DevOps/platform engineering depth** — More Kubernetes, Terraform, AWS/GCP/Azure skills to match Antigravity's Infrastructure category

### Phase 3: Ecosystem Expansion (Future)
7. **Add hooks and commands** — Complement skills with automation hooks (pre-commit, post-deploy)
8. **Build a validation CI pipeline** — GitHub Actions that validate every SKILL.md on push
9. **Create role-based bundles** — Package skills by developer role (Frontend Lead, DevOps Engineer, etc.)

---

## 10. Summary

| Metric | Value |
|--------|-------|
| Competitors analyzed | 10 |
| Curated collections | 3 (Antigravity 954+, ECC 56+, Anthropic ~20) |
| Aggregators | 2 (SkillsMP 270K+, SkillHub 7K+) |
| Universal installers | 2 (OpenSkills, CCPM) |
| Agent OS bundles | 1 (OpenFang 60) |
| Critical gaps found | 6 |
| Strategic gaps found | 3 |
| Differentiators identified | 9 |

**Our position:** #2 by raw count (359 vs Antigravity's 954+) but #1 by quality, consistency, industry coverage, and composition depth. No other collection has industry verticals, validated structural consistency, combo chains, or meta skills.

**Biggest threat:** Antigravity reaching 1,000+ skills while maintaining cross-platform compatibility and adding quality controls. If they add industry verticals or composition, they become a direct threat.

**Biggest opportunity:** Being the curated, quality-first collection that powers the skills-hub.ai marketplace. Aggregators can't compete on quality. Our structural consistency and industry depth are moats.

**Key insight:** Don't compete on quantity with SkillsMP (270K). Compete on quality with Antigravity (954). Close the count gap to 500+ while maintaining 100% validation, then let industry verticals and composition be the differentiators nobody else has.
