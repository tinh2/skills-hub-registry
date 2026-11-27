---
name: skill-writer
description: "Coach and generator for writing your own agent skill: turn an idea into a well-triggered, concise SKILL.md, test it locally, and publish it to skills-hub.ai. Triggers: write a skill, create a SKILL.md, build my own skill, publish a skill."
version: "1.1.0"
category: education
platforms:
  - CLAUDE_CODE
  - CURSOR
  - CODEX
---

Help the user turn a skill idea into a SKILL.md that works well with current models, then test and publish it. If they gave a description (argument or message), use it; if not, ask once, "What should your skill do, in 1-2 sentences?", then proceed without more questions. No emojis.

## 1. Shape the idea

From the description, decide:

- **name**: short kebab-case, matching the directory (`api-load-tester` beats `tester`).
- **category**: analysis, build, combo, deploy, docs, education, integration, meta, productivity, qa, review, security, spec, test or ux.
- **platforms**: CLAUDE_CODE, CURSOR, CODEX by default; add WINDSURF or GITHUB_COPILOT if relevant.
- **What the model can't know without the skill.** This is the skill's real value: project conventions, a proven procedure, exact commands, an output contract, domain pitfalls, lessons from past incidents. If the answer is "nothing, it's general good practice", say so: the skill probably isn't worth writing.

## 2. Explain the format

```
---
name: my-skill
description: "What it does and when to use it. Triggers: phrase one, phrase two."
version: "1.0.0"
category: analysis
platforms: [CLAUDE_CODE, CURSOR, CODEX]
---
<instructions in markdown>
```

- The **description** is the only part loaded until the skill is invoked; agents use it to decide _when_ to use the skill. Say what it does and when, with the trigger phrases users actually type. Keep it to one or two sentences (under ~300 characters).
- **version** is semver; bump it on any behavior change so installers know to re-pull.
- The **body** loads only when invoked. Supporting files (`references/*.md`, `scripts/`) sit beside SKILL.md and are read only when the body points to them, so long reference material belongs there, not inline.

## 3. Generate the skill

Write the complete SKILL.md in one fenced block, ready to copy. Principles for the body, which target current frontier models:

- **Open with the goal**, in plain second person ("Audit the API routes for missing auth and report..."). Role-play preambles ("You are a world-class...") add nothing.
- **Give constraints with reasons.** "Read-only: report, don't fix, because this runs in CI" generalizes better than "Do NOT modify files". Avoid ALL-CAPS MUST/NEVER and threats; current models over-apply shouted rules.
- **Include what's specific, skip what's default.** Exact commands, paths, thresholds, ordering that matters, known failure modes: yes. "Write clean code", "handle errors", "be thorough": no, the model already does that.
- **Prefer goals over scripts.** Spell out steps only where order or exact commands matter; otherwise state the outcome and let the model plan.
- **Inputs and defaults.** What `$ARGUMENTS` means and what happens without it.
- **Define done and how to verify it**: a command that must pass, a check to run, what to re-read before reporting.
- **Output contract.** An exact template when another tool or person parses the result; a loose shape otherwise.
- **Boundaries.** What not to touch, when to stop and ask (only for genuinely user-owned decisions), what to clean up.
- **Optional telemetry** for the /evolve pipeline: if `~/.claude/projects/<project>/` memory exists, append a short `skill-telemetry.md` entry (date, outcome, bottleneck, suggestion).

## 4. Review it

Check and report as a PASS/FAIL table, then fix any FAIL and show the corrected file:

| Check                | What passes                                                          |
| -------------------- | -------------------------------------------------------------------- |
| name                 | kebab-case, matches directory                                        |
| description          | says what and when, includes trigger phrases, ~300 chars max         |
| version              | semver string                                                        |
| category / platforms | valid, non-empty                                                     |
| goal stated up front | first lines say what the skill achieves                              |
| specific value       | contains knowledge or procedure the model wouldn't have              |
| no filler            | no restated defaults, role-play, shouting                            |
| inputs               | argument and no-argument behavior defined                            |
| verification         | defines done and how to check it                                     |
| output               | format defined at the right strictness                               |
| size                 | body is as short as it can be; long reference moved to `references/` |

## 5. Test locally

```
mkdir -p ~/.claude/skills/<skill-name>
cp SKILL.md ~/.claude/skills/<skill-name>/
# new Claude Code session:
/<skill-name> [arguments]
```

Then: does it trigger from natural phrasing (not just the slash command)? Does the output match the contract? Try edge cases: empty directory, no git, missing tools, a large repo. Better still, run it on 2-3 realistic tasks with and without the skill and compare; keep only instructions that change the result.

Validate with the CLI: `npx @skills-hub-ai/cli test ./SKILL.md`.

## 6. Publish

Requires a skills-hub.ai account and passing checks.

```
npx @skills-hub-ai/cli publish ./SKILL.md
npx @skills-hub-ai/cli search "<skill name>"     # confirm it's listed
```

To update: bump `version`, publish again. For discoverability, put the words users search for in the description and pick the most specific category.

## Output

The steps above in order, with the generated SKILL.md in a fenced block, then:

```
Next steps:
- Copy SKILL.md to ~/.claude/skills/<name>/ and test it.
- Publish with: npx @skills-hub-ai/cli publish ./SKILL.md
```
