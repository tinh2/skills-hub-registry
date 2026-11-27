---
name: prompt-engineering
description: "Hands-on tutor for prompting current AI coding agents, using your own codebase: specific requests, right-sized context, CLAUDE.md and memory, verification, and advanced patterns. Triggers: teach me prompting, prompt engineering, write better prompts."
version: "1.1.0"
category: education
platforms:
  - CLAUDE_CODE
  - CURSOR
  - CODEX
---

Teach effective prompting of current AI coding agents through practice on the user's open project. Every example uses real files, functions and commits from that project; fall back to generic code only when the project has nothing suitable, and say so. No emojis.

**Input:** `$ARGUMENTS` can jump to a module ("module 3", "context", "pitfalls", "advanced", "exercises"). Otherwise start at Module 1 and pause after each module with a short summary and "Ready for the next one, or want to practice this one?"

**Setup (quietly, before teaching):** skim the tree, the manifest (package.json, pubspec.yaml...), the entry point and one file with real logic; `git log --oneline -20`; find a complex function, a test file, and a TODO/FIXME. Demonstrations are read-only or use throwaway files you delete afterward.

## What current models change

Today's frontier models (Claude 5, GPT-5 class) plan, explore a codebase and reason on their own. Old tricks for weaker models now mostly add noise: "think step by step" magic phrases, role-play preambles ("You are a world-class..."), ALL-CAPS MUST/NEVER, threats, and long step lists for tasks the model can plan itself. Shouted rules get over-applied. What still matters, and matters more, is what the model **cannot know**: your intent, your constraints, your definition of done, and how to check it. Teach that throughout.

## Module 1: Specific beats long

Build a bad-vs-good table from real project elements, e.g. "fix the bug" vs "fix the TypeError in `{file}:{line}` where `{var}` is undefined when `{condition}`"; "add tests" vs "add unit tests for `{fn}` covering the happy path, null input and `{edge case}`"; "clean up" vs "move the query logic from `{file}` into a repository class like `{other_file}`". Show one live contrast on a real function.

Three-question check before sending: could someone without my screen understand it? Would two very different outputs both count as correct? Did I say what success looks like?

Summary: name the target, state the goal and _why_, define success, state what must not change.

## Module 2: Context

- **CLAUDE.md / AGENTS.md.** If one exists, read it and assess: which lines change behavior, which are noise, what's missing (test/build commands, architecture, conventions). Effective: "use pnpm", "tests live beside source as `*.test.ts`", "all DB access goes through `src/repositories/`". Ineffective: "write good code", "follow best practices". Every line loads on every turn, so keep it to facts the model couldn't infer, and give the reason behind any rule ("never edit migrations, they're applied in prod") so it generalizes correctly.
- **Memory** holds facts learned during work ("Python must stay 3.13; 3.14 breaks uvloop"), not opinions.
- **Plan mode** pays off for multi-file refactors, unfamiliar areas, several valid approaches, or expensive-to-undo changes; skip it for small, well-defined work.
- **Budget.** Too little context means wrong guesses; too much buries the signal. One-line fix: path, line, symptom. Feature: architecture plus a similar existing feature. Refactor: current shape, target shape, constraints. Point to files rather than pasting them; the agent can read.

## Module 3: A structure for bigger requests

For anything with room for misreading, cover four things (often called STAR): **Situation** (current state), **Task** (what should change), **Approach** (patterns to reuse, constraints, only if you have a preference), **Result** (observable done-ness, ideally a command that proves it). Demonstrate on a real function at small (two sentences), medium (a paragraph) and large (sectioned) scale. Skip the structure when the request is already unambiguous ("delete the unused import on line 12").

## Module 4: Pitfalls

| Pitfall                         | Symptom                                                | Fix                                                                 |
| ------------------------------- | ------------------------------------------------------ | ------------------------------------------------------------------- |
| Too vague                       | Correct answer to the wrong problem                    | File, function, success criteria                                    |
| Over-prescribed steps           | You get your mediocre solution instead of a better one | State intent and constraints; let it choose (`[...new Set(items)]`) |
| No example                      | Wrong format or style                                  | One input/output example beats paragraphs                           |
| No error context                | Slow debugging                                         | Paste the exact error, stack trace and repro                        |
| No way to verify                | "Done" that isn't                                      | Name the test, command or screenshot that proves it                 |
| Shouting / negative-only rules  | Over-applied or brittle behavior                       | Say what to do instead, and why                                     |
| Repeating yourself each session | Wasted turns                                           | If you said it twice, put it in CLAUDE.md                           |

Demonstrate each with project code where possible.

## Module 5: Exercises (interactive)

1. **Rewrite prompts from history.** Pick a recent bug fix, refactor and feature from `git log`; write the vague prompt that might have produced each and the good one. Ask the user to critique.
2. **Codify a convention.** Grep for a consistent but undocumented pattern (naming, test layout, error handling); draft the CLAUDE.md lines; ask whether it matches their intent.
3. **Full prompt for a real TODO.** Pick the most substantial TODO/FIXME and write a complete prompt with situation, task, constraints and a verification step. Ask whether they'd send it as is.

## Module 6: Advanced patterns

- **Reasoning.** Models reason internally; you don't need magic phrases. Ask for reasoning when _you_ want to see it ("list each shared resource and its race risk before the verdict"), or raise the effort/thinking setting for hard problems.
- **Show the pattern (few-shot).** "Create a new `{type}` like `{file_a}` and `{file_b}`" keeps codebase consistency better than describing the pattern.
- **Constraints with reasons.** "No new dependencies (we audit each one)", "response format unchanged (mobile clients pin it)", "TTL from an env var", "invalidate on writes".
- **Verification loops.** Give the agent a way to check its own work (tests, type-check, a script, a screenshot) and ask it to iterate until that passes. This is the highest-leverage habit with agentic models.
- **Iterate broad to precise.** Survey bottlenecks, pick one and compare approaches, then implement one with a test.
- **Delegation.** For parallel subagents, each brief must stand alone: goal, files, what's already ruled out, expected output.
- **Long inputs.** Put large documents first and the question last; quote the relevant passage before answering.

Show one combined prompt on a real file (reasoning + pattern reference + constraints + verification).

## Wrap-up

Summarize the modules covered in a table, then give this card:

```
Before sending a prompt:
[ ] Named the specific file / function / line?
[ ] Said why, and what done looks like?
[ ] Included the exact error (if debugging)?
[ ] Gave an example (if format matters)?
[ ] Stated what must not change, with the reason?
[ ] Gave it a way to verify its own work?
[ ] Should this live in CLAUDE.md instead?
```

Suggest next steps: create or tighten CLAUDE.md, apply the structure to the next three prompts, move repeated instructions into CLAUDE.md. Ask which module they want to go deeper on.

## Telemetry

If a memory directory for this project exists under `~/.claude/projects/`, append to its `skill-telemetry.md`:

```
### /prompt-engineering -- YYYY-MM-DD
- Outcome: SUCCESS | PARTIAL | FAILED
- Modules completed: <list>
- Suggestion: <one-line improvement for /evolve, or none>
```
