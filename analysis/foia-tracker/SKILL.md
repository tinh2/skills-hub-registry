---
name: foia-tracker
description: Manage the full Freedom of Information Act (FOIA) and state public records request lifecycle — intake form generation, agency-specific portal routing (FOIA.gov, FBI eFOIA, USCIS, FOIAonline successor portals), statutory clock tracking (20 working days federal + unusual circumstances tolling), exemption-aware redaction stub (b1 classified, b2 internal personnel rules, b3 statutory, b4 trade secrets, b5 deliberative, b6 personal privacy, b7 law enforcement, b8 financial institutions, b9 oil wells), appeal letter generator with case citations, response quality auditor (over-redaction detection, missing-page detection), and OPEN Government Act fee-waiver request templates. TRIGGER on "FOIA", "public records request", "5 U.S.C. § 552", "open records", "sunshine law", "freedom of information", "FOIA appeal", "FOIA redaction", "agency response", "FOIA backlog", "open government". Used by journalists, government accountability nonprofits, attorneys, agency FOIA officers, and researchers.
version: "1.0.0"
category: analysis
platforms:
  - CLAUDE_CODE
---

# FOIA Request Lifecycle Tracker

You manage the full FOIA / state public records request lifecycle — for both requesters (journalists, attorneys, accountability groups) and agency FOIA officers responding to requests. The federal backlog topped 200k pending requests in 2026; tooling that compresses any stage of the lifecycle is high-leverage.

============================================================
=== PRE-FLIGHT ===
============================================================

Verify:

- [ ] **Side**: requester (filing) OR agency (responding)? Different workflows.
- [ ] **Jurisdiction**: federal (5 U.S.C. § 552) OR state (each state has its own statute — CA Public Records Act, TX Public Information Act, NY Freedom of Information Law, FL Sunshine Law, etc. — wildly different timelines).
- [ ] **Target agency**: which federal/state agency? Some have dedicated portals (FBI eFOIA, USCIS Electronic Reading Room, DHS FOIA Online). Multi-agency requests get bounced.
- [ ] **Records scope**: specific document set / time range / officials? Vague requests get denied as "burdensome." Narrow scope = faster response.
- [ ] **Fee posture**: commercial (full fees), educational/journalism (search only), public-interest (waiver eligible).

Recovery:

- If jurisdiction unclear, default to federal and surface the state-specific differences as TODO.
- For multi-agency requests, generate one request per agency rather than a single shotgun letter.

============================================================
=== PHASE 1: INTAKE FORM GENERATOR ===
============================================================

Generate a standards-compliant FOIA request letter:

**Required elements** (federal):

- Statement: "This is a request under the Freedom of Information Act, 5 U.S.C. § 552."
- Records description: specific enough to allow a "professional employee familiar with the subject area to locate the records with a reasonable amount of effort" (5 C.F.R. § 294.106(a)).
- Time range.
- Format preferred (electronic, native format, OCR-readable PDF).
- Fee category and waiver request (if applicable).
- Expedited processing request (if eligible — imminent threat to life/safety, urgency to inform the public).
- Contact info + mailing/email address for response.

**Pre-built templates by category**:

- Records about a specific person (Privacy Act waiver attached if subject is requester).
- Records about a specific event or incident (date range + agency component).
- Policy / rule / guidance documents.
- Contract or grant records (cite SAM.gov reference).
- Communications / correspondence (cite participants + keywords).
- Statistical / aggregate data (cite specific database if known).

VALIDATION: Generated letter cites § 552 correctly, includes all required elements, and the records description passes a "specificity" review (would a third party know what to search for?).

FALLBACK: If records description is too vague, refuse to generate — prompt user to narrow.

============================================================
=== PHASE 2: AGENCY PORTAL ROUTING ===
============================================================

Route the request to the correct intake mechanism per agency:

| Agency           | Portal / channel                                                    | Notes                                         |
| ---------------- | ------------------------------------------------------------------- | --------------------------------------------- |
| FBI              | efoia.fbi.gov                                                       | Has its own Records/Information Dissemination |
| USCIS            | first.uscis.gov                                                     | Use eRequest for A-file requests              |
| DHS components   | Component-specific (TSA, CBP, ICE, USCIS)                           | Component-level FOIA officers                 |
| DOJ              | foiarequest.justice.gov                                             | Component routing (FBI, ATF, DEA, USMS, BOP)  |
| State Department | foia.state.gov                                                      | Diplomatic cables = long timelines            |
| HHS / CMS / FDA  | FDA has its own platform (post-2025 modernization)                  |                                               |
| EPA              | epa.gov/foia                                                        | High-volume agency                            |
| GSA              | gsa.gov/foia                                                        | Operates FOIA.gov portal infrastructure       |
| Other federal    | foia.gov (unified portal)                                           | Auto-routes to component                      |
| State agencies   | varies — `state.gov/foia` not enough — check the specific state DOJ |                                               |

Each portal accepts: PDF/MS Word OR direct form input. Generate both formats — some agencies still mail-only for classified or pre-decisional materials.

VALIDATION: Portal URL is current (not deprecated post-FOIAonline sunset).

============================================================
=== PHASE 3: STATUTORY CLOCK TRACKER ===
============================================================

Federal: agency has **20 working days** from receipt to issue a determination (5 U.S.C. § 552(a)(6)(A)). Extensions:

- 10 additional working days for "unusual circumstances" (must be in writing, citing one of three statutory reasons).
- Indefinite tolling permitted while the agency seeks clarification from the requester.
- "Multitrack" processing: simple vs complex queue. Asking for the simple queue speeds response.

State: ranges from 1 business day (FL) to 60+ days (DE without justification).

Generate a tracker (SQLite or JSON):

```json
{
  "request_id": "...",
  "agency": "...",
  "filed_at": "ISO8601",
  "ack_received": "ISO8601 or null",
  "determination_due": "computed",
  "extensions": [{"reason": "...", "ends": "..."}],
  "tolling_periods": [{"start": "...", "end": "...", "reason": "clarification requested"}],
  "interim_releases": [...],
  "final_response": null,
  "status": "intake|searching|reviewing|appealing|closed"
}
```

Send reminder when due date is in 5/2/0 days. After due date, generate the "constructive denial" appeal trigger.

VALIDATION: Working-day math respects federal holidays + weekends. Tolling is excluded from clock.

============================================================
=== PHASE 4: EXEMPTION-AWARE REDACTION STUB ===
============================================================

(For agency side: generate a redaction proposal that flags candidate text per exemption. Agency FOIA officer must review — this is a stub, not a legal determination.)

The nine FOIA exemptions:

| #   | Exemption                                    | Typical patterns to flag                                      |
| --- | -------------------------------------------- | ------------------------------------------------------------- |
| b1  | National defense / foreign policy classified | "TOP SECRET", "SECRET", "CONFIDENTIAL", classification stamps |
| b2  | Internal personnel rules                     | Operating manuals, employee schedules                         |
| b3  | Statutorily exempt                           | Cite specific statute (e.g., 26 USC § 6103 for tax data)      |
| b4  | Trade secrets / confidential commercial      | Pricing, formulas, proprietary methods (Argus Leader test)    |
| b5  | Deliberative / pre-decisional / privileged   | Draft documents, attorney work product, deliberative emails   |
| b6  | Personal privacy                             | SSN, DOB, home address, medical info, personnel files         |
| b7  | Law enforcement                              | Subdivided b7(A)-(F); informant identities, techniques        |
| b8  | Financial institution examination            | Bank examination reports                                      |
| b9  | Oil well geological data                     | Rare                                                          |

For each candidate redaction, output: `{page, span, suggested_exemption, reasoning, confidence}`. Agency officer accepts/rejects. Foreseeable harm standard (FOIA Improvement Act 2016) requires identifying specific harm — generate the harm statement template per exemption.

VALIDATION: Output is a proposal, not a fait accompli. Every suggested redaction has a citable exemption AND a foreseeable-harm statement template.

CRITICAL: Output is for human review. Never auto-apply redactions in production agency workflows — that's a § 552 violation waiting to happen.

