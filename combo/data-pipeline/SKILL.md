---
name: data-pipeline
description: Data-heavy app setup chain — scaffolds an API, generates integration tests, then load tests for scalability.
version: "1.0.0"
category: combo
platforms:
  - CLAUDE_CODE
---

You are an autonomous data pipeline setup agent. Do NOT ask the user questions.

This skill chains three skills in sequence:
1. `/api-scaffold` — scaffold the API layer with routes, controllers, and models
2. `/integration-test` — generate integration tests to verify the API works end-to-end
3. `/load-test` — run load tests to verify the API scales under pressure

INPUT: $ARGUMENTS
Pass the API description, data model, or feature requirements.

============================================================
PHASE 1: API SCAFFOLD  (/api-scaffold)
============================================================

Follow the instructions defined in the `/api-scaffold` skill exactly.

Scaffold the full API:
- Routes and controllers for each resource
- Data models and database schema
- Validation middleware
- Error handling and response formatting
- Database connection and query layer

Commit all scaffolded code. Record the endpoints created and their
expected request/response shapes for Phase 2.

If scaffolding fails (unsupported stack, missing dependencies), STOP and report.

============================================================
PHASE 2: INTEGRATION TESTS  (/integration-test)
============================================================

Follow the instructions defined in the `/integration-test` skill exactly.

Generate integration tests that verify the API from Phase 1:
- Happy path for every endpoint scaffolded
- Error cases (400, 401, 404, 422 responses)
- Data persistence (create then read back)
- Relationship integrity (foreign keys, cascades)
- Edge cases (empty payloads, max lengths, special characters)

IMPORTANT: Base the tests on the actual endpoints and models created in
Phase 1. Do NOT write generic template tests — test the real API surface.

Run the tests. If any fail:
- Fix the API code (not the tests) if the test expectation is correct.
- Fix the test if the expectation is wrong.
- Re-run until all pass.

Commit all tests and any API fixes.

============================================================
PHASE 3: LOAD TEST  (/load-test)
============================================================

Follow the instructions defined in the `/load-test` skill exactly.

Load test the API to verify it scales:
- Ramp-up test (10 → 100 → 500 concurrent users)
- Sustained load test (target throughput for 60 seconds)
- Spike test (sudden 5x traffic burst)
- Measure: p50/p95/p99 latency, error rate, throughput

IMPORTANT: Target the same endpoints from Phase 1. Use realistic
payloads based on the data models. Identify bottlenecks.

If the load test reveals critical performance issues (p99 > 2s or
error rate > 5%), document them with recommended optimizations.

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
