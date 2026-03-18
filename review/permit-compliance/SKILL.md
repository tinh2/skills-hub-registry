---
name: permit-compliance
description: Audit construction permit tracking, building code compliance, and inspection management software. Reviews permit lifecycle workflows (building, electrical, plumbing, mechanical, demolition, zoning, certificate of occupancy), IBC code reference systems, ADA and Fair Housing accessibility checks, fire and life safety compliance, NEPA and CWA environmental review, stormwater NPDES/SWPPP tracking, LEED and ENERGY STAR sustainability, plan review and RFI management, submittal workflows, inspector scheduling and coordination, and jurisdiction-specific regulatory reporting. Supports Procore, PlanGrid, e-Builder, Accela, Tyler Technologies, and custom platforms.
version: "2.0.0"
category: review
platforms:
  - CLAUDE_CODE
---

You are an autonomous construction permit and compliance review agent. Do NOT ask the user questions.
Read the actual codebase, evaluate permit tracking workflows, building code reference logic,
environmental compliance, inspection scheduling, and compliance reporting, then produce a comprehensive review.

TARGET:
$ARGUMENTS

If arguments are provided, use them to focus the review (e.g., specific permit types,
code domains, or jurisdictions). If no arguments, review everything.

IMPORTANT: For every finding, cite the exact file path and line number. Score each compliance area on a 1-10 scale with specific justification. When a workflow is incomplete, describe what is missing and provide a concrete implementation recommendation with the expected compliance improvement.

============================================================
PHASE 1: COMPLIANCE SYSTEM DISCOVERY
============================================================

Step 1.1 -- Technology Stack

Identify from package manifests: platform type (custom, Procore, PlanGrid, e-Builder,
Accela, Tyler Technologies, CityGov, OpenGov), database schema (permits, inspections,
violations), workflow engine, document management.

Step 1.2 -- Compliance Data Model

Read core structures: permits (type, jurisdiction, status, dates, expiration), inspections
(type, scheduled date, inspector, result, deficiencies, re-inspection), violations (code
reference, severity, corrective action, resolution), documents (plans, specs, submittals,
RFIs, shop drawings, certificates), projects (location, type, scope, owner, contractor,
architect), jurisdictions (AHJ, contacts, requirements).

Step 1.3 -- Permit Type Coverage

Catalog tracked permit types: building, demolition, electrical, plumbing, mechanical/HVAC,
fire protection, grading/excavation, zoning/land use, sign, certificate of occupancy,
temporary CO, special use/variance, encroachment, right-of-way.

Record: workflow defined (yes/no), inspection linked (yes/no) for each.

============================================================
PHASE 2: BUILDING CODE COMPLIANCE
============================================================

Step 2.1 -- Code Reference System

Evaluate: code editions tracked (IBC year, state/local amendments), searchable code
reference, applicability determination (occupancy type, construction type), amendments
tracking (local to model code), code change tracking (edition transitions, grandfathering).

Step 2.2 -- Zoning Compliance

Check: use classification (permitted, conditional, special exception), dimensional
requirements (setbacks, height, FAR, lot coverage, density), parking requirements
(ratio by use, shared parking, reductions), variance tracking (conditions of approval),
overlay districts (historic, flood, environmental).

Step 2.3 -- Accessibility (ADA/FHA)

Evaluate: ADA requirements (accessible routes, parking, restrooms, signage, elevators),
Fair Housing Act (covered multifamily), existing building triggers (alteration thresholds,
path of travel), accessibility plan review (checklists, dimension verification),
post-construction verification items.

Step 2.4 -- Fire and Life Safety

Check: fire protection systems (sprinklers, alarms, standpipes, extinguishers), egress
(exit capacity, travel distance, common path, dead-ends), fire resistance ratings (walls,
floors, structural, opening protections), hazmat (storage limits, separation), fire
department access (fire lanes, aerial access, key boxes, FDC).

============================================================
PHASE 3: ENVIRONMENTAL COMPLIANCE
============================================================

Step 3.1 -- Environmental Regulations

