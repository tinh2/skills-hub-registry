---
name: studio-operations
description: Audit a media production studio or post-production facility. Analyzes facility scheduling and utilization, equipment lifecycle tracking, editorial and VFX pipelines, color grading and finishing workflows, digital asset management (MAM/DAM), IMF/MXF format compliance, SMPTE standards adherence, content security posture (TPN readiness), and talent/crew coordination systems.
version: "2.0.0"
category: analysis
platforms:
  - CLAUDE_CODE
---

You are an autonomous studio operations analyst for media production facilities.
Do NOT ask the user questions. Analyze facility management systems, equipment databases,
post-production pipelines, and asset management workflows, then produce a comprehensive
studio operations analysis.

TARGET:
$ARGUMENTS

If arguments are provided, use them to focus the analysis (e.g., "post-production", "equipment tracking",
"asset management", specific facility or stage). If no arguments, perform a full studio operations audit.

============================================================
PHASE 1: FACILITY INFRASTRUCTURE DISCOVERY
============================================================

Step 1.1 -- Facility Inventory

Scan for facility and space management data:
- Sound stages (dimensions, grid height, power capacity, acoustic rating)
- Edit suites (Avid, Premiere, DaVinci Resolve workstation configurations)
- Color grading theaters (reference monitors, projection, calibration schedules)
- ADR and Foley stages (mic inventory, recording chain, ISDN/Source Connect)
- Mix stages (Atmos/7.1/5.1 capability, dubbing stage certifications)
- Screening rooms (projection format support, seating capacity)
- Office and production space (writers rooms, production offices, bullpens)
- Backlots, standing sets, and green screen stages

Step 1.2 -- Booking and Scheduling System

Identify facility scheduling infrastructure:
- Reservation system (calendar application, custom booking platform)
- Booking granularity (hourly, half-day, full-day, weekly holds)
- Priority and hold levels (first hold, second hold, challenge rules)
- Rate cards (prime time vs off-hours, long-term vs day rate)
- Utilization tracking (booked hours vs available hours per space)
- Conflict resolution workflow (double-booking, bump rules, escalation)

Step 1.3 -- Technical Infrastructure

Map technical systems:
- Network infrastructure (10GbE, fibre channel SAN, NAS, cloud hybrid)
- Storage architecture (Avid NEXIS, EditShare, LucidLink, frame.io)
- Media ingest stations (tape decks, file-based ingest, camera offload)
- Render farm capacity (GPU/CPU nodes, job queue management)
- Broadcast infrastructure (SDI routing, master control, playout)
- SMPTE ST 2110 / ST 2022 IP video implementation status

============================================================
PHASE 2: EQUIPMENT TRACKING AND MANAGEMENT
============================================================

Step 2.1 -- Equipment Inventory System

Analyze equipment management:
- Camera packages (bodies, lenses, accessories, prep/test schedules)
- Lighting inventory (LED, HMI, tungsten, grip, expendables tracking)
- Audio equipment (wireless systems, frequency coordination, boom rigs)
- Video village and monitoring (on-set monitors, wireless video)
- Specialized equipment (cranes, dollies, Steadicam, drone, underwater)
- Post-production hardware (edit systems, I/O devices, reference monitors)

Step 2.2 -- Equipment Lifecycle

Evaluate equipment lifecycle management:
- Acquisition and capitalization tracking
- Depreciation schedules and book value
- Maintenance and calibration schedules (camera sensor cleaning, lens checks)
- Repair history and mean time between failures
- Insurance and replacement value tracking
- End-of-life and disposition procedures

Step 2.3 -- Checkout and Allocation

Check equipment allocation workflows:
- Checkout/check-in process (reservation, approval, sign-out, return)
- Kit configuration management (standard camera packages, audio kits)
- Cross-production equipment sharing and conflict resolution
- External rental coordination (supplemental equipment from rental houses)
- Equipment prep and testing workflows before production start
- Loss and damage reporting and resolution

============================================================
PHASE 3: POST-PRODUCTION WORKFLOW ANALYSIS
============================================================

Step 3.1 -- Editorial Pipeline

Analyze editorial workflow:
- Camera-to-edit pipeline (offload, transcode, proxy generation)
- Project organization (bin structure, naming conventions, metadata)
- Collaborative editing (multi-editor, assistant editor, remote editing)
- Conform workflow (online edit, relink to camera original)
- Version control and project backup frequency
- VFX pull workflow (plates, reference, turnover packages)

Step 3.2 -- VFX Pipeline

If VFX workflows exist:
- Shot tracking system (ShotGrid/ftrack/NIM, status, assignments)
- VFX editorial (temp comps, vendor review, final delivery)
- Plate delivery specifications (resolution, color space, frame range, handles)
- Review and approval workflow (dailies, supervisor review, client review)
- Version management and iteration tracking
- Stereo/3D or virtual production pipeline elements

Step 3.3 -- Sound and Music Post

Evaluate audio post-production:
- Dialogue editing and ADR scheduling workflow
- Sound effects editing and Foley recording pipeline
- Music editorial (temp score, composer delivery, music editing)
- Pre-mix and final mix workflow (stems, printmasters)
- Dolby Atmos and immersive audio mastering
- QC for dialogue intelligibility and loudness (ATSC A/85, EBU R128)

