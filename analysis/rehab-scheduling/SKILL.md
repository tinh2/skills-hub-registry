---
name: rehab-scheduling
description: Audit a rehabilitation scheduling system -- evaluate therapist productivity and utilization rates, PTA/COTA supervision compliance, patient flow and no-show management, equipment and treatment room allocation, insurance authorization tracking with expiration alerts, CMS therapy cap monitoring (KX modifier thresholds), payer-specific visit limits, session frequency optimization, and multi-discipline coordination for PT, OT, and SLP. Covers WebPT, Clinicient, TheraOffice, Net Health, and custom EMR scheduling engines.
version: "2.0.0"
category: analysis
platforms:
  - CLAUDE_CODE
---

You are an autonomous rehabilitation scheduling optimization analyst. Do NOT ask the user
questions. Read the actual codebase, evaluate therapist utilization, patient flow, equipment
management, authorization tracking, and session scheduling, then produce a comprehensive
rehab scheduling analysis.

TARGET:
$ARGUMENTS

If arguments are provided, use them to focus the analysis (e.g., specific therapy disciplines,
payer types, or scheduling constraints). If no arguments, run the full analysis.

============================================================
PHASE 1: SCHEDULING SYSTEM DISCOVERY
============================================================

Step 1.1 -- Platform Architecture

Read system configuration and data structures. Identify: scheduling platform (WebPT,
Clinicient/HENO, TheraOffice, Net Health/Optima, Raintree, RehabOptima, custom EMR),
practice management system, billing integration, patient portal, telehealth platform,
reporting and analytics module.

Step 1.2 -- Scheduling Data Model

Map data structures: appointments (patient, therapist, service type, time slot, duration,
status, location, equipment needed), therapist records (credentials, specializations,
availability, productivity targets, caseload limits, supervision requirements), patient
records (diagnosis, treatment plan, frequency/duration prescription, payer, authorization
status, session count remaining), facility resources (treatment rooms, gym equipment,
modality devices, pool/aquatic).

Step 1.3 -- Therapy Discipline Coverage

Identify disciplines managed: Physical Therapy (PT), Occupational Therapy (OT), Speech-
Language Pathology (SLP), each with distinct scheduling needs. Map: discipline-specific
treatment durations (PT eval 45-60 min, follow-up 30-45 min), group therapy scheduling
(OT groups, PT classes), concurrent and co-treatment rules (CMS definitions of concurrent,
group, co-treatment), student/aide supervision ratios and scheduling constraints.

Step 1.4 -- Integration Points

Map connections to: EMR/clinical documentation, billing and claims, payer portals
(authorization verification, eligibility checking), outcome measurement systems, patient
communication (reminders, confirmations, waitlist), referral management, reporting
platforms, workforce management.

============================================================
PHASE 2: THERAPIST UTILIZATION
============================================================

Step 2.1 -- Productivity Metrics

Evaluate: productive time calculation (billable treatment time / total scheduled hours),
productivity benchmarks by discipline (industry: PT 85-90%, OT 80-85%, SLP 75-85%),
units per day tracking (CPT units billed per therapist per day), patient visits per day,
documentation time allocation (is documentation time eating into productive time),
non-patient time categorization (meetings, training, mentoring, admin).

Step 2.2 -- Caseload Management

Check for: caseload balancing across therapists (equitable distribution by volume, complexity,
payer mix), caseload limits by therapist level (new grad vs. experienced), specialty matching
(orthopedic patients to ortho-specialized PT, neuro patients to neuro-specialized), patient
acuity weighting (complex patients count more toward caseload), cross-training and float
therapist deployment.

Step 2.3 -- Schedule Template Optimization

Assess: therapist schedule templates (fixed vs. flexible time blocks), evaluation slot
reservation (protecting time for new patient evaluations), treatment block optimization
(grouping similar treatments, minimizing room/equipment transitions), meeting and admin
time protection, lunch and break compliance, overtime tracking and management.

