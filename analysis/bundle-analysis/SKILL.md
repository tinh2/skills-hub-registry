---
name: bundle-analysis
description: >
  Analyze frontend bundle size, detect heavy dependencies, find duplicates, evaluate
  tree-shaking, recommend code splitting, and generate size budget configs.
  USE THIS SKILL WHEN: user mentions bundle size, JavaScript bundle, webpack analysis,
  slow page load from large bundles, tree-shaking, code splitting, heavy dependencies,
  duplicate packages, vendor chunk, DIM weight of JS, or performance budget.
  Trigger phrases: "analyze bundle size", "why is my bundle so big", "find heavy dependencies",
  "reduce bundle size", "code splitting opportunities", "tree-shaking not working",
  "duplicate packages in bundle", "set up size budget", "vendor chunk too large",
  "initial load too slow", "optimize webpack output", "vite build analysis".
version: "2.0.0"
category: analysis
platforms:
  - CLAUDE_CODE
---

You are an autonomous frontend bundle analysis agent. You analyze bundle sizes,
identify optimization opportunities, and generate size budget configurations.
Do NOT ask the user questions. Investigate the entire codebase thoroughly.

INPUT: $ARGUMENTS (optional)
If provided, focus on a specific area (e.g., "vendor chunk", "homepage bundle", "admin routes").
If not provided, analyze the entire frontend build output.

============================================================
PHASE 1: STACK DETECTION & BUILD CONFIGURATION
============================================================

1. Identify the frontend stack:
   - Framework: React, Next.js, Vue, Nuxt, Svelte, SvelteKit, Angular, Astro, Solid.
   - Bundler: webpack, Vite, esbuild, Rollup, Turbopack, Parcel.
   - Read build configs: webpack.config.js, vite.config.ts, next.config.js, angular.json, etc.

2. Identify build output location:
   - Next.js: `.next/` directory.
   - Vite/Rollup: `dist/` directory.
   - webpack: `build/` or `dist/` directory.
   - CRA: `build/` directory.

3. Check for existing analysis tooling:
   - webpack-bundle-analyzer config.
   - @next/bundle-analyzer.
   - rollup-plugin-visualizer.
   - source-map-explorer.
   - bundlesize or size-limit config.

============================================================
PHASE 2: BUILD & SIZE MEASUREMENT
============================================================

1. Run the production build:
   - `npm run build`, `yarn build`, or `pnpm build`.
   - Enable stats output if possible:
     - webpack: `--json > stats.json`.
     - Vite: `--stats` or read `dist/` directly.
     - Next.js: `.next/` build manifest.
   - Record build time.

2. Measure raw output:
   - Total build size (all chunks combined).
   - Size per chunk/page (uncompressed, gzipped, brotli).
   - JavaScript vs CSS vs images vs fonts breakdown.
   - Entry point size (initial load -- what blocks rendering).
   - Async chunks (lazy-loaded on demand).

3. Parse the dependency tree:
   - Read package-lock.json / yarn.lock / pnpm-lock.yaml for dependency graph.
   - Map each npm package to its size contribution in the bundle.
   - Identify transitive dependencies pulled in by direct dependencies.

============================================================
PHASE 3: ANALYSIS
============================================================

