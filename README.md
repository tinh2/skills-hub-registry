# skills-hub-registry

The official skill collection for [skills-hub.ai](https://skills-hub.ai) -- a marketplace for Claude Code skills.

429 production-tested skills organized into 15 categories covering the complete software development lifecycle, 40 industry verticals and social-impact sectors, plus gaming and mobile app development. All skills ship as v2.0.0+ with built-in self-healing validation and self-evolution telemetry.

## Directory Structure

```
skills-hub-registry/
├── build            #  33 skills — Project Scaffolding & Build Pipelines
├── test             #  13 skills — Automated Testing
├── qa               #  15 skills — Quality Assurance
├── review           #  26 skills — Architecture, Code, Industry, Gaming & Mobile Review
├── deploy           #  18 skills — Infrastructure & Deployment
├── docs             #  11 skills — Documentation
├── security         #  12 skills — Security & Compliance
├── ux               #  26 skills — User Experience & Design
├── analysis         # 197 skills — Domain Analysis, Research & Industry Verticals
├── productivity     #   9 skills — Developer Experience
├── integration      #  13 skills — Third-Party Service Connectors
├── combo            #  34 skills — Multi-Skill Chains
├── meta             #  13 skills — Skills About Skills
├── education        #   8 skills — Learning & Onboarding
└── spec             #   1 skill  — Specification Authoring
```

## Architecture

### Main Skill + Sub-Skill Pattern

Most categories follow an orchestrator pattern where a **main skill** scans for gaps and routes work to specialized **sub-skills**. This allows running the main skill for broad coverage or invoking a sub-skill directly for targeted work.

| Main Skill    | Category     | Orchestrates                                                                                                        |
| ------------- | ------------ | ------------------------------------------------------------------------------------------------------------------- |
| `/integrate`  | integration  | auth-provider, stripe, email, push-notifications, search, storage, realtime, analytics-tracking                     |
| `/devops`     | deploy       | docker, github-actions, k8s, terraform, aws, cdn, dns, monitoring, secrets, app-icon                                |
| `/secure`     | security     | owasp, pentest, gdpr, soc2, encryption, dependency-scan, check-vanta                                                |
| `/test-suite` | test         | unit-test, e2e, integration-test, load-test, contract-test, accessibility-test, visual-regression, manual-test-plan |
| `/document`   | docs         | readme, api-docs, adr, changelog, diagram, onboarding, runbook, gen-catalog, skills-list                            |
| `/dx`         | productivity | devcontainer, env-setup, git-hooks, linter, monorepo, release                                                       |

**Standalone orchestrators** (no sub-skill routing, self-contained pipelines):

| Skill          | Category | What It Does                                                              |
| -------------- | -------- | ------------------------------------------------------------------------- |
| `/build`       | build    | Full project build from competitor analysis through implementation and QA |
| `/qa`          | qa       | Automated QA agent that walks every screen/endpoint, verifies, and fixes  |
| `/analyze`     | analysis | End-to-end domain analysis tracing features across all layers             |
| `/arch-review` | review   | Architect-level story review and implementation validation                |
| `/ux`          | ux       | Dual-mode UX quality audit (heuristics/a11y/motion) or design validation  |

### Duplicate Skill Names Across Categories

2 skill names appear in multiple categories. This is by design -- each implementation is different and tailored to its category's context. The full path (e.g., `analysis/backend-spec` vs `docs/backend-spec`) disambiguates them.

Duplicated names: `backend-spec` (analysis, docs), `design-to-code` (ux, combo).

## Skill Catalog

### build -- Project Scaffolding & Build Pipelines (33 skills)

| Skill                                               | Version | Description                                                                                                                                                                            |
| --------------------------------------------------- | ------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [ad-video](build/ad-video/)                         | 1.0.0   | Generate platform-optimized video ads from a product brief. Supports brand kits, 6 ad types, 6 platform formats (TikTok, Instagram, YouTube, Facebook, LinkedIn), batch...             |
| [android-app](build/android-app/)                   | 2.0.0   | Scaffold a production-ready native Android app -- generate a complete Kotlin project with Jetpack Compose UI, MVVM architecture, Hilt dependency injection, Room database with...      |
| [api-scaffold](build/api-scaffold/)                 | 2.0.0   | Scaffold a production-ready backend REST API -- generate a complete server project with routes, controllers, service layer, repository pattern, database models with migrations,...    |
| [app-builder](build/app-builder/)                   | 1.0.0   | Build working apps from plain English descriptions -- scaffolding, styling, and deployment with zero coding knowledge required. Triggers on: build me an app, I want to make,...       |
| [app-icon](build/app-icon/)                         | 2.0.0   | Generates professional app icons and applies them to any project. Triggers on mentions of icon, logo, branding, launcher icon, favicon, app icon, PWA icon, splash icon, or store...   |
| [automation-builder](build/automation-builder/)     | 1       | Build business automations from plain English -- scheduled tasks, file watchers, API integrations, and alerts with no coding required                                                  |
| [build](build/build/)                               | 2.0.0   | Full-stack app builder — takes a competitor app, idea, or spec and executes an 8-phase pipeline to produce a working application. Supports any tech stack. Trigger: build an app,...   |
| [chrome-extension](build/chrome-extension/)         | 2.0.0   | Build a complete Chrome browser extension with Manifest V3 -- generate popup UI with React 19 and Tailwind CSS, content scripts with Shadow DOM isolation, background service...       |
| [cli-tool](build/cli-tool/)                         | 2.0.0   | Generate a production-ready command-line tool -- scaffold a complete CLI application with subcommand parsing, interactive prompts with validation, colored and structured output...    |
| [content-creator](build/content-creator/)           | 1       | Generate blog posts, social media, email sequences, landing pages, and newsletters — SEO-optimized and platform-formatted                                                              |
| [cross-platform-app](build/cross-platform-app/)     | 2.0.0   | Scaffold a production-ready cross-platform mobile app -- auto-detect or select framework (Flutter with Riverpod and GoRouter, React Native with Redux Toolkit and React Navigation...  |
| [data-analyst](build/data-analyst/)                 | 1       | Analyze CSV, Excel, or JSON data — summaries, trends, charts, and plain-English insights with no coding required                                                                       |
| [db-migrate](build/db-migrate/)                     | 2.0.0   | Generates database migrations, updates ORM models, and verifies compilation. Auto-detects migration system, ORM, database, and language from the codebase.                             |
| [elevenlabs-voiceover](build/elevenlabs-voiceover/) | 1.0.0   | Generate professional AI voiceovers using ElevenLabs TTS for video narration, explainers, and content creation. Supports multiple voices, character presets (narrator, salesperson,... |
| [ffmpeg-media](build/ffmpeg-media/)                 | 1.0.0   | Process audio and video with FFmpeg -- encoding, format conversion, trimming, concatenation, audio extraction, noise reduction, volume normalization, watermarking, subtitle...        |
| [fintech-api](build/fintech-api/)                   | 2.0.0   | Scaffold a production-ready financial services API -- generate a complete fintech backend with Plaid bank account linking and transaction sync, ACH/wire/card payment processing...    |
| [flutter](build/flutter/)                           | 2.0.0   | Builds Flutter applications from videos, screenshots, descriptions, or app clone requests. Triggers on: flutter app, build a mobile app, replicate this app in Flutter, build from...  |
| [godot-scaffold](build/godot-scaffold/)             | 2.0.0   | Scaffolds a complete Godot 4 game project with scene tree, autoloads, signal bus, state machine, save system, export presets, and CI/CD. Triggers on: \"godot project\", \"godot...    |
| [healthcare-api](build/healthcare-api/)             | 2.0.0   | Scaffolds a FHIR R4-compliant healthcare API with clinical resource models, SMART on FHIR auth, HIPAA audit logging, PHI-safe error handling, and interoperability endpoints....       |
| [ios-app](build/ios-app/)                           | 2.0.0   | Scaffolds a native iOS app with SwiftUI, MVVM architecture, dependency injection, persistence, networking, push notifications, keychain, App Clips, and multi-environment Xcode...     |
| [iterate](build/iterate/)                           | 11      | Autonomous build loop — implements, tests, reviews, analyzes, and refines. Default 6 iterations (thorough) or --fast for 4 iterations (ship it quick).                                 |
| [nextjs](build/nextjs/)                             | 2.0.0   | Builds a production-ready Next.js 15 app with App Router, Server Components, authentication, Prisma database, and a full dashboard UI from a description or brief. Triggers on:...     |
| [react-native](build/react-native/)                 | 2.0.0   | Builds a production-ready React Native mobile app from designs, screenshots, or descriptions using Expo, typed navigation, TanStack Query, and full screen implementations....         |
| [remotion](build/remotion/)                         | 1.0.0   | Build programmatic videos with Remotion (React). Covers compositions, animations, sequencing, transitions, audio/video embedding, spring physics, text animations, voiceover...        |
| [ship](build/ship/)                                 | 2.1.0   | Fast autonomous build loop -- 4 iterations max. Ship it, quick build, fast implementation, just build it, ship fast.                                                                   |
| [social-clip](build/social-clip/)                   | 1.0.0   | Create short-form social media videos for TikTok, Instagram Reels, YouTube Shorts, and more. Two modes -- create from scratch with a brief, or repurpose long-form video into short... |
| [story-implementer](build/story-implementer/)       | 2.1.0   | Implements a story, spec, or ticket from any format (text, image, structured doc) using the repository's existing conventions. Writes tests, commits, and creates a PR. Trigger...     |
| [tutorial-video](build/tutorial-video/)             | 0.1.0   | Create Fireship-quality developer tutorial videos from annotated markdown and terminal recordings. Animated code transitions (Code Hike + Shiki Magic Move), terminal replay...        |
| [unity-scaffold](build/unity-scaffold/)             | 2.0.0   | Scaffolds a Unity game project with folder structure, assembly definitions, new Input System, scriptable object architecture, scene management, Git LFS, and CI/CD via GameCI....      |
| [unreal-scaffold](build/unreal-scaffold/)           | 2.0.0   | Scaffolds an Unreal Engine 5 project with C++ module structure, Enhanced Input, Gameplay Ability System, subsystem architecture, .uproject config, and CI/CD via BuildGraph....        |
| [video-toolkit](build/video-toolkit/)               | 1.0.0   | Create professional videos autonomously using AI -- voiceovers (Qwen3-TTS with voice cloning), image generation (FLUX.2), background music (MusicGen), talking head animation...       |
| [web-game](build/web-game/)                         | 2.0.0   | Scaffolds a browser-based game with Phaser 3, PixiJS, or Three.js including game loop, asset pipeline, responsive canvas, input handling, audio, save/load, and deployment to...       |
| [wedding-video](build/wedding-video/)               | 1.0.0   | Create cinematic wedding montage videos from photos and songs using Remotion. Features act-based narrative structure (5 acts), Ken Burns photo animations, multi-song audio with...    |

### test -- Automated Testing (13 skills)

| Skill                                          | Version | Description                                                                                                                                                                           |
| ---------------------------------------------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [accessibility-test](test/accessibility-test/) | 2.0.0   | Automated WCAG 2.1 AA accessibility testing with axe-core and Lighthouse CI. Auto-detects frontend framework (React, Next.js, Vue, Angular, Svelte, Astro, Flutter, React Native),... |
| [contract-test](test/contract-test/)           | 2.0.0   | Generate consumer-driven contract tests for APIs. Auto-detects framework (Express, Fastify, NestJS, Django, FastAPI, Go), selects Pact, OpenAPI validation, or schema snapshots,...   |
| [device-matrix](test/device-matrix/)           | 2.0.0   | Configure device matrix testing across real phones, tablets, and emulators. Sets up Firebase Test Lab, AWS Device Farm, or BrowserStack with smart device selection covering...       |
| [e2e](test/e2e/)                               | 2.0.0   | Auto-detects any tech stack, generates and runs exhaustive end-to-end tests. Triggered by "end-to-end tests", "e2e tests", "integration tests", "test the whole app", "generate...    |
| [full-test](test/full-test/)                   | 2.0.0   | Complete testing pipeline — full test suite, test everything, automated and manual tests.                                                                                             |
| [integration-test](test/integration-test/)     | 2.0.0   | Generate integration tests for APIs, databases, and external services. Auto-detects backend stack (Express, Fastify, NestJS, Django, FastAPI, Rails, Go), ORM (Prisma, TypeORM,...    |
| [load-test](test/load-test/)                   | 2.0.0   | Generate and run load tests with k6, Locust, or Artillery. Auto-detects API framework, creates realistic user behavior flows (browsing, authenticated CRUD, search-heavy), runs...    |
| [manual-test-plan](test/manual-test-plan/)     | 2.0.0   | Generates a manual test plan, QA plan, test scenarios, testing checklist, or guidance on how to test changes. Works from branch diffs, stories, specs, or requirements.               |
| [mobile-test](test/mobile-test/)               | 2.0.0   | Generate a complete mobile test suite covering unit, widget, integration, snapshot, accessibility, and platform-specific tests. Auto-detects Flutter, React Native, native iOS...     |
| [test-suite](test/test-suite/)                 | 2.0.0   | Analyze and score test coverage across all testing dimensions -- unit, integration, E2E, load, visual regression, contract, and accessibility. Auto-detects tech stack and test...    |
| [unit-test](test/unit-test/)                   | 2.0.0   | Generate comprehensive unit tests with edge cases, error paths, and boundary values. Auto-detects test framework (Vitest, Jest, pytest, go test, flutter_test, RSpec, cargo test,...  |
| [visual-regression](test/visual-regression/)   | 2.0.0   | Set up visual regression testing with baseline screenshots across breakpoints. Auto-detects frontend framework (Next.js, React, Vue, Angular, Flutter, Storybook), configures...      |
| [walkthrough](test/walkthrough/)               | 2.0.0   | Run an app walkthrough — launch a Flutter app on a simulator or emulator, generate and run exhaustive integration tests that exercise every screen, button, form, and user flow,...   |

### qa -- Quality Assurance (15 skills)

| Skill                                            | Version | Description                                                                                                                                                                            |
| ------------------------------------------------ | ------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [audit](qa/audit/)                               | 2.0.0   | Fast quality gate — detects stack, runs static analysis, checks cross-layer consistency, fixes issues. Run between every pipeline phase, before every commit push, after every...      |
| [balance-test](qa/balance-test/)                 | 2.0.0   | Analyze game balance by extracting stats from code and running mathematical simulations. Calculates DPS tier lists, TTK matrices, EHP comparisons, and character power rankings....    |
| [broken-links](qa/broken-links/)                 | 1.1.0   | Scan a codebase for broken links — dead URLs in Markdown/HTML, broken file references, invalid import paths, stale anchor links, and broken cross-doc references — then auto-fix...    |
| [chaos](qa/chaos/)                               | 2.0.0   | Chaos engineering analysis that maps every external dependency and I/O boundary, then generates tests for timeouts, connection failures, corrupt responses, disk errors, OOM,...       |
| [code-smell](qa/code-smell/)                     | 2.0.0   | Scan codebase for Martin Fowler's catalog of code smells: god classes, long methods, feature envy, data clumps, primitive obsession, shotgun surgery, message chains, and more....     |
| [dead-code](qa/dead-code/)                       | 2.0.0   | Find and safely remove dead code: unreachable paths, unused exports, unused functions, unused variables, unused CSS selectors, unused npm/pip/cargo dependencies, unused env vars,...  |
| [game-qa](qa/game-qa/)                           | 2.0.0   | Run a full game QA audit on Unity, Unreal, Godot, or web game projects. Finds null reference bugs, missing asset references, broken scene transitions, physics edge cases, input...    |
| [iterate-review](qa/iterate-review/)             | 6.0.0   | Autonomously review and improve existing code through up to 5 iterations of analysis, domain verification, fixing, and validation.                                                     |
| [migration-verify](qa/migration-verify/)         | 2.0.0   | Verify database migrations are safe before running them. Checks that migrations apply cleanly, reverse cleanly, preserve data integrity, are idempotent, and will not lock tables...   |
| [mobile-qa](qa/mobile-qa/)                       | 2.0.0   | Run a comprehensive mobile app QA audit covering permission flows, deep link verification, push notification delivery, offline mode resilience, background/foreground state...         |
| [perf](qa/perf/)                                 | 2.0.0   | Performance profiler — analyzes DB queries (any ORM), API call chains, memory usage, bundle sizes, network waterfalls, and frontend rendering. Produces ranked optimization...         |
| [preflight](qa/preflight/)                       | 2.0.0   | Pre-deploy verification gate. Checks git status, build, tests, migrations, secrets, and commit conventions. Reports READY or NOT READY. Read-only, no changes. Trigger words:...       |
| [qa](qa/qa/)                                     | 4.1.0   | Automated QA agent that starts the app, walks through every screen and API endpoint, verifies functionality, evaluates modern design and usability, runs domain analysis, and fixes... |
| [scale-audit](qa/scale-audit/)                   | 1.0.0   | Scalability audit — identifies performance bottlenecks, unbounded queries, N+1 patterns, missing indexes, synchronous blocking operations on hot paths, and memory pressure points.... |
| [stress-test-personas](qa/stress-test-personas/) | 2.0.0   | Stress-test your product through 6 adversarial decision-maker personas -- skeptical board member, activist investor, power user, churned customer, competitor CEO, and enterprise...   |

### review -- Architecture, Code, Industry, Gaming & Mobile Review (26 skills)

| Skill                                                        | Version | Description                                                                                                                                                                            |
| ------------------------------------------------------------ | ------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [api-review](review/api-review/)                             | 2.0.0   | Review API design against REST best practices and internal consistency. Audits naming conventions, HTTP method semantics, status code correctness, pagination and filtering...         |
| [arch-review](review/arch-review/)                           | 12.1.0  | Architect-level story review with component reuse, domain consistency, data privacy, service architecture, and infrastructure checks. Design review before coding or implementation... |
| [care-burnout-audit](review/care-burnout-audit/)             | 2.0.0   | Audit healthcare and caregiving software for provider burnout risk factors. Analyzes workload distribution fairness, scheduling equity, documentation burden, alert fatigue...         |
| [cfo-review](review/cfo-review/)                             | 2.0.0   | Conduct a CFO-perspective financial impact review of a codebase. Analyzes infrastructure costs and scaling projections, pricing model alignment with architecture, build-vs-buy...     |
| [cpo-review](review/cpo-review/)                             | 2.0.0   | Conduct a CPO-perspective product strategy review of a codebase. Evaluates feature completeness against core value proposition, time-to-value for new users, user journey quality,...  |
| [cto-review](review/cto-review/)                             | 2.0.0   | Conduct a CTO-perspective technical strategy review of a codebase. Evaluates architecture decisions and build-vs-buy trade-offs, scaling readiness at 10x and 100x, engineering...     |
| [database-review](review/database-review/)                   | 2.0.0   | Review database schema design, query patterns, and data access layer for correctness and performance. Checks normalization balance, index coverage against actual queries,...          |
| [energy-compliance](review/energy-compliance/)               | 2.0.0   | Audit energy utility software for NERC CIP cybersecurity, FERC market and tariff compliance, EPA emissions and CEMS reporting, renewable portfolio standards (RPS/REC tracking),...    |
| [environmental-compliance](review/environmental-compliance/) | 2.0.0   | Audit environmental software for EPA reporting (CEDRI, NetDMR, RCRAInfo), Clean Air Act (Title V, NESHAP, CEMS, TRI), Clean Water Act (NPDES, SWPPP, SPCC), RCRA hazardous waste...    |
| [financial-compliance](review/financial-compliance/)         | 2.0.0   | Audit fintech and financial services code for KYC/AML (CIP, CDD, EDD, sanctions screening, transaction monitoring), BSA (SAR/CTR filing, FinCEN reporting, Travel Rule), Reg E (EFT... |
| [game-accessibility](review/game-accessibility/)             | 2.0.0   | Audit game projects for accessibility across visual (colorblind modes, contrast, font scaling, photosensitivity), audio (subtitles, captions, visual sound indicators, mono audio),... |
| [game-code-review](review/game-code-review/)                 | 2.0.0   | Review game code architecture for component coupling, ECS vs OOP design, update loop organization (deltaTime, fixed timestep, frame budget), state machine quality (boolean soup,...   |
| [government-compliance](review/government-compliance/)       | 2.0.0   | Audit government and federal software for FedRAMP authorization readiness (Low/Moderate/High), NIST 800-53 controls (AC, AU, CM, IA, SC, SI families), FISMA compliance, Section...    |
| [healthcare-ops](review/healthcare-ops/)                     | 2.0.0   | Review healthcare software for operational efficiency: appointment scheduling and resource allocation, clinical workflow burden (order entry clicks, documentation templates, alert... |
| [housing-compliance](review/housing-compliance/)             | 2.0.0   | Audit affordable housing and property management software for Fair Housing Act (protected classes, disparate impact screening, AFFH), Section 504/ADA accessibility (5% mobility...    |
| [manufacturing-compliance](review/manufacturing-compliance/) | 2.0.0   | Audit manufacturing software for FDA 21 CFR Part 11 (electronic records, e-signatures, audit trails), ISO 9001/13485/14001/45001 quality management (document control, CAPA,...        |
| [mobile-security-review](review/mobile-security-review/)     | 2.0.0   | Audit mobile apps against OWASP Mobile Top 10 (M1-M10): credential hardcoding, supply chain dependencies, insecure auth/token storage (Keychain/Keystore), input validation (deep...   |
| [multiplayer-review](review/multiplayer-review/)             | 2.0.0   | Audit multiplayer netcode, online game networking, and real-time synchronization. Reviews client-server authority, lag compensation, client-side prediction, server reconciliation,... |
| [permit-compliance](review/permit-compliance/)               | 2.0.0   | Audit construction permit tracking, building code compliance, and inspection management software. Reviews permit lifecycle workflows (building, electrical, plumbing, mechanical,...   |
| [pr](review/pr/)                                             | 2.0.0   | Create a convention-compliant pull request from the current branch.                                                                                                                    |
| [procurement-review](review/procurement-review/)             | 2.0.0   | Audit procurement and procure-to-pay software for sourcing, purchasing, and vendor management. Reviews requisition-to-PO workflows, RFQ/RFP bid management, approval routing with...   |
| [regulatory-compliance](review/regulatory-compliance/)       | 2.0.0   | Audit codebases for cross-industry regulatory compliance across SOX, GDPR, HIPAA, PCI-DSS, CCPA/CPRA, FedRAMP, FISMA, COPPA, and FERPA. Reviews audit trail completeness...            |
| [school-ops](review/school-ops/)                             | 2.0.0   | Audit K-12 school operations, district management, and education administration software. Reviews master schedule building and constraint optimization, student course request...      |
| [security-review](review/security-review/)                   | 2.0.0   | Security audit and vulnerability assessment for any codebase. Scans for authentication bypasses, missing auth middleware, broken JWT validation (algorithm confusion, weak secrets,... |
| [store-compliance](review/store-compliance/)                 | 2.0.0   | Pre-submission audit for Apple App Store and Google Play Store compliance. Checks App Store Review Guidelines (safety, performance, business, design, legal sections) and Google...    |
| [therapist-documentation](review/therapist-documentation/)   | 2.0.0   | Audit therapy and behavioral health documentation platforms for clinical quality and regulatory compliance. Reviews SOAP, DAP, and BIRP note template structure, note completeness...  |

### deploy -- Infrastructure & Deployment (18 skills)

| Skill                                            | Version | Description                                                                                                                                                                            |
| ------------------------------------------------ | ------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [app-store-publish](deploy/app-store-publish/)   | 2.0.0   | Configure a complete iOS App Store publishing pipeline — sets up Fastlane with code signing (match), App Store Connect API key, TestFlight and release lanes, screenshot...            |
| [aws](deploy/aws/)                               | 2.1.0   | Generates production-ready Terraform files for AWS infrastructure. Writes complete .tf files for any cloud architecture — no deployment, just file generation.                         |
| [cdn](deploy/cdn/)                               | 2.0.0   | Configure a CDN with optimized caching, SSL/TLS, security headers, and cache invalidation — auto-detects hosting provider and app type, generates CloudFront, Cloudflare, or Vercel... |
| [ci-fixer](deploy/ci-fixer/)                     | 1       | Scan all repos for failing or stuck GitHub Actions workflows, diagnose issues, and fix them. Use when: 'fix ci', 'ci is broken', 'github actions failing', 'unblock ci', 'clear...     |
| [devops](deploy/devops/)                         | 2.0.0   | Audit deployment readiness across CI/CD, containers, monitoring, IaC, secrets, CDN, and DNS — score each area 0-100, identify critical gaps, and optionally auto-fix by chaining...    |
| [dns](deploy/dns/)                               | 2.0.0   | Set up DNS records, SSL/TLS certificates, subdomains, SPF/DKIM/DMARC email authentication, and health-check failover routing for Route53, Cloudflare, or GCP Cloud DNS — with...       |
| [docker](deploy/docker/)                         | 2.0.0   | Detect project stack and generate production-ready multi-stage Dockerfiles with compose services, .dockerignore, non-root users, health checks, layer caching, and optional dev...     |
| [flutter-deploy](deploy/flutter-deploy/)         | 1.0.0   | Build and deploy Flutter apps to App Store (TestFlight) and Google Play (internal/production). Auto-detects project structure, pulls signing secrets from AWS Secrets Manager,...      |
| [free-keys](deploy/free-keys/)                   | 2.0.0   | Provision free LLM API keys from 20+ providers. Health-checks existing keys, opens signup pages, validates new keys, and saves them to your project.                                   |
| [github-actions](deploy/github-actions/)         | 2.0.0   | Detect project stack and generate GitHub Actions CI/CD workflows — PR checks with lint/test/build/security, deploy pipelines for Vercel/AWS/GCP/Fly/Docker, dependency caching,...     |
| [hotfix](deploy/hotfix/)                         | 2.1.0   | Emergency bug fix pipeline — diagnose, fix, test, commit, push, and PR in 2 iterations max. Speed over perfection.                                                                     |
| [k8s](deploy/k8s/)                               | 2.0.0   | Generate production-grade Kubernetes manifests — Deployments with probes and security contexts, Services, Ingress with TLS, HPA, PDB, NetworkPolicy, ConfigMaps, Secrets — with...     |
| [mobile-ci-cd](deploy/mobile-ci-cd/)             | 2.0.0   | Set up mobile CI/CD pipelines for Flutter, React Native, or native iOS/Android — GitHub Actions workflows for testing, code signing, TestFlight/Play Store distribution, build...      |
| [monitoring](deploy/monitoring/)                 | 2.0.0   | Set up application observability with Prometheus, Grafana, Datadog, or CloudWatch — instrument metrics endpoints, configure Golden Signal dashboards, define alert rules with...       |
| [ota-updates](deploy/ota-updates/)               | 2.0.0   | Configure over-the-air mobile updates — Shorebird for Flutter, CodePush or EAS Update for React Native — with update channels, staged rollout, forced vs optional update policies,...  |
| [play-store-publish](deploy/play-store-publish/) | 2.0.0   | Configure the complete Google Play Store publishing pipeline — upload key generation, AAB bundle optimization, Fastlane supply lanes for internal/beta/production tracks, staged...    |
| [secrets](deploy/secrets/)                       | 2.0.0   | Audit codebases for leaked secrets and hardcoded credentials, generate .env templates, configure secrets management with AWS Secrets Manager, Vault, Doppler, or GCP Secret...         |
| [terraform](deploy/terraform/)                   | 2.0.0   | Generate Terraform infrastructure-as-code for AWS, GCP, or Azure. Creates modular VPC, compute, database, cache, CDN, and monitoring configs with per-environment sizing, remote...    |

### docs -- Documentation (11 skills)

| Skill                                  | Version | Description                                                                                                                                                                          |
| -------------------------------------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [adr](docs/adr/)                       | 2.0.0   | Create and manage Architecture Decision Records using the Michael Nygard format. Supports new ADR creation, retrospective analysis to document existing decisions, superseding,...   |
| [api-docs](docs/api-docs/)             | 2.0.0   | Generate OpenAPI 3.1 documentation from your API codebase. Auto-detects Express, Fastify, NestJS, Django, FastAPI, Flask, Rails, Spring, Go, and more. Extracts routes,...           |
| [engineering-spec](docs/backend-spec/) | 2.0.0   | Generates structured engineering specs (backend or frontend) from feature descriptions, designs, or ticket references. Triggers on "spec", "story", "ticket", "engineering spec",... |
| [blog-writer](docs/blog-writer/)       | 1       | Write human-sounding, SEO-optimized blog posts for skills-hub.ai. Use when: 'write a blog post', 'draft a post', 'update blog', 'blog about', 'write about'. Supports styles:...     |
| [changelog](docs/changelog/)           | 2.0.0   | Generate or update CHANGELOG.md from git history. Parses conventional commits, groups by version tags, categorizes into Added/Fixed/Changed/Breaking sections using...               |
| [diagram](docs/diagram/)               | 2.0.0   | Generate Mermaid architecture diagrams from your codebase. Produces C4 context and container diagrams, sequence diagrams for key flows, ER diagrams from database schemas, and...    |
| [document](docs/document/)             | 2.0.0   | Audit your project's documentation health and identify gaps. Scans for README, changelog, API docs, ADRs, runbooks, onboarding guides, and diagrams. Scores coverage against...      |
| [gen-catalog](docs/gen-catalog/)       | 2.0.0   | Generate skill catalog — auto-discovers skills, builds README tables, JSON, or HTML output. Triggers: generate skill catalog, update skills documentation, list all skills           |
| [onboarding](docs/onboarding/)         | 2.0.0   | Generate a comprehensive developer onboarding guide from your codebase. Analyzes tech stack, project structure, build commands, environment variables, code conventions, and git...  |
| [readme](docs/readme/)                 | 2.0.0   | Generate project documentation — README files, API docs, and changelogs. Triggers: README, documentation, generate docs, document this project, write README, API docs, changelog.   |
| [runbook](docs/runbook/)               | 2.0.0   | Generate an operations runbook from your deployment config, Docker/K8s manifests, CI/CD pipelines, and monitoring setup. Produces copy-pasteable procedures for deployment,...       |

### security -- Security & Compliance (12 skills)

| Skill                                        | Version | Description                                                                                                                                                                            |
| -------------------------------------------- | ------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [benefits-fraud](security/benefits-fraud/)   | 2.0.0   | Audit government benefits and entitlement systems for fraud prevention, detection, and recovery capabilities. Assesses identity proofing (document verification, SSA cross-match,...   |
| [check-vanta](security/check-vanta/)         | 2.0.0   | Fetches dependency vulnerabilities from Vanta, Snyk, Dependabot, or GitHub Security Advisories, creates a tracking issue in Jira/Linear/GitHub Issues, then fixes, commits, pushes,... |
| [dependency-scan](security/dependency-scan/) | 2.0.0   | Scan project dependencies for known vulnerabilities (CVEs), auto-fix safe patches, and generate SBOM. Auto-detects all package managers in monorepos — npm (npm audit), yarn (yarn...  |
| [encryption](security/encryption/)           | 2.0.0   | Audit and harden encryption across the full stack. Checks data-at-rest encryption (database TDE, field-level AES-256-GCM, file storage SSE, backup encryption), data-in-transit...     |
| [game-security](security/game-security/)     | 2.0.0   | Game-specific security review covering cheat prevention, exploit surfaces, and server authority. Audits client-side authority vulnerabilities (damage, health, currency, cooldown,...  |
| [gdpr](security/gdpr/)                       | 2.0.0   | GDPR and CCPA/CPRA privacy compliance audit for codebases. Inventories PII fields (email, phone, SSN, IP, device ID, geolocation, biometrics, behavioral data), maps data...           |
| [hipaa](security/hipaa/)                     | 2.0.0   | Deep HIPAA Security Rule technical audit mapping code-level findings to 45 CFR sections. Covers administrative safeguards (164.308 -- risk analysis, workforce security, access...     |
| [owasp](security/owasp/)                     | 2.0.0   | Systematic audit against the OWASP 2021 Top 10 web application security risks with severity-rated, file-level findings. Checks A01 Broken Access Control (IDOR, path traversal,...     |
| [pci-dss](security/pci-dss/)                 | 2.0.0   | PCI DSS v4.0 compliance audit for payment-handling codebases. Scans for PAN patterns (Visa, Mastercard, Amex, Discover), CVV storage violations, and track data retention. Audits...   |
| [pentest](security/pentest/)                 | 2.0.0   | Static-analysis penetration test that hunts for exploitable vulnerabilities with proof-of-concept payloads and fix code. Covers SQL and NoSQL injection (string concatenation, raw...  |
| [secure](security/secure/)                   | 2.0.0   | Full-stack security posture assessment with 0-100 risk scoring. Scans dependency vulnerabilities (npm audit, pip-audit, cargo audit, govulncheck), dangerous code patterns (SQL...     |
| [soc2](security/soc2/)                       | 2.0.0   | SOC 2 Type II readiness assessment against all five Trust Service Criteria. Evaluates Security controls (CC6/CC7 -- RBAC, access provisioning/removal, network segmentation, TLS...    |

### ux -- User Experience & Design (26 skills)

| Skill                                    | Version | Description                                                                                                                                                                            |
| ---------------------------------------- | ------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [dark-mode](ux/dark-mode/)               | 2.0.0   | Implement complete dark mode for any frontend project. Auto-detects theme system (Flutter ThemeData, Tailwind dark class, CSS variables, MUI, Chakra UI, styled-components),...        |
| [design-adapt](ux/design-adapt/)         | 1.0.0   | Make interfaces truly adaptive — not just responsive. Uses container queries for component-level adaptation, adaptive navigation patterns, and platform-aware layouts for web,...      |
| [design-amplify](ux/design-amplify/)     | 1.0.0   | Amplify safe, boring designs into visually confident interfaces. Increases contrast, adds dramatic typography, introduces bold color, and creates visual tension. Makes designs...     |
| [design-animate](ux/design-animate/)     | 1.0.0   | Add purposeful motion to interfaces using modern CSS — scroll-driven animations, view transitions, @starting-style, and GPU-accelerated transforms. Zero JS animation libraries...     |
| [design-audit](ux/design-audit/)         | 1.0.0   | Comprehensive autonomous design quality audit across accessibility (WCAG 2.2), performance, theming, responsive/adaptive design, and anti-pattern detection. Produces a prioritized... |
| [design-build](ux/design-build/)         | 1.0.0   | Build distinctive, production-grade interfaces with Ralph Wiggum velocity. Ships working code — web or mobile — with modern CSS, fluid typography, purposeful motion, and zero...      |
| [design-claude](ux/design-claude/)       | 1.0.0   | HTML-first hi-fi design skill: interactive prototypes, slide decks, animation demos, design variant exploration, visual direction advising, and expert critique. Triggers: make a...   |
| [design-color](ux/design-color/)         | 1.0.0   | Add strategic color to monochromatic or dull interfaces using oklch for perceptually uniform palettes. Generates harmonious color systems with automatic light/dark variants and...    |
| [design-copy](ux/design-copy/)           | 1.0.0   | Autonomous UX copy improvement — rewrites unclear labels, error messages, microcopy, CTAs, tooltips, and onboarding text. Makes every word earn its place. Supports web and mobile.    |
| [design-critique](ux/design-critique/)   | 1.0.0   | Autonomous design effectiveness evaluation — visual hierarchy, information architecture, emotional resonance, and craft quality. Produces actionable feedback with specific...         |
| [design-delight](ux/design-delight/)     | 1.0.0   | Add moments of joy — success celebrations, subtle hover reactions, personality in empty states, easter eggs, and contextual surprises. Elevates functional to memorable without...     |
| [design-harden](ux/design-harden/)       | 1.0.0   | Make interfaces bulletproof — error boundaries, loading states, empty states, text overflow, i18n readiness, offline handling, and every edge case that breaks in production. Makes... |
| [design-normalize](ux/design-normalize/) | 1.0.0   | Normalize a codebase to its design system — replace hardcoded values with tokens, enforce consistent component usage, align spacing/typography/color with the established system....   |
| [design-onboard](ux/design-onboard/)     | 1.0.0   | Design or improve onboarding flows, empty states, and first-time experiences. Progressive disclosure over feature dumps. Contextual guidance over tutorials. Makes users successful... |
| [design-optimize](ux/design-optimize/)   | 1.0.0   | Autonomous performance optimization for interfaces — content-visibility, CSS containment, scroll-driven animations replacing JS, view transitions replacing SPA transitions, image...  |
| [design-polish](ux/design-polish/)       | 1.0.0   | Final autonomous quality pass before shipping. Fixes alignment, spacing, consistency, typography hierarchy, color harmony, motion timing, and every micro-detail that separates...     |
| [design-setup](ux/design-setup/)         | 1.0.0   | One-time autonomous design context discovery. Scans the codebase to extract design tokens, typography, colors, spacing, brand patterns, and tech stack, then writes a Design...        |
| [design-simplify](ux/design-simplify/)   | 1.0.0   | Strip interfaces to their essence — remove unnecessary complexity, reduce visual noise, simplify navigation, and eliminate redundant UI elements. Great design is simple, powerful,... |
| [design-system](ux/design-system/)       | 2.0.0   | Extract and formalize a design system from existing UI code. Scans for every hardcoded color, font size, spacing value, border radius, and shadow across the codebase, deduplicates... |
| [design-to-code](ux/design-to-code/)     | 1.0.0   | Turn a design into production-quality frontend code: extract a design system with tokens and components, make layouts responsive across breakpoints, add dark mode with...             |
| [design-tokens](ux/design-tokens/)       | 1.0.0   | Extract, consolidate, and modernize design tokens — oklch color scales, fluid spacing with clamp(), typography scales, motion timing, and shadow depths. Builds a systematic token...  |
| [design-tone-down](ux/design-tone-down/) | 1.0.0   | Reduce visual intensity without losing design quality. Softens aggressive colors, calms excessive animations, balances overwhelming layouts, and restores visual breathing room.       |
| [game-ux](ux/game-ux/)                   | 2.0.0   | Audit game user experience across HUD clarity, menu navigation, tutorial effectiveness, control responsiveness, camera systems, feedback loops, loading screens, and settings...       |
| [i18n](ux/i18n/)                         | 2.0.0   | Set up internationalization by extracting all hardcoded user-facing strings to locale files. Auto-detects framework (Flutter, Next.js, React, Vue, Angular, iOS, Android) and...       |
| [responsive](ux/responsive/)             | 2.0.0   | Audit and fix responsive design issues across all breakpoints. Scans for fixed widths that cause mobile overflow, missing media query variants, non-responsive images, undersized...   |
| [ux](ux/ux/)                             | 2.1.0   | Dual-mode UX quality skill — runs a heuristic/accessibility/motion audit on the current codebase, or validates implementation against design mockups. Fixes all issues found and...    |

### analysis -- Domain Analysis, Research & Industry Verticals (197 skills)

| Skill                                                              | Version | Description                                                                                                                                                                            |
| ------------------------------------------------------------------ | ------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [actuarial-modeling](analysis/actuarial-modeling/)                 | 2.0.0   | >                                                                                                                                                                                      |
| [ad-yield-optimization](analysis/ad-yield-optimization/)           | 2.0.0   | >                                                                                                                                                                                      |
| [affordable-housing](analysis/affordable-housing/)                 | 2.0.0   | >                                                                                                                                                                                      |
| [alert-prioritization](analysis/alert-prioritization/)             | 2.0.0   | >                                                                                                                                                                                      |
| [analyze](analysis/analyze/)                                       | 2.0.0   | Deep cross-layer consistency audit for any codebase. Traces every feature from UI to database, finds broken wiring, missing handlers, model mismatches, and security gaps....          |
| [api-surface](analysis/api-surface/)                               | 2.0.0   | >                                                                                                                                                                                      |
| [app-size-optimizer](analysis/app-size-optimizer/)                 | 2.0.0   | >                                                                                                                                                                                      |
| [app-store-optimization](analysis/app-store-optimization/)         | 2.0.0   | >                                                                                                                                                                                      |
| [apparel-demand](analysis/apparel-demand/)                         | 2.0.0   | >                                                                                                                                                                                      |
| [asset-lifecycle](analysis/asset-lifecycle/)                       | 2.0.0   | >                                                                                                                                                                                      |
| [audit-support](analysis/audit-support/)                           | 2.0.0   | >                                                                                                                                                                                      |
| [backend-spec](analysis/backend-spec/)                             | 6.1.0   | Generates backend or frontend engineering specs in structured Jira format with description, categorized acceptance criteria, routes, dev notes, and table schemas.                     |
| [batch-optimization](analysis/batch-optimization/)                 | 2.0.0   | >                                                                                                                                                                                      |
| [behavioral-segmentation](analysis/behavioral-segmentation/)       | 2.0.0   | >                                                                                                                                                                                      |
| [benefits-processing](analysis/benefits-processing/)               | 2.0.0   | >                                                                                                                                                                                      |
| [bookkeeping-automation](analysis/bookkeeping-automation/)         | 2.0.0   | >                                                                                                                                                                                      |
| [box-optimization](analysis/box-optimization/)                     | 2.0.0   | >                                                                                                                                                                                      |
| [budget-allocation](analysis/budget-allocation/)                   | 2.0.0   | >                                                                                                                                                                                      |
| [bundle-analysis](analysis/bundle-analysis/)                       | 2.0.0   | >                                                                                                                                                                                      |
| [carbon-accounting](analysis/carbon-accounting/)                   | 2.0.0   | >                                                                                                                                                                                      |
| [care-plan-optimizer](analysis/care-plan-optimizer/)               | 2.0.0   | >                                                                                                                                                                                      |
| [caregiver-coordination](analysis/caregiver-coordination/)         | 2.0.0   | >                                                                                                                                                                                      |
| [case-outcome-predictor](analysis/case-outcome-predictor/)         | 2.0.0   | Audit legal case prediction systems for bias, fairness, accuracy, and ethical guardrails. Use when: 'check my prediction model for bias', 'audit case outcome fairness', 'evaluate...  |
| [catastrophe-modeling](analysis/catastrophe-modeling/)             | 2.0.0   | Analyze catastrophe modeling systems for natural disaster exposure, PML estimation, and reinsurance optimization. Use when: 'assess cat model', 'evaluate disaster exposure',...       |
| [claims-workflow](analysis/claims-workflow/)                       | 2.0.0   | Analyze insurance claims workflow systems for intake optimization, adjudication rules, subrogation, litigation management, and settlement analytics. Use when: 'audit claims...        |
| [climate-risk-agriculture](analysis/climate-risk-agriculture/)     | 2.0.0   | Analyze agricultural climate risk systems for weather impact modeling, crop insurance, drought/flood prediction, soil moisture, and carbon tracking. Use when: 'assess crop climate... |
| [clinical-data-review](analysis/clinical-data-review/)             | 2.0.0   | Review clinical data models and APIs for HL7 FHIR conformance, terminology standards, interoperability, and clinical workflow correctness. Use when: 'check FHIR compliance',...       |
| [cnc-furniture](analysis/cnc-furniture/)                           | 1.0.0   | >-                                                                                                                                                                                     |
| [codebase-health](analysis/codebase-health/)                       | 2.0.0   | Score your codebase 0-100 across complexity, coupling, cohesion, test coverage, documentation, churn hotspots, dependency health, and lint/type safety. Use when: 'how healthy is...   |
| [commodity-pricing](analysis/commodity-pricing/)                   | 2.0.0   | Analyze commodity pricing and trading systems including forward curves, option models, position management, risk metrics, and regulatory reporting. Use when: 'review pricing...       |
| [compete](analysis/compete/)                                       | 2.0.0   | Competitive intelligence and market positioning analysis. Researches competitors, compares features, pricing, and tech stacks, then produces a prioritized gap analysis with...        |
| [compliance-ops](analysis/compliance-ops/)                         | 2.0.0   | Analyze compliance operations for regulatory change tracking, control mapping, policy management, audit readiness, and training compliance. Use when: 'audit compliance program',...   |
| [consumer-modeling](analysis/consumer-modeling/)                   | 2.0.0   | Analyze consumer modeling systems for purchase prediction, lifetime value estimation, multi-touch attribution, brand affinity, and switching cost analysis. Use when: 'evaluate CLV... |
| [content-performance](analysis/content-performance/)               | 2.0.0   | Analyze content engagement metrics, audience retention, attribution models, A/B test results, and recommendation engine effectiveness. Use when: 'audit content metrics', 'evaluate... |
| [contract-risk](analysis/contract-risk/)                           | 2.0.0   | Audit contract management codebases for clause extraction accuracy, obligation tracking completeness, risk scoring model quality, renewal management, SLA monitoring, liability...     |
| [cost-analysis](analysis/cost-analysis/)                           | 2.0.0   | Analyzes infrastructure costs at 1K-100K user scales by reading the actual codebase, auto-detecting cloud providers, modeling per-action costs, and projecting total monthly spend...  |
| [cost-overrun-predictor](analysis/cost-overrun-predictor/)         | 2.0.0   | Audit construction project management software for budget tracking accuracy, earned value management (EVM) formula correctness, risk factor modeling, schedule-cost integration,...    |
| [credit-risk](analysis/credit-risk/)                               | 2.0.0   | Audit credit risk modeling software for scoring algorithm accuracy, regulatory compliance (ECOA, FCRA, SR 11-7), bias and disparate impact testing, model governance lifecycle, and... |
| [crisis-risk-monitor](analysis/crisis-risk-monitor/)               | 2.0.0   | Audit mental health crisis monitoring systems for risk signal detection accuracy, escalation protocol completeness, safety planning integration, crisis team coordination, and...      |
| [crisis-triage](analysis/crisis-triage/)                           | 2.0.0   | Audit emergency and crisis triage systems for call prioritization accuracy, resource dispatching algorithm quality, severity classification model evaluation, response time...         |
| [crop-yield](analysis/crop-yield/)                                 | 2.0.0   | Audit precision agriculture and crop management software for yield prediction model accuracy, soil analysis integration, irrigation optimization algorithms, pest and disease...       |
| [curriculum-optimizer](analysis/curriculum-optimizer/)             | 2.0.0   | Audit curriculum management software for learning outcome alignment, pacing guide optimization, standards coverage mapping (Common Core, NGSS, state standards), differentiation...    |
| [customer-success-audit](analysis/customer-success-audit/)         | 2.0.0   | Audit any product from a Customer Success Manager perspective -- evaluate onboarding flow completeness, self-service help infrastructure, customer health signal tracking, support...  |
| [cyber-risk-modeling](analysis/cyber-risk-modeling/)               | 2.0.0   | Quantify cyber risk using FAIR methodology with Monte Carlo simulation, assess control effectiveness against NIST CSF/CIS/ISO 27001 frameworks, evaluate risk appetite alignment,...   |
| [damage-prediction](analysis/damage-prediction/)                   | 2.0.0   | Audit transit damage prediction and prevention systems for packaging failure mode analysis, handling chain risk assessment, claims pattern detection, and protection level...          |
| [debt-payoff](analysis/debt-payoff/)                               | 2.0.0   | Analyze debt payoff software — avalanche vs snowball strategy engines, interest calculation accuracy, amortization schedules, payment scheduling automation, credit score impact...    |
| [defect-detection](analysis/defect-detection/)                     | 2.0.0   | Analyze manufacturing defect detection and quality control systems — computer vision inspection pipelines, SPC control charts, Six Sigma process capability (Cp/Cpk), defect...        |
| [defense-budget](analysis/defense-budget/)                         | 2.0.0   | Analyze defense program budgets and acquisition costs — earned value management (EVM/CPI/SPI), should-cost modeling, PPBE process alignment, cost estimation per GAO guidelines,...    |
| [defense-maintenance](analysis/defense-maintenance/)               | 2.0.0   | Analyze defense maintenance and readiness systems — MRO optimization, mission capable rate tracking, reliability-centered maintenance (RCM), condition-based maintenance (CBM+),...    |
| [defense-supply-chain](analysis/defense-supply-chain/)             | 2.0.0   | Analyze defense supply chain systems — DFARS compliance assessment, CMMC cybersecurity readiness, sole-source and DMSMS risk identification, counterfeit parts prevention per SAE...   |
| [demand-forecasting](analysis/demand-forecasting/)                 | 2.0.0   | Analyze demand forecasting systems — time-series decomposition (ARIMA, Prophet, ETS), seasonal and event-driven demand modeling, booking curve and pickup analysis, cancellation...    |
| [dep-map](analysis/dep-map/)                                       | 2.0.0   | Maps dependencies between stories, code modules, tickets, or specs. Computes optimal implementation order with parallel batches, cycle detection, and critical path analysis.          |
| [dependency-analysis](analysis/dependency-analysis/)               | 2.0.0   | Analyze project dependencies for health, security, and bloat — audit outdated, deprecated, vulnerable, duplicate, heavy, and unused packages across npm, pip, cargo, go mod, and...    |
| [disability-services](analysis/disability-services/)               | 2.0.0   | Analyze disability services software — IEP and ISP management, person-centered planning workflows, HCBS Settings Rule compliance, accommodation tracking, assistive technology...      |
| [disaster-prediction](analysis/disaster-prediction/)               | 2.0.0   | Analyze disaster prediction and early warning systems — model accuracy for flood, earthquake, wildfire, hurricane, and tsunami hazards, data pipeline reliability from sensor...       |
| [donor-retention](analysis/donor-retention/)                       | 2.0.0   | Analyze donor retention and CRM systems — lapse risk scoring and prediction models, stewardship workflow automation, donor lifetime value (LTV) modeling, communication...             |
| [dropout-risk](analysis/dropout-risk/)                             | 2.0.0   | Audit a student information system for dropout risk prediction. Analyzes attendance patterns, grade trajectories, behavioral indicators, early warning model accuracy, intervention... |
| [drug-discovery-ops](analysis/drug-discovery-ops/)                 | 2.0.0   | Audit a drug discovery pipeline for operational efficiency and scientific rigor. Evaluates compound library management, HTS screening workflows, hit-to-lead optimization, ADMET...    |
| [dynamic-pricing](analysis/dynamic-pricing/)                       | 2.0.0   | Audit a dynamic pricing engine for revenue optimization and fairness. Evaluates price elasticity models, competitive intelligence feeds, promotional ROI, markdown optimization,...    |
| [elder-care-ops](analysis/elder-care-ops/)                         | 2.0.0   | Audit an assisted living or elder care platform for resident safety and operational quality. Evaluates vital sign monitoring, fall detection and prevention, medication...             |
| [emergency-resource](analysis/emergency-resource/)                 | 2.0.0   | Audit an emergency resource management system for crisis readiness. Evaluates inventory tracking accuracy, deployment request-to-arrival pipeline, logistics and route...              |
| [emergency-response](analysis/emergency-response/)                 | 2.0.0   | Audit a 911 dispatch or emergency response system for operational reliability and compliance. Evaluates call routing and intake (E911/NG911), unit recommendation algorithms, AVL...   |
| [employer-matching](analysis/employer-matching/)                   | 2.0.0   | Audit a job matching platform for relevance, fairness, and candidate experience. Evaluates matching algorithm precision and recall, skill taxonomy and NLP extraction, culture fit...  |
| [energy-efficiency](analysis/energy-efficiency/)                   | 2.0.0   | Audit a manufacturing energy management system for monitoring quality, cost optimization, and compliance. Evaluates power metering infrastructure, energy baseline and EnPI...         |
| [ethical-sourcing](analysis/ethical-sourcing/)                     | 2.0.0   | Audit a supply chain compliance system for ethical sourcing and labor rights. Evaluates supplier audit programs (SMETA, BSCI), forced labor due diligence (UFLPA, Modern Slavery...    |
| [eviction-risk](analysis/eviction-risk/)                           | 2.0.0   | Audit a tenant management system for eviction prevention and risk prediction. Evaluates payment pattern analysis and arrears tracking, early warning indicators (financial,...         |
| [expansion-modeling](analysis/expansion-modeling/)                 | 2.0.0   | Analyze franchise expansion plans, model new market entry, score site selection candidates, map territory density, assess cannibalization risk, and build multi-year growth...         |
| [experiment-tracking](analysis/experiment-tracking/)               | 2.0.0   | Audit ML experiment tracking infrastructure for reproducibility gaps, parameter logging completeness, metric capture, artifact management, and pipeline orchestration. Covers...       |
| [extraction-optimization](analysis/extraction-optimization/)       | 2.0.0   | Optimize mining extraction operations by analyzing ore grade control, processing plant throughput, metallurgical recovery rates, energy consumption, and water balance. Covers...      |
| [facilities-energy](analysis/facilities-energy/)                   | 2.0.0   | Audit commercial building energy performance including HVAC optimization, ENERGY STAR scoring, utility cost analysis, demand response readiness, and sustainability compliance....     |
| [fall-risk](analysis/fall-risk/)                                   | 2.0.0   | Evaluate elder care fall risk prediction systems including wearable sensor integration, gait and balance analytics, risk scoring algorithms, environmental hazard detection,...        |
| [fleet-maintenance](analysis/fleet-maintenance/)                   | 2.0.0   | Analyze fleet maintenance programs for preventive maintenance scheduling effectiveness, parts inventory forecasting, vehicle downtime minimization, total cost of ownership...         |
| [fleet-safety](analysis/fleet-safety/)                             | 2.0.0   | Analyze fleet safety programs including driver behavior scoring, accident trend analysis, CSA BASIC score monitoring, DOT audit readiness, Hours of Service compliance, and drug...    |
| [food-waste](analysis/food-waste/)                                 | 2.0.0   | Analyze food supply chain systems for waste reduction opportunities including shelf life prediction models, FIFO and FEFO inventory rotation enforcement, demand forecasting...        |
| [franchise-benchmarking](analysis/franchise-benchmarking/)         | 2.0.0   | Benchmark franchise locations by comparing top and bottom quartile performance across revenue, profitability, and operational scores. Covers same-store sales decomposition into...    |
| [franchise-inventory](analysis/franchise-inventory/)               | 2.0.0   | Analyze franchise inventory management for par level optimization, waste tracking and root cause analysis, theoretical vs. actual food cost variance, menu engineering...              |
| [fraud-detection](analysis/fraud-detection/)                       | 2.0.0   | Analyze fraud detection systems including rule engines, ML scoring models, real-time transaction monitoring, alert triage workflows, false positive management, SAR/CTR regulatory...  |
| [fuel-optimization](analysis/fuel-optimization/)                   | 2.0.0   | Analyze fleet fuel optimization systems including MPG consumption analytics, eco-driving behavior scoring, route fuel cost modeling, idling detection and anti-idle programs, IFTA...  |
| [funding-allocation](analysis/funding-allocation/)                 | 2.0.0   | Analyze university and research institution funding allocation systems including RCM revenue attribution, performance-based budgeting, faculty startup package management, F&A...      |
| [fundraising-optimizer](analysis/fundraising-optimizer/)           | 2.0.0   | Analyze nonprofit fundraising software for RFM donor segmentation, campaign performance modeling with A/B testing, recurring giving retention and failed payment recovery, major...    |
| [game-ai](analysis/game-ai/)                                       | 2.0.0   | Analyze game AI systems including behavior trees, finite state machines, GOAP planning, utility AI scoring, A-star and NavMesh pathfinding, steering and flocking behaviors,...        |
| [game-design-review](analysis/game-design-review/)                 | 2.0.0   | Analyze game design documents and implementations for core gameplay loop clarity and depth, XP leveling curves and unlock pacing, difficulty curve spikes and plateaus, skill tree...  |
| [game-economy](analysis/game-economy/)                             | 2.0.0   | Analyze in-game economy systems including soft and hard currency source-sink balance, inflation projection modeling, loot table drop rate fairness and pity system evaluation,...      |
| [game-monetization](analysis/game-monetization/)                   | 2.0.0   | Analyze game monetization implementations including IAP purchase flow and server-side receipt validation, ad mediation waterfall and rewarded video placement, subscription...         |
| [game-performance](analysis/game-performance/)                     | 2.0.0   | Analyze game code for performance bottlenecks including draw call batching and overdraw, shader complexity and LOD strategy, per-frame GC allocation pressure, object pooling gaps,... |
| [grant-management](analysis/grant-management/)                     | 2.0.0   | Analyze grant management and sponsored research operations including proposal lifecycle tracking, pre-award routing and budget development, post-award expenditure monitoring and...   |
| [grant-writer](analysis/grant-writer/)                             | 2.0.0   | Audit a grant management system for proposal workflow efficiency, deadline tracking, budget-narrative alignment, outcome reporting, compliance readiness, and win rate...              |
| [grid-optimizer](analysis/grid-optimizer/)                         | 2.0.0   | Analyze smart grid and power distribution optimization code for power flow solver correctness, fault detection and restoration automation, distributed energy resource management,...  |
| [growth-audit](analysis/growth-audit/)                             | 2.0.0   | Audit a product codebase for growth readiness using the AARRR pirate metrics framework. Scans actual code for SEO implementation, onboarding friction, retention hooks,...             |
| [healthcare-compliance](analysis/healthcare-compliance/)           | 2.0.0   | Audit a healthcare software codebase for HIPAA Privacy and Security Rule compliance, HITECH breach notification readiness, 21st Century Cures Act interoperability requirements,...    |
| [hr-ops](analysis/hr-ops/)                                         | 2.0.0   | Analyze an HR operations system for headcount planning effectiveness, attrition pattern detection, compensation benchmarking accuracy, workforce analytics maturity, and onboarding... |
| [image-storage-optimization](analysis/image-storage-optimization/) | 2.1.0   | Audits and implements mandatory image resizing and compression for all uploaded user images to reduce storage costs while preserving visual quality.                                   |
| [impact-measurement](analysis/impact-measurement/)                 | 2.0.0   | Analyze program impact measurement software for logic model completeness, indicator tracking rigor, data collection methodology, causal attribution modeling, cost-effectiveness...    |
| [incident-response](analysis/incident-response/)                   | 2.0.0   | Analyze an incident response program for playbook coverage, MTTR optimization opportunities, evidence collection readiness, root cause analysis quality, and post-incident review...   |
| [incident-tracking](analysis/incident-tracking/)                   | 2.0.0   | Analyze a workplace safety incident tracking system for incident classification accuracy, root cause analysis depth, OSHA 300 log recordkeeping compliance, trend analysis...          |
| [insurance-claims](analysis/insurance-claims/)                     | 2.0.0   | Analyze an insurance claims processing system for lifecycle completeness, straight-through processing automation, fraud detection coverage, reserve estimation methodology,...         |
| [inventory-allocation](analysis/inventory-allocation/)             | 2.0.0   | Analyze an inventory allocation system for demand-driven distribution accuracy, store clustering methodology, safety stock optimization, markdown timing, replenishment logic, and...  |
| [inventory-forecast](analysis/inventory-forecast/)                 | 2.0.0   | Audit demand forecasting models and inventory optimization logic -- forecast accuracy (MAPE, bias), safety stock calculations, reorder point strategies (EOQ, ROP, min/max),...        |
| [job-dispatch](analysis/job-dispatch/)                             | 2.0.0   | Audit field service dispatch and workforce scheduling systems -- technician routing (VRP solvers, drive time modeling), skill-based job assignment, SLA priority scheduling,...        |
| [lab-automation](analysis/lab-automation/)                         | 2.0.0   | Audit laboratory automation systems -- LIMS architecture, instrument connectivity (SiLA 2, OPC-UA, serial drivers), sample tracking and chain of custody, protocol workflow...         |
| [lab-management](analysis/lab-management/)                         | 2.0.0   | Audit laboratory management systems -- chemical inventory (SDS, GHS, CAS tracking), equipment lifecycle and calibration scheduling, safety compliance (OSHA 29 CFR 1910.1450,...       |
| [lease-compliance](analysis/lease-compliance/)                     | 2.0.0   | Audit commercial lease compliance systems -- CAM reconciliation accuracy (pro-rata share, caps, admin fees), lease abstraction completeness, critical date tracking and deadline...    |
| [lease-optimizer](analysis/lease-optimizer/)                       | 2.0.0   | Audit commercial lease optimization software -- lease abstraction quality, rent optimization (market comparison, net effective rent, blend-and-extend modeling), ASC 842/IFRS 16...    |
| [legal-aid](analysis/legal-aid/)                                   | 2.0.0   | Audit legal aid and public defense case management systems -- client intake workflows, Federal Poverty Level eligibility screening accuracy, conflict-of-interest checking,...         |
| [legal-discovery](analysis/legal-discovery/)                       | 2.0.0   | Audit e-discovery and litigation document review systems -- data collection pipelines (PST, MBOX, SharePoint, Slack), document processing (OCR via Tesseract/ABBYY, metadata...        |
| [level-design](analysis/level-design/)                             | 2.0.0   | Audit game level design systems and procedural generation -- BSP room subdivision, Wave Function Collapse tile placement, cellular automata cave generation, Perlin noise terrain,...  |
| [litigation-predictor](analysis/litigation-predictor/)             | 2.0.0   | Audit litigation analytics and case outcome prediction systems -- ML outcome models (logistic regression, gradient boosting, neural nets with temporal train/test splits),...          |
| [load-forecast](analysis/load-forecast/)                           | 2.0.0   | Analyze energy load forecasting systems including demand prediction models (ARIMA, Prophet, LSTM), weather API integration, peak shaving strategies, demand response program...        |
| [maintenance-scheduling](analysis/maintenance-scheduling/)         | 2.0.0   | Analyze preventive and predictive maintenance scheduling systems including CMMS/EAM work order optimization, asset condition scoring with Facility Condition Index, PM compliance...   |
| [material-forecasting](analysis/material-forecasting/)             | 2.0.0   | Analyze material forecasting and requirements planning systems including MRP/MRP II logic evaluation, BOM explosion accuracy, supplier lead time variability tracking, seasonal...     |
| [medical-billing](analysis/medical-billing/)                       | 2.0.0   | Analyze medical billing and revenue cycle management software including claims processing pipelines, EDI transaction handling (837P/837I/835/270/271/276/277), ICD-10 and CPT code...  |
| [medication-adherence](analysis/medication-adherence/)             | 2.0.0   | Analyze medication adherence and management platforms including dose tracking accuracy (MPR, PDC metrics), drug-drug and drug-food interaction checking completeness, refill...        |
| [mental-health-clinic](analysis/mental-health-clinic/)             | 2.0.0   | Analyze mental health clinic and therapy practice software including appointment scheduling optimization with no-show backfill, therapist-client matching algorithms...                |
| [merchandising-analytics](analysis/merchandising-analytics/)       | 2.0.0   | Analyze retail merchandising systems including planogram optimization (space-to-sales alignment, fair share index, sales per linear foot), visual merchandising effectiveness for...   |
| [metrics](analysis/metrics/)                                       | 2.0.0   | Computes development quality and velocity metrics from git history and tracks improvement over time. Measures fix ratios, rework hotspots, test coverage, DORA metrics, and code...    |
| [mining-maintenance](analysis/mining-maintenance/)                 | 2.0.0   | Analyze mining equipment maintenance systems including heavy fleet condition monitoring (oil analysis, vibration per ISO 17359/10816, thermal imaging), predictive analytics with...   |
| [mining-safety](analysis/mining-safety/)                           | 2.0.0   | Analyze mining safety management systems including incident investigation quality (ICAM, TapRooT, BowTie analysis), hazard identification and risk register completeness, critical...  |
| [mobile-analytics](analysis/mobile-analytics/)                     | 2.0.0   | Analyze mobile app analytics implementation including event tracking completeness and naming conventions, SDK configuration audit (Firebase Analytics, Amplitude, Mixpanel,...         |
| [mobile-monetization](analysis/mobile-monetization/)               | 2.0.0   | Audit mobile app revenue implementation -- in-app purchases, subscriptions, ad SDKs, paywall design, trial conversion funnels, and store billing compliance. Covers StoreKit 2,...     |
| [mobile-performance](analysis/mobile-performance/)                 | 2.0.0   | Profile and audit mobile app performance -- cold/warm/hot startup time, memory leaks, battery drain, network efficiency, frame rate jank, and binary size. Covers Flutter, React...    |
| [mobile-ux-patterns](analysis/mobile-ux-patterns/)                 | 2.0.0   | Audit mobile UX implementation against platform conventions -- navigation patterns, gesture handling, pull-to-refresh, infinite scroll, skeleton screens, haptic feedback, adaptive... |
| [mvp](analysis/mvp/)                                               | 2.0.0   | MVP analysis, product analysis, app teardown, analyze this app, what does this app do, product breakdown, feature analysis                                                             |
| [narrative-design](analysis/narrative-design/)                     | 2.0.0   | Audit game narrative systems for technical quality -- branching dialogue trees, state/flag tracking, quest systems, choice-consequence mapping, localization pipelines, voice-over...  |
| [new-features](analysis/new-features/)                             | 1.0.0   | Feature discovery agent — mines project docs, memory, user feedback, and competitor gaps to surface the highest-leverage features to build next. Outputs a prioritized feature...      |
| [parts-inventory](analysis/parts-inventory/)                       | 2.0.0   | Analyze MRO parts inventory systems for field service optimization -- truck stock composition, first-time fix rate improvement, reorder point calculation, safety stock sizing,...     |
| [patient-engagement](analysis/patient-engagement/)                 | 2.0.0   | Audit patient-facing healthcare software for portal feature completeness, secure messaging, health literacy, telehealth readiness, consent management, and HIPAA compliance. Covers... |
| [peer-review-ops](analysis/peer-review-ops/)                       | 2.0.0   | Audit academic peer review operations -- reviewer matching algorithms, conflict of interest detection, turnaround time optimization, review quality scoring, and editorial workflow... |
| [pharma-compliance](analysis/pharma-compliance/)                   | 2.0.0   | Audit pharmaceutical regulatory compliance -- inspection readiness, CAPA system effectiveness, change control pipeline, data integrity (ALCOA+), and validation lifecycle tracking.... |
| [pharma-quality-control](analysis/pharma-quality-control/)         | 2.0.0   | Audit pharmaceutical QC laboratory operations -- OOS/OOT investigations, stability program trending, analytical method validation status, release testing optimization, and...         |
| [player-analytics](analysis/player-analytics/)                     | 2.0.0   | Audit game analytics and telemetry implementation -- event tracking completeness, FTUE and monetization funnel coverage, retention metric infrastructure, A/B testing framework,...    |
| [pmf-analysis](analysis/pmf-analysis/)                             | 2.0.0   | Audit a codebase for product-market fit readiness -- evaluate startup PMF signals, core value loop tightness, feature scatter vs focus ratio, user activation funnel friction,...      |
| [portfolio-optimizer](analysis/portfolio-optimizer/)               | 2.0.0   | Audit investment portfolio management software for mean-variance optimization, Black-Litterman model, risk parity allocation, VaR/CVaR risk metrics, Brinson performance...            |
| [predictive-maintenance](analysis/predictive-maintenance/)         | 2.0.0   | Audit manufacturing predictive maintenance systems for OPC-UA/MQTT sensor data pipelines, time-series storage retention, ML model lifecycle (training-serving skew, drift...           |
| [pricing-sensitivity](analysis/pricing-sensitivity/)               | 2.0.0   | Audit pricing research and sensitivity analysis systems for Van Westendorp price sensitivity meter (OPP/IDP/PMC/PME intersections), Gabor-Granger demand curves,...                    |
| [procurement-analysis](analysis/procurement-analysis/)             | 2.0.0   | Audit procurement and procure-to-pay systems for spend analytics (Pareto analysis, tail spend visibility), supplier consolidation opportunities, Kraljic matrix category...            |
| [production-budgeting](analysis/production-budgeting/)             | 2.0.0   | Audit film, television, and digital content production budgets for above-the-line (ATL) and below-the-line (BTL) cost accuracy, SAG-AFTRA/DGA/WGA/IATSE union rate compliance,...      |
| [production-optimizer](analysis/production-optimizer/)             | 2.0.0   | Audit manufacturing production optimization systems for OEE (Overall Equipment Effectiveness) calculation accuracy, Six Big Losses categorization, job shop and flow shop...           |
| [production-scheduling](analysis/production-scheduling/)           | 2.0.0   | Audit factory production scheduling systems for finite capacity planning, Drum-Buffer-Rope (DBR) Theory of Constraints implementation, dispatching rules (EDD, SPT, critical...        |
| [property-roi](analysis/property-roi/)                             | 2.0.0   | Audit real estate investment software for IRR/NPV/cap rate/cash-on-cash return calculations, pro forma income modeling (GPR, vacancy, rent growth, NNN pass-throughs), equity...       |
| [public-resource-allocation](analysis/public-resource-allocation/) | 2.0.0   | Audit public sector and government resource allocation systems for budget optimization algorithms (zero-based, incremental, performance-based), service demand forecasting (ARIMA,...  |
| [quote-automation](analysis/quote-automation/)                     | 2.0.0   | Audit a quoting or estimation system -- analyze labor hour estimation accuracy, material take-off completeness, pricing rule engines, markup and margin optimization,...               |
| [real-estate-market](analysis/real-estate-market/)                 | 2.0.0   | Audit a real estate analytics platform -- evaluate comparable sales and rental engines, automated valuation models (AVM), demographic and economic indicator pipelines, submarket...   |
| [recall](analysis/recall/)                                         | 2.0.0   | Reconstructs the development cycle from git history, distills sequential/parallel patterns, and produces actionable insights for improving future iterations. Triggers: recall,...     |
| [reconciliation](analysis/reconciliation/)                         | 2.0.0   | Audit financial reconciliation workflows -- evaluate automated transaction matching engines, intercompany balance reconciliation, suspense and clearing account health, variance...    |
| [recovery-metrics](analysis/recovery-metrics/)                     | 2.0.0   | Audit a rehabilitation recovery tracking system -- evaluate standardized outcome instruments (FIM, Barthel Index, SF-36, DASH, LEFS, PROMIS), functional assessment scoring...         |
| [regulatory-submissions](analysis/regulatory-submissions/)         | 2.0.0   | Audit a pharmaceutical regulatory submission system -- evaluate eCTD backbone assembly and XML validation, CTD module completeness (Modules 1-5), FDA ESG and EMA CESP gateway...      |
| [rehab-scheduling](analysis/rehab-scheduling/)                     | 2.0.0   | Audit a rehabilitation scheduling system -- evaluate therapist productivity and utilization rates, PTA/COTA supervision compliance, patient flow and no-show management, equipment...  |
| [rehab-therapy](analysis/rehab-therapy/)                           | 2.0.0   | Audit a rehabilitation or physical therapy platform end-to-end -- evaluate recovery metrics tracking (ROM, strength, balance, gait), patient-reported outcomes (DASH, LEFS, NDI,...    |
| [rent-burden](analysis/rent-burden/)                               | 2.0.0   | Audit a housing affordability system -- evaluate rent burden calculation accuracy (30% and 50% thresholds), area median income modeling with HUD Income Limits and family size...      |
| [research-data-management](analysis/research-data-management/)     | 2.0.0   | Audit research data management infrastructure -- score FAIR principles compliance (Findable, Accessible, Interoperable, Reusable) across all sub-principles, evaluate data...          |
| [resource-estimation](analysis/resource-estimation/)               | 2.0.0   | Audit a mineral resource estimation system -- evaluate drillhole database integrity and QA/QC (CRMs, blanks, duplicates, umpire checks), geological and domain modeling quality,...    |
| [resume-optimizer](analysis/resume-optimizer/)                     | 2.0.0   | Audit a resume builder or optimization tool for ATS compatibility, keyword matching accuracy, formatting standards, achievement quantification, skill extraction, and...               |
| [retirement-optimizer](analysis/retirement-optimizer/)             | 2.0.0   | Audit retirement planning software for projection model accuracy, asset allocation by age, Social Security optimization, tax-advantaged account strategy, withdrawal sequencing...     |
| [returns-optimization](analysis/returns-optimization/)             | 2.0.0   | Audit e-commerce and retail product return systems for return rate reduction strategies, reverse logistics efficiency, refurbishment routing, fraud detection in returns, and...       |
| [revenue-management](analysis/revenue-management/)                 | 2.0.0   | Audit dynamic pricing and revenue management systems for hotels, airlines, and hospitality including inventory controls, overbooking optimization, channel management, competitive...  |
| [rights-explainer](analysis/rights-explainer/)                     | 2.0.0   | Audit legal information systems that explain rights to the public, evaluating plain-language accuracy, jurisdiction-specific content correctness, reading level appropriateness...     |
| [rights-management](analysis/rights-management/)                   | 2.0.0   | Audit content licensing and rights management systems for territory and window tracking, royalty calculation accuracy, rights clearance workflows, and contract compliance across...   |
| [risk-simulation](analysis/risk-simulation/)                       | 2.0.0   | Audit risk simulation and decision support systems for Monte Carlo modeling quality, wargaming analysis, threat assessment, mission planning support, and course-of-action decision... |
| [route-optimizer](analysis/route-optimizer/)                       | 2.0.0   | Audit routing and delivery optimization software for algorithm quality, constraint handling, real-time traffic adaptation, multi-modal transport support, and cost modeling...         |
| [rural-health](analysis/rural-health/)                             | 2.0.0   | Audit rural health network software for telehealth readiness, provider coverage mapping, patient transportation coordination, referral network optimization, Critical Access...        |
| [safety-compliance](analysis/safety-compliance/)                   | 2.0.0   | Audit workplace safety compliance systems for OSHA regulatory gap analysis, inspection readiness assessment, permit-to-work management, lockout/tagout program compliance, confined... |
| [safety-training](analysis/safety-training/)                       | 2.0.0   | Audit OSHA training compliance, certification expirations, competency tracking, and LMS integration. Use when you need to evaluate safety training programs, check ANSI Z490.1...      |
| [sales-readiness](analysis/sales-readiness/)                       | 2.0.0   | Audit whether a product is ready for enterprise sales. Use when you need to assess SSO/SAML/SCIM support, RBAC maturity, multi-tenancy data isolation, audit logging coverage,...      |
| [seo](analysis/seo/)                                               | 2.0.0   | — a Claude Code skill for automating seo workflows.                                                                                                                                    |
| [service-triage](analysis/service-triage/)                         | 2.0.0   | Audit customer service triage systems for ticket routing, classification, and SLA compliance. Use when you need to evaluate ticket auto-classification accuracy, priority scoring...   |
| [setback-predictor](analysis/setback-predictor/)                   | 2.0.0   | Audit rehabilitation setback prediction systems for clinical risk modeling and early intervention. Use when you need to evaluate risk factor models (Charlson, Elixhauser), early...   |
| [shipping-cost](analysis/shipping-cost/)                           | 2.0.0   | Audit shipping costs and identify savings across carriers, zones, and modes. Use when you need to compare UPS/FedEx/USPS/DHL rates, analyze zone-skip and zone-reduction...            |
| [skill-gap](analysis/skill-gap/)                                   | 2.0.0   | Audit workforce skill gap identification systems and labor market alignment. Use when you need to evaluate skill taxonomy quality, individual and aggregate gap analysis accuracy,...  |
| [skills-list](analysis/skills-list/)                               | 4.1.0   | Displays the full skills catalog with descriptions, autonomous build chains, recommended pipelines, and parallelization rules.                                                         |
| [sku-optimization](analysis/sku-optimization/)                     | 2.0.0   | Audit SKU portfolio health and identify rationalization opportunities. Use when you need to evaluate assortment planning strategy, ABC/Pareto long-tail analysis, store clustering...  |
| [spending-behavior](analysis/spending-behavior/)                   | 2.0.0   | Audit personal finance and budgeting app spending intelligence features. Use when you need to evaluate transaction categorization accuracy (MCC mapping, ML classification,...         |
| [staff-scheduling](analysis/staff-scheduling/)                     | 2.0.0   | Audit workforce scheduling systems for labor optimization and compliance. Use when you need to evaluate labor demand forecasting accuracy, shift generation and optimization...        |
| [student-personalization](analysis/student-personalization/)       | 2.0.0   | Audit adaptive learning and student personalization systems for pedagogical quality. Use when you need to evaluate learning path algorithms (branching, remediation, acceleration),... |
| [studio-operations](analysis/studio-operations/)                   | 2.0.0   | Audit a media production studio or post-production facility. Analyzes facility scheduling and utilization, equipment lifecycle tracking, editorial and VFX pipelines, color grading... |
| [supply-chain-risk](analysis/supply-chain-risk/)                   | 2.0.0   | Assess supply chain risk exposure and resilience posture. Analyzes supplier dependency mapping (Tier 1/2/3), geographic concentration risk, single-source vulnerability, disruption... |
| [survey-analysis](analysis/survey-analysis/)                       | 2.0.0   | Evaluate survey data pipelines and research methodology. Analyzes response bias detection (speeders, straight-liners, bots), statistical significance testing (t-test, chi-square,...  |
| [sustainability-metrics](analysis/sustainability-metrics/)         | 2.0.0   | Audit ESG reporting software and sustainability metric accuracy. Analyzes Environmental (Scope 1/2/3 emissions, water, waste, biodiversity), Social (workforce diversity, pay...       |
| [tax-compliance](analysis/tax-compliance/)                         | 2.0.0   | Audit corporate tax compliance systems across jurisdictions. Analyzes tax engine configuration (Avalara, Vertex, ONESOURCE), nexus determination and Wayfair economic nexus...         |
| [teacher-workload](analysis/teacher-workload/)                     | 2.0.0   | Evaluate edtech tools for their real impact on teacher time and administrative burden. Analyzes grading automation (auto-scoring, rubric-based feedback, batch workflows), lesson...   |
| [tech-debt](analysis/tech-debt/)                                   | 2.0.0   | Inventory and prioritize all technical debt in a codebase. Scans for TODO/FIXME/HACK markers and stale comments, outdated and deprecated dependencies with CVE detection,...           |
| [technician-productivity](analysis/technician-productivity/)       | 2.0.0   | Analyze field service technician productivity and workforce efficiency. Evaluates wrench time utilization rates (benchmark 55-65%), travel time optimization, first-time fix rate...   |
| [therapy-outcomes](analysis/therapy-outcomes/)                     | 2.0.0   | Evaluate therapy outcome measurement systems for rehabilitation and physical therapy. Analyzes functional improvement scoring (MCID, MDC, risk-adjusted residuals), treatment...       |
| [therapy-personalization](analysis/therapy-personalization/)       | 2.0.0   | Evaluate physical therapy personalization and adaptive treatment systems. Analyzes exercise recommendation algorithms (rules-based, collaborative filtering, protocol-driven),...      |
| [threat-triage](analysis/threat-triage/)                           | 2.0.0   | Analyze cybersecurity threat intelligence, triage security alerts, classify IOCs, map attacks to MITRE ATT&CK kill chain, reduce false positives, and attribute threat actors....      |
| [training-path](analysis/training-path/)                           | 2.0.0   | Analyze learning management and training pathway systems for prerequisite mapping, competency-based progression, adaptive sequencing, and credential stacking. Evaluates LMS...        |
| [travel-operations](analysis/travel-operations/)                   | 2.0.0   | Analyze airline, airport, cruise, and tour operator systems for ground handling efficiency, aircraft turnaround optimization, disruption management, and GDS integration. Covers...    |
| [treatment-outcome](analysis/treatment-outcome/)                   | 2.0.0   | Analyze behavioral health outcome tracking systems for clinical measurement validity, treatment effectiveness, and provider performance comparison. Evaluates PHQ-9, GAD-7, PCL-5,...  |
| [underwriting-analysis](analysis/underwriting-analysis/)           | 2.0.0   | Analyze insurance underwriting systems for risk assessment accuracy, pricing adequacy, and portfolio exposure management. Evaluates predictive models (GLM, GBM), rating...            |
| [unit-economics](analysis/unit-economics/)                         | 2.0.0   | Analyze franchise and multi-location unit economics including per-location P&L construction, four-wall EBITDA margins, prime cost optimization, contribution margin analysis,...       |
| [vehicle-routing](analysis/vehicle-routing/)                       | 2.0.0   | Analyze vehicle routing and fleet optimization systems for route planning algorithms, multi-stop sequencing, time window constraints, and last-mile delivery performance. Evaluates... |
| [vendor-coordination](analysis/vendor-coordination/)               | 2.0.0   | Analyze vendor and contractor coordination systems for performance scoring, competitive bid evaluation, SLA compliance tracking, and vendor risk assessment. Covers scorecard...       |
| [vendor-management](analysis/vendor-management/)                   | 2.0.0   | Analyze vendor management systems for performance scorecards, third-party risk assessment, SLA enforcement, vendor rationalization, and relationship governance. Evaluates vendor...   |
| [volunteer-coordination](analysis/volunteer-coordination/)         | 2.0.0   | Analyze volunteer management platforms for skill-based matching algorithms, shift scheduling optimization, availability tracking, and retention analysis. Evaluates training...        |
| [warehouse-flow](analysis/warehouse-flow/)                         | 2.0.0   | Audit warehouse flow design and material movement -- evaluate pick path optimization algorithms, ABC velocity-based slotting compliance, zone configuration and boundary balancing,... |
| [warehouse-ops](analysis/warehouse-ops/)                           | 2.0.0   | Audit warehouse management system operations -- evaluate WMS platform architecture (Manhattan, Blue Yonder, SAP EWM, Korber, Infor), inbound receiving and ASN processing, putaway...  |
| [workplace-risk-scoring](analysis/workplace-risk-scoring/)         | 2.0.0   | Audit workplace risk scoring systems and occupational safety programs -- evaluate job hazard analysis (JHA/JSA) methodology and task-level hazard identification, risk matrix...       |
| [yield-prediction](analysis/yield-prediction/)                     | 2.0.0   | Audit pharmaceutical yield prediction systems and process analytical technology -- evaluate critical process parameter (CPP) to critical quality attribute (CQA) relationships,...     |

### productivity -- Developer Experience (9 skills)

| Skill                                        | Version | Description                                                                                                                                                                            |
| -------------------------------------------- | ------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [ci-health](productivity/ci-health/)         | 1.0.0   | Monitor and maintain CI runner health — check disk space, clear stale caches (Flutter, Gradle, npm, Docker), prune old worktrees, and report status. Prevents cache corruption...      |
| [daily-standup](productivity/daily-standup/) | 1       | >-                                                                                                                                                                                     |
| [devcontainer](productivity/devcontainer/)   | 2.0.0   | Generate a dev container for my project — auto-detect language, framework, and services like PostgreSQL or Redis, create devcontainer.json with VS Code extensions, port...            |
| [dx](productivity/dx/)                       | 2.0.0   | Audit developer experience and generate a DX health score. Evaluates devcontainer, git hooks, linting, build caching, environment setup, and release pipeline. Use when you want to... |
| [env-setup](productivity/env-setup/)         | 2.0.0   | Bootstrap a project from zero to working dev environment. Detects runtime versions, installs dependencies, creates .env from templates, starts Docker services, runs database...       |
| [git-hooks](productivity/git-hooks/)         | 2.0.0   | Set up pre-commit hooks for linting, formatting, and type-checking with commit message enforcement using conventional commits. Auto-detects stack and configures husky, lefthook,...   |
| [linter](productivity/linter/)               | 2.0.0   | Configure linting, formatting, and editor integration for any stack. Sets up ESLint 9 or Biome for JS/TS, Ruff for Python, golangci-lint for Go, Clippy for Rust, RuboCop for Ruby,... |
| [monorepo](productivity/monorepo/)           | 2.0.0   | Set up or migrate to a monorepo with Turborepo, Nx, or pnpm workspaces. Scaffolds apps and packages directory structure, configures task pipeline with dependency graph, enables...    |
| [release](productivity/release/)             | 2.0.0   | Set up automated releases with semantic versioning, changelog generation, and package publishing. Configures semantic-release, changesets, release-please, goreleaser, or...           |

### integration -- Third-Party Service Connectors (13 skills)

| Skill                                                 | Version | Description                                                                                                                                                                            |
| ----------------------------------------------------- | ------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [analytics-tracking](integration/analytics-tracking/) | 2.0.0   | Set up production-ready event tracking with Amplitude, Mixpanel, PostHog, or GA4. Auto-detects your framework (React, Next.js, Vue, Flutter, Angular, Python, Go, Rails), installs...  |
| [auth-provider](integration/auth-provider/)           | 2.0.0   | Set up complete OAuth/SSO authentication with Google, GitHub, Apple, or SAML providers. Auto-detects your framework and configures the best auth library (NextAuth, Passport,...       |
| [email](integration/email/)                           | 2.0.0   | Add transactional email to my app — set up Resend, SendGrid, SES, Postmark, or Mailgun with HTML templates for welcome, password reset, and notification emails, delivery webhooks,... |
| [integrate](integration/integrate/)                   | 2.0.0   | Audit my project's third-party integrations or set up multiple at once — scans for payments, auth, email, push, analytics, storage, search, and realtime, calculates a...              |
| [perplexity-search](integration/perplexity-search/)   | 1.0.0   | AI-powered web search and research using the Perplexity API (Sonar models). Performs deep web research with citations, fact-checking, competitive analysis, market research, and...    |
| [push-notifications](integration/push-notifications/) | 2.0.0   | Add push notifications to my app — set up FCM, APNs, or OneSignal for Flutter, React Native, Expo, or web with permission flows, foreground and background handlers, notification...   |
| [realtime](integration/realtime/)                     | 2.0.0   | Add realtime features to my app — set up WebSockets or SSE with Socket.io, Pusher, Ably, Supabase Realtime, or Firebase using channels, presence tracking, typing indicators,...       |
| [search](integration/search/)                         | 2.0.0   | Add full-text search to my app — set up Algolia, Meilisearch, Typesense, or Elasticsearch with index configuration, typo tolerance, faceted filtering, real-time sync from database... |
| [stitch-bridge](integration/stitch-bridge/)           | 1.0.0   | >-                                                                                                                                                                                     |
| [stitch-compare](integration/stitch-compare/)         | 1.0.0   | >-                                                                                                                                                                                     |
| [stitch-explore](integration/stitch-explore/)         | 1.0.0   | >-                                                                                                                                                                                     |
| [storage](integration/storage/)                       | 2.0.0   | Add file uploads and object storage to my app — set up AWS S3, Google Cloud Storage, Cloudflare R2, or Supabase Storage with presigned URLs, direct browser uploads, multipart...      |
| [stripe](integration/stripe/)                         | 2.0.0   | Add Stripe payments to my app — set up checkout sessions, payment intents, webhook handling with signature verification, subscription billing with plan management, customer...        |

### combo -- Multi-Skill Chains (34 skills)

| Skill                                                 | Version | Description                                                                                                                                                                            |
| ----------------------------------------------------- | ------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [cleanup-sprint](combo/cleanup-sprint/)               | 3.0.0   | Deep codebase cleanup — kills dead code, fixes all lint/format warnings, removes orphaned files, cleans stale TODOs, strips security hazards, tightens TypeScript strict mode, and...  |
| [compliance-gate](combo/compliance-gate/)             | 2.0.0   | Runs a 4-phase compliance pipeline: security scan, GDPR audit, dependency vulnerability check, and penetration test, producing a unified pass/fail compliance report. Triggers on:...  |
| [compliance-suite](combo/compliance-suite/)           | 2.0.0   | Runs a 5-phase enterprise compliance and security hardening pipeline: regulatory review, GDPR audit, SOC 2 evaluation, dependency scan, and penetration test with cross-framework...   |
| [data-pipeline](combo/data-pipeline/)                 | 2.0.0   | Build a production-ready data API from scratch: scaffold REST endpoints with models and validation, generate integration tests that verify every route, then load test for...          |
| [design-overhaul](combo/design-overhaul/)             | 2.1.0   | Complete autonomous design overhaul — tears down dated patterns and rebuilds with modern CSS, proper tokens, purposeful motion, and production-grade quality. The nuclear option...    |
| [design-pipeline](combo/design-pipeline/)             | 1.0.0   | Full autonomous design pipeline — Ralph Wiggum builds it, then the safety net polishes it. Chains: design-setup → design-build → (design-audit ∥ design-optimize) → design-polish →... |
| [design-to-code](combo/design-to-code/)               | 2.0.0   | Turn a design into production-quality frontend code: extract a design system with tokens and components, make layouts responsive across breakpoints, add dark mode with...             |
| [education-suite](combo/education-suite/)             | 2.0.0   | Comprehensive K-12 or higher-ed system analysis: predict student dropout risk with early warning indicators, optimize curriculum alignment and pacing, personalize learning paths...   |
| [fintech-launch](combo/fintech-launch/)               | 2.0.0   | Pre-launch compliance and security gate for fintech apps: audit PCI DSS payment card handling, review financial API integrations for idempotency and error handling, evaluate fraud... |
| [fix-and-ship](combo/fix-and-ship/)                   | 2.0.0   | Emergency fix-and-deploy pipeline — diagnose a bug, apply a minimal fix, verify safety, deploy to production, and confirm the service is healthy. Supports Vercel, AWS, Railway,...    |
| [full-deploy](combo/full-deploy/)                     | 2.0.0   | Ship an app from code to production-ready infrastructure: containerize with Docker and multi-stage builds, set up GitHub Actions CI/CD with automated testing and deployment, add...   |
| [game-design-audit](combo/game-design-audit/)         | 2.0.0   | Deep game design health assessment across five dimensions: review core loop and progression systems, analyze in-game economy for inflation and sink/source balance, mathematically...  |
| [game-launch](combo/game-launch/)                     | 2.0.0   | Pre-launch quality gate for games: audit rendering and memory performance against platform budgets, run QA for crash-causing defects and platform certification blockers, review...    |
| [healthcare-audit](combo/healthcare-audit/)           | 2.0.0   | Comprehensive healthcare system compliance and security audit: review HIPAA Privacy and Security Rule adherence, check HITECH and 21st Century Cures Act obligations, validate...      |
| [housing-audit](combo/housing-audit/)                 | 2.0.0   | End-to-end affordable housing compliance and risk audit: analyze property management and waitlist operations, predict eviction risk with early warning models, review Fair Housing...  |
| [impact-org](combo/impact-org/)                       | 2.0.0   | Full nonprofit operational health analysis: validate impact measurement methodology and theory of change, optimize fundraising channels and campaign ROI, audit grant management...    |
| [investor-ready](combo/investor-ready/)               | 2.0.0   | Prepare for fundraising due diligence — runs CTO, CFO, CPO, sales, and codebase health reviews to produce a consolidated investor brief with scorecard, red flags, and strengths....   |
| [launch-readiness](combo/launch-readiness/)           | 2.0.0   | Run a full pre-launch quality gate before shipping — chains product review, growth audit, UX audit, security scan, and deployment preflight into a go/no-go launch decision. Stops...  |
| [logistics-optimize](combo/logistics-optimize/)       | 2.0.0   | Optimize and stress-test a logistics system end-to-end — chains route optimization, warehouse operations review, inventory demand forecasting, supply chain risk analysis, and...      |
| [marketing-refresh](combo/marketing-refresh/)         | 1.0.0   | Autonomous competitive analysis and feature discovery pipeline. Runs /compete and /new-features on each project, produces actionable market positioning insights. Schedule daily or... |
| [mobile-launch](combo/mobile-launch/)                 | 2.0.0   | Run a complete mobile app pre-launch verification — chains performance audit, QA testing, OWASP mobile security review, App Store and Play Store compliance checks, and store...       |
| [mobile-publish](combo/mobile-publish/)               | 2.0.0   | Set up a complete mobile publishing pipeline — chains CI/CD workflow generation, iOS App Store publishing via Fastlane, Google Play Store publishing, and analytics verification...    |
| [mvp-spec](combo/mvp-spec/)                           | 2.0.0   | Chains /mvp → /spec — analyzes an app from video/screenshots/description, then generates implementation stories. Triggers: analyze and spec, product analysis to stories, app...       |
| [polish](combo/polish/)                               | 2.0.0   | Full quality pass -- chains parallel UX + scalability audit, then QA verification, then consistency gate. Fixes everything it finds. Works with any stack.                             |
| [public-services-audit](combo/public-services-audit/) | 2.0.0   | Audit a government or public services system for compliance, fraud risk, and security — chains benefits processing review, fraud detection analysis, regulatory compliance check...    |
| [research](combo/research/)                           | 2.0.0   | Full-spectrum product research pipeline. Runs competitive analysis, technology trend scouting, user feedback analysis, and feature ideation. Trigger on: research, competitive...      |
| [retro](combo/retro/)                                 | 2.0.0   | Run a full retrospective and dev cycle analysis. Chains /recall → /new-features to reconstruct what went wrong, extract lessons learned, identify rework patterns, and synthesize...   |
| [review-implement](combo/review-implement/)           | 2.0.0   | Review then build — chains architecture review into implementation. Accepts any spec format (ticket, PRD, engineering spec, feature description, screenshot) and autonomously...       |
| [secure-ship](combo/secure-ship/)                     | 2.0.0   | Build and ship features with security baked in — runs OWASP Top 10 pre-scan, builds and ships with /ship, validates with post-build security review, then penetration tests the...     |
| [ship-pipeline](combo/ship-pipeline/)                 | 3.0.0   | Full-stack app pipeline — build, test, review, and deploy across one or ALL repos. Scans CLAUDE.md, MEMORY.md, TODOs, open PRs, and issues for shippable work. Supports 'ship all'...  |
| [spec](combo/spec/)                                   | 2.0.0   | Chains /mvp → /backend-spec — analyzes an app from video/screenshots/description, then generates implementation stories from the analysis.                                             |
| [stitch-pipeline](combo/stitch-pipeline/)             | 1.0.0   | >-                                                                                                                                                                                     |
| [story](combo/story/)                                 | 2.0.0   | Full story lifecycle — review, implement, and PR. Takes a story from architecture review through implementation to pull request creation.                                              |
| [tech-debt-sprint](combo/tech-debt-sprint/)           | 2.0.0   | Run a focused tech debt reduction sprint — inventories all technical debt (TODOs, outdated deps, missing tests, god objects), fixes code smells, removes dead code, then hardens...    |

### meta -- Skills About Skills (13 skills)

| Skill                                      | Version | Description                                                                                                                                                                            |
| ------------------------------------------ | ------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [bootstrap](meta/bootstrap/)               | 4.1.0   | Scaffolds a new project from a saved template with CLAUDE.md, initial memory, recommended pipeline, known pitfalls, and foundation validation.                                         |
| [broadcast](meta/broadcast/)               | 1.0.0   | Apply the same change across multiple repos simultaneously using parallel agent teams. Creates worktrees, applies changes, runs tests, commits, and creates PRs. For cross-repo...     |
| [evolve](meta/evolve/)                     | 2.0.0   | Self-improving skill system. Reads /recall and /metrics output, identifies which skills need patching based on rework patterns and regression data, generates additive patches, and... |
| [extract-template](meta/extract-template/) | 2.0.0   | Extracts a reusable project template from a mature project — captures architecture, pipeline, conventions, CI/CD, Docker, testing, linting, and pitfalls into a portable template....  |
| [load-context](meta/load-context/)         | 2.0.0   | Load a saved conversation context to resume previous work. Supports local files, git repos, and URLs. Triggered by 'load context', 'resume previous work', 'pick up where I left...    |
| [promote](meta/promote/)                   | 2.0.0   | Cross-project pattern detection — discovers recurring conventions, rework patterns, and pipeline patterns across all projects, de-duplicates against existing global conventions,...   |
| [publish-skill](meta/publish-skill/)       | 1.0.0   | Publish a locally installed skill to the skills-hub registry and sync it to the production platform. Use when: 'publish skill X', 'push skill to hub', 'add skill to registry',...     |
| [registry-sync](meta/registry-sync/)       | 2.0.0   | Validate the entire skills registry — scan all SKILL.md files for frontmatter correctness, check category READMEs are current, detect duplicate skill names, find broken...            |
| [save-context](meta/save-context/)         | 2.0.0   | Save the current conversation context as a reloadable snapshot. Triggered by 'save context', 'save session', 'bookmark this', 'save progress', 'snapshot conversation', 'save my...    |
| [skill-creator](meta/skill-creator/)       | 2.0.0   | Create new skills, modify and improve existing skills, and measure skill performance. Use when users want to create a skill from scratch, edit, or optimize an existing skill, run...  |
| [skill-test](meta/skill-test/)             | 2.0.0   | Test a skill's quality before publishing — validate SKILL.md frontmatter schema, check instruction structure for phases and guardrails, score against the marketplace rubric out of... |
| [skillify](meta/skillify/)                 | 1.1.0   | Create a reusable, self-healing, self-evolving global skill — either from the current conversation context OR from a plain-language description of a workflow. Triggers on: 'turn...   |
| [tend](meta/tend/)                         | 1.2.0   | Automated app improvement cycles. Assesses each app's health, prioritizes by staleness and debt, consumes recall/metrics/evolve findings from cron, then runs targeted fix...          |

### education -- Learning & Onboarding (8 skills)

| Skill                                               | Version | Description                                                                                                                                                                            |
| --------------------------------------------------- | ------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [claude-code-101](education/claude-code-101/)       | 1       | Interactive tutorial teaching Claude Code fundamentals -- file ops, git, testing, context management, and advanced patterns. Use when: 'teach me claude code', 'how do I use claude... |
| [course-builder](education/course-builder/)         | 1       | Generate complete self-paced course content — modules, exercises, projects, and assessments from a topic description                                                                   |
| [getting-started](education/getting-started/)       | 1.0.0   | Interactive onboarding — detects your project, recommends skills, and walks you through your first install                                                                             |
| [prompt-engineering](education/prompt-engineering/) | 1       | Learn effective AI prompting through practice -- good vs bad prompts, context management, the STAR framework, and advanced techniques                                                  |
| [quickstart](education/quickstart/)                 | 1.0.0   | >-                                                                                                                                                                                     |
| [skill-writer](education/skill-writer/)             | 1       | Learn to build and publish your own AI agent skills -- from idea to published on skills-hub.ai                                                                                         |
| [workflow-builder](education/workflow-builder/)     | 1       | Map your goal to a multi-skill workflow -- suggests Combo chains, generates custom pipelines, and explains each step                                                                   |
| [workshop-generator](education/workshop-generator/) | 1       | Generate complete workshop materials for teaching AI skills -- outlines, exercises, slides, and facilitator guides.                                                                    |

### spec -- Specification Authoring (1 skills)

| Skill                            | Version | Description                                                                                                                                                                          |
| -------------------------------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [design-spec](spec/design-spec/) | 1.0.0   | Lock down design decisions before implementation — app name, terminology, design tokens, screen inventory, data models, and microcopy. Outputs a design-spec.md that other skills... |

## Industry Verticals

Skills covering domain-specific regulations, workflows, and compliance across 40 industries:

| Industry                        | Skills                                                                                                                                                                                                                                                                                                                 | Key Regulations/Standards                                                       |
| ------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| Healthcare                      | healthcare-compliance, hipaa, clinical-data-review, healthcare-ops, healthcare-api, medical-billing, patient-engagement                                                                                                                                                                                                | HIPAA, HITECH, HL7 FHIR, ICD-10/CPT                                             |
| Finance                         | credit-risk, fraud-detection, pci-dss, financial-compliance, portfolio-optimizer, fintech-api, insurance-claims                                                                                                                                                                                                        | PCI DSS v4.0, KYC/AML, SOX, BSA, Reg E                                          |
| Logistics & Supply Chain        | route-optimizer, inventory-forecast, supply-chain-risk, warehouse-ops, procurement-review                                                                                                                                                                                                                              | EDI, TSP/VRP, WMS, demand planning                                              |
| Construction & Real Estate      | cost-overrun-predictor, property-roi, lease-optimizer, permit-compliance, real-estate-market                                                                                                                                                                                                                           | ASC 842/IFRS 16, building codes, EVM                                            |
| Manufacturing                   | predictive-maintenance, production-optimizer, defect-detection, energy-efficiency, manufacturing-compliance                                                                                                                                                                                                            | ISO 9001/13485/14001, FDA 21 CFR Part 11, GMP, OSHA                             |
| Legal                           | contract-risk, litigation-predictor, legal-discovery, regulatory-compliance                                                                                                                                                                                                                                            | TAR, e-discovery, RBAC/ABAC, audit trails                                       |
| Energy & Utilities              | load-forecast, grid-optimizer, commodity-pricing, energy-compliance                                                                                                                                                                                                                                                    | NERC CIP, FERC, EPA, ISO 50001, 49 CFR 192/195                                  |
| Gaming                          | game-design-review, game-economy, game-performance, player-analytics, game-monetization, level-design, game-ai, narrative-design, game-code-review, game-accessibility, multiplayer-review, game-qa, balance-test, game-security, game-ux, unity-scaffold, unreal-scaffold, godot-scaffold, web-game                   | Unity, Unreal, Godot, CVAA, Xbox XAGs                                           |
| Mobile                          | ios-app, android-app, cross-platform-app, app-store-publish, play-store-publish, mobile-ci-cd, ota-updates, app-store-optimization, mobile-performance, mobile-analytics, mobile-ux-patterns, mobile-monetization, app-size-optimizer, mobile-security-review, store-compliance, mobile-test, device-matrix, mobile-qa | App Store Guidelines, Play Store Policy, OWASP Mobile, StoreKit 2, Play Billing |
| Biotech & Life Sciences         | lab-automation, research-data-management, experiment-tracking, drug-discovery-ops, regulatory-submissions                                                                                                                                                                                                              | GAMP 5, 21 CFR Part 11, ICH, eCTD, FAIR                                         |
| Insurance                       | underwriting-analysis, actuarial-modeling, catastrophe-modeling, claims-workflow                                                                                                                                                                                                                                       | NAIC, Solvency II, ACORD, AM Best, SOA                                          |
| Retail & E-commerce             | inventory-allocation, sku-optimization, dynamic-pricing, returns-optimization, merchandising-analytics                                                                                                                                                                                                                 | GS1, RFID, Robinson-Patman, CPFR                                                |
| Media & Entertainment           | production-budgeting, rights-management, content-performance, ad-yield-optimization, studio-operations                                                                                                                                                                                                                 | AICP, SAG-AFTRA, DDEX, IAB, SMPTE                                               |
| Travel & Hospitality            | revenue-management, staff-scheduling, demand-forecasting, travel-operations, service-triage                                                                                                                                                                                                                            | IATA, ICAO, HEDNA, FLSA, ITIL                                                   |
| Facilities & Property Mgmt      | maintenance-scheduling, vendor-coordination, facilities-energy, lease-compliance, asset-lifecycle                                                                                                                                                                                                                      | ASHRAE, BOMA, ENERGY STAR, LEED, IFMA                                           |
| Accounting & Tax                | bookkeeping-automation, audit-support, tax-compliance, reconciliation                                                                                                                                                                                                                                                  | GAAP, PCAOB, SOX, IRC, OECD BEPS                                                |
| Research & Academia             | grant-management, funding-allocation, peer-review-ops, lab-management                                                                                                                                                                                                                                                  | 2 CFR 200, NSF, NIH, COPE, OSHA lab                                             |
| Fleet & Transportation          | vehicle-routing, fleet-maintenance, fuel-optimization, fleet-safety                                                                                                                                                                                                                                                    | FMCSA, DOT, ELD, IFTA, EPA SmartWay                                             |
| Corporate Operations            | procurement-analysis, vendor-management, compliance-ops, hr-ops, budget-allocation                                                                                                                                                                                                                                     | CIPS, COSO, ISO 37301, SHRM, FP&A                                               |
| Textiles & Apparel              | production-scheduling, material-forecasting, ethical-sourcing, apparel-demand                                                                                                                                                                                                                                          | WRAP, SA8000, OEKO-TEX, Higg Index                                              |
| Pharma Manufacturing            | batch-optimization, pharma-compliance, yield-prediction, pharma-quality-control                                                                                                                                                                                                                                        | cGMP, ICH Q7-Q14, 21 CFR 210/211, USP                                           |
| Cybersecurity Operations        | threat-triage, alert-prioritization, incident-response, cyber-risk-modeling                                                                                                                                                                                                                                            | MITRE ATT&CK, NIST CSF, FAIR, STIX/TAXII                                        |
| Defense & Aerospace             | defense-supply-chain, defense-maintenance, defense-budget, risk-simulation                                                                                                                                                                                                                                             | DFARS, ITAR, CMMC, MIL-STD, DoD 5000                                            |
| Franchise Operations            | unit-economics, franchise-benchmarking, franchise-inventory, expansion-modeling                                                                                                                                                                                                                                        | FDD, IFA, Huff Model, COGS management                                           |
| Mining & Natural Resources      | mining-maintenance, mining-safety, extraction-optimization, resource-estimation                                                                                                                                                                                                                                        | MSHA, JORC, NI 43-101, ISO 17359                                                |
| Packaging & Distribution        | box-optimization, shipping-cost, warehouse-flow, damage-prediction                                                                                                                                                                                                                                                     | ISTA, ASTM D4169, NMFC, DIM weight                                              |
| Skilled Trades & Field Services | job-dispatch, parts-inventory, technician-productivity, quote-automation                                                                                                                                                                                                                                               | FSM, RSMeans, Croston's method, VRP                                             |
| Occupational Health & Safety    | incident-tracking, workplace-risk-scoring, safety-compliance, safety-training                                                                                                                                                                                                                                          | OSHA 29 CFR, ISO 45001, ANSI Z10, NFPA 70E                                      |
| Behavioral Economics            | survey-analysis, pricing-sensitivity, behavioral-segmentation, consumer-modeling                                                                                                                                                                                                                                       | Van Westendorp, FAIR, RFM, CLV models                                           |

## Social Impact Sectors

Skills for high-impact domains focused on human welfare, equity, and public good:

| Sector                        | Skills                                                                                                     | Focus Areas                                               |
| ----------------------------- | ---------------------------------------------------------------------------------------------------------- | --------------------------------------------------------- |
| Healthcare (Beyond Hospitals) | mental-health-clinic, elder-care-ops, rural-health, disability-services, rehab-therapy, care-burnout-audit | Burnout reduction, care access, scheduling, risk flagging |
| Education                     | dropout-risk, curriculum-optimizer, student-personalization, teacher-workload, school-ops                  | K-12, higher ed, personalization, IDEA/Title I            |
| Government & Public Services  | benefits-processing, public-resource-allocation, emergency-response, government-compliance, benefits-fraud | FedRAMP, Section 508, FISMA, FOIA                         |
| Housing & Affordable Housing  | affordable-housing, rent-burden, eviction-risk, housing-compliance                                         | Fair Housing, HUD, LIHTC, Section 8                       |
| Agriculture & Food Systems    | crop-yield, food-waste, climate-risk-agriculture                                                           | Precision ag, food security, climate adaptation           |
| Climate & Sustainability      | carbon-accounting, disaster-prediction, sustainability-metrics, environmental-compliance                   | GHG Protocol, CDP, TCFD, SDGs, EPA                        |
| Legal Aid & Public Defense    | legal-aid, case-outcome-predictor, rights-explainer                                                        | Access to justice, bias detection, plain language         |
| Nonprofits & NGOs             | fundraising-optimizer, grant-writer, impact-measurement, donor-retention                                   | Impact measurement, grant management, donor CRM           |
| Emergency & Crisis Services   | crisis-triage, volunteer-coordination, emergency-resource                                                  | 911 dispatch, resource deployment, mutual aid             |
| Elder Care & Caregiving       | fall-risk, medication-adherence, caregiver-coordination                                                    | Wearable sensors, medication management, burnout          |
| Mental Health & Behavioral    | crisis-risk-monitor, treatment-outcome, care-plan-optimizer, therapist-documentation                       | PHQ-9/GAD-7, crisis protocols, HIPAA                      |
| Financial Literacy            | debt-payoff, spending-behavior, retirement-optimizer                                                       | Payoff strategies, Monte Carlo, Social Security           |
| Workforce Development         | skill-gap, resume-optimizer, training-path, employer-matching                                              | O\*NET, ATS, competency-based, bias detection             |
| Rehabilitation                | recovery-metrics, therapy-personalization, setback-predictor                                               | FIM/Barthel, exercise personalization, readmission        |

### Industry & Social Impact Pipelines

```
/healthcare-audit       (runs: /hipaa → /clinical-data-review → /healthcare-compliance → /security-review)
/fintech-launch         (runs: /pci-dss → /fintech-api → /fraud-detection → /credit-risk → /preflight)
/logistics-optimize     (runs: /route-optimizer → /warehouse-ops → /inventory-forecast → /supply-chain-risk → /load-test)
/compliance-suite       (runs: /regulatory-compliance → /gdpr → /soc2 → /dependency-scan → /pentest)
/game-launch            (runs: /game-performance → /game-qa → /game-accessibility → /game-security → /game-ux)
/game-design-audit      (runs: /game-design-review → /game-economy → /balance-test → /player-analytics → /game-monetization)
/mobile-launch          (runs: /mobile-performance → /mobile-qa → /mobile-security-review → /store-compliance → /app-store-optimization)
/mobile-publish         (runs: /mobile-ci-cd → /app-store-publish → /play-store-publish → /mobile-analytics)
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

### Design Implementation

```
/design-pipeline  (runs: /design-setup → /design-build → /design-audit → /design-polish)
```

### Design Overhaul

```
/design-overhaul  (runs: /design-audit → /design-simplify → /design-tokens → /design-adapt → /design-polish)
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

/design-pipeline (design combo)
  ├── /design-setup
  ├── /design-build
  ├── /design-audit
  └── /design-polish

/design-overhaul (design combo)
  ├── /design-audit
  ├── /design-simplify
  ├── /design-tokens
  ├── /design-adapt
  └── /design-polish

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

`build` `test` `qa` `review` `deploy` `docs` `security` `ux` `analysis` `productivity` `integration` `combo` `meta` `education` `spec`

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

- **Self-healing validation:** Every skill includes category-specific retry loops that detect failures and re-attempt with corrective action. Validation blocks are tailored per category (e.g., build skills verify compilation, test skills verify passing suites, deploy skills verify infrastructure state)
- **Self-evolution telemetry:** Every skill logs execution metadata (duration, pass/fail, retry count, category) to project memory. The `/evolve` meta-skill reads this telemetry to identify underperforming skills and patch them automatically
- **Pre-build validation:** Static analysis gate before feature work begins
- **Co-commit rules:** Firestore rules, server validation, and model serialization ship with features
- **Domain analysis feedback:** `/analyze` embedded as a quality gate in build loops
- **Subagent spawning:** 8 combo skills use parallel Agent tool spawning to run independent tracks concurrently -- `polish`, `full-test`, `cleanup-sprint`, `research`, `retro`, `review-implement`, `secure-ship`, and `compliance-suite`
- **Wiring completeness:** Detect features that exist in one layer but are never connected
- **Monolith decomposition:** Files exceeding 500 lines are split before adding features
- **Orchestrator pattern:** Main skills scan for gaps and route to specialized sub-skills
- **Modern CSS-first design:** Design skills use oklch color spaces, container queries, scroll-driven animations, view transitions, and anchor positioning. Cross-platform skills target web, Flutter, SwiftUI, and Compose
- **Zero-question autonomy:** All skills run fully autonomously without prompting for user input -- they detect context, make decisions, and execute
