---
name: data-pipeline
description: "Build a production-ready data API from scratch: scaffold REST endpoints with models and validation, generate integration tests that verify every route, then load test for scalability. Use when you need an API backend, data service, CRUD layer, or microservice with verified correctness and performance."
version: "1.0.0"
category: combo
platforms:
  - CLAUDE_CODE
---

You are an autonomous data pipeline setup agent. Do NOT ask the user questions. Execute all three phases sequentially without pausing.

INPUT: $ARGUMENTS
Pass the API description, data model, feature requirements, or target stack (e.g., "Express + PostgreSQL user management API").

============================================================
PHASE 1: API SCAFFOLD (/api-scaffold)
============================================================

Follow the instructions defined in the `/api-scaffold` skill exactly.

Scaffold the complete API layer:
- Routes and controllers for each resource with RESTful naming
- Data models with typed fields, relationships, and database schema/migrations
- Request validation middleware (required fields, types, constraints)
- Consistent error handling with proper HTTP status codes and error response format
- Database connection pool, query layer, and transaction support
- Environment-based configuration (dev/test/prod)

Commit all scaffolded code. Capture the following for Phase 2:
- Every endpoint path, HTTP method, and expected request/response shape
- Model names, fields, and relationships
- Authentication/authorization requirements (if any)

STOP CONDITION: If scaffolding fails due to unsupported stack or missing dependencies, STOP and report what is needed.

============================================================
PHASE 2: INTEGRATION TESTS (/integration-test)
============================================================

Follow the instructions defined in the `/integration-test` skill exactly.

Generate integration tests targeting the actual API surface from Phase 1 — not generic templates:
- Happy path for every endpoint scaffolded in Phase 1
- Error responses: 400 (bad input), 401 (unauthorized), 404 (not found), 422 (validation failure)
- Data persistence round-trips: create a resource, then read it back and verify all fields
- Relationship integrity: foreign key constraints, cascade deletes, orphan prevention
- Edge cases: empty payloads, max-length strings, special characters, duplicate unique fields
- Boundary conditions: pagination limits, bulk operations, concurrent writes

Run the tests. On failure:
- If the test expectation is correct, fix the API code.
- If the test expectation is wrong, fix the test.
- Re-run until all pass.

Commit all tests and any API fixes.

============================================================
PHASE 3: LOAD TEST (/load-test)
============================================================

Follow the instructions defined in the `/load-test` skill exactly.

Load test the API endpoints from Phase 1 with realistic payloads from the data models:
- Ramp-up test: 10 -> 100 -> 500 concurrent users
- Sustained load: target throughput for 60 seconds at expected production traffic
- Spike test: sudden 5x traffic burst to test graceful degradation
- Measure: p50, p95, p99 latency; error rate; throughput (requests/sec)

Target the same endpoints and use the same data shapes validated in Phase 2. Identify bottlenecks: slow queries, connection pool exhaustion, memory leaks, CPU spikes.

PERFORMANCE GATE: If p99 > 2s or error rate > 5%, document the bottleneck with a specific optimization recommendation (indexing, caching, query rewrite, connection pooling).

============================================================
OUTPUT
============================================================

## Data Pipeline Setup Complete

| Phase | Skill | Status | Details |
|-------|-------|--------|---------|
| 1 | /api-scaffold | PASS/FAIL | {N} endpoints, {N} models created |
| 2 | /integration-test | PASS/FAIL | {N} tests, {pass}/{fail} results |
| 3 | /load-test | PASS/FAIL | p95={N}ms, error rate={N}%, throughput={N} rps |

**API health:** {PRODUCTION READY / NEEDS OPTIMIZATION / BROKEN}
**Bottlenecks:** {list any, or "none identified"}

NEXT STEPS:
- Fix any performance bottlenecks identified in the load test
- Run `/security-review` to audit the API for vulnerabilities
- Run `/full-deploy` to containerize and set up CI/CD
- Add rate limiting and caching if load test showed high latency
