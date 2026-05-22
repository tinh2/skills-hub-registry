# Skill Finder

A workflow orchestrator for skills-hub. Hand it a task. It decomposes the task into ordered steps, finds or installs the right skill for each step, runs the chain, and offers to save the chain as a reusable skill for next time.

## When to Invoke

Use Skill Finder when you have a goal that takes more than one skill to accomplish. Examples:

* Shipping a branch end to end (preflight, pr, security review, verify).
* Building a feature from scratch (spec, build, review, pr).
* Fixing a bug with regression coverage (debug, fix, test, pr).
* Auditing a codebase and acting on the findings (audit, fix, polish).

If your task fits inside a single skill, invoke that skill directly. Skill Finder is for chains.

## Invocation

```
/skill-finder                          # auto detect the task from project state
/skill-finder ship the auth flow       # use the args as the task
/skill-finder resume                   # pick up the most recent unfinished plan
```

## What Happens

Skill Finder runs six phases:

1. **Understand.** Figures out what task you want done.
2. **Discover.** Picks the right skills, local or from the catalog.
3. **Plan.** Writes a workflow plan and shows it to you for approval.
4. **Execute.** Runs the chain step by step. Retries failures once. Pauses if a step fails twice.
5. **Save as skill.** Optionally turns the chain into a reusable skill.
6. **Next steps.** Surfaces follow ups as concrete slash commands.

Read the full design in `docs/2026-05-22-skill-finder-v2-design.md`.

## Directory Map

```
skill-finder/
├── SKILL.md                                       # the orchestrator. Start here for runtime behavior.
├── README.md                                      # this file. Entry point for browsing.
├── docs/                                          # design docs, dated, append only
│   ├── 2026-05-22-skill-finder-v2-design.md       # v2 spec overview, links to section files
│   └── 2026-05-22-design/                         # spec sections
│       ├── user-experience.md                     # section 3
│       ├── architecture.md                        # section 4
│       ├── phases.md                              # section 5
│       └── edge-cases.md                          # section 6
└── references/                                    # verbose playbooks pulled in by phase
    ├── INDEX.md                                   # menu of references
    ├── workflow-patterns.md                       # pattern index + matching rules (Phase 2)
    ├── patterns/                                  # one file per workflow pattern
    │   ├── ship-branch.md
    │   ├── fix-bug.md
    │   ├── build-feature.md
    │   ├── design-overhaul.md
    │   ├── security-harden.md
    │   ├── write-and-publish.md
    │   ├── audit-and-ship.md
    │   ├── research-and-build.md
    │   └── bootstrap-project.md
    ├── execution-playbook.md                      # run loop, retries, pause prompts (Phase 4)
    ├── handoff-protocol.md                        # data passed step to step (Phase 4)
    ├── next-steps-detectors.md                    # scans for follow ups (Phase 6)
    └── save-as-skill-template.md                  # SKILL.md template for saved chains (Phase 5)
```

Plan files do not live here. They live in the user's project at `./skill-finder-plans/` so the skill stays stateless and shareable across projects.

**File size rule.** Every markdown file in this skill is 200 lines or less. Longer content gets split into a parent index file plus children. The parent links to the children with relative paths.

## File Roles

| File | What it is | When to read |
|------|------------|--------------|
| `SKILL.md` | The lean orchestrator. Six phases, each pointing to a reference for the verbose logic. | When you want to understand what the skill does at runtime. |
| `README.md` | This file. The entry point. | When you are new to the skill. |
| `docs/<date>-design.md` | Historical design docs. Dated. Never deleted. | When you want the reasoning behind a design choice. |
| `references/INDEX.md` | One screen menu of all reference files. | When you need to find the right verbose doc fast. |
| `references/workflow-patterns.md` | Slim pattern index. Matching rules and a table linking to `patterns/<name>.md`. | When you want to understand how task matching works. |
| `references/patterns/<name>.md` | One file per pattern. Trigger phrases, required steps, optional steps, handoff notes. | When you want to add a new workflow or edit an existing one. |
| `references/execution-playbook.md` | Per step run loop, success and failure rules, retry policy, pause prompt template, resume protocol. | When you want to tweak failure handling or how steps get classified. |
| `references/handoff-protocol.md` | The structured context passed from step N to step N+1. | When you want to understand or change what skills receive when they are chained. |
| `references/next-steps-detectors.md` | Phase 6 probes. Each detector returns zero or one suggested slash command. | When you want to add a new follow up detector. |
| `references/save-as-skill-template.md` | SKILL.md template for chains that get saved as new skills. | When you want to change what saved skills look like. |

## How to Extend

* New workflow pattern: edit `references/workflow-patterns.md` only.
* New failure rule or retry tweak: edit `references/execution-playbook.md` only.
* New follow up detector: edit `references/next-steps-detectors.md` only.
* Change saved skill output: edit `references/save-as-skill-template.md` only.

The orchestrator never inlines logic from these files. Edits to the references are picked up automatically.

## Version

Current: **2.0.0**. See `SKILL.md` frontmatter.

## Changelog

### 2.0.0 (2026 05 22)

Major rewrite. Skill Finder is now a workflow orchestrator, not a search and install assistant.

**Added**
* Six phase orchestration: Understand, Discover, Plan, Execute, Save, Next Steps.
* Pattern library with 9 canonical workflows (ship-branch, fix-bug, build-feature, design-overhaul, security-harden, write-and-publish, audit-and-ship, research-and-build, bootstrap-project). Each lives in `references/patterns/<name>.md`.
* Automatic retry on failure plus pause and prompt UX when retry also fails.
* Resume support via `/skill-finder resume` for aborted or manual paused chains.
* Plan files written to `./skill-finder-plans/` per project. Append only, dated, slugged.
* Handoff protocol between steps with four structured fields: output artifacts, git delta, summary, open items.
* Phase 6 next steps detection with 12 detectors and severity ordering.
* Save as skill flow that hands the chain to `skills-hub-registry-skillify` for publish.
* Modular reference library under `references/` plus a section index for the design spec under `docs/`.

**Changed**
* `search_skills`, `get_skill_detail`, `install_skill`, `list_installed_skills` are still used, but now in service of building a chain instead of just recommending.

**Removed**
* The standalone "recommend the top 3 to 5 skills" flow from v1. Skill Finder always builds a chain now. If the user just wants a recommendation, they can decline at the plan approval step.

**Conventions enforced**
* Every markdown file in the skill is 200 lines or less.
* No em dashes or en dashes in user facing copy.
* Skill creation always goes through skillify. Skill Finder never writes a SKILL.md to the skills directory itself.

### 1.0.0

Initial release. Search the skills hub catalog, recommend the top 3 to 5 matches, install on confirmation. No workflow chaining.

## Related Skills

* `skills-hub-registry-skillify`: handles the publish step when Skill Finder saves a chain.
* `superpowers:writing-plans`: alternative when you want a richer implementation plan instead of a chain.
* `superpowers:executing-plans`: alternative when you already have a plan and just want it run.

Skill Finder sits between these. Less ceremony than writing-plans plus executing-plans. More structure than running skills manually one at a time.
