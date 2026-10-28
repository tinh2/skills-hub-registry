---
name: clip
description: "Copy the snippet I recommended in my last response (a command, query, Slack or PR text) to the clipboard exactly, with no terminal wrap newlines. Use for '/clip', 'clip that', 'copy the command', 'put that on my clipboard'. /clip 2 picks the second snippet."
user-invocable: true
version: "1.0.0"
category: meta
platforms:
  - CLAUDE_CODE
---

Put the pasteable snippet from my most recent response on the clipboard, exactly as written. Use this instead of the built-in `/copy`, which copies the whole response, and instead of selecting text in the terminal, which picks up hard-wrap newlines and indentation.

## Step 1: Find the snippets

Look at my most recent response and list every snippet the user would paste or run:

- fenced code blocks (commands, SQL, config, `/compact` focus text)
- an inline command I told them to type
- a drafted message (Slack, PR description, Jira text) meant to be pasted

Skip prose, headings, explanations, and code shown only to illustrate something.

If the response has no such snippet, say so in one line and stop. Don't copy prose as a fallback.

## Step 2: Pick one

- With an argument: a number picks that snippet in order (`/clip 2`). A word picks the snippet that contains or is labeled by it (`/clip sql`).
- With no argument and one snippet: take it.
- With no argument and several: take the one the user acts on next, usually the first actionable one. List the others with numbers so they can run `/clip 2`.

## Step 3: Copy it exactly

- Copy the snippet's text only: no code fences, no backticks around inline code, no leading `$ ` or `> `, no trailing newline.
- Don't change the content. No reflowing, no edits to wording, dashes or quotes.
- Use a quoted heredoc so the shell interprets nothing, and strip the final newline:

```bash
cat <<'CLIP_EOF' | perl -pe 'chomp if eof' | pbcopy
<snippet text exactly>
CLIP_EOF
```

- Check it: `pbpaste | wc -l` must be 0 for a one-line snippet, or the snippet's real line count minus one for a multi-line one. `pbpaste | head -c 80` shows the start.

## Step 4: Confirm in one line

Say what is on the clipboard (its first few words) and, if there were others, their numbers. Nothing else.
