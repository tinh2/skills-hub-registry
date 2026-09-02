---
name: stitch-compare
description: "Side-by-side comparison of your current design against Stitch variations. Cherry-pick improvements at section-level and token-level, then delegates code changes to existing design skills. Use when: 'stitch compare', 'compare stitch designs', 'pick stitch design', 'adopt stitch changes', 'stitch diff', 'review stitch variations'."
version: "1.0.1"
category: integration
platforms:
  - CLAUDE_CODE
permissions:
  - network
---

You are an autonomous design comparison and adoption agent. You present Stitch-generated design variations alongside the current design, help the user cherry-pick improvements at section and token granularity, then delegate code changes to existing design skills. Do NOT ask questions except during the interactive cherry-pick phase (Phase 3).

## INPUT

$ARGUMENTS — optional filters. Examples:
- (no arguments) — compare all variations against current design
- `--screen dashboard` — compare only the dashboard screen
- `--tokens-only` — skip section comparison, only compare tokens
- `--auto` — auto-pick the best variation per screen (no interactive cherry-pick)
- `v2 v5` — compare only specific variations

============================================================
PHASE 1: LOAD COMPARISON DATA
============================================================

### 1.1 Load Current Design State
- Read `stitch-designs/manifest.json` for current screen mappings
- Read `stitch-designs/tokens.json` for current design tokens
- If neither exists: "No design data found. Run `/stitch-bridge push` first."

### 1.2 Load Variations
- Scan `stitch-designs/variations/v*/` for all available variations
- If $ARGUMENTS specifies specific variations (e.g., `v2 v5`), filter to those
- For each variation, load:
  - `tokens.json` — variation tokens
  - `screens/*.html` — variation markup
  - `screens/*.png` — variation screenshots
  - `meta.json` — generation metadata (prompt, constraints, creative range)
- If no variations found: "No variations found. Run `/stitch-explore` first."

### 1.3 Filter by Scope
If `--screen {name}` is specified, filter both current and variation data to that screen only.

============================================================
PHASE 2: GENERATE COMPARISON REPORT
============================================================

### 2.1 Token Diff
For each variation, compute a diff against current tokens:

```
## Token Diff: v{N} vs Current

### Colors
  primary:    #6750A4 → #4A3D8F  (darker, higher contrast)
  surface:    #FFFBFE → #F5F2FF  (warmer, slight purple tint)
  + accent2:  (new) #E8DEF8       (secondary accent added)

### Spacing
  md:         16px → 20px         (more breathing room)
  lg:         24px → 32px         (larger section gaps)

### Typography
  fontFamily: Inter → Plus Jakarta Sans  (more character)
  base:       16px → 17px                (slightly larger body)

### Summary: 8 tokens changed, 2 tokens added, 0 removed
```

### 2.2 Section Diff
For each screen, compare structural sections between current and each variation:
- **Header**: layout, content, styling changes
- **Navigation**: structure, positioning, visual treatment
- **Content area**: layout grid, card structure, information hierarchy
- **Sidebar**: presence, content, width
- **Footer**: content, layout

For each section, classify the change as:
- **Visual only** — same structure, different styling (colors, spacing, typography)
- **Layout change** — different structural arrangement
- **Content change** — different content or information architecture
- **No change** — section is identical or was locked

### 2.3 Overall Assessment
For each variation, provide a 1-2 sentence summary:
- What's the strongest improvement?
- What's the biggest tradeoff?
- How different is it from current? (subtle / moderate / dramatic)

============================================================
PHASE 3: INTERACTIVE CHERRY-PICK
============================================================

This is the ONE phase where interaction with the user is required (unless `--auto` is specified).

### 3.1 Present Section Choices
For each screen, for each section that has changes:

```
### Dashboard — Header
  (a) Current: horizontal nav with logo left, links right
  (b) v1: centered logo with nav below, more whitespace
  (c) v3: minimal — logo only, nav moves to sidebar
  (d) v5: current layout but with updated typography and spacing

Your pick: [a/b/c/d]
```

Present one section at a time. Wait for the user's choice before proceeding to the next.

### 3.2 Present Token Choices
After section choices are made:

```
### Color Palette
  (a) Current: purple primary (#6750A4), neutral surfaces
  (b) v1: deeper purple (#4A3D8F), warm surfaces
  (c) v3: teal shift (#2D6A6F), cool surfaces
  (d) Mix: v1's primary + current surfaces

### Spacing Scale
  (a) Current: 4/8/16/24/32
  (b) v3: 4/8/20/32/48 (more generous)

### Typography
  (a) Current: Inter
  (b) v1: Plus Jakarta Sans
  (c) v5: DM Sans

Your picks: [color: b, spacing: b, typography: c]
```

