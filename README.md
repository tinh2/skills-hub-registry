# skills-hub-registry

The official skill collection for [skills-hub.ai](https://skills-hub.ai) -- a marketplace for Claude Code skills.

172 production-tested skills organized into 13 categories covering the complete software development lifecycle plus 8 industry verticals.

## Directory Structure

```
skills-hub-registry/
├── build/              # 14 skills — Project scaffolding and full build pipelines + industry API scaffolds
├── test/               #  9 skills — Unit, E2E, integration, load, visual, contract, accessibility tests
├── qa/                 # 10 skills — Quality assurance, performance, chaos, code smells, dead code, stress-test personas
├── review/             # 15 skills — Architecture, API, database, security, executive, and industry compliance reviews
├── deploy/             # 11 skills — Docker, K8s, Terraform, CI/CD, monitoring, DNS, CDN, secrets
├── docs/               # 10 skills — README, API docs, ADR, changelog, diagrams, onboarding, runbook
├── security/           # 10 skills — OWASP, pentest, GDPR, SOC2, HIPAA, PCI-DSS, encryption, dependency scan
├── ux/                 #  5 skills — UX audit, design systems, dark mode, responsive, i18n
├── analysis/           # 44 skills — Domain analysis, research, metrics + industry verticals
├── productivity/       #  8 skills — Dev containers, linting, git hooks, monorepo, release, env setup
├── integration/        #  9 skills — Stripe, auth, email, push notifications, search, storage, realtime
├── combo/              # 20 skills — Multi-skill chains and pipeline compositions
└── meta/               #  7 skills — Skill creation, testing, evolution, templates, cross-project sync
```

## Architecture

### Main Skill + Sub-Skill Pattern

Most categories follow an orchestrator pattern where a **main skill** scans for gaps and routes work to specialized **sub-skills**. This allows running the main skill for broad coverage or invoking a sub-skill directly for targeted work.

| Main Skill | Category | Orchestrates |
|------------|----------|-------------|
| `/integrate` | integration | auth-provider, stripe, email, push-notifications, search, storage, realtime, analytics-tracking |
| `/devops` | deploy | docker, github-actions, k8s, terraform, aws, cdn, dns, monitoring, secrets, app-icon |
| `/secure` | security | owasp, pentest, gdpr, soc2, encryption, dependency-scan, check-vanta |
| `/test-suite` | test | unit-test, e2e, integration-test, load-test, contract-test, accessibility-test, visual-regression, manual-test-plan |
| `/document` | docs | readme, api-docs, adr, changelog, diagram, onboarding, runbook, gen-catalog, skills-list |
| `/dx` | productivity | devcontainer, env-setup, git-hooks, linter, monorepo, release, vscode |

**Standalone orchestrators** (no sub-skill routing, self-contained pipelines):

| Skill | Category | What It Does |
|-------|----------|-------------|
| `/build` | build | Full project build from competitor analysis through implementation and QA |
| `/qa` | qa | Automated QA agent that walks every screen/endpoint, verifies, and fixes |
| `/analyze` | analysis | End-to-end domain analysis tracing features across all layers |
| `/arch-review` | review | Architect-level story review and implementation validation |
| `/ux` | ux | Dual-mode UX quality audit (heuristics/a11y/motion) or design validation |

## Skill Catalog

### build -- Project Scaffolding & Build Pipelines (14 skills)

| Skill | Version | Description |
|-------|---------|-------------|
| [build](build/build/) | 3.0.0 | Master orchestrator -- takes a competitor app and builds a better, cheaper, modern clone end-to-end with Node.js backend and Flutter frontend |
| [ship](build/ship/) | 8.0.0 | Fast autonomous build loop -- 4 iterations max. Build it, make it work, analyze it, ship it |
| [iterate](build/iterate/) | 4.0.0 | Self-iterating build loop -- implements, tests, reviews, analyzes, and refines up to 6 iterations |
| [flutter](build/flutter/) | 2.0.0 | Analyzes a video or screenshots of an application and builds a Flutter mobile version |
| [nextjs](build/nextjs/) | 1.0.0 | Scaffolds a production-ready Next.js 15 application with App Router, auth, database, and dashboard UI |
| [react-native](build/react-native/) | 1.0.0 | Builds a production-ready React Native mobile application from a design or specification |
| [api-scaffold](build/api-scaffold/) | 1.0.0 | Scaffolds a production-ready backend API with routes, controllers, middleware, database, auth, validation, and OpenAPI spec |
| [chrome-extension](build/chrome-extension/) | 1.0.0 | Builds a complete Chrome extension with Manifest V3, popup UI, content scripts, and background service worker |
| [cli-tool](build/cli-tool/) | 1.0.0 | Generates a production-ready CLI tool with command parsing, interactive prompts, and config management |
| [hotfix](build/hotfix/) | 1.0.0 | Emergency bug fix pipeline -- diagnose, fix, test, commit, push, and PR in 2 iterations max |
| [story-implementer](build/story-implementer/) | 2.0.0 | Implements a Jira story using repo conventions, writes unit tests, creates PR, addresses bot review |
| [db-migrate](build/db-migrate/) | 1.0.0 | Scaffolds Flyway migration files -- generates timestamped SQL, updates Slick table definitions and model case classes |
| [healthcare-api](build/healthcare-api/) | 1.0.0 | Scaffold a FHIR R4-compliant healthcare API with resource models, SMART on FHIR auth, audit logging, and interoperability endpoints |
| [fintech-api](build/fintech-api/) | 1.0.0 | Scaffold a production-ready financial services API with Plaid integration, payment processing, double-entry ledger, and KYC workflow |

### test -- Automated Testing (9 skills)

| Skill | Version | Description |
|-------|---------|-------------|
| [test-suite](test/test-suite/) | 1.0.0 | **Main skill.** Analyzes test coverage across all testing types, identifies gaps, routes to sub-skills, and produces a health report |
| [unit-test](test/unit-test/) | 1.0.0 | Auto-detects test framework, scans for untested functions, generates unit tests with edge cases, runs and self-heals |
| [e2e](test/e2e/) | 1.0.0 | Auto-detects any tech stack, generates exhaustive end-to-end integration tests with self-healing |
| [integration-test](test/integration-test/) | 1.0.0 | Auto-detects framework, generates integration tests for APIs, databases, and service interactions |
| [load-test](test/load-test/) | 1.0.0 | Auto-detects API framework, generates realistic load test scenarios with k6/Locust/Artillery |
| [contract-test](test/contract-test/) | 1.0.0 | Auto-detects API framework, generates consumer-driven contract tests using Pact or OpenAPI validation |
| [accessibility-test](test/accessibility-test/) | 1.0.0 | Auto-detects frontend framework, sets up axe-core and Lighthouse CI for automated WCAG 2.1 AA testing |
| [visual-regression](test/visual-regression/) | 1.0.0 | Auto-detects frontend framework, sets up visual regression testing with baseline screenshots across breakpoints |
| [manual-test-plan](test/manual-test-plan/) | 2.0.0 | Generates a manual QA test plan based on code changes on the current branch |

### qa -- Quality Assurance (10 skills)

| Skill | Version | Description |
|-------|---------|-------------|
| [qa](qa/qa/) | 3.0.0 | **Main skill.** Automated QA agent that walks every screen and API endpoint, verifies functionality, evaluates design, runs domain analysis, and fixes issues |
| [iterate-review](qa/iterate-review/) | 5.0.0 | Autonomously reviews and improves existing code through up to 5 iterations of analysis and fixing |
| [audit](qa/audit/) | 2.0.0 | Lightweight domain consistency audit -- verify all layers match and fix issues. Fast gate between pipeline phases |
| [preflight](qa/preflight/) | 1.0.0 | Pre-deploy verification gate -- checks git status, build, tests, migrations, and commit conventions. Read-only |
| [perf](qa/perf/) | 1.0.0 | Performance profiler -- analyzes DB queries, API call chains, frontend widget rebuilds, and bundle sizes |
| [chaos](qa/chaos/) | 1.0.0 | Chaos engineering for application resilience. Identifies failure points, generates chaos tests, validates graceful degradation |
| [code-smell](qa/code-smell/) | 1.0.0 | Detects Martin Fowler's catalog of code smells across the codebase with severity and recommended refactoring |
| [dead-code](qa/dead-code/) | 1.0.0 | Detects and safely removes dead code -- unreachable paths, unused exports, unused dependencies, unused CSS |
| [migration-verify](qa/migration-verify/) | 1.0.0 | Verifies database migrations are safe -- applies cleanly, reverses cleanly, preserves data integrity, is idempotent |
| [stress-test-personas](qa/stress-test-personas/) | 1.0.0 | Applies 6 adversarial decision-maker personas to stress-test the product and architecture from different strategic angles |

### review -- Architecture, Code & Industry Review (15 skills)

| Skill | Version | Description |
|-------|---------|-------------|
| [arch-review](review/arch-review/) | 7.0.0 | Architect-level story review and implementation validation with domain consistency analysis |
| [api-review](review/api-review/) | 1.0.0 | API design review against REST best practices -- naming, HTTP semantics, status codes, pagination, error format, versioning |
| [database-review](review/database-review/) | 1.0.0 | Database schema design review -- normalization, index coverage, constraints, naming, N+1 patterns, connection pooling |
| [security-review](review/security-review/) | 1.0.0 | Security-focused code review -- auth bypasses, injection vectors, data exposure, hardcoded secrets, IDOR vulnerabilities |
| [pr](review/pr/) | 1.0.0 | Creates a convention-compliant pull request -- extracts story number from branch, generates summary and test plan |
| [cto-review](review/cto-review/) | 1.0.0 | CTO-perspective technical strategy review -- architecture decisions, scaling readiness, engineering velocity, technical debt ratio, security posture |
| [cfo-review](review/cfo-review/) | 1.0.0 | CFO-perspective financial impact review -- infrastructure costs, pricing model alignment, build-vs-buy economics, technical debt as financial liability |
| [cpo-review](review/cpo-review/) | 1.0.0 | CPO-perspective product strategy review -- feature completeness, user journey gaps, retention architecture, growth levers, competitive moat |
| [healthcare-ops](review/healthcare-ops/) | 1.0.0 | Hospital operations review -- scheduling, workflows, integrations, patient flow, reporting, and staff management |
| [financial-compliance](review/financial-compliance/) | 1.0.0 | Financial software review against KYC/AML, BSA, Reg E, SOX, GLBA, and state money transmitter regulations |
| [procurement-review](review/procurement-review/) | 1.0.0 | Procurement software review -- sourcing workflows, PO management, vendor scorecards, spend analytics |
| [permit-compliance](review/permit-compliance/) | 1.0.0 | Construction software review for permit tracking, building code compliance, environmental regulations, and inspections |
| [manufacturing-compliance](review/manufacturing-compliance/) | 1.0.0 | Manufacturing regulatory review -- ISO 9001/13485/14001, FDA 21 CFR Part 11, GMP, OSHA, lot/serial traceability |
| [regulatory-compliance](review/regulatory-compliance/) | 1.0.0 | Cross-industry regulatory review -- audit trails, data retention, RBAC/ABAC, change management, breach notification |
| [energy-compliance](review/energy-compliance/) | 1.0.0 | Energy sector compliance review -- NERC CIP, FERC reporting, EPA emissions, renewable portfolio standards, pipeline safety |

### deploy -- Infrastructure & Deployment (11 skills)

| Skill | Version | Description |
|-------|---------|-------------|
| [devops](deploy/devops/) | 1.0.0 | **Main skill.** Scans infrastructure gaps and orchestrates deployment readiness across CI/CD, containers, monitoring, and IaC |
| [docker](deploy/docker/) | 1.0.0 | Auto-detect stack and generate optimized multi-stage Dockerfiles with compose, health checks, and security hardening |
| [github-actions](deploy/github-actions/) | 1.0.0 | Auto-detect tech stack and generate production-grade GitHub Actions CI/CD workflows with caching and security scanning |
| [k8s](deploy/k8s/) | 1.0.0 | Generate production-grade Kubernetes manifests with Deployments, Services, Ingress, HPA, and optional Helm charts |
| [terraform](deploy/terraform/) | 1.0.0 | Generate modular multi-cloud Terraform configurations with VPC, compute, database, cache, CDN, and remote state |
| [aws](deploy/aws/) | 1.0.0 | Generates production-ready Terraform files for AWS infrastructure |
| [cdn](deploy/cdn/) | 1.0.0 | Auto-detect hosting and configure CDN with caching rules, SSL/TLS, edge functions, and performance optimization |
| [dns](deploy/dns/) | 1.0.0 | Configure DNS records, SSL/TLS certificates, subdomains, email authentication, and health check routing |
| [monitoring](deploy/monitoring/) | 1.0.0 | Auto-detect infrastructure and set up observability with dashboards, alerting rules, and application instrumentation |
| [secrets](deploy/secrets/) | 1.0.0 | Audit secret handling, set up secrets management with rotation, and configure CI/CD secrets integration |
| [app-icon](deploy/app-icon/) | 1.0.0 | Generates a polished app icon and applies it as the launcher icon for iOS and Android |

### docs -- Documentation (10 skills)

| Skill | Version | Description |
|-------|---------|-------------|
| [document](docs/document/) | 1.0.0 | **Main skill.** Scans for existing documentation, identifies gaps based on project maturity, and orchestrates sub-skills to fill them |
| [readme](docs/readme/) | 1.0.0 | Generate comprehensive, scannable README.md documentation for any application by analyzing the codebase |
| [api-docs](docs/api-docs/) | 1.0.0 | Auto-detects API framework, extracts routes and schemas, generates OpenAPI 3.1 spec with interactive docs |
| [adr](docs/adr/) | 1.0.0 | Creates and manages Architecture Decision Records following the Michael Nygard format with auto-numbering |
| [changelog](docs/changelog/) | 1.0.0 | Generates or updates CHANGELOG.md from git history using conventional commit parsing and keep-a-changelog format |
| [diagram](docs/diagram/) | 1.0.0 | Analyzes codebase structure and generates Mermaid architecture diagrams including C4, sequence, ER, and dependency graphs |
| [onboarding](docs/onboarding/) | 1.0.0 | Analyzes codebase to generate a complete developer onboarding guide covering setup, architecture, conventions, and workflow |
| [runbook](docs/runbook/) | 1.0.0 | Scans deployment config, Docker/K8s manifests, CI/CD, and monitoring to generate actionable operations runbooks |
| [gen-catalog](docs/gen-catalog/) | 1.0.0 | Auto-generates README.md and skills-list from SKILL.md frontmatter across all skill directories |
| [skills-list](docs/skills-list/) | 3.0.0 | Display the full skills catalog -- lists every available skill with descriptions and autonomous build chains |

### security -- Security & Compliance (10 skills)

| Skill | Version | Description |
|-------|---------|-------------|
| [secure](security/secure/) | 1.0.0 | **Main skill.** Comprehensive security posture scan -- dependencies, code patterns, config, auth, and data handling with risk scoring |
| [owasp](security/owasp/) | 1.0.0 | Audit codebase against the OWASP 2021 Top 10 web application security risks with severity-rated findings |
| [pentest](security/pentest/) | 1.0.0 | Static-analysis penetration testing -- find exploitable vulnerabilities with proof-of-concept and remediation guidance |
| [gdpr](security/gdpr/) | 1.0.0 | Scan codebase for GDPR and CCPA compliance gaps -- PII handling, consent, data rights, and third-party sharing |
| [soc2](security/soc2/) | 1.0.0 | Evaluate codebase against SOC2 Trust Service Criteria -- security, availability, integrity, confidentiality, privacy |
| [encryption](security/encryption/) | 1.0.0 | Audit and implement encryption -- data at rest, in transit, key management, password hashing, and token security |
| [dependency-scan](security/dependency-scan/) | 1.0.0 | Auto-detect package manager, scan for vulnerable dependencies, auto-fix where possible, and generate SBOM |
| [check-vanta](security/check-vanta/) | 2.0.0 | Fetches Vanta vulnerabilities due for remediation, creates a Jira story, then fixes, commits, pushes, and opens PRs |
| [hipaa](security/hipaa/) | 1.0.0 | Deep HIPAA Security Rule audit -- administrative, physical, and technical safeguards with code-level CFR mappings |
| [pci-dss](security/pci-dss/) | 1.0.0 | PCI DSS v4.0 audit -- network security, data protection, encryption, access controls, logging, and vulnerability management |

### ux -- User Experience & Design (5 skills)

| Skill | Version | Description |
|-------|---------|-------------|
| [ux](ux/ux/) | 1.0.0 | **Main skill.** Dual-mode UX quality skill -- runs heuristic/accessibility/motion audit, or validates implementation against design mockups |
| [design-system](ux/design-system/) | 1.0.0 | Extract or create a design system from existing UI code -- tokens, component inventory, and usage guidelines |
| [dark-mode](ux/dark-mode/) | 1.0.0 | Dark mode implementation -- generate dark palette, create theme switching, and verify WCAG contrast for both modes |
| [responsive](ux/responsive/) | 1.0.0 | Responsive design audit and fixes -- scan for breakpoint issues, fix overflow, and verify cross-device layouts |
| [i18n](ux/i18n/) | 1.0.0 | Internationalization setup -- extract hardcoded strings, configure locale files, and wire up i18n library |

### analysis -- Domain Analysis, Research & Industry Verticals (44 skills)

| Skill | Version | Description |
|-------|---------|-------------|
| [analyze](analysis/analyze/) | 3.0.0 | End-to-end domain analysis -- traces every feature across all layers, verifies consistency, and fixes issues |
| [compete](analysis/compete/) | 1.0.0 | Researches competing products, catalogs their features, and produces a prioritized feature gap analysis |
| [mvp](analysis/mvp/) | 2.0.0 | Analyzes a video or screenshots of an application to decipher its MVP and suggest improvements |
| [backend-spec](analysis/backend-spec/) | 5.0.0 | Generates backend or frontend engineering specs in Jira format with acceptance criteria, routes, and table schemas |
| [metrics](analysis/metrics/) | 1.0.0 | Computes development quality metrics from git history and tracks improvement over time |
| [recall](analysis/recall/) | 1.0.0 | Reconstructs the development cycle from git history, distills patterns, and produces actionable insights |
| [cost-analysis](analysis/cost-analysis/) | 1.0.0 | Analyzes Firebase infrastructure costs at 1K-100K user scales with optimization recommendations |
| [dep-map](analysis/dep-map/) | 1.0.0 | Maps dependencies between engineering stories, computes optimal implementation order with parallel batches |
| [dependency-analysis](analysis/dependency-analysis/) | 1.0.0 | Dependency graph analysis -- checks outdated, deprecated, vulnerable, duplicate, heavy, and unused packages |
| [api-surface](analysis/api-surface/) | 1.0.0 | Maps the entire API surface -- routes, middleware, auth requirements, request/response types, and inconsistencies |
| [bundle-analysis](analysis/bundle-analysis/) | 1.0.0 | Frontend bundle size analysis -- chunk sizes, duplicates, tree-shaking, code splitting, and size budget config |
| [codebase-health](analysis/codebase-health/) | 1.0.0 | Overall codebase health score (0-100) -- complexity, coupling, cohesion, test coverage, documentation, churn hotspots |
| [tech-debt](analysis/tech-debt/) | 1.0.0 | Technical debt inventory -- TODOs, deprecated usage, outdated deps, high-churn files, complexity hotspots, duplicated code |
| [image-storage-optimization](analysis/image-storage-optimization/) | 1.0.0 | Reduce storage costs by automatically resizing and compressing uploaded user images |
| [growth-audit](analysis/growth-audit/) | 1.0.0 | Growth marketing audit using the AARRR pirate metrics framework -- SEO, onboarding, retention, monetization, referral |
| [sales-readiness](analysis/sales-readiness/) | 1.0.0 | Enterprise sales readiness audit -- SSO/SAML, RBAC, multi-tenancy, audit logging, API quality, SOC2/ISO readiness |
| [customer-success-audit](analysis/customer-success-audit/) | 1.0.0 | Customer Success Manager perspective audit -- onboarding, self-service, health signals, support infrastructure, expansion triggers |
| [pmf-analysis](analysis/pmf-analysis/) | 1.0.0 | Product-market fit readiness analysis -- core value delivery, feature focus, activation, retention, analytics maturity, iteration speed |
| [healthcare-compliance](analysis/healthcare-compliance/) | 1.0.0 | Healthcare software audit for HIPAA, HITECH, 21st Century Cures Act, and state regulatory compliance |
| [clinical-data-review](analysis/clinical-data-review/) | 1.0.0 | Clinical data review for HL7 FHIR conformance, terminology standards, and interoperability |
| [medical-billing](analysis/medical-billing/) | 1.0.0 | Medical billing analysis -- claims processing, revenue cycle, ICD-10/CPT validation, payer rules, denial management |
| [patient-engagement](analysis/patient-engagement/) | 1.0.0 | Patient engagement audit -- portal completeness, secure messaging, telehealth, consent management, health literacy |
| [credit-risk](analysis/credit-risk/) | 1.0.0 | Credit risk modeling analysis -- fairness, accuracy, regulatory compliance, model governance, scoring algorithms |
| [fraud-detection](analysis/fraud-detection/) | 1.0.0 | Fraud detection system audit -- rule engines, ML models, real-time processing, alert workflows, adaptive learning |
| [portfolio-optimizer](analysis/portfolio-optimizer/) | 1.0.0 | Investment portfolio analysis -- allocation models, risk metrics, rebalancing logic, performance attribution |
| [insurance-claims](analysis/insurance-claims/) | 1.0.0 | Insurance claims processing analysis -- lifecycle completeness, automation rules, fraud indicators, reserve estimation |
| [route-optimizer](analysis/route-optimizer/) | 1.0.0 | Routing and delivery analysis -- algorithm quality, constraint handling, real-time adaptation, cost modeling |
| [inventory-forecast](analysis/inventory-forecast/) | 1.0.0 | Forecasting and inventory analysis -- model accuracy, safety stock logic, reorder strategies, demand signals |
| [supply-chain-risk](analysis/supply-chain-risk/) | 1.0.0 | Supply chain risk analysis -- disruption modeling, end-to-end visibility, compliance tracking, resilience strategies |
| [warehouse-ops](analysis/warehouse-ops/) | 1.0.0 | Warehouse management analysis -- layout optimization, picking strategies, inventory accuracy, automation readiness |
| [cost-overrun-predictor](analysis/cost-overrun-predictor/) | 1.0.0 | Construction project analysis -- budget tracking, risk factor modeling, schedule analysis, early warning detection |
| [property-roi](analysis/property-roi/) | 1.0.0 | Real estate investment analysis -- financial models, pro forma, tax modeling, sensitivity analysis, portfolio analytics |
| [lease-optimizer](analysis/lease-optimizer/) | 1.0.0 | Commercial lease analysis -- lease abstraction, rent optimization, ASC 842/IFRS 16 compliance, portfolio analysis |
| [real-estate-market](analysis/real-estate-market/) | 1.0.0 | Real estate analytics -- market data quality, demographics, economic indicators, predictive models, visualization |
| [predictive-maintenance](analysis/predictive-maintenance/) | 1.0.0 | Manufacturing predictive maintenance analysis -- sensor pipelines, ML lifecycle, MTBF/MTTF, spare parts integration |
| [production-optimizer](analysis/production-optimizer/) | 1.0.0 | Production scheduling analysis -- OEE calculations, bottleneck detection, changeover optimization, capacity planning |
| [defect-detection](analysis/defect-detection/) | 1.0.0 | Quality control analysis -- computer vision, SPC, Six Sigma metrics (Cp/Cpk), inspection automation, root cause analysis |
| [energy-efficiency](analysis/energy-efficiency/) | 1.0.0 | Energy management analysis -- power monitoring, ISO 50001, peak demand, renewable integration, carbon footprint |
| [contract-risk](analysis/contract-risk/) | 1.0.0 | Contract management analysis -- clause extraction, obligation tracking, risk scoring, SLA monitoring, liability analysis |
| [litigation-predictor](analysis/litigation-predictor/) | 1.0.0 | Litigation analytics -- case outcome modeling, settlement analysis, cost forecasting, precedent matching |
| [legal-discovery](analysis/legal-discovery/) | 1.0.0 | E-discovery analysis -- document processing, TAR, privilege detection, PII redaction, defensibility audit |
| [load-forecast](analysis/load-forecast/) | 1.0.0 | Energy load forecasting analysis -- demand prediction, weather integration, peak shaving, demand response |
| [grid-optimizer](analysis/grid-optimizer/) | 1.0.0 | Smart grid analysis -- power flow, fault detection/isolation/restoration, DER management, SCADA integration |
| [commodity-pricing](analysis/commodity-pricing/) | 1.0.0 | Commodity pricing analysis -- pricing models, market data feeds, position management, VaR/CVaR, settlement |

### productivity -- Developer Experience (8 skills)

| Skill | Version | Description |
|-------|---------|-------------|
| [dx](productivity/dx/) | 1.0.0 | **Main skill.** Audit developer experience foundations and generate a DX health report with actionable improvements |
| [devcontainer](productivity/devcontainer/) | 1.0.0 | Auto-detect stack and generate a production-grade dev container configuration with Codespaces compatibility |
| [env-setup](productivity/env-setup/) | 1.0.0 | Detect required tools, install dependencies, configure environment, and verify the project builds and tests pass |
| [git-hooks](productivity/git-hooks/) | 1.0.0 | Auto-detect stack and set up pre-commit and commit-msg hooks with conventional commit enforcement |
| [linter](productivity/linter/) | 1.0.0 | Auto-detect stack and configure linting, formatting, and editor integration with auto-fix for existing violations |
| [monorepo](productivity/monorepo/) | 1.0.0 | Set up or migrate to a monorepo with workspaces, build pipeline, task graph, and local plus remote caching |
| [release](productivity/release/) | 1.0.0 | Set up automated release pipeline with semantic versioning, changelog generation, and publishing |
| [vscode](productivity/vscode/) | 1.0.0 | Open VS Code in the current working directory |

### integration -- Third-Party Service Connectors (9 skills)

| Skill | Version | Description |
|-------|---------|-------------|
| [integrate](integration/integrate/) | 1.0.0 | **Main skill.** Master integration orchestrator that audits existing integrations, routes to sub-skills, and produces a health score |
| [auth-provider](integration/auth-provider/) | 1.0.0 | Sets up complete OAuth/SSO authentication with provider configuration, session management, and login UI |
| [stripe](integration/stripe/) | 1.0.0 | Sets up complete Stripe payment integration with checkout sessions, webhooks, and subscription billing |
| [email](integration/email/) | 1.0.0 | Sets up transactional email with provider SDK, templated messages, delivery tracking, and webhook handling |
| [push-notifications](integration/push-notifications/) | 1.0.0 | Sets up mobile and web push notifications with FCM, APNs, or OneSignal including deep linking |
| [search](integration/search/) | 1.0.0 | Sets up full-text search with indexing, search UI, and ranking -- supports Algolia, Typesense, Meilisearch, Elasticsearch |
| [storage](integration/storage/) | 1.0.0 | Sets up object storage with upload, download, presigned URLs, and CDN integration -- supports S3, GCS, R2, Supabase |
| [realtime](integration/realtime/) | 1.0.0 | Sets up WebSocket or SSE-based realtime communication with channels, presence, and offline handling |
| [analytics-tracking](integration/analytics-tracking/) | 1.0.0 | Sets up event tracking with analytics providers -- auto-detects framework, installs SDK, and instruments key flows |

### combo -- Multi-Skill Chains (20 skills)

| Skill | Version | Chain | Description |
|-------|---------|-------|-------------|
| [polish](combo/polish/) | 3.0.0 | /ux ∥ /scale-audit → /qa → /analyze | Full quality pass with parallel UX + scalability audit |
| [research](combo/research/) | 1.0.0 | /compete → /new-features | Competitive gap analysis + feature ideation |
| [spec](combo/spec/) | 1.0.0 | /mvp → /backend-spec | App analysis + story generation |
| [story](combo/story/) | 1.0.0 | /arch-review → /story-implementer → /pr | Full story lifecycle from review to PR |
| [review-implement](combo/review-implement/) | 1.0.0 | /arch-review → /story-implementer | Review architecture then implement |
| [full-test](combo/full-test/) | 1.0.0 | /e2e → /manual-test-plan | Automated E2E tests + manual test plan |
| [retro](combo/retro/) | 1.0.0 | /recall → /new-features | Dev retrospective + feature ideation |
| [fix-and-ship](combo/fix-and-ship/) | 1.0.0 | /hotfix → /preflight | Emergency fix + deploy verification |
| [secure-ship](combo/secure-ship/) | 1.0.0 | /owasp → /ship → /security-review → /pentest | Security-first build chain |
| [compliance-gate](combo/compliance-gate/) | 1.0.0 | /secure → /gdpr → /dependency-scan → /pentest | Full compliance pass with unified report |
| [full-deploy](combo/full-deploy/) | 1.0.0 | /docker → /github-actions → /monitoring → /preflight | Complete deploy pipeline |
| [design-to-code](combo/design-to-code/) | 1.0.0 | /design-system → /responsive → /dark-mode → /ux | Full design implementation chain |
| [data-pipeline](combo/data-pipeline/) | 1.0.0 | /api-scaffold → /integration-test → /load-test | Data-heavy app setup chain |
| [tech-debt-sprint](combo/tech-debt-sprint/) | 1.0.0 | /tech-debt → /code-smell → /dead-code → /iterate-review | Debt reduction sprint |
| [launch-readiness](combo/launch-readiness/) | 1.0.0 | /cpo-review → /growth-audit → /ux → /secure → /preflight | Full pre-launch quality gate with go/no-go decision |
| [investor-ready](combo/investor-ready/) | 1.0.0 | /cto-review → /cfo-review → /cpo-review → /sales-readiness → /codebase-health | Comprehensive investor due-diligence brief |
| [healthcare-audit](combo/healthcare-audit/) | 1.0.0 | /hipaa → /clinical-data-review → /healthcare-compliance → /security-review | Full healthcare compliance and security audit |
| [fintech-launch](combo/fintech-launch/) | 1.0.0 | /pci-dss → /fintech-api → /fraud-detection → /credit-risk → /preflight | Complete fintech launch readiness pipeline |
| [logistics-optimize](combo/logistics-optimize/) | 1.0.0 | /route-optimizer → /warehouse-ops → /inventory-forecast → /supply-chain-risk → /load-test | Full logistics optimization and stress testing |
| [compliance-suite](combo/compliance-suite/) | 1.0.0 | /regulatory-compliance → /gdpr → /soc2 → /dependency-scan → /pentest | Cross-industry compliance hardening pipeline |

### meta -- Skills About Skills (7 skills)

| Skill | Version | Description |
|-------|---------|-------------|
| [bootstrap](meta/bootstrap/) | 3.0.0 | Scaffolds a new project from a saved template -- creates CLAUDE.md, initial memory, and recommends first skill |
| [evolve](meta/evolve/) | 1.0.0 | Self-improving skill that reads /recall and /metrics output, identifies which skills need patching, and applies fixes |
| [extract-template](meta/extract-template/) | 1.0.0 | Extracts a reusable project template from a successful project -- captures pipeline, conventions, and pitfalls |
| [promote](meta/promote/) | 1.0.0 | Cross-project pattern detection -- reads all project memories, finds recurring patterns, promotes to global conventions |
| [skill-creator](meta/skill-creator/) | 1.0.0 | Creates new Claude Code skills following the marketplace SKILL.md format with proper frontmatter and quality scoring |
| [skill-test](meta/skill-test/) | 1.0.0 | Validates a SKILL.md file against the marketplace quality rubric, checking schema, structure, and computing a score |
| [registry-sync](meta/registry-sync/) | 1.0.0 | Scans and validates all SKILL.md files in the registry, checks category READMEs, detects duplicates, produces health report |

## Industry Verticals

Skills covering domain-specific regulations, workflows, and compliance across 8 industries:

| Industry | Skills | Key Regulations/Standards |
|----------|--------|--------------------------|
| Healthcare | healthcare-compliance, hipaa, clinical-data-review, healthcare-ops, healthcare-api, medical-billing, patient-engagement | HIPAA, HITECH, HL7 FHIR, ICD-10/CPT |
| Finance | credit-risk, fraud-detection, pci-dss, financial-compliance, portfolio-optimizer, fintech-api, insurance-claims | PCI DSS v4.0, KYC/AML, SOX, BSA, Reg E |
| Logistics & Supply Chain | route-optimizer, inventory-forecast, supply-chain-risk, warehouse-ops, procurement-review | EDI, TSP/VRP, WMS, demand planning |
| Construction & Real Estate | cost-overrun-predictor, property-roi, lease-optimizer, permit-compliance, real-estate-market | ASC 842/IFRS 16, building codes, EVM |
| Manufacturing | predictive-maintenance, production-optimizer, defect-detection, energy-efficiency, manufacturing-compliance | ISO 9001/13485/14001, FDA 21 CFR Part 11, GMP, OSHA |
| Legal | contract-risk, litigation-predictor, legal-discovery, regulatory-compliance | TAR, e-discovery, RBAC/ABAC, audit trails |
| Energy & Utilities | load-forecast, grid-optimizer, commodity-pricing, energy-compliance | NERC CIP, FERC, EPA, ISO 50001, 49 CFR 192/195 |

### Industry Pipelines

```
/healthcare-audit   (runs: /hipaa → /clinical-data-review → /healthcare-compliance → /security-review)
/fintech-launch     (runs: /pci-dss → /fintech-api → /fraud-detection → /credit-risk → /preflight)
/logistics-optimize (runs: /route-optimizer → /warehouse-ops → /inventory-forecast → /supply-chain-risk → /load-test)
/compliance-suite   (runs: /regulatory-compliance → /gdpr → /soc2 → /dependency-scan → /pentest)
```

## Recommended Pipelines

### New Project
```
/bootstrap → /research → /spec → /build → /polish
```

### Feature Development
```
/backend-spec → /arch-review → /story-implementer → /qa
```

### Fast Iteration
```
/ship [task] → /qa → /analyze
```

### Quality Gate
```
/polish  (runs: /ux ∥ /scale-audit → /qa → /analyze)
```

### Full Test Coverage
```
/test-suite  (scans gaps, routes to unit/e2e/integration/load/contract/a11y/visual)
```

### Security Hardening
```
/secure-ship  (runs: /owasp → /ship → /security-review → /pentest)
```

### Compliance Audit
```
/compliance-gate  (runs: /secure → /gdpr → /dependency-scan → /pentest)
```

### Deploy Pipeline
```
/full-deploy  (runs: /docker → /github-actions → /monitoring → /preflight)
```

### Tech Debt Paydown
```
/tech-debt-sprint  (runs: /tech-debt → /code-smell → /dead-code → /iterate-review)
```

### Executive Review
```
/cto-review → /cfo-review → /cpo-review
```

### Launch Readiness
```
/launch-readiness  (runs: /cpo-review → /growth-audit → /ux → /secure → /preflight)
```

### Investor Due Diligence
```
/investor-ready  (runs: /cto-review → /cfo-review → /cpo-review → /sales-readiness → /codebase-health)
```

### Retrospective
```
/recall → /metrics → /evolve
```

## Skill Dependency Graph

```
/build (orchestrator)
  ├── /mvp
  ├── /backend-spec
  ├── /arch-review (parallel)
  ├── /story-implementer (parallel)
  ├── /ux ∥ /manual-test-plan
  ├── /qa
  └── /analyze

/ship (fast build)
  ├── pre-build validation
  ├── /analyze (iteration 3)
  └── /readme

/iterate (iterative build)
  ├── pre-build validation
  ├── /analyze (iterations 2, final)
  └── /readme

/test-suite (test orchestrator)
  ├── coverage scan
  ├── /unit-test
  ├── /e2e
  ├── /integration-test
  ├── /load-test
  ├── /contract-test
  ├── /accessibility-test
  └── /visual-regression

/secure (security orchestrator)
  ├── /owasp
  ├── /pentest
  ├── /gdpr
  ├── /soc2
  ├── /encryption
  └── /dependency-scan

/document (docs orchestrator)
  ├── /readme
  ├── /api-docs
  ├── /adr
  ├── /changelog
  ├── /diagram
  ├── /onboarding
  └── /runbook

/devops (deploy orchestrator)
  ├── /docker
  ├── /github-actions
  ├── /k8s
  ├── /terraform
  ├── /monitoring
  └── /secrets

/integrate (integration orchestrator)
  ├── /auth-provider
  ├── /stripe
  ├── /email
  ├── /push-notifications
  ├── /search
  ├── /storage
  ├── /realtime
  └── /analytics-tracking

/dx (productivity orchestrator)
  ├── /devcontainer
  ├── /env-setup
  ├── /git-hooks
  ├── /linter
  ├── /monorepo
  └── /release

/polish (quality combo)
  ├── /ux (parallel track A)
  ├── /scale-audit (parallel track B)
  ├── /qa
  └── /analyze

/qa (testing)
  └── /analyze (phase 4)

/launch-readiness (launch combo)
  ├── /cpo-review
  ├── /growth-audit
  ├── /ux
  ├── /secure
  └── /preflight

/investor-ready (investor combo)
  ├── /cto-review
  ├── /cfo-review
  ├── /cpo-review
  ├── /sales-readiness
  └── /codebase-health

/evolve (meta)
  └── reads /recall + /metrics output
```

## SKILL.md Format

Every skill uses the skills-hub.ai marketplace format:

```yaml
---
name: my-skill
description: One-sentence description of what it does (10-1000 chars)
version: "1.0.0"
category: build
platforms:
  - CLAUDE_CODE
---

Your skill instructions here. This is the main content
loaded as context when the skill is invoked.
```

### Valid Categories

`build` `test` `qa` `review` `deploy` `docs` `security` `ux` `analysis` `productivity` `integration` `combo` `meta`

### Valid Platforms

`CLAUDE_CODE` `CURSOR` `CODEX_CLI` `OTHER`

### Quality Scoring

Skills are scored 0-100 on the marketplace:
- **Schema (0-25):** Required fields present, description >= 50 chars, valid semver, valid category
- **Instructions (0-75):** >= 500 chars, structured phases/steps, I/O spec, error handling, guardrails, examples, output format
- **Minimum to publish:** 20

## Contributing

1. Create a new directory under the appropriate category: `{category}/{skill-name}/SKILL.md`
2. Follow the SKILL.md format above
3. Ensure your skill scores >= 20 on the quality scale (run `/skill-test` to check)
4. Submit a PR

## Key Design Patterns

These patterns are validated across 7+ production projects:

- **Self-healing loops:** Skills iterate up to N times, fixing issues found each pass
- **Pre-build validation:** Static analysis gate before feature work begins
- **Co-commit rules:** Firestore rules, server validation, and model serialization ship with features
- **Domain analysis feedback:** `/analyze` embedded as a quality gate in build loops
- **Parallel execution:** Independent tracks run concurrently via Task tool subagents
- **Wiring completeness:** Detect features that exist in one layer but are never connected
- **Monolith decomposition:** Files exceeding 500 lines are split before adding features
- **Orchestrator pattern:** Main skills scan for gaps and route to specialized sub-skills
