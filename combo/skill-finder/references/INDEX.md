# References Index

This directory holds the verbose playbooks that the Skill Finder orchestrator pulls in on demand. The orchestrator (`SKILL.md`) stays lean and points here for the details.

Every file is 200 lines or less. Longer content is split into a parent index plus children.

## File Guide

| File | Purpose | Loaded by orchestrator during |
|------|---------|-------------------------------|
| `workflow-patterns.md` | Slim index of canonical task to step recipes. Matching rules plus a table linking to `patterns/<name>.md`. | Phase 2 (Discover and decompose) |
| `patterns/<name>.md` | One file per workflow pattern. Trigger phrases, required steps, optional steps, handoff notes. | Phase 2 after a pattern match |
| `execution-playbook.md` | Per step run loop, success or failure classification rules, retry policy, pause prompt template, resume protocol. | Phase 4 (Execute) |
| `handoff-protocol.md` | Structured data passed from step N to step N+1. Four fields: output artifacts, git delta, summary, open items. JSON shape and example. | Phase 4 (Execute), between every step |
| `next-steps-detectors.md` | Scan list for Phase 6. Each detector returns zero or one suggested slash command. Severity ordering. | Phase 6 (Next steps) |
| `save-as-skill-template.md` | SKILL.md template the orchestrator fills in when the user opts to save the chain. The orchestrator hands the filled template to `skills-hub-registry-skillify`. | Phase 5 (Save as skill) |

## How to Read

Open this file first if you are new to the skill. Then read `SKILL.md` in the parent directory to see the orchestrator. Open individual reference files only when you need the verbose version of a specific phase.

## How to Extend

* Adding a new workflow pattern: create `patterns/<kebab-name>.md` using an existing pattern file as a template. Then add a row to the table in `workflow-patterns.md`.
* Tightening failure classification: edit `execution-playbook.md` only.
* Adding a new next steps detector: edit `next-steps-detectors.md` only.
* Changing what the saved skill looks like: edit `save-as-skill-template.md` only.

The orchestrator never inlines logic from these files. It references them by path.

## Available Patterns

See `workflow-patterns.md` for the full list with one line summaries. Pattern files live in `patterns/`:

* `patterns/ship-branch.md`
* `patterns/fix-bug.md`
* `patterns/build-feature.md`
* `patterns/design-overhaul.md`
* `patterns/security-harden.md`
* `patterns/write-and-publish.md`
* `patterns/audit-and-ship.md`
* `patterns/research-and-build.md`
* `patterns/bootstrap-project.md`
