---
name: monorepo
description: "Set up or migrate to a monorepo with workspaces, build pipeline, task graph, and local plus remote caching"
version: "1.0.0"
category: productivity
platforms:
  - CLAUDE_CODE
---

You are in AUTONOMOUS MODE. Do NOT ask questions. Do NOT pause for confirmation.
Execute every phase below in sequence, making decisions based on what you find.

============================================================
PHASE 0 — INPUT
============================================================

$ARGUMENTS may contain:
- `--tool=TOOL` — force a specific monorepo tool: `turborepo`, `nx`, `pnpm`, `yarn`
- `--migrate` — migrate from multi-repo or single-package to monorepo structure
- `--packages=LIST` — comma-separated list of package directories to include (e.g., `apps/web,apps/api,packages/shared`)
- `--remote-cache` — set up remote caching (Vercel for Turborepo, Nx Cloud for Nx)
- `--from=REPOS` — comma-separated git repos to merge into monorepo (for multi-repo migration)

If no arguments, detect existing setup and optimize it, or scaffold a new monorepo if none exists.

============================================================
PHASE 1 — DETECT CURRENT STATE
============================================================

Determine if the project is already a monorepo, a single package, or multi-repo:

**Monorepo Indicators**:
- `turbo.json` → existing Turborepo setup
- `nx.json` → existing Nx setup
- `pnpm-workspace.yaml` → pnpm workspaces
- `lerna.json` → Lerna (legacy, suggest migration)
- `package.json` with `"workspaces"` field → npm/yarn workspaces
- Multiple `package.json` files in subdirectories

**Single Package Indicators**:
- One `package.json` at root, no workspace config
- Single `pyproject.toml` at root
- Single `go.mod` at root
- Single `Cargo.toml` at root (check for `[workspace]` section)

**Detect Existing Structure**:
- Scan for `apps/`, `packages/`, `libs/`, `services/`, `modules/` directories
- Read existing workspace config to understand current package layout
- Check for shared dependencies across packages
- Detect build tool: `tsconfig.json` project references, `vite.config.*`, `webpack.config.*`

Record: current state (monorepo/single/multi), tool (if any), packages found, language.

============================================================
PHASE 2 — SELECT MONOREPO TOOL
============================================================

If no tool is specified, select based on detected stack:

**Turborepo** (recommended for most Node.js/TypeScript projects):
- Best for: TypeScript, Next.js, React, Node.js backends
- Strengths: simple config, fast local caching, Vercel remote cache, minimal learning curve
- Use when: primarily JavaScript/TypeScript ecosystem

**Nx** (recommended for large/enterprise projects):
- Best for: Angular, React, Node.js, polyglot projects with 20+ packages
- Strengths: affected-only computation, generators, dependency graph visualization
- Use when: need code generation, advanced task orchestration, or have non-JS packages

**pnpm workspaces** (recommended for lightweight needs):
- Best for: projects that want workspaces without a build orchestrator
- Strengths: strict dependency isolation, fast installs, disk efficient
- Use when: workspace dependency management is sufficient, no complex build pipeline

**Cargo workspaces** (for Rust):
- Use `[workspace]` in root `Cargo.toml`

**Go workspaces** (for Go):
- Use `go.work` file (Go 1.22+)

============================================================
PHASE 3 — SCAFFOLD OR MIGRATE
============================================================

**3.1 — If starting fresh (no existing monorepo)**:

Create the directory structure:
```
.
├── apps/
│   ├── web/          # Frontend application
│   └── api/          # Backend application
├── packages/
│   ├── shared/       # Shared types, utils, constants
│   ├── ui/           # Shared UI components (if frontend)
│   ├── config/       # Shared configs (eslint, tsconfig, tailwind)
│   └── db/           # Database client and migrations (if applicable)
├── turbo.json        # or nx.json
├── package.json      # Root workspace config
├── pnpm-workspace.yaml  # if using pnpm
└── tsconfig.json     # Root tsconfig with project references
```

Adjust based on `--packages` if provided.

**3.2 — If migrating from single package (`--migrate`)**:

1. Create `apps/` and `packages/` directories
2. Move the existing app into `apps/{name}/`
3. Extract shared code into `packages/shared/`:
   - Types/interfaces used across modules
   - Utility functions
   - Constants and configuration
4. Update all import paths
5. Create workspace config at root
6. Update CI workflows to use workspace commands

**3.3 — If migrating from multi-repo (`--from=REPOS`)**:

1. For each repo in the `--from` list:
   - Clone into a temporary directory
   - Move contents into `apps/{repo-name}/` or `packages/{repo-name}/`
   - Preserve git history with subtree merge if possible
2. Deduplicate shared dependencies → move to root `package.json`
3. Extract common code into `packages/shared/`
4. Update all cross-repo imports to workspace references
5. Remove duplicated configs (eslint, prettier, tsconfig) → use shared configs from `packages/config/`

============================================================
PHASE 4 — CONFIGURE WORKSPACE
============================================================

**4.1 — Package Manager Workspace Config**:

For pnpm (create `pnpm-workspace.yaml`):
```yaml
packages:
  - 'apps/*'
  - 'packages/*'
```

For npm/yarn (add to root `package.json`):
```json
{
  "workspaces": ["apps/*", "packages/*"]
}
```

**4.2 — Shared Package Setup**:

For each package in `packages/`:
- Create `package.json` with `"name": "@{scope}/{package-name}"`
- Set `"main"` and `"types"` entry points
- Set `"private": true` if not published
- If TypeScript: create `tsconfig.json` extending root config with `"composite": true`

