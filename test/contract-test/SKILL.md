---
name: contract-test
description: Auto-detects API framework, generates consumer-driven contract tests using Pact or OpenAPI validation, verifies backward compatibility, and sets up CI verification.
version: "1.0.0"
category: test
platforms:
  - CLAUDE_CODE
---

You are in AUTONOMOUS MODE. Do NOT ask questions. Detect the API framework,
generate contract tests to validate API schemas, verify backward compatibility,
and configure CI-based contract verification.

INPUT:
$ARGUMENTS

If arguments are provided, focus on those specific APIs, consumers, or contracts.
If no arguments are provided, generate contract tests for ALL API endpoints.

============================================================
PHASE 1: API DISCOVERY
============================================================

Step 1.1 -- Detect API Framework

Scan for the API framework using the same detection table as `/integration-test`.

Record: framework, language, base URL, API versioning scheme (if any).

Step 1.2 -- Detect Existing API Specification

Check for existing API documentation:

| Indicator | Spec Type |
|---|---|
| openapi.yaml, openapi.json, swagger.yaml, swagger.json | OpenAPI/Swagger |
| api-docs/ directory | OpenAPI |
| graphql.schema, schema.graphql, *.graphql files | GraphQL SDL |
| proto/ directory, *.proto files | gRPC/Protobuf |
| asyncapi.yaml, asyncapi.json | AsyncAPI (events) |
| pact/ directory, pact-config.* | Pact contracts |
| dredd.yml | Dredd API testing |
| .spectral.yaml | Spectral linting |

Step 1.3 -- Discover All Endpoints

Build the full endpoint inventory (same method as `/integration-test`).

For each endpoint, extract the ACTUAL contract:

REQUEST CONTRACT:
- HTTP method
- URL path (with path parameters typed)
- Query parameters (name, type, required)
- Request headers (required and optional)
- Request body schema (field names, types, required/optional, validation rules)
- Content-Type

RESPONSE CONTRACT:
- Status codes (all possible: 200, 201, 400, 401, 403, 404, 500)
- Response body schema for each status code
- Response headers (Content-Type, pagination headers, rate limit headers)
- Error response format (consistent error shape)

Build the contract table:

| Endpoint | Method | Request Schema | Response 2xx Schema | Error Schema | Auth |
|----------|--------|---------------|---------------------|-------------|------|

Step 1.4 -- Identify Consumers

Determine who consumes this API:

- Frontend apps in the same repo (monorepo)
- Mobile apps
- Other microservices
- Third-party integrations
- Public API consumers

If consumers are in the same repo, read their API call code to extract
ACTUAL usage patterns (which fields they send, which fields they read).

============================================================
PHASE 2: CONTRACT TOOL SETUP
============================================================

Step 2.1 -- Select Contract Testing Approach

Choose based on project needs:

APPROACH 1 -- OPENAPI VALIDATION (schema-first):
Best for: Projects with an OpenAPI spec, or projects that should have one.
Tools: Prism (mock server), Spectral (linting), committee (Ruby), openapi-enforcer (Node.js)

APPROACH 2 -- CONSUMER-DRIVEN CONTRACTS (Pact):
Best for: Microservice architectures with multiple consumers.
Tools: Pact (pact-js, pact-python, pact-go)

APPROACH 3 -- API BLUEPRINT + DREDD:
Best for: Projects using API Blueprint documentation.
Tools: Dredd

APPROACH 4 -- SCHEMA SNAPSHOT TESTING:
Best for: Simple projects where a full contract framework is overkill.
Tools: Jest/Vitest snapshot tests on API response shapes

Decision logic:
1. If OpenAPI spec exists -> APPROACH 1 (validate against spec)
2. If multiple consumers exist -> APPROACH 2 (Pact)
3. If API Blueprint exists -> APPROACH 3 (Dredd)
4. If simple single-consumer project -> APPROACH 4 (schema snapshots)
5. If no spec exists -> Generate OpenAPI spec from code, then APPROACH 1

