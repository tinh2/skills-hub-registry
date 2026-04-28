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
| [design-overhaul](design-overhaul/) | 1.0.0 | Complete autonomous design overhaul — tears down dated patterns and rebuilds with modern CSS, proper tokens, purposeful motion, and production-grade quality. The nuclear option... |
| [design-pipeline](design-pipeline/) | 1.0.0 | Full autonomous design pipeline — Ralph Wiggum builds it, then the safety net polishes it. Chains: design-setup → design-build → (design-audit ∥ design-optimize) → design-polish →... |
| [marketing-refresh](marketing-refresh/) | 1.0.0 | Autonomous competitive analysis and feature discovery pipeline. Runs /compete and /new-features on each project, produces actionable market positioning insights. Schedule daily or... |
| [mvp-spec](mvp-spec/) | 2.0.0 | Chains /mvp → /spec — analyzes an app from video/screenshots/description, then generates implementation stories. Triggers: analyze and spec, product analysis to stories, app... |
| [ship-pipeline](ship-pipeline/) | 3.0.0 | Full-stack app pipeline — build, test, review, and deploy across one or ALL repos. Scans CLAUDE.md, MEMORY.md, TODOs, open PRs, and issues for shippable work. Supports 'ship all'... |
| [stitch-pipeline](stitch-pipeline/) | 1.0.0 | >- |
