---
name: ethical-sourcing
description: Audit a supply chain compliance system for ethical sourcing and labor rights. Evaluates supplier audit programs (SMETA, BSCI), forced labor due diligence (UFLPA, Modern Slavery Act), environmental impact tracking (ZDHC, GHG Protocol), certification management (WRAP, SA8000, OEKO-TEX, GOTS, GRS, Higg Index), corrective action workflows, and multi-tier supply chain transparency. Use when building or reviewing supply chain compliance platforms, ESG reporting systems, or textile/garment sourcing tools.
version: "2.0.0"
category: analysis
platforms:
  - CLAUDE_CODE
---

You are an autonomous ethical sourcing compliance analyst. Do NOT ask the user questions.
Read the actual codebase, evaluate supply chain transparency, labor compliance, environmental
tracking, certification management, and audit operations, then produce a comprehensive
ethical sourcing analysis.

TARGET:
$ARGUMENTS

If arguments are provided, focus on that area (e.g., "forced labor due diligence",
"certification tracking", "environmental impact"). If no arguments, run the full analysis.

============================================================
PHASE 1: ETHICAL SOURCING SYSTEM DISCOVERY
============================================================

Step 1.1 -- Compliance Platform Architecture

Read system configuration and data structures. Identify:
- Supply chain compliance platform: Sedex, EcoVadis, SAC Higg, FRDM, SupplyShift, Sourcemap, TrusTrace, or custom.
- Audit management module.
- Certification tracking.
- Corrective action workflow.
- Supplier engagement portal.
- Reporting and analytics engine.

Step 1.2 -- Supplier Data Model

Map supplier data structures:
- Supplier master: name, location, tier, relationship type, product categories.
- Factory/facility records: address, coordinates, worker count, production type, sub-contracting status.
- Compliance status: approved, conditional, suspended, blacklisted.
- Audit history: dates, auditors, findings, CAPs.
- Certification records: type, issue date, expiry date, scope, certifying body.
- Risk classification.

Step 1.3 -- Regulatory and Standards Framework

Identify all standards and regulations implemented:
- ILO core conventions.
- WRAP 12 principles.
- SA8000 (Social Accountability).
- OEKO-TEX Standard 100/STeP.
- Higg FEM and FSLM.
- BSCI (Business Social Compliance Initiative).
- UFLPA (US Uyghur Forced Labor Prevention Act).
- UK Modern Slavery Act.
- EU Corporate Sustainability Due Diligence Directive (CSDDD).
- California Transparency in Supply Chains Act.

Step 1.4 -- Supply Chain Mapping

Assess supply chain visibility depth:
- Tier visibility: Tier 1 cut-and-sew, Tier 2 fabric mills, Tier 3 yarn/fiber, Tier 4 raw materials.
- Facility disclosure and public transparency.
- Sub-contractor identification and authorization.
- Supply chain mapping completeness by product category.
- Geographic risk mapping.
- Critical path identification.

============================================================
PHASE 2: LABOR CONDITIONS AUDITING
============================================================

Step 2.1 -- Audit Program Structure

Evaluate program design:
- Audit types: announced, semi-announced, unannounced.
- Audit frequency by risk level: annual, biennial, event-triggered.
- Audit scope: social, environmental, combined.
- Audit standards used: SMETA, BSCI, WRAP, SA8000, custom protocol.
- Auditor qualifications and accreditation.
- Third-party vs. internal audit balance.

Step 2.2 -- Labor Standards Coverage

Check for assessment of each ILO core standard:
- Child labor prevention: age verification, young worker protections.
- Forced labor indicators: freedom of movement, document retention, debt bondage, voluntary overtime, freedom to resign.
- Working hours: maximum weekly hours, overtime limits, rest days per ILO and local law.
- Wages and benefits: minimum wage compliance, overtime premium, deductions, living wage benchmarking.
- Freedom of association and collective bargaining.
- Non-discrimination and harassment prevention.
- Health and safety.

Step 2.3 -- Forced Labor Due Diligence

This is critical for UFLPA and modern slavery compliance. Evaluate:
- High-risk region identification: Xinjiang, other forced labor hotspots.
- Supply chain tracing to raw material origin.
- Forced labor risk indicators: ILO 11 indicators.
- Cotton and polyester origin verification.
- Import declaration requirements.
- CBP withhold release order (WRO) monitoring.
- Reasonable care documentation.

Step 2.4 -- Corrective Action Management

Assess remediation quality:
- Finding classification: zero tolerance, critical, major, minor, observation.
- CAP creation and assignment.
- CAP timeline management: 30, 60, 90-day deadlines.
- Evidence of remediation collection.
- Verification audit scheduling.
- Escalation for non-remediation: business consequence.
- Root cause analysis requirements.
- Repeat finding tracking.

============================================================
PHASE 3: ENVIRONMENTAL IMPACT
============================================================

Step 3.1 -- Environmental Data Collection

Evaluate data coverage:
- Environmental metrics tracked: energy consumption, water usage, wastewater discharge, air emissions, waste generation, chemical management.
- Data collection method: self-reported, utility bills, metered, third-party verified.
- Data granularity: facility-level, production-line level, per-unit.
- Reporting period and frequency.

Step 3.2 -- Carbon and Climate

Check climate tracking:
- GHG emissions tracking: Scope 1, 2, 3 per GHG Protocol.
- Science-based target setting: SBTi alignment.
- Carbon footprint per product/unit.
- Renewable energy tracking and RE100 progress.
- Energy efficiency improvement measurement.
- Supplier climate action requirements and scoring.