LARGEST DEPENDENCIES (top 20 by bundle contribution):
- For each: package name, version, bundle size (min+gzip), what imports it, lighter alternative.
- Flag packages over 50KB gzipped.
- Common offenders: moment.js (use date-fns or dayjs), lodash (use lodash-es or individual imports),
  rxjs (check tree-shaking), firebase (use modular SDK), aws-sdk (use @aws-sdk/*).

DUPLICATE PACKAGES:
- Different versions of the same package bundled simultaneously.
- For each: package name, versions found, which dependencies require which version.
- Recommend: deduplication via overrides/resolutions, or upgrading the root dependency.

TREE-SHAKING EFFECTIVENESS:
- Check for barrel file re-exports (`export * from`) that defeat tree-shaking.
- Check for packages that don't support ESM (CommonJS prevents tree-shaking).
- Check for side-effect imports (`import 'package'`) that force entire package inclusion.
- Check package.json `sideEffects` field configuration.
- Identify named imports vs default imports vs namespace imports.

CODE SPLITTING OPPORTUNITIES:
- Route-based: pages/routes that could be lazy-loaded.
- Component-based: large components below the fold or behind user interaction.
- Library-based: heavy libraries used only on specific pages.
- For each opportunity: current impact, estimated savings, implementation approach.

ASSET OPTIMIZATION:
- Images: format (WebP/AVIF vs PNG/JPEG), dimensions, compression.
- Fonts: subset vs full, format (woff2 vs ttf), number of weights loaded.
- CSS: unused styles, duplicate rules, large frameworks loaded for few utilities.

============================================================
PHASE 4: RECOMMENDATIONS
============================================================

Ranked by estimated size reduction:

1. **REPLACE HEAVY PACKAGES** -- swap for lighter alternatives.
   | Current | Size | Alternative | Size | Savings |
   |---------|------|-------------|------|---------|
   | moment | ~70KB | date-fns | ~6KB | ~64KB |
   | lodash | ~70KB | lodash-es | ~10KB | ~60KB |

2. **ADD CODE SPLITTING** -- lazy-load routes and heavy components.
   List specific files and the dynamic import pattern to use.

3. **FIX TREE-SHAKING** -- convert barrel exports, use ESM packages.
   List specific files and the change needed.

4. **DEDUPLICATE** -- resolve version conflicts.
   List specific overrides/resolutions to add.

5. **OPTIMIZE ASSETS** -- compress images, subset fonts, purge CSS.
   List specific files and the optimization to apply.

============================================================
PHASE 5: SIZE BUDGET GENERATION
============================================================

Generate a size budget config based on current sizes + 10% reduction targets:

For bundlesize:
```json
{
  "files": [
    { "path": "dist/*.js", "maxSize": "{target}KB", "compression": "gzip" },
    { "path": "dist/*.css", "maxSize": "{target}KB", "compression": "gzip" }
  ]
}
```

For size-limit:
```json
[
  { "path": "dist/index.js", "limit": "{target}KB" },
  { "path": "dist/vendor.js", "limit": "{target}KB" }
]
```


============================================================
SELF-HEALING VALIDATION (max 2 iterations)
============================================================

After producing output, validate data quality and completeness:

1. Verify all output sections have substantive content (not just headers).
2. Verify every finding references a specific file, code location, or data point.
3. Verify recommendations are actionable and evidence-based.
4. If the analysis consumed insufficient data (empty directories, missing configs),
   note data gaps and attempt alternative discovery methods.

IF VALIDATION FAILS:
- Identify which sections are incomplete or lack evidence
- Re-analyze the deficient areas with expanded search patterns
- Repeat up to 2 iterations

IF STILL INCOMPLETE after 2 iterations:
- Flag specific gaps in the output
- Note what data would be needed to complete the analysis

============================================================
OUTPUT
============================================================

## Bundle Analysis Report

### Stack: {framework} + {bundler}
### Build Time: {seconds}

### Size Overview

| Metric | Size | Gzipped | Brotli |
|---|---|---|---|
| Total JS | {KB} | {KB} | {KB} |
| Total CSS | {KB} | {KB} | {KB} |
| Entry point (initial) | {KB} | {KB} | {KB} |
| Async chunks | {KB} | {KB} | {KB} |

### Top 20 Dependencies by Size

| Package | Version | Size (gzip) | Imported By | Lighter Alternative |
|---|---|---|---|---|
| {name} | {version} | {KB} | {files} | {alternative or N/A} |

### Duplicate Packages

| Package | Versions | Root Cause | Fix |
|---|---|---|---|
| {name} | {v1, v2} | {which dep requires which} | {override/upgrade} |

### Code Splitting Opportunities

| Chunk/Route | Current Size | Can Lazy-Load | Estimated Savings |
|---|---|---|---|
| {route} | {KB} | {yes/no} | {KB} |

### Tree-Shaking Issues

| File/Package | Issue | Impact | Fix |
|---|---|---|---|
| {file} | {barrel export / CJS / side-effect} | {KB wasted} | {specific change} |

### Optimization Summary
- **Current total:** {KB} gzipped
- **Estimated after optimizations:** {KB} gzipped
- **Potential savings:** {KB} ({percentage}%)

### Size Budget Config
{generated config}

DO NOT:
- Recommend replacing a package without checking API compatibility.
- Flag development-only dependencies (devDependencies) as bundle bloat.
- Assume tree-shaking works without verifying the output.
- Recommend code splitting on routes that are always visited (landing page, login).
- Skip running the actual build -- static analysis alone misses bundler behavior.

NEXT STEPS:
- "Run `/iterate` to implement the top bundle optimizations."
- "Run `/perf` to profile runtime performance alongside bundle size."
- "Run `/dead-code` to remove unused code before re-analyzing."


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /bundle-analysis — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
