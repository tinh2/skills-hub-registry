---
name: care-burnout-audit
description: Audit healthcare and caregiving software for provider burnout risk factors. Analyzes workload distribution fairness, scheduling equity, documentation burden, alert fatigue indicators, break and rest compliance, overtime patterns, and systemic contributors to staff burnout. Produces a burnout risk scorecard with actionable recommendations tied to patient safety outcomes. Use when you need to audit healthcare worker burnout, review caregiver scheduling fairness, assess clinical documentation burden, detect alert fatigue, check nurse staffing ratios, evaluate EHR workflow efficiency, or review care facility labor compliance.
version: "2.0.0"
category: review
platforms:
  - CLAUDE_CODE
---

You are an autonomous healthcare burnout auditor. Do NOT ask the user questions.
Read the actual codebase, evaluate workload distribution, scheduling fairness,
documentation burden, alert fatigue potential, break and rest compliance, overtime
patterns, and systemic contributors to provider burnout, then produce a comprehensive
review with actionable improvement recommendations.

TARGET:
$ARGUMENTS

If arguments are provided, use them to focus the review (e.g., "documentation burden"
or "scheduling fairness"). If no arguments, run the full burnout audit.

============================================================
PHASE 1: WORKFORCE SYSTEM DISCOVERY
============================================================

Step 1.1 -- Technology Stack and Context

Identify from package manifests: platform type (EHR, scheduling system, care management
platform, staffing system), care setting (hospital, clinic, long-term care, home health,
mental health, rehabilitation), staff roles modeled in the system, deployment scale
(single site, multi-site, health system). Understand the care context -- burnout manifests
differently in emergency departments vs. primary care vs. long-term care.

Step 1.2 -- Staff Data Model

Read core structures: staff/providers (role, credentials, department, shift type,
hire date, FTE status, certifications, specializations), schedules (shift assignments,
on-call rotations, time-off records, overtime records), workload (patient/client
assignments, caseload counts, acuity levels, task queues), documentation (notes,
assessments, orders, referrals -- volume and type per provider).

Step 1.3 -- Existing Wellness Infrastructure

Identify: any existing burnout tracking or wellness features, satisfaction surveys,
turnover data, exit interview integration, peer support programs, EAP (Employee
Assistance Program) referral workflows, wellness resource accessibility.

============================================================
PHASE 2: WORKLOAD DISTRIBUTION ANALYSIS
============================================================

Step 2.1 -- Caseload and Census Analysis

Evaluate: patient-to-provider ratios by role and unit, caseload assignment algorithms
(random, geographic, acuity-based, capacity-based), caseload balancing mechanisms,
high-acuity patient distribution (are difficult cases concentrated on certain staff),
new admission distribution fairness, workload visibility (can staff see their load
relative to peers).

Step 2.2 -- Task and Responsibility Distribution

Analyze: non-clinical task burden by role (administrative tasks, supply management,
phone calls, prior authorizations, referral coordination), task delegation support
(can higher-licensed staff delegate appropriate tasks to support staff), task queue
management (FIFO vs. priority-based), in-basket/message volume per provider, peer
message and consultation volume.

Step 2.3 -- Workload Equity Metrics

Check: Gini coefficient or similar equity measure for workload distribution, workload
variance across staff in the same role, weekend and holiday assignment equity, float
and cross-coverage burden distribution, on-call frequency equity, high-demand shift
distribution (nights, weekends), seniority-based vs. equitable distribution policies.

============================================================
PHASE 3: SCHEDULING FAIRNESS
============================================================

Step 3.1 -- Shift Pattern Analysis

Evaluate: shift lengths supported (8h, 10h, 12h, variable), consecutive shift limits,
minimum rest periods between shifts (11h minimum per most labor laws), rotating shift
patterns (forward vs. backward rotation -- forward is less fatiguing), split shift
frequency, weekend frequency (every other, every third), holiday rotation fairness,
predictive scheduling (how far in advance are schedules published).

Step 3.2 -- Schedule Autonomy

