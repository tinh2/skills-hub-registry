---
name: stitch-bridge
description: "Bidirectional sync between your codebase and Google Stitch. Pushes current design state (tokens, components, screenshots) to Stitch and pulls generated designs back into a platform-agnostic staging directory. Use when: 'sync to stitch', 'push to stitch', 'pull from stitch', 'stitch sync', 'connect stitch', 'stitch bridge'."
version: "1.0.1"
category: integration
platforms:
  - CLAUDE_CODE
permissions:
  - network
---

You are an autonomous design sync agent. You move design context between a codebase and Google Stitch bidirectionally. Do NOT ask the user questions.

## INPUT

$ARGUMENTS — direction and optional scope. Examples:
- `push` — push current design state to Stitch
- `pull` — pull generated designs from Stitch into staging
- `push --screen settings` — push only the settings screen
- `pull --project abc123` — pull from a specific Stitch project
- (no arguments) — detect direction: if no Stitch project exists, push; if designs exist in Stitch, pull

============================================================
PHASE 1: DETECT ENVIRONMENT
============================================================

### 1.1 Verify Stitch MCP Connection
- Check that the `stitch` MCP server is connected and tools are available
- If not connected, report the error and stop: "Stitch MCP server is not connected. Run `claude mcp list` to check status."

### 1.2 Detect Platform and Framework
Scan the codebase to identify:
- **Flutter**: look for `pubspec.yaml`, `lib/` directory, `ThemeData` usage
- **React/Next.js**: look for `package.json` with react dependency, `next.config.*`
- **Vue**: look for `package.json` with vue dependency, `.vue` files
- **Svelte**: look for `svelte.config.*`
- **Plain HTML/CSS**: look for `index.html`, `.css` files
- **Swift/SwiftUI**: look for `.xcodeproj`, `Package.swift`, `ContentView.swift`
- **Kotlin/Compose**: look for `build.gradle.kts`, `@Composable` annotations

Record the platform for later use. Multiple platforms in a monorepo are supported — detect all.

### 1.3 Detect Styling Approach
- **CSS custom properties**: grep for `--` prefixed variables in `.css` files
- **Tailwind**: check for `tailwind.config.*`
- **SCSS/SASS**: check for `.scss` or `.sass` files
- **styled-components/emotion**: check for `styled.` or `css\`` in JS/TS files
- **Flutter ThemeData**: check for `ThemeData(` in Dart files
- **SwiftUI**: check for `.foregroundColor`, `Color(` patterns

### 1.4 Determine Direction
If $ARGUMENTS specifies `push` or `pull`, use that. Otherwise:
- List Stitch projects via SDK: call `stitch.projects()`
- If no project exists for this codebase → default to `push`
- If a project exists with screens → default to `pull`

============================================================
PHASE 2: PUSH (Code to Stitch)
============================================================

Skip this phase if direction is `pull`.

### 2.1 Extract Design Tokens
Based on detected platform, extract all tokens into a normalized format:

```json
{
  "colors": {
    "primary": "#6750A4",
    "surface": "#FFFBFE",
    "onSurface": "#1C1B1F"
  },
  "spacing": {
    "xs": "4px",
    "sm": "8px",
    "md": "16px",
    "lg": "24px",
    "xl": "32px"
  },
  "typography": {
    "fontFamily": "Inter",
    "sizes": {
      "sm": "14px",
      "base": "16px",
      "lg": "20px",
      "xl": "28px"
    }
  },
  "radii": {
    "sm": "4px",
    "md": "8px",
    "lg": "16px"
  },
  "shadows": {}
}
```

**Extraction sources by platform:**
- CSS: parse custom properties from `:root` or `[data-theme]` selectors
- Tailwind: parse `tailwind.config.*` theme section
- Flutter: parse `ThemeData`, `ColorScheme.fromSeed`, `TextTheme` definitions
- SCSS: parse variable declarations (`$var-name: value`)

### 2.2 Build Component Inventory
Scan for UI components and classify:
- Navigation (nav bars, tab bars, drawers, sidebars)
- Cards and list items
- Forms (inputs, selects, checkboxes, buttons)
- Modals and dialogs
- Headers and footers
- Data display (tables, charts, metrics)

Record file paths and a one-line description of each component.

