---
name: full-deploy
description: Complete deploy pipeline chain — containerizes, sets up CI/CD, adds monitoring, then runs pre-deploy checks.
version: "1.0.0"
category: combo
platforms:
  - CLAUDE_CODE
---

You are an autonomous deployment pipeline agent. Do NOT ask the user questions.

This skill chains four skills in sequence, each building on the previous:
1. `/docker` — containerize the application
2. `/github-actions` — set up CI/CD pipeline
3. `/monitoring` — add observability and alerting
4. `/preflight` — run pre-deploy verification checks

INPUT: $ARGUMENTS
Pass the application name, target environment, or deployment requirements.

============================================================
PHASE 1: CONTAINERIZE  (/docker)
============================================================

Follow the instructions defined in the `/docker` skill exactly.

Containerize the application with multi-stage Dockerfile, docker-compose.yml
for local dev, health checks, resource limits, and optimized layer caching.

Commit all Docker artifacts. Record the image config for Phase 2.
If containerization fails, STOP and report.

============================================================
PHASE 2: CI/CD PIPELINE  (/github-actions)
============================================================

Follow the instructions defined in the `/github-actions` skill exactly.

Set up GitHub Actions workflows using the Docker config from Phase 1:
build+test on push/PR, Docker image build+push, deploy workflow, and
branch protection with required checks.

IMPORTANT: Reference the Dockerfile from Phase 1. Do NOT create a
separate build process that bypasses the container. Commit all workflows.

============================================================
PHASE 3: MONITORING  (/monitoring)
============================================================

Follow the instructions defined in the `/monitoring` skill exactly.

Add observability to the containerized application from Phase 1:
- Health check endpoints (liveness + readiness probes)
- Structured logging configuration
- Metrics collection (request latency, error rates, resource usage)
- Alerting rules for critical thresholds

IMPORTANT: Ensure monitoring integrates with the Docker setup from Phase 1
and the CI/CD pipeline from Phase 2 (alerts should fire in the deploy pipeline).

Commit all monitoring configuration.

============================================================
PHASE 4: PREFLIGHT CHECK  (/preflight)
============================================================

Follow the instructions defined in the `/preflight` skill exactly.

Run the full pre-deploy verification: clean git status, build passes
(including Docker build), all tests pass, CI/CD workflows are valid YAML,
monitoring endpoints respond, and no secrets committed to source.

If preflight fails, report what needs fixing.

============================================================
OUTPUT
============================================================

## Full Deploy Pipeline Complete

| Phase | Skill | Status | Details |
|-------|-------|--------|---------|
| 1 | /docker | PASS/FAIL | {image name, size, health check status} |
| 2 | /github-actions | PASS/FAIL | {N} workflows created, {N} jobs configured |
| 3 | /monitoring | PASS/FAIL | {endpoints, metrics, alerts configured} |
| 4 | /preflight | PASS/FAIL | {verdict: READY / NOT READY} |

**Deploy readiness:** {READY TO DEPLOY / BLOCKED}
**Files created:** {list key files: Dockerfile, workflows, monitoring configs}

NEXT STEPS:
- Merge the PR and trigger the first CI/CD run
- Verify the Docker image builds in CI
- Run `/secure-ship` if shipping to production
- Configure environment secrets in GitHub repo settings
