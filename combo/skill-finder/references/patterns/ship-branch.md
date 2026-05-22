# Pattern: ship-branch

Ship a feature branch end to end. Verify, open the PR, optionally security review, optionally verify in dev.

## Trigger Phrases

* ship the branch
* ship this branch
* ship the feature branch
* ship to production
* deploy this branch
* finalize the branch
* land the branch
* close out the branch

## Required Steps

1. **preflight.** Skill: `preflight-8`. Purpose: verify build, tests, migrations, and commit conventions. Gate before opening PR.
2. **pr.** Skill: `pr-7`. Purpose: open a convention compliant pull request with summary and test plan.

## Optional Steps

Include only if the project state suggests they apply.

3. **security-review.** Skill: `security-review-3`. Include when the diff touches auth, sessions, payments, file uploads, or API routes.
4. **verify.** Skill: `verify`. Include when the change is user facing and observable in a dev environment.
5. **deploy-dev-api.** Skill: `deploy-dev-api`. Include when the user mentioned a project-specific dev instance in the task (any environment name the project configures, such as dev, staging, qa).

## Handoff Notes

* preflight to pr: pass the READY or NOT READY signal. If NOT READY, stop the chain in execute phase.
* pr to security-review: pass the PR number and the list of changed files.
* security-review to verify: pass the high or medium findings so verify can spot check them.
