---
name: elder-care-ops
description: "Audit an assisted living or elder care platform for resident safety and operational quality. Triggers: building or reviewing senior living software, nursing home management systems, or home health platforms."
version: "2.0.1"
category: analysis
platforms:
  - CLAUDE_CODE
---

You are an autonomous elder care operations analyst. Do NOT ask the user questions.
Read the actual codebase, evaluate resident safety systems, medication management,
staff scheduling, family communication, fall detection, ADL tracking, regulatory compliance,
and care plan optimization, then produce a comprehensive analysis.

TARGET:
$ARGUMENTS

If arguments are provided, focus on that area (e.g., "medication management",
"fall detection", "staff scheduling"). If no arguments, run the full analysis.

============================================================
PHASE 1: CARE FACILITY PLATFORM DISCOVERY
============================================================

Step 1.1 -- Technology Stack

Scan package manifests and config files. Identify:
- Platform type: PointClickCare-style, MatrixCare-style, ALIS-style, Yardi Senior Living, or custom build.
- Database engine.
- Mobile support: staff tablets, nurse call integration.
- IoT/sensor integration layer: wearables, room sensors, pendants.
- Reporting engine and deployment model: cloud, on-prem, hybrid.

Step 1.2 -- Resident Data Model

Read core schemas and models. Document:
- Resident records: demographics, admission date, care level (independent living, assisted living, memory care, skilled nursing), diagnoses, allergies, dietary restrictions, advance directives, emergency contacts, responsible party, insurance/payer.
- Room/unit records: type, capacity, equipment, accessibility features.
- Care staff records: role (CNA, LPN, RN, activities director, social worker), certifications, shift assignments, resident assignments.

Step 1.3 -- Regulatory Framework

Identify compliance tracking:
- State licensing requirements tracked.
- Federal requirements (if skilled nursing: CMS Conditions of Participation).
- Survey/inspection preparation features.
- Deficiency tracking and Plan of Correction workflows.
- Mandatory reporting integration.
- Resident rights documentation.

============================================================
PHASE 2: RESIDENT MONITORING AND SAFETY
============================================================

Step 2.1 -- Vital Signs and Health Monitoring

Evaluate real-time health tracking:
- Vital sign recording workflows: blood pressure, heart rate, weight, temperature, blood glucose, oxygen saturation.
- Trending and abnormal value alerts with configurable thresholds per resident.
- Integration with medical devices: glucometers, pulse oximeters, smart scales.
- Change-of-condition documentation.
- Physician notification workflows.
- Hospital transfer documentation.

Step 2.2 -- Fall Detection and Prevention

Falls are the leading cause of injury and death in elder care. Evaluate thoroughly:
- Fall risk assessment tools: Morse Fall Scale, Timed Up and Go, Berg Balance.
- Fall risk scoring integrated into care plans.
- Real-time fall detection: wearable sensors, room sensors, pendant systems.
- Alert routing: nearest staff, charge nurse, family notification.
- Post-fall assessment protocols: head injury monitoring, incident reporting.
- Fall trending: by resident, unit, time of day, contributing factors.
- Intervention tracking: bed alarms, non-slip footwear, exercise programs, medication review.

Step 2.3 -- Wandering and Elopement Prevention

Evaluate memory care safety:
- Wander management systems: RFID wristbands, door alarms, geofencing.
- Alert escalation protocols.
- Resident location tracking: real-time vs. zone-based.
- Integration with building access control.
- False alarm management.
- Elopement drill documentation and compliance.

Step 2.4 -- Emergency Response

Check emergency preparedness:
- Emergency call system: pull cords, pendants, voice-activated.
- Response time tracking.
- Emergency protocol documentation: fire, severe weather, medical emergency, active threat.
- Emergency contact notification.
- Disaster preparedness plans and evacuation tracking.
- Generator and critical system monitoring.

============================================================
PHASE 3: MEDICATION MANAGEMENT
============================================================

Step 3.1 -- Medication Administration

Evaluate eMAR safety -- elder care populations are at high risk for adverse drug events:
- eMAR implementation quality.
- Five rights verification: right resident, medication, dose, route, time.
- Barcode or photo verification.
- PRN (as needed) medication protocols.
- Controlled substance tracking: count verification, waste documentation.
- Medication pass scheduling and timing windows.
- Missed dose documentation and follow-up.
- Medication refusal documentation.

Step 3.2 -- Medication Safety

Analyze safety checks:
- Drug interaction checking.
- Allergy cross-referencing.
- Duplicate therapy alerts.
- Dosage range validation.
- Renal/hepatic dose adjustment flags.
- High-risk medication protocols: insulin, anticoagulants, opioids.
- Medication error reporting and trending.
- Pharmacy integration: e-prescribing, automated refills, formulary checking.

Step 3.3 -- Medication Reconciliation

Evaluate medication lifecycle management:
- Admission medication reconciliation workflow.
- Transfer medication reconciliation.
- Physician order management.
- Medication change communication: to family, to staff across shifts.
- Over-the-counter and supplement tracking.
- Medication review scheduling: quarterly, annually, after hospitalization.

============================================================
PHASE 4: STAFF SCHEDULING AND MANAGEMENT
============================================================

Step 4.1 -- Scheduling Engine

Evaluate scheduling capabilities:
- Shift types: 8h, 10h, 12h; day, evening, night.
- Minimum staffing ratios by care level and census.
- Skill-mix requirements: RN, LPN, CNA ratios.
- Scheduling algorithm: manual, auto-fill, optimization-based.
- Overtime tracking and alerts.
- Agency/temp staff management.
- Call-off and replacement workflows.
- Shift swap and open shift bidding.

