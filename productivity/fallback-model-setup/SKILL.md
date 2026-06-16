---
name: fallback-model-setup
description: "Configures Claude Code's fallbackModel chain, --safe-mode troubleshooting protocol, and /cd workspace hygiene for production-resilient autonomous coding sessions. Audits current settings, installs the optimal three-model fallback chain, and documents a fast debugging loop. Requires Claude Code v2.1.166+."
version: "1.0.0"
category: productivity
platforms:
  - CLAUDE_CODE
---

You are configuring Claude Code for production resilience. Work autonomously — do not ask questions.

TARGET: $ARGUMENTS (defaults to current project if not specified)

============================================================
PHASE 1: AUDIT CURRENT CONFIGURATION
============================================================

1. LOCATE SETTINGS FILES
   Find all active settings files in order of precedence:
   - ~/.claude/settings.json (user-global)
   - <project>/.claude/settings.json (project-level)
   - <project>/.claude/settings.local.json (local overrides, gitignored)

   For each file found, record:
   - Current `model` value
   - Whether `fallbackModel` is already set (and its current value)
   - Whether `autoMode` is configured
   - Hook definitions (PreToolCall, PostToolCall, Stop, etc.)
   - Plugin and skill configuration

2. CHECK CLAUDE CODE VERSION
   Run: claude --version

   fallbackModel, --safe-mode, and /cd all require v2.1.166 or higher.
   If the installed version is older, output the upgrade command and stop:
   ```
   npm install -g @anthropic-ai/claude-code@latest
   ```

3. IDENTIFY RUNNING ENVIRONMENT
   Check environment variables for CI context: CI, GITHUB_ACTIONS, CIRCLECI,
   BUILDKITE, JENKINS_URL, TRAVIS.

   Record environment type:
   - CI/CD pipeline: benefits most from fallbackModel (prevents failed overnight runs)
   - Developer workstation: benefits most from --safe-mode and /cd hygiene
   - Both: configure everything

============================================================
PHASE 2: CONFIGURE FALLBACKMODEL CHAIN
============================================================

1. DETERMINE PRIMARY MODEL
   Read `model` from the effective settings.json. If unset, the runtime
   default is claude-opus-4-8.

2. WRITE FALLBACK CHAIN
   Apply to the project-level .claude/settings.json (create if absent).
   Use descending capability — most capable first, Haiku as the budget
   safety net:

   If primary is claude-opus-4-8:
   ```json
   {
     "model": "claude-opus-4-8",
     "fallbackModel": [
       "claude-sonnet-4-6",
       "claude-haiku-4-5-20251001"
     ]
   }
   ```

   If primary is claude-sonnet-4-6:
   ```json
   {
     "model": "claude-sonnet-4-6",
     "fallbackModel": [
       "claude-haiku-4-5-20251001"
     ]
   }
   ```

   If primary is already Haiku — no fallback exists. Flag this and
   recommend upgrading to Sonnet or Opus as the primary for any autonomous
   pipeline, then adding Haiku as the fallback.

3. VERIFY TOOL CAPABILITY ALIGNMENT
   Check whether the project uses tools that not all models support:
   - Computer use: not supported on Haiku — remove from chain if present
   - Extended thinking: not supported on Haiku — remove from chain if present
   - Agent tool (sub-agents): supported on all current models

   If a mismatch is found, remove the incompatible model from the chain
   and add a comment explaining why in the settings file.

4. VALIDATE JSON SYNTAX
   After writing settings.json, verify it parses:
   ```bash
   node -e "JSON.parse(require('fs').readFileSync('.claude/settings.json','utf8'))" && echo OK
   ```
   Fix and re-validate if the check fails.

============================================================
PHASE 3: INSTALL SAFE-MODE TROUBLESHOOTING PROTOCOL
============================================================

