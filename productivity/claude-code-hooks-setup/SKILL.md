---
name: claude-code-hooks-setup
description: "Autonomous Claude Code hooks configurator. Audits your project's existing .claude/settings.json hook setup, then installs a production-grade suite: PreToolUse safety enforcement (blocks rm -rf, sudo writes, secret leaks), PostToolUse auto-formatting and lint gates, SessionStart dynamic context injection, and FileChanged secret detection. Generates hook scripts and wires them into settings.json at project scope."
version: "1.0.0"
category: productivity
platforms:
  - CLAUDE_CODE
---

You are an autonomous Claude Code hooks configurator. Do NOT ask the user questions — audit, install, and verify.

TARGET PROJECT:
$ARGUMENTS

============================================================
PHASE 1: AUDIT EXISTING HOOKS
============================================================

1. Check for `.claude/settings.json` and `.claude/settings.local.json` in the project root.
   - If found, read and extract any existing `"hooks"` configuration.
   - List all configured events, matchers, and handler types.

2. Check for existing hook scripts in `.claude/hooks/`.
   - List any `.sh`, `.mjs`, `.py` scripts already present.

3. Check for `.claude/CLAUDE.md` — identify any instructions that should be enforced via hooks instead of advisory text (common candidates: "always run tests before committing", "never use rm -rf", "format files after editing").

4. Report findings:
   ```
   HOOKS AUDIT
   Configured events: [list or "none"]
   Existing hook scripts: [list or "none"]
   CLAUDE.md instructions that belong in hooks: [list]
   ```

============================================================
PHASE 2: DETECT PROJECT STACK
============================================================

Detect the project stack to configure the right formatters and linters:

- **JavaScript/TypeScript**: Look for `package.json`. Check for `prettier`, `eslint`, `biome` in `devDependencies`.
- **Python**: Look for `pyproject.toml`, `setup.py`, or `requirements.txt`. Check for `ruff`, `black`, `flake8`.
- **Rust**: Look for `Cargo.toml`.
- **Go**: Look for `go.mod`.
- **Ruby**: Look for `Gemfile`.
- **Monorepo**: Look for `pnpm-workspace.yaml`, `nx.json`, `turbo.json`.

Record: `STACK=[detected stack]`, `FORMATTER=[command]`, `LINTER=[command]`.

============================================================
PHASE 3: INSTALL HOOK SCRIPTS
============================================================

Create `.claude/hooks/` directory if it does not exist. Install the following scripts:

### 3a. PreToolUse safety check (`check-command.sh`)

```bash
#!/usr/bin/env bash
# claude-code-hooks-setup: PreToolUse safety enforcement
# Blocks destructive Bash commands and writes outside the project root.
set -euo pipefail

INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty')
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# Block destructive shell patterns
if [[ "$TOOL_NAME" == "Bash" ]]; then
  if echo "$COMMAND" | grep -qE '^\s*(rm\s+-[rRf]*f|sudo\s+rm|dd\s+if=|mkfs|shred)'; then
    jq -n '{
      hookSpecificOutput: {
        hookEventName: "PreToolUse",
        permissionDecision: "deny",
        permissionDecisionReason: "Destructive command blocked by project policy. Use targeted file deletions instead."
      }
    }'
    exit 0
  fi
fi

# Block writes outside project root
PROJECT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
if [[ -n "$FILE_PATH" && "$FILE_PATH" != "$PROJECT_ROOT"* ]]; then
  jq -n --arg path "$FILE_PATH" --arg root "$PROJECT_ROOT" '{
    hookSpecificOutput: {
      hookEventName: "PreToolUse",
      permissionDecision: "ask",
      permissionDecisionReason: ("File path " + $path + " is outside project root " + $root + " — confirm this is intentional.")
    }
  }'
  exit 0
fi

exit 0
```

Make executable: `chmod +x .claude/hooks/check-command.sh`

### 3b. PostToolUse formatter (`post-write.sh`)

Adapt based on detected stack:

**TypeScript/JavaScript (Prettier + ESLint)**:
```bash
#!/usr/bin/env bash
# claude-code-hooks-setup: PostToolUse auto-format
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

if [[ -z "$FILE_PATH" ]]; then exit 0; fi

# Only format source files
if [[ "$FILE_PATH" =~ \.(ts|tsx|js|jsx|mjs|cjs|css|json|md)$ ]]; then
  if command -v prettier &>/dev/null; then
    npx prettier --write "$FILE_PATH" 2>/dev/null || true
  fi
  
  LINT_STATUS="skipped"
  if [[ "$FILE_PATH" =~ \.(ts|tsx|js|jsx)$ ]]; then
    if npx eslint "$FILE_PATH" --max-warnings 0 2>/dev/null; then
      LINT_STATUS="passed"
    else
      LINT_STATUS="failed — run: npx eslint $FILE_PATH"
    fi
  fi
  
  jq -n --arg status "$LINT_STATUS" '{
    hookSpecificOutput: {
      hookEventName: "PostToolUse",
      additionalContext: ("Lint: " + $status)
    }
  }'
fi
exit 0
```

**Python (ruff)**:
```bash
#!/usr/bin/env bash
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')
if [[ "$FILE_PATH" =~ \.py$ ]]; then
  ruff format "$FILE_PATH" 2>/dev/null || true
  ruff check "$FILE_PATH" --fix 2>/dev/null || true
fi
exit 0
```

**Rust**:
```bash
#!/usr/bin/env bash
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')
if [[ "$FILE_PATH" =~ \.rs$ ]]; then
  rustfmt "$FILE_PATH" 2>/dev/null || true
fi
exit 0
```

**Go**:
```bash
#!/usr/bin/env bash
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')
if [[ "$FILE_PATH" =~ \.go$ ]]; then
  gofmt -w "$FILE_PATH" 2>/dev/null || true
fi
exit 0
```

Make executable: `chmod +x .claude/hooks/post-write.sh`

### 3c. SessionStart context injector (`session-start.sh`)

```bash
#!/usr/bin/env bash
# claude-code-hooks-setup: SessionStart — inject branch, env, and skill context
BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")
DIRTY=$(git status --short 2>/dev/null | wc -l | tr -d ' ')
ENV_STATUS="missing — copy .env.example before running"
[[ -f ".env" ]] && ENV_STATUS="found"

SKILL_LIST=$(ls .claude/skills/ 2>/dev/null | tr '\n' ', ' | sed 's/, $//')
[[ -z "$SKILL_LIST" ]] && SKILL_LIST="none"

NODE_VER=$(node --version 2>/dev/null || echo "not installed")
PKG_MANAGER=""
[[ -f "pnpm-lock.yaml" ]] && PKG_MANAGER="pnpm"
[[ -f "yarn.lock" ]] && PKG_MANAGER="yarn"
[[ -f "package-lock.json" ]] && PKG_MANAGER="npm"

jq -n \
  --arg branch "$BRANCH" \
  --arg dirty "$DIRTY" \
  --arg env "$ENV_STATUS" \
  --arg skills "$SKILL_LIST" \
  --arg node "$NODE_VER" \
  --arg pkg "$PKG_MANAGER" \
  '{
    hookSpecificOutput: {
      hookEventName: "SessionStart",
      reloadSkills: true,
      sessionTitle: ("branch: " + $branch),
      additionalContext: (
        "Git branch: " + $branch + " (" + $dirty + " uncommitted files)\n" +
        ".env: " + $env + "\n" +
        "Node: " + $node + " | Package manager: " + $pkg + "\n" +
        "Installed skills: " + $skills + "\n" +
        "Run /hooks to see all active lifecycle hooks."
      )
    }
  }'
```

Make executable: `chmod +x .claude/hooks/session-start.sh`

### 3d. FileChanged secret detector (`file-changed.sh`)

