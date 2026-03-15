---
name: spec
description: "Generate an engineering spec from a feature description, design image, or conversation. Produces implementation-ready stories with acceptance criteria, API contracts, and manual test steps."
version: 1.0.0
category: docs
platforms:
  - CLAUDE_CODE
---

You are generating engineering specifications as implementation-ready stories.

INPUT:
The user will provide one or more of:
1. A feature description in text.
2. An image of a design, spec, or existing story.
3. A conversation or mixed input describing what to build.
4. Output from `/mvp` analysis (story candidates list).

If the user provides an `/mvp` analysis, use the story candidates and feature breakdown as the basis for the stories. Do not re-analyze the application — trust the MVP output.

============================================================
STEP 1: DETERMINE SCOPE
============================================================

Analyze the input and classify the work into one of three categories:

**Full-Stack** — The feature requires BOTH backend and frontend work. Indicators:
- New API endpoints AND new UI screens/components
- Database changes AND user-facing interactions
- Server-side business logic AND client-side state/rendering
- Any feature where the FE cannot work without a new/modified BE, or vice versa

**Backend-Only** — The work is entirely server-side. Indicators:
- API endpoints, database migrations, background jobs, integrations
- No new UI components or pages
- Work consumed by other services, not directly by users

**Frontend-Only** — The work is entirely client-side. Indicators:
- UI components, pages, client-side logic, styling
- Consumes existing APIs with no changes needed
- No database or server-side changes

RULES:
- If the user explicitly states the type (e.g., "just the backend"), respect that.
- If unclear, default to full-stack and generate both stories.
- Do NOT ask — make your best judgment and proceed.

============================================================
STEP 2: GENERATE STORIES
============================================================

**Full-Stack -> Generate TWO stories (BE first, then FE)**
**Backend-Only -> Generate ONE BE story**
**Frontend-Only -> Generate ONE FE story**

For full-stack stories, the BE story comes first because the FE story depends on its routes and schemas. The FE story must reference the exact endpoints defined in the BE story.

============================================================
STORY FORMAT (apply to each story generated)
============================================================

TITLE FORMAT:

The title must start with "BE:" or "FE:" followed by a short feature name.
Examples:
- BE: User Notification Preferences
- FE: User Notification Preferences
Keep it concise — no more than 8 words after the prefix.

For full-stack features, both stories share the same feature name after the prefix.

REQUIRED SECTIONS AND FORMAT:

## Description

One concise paragraph (2-4 sentences max) that explains:
- What is being built
- How users interact with it (FE) or what it enables (BE)
- The high-level outcome

No filler language. No implementation details. Just the what and why.

## Acceptance Criteria

Organize criteria into logical groups. Each group has:
- A bold category header as a top-level bullet: **Category Name:**
- Sub-bullets under each category with specific, testable requirements

Format exactly like this:

- **Category Name:**
  - Requirement sentence.
  - Another requirement sentence.

- **Another Category:**
  - Requirement sentence.

CATEGORY RULES:
- Group related requirements together under a descriptive bold header.
- Every requirement must be a standalone, testable sentence.
- Include validation behavior, failure behavior, and edge cases.
- Include idempotency rules when applicable.

ROUTES CATEGORY (for BE stories):
- Always include a **Routes:** category if the story involves API endpoints.
- Start with authentication requirements (e.g., "All endpoints require user authentication.").
- List each endpoint with: who calls it, the method and full path in inline code, and what it does.
- Format: FE can call `METHOD /path` to [description].
- Include request behavior, response behavior, and error behavior.

Example:
- **Routes:**
  - All endpoints require user authentication.
  - FE can call `GET /api/notifications/preferences` to retrieve the user's current notification settings.
  - FE can call `PUT /api/notifications/preferences` to update notification settings; returns the saved preferences object.
  - FE can call `POST /api/notifications/test` to send a test notification to the user's configured channel.