1. CREATE OR UPDATE DEBUGGING RUNBOOK
   Create .claude/DEBUGGING.md (or append to it if it already exists):

   ```markdown
   ## Claude Code — Troubleshooting Protocol

   ### Step 1: Safe mode isolation
   If Claude Code behaves unexpectedly (loops, crashes, wrong tool use,
   unexpected prompts):

       claude --safe-mode

   Safe mode disables ALL customizations: CLAUDE.md, hooks, plugins,
   bundled skills. If the problem disappears → the culprit is in your
   config stack.

   ### Step 2: Layer bisect (when safe mode is clean)
   Re-enable layers one at a time, testing after each:
   1. Hooks (most common source of loops — check PreToolCall first)
   2. Plugins
   3. CLAUDE.md / nested .claude/ directories
   4. Bundled skills (`disableBundledSkills: false`)

   ### Step 3: Hook log inspection
   Hooks write to stderr by default. To capture hook output during a
   session, temporarily add verbose logging:

       "hooks": {
         "PreToolCall": [{
           "matcher": ".*",
           "hooks": [{"type": "command", "command": "echo \"[hook] $CLAUDE_TOOL_NAME\" >&2"}]
         }]
       }

   ### Step 4: Change directory without restarting
   To switch project root mid-session without losing context or cache:

       /cd <new-directory>

   Prompt cache is fully preserved. /cd does not rebuild context from
   scratch. Use it instead of opening a new session.

   ### Step 5: Fallback model verification
   If you suspect a fallbackModel switch caused unexpected behavior,
   check the session log (~/.claude/logs/) for lines containing
   "fallback" to confirm which model was active at each point.
   ```

2. VERIFY HOOK STDERR OUTPUT (IF HOOKS EXIST)
   For any existing hook command, confirm it writes actionable output to
   stderr on failure. A hook that silently exits non-zero is harder to
   debug than one that prints a clear error message. Update any silent
   hooks to log to stderr:
   ```bash
   <your-hook-command> || echo "[hook failed] <hook-name>" >&2
   ```

============================================================
PHASE 4: AUDIT NESTED SUB-AGENT DEPTH (IF APPLICABLE)
============================================================

1. SCAN FOR AGENT DEFINITIONS
   Check .claude/agents/*.md for sub-agent definitions. If no agent files
   exist, skip this phase and note "no agent files found."

2. AUDIT DEPTH CONSTRAINTS
   With v2.1.166+, sub-agents nest up to 5 levels deep. For each agent
   file found:
   - Determine whether it spawns child sub-agents
   - Estimate the maximum pipeline depth
   - Flag any pipelines exceeding depth 3 (they should be intentional and
     justified with a comment)

   Recommended depth budget:
   - Level 1: Orchestrator (parent session)
   - Level 2: Domain specialists (implement, test, review)
   - Level 3: Per-file workers (optional)
   - Levels 4–5: Reserved for deep recursive analysis only

3. ENSURE CHILD FAILURE HANDLING
   For each sub-agent that spawns children, verify its system prompt
   includes explicit failure handling. If it doesn't, add:

   ```
   If any child sub-agent fails its acceptance criteria, halt immediately
   and surface the child's transcript to the parent. Do not auto-retry.
   ```

   Auto-retry masks real problems. Hard-fail with transcript is the correct
   default.

============================================================
OUTPUT
============================================================

Produce a concise audit report:

### Claude Code Production Resilience Audit

**Claude Code version:** [installed version] — [OK ≥ 2.1.166 / UPGRADE REQUIRED]

**fallbackModel chain:**
- Primary: [model]
- Fallback 1: [model or "not configured"]
- Fallback 2: [model or "not configured"]
- Capability mismatches removed: [list or "none"]

**Safe mode:** [available / not available — old version]
**Debugging runbook:** [created at .claude/DEBUGGING.md / updated / already exists]

**Sub-agent audit:**
- Agent definition files found: [count]
- Estimated max pipeline depth: [N levels]
- Failure-handling gaps fixed: [count]
- Depth concerns: [list or "none"]

**Files modified:**
- [list each file and what changed]

**Next steps (manual):**
- [anything requiring action outside this session]

============================================================
SELF-HEALING VALIDATION (max 2 iterations)
============================================================

After producing output, validate:

1. All modified JSON files parse without errors.
2. The fallbackModel array contains only valid model IDs (no typos).
3. .claude/DEBUGGING.md exists and contains non-empty content.
4. If version check failed, the upgrade command is clearly stated.

If any check fails:
- Fix the failing item
- Re-run only that check
- Update the report

After 2 iterations, note any remaining gaps and stop.
