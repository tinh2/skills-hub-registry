# Development Cycle Recall

**Generated**: 2026-06-07  
**Previous report**: 2026-06-01 (overwritten per FILE NAMING DISCIPLINE)

---

## Scope

- **Repository**: skills-hub-registry
- **Branch**: main (single remote: origin)
- **Period**: 2026-02-28 → 2026-06-06 (98 days)
- **Total commits**: 190 raw (142 unique — early scaffold duplicated every commit)
- **Files changed**: 612
- **Lines**: +179,831 / -3,688
- **Authors**: Tho Le (177 commits), Claude automated (13 commits)

---

## ⚠️ PHANTOM PROGRESS — Uncommitted WIP

56 lines of changes exist in tracked files not yet in git history. Ready-to-run close:

```bash
# Python: skill-creator generate_report and eval runner
git add meta/skill-creator/scripts/generate_report.py scripts/test_run_eval.py
git commit -m "chore(meta): update generate_report and test_run_eval scripts"

# CSS: editorial-app-craft token additions
git add build/editorial-app-craft/assets/design-tokens.css build/editorial-app-craft/assets/patterns.css
git commit -m "chore(build): update editorial-app-craft design tokens and patterns"
```

---

## Timeline

```
[2026-02-28 16:32–19:57] PHASE 1: Day-0 Scaffold (58 commits, 3.5 hours)
  0 → 45 skills (initial) → 359 skills (social-impact, industry verticals, gaming, mobile)
  Rapid-fire. Every commit appears twice (duplicate hash pattern — two git histories merged at origin).

[2026-03-01 00:17–01:07] PHASE 2: Structural QA (8 commits)
  Fix broken frontmatter, name mismatches, add missing structural elements.
  Research: competitive gap analysis doc created.

[2026-03-06 01:38–01:40] PHASE 3: Reference Fixes (2 commits, 5-day gap)
  Fix broken cross-skill references. Sync README skill versions.

[2026-03-13 18:39–23:33] PHASE 4: Quality Upgrade Sweep (8 commits, burst day)
  Upgrade 52+313+10 skills with trigger-rich descriptions, multi-stack support,
  standardized frontmatter. 365 skills touched in one day.

[2026-03-15 18:55–21:14] PHASE 5: Registry QA (12 commits — biggest single-day fix cluster)
  Repair a11y in eval HTML, remove duplicate lowercase files, fix YAML blocks,
  add missing fields, sync README counts, document 19 duplicate skill names.
  Root cause: bulk scaffold produced inconsistent quality — caught 2 weeks late.

[2026-03-16 13:09–2026-03-18 13:10] PHASE 6: CI Infrastructure (8 commits)
  Add validate-skills.sh, GitHub Actions workflow. Three CI fix commits to get it passing
  (bash 3.2 compat, herestring fix, broken pipe fix). Self-hosted runner setup.

[2026-03-18 11:46–11:58] PHASE 7: Feature + PII scrub (2 commits)
  Add 20 autonomous design skills. Remove PII for public release.

[2026-03-19 16:39–23:35] PHASE 8: Sync + Repair (6 commits)
  Sync iterate v11, ship v2.0.0, arch-review v9. Fix frontmatter YAML parsing errors (9 skills).
  Fix design-overhaul/pipeline duplicate issue (created, then re-removed).

[2026-03-24 11:48–16:42] PHASE 9: Content Skills Burst (6 commits)
  7 education skills, 5 new skills (self-healing telemetry added), blog-writer, ci-fixer,
  gitignore cleanup, CI pipe fix.

[2026-03-25 00:11–2026-03-26 20:50] PHASE 10: Video & Infra Skills (9 commits, 2 days)
  video creation, arch-review v10, broken-links, flutter-ship → ship-pipeline v3,
  Google Stitch integration, quickstart, 4 video skills + Remotion ecosystem.

[2026-03-27 07:57–2026-04-01 17:09] PHASE 11: Maintenance + Tend (5 commits, 5 days)
  Add skill-creator test suites. cnc-furniture skill. Add .aider* to gitignore.
  CI actions Node.js 24 upgrade. Tend polish + trap cleanup.

[2026-04-09 10:00] PHASE 12: Design skills sync (1 commit)
  Add missing design skills, sync updates. 8-day gap since last commit.

[2026-04-15 14:18–22:50] PHASE 13: Meta tools (4 commits, burst)
  skillify v1.1.0, publish-skill v1.0.0, test suites for eval pipeline/recall,
  remove duplicate design-overhaul entries.

[2026-04-19 13:09–13:13] PHASE 14: Orchestrator & Reference Fix (2 commits)
  scale-audit + new-features skills. Fix /ship-it → /ship-pipeline refs across all skills.

[2026-04-26 17:32–2026-04-30 16:07] PHASE 15: Growth (5 commits, 5 days)
  design-claude, README sync (428 skills), README/category fixes, web-research,
  excalidraw, seo 2.1.0, marketing 2.0.0, youtube-research.

[2026-05-20 23:34–2026-05-22 08:47] PHASE 16: UX Sweep Cluster (6 commits, ~33 hours)
  4 marketing/SEO/AEO/GEO skills. copilot-credits-audit (Claude auto). editorial-app-craft,
  ui-craft, bug-sweep, css-token-sweep, mobile-sweep v1.0 → v1.1 (next morning).
  Rapid sequential build of a full "sweep" skills suite.

[2026-05-22 12:16–2026-05-23 10:47] PHASE 17: Industry Skill Explosion (7 commits, ~22 hours)
  evolve 2026-05-22 (5 patches). parallel-features + design-build gating. skill-finder v2.0.0.
  26 industry analysis skills across 5 commits: Manufacturing, Real Estate, SEO/GEO,
  Ecommerce, HR, Logistics, Government, Media, Finance. 5 SEO suite skills.

[2026-05-21 15:07–2026-06-06 15:13] PHASE 18: Automated Daily Pipeline (13 commits)
  Claude-authored, consistent ~15:15 UTC cadence (one per day):
  copilot-credits-audit → windsurf-spaces → cursor-parallel → antigravity-sdk →
  kiro-spec-driven → gemini-cli-migration → dynamic-skill-loader → kiro-quick-plan →
  requirements-verification → codex-bedrock → [recall 2026-06-01] →
  save-tokens v1→v2→v3 → acp-multi-agent → cursor-agent-safety → mcp-protocol-migration

[2026-06-01 03:01–05:08] PHASE 19: Docs + save-tokens Iteration (5 commits)
  Prior /recall report. Competitive gap analysis update.
  save-tokens: v1 (cloud LLM) → v2 fix (Ollama-only) → v3 (zero-LLM default) in 2 days.
```

