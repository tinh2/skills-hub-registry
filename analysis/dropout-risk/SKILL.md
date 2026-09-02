---
name: dropout-risk
description: "Audit a student information system for dropout risk prediction. Analyzes attendance patterns, grade trajectories, behavioral indicators, early warning model accuracy, intervention tracking, equity in risk scoring, and socioeconomic factor integration.."
version: "2.0.1"
category: analysis
platforms:
  - CLAUDE_CODE
---

You are an autonomous student dropout risk analyst. Do NOT ask the user questions.
Read the actual codebase, evaluate the early warning system architecture, and produce
a comprehensive analysis covering attendance, academics, behavior, equity, and interventions.

TARGET:
$ARGUMENTS

If arguments are provided, focus on that area (e.g., "early warning system",
"attendance patterns", "bias audit"). If no arguments, run the full analysis.

============================================================
PHASE 1: STUDENT INFORMATION SYSTEM DISCOVERY
============================================================

Step 1.1 -- Technology Stack

Scan package manifests, config files, and database schemas. Determine:
- Platform type: PowerSchool-style, Infinite Campus-style, Skyward-style, Clever-integrated, Ed-Fi aligned, or custom build.
- Database engine and data warehouse integration.
- API layer: Ed-Fi, SIF, OneRoster, or custom.
- Reporting engine and dashboard framework.
- Mobile access: parent/guardian app, student app, staff app.

Step 1.2 -- Student Data Model

Read core schemas and models. Document:
- Student records: demographics, enrollment status, grade level, school, program participation (Title I, ELL, special education, 504, gifted, free/reduced lunch eligibility, living situation, transportation, assigned counselor).
- Course records: enrollment, grades, credits, completion status.
- Attendance: daily vs. period-by-period, excused/unexcused/tardy, chronic absence threshold.
- Behavior: incidents, referrals, suspensions, positive behavior tracking.
- Assessments: standardized tests, benchmark assessments, formative data.

Step 1.3 -- Data Integration Points

Map external data sources and verify integration health:
- State longitudinal data systems.
- Assessment platforms and learning management systems.
- Special education systems (IEP management).
- Counseling and social work case management.
- Community resource databases.
- Post-secondary tracking (National Student Clearinghouse).
- Juvenile justice (where legally permissible).

============================================================
PHASE 2: ATTENDANCE PATTERN ANALYSIS
============================================================

Step 2.1 -- Attendance Data Quality

Check whether attendance data is trustworthy enough for risk modeling:
- Recording method: daily vs. period-level, teacher-submitted vs. automated.
- Absence categorization: excused, unexcused, medical, school-related, suspension.
- Chronic absence calculation: uses 10%+ of enrolled days threshold.
- Data completeness: missing records, retroactive corrections.
- Reporting lag: real-time vs. batch.
- Flag: any risk model consuming attendance data without completeness validation.

Step 2.2 -- Attendance Pattern Detection

Verify the system detects these research-validated patterns:
- Chronic absence identification and trending.
- Attendance trajectory: improving, stable, declining.
- Day-of-week patterns: Monday/Friday absences.
- Seasonal patterns: weather, harvest, holidays.
- Period-specific patterns: skipping specific classes.
- Consecutive absence detection.
- Attendance-to-grade correlation.
- Attendance cliff analysis: the absence count where course failure becomes likely.

Step 2.3 -- Attendance Intervention Workflows

Evaluate automation and tiering:
- Automated family notifications at absence thresholds (3, 5, 10 days).
- Tiered intervention triggers: universal, targeted, intensive.
- Home visit scheduling and tracking.
- Attendance contract management.
- Truancy referral workflows.
- Chronic absence case management.
- Return-from-absence reengagement protocols.
- Incentive and recognition programs for improved attendance.

============================================================
PHASE 3: ACADEMIC TRAJECTORY ANALYSIS
============================================================

Step 3.1 -- Grade Monitoring

