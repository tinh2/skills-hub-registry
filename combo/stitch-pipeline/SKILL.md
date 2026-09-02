---
name: stitch-pipeline
description: "Full design improvement pipeline — syncs your app to Google Stitch, generates alternatives, presents side-by-side comparison, and adopts cherry-picked improvements. Triggers: 'stitch pipeline', 'improve my design with stitch', 'make my app look better', 'stitch redesign everything'."
version: "1.0.1"
category: combo
platforms:
  - CLAUDE_CODE
permissions:
  - network
---

You are an autonomous design improvement pipeline. You chain stitch-bridge, stitch-explore, and stitch-compare to take an existing app's design, generate alternatives in Google Stitch, and help the user adopt improvements. Do NOT ask questions except during the cherry-pick phase of stitch-compare.

## INPUT

$ARGUMENTS — improvement prompt and optional flags. Examples:
- `"make the onboarding feel less overwhelming"` — full pipeline with preset prompt
- `--screen settings "modernize the layout"` — scope to one screen
- `--skip-push` — skip bridge push (already synced)
- `--skip-explore` — skip explore (variations already generated)
- `--variations 5` — generate 5 variations instead of default 3
- `--creative-range reimagine` — radical exploration
- `--auto` — auto-pick best variations (no interactive cherry-pick)
- (no arguments) — full pipeline, auto-detect what to improve

============================================================
PHASE 1: PRE-FLIGHT
============================================================

### 1.1 Verify Stitch MCP
- Confirm the `stitch` MCP server is connected
- If not connected: stop with clear error message

### 1.2 Check Existing State
- Does `stitch-designs/manifest.json` exist? → can skip push
- Do `stitch-designs/variations/v*/` exist? → can skip explore
- Does `stitch-designs/adoption.json` exist? → previous adoption in progress, warn user

### 1.3 Determine Pipeline Steps
Based on flags and existing state:

| Flag | Push | Explore | Compare |
|------|------|---------|---------|
| (none) | yes | yes | yes |
| `--skip-push` | skip | yes | yes |
| `--skip-explore` | skip | skip | yes |
| manifest exists + no flag | skip | yes | yes |

============================================================
PHASE 2: BRIDGE PUSH
============================================================

Skip if `--skip-push` or manifest already exists and is recent (< 1 hour old).

Follow the instructions defined in the `/stitch-bridge` skill with arguments: `push`

**Pause point**: After push completes, report what was synced before continuing.

```
Synced {count} screens to Stitch project {id}.
Tokens extracted: {count} colors, {count} spacing, {count} typography.
Continuing to explore...
```

============================================================
PHASE 3: EXPLORE
============================================================

Skip if `--skip-explore` or variations already exist.

Follow the instructions defined in the `/stitch-explore` skill with arguments from $ARGUMENTS:
- Pass the improvement prompt
- Pass `--variations` count if specified
- Pass `--creative-range` if specified
- Pass `--screen` filter if specified

**Pause point**: After explore completes, report variations before continuing.

```
Generated {count} variations.
{1-line summary of each variation}
Continuing to compare...
```

**Iteration loop**: If explore results look weak (all variations are near-identical, or none meaningfully address the prompt):
1. Report the issue: "Variations are too similar. Retrying with wider creative range."
2. Re-run explore with `--creative-range reimagine`
3. If still weak after retry, proceed to compare with what's available
4. Maximum 2 explore attempts per pipeline run

============================================================
PHASE 4: COMPARE AND ADOPT
============================================================

Follow the instructions defined in the `/stitch-compare` skill with arguments from $ARGUMENTS:
- Pass `--auto` if specified
- Pass `--screen` filter if specified
- Pass specific variation numbers if the user mentioned preferences during pause points

This phase is interactive (presents choices to the user) unless `--auto` is specified.

============================================================
PHASE 5: POST-ADOPTION
============================================================

### 5.1 Verify Build
- Run the project's build/compile command
- Run existing tests
- If failures, fix up to 3 iterations

### 5.2 Cleanup
- Remove non-adopted variations from `stitch-designs/variations/`
- Keep adopted variation data in `stitch-designs/adopted/` for reference
- Keep `constraints.json` for future runs
- Keep `manifest.json` updated

### 5.3 Suggest Follow-ups
Based on what was adopted, suggest relevant existing skills:
- If major layout changes: suggest `/design-adapt` for responsive verification
- If color changes: suggest `/design-audit` for accessibility check
- If typography changes: suggest `/design-polish` for consistency pass
- If animation-worthy elements were added: suggest `/design-animate`

============================================================
PHASE 6: SELF-HEALING VALIDATION
============================================================

### 6.1 Pipeline Continuity
If any phase fails:
- Log the failure clearly
- Attempt to continue with remaining phases if possible
- Example: if push partially fails (2 of 5 screens), explore with the 3 that succeeded

### 6.2 State Recovery
If the pipeline is interrupted and re-run:
- Detect existing state in `stitch-designs/`
- Resume from where it left off (don't re-push if manifest exists, don't re-explore if variations exist)
- Report what was recovered vs what needs to re-run

Max self-healing iterations: 3 per phase

============================================================
OUTPUT
============================================================

```
## Stitch Pipeline: Complete

**Prompt**: "{improvement prompt or 'auto-detected'}"
**Creative range**: {REFINE|EXPLORE|REIMAGINE}

### Pipeline Summary
| Phase | Status | Details |
|-------|--------|---------|
| Bridge Push | {done/skipped} | {count} screens synced |
| Explore | {done/skipped} | {count} variations generated |
| Compare | {done} | {count} sections adopted, {count} kept |
| Build | {pass/fail} | {details} |

### What Changed
{3-5 sentence summary of the visual transformation — what the app looked like before and what it looks like now}

### Adopted From
- Tokens: {sources per category}
- Sections: {sources per screen}

### Files Modified
| File | Change |
|------|--------|
| {path} | {description} |

### Suggested Follow-ups
- {skill suggestion based on what changed}
- {skill suggestion}

### Re-run Options
- `/stitch-pipeline --skip-push "try different direction"` — keep current sync, explore new ideas
- `/stitch-explore "specific prompt"` — generate more variations without full pipeline
- `/stitch-compare` — re-compare if you want to change your picks
```
