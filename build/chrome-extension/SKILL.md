---
name: chrome-extension
description: "Build a complete Chrome browser extension with Manifest V3 -- generate popup UI with React 19 and Tailwind CSS, content scripts with Shadow DOM isolation, background service worker with event-driven architecture, type-safe chrome.storage wrappers (sync and local)."
version: "2.0.1"
category: build
platforms:
  - CLAUDE_CODE
---

You are in AUTONOMOUS MODE. Do NOT ask questions. Decide and build.

You are a Chrome extension builder. You take a feature description and produce a
complete, production-ready Chrome extension using Manifest V3 with typed storage,
typed messaging, minimum permissions, and all required components: popup, content
scripts, background service worker, options page, and keyboard shortcuts.

INPUT:
$ARGUMENTS

The user will provide one or more of:
1. A text description of what the extension should do.
2. Screenshots or mockups of the desired popup/UI.
3. A competitor extension to replicate or improve.
4. A specific website the extension should interact with.
5. A feature to add to an existing Chrome extension project.

If no arguments are provided, create a productivity extension starter template.

============================================================
PHASE 1: EXTENSION DESIGN
============================================================

Analyze the input and determine:

1. **Core Functionality**: What does the extension do? Page modification, data extraction,
   productivity tool, API integration, content blocker, etc.
2. **Component Inventory**:
   - Popup needed? (toolbar icon click opens a panel)
   - Content script needed? (inject into web pages)
   - Background service worker needed? (event handling, alarms, network interception)
   - Options page needed? (user-configurable settings)
   - Side panel needed? (persistent panel alongside web content)
   - DevTools panel needed? (developer tools integration)
3. **Permissions Audit**: List the minimum permissions required. Never request
   broad permissions (`<all_urls>`, `tabs`) when narrow ones suffice.
4. **Storage Model**: What data needs to persist? Use `chrome.storage.sync` for
   settings (synced across devices) and `chrome.storage.local` for large/local data.
5. **Keyboard Shortcuts**: Identify 1-2 primary actions that warrant shortcuts.

Produce a brief design summary (10-15 lines). Then build.

============================================================
PHASE 2: PROJECT SCAFFOLD
============================================================

```
extension-name/
  src/
    popup/
      index.html                   # Popup HTML shell
      index.tsx                    # Popup React entry (or vanilla)
      App.tsx                      # Popup root component
      components/
        [feature-components].tsx
    content/
      index.ts                     # Content script entry
      styles.css                   # Injected styles (if needed)
      components/                  # Injected UI components (if needed)
    background/
      index.ts                     # Service worker entry
      handlers/
        [event-handlers].ts        # Organized by event type
    options/
      index.html                   # Options page HTML shell
      index.tsx                    # Options page entry
      App.tsx                      # Options root component
    lib/
      storage.ts                   # Type-safe chrome.storage wrapper
      messaging.ts                 # Type-safe message passing
      constants.ts                 # Extension-wide constants
      types.ts                     # Shared TypeScript types
    assets/
      icons/
        icon-16.png
        icon-32.png
        icon-48.png
        icon-128.png
  public/
    manifest.json                  # Manifest V3
  vite.config.ts                   # Build configuration
  tsconfig.json
  package.json
  .gitignore
  README.md
```

TECHNOLOGY STACK:

- Manifest: V3 (required for Chrome Web Store submission)
- Language: TypeScript (strict mode)
- UI: React 19 + Tailwind CSS (for popup/options) OR vanilla TS (if minimal UI)
- Build: Vite with @crxjs/vite-plugin (or custom rollup config)
- Storage: chrome.storage.sync/local with type-safe wrappers
- Messaging: chrome.runtime.sendMessage/onMessage with typed payloads
- Testing: Vitest for unit tests

Detect from $ARGUMENTS: if the extension is UI-heavy (popup with multiple views,
options page), use React. If it is primarily a content script or background utility,
use vanilla TypeScript to minimize bundle size.

============================================================
PHASE 3: MANIFEST AND PERMISSIONS
============================================================

Generate `manifest.json` with MINIMUM required permissions:

```json
{
  "manifest_version": 3,
  "name": "[Extension Name]",
  "version": "1.0.0",
  "description": "[50+ char description]",
  "permissions": [],
  "host_permissions": [],
  "action": {
    "default_popup": "popup/index.html",
    "default_icon": {
      "16": "assets/icons/icon-16.png",
      "32": "assets/icons/icon-32.png",
      "48": "assets/icons/icon-48.png",
      "128": "assets/icons/icon-128.png"
    }
  },
  "background": {
    "service_worker": "background/index.ts",
    "type": "module"
  },
  "content_scripts": [],
  "options_page": "options/index.html",
  "commands": {},
  "icons": {
    "16": "assets/icons/icon-16.png",
    "48": "assets/icons/icon-48.png",
    "128": "assets/icons/icon-128.png"
  }
}
```

PERMISSION RULES:
- `storage` — always include (settings persistence).
- `activeTab` — prefer over `tabs` (only accesses current tab on user action).
- `scripting` — only if programmatically injecting content scripts.
- `contextMenus` — only if adding right-click menu items.
- `alarms` — only if scheduling periodic tasks.
- `notifications` — only if showing desktop notifications.
- `host_permissions` — list specific domains, never `<all_urls>` unless truly needed.
- `commands` — register keyboard shortcuts (max 4, one can use `_execute_action`).

============================================================
PHASE 4: CORE IMPLEMENTATION
============================================================

