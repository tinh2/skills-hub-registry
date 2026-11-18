# QA

Quality assurance, performance profiling, chaos engineering, code smell detection, and pre-deploy verification.

## Main Skill

**[qa](qa/)** -- Automated QA agent that starts the app, walks through every screen and API endpoint, verifies functionality, evaluates design and usability, runs domain analysis, and fixes issues found.

## Skills (15)

| Skill | Version | Description |
|-------|---------|-------------|
| [qa](qa/) | 3.1.0 | Main skill. Automated QA agent that walks every screen/endpoint, verifies, evaluates design, runs domain analysis, fixes issues |
| [iterate-review](iterate-review/) | 5.0.0 | Autonomously reviews and improves existing code through up to 5 iterations of analysis and fixing |
| [audit](audit/) | 2.0.0 | Lightweight domain consistency audit -- verify all layers match and fix issues. Fast gate between pipeline phases |
| [preflight](preflight/) | 1.1.0 | Pre-deploy verification gate -- checks git status, build, tests, migrations, and commit conventions. Read-only |
| [perf](perf/) | 1.0.0 | Performance profiler -- analyzes DB queries, API call chains, frontend widget rebuilds, and bundle sizes |
| [chaos](chaos/) | 1.0.0 | Chaos engineering for application resilience. Identifies failure points, generates chaos tests, validates graceful degradation |
| [code-smell](code-smell/) | 1.0.0 | Detects Martin Fowler's catalog of code smells across the codebase with severity and recommended refactoring |
| [dead-code](dead-code/) | 1.0.0 | Detects and safely removes dead code -- unreachable paths, unused exports, unused dependencies, unused CSS |
| [migration-verify](migration-verify/) | 1.0.0 | Verifies database migrations are safe -- applies cleanly, reverses cleanly, preserves data integrity, is idempotent |
| [stress-test-personas](stress-test-personas/) | 1.0.0 | Applies 6 adversarial decision-maker personas to stress-test the product and architecture from different strategic angles |
| [balance-test](balance-test/) | 1.0.0 | Game balance testing with DPS calculations, TTK analysis, win rate simulation, character/weapon tier analysis, economy stress testing, progression pacing, and Monte Carlo simulation for RNG systems |
| [game-qa](game-qa/) | 1.0.0 | Automated game QA covering scene loading validation, null reference detection, boundary testing, input rebinding verification, save/load integrity, localization completeness, and platform compliance |
| [mobile-qa](mobile-qa/) | 1.0.0 | Comprehensive mobile QA -- permission flows, deep link verification, push notification testing, offline mode, background transitions, memory leak detection, network simulation, accessibility audit, and platform edge cases |

## Usage

- Full app verification (API + UI + domain analysis): `/qa`
- Iterative code improvement (up to 5 passes): `/iterate-review`
- Quick domain consistency check: `/audit`
- Pre-deploy verification gate: `/preflight`
- Performance profiling and optimization: `/perf`
- Resilience and failure mode testing: `/chaos`
- Code smell detection and refactoring guidance: `/code-smell`
- Dead code removal: `/dead-code`
- Database migration safety check: `/migration-verify`
- Adversarial persona stress testing: `/stress-test-personas`
- Game balance testing and simulation: `/balance-test`
- Automated game QA validation: `/game-qa`
- Mobile platform QA (permissions, deep links, push): `/mobile-qa`

## Recently Added

| Skill | Version | Description |
|-------|---------|-------------|
| [broken-links](broken-links/) | 1.1.0 | Scan a codebase for broken links — dead URLs in Markdown/HTML, broken file references, invalid import paths, stale anchor links, and broken cross-doc references — then auto-fix... |
| [scale-audit](scale-audit/) | 1.0.0 | Scalability audit — identifies performance bottlenecks, unbounded queries, N+1 patterns, missing indexes, synchronous blocking operations on hot paths, and memory pressure points.... |

<!-- BEGIN GENERATED: skills-hub-index (scripts/gen-index.mjs, do not edit by hand) -->
## All Qa skills on skills-hub.ai

