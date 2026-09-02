---
name: jd-craft
description: "Generate a bias-free, ATS-optimized, skills-based job description for 2026. Triggers: \"job description\", \"JD\", \"write a JD\", \"open req\", \"we're hiring\"."
version: "1.0.1"
category: analysis
platforms:
  - CLAUDE_CODE
---

# Job Description Generator

You generate job descriptions that (a) attract a wide qualified candidate pool, (b) survive ATS filters, (c) comply with pay-transparency laws, and (d) signal a credible employer brand. Bias-free is the floor, not the ceiling.

The signal is real: A Hewlett Packard study found women apply when they meet 100% of stated criteria; men at 60%. The wording of "required" vs "preferred", "5+ years" vs "demonstrated experience", "guru" vs "engineer" directly shapes who self-selects.

============================================================
=== PRE-FLIGHT ===
============================================================

Verify:

- [ ] **Role specifics**: title, level (IC1-IC7 / M1-M5), team, manager, comp band, location/remote policy.
- [ ] **State / country compliance**: pay transparency required in CA, CO, CT, HI, IL (Jan 2025), MD, NV, NY, RI, WA, DC. Federal contractors have additional disclosures. International: EU Pay Transparency Directive transposed in many member states by 2026.
- [ ] **Skills-based scope**: what are the 5-7 specific skills that determine success in year 1? Not "years of experience" as a proxy.
- [ ] **Hiring stage**: do you have a structured interview kit yet? (If not, route to /interview-kit-builder first — the JD and kit should match.)

Recovery:

- If comp band undefined, refuse to publish in transparency-required states and surface the requirement.
- If role title is jargony ("Code Ninja", "Growth Hacker"), suggest the standardized title for ATS search visibility.

============================================================
=== PHASE 1: BIAS-FILTER PASS ===
============================================================

Maintain a banned-pattern list. Categories:

**Gender-coded**:

- Masculine-skewed: rockstar, ninja, guru, aggressive, dominant, fearless, competitive, "thick skin", combat, hunt, conquer, killer.
- Feminine-skewed (also a problem): nurturing, supportive without context, gentle, compassionate when not core to role.

**Age-coded**:

- "Digital native", "young and hungry", "recent grad", "energetic", "fresh perspective" (often code for young).
- Conversely: "seasoned", "mature" (often code for older).

**Ability-coded**:

- "Walk the floor", "hit the ground running", "see eye to eye", "lend an ear".

**Race / cultural-coded**:

- "Culture fit" (use "culture add"), "tribe", "blackballed".

**Class-coded**:

- "Top-tier university" (drop unless regulatory), "Ivy League graduate".

**Vague status terms**:

- "Rockstar", "wizard", "guru" — banned all sides.

For each match, suggest the inclusive replacement. Refuse to publish if any banned term remains.

VALIDATION: A red-team fixture of 30 JDs with known violations — the filter catches ≥ 28.

============================================================
=== PHASE 2: SKILLS-BASED REQUIREMENTS ===
============================================================

Convert from "years of experience" to "demonstrated skills":

Bad: "5+ years of React experience."
Good: "You've shipped at least one React production app and can debug a re-render cycle."

Bad: "Bachelor's degree in CS required."
Good: "Proficiency in software design and one statically-typed language. CS degree, bootcamp, or self-taught all welcome."

Rule: only keep "X years required" if regulatory (e.g., FAA pilot hours, AMA medical license years). Otherwise convert to a behavioral skill.

Split requirements into two buckets:

- **Must have (3-5 max)**: things truly required for day 1. If you can train it, it doesn't belong here.
- **Nice to have (3-5)**: would accelerate ramp but the candidate can learn.

VALIDATION: "Must have" list ≤ 5 items. Each is a behavioral / skill description, not a credential.

============================================================
=== PHASE 3: PAY TRANSPARENCY BLOCK ===
============================================================

Auto-generate the comp section based on detected location. Default template:

```
## Compensation

Base salary range: $X–$Y (USD). This range reflects what we'd typically offer to a
candidate hired at this level for this location. The actual offer depends on level,
location-adjusted band, and equity grant.

Equity: This role is eligible for equity grants. Typical grant for this level is X–Y
options or RSUs (4-year vest, 1-year cliff).

Benefits: Health/dental/vision (we cover 100% of employee, 75% of dependents),
401(k) with 4% match, 20 days PTO + holidays + birthday off, $X/year learning budget.

Total compensation: We target {percentile} of {peer cohort} for this role/level.
```

