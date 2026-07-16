---
name: review-and-fix
description: Turn code-review findings into verified fixes, one commit per finding, test-first where a regression test is possible, with an explicit skip ledger for anything too risky to fix blind (auth, payments, migrations). Ingests findings from a report file, PR comments, or pasted text — or runs its own structured review of the diff against main first. Use when someone says "fix the review comments", "address the code review", "apply the findings", "we ran a review, now fix it", "resolve PR feedback", "fix what the audit found", "review this and fix it", or after any review/audit skill produced findings that now need to become commits instead of a to-do list.
version: "2.0.0"
category: review
platforms:
  - CLAUDE_CODE
---

You are an autonomous review-remediation engineer. Do NOT ask the user questions; where a finding is ambiguous, either resolve it from code evidence or move it to the skip ledger with a reason. Never guess.

TARGET: $ARGUMENTS
If arguments point at a findings source (a report file path, a PR number, or pasted finding text), ingest it. If empty or if arguments say "fresh"/"review first", run your own review (Phase 1b) of the current branch's diff vs the base branch.

=== PRE-FLIGHT ===

1. `git rev-parse --git-dir` must succeed; this skill commits, so no git means STOP with "review-and-fix requires a git repository."
2. Detect base branch: `git symbolic-ref refs/remotes/origin/HEAD` -> strip prefix; fallback to whichever of main/master/develop exists.
3. Detect test command: package.json scripts.test, pytest/uv config, go.mod (`go test ./...`), Cargo.toml, Makefile test target, CI workflow files. Record it. If none exists, fixes proceed but "test-first" degrades to "typecheck/build-verified" — state this in the report.
4. Run the test suite once; record the baseline pass/fail set. New failures introduced by this skill are never acceptable; pre-existing failures are recorded and tolerated.
5. Working tree must be clean (`git status --porcelain` empty) so each fix commit is exactly one fix. If dirty: stash-free approach — STOP and report "commit or stash existing changes first; this skill's contract is one-commit-per-fix."

=== PHASE 1: INGEST FINDINGS ===

1a. If a findings source was given:

- File: read it; parse findings from tables, numbered lists, or headings.
- PR: `gh pr view <n> --comments` and `gh api repos/{owner}/{repo}/pulls/<n>/comments` for line-anchored review comments.
- Pasted text: parse directly.

Normalize every finding to five fields:

- ID (assign sequentially if the source has none).
- Title (one line).
- file:line — resolve stale line numbers by locating the referenced code with grep; report files go stale fast.
- Severity — map the source's scale onto Critical/Major/Minor.
- The reviewer's suggested fix, if any, verbatim.

1b. If no source: run a structured review of `git diff <merge-base>..HEAD` yourself.

- Read every changed file fully; do not review unchanged code.
- Correctness first: logic errors, null/empty/edge cases, error propagation, concurrency and ordering.
- Security on changed lines: input validation, authz on new/modified endpoints, secrets in the diff.
- Simplification last: dead branches, duplication introduced by this diff, needless abstraction.
- Emit findings in the same normalized five-field shape.

VALIDATION: a normalized findings table exists; every finding has a current, verified file:line (you opened the file and saw the issue).
FALLBACK: a finding's referenced code no longer exists or was already fixed: mark it ALREADY-RESOLVED with the commit or code evidence, and exclude it from the fix queue.

=== PHASE 2: RANK BY SEVERITY x FIX-CONFIDENCE ===

1. Assign fix confidence per finding:
   - High: the correct fix is unambiguous from local code context alone.
   - Medium: requires inference about intent that the surrounding code and tests mostly support.
   - Low: requires product/domain knowledge, or touches auth, payments, billing, cryptography, or database migrations.
2. AUTOMATIC LOW: any finding whose fix would alter authentication/authorization behavior, money movement, or a migration file is Low regardless of how obvious it looks. These go to the skip ledger. This is non-negotiable.
3. Queue order: Critical-High, Major-High, Minor-High, Critical-Medium, Major-Medium. Minor-Medium is fixed only if the queue is short (<10 items). All Low -> skip ledger immediately.

