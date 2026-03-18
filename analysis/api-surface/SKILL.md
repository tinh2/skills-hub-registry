---
name: api-surface
description: >
  Maps the entire API surface of a codebase -- route definitions, middleware chains, auth requirements,
  request/response types, deprecated endpoints, orphaned endpoints, and cross-endpoint inconsistencies.

  USE THIS SKILL WHEN:
  - You need a complete inventory of all API endpoints in a project
  - Someone asks "what endpoints do we have?" or "what does our API look like?"
  - You are onboarding to a new backend codebase and need to understand its API
  - You need to find orphaned, undocumented, or deprecated endpoints
  - Someone asks about API inconsistencies (different response shapes, auth gaps)
  - You are preparing for an API review, documentation sprint, or versioning migration
  - You need to understand endpoint dependencies before refactoring
  - A project has no OpenAPI spec and you need to generate one from code
  - You suspect there are endpoints without authentication or rate limiting

  TRIGGER PHRASES: "API surface", "list all endpoints", "API inventory", "endpoint map",
  "orphaned endpoints", "API inconsistencies", "undocumented endpoints", "route discovery",
  "API audit", "middleware matrix", "endpoint dependencies", "API coverage"
version: "2.0.0"
category: analysis
platforms:
  - CLAUDE_CODE
---

You are an autonomous API surface mapping agent. You discover, catalog, and analyze
every endpoint in the codebase, producing a complete inventory with dependency graph.
Do NOT ask the user questions. Investigate the entire codebase thoroughly.

INPUT: $ARGUMENTS (optional)
If provided, focus on a specific API module or version (e.g., "v2 endpoints", "admin API", "webhooks").
If not provided, map the entire API surface.

============================================================
PHASE 1: STACK DETECTION & ROUTE DISCOVERY
============================================================

Step 1.1 -- Identify the Tech Stack

Read package.json, pubspec.yaml, requirements.txt, go.mod, Cargo.toml, Gemfile, pom.xml.
Identify the API framework:
- Node.js: Express, Fastify, Hono, Koa, NestJS
- Python: Flask, Django, FastAPI
- Java: Spring Boot
- Ruby: Rails
- Go: Gin, Echo, Chi
- Rust: Actix, Rocket, Axum
- Elixir: Phoenix

Step 1.2 -- Discover All Route Definitions

Use framework-specific discovery patterns:

**Express/Fastify/Koa/Hono:**
- Scan for `app.get()`, `app.post()`, `router.get()`, `fastify.route()`, etc.
- Follow router mounting: `app.use('/api', router)`.
- Resolve nested routers and prefix chains to compute full paths.

**NestJS:**
- Scan for `@Controller()`, `@Get()`, `@Post()`, etc. decorators.
- Resolve module imports and controller prefix chains.

**Django/Flask/FastAPI:**
- Scan for `urlpatterns`, `@app.route()`, `@router.get()`.
- Follow `include()` chains in Django.

**Spring Boot:**
- Scan for `@RequestMapping`, `@GetMapping`, `@PostMapping`.

**Rails:**
- Parse `config/routes.rb` for resources, get, post, etc.

**GraphQL:**
- Parse schema.graphql or type definitions for Query/Mutation/Subscription.
- Map resolvers to their type definitions.

**OpenAPI/Swagger:**
- Parse openapi.yaml/swagger.json if present.
- Cross-reference with actual code routes -- flag any mismatches.

Step 1.3 -- Discover Non-HTTP Endpoints

Scan for non-REST entry points:
- WebSocket handlers
- gRPC service definitions (.proto files)
- Message queue consumers (SQS, RabbitMQ, Kafka)
- Cloud Function triggers (Firestore, S3, scheduled)
- CLI commands that act as API entry points

============================================================
PHASE 2: ENDPOINT DETAIL EXTRACTION
============================================================

For each discovered endpoint, extract ALL of the following:

**Route Details:**
- HTTP method (GET, POST, PUT, PATCH, DELETE)
- Full path (with all prefixes resolved)
- Path parameters (`:id`, `{id}`)
- Query parameters (name, type, required/optional)

**Middleware Chain:**
- List every middleware applied, in execution order
- Auth middleware: type (JWT, session, API key, Firebase, OAuth)
- Validation middleware: what it validates (body, params, query)
- Rate limiting: limits and windows
- CORS: allowed origins
- Logging: request/response logging enabled?

**Request Type:**
- Body schema (from TypeScript types, Zod schemas, Joi, class-validator, Pydantic, serializers)
- Content-Type expected (JSON, form-data, multipart)
- Required vs. optional fields

**Response Type:**
- Success response schema and status code
- Error response schemas and status codes
- Pagination format (if list endpoint)

**Handler Internals:**
- Which services/repositories the handler calls
- Which database tables it reads from or writes to
- Which external APIs it calls
- Dependencies on other endpoints (internal calls)

============================================================
PHASE 3: DEPENDENCY GRAPH
============================================================

Build a complete endpoint dependency graph covering:

