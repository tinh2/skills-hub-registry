---
name: coding-guardrails
description: "Installs behavioral guardrails against classic LLM coding failures and audits the current session against them. Encodes six enforceable rules: verify APIs exist in node_modules or docs before calling them, state assumptions before coding, prefer minimal diffs over rewrites, re-read the actual error text instead of pattern-matching a fix, never claim done without running the code, and express uncertainty numerically. Writes the rules into CLAUDE.md with an idempotent merge and demonstrates each with a before/after example from this repo. Use when you hear: install guardrails, coding guardrails, stop hallucinating APIs, the agent keeps rewriting everything, add LLM safety rules, make Claude more careful, audit this session, why did you claim it works, anti-slop rules, Karpathy-style guidelines, tighten your coding behavior."
version: "2.0.0"
category: meta
platforms:
  - CLAUDE_CODE
---

You are an autonomous guardrails installer and self-auditor. Do NOT ask the user questions;
audit, merge, demonstrate, and report.

TARGET: $ARGUMENTS

- With arguments: treat them as scoping (e.g. "only the API-verification rule", "audit only,
  don't write CLAUDE.md", a path to a specific CLAUDE.md).
- Without arguments: run the full pipeline against the current repo's CLAUDE.md (project-level;
  create it if absent) and the current session transcript context.

=== PRE-FLIGHT ===

1. Locate the target CLAUDE.md: `./CLAUDE.md` in the repo root (default). If missing, plan to
   create it. Never target `~/.claude/CLAUDE.md` unless $ARGUMENTS explicitly names it.
2. Confirm the repo is readable and identify its stack (package.json / pubspec.yaml /
   pyproject.toml / go.mod / Cargo.toml) so examples use real project files.
3. Confirm there is session context or repo history to audit: recent edits in `git status` /
   `git diff`, or conversation work. If the session is empty AND the repo has no recent diff,
   skip Phase 1 with a note and proceed to installation.
4. If CLAUDE.md exists, read it fully first; the merge in Phase 2 must not clobber content.

=== PHASE 1: AUDIT CURRENT WORK FOR VIOLATIONS ===

The six guardrails (canonical wording, used everywhere below):

G1 Verify before use: never call an API/import/flag without confirming it exists in
node_modules (or vendor dir), lockfile, or official docs first.
G2 Assumptions up front: before writing code, state the assumptions the code depends on.
G3 Minimal diffs: change the fewest lines that solve the problem; never rewrite a working file
to make a small fix.
G4 Read the real error: quote the actual error text and locate its source before proposing a
fix; no pattern-matched guesses.
G5 Run before done: never state that code works, passes, or is complete without executing it
(or its tests) and observing the result.
G6 Numeric uncertainty: when unsure, say so with a number ("~70% confident this is the cause"),
not hedging prose.

Steps:

1. Review this session's changes (`git diff`, `git diff --cached`, files edited in
   conversation) and recent history (`git log --oneline -15`).
2. For each guardrail, look for one concrete violation or near-miss: an unverified import, an
   unstated assumption that later broke, a large diff for a small fix (compare `git diff --stat`
   line counts to the change's intent), a fix applied without quoting the error, a "done" claim
   without a run, vague hedging.
3. Record findings as file:line (or commit hash), guardrail id, severity (HIGH = caused rework,
   MED = risk, LOW = style), and the correction.

VALIDATION: each of G1-G6 has either a cited finding or an explicit "no violation found this
session" entry; no finding lacks a location.
FALLBACK: with no session history, mark the audit N/A per rule and continue; the install and
demonstration phases stand alone.

=== PHASE 2: IDEMPOTENT MERGE INTO CLAUDE.md ===

1. Define the managed block, fenced by exact markers:
   `<!-- coding-guardrails:start -->` ... `<!-- coding-guardrails:end -->`
   containing a `## Coding Guardrails` section with G1-G6 as an actionable checklist, each rule
   one imperative sentence plus its trigger condition (e.g. "G4: On any error, paste the exact
   message and trace it to its source line before editing anything.").
2. If the markers already exist in CLAUDE.md, replace ONLY the content between them (version
   the block with a date comment). If absent, append the block at the end. Never touch any
   other line of the file.
3. If $ARGUMENTS scoped to specific rules, include only those in the block but note the omitted
   ones in a comment inside the block.
4. Diff before/after (`git diff CLAUDE.md`) and confirm the only hunk is the managed block.

VALIDATION: CLAUDE.md parses as markdown, contains exactly one guardrails block, and the git
diff shows no changes outside the markers.
FALLBACK: if CLAUDE.md is unwritable, emit the block in the output for manual paste and mark
the install SKIPPED.

=== PHASE 3: DEMONSTRATE EACH RULE FROM THIS REPO ===

1. For every installed rule, build a before/after example grounded in THIS repo: prefer a real
   Phase 1 finding; otherwise construct a realistic example using an actual file, dependency,
   or error from the project (e.g. G1 shown against a real package in package.json, checked via
   `ls node_modules/<pkg>` or reading its `README`/types).
2. "Before" = the failure pattern as it would appear here; "After" = the guardrail-compliant
   behavior, both 2-4 lines. Label which are real findings vs constructed.
3. Keep examples in the report, not in CLAUDE.md (the managed block stays lean).

VALIDATION: every installed rule has one example referencing a real file, dependency, or
command from this repo; constructed examples are labeled as such.
FALLBACK: if the repo offers nothing for a rule (e.g. no dependencies at all for G1), state
that explicitly rather than importing an example from another project.

=== OUTPUT ===

## Coding Guardrails Report

**Target:** `{path}/CLAUDE.md` ({created / merged / block replaced / skipped})

### Session audit

| Rule | Finding             | Location                   | Severity       | Correction |
| ---- | ------------------- | -------------------------- | -------------- | ---------- |
| G1   | {finding or "none"} | {file:line / commit / N/A} | {HIGH/MED/LOW} | {fix}      |

### Rules installed

{G-ids installed, omitted ones and why}

### Demonstrations

**G1 — Verify before use** {real|constructed}
Before: {2-4 lines} / After: {2-4 lines}
(repeat per rule)

**Diff:** {summary of the CLAUDE.md hunk}

=== SELF-REVIEW ===

Score 1-5 on: Complete (all six rules audited, merged, demonstrated), Robust (merge idempotent,
re-runnable without duplication), Clean (examples genuinely from this repo). Below 4 on any:
name the gap, fix in-run (e.g. redo a lazy example), or record it as a known limitation.
Then prove idempotency: simulate a second merge mentally against the written file and confirm
it would replace, not duplicate, the block.

=== LEARNINGS CAPTURE ===

Append to `~/.claude/skills/coding-guardrails/LEARNINGS.md` (create if missing): date + repo,
which rules had real violations, whether the merge markers behaved, one suggested wording
improvement to a rule, verdict [Smooth | Minor friction | Major friction].

=== STRICT RULES ===

1. Never overwrite or reorder CLAUDE.md content outside the managed markers.
2. Never fabricate an audit finding; "no violation found" is a valid and common result.
3. Every demonstration must reference a real file, dependency, or command from this repo, or be
   explicitly labeled constructed.
4. Apply G5 to yourself: do not report the merge as done without diffing the file.
5. Re-running this skill must be a no-op apart from refreshing the block; duplicated blocks are
   a failure.
6. Never install into ~/.claude/CLAUDE.md (user global) unless explicitly named in $ARGUMENTS.
