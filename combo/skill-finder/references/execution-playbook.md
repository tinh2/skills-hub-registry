# Execution Playbook

The playbook the orchestrator follows during Phase 4 (Execute) for every step in the approved plan.

## Per Step Run Loop

For each step in the plan, run this loop:

1. **Build context.** Pull in:
   * The task statement from the plan file.
   * The handoff notes from the previous step (see `handoff-protocol.md`).
   * Any user provided args from the original invocation.
   * The current step's purpose line from the plan file.
2. **Invoke.** Call the target skill via the Skill tool with the built context as the prompt.
3. **Capture.** Save the raw tool result and any artifacts it produced.
4. **Classify.** Apply the success or failure rules below.
5. **Update plan.** Mark the step as `✓`, `✗`, or `⟳` in the plan file. Append the outcome and the handoff notes for the next step.
6. **Move on.** Continue to the next step, or trigger retry, or pause.

## Success and Failure Classification

A step is **success** when:

* The skill returned without an error.
* The post conditions hold. Post conditions are inferred from the step's label:
  * `spec` label: a spec file was created or updated.
  * `build` label: git diff shows changes in source files.
  * `test` label: tests ran and exited green.
  * `review` label: the review completed and produced a report.
  * `fix` label: the named bug or finding is no longer reproducible.
  * `pr` label: a PR was opened or updated and a URL was returned.
  * `verify` label: the user facing flow worked.
  * `deploy` label: the deploy command completed without error.
  * `audit` label: the audit completed and produced a report.
  * `document` label: a doc file was created or updated.
  * `polish` label: the polish pass completed without error.

A step is **failure** when:

* The skill errored out.
* The skill returned a clear failure signal (text contains "failed", "error", "NOT READY", "blocked").
* The post conditions do not hold.
* The skill produced no observable output and no artifacts.

A step is **ambiguous** when:

* The skill returned but the post conditions cannot be verified.
* The output text is silent on success or failure.

For ambiguous cases, do not silently mark as success. Ask the user with this prompt:

```
Step N of M: <skill name>
The skill returned but I could not verify success.

Output:
  <short excerpt, max 200 chars>

Mark as: success, failure, or skip? (s/f/k)
```

## Retry Policy

On classified failure, retry exactly once automatically. The retry uses a refined context that adds:

* A diagnostic line: "Attempt 1 failed. Reason: <classified reason>".
* The original task statement and the prior handoff notes, unchanged.
* Any specific guidance the skill returned (for example, a missing dependency).

Mark the step as `⟳` in the plan file during the retry attempt.

If the retry succeeds, mark as `✓` and proceed normally. The plan file should show: "Step succeeded on attempt 2."

If the retry also fails, do not retry again. Pause the chain.

## Pause Prompt Template

When a step fails twice, pause and prompt the user with this exact format:

```
Step N of M failed twice: <skill name>
  Attempt 1: <one line diagnostic>
  Attempt 2: <one line diagnostic>

Options:
  r = retry once more with extra context
  s = skip this step and continue
  f = let me fix it manually, resume from step N+1 when I'm ready
  a = abort the chain (plan saved for resume)
```

User responses:

* `r`: build context with even more detail. Add a request for the user's hypothesis if any. Retry. If this attempt also fails, do not auto pause again. Mark as failure and continue.
* `s`: mark step as `skipped` in the plan file. Continue to next step. The plan completion status becomes `partial`.
* `f`: mark step as `manual` in the plan file. Exit Phase 4. Tell the user to run `/skill-finder resume` when ready.
* `a`: mark step as `aborted` in the plan file. Mark plan status as `aborted`. Skip Phase 5 and 6.

## Ad Hoc Decomposition

When no pattern from `workflow-patterns.md` matches the user's task, derive steps directly. Use these rules:

1. Identify the verbs in the task statement. Common verbs map to step labels:
   * write, draft, document: `document`
   * design, build, implement, create: `build`
   * test, verify, check: `test` or `verify`
   * review, audit: `review` or `audit`
   * fix, debug, solve: `fix`
   * ship, deploy, publish, release: `deploy`
   * polish, clean, refine: `polish`
2. For each verb, create a step using the matching label.
3. Look up a default skill for each label:
   * `document`: prefer `readme` or `skills-hub-registry-engineering-spec`.
   * `build`: prefer `skills-hub-registry-story-implementer` or `feature`.
   * `test`: prefer `unit-test-2`.
   * `verify`: prefer `verify`.
   * `review`: prefer `code-review`.
   * `audit`: prefer `audit`.
   * `fix`: prefer `bugfix`.
   * `deploy`: prefer `pr-7` then `deploy-dev-api`.
   * `polish`: prefer `design-polish` or `polish`.
4. If the ad hoc derivation produces fewer than 2 steps, ask the user to clarify the task. Do not run a one step chain. That is not a workflow.
5. If the ad hoc derivation produces more than 6 steps, ask the user to confirm or trim before proceeding.

## Resume Protocol

If `/skill-finder` is invoked with `resume` as the only argument:

1. List all files in `./skill-finder-plans/` with status `in progress`, `partial`, `aborted`, or `manual`.
2. Sort by most recent.
3. If exactly one matches the current project (by working directory or git remote), offer to resume it.
4. If multiple match, list them and ask which one. Prompt:

```
Multiple unfinished plans found:
  1. 2026 05 22 13:42 ship the auth flow (step 3 of 4)
  2. 2026 05 21 09:15 audit and ship (step 2 of 4)

Resume which one? (1, 2, or n=none)
```

5. When the user picks one, jump directly to Phase 4 at the first step that is not marked `✓`. Skip Phases 1, 2, 3. The plan is already approved.
6. If the user picks `none`, exit cleanly.

## Plan File Updates

The plan file is the canonical record. Update it after every step. Use the structure shown in section 4.3 of the design spec.

When updating:

1. Read the existing plan file.
2. Modify only the rows that changed.
3. Append to the Decisions log with a timestamp and a one line note.
4. Write the file back.

Never delete a plan file. Plans are append only history.

## Install Step

If the plan has `install` source steps, run them all before any execute steps. One at a time:

1. Call `install_skill` with the catalog slug.
2. Report the install path.
3. If install fails, ask the user to skip the step or abort the chain.

Once installs complete, the plan transitions to execute. Do not interleave installs with executes.
