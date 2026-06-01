# Development Cycle Recall

**Generated**: 2026-06-01  
**Previous report**: 2026-05-15 (overwritten per FILE NAMING DISCIPLINE)

---

## Scope

- **Repository**: skills-hub-registry
- **Branch**: main (linear history, no feature branches)
- **Period**: 2026-02-28 → 2026-05-31 (92 days)
- **Total commits**: ~90 unique (git log --all shows 180 due to local + remote ref duplication)
- **Total files changed**: 606 files, +178,091 / -3,688 lines
- **Current skill count**: 483 SKILL.md files
- **Authors**: Tho Le (124 entries), Claude / automated (8 entries)

---

## Uncommitted WIP

`docs/competitive-gap-analysis.md` has 423 lines changed (+230/-193) uncommitted. This is docs-only — no source phantom progress detected.

---

## Timeline

```
[2026-02-28 16:32–22:00] BURST PHASE — 45 → 359 skills in ~5.5 hrs  (22 commits, +170k lines)
  Initial scaffold (45 skills) → integration, deploy, security, test, docs, productivity,
  QA, review, UX, build/meta, combo chains → industry verticals (healthcare, finance,
  logistics, construction, manufacturing, legal, energy) → social impact (58 skills) →
  gaming (21 skills) → mobile (20 skills) → 88 more industry skills across 21 sectors
  → all README docs regenerated (5 docs commits)

[2026-03-01 00:17–01:07] INITIAL QUALITY PASS — fix missing structure, upgrade 24 originals,
  competitive gap analysis research  (3 commits)

[2026-03-06 01:38–01:40] CROSS-REF FIX — broken references + README version sync  (2 commits)

[2026-03-13 18:39–23:33] MASS QUALITY UPGRADE — upgrade 52 skills, improve 313 remaining,
  improve final 10 analysis skills (3 commits, ~8k lines changed)

[2026-03-15 18:55–21:14] VALIDATION CLEANUP — fix a11y in HTML, remove duplicate files,
  repair broken YAML frontmatter (×10), fix missing name field, add 25 missing READMEs,
  sync 16 version mismatches  (6 commits)

[2026-03-16 13:09–20:43] CI INFRASTRUCTURE — validate-skills.sh, GitHub Actions workflow,
  broken frontmatter fix, duplicate cleanup  (4 commits)

[2026-03-17 07:23–22:18] CI STABILIZATION — workflow_dispatch trigger, remove dup vscode,
  docs marketing refresh  (3 commits)

[2026-03-18 08:49–11:46] FEATURE + FIX BURST — add 20 autonomous design skills, self-healing
  to all 366 skills, remove PII, fix README counts, fix bash 3.2 compat  (5 commits)

[2026-03-19 08:07–23:35] CLEANUP SPRINT — enhance-skills tests, sync iterate/ship/arch-review,
  add broadcast/ci-health/marketing-refresh, fix empty stubs, fix YAML errors, dedup  (7 commits)

[2026-03-20 → 2026-03-27] EXPANSION WAVE 1 — flutter-deploy, fix PII, 7 edu skills, blog-writer,
  ci-fixer, arch-review v10, broken-links + mobile/RN support, ship-pipeline v2/v3,
  Google Stitch skills, quickstart, 4 video skills + Remotion research, cnc-furniture  (13 commits)

[2026-03-30 → 2026-04-09] MAINTENANCE — .aider gitignore, CI → Node 24, tend fixes,
  design skills sync  (4 commits)

[2026-04-15 → 2026-04-19] META TOOLS — skillify v1.1, publish-skill, eval pipeline tests,
  duplicate cleanup, scale-audit + new-features skills, ship-it → ship-pipeline refs  (5 commits)

[2026-04-26 → 2026-04-30] CONTENT + TOOLS — design-claude skill, README sync (428 skills),
  web-research, excalidraw, seo 2.1.0, marketing 2.0.0, youtube-research  (7 commits)

[2026-05-20 → 2026-05-23] SPRINT: MARKETING/SEO + TOOL-SPECIFIC SKILLS
  4 marketing/SEO/AEO/GEO skills, copilot-credits-audit (Claude), editorial-app-craft,
  ui-craft, bug-sweep, css-token-sweep, mobile-sweep v1.0→v1.1  (8 commits by Tho Le)
  + windsurf-spaces, cursor-parallel (2 Claude commits)

[2026-05-22 → 2026-05-23] INDUSTRY EXPANSION SPRINT
  evolve cross-project patches, parallel-features + design-build, skill-finder v2.0.0,
  7 new industry skills (Manufacturing, Real Estate, SEO/GEO),
  6 skills (Ecommerce, HR, Logistics), 6 skills (Government, Media, Finance),
  7 skills (Real Estate, Ecommerce, Government), 5 SEO skills  (8 commits)
  + recall report (docs commit)

[2026-05-27 → 2026-05-31] AI TOOL MIGRATION SKILLS (5 Claude automated commits)
  antigravity-sdk, kiro-spec-driven, gemini-cli-migration, dynamic-skill-loader, kiro-quick-plan
```

---

