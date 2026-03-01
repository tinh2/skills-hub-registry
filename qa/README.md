# QA

Quality assurance, performance profiling, chaos engineering, code smell detection, and pre-deploy verification.

## Main Skill

**[qa](qa/)** -- Automated QA agent that starts the app, walks through every screen and API endpoint, verifies functionality, evaluates design and usability, runs domain analysis, and fixes issues found.

## Skills (10)

| Skill | Version | Description |
|-------|---------|-------------|
| [qa](qa/) | 3.0.0 | Main skill. Automated QA agent that walks every screen/endpoint, verifies, evaluates design, runs domain analysis, fixes issues |
| [iterate-review](iterate-review/) | 5.0.0 | Autonomously reviews and improves existing code through up to 5 iterations of analysis and fixing |
| [audit](audit/) | 2.0.0 | Lightweight domain consistency audit -- verify all layers match and fix issues. Fast gate between pipeline phases |
| [preflight](preflight/) | 1.0.0 | Pre-deploy verification gate -- checks git status, build, tests, migrations, and commit conventions. Read-only |
| [perf](perf/) | 1.0.0 | Performance profiler -- analyzes DB queries, API call chains, frontend widget rebuilds, and bundle sizes |
| [chaos](chaos/) | 1.0.0 | Chaos engineering for application resilience. Identifies failure points, generates chaos tests, validates graceful degradation |
| [code-smell](code-smell/) | 1.0.0 | Detects Martin Fowler's catalog of code smells across the codebase with severity and recommended refactoring |
| [dead-code](dead-code/) | 1.0.0 | Detects and safely removes dead code -- unreachable paths, unused exports, unused dependencies, unused CSS |
| [migration-verify](migration-verify/) | 1.0.0 | Verifies database migrations are safe -- applies cleanly, reverses cleanly, preserves data integrity, is idempotent |
| [stress-test-personas](stress-test-personas/) | 1.0.0 | Applies 6 adversarial decision-maker personas to stress-test the product and architecture from different strategic angles |

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
