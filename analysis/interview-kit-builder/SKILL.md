---
name: interview-kit-builder
description: Generate a complete structured interview kit for a role — 3-5 role-specific competencies, one behavioral (STAR-format) question per competency, 1-5 scoring rubric with explicit behavioral anchors at each level, per-panel scorecards, interviewer debrief template, calibration session script, and a decision matrix. Backed by 2026 research showing rubric-based structured interviews lift hiring accuracy 34% and cut bias (NACE 2026: 87% of employers use behavioral interviews as their primary skills assessment). Output is platform-ready (Lever, Greenhouse, Ashby, Workday, plain markdown). TRIGGER on "interview kit", "interview rubric", "scorecard", "structured interview", "behavioral questions", "interview loop", "interviewer training", "hiring loop", or any user setting up assessment for a role.
version: "1.0.0"
category: analysis
platforms:
  - CLAUDE_CODE
---

# Structured Interview Kit Builder

You generate a complete structured interview kit. The 2026 evidence: structured rubric-based interviews improve hiring accuracy 34% (Journal of Applied Psychology) and 87% of employers report behavioral interviews as their primary assessment method (NACE 2026). The gap between "we did interviews" and "we ran a structured loop" predicts hire performance better than years of experience or credentials.

A structured interview means: same questions, same rubric, same panel composition, calibrated scoring. Anything else is unstructured chat with a candidate.

============================================================
=== PRE-FLIGHT ===
============================================================

Verify:

- [ ] **Role + level**: title, IC1-IC7 or M1-M5, function (eng/PM/design/sales/marketing/ops/etc.).
- [ ] **JD reference**: must-have skills from the JD (5 max). Kit's competencies derive from JD — don't invent new ones here.
- [ ] **Loop structure**: how many interviews, who's on each, total candidate time. Default: 4 interviews × 60 min each = 4 hours of candidate time. Above 6 hours is candidate-hostile.
- [ ] **ATS platform**: Lever, Greenhouse, Ashby, Workday, plain markdown. Each has a different scorecard import format.
- [ ] **Bar-raiser / hiring committee**: does the org have one? If yes, the kit includes a bar-raiser-specific scorecard.

Recovery:

- If JD doesn't exist yet, route to /jd-craft first. Kit and JD must reference the same competencies.
- If loop is undefined, propose a default 4-round loop and surface it for confirmation.

============================================================
=== PHASE 1: COMPETENCY DEFINITION ===
============================================================

Extract 3-5 competencies from the JD's must-haves. Examples by role:

**Senior Backend Engineer**:

1. System design at scale
2. Production debugging / on-call
3. Code quality (testing, observability, security mindset)
4. Cross-functional partnership
5. Mentorship / leverage

**Sr. PM**:

1. Customer discovery
2. Roadmap prioritization under constraints
3. Cross-functional execution
4. Quantitative analysis
5. Communication & narrative

**B2B AE**:

1. Discovery / qualification (MEDDPICC or similar)
2. Multi-threading complex deals
3. Forecast accuracy / pipeline hygiene
4. Negotiation / closing
5. Customer empathy

Each competency must be observable — i.e., you can describe what "good" looks like via behavior, not credentials.

VALIDATION: ≤ 5 competencies. Each has a one-sentence behavioral definition.

============================================================
=== PHASE 2: BEHAVIORAL QUESTIONS (STAR FORMAT) ===
============================================================

One behavioral question per competency. STAR = Situation, Task, Action, Result.

Template:

> "Tell me about a time when [specific challenging situation that maps to this competency]. What was the [stakes/constraint]? What did you do? What was the outcome — and what would you do differently?"

Examples:

**System design at scale**:

> "Tell me about the highest-traffic system you've designed or significantly refactored. What were the load characteristics, the SLOs, and the biggest design trade-off you made? Looking back, what would you change?"

**Customer discovery (PM)**:

> "Walk me through a time when customer research changed your roadmap. How did you choose who to interview? What was the original hypothesis vs what you learned? What did you ship as a result?"

**Forecast accuracy (AE)**:

> "Describe a quarter where your forecast was significantly off — either over or under. What information were you missing? What's your process now to catch that signal earlier?"

Per question, include 3-5 **follow-up probes** the interviewer should use to dig deeper if the candidate stays high-level.

VALIDATION: Every competency has exactly one primary question + ≥ 3 follow-up probes. Questions don't reference protected categories.

============================================================
=== PHASE 3: 1-5 RUBRIC WITH BEHAVIORAL ANCHORS ===
============================================================

For each question, define what each score level looks like — not just "good" / "bad" but the specific signals.

Template (system design example):

| Score | Behavioral Anchor                                                                                                                                                                               |
| ----: | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|     5 | Drew the system from scratch, identified the bottleneck before being asked, explained the failure modes, proposed a measurable rollout plan, and connected design choices to business outcomes. |
|     4 | Drew the system cleanly, named at least one significant trade-off and articulated why. Some failure modes considered.                                                                           |
|     3 | Could describe a system they worked on, but didn't independently surface trade-offs without prompting.                                                                                          |
|     2 | Confused major concepts (e.g., consistency vs availability, latency vs throughput). Couldn't sketch a clean design.                                                                             |
|     1 | Could not engage with the design question; deferred to "we used X service" without depth.                                                                                                       |

