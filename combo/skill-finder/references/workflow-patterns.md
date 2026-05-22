# Workflow Patterns

Canonical task to step recipes. The orchestrator reads this file in Phase 2 to match the user's task to a known pattern, then loads the specific pattern file from `patterns/`.

## How Matching Works

A pattern matches if the user's task statement has 60 percent or more keyword overlap with one of its trigger phrases. The match is fuzzy. Stop words (the, a, an, to, of, for, with) are ignored.

If multiple patterns match, the one with the highest overlap wins. Ties break by specificity (more required steps wins).

If no pattern matches, the orchestrator falls back to ad hoc decomposition. See `execution-playbook.md` section "Ad Hoc Decomposition".

## Pattern File Format

Each pattern lives in its own file under `patterns/`. Every pattern file has these sections:

* **Trigger Phrases.** Bulleted list. The matcher uses these for keyword overlap.
* **Required Steps.** Numbered list. Each step has a label, a recommended skill slug, and a one line purpose.
* **Optional Steps.** Same shape as required. Included only if the project state suggests they apply.
* **Handoff Notes.** What context each step needs from the previous step.

The orchestrator parses each pattern file by section heading. Stick to the format.

## Available Patterns

| Pattern | File | One line summary |
|---------|------|------------------|
| ship-branch | [patterns/ship-branch.md](patterns/ship-branch.md) | Verify, open PR, optional security review and dev verify. |
| fix-bug | [patterns/fix-bug.md](patterns/fix-bug.md) | Root cause, fix with regression test, open PR. |
| build-feature | [patterns/build-feature.md](patterns/build-feature.md) | Spec, build, review, PR. |
| design-overhaul | [patterns/design-overhaul.md](patterns/design-overhaul.md) | Setup tokens, build, polish. Optional audit and animate. |
| security-harden | [patterns/security-harden.md](patterns/security-harden.md) | OWASP scan and fix high severity findings. |
| write-and-publish | [patterns/write-and-publish.md](patterns/write-and-publish.md) | Draft a post and publish to WordPress. |
| audit-and-ship | [patterns/audit-and-ship.md](patterns/audit-and-ship.md) | Full audit then fix and ship. |
| research-and-build | [patterns/research-and-build.md](patterns/research-and-build.md) | Competitive analysis, spec the top idea, build. |
| bootstrap-project | [patterns/bootstrap-project.md](patterns/bootstrap-project.md) | Quickstart tooling and scaffold a project. |

## How To Match A Task To A Pattern

The orchestrator does this in Phase 2:

1. Tokenize the task statement. Drop stop words. Lowercase.
2. For each pattern, read its `patterns/<name>.md` and tokenize the trigger phrases the same way.
3. Compute overlap as the fraction of task tokens that appear in any trigger phrase.
4. The pattern with the highest overlap above 60 percent wins.
5. Load that pattern file and use its Required Steps. Add Optional Steps based on project state signals.

## Adding A New Pattern

1. Create `patterns/<kebab-name>.md` using the format from any existing pattern file as a template.
2. Add a row to the "Available Patterns" table above with the file link and a one line summary.
3. Done. The orchestrator picks it up automatically on next run.

Keep each pattern file under 200 lines. If a pattern needs more than that, split it into a primary pattern plus sub patterns and link between them.
