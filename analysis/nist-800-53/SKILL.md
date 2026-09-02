---
name: nist-800-53
description: "Map a cloud system against NIST SP 800-53 Rev. 5 + FedRAMP baselines to produce the documentation an authorization needs — System Security Plan (SSP), Control Implementation Summary (CIS), Plan of Action and Milestones (POA&M), Continuous Monitoring (ConMon) Plan.."
version: "1.0.1"
category: analysis
platforms:
  - CLAUDE_CODE
---

# NIST 800-53 / FedRAMP Authorization Engine

You map a cloud system to NIST SP 800-53 Rev. 5 controls and produce the documentation an authorization needs. FedRAMP demands SSP documentation often over 300 pages, plus CIS, POA&M, and ConMon plan — and 3PAO + PMO will reject anything boilerplate.

**2026 landscape (CR26)**:

- **Certification Classes** replace Impact Levels: **A** (Pilot/Ready), **B** (Li-SaaS/Low), **C** (Moderate), **D** (High).
- **JAB authorization model is gone** — Agency authorization is the path.
- **Monthly ConMon required across all classes** — vulnerability scans, POA&M updates, inventory changes, executive summary.
- **Remediation timelines enforced**: 30 days (high), 90 days (moderate), 180 days (low).

============================================================
=== PRE-FLIGHT ===
============================================================

- [ ] **System boundary defined**: what's in scope? Components, data flows, interconnections, customer data, customer responsibility.
- [ ] **Certification Class target**: A / B / C / D — drives # of controls (~325 for C, ~421 for D).
- [ ] **Underlying CSP**: AWS GovCloud, Azure Government, GCC High, on-prem. Drives inheritable controls (the CSP carries some PE/SC/SI/AC controls).
- [ ] **3PAO selected**: required for assessment. Pick from FedRAMP marketplace.
- [ ] **Agency sponsor**: required since JAB is gone. Agency PMO sponsors authorization.
- [ ] **Existing posture**: SOC 2 Type II completed? StateRAMP? ISO 27001? Substantial uplift if any.

Recovery:

- If system boundary is ambiguous, force the user to draft a system architecture diagram + data flow diagram before continuing. Without boundary, controls don't have scope.
- For "FedRAMP Tailored" / Li-SaaS path: scope is narrower (Class A or B) — 130-160 controls.

============================================================
=== PHASE 1: BOUNDARY + INVENTORY ===
============================================================

Generate `system_boundary.md` with:

1. **Authorization Boundary Diagram (ABD)** — every component, interface, external connection.
2. **Data Flow Diagram (DFD)** — how customer data enters, processes, stores, leaves.
3. **Inventory** — hosts, containers, databases, queues, secrets stores, identity providers. Linked to a CMDB (Datadog, AWS Config, ServiceNow).
4. **Interconnections** — every external API, every shared boundary with another system. ICA (Interconnection Security Agreement) required for shared boundaries.

VALIDATION: Boundary diagram + DFD + inventory all consistent — every box in the ABD appears in the DFD and inventory.

============================================================
=== PHASE 2: CONTROL APPLICABILITY MATRIX ===
============================================================

For your Certification Class, enumerate the applicable controls + enhancements from 800-53 Rev. 5:

