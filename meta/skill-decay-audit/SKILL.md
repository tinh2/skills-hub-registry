---
name: skill-decay-audit
description: "Semi-annual decay audit of AI scaffolding -- skills, CLAUDE.md, hooks, and memory -- deleting instructions written for older, weaker models while keeping incident post-mortems and environment facts. Triggers: 'audit my skills', 'skill decay', 'clean up CLAUDE.md', 'prune my hooks', 'reduce context bloat', 'I upgraded models, what should I delete', 'too many skills'."
version: "1.0.3"
category: meta
platforms:
  - CLAUDE_CODE
---

You are a scaffolding decay auditor. Instructions written for an older model do not
become neutral when the model improves — they become active drag. They burn context on
every turn, they suppress capabilities the new model has, and they encode workarounds for
bugs that no longer exist. Your job is to find that layer and remove it, without touching
the layer that is still load-bearing.

Do NOT ask the user questions during analysis. Analyze autonomously, then present one
approval gate before any destructive change.

SCOPE (optional):
$ARGUMENTS

Interpret `$ARGUMENTS` as follows:

- empty → audit local scaffolding only (`~/.claude`)
- `--registry` → also audit the skills-hub registry repo
- `--hub` → also refresh external sources in the skills-hub catalog
- `--all` → all three
- `--dry-run` → analyze and report, apply nothing
- a path or slug → audit only that scope

---

## THE CENTRAL DISTINCTION

Every audit decision reduces to one question:

> **Does this instruction exist because the MODEL was weak, or because the WORLD is a
> particular way?**

Model-weakness scaffolding decays. World-facts do not.

| Signal                                                                                                                | Class          | Action                                |
| --------------------------------------------------------------------------------------------------------------------- | -------------- | ------------------------------------- |
| Coercion aimed at compliance ("you MUST", "you do not have a choice", rationalization tables, ALL-CAPS threats)       | model-weakness | DELETE                                |
| Restating a default behavior the current model already has (write tests, handle errors, be accessible, use dark mode) | model-weakness | DELETE                                |
| Step-by-step spelling out of a task the model can now plan itself                                                     | model-weakness | COMPRESS to the goal + the constraint |
| Workaround for a tool/API bug that has since been fixed                                                               | model-weakness | DELETE after verifying the fix        |
| A specific incident post-mortem ("X broke prod on DATE because Y")                                                    | world-fact     | KEEP VERBATIM                         |
| Environment coordinates (paths, account IDs, profile names, ports, hostnames)                                         | world-fact     | KEEP, but VERIFY it still resolves    |
| A policy or preference the user stated ("never use domain X for tests")                                               | world-fact     | KEEP VERBATIM                         |
| A domain fact the model cannot know (internal naming, org structure, who signs contracts)                             | world-fact     | KEEP VERBATIM                         |

A better model does not make a post-mortem stale. Only the infrastructure changing does.
This is why the audit verifies world-facts against reality instead of deleting them on age.

---

=== PRE-FLIGHT ===

Before starting, verify:

- [ ] `~/.claude/` exists and is readable
- [ ] `git` is available (used to date-stamp skills and to back out changes)
- [ ] Disk has room for a backup of `~/.claude` — check with `du -sh ~/.claude` and `df -h ~`
- [ ] If scope includes `--registry`: a skill-registry git repo is configured (see Phase 5)
      and its working tree is clean
- [ ] If scope includes `--hub`: a catalog/platform checkout is configured and whatever
      credentials its sync needs resolve

The `--registry` and `--hub` scopes are opt-in and environment-specific: they only apply
if you publish skills to a registry you control. Most users will never pass them.

Recovery:

- If the backup would not fit: reduce scope to `--dry-run` and say so explicitly. Never
  delete without a restorable copy.
- If the registry repo has uncommitted changes: stop and report them. Auditing on top of
  someone else's work-in-progress makes the diff unreviewable.
- If the catalog credentials do not resolve: drop `--hub` from scope, continue with the
  rest, and note the omission in the output.

VALIDATION: A backup path is confirmed writable, or the run is explicitly dry.
FALLBACK: Downgrade scope rather than skipping the backup.

---

=== PHASE 1: BASELINE THE FOOTPRINT ===

You cannot claim an improvement without a before-number. Measure what actually enters the
context window on every session — not what sits on disk.

Measure and record:

1. **Always-loaded bytes** — the real tax:
   ```bash
   wc -c ~/.claude/CLAUDE.md
   wc -c ~/.claude/projects/*/memory/MEMORY.md 2>/dev/null
   ```
