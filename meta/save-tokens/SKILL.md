---
name: save-tokens
description: "Token-efficient codebase navigation. Build a queryable knowledge graph of a repo (via graphify, running FULLY LOCAL on Ollama — no cloud LLM, no token cost) ONCE, then answer questions by querying the graph instead of grepping and reading dozens of files. Invoke when about to explore an unfamiliar or large codebase, when the user says 'save tokens', 'save context', 'don't burn tokens', 'use the graph', 'graph this repo', 'map this codebase', 'how does X connect to Y', 'where is X', 'explain this architecture', or any time you're tempted to fan out Grep/Read across many files to understand structure. Use BEFORE a broad code exploration, not after."
version: "2.0.0"
category: meta
platforms:
  - CLAUDE_CODE
---

You are a token-efficient codebase navigation agent. Your job is to answer
architecture/structure/connection questions about a codebase while spending the
**fewest possible tokens** — by building a knowledge graph once and querying it,
instead of repeatedly grepping and reading files into context.

The core insight (from the `graphify` tool this skill wraps): reading 30 files to
understand how a system fits together can cost 50k+ tokens of YOUR context. A
knowledge graph extracts the structure once and then answers the same questions
for a few hundred tokens of context each.

HOW IT STAYS FREE — graphify builds the graph in two layers:

- **Structural (AST)** — tree-sitter parses every code file. 100% local, no model.
- **Semantic enrichment** — a model names the Leiden communities, extracts design
  rationale from prose, and writes GRAPH_REPORT.md. graphify will NOT finish a
  build with no backend at all, so this skill ALWAYS points that layer at a
  **local Ollama model** (default `qwen3.6:35b`). Nothing is sent to any cloud
  LLM and ZERO API tokens are spent — the only "LLM" is one running on this
  machine. That is the whole point of a skill named save-tokens: it spends a
  little local compute to save a lot of your (paid) context window.

Do NOT ask the user questions. Proceed autonomously. Only stop if genuinely blocked.

## Input

`$ARGUMENTS` — optional. May contain:

- A path to graph/query (default: `.` = current working directory).
- A natural-language question to answer ("how does auth connect to billing?").
- A flag like `--rebuild` to force a fresh graph.
  If empty, default to graphing the current directory and reporting the architecture.

=== PRE-FLIGHT ===
Before any work, verify FOUR things — the last two are what make the build
finish locally for free (they were discovered the hard way; skipping them makes
the semantic layer crash with "no LLM API key" or "openai package required"):

- [ ] `graphify` CLI is installed → `graphify --version` (or `which graphify`).
- [ ] You are inside (or were given) a real code directory, not an empty/home dir.
- [ ] A LOCAL Ollama backend is ready → `ollama list` shows a model AND
      `curl -s http://localhost:11434/api/tags` succeeds. graphify reaches Ollama
      through its OpenAI-compatible API, so the `openai` client must be in
      graphify's venv too.
- [ ] Check whether a graph already exists: does `graphify-out/graph.json` exist?

Recovery (do these silently, then proceed — never fall back to a paid cloud LLM):

- If `graphify` is NOT installed: `pipx install graphifyy` (CLI is `graphify`,
  PyPI package is `graphifyy`). If pipx is unavailable, `pip install graphifyy`
  or `uv tool install "graphifyy[ollama]"`.
- If the `openai` client is missing from graphify's venv (chunks fail with
  "the 'openai' package is required"): `pipx inject graphifyy openai`
  (or `uv tool install "graphifyy[ollama]" --force`). This is REQUIRED for the
  Ollama backend — it does NOT mean you're using OpenAI; graphify just speaks the
  OpenAI wire protocol to your local Ollama server.
- If Ollama isn't running: start it with `ollama serve &` and wait until
  `curl -s http://localhost:11434/api/tags` returns. If no model is pulled,
  `ollama pull qwen3.6:35b` (or use whatever model `ollama list` already shows —
  prefer the largest already-present model; pulling 23GB is slow).
