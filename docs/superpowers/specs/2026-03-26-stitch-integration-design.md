# Stitch Integration Skills — Design Spec

**Date:** 2026-03-26
**Status:** Approved
**Scope:** 4 new skills integrating Google Stitch with the existing design skill library

## Problem

Existing apps have established designs, but lack a workflow to:
- Use Stitch as a design collaborator to improve existing UIs
- Compare Stitch-generated alternatives side-by-side with current designs
- Cherry-pick improvements at section and token granularity
- Sync design context bidirectionally between codebase and Stitch

## Design Principles

- **Stitch is a design tool, not a code generator** — existing design skills handle all code changes
- **Platform-agnostic intermediate format** — works with Flutter, web, native, and future platforms
- **Non-destructive until adoption** — all Stitch output stages in a working directory, nothing touches the codebase until explicitly confirmed
- **Builds on existing skills** — `design-tokens`, `design-normalize`, `design-to-code`, `design-build`, `design-polish` handle implementation

## Skills Overview

| Skill | Category | Purpose |
|-------|----------|---------|
| `stitch-bridge` | Integration | Bidirectional sync between codebase and Stitch |
| `stitch-explore` | Generation | Generate design alternatives with constraints |
| `stitch-compare` | Decision | Side-by-side diff + cherry-pick + delegate to existing skills |
| `stitch-pipeline` | Combo | Chain all three in one invoke |

## Skill 1: `stitch-bridge`

**Purpose:** Move design context between codebase and Stitch in both directions.

### Push Flow (Code to Stitch)

1. Scan codebase for current design state:
   - Tokens: colors, spacing, typography, radii, shadows
   - Component inventory: buttons, cards, forms, navigation, etc.
   - Screen screenshots via Playwright (web) or simulator (Flutter/mobile)
2. Auto-detect platform/framework from codebase (Flutter ThemeData, CSS custom properties, Tailwind config, SCSS variables, raw values)
3. Package as Stitch-compatible context
4. Use Stitch MCP tools to create or update the Stitch project

Push is idempotent — re-running updates the existing Stitch project, does not duplicate.

### Pull Flow (Stitch to Code)

1. Fetch generated designs from Stitch via MCP (HTML, tokens, screenshots)
2. Normalize into platform-agnostic intermediate format in `stitch-designs/` staging directory:
   - `tokens.json` — extracted design tokens
   - `screens/` — HTML + screenshots per screen
   - `manifest.json` — maps Stitch screens to codebase files
3. Does NOT write to codebase — `stitch-compare` handles adoption

### Key Decisions

- `stitch-designs/` is gitignored by default (working directory, not committed)
- Intermediate format is platform-agnostic: token JSON + markup + images
- Auto-detection covers Flutter, CSS, Tailwind, SCSS, and raw values

## Skill 2: `stitch-explore`

**Purpose:** Tell Stitch what to improve and get back design alternatives with constraints.

### Input Modes

- **Vibe-based** — "make this feel more premium", "simplify the navigation", "this looks too cluttered"
- **Targeted** — "redesign just the header", "give me 3 color palette options", "try a different layout for the card grid"
- **Constraint-based** — "keep my brand colors but improve spacing", "don't change the nav structure, just the visual treatment"

### Flow

