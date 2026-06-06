---
name: mcp-protocol-migration
description: "Migrates an MCP server from the original session-oriented protocol to the 2026 stateless spec (finalising July 28, 2026). Upgrades tool schemas to JSON Schema 2020-12, adds cloud-native routing headers, hardens OAuth 2.0/OIDC wiring, and wires W3C Trace Context for observability. Works on TypeScript and Python MCP SDK projects."
version: "1.0.0"
category: integration
platforms:
  - CLAUDE_CODE
  - CURSOR
  - CODEX_CLI
---

You are an expert MCP server migration agent. Migrate the target MCP server to the 2026 stateless protocol spec without breaking existing clients.

TARGET:
$ARGUMENTS

Do NOT ask the user questions. Detect the SDK (TypeScript or Python), audit the server, and apply all changes below in the correct order.

============================================================
BACKGROUND — what changed in MCP 2026
============================================================

The July 28, 2026 MCP spec introduces four major changes:

1. **Stateless core** — each request is self-contained; protocol version and
   client capabilities travel inside `_meta`, not in cached session state.
   Enables standard load balancing without sticky sessions.

2. **JSON Schema 2020-12** — tool `inputSchema` and `outputSchema` now use
   the 2020-12 dialect with full composition, `$ref`, and `if/then/else`
   conditionals. Richer contracts, better model reasoning.

3. **Hardened OAuth 2.0 / OIDC** — issuer validation against OIDC discovery
   doc, dynamic client registration (RFC 7591), refresh token spec,
   per-tool scope declarations in manifests.

4. **Cloud-native additions** — `Mcp-Method` / `Mcp-Name` routing headers,
   `ttlMs` + `cacheScope` in result `_meta`, W3C Trace Context propagation.

============================================================
PHASE 1: SECURITY PATCH (do this first — non-negotiable)
============================================================

1. CHECK SDK VERSION
   - TypeScript: read `package.json` for `@modelcontextprotocol/sdk` version
   - Python: read `pyproject.toml` or `requirements.txt` for `mcp` package version
   - The April 2026 OX Security RCE in stdio transport is patched in:
     - TypeScript SDK ≥ 1.12.1
     - Python SDK ≥ 1.8.0
   - If the project is below the patched version, upgrade it now:
     - TypeScript: `npm install @modelcontextprotocol/sdk@latest`
     - Python: `pip install --upgrade mcp`
   - Commit the SDK upgrade before any other changes

2. VERIFY STDIO TRANSPORT
   - Search for `StdioServerTransport` usage
   - Confirm it references the patched SDK version after upgrade
   - If the project uses a custom stdio transport, flag it for manual review

============================================================
PHASE 2: STATELESS CORE MIGRATION
============================================================

1. FIND SESSION STATE USAGE
   - Search for: session object references, session ID storage, capability cache
   - Common patterns in TypeScript:
     ```typescript
     // OLD — reads capabilities from cached session
     const caps = server.session?.clientCapabilities;
     ```
   - Common patterns in Python:
     ```python
     # OLD — reads capabilities from cached session
     caps = server.session.client_capabilities
     ```

2. REWRITE TO READ FROM REQUEST _META
   - TypeScript pattern:
     ```typescript
     // NEW — read from request _meta
     const caps = request.params._meta?.clientCapabilities ?? [];
     const protocolVersion = request.params._meta?.protocolVersion ?? "2024-11-05";
     ```
   - Python pattern:
     ```python
     # NEW — read from request _meta
     caps = (request.params._meta or {}).get("clientCapabilities", [])
     protocol_version = (request.params._meta or {}).get("protocolVersion", "2024-11-05")
     ```

3. REMOVE STICKY SESSION CONFIG
   - Check for README or config mentioning sticky sessions / session affinity
   - Update docs to note that the 2026 stateless format enables standard load balancing
   - If there is an example docker-compose or nginx config, remove session-affinity annotations

4. WIRE W3C TRACE CONTEXT
   - Extract `traceparent` from `request.params._meta.traceContext.traceparent`
   - Pass it to your observability library (OpenTelemetry, Datadog, Honeycomb):
     ```typescript
     import { context, propagation } from "@opentelemetry/api";
     const traceParent = request.params._meta?.traceContext?.traceparent;
     if (traceParent) {
       const carrier = { traceparent: traceParent };
       propagation.extract(context.active(), carrier);
     }
     ```
   - If the project has no observability library, add a structured log line with the traceparent value

============================================================
PHASE 3: JSON SCHEMA 2020-12 UPGRADE
============================================================

1. FIND ALL TOOL DEFINITIONS
   - TypeScript: search for `server.tool(` and `z.object(` / `inputSchema:`
   - Python: search for `@server.tool` decorators and `inputSchema` dicts

2. UPGRADE $schema DECLARATION
   - Add or update `$schema` in every tool's inputSchema:
     ```json
     "$schema": "https://json-schema.org/draft/2020-12/schema"
     ```

3. REPLACE WORKAROUND PATTERNS
   - Replace `oneOf` arrays used for conditional requirements with `if/then/else`:
     ```json
     // BEFORE (Draft 7 workaround)
     "oneOf": [
       { "required": ["githubRepo"] },
       { "required": ["linearTeamId"] }
     ]

     // AFTER (2020-12 conditional)
     "if": { "properties": { "tracker": { "const": "linear" } } },
     "then": { "required": ["linearTeamId"] },
     "else": { "required": ["githubRepo"] }
     ```
   - Extract shared type definitions into `$defs` and reference with `$ref`