VALIDATION: Each score has a behavioral anchor, not "exceeds expectations." Anchor describes observable evidence.

============================================================
=== PHASE 4: PER-PANEL SCORECARD ===
============================================================

Generate a scorecard per interviewer in the loop:

```markdown
# Scorecard — {Role} — {Interview Name}

Candidate: {name}
Interviewer: {name}
Date: {date}

## Competencies Assessed

- {Competency 1}: \_\_\_/5 (one anchor sentence with specific evidence)
- {Competency 2}: \_\_\_/5

## Notable Strengths (specific behaviors observed)

-
-

## Notable Concerns (specific behaviors observed)

-
-

## Reservations / Open Questions

-

## Recommendation

- [ ] Strong hire
- [ ] Hire
- [ ] No hire
- [ ] Strong no hire

(Pick one. "Lean hire" / "lean no hire" forbidden — calibration shows these collapse to "hire" 90% of the time. Force commitment.)
```

VALIDATION: Each interviewer's scorecard covers ≤ 3 competencies (avoid one interviewer scoring all 5 — accuracy degrades).

============================================================
=== PHASE 5: CALIBRATION SESSION ===
============================================================

Generate a calibration session script for the panel BEFORE interviews start:

1. **Mock candidate answer** for each question, written as a "3-out-of-5" baseline (so panel can see what "meets bar" looks like).
2. **Panel scoring exercise**: each interviewer independently scores the mock answer; group then debates and resolves to a shared score.
3. **Walk through the rubric anchors aloud** to surface interpretation differences.
4. **Set the hiring bar**: what does the candidate's average score need to be to advance? Default: ≥ 3.5 average across competencies, no single competency < 3.

VALIDATION: Calibration script is ≤ 1 page, takes 30-45 min to run.

============================================================
=== PHASE 6: DEBRIEF TEMPLATE ===
============================================================

Per-loop debrief template (post-loop, all interviewers + recruiter + hiring manager):

```markdown
# Debrief — {Candidate} — {Role}

## Round-by-round scores

| Round | Interviewer | Competency | Score | Key evidence |
| ----- | ----------- | ---------- | ----- | ------------ |
| Phone | Recruiter   | Comm       | 4     | ...          |
| HM    | {name}      | Leadership | 4     | ...          |

Average competency score: X.X / 5
Min competency score: X / 5

## Discussion (5-10 min)

- Strongest signal:
- Weakest signal:
- Outliers (any score ≥ 1 point off the panel mean): {who/what}
- Reservations that didn't show up in writing:

## Decision

- [ ] Offer — {level} — {comp band}
- [ ] No offer — primary reason: {one sentence}
- [ ] Hold — additional reference call / second technical / etc.

## If offer: assigned ramp manager + first-30-day plan creator
```

VALIDATION: Debrief produces a single decision in writing, attributable, with rationale.

============================================================
=== PHASE 7: ATS IMPORT ===
============================================================

Generate platform-specific exports:

- **Greenhouse**: scorecard YAML + interview kit attachment.
- **Lever**: feedback form schema + question library import.
- **Ashby**: structured interview kit JSON.
- **Workday**: questionnaire XML.
- **Plain**: a single markdown file with all sections.

VALIDATION: Generated file imports without errors into the target platform's sandbox.

============================================================
=== SELF-REVIEW ===
============================================================

Score 1–5:

- **Complete**: All 7 phases delivered? Rubric anchors specific to behavior?
- **Robust**: Calibration session is actionable (mock answer + scoring exercise)?
- **Clean**: Scorecard fits on 1 page? Debrief template is tight?
- **Hiring-credible**: Would a recruiting leader at a structured-interview-mature company (Google, Amazon, Stripe) accept this as kit-ready?

Common gap: rubric anchors written as "exceeds/meets/below" rather than observable behaviors. Rewrite each anchor with specific evidence.

============================================================
=== LEARNINGS CAPTURE ===
============================================================

Append to `~/.claude/skills/interview-kit-builder/LEARNINGS.md`:

## <YYYY-MM-DD> — <role, level, loop length>

- **What worked:**
- **What was awkward:**
- **Suggested patch:**
- **Verdict:** [Smooth / Minor friction / Major friction]

============================================================
=== STRICT RULES ===
============================================================

- Never write "lean hire / lean no hire". Calibration shows these are noise; force a binary.
- Never use questions that probe protected categories (family status, religion, age, etc.).
- Never score the candidate's school, prior employer's prestige, or accent. Score behavior on the rubric.
- Never reuse the same question across multiple panels for a single candidate. Repetition is wasted candidate time and panel signal.
- Always include calibration. Skipping it is the single biggest source of inter-rater noise.
