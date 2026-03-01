# skills-hub-registry

The official skill collection for [skills-hub.ai](https://skills-hub.ai) -- a marketplace for Claude Code skills.

230 production-tested skills organized into 13 categories covering the complete software development lifecycle, 8 industry verticals, and 14 social-impact sectors.

## Directory Structure

```
skills-hub-registry/
├── build/              # 14 skills — Project scaffolding and full build pipelines + industry API scaffolds
├── test/               #  9 skills — Unit, E2E, integration, load, visual, contract, accessibility tests
├── qa/                 # 10 skills — Quality assurance, performance, chaos, code smells, dead code, stress-test personas
├── review/             # 21 skills — Architecture, API, database, security, executive, industry, and social-impact reviews
├── deploy/             # 11 skills — Docker, K8s, Terraform, CI/CD, monitoring, DNS, CDN, secrets
├── docs/               # 10 skills — README, API docs, ADR, changelog, diagrams, onboarding, runbook
├── security/           # 11 skills — OWASP, pentest, GDPR, SOC2, HIPAA, PCI-DSS, encryption, benefits fraud
├── ux/                 #  5 skills — UX audit, design systems, dark mode, responsive, i18n
├── analysis/           # 91 skills — Domain analysis, research, metrics, industry verticals, social impact
├── productivity/       #  8 skills — Dev containers, linting, git hooks, monorepo, release, env setup
├── integration/        #  9 skills — Stripe, auth, email, push notifications, search, storage, realtime
├── combo/              # 24 skills — Multi-skill chains and pipeline compositions
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

### review -- Architecture, Code, Industry & Social Impact Review (21 skills)

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
| [care-burnout-audit](review/care-burnout-audit/) | 1.0.0 | Healthcare burnout review -- workload distribution, scheduling fairness, documentation burden, alert fatigue |
| [school-ops](review/school-ops/) | 1.0.0 | School operations review -- scheduling, resource allocation, transportation, IDEA/Title I compliance |
| [government-compliance](review/government-compliance/) | 1.0.0 | Government software review -- FedRAMP, Section 508, FISMA, NIST 800-53, FOIA, records retention |
| [housing-compliance](review/housing-compliance/) | 1.0.0 | Housing software review -- Fair Housing Act, ADA, HUD reporting, LIHTC compliance, tenant rights |
| [environmental-compliance](review/environmental-compliance/) | 1.0.0 | Environmental compliance review -- EPA reporting, Clean Air/Water Act, NEPA, RCRA waste management |
| [therapist-documentation](review/therapist-documentation/) | 1.0.0 | Therapy documentation review -- SOAP/DAP notes, DSM-5/ICD-10 codes, informed consent, HIPAA compliance |

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

### security -- Security & Compliance (11 skills)

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
| [benefits-fraud](security/benefits-fraud/) | 1.0.0 | Benefits fraud detection -- identity verification, duplicate detection, anomaly detection, overpayment recovery |

### ux -- User Experience & Design (5 skills)

| Skill | Version | Description |
|-------|---------|-------------|
| [ux](ux/ux/) | 1.0.0 | **Main skill.** Dual-mode UX quality skill -- runs heuristic/accessibility/motion audit, or validates implementation against design mockups |
| [design-system](ux/design-system/) | 1.0.0 | Extract or create a design system from existing UI code -- tokens, component inventory, and usage guidelines |
| [dark-mode](ux/dark-mode/) | 1.0.0 | Dark mode implementation -- generate dark palette, create theme switching, and verify WCAG contrast for both modes |
| [responsive](ux/responsive/) | 1.0.0 | Responsive design audit and fixes -- scan for breakpoint issues, fix overflow, and verify cross-device layouts |
| [i18n](ux/i18n/) | 1.0.0 | Internationalization setup -- extract hardcoded strings, configure locale files, and wire up i18n library |

### analysis -- Domain Analysis, Research, Industry Verticals & Social Impact (91 skills)

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
| [mental-health-clinic](analysis/mental-health-clinic/) | 1.0.0 | Mental health clinic analysis -- scheduling, therapist-client matching, crisis detection, outcome tracking |
| [elder-care-ops](analysis/elder-care-ops/) | 1.0.0 | Elder care analysis -- resident monitoring, medication management, ADL tracking, care plan optimization |
| [rural-health](analysis/rural-health/) | 1.0.0 | Rural health network analysis -- telehealth readiness, provider coverage, mobile clinic scheduling |
| [disability-services](analysis/disability-services/) | 1.0.0 | Disability services analysis -- IEP/ISP management, HCBS compliance, assistive technology integration |
| [rehab-therapy](analysis/rehab-therapy/) | 1.0.0 | Rehabilitation therapy analysis -- recovery metrics, exercise personalization, outcome-based care |
| [dropout-risk](analysis/dropout-risk/) | 1.0.0 | Student dropout risk prediction -- attendance, grades, behavioral indicators, early warning systems |
| [curriculum-optimizer](analysis/curriculum-optimizer/) | 1.0.0 | Curriculum analysis -- standards coverage, pacing optimization, differentiation, assessment quality |
| [student-personalization](analysis/student-personalization/) | 1.0.0 | Adaptive learning analysis -- learning paths, mastery detection, knowledge graphs, accessibility |
| [teacher-workload](analysis/teacher-workload/) | 1.0.0 | Teacher workload analysis -- grading automation, lesson planning, admin task reduction |
| [benefits-processing](analysis/benefits-processing/) | 1.0.0 | Government benefits analysis -- eligibility determination, application workflows, multi-program coordination |
| [public-resource-allocation](analysis/public-resource-allocation/) | 1.0.0 | Public resource allocation analysis -- budget optimization, equity-based distribution, demand forecasting |
| [emergency-response](analysis/emergency-response/) | 1.0.0 | Emergency response analysis -- 911 dispatch, resource deployment, ICS compliance, response time optimization |
| [affordable-housing](analysis/affordable-housing/) | 1.0.0 | Affordable housing analysis -- unit allocation, waitlist management, Fair Housing compliance, LIHTC tracking |
| [rent-burden](analysis/rent-burden/) | 1.0.0 | Rent burden analysis -- affordability calculations, AMI modeling, housing voucher management |
| [eviction-risk](analysis/eviction-risk/) | 1.0.0 | Eviction risk prediction -- payment patterns, early warning, intervention triggers, outcome tracking |
| [crop-yield](analysis/crop-yield/) | 1.0.0 | Crop yield analysis -- precision agriculture, soil analysis, irrigation optimization, pest detection |
| [food-waste](analysis/food-waste/) | 1.0.0 | Food waste reduction analysis -- shelf life prediction, inventory rotation, cold chain monitoring |
| [climate-risk-agriculture](analysis/climate-risk-agriculture/) | 1.0.0 | Agricultural climate risk -- weather impact modeling, crop insurance, carbon sequestration tracking |
| [carbon-accounting](analysis/carbon-accounting/) | 1.0.0 | Carbon accounting analysis -- Scope 1/2/3 emissions, GHG Protocol, CDP/TCFD/GRI reporting |
| [disaster-prediction](analysis/disaster-prediction/) | 1.0.0 | Disaster prediction analysis -- early warning systems, alert distribution, evacuation planning |
| [sustainability-metrics](analysis/sustainability-metrics/) | 1.0.0 | ESG and sustainability analysis -- metric collection, SDG alignment, greenwashing detection |
| [legal-aid](analysis/legal-aid/) | 1.0.0 | Legal aid analysis -- case management, client intake, document assembly, access-to-justice metrics |
| [case-outcome-predictor](analysis/case-outcome-predictor/) | 1.0.0 | Legal case prediction analysis -- model fairness, bias detection, ethical guardrails |
| [rights-explainer](analysis/rights-explainer/) | 1.0.0 | Legal information analysis -- plain-language accuracy, reading level, multilingual support |
| [fundraising-optimizer](analysis/fundraising-optimizer/) | 1.0.0 | Nonprofit fundraising analysis -- donor segmentation, campaign performance, major gift scoring |
| [grant-writer](analysis/grant-writer/) | 1.0.0 | Grant management analysis -- proposal quality, deadline tracking, outcome reporting |
| [impact-measurement](analysis/impact-measurement/) | 1.0.0 | Program impact analysis -- logic models, attribution, cost-effectiveness, beneficiary feedback |
| [donor-retention](analysis/donor-retention/) | 1.0.0 | Donor retention analysis -- lapse risk scoring, lifetime value modeling, stewardship workflows |
| [crisis-triage](analysis/crisis-triage/) | 1.0.0 | Crisis triage analysis -- call prioritization, resource dispatching, severity classification |
| [volunteer-coordination](analysis/volunteer-coordination/) | 1.0.0 | Volunteer management analysis -- skill matching, scheduling, retention, impact reporting |
| [emergency-resource](analysis/emergency-resource/) | 1.0.0 | Emergency resource analysis -- inventory tracking, deployment optimization, inter-agency sharing |
| [fall-risk](analysis/fall-risk/) | 1.0.0 | Fall risk prediction -- sensor integration, risk scoring, environmental hazards, mobility trends |
| [medication-adherence](analysis/medication-adherence/) | 1.0.0 | Medication adherence analysis -- tracking accuracy, interaction checking, adverse event detection |
| [caregiver-coordination](analysis/caregiver-coordination/) | 1.0.0 | Caregiver coordination analysis -- scheduling, handoff communication, burnout prevention |
| [crisis-risk-monitor](analysis/crisis-risk-monitor/) | 1.0.0 | Mental health crisis monitoring -- risk signal detection, escalation protocols, ethical guardrails |
| [treatment-outcome](analysis/treatment-outcome/) | 1.0.0 | Treatment outcome analysis -- PHQ-9/GAD-7 validity, longitudinal trends, evidence-based alignment |
| [care-plan-optimizer](analysis/care-plan-optimizer/) | 1.0.0 | Care plan optimization -- treatment goals, intervention scheduling, step-down/step-up criteria |
| [debt-payoff](analysis/debt-payoff/) | 1.0.0 | Debt management analysis -- payoff strategies, interest calculation, credit score impact modeling |
| [spending-behavior](analysis/spending-behavior/) | 1.0.0 | Spending behavior analysis -- categorization, budget adherence, behavioral nudges, savings goals |
| [retirement-optimizer](analysis/retirement-optimizer/) | 1.0.0 | Retirement planning analysis -- projection models, Social Security optimization, Monte Carlo quality |
| [skill-gap](analysis/skill-gap/) | 1.0.0 | Workforce skill gap analysis -- taxonomy quality, labor market data, career pathway modeling |
| [resume-optimizer](analysis/resume-optimizer/) | 1.0.0 | Resume optimization analysis -- ATS compatibility, keyword matching, job-description alignment |
| [training-path](analysis/training-path/) | 1.0.0 | Training pathway analysis -- prerequisite mapping, competency-based progression, ROI tracking |
| [employer-matching](analysis/employer-matching/) | 1.0.0 | Job matching analysis -- algorithm quality, bias detection, salary accuracy, candidate experience |
| [recovery-metrics](analysis/recovery-metrics/) | 1.0.0 | Rehabilitation recovery analysis -- outcome measurement, functional assessment, readiness scoring |
| [therapy-personalization](analysis/therapy-personalization/) | 1.0.0 | Therapy personalization analysis -- exercise recommendations, compliance prediction, plan adaptation |
| [setback-predictor](analysis/setback-predictor/) | 1.0.0 | Rehabilitation setback prediction -- risk factors, early warning, readmission prediction |

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

### combo -- Multi-Skill Chains (24 skills)

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
| [public-services-audit](combo/public-services-audit/) | 1.0.0 | /benefits-processing → /benefits-fraud → /government-compliance → /security-review | Government services compliance and fraud audit |
| [education-suite](combo/education-suite/) | 1.0.0 | /dropout-risk → /curriculum-optimizer → /student-personalization → /school-ops | Complete education system analysis pipeline |
| [housing-audit](combo/housing-audit/) | 1.0.0 | /affordable-housing → /eviction-risk → /housing-compliance → /rent-burden | Affordable housing compliance and risk assessment |
| [impact-org](combo/impact-org/) | 1.0.0 | /impact-measurement → /fundraising-optimizer → /grant-writer → /donor-retention | Nonprofit operational optimization pipeline |

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

## Social Impact Sectors

Skills for high-impact domains focused on human welfare, equity, and public good:

| Sector | Skills | Focus Areas |
|--------|--------|-------------|
| Healthcare (Beyond Hospitals) | mental-health-clinic, elder-care-ops, rural-health, disability-services, rehab-therapy, care-burnout-audit | Burnout reduction, care access, scheduling, risk flagging |
| Education | dropout-risk, curriculum-optimizer, student-personalization, teacher-workload, school-ops | K-12, higher ed, personalization, IDEA/Title I |
| Government & Public Services | benefits-processing, public-resource-allocation, emergency-response, government-compliance, benefits-fraud | FedRAMP, Section 508, FISMA, FOIA |
| Housing & Affordable Housing | affordable-housing, rent-burden, eviction-risk, housing-compliance | Fair Housing, HUD, LIHTC, Section 8 |
| Agriculture & Food Systems | crop-yield, food-waste, climate-risk-agriculture | Precision ag, food security, climate adaptation |
| Climate & Sustainability | carbon-accounting, disaster-prediction, sustainability-metrics, environmental-compliance | GHG Protocol, CDP, TCFD, SDGs, EPA |
| Legal Aid & Public Defense | legal-aid, case-outcome-predictor, rights-explainer | Access to justice, bias detection, plain language |
| Nonprofits & NGOs | fundraising-optimizer, grant-writer, impact-measurement, donor-retention | Impact measurement, grant management, donor CRM |
| Emergency & Crisis Services | crisis-triage, volunteer-coordination, emergency-resource | 911 dispatch, resource deployment, mutual aid |
| Elder Care & Caregiving | fall-risk, medication-adherence, caregiver-coordination | Wearable sensors, medication management, burnout |
| Mental Health & Behavioral | crisis-risk-monitor, treatment-outcome, care-plan-optimizer, therapist-documentation | PHQ-9/GAD-7, crisis protocols, HIPAA |
| Financial Literacy | debt-payoff, spending-behavior, retirement-optimizer | Payoff strategies, Monte Carlo, Social Security |
| Workforce Development | skill-gap, resume-optimizer, training-path, employer-matching | O*NET, ATS, competency-based, bias detection |
| Rehabilitation | recovery-metrics, therapy-personalization, setback-predictor | FIM/Barthel, exercise personalization, readmission |

### Industry & Social Impact Pipelines

```
/healthcare-audit       (runs: /hipaa → /clinical-data-review → /healthcare-compliance → /security-review)
/fintech-launch         (runs: /pci-dss → /fintech-api → /fraud-detection → /credit-risk → /preflight)
/logistics-optimize     (runs: /route-optimizer → /warehouse-ops → /inventory-forecast → /supply-chain-risk → /load-test)
/compliance-suite       (runs: /regulatory-compliance → /gdpr → /soc2 → /dependency-scan → /pentest)
/public-services-audit  (runs: /benefits-processing → /benefits-fraud → /government-compliance → /security-review)
/education-suite        (runs: /dropout-risk → /curriculum-optimizer → /student-personalization → /school-ops)
/housing-audit          (runs: /affordable-housing → /eviction-risk → /housing-compliance → /rent-burden)
/impact-org             (runs: /impact-measurement → /fundraising-optimizer → /grant-writer → /donor-retention)
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
