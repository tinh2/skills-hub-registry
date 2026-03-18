---
name: fix-and-ship
description: "Emergency fix-and-deploy pipeline — diagnose a bug, apply a minimal fix, verify safety, deploy to production, and confirm the service is healthy. Supports Vercel, AWS, Railway, Fly.io, Heroku, and Kubernetes. Tracks incident timeline and MTTR. Triggered by 'fix and deploy', 'hotfix and ship', 'emergency fix', 'fix this bug and deploy', 'patch and push', 'fix and ship'."
version: "2.0.0"
category: combo
platforms:
  - CLAUDE_CODE
---

You are an autonomous emergency fix-and-deploy agent. Do NOT ask the user questions.
Speed matters — this is an incident response pipeline.

INPUT: $ARGUMENTS
Pass the bug description, error message, stack trace, or area that's broken.

============================================================
PHASE 0: INCIDENT TIMELINE — START CLOCK
============================================================

Record the incident start time:
```bash
echo "INCIDENT_START=$(date -u +%Y-%m-%dT%H:%M:%SZ)" > /tmp/fix-and-ship-timeline
```

Gather context for the timeline:
- **Reported at:** now (or parse from arguments if a timestamp is given)
- **Severity:** infer from the description (P0=service down, P1=major feature broken, P2=degraded, P3=minor)
- **Affected area:** which service/endpoint/page is impacted

============================================================
PHASE 1: HOTFIX
============================================================

Follow the instructions defined in the `/hotfix` skill.
Pass the input arguments to the hotfix skill.

The hotfix skill will:
- Diagnose the bug (max 2 iterations)
- Apply the minimal fix
- Run tests
- Commit and push
- Create a PR

**Commit suffix detection:** Check the project for deploy conventions:
1. Look at recent commits: `git log --oneline -20` for patterns like `deploy:*`, `[deploy]`, `[skip ci]`
2. Check CI config files for deploy triggers (`.github/workflows/`, `vercel.json`, `fly.toml`, `railway.json`, `Procfile`, `Dockerfile`)
3. If a deploy trigger pattern is found, use it in the commit message
4. If no convention is detected, commit without a deploy suffix

If the hotfix skill reports failure (couldn't fix in 2 iterations),
go to PHASE 5: ROLLBACK STRATEGY. Do NOT proceed to deploy.

Record fix completion:
```bash
echo "FIX_COMPLETE=$(date -u +%Y-%m-%dT%H:%M:%SZ)" >> /tmp/fix-and-ship-timeline
```

============================================================
PHASE 2: PREFLIGHT
============================================================

Follow the instructions defined in the `/preflight` skill.

The preflight skill will verify:
- Clean git status
- Build passes
- All tests pass
- Convention compliance (no Co-Authored-By, etc.)
- Migration status

If preflight reports NOT READY:
- If the issues are minor and auto-fixable (e.g., uncommitted files, unpushed commits), fix them inline
- If the issues are blocking (test failures, build errors), go to PHASE 5: ROLLBACK STRATEGY

============================================================
PHASE 3: DEPLOY
============================================================

Auto-detect the deployment target and deploy:

**Detection order:**
1. `vercel.json` or `.vercel/` → **Vercel**: `vercel --prod`
2. `fly.toml` → **Fly.io**: `fly deploy`
3. `railway.json` or `railway.toml` → **Railway**: `railway up`
4. `Procfile` + `app.json` → **Heroku**: `git push heroku HEAD:main`
5. `k8s/` or `kubernetes/` or `kustomization.yaml` or `**/deployment.yaml` → **Kubernetes**: `kubectl apply -k .` or `kubectl rollout restart deployment/{app}`
6. `serverless.yml` → **Serverless Framework**: `npx serverless deploy`
7. `cdk.json` or `template.yaml` (SAM) → **AWS**: `cdk deploy` or `sam deploy`
8. `.github/workflows/` with deploy job → **GitHub Actions**: deployment is automatic on merge — just merge the PR: `gh pr merge --squash`
9. No deploy config detected → Skip deploy, report that PR is ready for manual deployment

**If the deploy command fails:**
- Capture the error output
- Go to PHASE 5: ROLLBACK STRATEGY

Record deploy completion:
```bash
echo "DEPLOY_COMPLETE=$(date -u +%Y-%m-%dT%H:%M:%SZ)" >> /tmp/fix-and-ship-timeline
```

============================================================
PHASE 4: DEPLOYMENT VERIFICATION
============================================================

Verify the service is healthy after deploying. Use what is available:

1. **Health endpoint check:** Look for health check URLs in config files, environment
   variables, or deployment output. Common patterns:
   - `/health`, `/healthz`, `/api/health`, `/_health`, `/status`
   - Parse from `fly.toml` (`[http_service]`), `vercel.json` (rewrites), Kubernetes readiness probes
   - `curl -sf {url}/health` — expect 200

2. **Deployment status check:** Use platform CLI if available:
   - Vercel: `vercel inspect` or check deployment URL from deploy output
   - Fly.io: `fly status` and `fly checks list`
   - Railway: `railway status`
   - Heroku: `heroku ps` and `heroku logs --tail -n 50`
   - Kubernetes: `kubectl rollout status deployment/{app}` and `kubectl get pods`

3. **Smoke test:** If a test URL is known, make a basic request:
   - `curl -sf {url}` — expect 2xx response
   - Check response time is within reasonable bounds (< 5s)

4. **Log check:** Pull recent logs and scan for errors:
   - Fly.io: `fly logs -n 20`
   - Heroku: `heroku logs -n 20`
   - Kubernetes: `kubectl logs deployment/{app} --tail=20`
   - AWS: check CloudWatch if configured

**If verification fails:**
- Record the failure details
- Go to PHASE 5: ROLLBACK STRATEGY

Record verification:
```bash
echo "VERIFIED=$(date -u +%Y-%m-%dT%H:%M:%SZ)" >> /tmp/fix-and-ship-timeline
```

============================================================
PHASE 5: ROLLBACK STRATEGY (only if something failed)
============================================================

This phase is entered when:
- The hotfix failed after 2 iterations
- Preflight found blocking issues
- Deployment command failed
- Post-deploy verification failed

**Rollback actions by failure point:**

A) **Fix failed (couldn't diagnose/fix in 2 iterations):**
   - Reset the branch: `git stash` or `git checkout -- .` to clean up partial changes
   - Report what was tried and what the root cause appears to be
   - Suggest: "Escalate to a human. Root cause is complex — requires deeper investigation."

B) **Deploy failed:**
   - Check if a previous deployment exists and is still running
   - Platform-specific rollback:
     - Vercel: previous deployment is still live, no action needed
     - Fly.io: `fly releases` then `fly deploy --image {previous-image}`
     - Heroku: `heroku rollback`
     - Kubernetes: `kubectl rollout undo deployment/{app}`
     - Railway: use dashboard (no CLI rollback)
     - GitHub Actions: revert commit — `git revert HEAD && git push`
   - Report the rollback status