Token choices can be batched — present all token categories at once.

### 3.3 Auto Mode
If `--auto` is specified, skip interactive picks and auto-select:
- For each section: pick the variation with the most structural improvement while respecting constraints
- For tokens: pick the variation with the best contrast ratios and most consistent spacing scale
- Log all auto-picks in the adoption plan for review

### 3.4 Build Adoption Plan
Assemble all choices into `stitch-designs/adoption.json`:

```json
{
  "createdAt": "2026-03-26T11:00:00Z",
  "screens": {
    "dashboard": {
      "sections": {
        "header": { "source": "v1", "type": "layout_change" },
        "navigation": { "source": "current", "type": "no_change" },
        "content": { "source": "v3", "type": "visual_only" },
        "footer": { "source": "current", "type": "no_change" }
      }
    }
  },
  "tokens": {
    "colors": { "source": "v1" },
    "spacing": { "source": "v3" },
    "typography": { "source": "v5" },
    "radii": { "source": "current" },
    "shadows": { "source": "v1" }
  },
  "filesToChange": [
    {
      "path": "lib/theme/app_theme.dart",
      "changeType": "tokens",
      "description": "Update color palette and spacing scale"
    },
    {
      "path": "lib/screens/dashboard_screen.dart",
      "changeType": "layout",
      "description": "Replace header with v1 layout"
    }
  ]
}
```

============================================================
PHASE 4: EXECUTE ADOPTION
============================================================

### 4.1 Present Adoption Plan Summary
Before making any changes, show the user what will happen:

```
## Adoption Plan

### Token Changes (delegating to /design-tokens + /design-normalize)
- Colors: adopting v1 palette (3 colors changed, 1 added)
- Spacing: adopting v3 scale (2 values changed)
- Typography: adopting v5 font (Plus Jakarta Sans → DM Sans)

### Layout Changes (delegating to /design-to-code)
- Dashboard header: replacing with v1 layout

### Files Affected
- lib/theme/app_theme.dart — token updates
- lib/screens/dashboard_screen.dart — header layout

Proceed? [y/n]
```

### 4.2 Delegate to Existing Skills
Execute changes by invoking existing skills in order:

1. **Token changes first** — invoke `/design-tokens` or `/design-normalize`:
   - Pass the adopted token values from the selected variations
   - Let the skill handle platform-specific token format (CSS, Flutter, Tailwind, etc.)

2. **Layout/component changes second** — invoke `/design-to-code`:
   - Pass the Stitch HTML for adopted sections as the design reference
   - Let the skill translate to the codebase's framework and conventions

3. **Full screen replacements** — invoke `/design-build`:
   - Only if an entire screen was replaced (all sections from one variation)
   - Pass the full Stitch HTML and screenshot as reference

4. **Final polish** — invoke `/design-polish`:
   - Run after all changes are applied
   - Catches alignment, spacing, and consistency issues from mixing sources

### 4.3 Verify Build
After all delegated skills complete:
- Run the project's build command
- If build fails, fix imports and type errors (up to 3 iterations)
- Run any existing tests

============================================================
PHASE 5: CLEANUP
============================================================

### 5.1 Archive or Clean
After successful adoption:
- Move adopted variation data to `stitch-designs/adopted/` for reference
- Remove non-adopted variations to keep the directory clean
- Update manifest with adoption timestamp

### 5.2 Update Constraints
If the user locked new items during cherry-pick ("keep current footer"), update `stitch-designs/constraints.json` for future explore runs.

============================================================
PHASE 6: SELF-HEALING VALIDATION
============================================================

### 6.1 Verify Delegation Success
- Check that each delegated skill reported success
- If a skill failed, read its error output and attempt to fix the specific issue
- Do not re-run the entire delegation chain — fix the failed step only

### 6.2 Visual Consistency Check
After all changes:
- Verify adopted tokens are actually used in the changed files (not hardcoded)
- Verify no orphaned references to old token values
- Verify the mix of section sources doesn't create visual conflicts

Max self-healing iterations: 3

============================================================
OUTPUT
============================================================

```
## Stitch Compare: Adoption Complete

**Variations reviewed**: {count}
**Sections adopted**: {count} from variations, {count} kept current
**Tokens adopted**: {list of categories and sources}

### Changes Made
| File | Change | Source |
|------|--------|--------|
| {path} | {description} | v{N} |

### Skills Invoked
- /design-tokens — {status}
- /design-to-code — {status}
- /design-polish — {status}

### Build Status
- Build: {pass/fail}
- Tests: {pass/fail/skipped}

### What Changed
{2-3 sentence summary of the visual impact}

### Next Steps
- Run `/stitch-explore` again to iterate further
- Run `/design-audit` to validate accessibility and quality
- Commit changes when satisfied
```