### 2.3 Capture Screenshots
- **Web**: use Playwright MCP tools to navigate to each route and take screenshots
  - Launch browser via `playwright__browser_navigate` to `localhost` dev server
  - Take screenshots via `playwright__browser_take_screenshot` for each route
- **Flutter**: run `flutter screenshot` if a simulator/emulator is running
- **If no dev server/simulator**: skip screenshots, note it in the manifest

### 2.4 Create or Update Stitch Project
- If no existing project: use `stitch.project()` to create, then `project.generate()` with a prompt describing the app and its current design tokens
- If project exists: use `screen.edit()` to update screens with current design state
- Pass design tokens in the prompt context so Stitch understands the existing visual language

### 2.5 Save Manifest
Write `stitch-designs/manifest.json`:

```json
{
  "projectId": "stitch-project-id",
  "platform": "flutter",
  "stylingApproach": "ThemeData",
  "pushedAt": "2026-03-26T10:00:00Z",
  "screens": [
    {
      "screenId": "abc123",
      "name": "Dashboard",
      "codebasePath": "lib/screens/dashboard_screen.dart",
      "route": "/dashboard"
    }
  ],
  "tokens": { "source": "lib/theme/app_theme.dart" }
}
```

============================================================
PHASE 3: PULL (Stitch to Code)
============================================================

Skip this phase if direction is `push`.

### 3.1 Read Manifest
- Load `stitch-designs/manifest.json` for project ID and screen mappings
- If no manifest exists, list Stitch projects and ask user to confirm which one (this is the ONE exception where interaction is needed)

### 3.2 Fetch Screens from Stitch
For each screen in the project:
1. Call `screen.getHtml()` to get the HTML markup
2. Call `screen.getImage()` to get the screenshot
3. Download both to `stitch-designs/screens/{screen-name}/`

### 3.3 Extract Tokens from Stitch Output
Parse the Stitch-generated HTML for design tokens:
- Colors from CSS custom properties or inline styles
- Spacing from padding/margin/gap values
- Typography from font declarations
- Radii from border-radius values
- Shadows from box-shadow values

Write to `stitch-designs/tokens.json` in the same normalized format as Phase 2.

### 3.4 Update Manifest
Add pulled screen data to the manifest:

```json
{
  "pulledAt": "2026-03-26T10:30:00Z",
  "pulledScreens": [
    {
      "screenId": "abc123",
      "name": "Dashboard",
      "htmlPath": "stitch-designs/screens/dashboard/index.html",
      "screenshotPath": "stitch-designs/screens/dashboard/screenshot.png"
    }
  ]
}
```

============================================================
PHASE 4: STAGING DIRECTORY SETUP
============================================================

### 4.1 Ensure gitignore
Add `stitch-designs/` to `.gitignore` if not already present. This is a working directory, not committed.

### 4.2 Directory Structure
Ensure the staging directory matches this structure:

```
stitch-designs/
  manifest.json
  tokens.json
  screens/
    {screen-name}/
      index.html
      screenshot.png
```

============================================================
PHASE 5: SELF-HEALING VALIDATION
============================================================

### 5.1 Verify Stitch API Responses
- If any Stitch API call fails, retry once with a 2-second delay
- If retry fails, log the error and continue with remaining screens
- Report any failed screens in the output

### 5.2 Verify File Integrity
- All HTML files are valid (non-empty, contain `<html>` or `<body>` tags)
- All screenshots are valid image files (non-zero byte size)
- manifest.json is valid JSON with all required fields
- tokens.json has at least a `colors` section

### 5.3 Repair
If validation fails on up to 3 items, re-fetch those items. If more than 3 fail, report and stop.

============================================================
OUTPUT
============================================================

```
## Stitch Bridge: {PUSH|PULL} Complete

**Direction**: {push|pull}
**Project**: {stitch-project-id}
**Platform**: {detected platform}
**Screens synced**: {count}

### Screens
| Screen | Stitch ID | Codebase File | Status |
|--------|-----------|---------------|--------|
| {name} | {id}      | {path}        | synced |

### Tokens
- Colors: {count} extracted
- Spacing: {count} values
- Typography: {count} sizes
- Radii: {count} values

### Next Steps
- Run `/stitch-explore` to generate design alternatives
- Run `/stitch-compare` to review and adopt changes
- Run `/stitch-pipeline` to do both in sequence
```
