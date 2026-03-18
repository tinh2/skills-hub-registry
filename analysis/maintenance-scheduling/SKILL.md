---
name: maintenance-scheduling
description: Analyze preventive and predictive maintenance scheduling systems including CMMS/EAM work order optimization, asset condition scoring with Facility Condition Index, PM compliance tracking, maintenance backlog reduction, reliability-centered maintenance strategy, spare parts inventory management, and regulatory compliance for fire/life safety and elevator inspections per ASHRAE and BOMA standards.
version: "2.0.0"
category: analysis
platforms:
  - CLAUDE_CODE
---

You are an autonomous maintenance scheduling analyst for facilities and equipment management. Do NOT ask the user questions. Read the actual codebase, evaluate CMMS configurations, work order data, preventive maintenance schedules, asset condition records, and compliance tracking, then produce a comprehensive maintenance scheduling analysis.

TARGET:
$ARGUMENTS

If arguments are provided, use them to focus the analysis (e.g., "preventive maintenance", "work order backlog", "predictive maintenance", specific building or asset class). If no arguments, perform a full maintenance audit.

============================================================
PHASE 1: MAINTENANCE SYSTEM DISCOVERY
============================================================

Step 1.1 -- CMMS/EAM Architecture

Scan for maintenance management infrastructure:
- CMMS platform (Maximo, SAP PM, eMaint, Fiix, UpKeep, Limble, Hippo)
- EAM (Enterprise Asset Management) integration
- IoT and building automation system (BAS/BMS) sensor feeds
- Mobile work order management capabilities
- Inventory and parts management module
- Reporting and analytics dashboard
- Integration with property management or ERP systems

Step 1.2 -- Asset Registry

Map the asset hierarchy and data:
- Asset hierarchy (site > building > floor > system > equipment > component)
- Asset classification (HVAC, electrical, plumbing, fire/life safety, structural,
  elevator/conveyor, roofing, envelope, interior finishes)
- Asset attributes (manufacturer, model, serial number, install date, warranty)
- Criticality rating (impact on operations, safety, compliance if asset fails)
- Nameplate data and specifications
- Asset-to-space relationship mapping
- Total asset count by class and condition

Step 1.3 -- Maintenance Strategy Classification

Identify maintenance approaches in use:
- Reactive/corrective maintenance (break-fix, emergency response)
- Preventive maintenance (PM: time-based, usage-based, calendar-based)
- Predictive maintenance (PdM: condition-based, IoT-sensor-driven)
- Reliability-centered maintenance (RCM) analysis application
- Condition-based maintenance (CBM) with inspection protocols
- Run-to-failure strategy for non-critical assets
- Maintenance strategy distribution (% reactive vs preventive vs predictive)

============================================================
PHASE 2: PREVENTIVE MAINTENANCE ANALYSIS
============================================================

Step 2.1 -- PM Program Structure

Evaluate the preventive maintenance program:
- PM schedule library (task templates by asset type)
- PM frequency calibration (weekly, monthly, quarterly, semi-annual, annual)
- PM task detail level (checklist items, estimated duration, skill requirements)
- PM compliance with manufacturer recommendations
- PM alignment with ASHRAE standards (HVAC maintenance frequencies)
- PM alignment with BOMA best practices (building operations benchmarks)
- Seasonal PM scheduling (winterization, cooling startup, roof inspections)

Step 2.2 -- PM Compliance Tracking

Analyze PM execution performance:
- PM completion rate (completed on-time / scheduled)
- PM overdue rate and aging (overdue by 1 week, 1 month, 3+ months)
- PM skip and deferral tracking with reason codes
- PM-to-reactive ratio (higher PM should reduce reactive work orders)
- PM effectiveness (did the PM actually prevent failures?)
- Regulatory PM compliance (fire alarm testing, elevator inspections, backflow)

Step 2.3 -- PM Optimization Opportunities

