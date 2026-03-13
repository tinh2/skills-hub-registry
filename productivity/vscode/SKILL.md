---
name: vscode
description: Open VS Code to edit files or directories. Triggered by "open VS Code", "open editor", "open in VS Code", "code .", "edit in vscode".
version: 2
category: productivity
user_invocable: true
platforms:
  - CLAUDE_CODE
---

Open Visual Studio Code using the `code` CLI, which works cross-platform (Linux, macOS, Windows).

## Default (current directory)

If no path is specified, open the current working directory:

```
code .
```

## Specific file or directory

If the user specifies a file or directory, open that path:

```
code <path>
```

Multiple files can be opened at once:

```
code <file1> <file2>
```

## Rules

- Do not ask any questions. Just open it and confirm it's done.
- Always use `code` (not `open -a "Visual Studio Code"`).
- If `code` is not found, tell the user to install the VS Code CLI: open VS Code, press Cmd+Shift+P / Ctrl+Shift+P, run "Shell Command: Install 'code' command in PATH".
