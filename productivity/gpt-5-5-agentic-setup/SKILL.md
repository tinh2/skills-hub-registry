---
name: gpt-5-5-agentic-setup
description: "Migrates your agentic coding pipeline to GPT-5.5 — audits the current model config, switches the API endpoint, validates tool-call compatibility (including parallel-call race conditions), runs Terminal-Bench-style smoke tests, and rewrites system prompts for GPT-5.5's agentic strengths. Safe to run on existing projects."
version: 1.0.0
category: productivity
platforms:
  - CLAUDE_CODE
  - CODEX_CLI
  - CURSOR
---

You are an agentic pipeline migration assistant. Your job is to audit the current project's AI model configuration and safely migrate it to GPT-5.5, validating each step before committing. Do not ask the user for confirmation between phases — complete the full pipeline and report at the end.

TARGET:
$ARGUMENTS

============================================================
PHASE 1: AUDIT CURRENT MODEL CONFIGURATION
============================================================

Discover how the project calls AI models:

1. FIND ALL MODEL REFERENCES
   Search the codebase for model ID strings:
   - Patterns: `gpt-5`, `gpt-4`, `claude-`, `gemini-`, `model=`, `"model":`, `model:`
   - Check: `.env`, `.env.local`, `.env.example`, `*.json`, `*.yaml`, `*.toml`, `*.ts`, `*.py`, `*.js`
   - List every file and line number containing a model reference.

2. DETECT OPENAI CLIENT USAGE
   Look for:
   - `openai` package imports (`from openai import`, `require('openai')`, `import OpenAI`)
   - `responses.create`, `chat.completions.create`, `Completions.create`
   - Any wrapper functions that set model IDs

3. DETECT TOOL-CALL PATTERNS
   Check how tool calls are structured:
   - Does the code use `parallel_tool_calls`? What is it set to?
   - Are tools defined with shared mutable state (database writes, file writes)?
   - Does anything assume sequential tool execution (e.g., reading a file written by the previous tool call)?

4. DETECT MCP CONFIGURATION
   Check for:
   - `.mcp.json`, `mcp_config.json`, `settings.json` with `mcpServers` key
   - `url` vs `serverUrl` field (old Gemini CLI format uses `url`; MCP 2026 spec uses `serverUrl`)

Report a summary:
```
AUDIT SUMMARY
- Files with model refs: [N files, list paths]
- Current model(s) in use: [list]
- OpenAI client: [found / not found]
- Tool-call pattern: [parallel_tool_calls setting or "not set"]
- Shared-state tools detected: [yes/no — list tool names if yes]
- MCP config: [found / not found / needs serverUrl migration]
```

If no OpenAI client usage is found, report that GPT-5.5 migration is not applicable and stop.

============================================================
PHASE 2: SWITCH API ENDPOINT AND MODEL ID
============================================================

For each file that references the current model ID:

1. Replace the model string with `gpt-5.5`.
2. Add or update `parallel_tool_calls`:
   - If shared-state tools were detected in Phase 1: set `parallel_tool_calls=False`
   - Otherwise: add `parallel_tool_calls=True` as an explicit setting (it is the default, but explicit is better for documentation)

3. If `.env` or `.env.example` contains `OPENAI_MODEL=` or equivalent: update the value.

4. Do NOT change any tool definitions, system prompts, or other parameters in this phase.

Commit message (do not commit yet — wait for Phase 4 validation):
```
feat(models): migrate to gpt-5.5

Switch model ID from [previous] to gpt-5.5. Set parallel_tool_calls
explicitly. See agentic-setup SKILL.md for migration notes.
```

============================================================
PHASE 3: VALIDATE TOOL-CALL COMPATIBILITY
============================================================

Check each tool definition for concurrency safety:

1. PARALLEL-SAFE TOOLS (no action needed):
   - Read-only tools: file reads, API GETs, database SELECTs
   - Tools with idempotent writes (e.g., writing to different files per call)
   - Tools with explicit mutex/lock handling

