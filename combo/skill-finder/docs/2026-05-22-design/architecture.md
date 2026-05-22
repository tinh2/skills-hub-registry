# Design: Architecture

Part of [Skill Finder v2 Design Spec](../2026-05-22-skill-finder-v2-design.md). Section 4.

## 4.1 Directory Structure

The skill lives at `~/.claude/skills/skill-finder/` and uses this layout:

```
skill-finder/
├── SKILL.md
├── README.md
├── docs/
│   ├── 2026-05-22-skill-finder-v2-design.md         (overview)
│   └── 2026-05-22-design/
│       ├── user-experience.md                        (section 3)
│       ├── architecture.md                           (this file)
│       ├── phases.md                                 (section 5)
│       └── edge-cases.md                             (section 6)
└── references/
    ├── INDEX.md
    ├── workflow-patterns.md
    ├── patterns/                                     (one file per pattern)
    ├── execution-playbook.md
    ├── handoff-protocol.md
    ├── next-steps-detectors.md
    └── save-as-skill-template.md
```

**Why this layout**

* `SKILL.md` stays lean. It is the orchestrator. It reads top to bottom in about 170 lines and references the docs in `references/` for the verbose details.
* `README.md` is a one screen overview for anyone browsing the directory. It explains what each file is for and where to start reading.
* `docs/` holds historical design docs and ADRs. Future designs land here with a date stamped filename. Subdirectories like `docs/2026-05-22-design/` hold the sections of a multi part spec.
* `references/` holds the verbose playbooks the orchestrator pulls in when needed. Each file has one job. The `INDEX.md` is a one screen menu so future readers do not have to open every file to find what they want.
* Runtime plan files do not live inside the skill. They live in the user's project at `./skill-finder-plans/`. This keeps the skill stateless and shareable across projects.
* Every markdown file in the skill is 200 lines or less. Longer content gets split into a parent index plus children.

## 4.2 File Responsibilities

**SKILL.md (orchestrator)**

* Frontmatter: name, description, version, category, triggers.
* Six numbered phases: Understand, Discover, Plan, Execute, Save, Next Steps.
* Each phase is 5 to 20 lines. Verbose explanations live in `references/`.
* Cross references use the form `see references/workflow-patterns.md`.

**README.md**

* What Skill Finder does in two sentences.
* When to invoke it.
* The directory map with a one line "what is this" per file.
* Quickstart: the three invocation forms plus expected output.

**docs/<date>-<topic>-design.md**

* Design docs. Dated. Append only. Never delete.
* New design overrides previous design when versions bump.
* Multi part specs split into a parent overview plus a `<date>-<topic>/` subdirectory of section files.

**references/INDEX.md**

* One line per reference file: filename, purpose, when the orchestrator pulls it in.
* Lets a maintainer find the right doc in under 10 seconds.

**references/workflow-patterns.md**

* Slim index. Matching rules plus a table of patterns linking to `patterns/<name>.md`.
* The orchestrator reads this file in Phase 2 to match the user's task to a known pattern, then loads the specific pattern file.

**references/patterns/<name>.md**

* One file per pattern. Each file has Trigger Phrases, Required Steps, Optional Steps, Handoff Notes.
* Keep each pattern file under 200 lines.

**references/execution-playbook.md**

* Per step run loop: build context, invoke, classify outcome, retry, pause.
* The exact pause prompt template.
* What counts as success or failure for common skill types.
* Resume protocol when an old plan file is detected on disk.

**references/handoff-protocol.md**

* The structured data passed from step N to step N+1.
* Four fields: output artifacts, git delta, summary, open items.
* JSON shape plus example.

**references/next-steps-detectors.md**

* The Phase 6 scan list: git, gh, test output, CLAUDE.md conventions.
* For each detector: what to look for, what slash command to suggest, severity ordering.

**references/save-as-skill-template.md**

* The SKILL.md template the orchestrator fills in when the user opts to save the chain.
* Includes frontmatter, the composition declaration, the trigger phrases, and the body that replays the chain.
* The orchestrator never invents this from scratch. It always uses the template.
* The orchestrator never creates the skill itself. It always hands the filled template to skillify.

## 4.3 Runtime Plan File

```
./skill-finder-plans/2026-05-22-1342-ship-the-auth-flow.md
```

**Why dated and slugged**

The filename answers three questions at a glance: when was this run, what was the task, was it from today or older. Easy to grep, easy to clean up.

**Plan file structure**

```markdown
# Task: Ship the auth-flow branch end to end
- Started: 2026 05 22 13:42
- Status: in progress
- Trigger: /skill-finder ship the auth flow branch

## Workflow

1. [✓] /preflight       READY. Build green. Tests pass.
2. [✓] /pr              PR #482 opened
3. [⟳] /security-review attempt 1 failed, retrying...
4. [ ] /verify

## Handoffs

step 1 to step 2:
  output_artifacts: []
  git_delta: 3 files modified, 0 added
  summary: All gates passed.
  open_items: none

step 2 to step 3:
  output_artifacts: [PR #482]
  git_delta: 0 since last step (PR creation is read-only on tree)
  summary: PR opened with title from branch name.
  open_items: PR needs reviewers

## Decisions

- 2026 05 22 13:44 user approved plan
- 2026 05 22 13:46 step 3 retry triggered automatically
```
