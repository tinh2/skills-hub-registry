# Test

Automated testing across every layer -- unit, integration, E2E, load, contract, accessibility, and visual regression.

## Main Skill

**[test-suite](test-suite/)** -- Analyzes test coverage across all testing types, identifies gaps, routes to the appropriate sub-skills, and produces a health report with scores per category. Start here if you are unsure which test type you need.

## Skills (13)

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
| [manual-test-plan](manual-test-plan/) | 2.1.0 | Generates a manual QA test plan based on code changes on the current branch |
| [mobile-test](mobile-test/) | 1.0.0 | Auto-detects mobile framework and generates comprehensive tests -- unit tests, widget and UI tests, integration tests, snapshot tests, platform-specific tests, accessibility tests, and device matrix configuration |
| [device-matrix](device-matrix/) | 1.0.0 | Sets up device matrix testing -- Firebase Test Lab, AWS Device Farm, or BrowserStack configuration with device selection strategy, test sharding, result aggregation, flaky test detection, and performance benchmarking |

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
- `/mobile-test` for Flutter/React Native specific test generation
- `/device-matrix` for cross-device cloud testing configuration

## Recently Added

| Skill | Version | Description |
|-------|---------|-------------|
| [full-test](full-test/) | 2.0.0 | Complete testing pipeline — full test suite, test everything, automated and manual tests. |
| [walkthrough](walkthrough/) | 2.0.0 | Run an app walkthrough — launch a Flutter app on a simulator or emulator, generate and run exhaustive integration tests that exercise every screen, button, form, and user flow,... |

<!-- BEGIN GENERATED: skills-hub-index (scripts/gen-index.mjs, do not edit by hand) -->
## All Test skills on skills-hub.ai

Each skill page on skills-hub.ai shows ratings and reviews, install counts, a one-command install, and related skills. 16 of 16 skills in this folder have a page. You can also [browse the Test category on skills-hub.ai](https://skills-hub.ai/browse?category=test), which includes skills from other publishers.

| Skill | Description | Page |
|-------|-------------|------|
| [accessibility-test](accessibility-test/) | Automated WCAG 2.1 AA accessibility testing with axe-core and Lighthouse CI. | [View on skills-hub](https://skills-hub.ai/skills/accessibility-test) |
| [browser-pilot](browser-pilot/) | Deterministic browser automation for testing and scripted web flows using Playwright with accessibility-snapshot navigation. | [View on skills-hub](https://skills-hub.ai/skills/browser-pilot) |
| [contract-test](contract-test/) | Generate consumer-driven contract tests for APIs. | [View on skills-hub](https://skills-hub.ai/skills/contract-test) |
| [device-matrix](device-matrix/) | Configure device matrix testing across real phones, tablets, and emulators. | [View on skills-hub](https://skills-hub.ai/skills/device-matrix) |
| [e2e](e2e/) | Auto-detects any tech stack, generates and runs exhaustive end-to-end tests. | [View on skills-hub](https://skills-hub.ai/skills/e2e) |
| [full-test](full-test/) | Complete testing pipeline — full test suite, test everything, automated and manual tests. | [View on skills-hub](https://skills-hub.ai/skills/full-test) |
| [integration-test](integration-test/) | Generate integration tests for APIs, databases, and external services. | [View on skills-hub](https://skills-hub.ai/skills/integration-test) |
| [load-test](load-test/) | Generate and run load tests with k6, Locust, or Artillery. | [View on skills-hub](https://skills-hub.ai/skills/load-test) |
| [manual-test-plan](manual-test-plan/) | Generates a manual test plan, QA plan, test scenarios, testing checklist, or guidance on how to test changes. | [View on skills-hub](https://skills-hub.ai/skills/manual-test-plan) |
| [mobile-test](mobile-test/) | Generate a complete mobile test suite covering unit, widget, integration, snapshot, accessibility, and platform-specific tests. | [View on skills-hub](https://skills-hub.ai/skills/mobile-test) |
| [tdd-enforcer](tdd-enforcer/) | Enforce strict red-green-refactor test-driven development for a feature. | [View on skills-hub](https://skills-hub.ai/skills/tdd-enforcer) |
| [test-bootstrap](test-bootstrap/) | Take an untested or under-tested repository to a real, running test suite in one pass. | [View on skills-hub](https://skills-hub.ai/skills/test-bootstrap) |
| [test-suite](test-suite/) | Analyze and score test coverage across all testing dimensions -- unit, integration, E2E, load, visual regression, contract, and... | [View on skills-hub](https://skills-hub.ai/skills/test-suite) |
| [unit-test](unit-test/) | Generate comprehensive unit tests with edge cases, error paths, and boundary values. | [View on skills-hub](https://skills-hub.ai/skills/unit-test) |
| [visual-regression](visual-regression/) | Set up visual regression testing with baseline screenshots across breakpoints. | [View on skills-hub](https://skills-hub.ai/skills/visual-regression) |
| [walkthrough](walkthrough/) | Run an app walkthrough — launch a Flutter app on a simulator or emulator, generate and run exhaustive integration tests that exercise... | [View on skills-hub](https://skills-hub.ai/skills/walkthrough) |
<!-- END GENERATED: skills-hub-index -->