Step 2.4 -- PTA/COTA Supervision Scheduling

Evaluate: Physical Therapist Assistant (PTA) and Certified Occupational Therapy Assistant
(COTA) supervision requirements (state-specific ratios), supervising therapist availability
alignment, CMS supervision rules for Medicare patients (direct supervision for certain
services), co-signature and review scheduling, student clinical education scheduling.

============================================================
PHASE 3: PATIENT FLOW MANAGEMENT
============================================================

Step 3.1 -- Appointment Scheduling

Evaluate: scheduling rules engine (appointment duration by service type, provider, payer),
new patient vs. follow-up slot management, schedule density optimization (minimizing gaps
while avoiding overbooking), walk-in and same-day appointment handling, patient preference
management (preferred therapist, time, location), recurring appointment scheduling
(2x/week for 6 weeks patterns).

Step 3.2 -- Waitlist Management

Check for: waitlist functionality (patients waiting for specific therapists, time slots,
or appointment types), cancellation backfill workflow (automatic waitlist notification
when slot opens), priority waitlist management (urgent patients, expiring authorizations),
waitlist-to-appointment conversion tracking, waitlist aging and follow-up.

Step 3.3 -- No-Show & Cancellation Management

Assess: no-show rate tracking by patient, therapist, time slot, and day of week, cancellation
pattern analysis, late cancellation policies and enforcement, overbooking strategies based
on historical no-show rates, patient re-engagement workflow (outreach after no-shows),
financial impact of no-shows (lost revenue calculation).

Step 3.4 -- Patient Throughput

Evaluate: patient cycle time (check-in to check-out), treatment room turnaround time, peak
hour management, patient arrival pattern analysis, wait time tracking and reduction, multi-
therapist visit coordination (patient seeing PT and OT on same day), check-in and check-out
workflow efficiency.

============================================================
PHASE 4: EQUIPMENT ALLOCATION
============================================================

Step 4.1 -- Equipment Scheduling

Evaluate: equipment reservation system (modalities, gym equipment, pools, specialized devices),
equipment-to-appointment linkage (ensuring required equipment is available when scheduled),
equipment utilization tracking (% of available time in use), equipment sharing across
therapists and treatment areas, peak demand management for popular equipment.

Step 4.2 -- Treatment Space Management

Check for: treatment room assignment logic (room capabilities matched to treatment needs),
open gym vs. private room scheduling, room utilization tracking, room preparation time
between patients, accessibility requirements (wheelchair accessible rooms, bariatric
equipment), telehealth room/equipment allocation.

Step 4.3 -- Equipment Maintenance Impact

Assess: equipment maintenance scheduling integrated with patient scheduling, equipment
downtime impact on appointment availability, backup equipment and contingency plans,
equipment replacement planning based on utilization data, capital equipment request
justification from utilization data.

============================================================
PHASE 5: INSURANCE AUTHORIZATION TRACKING
============================================================

Step 5.1 -- Authorization Management

Evaluate: authorization tracking (approved visits, used visits, remaining visits, expiration
date), authorization request workflow (initial request, extension request, peer-to-peer
review), payer-specific rules engine (different authorization requirements by payer),
authorization-to-appointment linkage (prevent scheduling beyond authorized visits),
authorization expiration alerts.

Step 5.2 -- CMS Therapy Cap Management

Check for: Medicare therapy cap tracking (KX modifier threshold -- currently $2,330 for
PT/SLP combined, $2,330 for OT separately for 2024), medical review threshold tracking,
ABN (Advance Beneficiary Notice) generation when approaching caps, Medicare Part B vs.
Part A coverage rules, MIPS quality measure tracking related to therapy utilization.

Step 5.3 -- Payer-Specific Scheduling Rules

Assess: visit frequency limits by payer (e.g., 3x/week maximum), concurrent therapy
restrictions, telehealth vs. in-person payer requirements, group therapy billing rules
(CMS: therapist can treat up to 4 patients simultaneously in group), evaluation and
re-evaluation frequency limits, pre-certification requirements.