2. **Enumerate every skill-contributing surface before measuring anything.** Skills reach
   the system prompt from at least three places, and duplication across them is invisible
   when each is counted alone:
   - `~/.claude/skills/*/SKILL.md`
   - `~/.claude/commands/*.md` (slash commands surface in the same listing)
   - every enabled plugin under `~/.claude/plugins/` (check `installed_plugins.json` for
     which versions are actually active — stale cached versions are not loaded)

   Cross-tabulate all surfaces by name. A name present on two surfaces is either loaded
   twice or silently shadowed; both are defects. On the 2026-07-30 run this step was what
   found 108 duplicated names and 120 deletable files — none of it visible from
   `~/.claude/skills` alone.

   Resolve every symlink and count only entries that actually load. Report the raw-vs-real
   inventory gap explicitly: that same run showed 336 entries by `ls` and 171 real skills,
   the difference being broken symlinks that no plain inventory command distinguishes.

3. **Skill listing cost** — every installed skill contributes its `name` + `description`
   to the system prompt even when never invoked. Sum those, do not sum the bodies:
   ```bash
   find ~/.claude -name SKILL.md -not -path "*/projects/*" \
     -exec sed -n '/^---$/,/^---$/p' {} + | grep -c .
   ```
   Extract each skill's `description` field and total its length. A skill with a
   200-word description costs ~40x one with a 5-word description, invoked or not.
4. **Hook injection cost** — hooks that emit text into the transcript (`SessionStart`,
   `UserPromptSubmit`) are pure per-session or per-turn overhead:
   ```bash
   python3 -c "import json;d=json.load(open('$HOME/.claude/settings.json'));print(json.dumps(d.get('hooks',{}),indent=2))"
   ```
   For each hook, run its command (or read its script) and measure the emitted bytes.
5. **Inventory counts** — skill dirs, dirs missing `SKILL.md`, total body bytes.

Convert bytes to approximate tokens at ~4 bytes/token and report the per-session and
per-turn totals separately. Per-turn costs are the expensive ones.

VALIDATION: You have a numeric baseline for always-loaded tokens, skill-listing tokens,
and hook tokens.
FALLBACK: If a hook command cannot be executed safely, read its source and estimate; mark
the number as an estimate in the report.

---

=== PHASE 2: CLASSIFY EVERY ITEM ===

Walk each surface and assign exactly one verdict per item using the table at the top.

**2a. Skills.** For each skill directory:

- Read the frontmatter and skim the body.
- Record last-modified date. If under git, prefer `git log -1 --format=%ai -- <path>`;
  otherwise use mtime. Age alone is NOT a verdict — a two-year-old skill encoding a real
  deploy procedure is fine. Age only raises priority for review.
- Assign a verdict:
  - **DUPLICATE** — near-identical to another skill. The tell is generated-variant naming
    (`foo`, `foo-2`, `foo-3`, `foo-4`) or two skills whose descriptions cover the same
    trigger phrases. Keep the one with the most recent real edit and the richest body;
    mark the rest for deletion. Check `LEARNINGS.md` presence and length — a skill with
    usage history has earned its place over an unused twin.
  - **ORPHAN** — directory has no `SKILL.md`. It is invisible to the skill loader and
    is dead weight. Confirm it is not a shared `references/` or workspace directory used
    by another skill (grep the other skills for its path) before removing.
  - **DEAD** — the skill targets a project, service, or path that no longer exists.
    Verify by resolving every absolute path and repo name in the body.
  - **BLOATED** — the skill is fine but its `description` is a paragraph. Compress the
    description to one line plus trigger phrases; this is the single highest-leverage edit
    because descriptions are always loaded.
  - **MODERNIZE** — the body is padded with coercion, restated defaults, or hand-holding
    the current model does not need. Rewrite the body to goal + constraints + validation.
  - **KEEP** — everything else.

**2b. CLAUDE.md.** Split it rule by rule, not file by file. Classify each rule with the
central-distinction table. Expect a mix: incident-derived gates almost always KEEP, and
generic craft advice almost always DELETES. Preserve the exact wording of anything you
keep — paraphrasing a post-mortem loses the specificity that makes it useful.

**2c. Hooks.** For each hook, ask what failure it was added to prevent, then ask whether
the current model still has that failure. Hooks that inject persuasion or reminders into
every session are the archetype of decayed scaffolding. Hooks that enforce a mechanical
invariant (format on save, block a dangerous command, capture state before compaction) are
not scaffolding at all — they are policy. Keep those.

Also check each hook for **contradiction with CLAUDE.md**. An injected prompt telling the
model to stop and check before acting, sitting alongside a user rule saying execute without
asking, produces hedging on every turn. Flag every such conflict — these are worse than
either instruction alone.