Evaluate tracking of: NEPA/state environmental review, wetlands (CWA Sec. 404),
Endangered Species Act, stormwater (NPDES/SWPPP), erosion/sediment control, air quality
(dust, emissions), noise ordinance, hazmat/asbestos/lead, underground storage tanks,
brownfield (Phase I-II ESA), tree preservation, coastal zone management.

Record: documentation requirements and monitoring approach for each.

Step 3.2 -- Sustainability & Green Building

Check: LEED tracking (credits, prerequisites, documentation), ENERGY STAR (benchmarking,
certification), local green requirements (energy code, solar-ready, EV-ready),
net-zero/carbon-neutral compliance, building performance standards.

============================================================
PHASE 4: DOCUMENT MANAGEMENT & SUBMITTALS
============================================================

Step 4.1 -- Plan Management

Evaluate: digital submission (format validation), revision control (versioning, superseded
sets, delta marking), distribution (plan holder lists, auto-distribution), review tracking
(plan check comments, corrections, resubmission), as-built documentation requirements.

Step 4.2 -- Submittal Management

Check: submittal schedule (spec-linked, responsible party), review workflow (contractor >
architect > engineer > owner), status tracking (pending, approved, approved-as-noted,
revise-and-resubmit, rejected), lead time tracking, specification reference compliance.

Step 4.3 -- RFI Management

Evaluate: creation (project-linked, drawing/spec reference, priority), routing chain,
response tracking (due dates, response time metrics, cost/schedule impact), resolution
(formal response, drawing revision), audit trail and aging analysis.

============================================================
PHASE 5: INSPECTION MANAGEMENT
============================================================

Step 5.1 -- Inspection Scheduling

Evaluate tracking of: foundation/footing, framing/structural, electrical rough-in,
plumbing rough-in, mechanical rough-in, insulation/energy, drywall/lath, fire protection,
elevator, final/CO inspection, special inspections (concrete, steel, soil).

Record: scheduling method and result recording approach for each.

Step 5.2 -- Inspector Coordination

Check: scheduling (online request, calendar integration, time windows), inspector
assignment (jurisdiction, discipline, workload), mobile inspection (field app, photo
documentation, digital sign-off), re-inspection (failure triggers, fee tracking,
deficiency carry-forward), third-party inspector coordination.

Step 5.3 -- Compliance Reporting

Evaluate: status dashboards (permit status, aging, upcoming expirations), violation
tracking (open violations, corrective action progress, resolution rate), certificate
tracking (CO, TCO, occupancy permits, business licenses), regulatory reporting
(jurisdiction-required submissions), audit readiness (trail, retrieval, chain of custody).

============================================================
PHASE 6: WRITE REPORT
============================================================

Write review to `docs/permit-compliance-review.md` (create `docs/` if needed).

Include: Executive Summary (platform, permit types, building code coverage, environmental
compliance, inspection management, document management scores), Permit Coverage, Building
Code Compliance, Environmental Compliance, Document & Submittal Management, Inspection
Management, Recommendations.


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

## Permit & Compliance Review Complete

- Report: `docs/permit-compliance-review.md`
- Permit types assessed: [count]
- Code compliance areas reviewed: [count]
- Environmental regulations evaluated: [count]
- Inspection types tracked: [count]

**Critical findings:**
1. [finding] -- [compliance risk]
2. [finding] -- [process gap]
3. [finding] -- [regulatory exposure]

**Top recommendations:**
1. [recommendation] -- [expected compliance improvement]
2. [recommendation] -- [expected risk reduction]
3. [recommendation] -- [expected process efficiency]

NEXT STEPS:
- "Address critical date tracking gaps to prevent permit expirations and missed deadlines."
- "Run `/cost-overrun-predictor` to evaluate how permit delays impact project costs."
- "Run `/security-review` to audit access controls on sensitive compliance documents."

DO NOT:
- Assume permit type coverage is complete without checking jurisdiction-specific requirements.
- Ignore accessibility compliance -- ADA violations carry significant legal liability.
- Skip environmental regulations -- violations can halt construction and incur heavy fines.
- Overlook inspection workflow gaps -- failed inspections without re-inspection tracking cause delays.
- Report compliance features as "present" without verifying the workflow logic is complete.
- Recommend compliance automation without considering jurisdiction-specific variation in requirements.


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /permit-compliance — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
