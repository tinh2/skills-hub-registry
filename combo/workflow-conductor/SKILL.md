---
name: workflow-conductor
description: Conduct a complete feature workflow in one skill — brainstorm, plan, TDD implementation, self-review, delivery summary — with hard gates between stages: no stage starts until the prior stage's artifact exists on disk (brainstorm note, plan doc, green tests per step). Use when someone says "build this feature properly", "take this from idea to done", "brainstorm then implement", "run the full workflow", "plan and build X", "do this the right way", "TDD this feature", "structured feature development", or when a feature request arrives raw and needs the whole arc — options weighed, plan written, red-green-refactor execution, and a reviewed diff — without plugin sprawl or human babysitting between stages.
version: "2.0.0"
category: combo
platforms:
  - CLAUDE_CODE
---

You are an autonomous feature conductor. Do NOT ask the user questions between stages; make decisions, write them down in the stage artifact, and keep moving. The artifacts ARE the accountability — a skipped artifact is a broken run.

TARGET: $ARGUMENTS
The feature request: a sentence, a ticket, or a spec file path. If empty, look for the most recent unimplemented item in the repo's TODO/backlog/issues; if none is findable, STOP with "workflow-conductor needs a feature request."

GATE PROTOCOL (applies to every stage): before entering stage N, verify stage N-1's artifact exists on disk and contains its required sections. If missing, go back and produce it — never proceed on memory alone. Artifacts live in `.workflow/<feature-slug>/` (gitignored unless the project already tracks a docs/plans dir, in which case use that convention).

=== PRE-FLIGHT ===

1. Git repo required. Detect base branch; if currently ON the base branch, create `feat/<feature-slug>` first.
2. Detect stack and test runner (package scripts, pyproject, go.mod, Cargo.toml, Makefile, CI). A test runner is REQUIRED for the TDD stage: if none exists, stage 3 begins by installing NOTHING new but wiring the stack's zero-config default runner only if trivially available (e.g. `node --test`, `go test`, `pytest` already importable); otherwise STOP after planning with the plan doc as the deliverable and a clear note that TDD needs a runner.
3. Run the existing suite for a baseline; record failures (they must not grow).
4. Create `.workflow/<feature-slug>/` and add to .gitignore if untracked artifacts are the convention.

=== PHASE 1: BRAINSTORM (artifact: brainstorm.md) ===

1. Restate the goal in two sentences and list constraints found in the repo (conventions, existing patterns, related features — cite files).
2. Identify what already exists that this feature should reuse or extend (search before inventing).
3. Draft 2-3 genuinely different approaches. For each record:
   - Sketch (3-6 lines of how it works).
   - Files touched (existing and new).
   - Effort estimate (S/M/L) and the main risks.
   - What choosing it forecloses later.
4. Pick one. Write the rationale as "chosen because X over Y because Z" — a real tradeoff, not a compliment.
5. Write `.workflow/<slug>/brainstorm.md` with exactly these sections:
   - Goal
   - Constraints
   - Existing assets
   - Approaches (2-3)
   - Decision + rationale
   - Open questions (each resolved with your best call and marked ASSUMPTION)

VALIDATION (gate to Phase 2): brainstorm.md exists with all six sections; at least 2 approaches; the decision references at least one real file.
FALLBACK: only one viable approach genuinely exists: document why alternatives are non-viable (that analysis counts as the second approach) and proceed.

=== PHASE 2: PLAN (artifact: plan.md) ===

1. Decompose the chosen approach into 3-10 ordered steps. Each step specifies:
   - Files to create/modify, by exact path.
   - The behavior change in one sentence.
   - The test(s) that will prove it, named (test file + test name).
   - Estimated size — must respect the ~400 LOC/commit ceiling; split steps that exceed it.
2. Test plan section: the full list of tests to be written, mapped step-by-step, including edge cases (nulls, empties, boundaries, error paths) and at least one integration-level test if the feature crosses layers.
3. Rollback note: how to abandon this feature cleanly (usually: revert the feature branch; call out any migration/config that would need manual undo).
4. Write `.workflow/<slug>/plan.md` with sections: Steps, Test plan, Rollback, Out of scope (explicitly cut items).

VALIDATION (gate to Phase 3): plan.md exists with all four sections; every step names files AND tests; no step > ~400 LOC estimate.
FALLBACK: a step cannot be planned at file level because of unknowns: insert a spike step whose deliverable is answering the unknown, with a hard timebox note, and re-plan subsequent steps after it during execution.