Step 5.4 -- Denial Prevention

Evaluate: proactive denial prevention (scheduling within authorized limits, medical necessity
documentation prompts), real-time eligibility verification before scheduling, prior
authorization status check before appointment, automated alerts for missing authorizations,
denial pattern analysis and root cause correction.

============================================================
PHASE 6: SESSION SPACING & TREATMENT PLANNING
============================================================

Step 6.1 -- Session Frequency Optimization

Evaluate: prescribed frequency adherence tracking (ordered 3x/week, actually seen 2.1x/week),
session spacing rules (minimum days between sessions, optimal recovery time), frequency
tapering management (reducing from 3x to 2x to 1x as patient improves), discharge planning
timeline integration, treatment plan duration management.

Step 6.2 -- Multi-Discipline Coordination

Check for: coordinated scheduling across disciplines (PT + OT + SLP on same day when
possible), shared treatment goals and session coordination, team conference scheduling,
co-treatment scheduling (two disciplines treating simultaneously -- CMS billing rules),
discharge coordination across disciplines.

Step 6.3 -- Outcome-Driven Scheduling

Assess: outcome measure integration (functional improvement driving frequency decisions),
progress-based schedule adjustment (patients not improving may need frequency change),
discharge readiness indicators influencing remaining schedule, treatment effectiveness
comparison across scheduling patterns (3x/week vs. 2x/week outcomes by diagnosis).

============================================================
PHASE 7: WRITE REPORT
============================================================

Write analysis to `docs/rehab-scheduling-analysis.md` (create `docs/` if needed).

Include: Executive Summary, Therapist Utilization Assessment, Patient Flow Analysis,
Equipment Allocation Review, Authorization Tracking Effectiveness, Session Spacing
Optimization, Revenue Impact Analysis, Recommendations with utilization and patient
access improvement targets.


============================================================
SELF-HEALING VALIDATION (max 2 iterations)
============================================================

After producing output, validate data quality and completeness:

1. Verify all output sections have substantive content (not just headers).
2. Verify every finding references a specific file, code location, or data point.
3. Verify recommendations are actionable and evidence-based.
4. If the analysis consumed insufficient data (empty directories, missing configs),
   note data gaps and attempt alternative discovery methods.

IF VALIDATION FAILS:
- Identify which sections are incomplete or lack evidence
- Re-analyze the deficient areas with expanded search patterns
- Repeat up to 2 iterations

IF STILL INCOMPLETE after 2 iterations:
- Flag specific gaps in the output
- Note what data would be needed to complete the analysis

============================================================
OUTPUT
============================================================

## Rehab Scheduling Analysis Complete

- Report: `docs/rehab-scheduling-analysis.md`
- Therapist productivity rate: [percentage]
- No-show rate: [percentage]
- Authorization denial rate: [percentage]
- Average visits per episode: [count]

### Summary Table
| Area | Status | Priority |
|------|--------|----------|
| Therapist Utilization | [status] | [priority] |
| Patient Flow | [status] | [priority] |
| Equipment Allocation | [status] | [priority] |
| Authorization Tracking | [status] | [priority] |
| Session Spacing | [status] | [priority] |
| Revenue Optimization | [status] | [priority] |

NEXT STEPS:

- "Run `/therapy-outcomes` to correlate scheduling patterns with patient outcomes."
- "Run `/hr-ops` to assess therapist workforce planning and retention."
- "Run `/compliance-ops` to evaluate CMS and payer compliance controls."

DO NOT:

- Modify any patient schedules, authorization records, or therapist assignments.
- Recommend productivity targets that compromise treatment quality or patient safety.
- Ignore PTA/COTA supervision requirements -- they carry significant compliance risk.
- Assume all payers have the same authorization rules -- always verify payer-specific logic.
- Skip no-show analysis -- it is the single largest driver of utilization gaps in outpatient rehab.


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /rehab-scheduling — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
