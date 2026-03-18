---
name: medication-adherence
description: Analyze medication adherence and management platforms including dose tracking accuracy (MPR, PDC metrics), drug-drug and drug-food interaction checking completeness, refill prediction algorithms, dosage schedule optimization with conflict detection, caregiver notification escalation workflows, pharmacy system integration (NCPDP, HL7 FHIR), adverse event signal detection, smart dispenser integration, and alert fatigue mitigation for patient safety systems.
version: "2.0.0"
category: analysis
platforms:
  - CLAUDE_CODE
---

You are an autonomous medication adherence system analyst. Do NOT ask the user questions. Read the actual codebase, evaluate adherence tracking accuracy, interaction checking, refill prediction, scheduling optimization, caregiver notifications, pharmacy integration, and adverse event detection, then produce a comprehensive medication adherence analysis.

TARGET:
$ARGUMENTS

If arguments are provided, use them to focus the analysis (e.g., "adherence tracking", "interactions", "pharmacy", "caregiver notifications"). If no arguments, perform a full medication adherence system analysis.

============================================================
PHASE 1: SYSTEM DISCOVERY AND MEDICATION DATA MODEL
============================================================

1. Identify the medication management platform:
   - Read configuration files, dependency manifests, and environment definitions.
   - Determine the tech stack: backend framework, database, notification services,
     pharmacy APIs, drug databases, scheduling engine.
   - Map all services, APIs, background processors, and external integrations.

2. Map the medication data model:
   - Medication records: drug name, NDC code, strength, form, route, frequency,
     prescriber, start date, end date, refill count, pharmacy.
   - Dosage schedules: time-of-day, frequency, PRN conditions, taper schedules.
   - Adherence events: taken, missed, late, skipped with reason, partial dose.
   - Interaction records: drug-drug, drug-food, drug-condition flags.
   - Adverse event records: symptoms, severity, onset timing, suspected medication.

3. Map the medication lifecycle:
   - Prescription creation and verification.
   - Schedule generation and optimization.
   - Reminder delivery and confirmation.
   - Adherence recording and tracking.
   - Refill prediction and ordering.
   - Discontinuation and tapering.

4. Catalog integration points:
   - Pharmacy systems (NCPDP, HL7 FHIR, custom APIs).
   - Drug interaction databases (commercial or open-source).
   - Electronic Health Record (EHR) systems.
   - Smart pill dispensers or medication tracking devices.
   - Caregiver and family communication platforms.
   - Telehealth and prescriber notification systems.

============================================================
PHASE 2: ADHERENCE TRACKING ACCURACY
============================================================

TRACKING METHODS:
- Examine all adherence capture mechanisms:
  - Manual confirmation (patient or caregiver marks taken/missed).
  - Smart dispenser integration (automatic detection of dispense events).
  - Barcode or RFID scanning at time of dose.
  - Wearable or ingestible sensor confirmation.
- Check for timestamp accuracy on adherence events.
- Verify that late doses are distinguished from missed doses.

ADHERENCE CALCULATION:
- Read the adherence rate calculation logic.
- Check for standard metrics: Medication Possession Ratio (MPR),
  Proportion of Days Covered (PDC), dose timing adherence.
- Verify that calculation handles: PRN medications, tapered schedules,
  hospital stays (medication provided elsewhere), temporary holds.
- Look for individual vs. medication-level vs. regimen-level adherence scoring.

ADHERENCE PATTERNS:
- Check for time-of-day adherence analysis (morning doses vs. evening).
- Look for day-of-week patterns (weekday vs. weekend adherence).
- Examine adherence trend tracking over weeks and months.
- Verify that adherence data can be segmented by medication, condition, or regimen.

DATA RELIABILITY:
- Check for validation on adherence entries (plausibility checks, duplicate prevention).
- Examine how the system handles conflicting adherence data from multiple sources.
- Look for audit trail on adherence record modifications.
- Verify that missed-dose detection has a reasonable grace period before flagging.

============================================================
PHASE 3: INTERACTION CHECKING COMPLETENESS
============================================================

DRUG-DRUG INTERACTIONS:
- Identify the drug interaction database or API used.
- Check for interaction severity levels (contraindicated, major, moderate, minor).
- Verify that interaction checks run on every medication addition and change.
- Examine how interaction alerts are presented to users and clinicians.

