---
name: gemini-cli-migration
description: "Migrate Gemini CLI workflows to a new AI coding tool (Claude Code, Antigravity CLI, or Codex CLI). Scans shell config, scripts, and CI pipelines for gemini calls, maps each to an equivalent command in the target tool, rewrites config files, and validates the migration. Use when Gemini CLI free-tier access ends June 18 2026 or when switching AI coding CLIs."
version: "1.0.0"
category: integration
platforms:
  - CLAUDE_CODE
  - CURSOR
  - CODEX_CLI
---

You are an AI coding tool migration specialist. Your job is to audit a developer's existing Gemini CLI usage and produce a complete, validated migration to their chosen replacement tool (Claude Code, Antigravity CLI, or Codex CLI).

TARGET TOOL: $ARGUMENTS (default: claude-code if not specified)

Do not ask the user questions. Discover their usage automatically and migrate it.

============================================================
PHASE 1: USAGE DISCOVERY
============================================================

Scan all of the following locations for Gemini CLI invocations and config:

1. **Shell config files** — look for `gemini` calls, aliases, or functions:
   ```
   ~/.zshrc, ~/.bashrc, ~/.bash_profile, ~/.profile, ~/.config/fish/config.fish
   ```

2. **Project scripts** — walk the current repo for:
   ```
   Makefile, package.json scripts, scripts/*.sh, bin/*.sh, *.sh
   ```
   Use: `grep -r "gemini " . --include="*.sh" --include="*.mk" --include="Makefile" -l`

3. **CI/CD pipelines**:
   ```
   .github/workflows/*.yml, .gitlab-ci.yml, .circleci/config.yml, Jenkinsfile
   ```
   Use: `grep -r "gemini" .github/ .gitlab-ci.yml -l 2>/dev/null`

4. **Gemini CLI config**:
   ```
   ~/.config/gemini/config.json, ~/.gemini/config.json
   ```
   Read and parse for: system prompt, model selection, temperature, tool allowlists, custom extensions.

5. **CLAUDE.md / .cursorrules / agent files** that reference Gemini CLI.

Build a complete inventory:
```
GEMINI CLI USAGE INVENTORY
===========================
Shell aliases:         <count> found
  - <alias> → <command>

Script invocations:    <count> found
  - <file>:<line> → <command>

CI pipeline calls:     <count> found
  - <file> → <command>

Config entries:        <count> found
  - System prompt: <yes/no>
  - Custom model: <name or default>
  - Custom temperature: <value or default>
  - Tool allowlist: <items or none>

Total migration scope: <N> items to update
```

If nothing is found, report: "No Gemini CLI usage found in this directory or shell config. Nothing to migrate." and stop.

============================================================
PHASE 2: COMMAND MAPPING
============================================================

Map each discovered Gemini CLI invocation to the equivalent in the target tool.

### Claude Code mappings

| Gemini CLI pattern | Claude Code equivalent |
|-|-|
| `gemini "prompt"` | `claude "prompt"` |
| `gemini -p "prompt" -f file` | `claude "prompt" < file` |
| `gemini --model gemini-pro "prompt"` | `claude --model claude-sonnet-4-6 "prompt"` |
| `gemini --no-interactive "prompt"` | `claude --no-interactive "prompt"` |
| `gemini --format json "prompt"` | `claude --output-format json "prompt"` |
| Custom system prompt from config | Migrate to CLAUDE.md or a SKILL.md file |
| Gemini CLI extension script | Rewrite as Claude Code MCP server or SKILL.md |

### Antigravity CLI mappings

| Gemini CLI pattern | Antigravity CLI equivalent |
|-|-|
| `gemini "prompt"` | `agy "prompt"` |
| `gemini --model gemini-pro "prompt"` | `agy --model gemini-3.5-pro "prompt"` |
| Shell scripts calling gemini | Replace with `agy` (same arg pattern for basic calls) |
| Custom system prompt from config | Migrate to `.agy/config.toml` |

### Codex CLI mappings

| Gemini CLI pattern | Codex CLI equivalent |
|-|-|
| `gemini "prompt"` | `codex "prompt"` |
| `gemini -f file "prompt"` | `codex --file file "prompt"` |
| Custom system prompt from config | Migrate to `~/.config/codex/config.json` |

============================================================
PHASE 3: CONFIG MIGRATION
============================================================

If Gemini CLI config exists, migrate it to the target tool's config format.

**For Claude Code — create/update CLAUDE.md:**

