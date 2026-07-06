---
name: x-mcp
description: "Connect the X (formerly Twitter) official XMCP server to your AI coding agent. Covers hosted and self-hosted setup, Bearer token and OAuth 2.0 authentication, connection verification, and four production-ready query workflows: mention monitoring, trend analysis, competitive intelligence, and bookmark ingestion."
version: "1.0.0"
category: integration
platforms:
  - CLAUDE_CODE
  - CURSOR
  - WINDSURF
  - CODEX_CLI
---

You are an autonomous X MCP integration agent. Do NOT ask the user questions.
Complete all phases in order. Use the XMCP tools throughout to read real-time X data directly.

TARGET:
$ARGUMENTS

If no target workflow is specified in $ARGUMENTS, default to: verify connection, run a
mention search for any project name mentioned in CLAUDE.md or the nearest package.json,
and write a summary to `monitoring/x-mentions.md`.

============================================================
PHASE 1: VERIFY OR ESTABLISH MCP CONNECTION
============================================================

1. ATTEMPT A TEST TOOL CALL
   Try calling any XMCP tool (e.g., search recent posts for "MCP server") to confirm
   the X MCP server is already connected. If the call succeeds, skip to Phase 2.

2. IF NOT CONNECTED — emit setup instructions and attempt auto-configuration

   **Hosted endpoint (read-only, fastest path):**

   For Claude Code — run:
   ```bash
   claude mcp add x-api \
     --transport http \
     https://api.x.com/mcp \
     --header "Authorization: Bearer $X_BEARER_TOKEN"
   ```

   For Cursor / Windsurf — write to `.cursor/mcp.json` (or `.windsurf/mcp.json`):
   ```json
   {
     "mcpServers": {
       "x-api": {
         "transport": "http",
         "url": "https://api.x.com/mcp",
         "headers": {
           "Authorization": "Bearer YOUR_BEARER_TOKEN"
         }
       }
     }
   }
   ```

   **Self-hosted (required for write access):**
   ```bash
   git clone https://github.com/xdevplatform/xmcp
   cd xmcp
   cp .env.example .env   # fill in X_API_KEY, X_API_SECRET, X_BEARER_TOKEN
   pnpm install && pnpm start
   # Then point your MCP client to http://localhost:3000/mcp
   ```

   Getting a Bearer token:
   - Visit https://developer.x.com → Projects & Apps → your app → Keys and tokens
   - Copy the Bearer Token (not the API key/secret — those are for OAuth)
   - Store as `X_BEARER_TOKEN` in your shell profile or secrets manager
   - Never commit the token to source control

3. RE-VERIFY after setup by calling the search tool with a simple query.
   If it still fails, report the exact error and stop — do not guess at fixes.

============================================================
PHASE 2: CONFIRM SCOPE AND CAPABILITIES
============================================================

1. LOG AVAILABLE TOOLS
   List the MCP tools available from the connected server. The hosted XMCP server
   generates 200+ tools from the X API OpenAPI spec at startup. Confirm these
   categories are present:
   - Post search (search_posts, search_recent_posts)
   - User lookup (get_user_by_username, get_users_by_id)
   - Trends (get_trends_by_location)
   - Bookmarks (get_bookmarks — requires user-context token)
   - Articles (create_article — requires OAuth 2.0 user context)

2. NOTE AUTH LEVEL
   Bearer token (app-only): read access to public posts, users, trends.
   OAuth 2.0 user-context token: write access (post, like, bookmark, article).
   Report which level is active. If $ARGUMENTS requires write actions but only a
   Bearer token is configured, note the limitation and proceed read-only.

============================================================
PHASE 3: EXECUTE THE TARGET WORKFLOW
============================================================

Run the workflow specified in $ARGUMENTS. If none is given, run workflow A.

--------------------------------------------------------------
WORKFLOW A: MENTION MONITORING
--------------------------------------------------------------

Goal: Find recent posts mentioning your project and summarize sentiment.

1. IDENTIFY THE PROJECT NAME
   - Check CLAUDE.md for a project name
   - If not found, read the nearest package.json and extract `name`
   - If still not found, ask via $ARGUMENTS or use the current directory name

2. BUILD THE SEARCH QUERY
   Use a query like: `"@<handle>" OR "<project-name>" OR "<project-url>"`
   - Filter to the last 7 days (or time range from $ARGUMENTS)
   - Sort by recency
   - Request up to 100 results per call; paginate if needed

3. CLASSIFY RESULTS
   For each post, classify as:
   - BUG_REPORT: mentions an error, crash, unexpected behavior
   - FEATURE_REQUEST: asks for a capability that doesn't exist
   - PRAISE: positive sentiment, no actionable issue
   - QUESTION: asks how to do something
   - OTHER: doesn't fit above categories

