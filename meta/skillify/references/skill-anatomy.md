# Skill Anatomy Reference

## Required Frontmatter

```yaml
---
name: kebab-case-name
description: "Triggering description — what it does + when to invoke it. Be pushy."
version: 1.0.0
category: build | deploy | meta | analyze | generate | test | ops | content
---
```

## Body Structure

A complete skill has these sections in order:

1. **Role declaration** — one line: "You are a X agent."
2. **Autonomy statement** — "Do NOT ask the user questions. Proceed autonomously."
3. **Input variable** — `$ARGUMENTS` for user-provided input, or omit if none.
4. **Pre-flight checks** — prerequisites validated before any work begins.
5. **Phased execution** — 2-5 named phases, each with a validation gate.
6. **Self-review block** — scoring + iterate-or-accept decision.
7. **Learnings capture** — append to LEARNINGS.md after delivery.
8. **Output template** — the exact format for the final report.
9. **Strict rules** — guard rails and non-negotiables.

## Pre-Flight Pattern

```
=== PRE-FLIGHT ===
Before starting, verify:
- [ ] <what must exist or be true>
- [ ] <another prerequisite>

Recovery:
- If <X> is missing: <do this — create it, skip gracefully, or halt with message>
- If <Y> is unavailable: <fallback action>
```

## Phase Pattern

```
=== PHASE N: PHASE NAME ===

<Concise instructions. Explain the WHY, not just the WHAT.>
<Use imperative form: "Run X", "Write Y", "Verify Z".>

VALIDATION: <What must be true before proceeding — e.g., "file exists and is non-empty">
FALLBACK: <What to do if validation fails — alternative approach, graceful skip, or clear error>
```

## Self-Review Pattern

```
=== SELF-REVIEW ===
Score the result (1–5 each):
- Complete: Did this fully accomplish the goal?
- Robust: Were failure modes handled? Were fallbacks triggered?
- Clean: Is the output well-structured and free of noise?

If any dimension scores < 4:
- Identify the specific gap.
- If fixable now: fix it, then re-score.
- If not fixable: note as a known limitation in the output.
```

## Learnings Capture Pattern

```
=== LEARNINGS CAPTURE ===
Append to ~/.claude/skills/<skill-name>/LEARNINGS.md:

## <YYYY-MM-DD> — <one-line context>
- **What worked:** <specific approach or step that went smoothly>
- **What was awkward:** <step that required retry, backtrack, or manual fix>
- **Suggested patch:** <concrete improvement — "add pre-flight check for X", "add fallback when Y">
- **Verdict:** [Smooth / Minor friction / Major friction]
```

## Output Template Pattern

End with a clear, scannable summary block:

```
## <Skill Name> Complete

**What was done:** <one sentence>
**Output:** <file path, URL, or inline result>
**Known limitations:** <any deferred issues>
**Next steps:** <what to run next, if anything>
```

## Writing Principles

**Explain the why.** Don't just say MUST DO X — say "X prevents Y, which caused Z in past runs."
The executing model is smart and responds better to reasoning than commands.

**Prefer phases over bullets.** A flat list of 15 steps is harder to follow and harder to
resume after a failure than 4 named phases with clear inputs and outputs.

**Name your fallbacks.** "Try an alternative" is not a fallback. Name the specific alternative:
"If `npm install` fails, check for a lockfile conflict with `npm ls` before retrying."

**Keep the body under 500 lines.** If you're approaching the limit, extract reference material
to `references/` and link to it with "read references/X.md for details."

**Use `$ARGUMENTS` for user input.** If the skill needs a name, path, or flag from the user,
reference it as `$ARGUMENTS` in the body. Document what it expects near the top.

## Category Guide

| Category | Use for                                |
| -------- | -------------------------------------- |
| build    | Coding, implementation, feature work   |
| deploy   | Shipping, CI/CD, publishing            |
| meta     | Skills about skills, context, memory   |
| analyze  | Auditing, reviewing, measuring         |
| generate | Content creation, scaffolding          |
| test     | QA, evals, coverage                    |
| ops      | Infrastructure, maintenance, ops tasks |
| content  | Writing, docs, marketing copy          |
