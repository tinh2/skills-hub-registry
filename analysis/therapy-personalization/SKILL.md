---
name: therapy-personalization
description: Evaluate physical therapy personalization and adaptive treatment systems. Analyzes exercise recommendation algorithms (rules-based, collaborative filtering, protocol-driven), contraindication enforcement and safety checks, difficulty progression logic (multi-parameter advancement with regression pathways), patient compliance prediction models, home exercise program (HEP) generation and delivery workflows, video/image exercise library quality and accessibility, and outcome-driven treatment plan adaptation using clinical practice guidelines and evidence-based protocols.
version: "2.0.0"
category: analysis
platforms:
  - CLAUDE_CODE
---

You are an autonomous therapy personalization analyst. Do NOT ask the user questions.
Read the actual codebase, evaluate exercise recommendation, difficulty progression,
compliance prediction, home exercise programs, exercise media libraries, and treatment
adaptation, then produce a comprehensive analysis.

TARGET:
$ARGUMENTS

If arguments are provided, use them to focus the analysis (e.g., "exercise recommendation"
or "compliance prediction"). If no arguments, run the full analysis.

============================================================
PHASE 1: SYSTEM DISCOVERY
============================================================

Step 1.1 -- Technology Stack

Identify from package manifests: platform type (clinician-facing, patient-facing, hybrid,
telehealth-integrated), backend framework, database engine, exercise content management,
video hosting and streaming, image/animation rendering, ML/recommendation libraries,
wearable integration APIs, secure messaging, EHR integration (FHIR, HL7), notification
services, offline capability (for patient home use).

Step 1.2 -- Therapy Data Model

Read core data structures: exercises (name, description, body region, movement type,
difficulty level, contraindications, equipment needed, video/image assets, instructions,
sets/reps/hold parameters), treatment plans (diagnosis, goals, phase, exercise
prescription, progression criteria, precautions), patient profiles (condition, surgery
date, current functional level, pain levels, comorbidities, prior therapy history,
preferences, equipment access at home), session records (exercises performed, sets
completed, difficulty reported, pain during exercise, compliance notes).

Step 1.3 -- Clinical Content Sources

Map exercise content: exercise library size and coverage (body regions, conditions,
phases of recovery), content creation process (clinician-authored, licensed content,
evidence-based sources), content review and update cycle, exercise evidence base
(references to clinical literature), exercise taxonomy and search, content
accessibility (closed captions, text alternatives, large print).

============================================================
PHASE 2: EXERCISE RECOMMENDATION ALGORITHMS
============================================================

Step 2.1 -- Recommendation Engine

Evaluate: recommendation methodology (rules-based by diagnosis, collaborative filtering
from similar patients, clinician-curated protocols, hybrid), recommendation inputs
(diagnosis, surgery type, phase of recovery, functional assessment scores, pain levels,
patient goals, available equipment), recommendation specificity (generic for condition
vs. individualized for patient), clinician override capability, evidence base for
recommendations (clinical practice guidelines, research protocols).

Step 2.2 -- Contraindication Checking

Evaluate: contraindication database (exercises contraindicated for specific conditions,
post-surgical restrictions, comorbidity conflicts), contraindication enforcement
(hard block vs. warning), precaution documentation (modified exercise vs. avoided),
time-based restrictions (no overhead reaching for 6 weeks post-surgery), weight-bearing
status integration (non-weight bearing, partial, full), physician restriction
integration (specific orders that limit exercise selection).

Step 2.3 -- Exercise Variety and Progression Options

Evaluate: exercise alternatives for same goal (variety prevents boredom, accommodates
equipment limitations), exercise progression variants (same movement with increased
difficulty), regression variants (easier version when exercise is too difficult),
bilateral vs. unilateral options, open vs. closed chain alternatives, isotonic vs.
isometric vs. isokinetic options, functional activity integration (not just isolated
exercises but task-specific training).

============================================================
PHASE 3: DIFFICULTY PROGRESSION LOGIC
============================================================

Step 3.1 -- Progression Criteria

