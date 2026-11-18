# Meta

Skills about skills -- creation, testing, evolution, templates, cross-project sync, and registry maintenance.

## Skills (12)

| Skill | Version | Description |
|-------|---------|-------------|
| [bootstrap](bootstrap/) | 3.1.0 | Scaffolds a new project from a saved template -- creates CLAUDE.md, initial memory, and recommends first skill |
| [evolve](evolve/) | 1.1.0 | Self-improving skill that reads /recall and /metrics output, identifies which skills need patching, and applies fixes |
| [extract-template](extract-template/) | 1.0.0 | Extracts a reusable project template from a successful project -- captures pipeline, conventions, and pitfalls |
| [promote](promote/) | 1.1.0 | Cross-project pattern detection -- reads all project memories, finds recurring patterns, promotes to global conventions |
| [skill-creator](skill-creator/) | 1.0.0 | Creates new Claude Code skills following the marketplace SKILL.md format with proper frontmatter and quality scoring |
| [skill-test](skill-test/) | 1.0.0 | Validates a SKILL.md file against the marketplace quality rubric, checking schema, structure, and computing a score |
| [registry-sync](registry-sync/) | 1.0.0 | Scans and validates all SKILL.md files in the registry, checks category READMEs, detects duplicates, produces health report |

## Usage

**Self-improvement loop:**
```
/recall → /metrics → /evolve → /promote
```

- `/recall` analyzes git history for development patterns
- `/metrics` computes quality scores from the findings
- `/evolve` patches skills based on the data
- `/promote` detects cross-project patterns and promotes to global conventions

**Skill development:**
- Create a new skill: `/skill-creator`
- Validate a skill against the quality rubric: `/skill-test`
- Scan the full registry for issues: `/registry-sync`

**Project lifecycle:**
- Scaffold a new project from template: `/bootstrap`
- Extract a template from a mature project: `/extract-template`

## Recently Added

| Skill | Version | Description |
|-------|---------|-------------|
| [broadcast](broadcast/) | 1.0.0 | Apply the same change across multiple repos simultaneously using parallel agent teams. Creates worktrees, applies changes, runs tests, commits, and creates PRs. For cross-repo... |
| [load-context](load-context/) | 2.0.0 | Load a saved conversation context to resume previous work. Supports local files, git repos, and URLs. Triggered by 'load context', 'resume previous work', 'pick up where I left... |
| [publish-skill](publish-skill/) | 1.0.0 | Publish a locally installed skill to the skills-hub registry and sync it to the production platform. Use when: 'publish skill X', 'push skill to hub', 'add skill to registry',... |
| [save-context](save-context/) | 2.0.0 | Save the current conversation context as a reloadable snapshot. Triggered by 'save context', 'save session', 'bookmark this', 'save progress', 'snapshot conversation', 'save my... |
| [skillify](skillify/) | 1.1.0 | Create a reusable, self-healing, self-evolving global skill — either from the current conversation context OR from a plain-language description of a workflow. Triggers on: 'turn... |

<!-- BEGIN GENERATED: skills-hub-index (scripts/gen-index.mjs, do not edit by hand) -->
## All Meta skills on skills-hub.ai

Each skill page on skills-hub.ai shows ratings and reviews, install counts, a one-command install, and related skills. 20 of 20 skills in this folder have a page. You can also [browse the Meta category on skills-hub.ai](https://skills-hub.ai/browse?category=meta), which includes skills from other publishers.

| Skill | Description | Page |
|-------|-------------|------|
| [bootstrap](bootstrap/) | Scaffolds a new project from a saved template with CLAUDE.md, initial memory, recommended pipeline, known pitfalls, and foundation... | [View on skills-hub](https://skills-hub.ai/skills/bootstrap) |
| [broadcast](broadcast/) | Apply the same change across multiple repos simultaneously using parallel agent teams. | [View on skills-hub](https://skills-hub.ai/skills/broadcast) |
| [clip](clip/) | Copy the snippet I recommended in my last response (a command, query, Slack or PR text) to the clipboard exactly, with no terminal wrap... | [View on skills-hub](https://skills-hub.ai/skills/clip) |
| [codex-record-replay](codex-record-replay/) | Guide to capturing, refining, and publishing workflows using Codex Record & Replay (launched June 18 2026). | [View on skills-hub](https://skills-hub.ai/skills/codex-record-replay) |
| [coding-guardrails](coding-guardrails/) | Installs behavioral guardrails against classic LLM coding failures and audits the current session against them. | [View on skills-hub](https://skills-hub.ai/skills/coding-guardrails) |
| [evolve](evolve/) | Self-improving skill system. Reads /recall and /metrics output, identifies which skills need patching based on rework patterns and... | [View on skills-hub](https://skills-hub.ai/skills/evolve) |
| [extract-template](extract-template/) | Extracts a reusable project template from a mature project — captures architecture, pipeline, conventions, CI/CD, Docker, testing,... | [View on skills-hub](https://skills-hub.ai/skills/extract-template) |
| [load-context](load-context/) | Load a saved conversation context to resume previous work. | [View on skills-hub](https://skills-hub.ai/skills/load-context) |
| [promote](promote/) | Cross-project pattern detection — discovers recurring conventions, rework patterns, and pipeline patterns across all projects,... | [View on skills-hub](https://skills-hub.ai/skills/promote) |
| [registry-sync](registry-sync/) | Validate the entire skills registry — scan all SKILL.md files for frontmatter correctness, check category READMEs are current, detect... | [View on skills-hub](https://skills-hub.ai/skills/registry-sync) |
| [save-context](save-context/) | Save the current conversation context as a reloadable snapshot. | [View on skills-hub](https://skills-hub.ai/skills/save-context) |
| [save-tokens](save-tokens/) | Token-efficient codebase navigation. Build a queryable knowledge graph of a repo (via graphify) ONCE — using NO LLM at all (pure local... | [View on skills-hub](https://skills-hub.ai/skills/save-tokens) |
| [skill-creator](skill-creator/) | Create new skills, modify and improve existing skills, and measure skill performance. | [View on skills-hub](https://skills-hub.ai/skills/skill-creator) |
| [skill-decay-audit](skill-decay-audit/) | Semi-annual decay audit of AI scaffolding -- skills, CLAUDE.md, hooks, and memory -- deleting instructions written for older, weaker... | [View on skills-hub](https://skills-hub.ai/skills/skill-decay-audit) |
| [skill-scout](skill-scout/) | Project-aware skill discovery and installation. | [View on skills-hub](https://skills-hub.ai/skills/skill-scout) |
| [skill-stack](skill-stack/) | Curated skill bundle installer keyed to project archetype. | [View on skills-hub](https://skills-hub.ai/skills/skill-stack) |
| [skill-test](skill-test/) | Test a skill's quality before publishing — validate SKILL.md frontmatter schema, check instruction structure for phases and guardrails,... | [View on skills-hub](https://skills-hub.ai/skills/skill-test) |
| [skillify](skillify/) | Create a reusable, self-healing, self-evolving global skill — either from the current conversation context OR from a plain-language... | [View on skills-hub](https://skills-hub.ai/skills/skillify) |
| [tend](tend/) | Automated app improvement cycles. Assesses each app's health, prioritizes by staleness and debt, consumes recall/metrics/evolve findings... | [View on skills-hub](https://skills-hub.ai/skills/tend) |
| [youtube-research](youtube-research/) | Research pipeline — search YouTube, ingest into NotebookLM, generate deliverables, organize in Obsidian vault | [View on skills-hub](https://skills-hub.ai/skills/youtube-research) |
<!-- END GENERATED: skills-hub-index -->
