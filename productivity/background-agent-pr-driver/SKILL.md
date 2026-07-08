---
name: background-agent-pr-driver
description: "Configures Claude Code's July 2026 async workflow: background agents that auto-commit, push, and open draft PRs when worktree tasks finish. Sets up Notification hooks for agent_needs_input and agent_completed events, enforces Manual permission mode, and wires dynamic workflow sizing. Lets you dispatch multiple agents in the morning and receive reviewable PRs without watching the terminal."
version: "1.0.0"
category: productivity
platforms:
  - CLAUDE_CODE
---

You are an autonomous Claude Code async-workflow configurator. Do NOT ask questions — audit, install, and validate.

TARGET PROJECT:
$ARGUMENTS

============================================================
PHASE 1: AUDIT EXISTING SETUP
============================================================

1. Check Claude Code version: `claude --version`
   - Minimum required: v2.1.198 (July 2, 2026) for auto-PR behavior.
   - If older, output: "Claude Code must be v2.1.198 or newer. Run: npm install -g @anthropic-ai/claude-code@latest"
   - Then exit.

2. Check `.claude/settings.json` and `.claude/settings.local.json` for:
   - `defaultMode` — report current value (default/auto/manual)
   - `model` — report current model
   - Existing `hooks.Notification` configuration

3. Check `.claude/hooks/` for existing hook scripts.

4. Verify git setup:
   ```
   git remote -v       # need at least one remote (for push)
   git status          # confirm clean or near-clean working tree
   git branch -a       # list existing branches
   ```

5. Report findings:
   ```
   AUDIT REPORT
   Claude Code version: [x.x.xxx]
   Current defaultMode: [default/auto/manual/unset]
   Current model: [model or "unset"]
   Notification hooks: [configured/not configured]
   Existing hook scripts: [list or "none"]
   Git remote: [configured/missing]
   ```

============================================================
PHASE 2: CONFIGURE MANUAL PERMISSION MODE
============================================================

Read `.claude/settings.json` (or create it if absent). Merge in:

```json
{
  "defaultMode": "manual",
  "model": "claude-sonnet-5"
}
```

Rules:
- Preserve all existing fields — do NOT overwrite unrelated settings.
- If `defaultMode` is already `"manual"` or `"auto"`, note it in the report but do not override a deliberate `"auto"` setting — only set `"manual"` if the field is unset or was `"default"`.
- Write the merged config back to `.claude/settings.json`.

Explain to the user:
- `"manual"` means every filesystem/shell tool call requires approval unless covered by an explicit allowlist rule.
- To run agents autonomously in CI, pass `--permission-mode auto` or set `"defaultMode": "auto"` in a CI-specific settings file.

============================================================
PHASE 3: INSTALL NOTIFICATION HOOKS
============================================================

Create `.claude/hooks/` if it does not exist.

### 3a. Detect platform

```bash
OS="$(uname -s)"
# Darwin = macOS, Linux = Linux, MINGW*/CYGWIN* = Windows
```

### 3b. Write notify.sh

```bash
#!/usr/bin/env bash
# background-agent-pr-driver: Notification hook for agent events
# Fires on: agent_needs_input, agent_completed
set -euo pipefail

INPUT=$(cat)
EVENT=$(echo "$INPUT" | jq -r '.event // empty')
AGENT=$(echo "$INPUT" | jq -r '.agentDescription // "background agent"')
SESSION=$(echo "$INPUT" | jq -r '.sessionId // ""')

if [[ -z "$EVENT" ]]; then exit 0; fi

TITLE="Claude Code"
case "$EVENT" in
  agent_needs_input)
    MSG="$AGENT needs input"
    ;;
  agent_completed)
    MSG="$AGENT finished — draft PR open"
    ;;
  *)
    exit 0
    ;;
esac

# Platform-specific notification
OS="$(uname -s)"
case "$OS" in
  Darwin)
    osascript -e "display notification \"$MSG\" with title \"$TITLE\"" 2>/dev/null || true
    ;;
  Linux)
    if command -v notify-send &>/dev/null; then
      notify-send "$TITLE" "$MSG" 2>/dev/null || true
    fi
    ;;
  MINGW*|CYGWIN*|MSYS*)
    powershell.exe -Command "
      Add-Type -AssemblyName System.Windows.Forms;
      \$n = New-Object System.Windows.Forms.NotifyIcon;
      \$n.Icon = [System.Drawing.SystemIcons]::Information;
      \$n.Visible = \$true;
      \$n.ShowBalloonTip(5000, '$TITLE', '$MSG', [System.Windows.Forms.ToolTipIcon]::Info);
      Start-Sleep 6; \$n.Dispose()
    " 2>/dev/null || true
    ;;
esac

# Optional: log event for audit trail
LOG_FILE="${CLAUDE_PROJECT_DIR:-$HOME}/.claude/agent-events.log"
echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) $EVENT session=$SESSION agent=\"$AGENT\"" >> "$LOG_FILE" 2>/dev/null || true

exit 0
```

Make executable: `chmod +x .claude/hooks/notify.sh`

### 3c. Merge Notification hook into settings.json

Read the current `.claude/settings.json`. Merge in the `hooks.Notification` block, preserving all existing hooks:

```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "agent_needs_input|agent_completed",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/notify.sh",
            "async": true
          }
        ]
      }
    ]
  }
}
```

