# Combo

Multi-skill chains and pipeline compositions -- automated sequences that run multiple skills without user intervention.

## Skills (34)

| Skill | Version | Chain | Description |
|-------|---------|-------|-------------|
| [polish](polish/) | 3.0.0 | /ux ∥ /codebase-health → /qa → /analyze | Full quality pass with parallel UX + scalability audit |
| [research](research/) | 1.0.0 | /compete → /new-features | Competitive gap analysis + feature ideation |
| [spec](spec/) | 1.0.0 | /mvp → /backend-spec | App analysis + story generation |
| [story](story/) | 1.0.0 | /arch-review → /story-implementer → /pr | Full story lifecycle from review to PR |
| [review-implement](review-implement/) | 1.0.0 | /arch-review → /story-implementer | Review architecture then implement |
| [full-test](full-test/) | 1.0.0 | /e2e → /manual-test-plan | Automated E2E tests + manual test plan |
| [retro](retro/) | 1.0.0 | /recall → /new-features | Dev retrospective + feature ideation |
| [fix-and-ship](fix-and-ship/) | 1.0.0 | /hotfix → /preflight | Emergency fix + deploy verification |
| [secure-ship](secure-ship/) | 1.0.0 | /owasp → /ship → /security-review → /pentest | Security-first build chain |
| [compliance-gate](compliance-gate/) | 1.0.0 | /secure → /gdpr → /dependency-scan → /pentest | Full compliance pass with unified report |
| [full-deploy](full-deploy/) | 1.0.0 | /docker → /github-actions → /monitoring → /preflight | Complete deploy pipeline |
| [design-to-code](design-to-code/) | 1.0.0 | /design-system → /responsive → /dark-mode → /ux | Full design implementation chain |
| [data-pipeline](data-pipeline/) | 1.0.0 | /api-scaffold → /integration-test → /load-test | Data-heavy app setup chain |
| [tech-debt-sprint](tech-debt-sprint/) | 1.0.0 | /tech-debt → /code-smell → /dead-code → /iterate-review | Debt reduction sprint |
| [launch-readiness](launch-readiness/) | 1.0.0 | /cpo-review → /growth-audit → /ux → /secure → /preflight | Full pre-launch quality gate with go/no-go decision |
| [investor-ready](investor-ready/) | 1.0.0 | /cto-review → /cfo-review → /cpo-review → /sales-readiness → /codebase-health | Comprehensive investor due-diligence brief |
| [healthcare-audit](healthcare-audit/) | 1.0.0 | /hipaa → /clinical-data-review → /healthcare-compliance → /security-review | Full healthcare compliance and security audit |
| [fintech-launch](fintech-launch/) | 1.0.0 | /pci-dss → /fintech-api → /fraud-detection → /credit-risk → /preflight | Complete fintech launch readiness pipeline |
| [logistics-optimize](logistics-optimize/) | 1.0.0 | /route-optimizer → /warehouse-ops → /inventory-forecast → /supply-chain-risk → /load-test | Full logistics optimization and stress testing |
| [compliance-suite](compliance-suite/) | 1.0.0 | /regulatory-compliance → /gdpr → /soc2 → /dependency-scan → /pentest | Cross-industry compliance hardening pipeline |
| [public-services-audit](public-services-audit/) | 1.0.0 | /benefits-processing → /benefits-fraud → /government-compliance → /security-review | Government services compliance and fraud audit |
| [education-suite](education-suite/) | 1.0.0 | /dropout-risk → /curriculum-optimizer → /student-personalization → /school-ops | Complete education system analysis pipeline |
| [housing-audit](housing-audit/) | 1.0.0 | /affordable-housing → /eviction-risk → /housing-compliance → /rent-burden | Affordable housing compliance and risk assessment |
| [impact-org](impact-org/) | 1.0.0 | /impact-measurement → /fundraising-optimizer → /grant-writer → /donor-retention | Nonprofit operational optimization pipeline |
| [game-launch](game-launch/) | 1.0.0 | /game-performance → /game-qa → /game-accessibility → /game-security → /game-ux | Complete game launch readiness pipeline |
| [game-design-audit](game-design-audit/) | 1.0.0 | /game-design-review → /game-economy → /balance-test → /player-analytics → /game-monetization | Full game design analysis |
| [mobile-launch](mobile-launch/) | 1.0.0 | /mobile-performance → /mobile-qa → /mobile-security-review → /store-compliance → /app-store-optimization | Mobile app launch readiness |
| [mobile-publish](mobile-publish/) | 1.0.0 | /mobile-ci-cd → /app-store-publish → /play-store-publish → /mobile-analytics | Full mobile publishing pipeline |

