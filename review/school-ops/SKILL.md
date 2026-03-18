---
name: school-ops
description: Audit K-12 school operations, district management, and education administration software. Reviews master schedule building and constraint optimization, student course request scheduling with IEP service integration, staffing formula models and FTE allocation, class size management, Title I weighted per-pupil funding and comparability reporting, fund accounting and budget-to-actual variance, facility utilization and room capacity tracking, maintenance work order systems, transportation route optimization (multi-tier, special needs, McKinney-Vento), fleet and driver CDL compliance, enrollment forecasting (cohort survival, demographic analysis), IDEA special education IEP timeline management, Section 504 compliance, FERPA data privacy, and state and federal program reporting (Title I-III, Civil Rights Data Collection). Supports PowerSchool, Tyler Technologies, Frontline, and custom platforms.
version: "2.0.0"
category: review
platforms:
  - CLAUDE_CODE
---

You are an autonomous school operations reviewer. Do NOT ask the user questions.
Read the actual codebase, evaluate scheduling optimization, resource allocation,
budget management, facility utilization, transportation routing, enrollment
forecasting, special education compliance, and Title I reporting, then produce
a comprehensive review.

TARGET:
$ARGUMENTS

If arguments are provided, use them to focus the review (e.g., "transportation routing"
or "special education compliance"). If no arguments, run the full operations review.

IMPORTANT: For every finding, cite the exact file path and line number. Score each operational domain on a 1-10 scale. When you find gaps, quantify the downstream impact on students, staff, or compliance. Prioritize equity-related findings (resource distribution across schools, program access, staff experience balance) alongside efficiency recommendations. Always check whether operational improvements reduce or increase teacher administrative burden.

============================================================
PHASE 1: SCHOOL OPERATIONS PLATFORM DISCOVERY
============================================================

Step 1.1 -- Technology Stack

Identify from package manifests: platform type (custom, Tyler Technologies-style,
Frontline-style, Alio-style, PowerSchool Business-style, or custom build), database
engine, financial system integration (ERP, accounting), HR system integration,
reporting engine, state reporting compatibility, GIS/mapping capabilities, dashboard
framework, mobile access for administrators.

Step 1.2 -- Operational Data Model

Read core structures: schools/buildings (location, capacity, rooms, grade configuration,
programs offered, designation -- Title I, magnet, charter), staff (positions, FTE,
salary, benefits, certifications, assignments, evaluation data), students (enrollment,
demographics, programs, transportation, special services), budget (fund accounting
structure, revenue sources, expenditure categories, grant tracking), facilities
(rooms, capacity, equipment, condition, maintenance), transportation (routes, vehicles,
stops, students assigned, drivers).

Step 1.3 -- Governance and Compliance Framework

Identify: state reporting requirements supported, federal program compliance (Title I,
Title II, Title III, IDEA, McKinney-Vento, Section 504), board policy integration,
audit preparation capabilities, data privacy compliance (FERPA, state student
privacy laws), open records/FOIA readiness.

============================================================
PHASE 2: SCHEDULING OPTIMIZATION
============================================================

Step 2.1 -- Master Schedule Building

Evaluate: master schedule generation (manual, semi-automated, constraint-based
optimization), constraint handling (teacher availability, room capacity, equipment
requirements, student course requests, singleton courses, travel time between buildings),
section count optimization (right-sizing sections to enrollment demand), schedule
conflict detection and resolution, multi-building scheduling for shared staff.

Step 2.2 -- Student Schedule Generation

Analyze: course request processing (priority ranking, alternate selections), schedule
generation algorithm (arena, batch, optimization-based), schedule quality metrics
(percent of students receiving first-choice courses, period distribution balance,
lunch distribution, study hall minimization), IEP-mandated service scheduling (related
services -- speech, OT, PT -- scheduled without missing core instruction), section
balancing (equitable class sizes).

Step 2.3 -- Schedule Impact Analysis

Evaluate: teacher load balancing (preparations count, consecutive teaching periods,
duty assignments), room utilization rates, bell schedule optimization (period lengths,
passing time, lunch waves), what-if scenario modeling (impact of adding/removing
sections, changing period structure), schedule comparison across years, student
schedule change request workflow.

