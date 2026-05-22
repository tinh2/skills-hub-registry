# Handoff Protocol

The structured data passed from step N to step N+1. The orchestrator builds this object after every step succeeds and writes it into the plan file under the `## Handoffs` section.

## Why a Protocol

Chained skills often fail not because they are broken but because the next skill in the chain does not get the context it needs. A pr skill that does not know the changed files. A verify skill that does not know which user flow was modified. The handoff protocol guarantees that each skill receives a consistent shape of context, so the chain composes cleanly.

## The Four Fields

Every handoff has exactly four fields. Keep them small. The orchestrator is the one passing this forward as a prompt prefix, not a 50 page dossier.

### 1. output_artifacts

Files, URLs, PR numbers, branch names, or other named outputs that the step produced. Always a list, even if empty.

Examples:

* `["docs/auth-flow-spec.md"]` after a spec step.
* `["#482", "https://github.com/example-org/example-repo/pull/482"]` after a pr step.
* `["src/auth/login.ts", "src/auth/session.ts"]` after a build step.
* `[]` for steps that produce no addressable artifact, like a verify step that just observes.

### 2. git_delta

A one line summary of the working tree change since the prior step. Format: `<N files modified>, <M files added>, <K files deleted>`.

Examples:

* `3 files modified, 1 file added, 0 files deleted`
* `0 files changed` for a read only step.
* `5 files modified, 0 files added, 2 files deleted (refactor)` with a parenthetical tag when useful.

The orchestrator computes this by running `git status --short` before and after the step and diffing the result.

### 3. summary

One to three sentences describing what the step did. Written in past tense. Avoid jargon the next skill might not understand. Include the outcome, not the method.

Examples:

* "Spec produced. Covers the login, MFA, and logout flows. Saved to docs/auth-flow-spec.md."
* "PR #482 opened. Title: 'feat: auth flow rewrite'. Body includes summary and test plan."
* "Security review completed. 0 high severity, 1 medium severity (rate limit on /login)."

### 4. open_items

A list of unresolved items the step flagged but did not finish. The next skill or the user may need to address these. Always a list.

Examples:

* `["PR needs reviewers", "Medium severity finding from security review"]`
* `["2 tests still red", "1 type error in build output"]`
* `[]` when the step completed cleanly with no open items.

## JSON Shape

The orchestrator builds this object after each step:

```json
{
  "step": 2,
  "skill": "pr-7",
  "output_artifacts": ["#482", "https://github.com/example-org/example-repo/pull/482"],
  "git_delta": "0 files changed",
  "summary": "PR #482 opened. Title from branch name. Body includes summary and test plan.",
  "open_items": ["PR needs reviewers assigned"]
}
```

## How It Gets Passed Forward

The orchestrator turns the handoff into a prompt prefix for the next skill. The format is:

```
Context from prior step:

  Step <N>: <skill name>
  Outcome: <summary>
  Artifacts: <comma list of output_artifacts>
  Git delta: <git_delta>
  Open items: <comma list of open_items>

Original task: <task statement>

Your job: <step purpose from plan file>
```

Example actual prompt prefix when invoking `/security-review` after a `/pr` step:

```
Context from prior step:

  Step 2: pr-7
  Outcome: PR #482 opened. Title from branch name. Body includes summary and test plan.
  Artifacts: #482, https://github.com/example-org/example-repo/pull/482
  Git delta: 0 files changed
  Open items: PR needs reviewers assigned

Original task: Ship the auth-flow branch end to end.

Your job: scan changed files for OWASP issues.
```

The target skill does not need to parse JSON. It reads the prefix as natural language context. The structured form is for the orchestrator's bookkeeping in the plan file.

## Where It Gets Written

Two places:

1. **Plan file `## Handoffs` section.** Append the JSON or the rendered version after each step. This is the audit trail.
2. **Next skill invocation.** The prompt prefix above.

Both stay in sync. The plan file is canonical. The invocation is derived from it.

## What Not to Include

Keep handoffs small. Do not include:

* Full file contents. Pass the path instead.
* Full diff output. Pass the file list and a one line summary.
* Full error messages. Pass the one line classification and any specific guidance.
* Prior step handoffs from N minus 2 or earlier. Only the immediately prior step's handoff is passed forward.

If a downstream skill needs more, it can read the plan file itself. The plan file path is always available in the original task context.

## Failure Handoffs

If a step fails and is skipped via the `s` pause option, the handoff written to the plan file is:

```json
{
  "step": 3,
  "skill": "security-review-3",
  "output_artifacts": [],
  "git_delta": "0 files changed",
  "summary": "Step failed twice and was skipped by user.",
  "open_items": ["Security review was not completed and should be run manually before merge"]
}
```

The next step still receives this handoff. Skipped steps surface as open items so the chain stays honest.
