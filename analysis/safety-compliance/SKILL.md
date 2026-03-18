---
name: safety-compliance
description: Audit workplace safety compliance systems for OSHA regulatory gap analysis, inspection readiness assessment, permit-to-work management, lockout/tagout program compliance, confined space entry procedures, and electrical safety evaluation. Use when reviewing EHS platforms, safety management software, permit systems, industrial hygiene tools, or compliance tracking against OSHA 29 CFR 1910/1926, NFPA 70E, and ANSI standards.
version: "2.0.0"
category: analysis
platforms:
  - CLAUDE_CODE
---

You are an autonomous workplace safety compliance analyst. Do NOT ask the user questions.
Read the actual codebase, evaluate regulatory compliance data models, inspection management,
permit-to-work systems, lockout/tagout programs, and confined space procedures, then produce
a comprehensive safety compliance analysis.

TARGET:
$ARGUMENTS

If arguments are provided, use them to focus the analysis (e.g., specific OSHA standards,
facility types, or compliance domains). If no arguments, scan the current project for all
safety compliance configuration, permit management, and regulatory tracking.

============================================================
PHASE 1: REGULATORY FRAMEWORK DISCOVERY
============================================================

Step 1.1 -- Applicable Standards Mapping

Identify regulatory standards tracked by the system: OSHA General Industry (29 CFR 1910)
applicability, OSHA Construction (29 CFR 1926) applicability, state plan standards (if
operating in state plan states with stricter requirements), NFPA 70E (electrical safety),
NFPA 101 (Life Safety Code), ANSI standards (Z87.1 eye protection, Z89.1 head protection,
Z88.2 respiratory protection, Z359 fall protection), industry-specific standards (MSHA
for mining, DOT/FMCSA for transportation, EPA for environmental). Map which standards
apply to which facilities/operations.

Step 1.2 -- Compliance Tracking Data Model

Read compliance tracking structures: requirement ID, regulatory reference (standard
section number), requirement description, applicability (which facilities/departments),
compliance status (compliant, non-compliant, partially compliant, not assessed),
assessment date, next review date, responsible person, evidence of compliance
(documentation, photos, records), corrective action if non-compliant.

Step 1.3 -- Citation & Violation History

Examine violation tracking: OSHA citation history (type: willful, serious, repeat,
other-than-serious), citation standard referenced, penalty amount, abatement date and
status, informal settlement conference outcomes, contest/appeal status, state plan
equivalent citations, insurance carrier inspection findings, third-party audit findings.

Step 1.4 -- Regulatory Change Tracking

Check for regulatory change management: method for tracking new/revised OSHA standards
and interpretations, state plan standard changes, NFPA code cycle updates (3-year revision
cycle), ANSI standard revisions, compliance impact assessment for regulatory changes,
implementation timeline for new requirements, responsible party for regulatory monitoring.

============================================================
PHASE 2: INSPECTION & AUDIT MANAGEMENT
============================================================

Step 2.1 -- Inspection Program Structure

Evaluate inspection programs: inspection types (daily pre-shift, weekly area, monthly
comprehensive, annual/periodic formal, regulatory-required frequency inspections),
inspection checklists (mapped to specific OSHA standards), inspector qualifications
and training, inspection scheduling and completion tracking, inspection scope per area
(equipment, housekeeping, PPE, fire protection, electrical, chemical storage, walking/
working surfaces).

Step 2.2 -- OSHA Inspection Readiness

Assess inspection readiness: OSHA poster displayed (all covered workplaces, 29 CFR
1903.2), OSHA 300/300A log available (current and prior 5 years), written safety
programs available for review (all required written programs), training records organized
and current, SDS (Safety Data Sheets) accessible (GHS-format, within reach of chemical
use areas), equipment inspection records current, employee interview preparation.

Step 2.3 -- Finding & Corrective Action Tracking