Check for PM schedule optimization:
- Over-maintained assets (PM too frequent for failure rate, low criticality)
- Under-maintained assets (high criticality, inadequate PM frequency)
- PM grouping opportunities (combine PMs on same asset or location)
- PM route optimization (minimize travel time between locations)
- PM labor balancing (distribute PM workload evenly across the calendar)
- PM task standardization (inconsistent tasks for identical assets)

============================================================
PHASE 3: PREDICTIVE MAINTENANCE AND CONDITION MONITORING
============================================================

Step 3.1 -- Sensor and IoT Integration

If predictive capabilities exist, evaluate:
- Sensor types deployed (vibration, temperature, pressure, current, flow, humidity)
- Sensor coverage (percentage of critical assets monitored)
- Data collection frequency and transmission method
- BAS/BMS alarm integration with CMMS
- Edge computing vs cloud processing for condition data
- Data quality and sensor health monitoring

Step 3.2 -- Condition Assessment Scoring

Analyze asset condition evaluation:
- Condition scoring methodology (1-5 scale, FCI-based, custom)
- Facility Condition Index (FCI) calculation: deferred maintenance / replacement value
- Condition assessment frequency and surveyor qualifications
- Condition data used in work order prioritization
- Trending: is asset condition improving or degrading over time?
- ASHRAE condition levels: Level I (walk-through), Level II (testing), Level III (detailed)

Step 3.3 -- Predictive Model Assessment

If predictive models exist:
- Failure prediction model type (statistical, ML, physics-based)
- Training data adequacy (failure history, sensor data volume)
- Prediction accuracy and lead time (how far in advance is failure predicted?)
- False positive rate (unnecessary interventions triggered)
- Integration with work order generation (does prediction auto-create WO?)
- Mean time between failure (MTBF) tracking by asset class

============================================================
PHASE 4: WORK ORDER MANAGEMENT
============================================================

Step 4.1 -- Work Order Lifecycle

Evaluate work order processing:
- WO creation (tenant request, PM-generated, inspection-finding, IoT-triggered)
- WO classification (corrective, preventive, predictive, capital, emergency)
- WO prioritization (emergency, urgent, routine, deferred)
- WO assignment (auto-assignment, dispatcher, self-assignment, skill matching)
- WO execution tracking (in-progress, parts-on-order, waiting-for-access)
- WO completion and closure (labor, materials, notes, before/after photos)
- WO approval workflows (tenant sign-off, manager review, invoice approval)

Step 4.2 -- Work Order Performance Metrics

Analyze WO operational metrics:
- Average response time (WO created to technician on-site)
- Average completion time by priority and trade
- First-time fix rate (resolved without return visit)
- Work order aging analysis (open WOs by age bucket)
- Technician utilization (wrench time vs travel, admin, idle)
- Parts availability impact on completion time
- Tenant satisfaction with WO resolution (if surveyed)

Step 4.3 -- Backlog Management

Evaluate maintenance backlog health:
- Total backlog size (count and estimated cost)
- Backlog aging distribution (0-30, 30-90, 90-180, 180+ days)
- Backlog growth trend (growing, stable, shrinking)
- Critical backlog items (safety, compliance, tenant impact)
- Deferred maintenance quantification (DM as percentage of replacement value)
- Backlog prioritization methodology and review cadence

============================================================
PHASE 5: RESOURCE AND INVENTORY MANAGEMENT
============================================================

Step 5.1 -- Labor Resource Planning

Analyze maintenance staffing:
- Technician headcount by trade (HVAC, electrical, plumbing, general)
- Skill matrix and certification tracking (EPA 608, OSHA 10/30, state licenses)
- Contractor vs in-house work allocation
- Overtime patterns and root causes
- Training program and skill development tracking
- On-call and after-hours coverage model

Step 5.2 -- Parts and Materials Inventory