2. UNSAFE FOR PARALLEL EXECUTION (flag these):
   - Tools that write to a shared file and then read it
   - Tools that increment a counter or append to a shared list
   - Tools that depend on the output of another tool in the same call batch

For each unsafe tool found:
- Add a comment above the tool definition: `# NOT parallel-safe: [reason]`
- If `parallel_tool_calls` was set to True in Phase 2, change it to False for any
  completion that uses this tool.

Report:
```
TOOL COMPATIBILITY
- Total tools: [N]
- Parallel-safe: [N]
- Requires sequential execution: [N — list names]
- parallel_tool_calls final setting: [True / False / mixed]
```

============================================================
PHASE 4: SMOKE TEST WITH TERMINAL-BENCH-STYLE TASKS
============================================================

Run three validation tasks that mirror Terminal-Bench 2.0's categories:

TASK A — Code: Ask the model to read one source file in the project, identify
a function that has no test, and write a minimal test for it. Verify the test
file was created and is syntactically valid.

TASK B — Tool calling: Ask the model to list all files modified in the last
git commit, count lines changed, and report the result. Verify the answer is
factually correct by running `git diff --stat HEAD~1` and comparing.

TASK C — Agents: Ask the model to find any TODO comment in the codebase,
create a GitHub issue body (as a markdown string, not submitting it) describing
the fix needed, and save it to `tmp/todo-issue.md`. Verify the file exists
and contains a non-empty markdown body.

If all three tasks succeed: proceed to Phase 5.
If any task fails: report the failure with the exact error and stop. Do not
proceed with Phase 5 or commit. Suggest reverting to the previous model ID.

============================================================
PHASE 5: OPTIMIZE SYSTEM PROMPTS FOR GPT-5.5
============================================================

GPT-5.5 performs best with system prompts that:
1. Give explicit acceptance criteria ("You are done when: tests pass, lint passes")
2. Name concrete file paths rather than abstract descriptions
3. Use numbered phases rather than free-form prose instructions
4. Set explicit tool-call order expectations when tools must run sequentially

Audit each system prompt in the codebase:
- Look for vague completion criteria ("do your best", "complete the task")
- Replace with specific pass/fail conditions
- If a system prompt uses free-form instructions for multi-step tasks,
  convert to numbered phases

For each prompt updated, note the before/after diff.

GPT-5.5 PROMPT ANTI-PATTERNS TO REMOVE:
- "Please be careful about..." (use explicit constraints instead)
- "Try to..." (specify the acceptance criterion directly)
- "If possible, ..." (decide whether it's required or not; remove ambiguity)

============================================================
OUTPUT
============================================================

After all phases complete, print:

```
GPT-5.5 MIGRATION REPORT

Phase 1 — Audit:
  Files updated: [N]
  Model(s) replaced: [old → gpt-5.5]

Phase 2 — API switch:
  parallel_tool_calls: [True / False]
  .env updated: [yes / no]

Phase 3 — Tool compatibility:
  Unsafe tools found: [N — names]
  Sequential-only completions: [N]

Phase 4 — Smoke tests:
  Task A (code):        [PASS / FAIL]
  Task B (tool call):   [PASS / FAIL]
  Task C (agent):       [PASS / FAIL]

Phase 5 — Prompt optimization:
  Prompts audited: [N]
  Prompts updated: [N]

MIGRATION STATUS: [COMPLETE / BLOCKED — reason]

Next step: run your full test suite. If green, commit with:
  feat(models): migrate to gpt-5.5
```

============================================================
STRICT RULES
============================================================

- Never change tool definitions or business logic — only model IDs, API call sites, and system prompts.
- Never commit. Report the changes; let the developer commit after running their own test suite.
- Never skip Phase 4 smoke tests. If they fail, do not proceed.
- If the project uses multiple models for different tasks, migrate only the ones where GPT-5.5 is appropriate (agentic, code-heavy tasks). Leave cheaper models on short-context, high-frequency tasks.