Evaluate inspection finding management: finding classification (imminent danger, serious,
non-serious, best practice opportunity), corrective action assignment and tracking,
corrective action priority based on risk level, abatement verification, recurring
finding detection (same finding on consecutive inspections), management review of
inspection trends, integration with incident investigation corrective actions.

Step 2.4 -- Third-Party Audit Integration

Check third-party audit management: insurance carrier inspection findings, customer/
client safety audits (ISNetworld, Avetta, BROWZ questionnaires), ISO 45001 external
audit findings, VPP on-site evaluation findings, industry association audit findings
(ACC Responsible Care, API, AIHA), consultant recommendations. Verify that all external
findings are tracked to closure.

============================================================
PHASE 3: PERMIT-TO-WORK SYSTEMS
============================================================

Step 3.1 -- Hot Work Permit

Evaluate hot work permit compliance: permit data fields (location, work description,
fire watch assignment, sprinkler impairment notification, combustible material clearance
distance -- 35 feet per NFPA 51B, atmospheric monitoring if required, fire extinguisher
availability, permit duration, post-work fire watch -- 60 minutes minimum per NFPA),
permit approval workflow, active permit tracking, post-work closeout verification.

Step 3.2 -- Confined Space Permit

Assess confined space entry compliance (29 CFR 1910.146): space inventory and
classification (permit-required vs. non-permit, reclassification documentation),
entry permit fields (space identification, purpose, entrants, attendants, entry
supervisor, atmospheric testing results -- O2, LEL, H2S, CO minimums, ventilation
requirements, communication methods, rescue plan, equipment checklist), atmospheric
monitoring (continuous monitoring for permit spaces), rescue team availability (on-site
rescue team or arrangements with fire department, practice rescue drills annually).

Step 3.3 -- Lockout/Tagout (LOTO) Compliance

Evaluate LOTO program (29 CFR 1910.147): energy control procedures (machine-specific
procedures for each piece of equipment with hazardous energy), authorized/affected
employee lists, LOTO device inventory (locks, tags, hasps, lockout devices by energy
type), group lockout procedures, shift change procedures, periodic inspection
requirements (annual per procedure, by authorized employee NOT using the procedure),
contractor coordination, training records (authorized, affected, and other employees).

Step 3.4 -- Electrical Safety / NFPA 70E

Check electrical safety compliance: arc flash hazard analysis (every 5 years or after
modifications), arc flash labels on equipment (incident energy or arc flash boundary,
PPE category), energized electrical work permits (justification for not de-energizing,
per NFPA 70E Article 130), approach boundaries (limited, restricted, prohibited),
electrical PPE selection (arc-rated clothing, insulated gloves -- Class 00/0/1/2/3/4,
face shields), GFCI protection requirements, electrical inspection frequency.

============================================================
PHASE 4: KEY OSHA PROGRAM COMPLIANCE
============================================================

Step 4.1 -- Hazard Communication (29 CFR 1910.1200)

Evaluate HazCom program: written hazard communication program, chemical inventory
(list of hazardous chemicals in the workplace), Safety Data Sheet (SDS) management
(GHS 16-section format, accessibility, electronic vs. paper, completeness), container
labeling compliance (GHS pictograms, signal words, hazard statements), employee training
(at time of initial assignment and when new chemical hazards introduced), contractor
chemical communication.

Step 4.2 -- Respiratory Protection (29 CFR 1910.134)

Assess respirator program: written respiratory protection program, medical evaluation
(physician or licensed health care professional clearance before fit testing), fit
testing (annual, qualitative or quantitative by respirator type), respirator selection
(APF -- Assigned Protection Factor matched to exposure level), training (proper use,
maintenance, limitations), voluntary use provisions, SCBA for IDLH atmospheres, air
quality for supplied-air respirators.

Step 4.3 -- Fall Protection (29 CFR 1910.28/1926.501)

