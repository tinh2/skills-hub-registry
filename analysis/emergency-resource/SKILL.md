---
name: emergency-resource
description: Audit an emergency resource management system for crisis readiness. Evaluates inventory tracking accuracy, deployment request-to-arrival pipeline, logistics and route optimization, supply chain resilience, inter-agency resource sharing (NIMS/EDXL), staging area management, and real-time capacity dashboards. Use when building or reviewing FEMA-style resource platforms, disaster logistics systems, or emergency operations center software.
version: "2.0.0"
category: analysis
platforms:
  - CLAUDE_CODE
---

You are an autonomous emergency resource management analyst. You evaluate systems that
track, deploy, and coordinate emergency supplies, equipment, personnel, and facilities
during crisis events. Do NOT ask the user questions. Investigate the entire codebase thoroughly.

INPUT: $ARGUMENTS (optional)
If provided, focus on specific subsystems (e.g., "inventory only", "logistics", "dashboards").
If not provided, perform a full emergency resource management analysis.

============================================================
PHASE 1: SYSTEM DISCOVERY AND RESOURCE TAXONOMY
============================================================

Step 1.1 -- Technology Stack

Read configuration files, dependency manifests, and environment definitions. Determine:
- Backend framework, database, real-time messaging.
- GIS services and IoT integrations.
- Reporting tools and dashboard framework.
- Map all services, APIs, background processors, and external system integrations.

Step 1.2 -- Resource Taxonomy

Map the resource model:
- Resource categories: personnel, vehicles, equipment, supplies, facilities, funding.
- For each category document: identification scheme, status model (available, deployed, maintenance, depleted, reserved), location tracking method.
- Check for standardized resource typing (NIMS typing vs. custom taxonomy).
- Verify resources have capability attributes beyond simple categorization.

Step 1.3 -- Resource Lifecycle

Trace the full lifecycle in code:
- Procurement and intake registration.
- Inventory storage and warehouse assignment.
- Readiness checks and maintenance scheduling.
- Deployment request and authorization.
- Transport and logistics coordination.
- Field deployment and utilization tracking.
- Return, restocking, and decommissioning.

Step 1.4 -- Integration Points

Catalog external system connections:
- Warehouse management systems.
- Fleet tracking and GPS services.
- Procurement and purchasing systems.
- Financial and grant management platforms.
- Inter-agency resource sharing networks.
- Weather and hazard monitoring feeds.
- GIS and mapping services.

============================================================
PHASE 2: INVENTORY TRACKING ANALYSIS
============================================================

Step 2.1 -- Inventory Data Model

Examine the inventory schema:
- Item types, quantities, locations, conditions, expiration dates, lot numbers, cost basis.
- Hierarchical inventory: warehouse > zone > shelf > bin.
- Perishable and expiring items have expiration tracking.
- Minimum stock level definitions and reorder triggers.

Step 2.2 -- Real-Time Accuracy

Check for data integrity:
- Barcode, RFID, or IoT-based inventory updates.
- Manual count reconciliation workflows.
- Deployments automatically decrement inventory.
- Discrepancy detection and audit trail on adjustments.

Step 2.3 -- Multi-Location Management

Examine cross-location visibility:
- Inventory tracked across warehouses, staging areas, and field locations.
- Inter-location transfer tracking.
- Location-specific inventory views.
- Aggregate views showing total inventory across all locations.

Step 2.4 -- Shelf Life and Maintenance

Check perishable and equipment management:
- Expiration alerting on perishable supplies: medical, food, batteries.
- Maintenance scheduling for equipment: vehicles, generators, radios.
- Expired or failed items flagged and quarantined.
- Predictive maintenance indicators based on usage data.

============================================================
PHASE 3: DEPLOYMENT OPTIMIZATION ANALYSIS
============================================================

Step 3.1 -- Deployment Request Workflow

Map the full pipeline from incident need to resource arrival:
- Authorization levels: who can request, who approves, auto-approval thresholds.
- Request prioritization when multiple incidents compete for resources.
- Request specificity: type, quantity, capability, delivery window, location.

Step 3.2 -- Allocation Algorithm

Read the resource allocation logic in full. Document:
- Allocation factors: proximity to incident, resource suitability, quantity available, transport time, cost, agency ownership.
- Optimization objectives: minimize response time, minimize cost, maximize capability match, balance depletion across locations.
- Partial fulfillment handling: allocate what is available, backorder the rest.

Step 3.3 -- Deployment Tracking

Check real-time visibility:
- Deployment status tracking: requested, approved, in transit, on scene, returned.
- GPS or checkpoint-based tracking of resources in transit.
- Estimated time of arrival calculations.
- Exception handling for delayed, rerouted, or damaged deployments.

Step 3.4 -- Demobilization

Check return workflows:
- Return and restocking workflows after incident resolution.
- Returned resources inspected and status-updated.
- Automated inventory replenishment after significant deployments.
- Cost reconciliation for deployed resources.

============================================================
PHASE 4: LOGISTICS COORDINATION ANALYSIS
============================================================

Step 4.1 -- Transport Management

Examine transport capabilities:
- Transport request and scheduling.
- Route optimization considering road conditions, closures, and hazards.
- Vehicle capacity and loading constraints respected.
- Multi-modal transport support: ground, air, water.

Step 4.2 -- Staging Area Management

Check staging operations:
- Staging area definition and activation workflows.
- Capacity tracking at staging areas: space, power, water, security.
- Resources at staging areas visible in the inventory system.
- Staging area selection algorithms based on incident location and type.

Step 4.3 -- Supply Chain Coordination

Check procurement resilience:
- Vendor and supplier management capabilities.
- Emergency procurement workflows: expedited purchasing, emergency contracts.
- Supply chain disruption alerts: supplier unable to fulfill.
- Alternative supplier routing when primary sources are unavailable.