Each skill page on skills-hub.ai shows ratings and reviews, install counts, a one-command install, and related skills. 18 of 18 skills in this folder have a page. You can also [browse the Qa category on skills-hub.ai](https://skills-hub.ai/browse?category=qa), which includes skills from other publishers.

| Skill | Description | Page |
|-------|-------------|------|
| [audit](audit/) | Fast quality gate — detects stack, runs static analysis, checks cross-layer consistency, fixes issues. | [View on skills-hub](https://skills-hub.ai/skills/audit) |
| [balance-test](balance-test/) | Analyze game balance by extracting stats from code and running mathematical simulations. | [View on skills-hub](https://skills-hub.ai/skills/balance-test) |
| [broken-links](broken-links/) | Scan a codebase for broken links — dead URLs in Markdown/HTML, broken file references, invalid import paths, stale anchor links, and... | [View on skills-hub](https://skills-hub.ai/skills/broken-links) |
| [browser-agent-verify](browser-agent-verify/) | Verifies front-end changes by driving a real browser — spins up the local dev server, navigates to the changed route, executes the... | [View on skills-hub](https://skills-hub.ai/skills/browser-agent-verify) |
| [bug-triage](bug-triage/) | Turn a pile of bugs, issues, and error reports into a ranked, actionable plan with reproduction evidence. | [View on skills-hub](https://skills-hub.ai/skills/bug-triage) |
| [chaos](chaos/) | Chaos engineering analysis that maps every external dependency and I/O boundary, then generates tests for timeouts, connection failures,... | [View on skills-hub](https://skills-hub.ai/skills/chaos) |
| [code-smell](code-smell/) | Scan codebase for Martin Fowler's catalog of code smells: god classes, long methods, feature envy, data clumps, primitive obsession,... | [View on skills-hub](https://skills-hub.ai/skills/code-smell) |
| [dead-code](dead-code/) | Find and safely remove dead code: unreachable paths, unused exports, unused functions, unused variables, unused CSS selectors, unused... | [View on skills-hub](https://skills-hub.ai/skills/dead-code) |
| [game-qa](game-qa/) | Run a full game QA audit on Unity, Unreal, Godot, or web game projects. | [View on skills-hub](https://skills-hub.ai/skills/game-qa) |
| [iterate-review](iterate-review/) | Autonomously review and improve existing code through up to 5 iterations of analysis, domain verification, fixing, and validation. | [View on skills-hub](https://skills-hub.ai/skills/iterate-review) |
| [migration-verify](migration-verify/) | Verify database migrations are safe before running them. | [View on skills-hub](https://skills-hub.ai/skills/migration-verify) |
| [mobile-qa](mobile-qa/) | Run a comprehensive mobile app QA audit covering permission flows, deep link verification, push notification delivery, offline mode... | [View on skills-hub](https://skills-hub.ai/skills/mobile-qa) |
| [perf](perf/) | Performance profiler — analyzes DB queries (any ORM), API call chains, memory usage, bundle sizes, network waterfalls, and frontend... | [View on skills-hub](https://skills-hub.ai/skills/perf) |
| [preflight](preflight/) | Pre-deploy verification gate. Checks git status, build, tests, migrations, secrets, and commit conventions. | [View on skills-hub](https://skills-hub.ai/skills/preflight) |
| [qa](qa/) | Automated QA agent that starts the app, walks through every screen and API endpoint, verifies functionality, evaluates modern design and... | [View on skills-hub](https://skills-hub.ai/skills/qa) |
| [root-cause](root-cause/) | Hypothesis-driven debugging that ends at a proven root cause, not a symptom patch. | [View on skills-hub](https://skills-hub.ai/skills/root-cause) |
| [scale-audit](scale-audit/) | Scalability audit — identifies performance bottlenecks, unbounded queries, N+1 patterns, missing indexes, synchronous blocking... | [View on skills-hub](https://skills-hub.ai/skills/scale-audit) |
| [stress-test-personas](stress-test-personas/) | Stress-test your product through 6 adversarial decision-maker personas -- skeptical board member, activist investor, power user, churned... | [View on skills-hub](https://skills-hub.ai/skills/stress-test-personas) |
<!-- END GENERATED: skills-hub-index -->