**Inter-Endpoint Dependencies:**
- Endpoints that call other endpoints internally
- Endpoints that must be called in sequence (create before update)
- Endpoints that share database transactions

**Service Dependencies:**
- Which services each endpoint depends on
- Shared services across endpoints (high fan-in = fragile)
- Service fan-out: services called by many endpoints

**Database Dependencies:**
- Which tables each endpoint reads/writes
- Endpoints that compete for same table locks (contention risk)
- Read-only vs. read-write classification per endpoint

**External Dependencies:**
- Which external APIs each endpoint calls
- Endpoints that fail if an external service is down (hard dependencies)

============================================================
PHASE 4: ANOMALY DETECTION
============================================================

**Orphaned Endpoints:**
- Endpoints defined in code but never called by any client, frontend, or test
- Search: frontend code, mobile code, API client libraries, integration tests, OpenAPI consumers, webhook registrations
- For each orphan: record last modified date (git log) and likely purpose
- Do NOT flag internal health/metrics endpoints as orphaned

**Inconsistencies:**
- Same data returned in different shapes from different endpoints
  (e.g., `/users/:id` returns `{ name }` but `/orders/:id` includes `{ user: { fullName } }`)
- Same operation available via multiple endpoints with different behavior
- Auth requirements that differ for similar operations (e.g., one CRUD endpoint requires auth, another does not)
- Error response formats that vary across endpoints

**Deprecated Endpoints:**
- Scan for @deprecated markers, TODO comments about removal, version headers
- Check if deprecated endpoints still have active callers
- Flag deprecated endpoints without a replacement or migration path

**Undocumented Endpoints:**
- Endpoints not present in OpenAPI/Swagger spec (if one exists)
- Endpoints without JSDoc/docstring describing purpose


============================================================
SELF-HEALING VALIDATION (max 2 iterations)
============================================================

After producing output, validate data quality and completeness:

1. Verify all output sections have substantive content (not just headers).
2. Verify every finding references a specific file, code location, or data point.
3. Verify recommendations are actionable and evidence-based.
4. If the analysis consumed insufficient data (empty directories, missing configs),
   note data gaps and attempt alternative discovery methods.

IF VALIDATION FAILS:
- Identify which sections are incomplete or lack evidence
- Re-analyze the deficient areas with expanded search patterns
- Repeat up to 2 iterations

IF STILL INCOMPLETE after 2 iterations:
- Flag specific gaps in the output
- Note what data would be needed to complete the analysis

============================================================
OUTPUT
============================================================

Write the full analysis to `docs/api-surface-map.md` (create `docs/` if needed).

## API Surface Map

### Stack: {detected stack}
### Total Endpoints: {count}
### API Versions: {list}

### Endpoint Inventory

| # | Method | Path | Auth | Rate Limit | Request Type | Response Type | Tables | External Deps |
|---|--------|------|------|-----------|-------------|--------------|--------|---------------|
| 1 | {GET} | {/api/v1/users} | {JWT} | {100/min} | {none} | {User[]} | {users} | {none} |

### Middleware Matrix

| Endpoint | Auth | Validation | Rate Limit | CORS | Logging |
|----------|------|-----------|-----------|------|---------|
| {path} | {type} | {schema} | {limit} | {origins} | {yes/no} |

### Dependency Graph

```
Endpoint A --calls--> Service X --reads--> Table Y
                               --calls--> External Z
Endpoint B --calls--> Service X (shared)
           --calls--> Service W --writes--> Table Y (contention)
```

### Orphaned Endpoints

| Endpoint | Last Modified | Likely Purpose | Recommendation |
|----------|-------------|---------------|----------------|
| {path} | {date} | {purpose} | {remove/document/connect} |

### Inconsistencies

| Issue | Endpoints Involved | Description | Recommendation |
|-------|-------------------|-------------|----------------|
| {shape mismatch} | {EP1, EP2} | {description} | {standardize on X} |

### Deprecated Endpoints

| Endpoint | Deprecated Since | Replacement | Active Callers |
|----------|-----------------|-------------|----------------|
| {path} | {date/version} | {new path} | {count} |

### Coverage Summary
- **Documented:** {n}/{total} endpoints
- **Authenticated:** {n}/{total} endpoints
- **Rate-limited:** {n}/{total} endpoints
- **Tested:** {n}/{total} endpoints (from test file analysis)

### Security Flags
- Endpoints without authentication: [list]
- Endpoints without rate limiting: [list]
- Endpoints accepting file uploads without size limits: [list]

DO NOT:
- Miss routes registered dynamically (scan for string patterns, not just static route defs).
- Ignore middleware applied at the app level (affects all routes).
- Flag internal health/metrics endpoints as orphaned.
- Assume OpenAPI spec is complete -- always cross-reference with actual code.

NEXT STEPS:
- "Run `/api-review` to evaluate API design quality."
- "Run `/api-docs` to generate or update API documentation."
- "Run `/security-review` to audit auth and access control."
- "Run `/dead-code` to remove truly orphaned endpoints."


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /api-surface — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
