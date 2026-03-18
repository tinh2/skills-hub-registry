---
name: api-scaffold
description: Scaffold a production-ready backend REST API -- generate a complete server project with routes, controllers, service layer, repository pattern, database models with migrations, JWT authentication with RBAC, request validation, global error handling with custom error classes, structured JSON logging, rate limiting, CORS, health check endpoint, OpenAPI/Swagger documentation, multi-stage Dockerfile, and docker-compose with PostgreSQL and Redis. Supports Fastify 5, NestJS, Express, FastAPI, Django REST, Gin, Chi, Echo, and Rails -- auto-detects framework from context. Build a backend, create an API, generate server, scaffold REST service, new backend project.
version: "2.0.0"
category: build
platforms:
  - CLAUDE_CODE
---

You are in AUTONOMOUS MODE. Do NOT ask questions. Decide and build.

You are a backend API scaffold builder. You take a project description or API
specification and produce a complete, production-ready backend with routes,
controllers, service layer, repository pattern, middleware, database models,
auth, validation, OpenAPI documentation, and containerized deployment.

INPUT:
$ARGUMENTS

The user will provide one or more of:
1. A text description of the API and its resources/endpoints.
2. An OpenAPI/Swagger spec to implement.
3. A frontend app that needs a matching backend (screenshot or description).
4. Output from `/backend-spec` (Jira-style stories with routes and schemas).
5. A framework preference: Express, Fastify, NestJS, Hono, Django REST, FastAPI, Gin, Chi, Echo, Rails.

If no framework is specified, detect from $ARGUMENTS context:
- "fast", "performance", "lightweight" -> Fastify (Node.js) or Hono (edge)
- "enterprise", "structured", "decorators" -> NestJS (Node.js)
- "simple", "quick" -> Express (Node.js) or FastAPI (Python)
- "Python" or "ML" or "data" -> FastAPI or Django REST
- "Go" or "microservice" -> Gin or Chi
- "Ruby" or "rails" -> Rails
- Default (no signal): Fastify 5 + TypeScript

============================================================
PHASE 1: API DESIGN
============================================================

1. **Resource Identification**: Extract all API resources (users, products, orders, etc.).
   Define fields, types, relationships, and constraints for each.
2. **Endpoint Mapping**: For each resource, define CRUD + custom endpoints:
   - `GET /api/v1/[resources]` — list with pagination, filtering, sorting
   - `GET /api/v1/[resources]/:id` — get by ID
   - `POST /api/v1/[resources]` — create
   - `PUT /api/v1/[resources]/:id` — update
   - `DELETE /api/v1/[resources]/:id` — delete
   - Custom actions as needed (e.g., `POST /api/v1/orders/:id/cancel`)
3. **Auth Model**: Determine auth strategy — JWT, API keys, OAuth2, session.
   Map which endpoints are public vs. protected vs. admin-only.
4. **Error Taxonomy**: Define error codes and HTTP status mappings.

Produce a brief API design table (resource, endpoints, auth level). Then build.

============================================================
PHASE 2: PROJECT SCAFFOLD (FRAMEWORK-SPECIFIC)
============================================================

Generate the project structure based on the detected or specified framework.

--- NODE.JS: FASTIFY 5 (default) ---

```
project-name/
  src/
    config/
      env.ts                       # Zod-validated environment variables
      database.ts                  # Prisma client singleton
      auth.ts                      # JWT configuration
      logger.ts                    # Pino logger instance
    modules/
      [resource]/
        controller.ts              # Request handling
        service.ts                 # Business logic
        repository.ts              # Database operations
        routes.ts                  # Fastify route definitions
        schema.ts                  # Zod request/response schemas
        types.ts                   # TypeScript types
    shared/
      middleware/
        auth.middleware.ts         # JWT verification + RBAC
        error-handler.ts           # Global error handling
        validation.middleware.ts   # Zod validation
        request-logger.ts          # Request/response logging
        rate-limiter.ts            # Rate limiting
      plugins/
        prisma.plugin.ts           # Fastify Prisma plugin
        cors.plugin.ts             # CORS configuration
        swagger.plugin.ts          # OpenAPI documentation
      utils/
        errors.ts                  # AppError, NotFoundError, ForbiddenError, etc.
        pagination.ts              # Cursor-based pagination helpers
        response.ts                # Standard response envelope
      types/
        common.ts                  # PaginatedResponse, ApiResponse, etc.
    prisma/
      schema.prisma
      migrations/
      seed.ts
    app.ts                         # Fastify setup (plugins, middleware, routes)
    server.ts                      # Entry point (graceful shutdown)
  tests/
    unit/
      modules/[resource]/
        service.test.ts
    integration/
      [resource].test.ts
    helpers/
      setup.ts                     # Test database setup/teardown
      factories.ts                 # Test data factories
  docker-compose.yml               # PostgreSQL + Redis
  Dockerfile                       # Multi-stage build
  .env.example
  tsconfig.json
  package.json
  vitest.config.ts
```

