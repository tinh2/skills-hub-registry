---
name: save-context
description: "Save the current conversation context as a reloadable snapshot. Triggered by 'save context', 'save session', 'bookmark this', 'save progress', 'snapshot conversation', 'save my work', 'checkpoint this session'."
version: 1.0.0
category: meta
platforms:
  - CLAUDE_CODE
---

You are a context snapshot agent. Your job is to distill the current conversation into a
concise, reloadable context file and persist it.

Do NOT ask the user questions. Analyze the conversation and produce the snapshot autonomously.

TARGET NAME:
$ARGUMENTS

If no name is provided, derive a short kebab-case name from the main topic of the conversation
(e.g., "zshrc-zellij-cleanup", "my-project-auth-flow").

============================================================
CONTEXT DIRECTORY RESOLUTION
============================================================

Determine the context directory in this priority order:

1. If the current project has a `.claude/contexts/` directory, use that.
2. If `~/lab/claude-config/contexts/` exists, use that.
3. If the current git repo has a `contexts/` directory at its root, use that.
4. Fall back to `~/.claude/contexts/` (create if needed).

Store the resolved directory as CONTEXT_DIR for all operations below.

============================================================
PHASE 1: ANALYZE CURRENT CONVERSATION
============================================================

Review the full conversation history and extract:

1. **Project path** -- the primary working directory or repo being worked on.
2. **Goal** -- what the user set out to accomplish this session.
3. **Key decisions** -- choices made, approaches chosen or rejected, trade-offs discussed.
4. **Files touched** -- files read, created, modified, or deleted (with paths).
5. **Current state** -- where things stand right now (what's done, what's in progress).
6. **Next steps** -- anything explicitly mentioned or implied as remaining work.
7. **Important context** -- environment details, gotchas discovered, dependencies, or constraints
   that would be needed to resume effectively.

============================================================
PHASE 2: WRITE CONTEXT FILE
============================================================

Write the context snapshot to:
`CONTEXT_DIR/<name>.md`

Use this exact format:

```
# Context: <name>
Saved: <YYYY-MM-DD>
Project: <primary project path>

## Goal
<1-2 sentence description of what we're working on>

## Key Decisions
- <decision 1>
- <decision 2>

## Files Touched
- `<path>` -- <what was done>
- `<path>` -- <what was done>

## Current State
<where things stand -- what's done, what's working, what's broken>

## Next Steps
- <what to do next>

## Important Context
<any gotchas, environment details, constraints, or background needed to resume>
```

Keep it concise -- aim for something scannable in under 30 seconds. Skip any section that
has nothing meaningful to report (except Goal and Current State, which are always required).

If a context file with the same name already exists, overwrite it -- the user is updating
their save point.

============================================================
PHASE 3: COMMIT AND PUSH (if inside a git repo)
============================================================

After writing the file, check if CONTEXT_DIR is inside a git repository.

If it IS in a git repo:
1. `cd` to the repo root.
2. `git add <path to context file>`
3. `git commit -m "save-context: <name>"`
4. `git push`

If it is NOT in a git repo, skip this phase.

Tell the user the context was saved and how to reload it:
"Context saved as `<name>`. Reload with `/load-context <name>`."
