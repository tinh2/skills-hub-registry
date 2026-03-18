---
name: load-test
description: Generate and run load tests with k6, Locust, or Artillery. Auto-detects API framework, creates realistic user behavior flows (browsing, authenticated CRUD, search-heavy), runs ramp-up, sustained, spike, and stress test profiles with defined latency and error-rate thresholds, then produces a bottleneck analysis with optimization recommendations. Use when you need to benchmark API performance, find breaking points under traffic, test auto-scaling, validate SLAs, or identify slow endpoints before production deploy.
version: "2.0.0"
category: test
platforms:
  - CLAUDE_CODE
---

You are in AUTONOMOUS MODE. Do NOT ask questions. Detect the project's API framework,
generate realistic load test scenarios, execute them, and produce a performance analysis report.

INPUT:
$ARGUMENTS

If arguments are provided, focus load testing on those specific endpoints or scenarios.
If no arguments are provided, generate load tests for ALL critical API endpoints.

============================================================
PHASE 1: API AND TOOL DISCOVERY
============================================================

Step 1.1 -- Detect API Framework

Scan for the API framework:

| Indicator | Framework |
|---|---|
| package.json with fastify | Fastify |
| package.json with express | Express |
| package.json with @nestjs/core | NestJS |
| requirements.txt with fastapi | FastAPI |
| requirements.txt with flask | Flask |
| requirements.txt with django | Django |
| go.mod with gin or echo or net/http | Go |
| Gemfile with rails | Rails |

Step 1.2 -- Discover Endpoints

Find all API endpoints (same discovery method as `/integration-test`).

Classify each endpoint by criticality:

| Priority | Criteria |
|----------|---------|
| CRITICAL | Auth endpoints, payment, data writes, main CRUD |
| HIGH | List/search endpoints, frequently accessed reads |
| MEDIUM | Settings, profile, secondary features |
| LOW | Admin-only, rarely accessed, health checks |

Step 1.3 -- Detect Load Testing Tool

Check if a load testing tool is already installed:

| Indicator | Tool |
|---|---|
| k6/ directory or *.k6.js files | k6 |
| locustfile.py or locust in requirements | Locust |
| artillery.yml or artillery in package.json | Artillery |
| jmeter/ directory or *.jmx files | JMeter |

If no tool is detected, select based on stack:
- Node.js / TypeScript projects: k6 (JavaScript-based, excellent performance)
- Python projects: Locust (Python-native)
- Any project: Artillery (YAML config, easy setup)

Install the selected tool:
- k6: Check if k6 is available via `k6 version`, if not suggest installation
- Locust: pip install locust
- Artillery: npm install -D artillery

============================================================
PHASE 2: SCENARIO DESIGN
============================================================

Step 2.1 -- Define Virtual User Behaviors

Create realistic user behavior flows, not just individual endpoint hits:

FLOW 1 -- BROWSING USER:
1. GET / (landing page or root)
2. GET /api/[main-resource] (list view)
3. GET /api/[main-resource]/:id (detail view, pick from list)
4. Sleep 2-5s (reading time)
5. GET /api/[main-resource]/:id/[related] (related data)
6. Repeat steps 2-5 with different resources

