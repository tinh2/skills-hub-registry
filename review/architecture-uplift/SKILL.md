---
name: architecture-uplift
description: Assess a codebase's architecture with hard evidence — module map, dependency direction, layering breaks, coupling and cohesion hotspots weighted by git churn — then rank 3-5 improvement moves by risk-adjusted value and actually execute the lowest-risk move end to end with tests green before and after, finishing with a dated architecture doc containing before/after mermaid diagrams. Use when someone says "improve the architecture", "this codebase is a mess", "reduce coupling", "untangle dependencies", "refactor safely", "layering is broken", "circular imports", "tech debt assessment", "where should we refactor first", or "clean up module boundaries" and wants executed change, not just a slideware review.
version: "2.0.0"
category: review
platforms:
  - CLAUDE_CODE
---

You are an autonomous software architect who ships refactors, not slide decks. Work through every phase end to end in one run, choose sensible defaults where the codebase leaves room for judgment, and record each decision in the final architecture doc.

TARGET: $ARGUMENTS
If arguments name a directory, package, or concern (e.g. "the api layer"), scope assessment there but still map its inbound/outbound dependencies. If empty, assess the whole repository.

=== PRE-FLIGHT ===

1. Confirm you are in a git repository (`git rev-parse --git-dir`). No git: proceed, but churn scoring is unavailable — state this and weight by size/fan-in only.
2. Detect the stack: language(s) by file census (`git ls-files | sed 's/.*\.//' | sort | uniq -c | sort -rn`), package layout (single package, workspaces/monorepo, multi-module), and build/test commands from package.json, Makefile, pyproject.toml, go.mod, Cargo.toml, or CI config.
3. Run the test suite once and record the baseline: command, pass/fail counts, duration. If tests fail at baseline: record the failing set — the uplift move must not grow it. If NO test suite exists: Phase 4 is restricted to moves verifiable by typecheck/build alone (file moves, import re-exports), and this restriction goes in the report.
4. Confirm the working tree is clean enough: uncommitted changes present means all uplift edits go on isolated commits touching only uplift files.

=== PHASE 1: MODULE MAP AND DEPENDENCY DIRECTION ===

1. Identify the module units the codebase actually uses (top-level dirs, workspace packages, Go packages, Python packages).
2. Build the dependency edge list between modules by scanning imports (grep import/require/use/from statements; use `madge`/`dependency-cruiser`/`go list -deps`-style tools only if already installed — do not install tools).
3. Infer the intended layering from structure and naming (e.g. ui -> application -> domain -> infrastructure, or routes -> services -> db). State the inferred layering explicitly; it is a hypothesis, labeled as such.
4. Flag boundary breaks, each with the importing file:line as evidence:
   - Edges pointing against the inferred layering direction.
   - Cycles between modules (list every edge in the cycle).
   - "shared"/"utils"/"common" modules that import FROM feature modules (dependency magnets).
   - Deep imports that sidestep a module's public entry point (index/mod/package facade).
   - Modules imported by everything AND importing everything (god modules).

VALIDATION: a module list, an edge list, and a boundary breaks list (possibly empty) all exist with file-level evidence for each boundary break (importing file:line).
FALLBACK: import scanning is unreliable (dynamic imports, DI containers, reflection): report edges you could verify and mark the map "partial — static analysis only".

=== PHASE 2: HOTSPOT SCORING ===

1. Per module and per file over ~1000 lines, compute:
   - Fan-in / fan-out (from the Phase 1 edge list; file-level for big files).
   - Size: `wc -l`.
   - Churn: `git log --since='12 months ago' --name-only --pretty=format: | sort | uniq -c | sort -rn` (fall back to full history if the repo is younger).
2. Hotspot score = normalized churn x normalized (fan-in + fan-out) x size factor. High-churn + high-coupling files are where architecture problems cost real money; a tangled file nobody touches intentionally scores low.
3. Produce the top 10 hotspots with all three raw numbers shown, not just the composite.

VALIDATION: top-10 table exists with raw churn, fan-in/out, and LOC columns.
FALLBACK: no git history (fresh clone with shallow depth): run `git fetch --unshallow` if cheap; otherwise score on coupling x size and label the table "churn unavailable".

=== PHASE 3: UPLIFT MOVES (RANKED) ===

1. Propose 3-5 concrete moves. Each MUST specify all six fields:
   - The change: files created, moved, and edited, by path.
   - The boundary break or hotspot it addresses, referencing Phase 1/2 evidence.
   - Expected value: which future changes get cheaper, concretely.
   - Blast radius: exact count of importing files that must change, counted from the edge list — never guessed.
   - Risk level: Low = mechanical and fully verifiable by tests/typecheck; Medium = behavior-adjacent; High = touches runtime semantics.
   - Rollback note: usually `git revert` of the move's commits; call out anything that would not revert cleanly.
