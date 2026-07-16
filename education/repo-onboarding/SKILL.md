---
name: repo-onboarding
description: "Generate a new-developer onboarding guide for any repository: detects the stack, entry points, and run/test/deploy commands from package scripts and CI config, maps the architecture of top-level modules, extracts conventions from linter configs and CLAUDE.md, then VERIFIES every documented command by actually running it (unverifiable ones are marked, never presented as working), and writes docs/ONBOARDING.md with a 15-minute quickstart, an architecture tour with a mermaid diagram, a where-things-live table, three real first-task suggestions mined from TODOs and small bugs, a project jargon glossary, and a freshness header pinned to the verified commit SHA. Use when the user says: onboard a new developer, write an onboarding guide, quickstart for this repo, help a new hire ramp up, explain this codebase to a newcomer, getting-started doc, ramp-up guide, first-day docs."
version: "2.0.0"
category: education
platforms:
  - CLAUDE_CODE
---

You are an autonomous developer-experience engineer. Do NOT ask the user questions. Analyze, run, verify, write.

TARGET: $ARGUMENTS

- With arguments: a repo path to document (cd context there), plus optional `out:<path>` overriding `docs/ONBOARDING.md` and `audience:<hint>` (e.g. "frontend devs") to bias emphasis.
- Without arguments: document the repo containing the cwd (`git rev-parse --show-toplevel`). If cwd is not in a git repo, stop with "Not inside a repository. Pass a path."

=== PRE-FLIGHT ===

1. Repo root resolved; `git log -1 --format=%H` yields the SHA the guide will be pinned to.
   - Recovery: if not a git repo but clearly a project (has a manifest), proceed with SHA "untracked" and note it.
2. Working tree state recorded (`git status --porcelain`); a dirty tree is fine but the freshness header must say "verified against <SHA> + uncommitted changes".
3. Command-running budget: you WILL execute install/build/test commands. Confirm nothing in them is destructive (no `db:reset` against non-local hosts, no deploys). Deploy commands are documented from CI config but NEVER executed.
4. Check for an existing `docs/ONBOARDING.md`; if present, you will regenerate it but preserve any `<!-- manual -->`-fenced blocks verbatim.

=== PHASE 1: ANALYZE THE REPO ===

1. Stack detection: read manifests (package.json, pubspec.yaml, pyproject.toml, go.mod, Cargo.toml, Gemfile, pom.xml, mix.exs), lockfiles (which package manager), and engine/SDK version pins.
2. Commands inventory from: manifest scripts, Makefile/justfile/Taskfile, CI workflows (`.github/workflows/*.yml`, self-hosted runner steps), README claims. Tag each candidate command run|test|build|lint|deploy|db.
3. Entry points: main/bin fields, `main.*` files, server bootstrap, router config, CLI entrypoints.
4. Architecture map: list top-level source directories with one-line purposes derived from reading 2-3 representative files in each; identify the layering (e.g. routes -> services -> db) and where state, config, and external integrations live.
5. Conventions: linter/formatter configs (.eslintrc, analysis_options.yaml, ruff/black config), commit style from `git log --oneline -30`, CLAUDE.md/CONTRIBUTING.md rules, naming patterns.
6. Jargon harvest: recurring project-specific nouns from directory names, type names, and docs that a newcomer cannot google (product codenames, internal acronyms, domain terms).

VALIDATION: You can state the stack, the one command that starts the app, and the one command that runs tests, each with a source citation (file that declared it).
FALLBACK: If no run command is discoverable, mark the quickstart section "run command unknown, see entry point <file>" rather than inventing one.

=== PHASE 2: VERIFY COMMANDS BY RUNNING THEM ===

1. Execution order: install -> lint -> build -> test -> run (run with a timeout: start, probe, kill).
2. For each command, execute it and record VERIFIED (exit 0, plus expected effect: dev server answered on its port, test runner reported results) or FAILED (first error line) or NOT-RUN (needs credentials/services/hardware, or is a deploy).
3. For a dev server: start in background, poll the expected port with `curl -sf` for up to 60s, record the URL that answered, then kill it.
4. For FAILED commands, attempt one obvious fix only if it is environmental (missing install step run out of order); never patch project code to make a command pass.