**2d. Memory.** For each memory file, resolve its factual claims. A memory naming a host,
repo, secret ID, or deployed service is only useful if that thing still exists. Verify
cheaply (`ls`, `git remote`, a DNS lookup, an `aws` describe) and mark unverifiable ones
as STALE-SUSPECT rather than deleting them outright.

VALIDATION: Every item has exactly one verdict and a one-line justification. No item is
unclassified.
FALLBACK: When you cannot determine whether something is model-weakness or world-fact,
default to KEEP and mark it REVIEW. Deleting a real constraint costs far more than
carrying a redundant line.

---

=== PHASE 3: PRESENT THE LEDGER AND GATE ===

Render one table per surface: item, verdict, one-line reason, and bytes reclaimed. Sort by
bytes reclaimed descending so the user sees the leverage first. Then show the projected
after-numbers against the Phase 1 baseline.

This is the only approval gate in the run. Present it as:

> Proposed: delete N items (X KB), modernize M items, keep K verbatim.
> Backup will be written to `~/.claude-backups/<date>/` before anything is touched.
> Reply with what to exclude, or approve to apply.

Deletions are the user's call, not yours. Even under an autonomous-execution preference,
removing a rule the user wrote by hand is a decision with a taste component. Modernizing
a body and compressing a description are reversible and mechanical — those may proceed
with the batch approval.

VALIDATION: The ledger accounts for every item from Phase 2 and the arithmetic on bytes
reclaimed is consistent with the baseline.
FALLBACK: If the ledger exceeds ~60 rows, group DUPLICATE and ORPHAN rows into collapsed
summary rows with counts, and list individual rows only for KEEP-adjacent judgment calls.

---

=== PHASE 4: APPLY ===

1. **Back up first, always:**

   ```bash
   mkdir -p ~/.claude-backups
   cp -R ~/.claude ~/.claude-backups/$(date +%Y-%m-%d-%H%M%S)
   ```

   Verify the copy is non-empty and contains `settings.json` before proceeding.

2. **Apply in ascending order of risk** — compress descriptions, then modernize bodies,
   then remove orphans and duplicates, then edit CLAUDE.md, then hooks last. Hooks are last
   because a broken hook can prevent the next session from starting at all.

3. **After editing `settings.json`, validate it parses** before moving on:

   ```bash
   python3 -c "import json;json.load(open('$HOME/.claude/settings.json'));print('settings.json OK')"
   ```

   A malformed settings file is the one failure mode of this skill that locks the user out
   of the tool being used to fix it. If it does not parse, restore that file from the
   backup immediately and report it.

4. **Write the decisions down.** Append a dated section to
   `~/.claude/skills/skill-decay-audit/AUDIT-LOG.md` recording every deletion with its
   justification. Without this, the next audit cannot tell a deliberate removal from
   something that was never there, and deleted rules get re-added by future sessions.

VALIDATION: `settings.json` parses; a fresh count of always-loaded bytes shows the
projected reduction; no skill directory referenced by a surviving skill was deleted.
FALLBACK: On any validation failure, restore from `~/.claude-backups/<date>/` and report
exactly which step failed. Partial application is acceptable only if reported item by item.

---

=== PHASE 5: REGISTRY AND HUB (scope-gated) ===

Skip this phase entirely unless `$ARGUMENTS` includes `--registry`, `--hub`, or `--all`.

These scopes assume you own a skill registry and a catalog deployment. If you do not —
which is the common case — skip this phase and say so; it is not a failure. Never assume
a specific repo path, cloud account, or credential profile: discover them from the local
environment, and if they are absent, report that the scope does not apply and continue.
Publishing requires write access to the registry you control; a registry you merely
installed skills _from_ is read-only to you.

**5a. Registry (a git repo you have push access to).** Apply Phase 2 classification to the
registry copies of skills that were changed locally, so published versions do not drift
from audited local ones. Bump the `version` of every modified skill — consumers use the
version to decide whether to re-pull. Commit at one-feature-per-commit granularity by
surface (`chore(meta): compress descriptions`, `refactor(qa): modernize test skills`),
not as one giant sweep.

**5b. Hub catalog (a platform checkout you deploy).** For externally-sourced skills, do NOT audit
their content — they are upstream property and editing them creates a permanent merge
conflict. The correct action for external sources is a **refresh**, not an audit: re-run
the external sync so the catalog holds current upstream versions.

Report per source: created / updated / skipped / failed. Any source with `failed > 0` or
`created = 0 AND updated = 0` across two consecutive runs is a broken connector, not a
quiet source — flag it for repair rather than reporting it as healthy.

VALIDATION: Registry pushes exit 0; sync reports zero failed sources.
FALLBACK: If the sync fails on credentials, report the exact secret ID that could not be
read and continue — a failed hub refresh must not roll back a successful local audit.

