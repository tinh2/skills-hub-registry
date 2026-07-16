---
name: session-handoff
description: Compress the current working session into a handoff document that a fresh session (or another person) can resume from without re-discovery. Inventories the session (task, decisions made and why, files touched with one-line diff summaries, commands that worked, dead ends to avoid, current blockers), writes it to .claude/handoff/<date>-<topic>.md with a paste-ready RESUME PROMPT section at the top, runs a stranger-test completeness check (no unexplained jargon, absolute file paths, next three actions explicit), and lists stale handoffs older than 30 days for pruning. Use when you say "hand off this session", "write a handoff", "save context before I close this", "I'm out of context, summarize for the next session", "pick this up tomorrow", "create a resume doc", or before compaction on a long task.
version: "2.0.0"
category: productivity
platforms:
  - CLAUDE_CODE
---

You are an autonomous session scribe. Do NOT ask the user questions. Reconstruct the
session from conversation context plus repository state, and produce a handoff a stranger
could resume from.

TARGET: $ARGUMENTS

If arguments name a topic, use it as the handoff topic slug and scope the inventory to
that thread of work. With no arguments, cover the whole session and derive the topic from
its dominant task.

=== PRE-FLIGHT ===

1. A project root exists (prefer `git rev-parse --show-toplevel`, else cwd). RECOVERY: if
   the session was not project-bound, write the handoff to
   `~/.claude/handoff/` instead and note that in the doc.
2. `.claude/handoff/` directory exists at the root. RECOVERY: create it.
3. Session has resumable substance (decisions, edits, or findings). RECOVERY: if the
   session was trivial (a one-off question), stop and say a handoff is not warranted
   rather than writing an empty document.
4. Repo state is inspectable: `git status --porcelain`, `git log --oneline -15`,
   `git diff --stat`. RECOVERY: without git, list files by recent mtime under the project
   and mark diff summaries BEST-EFFORT.

=== PHASE 1: INVENTORY THE SESSION ===

Reconstruct, from conversation context cross-checked against repo state:

1. TASK: the goal in one sentence, plus current percent-done judgment.
2. DECISIONS: each decision made, WHY it was made, and what was rejected (the why is the
   part a fresh session cannot recover; never omit it).
3. FILES TOUCHED: every created/modified file with a one-line summary of the change.
   Cross-check against `git status` and `git diff --stat`; include uncommitted vs
   committed state per file.
4. COMMANDS THAT WORKED: exact invocations for build, test, run, deploy, and any
   hard-won incantations (flags, env vars, ports).
5. DEAD ENDS: approaches tried and abandoned, each with the reason, so the next session
   does not repeat them.
6. BLOCKERS: what is currently stopping progress, with the exact error or missing input.
7. NEXT ACTIONS: the next 3 concrete actions, each starting with a verb and naming its
   file or command.

VALIDATION: every file in `git status` is either in the FILES TOUCHED list or explicitly
noted as pre-existing/unrelated; DECISIONS all carry a why.
FALLBACK: where conversation context has been compacted away, recover what you can from
git history and file contents, and mark those entries RECONSTRUCTED so the reader knows
confidence is lower.

=== PHASE 2: WRITE THE HANDOFF ===

Write `.claude/handoff/<YYYY-MM-DD>-<topic-slug>.md` with this exact structure:

```
# Handoff: <topic> (<date>)

## RESUME PROMPT
<A paste-ready first message for the next session, written in second person
imperative: working dir, one-paragraph state summary, the next 3 actions, the
verification command to run first, and "read the rest of this file at
<absolute path> before changing anything".>

## Task and status
## Decisions (with why)
## Files touched
| File (absolute path) | Change | Committed? |
## Commands that work
## Dead ends (do not retry)
## Blockers
## Next 3 actions
```

Rules: absolute paths everywhere; no em dashes; no jargon that is not defined inline; the
RESUME PROMPT must stand alone even if the reader never scrolls further.

VALIDATION: file exists, every template section is non-empty (write "none" explicitly
rather than omitting a section), RESUME PROMPT is under 250 words.
FALLBACK: if a filename collision exists for today+topic, append `-2` rather than
overwriting; never destroy a prior handoff.

=== PHASE 3: STRANGER TEST ===

Re-read the written handoff as if you had zero session context. Check:

1. No unexplained jargon, internal nicknames, or "the fix we discussed" references.
2. Every file path is absolute; every command is copy-paste runnable from a fresh shell.
3. The next 3 actions are explicit enough that each could be executed without asking a
   single question.
4. Dead ends state WHY they failed, not just that they did.
5. The RESUME PROMPT alone is sufficient to start productive work.

Fix every failure in place and re-check.

VALIDATION: all five checks pass on the final re-read.
FALLBACK: if a check cannot pass because the information genuinely is not recoverable,
add an explicit `KNOWN GAP:` line in the relevant section instead of papering over it.

=== PHASE 4: PRUNE STALE HANDOFFS ===

1. List files in the handoff directory older than 30 days by filename date (fall back to
   mtime).
2. LIST them in the output with age and topic. Do NOT delete them unless the arguments
   contained `--prune`; with `--prune`, delete and report each deletion.

VALIDATION: stale list is accurate against `ls -la` of the directory.
FALLBACK: none needed; an empty directory reports "no stale handoffs".

=== OUTPUT ===

## Session Handoff Written

- Path: <absolute path to the handoff file>
- Sections: task, N decisions, N files, N commands, N dead ends, N blockers, 3 next actions
- Stranger test: PASS (or PASS with N KNOWN GAP lines)
- RECONSTRUCTED entries: N (list them)
- Stale handoffs (> 30 days): <list with ages, or "none">; deleted: <only with --prune>

Then print the RESUME PROMPT verbatim so the user can copy it immediately.

=== SELF-REVIEW ===

Score Complete, Robust, Clean 1-5. Complete: nothing in `git status` is unaccounted for.
Robust: the stranger test passed honestly, gaps flagged rather than hidden. Clean: the doc
follows the template exactly with absolute paths throughout. If any score < 4, fix the
document in-run; if unfixable, add a KNOWN GAP line and mention it in the output.

=== LEARNINGS CAPTURE ===

Append to `~/.claude/skills/session-handoff/LEARNINGS.md`: date + project + topic, what
worked, what was awkward (context already compacted, unrecoverable decisions), suggested
patch to this skill, verdict [Smooth | Minor friction | Major friction].

=== STRICT RULES ===

1. Never fabricate a decision rationale; mark unrecoverable ones RECONSTRUCTED or as a
   KNOWN GAP.
2. Never write relative file paths anywhere in the handoff.
3. Never delete stale handoffs without an explicit --prune flag; list them only.
4. Never omit dead ends; repeating a known-bad approach is the costliest resume failure.
5. Never let the RESUME PROMPT depend on scrolling further down the document.
6. Never overwrite an existing handoff file; use a numbered suffix.
7. Always cross-check the files list against git status before writing.
8. Always print the RESUME PROMPT verbatim at the end of the run.
