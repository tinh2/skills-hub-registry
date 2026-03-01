---
name: docker
description: "Auto-detect stack and generate optimized multi-stage Dockerfiles with compose, health checks, and security hardening"
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
- `--compose` — also generate docker-compose.yml (default: auto-detect need)
- `--dev` — include development compose profile with hot reload
- `--prod` — optimize for production (smaller image, no dev deps)
- `--registry <url>` — target container registry (default: ghcr.io)
- A specific service name to Dockerize (for monorepos)
- `--slim` — use Alpine/distroless base images for minimal size

If no arguments, generate both Dockerfile and docker-compose.yml if the project has dependencies (database, cache, etc.).

============================================================
PHASE 1 — STACK DETECTION
============================================================

Detect the application stack:

**Node.js**:
- Read `package.json` for: `engines.node`, `scripts.start`, `scripts.build`, framework
- Lock file determines package manager: `package-lock.json` (npm), `yarn.lock` (yarn), `pnpm-lock.yaml` (pnpm)
- Framework detection: Next.js (`next.config.*`), Fastify, Express, NestJS, Remix, Astro
- Check for `tsconfig.json` — TypeScript build step needed

**Python**:
- Read `pyproject.toml`, `requirements.txt`, `Pipfile`, `setup.py`
- Framework: Django (`manage.py`), Flask, FastAPI (`uvicorn`/`gunicorn`)
- Python version from `.python-version`, `pyproject.toml`, or `runtime.txt`

**Go**:
- Read `go.mod` for module name and Go version
- Check for `cmd/main.go` or `main.go` entry point
- Static binary — ideal for scratch/distroless final stage

**Rust**:
- Read `Cargo.toml` for binary name
- Static binary with musl target — ideal for scratch/distroless

**Java**:
- Read `pom.xml` (Maven) or `build.gradle` (Gradle)
- Check for Spring Boot, Quarkus, Micronaut
- JRE-only final stage

**Ruby**:
- Read `Gemfile` for Ruby version and framework (Rails, Sinatra)
- Check for `config.ru` (Rack app)

Also detect dependencies:
- **Database**: Prisma schema (`prisma/schema.prisma`), SQLAlchemy, GORM, ActiveRecord, TypeORM — note the DB engine (postgres, mysql, sqlite)
- **Cache**: Redis references in config/code
- **Message queue**: RabbitMQ, Kafka references
- **Search**: Elasticsearch references
- **Object storage**: S3/MinIO references

============================================================
PHASE 2 — GENERATE DOCKERFILE
============================================================

Create a multi-stage `Dockerfile` following these principles:

**Stage 1 — Dependencies** (`deps` or `builder`):
- Use specific version tags, never `latest` (e.g., `node:22-alpine`, `python:3.12-slim`)
- Install only production dependencies first (layer caching optimization)
- Copy lock file BEFORE source code

**Stage 2 — Build** (if applicable):
- Copy source code
- Run build command (`npm run build`, `go build`, `cargo build --release`)
- For compiled languages, produce a static binary if possible

**Stage 3 — Production**:
- Use smallest appropriate base image:
  - Node.js: `node:22-alpine` (or `distroless` if `--slim`)
  - Python: `python:3.12-slim`
  - Go: `gcr.io/distroless/static-debian12` or `scratch`
  - Rust: `gcr.io/distroless/cc-debian12` or `scratch`
  - Java: `eclipse-temurin:21-jre-alpine`
  - Ruby: `ruby:3.3-slim`
- Copy only built artifacts and production deps from previous stages
- Set `WORKDIR /app`

**Security hardening** (always apply):
```dockerfile
# Create non-root user
RUN addgroup --system --gid 1001 appgroup && \
    adduser --system --uid 1001 --ingroup appgroup appuser
USER appuser
```

**Health check** (always include):
```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD [health check command appropriate to stack]
```
- Node.js: `wget --no-verbose --tries=1 --spider http://localhost:${PORT}/health || exit 1`
- Python: `curl -f http://localhost:${PORT}/health || exit 1`
- Go: built-in health endpoint check
- For apps without a health endpoint, use `CMD ["true"]` as minimal check

**Labels** (OCI standard):
```dockerfile
LABEL org.opencontainers.image.source="https://github.com/OWNER/REPO"
LABEL org.opencontainers.image.description="Description"
```