---

## Pipeline Execution Map

```
Canonical:  /mvp → /spec → /arch-review → /story-implementer → /ux → /qa → /analyze
Actual:     scaffold → quality-sweep → CI-infra → /evolve ⟳ → /tend ⟳ → /recall ⟳
```

This is a **content creation project** (skill library), not a software product build, so the
canonical pipeline doesn't apply directly. The actual meta-pipeline is:

```
scaffold → bulk-quality-fix → CI-validation → organic-growth → /evolve → /tend → /recall
              ↑ late catch                                         (repeat cycle)
```

Mark: ✓ scaffold, ⟳ /evolve (multiple runs), ⟳ /tend (multiple runs), ⟳ /recall (running now),
⊘ /spec (not applicable), ⊘ /story-implementer (not applicable)

---

## Sequential vs Parallel Analysis

| Phase/Feature                                | Execution         | Dependencies                  | Could Parallelize?               | Est. Time Saved |
| -------------------------------------------- | ----------------- | ----------------------------- | -------------------------------- | --------------- |
| Day-0 scaffold (45→359 skills)               | Sequential        | None — all independent        | ✅ 4 parallel agents by category | ~75% of 3.5h    |
| March quality sweep (313 skills)             | Sequential        | None                          | ✅ Parallel by category          | ~60% of effort  |
| CI infra (3 fix commits to work)             | Sequential (must) | Each depends on prior failure | ❌ No                            | —               |
| Industry skills burst (26 skills, May 22-23) | Sequential        | None                          | ✅ 4 parallel agents by sector   | ~70% of 22h     |
| UX sweep cluster (6 skills)                  | Sequential        | None                          | ✅ 3 parallel agents             | ~60%            |
| Automated daily pipeline (13 skills)         | 1/day sequential  | None                          | ✅ Could batch                   | ~90%            |

