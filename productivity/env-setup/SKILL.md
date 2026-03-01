---
name: env-setup
description: "Detect required tools, install dependencies, configure environment, and verify the project builds and tests pass from zero"
version: "1.0.0"
category: productivity
platforms:
  - CLAUDE_CODE
---

You are in AUTONOMOUS MODE. Do NOT ask questions. Do NOT pause for confirmation.
Execute every phase below in sequence, making decisions based on what you find.

============================================================
PHASE 0 — INPUT
============================================================

$ARGUMENTS may contain:
- `--check-only` — verify environment without installing or modifying anything
- `--skip-db` — skip database setup and migration steps
- `--skip-tests` — skip the final test verification step
- `--reset` — tear down existing environment and rebuild from scratch (docker-compose down -v, rm -rf node_modules, etc.)

If no arguments, run the full setup: detect, install, configure, verify.

============================================================
PHASE 1 — DETECT REQUIRED TOOLS
============================================================

Scan project files to build a requirements list:

**Runtime Detection**:
- `package.json` → Node.js (version from `engines.node` or `.nvmrc` or `.node-version`, default 20)
- `pyproject.toml` / `requirements.txt` → Python (version from `requires-python` or `.python-version`, default 3.12)
- `go.mod` → Go (version from `go` directive)
- `Cargo.toml` → Rust (stable channel)
- `pubspec.yaml` → Flutter (version from `environment.flutter`)
- `Gemfile` → Ruby (version from `.ruby-version`)

**Tool Detection**:
- `docker-compose.yml` → Docker + Docker Compose required
- `Dockerfile` → Docker required
- `prisma/schema.prisma` → Prisma CLI required
- `Makefile` → make required
- `Taskfile.yml` → go-task required
- `turbo.json` → Turborepo required (global or local)
- `.terraform/` → Terraform required
- `serverless.yml` → Serverless Framework required

**Package Manager Detection**:
- `package-lock.json` → npm
- `yarn.lock` → yarn
- `pnpm-lock.yaml` → pnpm
- `bun.lockb` → bun
- `poetry.lock` → poetry
- `Pipfile.lock` → pipenv
- `uv.lock` → uv
- `go.sum` → go modules (built-in)
- `Cargo.lock` → cargo (built-in)

Build the full requirements list with expected versions.

============================================================
PHASE 2 — CHECK INSTALLED VERSIONS
============================================================

For each required tool, check if it is installed and the version matches:

```
node --version        → compare against required
npm --version         → verify package manager
python3 --version     → compare against required
go version            → compare against required
rustc --version       → verify installed
flutter --version     → compare against required
docker --version      → verify installed
docker compose version → verify installed
```

Produce a status table:

| Tool | Required | Installed | Status |
|------|----------|-----------|--------|
| node | 20.x     | 20.11.0   | OK     |
| pnpm | 9.x      | not found | MISSING|

For MISSING tools:
- Detect the OS and package manager (macOS/brew, Linux/apt, etc.)
- Provide install commands but DO NOT run system-level installs automatically
- Exception: Node version managers (nvm, fnm), Python version managers (pyenv), and Rust (rustup) — these are safe to suggest running

For VERSION MISMATCH:
- Report the mismatch and suggest upgrade commands
- If using a version manager (.nvmrc exists), suggest `nvm use` or `fnm use`

If `--check-only`, stop here and report the status table. Do not proceed to install.

============================================================
PHASE 3 — INSTALL DEPENDENCIES
============================================================

Install project dependencies using the detected package manager:

**Node.js**:
- npm: `npm install` (or `npm ci` if `package-lock.json` exists and is not in CI)
- yarn: `yarn install`
- pnpm: `pnpm install`
- bun: `bun install`

**Python**:
- pip: `pip install -r requirements.txt` (create venv first if not in one: `python3 -m venv .venv && source .venv/bin/activate`)
- poetry: `poetry install`
- uv: `uv sync`
- pipenv: `pipenv install --dev`

**Go**: `go mod download`

**Rust**: `cargo fetch`

**Flutter**: `flutter pub get`

**Ruby**: `bundle install`

For monorepos, run install from the root. If workspace installs are needed, detect and run those too.

Verify install succeeded (exit code 0). If it fails, read the error and attempt to resolve:
- Missing peer dependencies → install them
- Engine mismatch → report and suggest fix
- Native build failures → report required system libraries

============================================================
PHASE 4 — CONFIGURE ENVIRONMENT
============================================================

**4.1 — Environment Variables**

