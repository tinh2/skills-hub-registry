# Pattern: security-harden

Run a security review and fix any high severity findings.

## Trigger Phrases

* security audit
* harden security
* fix security issues
* security review
* check for vulnerabilities
* OWASP scan

## Required Steps

1. **security-review.** Skill: `security-review-3`. Purpose: scan for OWASP top issues.
2. **bugfix.** Skill: `bugfix`. Purpose: fix any high severity findings.

## Optional Steps

3. **pr.** Skill: `pr-7`. Include when fixes were applied.
4. **verify.** Skill: `verify`. Include when the auth or session flow was touched.

## Handoff Notes

* security-review to bugfix: pass each high severity finding as a separate fix task.