Step 3.3 -- Water and Chemical Management

Assess water and chemical compliance:
- Water consumption tracking and reduction targets.
- Wastewater treatment and discharge compliance: ZDHC.
- RSL and MRSL implementation.
- Chemical inventory management per ZDHC gateway.
- Wet processing facility monitoring.
- Water risk assessment: WRI Aqueduct or similar.

Step 3.4 -- Higg Index Integration

Evaluate Higg adoption:
- Higg FEM participation rate.
- Higg FEM scoring and benchmarking.
- Verified vs. self-assessed modules.
- Higg FSLM adoption.
- Higg MSI for material selection.
- Higg BRM for corporate-level performance.

============================================================
PHASE 4: CERTIFICATION TRACKING
============================================================

Step 4.1 -- Certification Management

Evaluate certification lifecycle tracking:
- Certification types: WRAP, SA8000, OEKO-TEX, GOTS, GRS, OCS, BCI/Better Cotton, FSC, Fair Trade, bluesign, Cradle to Cradle.
- Certification validity monitoring: expiration alerts, renewal tracking.
- Scope management: which products/processes are certified.
- Certification verification: certificate authenticity, scope matching.

Step 4.2 -- Material Certifications

Check chain of custody:
- Organic cotton certification chain: GOTS, OCS transaction certificates.
- Recycled content certification: GRS mass balance and transaction tracking.
- OEKO-TEX Standard 100: product safety testing.
- OEKO-TEX STeP: sustainable textile production.
- Chain of custody documentation.
- Material traceability from raw material to finished product.

Step 4.3 -- Certification Impact

Assess certification effectiveness:
- Certification coverage: % of supply chain certified.
- Certification cost tracking.
- Certification as procurement criteria: preferred vendor selection.
- Customer-facing certification claims: marketing and labeling accuracy.
- Certification gap analysis by product line and supplier.

============================================================
PHASE 5: SUPPLIER AUDITS AND ENGAGEMENT
============================================================

Step 5.1 -- Supplier Risk Assessment

Evaluate risk model:
- Inherent risk scoring: country risk, industry risk, commodity risk, previous performance.
- Risk-based audit frequency determination.
- New supplier onboarding due diligence.
- Risk dashboard and heat maps.
- Emerging risk monitoring: political instability, natural disaster, regulatory change.
- Risk aggregation across the supply chain.

Step 5.2 -- Supplier Development

Check capacity building:
- Capacity building programs: training, technical assistance.
- Remediation support: helping suppliers fix issues, not just flagging them.
- Supplier recognition programs: rewarding high performers.
- Preferred supplier programs linked to compliance performance.
- Long-term relationship incentives: volume commitment for compliance investment.

Step 5.3 -- Transparency and Disclosure

Assess public transparency:
- Public supplier list publication: factory disclosure.
- Transparency reporting: Modern Slavery Act statements, California SB 657, CSDDD reporting.
- Fashion Transparency Index participation.
- Stakeholder engagement: worker voice mechanisms, grievance channels, community engagement.
- Public reporting of audit findings and progress.

============================================================
PHASE 6: REPORTING AND GOVERNANCE
============================================================

Step 6.1 -- Compliance Reporting

Evaluate reporting capabilities:
- Internal compliance dashboards: audit status, CAP progress, certification currency.
- Management reporting: compliance KPIs, trend analysis, risk profiles.
- Board-level ESG reporting.
- External reporting: sustainability reports, annual reports, CDP disclosure.
- Regulatory filing support: UFLPA import declarations, Modern Slavery statements.

Step 6.2 -- Governance Structure

Check governance rigor:
- Ethical sourcing policy documentation.
- Code of conduct for suppliers.
- Governance committee: sustainability committee, supply chain ethics board.
- Escalation procedures for severe findings.
- Whistleblower and grievance mechanisms.
- Due diligence process documentation and evidence.

============================================================
PHASE 7: WRITE REPORT
============================================================

Write analysis to `docs/ethical-sourcing-analysis.md` (create `docs/` if needed).

Include: Executive Summary, Supply Chain Transparency Assessment, Labor Compliance Review,
Environmental Impact Analysis, Certification Coverage, Audit Program Effectiveness,
Forced Labor Due Diligence, Recommendations with compliance risk prioritization.


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

## Ethical Sourcing Analysis Complete

- Report: `docs/ethical-sourcing-analysis.md`
- Supply chain tiers mapped: [count]
- Facilities assessed: [count]
- Certifications tracked: [count]
- Compliance standards evaluated: [count]

### Summary Table
| Area | Status | Priority |
|------|--------|----------|
| Supply Chain Transparency | [status] | [priority] |
| Labor Compliance | [status] | [priority] |
| Environmental Impact | [status] | [priority] |
| Certification Management | [status] | [priority] |
| Audit Program | [status] | [priority] |
| Forced Labor Due Diligence | [status] | [priority] |

NEXT STEPS:

- "Run `/material-forecasting` to ensure ethically sourced materials meet demand requirements."
- "Run `/production-scheduling` to verify ethical labor hour limits in production planning."
- "Run `/vendor-management` to evaluate supplier performance alongside ethical compliance."

DO NOT:

- Modify any audit records, corrective action plans, or certification data.
- Downplay forced labor risk indicators regardless of geographic or political sensitivity.
- Assume certification equals compliance -- verify scope, validity, and chain of custody.
- Ignore Tier 2+ suppliers where the most severe labor and environmental risks often exist.
- Recommend exiting supplier relationships without considering worker welfare impact.


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /ethical-sourcing — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
