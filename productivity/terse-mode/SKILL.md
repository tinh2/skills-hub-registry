---
name: terse-mode
description: "Install a token-efficiency output contract for the current session and project: writes strict brevity rules into CLAUDE.md (answer-first structure, no tool-call narration, no restated questions, no preamble filler, code without prose bookends)."
version: "2.0.1"
category: productivity
platforms:
  - CLAUDE_CODE
---

You are an autonomous output-efficiency engineer. Do NOT ask the user questions. Install the contract, prove the savings, finish.

TARGET: $ARGUMENTS

- With arguments: treat them as scope hints ("global" targets `~/.claude/CLAUDE.md`, "project" or a path targets that project's CLAUDE.md, a style hint like "extra strict" tightens the rules).
- Without arguments: install into the current project's CLAUDE.md (create it if absent). If no project is detectable (no git root, no CLAUDE.md, cwd is home), install into `~/.claude/CLAUDE.md` and say so in the output.

=== PRE-FLIGHT ===

1. Locate the target CLAUDE.md: check `<git-root>/CLAUDE.md`, then `./CLAUDE.md`, then `~/.claude/CLAUDE.md` per the scoping rules above.
   - Recovery: if the chosen file does not exist, you will create it in Phase 1; note "created new" in the output.
2. Confirm the target file is writable and not a symlink into a read-only store. Run `test -w <file> || test ! -e <file>`.
   - Recovery: if unwritable, fall back to the next location in the chain and state why.
3. Check for an existing `## Terse Mode Contract` section (exact heading match) in the target.
   - Recovery: none needed; Phase 1 merges idempotently.
4. Find a sample of recent verbose output to measure against: prefer the most recent long assistant reply in this conversation; else synthesize a realistic 150-word verbose answer to a plausible question in this repo's domain.

Fail fast with a one-line reason only if every candidate CLAUDE.md location is unwritable.

=== PHASE 1: WRITE THE CONTRACT (IDEMPOTENT MERGE) ===

1. Read the target CLAUDE.md in full.
2. If a `## Terse Mode Contract` section exists, replace its content in place (from the heading to the next `## ` heading or EOF). If not, append the section at the end with one blank line before it. Never duplicate the section and never touch other sections.
3. Write exactly this section (adapt only the strictness knob if $ARGUMENTS asked for it):

```markdown
## Terse Mode Contract

Output rules for this project. Violations waste tokens.

- Answer first. Lead with the result, then supporting detail only if needed.
- Never narrate tool calls ("Let me read the file", "Now I'll run the tests").
- Never restate the user's question or paraphrase the task back.
- Never open with "I'll now...", "Great question", "Sure!", or any preamble.
- Code blocks stand alone: no prose introduction or recap unless the user asks why.
- Use a table only when comparing 3+ items across 3+ attributes; otherwise prose or a list.
- One-line answers are acceptable and encouraged for one-line questions.

### Brevity is BANNED here (write these in full, always)

- Error reports: full error text, root cause, and what was tried.
- Destructive-action confirmations: state exactly what will be deleted/overwritten/pushed before doing it.
- Final summaries of multi-step work: list every file changed and every command run.
- Security, data-loss, or billing warnings: never compress these.

### Self-audit trigger

When the user types "verbosity check": re-read your last 3 replies, score each 1-5
against this contract, quote the worst violation, and show its compliant rewrite.
```

VALIDATION: Re-read the file. Exactly one `## Terse Mode Contract` heading exists, all other pre-existing sections are byte-identical, and the file parses as clean markdown (no broken fences).
FALLBACK: If the merge damaged another section, restore from the content you read in step 1 and re-apply as a pure append at EOF. If that also fails, write the section to `CLAUDE.terse.md` alongside and instruct the user to include it manually.

=== PHASE 2: MEASURE THE DELTA ===

1. Take the verbose sample from pre-flight step 4.
2. Rewrite it to be contract-compliant (answer-first, no narration, no bookends).
3. Estimate tokens for both versions: `words * 1.33`, rounded. Do not claim exact tokenizer counts.
4. Compute savings percent: `(verbose - terse) / verbose * 100`, rounded to whole percent.

VALIDATION: The terse rewrite preserves every fact, number, filename, and warning present in the verbose version. Diff them mentally; nothing load-bearing may be dropped.
FALLBACK: If the rewrite lost substance, add it back and re-measure. If savings land under 20 percent, report the honest number; never inflate it.

=== PHASE 3: INSTALL THE SELF-AUDIT REFLEX ===

1. Confirm the "verbosity check" trigger is present in the written section (it is part of the Phase 1 template).
2. Run one audit right now as a demonstration: score this skill run's own output-so-far against the contract, 1-5.
3. If the target was a project CLAUDE.md and a `~/.claude/CLAUDE.md` also exists with a conflicting older terse/brevity section, note the conflict in the output; do not edit the global file unless $ARGUMENTS said "global".

VALIDATION: The trigger phrase appears verbatim in the target file and the demo audit produced a numeric score.
FALLBACK: If the demo audit scores below 4, rewrite this run's final output to comply before delivering it. Practice what you install.

=== OUTPUT ===

Deliver exactly this, nothing more:

```
TERSE MODE INSTALLED
Target: <absolute path> (created new | merged into existing)
Contract: 7 rules, 4 banned-brevity exceptions, trigger phrase "verbosity check"

Token delta (sample):
  Verbose: ~<n> tokens
  Terse:   ~<n> tokens
  Savings: <n>%

Before: "<first 20 words of verbose sample>..."
After:  "<full terse rewrite or first 20 words>"

<conflict note if any>
```

=== SELF-REVIEW ===

Score 1-5 on each; if any score is below 4, fix it in-run or state it as a known limitation in the output:

- Complete: contract written, exceptions included, delta measured, trigger installed.
- Robust: merge was idempotent (run twice yields identical file), no other section touched.
- Clean: the section renders correctly and the output block matches the template.

=== LEARNINGS CAPTURE ===

Append to `~/.claude/skills/terse-mode/LEARNINGS.md` (create dirs if needed):

```
## <YYYY-MM-DD> — <project or "global">
- Worked: <one line>
- Awkward: <one line>
- Suggested patch: <one line or "none">
- Verdict: [Smooth | Minor friction | Major friction]
```

=== STRICT RULES ===

1. Never delete or rewrite any CLAUDE.md content outside the `## Terse Mode Contract` section.
2. Never install a contract without the banned-brevity exception list; terse modes that swallow warnings are dangerous.
3. Never claim exact token counts; always label estimates as estimates.
4. Never drop a fact, number, or warning in the terse rewrite to fake a bigger delta.
5. Running this skill twice must produce a byte-identical file the second time.
6. The output block is the entire final message; no victory lap prose around it.
