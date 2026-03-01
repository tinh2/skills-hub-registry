---
name: github-actions
description: "Auto-detect tech stack and generate production-grade GitHub Actions CI/CD workflows with caching and security scanning"
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
- A deploy target: `vercel`, `aws`, `gcp`, `fly`, `cloudflare`, `docker-registry`, `npm`, `pypi`
- A scope: `ci-only` (just PR checks), `cd-only` (just deploy), `full` (both — default)
- `--preview` — include preview deployment workflow for PRs
- `--matrix` — include matrix testing across multiple versions
- `--monorepo` — handle monorepo with path filters
- Specific workflow name to generate (e.g., `test`, `deploy`, `release`)

============================================================
PHASE 1 — STACK DETECTION
============================================================

Detect the project stack by scanning for manifest files:

**Node.js / TypeScript**:
- `package.json` — read scripts (`test`, `build`, `lint`, `typecheck`, `start`)
- Lock file: `package-lock.json` (npm), `yarn.lock` (yarn), `pnpm-lock.yaml` (pnpm)
- Framework: check dependencies for `next`, `nuxt`, `remix`, `astro`, `fastify`, `express`, `nestjs`
- `tsconfig.json` — TypeScript project

**Python**:
- `requirements.txt`, `pyproject.toml`, `setup.py`, `Pipfile`
- Framework: `django`, `flask`, `fastapi`, `starlette`
- Tool: `poetry`, `pip`, `pipenv`, `uv`

**Go**:
- `go.mod` — read module name and Go version
- Check for `cmd/` directory structure

**Rust**:
- `Cargo.toml` — read workspace members if monorepo

**Flutter / Dart**:
- `pubspec.yaml` — read dependencies, check for `flutter_test`

**Docker**:
- `Dockerfile` — if exists, prefer Docker-based CI steps

Record: language, package manager, framework, test command, build command, lint command.

============================================================
PHASE 2 — GENERATE PR CHECK WORKFLOW
============================================================

Create `.github/workflows/ci.yml`:

```yaml
name: CI
on:
  pull_request:
    branches: [main, master]
  push:
    branches: [main, master]
```

Include these jobs in order:

**1. Lint & Format**
- Node: `npm run lint` / `eslint .` / `prettier --check .`
- Python: `ruff check .` / `black --check .` / `mypy .`
- Go: `golangci-lint run`
- Rust: `cargo clippy -- -D warnings` / `cargo fmt --check`

**2. Type Check** (if applicable)
- Node/TS: `tsc --noEmit` or `npm run typecheck`
- Python: `mypy .` or `pyright`

**3. Test**
- Node: `npm test` with coverage (`--coverage`)
- Python: `pytest --cov` or `python -m pytest`
- Go: `go test ./... -race -coverprofile=coverage.out`
- Rust: `cargo test`
- Flutter: `flutter test --coverage`

**4. Build**
- Node: `npm run build`
- Go: `go build ./...`
- Rust: `cargo build --release`
- Flutter: `flutter build apk --debug` (or web)
- Docker: `docker build .` (if Dockerfile exists)

**5. Security Scan**
- Always include: `actions/dependency-review-action@v4` on PRs
- Node: `npm audit --audit-level=high`
- Python: `pip-audit` or `safety check`
- Go: `govulncheck ./...`
- Rust: `cargo audit`

**Caching** — always include appropriate caching:
- Node: `actions/cache@v4` for `node_modules` or use `actions/setup-node@v4` with `cache: 'npm'`
- Python: `actions/setup-python@v5` with `cache: 'pip'`
- Go: `actions/setup-go@v5` with `cache: true`
- Rust: `Swatinem/rust-cache@v2`
- Flutter: `subosito/flutter-action@v2` with `cache: true`

**Matrix testing** (if `--matrix`):
- Node: test against LTS and current (e.g., `[18, 20, 22]`)
- Python: `[3.10, 3.11, 3.12]`
- Go: last two minor versions
- OS matrix: `[ubuntu-latest]` default, add `macos-latest` if Flutter/mobile

