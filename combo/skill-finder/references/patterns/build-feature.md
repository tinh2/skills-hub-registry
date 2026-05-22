# Pattern: build-feature

Build a feature from spec to PR.

## Trigger Phrases

* build the feature
* implement the feature
* build this feature
* add the feature
* ship a new feature
* implement the spec
* implement the story
* build from spec

## Required Steps

1. **spec.** Skill: `spec` or `skills-hub-registry-engineering-spec`. Purpose: produce a clear engineering spec. Skip if a spec already exists in the conversation or as a file.
2. **build.** Skill: `skills-hub-registry-story-implementer` or `feature`. Purpose: implement the spec, write tests, follow repo conventions.
3. **review.** Skill: `code-review`. Purpose: scan the diff for correctness bugs.
4. **pr.** Skill: `pr-7`. Purpose: open the PR.

## Optional Steps

5. **unit-test.** Skill: `unit-test-2`. Include when the implementation lacks tests or test coverage dropped.
6. **verify.** Skill: `verify`. Include when the change is user facing.

## Handoff Notes

* spec to build: pass the spec file path.
* build to review: pass the changed files list from `git diff`.
* review to pr: pass the review findings so the PR body can flag known issues.