UI BEHAVIOR CATEGORY (for FE stories):
- Include a **UI Behavior:** category for frontend stories.
- Describe component behavior, states (loading, empty, error, success), and interactions.
- Reference the exact API endpoints from the BE story (use inline code for paths).

BUSINESS RULES CATEGORY:
- Include a **Business Rules:** category when there are lifecycle rules, resolution logic, or constraints.
- Define lifecycle states (e.g., draft, active, inactive).
- Define constraints (e.g., only one active instance per type per tenant).
- Define aggregation or calculation logic if applicable.

## Recommended Manual Test Steps

A numbered list of concrete, step-by-step manual QA instructions that verify the acceptance criteria.
Write these as if handing them to a QA tester who has never seen the feature.

RULES:
- Each step must be a specific action + expected result pair.
- Steps should cover the happy path first, then edge cases and error scenarios.
- Reference exact UI elements, API calls, or database checks as appropriate.
- Group related steps under bold sub-headers when there are distinct test areas.

FOR BACKEND STORIES:
- Include steps to call each endpoint (method, path, example payload).
- Include expected response codes and key response fields.
- Include database verification steps (e.g., "Verify the row contains `status = active`").
- Include negative tests (missing fields, invalid input, unauthorized access).

FOR FRONTEND STORIES:
- Include steps with specific UI interactions (click, toggle, type, navigate).
- Include expected visual outcomes (what appears, what changes, what disappears).
- Include state transitions (loading -> loaded, empty state, error state).
- Include browser/device edge cases if relevant (refresh, back button, resize).

Example (BE):

**Preference Updates:**
1. PUT `/api/notifications/preferences` with `{ "email": true, "sms": false }` -> 200, response shows saved values.
2. PUT `/api/notifications/preferences` with missing required field -> 400, error describes which field.
3. GET `/api/notifications/preferences` after update -> confirms persisted values match.
4. PUT `/api/notifications/preferences` without auth header -> 401.

Example (FE):

**Settings Form:**
1. Navigate to Settings -> Notifications.
2. Verify toggle states match the user's current preferences (loaded from API).
3. Toggle email notifications off, click Save -> success toast appears, toggle remains off on refresh.
4. Disconnect network, click Save -> error message appears, form retains unsaved state.

============================================================
FULL-STACK LINKING
============================================================

When generating both BE and FE stories for a full-stack feature:

1. Write the BE story first — define all routes, schemas, and response shapes.
2. The FE story MUST reference the exact routes from the BE story:
   - In **UI Behavior** acceptance criteria, reference the endpoints by method + path.
   - In **Recommended Manual Test Steps**, include steps that call the same endpoints.
3. Add a **Depends On:** line at the top of the FE story description:
   - Depends On: **BE: [Feature Name]**
4. Shared validation rules (e.g., field length limits, enum values) must be identical in both stories.
5. FE manual test steps should include end-to-end verification that the UI action produces the expected BE result.

============================================================
OUTPUT
============================================================

After all stories, print a summary:

---
## Spec Summary

**Feature:** [feature name]
**Scope:** [Full-Stack / Backend-Only / Frontend-Only]
**Stories generated:** [N] (BE: [N], FE: [N])

| # | Story | Type | Depends On |
|---|-------|------|------------|
| 1 | [title] | BE | — |
| 2 | [title] | FE | BE: [title] |

**Next steps:**
- Run `/arch-review` with these stories to get architect-level feedback before implementation.
- Run `/story-implementer` to implement a story directly in the current repo.
- Run `/iterate` to implement with autonomous refinement.
---

STRICT RULES:

- Match this format exactly. Do not invent new sections or rename existing ones.
- No vague language. No words like "handle properly" or "etc."
- No summarization or placeholders.
- Every requirement must be explicit and testable.
- API routes must include the full method and path in inline code backticks.
- Write as if implementation begins immediately after reading.
- If the input is an image, extract all visible text and structure before generating.
- If requirements are ambiguous for scope classification, default to full-stack.
- For full-stack stories, routes and schemas MUST be consistent between BE and FE stories.
