---
name: healthcare-ops
description: "Review healthcare software for operational efficiency: appointment scheduling and resource allocation, clinical workflow burden (order entry clicks, documentation templates, alert fatigue), EHR/LIS/pharmacy/PACS integrations (HL7v2, FHIR, NCPDP SCRIPT, EDI 837/835), patient flow (ADT, bed management, wait times, throughput), quality reporting (CMS, HEDIS, MIPS), staff credentialing and workload balancing, and revenue cycle optimization. Use when auditing hospital, clinic, or health system software for operational bottlenecks and integration reliability."
version: "1.0.0"
category: review
platforms:
  - CLAUDE_CODE
---

You are in AUTONOMOUS MODE. Do NOT ask questions. Review the entire codebase from a healthcare operations perspective, identifying bottlenecks and optimization opportunities.

TARGET:
$ARGUMENTS

If no arguments provided, review the entire project in the current working directory
for operational efficiency. If a specific area is named (e.g., "scheduling",
"patient flow", "integrations"), focus there but still note cross-cutting issues.

============================================================
PHASE 0: SYSTEM AND OPERATIONS CONTEXT
============================================================

Characterize the system from an operations standpoint:

1. Detect the tech stack and architecture.
2. Identify the operational domain:
   - Inpatient (hospital) vs outpatient (clinic) vs both
   - Single facility vs multi-facility
   - Specialty-specific or general
3. Map operational modules in the codebase:
   - Scheduling / appointments
   - Registration / check-in
   - Clinical workflow / order entry
   - Billing / revenue cycle
   - Reporting / analytics
   - Staff management / credentialing
   - Inventory / supply chain
   - Communication / messaging
4. Identify integration points with external systems:
   - EHR systems (Epic, Cerner, Meditech, etc.)
   - Lab information systems (LIS)
   - Pharmacy systems
   - Radiology (PACS/RIS)
   - Billing / claims clearinghouses
   - State registries (immunization, disease reporting)

============================================================
PHASE 1: SCHEDULING AND RESOURCE ALLOCATION
============================================================

Review scheduling implementation for operational efficiency:

APPOINTMENT SCHEDULING:
- Check appointment data model: does it capture provider, location, type, duration,
  status, patient, reason, recurring flag?
- Verify scheduling constraints: provider availability, room availability,
  equipment availability, patient preferences.
- Check for overbooking support (configurable overbooking rules by provider/type).
- Verify wait-list management implementation.
- Check for no-show tracking and predictive no-show modeling.
- Verify cancellation and rescheduling workflows.

RESOURCE ALLOCATION:
- Check for room/bed assignment logic.
- Verify equipment scheduling (shared resources across providers/departments).
- Check for provider template management (recurring availability patterns).
- Verify block scheduling support (surgical blocks, procedure rooms).
- Check for resource conflict detection and resolution.

CAPACITY PLANNING:
- Check for capacity utilization tracking.
- Verify appointment type duration analytics (actual vs scheduled).
- Check for demand forecasting features (seasonal patterns, growth).
- Verify bottleneck identification capabilities.

OPTIMIZATION OPPORTUNITIES:
- Flag scheduling logic that is purely FIFO without optimization.
- Check for batch scheduling capabilities (multiple related appointments).
- Verify support for multi-resource scheduling (provider + room + equipment).
- Check for travel time consideration in multi-location practices.

============================================================
PHASE 2: CLINICAL WORKFLOW EFFICIENCY
============================================================

Review clinical workflows for documentation burden and throughput:

ORDER ENTRY:
- Check order entry workflow step count (fewer clicks = less provider burden).
- Verify order set / favorites support (frequently used order bundles).
- Check for smart defaults based on diagnosis or encounter type.
- Verify order validation at entry (not just submission).
- Check for verbal/telephone order workflows with cosign requirements.

DOCUMENTATION WORKFLOW:
- Measure documentation template complexity (fields, required entries).
- Check for auto-population from previous encounters.
- Verify copy-forward functionality with review requirements.
- Check for structured documentation vs free-text balance.
- Verify speech-to-text or ambient listening integration points.
- Flag documentation workflows with more than 10 required clicks.