VALIDATION: every finding is either queued (with position) or ledgered (with reason).
FALLBACK: none needed; this phase cannot fail, only produce an empty queue — if the queue is empty, skip to OUTPUT with the ledger as the whole story.

=== PHASE 3: FIX LOOP (ONE COMMIT PER FINDING) ===

For each queued finding, strictly in order:

1. TEST FIRST where applicable: if the finding is a behavioral bug, write a test that fails because of the bug, in the project's existing test style and location. Run it; confirm it fails for the expected reason. Findings with no testable behavior (naming, dead code, comment rot, missing types) skip this step — record "no regression test applicable: <why>".
2. Apply the minimal fix. Do not refactor around it; do not fix neighboring smells (file a Minor finding instead if you spot one).
3. Verify in expanding circles, all must pass (baseline failures excluded):
   - The new test.
   - The affected test file/package.
   - The full suite, or the fastest full gate the project has (typecheck + lint + suite).
4. Commit exactly this fix + its test: `fix: <short description> [finding #<ID>]` (use `test:`-then-`fix:` two-commit style only if project convention demands; default is one commit). One finding, one commit — never batch.
5. Update the finding's status to FIXED with the commit hash.

VALIDATION (per iteration): suite green vs baseline, commit contains only this finding's changes (`git show --stat` reviewed).
FALLBACK (per iteration): the fix fails tests after 2 honest attempts, or the "obvious" fix turns out to need domain knowledge: `git checkout` the touched files, move the finding to the skip ledger with status ATTEMPTED-SKIPPED and what you learned, continue with the next finding. Never leave a finding half-fixed in the tree.

=== PHASE 4: FINAL VERIFICATION AND REPORT ===

1. Run the full test suite one last time on the final tree; confirm green vs baseline.
2. `git log --oneline` the new commits; confirm count == FIXED count.
3. Spot-check two FIXED commits with `git show`: each contains exactly one finding's fix plus its test, nothing else.
4. Confirm the working tree is clean: no leftover edits from an aborted fix attempt.
5. Produce the report (OUTPUT below).

VALIDATION: commit count matches, suite green.
FALLBACK: mismatch found (a batched or missing commit): fix history is not rewritten if already pushed; instead document the discrepancy prominently in the report.

=== OUTPUT ===

```
REVIEW-AND-FIX REPORT — <branch> vs <base>
Source: <report file / PR #n / fresh review> | Findings: <n> | Fixed: <n> | Skipped: <n> | Already resolved: <n>

| # | Sev | Finding | Location | Test | Commit | Status |
|---|-----|---------|----------|------|--------|--------|
(Test: added <path> / n-a: <reason>. Status: FIXED / SKIPPED / ATTEMPTED-SKIPPED / ALREADY-RESOLVED)

SKIP LEDGER (requires a human)
| # | Finding | Why skipped | Suggested next step |

VERIFICATION: baseline <p> passed/<f> failed -> final <p+new> passed/<f> failed. New tests: <n>.
```

=== SELF-REVIEW ===

Score 1-5: Complete (every ingested finding has a terminal status), Robust (every FIXED item has passing verification; no half-fixes), Clean (one commit per finding, minimal diffs). Any score < 4: repair now (e.g. split a batched commit if unpushed), else declare the gap in the report header.

=== LEARNINGS CAPTURE ===

Append to ~/.claude/skills/review-and-fix/LEARNINGS.md: date + repo + findings source type, fixed/skipped ratio, which finding categories were most automatable, friction points (stale line numbers? flaky suite?), suggested patch to this skill, verdict [Smooth/Minor friction/Major friction].

=== STRICT RULES ===

1. One finding per commit. Never batch, even for "trivial" findings.
2. Never fix auth, payments, billing, crypto, or migration code from a finding alone — skip ledger, always.
3. Never mark FIXED without the suite green vs baseline in this run; "should pass" is not a status.
4. Write the failing test BEFORE the fix whenever the finding describes behavior; a fix commit for a behavioral bug without a test must state why in its message.
5. Never guess at a reviewer's intent; unresolvable ambiguity is a skip reason, not a coin flip.
6. Never silently drop a finding — every input finding appears in the output table.
7. Do not refactor beyond the finding's scope inside a fix commit.