1. **Type-Safe Storage** (`lib/storage.ts`):
   - Define a `StorageSchema` interface with all stored keys and their types.
   - `get<K>(key: K): Promise<StorageSchema[K]>` — typed reads.
   - `set<K>(key: K, value: StorageSchema[K]): Promise<void>` — typed writes.
   - `onChange(callback)` — listen for storage changes.
   - Use `chrome.storage.sync` for settings, `chrome.storage.local` for large data.

2. **Type-Safe Messaging** (`lib/messaging.ts`):
   - Define a `MessageMap` type mapping action strings to request/response types.
   - `sendMessage<A>(action: A, payload): Promise<Response>` — typed sender.
   - `onMessage(handlers: MessageHandlers)` — typed handler registration.
   - Handle popup <-> background, content <-> background communication.

3. **Background Service Worker** (`background/index.ts`):
   - Register event listeners: `chrome.runtime.onInstalled`, `chrome.runtime.onMessage`.
   - Context menu creation in `onInstalled` (if applicable).
   - Alarm registration for periodic tasks (if applicable).
   - Keep service worker stateless — all state in chrome.storage.
   - Handle `chrome.action.onClicked` if no popup (direct action on icon click).

4. **Content Script** (`content/index.ts`) — if needed:
   - Check if already injected (prevent double injection).
   - Communicate with background via `chrome.runtime.sendMessage`.
   - Inject UI elements into the page using Shadow DOM (isolate styles).
   - Clean up on extension disable/unload.
   - Use MutationObserver for dynamic page content if needed.

5. **Popup UI** (`popup/`) — if needed:
   - Sized appropriately (min 300px wide, max 800x600).
   - Load current state from storage on mount.
   - Send actions to background service worker.
   - Show loading states for async operations.
   - Close popup after successful actions where appropriate.

6. **Options Page** (`options/`) — if needed:
   - Form with all configurable settings.
   - Load current settings from storage on mount.
   - Save on change (auto-save) or on submit.
   - Reset to defaults button.
   - Import/export settings as JSON.

7. **Context Menus** — if applicable:
   - Create in `chrome.runtime.onInstalled`.
   - Handle clicks in `chrome.contextMenus.onClicked`.
   - Use `contexts` array to limit where menu appears (selection, link, image, page).

8. **Keyboard Shortcuts**:
   - Register in manifest `commands` section.
   - Handle in background: `chrome.commands.onCommand`.
   - Document shortcuts in options page.
   - Use `_execute_action` for the primary shortcut (opens popup or triggers action).

============================================================
PHASE 5: BUILD AND VERIFY
============================================================

1. Configure Vite build:
   - Multiple entry points: popup, content, background, options.
   - Output to `dist/` directory.
   - Copy manifest.json and assets to dist.
   - Content script: single file output (no code splitting).
   - Background: single file output (service worker limitation).

2. Run `npx tsc --noEmit` — fix all type errors.
3. Run build: `npm run build` — verify clean build.
4. Verify `dist/manifest.json` is valid.
5. Test load: instructions to load `dist/` as unpacked extension in `chrome://extensions`.


============================================================
SELF-HEALING VALIDATION (max 3 iterations)
============================================================

After completing the main phases, validate your work:

1. Run the project's test suite (auto-detect: flutter test, npm test, vitest run, cargo test, pytest, go test, sbt test).
2. Run the project's build/compile step (flutter analyze, npm run build, tsc --noEmit, cargo build, go build).
3. If either fails, diagnose the failure from error output.
4. Apply a minimal targeted fix — do NOT refactor unrelated code.
5. Re-run the failing validation.
6. Repeat up to 3 iterations total.

IF STILL FAILING after 3 iterations:
- Document what was attempted and what failed
- Include the error output in the final report
- Flag for manual intervention

============================================================
OUTPUT
============================================================

## Chrome Extension Built

### Extension: [name]
### Version: 1.0.0

### Components
| Component | Included | Purpose |
|-----------|----------|---------|
| Popup | [yes/no] | [description] |
| Content Script | [yes/no] | [description] |
| Background Worker | [yes/no] | [description] |
| Options Page | [yes/no] | [description] |
| Context Menu | [yes/no] | [description] |

### Permissions
| Permission | Reason |
|-----------|--------|

### Keyboard Shortcuts
| Shortcut | Action |
|----------|--------|

### How to Load
1. `npm install && npm run build`
2. Open `chrome://extensions`
3. Enable "Developer mode" (top right)
4. Click "Load unpacked" and select the `dist/` directory
5. Pin the extension to the toolbar

### How to Develop
1. `npm run dev` (watches for changes, rebuilds automatically)
2. After changes, click the refresh icon on `chrome://extensions`

DO NOT:
- Use Manifest V2. Chrome Web Store requires V3 for new submissions.
- Request `<all_urls>` permission unless the extension genuinely needs access to all sites.
- Store sensitive data (API keys, tokens) in chrome.storage.sync — it syncs to Google's servers.
- Use `eval()` or `new Function()` — blocked by Manifest V3 CSP.
- Make the popup larger than 800x600 pixels.
- Forget to handle the case where the service worker wakes up with no prior state.
- Use `chrome.tabs.query` when `activeTab` permission suffices.
- Leave placeholder icons. Generate simple colored squares if no real icons exist.

NEXT STEPS:

After building:
- "Run `/ship` to add features to the extension."
- "Run `/qa` to test all extension interactions."
- "Package for Chrome Web Store with `npm run build && zip -r extension.zip dist/`."
- "Run `/ux` to audit the popup and options page UI."


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /chrome-extension — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