Step 2.2 -- Install Tools

FOR OPENAPI VALIDATION:

If no OpenAPI spec exists, generate one:
| Framework | Generation Method |
|---|---|
| Fastify | Use @fastify/swagger to auto-generate from route schemas |
| Express + Zod/Joi | Extract schemas from validation middleware |
| NestJS | Use @nestjs/swagger decorators (may already exist) |
| FastAPI | Auto-generated at /openapi.json |
| Django REST | Use drf-spectacular or drf-yasg |
| Go (Gin/Echo) | Use swaggo/swag annotations |

Install validation tools:
- Node.js: npm install -D @stoplight/prism-cli @stoplight/spectral-cli
- Python: pip install openapi-core schemathesis
- Ruby: gem install committee

FOR PACT:

Install consumer and provider packages:
- Node.js: npm install -D @pact-foundation/pact
- Python: pip install pact-python
- Go: (use pact-go, requires pact CLI tools)

FOR SCHEMA SNAPSHOTS:

No additional installation needed. Uses existing test framework snapshot capabilities.

============================================================
PHASE 3: CONTRACT TEST GENERATION
============================================================

Step 3.1 -- OpenAPI Validation Tests

If using APPROACH 1:

SPEC LINTING:
- Run Spectral against the OpenAPI spec
- Check for: missing descriptions, inconsistent naming, missing error responses,
  deprecated endpoints without alternatives

RESPONSE VALIDATION:
For each endpoint, generate a test that:
1. Calls the endpoint with valid request data
2. Validates the response against the OpenAPI schema
3. Verifies all required fields are present
4. Verifies field types match the schema
5. Verifies enum values are within allowed set
6. Verifies nullable fields handle null correctly

REQUEST VALIDATION:
For each endpoint, generate a test that:
1. Sends a request missing required fields -> verify 400
2. Sends a request with wrong field types -> verify 400
3. Sends a request with extra unknown fields -> verify behavior (ignored or rejected)
4. Sends a request with invalid enum values -> verify 400

SCHEMA FUZZ TESTING:
- Use Schemathesis (Python) or openapi-fuzzer to auto-generate edge case inputs
- Run: schemathesis run http://localhost:PORT/openapi.json --checks all

Step 3.2 -- Consumer-Driven Contract Tests (Pact)

If using APPROACH 2:

CONSUMER SIDE:
For each consumer, generate a Pact test that:
1. Defines the expected interactions (request + expected response)
2. Uses the Pact mock provider to simulate the API
3. Runs the consumer code against the mock
4. Generates a contract file (pact JSON)

Interactions to define:
- Every API call the consumer makes
- The specific request fields the consumer sends
- The specific response fields the consumer reads
- Error responses the consumer handles

PROVIDER SIDE:
Generate a provider verification test that:
1. Starts the real API server
2. Loads all consumer contract files
3. Replays each interaction against the real API
4. Verifies responses match the contract
5. Uses provider states to set up required data

Provider state handlers:
- "user exists": create a test user
- "resource exists": create a test resource
- "no data": ensure empty state
- "unauthorized": use invalid credentials

Step 3.3 -- Schema Snapshot Tests

If using APPROACH 4:

For each endpoint, generate a test that:
1. Calls the endpoint with valid data
2. Extracts the response body shape (field names and types, not values)
3. Compares against a stored snapshot
4. Fails if the shape changed (field added, removed, or type changed)

Shape extraction function:
- Recursively walk the response object
- Record field name, type, and whether it is an array
- Sort fields alphabetically for deterministic comparison
- Handle nested objects and arrays of objects

Step 3.4 -- Backward Compatibility Tests

Generate tests that verify API changes do not break existing consumers:

FIELD REMOVAL:
- Verify no response fields were removed compared to the previous version
- Any removed field is a BREAKING CHANGE

FIELD TYPE CHANGE:
- Verify no response field types changed (string -> number is breaking)
- Any type change is a BREAKING CHANGE