If `.env.example` or `.env.template` exists and `.env` does not:
1. Copy: `cp .env.example .env`
2. Scan the template for variables that need values:
   - `DATABASE_URL` → construct from docker-compose service config or use default: `postgresql://postgres:postgres@localhost:5432/app_dev`
   - `REDIS_URL` → `redis://localhost:6379`
   - `JWT_SECRET` / `SECRET_KEY` → generate a random 64-char hex string using `openssl rand -hex 32`
   - `PORT` → keep the default from template
   - `NODE_ENV` / `ENVIRONMENT` → set to `development`
   - `API_KEY` / `THIRD_PARTY_*` → leave as placeholder with comment: `# TODO: add your key`
3. Write the populated `.env` file

If no `.env.example` exists but the project clearly needs env vars (detected from code scanning for `process.env`, `os.environ`, `os.Getenv`), create a `.env.example` with discovered variables and sensible defaults.

**4.2 — Database Setup**

Skip if `--skip-db`.

If `docker-compose.yml` exists with database services:
1. Start services: `docker compose up -d`
2. Wait for database to be ready (poll with connection check, max 30 seconds)
3. Run migrations:
   - Prisma: `npx prisma migrate dev` or `npx prisma db push`
   - Django: `python manage.py migrate`
   - Alembic: `alembic upgrade head`
   - Goose: `goose up`
   - Knex: `npx knex migrate:latest`
   - Rails: `rails db:migrate`
4. Run seed if available:
   - Prisma: `npx prisma db seed` (if seed script defined in package.json)
   - Django: `python manage.py loaddata`
   - Custom: check for `scripts/seed.*` or `db/seed.*`

If no docker-compose.yml but database is needed:
- Generate a minimal `docker-compose.yml` with the required database service
- Then proceed with the steps above

**4.3 — Additional Setup**

- If `Makefile` exists with a `setup` or `init` target: run `make setup` or `make init`
- If `scripts/setup.sh` exists: run `bash scripts/setup.sh`
- If `Taskfile.yml` exists with a `setup` task: run `task setup`
- If Prisma is detected: run `npx prisma generate` to generate the client
- If Husky is detected: run `npx husky install` or `npx husky` (v9+)
- If pre-commit is detected: run `pre-commit install`

============================================================
PHASE 5 — VERIFY BUILD AND TESTS
============================================================

Run verification checks to confirm the project is ready for development:

**5.1 — Build Check**:
- Node/TS: `npm run build` or `npx tsc --noEmit` (whichever is in scripts)
- Python: `python -c "import {main_package}"` (verify imports work)
- Go: `go build ./...`
- Rust: `cargo build`
- Flutter: `flutter analyze`

**5.2 — Test Check** (skip if `--skip-tests`):
- Node: `npm test` (or `npx vitest run` / `npx jest`)
- Python: `pytest` or `python -m pytest`
- Go: `go test ./...`
- Rust: `cargo test`
- Flutter: `flutter test`

**5.3 — Dev Server Check** (non-blocking):
- If a `dev` or `start:dev` script exists, verify it starts without immediate crash
- Start the server, wait 5 seconds, check it responds on the expected port, then stop it

Report results for each check: PASS / FAIL with error details.

============================================================
OUTPUT
============================================================

Print the setup summary:

```
## Environment Setup Complete

### System Requirements
| Tool   | Required | Installed | Status  |
|--------|----------|-----------|---------|
| node   | 20.x     | 20.11.0   | OK      |
| docker | any      | 27.1.1    | OK      |
| ...

### Dependencies
- {package manager}: {N} packages installed

### Environment
- .env: created from .env.example with {N} variables populated
- Database: {PostgreSQL 16 running on localhost:5432}
- Migrations: {applied N migrations}
- Seed data: {loaded / not available}

### Verification
- Build: PASS
- Tests: PASS ({N} tests, {N} passed)
- Dev server: PASS (responding on localhost:{port})

### Manual Steps Required
- {any tools that need manual install}
- {any API keys that need manual configuration}
```

============================================================
NEXT STEPS
============================================================

1. Start developing: `npm run dev` / `python manage.py runserver` / `go run .`
2. Run `/git-hooks` to set up pre-commit hooks
3. Run `/devcontainer` to containerize this setup for team consistency
4. Share `.env.example` with the team (never commit `.env`)

============================================================
DO NOT
============================================================

- Do NOT install system packages without explicit user instruction (no `brew install`, `apt install`)
- Do NOT commit `.env` files — ensure `.env` is in `.gitignore`
- Do NOT use production database credentials — always use local development defaults
- Do NOT run `docker compose down -v` unless `--reset` was explicitly passed
- Do NOT modify existing `.env` files — only create new ones from templates
- Do NOT skip the verification phase — the whole point is confirming everything works
- Do NOT hardcode absolute paths — use relative paths and environment variables
- Do NOT run migrations against non-local databases
- Do NOT generate secrets that are less than 32 bytes — use `openssl rand -hex 32` minimum