State-specific adjustments:

- **CA**: must include hourly range for non-exempt roles.
- **CO**: must include "expected close date" if known.
- **NY/NYC**: must include "good faith" salary range.
- **WA**: must include compensation AND general description of benefits.

VALIDATION: For each state in the listing's location field, the appropriate disclosures are present.

============================================================
=== PHASE 4: ATS STRUCTURE ===
============================================================

Up to 75% of applications are filtered by ATS before a recruiter sees them. Generate JD as **ATS-parseable**:

- Single column.
- Headings as plain text (`## About the role`, not images of headings).
- No tables, no graphics in the JD body.
- Bullet lists, not paragraphs of dense text.
- Skill keywords listed naturally in the prose (so candidate ATS-matching works both ways).
- Action verbs, present tense, second person ("You'll ship...", "You'll partner with...").
- Avoid acronym-only ("KPI", "OKR") — spell out at first mention.

VALIDATION: JD rendered as plain text retains all critical information. No essential content lives in images.

============================================================
=== PHASE 5: CHANNEL VARIANTS ===
============================================================

Generate variants for each channel:

1. **Internal careers page** (full version, ~500-800 words).
2. **LinkedIn long-form** (~400-600 words; LinkedIn truncates after ~2000 chars in the feed preview, so lead with hook).
3. **Indeed structured** (job title ≤ 100 chars, summary ≤ 1500 chars, ATS-keyword density tuned).
4. **Slack / X / community announcement** (≤ 280 chars + link).
5. **Lever / Greenhouse / Workday import** (CSV or JSON matching their schema).

VALIDATION: Each variant respects its character limit and surfaces the role + compensation + apply-link in the first viewport.

============================================================
=== PHASE 6: PROCESS TRANSPARENCY ===
============================================================

Top-quartile candidates pre-screen the process. Include in the JD:

- **Interview stages** (with rough duration): "30-min recruiter call → 60-min hiring manager → 90-min technical → 90-min cross-functional → reference checks → offer."
- **Expected timeline**: "We aim to make a decision within 2 weeks of first conversation."
- **Visa / sponsorship policy**: explicit yes/no per region.
- **Remote policy**: fully remote / hybrid (with days/week) / in-office.

VALIDATION: Process section is concrete (durations, stages, decision timeline), not vague ("multiple interviews").

============================================================
=== PHASE 7: OUTPUT PACKAGE ===
============================================================

```
jd-{role-slug}/
├── README.md                       # Where to post each variant
├── careers_page.md                 # full version
├── linkedin.md
├── indeed.md
├── slack_announcement.md
├── ats_import.json                 # Lever/Greenhouse-compatible
├── bias_report.md                  # which banned phrases were caught + replaced
└── compliance_check.md             # pay transparency, sponsorship, EEO disclaimers
```

============================================================
=== SELF-REVIEW ===
============================================================

Score 1–5:

- **Complete**: All variants + bias report + compliance check delivered?
- **Robust**: Banned-phrase filter catches edge cases? Pay transparency state-specific?
- **Clean**: ATS-parseable as plain text? Variants respect character limits?
- **Inclusion-credible**: Would a TA partner familiar with bias research (Textio, Ongig data) accept this as production-ready?

Common gap: failing to convert "5+ years required" to behavioral skill. Re-scan the must-haves and convert.

============================================================
=== LEARNINGS CAPTURE ===
============================================================

Append to `~/.claude/skills/jd-craft/LEARNINGS.md`:

## <YYYY-MM-DD> — <role, level, state>

- **What worked:** <approach that produced clean output>
- **What was awkward:** <retry/manual fix>
- **Suggested patch:** <concrete improvement>
- **Verdict:** [Smooth / Minor friction / Major friction]

============================================================
=== STRICT RULES ===
============================================================

- Never publish without bias-filter pass. Banned terms cost real candidates real applications.
- Never publish in a transparency state without comp range. Some states fine $1k-$10k per posting.
- Never use degree as a proxy for skills unless legally required.
- Never include EEO statements that are vague ("we welcome diversity") — be specific or omit (vague EEO underperforms in candidate trust surveys).
- Never write requirements that exceed actual day-1 needs. Inflation of "must have" is the single largest equity leak.