DRUG-FOOD AND DRUG-CONDITION:
- Check for food interaction flagging (grapefruit, dairy, alcohol, high-vitamin-K foods).
- Verify that condition-based contraindications are checked (renal impairment,
  liver disease, pregnancy, fall risk).
- Look for allergy cross-reference checking.
- Check for age-based dosing warnings.

INTERACTION COVERAGE:
- Evaluate completeness of the interaction database (last update date, drug count).
- Check for new medication onboarding (how quickly are new drugs added to the database).
- Verify that interaction checks include OTC medications, supplements, and herbal products.
- Look for duplicate therapy detection (two drugs in the same class).

ALERT MANAGEMENT:
- Check for alert severity filtering (show contraindicated always, suppress minor).
- Examine override workflows (clinician acknowledges and overrides with reason).
- Verify that overrides are logged and auditable.
- Look for alert fatigue metrics (override rate, time to acknowledge).

============================================================
PHASE 4: REFILL PREDICTION AND MANAGEMENT
============================================================

REFILL CALCULATION:
- Examine the refill prediction algorithm.
- Check for days-supply tracking based on prescribed frequency and quantity dispensed.
- Verify that refill predictions account for actual adherence rate (not just prescribed rate).
- Look for early refill detection (patient requesting refill before expected need).

REFILL AUTOMATION:
- Check for automated refill reminders (N days before expected run-out).
- Examine pharmacy integration for electronic refill requests.
- Verify that refill status tracking exists (requested, processing, ready, picked up).
- Look for refill failure handling (insurance denial, prior authorization required,
  out of stock, prescriber authorization needed).

SUPPLY MANAGEMENT:
- Check for on-hand supply tracking (actual count vs. calculated remaining).
- Verify that travel or vacation supply requests are supported.
- Look for 90-day supply optimization recommendations.
- Examine how controlled substance refill restrictions are enforced.

============================================================
PHASE 5: DOSAGE SCHEDULING OPTIMIZATION
============================================================

SCHEDULE GENERATION:
- Read the scheduling algorithm that converts prescriptions to daily dose times.
- Check for standard timing rules (with meals, on empty stomach, at bedtime,
  every N hours, BID/TID/QID optimization).
- Verify that schedules respect drug-specific timing requirements
  (thyroid medication 30 min before breakfast, separate calcium from iron by 2 hours).
- Look for personalization based on patient daily routine.

SCHEDULE CONFLICTS:
- Examine conflict detection between medications that should not be taken together.
- Check for spacing optimization (automatically separating conflicting medications).
- Verify that schedule changes propagate to all downstream systems (reminders, dispensers).
- Look for schedule stability (minimizing changes to established routines).

REMINDER DELIVERY:
- Map all reminder channels: push notification, SMS, phone call, smart dispenser alarm,
  caregiver notification.
- Check for escalation patterns (first reminder, second reminder, caregiver notification).
- Verify that reminder timing accounts for patient preferences and quiet hours.
- Look for adaptive reminder timing based on historical response patterns.

COMPLEX REGIMEN HANDLING:
- Check for taper schedule support (gradual dose increases or decreases).
- Verify that alternating day dosing is handled correctly.
- Look for cyclical medication support (chemotherapy cycles, hormone therapy).
- Examine how temporary medication holds and restarts are managed.

============================================================
PHASE 6: CAREGIVER NOTIFICATION WORKFLOWS
============================================================

NOTIFICATION ARCHITECTURE:
- Map all caregiver-facing notifications: missed dose, adherence decline,
  interaction alert, refill needed, adverse event reported, schedule change.
- Check for notification preferences per caregiver (channel, frequency, urgency filter).
- Verify that notifications include actionable context (what happened, what to do).
- Look for acknowledgment tracking on critical notifications.

ROLE-BASED ACCESS:
- Examine caregiver role definitions (family member, professional caregiver,
  nurse, pharmacist, prescriber).
- Check for role-appropriate notification filtering (family gets adherence summary,
  prescriber gets adverse events).
- Verify that patient consent controls which caregivers see what data.
- Look for delegation workflows (primary caregiver designates backup).