**Biggest opportunity**: The automated daily pipeline runs 1 skill/day for 13 days. These are fully independent new skill additions. Batching into 2-3 parallel sessions would cut wall-clock time from 13 days to ~4-5 days.

---

## Iteration Efficiency

| Skill/Area                    | Iterations                       | Rework % | First-Time-Right | Top Rework Cause                              |
| ----------------------------- | -------------------------------- | -------- | ---------------- | --------------------------------------------- |
| save-tokens                   | 3 (v1→v2 fix→v3)                 | 67%      | ❌               | Design ambiguity: cloud vs Ollama vs zero-LLM |
| validate-skills.sh / CI       | 4 (3 fix commits)                | 75%      | ❌               | Bash 3.2 compat, pipe syntax, macOS vs Linux  |
| design-overhaul/pipeline      | 2 (created, removed, re-created) | 50%      | ❌               | Duplicate location confusion                  |
| Automated daily skills (13)   | 1 each                           | 0%       | ✅               | —                                             |
| Industry analysis skills (26) | 1 each                           | 0%       | ✅               | —                                             |
| mobile-sweep                  | 2 (v1.0→v1.1 next day)           | 50%      | ❌               | Missing WCAG exemption flags                  |

**Overall fix:feat ratio**: 36/112 = **0.32** (down from 0.47 baseline — significant improvement)

---

## Rework Hotspots

| File/Area                           | Times Modified | Fix Commits     | Root Cause                                                        |
| ----------------------------------- | -------------- | --------------- | ----------------------------------------------------------------- |
| README.md                           | 28             | ~10             | README is generated from skills — every skill batch requires sync |
| review/arch-review/SKILL.md         | 22             | ~5              | Active high-value skill, frequently upgraded                      |
| build/ship/SKILL.md                 | 16             | ~3              | ship-pipeline renamed/refactored mid-lifecycle                    |
| combo/README.md, analysis/README.md | 15 each        | ~6              | Category READMEs lag every skill addition                         |
| Frontmatter (many SKILL.md files)   | N/A            | 15+ fix commits | Bulk scaffold didn't validate YAML at creation                    |

**Pattern**: README drift is structural — README.md modified 28× because it's manually synced after
every skill batch. A script/CI check for README-skill count drift would eliminate most of these.

---

## Dependency Graph

```
Day-0 Scaffold (Feb 28)
    ↓
Quality Fix Sweep (Mar 1, 15) ←── Late catch: 2-week lag
    ↓
CI Infrastructure (Mar 16-18) ←── Enables ongoing validation
    ↓
Quality Upgrade Sweep (Mar 13-18) ←── All 366 skills standardized
    ↓
Organic Growth Cluster ─────────────────────────────────────────────────────────────┐
│ video skills → ship-pipeline → stitch → arch-review v10 → broken-links → blog-writer │
└────────────────────────────────────────────────────────────────────────────────────┘
    ↓
/evolve run (May 22) ←── Cross-project recall drove this
    ↓
UX Sweep Cluster (May 21-22) ─┐
Industry Burst (May 22-23) ───┤ ← Parallel in time but sequential in execution
Automated Daily (May 21+) ────┘
    ↓
/recall (Jun 1, Jun 7) ←── Closing feedback loop
    ↓
[Current state — uncommitted WIP in editorial-app-craft + skill-creator]
```

Critical path: Scaffold → Quality Fix → CI → (everything else is parallel-ready)

---

## Key Insights

### What worked

1. **Automated daily pipeline has 0 rework** — 13 skills added by Claude with no follow-up fix commits. When the scope is narrow (one skill, no cross-file refs), automated authoring is highly reliable.

2. **fix:feat ratio dropped from 0.47 → 0.32** — Quality is trending in the right direction. The CI validation gate (added March 16) likely accounts for most of this improvement.

3. **Industry skill burst (26 skills, 22 hours) shipped clean** — No fix commits followed. Suggests the skill template is mature enough to scale.

