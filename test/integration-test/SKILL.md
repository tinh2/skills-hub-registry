---
name: integration-test
description: Generate integration tests for APIs, databases, and external services. Auto-detects backend stack (Express, Fastify, NestJS, Django, FastAPI, Rails, Go), ORM (Prisma, TypeORM, SQLAlchemy, GORM), and database (PostgreSQL, MongoDB, Firestore), then creates tests covering endpoint CRUD, auth flows, DB transactions, and external service failures with proper fixtures and mocks. Self-heals failing tests up to 3 iterations. Use when you need to test API endpoints end-to-end, verify database operations, test service interactions, or validate auth and error handling.
version: "2.0.0"
category: test
platforms:
  - CLAUDE_CODE
---

You are in AUTONOMOUS MODE. Do NOT ask questions. Detect the project's stack,
generate integration tests covering API endpoints, database operations, and
service interactions, then run them with a self-healing fix loop.

INPUT:
$ARGUMENTS

If arguments are provided, focus on those specific APIs, services, or modules.
If no arguments are provided, generate integration tests for the ENTIRE project.

============================================================
PHASE 1: STACK AND SERVICE DISCOVERY
============================================================

Step 1.1 -- Framework Detection

Detect the backend framework and test infrastructure:

| Indicator | Framework |
|---|---|
| package.json with fastify | Fastify |
| package.json with express | Express |
| package.json with @nestjs/core | NestJS |
| manage.py + settings.py | Django |
| requirements.txt with fastapi | FastAPI |
| requirements.txt with flask | Flask |
| go.mod + net/http or gin or echo | Go |
| Gemfile with rails | Ruby on Rails |
| pubspec.yaml with shelf or dart_frog | Dart backend |

Detect the ORM / database layer:

| Indicator | ORM |
|---|---|
| prisma/ directory or schema.prisma | Prisma |
| ormconfig.* or typeorm in package.json | TypeORM |
| sequelize in package.json | Sequelize |
| drizzle.config.* | Drizzle |
| settings.py with DATABASES | Django ORM |
| requirements.txt with sqlalchemy | SQLAlchemy |
| go.mod with gorm | GORM |
| Gemfile with activerecord | ActiveRecord |

Detect the database:

| Indicator | Database |
|---|---|
| DATABASE_URL with postgres | PostgreSQL |
| DATABASE_URL with mysql | MySQL |
| *.sqlite or DATABASE_URL with sqlite | SQLite |
| firebase.json or firebaseConfig | Firestore |
| MONGODB_URI or mongoose in deps | MongoDB |
| REDIS_URL or redis in deps | Redis |

Detect the test framework (same as `/unit-test` detection table).

Step 1.2 -- API Endpoint Discovery

Discover ALL API endpoints in the project:

| Framework | Discovery Method |
|---|---|
| Fastify | Read route registration files, search for fastify.get/post/put/delete |
| Express | Search for app.get/post/put/patch/delete, router.* |
| NestJS | Read *.controller.ts, find @Get/@Post/@Put/@Delete/@Patch decorators |
| Django | Read urls.py, find path() and urlpatterns |
| FastAPI | Read *.py, find @app.get/@router.post decorators |
| Flask | Read *.py, find @app.route, @blueprint.route |
| Go | Search for http.HandleFunc, r.GET/POST (gin), e.GET/POST (echo) |
| Rails | Read config/routes.rb, run rake routes if available |

Build the endpoint inventory:

| # | Method | Path | Auth | Request Body | Response | Handler File |
|---|--------|------|------|-------------|----------|-------------|

Step 1.3 -- Database Model Discovery

Discover ALL data models:

