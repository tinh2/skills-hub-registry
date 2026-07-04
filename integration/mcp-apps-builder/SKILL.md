---
name: mcp-apps-builder
description: "Build MCP Apps — the interactive HTML UI primitive introduced in the 2026-07-28 MCP specification. Scaffolds UI templates, wires the JSON-RPC back-channel, declares tool manifests, and validates against the conformance suite. Use when adding visual interfaces (forms, data previews, approval flows) to an existing MCP server."
version: "1.0.0"
category: integration
platforms:
  - CLAUDE_CODE
---

You are an MCP Apps implementation agent. Build interactive HTML UI interfaces for the target MCP server using the 2026-07-28 MCP specification (SEP-1865). Do NOT ask the user questions — read the server, identify tools that benefit from a UI, and implement them.

TARGET:
$ARGUMENTS

============================================================
BACKGROUND — what MCP Apps is
============================================================

MCP Apps (SEP-1865) lets MCP servers ship interactive HTML interfaces that
hosts render in sandboxed iframes. Key properties:

1. **Tool-declared templates** — tools list UI templates in their manifest so
   hosts can prefetch, cache, and security-review them before anything runs.

2. **Same JSON-RPC back-channel** — all UI-initiated actions go through the
   identical `tools/call` consent and audit path as direct agent invocations.
   There is no new permission surface.

3. **Explicit sandbox** — `sandbox` attribute on the UI declaration controls
   exactly which iframe capabilities are granted. Principle of least privilege.

4. **Independent rendering** — hosts that don't support MCP Apps ignore the
   `ui` field and fall back to text output. MCP Apps is an enhancement, not a
   hard dependency.

Use MCP Apps for:
- Configuration forms with many parameters
- Data previews where results should be scanned before an action is confirmed
- Human-in-the-loop approval flows that deserve a real UI element

============================================================
PHASE 1: AUDIT — which tools benefit from a UI
============================================================

1. READ THE SERVER
   - Identify the SDK (TypeScript or Python)
   - List all registered tools with their inputSchema and description
   - Count parameters per tool

2. SCORE EACH TOOL FOR UI SUITABILITY
   Tools score high if they have:
   - 4+ parameters (form makes them manageable)
   - Return structured data (table, chart, list) the user needs to scan
   - A confirmation step before a destructive or irreversible action
   - Enum parameters where radio/select beats free-text

3. SELECT CANDIDATES
   Recommend the top 1–3 tools. Do not implement more than 3 in one pass —
   MCP Apps UIs require testing and MCP Apps support is not universal yet.

Output the audit as:
```
UI CANDIDATES
1. <tool-name> — <reason> — priority: HIGH / MEDIUM / LOW
2. <tool-name> — <reason> — priority: HIGH / MEDIUM / LOW
```

============================================================
PHASE 2: SCAFFOLD THE UI TEMPLATES
============================================================

For each selected tool:

1. CREATE THE DIRECTORY
   - TypeScript: `src/ui/<tool-slug>/`
   - Python: `ui/<tool-slug>/`

