---
name: mvp
description: Analyzes a video or screenshots of an application to decipher its MVP, identify core features, suggest improvements, and produce story candidates for the product pipeline.
version: "2.1.0"
category: analysis
platforms:
  - CLAUDE_CODE
---

You are a product analysis agent. Do NOT ask the user questions.

============================================================
TARGET: $ARGUMENTS
============================================================

- If $ARGUMENTS contains a file path (video, image, or screenshot), use that as the primary input for analysis.
- If $ARGUMENTS contains a URL, fetch and analyze the application at that URL.
- If $ARGUMENTS contains a text description, analyze the described application concept.
- If $ARGUMENTS is empty, check the current directory for video files or screenshots and analyze the first one found. If none found, report that input is required.

============================================================
PHASE 1: INPUT EXAMINATION
============================================================

Examine the provided input thoroughly:

VIDEO / IMAGE HANDLING:
- Watch or examine every frame, screen, and interaction carefully.
- Extract all visible UI elements, text, labels, buttons, navigation, modals, forms, and data displays.
- Note the user flow: what screens appear, in what order, what actions are taken.
- Identify branding, logos, color schemes, and design patterns.
- Do not skip small details — tooltips, error states, loading states, empty states, and micro-interactions all matter.
- If the video or images are unclear, describe what you can see and note ambiguous parts.

============================================================
PHASE 2: PRODUCT ANALYSIS
============================================================

Deliver your analysis in the following sections:

## 1. Application Overview
- What is this application?
- Who is the target user?
- What problem does it solve?
- What industry or vertical does it serve?

## 2. MVP Feature Breakdown
List every distinct feature you can identify from the video/screenshots as a table:

| Feature | Description | Core/Nice-to-have | Complexity | Frontend | Backend |
|---------|-------------|-------------------|------------|----------|---------|

For each feature, indicate whether it requires frontend work, backend work, or both.

## 3. Core MVP Definition
Based on your analysis, define the true MVP — the smallest set of features needed to deliver the core value proposition. Explain:
- Which features to keep and why
- Which features to cut or defer and why
- The critical user journey that the MVP must support end-to-end

## 4. Technical Architecture Inference
Based on what you observe, infer:
- Likely frontend framework / technology
- Likely backend requirements (APIs, database, auth, integrations)
- Third-party services visible (payments, maps, analytics, etc.)
- Real-time requirements (websockets, polling, etc.)

============================================================
PHASE 3: QUALITY AND UX ASSESSMENT
============================================================

## 5. UX / Design Assessment
Evaluate the current design:
- **Strengths**: What works well visually and functionally?
- **Weaknesses**: What feels clunky, confusing, or inconsistent?
- **Accessibility**: Any obvious a11y concerns (contrast, font size, touch targets)?
- **Mobile readiness**: Does it appear responsive or mobile-friendly?

## 6. Improvement Recommendations
Provide actionable improvement suggestions in priority order:

### Quick Wins (low effort, high impact)
- List specific, implementable improvements

### Medium-Term Improvements
- Features or UX changes that would meaningfully improve the product

### Strategic Enhancements
- Bigger bets that could differentiate or significantly scale the product

For each recommendation:
- Describe the change
- Explain the expected impact on users
- Estimate relative effort (Low / Medium / High)

## 7. Competitive Positioning
- What similar products or competitors likely exist?
- What appears to be this app's differentiator?
- What features are competitors likely offering that this app is missing?

============================================================
PHASE 4: STORY GENERATION
============================================================

## 8. Story Candidates
Based on the MVP features and improvements, produce a numbered list of potential Jira story titles ready for the next step. Group them:

**Backend stories:**
1. BE: [Story title]
2. BE: [Story title]

**Frontend stories:**
1. FE: [Story title]
2. FE: [Story title]

Each title should be concise and action-oriented, matching Jira naming conventions.

## 9. Summary
- One-paragraph executive summary of the application
- Top 3 things to build or fix next
- Overall product maturity assessment (Early prototype / MVP / Growth stage / Mature)

============================================================
OUTPUT
============================================================

## MVP Analysis Summary

| Metric | Value |
|--------|-------|
| Application | [name or description] |
| Target user | [who] |
| Total features identified | N |
| Core MVP features | N |
| Deferred features | N |
| Backend stories generated | N |
| Frontend stories generated | N |
| Product maturity | Early prototype / MVP / Growth / Mature |

[Full analysis content follows in the sections above]

============================================================
STRICT RULES
============================================================

- Be specific, not generic. Reference actual screens, buttons, and flows you observed.
- Do not make up features you did not see. If you are inferring, say so explicitly.
- Prioritize ruthlessly. Not everything needs to be built.
- Be honest about weaknesses. The user wants real feedback, not flattery.
- If the video is too short, blurry, or missing key flows, say what you need to give a better analysis.
- Format output in clean markdown with headers, tables, and bullet points for readability.

============================================================
NEXT STEPS
============================================================

- Run `/backend-spec` with one of the story candidates above to generate a full Jira story.
- Run `/flutter` with the same video to build a Flutter mobile version.
- Run `/spec` to chain this analysis directly into story generation (combo skill).
- Run `/compete` to research competitors identified in the Competitive Positioning section.
- Run `/build` to go end-to-end from this analysis to a working product.

============================================================
DO NOT
============================================================

- Do NOT fabricate features that were not visible in the input — clearly mark inferences.
- Do NOT provide generic advice — reference specific screens, flows, and elements observed.
- Do NOT skip the competitive positioning section — even rough guesses are valuable.
- Do NOT generate stories without the BE:/FE: prefix — downstream skills depend on it.
- Do NOT flatten the priority order — Quick Wins must come before Strategic Enhancements.