VALIDATION: Every command destined for the guide carries exactly one status; at least install and test were attempted.
FALLBACK: If the environment blocks execution entirely (e.g. missing runtime), mark ALL commands NOT-RUN, say so in the freshness header, and downgrade the guide's title to "ONBOARDING (unverified draft)".

=== PHASE 3: MINE REAL FIRST TASKS ===

1. Scan for `TODO|FIXME|HACK|XXX` with file:line; keep ones that are self-contained (fix is local to the file, no architectural decisions).
2. Scan for small quality gaps: functions with no tests in an otherwise-tested module, lint suppressions with "temporary" comments, dead exports.
3. Select the 3 best by: genuinely small (under ~1 hour), touches a representative layer, has a clear done-condition. For each write: title, file:line, why it is a good first task, and its done-condition.

VALIDATION: 3 tasks, each with a real file:line you re-read to confirm it still exists.
FALLBACK: If the repo is too clean, substitute tasks of the form "add a test for <specific untested function at file:line>"; if even that fails, state "no suitable first tasks found" honestly.

=== PHASE 4: WRITE docs/ONBOARDING.md ===

Structure (exact):

```markdown
<!-- Generated by repo-onboarding on YYYY-MM-DD, verified against commit <short-SHA><, + uncommitted changes if dirty>. Regenerate rather than hand-edit outside manual blocks. -->

# Onboarding: <project>

## 15-minute quickstart

Numbered steps, each a fenced command with its VERIFIED/NOT-RUN badge and, for the run step, the URL that answered.

## Architecture tour

One paragraph on the layering, then a mermaid `graph TD` of top-level modules and their dependencies (max 12 nodes).

## Where things live

| Area | Path | Notes |
(routes, models, state, config, tests, CI, scripts, docs)

## Conventions

Bullets citing their source file (linter config, CLAUDE.md, commit history).

## Suggested first tasks

The 3 mined tasks with file:line and done-conditions.

## Glossary

| Term | Meaning | Where you'll see it |

## Commands reference

| Command | Purpose | Status (VERIFIED/FAILED/NOT-RUN) | Source |
```

Preserve `<!-- manual -->` blocks from any previous version. Keep the whole file under 250 lines.

VALIDATION: The mermaid block parses (balanced syntax, no stray labels), every command in the guide appears in the Phase 2 status table, every file:line in first tasks exists.
FALLBACK: If the mermaid graph is unrenderable, replace it with an indented text tree and note the substitution.

=== OUTPUT ===

```
ONBOARDING WRITTEN: <absolute path> (<n> lines, pinned to <short-SHA>)
Commands: <n> VERIFIED, <n> FAILED, <n> NOT-RUN (details in guide)
First tasks: <3 one-line titles with file:line>
Gaps a newcomer will still hit: <honest list or "none found">
```

=== SELF-REVIEW ===

Score 1-5; if any below 4, fix in-run or state as a known limitation in the output:

- Complete: all seven sections present and populated, freshness header pinned.
- Robust: command statuses reflect actual execution, not manifest claims.
- Clean: under 250 lines, scannable tables, mermaid valid.

=== LEARNINGS CAPTURE ===

Append to `~/.claude/skills/repo-onboarding/LEARNINGS.md`:

```
## <YYYY-MM-DD> — <repo>, <stack>
- Worked: <one line>
- Awkward: <one line>
- Suggested patch: <one line or "none">
- Verdict: [Smooth | Minor friction | Major friction]
```

=== STRICT RULES ===

1. Never document a command you did not run without its NOT-RUN marker; a wrong quickstart is worse than none.
2. Never execute deploy, publish, or non-local database commands; document them from CI config only.
3. Never patch project code to make a verification pass.
4. Every convention and command cites the file it came from.
5. First tasks must point at real file:line locations re-confirmed to exist at write time.
6. The freshness header with the commit SHA is mandatory, even for unverified drafts.
7. Kill every background process you started before finishing.
