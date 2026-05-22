# Pattern: fix-bug

Root cause and fix a bug with regression coverage.

## Trigger Phrases

* fix the bug
* fix this bug
* debug and fix
* root cause and fix
* squash the bug
* solve the issue
* fix the broken
* fix the failing

## Required Steps

1. **debug.** Skill: `superpowers:systematic-debugging`. Purpose: produce a root cause hypothesis backed by evidence.
2. **bugfix.** Skill: `bugfix`. Purpose: implement the fix, write a regression test, and verify.
3. **pr.** Skill: `pr-7`. Purpose: open the PR with the bug and fix described.

## Optional Steps

4. **verify.** Skill: `verify`. Include when the bug is observable in a dev environment.

## Handoff Notes

* debug to bugfix: pass the root cause statement and the file or function locations identified.
* bugfix to pr: pass the diff summary and the regression test path.