============================================================
=== PHASE 5: RESPONSE QUALITY AUDITOR (REQUESTER SIDE) ===
============================================================

When the agency response arrives, audit for:

1. **Page count delta** — did they release everything claimed? Compare cover letter count to actual PDF count.
2. **Over-redaction signals** — fully-redacted pages, every-paragraph black bars, missing context.
3. **Unjustified exemptions** — exemptions cited without specific harm explanation (post-2016 standard).
4. **Withheld in full** — "no documents" claims should be skeptically reviewed; suggest reformulating.
5. **Glomar response** ("can neither confirm nor deny") — narrow path to challenge.
6. **Categorical denials** — courts disfavor; suggests appeal viability.

Generate `audit_report.md` with appeal-viability score (1-5) and specific findings.

VALIDATION: Audit produces a concrete next-step recommendation (accept / appeal / re-formulate / litigation).

============================================================
=== PHASE 6: APPEAL LETTER GENERATOR ===
============================================================

If denial or partial release is unsatisfactory, generate an administrative appeal:

- Address to agency's FOIA Appeals officer (look up via Department of Justice OIP guidance).
- Cite specific exemption claims and explain why they fail.
- Cite case law:
  - **Argus Leader Media v. USDA** (2019) — narrowed b4 to "customarily and actually" confidential.
  - **DOJ v. Reporters Committee** (1989) — b6/b7C balancing test for personal privacy.
  - **Lindsey v. United States** — foreseeable harm requirement.
  - **NLRB v. Sears, Roebuck & Co.** (1975) — b5 deliberative process.
- Request fee waiver clarification if denied.
- 90-day deadline for federal administrative appeal (5 U.S.C. § 552(a)(6)(A)(ii)).

VALIDATION: Appeal cites specific exemption claim + counter-argument + case authority. Filed within 90 days.

============================================================
=== PHASE 7: FEE WAIVER + EXPEDITED PROCESSING ===
============================================================

**Fee waiver criteria** (28 C.F.R. § 16.10):

1. Subject concerns "operations or activities of the government"
2. Disclosure is "likely to contribute significantly to public understanding"
3. Public interest, not commercial interest

Generate fee-waiver template that addresses all three prongs concretely (not boilerplate).

**Expedited processing criteria**:

- Imminent threat to life or physical safety, OR
- Urgency to inform the public + requester is "primarily engaged in disseminating information."

Generate expedited-processing certification including the "I certify that my statement is true and correct to the best of my knowledge" sworn statement (5 U.S.C. § 552(a)(6)(E)(vi)).

VALIDATION: Templates address specific statutory prongs, not generic justification.

============================================================
=== SELF-REVIEW ===
============================================================

Score 1–5:

- **Complete**: Intake + routing + clock + redaction stub + audit + appeal + waiver all delivered?
- **Robust**: Working-day math correct? Tolling excluded? Exemption proposals tied to foreseeable harm?
- **Clean**: Letters reference current statutory citations, not deprecated language?
- **FOIA-credible**: Would a journalist who's filed 100+ requests OR an agency FOIA officer recognize the templates as production-ready?

Common gap: assuming all 9 exemptions apply equally — b1/b3/b7 require very specific justifications.

============================================================
=== LEARNINGS CAPTURE ===
============================================================

Append to `~/.claude/skills/foia-tracker/LEARNINGS.md`:

## <YYYY-MM-DD> — <jurisdiction, agency, side>

- **What worked:**
- **What was awkward:**
- **Suggested patch:**
- **Verdict:** [Smooth / Minor friction / Major friction]

============================================================
=== STRICT RULES ===
============================================================

- Never auto-apply redactions to an agency response without human review. Wrong redaction = constitutional violation.
- Never cite exemptions without paired foreseeable-harm rationale. Post-2016 FOIA Improvement Act requires it.
- Never overlook tolling. If agency requested clarification, the clock paused — don't accuse them of missing the deadline they're entitled to extend.
- Never use deprecated language (e.g., FOIAonline references — sunset April 2024).
- Always check state law when the target is state agency, not federal. State timelines and exemptions differ materially.
