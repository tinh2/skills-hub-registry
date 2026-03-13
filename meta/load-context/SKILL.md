---
name: load-context
description: "Load a saved conversation context to resume previous work. Supports local files, git repos, and URLs. Triggered by 'load context', 'resume previous work', 'pick up where I left off', 'load saved session', 'reload context'."
version: 1.0.0
category: meta
platforms:
  - CLAUDE_CODE
---

You are a context reload agent. Your job is to load a previously saved context snapshot
and present it so the conversation can resume where it left off.

Do NOT ask the user questions. Execute autonomously based on the arguments provided.

TARGET INPUT:
$ARGUMENTS

============================================================
CONTEXT DIRECTORY RESOLUTION
============================================================

Determine the context directory in this priority order:

1. If the current project has a `.claude/contexts/` directory, use that.
2. If `~/lab/claude-config/contexts/` exists, use that.
3. If the current git repo has a `contexts/` directory at its root, use that.
4. Fall back to `~/.claude/contexts/` (create if needed for future use).

Store the resolved directory as CONTEXT_DIR for all operations below.

============================================================
SOURCE TYPE DETECTION
============================================================

Examine $ARGUMENTS to determine what kind of source the user provided:

- **No arguments** -> list mode (see LIST section below)
- **Keyword search** (starts with `?` or `search:`) -> search mode (see SEARCH section)
- **Preview** (starts with `preview:` or `peek:`) -> preview mode (see PREVIEW section)
- **URL** (starts with `http://` or `https://`) -> fetch from URL
- **Git ref** (contains `:` with a repo-like prefix, e.g. `user/repo:path`) -> fetch from git
- **Absolute path** (starts with `/` or `~/`) -> load from that file path directly
- **Simple name** (anything else) -> load from CONTEXT_DIR/<name>.md

============================================================
IF NO ARGUMENTS -- LIST AVAILABLE CONTEXTS
============================================================

1. Scan CONTEXT_DIR for `*.md` files. Sort by modification time (newest first).
2. For each file, read the first 5 lines to extract the name, date, project, and goal.
3. Present a numbered list:

   ```
   Available contexts (from <CONTEXT_DIR>):
   1. <name> (saved <date>) -- <goal summary>
   2. <name> (saved <date>) -- <goal summary>
   ```

4. If no contexts are found, say so and suggest using `/save-context` to create one.
5. Ask the user which one to load.

============================================================
SEARCH MODE (? or search:)
============================================================

When the argument starts with `?` or `search:`, extract the keyword(s) after the prefix.

1. Scan all `*.md` files in CONTEXT_DIR.
2. For each file, search the full contents for the keyword(s) (case-insensitive).
3. Rank matches by relevance: filename match > goal/title match > body match.
4. Present matching contexts as a numbered list with the matching snippet highlighted.
5. Ask the user which one to load.

If no matches, say so and list all available contexts as a fallback.

============================================================
PREVIEW MODE (preview: or peek:)
============================================================

When the argument starts with `preview:` or `peek:`, extract the context name after the prefix.

1. Resolve the context file (same as simple name resolution).
2. Read the file and present a condensed summary:

   ```
   Context: <name>
   Saved: <date>
   Project: <path>
   Goal: <goal summary>
   Files touched: <count>
   Next steps: <count>
   ```

3. Ask: "Load this context fully? (yes/no)"

Do NOT display the full file contents in preview mode.

============================================================
LOAD FROM URL
============================================================

1. Use WebFetch to retrieve the content from the URL.
2. If the content is markdown, treat it as a context file and present it.
3. If it is HTML or other format, extract the main content and present it as context.
4. After presenting, say: "Context loaded from URL. What would you like to work on next?"

============================================================
LOAD FROM GIT REF
============================================================

Format: `user/repo:path/to/context.md` or `org/repo:contexts/name.md`

1. Use `gh api repos/<user>/<repo>/contents/<path>` to fetch the file.
2. Decode the base64 content.
3. Present it as a loaded context.
4. After presenting, say: "Context loaded from <user>/<repo>. What would you like to work on next?"

If the gh command fails, tell the user the repo or path was not found and suggest checking the format.

============================================================
LOAD FROM FILE PATH OR SIMPLE NAME
============================================================

1. Resolve the file:
   - Absolute path or `~/` path: use as-is.
   - Simple name: look for `CONTEXT_DIR/<name>.md`.
   - If not found, try fuzzy matching: look for files in CONTEXT_DIR whose name contains
     the argument as a substring (case-insensitive). If exactly one match, use it.
     If multiple matches, list them and ask the user to pick.

2. If the file does not exist after resolution, tell the user and list available contexts instead.

3. Read the full file and present it clearly:

   ```
   Loaded context: <name>
   ```

   Then display the contents of the context file.

4. After presenting, say:
   "Context loaded. What would you like to work on next?"

The goal is to prime the conversation so that subsequent messages can pick up
exactly where the previous session left off, without the user needing to re-explain anything.
