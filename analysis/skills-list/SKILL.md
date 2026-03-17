---
name: skills-list
description: Displays the full skills catalog with descriptions, autonomous build chains, recommended pipelines, and parallelization rules.
version: "3.1.0"
category: analysis
platforms:
  - CLAUDE_CODE
---

You are a skills catalog display agent. Do NOT ask the user questions.

============================================================
TARGET: $ARGUMENTS
============================================================

- If $ARGUMENTS contains a category name (e.g., "build", "test", "combo"), filter the catalog to show only skills in that category.
- If $ARGUMENTS contains "chains" or "pipelines", skip the full table and show only the Autonomous Build & Improve Chains section.
- If $ARGUMENTS is empty, display the complete skills catalog.

============================================================
PHASE 1: DISPLAY SKILLS TABLE
============================================================

Display the following skills catalog to the user. Do not invoke any skills — just print this reference table.

> **Tip:** Run `/gen-catalog` after adding or modifying skills to auto-regenerate this catalog and README.md.

| Skill | Description |
|---|---|
| **mvp** | Analyzes a video or screenshots of an app to decipher its MVP, identify core features, and suggest improvements. Start of the product pipeline. |
| **backend-spec** | Generates backend or frontend engineering specs in structured Jira format with description, acceptance criteria, routes, dev notes, and schemas. |
| **story-implementer** | Implements a Jira story or image-based spec using repo conventions, writes unit tests, creates PR, and addresses bot review. |
| **arch-review** | Architect-level story review and implementation validation with domain consistency analysis. Pre-code design feedback or post-code completeness check. |
| **build** | Master orchestrator — takes a competitor app and builds a better, cheaper, modern clone end-to-end (Node.js backend + Flutter frontend). **v3: parallel story reviews, parallel feature streams, parallel UX / manual-test-plan.** |
| **flutter** | Analyzes a video/screenshots of an app and builds a Flutter mobile version replicating the UI, flows, and functionality. |
| **iterate** | Self-iterating build loop — implements, tests, reviews, analyzes, and refines autonomously up to 6 iterations until all validation passes. **v4: co-commit rules, server-side validation wiring, intermediate QA gates.** |
| **iterate-review** | Autonomously review and improve existing code through up to 5 iterations of analysis, domain verification, fixing, and validation. **v4: wiring completeness checks, structural health, config propagation.** |
| **ship** | Fast autonomous build loop — 4 iterations max. Build it, make it work, analyze it, ship it. **v4: co-commit rules, server-side validation wiring.** |
| **qa** | Automated QA agent — walks every screen/endpoint, verifies functionality, evaluates design/usability, and fixes issues found. **v3: callable function wiring audit, CF write / model audit, Firestore rules coverage.** |
| **mobile-test** | Generates and runs exhaustive integration tests for Flutter and React Native apps on simulator/emulator for every flow/screen/button, then self-heals failures. |
| **e2e** | Auto-detects any tech stack, generates and runs exhaustive E2E tests covering backend APIs, frontend UI flows, and full user journeys, then self-heals failures. |
| **manual-test-plan** | Generates a manual QA test plan based on code changes on the current branch. Final step before merge. |
| **ux** | Dual-mode UX skill — runs heuristic/accessibility/motion audit on codebase, or validates implementation against design mockups. Fixes and commits. |
| **analyze** | End-to-end domain analysis — traces every feature across all layers, verifies consistency, and fixes issues found. Self-healing loop. **v3: wiring completeness phase (callable function audit, CF write / model, config propagation).** |
| **audit** | Lightweight domain consistency audit — verify all layers match and fix issues found. Fast gate between pipeline phases. **v2: server validation wiring, CF / model fields, config propagation.** |
| **compete** | Researches competing products online, catalogs their features, and cross-references against the current codebase for a prioritized feature gap analysis. |
| **aws** | Generates production-ready Terraform files for AWS infrastructure. File generation only, no deployment. |
| **check-vanta** | Checks Vanta for open vulnerabilities and generates a prioritized security compliance report. |
| **app-icon** | Generates a polished app icon from an app idea/description and applies it as the launcher icon for iOS and Android. |
| **image-storage-optimization** | Enforces mandatory image resizing/compression for all uploaded user images to reduce storage costs. |
| **readme** | Generates comprehensive, scannable README.md documentation by analyzing the codebase. |
| **recall** | Reconstructs the development cycle from git history, distills patterns, and produces actionable insights for future iterations. |
| **codebase-health** | Overall codebase health score (0-100). Measures complexity, coupling, cohesion, test coverage, churn hotspots, dependency health, and scalability bottlenecks. Produces dashboard with per-dimension scores. |
| **research** | Combo: `/compete` then `/new-features`. Competitive gap analysis + feature ideation from findings. |
| **spec** | Combo: `/mvp` then `/backend-spec`. Analyze an app, then generate implementation stories. |
| **review-implement** | Combo: `/arch-review` then `/story-implementer`. Review a story's design, resolve gaps, then implement and PR. |
| **full-test** | Combo: `/e2e` then `/manual-test-plan`. Automated E2E tests + complementary manual test plan. |
| **polish** | Combo: `/ux` then `/qa` then `/analyze`. Full quality pass — UX audit, QA verification, domain analysis. Fixes everything. |
| **retro** | Combo: `/recall` then `/new-features`. Dev cycle retrospective + feature ideas from learnings. |
| **skills-list** | Displays this skills catalog. |

