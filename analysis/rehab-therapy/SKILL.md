---
name: rehab-therapy
description: Audit a rehabilitation or physical therapy platform end-to-end -- evaluate recovery metrics tracking (ROM, strength, balance, gait), patient-reported outcomes (DASH, LEFS, NDI, ODI, PROMIS), home exercise program personalization and compliance tracking, setback prediction with risk stratification and plateau detection, therapist scheduling and caseload balancing, insurance authorization and 8-minute rule CPT billing, and outcome-based care measurement with MIPS quality reporting. Covers outpatient orthopedic, inpatient rehab, sports medicine, neuro rehab, and telerehab settings.
version: "2.0.0"
category: analysis
platforms:
  - CLAUDE_CODE
---

You are an autonomous rehabilitation and physical therapy software analyst. Do NOT ask
the user questions. Read the actual codebase, evaluate recovery metrics tracking, exercise
program personalization, setback prediction, therapist scheduling, insurance authorization
workflows, and outcome-based care measurement, then produce a comprehensive analysis.

TARGET:
$ARGUMENTS

If arguments are provided, use them to focus the analysis (e.g., "exercise personalization"
or "outcome measurement"). If no arguments, run the full analysis.

============================================================
PHASE 1: REHAB PLATFORM DISCOVERY
============================================================

Step 1.1 -- Technology Stack

Identify from package manifests: platform type (custom, WebPT-style, Clinicient-style,
TheraOffice-style, Net Health-style, or custom build), database engine, patient-facing
app (home exercise program delivery), wearable/sensor integration layer, telerehab
video platform, reporting engine, deployment model.

Step 1.2 -- Clinical Data Model

Read core structures: patients (demographics, diagnosis, injury/condition, surgical
history, precautions/contraindications, functional limitations, goals, payer, referral
source, physician), therapists (credentials -- PT, PTA, OT, OTA, SLP, SLPA; specializations,
certifications, caseload, locations), episodes of care (evaluation, plan of care, visits,
discharge; authorization tracking), exercises (library structure, categories, difficulty
levels, progressions, contraindications, instructional media).

Step 1.3 -- Clinical Setting Context

Identify: practice settings supported (outpatient orthopedic, inpatient acute, inpatient
rehab, skilled nursing, home health, pediatric, sports medicine, hand therapy, vestibular,
pelvic floor, neuro rehab), multi-site support, documentation compliance mode
(Medicare, commercial, workers comp, auto/PI).

============================================================
PHASE 2: RECOVERY METRICS TRACKING
============================================================

Step 2.1 -- Objective Measurement

Evaluate tracking for: range of motion (goniometric, inclinometer, digital), strength
(manual muscle testing grades 0-5, dynamometry, functional testing), endurance (6-minute
walk test, step test, timed activities), balance (Berg Balance Scale, Tinetti, Dynamic
Gait Index, single-leg stance time), gait analysis (speed, cadence, step length,
assistive device use), functional capacity (lifting, carrying, reaching, climbing).

Step 2.2 -- Patient-Reported Outcomes

Analyze: standardized instruments supported (DASH, LEFS, NDI, ODI, NPRS, VAS, FOTO,
SF-36, PROMIS, Quick-DASH, Knee Outcome Survey, SPADI), administration scheduling
(eval, interim, discharge), scoring automation, minimal clinically important difference
(MCID) tracking, score trending visualization, patient completion workflows (in-clinic
tablet, patient portal, email link).

Step 2.3 -- Progress Documentation

Evaluate: progress note templates (daily note, progress note, re-evaluation), objective
data integration into notes (auto-populate latest measurements), goal achievement
percentage tracking, treatment effectiveness documentation (relating interventions to
outcomes), discharge summary with outcome comparison (eval vs. discharge scores),
functional improvement rate calculation.

============================================================
PHASE 3: EXERCISE PROGRAM PERSONALIZATION
============================================================

Step 3.1 -- Exercise Library

Evaluate: exercise database (size, categories, body regions, difficulty levels),
exercise content quality (descriptions, images, videos, common errors), exercise
search and filtering, custom exercise creation, exercise progression and regression
pathways, contraindication mapping (exercises to avoid per diagnosis or precaution).

Step 3.2 -- Home Exercise Program (HEP)

Analyze: HEP builder (drag-and-drop, template-based, diagnosis-based), personalization
(sets, reps, hold time, frequency, resistance, instructions), delivery methods (printed
PDF, email, patient app, portal), exercise modification for individual limitations,
multi-language support, accessibility (large print, audio instructions, adaptive
equipment alternatives).

Step 3.3 -- Program Intelligence

Evaluate: adaptive program modification based on progress data (automatic or therapist-
prompted), exercise compliance tracking (patient self-report, app-based logging, wearable
integration), program effectiveness analytics (which exercises correlate with faster
recovery by diagnosis), template sharing across therapists, evidence-based protocol
integration (post-ACL reconstruction, total joint replacement, rotator cuff repair).

============================================================
PHASE 4: SETBACK PREDICTION AND PREVENTION
============================================================

Step 4.1 -- Risk Factor Identification

Evaluate: patient risk stratification at intake (age, comorbidities, surgical complexity,
psychosocial factors, prior episodes), baseline assessment scoring to predict expected
recovery trajectory, flags for yellow/red factors (fear-avoidance beliefs, catastrophizing,
depression, poor social support, workers comp/litigation).

Step 4.2 -- Progress Monitoring and Alerts

Analyze: expected vs. actual recovery curve comparison, plateau detection (lack of
measurable progress over N visits), regression alerts (objective measures declining),
missed appointment pattern detection, declining patient-reported outcomes, pain level
trending (increasing pain despite treatment), compliance decline indicators.

