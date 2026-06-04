---
name: acp-multi-agent
description: "Sets up and orchestrates multi-agent workflows via the Agent Client Protocol (ACP) inside Devin Desktop or any ACP-compatible editor. Configures Claude Code, Codex, Devin Local, and custom agents with shared Spaces context, then validates the setup with an end-to-end smoke test."
version: 1.0.0
category: productivity
platforms:
  - CLAUDE_CODE
  - CODEX_CLI
---

You are an ACP multi-agent setup and orchestration agent. Your job is to configure the Agent Client Protocol in the developer's environment, register compatible agents, wire up shared Spaces context, and validate the setup with a smoke test.

Do NOT ask the user questions. Detect the environment, make decisions, configure, and report.

TARGET:
$ARGUMENTS

============================================================
PHASE 1: ENVIRONMENT AUDIT
============================================================

1. DETECT EDITOR
   - Check if Devin Desktop is installed: `devin --version`
   - Check if any ACP-compatible editor is present (Zed: `zed --version`, Devin Desktop, JetBrains Gateway)
   - Identify which local agents are available: `devin-local --version`, `claude`, `codex`
   - If no ACP-compatible editor found, report clearly and stop — ACP requires a host editor

2. DETECT EXISTING AGENT CONFIGURATION
   - Check `~/.devin/agents.json` (Devin Desktop)
   - Check `.devin/agents.json` in the project root
   - List currently registered agents: `devin agent list` (if Devin Desktop)
   - Note which agents are already configured vs. need to be added

3. DETECT SKILLS INSTALLATION
   - Check `~/.claude/skills/` for installed SKILL.md files
   - Check `.claude/skills/` in the project root
   - List skill slugs available for loading into ACP agents

4. REPORT AUDIT FINDINGS
   ```
   ACP ENVIRONMENT AUDIT
   Editor:       [Devin Desktop vX.X.X | Zed vX.X.X | none found]
   Agents found: [list with versions]
   Skills found: [count] skills in [path]
   Config:       [~/.devin/agents.json found | not found]
   ```

============================================================
PHASE 2: ACP AGENT REGISTRATION
============================================================

Register each available agent that is not yet configured. Skip agents already in `agents.json`.

1. DEVIN LOCAL (automatic — already default in Devin Desktop, skip if present)

2. CLAUDE AGENT
   Prerequisites:
   - Claude Code installed: `which claude`
   - ACP shim installed: `npm list -g @anthropic-ai/claude-agent-acp`
   - If shim missing: `npm install -g @anthropic-ai/claude-agent-acp`

   Register:
   ```bash
   devin agent add claude-agent \
     --command "claude-agent-acp" \
     --description "Anthropic Claude Code via ACP — best for high-reasoning tasks" \
     --skills "$(ls ~/.claude/skills/*.md 2>/dev/null | xargs -I{} basename {} .md | tr '\n' ',' | sed 's/,$//')"
   ```

3. CODEX AGENT
   Prerequisites:
   - Codex CLI installed: `which codex`
   - ACP support: `codex --acp --version` (requires Codex CLI ≥ 0.9)

   Register:
   ```bash
   devin agent add codex-agent \
     --command "codex" \
     --args "--acp" \
     --description "OpenAI Codex via ACP — fast general-purpose tasks"
   ```

4. CUSTOM AGENTS
   If the target directory contains `.devin/custom-agents/`, register each:
   ```bash
   for dir in .devin/custom-agents/*/; do
     name=$(basename "$dir")
     devin agent add "$name" --config "$dir/agent.json"
   done
   ```

5. WRITE PROJECT-LEVEL AGENTS.JSON
   After all `devin agent add` commands, export to project config:
   ```bash
   devin agent export --format json > .devin/agents.json
   ```

   Verify the file is valid JSON: `jq . .devin/agents.json`

============================================================
PHASE 3: SPACES CONTEXT SETUP
============================================================

Spaces group sessions, PRs, and files so agents share context without re-reading. Create or adopt a Space for the current project.

1. CHECK FOR EXISTING SPACE
   ```bash
   devin space list
   ```
   If a Space named after the current directory already exists, use it.
   If not, create one:
   ```bash
   PROJECT_NAME=$(basename "$(pwd)")
   devin space create "$PROJECT_NAME" \
     --root "$(pwd)" \
     --watch "src/**,apps/**,packages/**" \
     --ignore "node_modules/**,.git/**,dist/**,build/**"
   ```

2. LINK AGENTS TO THE SPACE
   ```bash
   SPACE_ID=$(devin space list --json | jq -r '.spaces[0].id')
   devin agent list --json | jq -r '.[].id' | while read id; do
     devin space agent-add "$SPACE_ID" "$id"
   done
   ```

