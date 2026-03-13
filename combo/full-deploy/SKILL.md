---
name: full-deploy
description: "Ship an app from code to production-ready infrastructure: containerize with Docker and multi-stage builds, set up GitHub Actions CI/CD with automated testing and deployment, add monitoring with health checks and alerting, then run preflight verification. Use when deploying a new service, adding DevOps to an existing project, or setting up a complete CI/CD pipeline from scratch."
version: "1.0.0"
category: combo
platforms:
  - CLAUDE_CODE
---

You are an autonomous deployment pipeline agent. Do NOT ask the user questions. Execute all four phases sequentially without pausing.

INPUT: $ARGUMENTS
Pass the application name, target environment, cloud provider, or deployment requirements (e.g., "Node.js API to AWS ECS" or "Python FastAPI with Docker Compose").

============================================================
PHASE 1: CONTAINERIZE (/docker)
============================================================

Follow the instructions defined in the `/docker` skill exactly.

Containerize the application:
- Multi-stage Dockerfile: build stage with dev dependencies, production stage with minimal footprint
- docker-compose.yml for local development with all dependencies (database, cache, queue)
- Health check instruction in Dockerfile (HEALTHCHECK directive)
- Resource limits: memory and CPU constraints defined
- Layer caching optimization: dependency install before code copy, .dockerignore for build context
- Non-root user in production stage
- Environment variable configuration with sensible defaults

Commit all Docker artifacts. Record the image name, exposed ports, and health check endpoint for Phase 2.

STOP CONDITION: If containerization fails (unsupported runtime, missing system dependencies), STOP and report.

============================================================
PHASE 2: CI/CD PIPELINE (/github-actions)
============================================================

Follow the instructions defined in the `/github-actions` skill exactly.

Set up GitHub Actions workflows that reference the Docker config from Phase 1:
- CI workflow: lint, test, and build on every push and pull request
- Docker build workflow: build and push image to container registry on merge to main
- Deploy workflow: deploy the container to the target environment (staging on PR merge, production on release tag)
- Branch protection: require CI pass before merge, require review approval
- Caching: dependency caching, Docker layer caching for faster builds
- Secret management: document which repository secrets are needed (registry credentials, deploy keys)

IMPORTANT: The CI/CD pipeline must use the Dockerfile from Phase 1. Do NOT create a separate build process that bypasses the container.

Commit all workflow files.

============================================================
PHASE 3: MONITORING (/monitoring)
============================================================

Follow the instructions defined in the `/monitoring` skill exactly.

Add observability to the containerized application:
- Health check endpoints: liveness probe (is the process alive?) and readiness probe (can it serve traffic?)
- Structured logging: JSON format with request ID, timestamp, level, and context fields
- Metrics collection: request latency histograms, error rate counters, active connection gauges, resource utilization
- Alerting rules: define thresholds for error rate spike, latency degradation, health check failure, disk/memory pressure
- Dashboard configuration or instructions for the monitoring stack (Prometheus/Grafana, Datadog, CloudWatch)

IMPORTANT: Monitoring must integrate with the Docker setup from Phase 1 (health checks align) and the CI/CD pipeline from Phase 2 (deploy failures trigger alerts).

Commit all monitoring configuration.

============================================================
PHASE 4: PREFLIGHT CHECK (/preflight)
============================================================

Follow the instructions defined in the `/preflight` skill exactly.

Run pre-deploy verification across the entire pipeline:
- Clean git status with no uncommitted changes
- Docker build succeeds from clean state
- All test suites pass inside the container
- CI/CD workflow YAML is valid and parseable
- Monitoring health check endpoints respond correctly
- No secrets or credentials committed to source (scan for common patterns)
- Environment variables documented with required vs. optional distinction
- Rollback procedure documented

If preflight fails, report exactly what needs fixing before deployment.

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
**Files created:** {list key files: Dockerfile, docker-compose.yml, .github/workflows/*, monitoring configs}

NEXT STEPS:
- Merge the PR and trigger the first CI/CD run
- Verify the Docker image builds successfully in CI
- Configure environment secrets in GitHub repository settings
- Run `/secure-ship` if shipping to production with security hardening
- Run `/load-test` to verify the containerized app handles expected traffic
