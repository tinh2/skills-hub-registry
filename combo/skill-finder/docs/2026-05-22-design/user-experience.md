# Design: User Experience

Part of [Skill Finder v2 Design Spec](../2026-05-22-skill-finder-v2-design.md). Section 3.

## 3.1 Invocation

```
/skill-finder
/skill-finder <task description>
/skill-finder resume
```

The first form auto detects the task from project state. The second uses the args directly. The third resumes the most recent unfinished plan if one exists.

## 3.2 Happy Path Session

```
> /skill-finder ship the auth flow branch

Detected task: "Ship the auth-flow branch end to end."
Project signals: 3 uncommitted files, 5 commits ahead of main, no PR open.

Proceed? (Y/edit/cancel)
> y

Planning workflow...

Workflow plan:
  1. [local]   /preflight     verify build, tests, migrations
  2. [local]   /pr            open PR with convention compliant title and body
  3. [install] /security-review  scan changed files for OWASP issues
  4. [local]   /verify        run the app and confirm the auth flow works

Plan saved to ./skill-finder-plans/2026-05-22-1342-ship-the-auth-flow.md

Install 1 missing skill and run? (Y/edit/no)
> y

Installing security-review-3 from skills hub...
  installed: ~/.claude/skills/security-review-3

Step 1 of 4: /preflight
  result: READY. Build green. Tests pass. No migrations pending.

Step 2 of 4: /pr
  result: PR #482 opened. https://github.com/example-org/example-repo/pull/482

Step 3 of 4: /security-review
  result: 0 high, 1 medium (rate limit on /login endpoint).

Step 4 of 4: /verify
  result: Login flow works in dev. MFA works. Logout works.

Chain complete. 4 of 4 steps succeeded.

Save this workflow as a reusable skill? (y/n/later)
> y

Skill name (default ship-auth-flow-pipeline):
> auth-ship

Description (default "Ship an auth flow end to end..."):
> [accept default]

Handing off to /skillify to publish...
  published: skills-hub.ai/skills/auth-ship v1.0.0

Next steps detected:
  1. PR #482 needs reviewers assigned.
     Run: gh pr edit 482 --add-reviewer @reviewer1,@reviewer2
  2. Medium severity finding from security review.
     Run: open .skill-finder-plans/2026-05-22-1342-ship-the-auth-flow.md to see details
```

## 3.3 Failure Path

A step fails. The orchestrator retries once. If the retry also fails, it pauses and asks the user.

```
Step 3 of 4: /security-review
  attempt 1 failed: tool error, MCP server timeout
  attempt 2 failed: same error

Pause options:
  r = retry once more
  s = skip and continue
  f = let me fix it manually, resume from step 4 when I'm ready
  a = abort the chain (plan saved for resume)
> s

Step 3 skipped. Continuing to step 4...
```
