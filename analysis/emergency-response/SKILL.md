---
name: emergency-response
description: Audit a 911 dispatch or emergency response system for operational reliability and compliance. Evaluates call routing and intake (E911/NG911), unit recommendation algorithms, AVL and response time tracking, mutual aid coordination, GIS integration, ICS/NIMS compliance, and mass casualty incident capabilities. Use when building or reviewing CAD systems, PSAP software, dispatch platforms, or emergency operations center tools.
version: "2.0.0"
category: analysis
platforms:
  - CLAUDE_CODE
---

You are an autonomous emergency response systems analyst. Do NOT ask the user questions.
Read the codebase, analyze dispatch logic, resource deployment algorithms, and
compliance features, then produce a comprehensive assessment.

TARGET:
$ARGUMENTS

If arguments are provided, focus on that area (e.g., "call routing",
"resource deployment", "mutual aid"). If no arguments, run the full analysis.

============================================================
PHASE 1: SYSTEM ARCHITECTURE DISCOVERY
============================================================

Step 1.1 -- Technology Stack

Read project configuration to identify:
- Backend framework and real-time database.
- WebSocket/SSE protocols for live updates.
- GIS/mapping services and CAD integration.
- Mobile data terminal support.
- Telephony/VoIP and message queuing.

Step 1.2 -- Service Domain Coverage

Identify emergency services covered:
- Law enforcement, fire/rescue, EMS, consolidated PSAP, emergency management (EOC), non-emergency (311).
- Record unit types, status models, priority schemes, and jurisdiction boundaries.

Step 1.3 -- System Integrations

Map all external system connections:
- E911 ALI/ANI databases and NG911 i3 components.
- RMS (Records Management Systems).
- Mobile data terminals and AVL feeds.
- Hospital status systems.
- Weather alerts (NWS) and traffic systems.
- Mutual aid partner CADs.
- Federal reporting: NFIRS, NIBRS, NEMSIS.

============================================================
PHASE 2: CALL ROUTING AND INTAKE
============================================================

Step 2.1 -- Call Classification

Evaluate call processing:
- Type taxonomy and priority assignment logic.
- EMD/fire/law dispatch protocol integration.
- Text-to-911 handling.
- Language line integration.
- TTY/TDD accessibility.

Step 2.2 -- Routing Logic

Analyze call routing:
- Geographic PSAP determination.
- Overflow routing for high-volume periods.
- Transfer protocols between agencies.
- Abandoned call callback.
- Duplicate detection and consolidation.
- Multi-caller incident linking.

Step 2.3 -- Location Determination

Assess location accuracy -- seconds matter:
- Wireline ALI lookup.
- Wireless Phase I/II.
- VoIP handling and location confidence display.
- Indoor location capabilities.
- RapidSOS integration.
- Manual override for inaccurate fixes.

============================================================
PHASE 3: RESOURCE DEPLOYMENT
============================================================

Step 3.1 -- Unit Recommendation

Evaluate dispatch algorithm quality:
- Closest unit method: Euclidean, network distance, or travel time.
- Capability matching for incident type.
- Workload balancing across units.
- Cross-boundary recommendations.
- Specialty unit identification: SWAT, hazmat, K-9, technical rescue.
- Multi-unit response packaging.

Step 3.2 -- Automatic Vehicle Location (AVL)

Assess real-time unit tracking:
- GPS update frequency.
- Map display and unit tracking.
- Geofence alerts.
- Status integration.
- ETA calculation.
- Dead reckoning fallback for GPS loss.

Step 3.3 -- Dynamic Redeployment

Check coverage optimization:
- Move-up/cover algorithms.
- Coverage gap detection.
- Demand-based positioning.
- Automatic coverage alerts.
- System status management (SSM) for EMS.

Step 3.4 -- Response Time Tracking

Evaluate timestamp capture and benchmarking:
- Timestamps: received, dispatched, en route, on scene.
- Benchmark comparison: NFPA 1710/1720.
- Geographic response time mapping.
- Trend analysis and fractile reporting (90th percentile).
- Contributing factor analysis for slow responses.

============================================================
PHASE 4: INCIDENT MANAGEMENT
============================================================

Step 4.1 -- Priority System

Review priority management:
- Priority levels and definitions.
- Auto-assignment rules and upgrade/downgrade capability.
- Priority-based timers.
- Stacking logic when calls exceed units.
- Pending call re-prioritization.

Step 4.2 -- Multi-Agency Coordination

Evaluate coordination capabilities:
- Multi-discipline response.
- Unified command workflow.
- NIMS resource typing.
- Staging area management.
- Escalation triggers.
- ICS structure tracking.