| ORM | Discovery Method |
|---|---|
| Prisma | Read schema.prisma for model definitions |
| TypeORM | Read *.entity.ts files |
| Sequelize | Read *.model.ts or models/ directory |
| Django | Read models.py files |
| SQLAlchemy | Read models.py, find class inheriting Base |
| GORM | Read *.go files with gorm struct tags |
| ActiveRecord | Read app/models/*.rb |
| Drizzle | Read schema.ts or drizzle/ directory |

Build the model inventory:

| Model | Fields | Relations | Unique Constraints | Validation Rules |
|-------|--------|-----------|-------------------|-----------------|

Step 1.4 -- External Service Discovery

Identify all external service integrations:

- HTTP clients (Axios, fetch, got, httpx, requests)
- Message queues (RabbitMQ, SQS, Redis pub/sub)
- Email services (SendGrid, SES, Nodemailer)
- Payment processors (Stripe, PayPal)
- Auth providers (Auth0, Clerk, Firebase Auth, Supabase Auth)
- Storage services (S3, GCS, Firebase Storage)
- Search engines (Elasticsearch, Algolia, Meilisearch)

============================================================
PHASE 2: TEST INFRASTRUCTURE SETUP
============================================================

Step 2.1 -- Test Database Configuration

Set up an isolated test database:

FOR POSTGRESQL / MYSQL:
- Check for existing test database URL in .env.test or test config
- If none exists, create a test-specific connection using the same DB with a test schema
  or a separate test database
- Ensure migrations run against the test database

FOR SQLITE:
- Use an in-memory database or a temporary file

FOR MONGODB:
- Use mongodb-memory-server (Node.js) or mongomock (Python)

FOR FIRESTORE:
- Use Firebase emulators (firebase emulators:start --only firestore)

Step 2.2 -- Test Helpers

Create shared test helpers based on the detected framework:

FOR NODE.JS (Vitest/Jest + Supertest):

Create test helpers with:
- buildApp(): Creates and configures the app instance for supertest
- createTestUser(role?): Registers a user and returns auth token
- seedTestData(fixtures): Loads fixture data into the test database
- cleanDatabase(): Truncates all tables between tests
- authenticatedRequest(method, path, token): Shorthand for auth requests

FOR PYTHON (pytest):

Create conftest.py fixtures:
- client: TestClient or AsyncClient with the app
- db_session: Database session with transaction rollback
- auth_headers: Returns headers with a valid JWT for a test user
- seed_data: Loads fixtures into the test database

FOR GO:

Create test helpers:
- setupTestServer(): Returns httptest.Server with the app handler
- createTestUser(t): Creates a user and returns the auth token
- seedDB(t, fixtures): Loads test data
- cleanDB(t): Truncates tables

Step 2.3 -- Mock Setup for External Services

Create mocks/stubs for every external service discovered in Phase 1:

- HTTP calls: Use nock (Node.js), responses (Python), httpmock (Go)
- Email: Mock the email client, capture sent emails for assertion
- Payment: Mock Stripe/PayPal client, return realistic responses
- Storage: Mock upload/download, use local filesystem or memory
- Message queues: Mock publish, capture messages for assertion

Each mock must:
- Return realistic response structures matching the real service
- Support configurable failure scenarios (timeout, 500, rate limit)
- Track call count and arguments for assertion

============================================================
PHASE 3: TEST GENERATION
============================================================

Step 3.1 -- API Endpoint Tests

For EACH endpoint discovered in Phase 1, generate tests covering:

HAPPY PATH:
- Send valid request with realistic data
- Verify correct HTTP status (200, 201, 204)
- Verify response body shape and values
- Verify database state changed correctly (read back from DB)

VALIDATION AND ERRORS:
- Missing required fields -> 400
- Invalid field types -> 400
- Invalid field values (out of range, wrong format) -> 400
- Empty request body when required -> 400

AUTHENTICATION AND AUTHORIZATION:
- No auth token on protected endpoint -> 401
- Expired or malformed token -> 401
- Wrong role accessing restricted endpoint -> 403
- Accessing another user's resource -> 403 or 404

RESOURCE LIFECYCLE:
- Create -> Read (verify) -> Update -> Read (verify) -> Delete -> Read (verify 404)
- Duplicate creation (unique constraint) -> 409
- Update non-existent resource -> 404
- Delete non-existent resource -> 404

QUERY AND FILTERING (for list endpoints):
- Pagination: first page, middle page, last page, beyond last page
- Filtering: each filter field individually, combined filters
- Sorting: ascending, descending, by different fields
- Search: matching term, no results, partial match

Step 3.2 -- Database Operation Tests

For EACH model discovered in Phase 1, generate tests covering:

CRUD OPERATIONS:
- Create with all required fields -> record persisted
- Create with optional fields -> defaults applied correctly
- Read by primary key -> correct record returned
- Read by unique field -> correct record returned
- Update single field -> only that field changes
- Update multiple fields -> all fields updated
- Delete -> record removed, related records handled per cascade rules

CONSTRAINTS:
- Unique constraint violation -> appropriate error
- Foreign key constraint -> cannot delete parent with children (or cascades)
- Not-null constraint -> cannot create with null required field
- Check constraints -> out-of-range values rejected

TRANSACTIONS:
- Multi-step operation succeeds atomically
- Multi-step operation rolls back on failure in any step
- Concurrent updates to the same record (optimistic locking if present)

QUERIES:
- Complex queries with joins return correct data shape
- Aggregation queries return correct counts/sums
- Queries with pagination return correct slices

Step 3.3 -- Service Interaction Tests

For EACH external service integration, generate tests covering:

SUCCESS SCENARIOS:
- Service called with correct parameters
- Response parsed and transformed correctly
- Side effects triggered (database updated, event emitted)

FAILURE SCENARIOS:
- Service returns 500 -> error handled gracefully, no crash
- Service times out -> timeout handled, appropriate error returned
- Service returns unexpected response shape -> error logged, fallback behavior
- Service rate-limits (429) -> retry or backoff behavior
- Network error -> appropriate error message to caller

MOCK VERIFICATION:
- Correct endpoint called
- Correct HTTP method used
- Correct headers sent (auth, content-type)
- Correct request body sent
- Correct number of calls made (no duplicate calls)

============================================================
PHASE 4: EXECUTION AND SELF-HEALING
============================================================

Step 4.1 -- Start Required Services

Start any services needed for integration tests:
- Database: ensure test DB is running and migrated
- Docker: docker compose up -d if compose file exists
- Firebase emulators: firebase emulators:start if Firebase detected
- App server: start in test mode if needed for supertest/httptest

Step 4.2 -- Run Tests

Execute all generated integration tests:

| Framework | Command |
|---|---|
| Vitest | npx vitest run tests/integration/ --reporter=verbose |
| Jest | npx jest tests/integration/ --verbose --forceExit --runInBand |
| pytest | pytest tests/integration/ -v --tb=short |
| go test | go test -v -count=1 ./tests/integration/... |
| RSpec | bundle exec rspec spec/integration/ --format documentation |

Note: Use --runInBand or equivalent for integration tests to avoid
parallel database conflicts.

Step 4.3 -- Self-Healing Loop (max 3 iterations)

For each failure, diagnose:

TEST BUG: Wrong URL, missing mock, incorrect assertion, async timing
-> Fix the test

APP BUG: Missing validation, wrong status code, broken query, unhandled error
-> Fix the application code

INFRASTRUCTURE: Database not running, port conflict, migration not applied
-> Fix the environment, restart services

Apply fixes, re-run ONLY failing tests. Repeat up to 3 iterations.

Never delete tests. Never weaken assertions. Never skip failures.

Step 4.4 -- Full Suite Run

After healing, run ALL tests (existing + new) to verify no regressions.

============================================================
OUTPUT
============================================================

## Integration Test Report

### Stack Detected
- **Framework:** [name]
- **ORM:** [name]
- **Database:** [type]
- **External services:** [list]
- **Test framework:** [name]

### Endpoints Tested

| Method | Path | Happy Path | Validation | Auth | Edge Cases | Status |
|--------|------|-----------|-----------|------|-----------|--------|

### Database Operations Tested

| Model | Create | Read | Update | Delete | Constraints | Transactions | Status |
|-------|--------|------|--------|--------|-------------|-------------|--------|

### External Service Tests

| Service | Success | Timeout | Error | Rate Limit | Status |
|---------|---------|---------|-------|-----------|--------|

### Results Summary
- Total tests: N
- Passed: N
- Failed: N (after self-healing)
- Unresolved: N

### Self-Healing Log
- Iteration 1: N fixed ([test bugs / app bugs])
- Iteration 2: N fixed
- Iteration 3: N fixed

### App Bugs Found and Fixed
| Bug | File | Root Cause | Fix |
|-----|------|-----------|-----|

NEXT STEPS:

- "Integration tests passing? Run `/e2e` for full user-flow end-to-end tests."
- "Run `/unit-test` if unit coverage is still low."
- "Run `/contract-test` to validate API schemas against consumers."
- "Run `/load-test` to verify endpoints handle production traffic."
- "Run `/test-suite` to see overall test health after adding integration tests."

DO NOT:

- Do NOT run integration tests in parallel unless the test framework supports isolated DB transactions per test.
- Do NOT use production database credentials. Always use test database configuration.
- Do NOT leave test data in the database after tests complete.
- Do NOT mock the database in integration tests. Use a real test database.
- Do NOT skip authentication tests even if the project has no auth yet.
- Do NOT generate tests for third-party library internals.
- Do NOT weaken assertions to make tests pass. Fix the underlying issue.
- Do NOT delete or modify existing tests.


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /integration-test — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