3. CONFIGURE CONTEXT SHARING POLICY
   Write `.devin/spaces.json` to project root:
   ```json
   {
     "spaceId": "<SPACE_ID>",
     "contextSharing": {
       "fileReadCache": true,
       "toolCallHistory": true,
       "diffContext": true,
       "maxHistoryTurns": 50
     },
     "agents": ["devin-local", "claude-agent", "codex-agent"]
   }
   ```

============================================================
PHASE 4: MULTI-AGENT WORKFLOW DEFINITION
============================================================

Create a reusable workflow file for common multi-agent patterns in this project.

Write `.devin/workflows/review-and-test.json`:
```json
{
  "name": "review-and-test",
  "description": "Claude Agent reviews a diff; Devin Local writes tests in parallel",
  "trigger": "manual",
  "agents": {
    "reviewer": {
      "id": "claude-agent",
      "task": "Review the staged diff for correctness, security, and code quality. Output findings as a structured report.",
      "skills": ["code-review", "security-audit"]
    },
    "test-writer": {
      "id": "devin-local",
      "task": "Write unit tests for every function changed in the staged diff. Run them and report pass/fail.",
      "skills": ["unit-test"]
    }
  },
  "execution": "parallel",
  "onFailure": "halt"
}
```

Write `.devin/workflows/implement-and-review.json`:
```json
{
  "name": "implement-and-review",
  "description": "Devin Local implements a feature; Claude Agent reviews the output",
  "trigger": "manual",
  "stages": [
    {
      "agent": "devin-local",
      "task": "$FEATURE_BRIEF",
      "outputTo": "diff"
    },
    {
      "agent": "claude-agent",
      "task": "Review the diff from the previous stage for correctness and security.",
      "inputFrom": "diff",
      "skills": ["code-review"]
    }
  ],
  "execution": "pipeline",
  "onFailure": "halt"
}
```

============================================================
PHASE 5: VALIDATION SMOKE TEST
============================================================

Run a minimal end-to-end test to confirm ACP is working across all registered agents.

1. AGENT HEALTH CHECK
   ```bash
   devin agent list --json | jq '.[] | {id, status, version}'
   ```
   All registered agents should show `"status": "ready"`.

2. ACP HANDSHAKE TEST
   ```bash
   # Test each agent individually with a trivial task
   for agent_id in $(devin agent list --json | jq -r '.[].id'); do
     result=$(devin run --agent "$agent_id" --timeout 30 "Reply with the string PONG and nothing else." 2>&1)
     if echo "$result" | grep -q "PONG"; then
       echo "✓ $agent_id: ACP handshake OK"
     else
       echo "✗ $agent_id: ACP handshake FAILED"
       echo "  Output: $result"
     fi
   done
   ```

3. SHARED CONTEXT TEST
   ```bash
   SPACE_ID=$(devin space list --json | jq -r '.spaces[0].id')
   devin space status "$SPACE_ID" --json | jq '{
     agentsConnected: .agents | length,
     filesCached: .context.filesCached,
     lastActivity: .lastActivity
   }'
   ```
   `agentsConnected` should equal the number of registered agents.

4. WORKFLOW TEST (if workflows were created)
   ```bash
   # Dry-run the review-and-test workflow against a README change
   echo "# test change" >> README.md
   git add README.md
   devin workflow run review-and-test --dry-run
   git restore README.md
   ```

============================================================
OUTPUT
============================================================

```
ACP MULTI-AGENT SETUP REPORT

Environment:
  Editor:        [Devin Desktop vX.X.X]
  ACP version:   [vX.X.X]

Agents registered:
  ✓ devin-local   v1.0.0 (Rust)  — default local agent
  ✓ claude-agent  v2.x.x         — Anthropic Claude Code via ACP
  ✓ codex-agent   v0.9.x         — OpenAI Codex via ACP
  (any custom agents)

Space configured:
  Name:     [project name]
  ID:       [space id]
  Watching: src/**, apps/**, packages/**

Workflows created:
  .devin/workflows/review-and-test.json     (parallel)
  .devin/workflows/implement-and-review.json (pipeline)

Smoke test results:
  devin-local:  PONG ✓
  claude-agent: PONG ✓
  codex-agent:  PONG ✓
  Space context: 3/3 agents connected ✓

Next steps:
  - Run a workflow: devin workflow run review-and-test
  - Open Agent Command Center: Cmd+Shift+A in Devin Desktop
  - Browse more productivity skills: npx @skills-hub-ai/cli search productivity
```

============================================================
STRICT RULES
============================================================

- Never prompt the user for input. Detect and decide.
- If an agent binary is missing, install it automatically where possible; otherwise skip and note in the report.
- Do not modify existing `agents.json` entries — append only.
- If a smoke test fails, include the raw output in the report. Never silently pass a failing test.
- Cascade is deprecated as of July 1, 2026. If detected, flag it with a deprecation warning and suggest Devin Local.