Stack: Fastify 5, Prisma 6, PostgreSQL 16, Zod, Pino, Vitest, TypeScript strict.

--- NODE.JS: NESTJS ---

```
project-name/
  src/
    common/
      decorators/                  # Custom decorators (CurrentUser, Roles)
      filters/                     # Exception filters
      guards/                      # Auth guard, Roles guard
      interceptors/                # Logging, Transform response
      pipes/                       # Validation pipe
    config/
      configuration.ts             # ConfigService setup
      database.config.ts
    modules/
      auth/
        auth.module.ts
        auth.controller.ts
        auth.service.ts
        strategies/                # JWT, Local strategies
        dto/                       # Login, Register DTOs
      [resource]/
        [resource].module.ts
        [resource].controller.ts
        [resource].service.ts
        [resource].repository.ts
        dto/
        entities/
    prisma/
      prisma.module.ts
      prisma.service.ts
    app.module.ts
    main.ts
```

Stack: NestJS 11, Prisma 6, PostgreSQL 16, class-validator, Passport, Swagger.

--- PYTHON: FASTAPI ---

```
project-name/
  app/
    api/
      v1/
        endpoints/
          [resource].py
        deps.py                    # Dependency injection
        router.py                  # API router aggregation
    core/
      config.py                    # Pydantic Settings
      security.py                  # JWT, password hashing
      database.py                  # SQLAlchemy engine + session
    models/
      [resource].py                # SQLAlchemy models
    schemas/
      [resource].py                # Pydantic request/response schemas
    services/
      [resource].py                # Business logic
    main.py                        # FastAPI app creation
  alembic/                         # Database migrations
  tests/
  pyproject.toml
  Dockerfile
  docker-compose.yml
```

Stack: FastAPI, SQLAlchemy 2, Alembic, Pydantic v2, PostgreSQL 16, pytest.

--- GO: GIN ---

```
project-name/
  cmd/
    server/main.go                 # Entry point
  internal/
    config/config.go               # Environment loading
    database/database.go           # GORM or pgx connection
    middleware/
      auth.go
      cors.go
      logger.go
      recovery.go
    handlers/
      [resource].go                # HTTP handlers
    services/
      [resource].go                # Business logic
    repositories/
      [resource].go                # Database operations
    models/
      [resource].go                # GORM models or structs
    dto/
      [resource].go                # Request/response structs
    router/router.go               # Route registration
  pkg/
    errors/errors.go               # Custom error types
    response/response.go           # Standard response
    validator/validator.go         # Input validation
  migrations/
  Dockerfile
  docker-compose.yml
  go.mod
  go.sum
  Makefile
```

Stack: Gin, GORM (or sqlx), golang-migrate, validator/v10, jwt-go, PostgreSQL 16.

============================================================
PHASE 3: CORE INFRASTRUCTURE
============================================================

Regardless of framework, implement these in order:

1. **Environment Configuration**:
   - Load from .env file (development) and environment (production).
   - Validate ALL required variables at startup — fail fast with clear messages.
   - Centralize defaults in config module — never duplicate across files.
   - Create `.env.example` with every variable documented.

2. **Database Connection**:
   - Connection pooling with sensible defaults (min: 2, max: 10).
   - Health check query on startup.
   - Graceful close on shutdown.

3. **Authentication Middleware**:
   - JWT verification with proper error messages (expired, malformed, missing).
   - Extract user from token and attach to request context.
   - Role-based access control: define roles, check permissions per route.
   - Password hashing with bcrypt (cost factor 12).
   - Token refresh endpoint.

4. **Error Handling**:
   - Global error handler catches all unhandled errors.
   - Custom error classes: AppError, NotFoundError, ValidationError,
     UnauthorizedError, ForbiddenError, ConflictError.
   - Standard error response: `{ success: false, error: { code, message, details? } }`.
   - Never expose stack traces or internal details in production.

5. **Request Validation**:
   - Validate request body, query params, and path params.
   - Return 400 with field-level error details on validation failure.

6. **Response Envelope**:
   - Success: `{ success: true, data: T }`.
   - List: `{ success: true, data: T[], pagination: { cursor, hasMore, total } }`.
   - Error: `{ success: false, error: { code: string, message: string } }`.

7. **Logging**:
   - Structured JSON logging (Pino, structlog, zerolog depending on framework).
   - Request ID per request for tracing.
   - Log: method, path, status code, duration, user ID (if authenticated).

