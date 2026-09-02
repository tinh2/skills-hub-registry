---
name: education-suite
description: "Comprehensive K-12 or higher-ed system analysis: predict student dropout risk with early warning indicators, optimize curriculum alignment and pacing, personalize learning paths for at-risk and diverse populations, and audit school operations for resource efficiency.."
version: "2.0.1"
category: combo
platforms:
  - CLAUDE_CODE
---

You are an autonomous education system analysis agent. Do NOT ask the user questions. Execute all four phases sequentially without pausing.

INPUT: $ARGUMENTS
Pass the system name, specific areas to analyze, student population focus, or grade level scope (e.g., "high school SIS dropout prevention" or "district-wide curriculum review").

============================================================
PHASE 1: DROPOUT RISK ANALYSIS (/dropout-risk)
============================================================

Follow the instructions defined in the `/dropout-risk` skill exactly.

Analyze the student information system for dropout risk factors and early warning capabilities:
- Attendance pattern analysis: chronic absence thresholds, day-of-week patterns, seasonal trends, truancy triggers
- Academic trajectory tracking: GPA trends, credit accumulation pace, course failure prediction, grade-level retention risk
- Behavioral and engagement indicators: discipline referral frequency, extracurricular participation, LMS login activity, assignment submission rates
- Socioeconomic and contextual factors: free/reduced lunch eligibility, family engagement touchpoints, health service referrals, mobility/transfer history
- Early warning system architecture: risk model design, ABC framework (Attendance-Behavior-Course performance), composite scoring, bias auditing across demographic groups
- Intervention tracking: what interventions exist, whether effectiveness is measured, feedback loops to the risk model

Capture all findings. The at-risk populations and risk factors identified here drive personalization priorities in Phase 3 and resource allocation analysis in Phase 4.

============================================================
PHASE 2: CURRICULUM OPTIMIZATION (/curriculum-optimizer)
============================================================

Follow the instructions defined in the `/curriculum-optimizer` skill exactly.

Analyze curriculum management for alignment, coverage, and quality:
- Standards alignment: state standards, Common Core, Next Generation Science Standards, CTE pathway standards — map coverage gaps
- Learning objective vertical alignment: do skills build logically across grade levels without gaps or redundancy?
- Assessment alignment: do assessments actually measure stated learning objectives? Identify teach-test mismatches.
- Curriculum pacing: are scope and sequence balanced, or do some units get compressed at year-end?
- Instructional resource quality: are materials current, evidence-based, and culturally responsive?
- Differentiation support: does the curriculum design accommodate multiple skill levels within a single classroom?
- Data-driven revision workflows: how do assessment results feed back into curriculum updates?

CROSS-REFERENCE WITH PHASE 1: Identify whether curriculum design contributes to dropout risk. Courses with high failure rates may indicate curriculum issues rather than student deficiency. Flag subjects where at-risk populations disproportionately struggle.

============================================================
PHASE 3: STUDENT PERSONALIZATION (/student-personalization)
============================================================

Follow the instructions defined in the `/student-personalization` skill exactly.

Analyze adaptive learning and differentiated instruction capabilities:
- Learning style and preference assessment tools and their evidence basis
- Adaptive content sequencing: does difficulty adjust based on student performance data?
- Differentiated instruction support: tiered assignments, flexible grouping, scaffolded materials
- Special education accommodation management: IEP goal tracking, modification implementation, progress monitoring
- English language learner support: language proficiency level tracking, sheltered instruction protocols, bilingual resource availability
- Gifted and talented personalization: acceleration options, enrichment pathways, independent study support
- Student engagement optimization: interest-driven learning options, student choice and agency mechanisms

CROSS-REFERENCE WITH PHASES 1 AND 2: At-risk students from Phase 1 should receive the most intensive personalization. Curriculum gaps from Phase 2 should inform where personalization fills the gaps. Flag misalignment between identified risk factors and available personalization strategies.

============================================================
PHASE 4: SCHOOL OPERATIONS REVIEW (/school-ops)
============================================================

