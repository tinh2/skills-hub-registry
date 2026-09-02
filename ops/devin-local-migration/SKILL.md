---
name: devin-local-migration
description: "Audits a repository for all Cascade (legacy Windsurf local agent) references and migrates them to Devin Local."
version: "1.0.1"
category: ops
platforms:
  - CLAUDE_CODE
  - CURSOR
  - CODEX_CLI
---

You are an autonomous migration agent. Audit the current repository for all Cascade references and produce a migration to Devin Local. Do not ask for confirmation — find, patch, and report.

TARGET:
$ARGUMENTS (defaults to current working directory if empty)

============================================================
PHASE 1: DISCOVERY
============================================================

Grep the repo for all Cascade references. Search these file types:

```shell
grep -rI \
  --include="*.yml" --include="*.yaml" \
  --include="*.sh" --include="Makefile" \
  --include="*.json" --include="*.md" \
  --include="*.toml" --include="*.env*" \
  -l "cascade" . 2>/dev/null | sort
```

Also check for binary references and hidden directories:

```shell
grep -rI --include="*.yml" --include="*.yaml" \
  --include="*.sh" --include="Makefile" \
  -n "cascade" . 2>/dev/null
```

Catalog all findings into three buckets:

**BUCKET A — Safe string replacement**
- GitHub Actions workflow files (`*.yml` / `*.yaml` in `.github/workflows/`)
- Shell scripts (`*.sh`, `scripts/**`)
- Makefile targets
- Agent rule files (`.windsurf/rules/`, `.devin/rules/`)
- Package scripts in `package.json`

**BUCKET B — Structural review needed**
- Custom tool definitions (`*.py`, `*.js`) in `.windsurf/tools/` or `.devin/tools/`
- Any file that imports from a `cascade` Python package
- Config files that reference `cascade` as a named agent type with custom options

**BUCKET C — Documentation only (low risk)**
- README files and Markdown docs that mention Cascade
- CHANGELOG entries
- Comment blocks in source code

Output:
```
DISCOVERY REPORT
Total files with Cascade references: N
  Bucket A (safe replacement): N files
  Bucket B (structural review): N files
  Bucket C (docs only): N files
```

If total files = 0: output "No Cascade references found — migration already complete." and stop.

============================================================
PHASE 2: BUCKET A MIGRATION
============================================================

For each Bucket A file, apply these transformations:

1. **Binary/command references**
   - `cascade run` → `devin-local run`
   - `cascade agent` → `devin-local agent`
   - `cascade --task` → `devin-local --task`

2. **Agent name declarations**
   - `agent: cascade` → `agent: devin-local`
   - `"agent": "cascade"` → `"agent": "devin-local"`

3. **Environment variables**
   - `CASCADE_API_KEY` → `DEVIN_LOCAL_API_KEY` (update both declaration and usage)
   - `CASCADE_MODEL` → `DEVIN_LOCAL_MODEL`

4. **Path references**
   - `.windsurf/cascade/` → `.devin/` (if directory exists)
   - `windsurf-cascade` → `devin-local` in any slug or identifier

5. **GitHub Actions runner names**
   - `uses: cognition-ai/cascade-action` → `uses: cognition-ai/devin-local-action`

Apply changes with `sed` or direct file edits. Do not change comments or documentation (those are Bucket C).

After applying: run `git diff --stat` to show the scope of changes.

============================================================
PHASE 3: BUCKET B AUDIT
============================================================

For each Bucket B file:

1. Open and read the full file
2. Identify which Cascade-specific internals it uses:
   - Cascade Python subprocess model (import cascade / from cascade import)
   - Cascade plugin hooks (on_task_start, on_tool_call, etc.)
   - Cascade-specific context passing patterns

3. Assess rewrite complexity:
   - **Low**: Only the agent name needs changing, no internal API usage
   - **Medium**: Uses Cascade Python API but the logic maps directly to Devin Local's Rust FFI
   - **High**: Deep integration with Cascade internals — needs a full rewrite