| Family                               | Controls Class C count | Sample controls                                         |
| ------------------------------------ | ---------------------- | ------------------------------------------------------- |
| AC (Access Control)                  | 25+                    | AC-2, AC-3, AC-4, AC-5, AC-6, AC-7, AC-11, AC-17, AC-22 |
| AT (Awareness & Training)            | 4                      | AT-1, AT-2, AT-3, AT-4                                  |
| AU (Audit & Accountability)          | 14+                    | AU-2, AU-3, AU-6, AU-9, AU-12                           |
| CA (Assessment, Authorization)       | 9                      | CA-2, CA-3, CA-5, CA-7, CA-9                            |
| CM (Configuration Management)        | 12                     | CM-2, CM-3, CM-6, CM-7, CM-8, CM-10                     |
| CP (Contingency Planning)            | 13                     | CP-2, CP-3, CP-4, CP-9, CP-10                           |
| IA (Identification & Authentication) | 11                     | IA-2 (incl. MFA enhancements), IA-5, IA-8               |
| IR (Incident Response)               | 10                     | IR-4, IR-5, IR-6, IR-7, IR-8                            |
| MA (Maintenance)                     | 6                      | MA-2, MA-3, MA-4                                        |
| MP (Media Protection)                | 8                      | MP-2, MP-4, MP-5, MP-6                                  |
| PE (Physical & Environmental)        | 17                     | PE-2, PE-6, PE-12, PE-14 (usually inherited from CSP)   |
| PL (Planning)                        | 11                     | PL-2, PL-4, PL-8                                        |
| PS (Personnel Security)              | 9                      | PS-3, PS-4, PS-7                                        |
| PT (PII Processing & Transparency)   | new in Rev 5           | PT-1, PT-2, PT-3                                        |
| RA (Risk Assessment)                 | 10                     | RA-3, RA-5, RA-9                                        |
| SA (System & Services Acquisition)   | 22                     | SA-4, SA-8, SA-11, SA-22                                |
| SC (System & Communications)         | 30+                    | SC-7, SC-8, SC-12, SC-13, SC-17, SC-23                  |
| SI (System & Information Integrity)  | 17                     | SI-2, SI-3, SI-4, SI-7, SI-10                           |
| SR (Supply Chain Risk Mgmt)          | new in Rev 5           | SR-3, SR-5, SR-6, SR-11                                 |
| PM (Program Management)              | enterprise-level       | PM-1, PM-2, PM-7                                        |

Mark each control as:

- **Customer Responsibility** (you implement)
- **Provider Responsibility** (CSP — inherited; reference CSP's FedRAMP package)
- **Shared** (both — split the implementation)
- **Hybrid** (system & customer)

VALIDATION: Every applicable control assigned an owner.

============================================================
=== PHASE 3: IMPLEMENTATION STATEMENTS (SSP CORE) ===
============================================================

For each Customer Responsibility / Shared / Hybrid control, draft an implementation statement. FedRAMP rejects boilerplate — be specific.

Template per control:

```markdown
### AC-2: Account Management

#### Implementation Status

- [x] Implemented
- [ ] Partially Implemented
- [ ] Planned
- [ ] Alternative Implementation
- [ ] Not Applicable

#### Implementation Description

{Tenant accounts are managed via {Identity Provider, e.g., AWS IAM Identity Center / Okta}
with the following lifecycle:

a. Account types: ...
b. Provisioning: SCIM-based push from HRIS (Workday) on hire.
c. Authorization workflow: tickets in JIRA Service Management with approval from manager + security.
d. Deprovisioning: automated on termination event from HRIS within {N} minutes; manual review at {cadence}.
e. Quarterly access review: documented in Confluence; failed reviews opened as POA&M items.

Evidence:

- Screenshot of Identity Provider console
- Sample provisioning ticket
- Sample quarterly review report
- Automated test in security CI: `tests/AC-2.test.ts`}

#### Customer Responsibility

{If shared/hybrid — explicit statement of what the customer agency must do.}

#### Control Enhancements Implemented

- AC-2(1) Automated System Account Management: ...
- AC-2(2) Removal of Temporary / Emergency Accounts: ...
- ...
```

Generate one per applicable control. Output `ssp/controls/{family}-{number}.md`.

VALIDATION: Each implementation statement references SPECIFIC tools, processes, evidence locations. No "documented elsewhere" placeholders.

============================================================
=== PHASE 4: POA&M GENERATION ===
============================================================

Plan of Action & Milestones tracks every control NOT fully implemented + every finding from scans / assessments.

Schema:

```json
{
  "poam_id": "POAM-2026-0042",
  "weakness": "AC-2(11): Account Use Conditions — circumstances and usage restrictions not documented for service accounts.",
  "control": "AC-2(11)",
  "severity": "Moderate",
  "discovered_date": "2026-05-01",
  "discovered_by": "Internal review",
  "current_status": "Ongoing",
  "scheduled_completion": "2026-08-01",
  "remediation_plan": "Document service-account usage conditions in Confluence runbook; automate enforcement via IAM policy.",
  "milestones": [
    { "date": "2026-06-01", "milestone": "Runbook drafted, peer reviewed" },
    { "date": "2026-07-01", "milestone": "IAM policy templates updated" },
    {
      "date": "2026-08-01",
      "milestone": "All service accounts compliant; closing POA&M"
    }
  ],
  "resources_required": "1 FTE-week security engineering",
  "vendor_dependency": false
}
```

Timelines (enforced per FedRAMP):

- High severity: 30 days
- Moderate: 90 days
- Low: 180 days

VALIDATION: Every POA&M item has milestones + deadline + owner.

============================================================
=== PHASE 5: CONTINUOUS MONITORING (CONMON) PLAN ===
============================================================

Monthly ConMon deliverables required across all classes:

1. **Vulnerability Scans** — authenticated scans of all in-boundary hosts (Tenable, Qualys, Nessus). Web app scans (OWASP ZAP, Burp Pro). Container scans (Snyk, Aqua). All scan results uploaded to FedRAMP repository.
2. **POA&M Updates** — status changes, new findings, closures.
3. **Inventory Changes** — added/removed/changed components.
4. **Configuration Drift** — compare current state to baselines (CIS, DISA STIGs).
5. **Executive Summary** — 2-3 page agency-facing summary.

Generate `conmon_plan.md` with monthly cadence, tooling, evidence retention rules (1-year minimum per FedRAMP).

Plus **Annual Assessment** by 3PAO (Class C/D), **Significant Change** notifications.

VALIDATION: Plan covers all 5 monthly artifacts + annual assessment cadence.

============================================================
=== PHASE 6: 3PAO READINESS ===
============================================================

Pre-assessment checklist before 3PAO engagement:

- [ ] SSP complete (Phase 3)
- [ ] CIS (Control Implementation Summary) — 1-line per control of who owns what
- [ ] POA&M current
- [ ] Recent vulnerability scans (within 30 days)
- [ ] ConMon plan documented
- [ ] Incident Response Plan tested (tabletop exercise within 12 months)
- [ ] Contingency Plan tested (DR exercise within 12 months)
- [ ] Penetration test scheduled with 3PAO (required for Class C/D)
- [ ] Privacy Impact Assessment (if PII processed)
- [ ] Supply Chain Risk Management plan (SR family)
- [ ] FIPS 140-3 validated crypto modules in use (where required)

VALIDATION: All checklist items have evidence pointers.

============================================================
=== PHASE 7: PACKAGE & SUBMISSION ===
============================================================

```
fedramp-package/
├── README.md
├── ssp/
│   ├── core.md                   # exec summary + boundary
│   ├── controls/                 # one MD per control
│   └── attachments/
│       ├── ABD.png
│       ├── DFD.png
│       ├── ICA-{partner}.pdf
│       └── ...
├── cis/
│   └── control_implementation_summary.xlsx
├── poam/
│   └── poam_2026Q2.xlsx
├── conmon/
│   └── conmon_plan.md
├── policies/                     # 20+ org policies (AC-1, AT-1, AU-1, etc.)
└── evidence/                     # screenshots, scan results, test outputs
    └── 2026-05/
```

Submit to FedRAMP via OMB Max + agency sponsor.

VALIDATION: Package structure matches FedRAMP template. All required attachments present.

============================================================
=== SELF-REVIEW ===
============================================================

- **Complete**: Boundary + control matrix + SSP + POA&M + ConMon + 3PAO checklist?
- **Robust**: Inheritance correctly mapped to underlying CSP? Class-appropriate control set?
- **Clean**: Each implementation statement references specific tools / evidence (no boilerplate)?
- **FedRAMP-credible**: Would a 3PAO or PMO reviewer accept the SSP as substantive?

Common gap: claiming "implemented" without evidence pointer. Every control needs traceable evidence.

============================================================
=== LEARNINGS CAPTURE ===
============================================================

`~/.claude/skills/nist-800-53/LEARNINGS.md`.

============================================================
=== STRICT RULES ===
============================================================

- Never use boilerplate implementation statements. 3PAO + PMO will reject.
- Never claim an inherited control without referencing the CSP's authorization package + Customer Responsibility Matrix.
- Never miss a ConMon month. Lapses jeopardize authorization.
- Never miss POA&M remediation deadlines (30/90/180 days). Late POA&Ms trigger agency conditional authorization or revocation.
- Always reference CR26 Certification Classes (A/B/C/D), not legacy Low/Mod/High. The labels changed in 2026.
- Always confirm FIPS 140-3 (not 140-2) crypto module validation — 140-2 sunset 2026.