============================================================
PHASE 3: RESOURCE ALLOCATION
============================================================

Step 3.1 -- Staff Allocation

Evaluate: staffing formula models (enrollment-based, weighted student count, program-
based), FTE allocation calculation, position control (authorized vs. filled positions),
class size management (targets, caps, overage tracking), specialist allocation (counselors,
librarians, nurses, psychologists per student ratios), teacher assignment optimization
(matching certification to course assignments, minimizing split assignments).

Step 3.2 -- Instructional Resource Allocation

Analyze: textbook and material inventory management, technology device allocation and
tracking (1:1 programs, shared carts, lab equipment), software license management
(per-student, per-teacher, site licenses), supply budget distribution (per-pupil
allocation, department allocation), library resource management, assessment material
procurement and distribution.

Step 3.3 -- Equity-Based Resource Distribution

Evaluate: Title I allocation calculations (per-pupil poverty-based distribution),
weighted student funding models (additional weight for ELL, special education, gifted,
at-risk), resource equity audits (are high-need schools receiving proportionally more
resources), staff experience distribution (are novice teachers concentrated in
high-need schools), program access equity (AP, gifted, elective access across schools).

============================================================
PHASE 4: BUDGET MANAGEMENT
============================================================

Step 4.1 -- Budget Architecture

Evaluate: fund accounting structure (general fund, special revenue, capital projects,
food service, grants), chart of accounts compliance (state-mandated coding), budget
development workflow (site-based input, central compilation, board approval), budget
amendment process, multi-year budget projection, encumbrance tracking, purchase
order workflow.

Step 4.2 -- Revenue and Expenditure Tracking

Analyze: revenue forecasting (local, state, federal by source), enrollment-driven
revenue modeling (per-pupil state aid calculations), grant revenue and expenditure
tracking (allowable costs, drawdown schedules, matching requirements), cash flow
management, payroll integration (largest expenditure category -- 80%+ of budget),
benefits cost tracking and projection, budget-to-actual variance reporting.

Step 4.3 -- Financial Reporting and Audit Readiness

Evaluate: state financial reporting compliance (annual financial report format), audit
trail completeness (every transaction traceable to approval and documentation), internal
controls documentation, segregation of duties enforcement in system access, board
financial report generation, grant financial reporting (federal and state specific
formats), transparency reporting (public-facing budget information), single audit
preparation support.

============================================================
PHASE 5: FACILITY UTILIZATION
============================================================

Step 5.1 -- Space Management

Evaluate: room inventory and classification (classroom, lab, gym, auditorium, office,
storage, specialized -- art, music, STEM), room capacity tracking, utilization rate
calculation (hours used vs. available hours), underutilized space identification,
space request and reservation system, shared space scheduling (gym, library, cafeteria,
auditorium), portable/modular classroom tracking.

Step 5.2 -- Maintenance and Operations

Analyze: work order management (submission, priority, assignment, completion, cost
tracking), preventive maintenance scheduling, building condition assessment tracking
(facility condition index), capital improvement planning, energy management and
consumption tracking, custodial task management, vendor management for contracted
services, safety inspection tracking (fire, health, environmental).

Step 5.3 -- Capacity Planning

Evaluate: enrollment projection impact on facility needs, renovation and construction
project tracking, boundary and attendance zone management, facility master planning
tools, portable and modular classroom deployment decisions, ADA accessibility
compliance tracking, indoor air quality and environmental health monitoring.

============================================================
PHASE 6: TRANSPORTATION ROUTING
============================================================

Step 6.1 -- Route Optimization

Evaluate: routing algorithm (manual, optimization-based, GPS-assisted), route efficiency
metrics (ride time limits, miles per student, route density), stop placement optimization
(walking distance, safe crossing, shelter), multi-tier routing (using buses for multiple
schools with staggered bell times), special needs transportation (door-to-door, wheelchair
accessible, aide assignment), hazard identification (busy intersections, railroad
crossings, construction zones).

Step 6.2 -- Fleet and Driver Management

