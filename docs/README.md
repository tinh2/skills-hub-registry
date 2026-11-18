# Docs

Documentation generation -- README, API docs, ADR, changelog, diagrams, onboarding guides, and operations runbooks.

## Main Skill

**[document](document/)** -- Scans for existing documentation, identifies gaps based on project maturity, and orchestrates sub-skills to fill missing docs. Start here if you want a comprehensive documentation pass.

## Skills (11)

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

## Recently Added

| Skill | Version | Description |
|-------|---------|-------------|
| [engineering-spec](backend-spec/) | 2.0.0 | Generates structured engineering specs (backend or frontend) from feature descriptions, designs, or ticket references. Triggers on "spec", "story", "ticket", "engineering spec",... |
| [blog-writer](blog-writer/) | 1 | Write human-sounding, SEO-optimized blog posts for skills-hub.ai. Use when: 'write a blog post', 'draft a post', 'update blog', 'blog about', 'write about'. Supports styles:... |

<!-- BEGIN GENERATED: skills-hub-index (scripts/gen-index.mjs, do not edit by hand) -->
## All Docs skills on skills-hub.ai

Each skill page on skills-hub.ai shows ratings and reviews, install counts, a one-command install, and related skills. 16 of 16 skills in this folder have a page. You can also [browse the Docs category on skills-hub.ai](https://skills-hub.ai/browse?category=docs), which includes skills from other publishers.

| Skill | Description | Page |
|-------|-------------|------|
| [adr](adr/) | Create and manage Architecture Decision Records using the Michael Nygard format. | [View on skills-hub](https://skills-hub.ai/skills/adr) |
| [api-docs](api-docs/) | Generate OpenAPI 3.1 documentation from your API codebase. | [View on skills-hub](https://skills-hub.ai/skills/api-docs) |
| [engineering-spec](backend-spec/) | Generates structured engineering specs (backend or frontend) from feature descriptions, designs, or ticket references. | [View on skills-hub](https://skills-hub.ai/skills/engineering-spec) |
| [blog-writer](blog-writer/) | Write human-sounding, SEO-optimized blog posts for skills-hub.ai. | [View on skills-hub](https://skills-hub.ai/skills/blog-writer) |
| [changelog](changelog/) | Generate or update CHANGELOG.md from git history. | [View on skills-hub](https://skills-hub.ai/skills/changelog) |
| [claude-code-artifacts](claude-code-artifacts/) | Publishes structured, actionable artifacts from Claude Code sessions — PR walkthroughs, incident timelines, system explainers, release... | [View on skills-hub](https://skills-hub.ai/skills/claude-code-artifacts) |
| [diagram](diagram/) | Generate Mermaid architecture diagrams from your codebase. | [View on skills-hub](https://skills-hub.ai/skills/diagram) |
| [docs-to-context](docs-to-context/) | Convert any pile of documents (PDF, Word, HTML pages, wiki exports, PowerPoint slides) into clean, LLM-ready markdown context:... | [View on skills-hub](https://skills-hub.ai/skills/docs-to-context) |
| [document](document/) | Audit your project's documentation health and identify gaps. | [View on skills-hub](https://skills-hub.ai/skills/document) |
| [excalidraw](excalidraw/) | Generate Excalidraw architecture diagrams (.excalidraw JSON files) from your codebase. | [View on skills-hub](https://skills-hub.ai/skills/excalidraw) |
| [gen-catalog](gen-catalog/) | Generate skill catalog — auto-discovers skills, builds README tables, JSON, or HTML output. | [View on skills-hub](https://skills-hub.ai/skills/gen-catalog) |
| [office-suite](office-suite/) | Creates and edits Word (.docx), PowerPoint (.pptx), Excel (.xlsx), and PDF files programmatically: detects the available runtime and... | [View on skills-hub](https://skills-hub.ai/skills/office-suite) |
| [onboarding](onboarding/) | Generate a comprehensive developer onboarding guide from your codebase. | [View on skills-hub](https://skills-hub.ai/skills/onboarding) |
| [pitch-deck](pitch-deck/) | Build an investor or product pitch deck as a real PPTX file from a written brief: extracts the fundamentals (problem, solution, market,... | [View on skills-hub](https://skills-hub.ai/skills/pitch-deck) |
| [readme](readme/) | Generate project documentation — README files, API docs, and changelogs. | [View on skills-hub](https://skills-hub.ai/skills/readme) |
| [runbook](runbook/) | Generate an operations runbook from your deployment config, Docker/K8s manifests, CI/CD pipelines, and monitoring setup. | [View on skills-hub](https://skills-hub.ai/skills/runbook) |
<!-- END GENERATED: skills-hub-index -->