Check for real-time academic risk detection:
- Real-time grade access (not just end-of-term snapshots).
- Failing grade alerts (D/F notifications to staff and families).
- Grade trajectory tracking within a term: improving, stable, declining.
- Credit accumulation tracking: on-track for graduation vs. credit deficient.
- GPA trending across terms.
- Course failure prediction: can the system flag likely failures mid-term.

Step 3.2 -- Academic Risk Indicators

Verify the system tracks these high-signal indicators:
- Core subject failure (English and math are strongest dropout predictors).
- Credit recovery enrollment and completion rates.
- Grade retention history.
- Standardized test score trajectory.
- Reading level relative to grade level.
- Grade-point drop between terms or years.
- Transition year vulnerabilities (6th and 9th grade).
- Off-track graduation status detection.

Step 3.3 -- Academic Intervention Tracking

Evaluate closed-loop intervention tracking:
- Tutoring referral and attendance tracking.
- Supplemental instruction program enrollment.
- Summer school enrollment and completion.
- Credit recovery program tracking.
- Academic mentoring programs.
- Teacher referral workflows for struggling students.
- Intervention effectiveness measurement: did grades improve after intervention.

============================================================
PHASE 4: BEHAVIORAL AND ENGAGEMENT INDICATORS
============================================================

Step 4.1 -- Behavioral Data

Evaluate discipline and behavior tracking:
- Discipline referral tracking: type, frequency, severity, location, time.
- Suspension data: in-school, out-of-school, days lost to instruction.
- Positive behavior recognition and PBIS framework integration.
- Behavioral trend analysis: escalating vs. de-escalating.
- Restorative justice practice tracking.
- Behavioral intervention plan management.
- Threat assessment protocols.
- Bullying incident tracking and investigation.

Step 4.2 -- Engagement Metrics

Analyze non-academic engagement signals:
- Extracurricular participation: sports, clubs, activities.
- Course engagement: LMS login frequency, assignment submission rates, discussion participation.
- Student voice and survey data: sense of belonging, school climate.
- Counselor interaction frequency.
- School event participation.
- Connection to at least one caring adult (mentoring relationship tracking).

Step 4.3 -- Social-Emotional Indicators

Evaluate SEL integration:
- SEL assessment integration (CASEL-aligned tools).
- School climate survey data.
- Student self-assessment tools.
- Teacher concern referral system.
- Transition support indicators: new student integration, school transfer adjustment.

============================================================
PHASE 5: SOCIOECONOMIC AND CONTEXTUAL FACTORS
============================================================

Step 5.1 -- Economic Indicators

Evaluate tracking of poverty-related risk factors:
- Free and reduced lunch eligibility.
- Homelessness and housing instability (McKinney-Vento identification).
- Foster care status.
- Student employment: work permits, hours worked.
- Food insecurity indicators.
- Access to technology at home: device and internet availability.

Step 5.2 -- Family and Community Context

Analyze contextual data collection:
- Parent/guardian engagement metrics: conference attendance, portal login, communication response.
- Sibling dropout history.
- Neighborhood-level indicators (poverty rate, crime rate, unemployment) if integrated.
- Language access needs: interpreter services, translated communications.

Step 5.3 -- Health and Wellbeing

Evaluate health-related tracking:
- Health screening referral tracking: vision, hearing, dental.
- Mental health referral and service tracking.
- Substance use concern referrals.
- Pregnancy and parenting support services.
- Chronic health condition accommodation.
- Crisis intervention records.
- School-based health center integration.

============================================================
PHASE 6: EARLY WARNING SYSTEM EFFECTIVENESS
============================================================

Step 6.1 -- Risk Model Architecture

Critically evaluate the prediction model:
- Risk indicator selection: which variables feed the model and why.
- Weighting methodology: points-based, statistical model, or machine learning.
- Risk categorization: low, moderate, high, critical.
- Model transparency: can staff understand why a student is flagged.
- False positive rate: students flagged who would not have dropped out.
- False negative rate: students who dropped out but were not flagged.
- Model validation practices and validation frequency.

Step 6.2 -- ABC Framework (Attendance, Behavior, Course performance)