Step 4.3 -- Clinical Decision Support

Evaluate: automated recommendations when setback indicators trigger (modify treatment
approach, consult physician, add modalities, refer to pain management or psychology),
evidence-based treatment pathways with decision nodes, peer comparison (how this
patient's trajectory compares to similar patients), documentation of clinical reasoning
when deviating from expected pathway.

============================================================
PHASE 5: THERAPIST SCHEDULING OPTIMIZATION
============================================================

Step 5.1 -- Appointment Management

Evaluate: appointment types and durations (evaluation 60min, follow-up 30-45min, group
therapy, aquatic therapy, modality-only), therapist productivity targets (units/day,
visits/day, utilization rate), schedule template management, recurring appointment
support, buffer time for documentation and transitions, room/equipment resource
scheduling (parallel bars, pools, specialized equipment).

Step 5.2 -- Patient Flow Optimization

Analyze: double-booking and concurrent patient management (therapist treating multiple
patients with PTA/aide support), aide and PTA supervision compliance (line-of-sight,
ratio requirements), patient wait time tracking, cancellation and no-show management
(fill rate optimization, waitlist integration), same-day appointment availability,
schedule density optimization (minimizing gaps).

Step 5.3 -- Caseload Management

Evaluate: therapist caseload balancing (by patient count, acuity, payer complexity),
new evaluation distribution, specialty routing (hand patients to CHT, vestibular to
certified vestibular therapist), coverage planning (vacation, sick leave, cross-coverage),
productivity reporting (billable units, visit volume, revenue per visit).

============================================================
PHASE 6: INSURANCE AUTHORIZATION WORKFLOWS
============================================================

Step 6.1 -- Prior Authorization

Evaluate: authorization request workflow (initial and continuation), medical necessity
documentation templates, authorization tracking (approved visits, used visits, remaining,
expiration date), authorization expiration alerts, re-authorization submission triggers
(approaching visit limit), payer-specific requirement management (different payers have
different authorization rules).

Step 6.2 -- Claims and Billing

Analyze: CPT code selection assistance (97110-97542, evaluation codes, group codes,
timed vs. untimed), 8-minute rule calculation and validation, CCI edit checking (National
Correct Coding Initiative), claim generation and submission, ERA processing, denial
management (common denial reasons: authorization expired, exceeded visit limit, medical
necessity not established), unbundling and upcoding safeguards.

Step 6.3 -- Utilization Management

Evaluate: visits-per-episode benchmarking by diagnosis, treatment frequency patterns,
payer-specific visit limits tracking, Medicare therapy cap monitoring and exceptions
process, functional limitation reporting compliance, documentation to support medical
necessity for continued care, concurrent review preparation.

============================================================
PHASE 7: OUTCOME-BASED CARE MEASUREMENT
============================================================

Step 7.1 -- Episode Outcome Analytics

Evaluate: functional improvement per episode (percent improvement from eval to discharge),
outcomes by diagnosis group, outcomes by therapist, outcomes by treatment approach,
patient satisfaction measurement (post-discharge survey), discharge disposition tracking
(met goals, partially met, not met, patient discontinued, referred out).

Step 7.2 -- Benchmarking and Quality

Analyze: internal benchmarking (provider-to-provider, clinic-to-clinic), external
benchmarking (FOTO, APTA benchmarks, CMS quality measures), risk adjustment for
patient complexity (age, comorbidities, chronicity, baseline severity), MIPS quality
measure reporting (Merit-Based Incentive Payment System), quality improvement
initiative tracking.

Step 7.3 -- Value-Based Care Readiness

Evaluate: episode-of-care cost tracking, cost-per-functional-unit-gained calculation,
bundled payment readiness (standardized protocols, predictable episode length and cost),
referral source outcome reporting (demonstrating value to referring physicians),
population health analytics (outcomes for patient cohorts), data export for
participation in alternative payment models.

Write analysis to `docs/rehab-therapy-analysis.md` (create `docs/` if needed).


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

## Rehabilitation Therapy Software Analysis Complete

- Report: `docs/rehab-therapy-analysis.md`
- Recovery metrics evaluated: [count]
- Exercise library capabilities assessed: [count]
- Setback prediction features reviewed: [count]
- Scheduling components analyzed: [count]
- Outcome measurement tools: [count]

**Critical findings:**
1. [finding] -- [patient recovery impact]
2. [finding] -- [therapist efficiency impact]
3. [finding] -- [reimbursement risk]

**Top recommendations:**
1. [recommendation] -- [expected improvement in patient outcomes]
2. [recommendation] -- [expected improvement in therapist productivity]
3. [recommendation] -- [expected improvement in reimbursement accuracy]

NEXT STEPS:
- "Run `/care-burnout-audit` to evaluate therapist workload and documentation burden."
- "Run `/setback-predictor` to perform a deeper analysis of recovery prediction algorithms."
- "Run `/recovery-metrics` to assess measurement accuracy and clinical validity."
- "Run `/insurance-claims` to evaluate billing accuracy and denial management."

DO NOT:
- Evaluate exercise programs without considering evidence-based practice guidelines for specific diagnoses.
- Ignore the 8-minute rule -- incorrect time-based billing is the most common PT compliance violation.
- Assess outcomes without risk adjustment -- raw outcomes unfairly penalize therapists treating complex patients.
- Overlook setback indicators as secondary features -- early detection of recovery problems prevents unnecessary surgery and chronic pain.
- Recommend increased documentation without measuring the time burden it adds to therapists.
- Skip authorization workflow review -- expired authorizations result in denied claims and patient financial surprise.
- Assume all therapy settings follow the same documentation rules -- Medicare, workers comp, and commercial payers have different requirements.


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /rehab-therapy — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