## Pipeline Execution Map

This registry uses a **content-production pipeline**, not a software build pipeline. No `/mvp → /spec → /arch-review` sequence applies. The actual pipeline:

```
Actual:  BURST-ADD → quality-fix → CI-infra → mass-upgrade → evolve → expand → evolve
                         ⟳ repeated fix cycles in March            ⟳ ongoing expansion
```

Skill signatures detected:

- `/evolve`: `feat(skills): evolve 2026-05-22` — explicit evolve run
- `/tend`: `chore(tend)` commits (3) — automated tend pipeline
- `/recall`: `docs(tend): update auto-generated recall report` (May 23)
- **Automated remote trigger**: 8 `Claude`-authored commits (May 21 – May 31) — suggest a RemoteTrigger or scheduled pipeline for community skill contributions

---

## Sequential vs Parallel Analysis

| Phase/Feature                               | Execution  | Dependencies                              | Could Parallelize?                                       | Est. Time Saved |
| ------------------------------------------- | ---------- | ----------------------------------------- | -------------------------------------------------------- | --------------- |
| Feb 28 industry vertical batches (×5 waves) | Sequential | None — each batch is a different industry | Yes — 5 parallel                                         | ~4× speedup     |
| March 15–20 fix cluster (17 commits)        | Sequential | Some ordering needed                      | Partially — frontmatter fixes independent of README sync | ~30%            |
| May 22–23 industry expansion (4 batches)    | Sequential | None                                      | Yes — 4 parallel                                         | ~3× speedup     |
| May 20–23 sweep skills (×5 skills)          | Sequential | None                                      | Yes                                                      | ~4× speedup     |
| CI infra + feature adds (Mar 16–18)         | Sequential | CI infra first, then validate             | No (correct order)                                       | —               |

**Biggest parallelization gap**: The Feb 28 burst added 314 skills in 22 sequential commits. These could have been dispatched as 5–6 parallel agents (one per industry cluster), reducing wall-clock time from ~5.5 hrs to ~1 hr.

---

## Iteration Efficiency

| Area                    | First-Pass Commits     | Follow-on Fix Commits                      | First-Time-Right | Top Root Cause                                     |
| ----------------------- | ---------------------- | ------------------------------------------ | ---------------- | -------------------------------------------------- |
| Skill YAML frontmatter  | ~40 skills with issues | 6 fix commits (Mar 1–16)                   | ~85%             | Mass generation without per-file validation        |
| README / skill counts   | ~8 docs commits        | 5 fix commits                              | ~62%             | READMEs not regenerated atomically with skills     |
| CI / validate-skills.sh | 2 infra commits        | 3 fix commits (bash compat, pipe, version) | 40%              | Shell compatibility not tested on macOS bash 3.2   |
| Duplicate skills        | 1 dedup commit         | 3 more dedup commits                       | Recurring        | Design-overhaul/pipeline created in two places     |
| Cross-skill references  | 1 fix (Mar 6)          | 1 fix (Apr 19 ship-it refs)                | ~75%             | Reference targets renamed after widespread linking |

**Overall fix:feat ratio**: 25 fix / 79 feat = **0.32** (improved from baseline 0.47 — trend positive)

---

## Rework Hotspots

| File/Area                                | Times Modified | Initial Commits | Fix Commits             | Root Cause                                                             |
| ---------------------------------------- | -------------- | --------------- | ----------------------- | ---------------------------------------------------------------------- |
| `README.md`                              | 28             | ~15             | ~13                     | Every skill add triggers a count update; no automation                 |
| `review/arch-review/SKILL.md`            | 22             | 1               | 21 (iterative upgrades) | Most-evolved skill; each `/iterate` pass touches it                    |
| `build/ship/SKILL.md`                    | 16             | 1               | 15 (iterative)          | Core pipeline skill, renamed twice (flutter-ship → ship-pipeline → v3) |
| `combo/README.md` + `analysis/README.md` | 15             | 2               | 13                      | README-per-commit churn from manual syncing                            |
| `build/db-migrate/SKILL.md`              | 13             | 1               | 12                      | Heavily iterated                                                       |
| CI validate-skills.sh                    | 4              | 1               | 3                       | Bash compat, broken pipes discovered post-commit                       |

**Critical pattern**: `README.md` is modified 28 times — almost every feat commit requires a manual README update. This is a structural churn source.

---

## Dependency Graph

```
Initial batch (Feb 28)
    │
    ├──► YAML/structure fix (Mar 1)
    │         │
    │         └──► Cross-ref fix (Mar 6) ──► Mass quality upgrade (Mar 13-15)
    │                                                │
    │                                                └──► Fix cluster (Mar 15-20) ──► CI infra
    │                                                                                      │
    ├──── Feature expansion (Mar 24 – Apr 30) ◄──────────────────────────────────────────┘
    │         (blog-writer, broken-links, ship-pipeline, video skills, etc.)
    │
    └──── May sprint (May 20-31)
              ├── sweep skills (ux/review)
              ├── industry expansion (26 skills)
              └── AI tool migration skills (5 Claude auto)
```

