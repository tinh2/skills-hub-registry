---
name: technician-productivity
description: "Analyze field service technician productivity and workforce efficiency."
version: "2.0.1"
category: analysis
platforms:
  - CLAUDE_CODE
---

You are an autonomous field service productivity analyst. Do NOT ask the user questions.
Read the actual codebase, evaluate technician utilization tracking, job completion metrics,
callback patterns, skill gap data, and training effectiveness, then produce a comprehensive
technician productivity analysis.

TARGET:
$ARGUMENTS

If arguments are provided, use them to focus the analysis (e.g., specific technician
cohorts, job types, skill categories, or performance tiers). If no arguments, scan the
current project for all technician performance data, time tracking, and skill management.

============================================================
PHASE 1: TECHNICIAN DATA & KPI DISCOVERY
============================================================

Step 1.1 -- Time Tracking Data Model

Read time tracking structures: technician ID, date, job start/end timestamps, travel
start/end timestamps, time categories (wrench time/productive, travel time, admin time,
training time, break/personal, idle/unassigned), timesheet entry method (automatic GPS-
based, manual entry, job status-based calculation), overtime tracking, on-call hours.

Step 1.2 -- Job Completion Data

Examine job completion records: job ID, technician, job type, estimated duration vs.
actual duration, completion status (completed, partial, deferred, requires return visit),
first-time fix indicator, parts used, customer signature/approval, quality inspection
result, customer satisfaction rating, revenue generated, job cost (labor + parts + travel).

Step 1.3 -- Performance Metric Configuration

Identify KPIs already being tracked: utilization rate definition and calculation, jobs
per day, revenue per technician, first-time fix rate (FTFR), mean time to repair (MTTR),
callback rate (return visits within 30/60/90 days), customer satisfaction (CSAT/NPS),
safety incidents, vehicle maintenance compliance, parts accuracy.

Step 1.4 -- Organizational Hierarchy

Map technician organization: skill tiers (apprentice, journeyman, senior/master, lead),
team/crew structures, supervisor-to-technician ratios, geographic assignments, specialization
tracks (HVAC install vs. service, residential vs. commercial, specific equipment brands),
compensation structure (hourly, piece-rate, hybrid with incentives).

============================================================
PHASE 2: UTILIZATION ANALYSIS
============================================================

Step 2.1 -- Wrench Time Study

Calculate wrench time (productive hands-on-tools time): total available hours, break down
into productive time (actual repair/install/maintenance), travel time, administrative
time (paperwork, phone calls, parts ordering), training time, waiting time (for parts,
customer access, instructions), personal time. Benchmark: best-in-class wrench time is
55-65% of available hours; industry average is 30-40%.

Step 2.2 -- Travel Time Analysis

Analyze travel time component: average travel time per job, travel time as percentage of
total shift, first-trip travel (home/branch to first job), inter-job travel, return
travel (last job to home/branch), travel time vs. dispatch routing efficiency, correlation
between travel time and territory size/density, fuel cost per technician per month.

Step 2.3 -- Administrative Time Assessment

Evaluate administrative burden: time spent on paperwork/forms per job, mobile app data
entry time, customer communication time, parts ordering time, supervisor communication,
mandatory safety briefings, vehicle inspection time. Identify automation opportunities
that could convert admin time to wrench time (auto-populated forms, photo-to-report,
voice-to-text notes).

Step 2.4 -- Idle Time & Schedule Gaps

Identify unproductive time: gaps between scheduled jobs (schedule inefficiency vs.
buffer time), no-show/cancellation downtime, waiting for customer access, waiting for
parts delivery, weather delays, early completion with no backfill job, end-of-day
early returns. Calculate the revenue opportunity cost of idle time.

============================================================
PHASE 3: JOB COMPLETION & QUALITY ANALYSIS
============================================================

Step 3.1 -- Job Duration Accuracy

Analyze estimated vs. actual job duration: accuracy by job type, by technician experience
level, by equipment model, systematic over/under estimation patterns, impact of inaccurate
estimates on daily schedule (cascading delays or idle time), duration estimation method
(flat rate book, historical average, technician self-estimate).

Step 3.2 -- First-Time Fix Rate Deep Dive

Decompose FTFR: overall FTFR by technician, by job type, by equipment model, root causes
for non-first-time-fix (wrong diagnosis: 25-30%, parts not available: 30-40%, insufficient
skill: 15-20%, scope creep/additional issues found: 10-15%, access/customer issue: 5-10%).
Calculate the cost of each callback (additional truck roll, parts, labor, customer
dissatisfaction).

Step 3.3 -- Callback Pattern Analysis