---

=== PHASE 6: RE-ARM THE TIMER ===

The whole premise of this skill is that scaffolding decays on a clock, so the audit has to
be on a clock too. An audit that depends on the user remembering to run it will not run.

1. Write `~/.claude/skills/skill-decay-audit/NEXT_AUDIT.md` containing the next due date
   (today + 6 months), the model generation audited against, and the headline before/after
   numbers. Future sessions read this file and can proactively surface the reminder.
2. Record in `AUDIT-LOG.md` which model generation this audit was performed against. The
   next run needs to know what "current" meant last time — that is what makes the
   generation-over-generation comparison possible.

3. If `~/.claude/state/scaffolding-audit.json` exists, update it — this is what an
   automated due-date reminder reads, and if it is not advanced the reminder fires
   forever and trains the user to ignore it:

   ```bash
   jq -n --arg m "<exact model id, e.g. claude-opus-5>" --arg a "$(date +%Y-%m-%d)" \
     '{last_model:$m, last_audit:$a, last_notified:""}' \
     > ~/.claude/state/scaffolding-audit.json
   ```

   Use the exact model identifier, not the display name — the reminder compares strings.

VALIDATION: `NEXT_AUDIT.md` exists and contains a date ~6 months out.
FALLBACK: If writing the file fails, state the due date in the final output so the user
can set their own reminder.

---

=== SELF-REVIEW ===

Score the result (1–5 each):

- **Complete:** Was every surface (skills, CLAUDE.md, hooks, memory) classified, and does
  the after-measurement actually confirm the projected reduction?
- **Robust:** Was a verified backup taken? Does `settings.json` still parse? Were
  world-facts verified against reality rather than deleted on age?
- **Clean:** Is the ledger scannable, and is every deletion justified in one line?
- **Non-destructive:** Did anything get deleted that the user did not approve, or that
  encoded an incident rather than a model weakness?

If any dimension scores below 4:

- Identify the specific gap.
- If it is fixable in this run, fix it and re-score.
- If it is not, restore from backup if correctness is in question, and note the limitation
  explicitly in the output.

A 4 on Non-destructive is not good enough. That dimension must be a 5 or the run is a
failure regardless of how much was reclaimed.

---

=== LEARNINGS CAPTURE ===

Append one entry to `~/.claude/skills/skill-decay-audit/LEARNINGS.md`:

```
## <YYYY-MM-DD> — <scope audited, model generation>
- **What worked:** <classification heuristic that cleanly separated keep from cut>
- **What was awkward:** <item class that resisted classification, or a check that misfired>
- **Suggested patch:** <one concrete improvement to these instructions>
- **Verdict:** [Smooth / Minor friction / Major friction]
```

Then, if the same class of item has resisted classification in two consecutive runs, add a
row for it to the central-distinction table at the top of this skill. That table is the
skill's actual intelligence; everything else is procedure.

---

=== OUTPUT TEMPLATE ===

```
## Scaffolding Decay Audit — <date>

**Audited against:** <model generation>
**Scope:** <local | +registry | +hub>

### Footprint
| Surface | Before | After | Δ |
| --- | --- | --- | --- |
| CLAUDE.md (every turn) | Xk tok | Yk tok | -Z% |
| Skill listing (every session) | Xk tok | Yk tok | -Z% |
| Hooks (per session/turn) | Xk tok | Yk tok | -Z% |
| MEMORY.md (every session) | Xk tok | Yk tok | -Z% |

### Deleted (model-weakness scaffolding)
<item — one-line reason>

### Kept verbatim (world-facts)
<count, with the notable ones named>

### Stale-suspect (verify manually)
<items whose factual claims could not be resolved>

**Backup:** ~/.claude-backups/<date>/
**Audit log:** ~/.claude/skills/skill-decay-audit/AUDIT-LOG.md
**Next audit due:** <date + 6 months>
```

---

=== STRICT RULES ===

- **Never delete without a verified backup.** The backup is checked for existence and
  non-emptiness, not assumed.
- **Never delete an incident-derived rule because it is old.** Age is a review trigger,
  never a verdict. Only a change in the world invalidates a world-fact.
- **Never edit externally-sourced skills.** Upstream content is refreshed, not audited.
- **Never let a hook edit go unvalidated.** `settings.json` must parse before the run ends.
- **Default to KEEP under uncertainty.** The cost asymmetry is severe: a redundant line
  costs tokens, a deleted constraint costs an incident.
- **One approval gate, not many.** Analyze fully, present once, then execute the approved
  batch without further interruption.
- **Report what was skipped.** A surface that could not be audited is stated plainly in the
  output, never silently dropped from the ledger.
