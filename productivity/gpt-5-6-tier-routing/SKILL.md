---
name: gpt-5-6-tier-routing
description: "Autonomously selects the right GPT-5.6 tier (Sol / Terra / Luna) for each coding task based on scope, file count, and planning complexity — then applies explicit cache breakpoints for SKILL.md files and system prompts. Reduces monthly AI coding costs by 50–80% without sacrificing output quality on complex tasks."
version: 1.0.0
category: productivity
platforms:
  - CLAUDE_CODE
  - CURSOR
  - CODEX_CLI
---

You are a GPT-5.6 tier-routing agent. Before every AI coding task, evaluate the task scope and route it to the appropriate GPT-5.6 model tier. Do NOT use the same tier for every task — that is the anti-pattern this skill exists to fix.

TARGET:
$ARGUMENTS

============================================================
PHASE 1: TASK SCOPE ASSESSMENT
============================================================

Evaluate the incoming task on these axes before selecting a tier:

1. **File count** — How many files will this task read or modify?
   - 1–2 files → lean toward Terra or Luna
   - 3–10 files → Terra (interactive) or Sol (cross-module)
   - 10+ files → Sol only

2. **Planning requirement** — Does the task require decomposition into sub-steps before execution?
   - No planning needed (single-step, well-defined output) → Terra or Luna
   - Requires intermediate reasoning steps → Sol

3. **Error cost** — What happens if the model makes a wrong intermediate decision?
   - High cost (schema migration, security-sensitive, API contract change) → Sol
   - Low cost (can iterate quickly, no downstream breakage) → Terra or Luna

4. **Latency sensitivity** — Is this task user-blocking (interactive) or background?
   - User is waiting for response → Terra or Luna
   - Background batch job → Luna if low-stakes, Sol if high-stakes

5. **Task type classification:**

   | Task type | Default tier |
   |---|---|
   | Autocomplete / inline suggestion | Luna |
   | Docstring / comment generation | Luna |
   | Commit message draft | Luna |
   | Quick type lookup / explain snippet | Luna |
   | Write / fix a single function | Terra |
   | Write tests for existing code | Terra |
   | PR description draft | Terra |
   | Debug failing test (single file) | Terra |
   | Refactor across 3+ files | Sol |
   | Security audit | Sol |
   | Framework migration | Sol |
   | Multi-file architectural change | Sol |
   | Agentic loop with 5+ tool calls | Sol with ultra mode |

============================================================
PHASE 2: TIER SELECTION AND CONFIGURATION
============================================================

Based on Phase 1, select one of:

**Luna** (`gpt-5.6-luna`): $1/$6 per 1M tokens. Use for high-volume, low-stakes, latency-sensitive tasks.

**Terra** (`gpt-5.6-terra`): $2.50/$15 per 1M tokens. Default for interactive daily coding. Best cost/quality ratio for single-file to small multi-file work.

**Sol** (`gpt-5.6-sol`): $5/$30 per 1M tokens. Use for complex agentic tasks, large-scope refactors, high-error-cost scenarios.
- Add `reasoning_effort: "ultra"` for tasks with 5+ planning steps.
- Ultra mode is Sol-only. Never request ultra on Terra or Luna.

Output the selection as:

```
TIER SELECTION
Model: gpt-5.6-{tier}
Ultra mode: {yes | no}
Rationale: {one sentence}
Estimated cost delta vs. always-Sol: {-X%}
```

============================================================
PHASE 3: EXPLICIT CACHE BREAKPOINT WIRING
============================================================

GPT-5.6 supports explicit cache breakpoints with a guaranteed 30-minute minimum cache lifetime. Wire breakpoints to maximize savings:

1. **Identify the stable prefix** — everything in your prompt that doesn't change between requests:
   - System prompt / SKILL.md instructions
   - Codebase context / file tree
   - Project-specific conventions
   - Tool definitions

2. **Mark the breakpoint** — after the stable prefix, before the per-request content:

```python
# Responses API — Python
response = client.responses.create(
    model="gpt-5.6-terra",
    input=[
        {
            "role": "system",
            "content": STABLE_SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": "<<CACHE_BREAKPOINT>>",  # marker
        },
        {
            "role": "user",
            "content": per_request_task,
        },
    ],
    cache_control={"type": "breakpoint"},
)
```

```typescript
// TypeScript — Responses API
const response = await openai.responses.create({
  model: "gpt-5.6-terra",
  input: [
    { role: "system", content: STABLE_SYSTEM_PROMPT },
    { role: "user", content: "<<CACHE_BREAKPOINT>>" },
    { role: "user", content: perRequestTask },
  ],
  cache_control: { type: "breakpoint" },
});
```

3. **Expected savings** — with a 2,000-token system prompt:
   - Without caching: 2,000 tokens charged per request
   - With caching: ~200–400 tokens charged after the first request in a 30-min window
   - Effective input cost reduction: 80–90% on the cached prefix

============================================================
PHASE 4: CODEX CLI CONFIG
============================================================

For Codex CLI users, wire the tier router into your config:

```toml
# ~/.codex/config.toml
# Default to Terra for interactive sessions
model = "gpt-5.6-terra"

# Override per command:
# codex run --model gpt-5.6-sol "refactor the auth module across all callers"
# codex run --model gpt-5.6-luna "generate docstrings for this file"
```

For multi-agent pipelines (Claude Code orchestrating Codex subagents):

```typescript
function selectGpt56Tier(task: {
  filesAffected: number;
  requiresPlanning: boolean;
  taskType: string;
  errorCostHigh: boolean;
}): "gpt-5.6-sol" | "gpt-5.6-terra" | "gpt-5.6-luna" {
  const lowStakesTypes = ["autocomplete", "docstring", "commit-message", "explain-snippet"];
  if (lowStakesTypes.includes(task.taskType)) return "gpt-5.6-luna";

  const solConditions =
    task.filesAffected > 3 ||
    task.requiresPlanning ||
    task.errorCostHigh;

  return solConditions ? "gpt-5.6-sol" : "gpt-5.6-terra";
}
```

============================================================
PHASE 5: COST REPORTING
============================================================

After each session or batch job, output a cost summary:

```
GPT-5.6 TIER ROUTING REPORT

Tasks routed this session:
  Sol:   N tasks  — ~$X.XX
  Terra: N tasks  — ~$X.XX
  Luna:  N tasks  — ~$X.XX

Cache hit ratio: ~X%
Estimated cost if always-Sol: $X.XX
Actual estimated cost: $X.XX
Savings: $X.XX (X%)

Routing decisions that saved the most:
  1. [task description] → Luna (saved $X vs Sol)
  2. [task description] → Terra (saved $X vs Sol)
```

This report surfaces patterns — tasks you're routing to Luna that keep failing,
or tasks you're routing to Terra that need Sol's planning depth. Use it to tune
your routing heuristics over time.

============================================================
STRICT RULES
============================================================

- Never default to Sol for all tasks. Sol is the right choice for ~20–30% of typical coding workloads.
- Never use ultra mode on Terra or Luna — it silently no-ops and wastes your prompt budget.
- Always wire cache breakpoints when system prompts exceed 500 tokens.
- If you cannot determine the task scope, default to Terra — not Sol.
- Cost reports are not optional. Output them after every session so the user can verify the routing is saving money.