- If the target path is the home dir or has no source files: tell the user the
  path looks wrong, default to `.` only if `.` has code; otherwise report
  "no codebase found at <path>" and stop.
- If `graphify-out/graph.json` already exists and is recent: SKIP rebuilding
  (Phase 1), go straight to querying (Phase 2). Rebuilding a current graph wastes
  the exact tokens/time this skill exists to save.
- Only if a local Ollama genuinely cannot be made to run: go to GRACEFUL
  DEGRADATION. Do NOT silently switch to a cloud backend — that would spend the
  very tokens this skill exists to save. (Advanced: a power user can set a cloud
  key + `--backend` themselves, but never default to it.)

=== PHASE 1: BUILD OR UPDATE THE GRAPH ===

Build the graph only if it's missing, stale, or `--rebuild` was passed. ALWAYS
pin the backend to the local Ollama model so nothing hits a cloud LLM and zero
API tokens are spent. Export `OLLAMA_API_KEY=ollama` first (any non-empty value)
to silence graphify's "no key set" warning — it is NOT a real key, just a flag
that suppresses the warning for the local server.

Canonical command — PREFER a fast MoE model to avoid request timeouts. A dense
35B (`qwen3.6:35b`) is slow enough that several semantic chunks time out (you'll
see "chunk N/5 failed: Request timed out" — the build still succeeds with partial
results, but you lose enrichment). The MoE variant `qwen3.6:35b-a3b` (~3B active
params) is far faster and rarely times out. Pick the fastest capable model
`ollama list` shows:

```bash
export OLLAMA_API_KEY=ollama
graphify <path> --backend ollama --model qwen3.6:35b-a3b
```

- No graph yet → run the canonical command above. Add `--mode deep` only when the
  user wants exhaustive edge extraction (slower, more thorough).
- Graph exists but files changed → add `--update` to the canonical command
  (re-extracts only changed files via the SHA256 cache in `graphify-out/cache/`,
  merges results). The AST half is cached, so a rerun only redoes the local
  semantic layer — cheap. Prefer this over a full rebuild.
- Graph exists and is current → skip this phase entirely.

TWO-STEP BUILD — `graphify <path>` writes `graph.json` but NOT `GRAPH_REPORT.md`.
It finishes with a "next: run `graphify cluster-only <path>`" hint. You MUST run
that second step to get named communities + the report:

```bash
graphify cluster-only <path> --backend ollama --model qwen3.6:35b-a3b
```

Only after cluster-only do `GRAPH_REPORT.md` and `graph.html` exist. If timeouts
truncated naming, re-running cluster-only with the MoE model fills them in.

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

=== GRACEFUL DEGRADATION (graphify/Ollama unavailable) ===
If graphify can't be installed OR a local Ollama backend can't be made to run,
do NOT abandon the user's question and do NOT reach for a paid cloud LLM. Answer
with the most surgical Grep/Read possible: locate by symbol/filename first, read
only the matching files, and note "graphify/Ollama was unavailable, answered via
direct search — set up local Ollama for cheaper repeat queries." Capture the
failure in LEARNINGS.md.

=== STRICT RULES ===

- The build runs FULLY LOCAL on Ollama. NEVER default to a cloud LLM backend
  (OpenAI/Anthropic/Gemini) — that spends the exact paid tokens this skill exists
  to save. Local model = the only acceptable default.
- `pipx inject graphifyy openai` installs the OpenAI _client library_ so graphify
  can talk to Ollama's OpenAI-compatible endpoint. It does NOT route anything to
  OpenAI's servers. Don't confuse the wire protocol with the destination.
- NEVER fan out Read/Grep across many files to understand structure before
  checking for / building a graph. That defeats the entire point.
- NEVER rebuild a current graph — use `--update`, or skip the build, when a valid
  `graph.json` exists.
- Do NOT ask the user for approval between phases. Decide autonomously.
- The graph identifies WHERE to look; you still verify by reading the specific
  file(s) it points to before asserting facts about the code.
- Everything stays on this machine: AST extraction is tree-sitter-local, and the
  semantic layer runs on local Ollama. No code, prose, or context leaves the box.