```bash
#!/usr/bin/env bash
# claude-code-hooks-setup: FileChanged — detect new secrets added to .env files
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.file_path // empty')

if [[ "$FILE_PATH" =~ \.env ]]; then
  # Check for patterns that look like new secrets
  if grep -qE '(SECRET|PASSWORD|API_KEY|TOKEN|PRIVATE_KEY)\s*=\s*\S+' "$FILE_PATH" 2>/dev/null; then
    jq -n --arg path "$FILE_PATH" '{
      systemMessage: ("Warning: secret-like values detected in " + $path + ". Verify this file is in .gitignore before committing."),
      hookSpecificOutput: {
        hookEventName: "FileChanged",
        additionalContext: "Secret detection: env file changed — check .gitignore coverage."
      }
    }'
  fi
fi
exit 0
```

Make executable: `chmod +x .claude/hooks/file-changed.sh`

============================================================
PHASE 4: WRITE settings.json
============================================================

Read the existing `.claude/settings.json` (or create it if absent). Merge in the hooks configuration — preserve any existing settings, do NOT overwrite them.

Target `hooks` block to merge:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/session-start.sh",
            "timeout": 15,
            "statusMessage": "Loading session context..."
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Bash|Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/check-command.sh",
            "timeout": 10,
            "statusMessage": "Checking command safety..."
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/post-write.sh",
            "timeout": 30,
            "statusMessage": "Formatting and linting..."
          }
        ]
      }
    ],
    "FileChanged": [
      {
        "matcher": "\\.env|\\.env\\..*",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/file-changed.sh",
            "async": true
          }
        ]
      }
    ]
  }
}
```

Write the merged result back to `.claude/settings.json`.

============================================================
PHASE 5: VALIDATE
============================================================

1. Verify all four hook scripts exist and are executable:
   ```
   ls -la .claude/hooks/
   ```

2. Verify `.claude/settings.json` contains a `"hooks"` key with all four events.

3. Dry-run the session-start script to confirm it produces valid JSON:
   ```
   echo '{}' | .claude/hooks/session-start.sh | jq .
   ```

4. Dry-run the safety check with a safe command to confirm exit 0:
   ```
   echo '{"tool_name":"Bash","tool_input":{"command":"echo hello"}}' | .claude/hooks/check-command.sh | jq .
   ```

5. Dry-run the safety check with a destructive command to confirm deny:
   ```
   echo '{"tool_name":"Bash","tool_input":{"command":"rm -rf /tmp/test"}}' | .claude/hooks/check-command.sh | jq .
   ```
   Expected: `permissionDecision: "deny"`

============================================================
PHASE 6: REPORT
============================================================

Output a summary:

```
HOOKS SETUP COMPLETE

Scripts installed:
  ✓ .claude/hooks/check-command.sh   (PreToolUse safety)
  ✓ .claude/hooks/post-write.sh      (PostToolUse formatter)
  ✓ .claude/hooks/session-start.sh   (SessionStart context)
  ✓ .claude/hooks/file-changed.sh    (FileChanged secrets)

settings.json events configured:
  ✓ SessionStart  → session-start.sh
  ✓ PreToolUse    → check-command.sh  (matcher: Bash|Write|Edit)
  ✓ PostToolUse   → post-write.sh     (matcher: Write|Edit)
  ✓ FileChanged   → file-changed.sh   (matcher: .env files)

Stack detected: [STACK]
Formatter: [FORMATTER]
Linter: [LINTER]

Validation: [PASS/FAIL with details]

Next steps:
- Run /hooks inside a Claude Code session to verify all hooks appear
- Commit .claude/settings.json and .claude/hooks/ to share with your team
- Add .claude/settings.local.json to .gitignore for user-specific overrides
```

============================================================
STRICT RULES
============================================================

- Never overwrite existing settings.json fields other than "hooks".
- Never install hooks that require network access without user acknowledgment.
- If jq is not installed, abort and instruct the user to install it first.
- Always make hook scripts executable (chmod +x) after writing them.
- Hook scripts must handle empty tool_input gracefully (exit 0 if no relevant input).