**Environment**:
```dockerfile
ENV NODE_ENV=production
ENV PORT=3000
EXPOSE ${PORT}
```

============================================================
PHASE 3 — GENERATE .dockerignore
============================================================

Create `.dockerignore` to minimize build context:

```
node_modules
.git
.github
.env
.env.*
*.md
.vscode
.idea
coverage
.nyc_output
dist
.next
__pycache__
*.pyc
.pytest_cache
target/debug
tmp
logs
```

Adjust based on detected stack. Always exclude:
- `.git` directory
- IDE config (`.vscode`, `.idea`)
- Test coverage output
- Environment files (`.env*`)
- Build artifacts that will be regenerated

============================================================
PHASE 4 — GENERATE DOCKER COMPOSE
============================================================

Create `docker-compose.yml` if the application has external dependencies or `--compose` is set.

**Structure**:
```yaml
version: "3.9"  # Omit if Docker Compose V2+

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
      target: production  # or development for --dev
    ports:
      - "${PORT:-3000}:3000"
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/appdb
    depends_on:
      db:
        condition: service_healthy
    restart: unless-stopped
    networks:
      - app-network

  db:  # if database detected
    image: postgres:16-alpine  # or mysql:8, etc.
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: appdb
    volumes:
      - db-data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 3s
      retries: 5
    networks:
      - app-network

  redis:  # if cache detected
    image: redis:7-alpine
    command: redis-server --maxmemory 256mb --maxmemory-policy allkeys-lru
    volumes:
      - redis-data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 3s
      retries: 5
    networks:
      - app-network

volumes:
  db-data:
  redis-data:

networks:
  app-network:
    driver: bridge
```

**Development profile** (if `--dev`):
Add a `docker-compose.dev.yml` override:
- Mount source code as volume for hot reload
- Use development target in Dockerfile
- Expose debug ports
- Set `NODE_ENV=development` or equivalent

============================================================
PHASE 5 — VALIDATION
============================================================

After generating files, verify:

1. **Dockerfile builds** — run `docker build --check .` if available, otherwise verify syntax
2. **Layer ordering** — confirm dependency install comes before source copy
3. **No secrets** — verify no hardcoded passwords, API keys, or tokens in Dockerfile or compose
4. **Port consistency** — EXPOSE matches the app's actual listen port
5. **Health check** — endpoint referenced in HEALTHCHECK actually exists in the app (or note to create it)

============================================================
OUTPUT
============================================================

Print a summary:

```
## Docker Setup Complete

### Files Created
- Dockerfile — Multi-stage build ({base image}, {final size estimate})
- .dockerignore — {N} patterns to minimize build context
- docker-compose.yml — Services: {list}
- docker-compose.dev.yml — Development overrides (if generated)

### Build Commands
- Production: docker compose up --build -d
- Development: docker compose -f docker-compose.yml -f docker-compose.dev.yml up
- Image only: docker build -t {name}:latest .

### Image Details
- Base: {base image}
- Estimated size: {size estimate}
- User: appuser (non-root, UID 1001)
- Health check: {endpoint}
- Exposed port: {port}

### Services
| Service | Image | Port | Volume |
|---------|-------|------|--------|
| app | built | {port} | — |
| db | postgres:16 | 5432 | db-data |
```

============================================================
NEXT STEPS
============================================================

1. Build and test locally: `docker compose up --build`
2. Add a `/health` endpoint to the application if one does not exist
3. Configure CI/CD to build and push the Docker image
4. Set real database credentials via environment variables or secrets manager

============================================================
DO NOT
============================================================

- Do NOT use `latest` tag for base images — pin to specific versions
- Do NOT run containers as root — always create and switch to a non-root user
- Do NOT copy `.env` files into the image — use environment variables at runtime
- Do NOT install development dependencies in the production stage
- Do NOT use `ADD` when `COPY` suffices (ADD has implicit tar extraction and URL fetch)
- Do NOT include `apt-get upgrade` — use a pinned base image instead
- Do NOT leave package manager caches in final image (use `--mount=type=cache` or clean up)
- Do NOT overwrite an existing Dockerfile without reading it first and preserving custom configuration
- Do NOT hardcode database passwords — use environment variable references
