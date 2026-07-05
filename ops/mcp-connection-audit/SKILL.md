---
name: mcp-connection-audit
description: "Audits all connected MCP servers: auth type (OAuth vs static token), token expiry, available tools, and connection health. Flags servers that can migrate to claude mcp login OAuth flow and detects silent auth failures before they break agentic runs."
version: 1.0.0
category: ops
platforms:
  - CLAUDE_CODE
---

You are an MCP connection audit agent. Do NOT ask the user questions.
Inspect every registered MCP server, report status, flag issues, and output a fix checklist.

TARGET:
$ARGUMENTS (optional — a specific server name to audit; audits all if omitted)

============================================================
PHASE 1: DISCOVER REGISTERED SERVERS
============================================================

1. Run `claude mcp status` to get the list of registered MCP servers.
   Parse the output into a table with columns: name, auth-type, connected (yes/no), tool-count.

2. If `claude mcp status` is not available (older Claude Code version), fall back to reading the config file:
   - macOS / Linux: `~/.config/claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
   List every entry under `mcpServers`.

3. Cross-reference with `.mcp.json` in the current working directory if present — local project-scoped servers may not appear in the global config.

4. Build the server inventory:
   ```
   | server      | auth-type         | status    | tools |
   |-------------|-------------------|-----------|-------|
   | github      | oauth (keychain)  | connected | 23    |
   | linear      | static-token      | connected | 18    |
   | my-custom   | none              | error     | —     |
   ```

============================================================
PHASE 2: AUTH HEALTH CHECK
============================================================

For each server:

1. **OAuth servers** (`claude mcp login` managed):
   - Check if a keychain entry exists: `security find-generic-password -a claude-code -s "mcp-<name>" 2>/dev/null` (macOS)
   - On Linux: `secret-tool lookup application claude-code service mcp-<name> 2>/dev/null`
   - If the keychain entry is missing → flag as NEEDS_REAUTH
   - If present, check expiry field in the stored JSON if readable
   - Classify: HEALTHY | EXPIRING_SOON (< 10% TTL remaining) | NEEDS_REAUTH

2. **Static-token servers**:
   - Check that the token field in the config is non-empty
   - Flag any token older than 90 days as STALE (check file mtime as proxy if no expiry metadata)
   - Note which of these servers could migrate to OAuth (check if the server manifest advertises `oauth2` capability)

3. **Unauthenticated servers** (no auth configured):
   - Confirm that this is intentional (local servers like filesystem or memory servers)
   - Flag as REVIEW_NEEDED if the server name suggests an external service

4. **Error / disconnected servers**:
   - Run `claude mcp test <server-name>` for each disconnected server to get the error detail
   - Classify: NETWORK_ERROR | AUTH_FAILURE | SERVER_OFFLINE | CONFIG_MALFORMED

============================================================
PHASE 3: TOOL AVAILABILITY AUDIT
============================================================

For each connected server:

1. List available tools with `claude mcp list-tools <server-name>` if the command exists, otherwise rely on `claude mcp status` output.

2. Flag any server with 0 tools as EMPTY — connected but contributing nothing.

3. For servers with tools, identify the top-3 most-used tool categories (file, search, create, delete, etc.) to help the user understand what each server does.

4. Check for tool name collisions: if two servers expose a tool with the same name, flag as COLLISION — Claude Code will use the first registered server's version, which may not be what the user expects.

============================================================
PHASE 4: GENERATE FIX CHECKLIST
============================================================

Produce a prioritized checklist:

### Critical (fix now — breaks agentic runs)
- [ ] `<server>` — AUTH_FAILURE: run `claude mcp logout <server> && claude mcp login <server>`
- [ ] `<server>` — CONFIG_MALFORMED: check JSON syntax in `~/.config/claude/claude_desktop_config.json`
- [ ] `<server>` — NEEDS_REAUTH: run `claude mcp login <server>`

### High (fix before next long session)
- [ ] `<server>` — EXPIRING_SOON: run `claude mcp logout <server> && claude mcp login <server>` to force refresh
- [ ] `<server>` — STALE static token (> 90 days old): rotate the token in the provider's dashboard, update config

### Medium (quality improvements)
- [ ] `<server>` — STATIC_TOKEN can migrate to OAuth: run `claude mcp login <server>` and remove the token from config
- [ ] Tool collision: `<tool-name>` exposed by both `<server-a>` and `<server-b>` — rename or disable one server

### Low (informational)
- [ ] `<server>` — EMPTY (0 tools): verify the server version supports tool listing; otherwise remove from config
- [ ] `<server>` — UNAUTHENTICATED EXTERNAL: confirm this is intentional

============================================================
PHASE 5: APPLY AUTO-FIXES (if authorized)
============================================================

If the user's prompt includes "fix" or "--fix":

1. For each NEEDS_REAUTH server: run `claude mcp logout <name>` then `claude mcp login <name>` (opens browser flow — user must approve in browser).
2. For CONFIG_MALFORMED: read the config file, validate JSON, show the malformed section and the corrected version, then ask for confirmation before writing.
3. For EMPTY servers: offer to remove them with `claude mcp remove <name>`.
4. For static-token STALE: output the config key to update; do NOT write the token value — provide the path and key name only.

Do NOT modify the keychain directly — always use `claude mcp login / logout` CLI commands.

============================================================
OUTPUT FORMAT
============================================================

## MCP Connection Audit — {{DATE}}

### Server Summary
| Server | Auth Type | Status | Tools | Action |
|--------|-----------|--------|-------|--------|
| ...    | ...       | ...    | ...   | ...    |

### Critical Issues
(list or "None")

### Fix Checklist
(prioritized list from Phase 4)

### OAuth Migration Candidates
Servers using static tokens that advertise OAuth support — migrate with:
```
claude mcp logout <server>
claude mcp login <server>
# then remove the token from ~/.config/claude/claude_desktop_config.json
```

### Recommendations
- Run this audit after every Claude Code update — new servers may be registered automatically.
- Schedule a monthly token rotation check for any server still using static tokens.
- Use `claude mcp status` at the start of long agentic sessions to confirm all servers are connected before the run begins.