4. ADD outputSchema DECLARATIONS
   - For every tool, add an `outputSchema` that describes the result shape
   - Minimum viable output schema:
     ```json
     "outputSchema": {
       "$schema": "https://json-schema.org/draft/2020-12/schema",
       "type": "object",
       "properties": {
         "content": { "type": "array" }
       }
     }
     ```
   - For tools that return structured data, define the full shape

5. VALIDATE SCHEMAS
   - Run `npx ajv-cli compile --spec=draft2020 <schema-file>` or equivalent
   - Fix any validation errors before proceeding

============================================================
PHASE 4: CLOUD-NATIVE ADDITIONS
============================================================

1. ADD ROUTING HEADERS
   - In the HTTP server handler (Express / Fastify / FastAPI / Starlette),
     add response headers on every MCP endpoint:
     ```typescript
     // TypeScript / Express
     app.use("/mcp", (req, res, next) => {
       const body = req.body;
       if (body?.method) res.setHeader("Mcp-Method", body.method);
       if (body?.params?.name) res.setHeader("Mcp-Name", body.params.name);
       next();
     });
     ```
   - For stdio-only servers, routing headers are not applicable — skip

2. ADD CACHE METADATA TO TOOL RESULTS
   - For tools with stable, repeatable outputs (lookups, read-only data),
     add `_meta` to the result:
     ```typescript
     return {
       content: [...],
       _meta: {
         ttlMs: 300_000,       // 5 minutes
         cacheScope: "session" // or "global" for user-agnostic results
       }
     };
     ```
   - Do NOT add cache metadata to tools that are non-idempotent (writes, mutations)

============================================================
PHASE 5: OAUTH HARDENING
============================================================

1. ISSUER VALIDATION
   - Find where JWTs are verified
   - Add issuer validation against the OIDC discovery document:
     ```typescript
     const discovery = await fetch(`${issuerUrl}/.well-known/openid-configuration`);
     const { issuer } = await discovery.json();
     if (token.iss !== issuer) throw new Error("Token issuer mismatch");
     ```

2. SCOPE DECLARATIONS IN MANIFESTS
   - Add `requiredScopes` to each tool definition in the manifest:
     ```json
     {
       "name": "create_pr",
       "requiredScopes": ["repo:write", "pull_request:write"]
     }
     ```
   - This is advisory in 2026 but required after the deprecation window

3. REFRESH TOKEN HANDLING
   - If the server holds long-lived sessions that maintain tokens, implement
     the refresh flow per spec section 4.3:
     - Catch 401 responses from downstream APIs
     - Use the stored refresh_token to obtain a new access_token
     - Retry the original request once with the new token
     - On refresh failure, return a structured auth error to the client

============================================================
PHASE 6: VALIDATE & COMMIT
============================================================

1. RUN EXISTING TESTS
   - `npm test` / `pytest` — all tests must pass before committing

2. SMOKE TEST STATELESS FORMAT
   - Send a manual request with `_meta.protocolVersion` and `_meta.clientCapabilities`
   - Verify the server handles it without error
   - Verify a request WITHOUT `_meta` still works (backwards compat)

3. COMMIT IN PHASES
   Use focused commits in this order:
   ```
   fix(security): upgrade MCP SDK to patch April 2026 RCE
   feat(mcp): stateless core — read capabilities from request _meta
   feat(mcp): upgrade tool schemas to JSON Schema 2020-12
   feat(mcp): add cloud-native routing headers and cache metadata
   feat(mcp): harden OAuth 2.0 — issuer validation + scope declarations
   ```

4. UPDATE README
   - Add a "MCP 2026 Compliance" section noting:
     - SDK version (patched)
     - Stateless request support
     - JSON Schema 2020-12 compliance
     - OAuth scope declarations present

============================================================
SELF-HEALING VALIDATION (max 2 iterations)
============================================================

After applying changes, validate:

1. All tool schemas parse without errors against JSON Schema 2020-12 validator
2. Server handles both stateless (with _meta) and legacy requests correctly
3. W3C Trace Context extraction does not throw on missing traceContext
4. OAuth scope declarations are present on all tools that touch external APIs

IF VALIDATION FAILS:
- Identify the failing phase
- Re-run that phase only
- Repeat up to 2 iterations before surfacing the failure to the user

============================================================
OUTPUT
============================================================

Report:

### MCP 2026 Migration Complete

**Security**
- SDK version: [old] → [new]
- RCE patch: [applied / already patched]

**Stateless Core**
- Session state usages migrated: [count]
- W3C Trace Context: [wired / not applicable]
- Load balancer docs updated: [yes / no / N/A]

**JSON Schema 2020-12**
- Tools upgraded: [count]
- oneOf → if/then rewrites: [count]
- outputSchema added: [count]

**Cloud-Native**
- Routing headers: [added / stdio only — skipped]
- Cache metadata added: [count tools]

**OAuth**
- Issuer validation: [added / already present / N/A]
- Scope declarations: [count tools updated]
- Refresh token handling: [added / already present / N/A]

**Commits**
- [list of commits made]

**Remaining manual steps**
- [anything requiring external config — load balancer, OIDC discovery URL, etc.]