For apps referencing shared packages:
- Add workspace dependency: `"@{scope}/shared": "workspace:*"`
- Update `tsconfig.json` to include project reference: `"references": [{ "path": "../packages/shared" }]`

**4.3 — Root TypeScript Config** (if TypeScript):

Create root `tsconfig.json`:
```json
{
  "compilerOptions": {
    "composite": true,
    "declaration": true,
    "declarationMap": true,
    "incremental": true
  },
  "references": [
    { "path": "apps/web" },
    { "path": "apps/api" },
    { "path": "packages/shared" }
  ]
}
```

============================================================
PHASE 5 — CONFIGURE BUILD PIPELINE
============================================================

**5.1 — Turborepo Config** (if selected):

Create `turbo.json`:
```json
{
  "$schema": "https://turbo.build/schema.json",
  "globalDependencies": ["**/.env.*local"],
  "tasks": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**", ".next/**", "build/**"]
    },
    "lint": {
      "dependsOn": ["^build"]
    },
    "typecheck": {
      "dependsOn": ["^build"]
    },
    "test": {
      "dependsOn": ["^build"]
    },
    "dev": {
      "cache": false,
      "persistent": true
    }
  }
}
```

Add scripts to root `package.json`:
```json
{
  "scripts": {
    "build": "turbo run build",
    "dev": "turbo run dev",
    "lint": "turbo run lint",
    "test": "turbo run test",
    "typecheck": "turbo run typecheck"
  }
}
```

**5.2 — Nx Config** (if selected):

Create `nx.json`:
```json
{
  "$schema": "https://raw.githubusercontent.com/nrwl/nx/master/packages/nx/schemas/nx-schema.json",
  "targetDefaults": {
    "build": {
      "dependsOn": ["^build"],
      "cache": true
    },
    "lint": { "cache": true },
    "test": { "cache": true }
  },
  "defaultBase": "main",
  "namedInputs": {
    "default": ["{projectRoot}/**/*", "sharedGlobals"],
    "sharedGlobals": ["{workspaceRoot}/tsconfig.base.json"],
    "production": ["default", "!{projectRoot}/**/*.spec.ts"]
  }
}
```

Create `project.json` in each package/app with targets.

**5.3 — Caching**:

Local caching is enabled by default for both Turborepo and Nx.

For remote caching (if `--remote-cache`):
- Turborepo: `npx turbo login && npx turbo link` (Vercel Remote Cache)
  - Or self-hosted: configure `turbo.json` with `"remoteCache": { "signature": true }`
- Nx: `npx nx connect` (Nx Cloud)
  - Generates `nx-cloud.env` with access token

============================================================
PHASE 6 — CONFIGURE CI
============================================================

Create or update `.github/workflows/ci.yml` for affected-only builds:

**Turborepo CI**:
```yaml
name: CI
on:
  pull_request:
    branches: [main]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 2
      - uses: pnpm/action-setup@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: pnpm
      - run: pnpm install --frozen-lockfile
      - run: pnpm turbo run lint typecheck test build --filter=...[HEAD~1]
```

**Nx CI**:
```yaml
      - run: npx nx affected --target=lint --base=origin/main
      - run: npx nx affected --target=test --base=origin/main
      - run: npx nx affected --target=build --base=origin/main
```

============================================================
PHASE 7 — VERIFY SETUP
============================================================

1. Install all dependencies from root: `pnpm install` (or npm/yarn equivalent)
2. Run build: `pnpm turbo run build` (or `npx nx run-many --target=build`)
3. Verify each package resolves workspace dependencies correctly
4. Run lint across all packages
5. Run tests across all packages
6. Verify the task graph: `pnpm turbo run build --dry` or `npx nx graph`
7. Check cache hits: run build twice and verify second run uses cache

Fix any issues found during verification.

============================================================
OUTPUT
============================================================

Print a summary:

```
## Monorepo Setup Complete

### Tool: {Turborepo | Nx | pnpm workspaces}
### Package Manager: {pnpm | npm | yarn}

### Workspace Structure
- apps/web — {description}
- apps/api — {description}
- packages/shared — {description}
- packages/config — {description}

### Task Pipeline
- build: depends on ^build, cached, outputs: dist/**
- lint: cached
- test: cached
- dev: not cached, persistent

### Caching
- Local: enabled ({cache directory})
- Remote: {configured with Vercel/Nx Cloud | not configured}

### CI Configuration
- .github/workflows/ci.yml — affected-only builds on PRs

### Files Created/Modified
- {list of files}
```

============================================================
NEXT STEPS
============================================================

1. Run `pnpm dev` to start all apps in development mode
2. Add new packages: create directory in `packages/`, add `package.json`, run `pnpm install`
3. Run `/release --monorepo` to set up versioning with changesets
4. Run `/linter` to set up shared lint config in `packages/config/`
5. Enable remote caching: run with `--remote-cache` flag

============================================================
DO NOT
============================================================

- Do NOT mix monorepo tools (e.g., Turborepo AND Nx in the same project)
- Do NOT hoist all dependencies to root — respect package boundaries
- Do NOT use `*` version ranges for workspace dependencies — use `workspace:*` (pnpm) or `*` (npm/yarn)
- Do NOT create circular dependencies between packages
- Do NOT put app-specific code in shared packages — shared packages must be genuinely reusable
- Do NOT skip the verify step — broken workspace references cause cascading failures
- Do NOT configure remote caching without `--remote-cache` flag — it requires authentication
- Do NOT use Lerna for new projects — it is in maintenance mode, use Turborepo or Nx
- Do NOT overwrite existing monorepo configs without reading them first
