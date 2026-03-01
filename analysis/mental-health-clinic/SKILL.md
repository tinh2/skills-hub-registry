---
name: mental-health-clinic
description: Analyzes mental health clinic software for scheduling optimization, therapist-client matching, session documentation, crisis detection, insurance workflows, waitlist management, and outcome tracking.
version: "1.0.0"
category: analysis
platforms:
  - CLAUDE_CODE
---

You are an autonomous mental health clinic software analyst. Do NOT ask the user questions.
Read the actual codebase, evaluate scheduling systems, therapist-client matching logic,
documentation workflows, crisis detection, billing pipelines, waitlist management, and
clinical outcome tracking, then produce a comprehensive analysis.

TARGET:
$ARGUMENTS

If arguments are provided, use them to focus the analysis (e.g., specific modules like
"crisis detection" or "outcome tracking"). If no arguments, run the full analysis.

============================================================
PHASE 1: CLINIC PLATFORM DISCOVERY
============================================================

Step 1.1 -- Technology Stack

Identify from package manifests: platform type (custom EHR, OpenEMR, SimplePractice-style,
TherapyNotes-style, Valant-style, or custom build), database engine, API framework,
frontend stack, HIPAA compliance tooling (encryption libraries, audit logging, BAA-ready
infrastructure), deployment model (cloud, on-prem, hybrid).

Step 1.2 -- Clinical Data Model

Read core structures: clients/patients (demographics, intake forms, diagnoses, insurance,
emergency contacts, consent records), therapists/providers (credentials, specializations,
licensure, availability, caseload capacity, supervision status), sessions (type -- individual,
group, couples, family; modality -- in-person, telehealth, phone; duration, recurring
patterns), clinical notes (SOAP, DAP, BIRP, narrative formats), treatment plans (goals,
objectives, interventions, target dates, review cycles).

Step 1.3 -- Integration Points

Map external systems: EHR/EMR integrations, insurance clearinghouses, telehealth platforms
(Zoom, Doxy.me, custom), e-prescribing (EPCS compliance), lab integrations, referral
networks, patient portals, secure messaging, payment processors.

============================================================
PHASE 2: SCHEDULING OPTIMIZATION
============================================================

Step 2.1 -- Appointment Architecture

Evaluate: appointment types and durations (intake 60-90min, follow-up 45-60min, crisis
variable, group 90-120min), recurring appointment support, buffer time between sessions
(travel, documentation, decompression), room assignment logic for in-person sessions,
telehealth session creation and link management, timezone handling for remote clients.

Step 2.2 -- Schedule Efficiency

Analyze: provider utilization rates (billable hours vs. available hours), gap detection
(unused slots between appointments), overbooking policies, cancellation and no-show
handling (automated waitlist backfill, late cancellation fees), same-day appointment
availability, after-hours and weekend scheduling support, group session capacity management.

Step 2.3 -- Client Self-Scheduling

Evaluate: online booking portal availability, appointment type restrictions (new vs.
returning clients), provider preference selection, insurance pre-verification at booking,
automated appointment reminders (SMS, email, push -- 24h, 48h, 1-week cadence),
cancellation/rescheduling self-service, intake form completion workflows triggered
by booking.

============================================================
PHASE 3: THERAPIST-CLIENT MATCHING
============================================================

Step 3.1 -- Matching Criteria

Evaluate whether the system supports matching on: therapeutic specialization (anxiety,
depression, PTSD, substance use, eating disorders, OCD, grief, relationship issues),
treatment modality (CBT, DBT, EMDR, psychodynamic, ACT, MI, play therapy),
population expertise (children, adolescents, adults, geriatric, LGBTQ+, veterans,
first responders), language capabilities, insurance acceptance, availability alignment
with client schedule, gender preference, cultural competency indicators, trauma-informed
care certification.

Step 3.2 -- Matching Algorithm Quality

Analyze: is matching rule-based or algorithmic? Are there weighted scoring factors?
Does the system account for provider caseload balance? Does it track match outcomes
(client retention after initial match, early termination rates, client-reported
therapeutic alliance)? Is there a re-matching workflow when fit is poor? Does it
consider provider burnout risk when assigning high-acuity clients?

Step 3.3 -- Waitlist Intelligence

Evaluate: waitlist data model (priority levels, presenting concerns, urgency indicators,
insurance type, preferred provider, date added), automated matching when slots open,
waitlist-to-appointment conversion tracking, average wait time metrics by presenting
concern and insurance type, waitlist communication (automated status updates,
alternative provider suggestions, crisis resource provision while waiting).

============================================================
PHASE 4: SESSION DOCUMENTATION EFFICIENCY
============================================================

Step 4.1 -- Note Templates and Workflows

Evaluate: supported note formats (SOAP, DAP, BIRP, narrative, custom), template
customization by session type and diagnosis, auto-population from previous notes
(carrying forward ongoing issues, medications, treatment plan goals), structured
data capture vs. free-text ratio, time-to-complete metrics, draft and finalization
workflows, co-signature support for supervisees.

Step 4.2 -- Documentation Automation

Check for: voice-to-text integration, AI-assisted note generation or summarization,
symptom checklist auto-scoring (PHQ-9, GAD-7, PCL-5, AUDIT, DAST), treatment plan
goal linking (connecting session notes to active treatment plan objectives),
auto-generated progress summaries for insurance reviews, batch signing capabilities.

Step 4.3 -- Compliance and Audit Trail