2. WRITE index.html
   Requirements:
   - Self-contained (inline CSS and JS — no external dependencies)
   - Responsive: uses relative units, flexbox or grid
   - Theme-aware: `prefers-color-scheme` dark/light via CSS variables
   - Zero runtime frameworks — plain HTML + CSS + vanilla JS only
   - Accessible: all inputs have visible labels, `aria-label` on icon-only buttons,
     48px minimum touch targets, focus-visible ring on interactive elements

   Template:
   ```html
   <!doctype html>
   <html lang="en">
   <head>
     <meta charset="utf-8" />
     <meta name="viewport" content="width=device-width, initial-scale=1" />
     <title><TOOL_NAME></title>
     <style>
       :root {
         --bg: #ffffff;
         --fg: #111827;
         --border: #e5e7eb;
         --primary: #7c3aed;
         --primary-fg: #ffffff;
         --radius: 8px;
       }
       @media (prefers-color-scheme: dark) {
         :root {
           --bg: #0f0f0f;
           --fg: #f3f4f6;
           --border: #27272a;
         }
       }
       * { box-sizing: border-box; margin: 0; padding: 0; }
       body { background: var(--bg); color: var(--fg); font-family: system-ui, sans-serif;
              padding: 16px; min-height: 100vh; }
       form { display: flex; flex-direction: column; gap: 12px; max-width: 480px; }
       label { font-size: 14px; font-weight: 500; }
       input, select, textarea {
         width: 100%; padding: 10px 12px; border: 1px solid var(--border);
         border-radius: var(--radius); background: var(--bg); color: var(--fg);
         font-size: 14px; min-height: 48px;
       }
       input:focus-visible, select:focus-visible, textarea:focus-visible {
         outline: 2px solid var(--primary); outline-offset: 2px;
       }
       button[type="submit"] {
         background: var(--primary); color: var(--primary-fg);
         border: none; border-radius: var(--radius);
         padding: 12px 20px; font-size: 14px; font-weight: 600;
         cursor: pointer; min-height: 48px;
       }
       button[type="submit"]:hover { opacity: 0.9; }
       button[type="submit"]:focus-visible { outline: 2px solid var(--primary); outline-offset: 2px; }
       #status { font-size: 13px; margin-top: 8px; }
       #result { margin-top: 16px; padding: 12px; border: 1px solid var(--border);
                 border-radius: var(--radius); font-family: monospace; font-size: 13px;
                 white-space: pre-wrap; display: none; }
     </style>
   </head>
   <body>
     <!-- FORM: one <label>+<input> pair per tool parameter -->
     <form id="main-form" aria-label="<TOOL_NAME> configuration">
       <!-- INSERT FIELDS HERE -->
       <button type="submit">Run <TOOL_NAME></button>
       <p id="status" aria-live="polite"></p>
     </form>
     <div id="result" role="log" aria-live="polite" aria-label="Tool result"></div>
     <script>
       const MCP_HOST = window.parent;

       document.getElementById("main-form").addEventListener("submit", async (e) => {
         e.preventDefault();
         document.getElementById("status").textContent = "Running…";

         const args = {}; // collect form values here

         MCP_HOST.postMessage({
           jsonrpc: "2.0",
           id: crypto.randomUUID(),
           method: "tools/call",
           params: { name: "<TOOL_NAME>", arguments: args }
         }, "*");
       });

       window.addEventListener("message", (e) => {
         if (e.data?.result) {
           const el = document.getElementById("result");
           el.style.display = "block";
           el.textContent = JSON.stringify(e.data.result, null, 2);
           document.getElementById("status").textContent = "Done.";
         } else if (e.data?.error) {
           document.getElementById("status").textContent =
             "Error: " + e.data.error.message;
         }
       });
     </script>
   </body>
   </html>
   ```

3. FILL IN TOOL-SPECIFIC FIELDS
   For each parameter in the tool's inputSchema, add a labeled input:
   - `string` → `<input type="text">`
   - `number` / `integer` → `<input type="number">`
   - `boolean` → `<input type="checkbox">`
   - `string` with `enum` → `<select>` with one `<option>` per enum value
   - `string` with long description → `<textarea rows="4">`
   - Required parameters get `required` attribute on the input

============================================================
PHASE 3: DECLARE THE UI IN THE TOOL MANIFEST
============================================================

1. TYPESCRIPT — update server.tool() call
   ```typescript
   server.tool(
     "deploy_preview",
     "Deploy a preview environment.",
     {
       branch: z.string().describe("Git branch to deploy"),
     },
     async ({ branch }) => { /* handler */ },
     {
       ui: {
         template: "deploy-preview-ui",
         entrypoint: "index.html",
         sandbox: ["allow-scripts", "allow-same-origin"],
       },
     }
   );
   ```

2. PYTHON — update @server.tool() decorator
   ```python
   @server.tool(
     ui={
       "template": "deploy-preview-ui",
       "entrypoint": "index.html",
       "sandbox": ["allow-scripts", "allow-same-origin"],
     }
   )
   async def deploy_preview(branch: str) -> list[TextContent]:
       """Deploy a preview environment."""
       ...
   ```

