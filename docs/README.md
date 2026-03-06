# Docs

Documentation generation -- README, API docs, ADR, changelog, diagrams, onboarding guides, and operations runbooks.

## Main Skill

**[document](document/)** -- Scans for existing documentation, identifies gaps based on project maturity, and orchestrates sub-skills to fill missing docs. Start here if you want a comprehensive documentation pass.

## Skills (10)

| Skill | Version | Description |
|-------|---------|-------------|
| [document](document/) | 1.0.0 | Main orchestrator. Scans for existing docs, identifies gaps, routes to sub-skills to fill them |
| [readme](readme/) | 1.0.0 | Generate comprehensive, scannable README.md documentation for any application by analyzing the codebase |
| [api-docs](api-docs/) | 1.0.0 | Auto-detects API framework, extracts routes and schemas, generates OpenAPI 3.1 spec with interactive docs |
| [adr](adr/) | 1.0.0 | Creates and manages Architecture Decision Records following the Michael Nygard format with auto-numbering |
| [changelog](changelog/) | 1.0.0 | Generates or updates CHANGELOG.md from git history using conventional commit parsing and keep-a-changelog format |
| [diagram](diagram/) | 1.0.0 | Analyzes codebase structure and generates Mermaid architecture diagrams including C4, sequence, ER, and dependency graphs |
| [onboarding](onboarding/) | 1.0.0 | Analyzes codebase to generate a complete developer onboarding guide covering setup, architecture, conventions, and workflow |
| [runbook](runbook/) | 1.0.0 | Scans deployment config, Docker/K8s manifests, CI/CD, and monitoring to generate actionable operations runbooks |
| [gen-catalog](gen-catalog/) | 1.1.0 | Auto-generates README.md and skills-list from SKILL.md frontmatter across all skill directories |
| [skills-list](skills-list/) | 3.1.0 | Display the full skills catalog -- lists every available skill with descriptions and autonomous build chains |

## Usage

- Full documentation gap analysis and fill: `/document`
- Generate a project README: `/readme`
- Generate OpenAPI spec and interactive docs: `/api-docs`
- Create architecture decision records: `/adr`
- Generate or update changelog from git: `/changelog`
- Generate Mermaid architecture diagrams: `/diagram`
- Generate developer onboarding guide: `/onboarding`
- Generate operations runbook: `/runbook`
- Auto-generate skill catalog from SKILL.md files: `/gen-catalog`
- Display the full skills reference: `/skills-list`