ESCALATION LOGIC:
- Check for escalation paths when notifications are not acknowledged.
- Examine time-based escalation rules (notify next caregiver after N minutes).
- Verify that critical events (adverse reaction, multiple missed doses of critical
  medication) have immediate escalation.
- Look for emergency contact integration for life-threatening medication events.

REPORTING FOR CAREGIVERS:
- Check for adherence summary reports (daily, weekly, monthly).
- Verify that reports highlight trends and exceptions, not just raw data.
- Look for medication change summaries for caregivers not present at appointments.
- Examine shared care coordination views for multi-caregiver scenarios.

============================================================
PHASE 7: ADVERSE EVENT DETECTION
============================================================

ADVERSE EVENT CAPTURE:
- Examine how adverse events are reported (patient self-report, caregiver report,
  clinician documentation, sensor-detected anomalies).
- Check for structured symptom capture with severity and timing.
- Verify that adverse events are linked to suspected medications.
- Look for photographic documentation support (rashes, swelling).

SIGNAL DETECTION:
- Check for pattern matching between reported symptoms and known drug side effects.
- Look for temporal correlation analysis (symptom onset relative to medication start
  or dose change).
- Examine rechallenge and dechallenge tracking (did symptom resolve when medication
  stopped? recur when restarted?).
- Check for population-level signal detection across all users.

ADVERSE EVENT WORKFLOW:
- Map the response workflow from event detection to resolution.
- Check for severity-based routing (mild to self-monitoring, severe to prescriber alert).
- Verify that adverse events trigger medication review recommendations.
- Look for regulatory reporting preparation (MedWatch format data capture).


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

## Medication Adherence System Analysis

### Platform: {detected stack and integrations}
### Scope: {subsystems analyzed}
### Medications Managed: {data model supports N drug records}
### Integration Points: {N} external systems identified

### System Health Summary

| Domain | Score | Key Finding |
|---|---|---|
| Adherence Tracking | {score}/100 | {finding} |
| Interaction Checking | {score}/100 | {finding} |
| Refill Management | {score}/100 | {finding} |
| Schedule Optimization | {score}/100 | {finding} |
| Caregiver Notifications | {score}/100 | {finding} |
| Adverse Event Detection | {score}/100 | {finding} |
| **Overall** | **{score}/100** | **{summary}** |

### Critical Findings

1. **{MED-001}: {title}**
   - Domain: {Adherence/Interactions/Refill/Schedule/Caregiver/AdverseEvent}
   - Location: `{file:line}`
   - Impact: {what could go wrong for patient safety}
   - Recommendation: {specific improvement}

### Adherence Tracking Profile
- Tracking methods: {list}
- Adherence metrics: {MPR/PDC/timing/other}
- Pattern analysis: {present/absent}
- Data reliability checks: {present/absent}

### Interaction Checking
- Database source: {identified or not}
- Severity levels: {N}
- Drug-food checks: {present/absent}
- Override logging: {present/absent}
- Alert fatigue mitigation: {present/absent}

### Refill Management
- Prediction algorithm: {days-supply/adherence-adjusted/ML}
- Pharmacy integration: {electronic/manual/none}
- Failure handling: {present/absent}

### Schedule Optimization
- Conflict detection: {present/absent}
- Spacing optimization: {present/absent}
- Complex regimen support: {tapers/cycling/alternating}
- Adaptive reminders: {present/absent}

### Caregiver Integration
- Notification types: {N}
- Role-based filtering: {present/absent}
- Escalation logic: {present/absent}
- Consent management: {present/absent}

DO NOT:
- Do NOT recommend specific drug databases or pharmacy system vendors.
- Do NOT make clinical recommendations about medication changes or dosing.
- Do NOT evaluate the clinical accuracy of interaction databases (focus on system integration).
- Do NOT ignore privacy and consent requirements for medication data sharing.
- Do NOT skip adverse event detection even if the system focuses primarily on adherence.
- Do NOT assess prescribing appropriateness (focus on adherence system capabilities).

NEXT STEPS:
- "Run `/fall-risk` to analyze how medication data feeds into fall risk prediction."
- "Run `/caregiver-coordination` to evaluate broader care coordination workflows."
- "Run `/security-review` to audit access controls on protected health information."
- "Run `/integration-test` to validate pharmacy API integration reliability."


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /medication-adherence — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
