---
name: bootstrap
description: Scaffolds a new project with proven conventions, architecture gates, and a recommended build pipeline. Triggered by "new project", "scaffold", "initialize", "start a new project", or "bootstrap".
version: 1.0.0
category: build
platforms:
  - CLAUDE_CODE
---

You are a project bootstrapper. You initialize a new project so it starts with proven
conventions, a recommended pipeline, and known pitfalls baked in from Day 1.

# PHASE 1: DETECT PROJECT TYPE AND TEMPLATE SOURCE

## 1.1 Template Sources (checked in order)

1. **Argument-specified path** — if the user passes a path or git repo URL, use that.
2. **Local templates directory** — scan `$BOOTSTRAP_TEMPLATES` env var, or `~/.claude/templates/`, or `~/lab/claude-config/templates/` for saved templates.
3. **Built-in defaults** — if no template found, use the built-in project type defaults below.

If no argument is given and templates exist in the local directory, list them and ask which to use. If no templates exist anywhere, proceed with built-in defaults.

## 1.2 Supported Project Types

Detect automatically from existing files, or ask the user if the directory is empty:

| Type | Detection | Key Files |
|------|-----------|-----------|
| **Node.js API** | `package.json` with no frontend framework | `src/`, `tsconfig.json` |
| **React app** | `package.json` with `react` dep | `src/App.tsx`, `vite.config.*` |
| **Next.js app** | `package.json` with `next` dep | `app/` or `pages/`, `next.config.*` |
| **Python package** | `pyproject.toml` or `setup.py` | `src/`, `tests/` |
| **Go service** | `go.mod` | `cmd/`, `internal/` |
| **Rust crate** | `Cargo.toml` | `src/main.rs` or `src/lib.rs` |
| **Flutter app** | `pubspec.yaml` with `flutter` dep | `lib/`, `test/` |
| **Generic** | No detection match | Minimal scaffold |

# PHASE 2: GATHER PROJECT DETAILS

Read the current directory to understand what already exists:
- Config files (`package.json`, `pubspec.yaml`, `go.mod`, `Cargo.toml`, `pyproject.toml`, etc.)
- Is there already a `CLAUDE.md`? If so, confirm before overwriting.
- Is there a git repo initialized? If not, offer to `git init`.
- What is the project name (from directory name or config files)?
- What is the target deployment environment (if evident from config)?

# PHASE 3: APPLY SCAFFOLD

## 3.1 Create CLAUDE.md

Generate a `CLAUDE.md` tailored to the detected project type. Include:

- **Project overview** — name, type, language, framework
- **Directory structure** — expected layout for the project type
- **Conventions** — naming, file organization, import ordering
- **Commands** — build, test, lint, run commands for the framework
- **Architecture decisions** — document any choices made during scaffold

If using a template, replace placeholders with actual project details and keep all convention sections intact.

## 3.2 Create Project Memory

Create `~/.claude/projects/{project-path}/memory/MEMORY.md` with:
- Template/type used and bootstrap date
- Recommended build pipeline
- Initial metrics baseline targets
- Foundation checklist status (from Phase 3.3)

## 3.3 Validate Foundation Requirements

Before recommending feature development, verify the project has these foundations in place.
Check each item. If missing, add it to CLAUDE.md as a "Foundation TODO" and flag it in
the pipeline as "MUST complete before feature development."

### a) SERVICE / MODULE LAYER
Domain-split service or module files exist — not one monolithic service or controller.
Each business domain should have its own module from the start.
**Why:** Monolithic files become rework magnets. Splitting after the fact costs dozens of commits.

### b) STRING CONSTANTS / LOCALIZATION
A string constants file, i18n setup, or equivalent exists for user-facing text.
Brand terms and feature names are constants, not inline strings.
**Why:** Late renames cascade through the entire codebase — tests, UI, docs.

### c) REUSABLE COMPONENT LIBRARY (UI projects)
Reusable themed components exist with accessibility baked in (semantic labels,
appropriate touch/click targets, design tokens). Screens/pages should compose from these.
**Why:** Retrofitting accessibility and consistent styling costs many commits spread across days.

### d) PRIVACY-AWARE DATA MODEL
Public vs private data separation is designed upfront. Models that will be read by
other users have public projections without PII.
**Why:** Late-breaking PII exposure requires multi-step migrations.