## Usage

Combo skills chain multiple skills together into automated pipelines. They run sequentially (or in parallel where noted) without user intervention. Each phase passes its output as context to the next.

**Quality:**
- `/polish` -- Full quality pass with parallel UX + scalability audit, then QA and domain analysis
- `/full-test` -- Automated E2E tests with self-healing, then manual test plan for edge cases

**Build + Ship:**
- `/story` -- Full story lifecycle: architecture review, implementation, PR creation
- `/review-implement` -- Review architecture then implement
- `/fix-and-ship` -- Emergency bug fix then pre-deploy verification
- `/secure-ship` -- Security-first build: OWASP scan, build, security review, pentest

**Research + Planning:**
- `/research` -- Competitive gap analysis then feature ideation
- `/spec` -- MVP analysis from video/screenshots then story generation
- `/retro` -- Development retrospective then feature ideation

**Infrastructure:**
- `/full-deploy` -- Containerize, CI/CD, monitoring, pre-deploy checks
- `/compliance-gate` -- Security scan, GDPR, dependency audit, pentest

**Design:**
- `/design-to-code` -- Design system, responsive layout, dark mode, UX audit

**Data:**
- `/data-pipeline` -- API scaffold, integration tests, load tests

**Executive & Strategic:**
- `/launch-readiness` -- Pre-launch quality gate: product review, growth audit, UX, security, preflight
- `/investor-ready` -- Investor due diligence: CTO, CFO, CPO reviews, sales readiness, codebase health

**Industry:**
- `/healthcare-audit` -- Full HIPAA + clinical data + compliance + security audit
- `/fintech-launch` -- PCI DSS + fintech API + fraud detection + credit risk + preflight
- `/logistics-optimize` -- Route optimization + warehouse + inventory + supply chain + load test
- `/compliance-suite` -- Cross-industry regulatory + GDPR + SOC2 + dependency scan + pentest

**Social Impact:**
- `/public-services-audit` -- Benefits processing + fraud detection + government compliance + security review
- `/education-suite` -- Dropout risk + curriculum + personalization + school ops
- `/housing-audit` -- Affordable housing + eviction risk + housing compliance + rent burden
- `/impact-org` -- Impact measurement + fundraising + grant writing + donor retention

**Gaming:**
- `/game-launch` -- Performance + QA + accessibility + security + UX audit
- `/game-design-audit` -- Game design + economy + balance + analytics + monetization review

**Mobile:**
- `/mobile-launch` -- Performance + QA + security + store compliance + ASO
- `/mobile-publish` -- CI/CD + App Store + Play Store + analytics verification

**Maintenance:**
- `/tech-debt-sprint` -- Debt inventory, code smell fixes, dead code removal, review pass

## Recently Added

| Skill | Version | Description |
|-------|---------|-------------|
| [cleanup-sprint](cleanup-sprint/) | 3.0.0 | Deep codebase cleanup — kills dead code, fixes all lint/format warnings, removes orphaned files, cleans stale TODOs, strips security hazards, tightens TypeScript strict mode, and... |
| [design-overhaul](design-overhaul/) | 2.2.0 | Complete autonomous design overhaul — tears down dated patterns and rebuilds with modern CSS, proper tokens, purposeful motion, and production-grade quality. The nuclear option... |
| [design-pipeline](design-pipeline/) | 1.1.0 | Full autonomous design pipeline — builds fast, then the safety net polishes it. Chains: design-setup → design-build → (design-audit ∥ design-optimize) → design-polish →...            |
| [marketing-refresh](marketing-refresh/) | 1.0.0 | Autonomous competitive analysis and feature discovery pipeline. Runs /compete and /new-features on each project, produces actionable market positioning insights. Schedule daily or... |
| [mvp-spec](mvp-spec/) | 2.0.0 | Chains /mvp → /spec — analyzes an app from video/screenshots/description, then generates implementation stories. Triggers: analyze and spec, product analysis to stories, app... |
| [ship-pipeline](ship-pipeline/) | 3.1.0 | Full-stack app pipeline — build, test, review, and deploy across one or ALL repos. Scans CLAUDE.md, MEMORY.md, TODOs, open PRs, and issues for shippable work. Supports 'ship all'... |
| [stitch-pipeline](stitch-pipeline/) | 1.0.0 | >- |

<!-- BEGIN GENERATED: skills-hub-index (scripts/gen-index.mjs, do not edit by hand) -->
## All Combo skills on skills-hub.ai