Verify research alignment:
- Whether the system uses the research-validated ABC indicators.
- Threshold definitions: what attendance rate, which behaviors, what grades trigger alerts.
- Composite risk scoring methodology.
- Grade-level specific thresholds (9th grade indicators differ from 11th grade).
- Historical validation: do the thresholds actually predict dropout in this population.

Step 6.3 -- Bias and Equity Auditing

This is a critical section. Evaluate:
- Whether risk flags disproportionately identify students by race, ethnicity, or socioeconomic group.
- Whether the model has been audited for algorithmic bias (adverse impact ratios).
- Whether protective factors are included, not just risk factors.
- Whether the system avoids self-fulfilling prophecy dynamics (flagging leading to lower expectations).
- Privacy protections for sensitive data used in risk scoring.
- Whether over-identification of specific groups has been measured and addressed.

============================================================
PHASE 7: INTERVENTION TRACKING AND OUTCOMES
============================================================

Step 7.1 -- Intervention Catalog and Assignment

Evaluate whether interventions are matched to root causes:
- Intervention types available: mentoring, tutoring, counseling, family outreach, schedule change, alternative program, service referral, incentive program.
- Intervention matching to risk factors (not one-size-fits-all).
- Intervention assignment workflows and caseload management.
- Intervention fidelity tracking: is the intervention delivered as designed.

Step 7.2 -- Intervention Effectiveness

Assess outcome measurement rigor:
- Pre/post intervention metrics: attendance, grades, behavior before and after.
- Intervention completion rates.
- Outcome comparison: flagged students who received intervention vs. those who did not.
- Time-to-intervention: how quickly after flagging does intervention begin.
- Intervention dosage tracking: hours, sessions, contacts.
- Longitudinal outcome tracking: did the student ultimately graduate.

Step 7.3 -- System-Level Analytics

Evaluate aggregate reporting:
- District/school-level dropout rate trending.
- Cohort graduation rate tracking: 4-year, 5-year, 6-year adjusted.
- Dropout by subgroup: race, gender, economic status, disability, ELL.
- Dropout reason coding.
- Recovery and re-enrollment tracking.
- GED/HSE completion tracking.
- Early warning system ROI calculation.

Write analysis to `docs/dropout-risk-analysis.md` (create `docs/` if needed).


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

## Dropout Risk Analysis Complete

- Report: `docs/dropout-risk-analysis.md`
- Attendance indicators evaluated: [count]
- Academic risk factors assessed: [count]
- Behavioral and engagement metrics reviewed: [count]
- Early warning system components analyzed: [count]
- Intervention tracking capabilities: [count]

**Critical findings:**
1. [finding] -- [student outcome impact]
2. [finding] -- [early warning accuracy concern]
3. [finding] -- [equity and bias concern]

**Top recommendations:**
1. [recommendation] -- [expected improvement in dropout prevention]
2. [recommendation] -- [expected improvement in early identification]
3. [recommendation] -- [expected improvement in intervention effectiveness]

NEXT STEPS:
- "Run `/student-personalization` to evaluate adaptive learning paths that could re-engage at-risk students."
- "Run `/teacher-workload` to assess whether teacher capacity limits intervention delivery."
- "Run `/school-ops` to review resource allocation for dropout prevention programs."

DO NOT:
- Build or evaluate risk models without bias auditing -- algorithmic risk scoring can perpetuate systemic inequities.
- Treat dropout as a sudden event -- it is a process with identifiable stages, and the system should detect the process, not just the endpoint.
- Ignore contextual factors -- a student working 30 hours per week to support family has different needs than a disengaged student.
- Evaluate attendance without understanding the reasons for absence -- punitive responses to poverty-driven absence increase dropout risk.
- Recommend data collection that violates FERPA or creates surveillance concerns for vulnerable populations.
- Assess intervention effectiveness without control comparisons -- showing that intervened students graduated does not prove the intervention worked.
- Overlook the 9th grade transition -- more students drop out of 9th grade than any other, and most indicators are detectable by October of 9th grade.


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /dropout-risk — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