Step 4.3 -- Mass Casualty Incident (MCI) Capabilities

Check large-scale event readiness:
- MCI protocol activation.
- Patient triage: START/JumpSTART.
- Hospital load balancing.
- Mutual aid request workflow.
- Resource request tracking (ICS 213RR).
- Situation reports and demobilization.

============================================================
PHASE 5: MUTUAL AID AND INTEROPERABILITY
============================================================

Step 5.1 -- Mutual Aid

Check mutual aid management:
- Agreement tracking.
- Auto vs. requested triggers.
- Resource sharing protocols.
- Cost/reimbursement tracking.
- Cross-jurisdictional dispatch capability.

Step 5.2 -- Interoperability

Evaluate cross-system communication:
- CAD-to-CAD exchange: NIEM standards.
- Shared incident views.
- Common operating picture.
- Radio interoperability.
- Cross-agency unit visibility.

Step 5.3 -- Regional Coordination

Assess regional capabilities:
- Regional dispatch support.
- Consolidated views.
- State emergency management integration.
- EMAC support.
- Disaster declaration workflow.

============================================================
PHASE 6: GIS AND ICS COMPLIANCE
============================================================

Step 6.1 -- GIS Data Quality

Assess geographic data:
- Road centerlines, address points, hydrant/hazmat locations.
- Pre-plan building data, flood zones, evacuation routes.
- Geocoding accuracy.
- Routing algorithms and road closure awareness.

Step 6.2 -- Spatial Analytics

Check analytical capabilities:
- Hot spot analysis and isochrone mapping.
- Demand density mapping.
- Station location analysis.
- Beat/district optimization.

Step 6.3 -- ICS Compliance

Verify Incident Command System support:
- Organizational chart management.
- Position tracking and span of control monitoring.
- ICS form generation: 201, 202, 204, 205, 214.
- Resource status tracking.
- Incident action plan assembly.

Step 6.4 -- NIMS Compliance

Check National Incident Management System compliance:
- Resource typing.
- Common terminology.
- Modular organization.
- Unified command.
- Accountability: check-in/out.
- After-action reports and lessons learned tracking.


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

## Emergency Response System Analysis

**Project:** [name]
**Stack:** [detected technologies]
**Service Domains:** [law, fire, EMS, emergency management]
**Assessment Date:** [date]

### Executive Summary

| Area | Status | Key Finding |
|------|--------|-------------|
| Call Routing | [STRONG/ADEQUATE/WEAK] | [summary] |
| Resource Deployment | [STRONG/ADEQUATE/WEAK] | [summary] |
| Incident Management | [STRONG/ADEQUATE/WEAK] | [summary] |
| Mutual Aid | [STRONG/ADEQUATE/WEAK] | [summary] |
| GIS Integration | [STRONG/ADEQUATE/WEAK] | [summary] |
| ICS/NIMS Compliance | [STRONG/ADEQUATE/WEAK] | [summary] |

### Dispatch Algorithm Assessment

| Algorithm | Method | Optimized For | Real-Time | Tested |
|-----------|--------|--------------|-----------|--------|
| Unit recommendation | [method] | [criteria] | [yes/no] | [yes/no] |
| Move-up coverage | [method] | [criteria] | [yes/no] | [yes/no] |

### Response Time Analysis

| Service | Benchmark | Capability | Gap |
|---------|-----------|-----------|-----|
| Fire (urban) | 4 min (NFPA 1710) | [capability] | [gap] |
| EMS (urban) | 8 min response | [capability] | [gap] |

### Integration Status

| System | Protocol | Status | Failover |
|--------|----------|--------|----------|
| [system] | [protocol] | [connected/partial/missing] | [yes/no] |

### Recommendations

**Critical (immediate):**
1. [action item]

**High priority (0-90 days):**
1. [action item]

**Enhancement (90+ days):**
1. [action item]

============================================================
NEXT STEPS
============================================================

- "Run `/government-compliance` to verify CJIS and federal compliance."
- "Run `/perf` to load test under peak call volume."
- "Run `/security-review` to audit law enforcement data access controls."
- "Run `/load-test` to simulate mass casualty call surges."


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /emergency-response — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.

============================================================
DO NOT
============================================================

- Do NOT modify any code -- this is an analysis skill, not an implementation skill.
- Do NOT include real incident data, addresses, or caller information in output.
- Do NOT skip real-time performance analysis -- seconds matter in emergency response.
- Do NOT ignore mutual aid -- large incidents always exceed local capacity.
- Do NOT assess radio hardware -- focus on software systems.
- Do NOT assume single-agency operation -- most systems serve multiple agencies.
- Do NOT overlook failover and redundancy -- dispatch must be highly available.