Output per file:
```
FILE: .windsurf/tools/my-tool.py
Complexity: Medium
Uses: cascade.on_tool_call hook
Devin Local equivalent: devin_local::hooks::on_tool_call (Rust FFI) or MCP tool (recommended)
Action required: Rewrite as MCP tool for language-agnostic integration
```

**Recommended migration path for custom tools:**
Rewrite Cascade Python tool definitions as MCP servers instead of Devin Local Rust FFI. MCP tools work across all agents (Devin Local, Claude Agent, Codex) and don't require rewriting when you switch agents again.

Template:
```json
// .devin/tools/my-tool/mcp.json
{
  "name": "my-tool",
  "description": "What this tool does",
  "command": "node .devin/tools/my-tool/server.js",
  "protocol": "mcp"
}
```

============================================================
PHASE 4: ACP CONFIGURATION (OPTIONAL)
============================================================

If the repo has agent workflow rules that route to Cascade, check whether the team would benefit from ACP multi-agent routing to Devin Local + Claude Agent or Codex.

Look for routing rules in:
- `.windsurf/rules/*.md` (now `.devin/rules/*.md`)
- Any workflow file with conditional agent routing

If found, generate a sample ACP routing config:

```json
// .devin/agents/claude-agent.json
{
  "name": "claude-agent",
  "protocol": "acp",
  "command": "npx @anthropic-ai/claude-agent",
  "capabilities": ["code", "test", "review", "large-context"]
}
```

```json
// .devin/agents/codex.json
{
  "name": "codex",
  "protocol": "acp",
  "command": "npx @openai/codex",
  "capabilities": ["code", "test"]
}
```

Output this as a recommendation, not an automatic change. Include a one-line explanation of when to route to each agent.

============================================================
PHASE 5: DOCUMENTATION UPDATES (BUCKET C)
============================================================

For each Bucket C file:

- Add a brief note that Cascade references are historical (the agent reached EOL July 1, 2026)
- Update any "how to run locally" instructions that mention Cascade
- Replace Cascade setup steps with Devin Local equivalents

Do not alter CHANGELOG entries — those are historical records and should not be modified.

============================================================
PHASE 6: VALIDATION
============================================================

After applying all Bucket A changes:

1. Run `git diff` — verify only expected files changed
2. Check no new `cascade` references were introduced:
   ```shell
   grep -rI --include="*.yml" --include="*.sh" --include="Makefile" "cascade" .
   ```
3. If the repo has CI tests, run them:
   ```shell
   # Detect CI test runner
   if [ -f "package.json" ]; then pnpm test 2>/dev/null || npm test 2>/dev/null; fi
   if [ -f "Makefile" ]; then make test 2>/dev/null; fi
   ```
4. Verify the Devin Local binary is reachable if available:
   ```shell
   which devin-local 2>/dev/null || echo "devin-local not in PATH — install via Devin Desktop"
   ```

============================================================
OUTPUT
============================================================

## Devin Local Migration Report

### Summary
- Cascade references found: [N]
- Files auto-patched: [N] (Bucket A)
- Files needing manual review: [N] (Bucket B)
- Documentation updated: [N] (Bucket C)

### Auto-patched files
[list each file with the change summary]

### Manual review required
[list each Bucket B file with complexity rating and recommended action]

### ACP routing opportunity
[present if routing rules were found, otherwise omit]

### Validation
- Git diff: [N lines changed across N files]
- Remaining Cascade references: [0 / N (list if >0)]
- CI tests: [pass / fail / skipped — no test command found]

### Next steps
1. Review `git diff` before staging
2. For Bucket B files: rewrite as MCP tools (recommended) or Devin Local Rust FFI
3. Set `DEVIN_LOCAL_API_KEY` in your CI environment if `CASCADE_API_KEY` was used
4. Update Devin Desktop to the latest version to get Devin Local
5. Test your first Devin Local session interactively before relying on CI automation

============================================================
STRICT RULES
============================================================

- Never modify CHANGELOG entries — they are historical records
- Never auto-apply Bucket B changes — only report and recommend
- Never delete files — only patch them
- If grep returns zero results, report success and stop immediately
- If validation finds new Cascade references introduced by the patch, halt and report the regression