If `hooks.Notification` already exists, append the new entry rather than replacing it.

============================================================
PHASE 4: CONFIGURE DYNAMIC WORKFLOW SIZING
============================================================

Open Claude Code interactively (or document the step clearly):

Dynamic workflow size is set via `/config` inside a Claude Code session — it is not a JSON field. Output the following instructions for the user:

```
MANUAL STEP REQUIRED
Inside a Claude Code session, run:
  /config

Then navigate to:
  Dynamic workflow size → set to your preference:
  - small: 2–3 agents (targeted tasks, low token spend)
  - medium: 4–6 agents (default; most feature work)
  - large: 8–12 agents (whole-codebase refactors, migrations)

This is advisory — the model weighs task complexity too.
```

Also check: is there a `.claude/config.json` with a `workflowSize` field? If so, report its current value.

============================================================
PHASE 5: ADD AGENT-LAUNCH WORKFLOW SCRIPT
============================================================

Create `.claude/scripts/dispatch-agents.sh` — a reference script for the async morning-dispatch workflow:

```bash
#!/usr/bin/env bash
# background-agent-pr-driver: Dispatch multiple background agents
# Each runs in an isolated git worktree and opens a draft PR on finish.
#
# Usage: ./.claude/scripts/dispatch-agents.sh "task 1" "task 2" "task 3"
#
# Requirements: claude >= v2.1.198, git remote configured, gh CLI installed
set -euo pipefail

if [[ $# -eq 0 ]]; then
  echo "Usage: $0 \"task description 1\" \"task description 2\" ..."
  echo ""
  echo "Each task runs as an isolated background agent in its own worktree."
  echo "Agents commit, push, and open draft PRs when finished."
  exit 1
fi

TIMESTAMP="$(date -u +%Y%m%d-%H%M)"

for TASK in "$@"; do
  SLUG="$(echo "$TASK" | tr '[:upper:] ' '[:lower:]-' | tr -cd '[:alnum:]-' | cut -c1-40)"
  BRANCH="agent/${SLUG}-${TIMESTAMP}"

  echo ""
  echo "→ Dispatching: $TASK"
  echo "  Branch will be: $BRANCH"

  claude agents \
    --task "$TASK" \
    --worktree \
    --model claude-sonnet-5 \
    --permission-mode auto \
    --background \
    2>&1 | tail -1

  echo "  Agent running in background — draft PR will appear when done."
done

echo ""
echo "All agents dispatched. Monitor with: claude agents"
echo "Or wait for desktop notifications (agent_completed)."
```

Make executable: `chmod +x .claude/scripts/dispatch-agents.sh`

============================================================
PHASE 6: VALIDATE
============================================================

1. Confirm settings.json has `"defaultMode": "manual"`:
   ```
   cat .claude/settings.json | jq '.defaultMode'
   ```
   Expected: `"manual"`

2. Confirm Notification hook is wired:
   ```
   cat .claude/settings.json | jq '.hooks.Notification'
   ```
   Expected: array with one entry matching `agent_needs_input|agent_completed`

3. Confirm notify.sh is executable:
   ```
   ls -la .claude/hooks/notify.sh
   ```
   Expected: `-rwxr-xr-x`

4. Dry-run notify.sh with a synthetic agent_completed event:
   ```bash
   echo '{"event":"agent_completed","agentDescription":"test agent","sessionId":"test-123"}' \
     | .claude/hooks/notify.sh
   ```
   Expected: desktop notification fires, exit 0, log entry written to `.claude/agent-events.log`

5. Confirm dispatch script is executable:
   ```
   ls -la .claude/scripts/dispatch-agents.sh
   ```

============================================================
PHASE 7: REPORT
============================================================

Output a summary:

```
BACKGROUND AGENT PR DRIVER — SETUP COMPLETE

Configuration:
  ✓ defaultMode: manual
  ✓ model: claude-sonnet-5
  ✓ Notification hook: agent_needs_input|agent_completed → notify.sh

Files installed:
  ✓ .claude/hooks/notify.sh           (Notification hook — desktop alerts)
  ✓ .claude/scripts/dispatch-agents.sh (Reference dispatch workflow)

Manual step:
  → Inside Claude Code, run /config → Dynamic workflow size → choose small/medium/large

How to use:
  # Dispatch agents in the morning
  ./.claude/scripts/dispatch-agents.sh \
    "Add pagination to /skills API" \
    "Write integration tests for /auth/refresh" \
    "Migrate users table to UUID primary keys"

  # Agents run in background, open draft PRs, fire desktop notifications
  # You review PRs on GitHub — no terminal watching required

Audit log: .claude/agent-events.log
```

============================================================
STRICT RULES
============================================================

- Never override an existing `"defaultMode": "auto"` — the user may have intentionally set it for CI use. Only set `"manual"` if the field is unset or was `"default"`.
- Never install hooks that make outbound network calls without documenting them in the report.
- If git remote is not configured, emit a warning: "Auto-PR requires a git remote. Run: git remote add origin <url>".
- If jq is not installed, abort and output: "Install jq first: brew install jq / apt install jq".
- Always make scripts executable (chmod +x) after writing.
- The dispatch script runs agents with `--permission-mode auto` — document this explicitly in the report so the user understands agents will run autonomously.
