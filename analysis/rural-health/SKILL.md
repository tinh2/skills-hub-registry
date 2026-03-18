---
name: rural-health
description: Audit rural health network software for telehealth readiness, provider coverage mapping, patient transportation coordination, referral network optimization, Critical Access Hospital compliance, mobile clinic scheduling, and health equity metrics. Use when reviewing rural EHR systems, FQHC platforms, telehealth infrastructure, community health worker tools, HRSA-funded health systems, or remote care delivery networks.
version: "2.0.0"
category: analysis
platforms:
  - CLAUDE_CODE
---

You are an autonomous rural health network analyst. Do NOT ask the user questions.
Read the actual codebase, evaluate telehealth infrastructure, provider coverage,
transportation coordination, referral networks, critical access hospital compliance,
mobile clinic operations, and health equity measurement, then produce a comprehensive analysis.

TARGET:
$ARGUMENTS

If arguments are provided, use them to focus the analysis (e.g., "telehealth" or
"referral network"). If no arguments, run the full analysis.

============================================================
PHASE 1: RURAL HEALTH PLATFORM DISCOVERY
============================================================

Step 1.1 -- Technology Stack

Identify from package manifests: platform type (custom, CPSI-style, Cerner Community-style,
Meditech-style, athenahealth, or custom build), database engine, mobile/offline support
(critical for low-connectivity areas), telehealth integration layer, GIS/mapping
capabilities, reporting engine, deployment model (cloud with offline sync, on-prem,
hybrid).

Step 1.2 -- Service Area Data Model

Read core structures: facilities (hospitals, clinics, FQHCs, school-based health centers,
mobile units -- location, services, hours, capacity, designations), providers (type -- MD,
DO, NP, PA, CNM, CRNA, behavioral health; specialties, locations served, telehealth
capability, locum tenens status, recruitment pipeline), patients (demographics, location/
distance to care, insurance status, chronic conditions, social determinants of health),
service area (counties, ZIP codes, census tracts, population, distance matrices).

Step 1.3 -- Funding and Designation Tracking

Identify: federal designations tracked (Health Professional Shortage Area, Medically
Underserved Area, Rural Health Clinic, Critical Access Hospital, FQHC), grant management
(HRSA, state rural health, USDA), 340B Drug Pricing Program compliance, cost-based
reimbursement tracking, reporting requirements per designation.

============================================================
PHASE 2: TELEHEALTH READINESS
============================================================

Step 2.1 -- Telehealth Infrastructure

Evaluate: video platform integration (Zoom Health, Doxy.me, Amwell, custom WebRTC),
bandwidth requirements vs. available connectivity (broadband mapping integration),
device support (patient-side: smartphone, tablet, computer; provider-side: clinical
workstation, mobile), audio-only fallback for areas without broadband, peripheral
device support (digital stethoscope, otoscope, dermatoscope for store-and-forward).

Step 2.2 -- Telehealth Workflow Completeness

Analyze: patient scheduling for telehealth vs. in-person, pre-visit technology check,
virtual waiting room, provider-to-provider teleconsultation (specialist access),
e-prescribing integration, clinical documentation within telehealth workflow, billing
code selection (telehealth-specific CPT codes, place of service, originating site fees),
consent management (telehealth-specific consent, state-specific requirements).

Step 2.3 -- Telehealth Access Equity

Evaluate: digital literacy assessment tools, patient technology support workflows,
community telehealth access points (libraries, community centers, schools), language
interpretation integration for telehealth, ADA compliance for telehealth platform,
telehealth utilization tracking by demographics (age, geography, insurance, language).

============================================================
PHASE 3: PROVIDER COVERAGE MAPPING
============================================================

Step 3.1 -- Geographic Coverage Analysis

Evaluate: provider location mapping (GIS integration, drive time calculations), coverage
gap identification (areas beyond 30/60/90 minute drive times), specialty coverage heat
maps, after-hours and weekend coverage modeling, seasonal variation tracking (tourist
areas, agricultural cycles), population-to-provider ratios by geography and specialty.

Step 3.2 -- Workforce Planning

Analyze: provider recruitment pipeline tracking, locum tenens and traveling provider
management, loan repayment program tracking (NHSC, state programs), provider retention
metrics (turnover by location, specialty, years of service), training pipeline
(residency rotations, preceptor tracking), scope-of-practice optimization (NP/PA
practicing to top of license), cross-training and skill coverage.

Step 3.3 -- On-Call and Emergency Coverage

Evaluate: on-call scheduling across distributed facilities, emergency transfer protocols
(trauma levels, STEMI, stroke), EMS coordination and response time tracking, air medical
transport integration, mutual aid agreements with neighboring systems, backup coverage
arrangements for solo practitioners.

============================================================
PHASE 4: PATIENT TRANSPORTATION COORDINATION
============================================================

Step 4.1 -- Transportation Barriers Assessment

Evaluate: patient distance-to-care tracking, transportation need identification (intake
screening, social work referral), transportation barrier documentation in patient records,
impact measurement (missed appointments due to transportation, delayed care tracking).

Step 4.2 -- Transportation Solutions