### e) DEFENSIVE DEFAULTS (API/service projects)
HTTP clients and service layers include: timeouts, error handling on all async calls,
error sanitization (no internal details leaked to callers), and graceful shutdown.
**Why:** Missing defaults cause repeated fix commits across the project lifecycle.

### f) QUERY SAFETY (database-backed projects)
All database queries have limits by default. Batch write helpers and idempotency
patterns are established for background jobs.
**Why:** Unbounded queries and non-idempotent operations cause scale retrofits.

### g) ENV / CONFIG STRATEGY
Environment variable loading is established and verified working before feature
development begins. A `.env.example` documents all required and optional vars.
Config defaults are centralized in a shared config module, not scattered across files.
**Why:** Trial-and-error env loading and duplicated config defaults cause co-change rework.

### h) TEST INFRASTRUCTURE
Test runner is configured and at least one example test passes. CI pipeline runs tests
on every push (if applicable). Tests are written alongside features, not batched after.
**Why:** Batch-written tests discover issues requiring return trips to feature code.

## 3.4 Architecture Gate

Add the following to the project's CLAUDE.md:

```
## Architecture Gate
Run an architecture review AFTER foundations are in place but BEFORE feature buildout.
This catches monolith patterns, missing service splits, and data model issues when they
cost 1 commit to fix, not 30+.

Timeline: bootstrap -> foundations -> architecture review -> feature development
```

Also add this as a mandatory (BLOCKING) step in the pipeline between foundations and features.

**Why:** Architecture reviews run after features are built find issues that are expensive to
fix in existing code. Running them early catches problems at near-zero rework cost.

# PHASE 4: DISPLAY RESULTS

## Output Format

```
## Project Bootstrapped: {project-name}

### Type: {detected-or-selected type}
### Template: {template-name or "built-in defaults"}

### Files Created
- `CLAUDE.md` — project conventions and architecture
- `~/.claude/projects/.../memory/MEMORY.md` — initial memory

### Foundation Checklist
- [x] Service layer split          (or [ ] TODO)
- [x] String constants             (or [ ] TODO)
- [x] Component library            (or [ ] TODO — UI projects only)
- [x] Privacy-aware data model     (or [ ] TODO)
- [x] Defensive defaults           (or [ ] TODO — API projects only)
- [x] Query safety                 (or [ ] TODO — DB projects only)
- [x] Env/config strategy          (or [ ] TODO)
- [x] Test infrastructure          (or [ ] TODO)

### Recommended Pipeline
1. Complete foundation TODOs above
2. Architecture review (BLOCKING — do not skip)
3. Feature development
4. Security review after each feature batch
5. QA (cap at 2 rounds — route remaining issues upstream)

### Top Pitfalls to Watch
1. {pitfall relevant to project type} — {prevention}
2. ...

### First Step
{What to do next based on foundation checklist status}
```

# PROJECT TYPE DEFAULTS

When no template is available, use these sensible defaults per project type:

## Node.js API
- Structure: `src/` with domain-split modules, `src/config.ts`, `tests/`
- Lint: ESLint + Prettier
- Test: Jest or Vitest
- Key convention: centralized error handling middleware, typed request/response

## React App
- Structure: `src/components/`, `src/hooks/`, `src/services/`, `src/constants/`
- Lint: ESLint + Prettier
- Test: Vitest + React Testing Library
- Key convention: design tokens in theme file, reusable component library

## Next.js App
- Structure: `app/` (App Router), `components/`, `lib/`, `constants/`
- Lint: ESLint + Prettier + next lint
- Test: Jest or Vitest
- Key convention: server vs client component boundaries documented

## Python Package
- Structure: `src/{pkg}/`, `tests/`, `pyproject.toml`
- Lint: Ruff
- Test: pytest
- Key convention: type hints on all public APIs, `__all__` exports

## Go Service
- Structure: `cmd/`, `internal/`, `pkg/` (if shared)
- Lint: golangci-lint
- Test: go test
- Key convention: interface-driven design, domain packages under `internal/`

## Rust Crate
- Structure: `src/`, `tests/`, `Cargo.toml`
- Lint: clippy
- Test: cargo test
- Key convention: error types defined early, `thiserror` for library, `anyhow` for binary

## Flutter App
- Structure: `lib/` with domain-split folders, `lib/constants/`, `lib/widgets/`, `test/`
- Lint: flutter_lints
- Test: flutter test
- Key convention: Semantics on all interactive widgets, design tokens, domain services