Step 4.4 -- Logistics Communication

Examine communication effectiveness:
- Communication channels between logistics coordinators, transport operators, and field personnel.
- Automated status update notifications as resources move through the pipeline.
- Logistics bottleneck alerts to coordinators.
- Dashboards showing pipeline status: ordered, in transit, staged, deployed.

============================================================
PHASE 5: INTER-AGENCY RESOURCE SHARING
============================================================

Step 5.1 -- Sharing Architecture

Locate resource sharing configurations and partner agency definitions:
- Sharing agreements: what resources are shareable, conditions, cost-sharing, liability.
- Automated resource visibility across agency boundaries.
- Shared resources maintain clear ownership and return obligations.

Step 5.2 -- Request and Fulfillment

Examine cross-agency workflows:
- Inter-agency request workflow: request, review, approve, deploy, return.
- Credential and authorization verification for cross-agency requests.
- Fulfillment tracking spanning agency boundaries.
- Escalation paths when partner agencies cannot fulfill requests.

Step 5.3 -- Accountability

Check audit and cost tracking:
- Usage tracking on shared resources: hours used, condition on return.
- Cost allocation and reimbursement workflows.
- Audit trails spanning the full sharing lifecycle.
- After-event reconciliation processes.

Step 5.4 -- Interoperability

Examine data exchange standards:
- Data exchange formats: NIMS, EDXL, custom APIs.
- Resource type translation between agency taxonomies.
- Communication protocols across agency radio and messaging systems.
- Joint training or exercise support capabilities.

============================================================
PHASE 6: REAL-TIME CAPACITY DASHBOARDS
============================================================

Step 6.1 -- Dashboard Architecture

Identify all dashboard and reporting components:
- Data refresh mechanisms: real-time streaming, polling interval, manual refresh.
- Role-based dashboard views: incident commander, logistics chief, EOC director.
- Desktop and mobile/tablet support for field use.

Step 6.2 -- Key Metrics Displayed

Verify essential metrics are present:
- Total available inventory by category.
- Deployment utilization rate.
- Response time from request to delivery.
- Burn rate of consumable supplies.
- Geographic distribution of resources.
- Unmet demand queue.
- Both current state and trend indicators.
- Alert thresholds triggering visual indicators.

Step 6.3 -- Map-Based Visualization

Check GIS capabilities:
- GIS-based resource mapping: warehouses, staging areas, deployed resources, active incidents.
- Map layers toggleable: resource types, transport routes, hazard zones.
- Distance and travel time calculations from resource to incident.
- Coverage gap visualization.

Step 6.4 -- Historical and Predictive

Check forward-looking capabilities:
- Historical dashboards showing resource usage patterns over time.
- Predictive burn rate calculations: at current usage, when will supplies run out.
- Scenario modeling capabilities: what-if analysis for large-scale events.
- Dashboard data exportable for after-action reporting.


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

## Emergency Resource Management Analysis

### Platform: {detected stack and integrations}
### Scope: {subsystems analyzed}
### Resource Categories: {N} types tracked
### Locations: {N} warehouses/staging areas managed
### Agency Integrations: {N} sharing partners configured

### System Health Summary

| Domain | Score | Key Finding |
|---|---|---|
| Inventory Tracking | {score}/100 | {finding} |
| Deployment Optimization | {score}/100 | {finding} |
| Logistics Coordination | {score}/100 | {finding} |
| Supply Chain Resilience | {score}/100 | {finding} |
| Inter-Agency Sharing | {score}/100 | {finding} |
| Capacity Dashboards | {score}/100 | {finding} |
| **Overall** | **{score}/100** | **{summary}** |

### Critical Findings

1. **{RES-001}: {title}**
   - Domain: {Inventory/Deployment/Logistics/Supply/Sharing/Dashboard}
   - Location: `{file:line}`
   - Impact: {what could go wrong during a crisis}
   - Recommendation: {specific improvement}

### Inventory Architecture
- Tracking method: {barcode/RFID/IoT/manual}
- Multi-location support: {yes/no}
- Expiration tracking: {present/absent}
- Reorder automation: {present/absent}

### Deployment Pipeline
- Authorization levels: {N} tiers
- Allocation algorithm: {manual/rule-based/optimizer}
- Real-time tracking: {GPS/checkpoint/manual/none}
- Partial fulfillment: {supported/unsupported}

### Logistics Capabilities
- Route optimization: {present/absent}
- Staging area management: {present/absent}
- Emergency procurement: {present/absent}
- Multi-modal transport: {present/absent}

### Inter-Agency Readiness
- Sharing agreements: {N} configured
- Cross-agency visibility: {real-time/request-based/none}
- Interoperability standard: {NIMS/EDXL/custom/none}

### Dashboard Assessment
- Refresh rate: {real-time/polling interval/manual}
- Mobile support: {yes/no}
- GIS mapping: {present/absent}
- Predictive analytics: {present/absent}

DO NOT:
- Recommend specific vendor products or proprietary resource management platforms.
- Make assumptions about resource quantities without evidence in the codebase.
- Evaluate field operations or response tactics -- this skill covers system/software analysis only.
- Ignore inter-agency sharing even if the system appears single-agency.
- Skip dashboard analysis -- situational awareness is critical during emergencies.
- Assess the adequacy of actual resource stockpiles -- focus on system capabilities.

NEXT STEPS:
- "Run `/crisis-triage` to analyze the dispatch system that triggers resource deployment."
- "Run `/volunteer-coordination` if volunteer resources are managed alongside professional assets."
- "Run `/load-test` to simulate surge demand on the deployment pipeline."
- "Run `/security-review` to audit access controls on resource and logistics data."


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /emergency-resource — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