1. Read current Stitch project state (from bridge's last push)
2. Send improvement prompt to Stitch with constraints attached
3. Request multiple variations (default: 3 alternatives per screen/section)
4. Pull results through bridge's pull flow into `stitch-designs/`
5. Each variation stored in its own subdirectory: `stitch-designs/variations/v1/`, `v2/`, `v3/`

### Constraint System

Constraints control what Stitch can and cannot change:

- **Lock tokens** — "keep these colors/fonts" sends them as fixed constraints
- **Lock sections** — "don't touch the footer" excludes from generation
- **Lock components** — "keep my button style" preserves specific component patterns
- Constraints saved in `stitch-designs/constraints.json` so iterating doesn't require re-specifying

### Key Decisions

- Variations are additive — running explore again adds new variations, does not overwrite
- Can run explore multiple times with different prompts before moving to compare
- Each variation tracks which prompt generated it for traceability

## Skill 3: `stitch-compare`

**Purpose:** Present current design against Stitch variations, let user pick what to adopt at section and token level, then delegate code changes to existing design skills.

### Comparison Flow

1. Read current screens (screenshots + tokens) and Stitch variations from `stitch-designs/variations/`
2. Generate comparison report per screen:
   - Screenshot side-by-side: current vs each variation
   - Token diff: what changed (colors, spacing, typography, shadows)
   - Section diff: header, nav, content, footer — structural differences
3. Present choices interactively:
   - **Section-level** — "For the dashboard header, use: (a) current, (b) v1, (c) v2, (d) v3"
   - **Token-level** — "For color palette, use: (a) current, (b) v1's palette, (c) v2's palette"
   - Mixing allowed — pick v1's header with v3's color palette

### Adoption Output

1. Assemble choices into adoption plan: `stitch-designs/adoption.json`
2. Map each choice to codebase files that need to change
3. Delegate actual code changes to existing skills:
   - Token changes → `design-tokens` or `design-normalize`
   - Layout/component changes → `design-to-code`
   - Full screen replacements → `design-build`
   - Final cleanup → `design-polish`

### Key Decisions

- Non-destructive until adoption plan is confirmed
- Can re-run compare to change choices before adopting
- `adoption.json` is human-readable for review before execution
- Existing skills handle platform-specific code generation — compare stays platform-agnostic

## Skill 4: `stitch-pipeline`

**Purpose:** Chain all three skills for the common "make my app look better" workflow.

### Default Flow

1. `stitch-bridge` push — sync current design to Stitch
2. `stitch-explore` — prompt for what to improve, generate 3 variations
3. `stitch-bridge` pull — fetch variations
4. `stitch-compare` — present choices, build adoption plan
5. On approval — delegate to existing design skills

### Invocation Options

- `/stitch-pipeline` — full flow, asks what to improve
- `/stitch-pipeline "make the onboarding feel less overwhelming"` — full flow with pre-set prompt
- `/stitch-pipeline --screen settings` — scope to a single screen
- `/stitch-pipeline --skip-push` — skip bridge push if already synced recently

### Behavior

- Pause points between each phase for course adjustment
- If explore results aren't satisfactory, loops back to explore with refined constraints
- Respects existing `constraints.json` from previous runs
- Cleans up `stitch-designs/` after adoption is complete (or keeps with `--keep`)

## Intermediate Format

The `stitch-designs/` directory is the handoff point between all skills:

```
stitch-designs/
  manifest.json          # Maps Stitch screens to codebase files
  tokens.json            # Current extracted tokens
  constraints.json       # Locked tokens/sections/components
  variations/
    v1/
      tokens.json        # Variation tokens
      screens/
        dashboard.html   # Screen markup
        dashboard.png    # Screen screenshot
      meta.json          # Prompt that generated this, timestamp
    v2/
      ...
    v3/
      ...
  adoption.json          # Cherry-picked choices (after compare)
```

## Existing Skill Dependencies

These existing skills are invoked during the adoption phase:

| Existing Skill | When Used |
|---------------|-----------|
| `design-tokens` | Token changes (colors, spacing, typography) |
| `design-normalize` | Aligning codebase to adopted token changes |
| `design-to-code` | Layout and component changes from Stitch markup |
| `design-build` | Full screen replacements |
| `design-polish` | Final quality pass after adoption |
| `design-setup` | Initial context discovery if no design tokens exist yet |

## Prerequisites

- Google Stitch MCP server configured in Claude Code (`stitch` MCP)
- Stitch API key stored (currently in AWS Secrets Manager: `stitch-api-key`)
- For screenshot capture: Playwright (web) or platform simulator (mobile)

## Out of Scope

- Stitch as a code generator — all code changes go through existing skills
- Stitch project management (teams, sharing, permissions)
- Figma-to-Stitch sync (separate concern, could be a future skill)