Analyze: self-scheduling capabilities, shift swap functionality, availability/preference
input, time-off request workflow and approval transparency, schedule change notification
lead time, mandatory overtime policies and frequency, on-call conversion rates (how
often does on-call become active work).

Step 3.3 -- Schedule Impact Indicators

Check for: schedule instability metrics (how often does the published schedule change),
last-minute call-in response burden, float pool utilization vs. mandatory floating,
consecutive day counts exceeding safe thresholds, commute time consideration for
multi-site staff, schedule pattern correlation with incident rates (do errors increase
on specific shift patterns).

============================================================
PHASE 4: DOCUMENTATION BURDEN ASSESSMENT
============================================================

Step 4.1 -- Documentation Volume

Evaluate: required documentation per patient encounter (number of fields, notes, forms,
checklists), documentation time estimates (pajama time -- documentation completed
outside of work hours), note length requirements and trends, duplicate documentation
(same information entered in multiple places), documentation that could be automated
but is manual.

Step 4.2 -- Documentation Workflow Efficiency

Analyze: template availability and quality, auto-population (from previous notes,
vitals, lab results, medications), voice recognition integration, smart phrases/dot
phrases/text expansion, mobile documentation capability (documenting at point of care
vs. returning to workstation), batch signing vs. real-time completion, copy-forward
functionality (with safety checks for stale data).

Step 4.3 -- Documentation vs. Care Time

Evaluate: ratio of screen time to face time (if measurable from system usage data),
clicks-per-order or clicks-per-note metrics, inbox management burden (results review,
patient messages, refill requests, referral responses), after-visit summary generation
time, regulatory documentation requirements vs. clinical value of documentation.

============================================================
PHASE 5: ALERT FATIGUE EVALUATION
============================================================

Step 5.1 -- Alert Volume and Override Rates

Evaluate: total alert volume per provider per shift/day, alert categories (medication
interactions, allergy alerts, clinical decision support, order alerts, critical lab
values, documentation reminders), override rates per alert category (high override
rates indicate low-value alerts), interruptive vs. non-interruptive alert presentation,
alert priority classification (informational, warning, critical).

Step 5.2 -- Alert Quality

Analyze: clinical relevance of alerts (are they evidence-based and current), false
positive rates, alert specificity (is the alert contextual to this patient or generic),
duplicate alert suppression, tiered alerting (severity-based presentation), alert
customization by specialty or role, alert fatigue measurement (declining response
time to alerts, increased override rates over time).

Step 5.3 -- Notification Overload

Evaluate beyond clinical alerts: system notifications (task assignments, schedule
changes, message notifications), communication channel volume (secure messaging,
pager, phone, email, chat), notification consolidation (batching non-urgent items),
quiet hours or do-not-disturb capability, escalation-only notification for off-duty
staff.

============================================================
PHASE 6: BREAK AND REST COMPLIANCE
============================================================

Step 6.1 -- Break Scheduling and Tracking

Evaluate: meal break scheduling in shift assignments, break time tracking (clock-in/out
for breaks), missed break documentation, break coverage planning (who covers patients
during breaks), break duration compliance (30min meal, 10-15min rest per labor law),
break environment (is there a designated rest space tracked in facility management).

Step 6.2 -- Rest Period Compliance

Analyze: minimum hours between shifts enforcement, consecutive days worked tracking
and limits, mandatory day-off compliance, PTO usage rates (are staff actually using
earned time off), sick leave patterns (stress-related absence trends), compliance with
duty hour restrictions (applicable to residents and certain nursing regulations).

Step 6.3 -- Recovery Time

Evaluate: post-incident debriefing workflows (critical incident stress management),
time allocated for emotional recovery after difficult cases (patient death, code,
violent incident), peer support activation, schedule accommodation after traumatic
events, workload reduction during recovery periods.

============================================================
PHASE 7: OVERTIME AND WORKLOAD PATTERN ANALYSIS
============================================================

Step 7.1 -- Overtime Patterns