4. **/evolve + /recall feedback loop is working** — The May 22 evolve run was directly traceable to cross-project recall findings. The loop (recall → learn → evolve → ship) is closing properly.

5. **Burst-day patterns are productive** — The largest feature days (Feb 28: 58 commits; Mar 15: 12 commits; Mar 18: 8 commits; May 22: 7 commits) account for ~60% of the value shipped.

### What caused unnecessary rework

1. **Scaffold produced systematically broken YAML** — 15+ fix commits across March 1-15 were fixing frontmatter, missing fields, and duplicates that were all baked in at scaffold time. Adding a YAML validation pre-commit hook at Day 0 would have eliminated this entire fix cluster.

2. **README.md is manually synced → perpetual drift** — 28 modifications to README.md, mostly count updates. A CI check comparing `find . -name SKILL.md | wc -l` against the README count would make this self-correcting.

3. **save-tokens needed 3 attempts to stabilize** — Design ambiguity (cloud LLM vs local Ollama vs zero-LLM) wasn't resolved before v1 shipped. A one-paragraph design brief before implementation would have produced v3 directly.

4. **CI took 4 commits to pass** — The `validate-skills.sh` script was written for Linux but ran on macOS (bash 3.2). Testing locally on the target platform before pushing would have prevented 3 follow-up fix commits.

5. **design-overhaul/pipeline created twice** — Files created in `ux/` were already in `combo/`. No dedup check at creation time produced the confusion.

### Bottlenecks

1. **Automated pipeline: 1 skill/day** — 13 days for 13 fully independent skills. At 0% rework rate, this is purely a scheduling constraint, not a quality constraint. Batching 4-5 in parallel would cut to 3 days.

2. **README sync** — Every skill batch requires a manual README update commit. This is implicit overhead on every feature that isn't measured but adds ~1 commit overhead per batch.

3. **Uncommitted WIP** — 4 files with 56 lines of changes are invisible to git history right now. Small but represents work-in-progress that isn't captured.

---

## Recommendations for Next Iteration

1. **Add YAML validation pre-commit hook** — Run `validate-skills.sh` before every commit. Why: 15+ fix commits across March were fixing frontmatter issues baked in at creation time. Expected impact: eliminate the entire "structural QA" phase.

2. **Auto-generate README counts in CI** — Script that counts SKILL.md files per category and updates README.md automatically. Why: 28 README.md modifications, mostly count drift. Expected impact: eliminate ~15 mechanical README commits.

3. **Batch the automated daily pipeline** — Instead of 1 skill/day over 13 days, run 4-5 parallel sessions per batch. Why: 0% rework rate proves reliability — it's purely a scheduling bottleneck. Expected impact: 13 days → 3 days for same output.

4. **Design brief before skill v1** — For any skill that touches external dependencies (LLMs, cloud, native APIs), write a one-paragraph design brief answering: what's the zero-dependency mode? Why: save-tokens needed 3 versions to answer this. Expected impact: eliminate v2/v3 rework cycles.

5. **Commit WIP before recall** — Close the phantom progress loop above before running analysis. 4 uncommitted files right now are invisible to this recall's timeline.

6. **Add dedup check to skill creation** — Before creating a new SKILL.md, grep for the skill name across existing files. Why: design-overhaul/pipeline was created twice in different locations. Expected impact: eliminate duplicate-then-remove commits.

---

## Suggested Pipeline for Next Build Cycle

```
skill-idea → design-brief (1 para: scope, zero-dep mode, trigger)
    → create SKILL.md (validate-skills.sh passes locally)
    → commit (pre-commit hook enforces validation)
    → CI auto-updates README counts
    → /evolve (periodic batch, draw from cross-project recalls)
    → /recall (monthly or after burst sessions)
```

**For bulk skill batches** (industry verticals, sweep suites):

```
batch-idea
    ├─ agent-1: sector A (4-5 skills)
    ├─ agent-2: sector B (4-5 skills)  ← parallel
    ├─ agent-3: sector C (4-5 skills)
    └─ merge → validate all → commit batch
```

---

_Next steps: Run `/evolve` incorporating the dedup-check and design-brief recommendations. Commit the uncommitted WIP above first._