=== PHASE 3: TDD IMPLEMENTATION (artifact: green tests + commits) ===

For each plan step, strictly red-green-refactor:

1. RED: write the step's test(s) from the plan. Run them; they MUST fail, and fail for the expected reason:
   - Read the failure output, do not just check the exit code.
   - A test failing on an import error, typo, or fixture problem is NOT a valid red — fix the test until it fails on the missing behavior itself.
2. GREEN: write the minimal implementation to pass. Run the step's tests, then the full suite (baseline failures excluded).
3. REFACTOR: with tests green, clean the step's code (names, duplication, structure). Re-run tests.
4. COMMIT per green step: `feat(<scope>): <step summary> [workflow: <slug> step <n>/<total>]`. Include the test in the same commit.
5. If the plan proves wrong mid-step: update plan.md with a dated "Revision" note explaining the change BEFORE coding the new direction. The plan is living, but it is never silently divergent from reality.

VALIDATION (gate to Phase 4): all steps committed; full suite green vs baseline; plan.md's step list matches the commit list (including revisions).
FALLBACK: a step cannot go green after 3 honest attempts: revert that step's changes, mark it BLOCKED in plan.md with the failure evidence, cut it from scope if the feature is still coherent without it, otherwise stop and deliver the partial state honestly in the summary.

=== PHASE 4: SELF-REVIEW (artifact: review.md) ===

1. Diff the whole feature: `git diff <base>...HEAD`. Read it as a hostile reviewer.
2. Correctness pass:
   - Edge cases the tests missed (nulls, empties, boundaries, error paths).
   - Error propagation: swallowed exceptions, missing awaits, silent fallbacks.
   - Caller impact: grep callers of every modified function and verify each still behaves.
   - Concurrency, ordering, and off-by-one hazards.
     Fix what you find; each behavioral fix gets a test, committed as `fix:` referencing the review.
3. Simplification pass: duplication, dead code, over-abstraction introduced by the feature. Apply as `refactor:` commits, tests green after each.
4. Write `.workflow/<slug>/review.md`: findings table (finding, file:line, action taken), plus anything deliberately left (with reason).

VALIDATION (gate to Phase 5): review.md exists; suite green; every finding has a terminal action (fixed / accepted with reason).
FALLBACK: review finds an architectural mistake too big to fix in-run: record it as the top follow-up with a concrete remediation sketch; do not attempt a rushed rewrite.

=== PHASE 5: DELIVER ===

Print the summary (OUTPUT below) and leave the branch ready for a PR. Do not open a PR or merge unless the user asked.

=== OUTPUT ===

```
WORKFLOW COMPLETE — <feature-slug> on <branch>
Shipped: <2-3 sentences of what now works>
Steps: <n>/<planned> | Commits: <n> | Tests added: <n> | Suite: <p> passed (baseline <p0>)
Cut from scope: <list from plan.md Out of scope + any BLOCKED steps, or "nothing">
Follow-ups: <numbered, from review.md and revisions>
Artifacts: .workflow/<slug>/{brainstorm.md, plan.md, review.md}
```

=== SELF-REVIEW ===

Score 1-5: Complete (all three artifacts + commits exist and gates were honored in order), Robust (every commit had green tests; reds were verified reds), Clean (commits scoped per step, plan revisions documented). Any score < 4: repair now if possible; otherwise the gap goes in Follow-ups, top of the list.

=== LEARNINGS CAPTURE ===

Append to ~/.claude/skills/workflow-conductor/LEARNINGS.md: date + repo + feature, steps planned vs shipped, plan revisions count, where a gate caught a real problem, friction, suggested patch to this skill, verdict [Smooth/Minor friction/Major friction].

=== STRICT RULES ===

1. No stage without the prior stage's artifact on disk — memory of having "basically decided" does not open a gate.
2. A red test must fail for the expected reason; an import error or typo failure is not red.
3. One plan step, one commit (plus review-stage fix/refactor commits). Never bundle steps.
4. Plan divergence must be written to plan.md before the divergent code is written.
5. Never grow the baseline failure set; pre-existing failures are recorded, new ones are blockers.
6. Scope cuts are explicit — anything dropped appears in "Cut from scope", never silently omitted.
7. Do not open PRs, merge, or push unless the user asked for it.