Critical path: Initial burst → quality fix → CI infra → everything else

---

## Key Insights

**What worked:**

1. **Burst-then-fix pattern at scale**: Adding 314 skills in one evening and then doing quality passes in subsequent days produced a usable registry quickly. The rework cost was ~17 fix commits — high but bounded, and the result was a functional CI-validated registry within 3 weeks.

2. **CI gate addition (Mar 16)**: Adding `validate-skills.sh` + GitHub Actions created a quality floor. Most fix commits from March 19 onward were caught pre-merge rather than discovered late.

3. **evolve / tend automation**: The `chore(tend)` and `feat(skills): evolve` commits demonstrate a working automated pipeline that reduces manual skill maintenance. The 8 Claude-authored commits (May) suggest a functional remote trigger for community-contributed skills.

4. **Skill-finder v2.0 as orchestrator**: Upgrading skill-finder to a workflow orchestrator (May 22) is a meta-win — the registry's navigation layer keeps pace with its 483-skill depth.

5. **Fix:feat ratio improvement**: 0.32 vs baseline 0.47 — quality is trending up despite accelerating output.

**What caused unnecessary rework:**

1. **No atomic README generation**: Every skill add requires a manual README count update. This produced ~13 "fix README" commits and makes every feat commit 20% more likely to need a follow-on doc fix. → **Recommendation**: Auto-generate category READMEs from SKILL.md file count in a pre-commit hook or CI step.

2. **Mass generation without per-file validation**: The Feb 28 batch added 314 skills without running `validate-skills.sh` (which didn't exist yet). Result: 6 fix commits for YAML errors, duplicates, and missing fields. → **Recommendation**: Run validation locally before committing any batch larger than 10 skills.

3. **Duplicate skill locations**: design-overhaul and design-pipeline existed in both `ux/` and `combo/` — needed 3 separate dedup commits to fully resolve. → **Recommendation**: Enforce a "one canonical path per skill name" rule in validate-skills.sh (skill name must be unique across all paths).

4. **CI tested on GitHub Actions only, not macOS bash 3.2**: validate-skills.sh passed CI (Linux bash 5.x) but broke on macOS (bash 3.2). Needed 2 fix commits. → **Recommendation**: Add `shellcheck` + local bash 3.2 test to pre-commit hook.

5. **ship-pipeline naming churn**: flutter-ship → ship-pipeline required a global reference sweep (Apr 19). Naming settled too late — 50+ skills referenced the old name. → **Recommendation**: Finalize canonical skill names before cross-referencing.

**Bottlenecks:**

1. **Manual README maintenance**: The single highest-churn file (28 commits). Every batch add requires a manual sync pass. Automation would eliminate ~13 commits/cycle.

2. **Sequential industry batch expansion**: May 22-23 added 26 skills in 4 sequential commits that had zero dependencies on each other. Parallel agents would have reduced this from ~2 hrs to ~30 min.

3. **Fix cluster compaction**: The 17 fix commits in March 15-20 could have been 2-3 if validation had run before the initial burst commits.

---

## Recommendations for Next Iteration

1. **Auto-generate READMEs** — Add a script that re-counts and rewrites all category `README.md` files from SKILL.md files on disk. Run it in CI and as a pre-commit hook. Eliminates ~13 fix commits/cycle. → **Expected impact**: 40% reduction in fix:feat ratio.

2. **Validate before large batches** — Run `validate-skills.sh` locally before committing any batch >5 skills. Add to CONTRIBUTING.md. → **Expected impact**: Eliminate the fix cluster that follows every burst phase.

3. **Enforce unique skill names in CI** — Add a check to validate-skills.sh: skill `name:` field must be unique across entire registry. Prevents duplicate location bugs. → **Expected impact**: Eliminates recurring dedup commits.

4. **Parallelize industry expansion batches** — When adding multiple independent industry clusters, dispatch as parallel subagents (one per cluster). Use `superpowers:dispatching-parallel-agents`. → **Expected impact**: 3-4× wall-clock speedup on expansion sprints.

5. **Commit uncommitted `competitive-gap-analysis.md`** — 423 lines of changes are not in git. This is significant research debt. Commit now.

6. **Investigate `build/video-upscale/`** — Listed as untracked in the previous recall and still appears in gitStatus. Either commit it or delete it.

---

## Suggested Pipeline for Next Build

```
For a new skill batch (>10 skills):
  1. Research phase (1 agent): domain analysis, competitive gaps
  2. Generation phase (N parallel agents): one agent per independent skill cluster
         ↓ all agents complete
  3. Validation gate: validate-skills.sh locally — fix before committing
  4. Commit per cluster (not one mega-commit)
  5. Auto-regen READMEs (script, not manual)
  6. CI green → push

For skill evolution (/evolve):
  /recall → identify highest-churn skills → /evolve targeted skills → validate → commit

For meta-skills (/skillify, /publish-skill):
  Sequential — these have dependencies on each other
```

---

_Next steps: Run `/evolve` targeting arch-review (22x churn), ship (16x churn), and db-migrate (13x churn) — these are the highest-iteration skills and most likely to benefit from a quality pass._
