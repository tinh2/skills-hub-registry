# Build

Project scaffolding and full build pipelines -- from competitor analysis to production-ready applications, including industry-specific API scaffolds.

## Skills (14)

| Skill | Version | Description |
|-------|---------|-------------|
| [build](build/) | 3.0.0 | Master orchestrator -- takes a competitor app and builds a better, cheaper, modern clone end-to-end with Node.js backend and Flutter frontend |
| [ship](ship/) | 8.0.0 | Fast autonomous build loop -- 4 iterations max. Build it, make it work, analyze it, ship it |
| [iterate](iterate/) | 4.0.0 | Self-iterating build loop -- implements, tests, reviews, analyzes, and refines up to 6 iterations |
| [flutter](flutter/) | 2.0.0 | Analyzes a video or screenshots of an application and builds a Flutter mobile version |
| [nextjs](nextjs/) | 1.0.0 | Scaffolds a production-ready Next.js 15 application with App Router, auth, database, and dashboard UI |
| [react-native](react-native/) | 1.0.0 | Builds a production-ready React Native mobile application from a design or specification |
| [api-scaffold](api-scaffold/) | 1.0.0 | Scaffolds a production-ready backend API with routes, controllers, middleware, database, auth, validation, and OpenAPI spec |
| [chrome-extension](chrome-extension/) | 1.0.0 | Builds a complete Chrome extension with Manifest V3, popup UI, content scripts, and background service worker |
| [cli-tool](cli-tool/) | 1.0.0 | Generates a production-ready CLI tool with command parsing, interactive prompts, and config management |
| [hotfix](hotfix/) | 1.0.0 | Emergency bug fix pipeline -- diagnose, fix, test, commit, push, and PR in 2 iterations max |
| [story-implementer](story-implementer/) | 2.0.0 | Implements a Jira story using repo conventions, writes unit tests, creates PR, addresses bot review |
| [db-migrate](db-migrate/) | 1.0.0 | Scaffolds Flyway migration files -- generates timestamped SQL, updates Slick table definitions and model case classes |
| [healthcare-api](healthcare-api/) | 1.0.0 | Scaffold a FHIR R4-compliant healthcare API with resource models, SMART on FHIR auth, audit logging, and interoperability endpoints |
| [fintech-api](fintech-api/) | 1.0.0 | Scaffold a production-ready financial services API with Plaid integration, payment processing, double-entry ledger, and KYC workflow |

## Usage

**When to use these skills:**

- Starting a new project from competitor analysis: `/build`
- Fast autonomous feature development: `/ship` (4 iterations) or `/iterate` (6 iterations)
- Building a Flutter app from video/screenshots: `/flutter`
- Scaffolding a Next.js web application: `/nextjs`
- Building a React Native mobile app: `/react-native`
- Scaffolding a backend API: `/api-scaffold`
- Building a Chrome extension: `/chrome-extension`
- Generating a CLI tool: `/cli-tool`
- Implementing a specific Jira story: `/story-implementer`
- Emergency bug fix: `/hotfix`
- Database schema changes: `/db-migrate`
- Healthcare/FHIR API scaffold: `/healthcare-api`
- Fintech API scaffold: `/fintech-api`

**Build orchestrators** (`/build`, `/ship`, `/iterate`) are self-contained pipelines that run analysis, testing, and quality checks internally. Use them for end-to-end work. Use the other skills for targeted scaffolding or focused tasks.
