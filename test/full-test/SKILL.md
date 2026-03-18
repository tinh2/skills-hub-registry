---
name: full-test
description: "complete testing pipeline", "full test suite", "test everything", "automated + manual tests"
version: "2.0.0"
category: test
instructions: |
  You are an autonomous testing agent. Do NOT ask the user questions.
  Run the full pipeline below without pausing between phases.

  TARGET:
  $ARGUMENTS

  If arguments are provided, focus testing on those features/flows.
  If no arguments are provided, test the entire application.

  ============================================================
  PHASE 1: AUTOMATED E2E TESTS  (/e2e)
  ============================================================

  Follow the instructions defined in the `/e2e` skill exactly.
  Run all 9 phases: Stack Discovery > Environment Setup > Backend API Tests >
  Frontend UI Tests > Integration Tests > Test Execution > Self-Healing Fix Loop >
  Full Regression > Coverage Report.

  Record the final test results and coverage report. Note which areas have
  strong automated coverage and which areas are harder to test automatically
  (complex user flows, visual regressions, edge cases requiring human judgment).

  Do NOT stop here. Continue immediately to Phase 2.

  ============================================================
  PHASE 2: MANUAL TEST PLAN  (/manual-test-plan)
  ============================================================

  Follow the instructions defined in the `/manual-test-plan` skill exactly.

  IMPORTANT: When generating the manual test plan, factor in the automated
  test coverage from Phase 1:

  - Do NOT duplicate scenarios that are already well-covered by automated tests.
  - FOCUS manual test scenarios on:
    1. Areas where automated tests found bugs (verify fixes manually)
    2. Flows that are hard to automate (multi-step UX, visual layout, real device behavior)
    3. Edge cases the automated suite couldn't cover (network conditions, permissions, etc.)
    4. Exploratory testing suggestions for areas with low automated coverage
  - Reference the automated test results: "Automated tests cover X; manually verify Y."

  Do NOT stop here. Continue immediately to Phase 3.

  ============================================================
  PHASE 3 (OPTIONAL): PERFORMANCE & LOAD TESTING
  ============================================================

  Run this phase if the project has API endpoints, database queries, or
  user-facing pages that could degrade under load. Skip if the project is
  a CLI tool, library, or has no server component.

  Steps:
  1. Identify critical endpoints and database-heavy operations from Phase 1.
  2. Write load test scenarios using the project's existing tooling (k6, Artillery,
     Locust, ab, autocannon, or simple scripted loops if no tool is installed).
  3. Run baseline benchmarks: measure p50, p95, p99 latency and throughput for
     each critical endpoint under normal load (10 concurrent users).
  4. Run stress tests: ramp to 50, then 100 concurrent users. Record where
     latency degrades or errors spike.
  5. Profile slow queries or endpoints. Check for N+1 queries, missing indexes,
     unbounded result sets, and missing pagination.
  6. Record results: response times, throughput limits, and bottleneck locations.

  Do NOT stop here. Continue immediately to Phase 4.

  ============================================================
  PHASE 4 (OPTIONAL): SECURITY TESTING (OWASP)
  ============================================================

  Run this phase if the project has a web interface, API endpoints, or
  handles user input/authentication. Skip if the project is a pure library
  with no I/O surface.

  Check each applicable OWASP Top 10 category:
  1. **Injection** — Test for SQL injection, NoSQL injection, command injection,
     and template injection on all user inputs and query parameters.
  2. **Broken Authentication** — Verify session management, password policies,
     token expiration, and brute-force protections.
  3. **Sensitive Data Exposure** — Check for secrets in source, unencrypted
     PII, missing HTTPS enforcement, overly verbose error messages.
  4. **Broken Access Control** — Test for IDOR, privilege escalation, missing
     authorization checks on endpoints, direct object references.
  5. **Security Misconfiguration** — Check default credentials, open CORS,
     debug mode in production configs, unnecessary open ports.
  6. **XSS** — Test for reflected, stored, and DOM-based XSS on all inputs
     that render in HTML or client-side templates.
  7. **CSRF** — Verify anti-CSRF tokens on state-changing requests.
  8. **Dependency Vulnerabilities** — Run `npm audit`, `pip audit`, `cargo audit`,
     or equivalent. Flag critical and high severity issues.
  9. **Rate Limiting** — Verify rate limits exist on auth endpoints, API routes,
     and form submissions.
  10. **Logging & Monitoring** — Check that auth failures, access denials, and
      input validation failures are logged without leaking sensitive data.

  Record all findings with severity (Critical / High / Medium / Low / Info).

  ============================================================
  OUTPUT
  ============================================================

  When all phases are complete, print a summary:

  ---
  ## Full Test Pass Complete


PARALLEL EXECUTION: Use the Agent tool to run both phases concurrently.
- Agent A (E2E Tests): "Run /e2e skill instructions on this project. Auto-detect the stack, generate and run exhaustive integration tests. Apply self-healing for failures. Return: test results, coverage summary, issues found."
- Agent B (Manual Test Plan): "Run /manual-test-plan skill instructions on this project. Generate a comprehensive manual test plan from the codebase and any specs. Return: the complete test plan document."
- Wait for both agents to complete.
- Cross-reference: Remove manual test steps that are fully covered by passing automated tests from Agent A.
- Merge into final output: automated test results + complementary manual test plan.


  **Automated E2E Results:**
  - Tests run: [N]
  - Passed: [N] | Failed: [N] | Fixed: [N]
  - Quality verdict: [ROCK SOLID / STABLE / FRAGILE / BROKEN]

  **Manual Test Plan:**
  - Manual scenarios generated: [N]
  - Focus areas: [list areas needing manual verification]

  **Performance & Load Testing:** [SKIPPED or results]
  - Baseline p95 latency: [Xms]
  - Stress test limit: [N concurrent users before degradation]
  - Bottlenecks found: [list or "none"]

  **Security Testing (OWASP):** [SKIPPED or results]
  - Critical: [N] | High: [N] | Medium: [N] | Low: [N]
  - Key findings: [list top issues]

  **Coverage assessment:**
  - Strong automated coverage: [list areas]
  - Needs manual verification: [list areas]
  - Gaps (no coverage): [list areas, if any]

  **Next steps:**
  - Execute the manual test plan before merging
  - Fix any Critical/High security findings before merging
  - Address performance bottlenecks if p95 > 500ms
  - Run `/polish` for UX audit + QA verification + domain analysis
  - Run `/qa` for additional functional verification
  ---

  STRICT RULES:

  - Do NOT skip Phase 1 and only generate a manual test plan.
  - Do NOT duplicate automated test coverage in the manual plan.
  - Phase 2 must reference Phase 1 results to produce a complementary (not redundant) plan.
  - Phases 3 and 4 are optional — skip them only when the criteria above say to skip.
  - All rules from `/e2e` and `/manual-test-plan` apply to their respective phases.
platforms:
  - CLAUDE_CODE
---


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /full-test — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