Verify: note completion deadlines and enforcement (24h, 48h, 72h policies), late note
alerts and reporting, amendment tracking with original content preservation, access
logging (who viewed which client record and when), client consent documentation
(informed consent, telehealth consent, release of information), retention and
destruction policies aligned with state regulations.

============================================================
PHASE 5: CRISIS DETECTION AND SAFETY
============================================================

Step 5.1 -- Risk Assessment Integration

Evaluate: standardized risk assessment tools (Columbia Suicide Severity Rating Scale,
PHQ-9 Item 9 flagging, safety plan templates), risk level classification (low,
moderate, high, imminent), automated alerts when risk indicators trigger (elevated
scores, keyword detection in notes), safety plan documentation and accessibility.

Step 5.2 -- Crisis Workflow

Check: crisis protocol activation (who gets notified, escalation chain), warm handoff
workflows to crisis services (988 Suicide and Crisis Lifeline, local crisis teams,
emergency services), after-hours crisis coverage routing, crisis session documentation
requirements, follow-up scheduling after crisis events (24h, 48h, 1-week check-ins),
supervisor notification for trainee-managed crises.

Step 5.3 -- Safety Plan Management

Evaluate: digital safety plan creation and storage, client access to their safety plan
(portal, mobile, printed), safety plan review reminders during sessions, integration
with emergency contacts, crisis resource directories (local hospitals, crisis lines,
peer support), safety plan versioning and update tracking.

============================================================
PHASE 6: INSURANCE AND BILLING WORKFLOWS
============================================================

Step 6.1 -- Insurance Verification

Evaluate: eligibility checking (real-time vs. batch), benefits verification (copay,
deductible, coinsurance, session limits, prior authorization requirements), out-of-network
benefits calculation, insurance panel management (which providers are in-network with
which payers), client financial responsibility estimation at time of booking.

Step 6.2 -- Claims Processing

Analyze: claim generation (CMS-1500, electronic 837P), CPT code selection assistance
(90834, 90837, 90847, 90853 for group, add-on codes for crisis), diagnosis code management
(ICD-10 selection, medical necessity documentation), claim submission workflow (clearinghouse
integration), ERA/EOB processing, denial management (denial reasons, resubmission workflows,
appeal letter generation), aging reports.

Step 6.3 -- Sliding Scale and Financial Access

Evaluate: sliding scale fee schedule management, income verification workflows, superbill
generation for out-of-network clients, statement generation, payment plan support,
pro bono tracking, grant-funded session tracking, financial hardship documentation.

============================================================
PHASE 7: OUTCOME TRACKING AND MEASUREMENT
============================================================

Step 7.1 -- Standardized Measures

Evaluate administration of: PHQ-9 (depression), GAD-7 (anxiety), PCL-5 (PTSD),
AUDIT-C (alcohol use), PHQ-A (adolescent depression), Columbia Suicide Severity Rating
Scale, OQ-45 (general functioning), DASS-21, WHO-5 Well-Being Index. Check: automated
scoring, score interpretation, trend visualization, clinically significant change
detection (Reliable Change Index), administration scheduling (intake, every N sessions,
discharge).

Step 7.2 -- Treatment Outcome Analytics

Analyze: individual client trajectory visualization (score-over-time graphs), cohort
analytics (outcomes by diagnosis, by provider, by treatment modality), benchmarking
against published norms, treatment response classification (improved, recovered, no
change, deteriorated), average sessions to clinically significant improvement,
discharge outcome documentation, provider effectiveness reporting (risk-adjusted
for client complexity).

Step 7.3 -- Measurement-Based Care Integration

Evaluate: whether outcome measures feed back into clinical decision-making (alerts when
client not progressing, treatment plan review triggers), whether clients can self-administer
measures between sessions (portal or app), whether aggregate outcome data supports
program evaluation and grant reporting, and whether data can be exported for research.

Write analysis to `docs/mental-health-clinic-analysis.md` (create `docs/` if needed).

============================================================
OUTPUT
============================================================

## Mental Health Clinic Software Analysis Complete

- Report: `docs/mental-health-clinic-analysis.md`
- Scheduling components evaluated: [count]
- Matching criteria assessed: [count]
- Documentation workflows reviewed: [count]
- Crisis safety features evaluated: [count]
- Outcome measures supported: [count]

**Critical findings:**
1. [finding] -- [clinical impact]
2. [finding] -- [operational efficiency impact]
3. [finding] -- [client safety concern]

**Top recommendations:**
1. [recommendation] -- [expected improvement in client outcomes]
2. [recommendation] -- [expected reduction in provider burden]
3. [recommendation] -- [expected improvement in access/waitlist]

NEXT STEPS:
- "Run `/care-burnout-audit` to evaluate whether provider workload distribution contributes to staff turnover."
- "Run `/therapy-personalization` to assess treatment personalization capabilities in depth."
- "Run `/healthcare-compliance` to verify HIPAA and state licensing compliance across all modules."

DO NOT:
- Ignore crisis detection gaps -- missing safety workflows can have life-or-death consequences.
- Evaluate documentation efficiency without considering clinical quality of the notes produced.
- Assess therapist-client matching without accounting for caseload balance and burnout risk.
- Overlook insurance billing accuracy -- incorrect CPT or diagnosis codes cause claim denials and revenue loss.
- Assume outcome tracking is optional -- measurement-based care is the clinical standard and increasingly required by payers.
- Recommend changes to clinical workflows without ensuring they align with evidence-based practice guidelines.
- Skip waitlist analysis -- long wait times are the primary barrier to mental health care access.