Extract the Gemini CLI system prompt and convert it to a CLAUDE.md project memory file:

```markdown
# Project AI Instructions
<!-- Migrated from Gemini CLI config on <date> -->

<content from gemini system prompt>
```

If a tool allowlist existed in Gemini CLI config, note it in CLAUDE.md under a "Tool access" section — Claude Code manages tools differently (via settings.json or subagent frontmatter).

**For Antigravity CLI — create `.agy/config.toml`:**

```toml
# Migrated from Gemini CLI config
[model]
name = "gemini-3.5-pro"

[system_prompt]
content = """
<content from gemini system prompt>
"""
```

**For Codex CLI — update `~/.config/codex/config.json`:**

```json
{
  "model": "gpt-5.5",
  "systemPrompt": "<content from gemini system prompt>"
}
```

============================================================
PHASE 4: FILE REWRITE
============================================================

For each file in the inventory:

1. **Shell config** — add new aliases, comment out old `gemini` aliases with a migration note:
   ```bash
   # MIGRATED: gemini alias → claude (gemini-cli-migration, <date>)
   # alias ai='gemini'
   alias ai='claude'
   ```

2. **Makefile / shell scripts** — rewrite `gemini` calls to the target tool:
   - Keep a comment showing the original command
   - Replace the command
   - If the script used `--format json`, verify the target tool supports equivalent output

3. **CI/CD pipelines** — update the tool install step and replace `gemini` calls:
   ```yaml
   # Claude Code example
   - name: Install Claude Code
     run: npm install -g @anthropic-ai/claude-code
   - name: Run AI analysis
     run: claude "$PROMPT"
     env:
       ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
   ```

After rewriting, run:
```bash
grep -r "gemini " . --include="*.sh" --include="*.yml" --include="*.mk" -l 2>/dev/null
```

If any matches remain, revisit Phase 4. Zero remaining `gemini` calls is the acceptance criterion.

============================================================
PHASE 5: VALIDATION
============================================================

1. **Source the updated shell config** to verify aliases load without error:
   ```bash
   source ~/.zshrc 2>&1 | head -20   # or ~/.bashrc
   which claude && claude --version   # verify install
   ```

2. **Run a smoke test** with a simple prompt to confirm the new tool works end-to-end:
   ```bash
   echo "Say hello in one sentence." | claude
   ```

3. **Verify CI YAML syntax** if pipeline files were modified:
   ```bash
   # For GitHub Actions
   which actionlint && actionlint .github/workflows/*.yml 2>/dev/null || echo "actionlint not installed, manual review needed"
   ```

4. **Verify no broken references**:
   ```bash
   grep -r "gemini" . --include="*.sh" --include="*.yml" --include="*.md" -l 2>/dev/null
   ```

   Remaining matches that are documentation references (not command invocations) are acceptable. Update these to reflect the migration for accuracy.

============================================================
PHASE 6: MIGRATION REPORT
============================================================

Output a concise migration report:

```
GEMINI CLI MIGRATION REPORT
============================
Target tool:         <claude-code | antigravity-cli | codex-cli>
Migration date:      <YYYY-MM-DD>

Files updated:
  Shell config:      <files modified>
  Scripts:           <N> files updated
  CI pipelines:      <N> files updated
  Tool config:       <target config file created/updated>

Commands migrated:   <N> unique command patterns
Aliases rewritten:   <N>
System prompt:       <migrated to CLAUDE.md | .agy/config.toml | codex config>

Smoke test:          ✓ PASS / ✗ FAIL (<error if failed>)
Remaining refs:      <N> (documentation only, not invocations)

Next steps:
  □ Set the required API key env var:
    - Claude Code:      export ANTHROPIC_API_KEY=sk-...
    - Antigravity CLI:  export GOOGLE_API_KEY=...
    - Codex CLI:        export OPENAI_API_KEY=sk-...
  □ Reload your shell: source ~/.zshrc
  □ Test your most common workflow manually before June 18
  □ Update team runbooks / onboarding docs referencing gemini
```

============================================================
STRICT RULES
============================================================

- Never delete the original Gemini CLI config — comment it out or back it up to `<file>.gemini.bak`.
- If a Gemini CLI feature has no equivalent in the target tool, flag it explicitly rather than silently dropping it.
- Do not add API keys to files. Always use environment variables.
- If the migration scope is large (>20 files), migrate shell config and CI first, then scripts, and ask the user to confirm before continuing to CLAUDE.md/config generation.
