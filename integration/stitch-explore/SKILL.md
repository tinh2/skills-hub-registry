---
name: stitch-explore
description: >-
  Generate design alternatives in Google Stitch with constraints. Tell Stitch what to
  improve about your UI and get back multiple variations — vibe-based, targeted, or
  constraint-locked. Use when: 'stitch explore', 'stitch redesign', 'stitch alternatives',
  'improve design with stitch', 'stitch variations', 'make it look better with stitch'.
version: "1.0.0"
category: integration
platforms:
  - CLAUDE_CODE
permissions:
  - network
---

You are an autonomous design exploration agent. You use Google Stitch to generate design alternatives for existing UIs based on user-provided improvement prompts and constraints. Do NOT ask the user questions.

## INPUT

$ARGUMENTS — what to improve. Examples:
- `"make the dashboard feel more premium"` — vibe-based, full app
- `"redesign the header"` — targeted section
- `"3 color palette options that feel warmer"` — targeted tokens
- `"simplify navigation, keep brand colors"` — constraint-based
- `--screen settings "modernize the layout"` — scope to one screen
- `--variations 5` — override default variation count (default: 3)
- `--creative-range reimagine` — REFINE (subtle), EXPLORE (default), or REIMAGINE (radical)

If no arguments: read the codebase, identify the weakest UI areas, and generate improvement prompts automatically.

============================================================
PHASE 1: LOAD CONTEXT
============================================================

### 1.1 Read Manifest
- Load `stitch-designs/manifest.json` for project ID and screen mappings
- If manifest does not exist: run `/stitch-bridge push` first, then continue

### 1.2 Load Constraints
- Check for `stitch-designs/constraints.json`
- If exists, load locked tokens, sections, and components
- These constraints carry forward from previous explore runs

### 1.3 Parse Improvement Prompt
From $ARGUMENTS, extract:
- **Target**: full app, specific screen, specific section, or specific tokens
- **Intent**: vibe (emotional/qualitative), targeted (structural), or constraint-based
- **Locked items**: anything prefixed with "keep" or "don't change"
- **Variation count**: from `--variations N` or default 3
- **Creative range**: from `--creative-range` or default EXPLORE

============================================================
PHASE 2: BUILD CONSTRAINTS
============================================================

### 2.1 Extract Lock Directives from Prompt
Parse natural language constraints:
- "keep my brand colors" → lock all values in `tokens.json` colors section
- "don't touch the footer" → lock the footer section
- "keep my button style" → lock button component patterns
- "keep the navigation structure" → lock nav layout, allow visual changes

### 2.2 Merge with Existing Constraints
Load `stitch-designs/constraints.json` if it exists and merge:
- New explicit locks override old ones
- Old locks persist unless explicitly unlocked ("unlock colors", "change everything")

### 2.3 Write Updated Constraints
Save to `stitch-designs/constraints.json`:

```json
{
  "updatedAt": "2026-03-26T10:00:00Z",
  "lockedTokens": {
    "colors": ["primary", "secondary"],
    "typography": ["fontFamily"]
  },
  "lockedSections": ["footer", "navigation"],
  "lockedComponents": ["button", "card"],
  "unlockedEverythingElse": true
}
```

============================================================
PHASE 3: GENERATE VARIATIONS
============================================================

### 3.1 Build Stitch Prompts
For each target screen, construct a prompt that:
1. Describes the current design (reference tokens and layout from manifest)
2. States the improvement goal from $ARGUMENTS
3. Includes constraints as explicit rules ("DO NOT change: ...")
4. Requests specific aspects based on intent:
   - Vibe-based: request changes to COLOR_SCHEME, IMAGES, TEXT_FONT
   - Targeted section: request LAYOUT changes for that section
   - Token-focused: request only the relevant aspect (COLOR_SCHEME, TEXT_FONT, etc.)

### 3.2 Call Stitch Variants API
For each screen in scope:

```
screen.variants(prompt, {
  variantCount: N,           // from --variations or default 3
  creativeRange: range,      // REFINE | EXPLORE | REIMAGINE
  aspects: detectedAspects   // LAYOUT, COLOR_SCHEME, IMAGES, TEXT_FONT, TEXT_CONTENT
})
```

This returns an array of Screen objects — one per variation.

### 3.3 Download Variation Assets
For each variation:
1. Call `screen.getHtml()` — download HTML to staging
2. Call `screen.getImage()` — download screenshot to staging

### 3.4 Extract Variation Tokens
Parse each variation's HTML to extract its design tokens (same extraction logic as stitch-bridge pull). Save per-variation `tokens.json`.

### 3.5 Determine Next Variation Directory
- List existing `stitch-designs/variations/v*/` directories
- New variations start at the next available number
- Example: if `v1/`, `v2/`, `v3/` exist, new variations start at `v4/`

### 3.6 Write Variation Files
For each variation, create:

```
stitch-designs/variations/v{N}/
  tokens.json              # Extracted tokens for this variation
  screens/
    {screen-name}.html     # Screen HTML
    {screen-name}.png      # Screen screenshot
  meta.json                # Generation metadata
```

`meta.json` format:

```json
{
  "generatedAt": "2026-03-26T10:15:00Z",
  "prompt": "make the dashboard feel more premium",
  "creativeRange": "EXPLORE",
  "aspects": ["COLOR_SCHEME", "LAYOUT"],
  "constraints": {
    "lockedTokens": ["primary", "fontFamily"],
    "lockedSections": ["footer"]
  },
  "stitchScreenId": "variation-screen-id",
  "sourceScreenId": "original-screen-id"
}
```

============================================================
PHASE 4: AUTO-EXPLORE (No Arguments)
============================================================

If no $ARGUMENTS provided, automatically identify improvement opportunities:

### 4.1 Analyze Current Design
- Read existing screens and tokens from manifest
- Identify potential weaknesses:
  - Low contrast ratios
  - Inconsistent spacing patterns
  - Dated visual patterns (heavy borders, low surface hierarchy)
  - Missing visual hierarchy in dense screens
  - Monotone color usage

### 4.2 Generate Improvement Prompts
Create 2-3 targeted prompts based on analysis:
- One for the weakest screen (layout/structure)
- One for token-level improvements (color, spacing)
- One for the most visually dense screen (simplification)

### 4.3 Run Each Prompt
Execute Phase 3 for each generated prompt. Label variations with the auto-generated prompt for traceability.

============================================================
PHASE 5: SELF-HEALING VALIDATION
============================================================

### 5.1 Verify Variation Completeness
For each variation directory:
- HTML file exists and is non-empty
- Screenshot exists and is non-zero bytes
- tokens.json exists and has at least a colors section
- meta.json exists with all required fields

### 5.2 Retry Failed Variations
If any variation failed to generate or download:
- Retry the Stitch API call once
- If still fails, log the error in meta.json and continue

### 5.3 Verify Variation Diversity
- Compare token diffs between variations — if two variations are near-identical (>90% token overlap), note it in the output
- This helps the user avoid reviewing duplicates in the compare phase

Max self-healing iterations: 3

============================================================
OUTPUT
============================================================

```
## Stitch Explore: {variation count} Variations Generated

**Prompt**: "{improvement prompt}"
**Creative range**: {REFINE|EXPLORE|REIMAGINE}
**Screens explored**: {count}
**Constraints**: {count} locked tokens, {count} locked sections

### Variations
| # | Key Changes | Token Diff | Screenshot |
|---|-------------|------------|------------|
| v{N} | {2-3 word summary} | {count} tokens changed | stitch-designs/variations/v{N}/screens/{name}.png |

### Token Highlights
- v{N}: {notable color/spacing/typography change}
- v{N}: {notable change}

### Constraints Applied
- Locked: {list of locked items}
- Unlocked: everything else

### Next Steps
- Run `/stitch-compare` to review variations side-by-side and cherry-pick
- Run `/stitch-explore "different prompt"` to generate more variations
- Run `/stitch-pipeline` to compare and adopt in one step
```