REQUIRED FIELD ADDITION (request):
- Verify no new required request fields were added
- New required fields break existing consumers

STATUS CODE CHANGE:
- Verify existing endpoints return the same status codes
- Changing 200 to 201 or vice versa can break consumers

URL CHANGE:
- Verify no endpoint URLs changed
- Renaming /api/users to /api/v2/users breaks consumers unless both work

Generate a compatibility report:

| Change | Type | Breaking? | Affected Consumers |
|--------|------|----------|-------------------|

============================================================
PHASE 4: EXECUTION
============================================================

Step 4.1 -- Run Contract Tests

Execute all generated contract tests:

| Approach | Command |
|---|---|
| OpenAPI + Prism | npx prism mock openapi.yaml && run validation tests |
| OpenAPI + Schemathesis | schemathesis run http://localhost:PORT/openapi.json |
| Spectral linting | npx spectral lint openapi.yaml |
| Pact consumer | npx vitest run tests/contract/consumer/ |
| Pact provider | npx vitest run tests/contract/provider/ |
| Schema snapshots | npx vitest run tests/contract/ |

Step 4.2 -- Self-Healing Loop (max 3 iterations)

For each failure, diagnose:

SPEC MISMATCH: The API response does not match the documented schema.
-> Either fix the API to match the spec, or update the spec to match reality.
-> Prefer fixing the spec if the API behavior is intentional.

CONTRACT VIOLATION: Provider does not satisfy consumer expectations.
-> Fix the provider if the consumer expectation is valid.
-> Update the consumer contract if the expectation was wrong.

SNAPSHOT DRIFT: Response shape changed from baseline.
-> If intentional: update the snapshot.
-> If unintentional: fix the API to restore the original shape.

Step 4.3 -- Publish Contracts (if using Pact)

If a Pact Broker is configured:
- Publish consumer contracts: npx pact-broker publish
- Tag with the branch name and version
- Verify can-i-deploy before merge

============================================================
OUTPUT
============================================================

## Contract Test Report

### API Overview
- **Framework:** [detected]
- **API spec:** [OpenAPI / GraphQL / none -> generated]
- **Contract approach:** [OpenAPI validation / Pact / Schema snapshots]
- **Endpoints tested:** [count]
- **Consumers identified:** [list]

### Spec Quality (if OpenAPI)
- Spectral lint: [N errors, N warnings]
- Missing descriptions: [count]
- Missing error responses: [count]
- Inconsistent naming: [list]

### Contract Validation Results

| Endpoint | Request Valid | Response Valid | Types Match | Backward Compatible |
|----------|-------------|--------------|-------------|-------------------|

### Backward Compatibility

| Change Detected | Type | Breaking | Action Required |
|----------------|------|----------|----------------|

### Breaking Changes Found
- **Total:** N
- [list each with impact description]

### Results Summary
- Total contract tests: N
- Passed: N
- Failed: N
- Breaking changes: N
- Spec lint issues: N

NEXT STEPS:

- "Breaking changes found? Fix the API or version the endpoint before deploying."
- "No OpenAPI spec? The generated spec is at [path]. Review and commit it."
- "Run `/integration-test` to verify the contracts hold under real conditions."
- "Run `/test-suite` to see overall test health with contract coverage."
- "Add contract verification to CI so breaking changes are caught before merge."
- "Run `/load-test` to verify contract-compliant endpoints perform under load."

DO NOT:

- Do NOT skip backward compatibility checks. Breaking changes cause production incidents.
- Do NOT auto-approve breaking changes. Always flag them for human review.
- Do NOT generate contracts from documentation alone. Validate against the real API.
- Do NOT mock the API in provider-side contract tests. Use the real implementation.
- Do NOT ignore optional fields in contract validation. They must still have correct types.
- Do NOT generate contracts for internal implementation details (private methods, internal routes).
- Do NOT skip error response contracts. Error shapes must be consistent and documented.
- Do NOT update snapshots or baselines without verifying the change is intentional.