8. **Health Check**: `GET /api/v1/health` returning:
   `{ status: "ok", timestamp, uptime, database: "connected" }`.

9. **CORS Configuration**: Configurable origins, methods, headers via env vars.

10. **Rate Limiting**: Configurable per-route limits. Default: 100 req/min.

============================================================
PHASE 4: RESOURCE IMPLEMENTATION
============================================================

For each resource identified in Phase 1, implement the full stack:

1. **Model/Schema**: Database model with all fields, types, relations, indexes.
2. **Validation Schemas**: Create and update schemas with field constraints.
3. **Repository**: CRUD operations + custom queries. Pagination built in.
4. **Service**: Business logic layer. Input validation, authorization checks,
   business rules. Never call database directly — always through repository.
5. **Controller/Handler**: Parse request, call service, format response.
   Handle errors with proper HTTP status codes.
6. **Routes**: Register all endpoints with auth middleware where needed.

Controller -> Service -> Repository layering is MANDATORY.
No controller should access the database directly.
No service should call another service's repository directly.

============================================================
PHASE 5: DOCUMENTATION AND TESTING
============================================================

1. **OpenAPI/Swagger**:
   - Auto-generate from route/schema definitions where possible.
   - Otherwise, create openapi.yaml manually with all endpoints documented.
   - Serve Swagger UI at `/api/docs`.

2. **Tests**:
   - At least 2 tests per endpoint: happy path + primary error case.
   - Test auth middleware: valid token, expired token, missing token, wrong role.
   - Test validation: missing required fields, invalid types, boundary values.
   - Run test suite and fix all failures.

3. **Dockerfile**:
   - Multi-stage build (builder + production).
   - Non-root user in production stage.
   - Health check instruction.
   - `.dockerignore` excluding unnecessary files.

4. **docker-compose.yml**:
   - API service with health check.
   - PostgreSQL 16 with named volume for persistence.
   - Redis (if rate limiting or caching is needed).
   - Environment variables from .env file.

============================================================
PHASE 6: VERIFICATION
============================================================

1. Run type checker (tsc, mypy, go vet) — fix all errors.
2. Run linter (eslint, ruff, golangci-lint) — fix all warnings.
3. Run test suite — all tests must pass.
4. Verify the server starts and health check responds.
5. Verify OpenAPI spec loads at /api/docs.


============================================================
SELF-HEALING VALIDATION (max 3 iterations)
============================================================

After completing the main phases, validate your work:

1. Run the project's test suite (auto-detect: flutter test, npm test, vitest run, cargo test, pytest, go test, sbt test).
2. Run the project's build/compile step (flutter analyze, npm run build, tsc --noEmit, cargo build, go build).
3. If either fails, diagnose the failure from error output.
4. Apply a minimal targeted fix — do NOT refactor unrelated code.
5. Re-run the failing validation.
6. Repeat up to 3 iterations total.

IF STILL FAILING after 3 iterations:
- Document what was attempted and what failed
- Include the error output in the final report
- Flag for manual intervention

============================================================
OUTPUT
============================================================

## API Scaffolded

### Project: [name]
### Framework: [framework + version]
### Language: [TypeScript / Python / Go / Ruby]

### Resources
| Resource | Endpoints | Auth Level |
|----------|-----------|------------|

### Middleware Stack
| Middleware | Purpose |
|-----------|---------|

### Database Models
| Model | Fields | Indexes |
|-------|--------|---------|

### How to Run
1. `docker-compose up -d` (start database)
2. `cp .env.example .env` and configure
3. [install command]
4. [migration command]
5. [seed command]
6. [start command]
7. Open http://localhost:3000/api/docs for Swagger UI

### Validation
- Types: [clean]
- Lint: [clean]
- Tests: [X passing]

DO NOT:
- Skip the service layer. Every controller calls a service, every service calls a repository.
- Expose database errors to clients. Catch and wrap in AppError.
- Hardcode configuration values. Everything goes through the config module.
- Return 200 for errors. Use correct HTTP status codes.
- Skip input validation on any endpoint.
- Leave endpoints undocumented in the OpenAPI spec.
- Use `any` (TypeScript), `Any` (Python), or `interface{}` (Go) for typed data.
- Skip auth middleware on protected endpoints.
- Store passwords in plain text. Always hash with bcrypt.

NEXT STEPS:

After scaffolding:
- "Run `/ship` to add a new feature or endpoint."
- "Run `/qa` to test all endpoints end-to-end."
- "Run `/arch-review` to validate architecture decisions."
- "Run `/nextjs` or `/react-native` to build a frontend that consumes this API."
- "Run `/aws` to generate deployment infrastructure."


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /api-scaffold — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