Each skill page on skills-hub.ai shows ratings and reviews, install counts, a one-command install, and related skills. 39 of 39 skills in this folder have a page. You can also [browse the Combo category on skills-hub.ai](https://skills-hub.ai/browse?category=combo), which includes skills from other publishers.

| Skill | Description | Page |
|-------|-------------|------|
| [cleanup-sprint](cleanup-sprint/) | Deep codebase cleanup — kills dead code, fixes all lint/format warnings, removes orphaned files, cleans stale TODOs, strips security... | [View on skills-hub](https://skills-hub.ai/skills/cleanup-sprint) |
| [compliance-gate](compliance-gate/) | Runs a 4-phase compliance pipeline: security scan, GDPR audit, dependency vulnerability check, and penetration test, producing a unified... | [View on skills-hub](https://skills-hub.ai/skills/compliance-gate) |
| [compliance-suite](compliance-suite/) | Runs a 5-phase enterprise compliance and security hardening pipeline: regulatory review, GDPR audit, SOC 2 evaluation, dependency scan,... | [View on skills-hub](https://skills-hub.ai/skills/compliance-suite) |
| [data-pipeline](data-pipeline/) | Build a production-ready data API from scratch: scaffold REST endpoints with models and validation, generate integration tests that... | [View on skills-hub](https://skills-hub.ai/skills/data-pipeline) |
| [design-overhaul](design-overhaul/) | Complete autonomous design overhaul — tears down dated patterns and rebuilds with modern CSS, proper tokens, purposeful motion, and... | [View on skills-hub](https://skills-hub.ai/skills/design-overhaul) |
| [design-pipeline](design-pipeline/) | Full autonomous design pipeline — builds fast, then the safety net polishes it. | [View on skills-hub](https://skills-hub.ai/skills/design-pipeline) |
| [design-to-code](design-to-code/) | Turn a design into production-quality frontend code: extract a design system with tokens and components, make layouts responsive across... | [View on skills-hub](https://skills-hub.ai/skills/design-to-code) |
| [education-suite](education-suite/) | Comprehensive K-12 or higher-ed system analysis: predict student dropout risk with early warning indicators, optimize curriculum... | [View on skills-hub](https://skills-hub.ai/skills/education-suite) |
| [fintech-launch](fintech-launch/) | Pre-launch compliance and security gate for fintech apps: audit PCI DSS payment card handling, review financial API integrations for... | [View on skills-hub](https://skills-hub.ai/skills/fintech-launch) |
| [fix-and-ship](fix-and-ship/) | Emergency fix-and-deploy pipeline — diagnose a bug, apply a minimal fix, verify safety, deploy to production, and confirm the service is... | [View on skills-hub](https://skills-hub.ai/skills/fix-and-ship) |
| [full-deploy](full-deploy/) | Ship an app from code to production-ready infrastructure: containerize with Docker and multi-stage builds, set up GitHub Actions CI/CD... | [View on skills-hub](https://skills-hub.ai/skills/full-deploy) |
| [game-design-audit](game-design-audit/) | Deep game design health assessment across five dimensions: review core loop and progression systems, analyze in-game economy for... | [View on skills-hub](https://skills-hub.ai/skills/game-design-audit) |
| [game-launch](game-launch/) | Pre-launch quality gate for games: audit rendering and memory performance against platform budgets, run QA for crash-causing defects and... | [View on skills-hub](https://skills-hub.ai/skills/game-launch) |
| [healthcare-audit](healthcare-audit/) | Comprehensive healthcare system compliance and security audit: review HIPAA Privacy and Security Rule adherence, check HITECH and 21st... | [View on skills-hub](https://skills-hub.ai/skills/healthcare-audit) |
| [housing-audit](housing-audit/) | End-to-end affordable housing compliance and risk audit: analyze property management and waitlist operations, predict eviction risk with... | [View on skills-hub](https://skills-hub.ai/skills/housing-audit) |
| [impact-org](impact-org/) | Full nonprofit operational health analysis: validate impact measurement methodology and theory of change, optimize fundraising channels... | [View on skills-hub](https://skills-hub.ai/skills/impact-org) |
| [investor-ready](investor-ready/) | Prepare for fundraising due diligence — runs CTO, CFO, CPO, sales, and codebase health reviews to produce a consolidated investor brief... | [View on skills-hub](https://skills-hub.ai/skills/investor-ready) |
| [launch-kit](launch-kit/) | Build a complete indie launch package for an app, tool, or library — product audit, positioning (one-liner, value props, objection... | [View on skills-hub](https://skills-hub.ai/skills/launch-kit) |
| [issue-to-qa](issue-to-qa/) | Takes one issue to ready for QA: research, lean BE/FE stories, one approval stop, worktree builds, PRs, review bot rounds, dev deploy,... | [View on skills-hub](https://skills-hub.ai/skills/issue-to-qa) |
| [launch-readiness](launch-readiness/) | Run a full pre-launch quality gate before shipping — chains product review, growth audit, UX audit, security scan, and deployment... | [View on skills-hub](https://skills-hub.ai/skills/launch-readiness) |
| [logistics-optimize](logistics-optimize/) | Optimize and stress-test a logistics system end-to-end — chains route optimization, warehouse operations review, inventory demand... | [View on skills-hub](https://skills-hub.ai/skills/logistics-optimize) |
| [marketing](marketing/) | Complete marketing pipeline for apps, dev tools, libraries, and SaaS products in 2026. | [View on skills-hub](https://skills-hub.ai/skills/marketing) |
| [marketing-refresh](marketing-refresh/) | Autonomous competitive analysis and feature discovery pipeline. | [View on skills-hub](https://skills-hub.ai/skills/marketing-refresh) |
| [mobile-launch](mobile-launch/) | Run a complete mobile app pre-launch verification — chains performance audit, QA testing, OWASP mobile security review, App Store and... | [View on skills-hub](https://skills-hub.ai/skills/mobile-launch) |
| [mobile-publish](mobile-publish/) | Set up a complete mobile publishing pipeline — chains CI/CD workflow generation, iOS App Store publishing via Fastlane, Google Play... | [View on skills-hub](https://skills-hub.ai/skills/mobile-publish) |
| [mvp-spec](mvp-spec/) | Chains /mvp → /spec — analyzes an app from video/screenshots/description, then generates implementation stories. | [View on skills-hub](https://skills-hub.ai/skills/mvp-spec) |
| [polish](polish/) | Full quality pass -- chains parallel UX + scalability audit, then QA verification, then consistency gate. | [View on skills-hub](https://skills-hub.ai/skills/polish) |
| [pre-merge](pre-merge/) | One-command PR gate that runs four passes over exactly the changed surface — code review (correctness then simplification), security... | [View on skills-hub](https://skills-hub.ai/skills/pre-merge) |
| [public-services-audit](public-services-audit/) | Audit a government or public services system for compliance, fraud risk, and security — chains benefits processing review, fraud... | [View on skills-hub](https://skills-hub.ai/skills/public-services-audit) |
| [research](research/) | Full-spectrum product research pipeline. Runs competitive analysis, technology trend scouting, user feedback analysis, and feature ideation. | [View on skills-hub](https://skills-hub.ai/skills/research) |
| [retro](retro/) | Run a full retrospective and dev cycle analysis. | [View on skills-hub](https://skills-hub.ai/skills/retro) |
| [review-implement](review-implement/) | Review then build — chains architecture review into implementation. | [View on skills-hub](https://skills-hub.ai/skills/review-implement) |
| [secure-ship](secure-ship/) | Build and ship features with security baked in — runs OWASP Top 10 pre-scan, builds and ships with /ship, validates with post-build... | [View on skills-hub](https://skills-hub.ai/skills/secure-ship) |
| [ship-pipeline](ship-pipeline/) | Full-stack app pipeline — build, test, review, and deploy across one or ALL repos. | [View on skills-hub](https://skills-hub.ai/skills/ship-pipeline) |
| [skill-finder](skill-finder/) | Workflow orchestrator. Decomposes a task into ordered steps, finds or installs the right skill for each step, runs the chain, and offers... | [View on skills-hub](https://skills-hub.ai/skills/skill-finder) |
| [spec](spec/) | Chains /mvp → /backend-spec — analyzes an app from video/screenshots/description, then generates implementation stories from the analysis. | [View on skills-hub](https://skills-hub.ai/skills/spec) |
| [stitch-pipeline](stitch-pipeline/) | Full design improvement pipeline — syncs your app to Google Stitch, generates alternatives, presents side-by-side comparison, and adopts... | [View on skills-hub](https://skills-hub.ai/skills/stitch-pipeline) |
| [story](story/) | Full story lifecycle — review, implement, and PR. | [View on skills-hub](https://skills-hub.ai/skills/story) |
| [tech-debt-sprint](tech-debt-sprint/) | Run a focused tech debt reduction sprint — inventories all technical debt (TODOs, outdated deps, missing tests, god objects), fixes code... | [View on skills-hub](https://skills-hub.ai/skills/tech-debt-sprint) |
| [workflow-conductor](workflow-conductor/) | Conduct a complete feature workflow in one skill — brainstorm, plan, TDD implementation, self-review, delivery summary — with hard gates... | [View on skills-hub](https://skills-hub.ai/skills/workflow-conductor) |
<!-- END GENERATED: skills-hub-index -->