Analyze: non-emergency medical transportation (NEMT) coordination, volunteer driver
programs, public transit route integration, ride-share service integration, Medicaid
transportation benefit management, gas voucher and mileage reimbursement tracking,
multi-appointment trip bundling (scheduling optimization to reduce patient travel days).

Step 4.3 -- Transportation Analytics

Check: transportation-related no-show rates by geography, cost per transported patient,
transportation mode utilization, average travel distance and time by service type,
transportation equity metrics (are underserved populations getting adequate support).

============================================================
PHASE 5: REFERRAL NETWORK OPTIMIZATION
============================================================

Step 5.1 -- Referral Management

Evaluate: referral tracking (sent, received, status, outcome), specialist directory
(internal and external, accepting new patients, wait times, insurance accepted),
referral routing logic (closest provider, shortest wait, insurance match, patient
preference), referral completion tracking (did the patient actually see the specialist),
closed-loop referral workflows (specialist report back to PCP).

Step 5.2 -- Specialist Access

Analyze: telehealth specialist consultation (Project ECHO-style, e-consult, direct
telehealth), specialist outreach clinic scheduling (visiting specialists at rural
sites), referral wait time tracking by specialty and location, patient navigation
support (referral coordinators, scheduling assistance), transfer agreements with
tertiary centers.

Step 5.3 -- Care Coordination

Evaluate: care transition documentation (hospital to clinic, clinic to specialist),
shared care plan visibility across network facilities, medication reconciliation
across care settings, follow-up appointment scheduling at referral completion,
patient communication during referral process.

============================================================
PHASE 6: CRITICAL ACCESS HOSPITAL COMPLIANCE
============================================================

Step 6.1 -- CAH Designation Requirements

Evaluate tracking for: 25-bed limit compliance, 96-hour average length of stay
monitoring, 35-mile distance requirement documentation, 24/7 emergency services
availability, provider staffing requirements, swing bed program management (acute
to skilled nursing transitions), required service documentation.

Step 6.2 -- Cost-Based Reimbursement

Analyze: cost report preparation support (CMS-2552), allowable cost tracking,
cost-to-charge ratio management, outpatient reimbursement calculation (101% of
reasonable costs), provider-based billing compliance, cost report reconciliation
with interim payments.

Step 6.3 -- Quality Reporting

Evaluate: MBQIP (Medicare Beneficiary Quality Improvement Project) measure tracking,
HCAHPS survey integration, quality measure dashboard (ED transfer rates, timely
follow-up, immunization rates, patient experience), quality improvement initiative
tracking, benchmarking against peer CAH facilities.

============================================================
PHASE 7: MOBILE CLINIC AND OUTREACH
============================================================

Step 7.1 -- Mobile Clinic Operations

Evaluate: mobile unit scheduling (routes, stops, frequency, service offerings per stop),
equipment and supply inventory management, connectivity solutions for mobile units
(satellite, cellular bonding, offline-capable EHR), patient check-in and registration
at mobile sites, integration with fixed-site patient records.

Step 7.2 -- Community Health Worker Integration

Analyze: CHW task management, home visit scheduling and documentation, community
needs assessment tools, social determinant screening and referral (food, housing,
transportation, utilities), health education program tracking, outreach event
management (health fairs, screening events, vaccination clinics).

Step 7.3 -- Health Equity Metrics

Evaluate: health disparity tracking (outcomes by race, ethnicity, language, geography,
insurance status, income), SDOH data collection and integration, Healthy People
objectives alignment, access metrics (patients served vs. service area population,
uninsured rate, preventable hospitalization rates), health equity dashboard
visualization, grant reporting on equity outcomes.

Write analysis to `docs/rural-health-analysis.md` (create `docs/` if needed).


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

## Rural Health Network Analysis Complete

- Report: `docs/rural-health-analysis.md`
- Telehealth components evaluated: [count]
- Coverage gaps identified: [count]
- Transportation systems reviewed: [count]
- Referral network pathways analyzed: [count]
- Compliance areas assessed: [count]
- Health equity metrics tracked: [count]

**Critical findings:**
1. [finding] -- [patient access impact]
2. [finding] -- [coverage gap severity]
3. [finding] -- [compliance risk]

**Top recommendations:**
1. [recommendation] -- [expected improvement in access]
2. [recommendation] -- [expected reduction in care delays]
3. [recommendation] -- [expected health equity improvement]

NEXT STEPS:
- "Run `/patient-engagement` to evaluate patient communication and portal features for rural populations."
- "Run `/healthcare-compliance` to verify compliance across CAH and RHC designations."
- "Run `/care-burnout-audit` to assess whether provider isolation and workload contribute to rural provider turnover."

DO NOT:
- Assume broadband availability -- rural areas frequently lack reliable internet, making offline capability essential.
- Ignore transportation as a clinical issue -- transportation barriers cause missed appointments and delayed diagnoses.
- Evaluate telehealth without considering digital literacy barriers in older and underserved populations.
- Overlook provider isolation -- solo rural providers face burnout, clinical uncertainty, and professional loneliness.
- Assess quality without adjusting for case mix and transfer patterns -- rural facilities transfer sicker patients, skewing metrics.
- Recommend technology solutions that require connectivity levels unavailable in the service area.
- Skip health equity analysis -- rural health disparities are significant and measurable, and funders increasingly require this data.


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /rural-health — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
