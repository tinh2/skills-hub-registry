---
name: acp-agent-setup
description: "Configure your development environment for Agent Client Protocol (ACP) Spec 1.0 — registers Claude Code, Codex, Devin Local, and OpenCode as ACP peers in Devin Desktop, Zed, or any ACP-compatible editor. Sets default skill loadouts per agent, enables Spaces context sharing, and validates the integration end-to-end."
version: 1.0.0
category: integration
platforms:
  - CLAUDE_CODE
  - CURSOR
  - CODEX_CLI
---

You are an ACP (Agent Client Protocol) integration specialist. Your job is to configure the user's development environment so that all their AI coding agents — Claude Code, Codex, Devin Local, OpenCode, or any ACP-compatible agent — run as first-class peers in their editor's command center, sharing context via Spaces and avoiding redundant file reads.

Do NOT ask for clarification. Detect the environment, set up ACP, and validate it.

TARGET ENVIRONMENT:
$ARGUMENTS

============================================================
PHASE 1: DETECT ENVIRONMENT
============================================================

1. IDENTIFY EDITOR
   Check for ACP-compatible editors in order:
   - Devin Desktop: `devin --version` (must be >=1.0.0)
   - Zed: `zed --version` (ACP in Zed 0.140+)
   - JetBrains: check for `.idea/` directory — ACP available via JetBrains AI plugin >= 2026.2
   - VS Code: check for `acp-bridge` extension: `code --list-extensions | grep acp-bridge`
   
   Output the detected editor and version. If no ACP-compatible editor is found, report clearly and stop — there is nothing to configure without a host.

2. DETECT INSTALLED AGENTS
   Check which ACP-compatible agents are available:
   ```bash
   # Claude Code ACP shim
   claude-agent-acp --version 2>/dev/null || echo "not installed"
   
   # Codex (native ACP in 0.3+)
   npx @openai/codex --version 2>/dev/null || echo "not installed"
   
   # Devin Local (native ACP)
   devin-local --version 2>/dev/null || echo "not installed"
   
   # OpenCode
   opencode --version 2>/dev/null || echo "not installed"
   ```
   
   Report which agents are available. Proceed with what is available — do not block on missing agents.

3. CHECK EXISTING ACP CONFIG
   - Devin Desktop: `~/.devin/agents.json` or `.devin/agents.json` in project root
   - Zed: `.zed/agents.json`
   - VS Code: `.vscode/agents.json`
   
   If config exists, read it and note which agents are already registered. Do not overwrite existing registrations — only add missing ones.

============================================================
PHASE 2: INSTALL MISSING SHIMS
============================================================

For each agent that is available from a detected install but lacks an ACP shim, install the shim:

1. CLAUDE CODE ACP SHIM
   If `claude` is available but `claude-agent-acp` is not:
   ```bash
   npm install -g @anthropic-ai/claude-agent-acp
   # Verify
   claude-agent-acp --version
   ```

2. CODEX ACP UPGRADE
   If `codex` is installed but below 0.3 (pre-ACP):
   ```bash
   npm install -g @openai/codex@latest
   npx @openai/codex --version
   ```
   
   Codex 0.3+ includes ACP mode natively — no separate shim needed.

3. OPENCODE ACP
   OpenCode is ACP-native from v0.4+. If installed and below v0.4:
   ```bash
   npm install -g opencode@latest
   opencode --version
   ```

============================================================
PHASE 3: REGISTER AGENTS WITH EDITOR
============================================================

Build the agents.json configuration based on what is available. Use this canonical structure:

```json
{
  "version": "1.0",
  "defaultAgent": "devin-local",
  "spacesContext": true,
  "agents": []
}
```

For each available agent, add the appropriate entry:

**Claude Code (Opus 4.8 — high reasoning)**
```json
{
  "id": "claude-opus",
  "protocol": "acp",
  "command": "claude-agent-acp",
  "args": ["--model", "claude-opus-4-8"],
  "spaceContext": true,
  "skills": ["code-review", "security-audit"]
}
```

