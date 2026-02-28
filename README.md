# skills-hub-registry

The official skill collection for [skills-hub.ai](https://skills-hub.ai) — a marketplace for Claude Code skills.

45 production-tested skills organized into 13 categories covering the complete software development lifecycle.

## Directory Structure

```
skills-hub-registry/
├── build/              # 7 skills  — Project scaffolding and full build pipelines
├── test/               # 2 skills  — Unit tests, E2E tests, integration tests
├── qa/                 # 5 skills  — Quality assurance, bug detection, code review
├── review/             # 2 skills  — Architecture review, PR creation
├── deploy/             # 2 skills  — Infrastructure, CI/CD, cloud deployment
├── docs/               # 3 skills  — README generation, API docs, changelogs
├── security/           # 1 skill   — Vulnerability checks, compliance
├── ux/                 # 1 skill   — Accessibility, usability, design systems
├── analysis/           # 9 skills  — Domain analysis, competitive analysis, metrics
├── productivity/       # 1 skill   — Workflow automation, IDE tools
├── integration/        # (empty)   — Third-party service connectors
├── combo/              # 8 skills  — Multi-skill chains and compositions
└── meta/               # 4 skills  — Skills about skills: recall, evolve, promote
```

## Skill Catalog

### build — Project Scaffolding & Build Pipelines

| Skill | Version | Description |
|-------|---------|-------------|
| [build](build/build/) | 3.0.0 | Master orchestrator — takes a competitor app and builds a better clone end-to-end |
| [ship](build/ship/) | 8.0.0 | Fast autonomous build loop — 4 iterations max with domain analysis |
| [iterate](build/iterate/) | 4.0.0 | Self-iterating build loop — up to 6 iterations with validation and review |
| [flutter](build/flutter/) | 2.0.0 | Builds Flutter mobile app from video/screenshots |
| [hotfix](build/hotfix/) | 1.0.0 | Emergency bug fix pipeline — diagnose, fix, test, PR in 2 iterations |
| [story-implementer](build/story-implementer/) | 2.0.0 | Implements a Jira story using repo conventions, writes tests, creates PR |
| [db-migrate](build/db-migrate/) | 1.0.0 | Scaffolds database migration files with Slick/Prisma table definitions |

### test — Automated Testing

| Skill | Version | Description |
|-------|---------|-------------|
| [e2e](test/e2e/) | 1.0.0 | Auto-detects any tech stack, generates exhaustive E2E tests with self-healing |
| [manual-test-plan](test/manual-test-plan/) | 2.0.0 | Generates manual QA test plan from branch code changes |

### qa — Quality Assurance

| Skill | Version | Description |
|-------|---------|-------------|
| [qa](qa/qa/) | 3.0.0 | Automated QA agent — walks every screen/endpoint, verifies and fixes |
| [iterate-review](qa/iterate-review/) | 5.0.0 | Autonomously reviews and improves code through up to 5 iterations |
| [preflight](qa/preflight/) | 1.0.0 | Pre-deploy verification gate — checks git, build, tests, migrations |
| [perf](qa/perf/) | 1.0.0 | Performance profiler — analyzes queries, API chains, widget rebuilds |
| [audit](qa/audit/) | 2.0.0 | Lightweight domain consistency audit — fast gate between pipeline phases |

### review — Architecture & Code Review

| Skill | Version | Description |
|-------|---------|-------------|
| [arch-review](review/arch-review/) | 7.0.0 | Architect-level story review and implementation validation |
| [pr](review/pr/) | 1.0.0 | Creates convention-compliant PRs with story extraction and test plans |

### deploy — Infrastructure & Deployment

| Skill | Version | Description |
|-------|---------|-------------|
| [aws](deploy/aws/) | 1.0.0 | Generates production-ready Terraform files for AWS infrastructure |
| [app-icon](deploy/app-icon/) | 1.0.0 | Generates polished app icons and applies as launcher icons |

### docs — Documentation

| Skill | Version | Description |
|-------|---------|-------------|
| [readme](docs/readme/) | 1.0.0 | Generates comprehensive README.md by analyzing codebase |
| [gen-catalog](docs/gen-catalog/) | 1.0.0 | Auto-generates README and skill catalog from SKILL.md frontmatter |
| [skills-list](docs/skills-list/) | 3.0.0 | Displays the full skills catalog reference |

### security — Security & Compliance

| Skill | Version | Description |
|-------|---------|-------------|
| [check-vanta](security/check-vanta/) | 2.0.0 | Fetches Vanta vulnerabilities, fixes and creates PRs autonomously |

### ux — User Experience & Design

| Skill | Version | Description |
|-------|---------|-------------|
| [ux](ux/ux/) | 1.0.0 | Dual-mode UX audit (heuristics/a11y/motion) or design validation |

### analysis — Domain Analysis & Research

| Skill | Version | Description |
|-------|---------|-------------|
| [analyze](analysis/analyze/) | 3.0.0 | End-to-end domain analysis — traces features across all layers |
| [compete](analysis/compete/) | 1.0.0 | Researches competitors, produces prioritized feature gap analysis |
| [mvp](analysis/mvp/) | 2.0.0 | Analyzes app video/screenshots to decipher MVP and suggest improvements |
| [metrics](analysis/metrics/) | 1.0.0 | Computes development quality metrics from git history |
| [recall](analysis/recall/) | 1.0.0 | Reconstructs development cycle from git, extracts patterns |
| [cost-analysis](analysis/cost-analysis/) | 1.0.0 | Analyzes Firebase infrastructure costs at multiple user scales |
| [dep-map](analysis/dep-map/) | 1.0.0 | Maps story dependencies, computes optimal implementation order |
| [backend-spec](analysis/backend-spec/) | 5.0.0 | Generates engineering specs in Jira format with acceptance criteria |
| [image-storage-optimization](analysis/image-storage-optimization/) | 1.0.0 | Enforces image resizing/compression to reduce storage costs |

### productivity — Workflow Automation

| Skill | Version | Description |
|-------|---------|-------------|
| [vscode](productivity/vscode/) | 1.0.0 | Opens VS Code in the current working directory |

### combo — Multi-Skill Chains

| Skill | Version | Chain | Description |
|-------|---------|-------|-------------|
| [polish](combo/polish/) | 3.0.0 | /ux ∥ /scale-audit → /qa → /analyze | Full quality pass with parallel tracks |
| [research](combo/research/) | 1.0.0 | /compete → /new-features | Competitive analysis + feature ideation |
| [spec](combo/spec/) | 1.0.0 | /mvp → /backend-spec | App analysis + story generation |
| [story](combo/story/) | 1.0.0 | /arch-review → /si → /pr | Full story lifecycle |
| [review-implement](combo/review-implement/) | 1.0.0 | /arch-review → /si | Review design then implement |
| [full-test](combo/full-test/) | 1.0.0 | /e2e → /manual-test-plan | Automated + manual test plans |
| [retro](combo/retro/) | 1.0.0 | /recall → /new-features | Dev retrospective + feature ideas |
| [fix-and-ship](combo/fix-and-ship/) | 1.0.0 | /hotfix → /preflight | Emergency fix + deploy verification |

### meta — Skills About Skills

| Skill | Version | Description |
|-------|---------|-------------|
| [bootstrap](meta/bootstrap/) | 3.0.0 | Scaffolds new projects from saved templates |
| [evolve](meta/evolve/) | 1.0.0 | Self-improving — patches skills based on /recall and /metrics findings |
| [extract-template](meta/extract-template/) | 1.0.0 | Captures pipeline + conventions as reusable template |
| [promote](meta/promote/) | 1.0.0 | Cross-project pattern detection, promotes to global conventions |

## Recommended Pipelines

### New Project
```
/bootstrap → /research → /spec → /build → /polish
```

### Feature Development
```
/backend-spec → /arch-review → /story-implementer → /qa
```

### Fast Iteration
```
/ship [task] → /qa → /analyze
```

### Quality Gate
```
/polish  (runs: /ux ∥ /scale-audit → /qa → /analyze)
```

### Retrospective
```
/recall → /metrics → /evolve
```

## Skill Dependency Graph

```
/build (orchestrator)
  ├── /mvp
  ├── /backend-spec
  ├── /arch-review (parallel)
  ├── /story-implementer (parallel)
  ├── /ux ∥ /manual-test-plan
  ├── /qa
  └── /analyze

/ship (fast build)
  ├── pre-build validation
  ├── /analyze (iteration 3)
  └── /readme

/iterate (iterative build)
  ├── pre-build validation
  ├── /analyze (iterations 2, final)
  └── /readme

/polish (quality combo)
  ├── /ux (parallel track A)
  ├── /scale-audit (parallel track B)
  ├── /qa
  └── /analyze

/qa (testing)
  └── /analyze (phase 4)

/evolve (meta)
  └── reads /recall + /metrics output
```

## SKILL.md Format

Every skill uses the skills-hub.ai marketplace format:

```yaml
---
name: my-skill
description: One-sentence description of what it does (10-1000 chars)
version: "1.0.0"
category: build
platforms:
  - CLAUDE_CODE
---

Your skill instructions here. This is the main content
loaded as context when the skill is invoked.
```

### Valid Categories

`build` `test` `qa` `review` `deploy` `docs` `security` `ux` `analysis` `productivity` `integration` `combo` `meta`

### Valid Platforms

`CLAUDE_CODE` `CURSOR` `CODEX_CLI` `OTHER`

### Quality Scoring

Skills are scored 0-100 on the marketplace:
- **Schema (0-25):** Required fields present, description >= 50 chars, valid semver, valid category
- **Instructions (0-75):** >= 500 chars, structured phases/steps, I/O spec, error handling, guardrails, examples, output format
- **Minimum to publish:** 20

## Contributing

1. Create a new directory under the appropriate category: `{category}/{skill-name}/SKILL.md`
2. Follow the SKILL.md format above
3. Ensure your skill scores >= 20 on the quality scale
4. Submit a PR

## Key Design Patterns

These patterns are validated across 7+ production projects:

- **Self-healing loops:** Skills iterate up to N times, fixing issues found each pass
- **Pre-build validation:** Static analysis gate before feature work begins
- **Co-commit rules:** Firestore rules, server validation, and model serialization ship with features
- **Domain analysis feedback:** `/analyze` embedded as a quality gate in build loops
- **Parallel execution:** Independent tracks run concurrently via Task tool subagents
- **Wiring completeness:** Detect features that exist in one layer but are never connected
- **Monolith decomposition:** Files exceeding 500 lines are split before adding features