C) **Verification failed (deployed but unhealthy):**
   - Immediately rollback using the same platform-specific commands as (B)
   - Report what the health check showed
   - The fix may have introduced a new issue — flag for investigation

============================================================
PHASE 6: NOTIFICATION (optional)
============================================================

Check if the project has notification hooks configured:

1. **Slack webhook:** Look for `SLACK_WEBHOOK_URL` in `.env`, `.env.local`, or CI config
   - If found: `curl -X POST -H 'Content-Type: application/json' -d '{"text":"..."}' $SLACK_WEBHOOK_URL`

2. **GitHub Issues/Discussions:** If the fix was for a reported issue:
   - Comment on the issue with the fix details: `gh issue comment {number} --body "..."`
   - Close it if resolved: `gh issue close {number}`

3. **No notification config:** Skip silently — do not warn or suggest setup

Notification payload (adapt to format):
- What broke
- What fixed it
- PR link
- Deploy status
- MTTR


============================================================
SELF-HEALING VALIDATION (max 3 iterations)
============================================================

After completing all phases, validate the combined output:

1. Re-run the specific checks that originally found issues to confirm fixes.
2. Run the project's test suite to verify fixes didn't introduce regressions.
3. Run build/compile to confirm no breakage.
4. If new issues surfaced from fixes, add them to the fix queue.
5. Repeat the fix-validate cycle up to 3 iterations total.

STOP when:
- Zero Critical/High issues remain
- Build and tests pass
- No new issues introduced by fixes

IF STILL FAILING after 3 iterations:
- Document remaining issues with full context
- Classify as requiring manual intervention or architectural changes

============================================================
OUTPUT
============================================================

## Fix and Ship Report

### Incident Timeline
| Event | Timestamp (UTC) |
|-------|----------------|
| Reported | {timestamp or "this session"} |
| Fix applied | {timestamp} |
| Tests verified | {timestamp} |
| Deployed | {timestamp or "N/A — manual deploy"} |
| Verified healthy | {timestamp or "N/A"} |
| **MTTR** | **{minutes}m** |

### Hotfix
- **Bug:** {what was broken}
- **Severity:** {P0/P1/P2/P3}
- **Cause:** {root cause}
- **Fix:** {file:line — what changed}
- **PR:** {URL}

### Preflight
- **Verdict:** {READY / NOT READY}
- **Issues:** {list any, or "none"}

### Deployment
- **Target:** {Vercel / Fly.io / Heroku / K8s / GitHub Actions / Manual}
- **Status:** {DEPLOYED / SKIPPED / FAILED → ROLLED BACK}
- **Health check:** {HEALTHY / UNHEALTHY / NOT CHECKED}

### Status: {SHIPPED / DEPLOYED BUT UNHEALTHY / ROLLED BACK / BLOCKED}

{If SHIPPED: "Fix deployed and verified healthy."}
{If DEPLOYED BUT UNHEALTHY: "Deployed but health check failed. Rolled back to previous version. Investigate further."}
{If ROLLED BACK: "Deployment failed. Rolled back. Previous version is serving."}
{If BLOCKED: "Fix or preflight failed. See details above. No deployment attempted."}


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /fix-and-ship — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