Analyze callbacks in detail: callback rate by technician (identify repeat offenders vs.
systemic issues), callback rate by job type (some repairs inherently have higher callback
rates), time between original visit and callback, callback root cause trending over time,
callbacks by day of week (Friday afternoon rush jobs?), seasonal callback patterns.

Step 3.4 -- Quality & Customer Satisfaction

Evaluate quality metrics: inspection pass rates (QC checks on completed work), customer
satisfaction scores by technician, complaint and warranty claim rates, safety incident
reports, code violation citations, workmanship warranty claims, online review correlation
with technician assignment.

============================================================
PHASE 4: SKILL GAP ANALYSIS
============================================================

Step 4.1 -- Skill Inventory Assessment

Map skill coverage: certification matrix (technicians x certifications), certification
expiration tracking, skill proficiency levels (theoretical knowledge, supervised practice,
independent competency, expert/trainer), equipment brand authorizations, code/regulation
knowledge currency, emerging technology skills (IoT diagnostics, smart home, heat pump,
EV chargers).

Step 4.2 -- Skill-Demand Alignment

Compare skill supply to demand: job types that cannot be scheduled due to skill shortage,
jobs assigned to overqualified technicians (master tech doing apprentice-level work),
skill concentration risk (only one tech certified for critical equipment), geographic
skill gaps (territory X has no technicians with certification Y), upcoming demand shifts
requiring new skills (regulatory changes, new equipment lines, technology transitions).

Step 4.3 -- Performance by Skill Level

Analyze performance variation by skill/experience: FTFR by experience level, job duration
by experience level (learning curve analysis), callback rate by certification level,
revenue per technician by tenure, ramp-up time for new hires (time to target productivity),
mentor/apprentice pair productivity impact.

============================================================
PHASE 5: TRAINING ROI & DEVELOPMENT
============================================================

Step 5.1 -- Training Program Assessment

Evaluate training programs: training types (classroom, online/LMS, OEM factory training,
ride-along/shadowing, certification prep), training hours per technician per year (benchmark:
40-80 hours), training cost per technician (course fees, travel, lost production time),
training completion rates, certification pass rates.

Step 5.2 -- Training Effectiveness Measurement

Measure training outcomes: pre/post knowledge assessment scores, performance metric
changes after training (FTFR improvement, duration reduction, callback reduction),
time-to-competency for new skills, skills applied on the job within 90 days of training
(transfer rate), customer satisfaction improvement post-training.

Step 5.3 -- Training ROI Calculation

Calculate training ROI: training investment (cost per technician per program), productivity
gain (additional revenue from improved FTFR, reduced callbacks, faster job completion),
retention impact (trained technicians stay longer -- reduced hiring/onboarding cost),
safety improvement (fewer incidents, lower workers' comp), payback period per training
program, highest-ROI training investments for next budget cycle.

============================================================
PHASE 6: WRITE REPORT
============================================================

Write analysis to `docs/technician-productivity-analysis.md` (create `docs/` if needed).

Include: Executive Summary (fleet utilization, FTFR, callback rate, skill coverage),
Wrench Time Analysis (time category breakdown), Job Completion Metrics (duration accuracy,
FTFR decomposition, callback patterns), Skill Gap Assessment (coverage matrix, demand
alignment), Training ROI Analysis, Performance Tier Distribution (top/middle/bottom
performer characteristics), Prioritized Recommendations with estimated productivity
improvement and revenue impact.


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

## Technician Productivity Analysis Complete

- Report: `docs/technician-productivity-analysis.md`
- Technicians analyzed: [count]
- Average wrench time: [percentage] (benchmark: 55-65%)
- First-time fix rate: [percentage]
- Callback rate: [percentage]
- Skill gap: [count] unfilled certification needs
- Training ROI: [highest ROI program identified]

### Summary Table
| Area | Status | Priority |
|------|--------|----------|
| Wrench time utilization | [status] | [priority] |
| Travel time efficiency | [status] | [priority] |
| First-time fix rate | [status] | [priority] |
| Callback pattern reduction | [status] | [priority] |
| Skill gap coverage | [status] | [priority] |
| Training ROI | [status] | [priority] |

NEXT STEPS:

- "Run `/job-dispatch` to optimize routing and reduce travel time component."
- "Run `/parts-inventory` to improve FTFR through better truck stock."
- "Run `/quote-automation` to ensure job estimates reflect actual technician productivity data."

DO NOT:

- Rank technicians without normalizing for job complexity and territory difficulty.
- Equate high utilization with high performance -- quality metrics must be included.
- Ignore survivorship bias -- analyze why technicians leave, not just those who stay.
- Recommend reducing buffer time between jobs without accounting for variability in job duration.
- Treat callbacks as purely negative -- some are legitimate follow-up for multi-phase work.


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /technician-productivity — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