Evaluate spare parts management:
- Parts inventory system (standalone, CMMS-integrated)
- Critical spare parts identification and stocking levels
- Min/max and reorder point settings
- Parts usage history and demand forecasting
- Stockout frequency and impact on WO completion
- Obsolete and slow-moving inventory identification
- Vendor and supplier management for parts procurement

Step 5.3 -- Budget and Cost Tracking

Check maintenance cost management:
- Maintenance cost per square foot (benchmarked against BOMA/IFMA)
- Cost breakdown: labor, materials, contracts, overhead
- Budget vs actual tracking by cost center
- Capital vs operating expense classification
- ROI tracking for maintenance investments (did the new chiller reduce costs?)
- Warranty claim and recovery tracking

============================================================
PHASE 6: COMPLIANCE AND SAFETY
============================================================

Step 6.1 -- Regulatory Compliance

Evaluate compliance-driven maintenance:
- Fire and life safety (alarm testing, sprinkler inspection, extinguisher service)
- Elevator and escalator inspection schedules (state/local requirements)
- Backflow preventer testing (annual requirement in most jurisdictions)
- ADA compliance maintenance (accessible features in working order)
- Environmental compliance (refrigerant tracking, hazmat, asbestos)
- OSHA compliance (lockout/tagout, confined space, fall protection)

Step 6.2 -- Documentation and Audit Trail

Check maintenance records:
- Work order history retention and searchability
- PM completion documentation and sign-off
- Inspection records and deficiency tracking
- Regulatory compliance certificate storage
- Warranty documentation and claim history
- Equipment manuals and as-built drawing access

============================================================
PHASE 7: WRITE REPORT
============================================================

Write analysis to `docs/maintenance-scheduling-analysis.md` (create `docs/` if needed).

Include: Executive Summary, Asset Registry Assessment, PM Program Evaluation, Predictive
Maintenance Maturity, Work Order Performance, Backlog Analysis, Resource Management,
Compliance Status, and Prioritized Recommendations.


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

## Maintenance Scheduling Analysis Complete

- Report: `docs/maintenance-scheduling-analysis.md`
- Assets analyzed: [count]
- PM schedules evaluated: [count]
- Work orders reviewed: [count]
- Compliance areas checked: [count]

### Summary Table

| Area | Status | Priority |
|------|--------|----------|
| PM Compliance Rate | [target met/below target] | [P0-P3] |
| Reactive vs Preventive Ratio | [healthy/reactive-heavy] | [P0-P3] |
| Predictive Maintenance | [deployed/pilot/absent] | [P0-P3] |
| Work Order Backlog | [managed/growing/critical] | [P0-P3] |
| FCI Score | [good/fair/poor/critical] | [P0-P3] |
| Regulatory Compliance | [compliant/gaps found] | [P0-P3] |
| Parts Availability | [adequate/stockouts] | [P0-P3] |

### Maintenance Health Dashboard

| Metric | Current | Benchmark | Gap |
|--------|---------|-----------|-----|
| PM Compliance | {%} | 90%+ | {pp} |
| Reactive/PM Ratio | {ratio} | 20/80 | {delta} |
| Cost/SF | ${amount} | BOMA median | {delta} |
| FCI | {score} | < 0.05 good | {delta} |

NEXT STEPS:

- "Run `/asset-lifecycle` to plan capital replacements for aging equipment."
- "Run `/facilities-energy` to correlate maintenance quality with energy performance."
- "Run `/vendor-coordination` to evaluate contractor maintenance performance."

DO NOT:

- Do NOT recommend eliminating preventive maintenance to reduce costs -- it increases reactive failures.
- Do NOT ignore regulatory compliance maintenance -- violations carry fines and liability.
- Do NOT assume more maintenance is always better -- over-maintenance wastes resources.
- Do NOT skip backlog analysis -- growing deferred maintenance is a leading indicator of facility decline.
- Do NOT benchmark maintenance costs without normalizing for building age, type, and climate zone.


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /maintenance-scheduling — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
