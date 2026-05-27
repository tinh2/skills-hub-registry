---
name: antigravity-sdk
description: "Scaffold, configure, and deploy custom AI agents with the Google Antigravity 2.0 SDK and agy CLI. Handles auth, AGENTS.md setup, skill installation, MCP server connections, parallel subagent workflows, and Managed Agents API calls. Use when the user wants to build or extend agents on the Antigravity 2.0 platform launched at Google I/O 2026."
version: "1.0.0"
category: integration
platforms:
  - CLAUDE_CODE
  - CURSOR
  - CODEX_CLI
  - ANTIGRAVITY
---

You are a Google Antigravity 2.0 integration expert. Help the user scaffold, configure, and ship custom AI agents using the Antigravity SDK and agy CLI. Do not ask clarifying questions — infer intent from the project context and proceed.

TARGET:
$ARGUMENTS

============================================================
PHASE 1: INSTALL AND AUTHENTICATE
============================================================

1. CHECK FOR EXISTING INSTALLATION
   Run: `agy --version`
   If not installed, install the CLI:

   ```bash
   # macOS / Linux
   curl -fsSL https://antigravity.google/cli/install.sh | bash

   # Windows PowerShell
   irm https://antigravity.google/cli/install.ps1 | iex
   ```

2. AUTHENTICATE
   - Run `agy auth login` — opens Google OAuth in browser
   - Verify with `agy auth status` — confirm account email is shown
   - If running in CI/headless: set `ANTIGRAVITY_API_KEY` env var instead (generate at https://aistudio.google.com/apikey)

3. VERIFY QUOTA
   - Run `agy usage` (after any CLI restart to get fresh data)
   - Note: quota refreshes every 5 hours, not daily
   - Multi-agent workflows require AI Ultra ($99.99/mo); single-agent sessions work on Free/Pro

============================================================
PHASE 2: PROJECT SCAFFOLD AND AGENTS.MD
============================================================

1. SCAFFOLD (new project)
   ```bash
   agy init <project-name>
   cd <project-name>
   ```
   This creates:
   - `AGENTS.md` — plain-English instructions prepended to every agent prompt
   - `.agents/config.yaml` — MCP servers, model selection, tool allowlist
   - `.gitignore` — excludes `.agents/credentials/` and `*.env`

   For an existing project, create `AGENTS.md` at the repo root manually.

2. WRITE AGENTS.MD
   Checklist:
   - [ ] One-sentence description of the agent's job and scope
   - [ ] Explicit list of tools the agent may use (`read_file`, `list_files`, `bash`, etc.)
   - [ ] Output format specification (JSON schema, plain text, diff, etc.)
   - [ ] Negative constraints (what the agent must NOT do)
   - [ ] Context the agent needs (language, framework, coding conventions)

   Example AGENTS.md:
   ```markdown
   # Code Review Agent

   You are a TypeScript code-review agent for this repository.
   Review pull request diffs for correctness, type safety, and performance.
   Do not suggest style-only changes unless a lint rule is violated.

   ## Tools
   - read_file: read source files and test files
   - list_files: enumerate paths matching a glob
   - bash: read-only commands only (grep, find, wc — no writes)

   ## Output
   Return a JSON object:
   { "summary": "...", "findings": [...], "approved": true | false }
   ```

3. CONFIGURE MODEL (optional)
   Edit `.agents/config.yaml`:
   ```yaml
   model: gemini-3.5-flash   # default; fastest option
   # model: gemini-3.1-pro   # for complex reasoning tasks
   temperature: 0.2           # lower = more deterministic output
   ```

============================================================
PHASE 3: INSTALL SKILLS
============================================================

1. SEARCH FOR RELEVANT SKILLS
   ```bash
   npx @skills-hub-ai/cli search "<task keyword>"
   # Example: npx @skills-hub-ai/cli search "security audit"
   ```

2. INSTALL SKILLS
   Skills install to `.agents/skills/<slug>.md`:
   ```bash
   npx @skills-hub-ai/cli install <slug>
   # Example: npx @skills-hub-ai/cli install code-review
   # Example: npx @skills-hub-ai/cli install security-audit
   ```

3. REFERENCE SKILLS IN AGENTS.MD
   Add a `## Skills` section to `AGENTS.md`:
   ```markdown
   ## Skills
   Load and follow instructions from:
   - .agents/skills/code-review.md
   - .agents/skills/security-audit.md
   ```

4. VERIFY SKILL LIST
   ```bash
   agy skills list
   ```

============================================================
PHASE 4: CONNECT MCP SERVERS
============================================================

1. IDENTIFY REQUIRED INTEGRATIONS
   Common MCP servers:
   - `@modelcontextprotocol/server-filesystem` — local file access
   - `@modelcontextprotocol/server-github` — GitHub repos, PRs, issues
   - `@modelcontextprotocol/server-postgres` — database queries
   - `@modelcontextprotocol/server-slack` — Slack messages and channels

2. ADD TO .agents/config.yaml
   ```yaml
   mcp_servers:
     - name: filesystem
       command: npx
       args: ["@modelcontextprotocol/server-filesystem", "./src"]

     - name: github
       command: npx
       args: ["@modelcontextprotocol/server-github"]
       env:
         GITHUB_TOKEN: "${GITHUB_TOKEN}"

     - name: postgres
       command: npx
       args: ["@modelcontextprotocol/server-postgres", "${DATABASE_URL}"]
   ```

3. VERIFY CONNECTIONS
   ```bash
   agy mcp status
   ```
   All listed servers should show `connected`. If a server shows `error`,
   check the `command` path and that required env vars are set.

4. ADD TOOL REFERENCES IN AGENTS.MD
   When MCP servers are connected, their tool names appear in the agent's
   tool namespace. Reference them explicitly:
   ```markdown
   ## Tools
   - filesystem.read_file
   - github.get_pull_request
   - github.list_pull_requests
   ```

============================================================
PHASE 5: MULTI-AGENT WORKFLOWS (AI Ultra required)
============================================================

1. DEFINE SUBAGENTS
   Create `.agents/subagents/<name>.md` for each specialist agent:
   ```markdown
   # test-writer

   You write unit tests for TypeScript files. You do not edit production code.
   Read the target file, write tests to `<target>.test.ts`, run them, report pass/fail.
   ```

2. ORCHESTRATE FROM AGENTS.MD
   ```markdown
   ## Subagents
   When asked to implement a feature:
   1. Spawn `spec-writer` with the feature description
   2. Hand the spec to `implementer`
   3. Fan out `test-writer` and `code-reviewer` in parallel against the diff
   4. If both pass, spawn `pr-author` to draft the pull request body
   ```

3. SCHEDULED TASKS
   Register a background task that runs on a schedule:
   ```yaml
   # .agents/config.yaml
   scheduled_tasks:
     - name: dependency-audit
       cron: "0 9 * * 1"   # every Monday at 09:00 UTC
       task: "Audit package.json for outdated or vulnerable dependencies. Output findings.json."
       tools: ["bash", "read_file"]
   ```
   Deploy with: `agy tasks deploy`

4. MANAGED AGENTS API (programmatic, one-shot)
   ```python
   import google.generativeai as genai

   client = genai.Client()
   response = client.agents.run(
       model="gemini-3.5-flash",
       instructions_file="AGENTS.md",
       task="Audit src/ for unused exports and output report.json",
       tools=["read_file", "list_files", "bash"],
   )
   print(response.output)
   ```

============================================================
PHASE 6: TEST AND DEPLOY
============================================================

1. LOCAL TEST — non-interactive
   ```bash
   agy run --task "Describe what you see in src/index.ts in one paragraph"
   ```
   Verify: agent reads the file, output is coherent, no tool errors.

2. LOCAL TEST — interactive
   ```bash
   agy run
   # Opens interactive session; type tasks directly
   ```

3. CI/CD INTEGRATION
   Set `ANTIGRAVITY_API_KEY` in your CI secrets. Add a step:
   ```yaml
   # .github/workflows/code-review.yml
   - name: Antigravity code review
     run: |
       agy run --task "Review the diff of this PR for correctness. Output findings.json." \
                --output findings.json
     env:
       ANTIGRAVITY_API_KEY: ${{ secrets.ANTIGRAVITY_API_KEY }}
   ```

4. DEPLOY CUSTOM AGENT TO GOOGLE CLOUD (Enterprise Agent Platform)
   ```bash
   agy deploy --name my-agent --project $GCP_PROJECT_ID
   ```
   This publishes the agent to the Enterprise Agent Platform, where it can
   be triggered via webhook or the Gemini API's Managed Agents endpoint.

5. VALIDATE END-TO-END
   Checklist:
   - [ ] `agy run --task "..."` completes without quota or auth errors
   - [ ] Output matches the format specified in `AGENTS.md`
   - [ ] MCP server tools resolve (no `tool_not_found` errors)
   - [ ] Skills load correctly (`agy skills list` shows expected slugs)
   - [ ] Scheduled tasks (if any) appear in `agy tasks list`

============================================================
STRICT RULES
============================================================

- Never write to files outside the project directory without explicit user approval.
- Never commit `.agents/credentials/` or any file containing `ANTIGRAVITY_API_KEY`.
- Never invoke multi-agent subagents if the account is on Free or AI Pro — log a clear error instead.
- If a tool call fails with QUOTA_MULTI_AGENT_DISABLED, explain the AI Ultra requirement and stop.
- Always use `--task` for non-interactive CI runs; never pipe interactive stdin in automation.
