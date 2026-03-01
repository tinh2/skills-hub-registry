---
name: devops
description: "Scan infrastructure gaps and orchestrate deployment readiness across CI/CD, containers, monitoring, and IaC"
version: "1.0.0"
category: deploy
platforms:
  - CLAUDE_CODE
---

You are in AUTONOMOUS MODE. Do NOT ask questions. Do NOT pause for confirmation.
Execute every phase below in sequence, making decisions based on what you find.

============================================================
PHASE 0 — INPUT
============================================================

$ARGUMENTS may contain:
- A specific sub-area to focus on: `ci`, `docker`, `k8s`, `monitoring`, `terraform`, `secrets`, `cdn`, `dns`
- `--report-only` — produce the readiness report without generating or modifying files
- `--fix` — attempt to fix all identified gaps by chaining sub-skills
- A target environment: `aws`, `gcp`, `azure`, `fly`, `vercel`
- If no arguments, default to `--report-only`

============================================================
PHASE 1 — INFRASTRUCTURE DISCOVERY
============================================================

Scan the entire project root for existing infrastructure artifacts. Check for:

1. **CI/CD**: `.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile`, `.circleci/`, `bitbucket-pipelines.yml`
2. **Containers**: `Dockerfile`, `docker-compose.yml`, `docker-compose.*.yml`, `.dockerignore`
3. **Kubernetes**: `k8s/`, `kubernetes/`, `helm/`, `charts/`, any `*.yaml` with `apiVersion: apps/`
4. **IaC**: `terraform/`, `*.tf`, `pulumi/`, `Pulumi.yaml`, `cdk/`, `cloudformation/`
5. **Monitoring**: `prometheus.yml`, `grafana/`, `datadog.yaml`, `.newrelic.yml`, `alertmanager.yml`
6. **Secrets**: `.env`, `.env.*`, `vault/`, `secrets/`, hardcoded API keys or tokens in source
7. **CDN**: `cdn/`, Cloudflare config (`wrangler.toml`), CloudFront references in Terraform
8. **DNS**: DNS records in Terraform, Cloudflare zone configs, Route53 references

Also detect the application stack:
- **Language**: Check `package.json`, `go.mod`, `Cargo.toml`, `requirements.txt`, `pyproject.toml`, `Gemfile`, `pubspec.yaml`, `pom.xml`, `build.gradle`
- **Framework**: Next.js, Fastify, Express, Django, Flask, FastAPI, Gin, Actix, Rails, Spring Boot, Flutter
- **Database**: Prisma schema, SQLAlchemy models, GORM, ActiveRecord, TypeORM

Store all findings in memory for scoring.

============================================================
PHASE 2 — READINESS SCORING
============================================================

Score each area on a 0-100 scale:

| Area | 0 | 25 | 50 | 75 | 100 |
|------|---|----|----|----|----|
| **CI/CD** | Nothing | Basic lint/test | PR checks + deploy | + caching + matrix | + security scan + preview deploys |
| **Containers** | Nothing | Dockerfile exists | + multi-stage | + compose + healthcheck | + non-root + .dockerignore + optimized layers |
| **Kubernetes** | Nothing | Basic deployment | + service + ingress | + HPA + probes | + PDB + resource limits + Helm |
| **IaC** | Nothing | Single resource | Modular structure | + remote state + envs | + cost tags + proper naming + outputs |
| **Monitoring** | Nothing | Basic logging | Metrics endpoint | + dashboards + alerts | + SLOs + distributed tracing |
| **Secrets** | Hardcoded values | .env files | Secrets manager | + rotation | + CI integration + audit trail |
| **CDN** | Nothing | Static hosting | CDN configured | + caching rules | + edge functions + invalidation |
| **DNS** | Nothing | Manual records | IaC-managed | + SSL + subdomains | + email DNS + health routing |

Calculate an overall **Deployment Readiness Score** as the weighted average:
- CI/CD: 25%
- Containers: 20%
- Monitoring: 15%
- IaC: 15%
- Secrets: 10%
- Kubernetes: 5% (0-weight if app is serverless/edge)
- CDN: 5%
- DNS: 5%

============================================================
PHASE 3 — GAP ANALYSIS
============================================================

For each area scoring below 50, generate a specific remediation plan:

1. What is missing
2. What sub-skill can fix it (reference: `deploy/github-actions`, `deploy/docker`, `deploy/k8s`, `deploy/monitoring`, `deploy/terraform`, `deploy/secrets`, `deploy/cdn`, `deploy/dns`)
3. Estimated effort (quick: <5 min, moderate: 5-15 min, significant: 15+ min)
4. Priority (critical, high, medium, low) based on:
   - **Critical**: No CI/CD, secrets in source code, no containerization for production app
   - **High**: No monitoring, no IaC for cloud resources, no health checks
   - **Medium**: Missing caching, no preview deploys, basic Kubernetes without HPA
   - **Low**: No CDN, no email DNS, no edge functions

============================================================
PHASE 4 — REMEDIATION (if --fix)
============================================================

If `--fix` was passed, execute remediations in priority order:

1. **Critical items first** — fix secrets exposure, add basic CI/CD
2. **High items next** — add Dockerfile, monitoring, IaC
3. **Medium items** — optimize CI caching, add HPA, preview deploys
4. **Low items** — CDN, DNS, edge functions

For each remediation, invoke the appropriate sub-skill pattern:
- Read the sub-skill's approach and apply it inline (do not shell out)
- After each fix, re-score that area
- Stop if cumulative changes exceed 20 new files (to avoid overwhelming a single PR)

============================================================
PHASE 5 — OUTPUT
============================================================

Generate a deployment readiness report. Print to stdout AND write to `DEPLOY_READINESS.md` in the project root.

```
## Deployment Readiness Report

**Project**: {detected project name}
**Stack**: {language} / {framework} / {database}
**Date**: {current date}
**Overall Score**: {score}/100

### Area Scores

| Area | Score | Status | Key Finding |
|------|-------|--------|-------------|
| CI/CD | XX | {emoji} | {one-line summary} |
| Containers | XX | {emoji} | {one-line summary} |
| Kubernetes | XX | {emoji} | {one-line summary} |
| IaC | XX | {emoji} | {one-line summary} |
| Monitoring | XX | {emoji} | {one-line summary} |
| Secrets | XX | {emoji} | {one-line summary} |
| CDN | XX | {emoji} | {one-line summary} |
| DNS | XX | {emoji} | {one-line summary} |

### Critical Gaps
{list of critical and high priority gaps}

### Recommended Actions
{ordered list of remediations with sub-skill references}

### Changes Made (if --fix)
{list of files created/modified}
```

============================================================
NEXT STEPS
============================================================

After generating the report, suggest:
1. Which sub-skill to run first if gaps exist
2. Whether the project is ready for production deployment
3. Any architectural concerns (e.g., no database backups, no rate limiting)

============================================================
DO NOT
============================================================

- Do NOT delete existing infrastructure files — only add or modify
- Do NOT commit changes — leave them staged for review
- Do NOT expose secrets in the report output
- Do NOT assume a cloud provider — detect or ask via $ARGUMENTS
- Do NOT generate Kubernetes manifests for projects that are clearly serverless/edge
- Do NOT modify application source code — only infrastructure files
- Do NOT install CLI tools or dependencies — work with what is available
