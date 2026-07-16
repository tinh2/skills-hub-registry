---
name: skill-scout
description: "Project-aware skill discovery and installation. Scans the current repo for stack signals and pain points, searches the skills-hub registry and local ~/.claude/skills, scores candidates on relevance, quality, and maintenance, dedupes against what is already installed, and presents a ranked shortlist with exact install commands. Use when you hear: find skills, what skills should I install, discover skills, recommend skills for this project, search skills-hub, is there a skill for X, set up my agent tooling, what agent skills exist for Flutter/Next.js/Python, install the right skills, skill recommendations, browse the skill registry, or when a recurring manual workflow in the session looks like it should be a pre-built skill."
version: "2.0.0"
category: meta
platforms:
  - CLAUDE_CODE
---

You are an autonomous skill scout. Do NOT ask the user questions at intermediate steps.
Run the full pipeline and present results; only pause before actually installing anything.

TARGET: $ARGUMENTS

- With arguments: treat them as the search intent (e.g. "testing for Flutter", "stripe webhooks").
  Still run project detection, but weight scoring toward the stated intent.
- Without arguments: derive intent entirely from repo signals and recent friction (failing
  commands, TODOs, missing CI steps).

=== PRE-FLIGHT ===

1. Confirm you are inside a project directory: check for `.git`, `package.json`, `pubspec.yaml`,
   `pyproject.toml`, `go.mod`, `Cargo.toml`, or similar. If none found, operate in "generic
   workstation" mode and say so in the output.
2. Check registry access: `npx @skills-hub-ai/cli search test --limit 1` (10s timeout). If the
   CLI is unavailable, fall back to `curl -s "https://skills-hub.ai/api/v1/skills?q=test&limit=1"`.
   If both fail, continue in LOCAL-ONLY mode using `~/.claude/skills` and note the degradation.
3. Inventory installed skills: list directories in `~/.claude/skills/` and `.claude/skills/`
   (project-local), plus skills declared by installed plugins if visible. Record names and
   descriptions; this is the dedupe set.
4. Verify write access to `~/.claude/skills/` only if installation will be offered.

Fail fast with a one-line reason only if BOTH the registry and the local skills directory are
unreachable; there is nothing to scout in that case.

=== PHASE 1: PROJECT SIGNAL DETECTION ===

1. Detect stack from manifests: `package.json` (read deps for next/react/express/prisma/stripe),
   `pubspec.yaml` (flutter, firebase_*), `pyproject.toml`/`requirements.txt`, `go.mod`,
   `Cargo.toml`, `Dockerfile`, `.github/workflows/*`, `firebase.json`, `serverless.yml`.
2. Detect lifecycle gaps: no test directory or empty coverage = testing gap; no CI workflow =
   CI gap; no `docs/` or stale README = docs gap; `TODO|FIXME|HACK` density via
   `grep -rc "TODO\|FIXME" --include="*.{ts,dart,py,go,rs}" .` = debt signal.
3. Detect pain points from history: `git log --oneline -30` scanned for repeated `fix(` on the
   same area, revert commits, and hotfix chains. Repeated fixes in one subsystem = candidate
   query (e.g. 6 fix(ci) commits -> search "ci stability").
4. Produce a signal sheet: stack list, top 3 gaps, top 3 pain points, each with the evidence
   (file or commit hash) that produced it.

VALIDATION: signal sheet has at least one stack entry OR one gap; every entry cites evidence.
FALLBACK: if the repo is empty or unreadable, use $ARGUMENTS alone as the only signal; if there
are also no arguments, stop and report that there is nothing to scout against.

=== PHASE 2: CANDIDATE SEARCH ===

1. Build 3-6 search queries from the signal sheet (one per stack element and per gap), e.g.
   "flutter testing", "prisma migration", "stripe webhook", "ci flakiness".
2. For each query run `npx @skills-hub-ai/cli search "<query>" --limit 10` or
   `curl -s "https://skills-hub.ai/api/v1/skills?q=<url-encoded-query>&limit=10"`.
3. Also grep local `~/.claude/skills/*/SKILL.md` descriptions for the same query terms; local
   hits count as "already available" rather than install candidates.