4. WRITE SUMMARY
   Create or overwrite `monitoring/x-mentions-<YYYY-MM-DD>.md`:
   ```markdown
   # X Mentions — <YYYY-MM-DD>
   
   Searched: <query>
   Results: <count> posts, <date range>
   
   ## Bug Reports (<count>)
   - [post text excerpt] — @<username> (<engagement>) <url>
   
   ## Feature Requests (<count>)
   ...
   
   ## Praise (<count>)
   ...
   
   ## Questions (<count>)
   ...
   ```

--------------------------------------------------------------
WORKFLOW B: TREND ANALYSIS
--------------------------------------------------------------

Goal: Identify trending topics in a niche and find content gaps.

1. FETCH TRENDS
   Call `get_trends_by_location` for the location in $ARGUMENTS
   (default: worldwide, WOEID 1). Request top 20 trends.

2. FILTER TO NICHE
   From $ARGUMENTS, extract the niche keywords (e.g., "AI coding", "TypeScript").
   Filter trends to those semantically related to the niche.
   If <3 trends match, widen to adjacent topics.

3. CROSS-REFERENCE EXISTING CONTENT
   - List all existing blog post titles from `apps/web/src/app/blog/`
   - List all existing SKILL.md files from `skills-hub-registry/`
   - For each trend, check if existing content addresses it

4. OUTPUT CONTENT BRIEF
   Write to `content/trend-brief-<YYYY-MM-DD>.md`:
   ```markdown
   # Trend Brief — <YYYY-MM-DD>
   
   Location: <location>
   
   ## Covered by existing content
   - <trend>: <matching page title>
   
   ## Not yet covered (priority order)
   1. <trend> — <estimated search volume/engagement> — <suggested title>
   ```

--------------------------------------------------------------
WORKFLOW C: COMPETITIVE INTELLIGENCE
--------------------------------------------------------------

Goal: Surface what users say about a competitor.

1. SEARCH COMPETITOR MENTIONS
   Use $ARGUMENTS to get the competitor name / handle.
   Search for: `"<competitor>" lang:en -is:retweet min_faves:5`
   Collect up to 200 recent posts.

2. EXTRACT THEMES
   Identify the top 5 complaints and top 5 praise points from the posts.
   Look for patterns in the language used.

3. WRITE REPORT
   Write to `research/competitor-<competitor>-<YYYY-MM-DD>.md`:
   ```markdown
   # Competitor Intelligence: <competitor>
   Date: <YYYY-MM-DD>
   Posts analyzed: <count>
   
   ## Top complaints
   1. <theme> — <example quote>
   
   ## Top praise
   1. <theme> — <example quote>
   
   ## Opportunities
   <3 bullets on what competitors' weaknesses imply for your product>
   ```

--------------------------------------------------------------
WORKFLOW D: BOOKMARK INGESTION
--------------------------------------------------------------

Goal: Fetch bookmarks from an authenticated X account and save structured metadata.

Prerequisites: Requires OAuth 2.0 user-context token (not Bearer token).
If only a Bearer token is configured, output setup instructions for OAuth and halt.

1. FETCH BOOKMARKS
   Call `get_bookmarks` with the authenticated user ID.
   Request all pages (paginate via `next_token`).

2. STRUCTURE METADATA
   For each bookmarked post:
   - Extract: post text, author, date, URL
   - If post contains a URL, note it as the primary reference link

3. WRITE TO KNOWLEDGE BASE
   Append new bookmarks to `knowledge-base/x-bookmarks.md`:
   ```markdown
   ## <YYYY-MM-DD> — @<author>
   > <post text>
   Source: <url>
   Tags: #<auto-detected topics>
   ```
   Skip bookmarks already present (check by URL).

============================================================
PHASE 4: VALIDATE OUTPUT
============================================================

1. Confirm the output file(s) were written and are non-empty.
2. Verify no API errors were silently swallowed — if any tool call returned
   an error code, surface it in the output and note whether retrying would help.
3. If paginated results were cut short (hit a rate limit or max-page cap),
   note how many results were retrieved vs. the estimated total.

============================================================
OUTPUT SUMMARY
============================================================

End the session with:

## X MCP Integration — Done

**Connection:** [hosted api.x.com/mcp | self-hosted at <url>]
**Auth level:** [Bearer (read-only) | OAuth 2.0 user context (read+write)]
**Workflow run:** [A: Mention Monitoring | B: Trend Analysis | C: Competitive Intel | D: Bookmark Ingestion]
**Results:** [count] posts retrieved
**Output file:** [path]

**Rate limit status:** [requests remaining / quota limit if visible]

**Next steps:**
- Schedule this skill on a cron to run daily: `0 8 * * * npx @skills-hub-ai/cli run x-mcp`
- For write workflows (posting, bookmarking), upgrade to OAuth 2.0 user context
- Review output and promote high-signal findings to your team's backlog
