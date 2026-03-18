---
name: engineering-spec
description: Generates structured engineering specs (backend or frontend) from feature descriptions, designs, or ticket references. Triggers on "spec", "story", "ticket", "engineering spec", "write a story for", "write a spec for", "create a ticket for".
version: "2.0.0"
category: docs
platforms:
  - CLAUDE_CODE
---

You are generating a structured engineering specification suitable for any project management tool (Jira, Linear, GitHub Issues, plain markdown, etc.).

## Input

The user will provide one or more of:
1. A feature description in text.
2. An image of a design, spec, or existing ticket.
3. A conversation or mixed input describing what to build.
4. Output from a prior analysis skill (e.g., `/mvp`) with story candidates.

If the user provides prior analysis output, use the story candidates and feature breakdown as the basis. Do not re-analyze.

## Determine Story Type

Based on the input, determine whether this is a backend or frontend story:
- **Backend:** API endpoints, database changes, business logic, server-side processing, integrations, queues, cron jobs. Prefix with `BE:`.
- **Frontend:** UI components, pages, user interactions, client-side logic, styling. Prefix with `FE:`.
- If the user explicitly states the type, use that.
- If unclear, ask.

## Title Format

Start with `BE:` or `FE:` followed by a concise feature name (max 8 words after prefix).

Examples:
- `BE: User Invitation Flow`
- `FE: Dashboard Analytics Page`
- `BE: Webhook Event Processing`
- `FE: Settings Profile Editor`

## Required Sections

### Description

One paragraph (2-4 sentences). Explain:
- What is being built
- How users interact with it
- The high-level outcome

No filler. No implementation details. Just the what and why.

### Acceptance Criteria

Organize criteria into logical groups. Each group has a bold category header as a top-level bullet with sub-bullets for specific, testable requirements.

Format:

```
- **Category Name:**
  - Requirement sentence.
  - Another requirement sentence.

- **Another Category:**
  - Requirement sentence.
```

**Category rules:**
- Group related requirements under a descriptive bold header.
- Every requirement must be standalone and testable.
- Include validation behavior, failure behavior, and edge cases.
- Include idempotency rules when applicable.

**For BE stories — always include a Routes category if API endpoints are involved:**
- Start with authentication requirements.
- List each endpoint: who calls it, method + path in inline code, what it does.
- Format: `FE calls METHOD /path` to [description].
- Include request behavior, response shape, and error behavior.

Example:
```
- **Routes:**
  - All endpoints require user authentication.
  - FE calls `GET /api/invitations` to list pending invitations for the current user.
  - FE calls `POST /api/invitations` to create a new invitation; returns the invitation object with a unique token.
  - FE calls `DELETE /api/invitations/:id` to revoke a pending invitation; returns 404 if already accepted.
```

**For FE stories — include a UI Behavior category:**
- Describe component behavior and interaction states (loading, empty, error, success).
- Reference API endpoints the FE will consume using inline code for paths.

**Include a Business Rules category when applicable:**
- Lifecycle states (draft, active, archived).
- Constraints (e.g., only one active per organization).
- Resolution or aggregation logic.

### Dev Notes

Technical implementation guidance for the developer.

**For BE stories:**

- **Schema/Database:** State new or modified schemas/tables.
- **Tables:** List each table with columns:
  ```
  **table_name**
  - column_name (TYPE, modifiers) -- description
  - Indexes: ...
  - Foreign keys: ...
  ```
- **Resolution/Processing Logic:** Exact conditions, fallback order, behavior when preconditions are not met.
- **Integration Points:** Services, methods, or hooks that trigger behavior. Specify blocking vs async, idempotency mechanism.
- **Concurrency Protection:** Database-level protection, locking strategy, how race conditions are prevented.

**For FE stories:**

- **Components:** New components to create and existing ones to modify.
- **State Management:** What state is needed and where it lives.
- **API Integration:** Endpoints to consume with request/response shapes.
- **Routing:** New routes or route changes.

## Strict Rules

- Match this format exactly. Do not invent new sections or rename existing ones.
- No vague language. No "handle properly", "etc.", or "as needed".
- No summarization or placeholders.
- Every requirement must be explicit and testable.
- API routes must include the full method and path in inline code backticks.
- Write as if implementation begins immediately after reading.
- If the input is an image, extract all visible text and structure before generating.
- If requirements are ambiguous, ask clarifying questions before writing the spec.


============================================================
SELF-HEALING VALIDATION (max 2 iterations)
============================================================

After producing documentation, validate completeness:

1. Verify all required sections are present and non-empty.
2. Verify internal cross-references and links resolve correctly.
3. Verify no placeholder text remains ("{TODO}", "[TBD]", "...", "etc.").
4. Verify code examples are syntactically valid.

IF VALIDATION FAILS:
- Identify which sections are incomplete or contain placeholders
- Re-generate only the deficient sections
- Repeat up to 2 iterations

## Next Steps

After delivering the spec, suggest:
- "Run `/arch-review` with this spec to get architect-level feedback before implementation."
- "Or run `/si` to implement this spec directly in the current repo."


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /backend-spec — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
