# Design: Edge Cases and Decisions

Part of [Skill Finder v2 Design Spec](../2026-05-22-skill-finder-v2-design.md). Section 6.

## No Git Repo

Phase 1 auto detection falls back to reading CLAUDE.md and TODO files only. Phase 6 skips git detectors. The chain still runs.

## Task Too Vague For Any Pattern Match

Phase 2 ad hoc decomposition kicks in. If the orchestrator cannot produce at least 2 steps, it asks the user to clarify the task and re runs Phase 2.

## User Wants to Add a Manual Step in the Middle

Not supported in v2. The user can abort, edit the plan file by hand, then run `/skill-finder resume`. v3 may add inline plan edits.

## Two Plans Exist For the Same Task Slug

New plan file is written with a unique HHmm suffix. The older one is preserved.

## Plan File From a Different Project Is In the Directory

The orchestrator only resumes plans matching the current git remote or working directory. Other plans are ignored.

## Skill Returns Ambiguous Output

The execution playbook defines a fallback: ask the user. Do not silently mark as success. See `references/execution-playbook.md` section "Success and Failure Classification".

## Save As Skill Collides With an Existing Skill Name

Skill Finder defers to skillify's name collision logic. It does not try to handle this itself.

## Skillify Unavailable

Phase 5 halts. The plan file stays as `complete`. The user is told that the chain succeeded but saving as a skill requires skillify, which was not reachable. The user can retry Phase 5 later by running `/skill-finder resume` on the same plan file.
