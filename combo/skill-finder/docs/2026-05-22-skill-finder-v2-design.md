# Skill Finder v2 Design Spec

**Date:** 2026 05 22
**Status:** Implemented
**Replaces:** Skill Finder v1.0.0 (recommend and install only)

---

## Section Index

This spec is split across multiple files. Each section file is under 200 lines.

| Section | File | Topic |
|---------|------|-------|
| 3. User Experience | [2026-05-22-design/user-experience.md](2026-05-22-design/user-experience.md) | Invocation forms, happy path session, failure path |
| 4. Architecture | [2026-05-22-design/architecture.md](2026-05-22-design/architecture.md) | Directory structure, file responsibilities, runtime plan file |
| 5. The Six Phases | [2026-05-22-design/phases.md](2026-05-22-design/phases.md) | Inputs, outputs, and steps for every phase |
| 6. Edge Cases | [2026-05-22-design/edge-cases.md](2026-05-22-design/edge-cases.md) | Behavior when assumptions break |

Sections 1, 2, 7, 8, and 9 are in this file below.

---

## 1. Goal

Upgrade Skill Finder from a "search and install" assistant into a full workflow orchestrator. When the user invokes `/skill-finder`, it should not stop at recommendations. It should decompose the task into ordered steps, find or install the right skill for each step, run the chain, offer to save the chain as a reusable composition skill, and surface concrete next steps.

The skill should feel like a single command that takes a high level intent and produces a finished outcome, with the option to capture that workflow for next time.

---

## 2. Non Goals

* Skill Finder will not create or publish skills on its own. It hands the creation step to the existing `skills-hub-registry-skillify` skill.
* Skill Finder will not version, sign, or scope skills. It only produces the SKILL.md and the description. Skillify handles the rest.
* Skill Finder will not replace specialized chained skills like `design-pipeline`, `research`, or `stitch-pipeline`. Those remain first class and Skill Finder will prefer them when a task matches their patterns.
* Skill Finder will not run skills in parallel in v2. All chains are sequential. Parallel execution is a v3 candidate.

---

## 7. Open Questions

None at design time. All four clarifying answers from brainstorming are captured:

1. Workflow mode: show plan, execute chain, ask to save, give next steps.
2. Skill source: hybrid (local first, propose catalog gaps).
3. Task input: args or auto detect from project.
4. Failure mode: pause and ask, but auto retry once first.

---

## 8. Acceptance Criteria

The redesigned skill is considered shipped when:

1. `/skill-finder ship the auth flow` runs end to end in a real project and produces the happy path output in [user-experience.md section 3.2](2026-05-22-design/user-experience.md).
2. A forced failure in step N triggers the retry, then the pause prompt.
3. Saving the chain produces a valid SKILL.md and skillify publishes it.
4. `/skill-finder resume` picks up an aborted chain at the correct step.
5. The directory layout in [architecture.md section 4.1](2026-05-22-design/architecture.md) exists as documented and the README.md is a useful entry point for a new maintainer.
6. Every markdown file in the skill is 200 lines or less. Longer content is split into a parent index plus children.

---

## 9. Implementation Plan

Skipped formal `superpowers:writing-plans` step. The spec was implemented directly. See git history for the build sequence.
