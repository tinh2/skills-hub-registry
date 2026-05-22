# Next Steps Detectors

Phase 6 scans the project for follow ups and surfaces them as a short ordered list of suggested slash commands. Each detector is a small probe that returns zero or one suggestion.

## Detector Format

Each detector has:

* **Name.** Short label.
* **Probe.** The shell command or check that runs.
* **Trigger condition.** What probe output means "yes, suggest something".
* **Suggestion.** The text shown to the user.
* **Severity.** `blocker`, `important`, or `convenience`.

## Severity Ordering

The Phase 6 list is sorted by severity:

1. **Blockers.** Things that must happen before the work is shippable. Failing tests, broken builds, unresolved high severity security findings.
2. **Important.** Things that need to happen soon. Unpushed commits, PR without reviewers, missing PR description sections.
3. **Conveniences.** Optional improvements. Clean up the plan file, run a polish pass, update docs.

Cap the list at 5 entries. If more than 5 detect, keep the 5 highest severity.

## Detectors

### Detector: uncommitted_changes

* **Probe.** `git status --porcelain | wc -l`
* **Trigger condition.** Output greater than zero.
* **Suggestion.** "N uncommitted files in the working tree. Commit or stash before declaring done."
* **Severity.** Important.

### Detector: unpushed_commits

* **Probe.** `git log @{u}..HEAD --oneline 2>/dev/null | wc -l`
* **Trigger condition.** Output greater than zero.
* **Suggestion.** "N commits unpushed on branch <branch>. Run: git push"
* **Severity.** Important.

### Detector: pr_no_reviewers

* **Probe.** `gh pr view --json reviewRequests,number 2>/dev/null`
* **Trigger condition.** PR exists, reviewRequests is empty.
* **Suggestion.** "PR #<number> has no reviewers. Run: gh pr edit <number> --add-reviewer <handle>"
* **Severity.** Important.

### Detector: pr_open_but_not_ready

* **Probe.** `gh pr view --json isDraft,statusCheckRollup 2>/dev/null`
* **Trigger condition.** PR is draft or checks are failing.
* **Suggestion.** "PR #<number> is draft or has failing checks. Resolve before merge."
* **Severity.** Blocker.

### Detector: failing_tests

* **Probe.** Inspect the chain's most recent test step output. If absent, skip.
* **Trigger condition.** Test step finished with red.
* **Suggestion.** "Tests failing from step <N>. Run: <project specific test command>"
* **Severity.** Blocker.

### Detector: high_severity_security

* **Probe.** Inspect the chain's most recent security-review step output. If absent, skip.
* **Trigger condition.** Output mentions 1 or more high severity findings.
* **Suggestion.** "<N> high severity security findings. Run: /bugfix to address them."
* **Severity.** Blocker.

### Detector: preflight_not_run

* **Probe.** Check the chain's executed steps. If preflight was not run and the project has a CLAUDE.md mentioning preflight as a convention, suggest it.
* **Trigger condition.** Preflight not in the chain, project convention says to run it.
* **Suggestion.** "Preflight not run. Run: /preflight to verify before deploy."
* **Severity.** Important.

### Detector: claude_md_convention

* **Probe.** Read CLAUDE.md for any line matching `Always run /X before Y` or `Run /X after Z`.
* **Trigger condition.** A convention referenced a slash command that was not run in the chain.
* **Suggestion.** "CLAUDE.md says to run /<command> <when>. Not in the chain. Run: /<command>"
* **Severity.** Important.

### Detector: stale_plan_files

* **Probe.** `ls ./skill-finder-plans/ | head -20`. Count files older than 30 days.
* **Trigger condition.** More than 5 stale plan files.
* **Suggestion.** "<N> plan files older than 30 days. Run: rm ./skill-finder-plans/*-<old-month>-*.md"
* **Severity.** Convenience.

### Detector: open_items_remain

* **Probe.** Read the just completed plan file. Collect all `open_items` from all step handoffs.
* **Trigger condition.** One or more open items.
* **Suggestion.** "Open items from the chain: <bullet list>. Address before declaring done."
* **Severity.** Important.

### Detector: deploy_target_mentioned

* **Probe.** Check the task statement for words `deploy`, `ship`, `production`, or any project-specific dev instance name (e.g. dev, staging, qa, or named environments configured by the project).
* **Trigger condition.** The task mentioned deploy or a target but no deploy step ran.
* **Suggestion.** "Task mentioned <target> but no deploy step ran. Run: /deploy-dev-api <target> or /preflight first."
* **Severity.** Important.

### Detector: docs_stale

* **Probe.** Check the chain's git_delta entries. If source files changed but no docs files changed, suggest a docs pass.
* **Trigger condition.** Source diff present, doc diff absent.
* **Suggestion.** "Source changed but docs did not. Run: /readme or /documentation-writer to update."
* **Severity.** Convenience.

### Detector: polish_pending

* **Probe.** Check whether the chain ran a build or design step but no polish step.
* **Trigger condition.** build or design step succeeded, polish step absent.
* **Suggestion.** "Build done but no polish pass. Run: /design-polish for a final QA pass."
* **Severity.** Convenience.

## Output Format

Render the detected items as a numbered list. Each line shows the suggestion plus the runnable command. Do not auto run. The user is the one who decides.

```
Next steps detected:
  1. <blocker suggestion>
     Run: <command>
  2. <important suggestion>
     Run: <command>
  3. <convenience suggestion>
     Run: <command>

Pick one, or say "stop" to end the session.
```

If zero detectors fire, render:

```
Next steps: none detected. The chain wrapped cleanly.
```

## How to Add a Detector

Append a new section using the format above. The orchestrator iterates through every detector in this file. Keep probes cheap. If a probe is expensive, gate it behind a cheap check first.