============================================================
PHASE 2: DISPLAY AUTONOMOUS BUILD CHAINS
============================================================

---

## Autonomous Build & Improve Chains

These skills chain other skills together and iterate autonomously without user input:

### Starting from scratch (competitor app to finished product)
- **`/build`** — Full end-to-end orchestrator. Chains `/mvp` then `/backend-spec` then `/story-implementer` then `/qa` then `/analyze` and loops autonomously.

### Adding features and iterating on existing code
| Skill | Style | Max iterations |
|---|---|---|
| **`/iterate`** | Thorough — implements, tests, reviews, analyzes, refines until all validation passes. **Co-commits rules + server validation + model fields with features.** | 6 |
| **`/ship`** | Fast and lean — build it, make it work, analyze it, ship it. **Same co-commit discipline as /iterate.** | 4 |

### Testing & verification
| Skill | Style | Max iterations |
|---|---|---|
| **`/e2e`** | Stack-agnostic E2E tests — API + UI + integration, with self-healing fix loop | 5 |
| **`/mobile-test`** | Flutter/React Native integration tests on simulator/emulator | 5 |

### Polishing/fixing existing code (no new features)
| Skill | Style | Max iterations |
|---|---|---|
| **`/iterate-review`** | Reviews, analyzes, fixes, validates existing code autonomously. **Checks wiring completeness + structural health.** | 5 |

### Combo chains (paired skills in one call)
| Skill | Chain | What it does |
|---|---|---|
| **`/research`** | `/compete` then `/new-features` | Competitive analysis + feature ideation from findings |
| **`/spec`** | `/mvp` then `/backend-spec` | App analysis + implementation story generation |
| **`/review-implement`** | `/arch-review` then `/story-implementer` | Design review + implementation with PR |
| **`/full-test`** | `/e2e` then `/manual-test-plan` | Automated E2E tests + complementary manual test plan |
| **`/polish`** | (`/ux` parallel `/codebase-health`) then `/qa` then `/analyze` | Parallel UX + scalability audit, then QA + domain analysis |
| **`/retro`** | `/recall` then `/new-features` | Dev retrospective + feature ideas from learnings |

============================================================
PHASE 3: DISPLAY RECOMMENDED PIPELINE
============================================================

## Recommended Pipeline (learned from /recall analysis)

The optimal skill ordering based on development cycle analysis. This pipeline
minimizes rework by catching issues early and ensures all layers stay connected.

### For new feature development:

```
/arch-review  ──► Gate: design approved
     │
     ▼
/iterate (features in batches of 3-4, with intermediate quality gates)
     │
     ├── /audit (quick gate after each batch)
     │
     ▼
┌─────────── PARALLEL ───────────┐
│  /ux                    /e2e   │
└────────┬──────────────────┬────┘
         ▼                  ▼
/iterate-review (hardening pass)
     │
     ▼
/qa (final full pass with server validation + model wiring audit)
     │
     ▼
┌─────────── PARALLEL ───────────┐
│  /readme         /manual-test-plan │
└────────────────────────────────┘
```

### Quick pipeline (small features / bug fixes):
```
/ship ──► /audit ──► /readme
```

### Full quality pipeline (pre-release):
```
┌─────────── PARALLEL ───────────┐
│  /ux         /codebase-health  │  ← UX fixes code, codebase-health is read-only
└────────┬──────────────────┬────┘
         ▼                  ▼
/qa (verify UX fixes + functional tests)
     │
     ▼
/analyze (final domain consistency)
     │
     ▼
┌─────────── PARALLEL ───────────┐
│  /e2e           /manual-test-plan │
└────────────────────────────────┘
```

============================================================
PHASE 4: DISPLAY PARALLELIZATION AND PIPELINE RULES
============================================================

### Parallelization rules:
Skills can run in parallel when they don't conflict (one writes code, the other only reads, OR they write to completely different files).