2. Rank by risk-adjusted value: value / blast radius, with High-risk moves never ranked above Medium regardless of value.
3. Typical move shapes to consider:
   - Break one cycle by extracting an interface/types-only module both sides can depend on.
   - Give a module a public entry point and rewrite all deep imports through it.
   - Split a god-file along its churn seams (the functions that change together stay together).
   - Invert a wrong-direction edge with a small port/adapter.
   - Quarantine "utils" by relocating feature-owned helpers into their features.

VALIDATION: every move has all six fields; blast radius is a counted number with the counting command shown.
FALLBACK: fewer than 3 defensible moves exist (architecture is genuinely fine): say so plainly, list the 1-2 real ones or zero, and skip Phase 4 only if zero.

=== PHASE 4: EXECUTE THE LOWEST-RISK MOVE ===

1. Take the lowest-risk move from the ranking (not the highest-value one; executing the smallest-blast-radius change first keeps the refactor recoverable).
2. Execute in small steps; after each step run typecheck/build; commit each coherent step with message `refactor(arch): <step> [uplift: <move name>]`. Respect the ~400 LOC per commit ceiling.
3. Mechanical rewrites of importers (path updates) may be scripted with sed/codemod, but verify by compiler, not by eyeball.
4. Run the full test suite. Baseline-passing tests must all pass; the pre-existing failure set must not grow.
5. Re-derive the affected slice of the dependency map and confirm the targeted boundary break/cycle is actually gone.

VALIDATION: tests green vs baseline, boundary break demonstrably removed, commits self-contained.
FALLBACK: the move turns out riskier mid-flight (hidden dynamic import, test explosion): stop, `git revert` the move's commits cleanly, mark it "attempted — reverted, here is what we learned", and execute the next-lowest-risk move if one qualifies; otherwise report with the revert documented.

=== PHASE 5: ARCHITECTURE DOC ===

Write `docs/architecture/uplift-<YYYY-MM-DD>.md` (create dirs) containing, in order:

1. Stack summary and how the module map was derived.
2. Inferred layering with its confidence level and the evidence behind it.
3. BEFORE mermaid `graph TD` of modules, boundary break edges styled red.
4. Hotspot top-10 table (churn, fan-in/out, LOC, composite).
5. The ranked move list with all six fields per move.
6. The executed move's narrative: steps, commit hashes, test evidence before/after.
7. AFTER mermaid diagram showing the removed boundary break.
8. Remaining moves as a prioritized backlog with blast radii.
   Keep mermaid node counts <= 20 by grouping small modules into labeled clusters.

VALIDATION: file exists, both diagrams parse (balanced brackets, valid arrow syntax), backlog present.
FALLBACK: module count too high for a readable diagram: diagram the affected subsystem only and state the elision.

=== OUTPUT ===

1. The doc at docs/architecture/uplift-<date>.md.
2. Executed commits on the current branch (listed by hash + message).
3. A terminal summary:
   - Boundary breaks found and hotspot #1.
   - Move executed, with test delta (before/after pass counts).
   - The top remaining move with its counted blast radius.

=== SELF-REVIEW ===

Before finishing, assess your own work on three dimensions, each 1-5: Complete (map + scoring + ranked moves + one executed move + doc all delivered), Robust (test baseline honored, revert path proven or unneeded), Clean (commits scoped, no unrelated edits). If any dimension falls below 4, repair it within this run when feasible; otherwise record it as a known limitation in the doc's header.

=== LEARNINGS CAPTURE ===

Append to ~/.claude/skills/architecture-uplift/LEARNINGS.md: date + repo, which detection worked (imports/churn), which move shape was executed, friction encountered, suggested patch to this skill, verdict [Smooth/Minor friction/Major friction].

=== STRICT RULES ===

1. Never present the inferred layering as fact; it is labeled a hypothesis with the evidence that produced it.
2. Blast radius is always a counted number from the edge list, never an adjective.
3. Never execute a Medium- or High-risk move when a Low-risk move exists; never execute any move without a recorded test (or typecheck) baseline.
4. Never leave a half-executed move in the tree — complete it or revert it fully.
5. Every boundary break and hotspot claim cites file:line or a reproducible command.
6. Do not install analysis tooling; work with what the repo has.
7. Churn weighting is mandatory when git history exists; a coupling-only ranking must be labeled as degraded.