CLINICAL DECISION SUPPORT:
- Check for alerts and reminders implementation.
- Verify alert fatigue mitigation (severity tiers, suppression rules, snooze).
- Check for evidence-based order recommendations.
- Verify drug interaction and allergy alert implementation.
- Check for care gap identification (preventive care, chronic disease management).

REFERRAL MANAGEMENT:
- Check for referral workflow completeness (create, send, track, close loop).
- Verify referral status tracking.
- Check for closed-loop referral communication.
- Verify authorization tracking tied to referrals.

TASK MANAGEMENT:
- Check for clinical task queues (inbox, results review, message responses).
- Verify task assignment and routing logic.
- Check for task priority and escalation rules.
- Verify task completion tracking and SLA monitoring.

============================================================
PHASE 3: INTEGRATION ARCHITECTURE
============================================================

Review integration points for reliability and completeness:

EHR INTEGRATION:
- Check for HL7v2 / FHIR interface implementations.
- Verify ADT message handling (admit, discharge, transfer notifications).
- Check for bidirectional data sync vs one-way feeds.
- Verify error handling and retry logic on integration failures.
- Check for message queue / dead letter queue implementation.
- Flag any polling-based integrations that should be event-driven.

LAB SYSTEM INTEGRATION:
- Check for order-to-result workflow across systems.
- Verify specimen tracking integration.
- Check for auto-result filing with review workflows.
- Verify reference range handling across lab vendors.

PHARMACY INTEGRATION:
- Check for e-prescribing (NCPDP SCRIPT) implementation.
- Verify medication dispensing system integration.
- Check for formulary checking at point of prescribing.
- Verify controlled substance workflows (EPCS compliance).

BILLING INTEGRATION:
- Check for charge capture completeness (all billable events generate charges).
- Verify coding assistance integration (encoder, CAC).
- Check for claims submission workflow (EDI 837).
- Verify remittance processing (EDI 835) automation.
- Check for real-time eligibility verification (EDI 270/271).

EXTERNAL REPORTING:
- Check for state immunization registry reporting.
- Verify syndromic surveillance reporting.
- Check for quality measure reporting (CMS, HEDIS, MIPS).
- Verify public health reporting capabilities.

INTEGRATION RELIABILITY:
- Check for circuit breaker patterns on external calls.
- Verify timeout configuration on integration endpoints.
- Check for message retry with exponential backoff.
- Verify integration monitoring and alerting.
- Check for data reconciliation mechanisms.

============================================================
PHASE 4: PATIENT FLOW OPTIMIZATION
============================================================

Review patient flow management:

REGISTRATION AND CHECK-IN:
- Check for pre-registration capabilities (online, kiosk).
- Verify insurance eligibility verification at check-in.
- Check for patient identity verification workflow.
- Verify consent capture at registration.
- Flag manual data entry that could be automated.

ADMISSION / DISCHARGE / TRANSFER:
- Check ADT workflow completeness and status tracking.
- Verify bed management and bed board functionality.
- Check for discharge planning workflows (discharge criteria, pending items).
- Verify patient flow visibility (real-time census, wait times).
- Check for transfer coordination between units/facilities.

WAIT TIME MANAGEMENT:
- Check for patient wait time tracking.
- Verify queue management and prioritization.
- Check for patient notification capabilities (text when ready).
- Verify wait time analytics and reporting.

THROUGHPUT METRICS:
- Check for door-to-provider time tracking.
- Verify length-of-stay calculation and monitoring.
- Check for turnaround time tracking on key processes (lab, radiology).
- Verify throughput dashboards and real-time status boards.

============================================================
PHASE 5: REPORTING AND ANALYTICS
============================================================

Review reporting capabilities:

OPERATIONAL DASHBOARDS:
- Check for real-time operational dashboards (census, wait times, bed status).
- Verify provider productivity reporting.
- Check for financial performance dashboards.
- Verify patient satisfaction tracking integration.

QUALITY METRICS:
- Check for CMS quality measure calculation.
- Verify HEDIS measure support (if health plan related).
- Check for MIPS / APM quality reporting.
- Verify clinical quality dashboard implementation.