3. REGISTER TEMPLATES IN SERVER INIT
   TypeScript:
   ```typescript
   server.registerUiTemplate("deploy-preview-ui", {
     path: "./src/ui/deploy-preview",
   });
   ```
   Python:
   ```python
   server.register_ui_template("deploy-preview-ui", path="./ui/deploy-preview")
   ```

4. VERIFY MANIFEST
   The `tools/list` response must include the `ui` field for each tool that has
   a registered template. Verify with:
   ```shell
   curl -s -X POST http://localhost:3000/mcp \
     -H "Content-Type: application/json" \
     -H "Mcp-Method: tools/list" \
     -H "Mcp-Name: list" \
     -H "MCP-Protocol-Version: 2026-07-28" \
     -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' \
     | jq '.result.tools[] | {name, ui}'
   ```

============================================================
PHASE 4: WIRE SECURITY
============================================================

1. SANDBOX ATTRIBUTE SELECTION
   Start with the most restrictive set and add only what's needed:
   - `allow-scripts` — required for any JS (always include)
   - `allow-same-origin` — required if the UI fetches from the same server
   - `allow-forms` — only if the UI submits to an external URL (avoid)
   - NEVER add `allow-top-navigation` or `allow-popups` unless there is a
     specific documented reason reviewed by a security engineer

2. ORIGIN VALIDATION ON MESSAGE EVENTS
   In the UI's `window.addEventListener("message", ...)` handler, always
   validate the origin before acting on the message:
   ```javascript
   window.addEventListener("message", (e) => {
     // Only accept messages from the parent host — not from any origin
     if (e.origin !== window.location.origin && e.source !== window.parent) return;
     // ... handle result
   });
   ```

3. CONTENT SECURITY POLICY
   Add a `<meta>` CSP header to every UI template:
   ```html
   <meta http-equiv="Content-Security-Policy"
         content="default-src 'none'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';">
   ```
   This prevents the UI from loading external scripts or making cross-origin
   requests — the sandbox attribute alone is not sufficient.

============================================================
PHASE 5: TEST AND VALIDATE
============================================================

1. HOST RENDERING TEST
   Open the host that supports MCP Apps (e.g., Claude Desktop with MCP Apps
   support enabled in settings). Invoke the tool via the agent. The host should
   render the iframe instead of printing the JSON args.

2. FORM SUBMISSION TEST
   Fill in the form and submit. Verify:
   - The `tools/call` postMessage is sent with the correct arguments
   - The host returns the result message
   - The result renders in `#result`
   - Error messages render in `#status`

3. FALLBACK TEST
   Connect a client that does NOT support MCP Apps (older client or plain API).
   Invoke the tool normally. Verify it still works via the standard text output —
   the `ui` field on the manifest should be silently ignored.

4. CONFORMANCE SUITE
   ```shell
   npx @modelcontextprotocol/conformance run \
     --server http://localhost:3000/mcp \
     --suite mcp-apps
   ```
   Fix any failures before committing.

5. ACCESSIBILITY CHECK
   Open each UI template in a browser and verify:
   - All inputs are focusable and have visible focus indicators
   - All inputs have associated labels (click label → focuses input)
   - All interactive elements are reachable by keyboard alone
   - `aria-live` regions announce result and error states

============================================================
OUTPUT
============================================================

### MCP Apps Build Complete

**Audit**
- Tools evaluated: [count]
- Tools selected for MCP Apps UI: [list]

**Templates built**
- [tool-name]: [path/to/ui] — [key UI decisions: form type, theme support, etc.]

**Manifest declarations**
- [count] tools updated with `ui` field
- Sandbox policy: [list of sandbox attributes used and why]

**Security**
- CSP meta tag: [added / not needed — stdio only]
- Origin validation: [added / not applicable]

**Tests**
- Host rendering: [pass / skip — no MCP Apps host available]
- Form submission: [pass / skip]
- Fallback (no-UI client): [pass / skip]
- Conformance suite: [pass / fail / skip]
- Accessibility: [pass / issues found: list]

**Next steps**
- Ship to users on an MCP Apps-compatible host (Claude Desktop 1.4+, or any host that implements SEP-1865)
- Monitor host adoption — MCP Apps renders only if the host supports it; tool works for all clients regardless