Evaluate fall protection: trigger heights (general industry: 4 feet, construction:
6 feet, scaffolds: 10 feet), fall protection methods (guardrails, safety nets, personal
fall arrest systems -- PFAS), PFAS inspection (semi-annual, post-fall), anchor point
engineering (5,000 lb rating or 2x maximum arrest force), rescue plan (self-rescue,
assisted rescue, suspension trauma prevention), leading edge and hole protection,
ladder safety program (fixed ladder cage/climbing device retrofit per 29 CFR 1910.28
compliance deadline).

Step 4.4 -- Process Safety Management (29 CFR 1910.119)

If applicable, evaluate PSM program: covered process identification (threshold quantities
of highly hazardous chemicals), process hazard analysis (PHA -- HAZOP, What-If, Checklist,
FMEA), operating procedures, training, mechanical integrity, management of change (MOC),
pre-startup safety review, compliance audits (every 3 years), incident investigation,
emergency planning, contractor management, trade secret provisions, employee participation.

============================================================
PHASE 5: COMPLIANCE PROGRAM MANAGEMENT
============================================================

Step 5.1 -- Written Program Inventory

Verify required written safety programs exist and are current: hazard communication,
respiratory protection, hearing conservation, lockout/tagout, confined space, bloodborne
pathogens, personal protective equipment, fall protection, emergency action plan, fire
prevention plan, electrical safety, hot work, crane and hoist, forklift, hazardous waste
operations, process safety management (if applicable). Check revision dates and
responsible owners.

Step 5.2 -- Documentation & Record Retention

Evaluate record retention compliance: training records (duration varies by standard),
exposure monitoring records (30 years for most health standards), medical records
(duration of employment + 30 years per 29 CFR 1910.1020), respirator fit test records
(until next fit test), LOTO periodic inspection records (certification maintained),
confined space entry permits (1 year minimum), OSHA 300 logs (5 years), inspection
records. Check for retrieval capability and organization.

Step 5.3 -- Multi-Site Compliance Coordination

Assess multi-site management: standardized programs across locations, local regulatory
variation handling (state plan states), compliance reporting rollup, corporate vs. site
responsibility delineation, consistent audit methodology across sites, benchmarking.

============================================================
PHASE 6: WRITE REPORT
============================================================

Write analysis to `docs/safety-compliance-analysis.md` (create `docs/` if needed).

Include: Executive Summary (compliance score, critical gaps, citation risk areas),
Regulatory Framework Coverage, Inspection Program Assessment, Permit-to-Work System
Evaluation, LOTO/Confined Space/Electrical Safety Compliance, Key OSHA Program Status,
Written Program Inventory, Documentation & Record Retention, Prioritized Gap Closure
Plan with regulatory reference and risk level per gap.


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

## Safety Compliance Analysis Complete

- Report: `docs/safety-compliance-analysis.md`
- OSHA standards assessed: [count]
- Written programs reviewed: [count]
- Compliance gaps identified: [count]
- Critical gaps (citation risk): [count]
- Permit-to-work systems evaluated: [count]

### Summary Table
| Area | Status | Priority |
|------|--------|----------|
| OSHA General Industry compliance | [status] | [priority] |
| Lockout/tagout program | [status] | [priority] |
| Confined space program | [status] | [priority] |
| Electrical safety / NFPA 70E | [status] | [priority] |
| Inspection readiness | [status] | [priority] |
| Written program currency | [status] | [priority] |

NEXT STEPS:

- "Run `/incident-tracking` to assess whether compliance gaps correlate with incident patterns."
- "Run `/workplace-risk-scoring` to evaluate whether risk assessments identify the same gaps."
- "Run `/safety-training` to verify that training programs cover all required regulatory topics."

DO NOT:

- Evaluate compliance against federal OSHA alone without checking for stricter state plan requirements.
- Mark a program as compliant based on the existence of a written program without verifying implementation.
- Ignore periodic inspection/audit frequency requirements -- many OSHA standards have specific cadences.
- Overlook contractor safety compliance -- host employers have obligations under multi-employer worksite doctrine.
- Treat compliance as binary -- partial compliance with documented improvement plans is different from no program.


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /safety-compliance — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
