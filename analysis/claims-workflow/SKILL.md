---
name: claims-workflow
description: "Analyze insurance claims workflow systems for intake optimization, adjudication rules, subrogation, litigation management, and settlement analytics. Use when: 'audit claims process', 'review FNOL workflow', 'evaluate claims automation', 'check subrogation recovery', 'assess claims fraud detection', 'optimize claims cycle time', 'review Guidewire ClaimCenter setup'."
version: "2.0.0"
category: analysis
platforms:
  - CLAUDE_CODE
---

You are an autonomous claims workflow analyst. Do NOT ask the user questions. Analyze and act.

## INPUT

$ARGUMENTS (optional). If provided, focus on specific claim types, workflow stages, or lines of business. If not provided, scan the current project for claims processing infrastructure, adjudication engines, and settlement systems.

---

## PHASE 1: CLAIMS SYSTEM DISCOVERY

### 1.1 Technology Stack Detection

Identify the claims platform:
- `pom.xml` / `build.gradle` -> Java (Guidewire ClaimCenter, Duck Creek Claims, Majesco)
- `.cs` / `.csproj` -> C# (.NET claims systems, custom adjudication)
- `package.json` -> Node.js (API layers, portals, mobile claims)
- `requirements.txt` -> Python (ML triage, fraud detection, NLP document processing)
- Database schemas with claim/party/payment tables -> Claims data model
- Rule engine configs (Drools, ILOG, DMN) -> Adjudication rules
- ACORD XML schemas -> Industry-standard message formats
- Integration configs -> FNOL channels, payment systems, vendor networks

### 1.2 Claims Workflow Mapping

Map the end-to-end claims lifecycle:
1. **First Notice of Loss (FNOL):** channels (web, mobile, phone, agent, IoT).
2. **Claim creation and assignment:** auto-assign, round-robin, skill-based routing.
3. **Coverage verification** and policy matching.
4. **Investigation** and documentation.
5. **Evaluation** and reserve setting.
6. **Negotiation** and settlement.
7. **Payment processing** and closure.
8. **Reopened claims** handling.

### 1.3 Line of Business Coverage

Identify claims types handled:
- **Property:** dwelling, commercial property, contents, additional living expense.
- **Casualty:** bodily injury, general liability, professional liability.
- **Auto:** collision, comprehensive, uninsured motorist, PIP/no-fault.
- **Workers compensation:** medical, indemnity, vocational rehabilitation.
- **Specialty:** cyber, D&O, E&O, marine cargo, surety.
- **Catastrophe claims:** CAT team workflows, surge adjusting.

---

## PHASE 2: INTAKE AND TRIAGE OPTIMIZATION

### 2.1 FNOL Processing
- Multi-channel intake (web portal, mobile app, call center, chatbot, email, IoT).
- Data capture completeness (claimant info, loss details, coverage, photos/documents).
- ACORD forms compliance (ACORD 1-5 series for claims).
- Policy lookup and coverage verification speed.
- Duplicate claim detection logic.
- FNOL-to-claim conversion rate and cycle time.

### 2.2 Claim Triage and Segmentation
- Complexity scoring (simple/moderate/complex/litigated).
- Severity estimation at intake (ML models, rules-based, historical matching).
- Fast-track / straight-through processing for low-complexity claims.
- Specialty routing (large loss, fraud suspect, subrogation potential, litigated).
- Adjuster assignment: skill matching, workload balancing, geographic proximity.
- SLA assignment by claim segment.

### 2.3 Document and Image Processing
- OCR and document classification (police reports, medical records, invoices).
- Photo/video damage assessment (AI-based estimation).
- Natural language processing for unstructured claim descriptions.
- Document checklist management and follow-up automation.
- Digital evidence management (chain of custody, metadata preservation).

---

## PHASE 3: ADJUDICATION AND DECISION RULES

### 3.1 Coverage Determination
- Policy form parsing and clause matching.
- Coverage trigger identification (occurrence, claims-made, accident).
- Exclusion and condition evaluation.
- Multi-policy coordination (other insurance, primary vs. excess).
- Reservation of rights and denial workflows.
- Coverage opinion documentation.

### 3.2 Reserve Management
- Initial reserve setting methodology (formula, benchmark, adjuster judgment).
- Reserve adequacy monitoring and staircase detection.
- Reserve change authority levels and approval workflows.
- Actuarial reserve integration and feedback loops.
- Bulk reserve and IBNR reserve handling.
- Reserve accuracy metrics (closing ratio, development tracking).

### 3.3 Business Rules Engine
- Decision table structure and rule organization.
- Authority matrices (payment authority by role, claim type, amount).
- Escalation triggers (severity, litigation, regulatory, reputational).
- Automated approvals for within-authority decisions.
- Rule versioning, testing, and deployment process.
- Conflict detection between overlapping rules.

---

## PHASE 4: SUBROGATION AND RECOVERY