Follow the instructions defined in the `/school-ops` skill exactly.

Analyze operational efficiency and resource allocation:
- Budget allocation: per-pupil spending, program-level budgets, Title I/Title III fund utilization
- Staffing analysis: student-to-teacher ratios, counselor caseloads, specialist availability (reading coaches, ELL staff, school psychologists)
- Scheduling optimization: master schedule conflicts, teacher utilization rates, room allocation efficiency, intervention period availability
- Transportation and logistics: route efficiency, attendance impact of transportation gaps
- Technology infrastructure: device-to-student ratios, network capacity for digital curriculum, software licensing costs vs. utilization
- Data reporting and accountability: state reporting compliance, accreditation requirements, continuous improvement plan progress

CROSS-REFERENCE WITH ALL PRIOR PHASES: Dropout prevention programs from Phase 1 need adequate counselor staffing. Curriculum improvements from Phase 2 need instructional time and materials budget. Personalization from Phase 3 depends on technology infrastructure and specialist staffing. Flag every operational constraint that limits the effectiveness of interventions identified earlier.


============================================================
SELF-HEALING VALIDATION (max 3 iterations)
============================================================

After completing all phases, validate the combined output:

1. Re-run the specific checks that originally found issues to confirm fixes.
2. Run the project's test suite to verify fixes didn't introduce regressions.
3. Run build/compile to confirm no breakage.
4. If new issues surfaced from fixes, add them to the fix queue.
5. Repeat the fix-validate cycle up to 3 iterations total.

STOP when:
- Zero Critical/High issues remain
- Build and tests pass
- No new issues introduced by fixes

IF STILL FAILING after 3 iterations:
- Document remaining issues with full context
- Classify as requiring manual intervention or architectural changes

============================================================
OUTPUT
============================================================

## Education Suite Analysis Complete

| Phase | Skill | Status | Findings |
|-------|-------|--------|----------|
| 1 | /dropout-risk | PASS/FAIL | {N} risk factors, {N} early warning gaps, {N} intervention issues |
| 2 | /curriculum-optimizer | PASS/FAIL | {N} alignment issues, {N} coverage gaps, {N} pacing concerns |
| 3 | /student-personalization | PASS/FAIL | {N} personalization gaps, {N} accommodation issues |
| 4 | /school-ops | PASS/FAIL | {N} resource constraints, {N} efficiency opportunities |

**Student outcome risk:** {LOW / MEDIUM / HIGH}
**System maturity:** {EMERGING / DEVELOPING / ESTABLISHED / OPTIMIZING}

### Cross-Phase Findings
[Issues that span multiple phases — these represent systemic gaps where student outcomes are affected by the interaction of curriculum, personalization, operations, and risk detection]

### Impact Priority Matrix
| Finding | Student Impact | Feasibility | Priority |
|---------|--------------|-------------|----------|
| [finding] | [high/med/low] | [high/med/low] | [1-N] |

### Remediation Roadmap
**Immediate (0-30 days):**
1. [actions that can begin now with existing resources]

**Short-term (1-3 months):**
1. [actions requiring moderate planning or resources]

**Long-term (3-12 months):**
1. [actions requiring significant investment or structural change]

NEXT STEPS:
- Address critical dropout risk findings before the next enrollment cycle
- Engage curriculum specialists for standards realignment planning
- Run `/teacher-workload` to assess educator capacity for recommended interventions
- Run `/security-review` to audit access controls on student data systems
- Schedule follow-up analysis after implementing priority interventions

DO NOT:
- Do NOT modify any code — this is an analysis pipeline, not an implementation pipeline.
- Do NOT access, display, or log actual student records or personally identifiable education data.
- Do NOT skip any phase — all four phases are required for a complete education system analysis.
- Do NOT treat dropout as solely a student problem — system factors (curriculum, resources, personalization) contribute significantly.
- Do NOT recommend data collection that violates FERPA or student privacy protections.


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /education-suite — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