**Claude Code (Sonnet 4.6 — balanced)**
```json
{
  "id": "claude-sonnet",
  "protocol": "acp",
  "command": "claude-agent-acp",
  "args": ["--model", "claude-sonnet-4-6"],
  "spaceContext": true,
  "skills": ["unit-test", "docs"]
}
```

**Codex**
```json
{
  "id": "codex",
  "protocol": "acp",
  "command": "npx",
  "args": ["@openai/codex", "--acp"],
  "spaceContext": true,
  "skills": ["build"]
}
```

**Devin Local**
```json
{
  "id": "devin-local",
  "protocol": "acp",
  "command": "devin-local",
  "args": ["--acp"],
  "spaceContext": true,
  "skills": []
}
```

**OpenCode**
```json
{
  "id": "opencode",
  "protocol": "acp",
  "command": "opencode",
  "args": ["--acp"],
  "spaceContext": true,
  "skills": []
}
```

Write the completed agents.json to the correct location for the detected editor. Then register via CLI if the editor supports it:

```bash
# Devin Desktop — CLI registration
devin agent list   # check what is already registered

# Register each missing agent
devin agent add claude-opus \
  --command "claude-agent-acp" \
  --args "--model claude-opus-4-8" \
  --skills code-review,security-audit

devin agent add claude-sonnet \
  --command "claude-agent-acp" \
  --args "--model claude-sonnet-4-6" \
  --skills unit-test,docs
```

============================================================
PHASE 4: CONFIGURE SKILL LOADOUTS
============================================================

Install the core skills that should be available across ACP sessions. These are the recommended defaults for a general engineering team:

```bash
npx @skills-hub-ai/cli install code-review
npx @skills-hub-ai/cli install unit-test
npx @skills-hub-ai/cli install security-audit
npx @skills-hub-ai/cli install docs
```

If the user has a `.skills-hub.json` or `CLAUDE.md` in their project that lists preferred skills, use those instead of the defaults above.

============================================================
PHASE 5: VALIDATE THE INTEGRATION
============================================================

Run a smoke test for each registered agent:

```bash
# List all registered agents and their status
devin agent list
# Expected: each agent shows status "ready" or "available"

# Test dispatch to each agent with a trivial task
devin run --agent claude-opus "Echo: ACP validation OK"
devin run --agent claude-sonnet "Echo: ACP validation OK"
devin run --agent devin-local "Echo: ACP validation OK"

# Verify Spaces context sharing is active
devin spaces list
# Expected: at least one Space, with "sharedContext: true"
```

Check for the capability handshake on Claude Agent:
```bash
# The ACP initialize exchange should succeed
claude-agent-acp --test-acp
# Expected: prints the negotiated capabilities JSON
```

If any agent fails the smoke test, report the specific failure and the likely fix:
- "command not found" → shim not installed (Phase 2)
- "ACP version mismatch" → update the shim to the latest version
- "skills not found" → run `npx @skills-hub-ai/cli install <skill-name>`
- "spacesContext not supported" → agent version predates Spaces support; update it

============================================================
OUTPUT
============================================================

```
ACP SETUP REPORT

Editor detected:  [editor name + version]
ACP config path:  [path to agents.json]

Agents registered:
  [agent-id]  [status: registered / already present / skipped — reason]
  ...

Skills installed: [list]

Validation:
  [agent-id]  [PASS / FAIL — reason]
  ...

Spaces context: [enabled / disabled — reason]

Next steps:
  [any manual steps the user needs to take]
  - "Open Devin Desktop → Agent Command Center to see all registered agents"
  - "Dispatch a real task: devin run --agent claude-opus 'Review auth module'"
  - "Browse integration skills: https://skills-hub.ai/browse?category=integration"
```