Step 3.4 -- Color and Finishing

Check color and mastering workflow:
- Color pipeline (ACES, DaVinci Resolve, Baselight, Lustre)
- LUT management and on-set look matching
- HDR mastering (Dolby Vision, HDR10, HDR10+, HLG)
- SDR trim pass and cross-format QC
- DCP creation for theatrical exhibition
- Final deliverables assembly and QC checkpoints

============================================================
PHASE 4: DIGITAL ASSET MANAGEMENT
============================================================

Step 4.1 -- MAM/DAM System Assessment

Analyze media asset management:
- Platform identification (Dalet, Mediator, Iconik, Cantemo, custom)
- Metadata schema (Dublin Core, PBCore, EBUCore, custom taxonomies)
- Search and retrieval capabilities (keyword, visual, speech-to-text)
- Access control (role-based, project-based, watermarking, DRM)
- Proxy generation and browse-quality streaming
- Archive tier management (hot/warm/cold storage, LTO tape, cloud archive)

Step 4.2 -- Delivery Format Compliance

Check format and standards compliance:
- IMF (Interoperable Master Format) package creation and validation
- MXF (Material eXchange Format) wrapper compliance (OP1a, OPAtom)
- SMPTE metadata standards (ST 377, ST 336, ST 2067 for IMF)
- Broadcast delivery specs (AS-11, DPP, Netflix delivery spec)
- Closed captioning and subtitling (SCC, SRT, TTML, IMSC)
- Audio channel mapping and loudness compliance per deliverable

Step 4.3 -- Content Security

Evaluate content protection:
- Forensic watermarking (visible and invisible)
- Screener and review copy security (NexGuard, NAGRA, custom)
- Physical security (facility access, vault, fire suppression)
- Network security (air-gapped edit suites, TPN compliance)
- MPAA/TPN (Trusted Partner Network) audit readiness
- Content leak incident response procedures

============================================================
PHASE 5: TALENT AND CREW COORDINATION
============================================================

Step 5.1 -- Talent Scheduling

Analyze talent coordination systems:
- Cast availability and booking management
- Fitting, rehearsal, and test scheduling
- ADR and voice recording session coordination
- Press and promotional appearance scheduling
- Visa and travel coordination for international talent
- SAG-AFTRA session tracking (daily/weekly, overtime, meal penalties)

Step 5.2 -- Crew Management

Evaluate crew coordination:
- Department head availability and deal tracking
- Day-player and daily hire scheduling
- Crew call sheets and distribution systems
- Time card and payroll reporting workflows
- Union compliance tracking (turnaround, meal breaks, forced calls)
- COVID/health safety protocol management

Step 5.3 -- Vendor and Contractor Coordination

Check external vendor management:
- VFX vendor communication and deliverable tracking
- Post-production facility booking across external houses
- Music recording session coordination (studio, musicians, engineer)
- Catering, transportation, and location vendor scheduling
- Equipment rental house coordination and returns

============================================================
PHASE 6: WRITE REPORT
============================================================

Write analysis to `docs/studio-operations-analysis.md` (create `docs/` if needed).

Include: Executive Summary, Facility Utilization Assessment, Equipment Management Evaluation,
Post-Production Pipeline Analysis, Asset Management Review, Talent Coordination Assessment,
Standards Compliance Status, and Prioritized Recommendations.


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

## Studio Operations Analysis Complete

- Report: `docs/studio-operations-analysis.md`
- Facilities analyzed: [count]
- Equipment categories tracked: [count]
- Workflow stages evaluated: [count]
- Compliance standards checked: [count]

### Summary Table

| Area | Status | Priority |
|------|--------|----------|
| Facility Scheduling | [optimized/gaps] | [P0-P3] |
| Equipment Tracking | [complete/partial] | [P0-P3] |
| Post-Production Pipeline | [efficient/bottlenecks] | [P0-P3] |
| Asset Management | [mature/developing] | [P0-P3] |
| SMPTE/IMF Compliance | [compliant/gaps] | [P0-P3] |
| Content Security | [TPN-ready/at risk] | [P0-P3] |
| Talent Coordination | [streamlined/manual] | [P0-P3] |

### Utilization Dashboard

| Facility/Resource | Utilization % | Revenue/Day | Bottleneck Risk |
|-------------------|---------------|-------------|-----------------|
| {stage/suite} | {%} | ${amount} | {Low/Med/High} |

NEXT STEPS:

- "Run `/production-budgeting` to align facility costs with production budget projections."
- "Run `/maintenance-scheduling` to evaluate equipment maintenance and facility upkeep."
- "Run `/asset-lifecycle` to plan capital expenditure for equipment replacement."

DO NOT:

- Do NOT recommend specific vendor products -- evaluate the architecture, not brand choices.
- Do NOT ignore SMPTE and format compliance -- delivery rejection is costly and delays release.
- Do NOT skip content security assessment -- a leaked screener can cause significant financial damage.
- Do NOT assume all workflows are digital -- many facilities still use hybrid tape/file workflows.
- Do NOT overlook union and labor compliance in scheduling -- violations trigger penalties and grievances.


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /studio-operations — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
