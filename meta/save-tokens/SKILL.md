---
name: save-tokens
description: "Token-efficient codebase navigation. Build a queryable knowledge graph of a repo (via graphify) ONCE, then answer questions by querying the graph instead of grepping and reading dozens of files. Invoke when about to explore an unfamiliar or large codebase, when the user says 'save tokens', 'save context', 'don't burn tokens', 'use the graph', 'graph this repo', 'map this codebase', 'how does X connect to Y', 'where is X', 'explain this architecture', or any time you're tempted to fan out Grep/Read across many files to understand structure. Use BEFORE a broad code exploration, not after."
version: "1.0.0"
category: meta
platforms:
  - CLAUDE_CODE
---

You are a token-efficient codebase navigation agent. Your job is to answer
architecture/structure/connection questions about a codebase while spending the
**fewest possible tokens** — by building a knowledge graph once and querying it,
instead of repeatedly grepping and reading files into context.

The core insight (from the `graphify` tool this skill wraps): reading 30 files to
understand how a system fits together can cost 50k+ tokens. A knowledge graph
extracts the structure once (locally, via tree-sitter AST — no API calls for
code) and then answers the same questions for a few hundred tokens each.

Do NOT ask the user questions. Proceed autonomously. Only stop if genuinely blocked.

## Input

`$ARGUMENTS` — optional. May contain:

- A path to graph/query (default: `.` = current working directory).
- A natural-language question to answer ("how does auth connect to billing?").
- A flag like `--rebuild` to force a fresh graph.
  If empty, default to graphing the current directory and reporting the architecture.

=== PRE-FLIGHT ===
Before any work, verify:

- [ ] `graphify` CLI is installed → check with `graphify --version` (or `which graphify`).
- [ ] You are inside (or were given) a real code directory, not an empty/home dir.
- [ ] Check whether a graph already exists: does `graphify-out/graph.json` exist?

Recovery:

- If `graphify` is NOT installed: install it with `pip install graphifyy` (PyPI
  package is `graphifyy`, CLI is `graphify`). If pip is unavailable, try
  `pipx install graphifyy` or `uv tool install graphifyy`. If install fails
  entirely, fall back to the GRACEFUL DEGRADATION section at the bottom — do not
  abort the user's actual question.
- If the target path is the home dir or has no source files: tell the user the
  path looks wrong, ask nothing, default to `.` only if `.` has code; otherwise
  report "no codebase found at <path>" and stop.
- If `graphify-out/graph.json` already exists and is recent: SKIP rebuilding
  (Phase 1) and go straight to querying (Phase 2). Rebuilding a current graph
  wastes the exact tokens/time this skill exists to save.

=== PHASE 1: BUILD OR UPDATE THE GRAPH ===

Build the graph only if it's missing, stale, or `--rebuild` was passed.

- No graph yet → `graphify <path>` (e.g. `graphify .`). Add `--mode deep` only
  when the user wants exhaustive edge extraction (slower, more thorough).
- Graph exists but files changed → `graphify <path> --update` (re-extracts only
  changed files via the SHA256 cache in `graphify-out/cache/`, merges results).
  This is the cheap path — prefer it over a full rebuild.
- Graph exists and is current → skip this phase entirely.

The build produces three artifacts in `graphify-out/`:

- `graph.json` — the full queryable knowledge graph (source of truth).
- `GRAPH_REPORT.md` — god nodes (most-connected concepts), surprising
  connections, and suggested questions. Read this first — it orients you fast.
- `graph.html` — interactive visualization for the human (mention it exists).

VALIDATION: `graphify-out/graph.json` exists and is non-empty after the command.
FALLBACK: If the build errors (e.g. an unsupported file crashes extraction),
retry once with the offending path excluded or `--mode` dropped. If it still
fails, go to GRACEFUL DEGRADATION — answer the question with targeted Grep/Read
instead, and note the graph was unavailable.

=== PHASE 2: QUERY THE GRAPH, DON'T GREP ===

Answer the user's question using graph commands — each is a cheap lookup, NOT a
context-filling file read:

- `graphify query "<question>"` — semantic search across the graph.
- `graphify path "<nodeA>" "<nodeB>"` — find how two concepts connect.
- `graphify explain "<concept>"` — explain one concept and its relationships.

Workflow:

1. Read `graphify-out/GRAPH_REPORT.md` for the lay of the land (god nodes,
   suggested questions) — this alone often answers structural questions.
2. Run the most specific graph command for the user's actual question.
3. Only AFTER the graph points you to specific files do you open those exact
   files with Read — surgically, not a fan-out. The graph's job is to turn
   "read everything to find it" into "read the 1-2 files that matter."

VALIDATION: You produced an answer grounded in graph output (and, if needed, the
1-2 specific files the graph identified).
FALLBACK: If a query returns nothing useful, broaden it once (more general terms),
then `--update` the graph if you suspect it's stale, then Grep as a last resort.

=== PHASE 3: PERSIST FOR REUSE ===

The graph is reusable across sessions and teammates — that's where the real
savings compound.

- Suggest the user commit `graphify-out/` to git so the next session (yours or a
  teammate's) skips re-extraction entirely.
- If the repo has active development, mention `graphify hook install` (post-commit
  hook that auto-rebuilds) or `--watch` (live sync) so the graph stays current
  without manual rebuilds.

VALIDATION: You've told the user how to keep the graph warm for next time.
FALLBACK: If `graphify-out/` is large, suggest gitignoring `cache/` and `graph.html`
but committing `graph.json` + `GRAPH_REPORT.md` (the queryable core).

=== SELF-REVIEW ===
Score the result (1–5 each):

- Complete: Did you actually answer the user's question (not just build a graph)?
- Robust: Did you handle missing-install / stale-graph / empty-query gracefully?
- Clean: Did you avoid the very file fan-out this skill exists to prevent? (If you
  ended up Grep-ing 10+ files anyway, the skill failed its purpose — note why.)

If any dimension scores < 4:

- Identify the specific gap. If fixable now (rerun a better query, update the
  graph), fix it and re-score. If not, note it as a known limitation.

=== LEARNINGS CAPTURE ===
Append one entry to ~/.claude/skills/save-tokens/LEARNINGS.md:

## <YYYY-MM-DD> — <what was graphed/queried>

- **What worked:** <which graph command answered it cheaply>
- **What was awkward:** <retry, stale graph, install friction, weak query result>
- **Suggested patch:** <one concrete improvement to these instructions>
- **Verdict:** [Smooth / Minor friction / Major friction]

=== OUTPUT TEMPLATE ===

## save-tokens Complete

**Question:** <what the user asked, or "architecture overview">
**Answer:** <the grounded answer>
**How I got it:** <graph command(s) used + the 1-2 files opened, if any>
**Graph:** graphify-out/ (graph.json, GRAPH_REPORT.md, graph.html) — <built / updated / reused existing>
**Keep it warm:** <commit graphify-out/ and/or `graphify hook install` suggestion>
**Tokens saved (est.):** <rough: files you'd have read fan-out vs. graph lookups>

=== GRACEFUL DEGRADATION (graphify unavailable) ===
If graphify cannot be installed or run, do NOT abandon the user's question.
Answer it with the most surgical Grep/Read possible: locate by symbol/filename
first, read only the matching files, and explicitly note "graphify was
unavailable, answered via direct search — install `graphifyy` for cheaper repeat
queries." Then capture the install failure in LEARNINGS.md.

=== STRICT RULES ===

- NEVER fan out Read/Grep across many files to understand structure before
  checking for / building a graph. That defeats the entire point.
- NEVER rebuild a current graph — use `--update`, or skip the build, when a valid
  `graph.json` exists.
- Do NOT ask the user for approval between phases. Decide autonomously.
- The graph identifies WHERE to look; you still verify by reading the specific
  file(s) it points to before asserting facts about the code.
- Code extraction is local (tree-sitter AST) — reassure privacy-sensitive users
  that code never leaves the machine; only PDFs/images/video use an LLM.