Analyze: vehicle inventory and maintenance tracking (inspections, oil changes, tire
rotation, mileage), driver certification and training tracking (CDL, physical exam,
drug testing, background check), driver availability and absence management, substitute
driver assignment, fuel consumption tracking and optimization, GPS/AVL (Automatic
Vehicle Location) integration, vehicle camera system integration.

Step 6.3 -- Transportation Operations

Evaluate: daily route adjustments (weather, road closures, substitute drivers), parent
notification system (bus tracking, delay alerts, route changes), field trip transportation
management (vehicle assignment, driver assignment, routing, billing), transportation
eligibility determination (distance-based, hazard-based), McKinney-Vento transportation
(homeless students to school of origin), foster care transportation, special education
transportation compliance (IEP-mandated), ridership tracking, complaint management.

============================================================
PHASE 7: ENROLLMENT FORECASTING AND COMPLIANCE
============================================================

Step 7.1 -- Enrollment Forecasting

Evaluate: projection methodology (cohort survival, ratio-based, regression, demographic
analysis), historical accuracy tracking (projected vs. actual over past 5 years),
enrollment trend analysis by grade, school, and program, new development impact
modeling (housing starts, apartment construction), boundary change impact modeling,
school choice and open enrollment impact, kindergarten registration forecasting,
real-time enrollment monitoring during enrollment season.

Step 7.2 -- Special Education Compliance (IDEA)

Analyze: IEP timeline management (evaluation, eligibility, IEP development, annual
review, triennial re-evaluation), procedural safeguard documentation, parent
notification tracking (prior written notice, meeting invitations), service delivery
tracking (IEP services actually provided vs. required), progress reporting on IEP
goals (aligned with report card periods), least restrictive environment data
(percentage of time in general education), discipline tracking for students with
disabilities (manifestation determination, pattern of removals), state special
education reporting compliance, Medicaid billing for related services.

Step 7.3 -- Title I and Federal Program Reporting

Evaluate: Title I eligibility determination (schoolwide vs. targeted assistance),
comparability reporting (Title I schools receive equitable state/local resources),
supplement-not-supplant documentation, parent and family engagement compliance
(Title I compact, policy, meeting documentation), needs assessment process, school
improvement plan management, Title I financial reporting (expenditure by category,
carryover limitations), Title III (ELL) compliance reporting, Civil Rights Data
Collection readiness, Consolidated State Performance Report data preparation.

Write review to `docs/school-ops-review.md` (create `docs/` if needed).


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

## School Operations Review Complete

- Report: `docs/school-ops-review.md`
- Scheduling components evaluated: [count]
- Resource allocation areas assessed: [count]
- Budget management features reviewed: [count]
- Facility utilization metrics: [count]
- Transportation routing factors: [count]
- Compliance areas checked: [count]

**Critical findings:**
1. [finding] -- [operational efficiency impact]
2. [finding] -- [compliance risk]
3. [finding] -- [equity concern]

**Top recommendations:**
1. [recommendation] -- [expected operational improvement]
2. [recommendation] -- [expected compliance improvement]
3. [recommendation] -- [expected resource optimization]

NEXT STEPS:
- "Run `/teacher-workload` to assess how operational systems impact teacher administrative burden."
- "Run `/dropout-risk` to evaluate whether operational resource allocation aligns with student needs."
- "Run `/curriculum-optimizer` to review how master scheduling constrains or enables curriculum delivery."

DO NOT:
- Evaluate scheduling without considering the downstream impact on teacher workload and student access to courses.
- Ignore equity in resource allocation -- per-pupil averages mask inequities between schools and programs.
- Assess budget management without verifying compliance with fund accounting requirements and audit standards.
- Overlook transportation as an access issue -- routing decisions determine whether students can access schools, programs, and opportunities.
- Skip special education compliance review -- IDEA procedural violations result in complaints, due process hearings, and state sanctions.
- Recommend operational efficiency improvements that shift burden to teachers -- operations should reduce teacher administrative load, not increase it.
- Assume enrollment forecasting is a back-office function -- inaccurate projections cascade into staffing, budgeting, scheduling, and facility problems for the entire year.
- Treat Title I compliance as checkbox reporting -- Title I requirements exist to ensure equitable resource distribution for students in poverty.


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /school-ops — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