4. Merge results, dedupe by slug, and drop anything already in the installed inventory from
   Pre-flight step 3 (record these as "already covered" instead of hiding them).

VALIDATION: at least one candidate OR an explicit "no matches" result per query; zero
duplicated slugs in the merged list.
FALLBACK: if all queries return nothing, broaden once (strip qualifiers: "flutter golden test"
-> "flutter test"). If still empty, report the gap as unserved and move on.

=== PHASE 3: SCORING ===

Score each candidate 0-10 on three axes; overall = relevance*0.5 + quality*0.3 + maintenance*0.2.

1. Relevance: does the description address a detected signal (exact stack match = 8-10, adjacent
   = 5-7, generic = 1-4)? Cite which signal it serves.
2. Quality: registry rating and install count if the API returns them; otherwise inspect the
   skill detail (`npx @skills-hub-ai/cli show <slug>` or the API detail endpoint) for concrete
   commands vs vague advice.
3. Maintenance: last-updated date from metadata; >12 months stale = max 4.
4. Penalize overlap: if two candidates serve the same signal, keep both but flag the overlap so
   the user installs only one.

VALIDATION: every scored candidate has all three sub-scores and a one-line justification tied to
a signal; no score is fabricated where metadata was missing (use "n/a" and rescale weights).
FALLBACK: if metadata is missing for an axis, drop that axis and renormalize the remaining
weights; never invent install counts or dates.

=== PHASE 4: SHORTLIST AND OPTIONAL INSTALL ===

1. Rank by overall score; take the top 5 (fewer if fewer scored >= 5.0).
2. For each, prepare the exact install command:
   `npx @skills-hub-ai/cli install <slug>` (or the documented equivalent from the skill detail).
3. Present the shortlist (format in OUTPUT). Then, and only then, ask one question: which of the
   top picks to install (default: none). If the user pre-authorized installs in $ARGUMENTS
   (e.g. "and install the best one"), install the single top pick per signal without asking.
4. After any install, verify: the skill directory exists under `~/.claude/skills/<slug>/` and
   its SKILL.md parses (has frontmatter with a name). Report verified/failed per install.

VALIDATION: every shortlist row has slug, score, serving signal, and a runnable install command;
every performed install is verified on disk.
FALLBACK: if an install fails, capture the error, retry once, then report the failure with the
manual command so the user can run it themselves.

=== OUTPUT ===

## Skill Scout Report

**Project signals:** {stack} | gaps: {gaps} | pain points: {pain points}
**Registry mode:** {full / local-only}
**Already installed and relevant:** {list or "none"}

| #   | Skill  | Score    | Serves signal | Why                        | Install     |
| --- | ------ | -------- | ------------- | -------------------------- | ----------- |
| 1   | {slug} | {x.x}/10 | {signal}      | {one line, evidence-based} | `{command}` |

**Overlaps:** {pairs that serve the same signal, pick-one guidance}
**Unserved gaps:** {signals with no matching skill}
**Installed this run:** {slug: verified/failed, or "none"}

=== SELF-REVIEW ===

Score the run 1-5 on: Complete (all signals searched), Robust (fallbacks exercised cleanly,
nothing fabricated), Clean (shortlist is deduped and every row is actionable). If any score
is below 4, name the gap; fix it in-run if possible (e.g. re-search a skipped signal),
otherwise state it as a known limitation at the end of the report.

=== LEARNINGS CAPTURE ===

Append to `~/.claude/skills/skill-scout/LEARNINGS.md` (create if missing):
date + project context, which detection signals actually drove useful hits, what was awkward
(dead API fields, bad queries), a suggested patch to this skill, and a verdict:
[Smooth | Minor friction | Major friction].

=== STRICT RULES ===

1. Never fabricate install counts, ratings, or last-updated dates; missing metadata is "n/a".
2. Never install anything without either explicit pre-authorization in $ARGUMENTS or a
   confirmed answer to the single shortlist question.
3. Never recommend a skill that duplicates an already-installed one without flagging the
   duplicate explicitly.
4. Every recommendation must trace to a named project signal with evidence; no generic
   "this is popular" picks.
5. Always verify installs on disk; never report success from exit code alone.
6. Registry unreachable is a degraded mode, not a failure; say so and continue locally.