Evaluate: how progression triggers are defined (pain level below threshold, completed
prescribed sets without difficulty, ROM milestone reached, strength milestone reached,
time-based protocol progression), progression granularity (small increments vs. phase
jumps), multi-parameter progression (increase sets before increasing resistance,
increase resistance before increasing complexity).

Step 3.2 -- Progression Pathways

Evaluate: progression parameter options (repetitions, sets, hold duration, resistance,
speed, range of motion, balance challenge, surface instability, functional complexity),
progression sequencing (which parameter changes first), maximum progression rate limits
(safety guards against advancing too quickly), regression pathway when patient struggles
(automatic difficulty reduction), plateau-specific strategies (change exercise type
when plateau detected).

Step 3.3 -- Progression Automation vs. Clinical Judgment

Evaluate: automated progression recommendations (system suggests, clinician approves),
fully automated progression (system advances without clinician input -- higher risk),
clinician-only progression (manual only -- misses optimization opportunities), data-
driven progression support (patient's metrics suggest readiness to advance), progression
documentation and audit trail, progression override documentation (why clinician
deviated from system recommendation).

============================================================
PHASE 4: PATIENT COMPLIANCE PREDICTION
============================================================

Step 4.1 -- Compliance Tracking

Evaluate: compliance measurement methods (session attendance, HEP completion self-report,
wearable-verified exercise completion, app usage analytics, video exercise completion
tracking), compliance rate calculation (completed exercises / prescribed exercises),
compliance trending over time (declining, stable, improving), compliance by exercise
type (which exercises are most and least completed), partial compliance recognition
(completed 2 of 3 sets -- not binary).

Step 4.2 -- Compliance Prediction Model

Evaluate: prediction features (historical compliance, exercise complexity, pain levels,
program duration, number of exercises prescribed, session frequency, patient demographics,
motivation indicators, barriers reported), model type (logistic regression, decision
tree, neural network, rules-based), prediction accuracy, prediction timing (how early
can non-compliance be detected), model validation.

Step 4.3 -- Compliance Intervention

Evaluate: non-compliance alerts (to clinician, to patient), intervention options
(simplify program, reduce exercise count, address barriers, motivational messaging,
schedule adjustment, family/caregiver engagement), intervention trigger thresholds,
intervention effectiveness tracking, program modification based on compliance patterns
(prescribe fewer exercises to improve completion rate), gamification and engagement
features (streaks, badges, progress milestones).

============================================================
PHASE 5: HOME EXERCISE PROGRAM GENERATION
============================================================

Step 5.1 -- HEP Creation Workflow

Evaluate: exercise selection for HEP (clinician selects from library, system suggests
based on treatment plan, combination), HEP customization (sets, reps, frequency,
hold times, resistance level per exercise), HEP formatting (printable PDF, mobile
app, email, patient portal), HEP language and reading level (patient literacy
considerations), HEP modification workflow (update program between visits).

Step 5.2 -- HEP Content Quality

Evaluate: exercise instruction clarity (step-by-step text, key cues, common errors),
visual aids (photos, illustrations, video demonstrations), exercise parameter display
(sets, reps, hold time, frequency clearly shown), safety warnings and precautions,
pain guidance (expected discomfort vs. stop immediately), warm-up and cool-down
inclusion, exercise order and grouping logic.

Step 5.3 -- HEP Delivery and Tracking

Evaluate: multi-channel delivery (mobile app, email, text, printed handout, patient
portal), offline access (exercises viewable without internet connection), exercise
completion logging (patient marks exercises as done), HEP adherence reminders
(configurable notification schedule), exercise feedback mechanism (patient reports
difficulty, pain, or questions), HEP version history (what was prescribed when),
caregiver access (family member can view and assist).

============================================================
PHASE 6: VIDEO AND IMAGE EXERCISE LIBRARIES
============================================================

Step 6.1 -- Content Library

Evaluate: library size (number of exercises with media), body region coverage,
condition coverage, media quality (resolution, lighting, camera angles, professional
production), model diversity (age, body type, ability level -- patients should see
themselves represented), media format options (video, animated GIF, static image,
illustration), content update process.

Step 6.2 -- Media Accessibility

Evaluate: closed captions for video, audio descriptions, text alternatives for images,
playback speed control, looping capability for technique review, downloadable for
offline viewing, mobile-optimized (responsive sizing, bandwidth-aware), language
options (subtitles, voiceover), color contrast and readability of overlaid text.

Step 6.3 -- Custom Content

Evaluate: ability to upload custom exercise videos (clinician-recorded for specific
patient), custom content annotation (draw on video, add markers), custom content
sharing (share custom exercise across clinicians in same practice), content rights
management, patient-recorded video for remote assessment (patient uploads form check),
telehealth integration (live demonstration with recording).

============================================================
PHASE 7: TREATMENT PLAN ADAPTATION
============================================================

Step 7.1 -- Outcome-Driven Adaptation

Evaluate: which outcomes trigger plan modification (assessment score changes, goal
achievement, goal non-achievement, regression, pain increase, patient request),
adaptation response types (exercise change, intensity change, frequency change,
modality addition, referral to specialist), adaptation timing (real-time after
each session, at formal reassessment points, clinician-initiated only).

Step 7.2 -- Evidence-Based Protocols

Evaluate: clinical practice guideline integration (APTA clinical practice guidelines,
condition-specific protocols), protocol adherence tracking, protocol deviation
documentation, protocol selection based on evidence quality (randomized controlled
trials, systematic reviews), protocol update process when new evidence published,
protocol variation by patient complexity.

Step 7.3 -- Multi-Disciplinary Coordination

Evaluate: treatment plan sharing with other providers (physician, occupational
therapist, speech therapist, psychologist), co-treatment documentation, care
coordination communication tools, interdisciplinary goal alignment, handoff
procedures (transition between care settings -- inpatient to outpatient to home),
patient-centered plan modifications (incorporating patient preferences and life
context).

Write analysis to `docs/therapy-personalization-analysis.md` (create `docs/` if needed).


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

## Therapy Personalization Analysis Complete

- Report: `docs/therapy-personalization-analysis.md`
- Exercise recommendation components evaluated: [count]
- Difficulty progression factors assessed: [count]
- Compliance prediction capabilities: [count]
- Home exercise program features reviewed: [count]
- Exercise library quality metrics: [count]
- Treatment adaptation mechanisms analyzed: [count]

**Critical findings:**
1. [finding] -- [patient outcome impact]
2. [finding] -- [personalization accuracy concern]
3. [finding] -- [compliance prediction gap]

**Top recommendations:**
1. [recommendation] -- [expected improvement in exercise adherence]
2. [recommendation] -- [expected improvement in outcome-driven adaptation]
3. [recommendation] -- [expected improvement in patient experience]

NEXT STEPS:
- "Run `/recovery-metrics` to evaluate the outcome measurements that drive treatment adaptation."
- "Run `/setback-predictor` to analyze prediction of therapy setbacks and readmission risk."
- "Run `/security-review` to audit access controls on patient health data."

DO NOT:
- Do NOT modify any code -- this is an analysis skill, not an implementation skill.
- Do NOT include real patient names, medical records, or protected health information in output.
- Do NOT evaluate clinical treatment decisions -- evaluate the system's ability to support and personalize those decisions.
- Do NOT treat exercise prescription as simple -- contraindication checking is a patient safety concern.
- Do NOT ignore compliance barriers -- the best exercise program is worthless if patients cannot or will not do it.
- Do NOT assume technology access -- many rehabilitation patients are elderly and may have limited device literacy.
- Do NOT overlook the clinician workflow -- overly complex personalization systems that slow clinicians down will not be used.
- Do NOT evaluate progression logic without safety limits -- automated progression without clinical oversight is a liability risk.
- Do NOT assume video quality replaces instruction quality -- clear written cues matter as much as visual demonstration.


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /therapy-personalization — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
