---
name: devcontainer
description: "Auto-detect stack and generate a production-grade dev container configuration with Codespaces compatibility"
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
- `--compose` — force Docker Compose-based setup even for single-service projects
- `--minimal` — generate a lightweight config without extras (no extensions, no features)
- A base image override (e.g., `mcr.microsoft.com/devcontainers/python:3.12`)

If no arguments, auto-detect everything and generate a full-featured config.

============================================================
PHASE 1 — STACK DETECTION
============================================================

Detect the project stack by scanning for manifest files:

**Language & Runtime**:
- `package.json` → Node.js (read `engines.node` for version, default 20)
- `tsconfig.json` → TypeScript project
- `pyproject.toml` / `requirements.txt` / `Pipfile` → Python (read `requires-python`, default 3.12)
- `go.mod` → Go (read `go` directive for version)
- `Cargo.toml` → Rust
- `pubspec.yaml` → Flutter/Dart
- `Gemfile` → Ruby (read `.ruby-version` for version)

**Services**:
- `docker-compose.yml` / `docker-compose.*.yml` → existing services to integrate
- `prisma/schema.prisma` → read `provider` for database type (postgresql, mysql, sqlite, mongodb)
- `.env.example` → scan for `DATABASE_URL`, `REDIS_URL`, `MONGO_URI` patterns
- `pyproject.toml` → check for `sqlalchemy`, `django` with database backends

**Package Manager**:
- `package-lock.json` (npm), `yarn.lock` (yarn), `pnpm-lock.yaml` (pnpm), `bun.lockb` (bun)
- `poetry.lock` (poetry), `Pipfile.lock` (pipenv), `uv.lock` (uv)

Record: language, version, framework, package manager, required services (database, cache, queue).

============================================================
PHASE 2 — GENERATE DEVCONTAINER CONFIG
============================================================

Create `.devcontainer/devcontainer.json`:

**Base Image Selection** (use Microsoft Dev Container images):
- Node.js: `mcr.microsoft.com/devcontainers/javascript-node:{version}`
- TypeScript: `mcr.microsoft.com/devcontainers/typescript-node:{version}`
- Python: `mcr.microsoft.com/devcontainers/python:{version}`
- Go: `mcr.microsoft.com/devcontainers/go:{version}`
- Rust: `mcr.microsoft.com/devcontainers/rust:latest`
- Ruby: `mcr.microsoft.com/devcontainers/ruby:{version}`
- Universal (polyglot): `mcr.microsoft.com/devcontainers/universal:2`

**Dev Container Features** (add based on detected stack):
- Docker-in-Docker: `ghcr.io/devcontainers/features/docker-in-docker:2` (if Dockerfile exists)
- GitHub CLI: `ghcr.io/devcontainers/features/github-cli:1`
- Common utilities: `ghcr.io/devcontainers/features/common-utils:2`
- Node.js (if secondary): `ghcr.io/devcontainers/features/node:1`
- Python (if secondary): `ghcr.io/devcontainers/features/python:1`
- AWS CLI: `ghcr.io/devcontainers/features/aws-cli:1` (if AWS config detected)

**VS Code Extensions** (match detected stack):
- Node/TS: `dbaeumer.vscode-eslint`, `esbenp.prettier-vscode`, `ms-vscode.vscode-typescript-next`
- Python: `ms-python.python`, `ms-python.vscode-pylance`, `charliermarsh.ruff`
- Go: `golang.go`
- Rust: `rust-lang.rust-analyzer`
- Flutter: `Dart-Code.dart-code`, `Dart-Code.flutter`
- Common: `eamodio.gitlens`, `EditorConfig.EditorConfig`, `usernamehw.errorlens`
- Database: `mtxr.sqltools` + appropriate driver extension
- Docker: `ms-azuretools.vscode-docker`

**Port Forwarding** (detect from project):
- Read `docker-compose.yml` for exposed ports
- Read `.env.example` for `PORT`, `API_PORT`, `DB_PORT` variables
- Common defaults: 3000 (Node API), 5432 (PostgreSQL), 6379 (Redis), 8000 (Python), 8080 (Go), 27017 (MongoDB)