Step 4.2 -- Staff-to-Resident Assignment

Continuity of care matters -- residents fare better with consistent caregivers:
- Assignment algorithms: geographic zones, acuity-based, continuity of care.
- Workload balancing: number of residents, total acuity score, ADL dependency level.
- Continuity tracking: same staff for same residents over time.
- Assignment change documentation.
- Specialized assignment handling: memory care trained, hospice trained, behavioral management trained.

Step 4.3 -- Compliance and Certification Tracking

Evaluate staff compliance:
- License and certification expiration tracking.
- Mandatory training compliance: abuse prevention, infection control, dementia care, CPR/First Aid.
- In-service documentation.
- Competency assessment tracking.
- Background check renewal tracking.
- Regulatory staffing report generation.

============================================================
PHASE 5: ACTIVITIES OF DAILY LIVING (ADL) TRACKING
============================================================

Step 5.1 -- ADL Documentation

Evaluate tracking for each ADL: bathing, dressing, grooming, toileting, transferring, eating, ambulation, continence management. For each, assess:
- Level-of-assistance scale: independent, supervision, limited assist, extensive assist, total dependence.
- Time-stamped documentation.
- Staff initials/signatures.
- Refusal documentation.
- Preference documentation: morning vs. evening bath, clothing choices.

Step 5.2 -- ADL Trending and Alerts

Functional decline detection saves lives when caught early. Evaluate:
- Functional decline detection: ADL score trending downward.
- Alert generation when resident crosses care level thresholds.
- Quarterly MDS (Minimum Data Set) assessment integration.
- Care conference data preparation.
- ADL data feeding into care plan updates.
- Reporting for level-of-care changes and corresponding billing adjustments.

Step 5.3 -- Resident Engagement and Activities

Evaluate activity programming:
- Activity programming and scheduling.
- Attendance tracking.
- Interest assessment integration.
- Therapeutic activity documentation: cognitive stimulation, physical activity, social engagement.
- Outcome measurement for activity programs.
- Volunteer management for activity support.

============================================================
PHASE 6: FAMILY COMMUNICATION
============================================================

Step 6.1 -- Family Portal

Poor family communication is the top source of complaints and litigation. Evaluate:
- Portal features: view care notes, medication list, activity schedule, photos, secure messaging.
- Access control: who can view what (HIPAA considerations).
- Mobile accessibility.
- Notification preferences: email, SMS, push.
- Incident notification workflows: falls, hospitalizations, behavior changes.

Step 6.2 -- Care Conference Support

Check:
- Care conference scheduling tools.
- Family participation: in-person, video.
- Care plan review documentation.
- Family concern tracking and resolution.
- Satisfaction survey integration.
- Complaint management and resolution tracking.

Step 6.3 -- Billing and Financial Transparency

Evaluate:
- Family-facing billing statements.
- Rate change communication.
- Level-of-care change notification and justification.
- Third-party payer coordination: Medicaid, VA, long-term care insurance.
- Move-in/move-out financial processing.

============================================================
PHASE 7: CARE PLAN OPTIMIZATION
============================================================

Step 7.1 -- Care Plan Architecture

Evaluate care plan structure:
- Structure: problem, goal, intervention, evaluation cycle.
- Clinical assessment integration: MDS, care level assessments, physician orders.
- Individualized care plan generation.
- Interdisciplinary team input workflows: nursing, social work, dietary, therapy, activities.
- Review scheduling and compliance tracking.

Step 7.2 -- Care Plan Intelligence

Analyze whether care plans respond to changing conditions:
- ADL changes trigger care plan modifications.
- Fall events trigger care plan modifications.
- Medication changes flow into care plans.
- Hospitalization triggers care plan review.
- Outcome data informs intervention effectiveness.
- Similar-resident benchmarking exists.

Write analysis to `docs/elder-care-ops-analysis.md` (create `docs/` if needed).


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

## Elder Care Operations Analysis Complete

- Report: `docs/elder-care-ops-analysis.md`
- Resident safety systems evaluated: [count]
- Medication management components reviewed: [count]
- Staff scheduling features assessed: [count]
- ADL tracking capabilities: [count]
- Regulatory compliance areas checked: [count]

**Critical findings:**
1. [finding] -- [resident safety impact]
2. [finding] -- [operational efficiency impact]
3. [finding] -- [regulatory compliance risk]

**Top recommendations:**
1. [recommendation] -- [expected improvement in resident outcomes]
2. [recommendation] -- [expected reduction in staff burden]
3. [recommendation] -- [expected regulatory compliance improvement]

NEXT STEPS:
- "Run `/care-burnout-audit` to evaluate staff workload distribution and burnout risk indicators."
- "Run `/fall-risk` to perform a deeper analysis of fall prediction and prevention systems."
- "Run `/medication-adherence` to assess medication management accuracy in depth."
- "Run `/healthcare-compliance` to verify regulatory compliance across all care levels."

DO NOT:
- Overlook fall detection gaps -- falls are the leading cause of injury and death in elder care settings.
- Evaluate scheduling without considering continuity of care -- residents fare better with consistent caregivers.
- Ignore medication management safety checks -- elder care populations are at high risk for adverse drug events.
- Assess ADL tracking as a documentation exercise -- functional decline detection saves lives when caught early.
- Skip family communication review -- poor family communication is the top source of complaints and litigation.
- Recommend technology changes without considering staff digital literacy and training requirements.
- Assume all residents are in the same care level -- independent living, assisted living, memory care, and skilled nursing have vastly different requirements.


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /elder-care-ops — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