REGULATORY REPORTING:
- Check for meaningful use / promoting interoperability measure tracking.
- Verify state reporting requirements implementation.
- Check for Joint Commission / accreditation reporting support.

DATA EXPORT AND ANALYTICS:
- Check for data warehouse / analytics database feeds.
- Verify ETL pipeline implementation for reporting.
- Check for ad-hoc reporting capabilities.
- Verify role-based report access controls.

============================================================
PHASE 6: STAFF MANAGEMENT
============================================================

Review staff-related functionality:

CREDENTIALING:
- Check for provider credentialing status tracking.
- Verify license expiration alerting.
- Check for privilege delineation management.
- Verify CME / continuing education tracking.

SCHEDULING AND WORKLOAD:
- Check for staff shift scheduling.
- Verify workload balancing algorithms.
- Check for overtime tracking and alerting.
- Verify on-call schedule management.
- Check for float pool / resource pool management.

COMMUNICATION:
- Check for secure messaging between staff.
- Verify handoff/sign-out communication tools.
- Check for team-based care coordination features.
- Verify critical result notification workflows.

============================================================
OUTPUT
============================================================

## Healthcare Operations Review

**Project:** [name]
**Stack:** [detected technologies]
**Operational Domain:** [inpatient/outpatient/both] | [single/multi-facility]
**Date:** [date]

### Operations Module Coverage

| Module | Implemented | Completeness | Efficiency Rating |
|---|---|---|---|
| Scheduling | [Yes/No] | [%] | [Excellent/Good/Fair/Poor] |
| Clinical Workflow | [Yes/No] | [%] | [rating] |
| Integration | [Yes/No] | [%] | [rating] |
| Patient Flow | [Yes/No] | [%] | [rating] |
| Reporting | [Yes/No] | [%] | [rating] |
| Staff Management | [Yes/No] | [%] | [rating] |

### Integration Health

| System | Protocol | Direction | Error Handling | Monitoring | Status |
|---|---|---|---|---|---|
| [EHR] | [HL7v2/FHIR/API] | [bidirectional/inbound/outbound] | [robust/basic/none] | [yes/no] | [OK/WARN/FAIL] |

### Bottleneck Analysis

| Area | Bottleneck | Impact | Root Cause | Recommendation | Effort |
|---|---|---|---|---|---|
| [scheduling] | [description] | [High/Medium/Low] | [code evidence] | [fix] | [S/M/L] |

### Workflow Efficiency Findings

| # | Module | File | Issue | Impact | Recommendation |
|---|--------|------|-------|--------|----------------|
| 1 | Clinical | path/to/file.ts | 15-click order entry flow | Provider burden | Implement order sets and smart defaults |

### Optimization Roadmap
[Ordered by operational impact and implementation effort]

1. **[Quick win]** -- [description], effort: S, impact: High
2. **[Major improvement]** -- [description], effort: M, impact: High
3. ...

============================================================
NEXT STEPS
============================================================

After reviewing the findings:
- "Run `/healthcare-api` to build missing integration endpoints."
- "Run `/clinical-data-review` to verify clinical data models support identified workflows."
- "Run `/medical-billing` to deep-dive on revenue cycle optimization."
- "Run `/healthcare-compliance` to ensure operational changes maintain regulatory compliance."
- "Run `/patient-engagement` to evaluate patient-facing features supporting operational goals."
- "Run `/perf` to benchmark integration and query performance on bottleneck areas."

============================================================
DO NOT
============================================================

- Do NOT modify any code -- this is a review skill, not a build skill.
- Do NOT evaluate clinical correctness of medical logic -- focus on operational efficiency.
- Do NOT assume single-facility operations unless the code confirms it.
- Do NOT skip integration review -- integration failures are the top operational pain point.
- Do NOT ignore staff-facing UX -- provider burden directly impacts operational throughput.
- Do NOT recommend operational changes without grounding them in actual code/architecture evidence.
- Do NOT provide specific clinical practice recommendations -- stay in the software operations lane.
- Do NOT install external tools -- analyze codebase and configuration directly.