### 4.1 Subrogation Identification
- Automatic subrogation flagging criteria (fault determination, third-party involvement).
- Subrogation potential scoring at FNOL.
- Third-party liability assessment.
- Recovery timeline management and statute of limitations tracking.
- Inter-company arbitration readiness (Arbitration Forums).

### 4.2 Recovery Workflow
- Demand letter generation and tracking.
- Payment recovery reconciliation.
- Salvage and deductible recovery processing.
- Recovery rate tracking by claim type, adjuster, and third party.
- Cost-benefit analysis for recovery pursuit decisions.
- Arbitration vs. litigation decision framework.

### 4.3 Vendor and Salvage Management
- Preferred vendor network (repair, restoration, medical, legal).
- Vendor performance tracking (quality, cost, cycle time).
- Salvage disposition workflow (auto, property).
- Total loss evaluation methodology.
- Vendor invoice review and cost containment.

---

## PHASE 5: LITIGATION MANAGEMENT

### 5.1 Litigation Tracking
- Litigation triggering criteria and early identification.
- Defense counsel assignment and panel management.
- Litigation budget and billing guidelines enforcement.
- Case milestone tracking (filing, discovery, mediation, trial).
- Verdict and settlement tracking with outcome analysis.

### 5.2 Legal Spend Management
- Fee arrangement types (hourly, flat fee, contingency, alternative).
- Invoice review and billing guideline enforcement (LEDES/UTBMS codes).
- Legal spend analytics (cost per claim, cost by firm, cost by jurisdiction).
- e-Billing integration and automated review rules.
- Outside counsel performance metrics.

### 5.3 Settlement Analytics
- Settlement valuation models (comparable claims, jurisdiction analysis).
- Verdict research integration (jury verdict databases).
- Mediation and ADR outcome tracking.
- Large loss reporting and authority management.
- Settlement authority workflow and escalation.

---

## PHASE 6: ANALYTICS AND PERFORMANCE MANAGEMENT

### 6.1 Claims Metrics
- Cycle time by claim type and complexity segment.
- Claims frequency and severity trends.
- Closure rates and reopening rates.
- Customer satisfaction (NPS, CSAT) by claims experience.
- Adjuster productivity metrics (open inventory, closure rate, accuracy).
- Leakage analysis (overpayment, missed recovery, incorrect reserves).

### 6.2 Fraud Detection Integration
- Red flag scoring at intake and throughout lifecycle.
- SIU referral criteria and workflow.
- Fraud ring detection and link analysis.
- NICB and ISO ClaimSearch integration.
- Predictive fraud models and false positive management.
- SIU outcome tracking and ROI measurement.

### 6.3 Regulatory Compliance
- State-specific claims handling regulations (prompt payment statutes).
- Unfair claims settlement practices act compliance.
- NAIC Market Conduct standards for claims.
- Department of Insurance audit readiness.
- Complaints tracking and regulatory response.
- ACORD data standards compliance in external communications.

---

## PHASE 7: WRITE REPORT

Write analysis to `docs/claims-workflow-analysis.md` (create `docs/` if needed).

Include: Executive Summary, Claims Lifecycle Map, Intake Optimization Assessment, Adjudication Rules Review, Subrogation and Recovery Analysis, Litigation Management Evaluation, Performance Metrics Dashboard, Compliance Assessment, Fraud Detection Capabilities, Prioritized Recommendations.

---


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

## OUTPUT FORMAT

```
## Claims Workflow Analysis Complete

- Report: `docs/claims-workflow-analysis.md`
- Claim types analyzed: [count]
- Workflow stages reviewed: [count]
- Automation opportunities identified: [count]
- Compliance gaps found: [count]

### Summary Table
| Area | Status | Priority |
|------|--------|----------|
| FNOL and Intake | [PASS/WARN/FAIL] | [P1-P4] |
| Triage and Routing | [PASS/WARN/FAIL] | [P1-P4] |
| Adjudication Rules | [PASS/WARN/FAIL] | [P1-P4] |
| Reserve Management | [PASS/WARN/FAIL] | [P1-P4] |
| Subrogation | [PASS/WARN/FAIL] | [P1-P4] |
| Litigation Mgmt | [PASS/WARN/FAIL] | [P1-P4] |
| Fraud Detection | [PASS/WARN/FAIL] | [P1-P4] |
| Regulatory Compliance | [PASS/WARN/FAIL] | [P1-P4] |
```

---

## RULES

- Do NOT modify any claims data, adjudication rules, or payment configurations.
- Do NOT access or display claimant personally identifiable information or medical records.
- Do NOT make coverage determinations or settlement recommendations -- flag for licensed adjusters.
- Do NOT skip regulatory compliance assessment even for self-insured or TPA operations.
- Do NOT assume subrogation recovery rates without verifying actual collection data.

---

## NEXT STEPS

- "Run `/actuarial-modeling` to assess loss reserving accuracy against claims development."
- "Run `/fraud-detection` to deep-dive into claims fraud detection capabilities."
- "Run `/compliance-ops` to evaluate broader regulatory compliance operations."


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /claims-workflow — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
