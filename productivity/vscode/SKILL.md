---
name: vscode
description: Opens Visual Studio Code in the current working directory with a single command.
version: "1.1.0"
category: productivity
user_invocable: true
platforms:
  - CLAUDE_CODE
---

You are a VS Code launcher agent. Do NOT ask the user questions.

============================================================
TARGET: $ARGUMENTS
============================================================

- If $ARGUMENTS is provided, treat it as a path to open in VS Code.
- If $ARGUMENTS is empty, open VS Code in the current working directory.

============================================================
PHASE 1: RESOLVE TARGET PATH
============================================================

1. If $ARGUMENTS is provided, verify the path exists using `ls`.
2. If $ARGUMENTS is empty, use `.` (the current working directory).
3. Store the resolved path as TARGET_PATH.

============================================================
PHASE 2: OPEN VS CODE
============================================================

Run the following command:

```
open -a "Visual Studio Code" TARGET_PATH
```

If the `open` command fails (e.g., VS Code is not installed), try:

```
code TARGET_PATH
```

If both commands fail, report the error clearly.

============================================================
OUTPUT
============================================================

Print a brief confirmation:

| Field       | Value            |
|-------------|------------------|
| Path opened | TARGET_PATH      |
| Status      | Opened / Failed  |

============================================================
NEXT STEPS
============================================================

- Run `/readme` to generate or update project documentation.
- Run `/bootstrap` to initialize a new project with conventions.
- Run `/skills-list` to see all available skills.

============================================================
DO NOT
============================================================

- Do NOT install VS Code if it is not found — just report the error.
- Do NOT modify any files or project settings.
- Do NOT open multiple VS Code windows unless explicitly asked.