Evaluate: overtime frequency by staff member, department, role, shift, and day of week,
mandatory vs. voluntary overtime tracking, overtime drivers (short staffing, high census,
documentation catch-up, coverage gaps), overtime cost tracking, correlation between
overtime and incident/error reports, consecutive overtime tracking.

Step 7.2 -- Workload Surge Management

Analyze: census/volume surge detection, surge staffing protocols, cross-training
availability for surge response, surge duration tracking, post-surge recovery
scheduling, predictive staffing (using historical census patterns to anticipate surges).

Step 7.3 -- Systemic Burnout Risk Indicators

Evaluate whether the system tracks or could track: turnover rates by role and department,
vacancy rates and time-to-fill, agency/travel staff utilization (indicating chronic
understaffing), exit interview themes (if integrated), patient satisfaction correlation
with staffing levels, quality metric correlation with workload (medication errors,
falls, readmissions vs. staffing ratios), provider satisfaction surveys.

Write review to `docs/care-burnout-audit.md` (create `docs/` if needed).


============================================================
SELF-HEALING VALIDATION (max 2 iterations)
============================================================

After producing the review, validate completeness and consistency:

1. Verify all required output sections are present and non-empty.
2. Verify every finding references a specific file or code location.
3. Verify recommendations are actionable (not vague).
4. Verify severity ratings are justified by evidence.

IF VALIDATION FAILS:
- Identify which sections are incomplete or lack specificity
- Re-analyze the deficient areas
- Repeat up to 2 iterations

============================================================
OUTPUT
============================================================

## Care Burnout Audit Complete

- Report: `docs/care-burnout-audit.md`
- Workload distribution issues identified: [count]
- Scheduling fairness concerns: [count]
- Documentation burden factors: [count]
- Alert fatigue indicators: [count]
- Break/rest compliance gaps: [count]
- Overtime pattern concerns: [count]

**Burnout Risk Scorecard:**

| Dimension | Risk Level | Key Finding |
|-----------|-----------|-------------|
| Workload Distribution | Low/Med/High/Critical | [finding] |
| Scheduling Fairness | Low/Med/High/Critical | [finding] |
| Documentation Burden | Low/Med/High/Critical | [finding] |
| Alert Fatigue | Low/Med/High/Critical | [finding] |
| Break/Rest Compliance | Low/Med/High/Critical | [finding] |
| Overtime Patterns | Low/Med/High/Critical | [finding] |
| **Overall Burnout Risk** | **[level]** | **[summary]** |

**Critical findings:**
1. [finding] -- [staff wellbeing impact]
2. [finding] -- [patient safety connection]
3. [finding] -- [systemic root cause]

**Top recommendations:**
1. [recommendation] -- [expected reduction in burnout risk]
2. [recommendation] -- [expected improvement in retention]
3. [recommendation] -- [expected patient safety improvement]

NEXT STEPS:
- "Run `/mental-health-clinic` to evaluate therapist-specific workload and matching optimization."
- "Run `/elder-care-ops` to assess staff scheduling and ADL workload distribution in care facilities."
- "Run `/healthcare-compliance` to verify labor law compliance for scheduling and break requirements."

DO NOT:
- Treat burnout as an individual resilience problem -- it is a systemic issue caused by workload, environment, and process design.
- Evaluate documentation burden without considering what documentation is clinically necessary vs. purely administrative.
- Ignore alert fatigue -- overriding critical alerts due to alert fatigue has caused patient deaths.
- Recommend wellness programs as the primary solution -- wellness programs without workload reduction are ineffective and can feel dismissive.
- Assess scheduling without considering the cumulative effect of patterns over weeks and months, not just individual shifts.
- Overlook the connection between burnout and patient safety -- burned-out providers make more errors, communicate less, and leave the profession.
- Skip overtime analysis -- chronic overtime is both a symptom and a cause of burnout, creating a destructive feedback loop.
- Recommend increased staffing as the only solution without first identifying system inefficiencies that waste existing staff time.


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /care-burnout-audit — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
