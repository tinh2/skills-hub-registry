# Design: The Six Phases (Specified)

Part of [Skill Finder v2 Design Spec](../2026-05-22-skill-finder-v2-design.md). Section 5.

## Phase 1: Understand Task

**Inputs:** $ARGS (optional), project working directory.

**Outputs:** A one line task statement, confirmed by user.

**Steps:**

1. If `$ARGS` is non empty and not the word `resume`, treat args as the task. Skip to confirmation.
2. If `$ARGS` is `resume`, look for the most recent file in `./skill-finder-plans/` with status not equal to "complete". If found, ask: "Resume <task> from step N? (Y/n)". If yes, jump to Phase 4 at the unfinished step.
3. Otherwise, run auto detection:
   * Read `CLAUDE.md` if present.
   * Read `TODO.md` or any file matching `TODO*` if present.
   * Run `git log -10 --oneline`.
   * Run `git status --short`.
   * Run `gh pr view --json title,state,number 2>/dev/null` to check current branch's PR.
4. Synthesize a one line task statement from the signals. Prefer the most recent commit subject or the open PR title. Add a clause about uncommitted changes or unpushed commits if relevant.
5. Show the task plus the signals used, and ask: "Proceed? (Y/edit/cancel)".

**Confirmation prompt format:**

```
Detected task: "<one-line task>"
Project signals: <comma list of signals>

Proceed? (Y/edit/cancel)
```

If user picks edit, accept a freeform replacement and re confirm once.

## Phase 2: Discover and Decompose

**Inputs:** Confirmed task statement.

**Outputs:** An ordered list of (step_name, skill_slug, source) tuples where source is `local` or `install`.

**Steps:**

1. Call `list_installed_skills` to get the local catalog.
2. Try to match the task to a pattern from `references/workflow-patterns.md`. Match is fuzzy: trigger phrases plus signal weights. A pattern matches if the task has 60 percent or more keyword overlap with one of its trigger phrases.
3. If a pattern matches, load `references/patterns/<name>.md` and use its required steps. Add optional steps based on project state signals.
4. If no pattern matches, derive ad hoc steps from the task using reasoning. Each ad hoc step gets one of these labels: spec, build, test, review, fix, deploy, document, audit, polish. Use the label to look up a default skill.
5. For each step, check if the chosen skill is in the local catalog. If yes, mark source as `local`. If no, call `search_skills` and `get_skill_detail` to pick the best catalog match. Mark source as `install`.
6. If a step has no good match in either place, mark the slug as `none` and present it as a "no skill found" gap in the plan.

## Phase 3: Plan

**Inputs:** Ordered step list from Phase 2.

**Outputs:** A plan file on disk plus a rendered plan shown to the user.

**Steps:**

1. Create `./skill-finder-plans/` if it does not exist.
2. Write the plan file with the format defined in [architecture.md section 4.3](architecture.md). Status starts as "draft".
3. Render the plan to the user. Flag `install` rows with a download icon and `none` rows with a warning icon.
4. Ask: "Install N missing skills and run? (Y/edit/no)".
5. On `edit`, accept either a freeform new ordering or a "remove step N" instruction. Re render and re ask.
6. On `Y`, mark plan status as "approved" and move to Phase 4.

## Phase 4: Execute

**Inputs:** Approved plan file.

**Outputs:** Plan file updated with per step outcomes.

**Steps:**

1. For each `install` step, call `install_skill` one at a time. Report each. If install fails, ask the user whether to skip this step or abort.
2. For each step in order:
   a. Build context for the invocation. Pull in the task statement, the prior step's handoff notes, and any user provided args. See `references/handoff-protocol.md`.
   b. Invoke the skill via the Skill tool with that context.
   c. Capture the result.
   d. Classify as success or failure using the rules in `references/execution-playbook.md`.
   e. If failure, retry once with a refined context that includes the failure diagnostic. Mark the step as `⟳` in the plan file during the retry.
   f. If retry also fails, pause and prompt as shown in [user-experience.md section 3.3](user-experience.md).
   g. On success, update the plan file with the outcome and the handoff notes. Continue to next step.
3. When all steps are processed, mark plan status as "complete" if all succeeded, "partial" if any were skipped, or "aborted" if the user bailed.

## Phase 5: Save As Skill

**Inputs:** Completed plan file.

**Outputs:** A new SKILL.md handed to `skills-hub-registry-skillify` for publish, or nothing if the user declines.

**Hard rule.** Skill Finder NEVER creates the skill itself. The only path is invoking skillify.

**Steps:**

1. Ask: "Save this workflow as a reusable skill? (y/n/later)".
2. On `later`, write a marker in the plan file and exit phase. Next time `/skill-finder` runs a similar task, the orchestrator will reoffer.
3. On `n`, exit phase.
4. On `y`:
   a. Default the skill name to a kebab case derived from the task slug plus the suffix `-pipeline`. Confirm or edit.
   b. Default the description to a templated summary. Confirm or edit.
   c. Read `references/save-as-skill-template.md` and fill in the slots.
   d. Run the validation checklist from `save-as-skill-template.md`.
   e. Invoke skillify via the Skill tool. Pass the filled SKILL.md body plus the structured metadata.
   f. Capture skillify's response. Report the published URL or the error verbatim.

## Phase 6: Next Steps

**Inputs:** Completed or partial plan file, current project state.

**Outputs:** A short ordered list of suggested slash commands.

**Steps:**

1. Run the detectors from `references/next-steps-detectors.md`. Each detector returns zero or one suggestion.
2. Order the suggestions by severity (blockers first, conveniences last).
3. Print the top 5 as a numbered list with the runnable command for each. Do not auto run anything.
4. Exit the skill.
