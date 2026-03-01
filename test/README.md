# Test

Automated testing across every layer -- unit, integration, E2E, load, contract, accessibility, and visual regression.

## Main Skill

**[test-suite](test-suite/)** -- Analyzes test coverage across all testing types, identifies gaps, routes to the appropriate sub-skills, and produces a health report with scores per category. Start here if you are unsure which test type you need.

## Skills (9)

| Skill | Version | Description |
|-------|---------|-------------|
| [test-suite](test-suite/) | 1.0.0 | Main orchestrator. Analyzes test coverage, identifies gaps, routes to sub-skills, produces health report |
| [unit-test](unit-test/) | 1.0.0 | Auto-detects test framework, scans for untested functions, generates unit tests with edge cases, runs and self-heals |
| [e2e](e2e/) | 1.0.0 | Auto-detects any tech stack, generates exhaustive end-to-end integration tests with self-healing |
| [integration-test](integration-test/) | 1.0.0 | Auto-detects framework, generates integration tests for APIs, databases, and service interactions |
| [load-test](load-test/) | 1.0.0 | Auto-detects API framework, generates realistic load test scenarios with k6/Locust/Artillery |
| [contract-test](contract-test/) | 1.0.0 | Auto-detects API framework, generates consumer-driven contract tests using Pact or OpenAPI validation |
| [accessibility-test](accessibility-test/) | 1.0.0 | Auto-detects frontend framework, sets up axe-core and Lighthouse CI for automated WCAG 2.1 AA testing |
| [visual-regression](visual-regression/) | 1.0.0 | Auto-detects frontend framework, sets up visual regression testing with baseline screenshots across breakpoints |
| [manual-test-plan](manual-test-plan/) | 2.0.0 | Generates a manual QA test plan based on code changes on the current branch |

## Usage

- Run `/test-suite` to get a full coverage scan and let it route to the right sub-skills
- Run individual sub-skills directly when you know exactly what test type you need
- `/unit-test` for function-level coverage
- `/e2e` for full user journey testing
- `/integration-test` for API and service interaction testing
- `/load-test` for performance and scalability validation
- `/contract-test` for API contract verification between services
- `/accessibility-test` for WCAG 2.1 AA compliance
- `/visual-regression` for screenshot-based UI drift detection
- `/manual-test-plan` as a final pre-merge step to generate manual QA checklists
- `/full-test` (combo skill) to chain `/e2e` then `/manual-test-plan`