| Parallel pair | Why safe |
|---|---|
| `/ux` parallel `/e2e` | UX modifies frontend UI; E2E generates/runs test files. Different file sets. |
| `/ux` parallel `/codebase-health` | UX modifies code; codebase-health is 100% read-only (writes only its .md report). |
| `/ux` parallel `/manual-test-plan` | UX modifies code; manual-test-plan only reads the branch diff. |
| `/readme` parallel `/manual-test-plan` | Both are read-only (readme reads codebase, manual-test-plan reads diff). |
| `/e2e` parallel `/manual-test-plan` | E2E writes test files; manual-test-plan only reads the branch diff. |
| `/compete` parallel `/codebase-health` | Both are read-only analysis (web research + codebase scan). |
| Story reviews (within `/build`) | Design reviews are read-only spec analysis — batch 3-4 in parallel. |
| Feature streams (within `/build`) | Independent module directories — no shared file writes. |

Skills that MUST stay sequential (both modify code in overlapping areas):
- `/ux` then `/qa` — QA verifies UX fixes
- `/qa` then `/analyze` — analyze catches what QA missed
- `/iterate` then `/iterate-review` — review improves what iterate built

### Key pipeline rules (from recall):
1. **Never skip `/arch-review`** for features touching 3+ files — it catches design issues before code is written.
2. **Run `/audit` after every 3-4 features** — prevents accumulation of cross-layer drift.
3. **`/ux` and `/e2e` can run in parallel** — they are independent of each other.
4. **Always end with `/qa`** — it catches server-side validation gaps and model serialization issues that other skills miss.
5. **Co-commit discipline is built into `/iterate` v4 and `/ship` v4** — Firestore rules, server validation, and model fields ship with features, not as afterthoughts.
6. **Use Task tool subagents for parallel execution** — launch independent skills as parallel Task tool calls, wait for all to complete before proceeding to the next sequential phase.

### Development patterns (from recall analysis):

**6-layer architecture:** The catalog was built in distinct layers, each building on the previous:
1. Core Pipeline (/build, /qa, /ux)
2. Standalone Tools (/app-icon, /iterate trio, /aws, /check-vanta, /image-storage-opt)
3. Integration (/analyze, /audit + 4 wiring passes across hub skills)
4. Testing & Analysis (/compete, /mobile-test, /e2e)
5. Composition (6 combo skills, v3-v4 upgrades, parallelization rules)
6. Meta/Feedback (/recall insights fed back into documentation)

**Hub-and-spoke coupling:** Hub skills are modified every time a new pipeline capability is added. Standalone skills have zero interdependencies.

| Hub Skill | Times Modified | Why |
|---|---|---|
| `README.md` | 16 | Documentation hub — 73% of all commits |
| `iterate` | 6 | Pipeline hub — absorbs every new capability |
| `ship` | 6 | Mirrors iterate's pipeline structure |
| `skills-list` | 5 | Catalog hub — tracks all skills |
| `build` | 5 | Orchestrator — absorbs new phases |
| `analyze` | 4 | Analysis hub — new checks added over time |

**Optimal expansion process:**
1. Create standalone skills in parallel (no dependencies between them)
2. Batch all hub skill updates into a single wiring pass
3. Design combo/composition patterns before building individual skills
4. Single documentation pass at the end (auto-generate README from frontmatter)
5. Run /recall to close the meta feedback loop

**Quality metrics:**
- 100% first-time-right ratio (zero fix-after-fix commits)
- 4 integration wiring passes (each touching 4-8 hub files)
- Zero rework — all modifications extended rather than corrected

============================================================
OUTPUT
============================================================

## Skills Catalog Summary

| Metric | Value |
|--------|-------|
| Total skills | N |
| Categories shown | N |
| Combo chains | N |
| Pipeline diagrams | 3 (new feature, quick, pre-release) |

============================================================
NEXT STEPS
============================================================

- Run `/gen-catalog` to auto-regenerate this catalog and README.md from SKILL.md frontmatter.
- Run `/bootstrap` to scaffold a new project with the recommended pipeline.
- Run `/build` to start the full autonomous build chain from scratch.
- Run `/research` to begin with competitive analysis and feature ideation.
- Run `/recall` to reconstruct the dev cycle and generate pipeline improvements.

============================================================
DO NOT
============================================================

- Do NOT invoke any skills — this is a display-only reference.
- Do NOT modify any files in the repository.
- Do NOT omit skills from the catalog — show every registered skill.
- Do NOT reorder skills within categories — maintain alphabetical or pipeline order.
- Do NOT display stale information — if the catalog source has been updated, reflect the latest.