============================================================
PHASE 3 — GENERATE DEPLOY WORKFLOW
============================================================

Create `.github/workflows/deploy.yml` based on deploy target:

**Vercel**:
- Use `amondnet/vercel-action@v25` or Vercel CLI
- Production deploy on push to main
- Preview deploy on PR (if `--preview`)

**AWS (ECS/ECR)**:
- `aws-actions/configure-aws-credentials@v4`
- `aws-actions/amazon-ecr-login@v2`
- Build, tag, push Docker image
- Update ECS service with new task definition

**AWS (S3 + CloudFront)**:
- Sync build output to S3
- Invalidate CloudFront distribution

**GCP (Cloud Run)**:
- `google-github-actions/auth@v2`
- `google-github-actions/deploy-cloudrun@v2`
- Build with Cloud Build or Docker

**Fly.io**:
- `superfly/flyctl-actions/setup-flyctl@master`
- `flyctl deploy --remote-only`

**Cloudflare (Pages/Workers)**:
- `cloudflare/wrangler-action@v3`

**Docker Registry (GHCR)**:
- `docker/login-action@v3` with `registry: ghcr.io`
- `docker/build-push-action@v5` with layer caching
- Tag with SHA and `latest`

**npm / PyPI**:
- Publish on release tag creation
- npm: `npm publish` with `NODE_AUTH_TOKEN`
- PyPI: `pypa/gh-action-pypi-publish@release/v1`

Include environment protection rules reference:
```yaml
environment:
  name: production
  url: ${{ steps.deploy.outputs.url }}
```

============================================================
PHASE 4 — GENERATE ADDITIONAL WORKFLOWS
============================================================

If applicable, also create:

**Release workflow** (`.github/workflows/release.yml`):
- Triggered on tag push (`v*`)
- Create GitHub Release with changelog
- Build and attach artifacts

**Scheduled workflows**:
- Dependency updates: `schedule: cron: '0 6 * * 1'` (weekly Monday 6am)
- Security scan: if not in CI, run nightly

**Preview deploy** (if `--preview`):
- Comment on PR with preview URL
- Clean up preview on PR close

============================================================
PHASE 5 — SECRETS DOCUMENTATION
============================================================

Create or update `.github/SECRETS.md` listing all required repository secrets:

```
## Required Secrets

| Secret | Description | Where to get it |
|--------|-------------|-----------------|
| DEPLOY_TOKEN | Vercel/Fly/etc deploy token | {provider dashboard URL} |
```

Also create `.github/dependabot.yml` if it does not exist:
```yaml
version: 2
updates:
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
```

============================================================
OUTPUT
============================================================

Print a summary of all generated files:

```
## GitHub Actions Setup Complete

### Files Created
- .github/workflows/ci.yml — PR checks (lint, typecheck, test, build, security)
- .github/workflows/deploy.yml — Deploy to {target} on push to main
- .github/dependabot.yml — Automated dependency updates

### Required Secrets
{list of secrets to configure in GitHub repo settings}

### Detected Stack
- Language: {language}
- Framework: {framework}
- Package Manager: {pm}
- Deploy Target: {target}
```

============================================================
NEXT STEPS
============================================================

1. Add required secrets to GitHub repository settings
2. Push workflows to trigger the first run
3. Consider adding branch protection rules requiring CI to pass
4. Review caching strategy after first run to verify cache hits

============================================================
DO NOT
============================================================

- Do NOT use deprecated actions (e.g., `actions/checkout@v2` — use `v4`)
- Do NOT hardcode secrets — always use `${{ secrets.NAME }}`
- Do NOT use `actions/setup-node@v3` — use `v4`
- Do NOT skip the security scanning step
- Do NOT use `ubuntu-20.04` — use `ubuntu-latest` or `ubuntu-24.04`
- Do NOT add `permissions: write-all` — use minimal permissions per job
- Do NOT generate workflows for stacks not detected in the project
- Do NOT overwrite existing workflow files without reading them first and preserving custom steps
- Do NOT use `npm ci` without checking that `package-lock.json` exists (use `npm install` if no lock file)