FLOW 2 -- AUTHENTICATED USER:
1. POST /api/auth/login (obtain token)
2. GET /api/[user-resource] (user's data)
3. POST /api/[main-resource] (create something)
4. PUT /api/[main-resource]/:id (update it)
5. GET /api/[main-resource] (verify in list)
6. DELETE /api/[main-resource]/:id (cleanup)

FLOW 3 -- SEARCH-HEAVY USER:
1. GET /api/search?q=[term1] (broad search)
2. GET /api/search?q=[term2]&filter=[value] (filtered search)
3. GET /api/[resource]?sort=created&order=desc (sorted list)
4. GET /api/[resource]?page=2&limit=20 (pagination)

FLOW 4 -- API CONSUMER (if B2B/API product):
1. Rapid sequential API calls with different parameters
2. Batch operations if supported
3. Webhook delivery simulation

Use realistic think times between requests (1-5 seconds for humans, 100-500ms for API consumers).

Step 2.2 -- Define Load Profiles

Generate four standard load profiles:

RAMP-UP TEST:
- Start: 1 virtual user (VU)
- Ramp to target VUs over 2 minutes
- Hold at target for 5 minutes
- Ramp down over 1 minute
- Purpose: Find the performance baseline under normal load

SUSTAINED LOAD TEST:
- Constant load at expected peak traffic
- Duration: 10 minutes
- Purpose: Verify stability under sustained traffic

SPIKE TEST:
- Normal load for 2 minutes
- Sudden spike to 5x normal load for 1 minute
- Return to normal for 2 minutes
- Spike again to 10x for 30 seconds
- Return to normal for 2 minutes
- Purpose: Test auto-scaling and recovery

STRESS TEST:
- Start at normal load
- Increase by 20% every 2 minutes until failure
- Record the breaking point
- Purpose: Find system limits and failure modes

Step 2.3 -- Define Thresholds

Set pass/fail thresholds:

| Metric | Threshold |
|--------|----------|
| HTTP error rate | < 1% |
| p95 response time | < 500ms |
| p99 response time | < 2000ms |
| Median response time | < 200ms |
| Requests per second (sustained) | > [baseline from ramp-up] |
| Failed requests | 0 for non-stress tests |

Adjust thresholds based on endpoint type:
- Read endpoints: stricter latency (p95 < 200ms)
- Write endpoints: allow higher latency (p95 < 1000ms)
- Search endpoints: moderate (p95 < 500ms)
- File upload endpoints: lenient (p95 < 5000ms)

============================================================
PHASE 3: TEST GENERATION
============================================================

Step 3.1 -- Generate Test Scripts

FOR K6 (JavaScript):

Create k6/scenarios/ directory with:
- ramp-up.js: Ramp-up test with ramping-vus executor
- sustained.js: Constant load with constant-vus executor
- spike.js: Spike test with ramping-vus executor
- stress.js: Stress test with ramping-arrival-rate executor
- helpers/auth.js: Login helper, token management
- helpers/data.js: Test data generators (realistic names, emails, etc.)

Each script must:
- Use k6 groups to organize requests logically
- Include checks (response status, body content, response time)
- Use thresholds for pass/fail criteria
- Include realistic headers (User-Agent, Accept, Content-Type)
- Use parameterized data from CSV or JSON files

FOR LOCUST (Python):

Create locust/ directory with:
- locustfile.py: Main test with user classes
- scenarios/browsing.py: Browsing user behavior
- scenarios/authenticated.py: Authenticated user flows
- scenarios/search.py: Search-heavy user behavior
- helpers/auth.py: Authentication helper
- helpers/data.py: Test data generators

Each user class must:
- Use @task decorators with weights
- Include wait_time (between, constant)
- Handle auth token lifecycle
- Use on_start for login

FOR ARTILLERY (YAML + JS):

Create artillery/ directory with:
- ramp-up.yml: Ramp-up scenario
- sustained.yml: Sustained load scenario
- spike.yml: Spike test scenario
- stress.yml: Stress test scenario
- functions.js: Custom JS functions for data generation and auth
- data/users.csv: Test user data

Each config must:
- Define phases with duration and arrivalRate
- Use scenarios with weighted flows
- Include custom metrics capture
- Set ensure thresholds

Step 3.2 -- Generate Test Data

Create realistic test data files:

- users.csv or users.json: 100+ unique test users with realistic data
- search-terms.json: 50+ realistic search queries
- resource-data.json: Sample payloads for POST/PUT endpoints

Test data rules:
- Use realistic but clearly fake data (e.g., "loadtest-user-001@example.com")
- Include variety (different string lengths, numeric ranges)
- Include edge cases in data (unicode, special chars, max-length values)
- Never use production data or real credentials

============================================================
PHASE 4: EXECUTION
============================================================

Step 4.1 -- Pre-flight Checks

Before running load tests:
- Verify the API server is running and responding
- Verify test data endpoints are accessible
- Run a single-user dry run of each scenario to catch script errors
- Confirm no rate limiting is enabled on the test environment

Step 4.2 -- Run Tests

Execute in this order:
1. Ramp-up test (establish baseline)
2. Sustained load test (verify stability)
3. Spike test (verify resilience)
4. Stress test (find breaking point)

Run commands:

| Tool | Command |
|---|---|
| k6 | k6 run --out json=results/[test].json k6/scenarios/[test].js |
| Locust | locust -f locust/locustfile.py --headless -u [users] -r [rate] -t [time] --csv=results/[test] |
| Artillery | artillery run artillery/[test].yml -o results/[test].json |

Capture output for each test run.

Step 4.3 -- Results Collection

Parse results from each test run and extract:

- Total requests sent
- Requests per second (avg, min, max)
- Response times (min, median, p95, p99, max)
- Error rate (% of non-2xx responses)
- Error breakdown by status code
- Data transferred
- Virtual users at peak
- Threshold pass/fail status


============================================================
SELF-HEALING VALIDATION (max 3 iterations)
============================================================

After generating and running tests, validate:

1. All generated test files compile/parse without syntax errors.
2. Run the generated tests — capture pass/fail results.
3. If tests fail due to test code bugs (not application bugs), fix the test code.
4. Re-run to confirm tests pass or legitimately fail on application issues.
5. Repeat up to 3 iterations.

IF STILL FAILING after 3 iterations:
- Separate test failures into: test bugs vs application bugs
- Fix test bugs, document application bugs

============================================================
OUTPUT
============================================================

## Load Test Report

### Environment
- **API Framework:** [detected]
- **Load Testing Tool:** [selected]
- **Target URL:** [base URL]
- **Endpoints tested:** [count]

### Endpoints Under Test

| Endpoint | Method | Priority | Auth Required |
|----------|--------|----------|--------------|

### Results by Test Profile

#### Ramp-Up Test (Baseline)
| Metric | Value | Threshold | Status |
|--------|-------|----------|--------|
| Total requests | N | - | - |
| Avg RPS | N | - | - |
| Median latency | Nms | < 200ms | PASS/FAIL |
| p95 latency | Nms | < 500ms | PASS/FAIL |
| p99 latency | Nms | < 2000ms | PASS/FAIL |
| Error rate | N% | < 1% | PASS/FAIL |

#### Sustained Load Test
[same table format]

#### Spike Test
[same table format + recovery time metric]

#### Stress Test
- **Breaking point:** N concurrent VUs / N RPS
- **Failure mode:** [what happened -- timeouts, 5xx, connection refused]
- **Recovery:** [did the system recover after load reduced?]

### Endpoint Performance Breakdown

| Endpoint | Median | p95 | p99 | Error Rate | Bottleneck? |
|----------|--------|-----|-----|-----------|------------|

### Bottleneck Analysis
- **Slowest endpoints:** [list with latency]
- **Highest error rate:** [list with rates]
- **Likely bottlenecks:** [database queries, external APIs, CPU, memory]
- **Recommendations:** [caching, connection pooling, query optimization, indexing]

### Performance Grade
- **FAST:** All thresholds pass, p95 < 200ms, handles 2x expected load
- **ACCEPTABLE:** All thresholds pass under normal load, some degradation at peak
- **SLOW:** Some thresholds fail under normal load, optimization needed
- **CRITICAL:** Significant failures under expected load, requires immediate attention

NEXT STEPS:

- "Performance bottlenecks found? Run `/perf` for detailed performance optimization."
- "Run `/integration-test` to verify correctness under normal conditions."
- "Run `/test-suite` to see overall test health including load test coverage."
- "Set up CI integration to run load tests on every deploy."

DO NOT:

- Do NOT run load tests against production environments.
- Do NOT use real user credentials or PII in test data.
- Do NOT run stress tests without confirming the target is a test/staging environment.
- Do NOT set unrealistic thresholds (sub-millisecond for complex queries).
- Do NOT generate tests that only hit a single URL repeatedly. Test realistic user flows.
- Do NOT skip the dry run. Script errors under load are hard to diagnose.
- Do NOT ignore error responses. Investigate every non-2xx status code.
- Do NOT report raw numbers without context. Always compare against thresholds.


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /load-test — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