**Post-Create Command**:
- Node (npm): `npm install`
- Node (pnpm): `pnpm install`
- Node (yarn): `yarn install`
- Python (pip): `pip install -r requirements.txt`
- Python (poetry): `poetry install`
- Python (uv): `uv sync`
- Go: `go mod download`
- Rust: `cargo fetch`
- Flutter: `flutter pub get`
- If database migrations exist, chain: `&& npx prisma migrate dev` or equivalent

============================================================
PHASE 3 — MULTI-SERVICE SETUP
============================================================

If the project requires services (database, cache, queue) OR `--compose` was passed:

Create `.devcontainer/docker-compose.yml`:

```yaml
services:
  app:
    build:
      context: ..
      dockerfile: .devcontainer/Dockerfile
    volumes:
      - ..:/workspaces/${localWorkspaceFolderBasename}:cached
    command: sleep infinity
```

Add detected services:
- **PostgreSQL**: `postgres:16-alpine` with `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`, volume for data persistence
- **MySQL**: `mysql:8` with equivalent config
- **MongoDB**: `mongo:7` with init script volume
- **Redis**: `redis:7-alpine` with persistence config
- **RabbitMQ**: `rabbitmq:3-management-alpine` with management UI port

Create `.devcontainer/Dockerfile` using the detected base image with any additional tooling.

Update `devcontainer.json` to reference docker-compose:
```json
{
  "dockerComposeFile": "docker-compose.yml",
  "service": "app",
  "workspaceFolder": "/workspaces/${localWorkspaceFolderBasename}"
}
```

If no services are needed, use the simpler `image` or `build` approach directly in `devcontainer.json`.

============================================================
PHASE 4 — CODESPACES COMPATIBILITY
============================================================

Ensure GitHub Codespaces compatibility:

- Set `"hostRequirements"` if the project needs more than the default 2-core machine:
  - Projects with Docker-in-Docker or large builds: `"cpus": 4`
  - AI/ML projects: `"cpus": 4, "memory": "8gb"`
- Add `"codespaces"` section if needed for prebuild configuration
- Ensure all paths use `${localWorkspaceFolderBasename}` not hardcoded names
- Add `.devcontainer/devcontainer.json` to `.gitattributes` as `linguist-generated` if the file does not exist

Verify the generated config is valid JSON (no trailing commas, proper escaping).

============================================================
OUTPUT
============================================================

Print a summary of all generated files:

```
## Dev Container Setup Complete

### Files Created
- .devcontainer/devcontainer.json — main configuration
- .devcontainer/docker-compose.yml — multi-service orchestration (if applicable)
- .devcontainer/Dockerfile — custom image (if applicable)

### Detected Stack
- Language: {language} {version}
- Framework: {framework}
- Package Manager: {pm}
- Services: {postgresql, redis, etc. or "none"}

### Included Extensions
- {list of VS Code extensions}

### Port Forwarding
- {port}: {service description}

### Post-Create Setup
- {command that runs after container creation}
```

============================================================
NEXT STEPS
============================================================

1. Open the project in VS Code and select "Reopen in Container"
2. Or push to GitHub and open in Codespaces
3. Run `/env-setup` to verify all dependencies and services are working
4. Run `/git-hooks` to set up pre-commit hooks inside the container

============================================================
DO NOT
============================================================

- Do NOT use deprecated base images (e.g., `vscode/devcontainers` — use `mcr.microsoft.com/devcontainers`)
- Do NOT hardcode secrets or passwords in devcontainer.json — use `.env` files or Codespaces secrets
- Do NOT include production databases — dev containers are for local development only
- Do NOT add extensions for stacks not detected in the project
- Do NOT overwrite an existing `.devcontainer/devcontainer.json` without reading it first and preserving custom settings
- Do NOT use `root` as the container user unless absolutely necessary — prefer the default dev container user
- Do NOT skip port forwarding for detected services — developers expect ports to be accessible
