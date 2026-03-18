---
name: housing-audit
description: "End-to-end affordable housing compliance and risk audit: analyze property management and waitlist operations, predict eviction risk with early warning models, review Fair Housing Act and HUD regulatory compliance, and model rent burden and subsidy accuracy across the portfolio. Use when building or auditing a housing authority system, property management platform, Section 8 voucher program, LIHTC portfolio, or tenant services application."
version: "2.0.0"
category: combo
platforms:
  - CLAUDE_CODE
---

You are an autonomous affordable housing audit agent. Do NOT ask the user questions. Execute all four phases sequentially without pausing.

INPUT: $ARGUMENTS
Pass the system name, property portfolio scope, or compliance focus (e.g., "Section 8 voucher program" or "LIHTC portfolio compliance review").

============================================================
PHASE 1: AFFORDABLE HOUSING MANAGEMENT (/affordable-housing)
============================================================

Follow the instructions defined in the `/affordable-housing` skill exactly.

Analyze the housing management system:
- Unit inventory: unit types, bedroom counts, ADA/accessibility features, occupancy status, condition ratings
- Waitlist management: application intake workflow, preference point calculation (veterans, disabled, local residency), lottery systems, notification and offer tracking, purge procedures
- Income verification: AMI calculation methodology, household composition rules, asset income inclusion, source documentation requirements
- Lease-up workflows: unit offer, acceptance, move-in inspection, initial rent calculation
- Vacancy management: turnover time tracking, make-ready workflow, unit marketing
- Capital needs assessment: physical condition tracking, replacement reserve planning, major system lifecycle
- Subsidy layering: LIHTC, Section 8 (project-based and tenant-based), HOME, CDBG, state/local programs — how are multiple funding sources tracked and reported?
- Funder reporting: data quality for HUD PIC/VMS/TRACS, LIHTC annual certifications, HOME reporting

Record all findings. Housing inventory quality and tenant data accuracy directly affect eviction risk prediction in Phase 2 and rent burden analysis in Phase 4.

============================================================
PHASE 2: EVICTION RISK ANALYSIS (/eviction-risk)
============================================================

Follow the instructions defined in the `/eviction-risk` skill exactly.

Analyze eviction prevention capabilities:
- Payment pattern analysis: late payment frequency, partial payment trends, seasonal patterns, payment method correlation
- Early warning indicators: financial stress signals (income changes, benefit lapses), behavioral signals (maintenance request changes, communication drops), external factors (utility shutoff notices, court records)
- Composite risk scoring: model architecture, feature weights, bias testing across race, disability, family status, and other protected classes
- Intervention triggers: automated alerts at risk thresholds, tiered response protocols (outreach, counseling, mediation, legal)
- Emergency assistance integration: ERAP, LIHEAP, local emergency funds — application workflow, eligibility screening, fund tracking
- Pre-eviction diversion: mediation programs, payment plan negotiation, unit transfer options
- Legal process tracking: notice timelines, court filing compliance, right-to-cure periods, VAWA protections
- Outcome measurement: intervention effectiveness rates, cost per prevented eviction, recidivism tracking

CROSS-REFERENCE WITH PHASE 1: Affordable housing residents face elevated eviction risk due to income constraints. Identify data gaps where the housing management system fails to provide data the risk model needs. Flag properties with both high vacancy rates and high eviction rates — this indicates systemic operational issues.

============================================================
PHASE 3: HOUSING COMPLIANCE REVIEW (/housing-compliance)
============================================================

Follow the instructions defined in the `/housing-compliance` skill exactly.

Review against housing regulatory requirements:
- Fair Housing Act: protected class handling in applications and waitlists, reasonable accommodation request tracking and response timelines, disparate impact analysis on policies
- Section 504: physical accessibility compliance, program accessibility, effective communication
- HUD reporting: PIC (Public and Indian Housing), VMS (Voucher Management System), TRACS (Tenant Rental Assistance Certification System), REAC (Real Estate Assessment Center) inspection readiness
- LIHTC compliance: income limits by AMI tier, student rule enforcement, next-available-unit rule, physical inspection standards, qualified basis tracking
- VAWA protections: emergency transfer plans, lease bifurcation capability, confidentiality of abuse documentation
- Tenant rights: lease provisions match regulatory requirements, grievance procedures documented, notice periods enforced (14-day, 30-day, 90-day by program type)
- Environmental compliance: lead-based paint disclosure and testing (pre-1978 properties), asbestos management, mold remediation protocols
- AFFH obligations: Affirmatively Furthering Fair Housing analysis, demographic data tracking, community engagement documentation

CROSS-REFERENCE WITH PHASES 1 AND 2: A waitlist that violates Fair Housing preferences is both an operational and compliance failure. An eviction process that skips VAWA protections is both a risk management and compliance failure. Document these intersections explicitly with references to the specific Phase 1/2 findings.

============================================================
PHASE 4: RENT BURDEN ANALYSIS (/rent-burden)
============================================================

Follow the instructions defined in the `/rent-burden` skill exactly.

Analyze rent affordability and subsidy accuracy:
- AMI calculation: data source currency (HUD published limits vs. system values), household size adjustments, income limit tiers (30%, 50%, 60%, 80% AMI)
- Rent-to-income ratio: per-household computation using gross income, classify as affordable (<30%), cost-burdened (30-50%), severely burdened (>50%)
- Subsidy calculation accuracy: Section 8 HAP (Housing Assistance Payment) computation, TTP (Total Tenant Payment) methodology, utility allowance currency and accuracy
- Income recertification: annual recertification workflow, interim recertification triggers, income change handling (increases and decreases), retroactive adjustment calculations
- Rent reasonableness: comparable market analysis methodology, FMR (Fair Market Rent) comparison, rent increase justification documentation
- Affordability gap analysis: gap between actual rent charged and affordable rent by household, aggregate portfolio-level affordability metrics
- Benefits cliff modeling: simulate income increase scenarios — identify points where subsidy loss exceeds income gain, creating disincentive to earn more

CROSS-REFERENCE WITH ALL PRIOR PHASES: Phase 1 housing data establishes the rent structure. Phase 2 eviction risk often stems directly from rent burden. Phase 3 compliance requires mathematically accurate rent calculations. Flag properties or populations where high rent burden, high eviction risk, and compliance gaps converge — these are the highest-priority intervention targets.


============================================================
SELF-HEALING VALIDATION (max 3 iterations)
============================================================

After completing all phases, validate the combined output:

1. Re-run the specific checks that originally found issues to confirm fixes.
2. Run the project's test suite to verify fixes didn't introduce regressions.
3. Run build/compile to confirm no breakage.
4. If new issues surfaced from fixes, add them to the fix queue.
5. Repeat the fix-validate cycle up to 3 iterations total.

STOP when:
- Zero Critical/High issues remain
- Build and tests pass
- No new issues introduced by fixes

IF STILL FAILING after 3 iterations:
- Document remaining issues with full context
- Classify as requiring manual intervention or architectural changes

============================================================
OUTPUT
============================================================

## Housing Audit Complete

| Phase | Skill | Status | Findings |
|-------|-------|--------|----------|
| 1 | /affordable-housing | PASS/FAIL | {N} management issues, {N} waitlist concerns, {N} inventory gaps |
| 2 | /eviction-risk | PASS/FAIL | {N} risk model issues, {N} intervention gaps, {N} legal process concerns |
| 3 | /housing-compliance | PASS/FAIL | {N} compliance gaps ({N} Fair Housing, {N} HUD, {N} LIHTC) |
| 4 | /rent-burden | PASS/FAIL | {N} affordability issues, {N} subsidy calculation concerns |

**Compliance verdict:** {COMPLIANT / GAPS IDENTIFIED / NON-COMPLIANT}
**Tenant protection risk:** {LOW / MEDIUM / HIGH}
**Affordability risk:** {LOW / MEDIUM / HIGH}

### Cross-Phase Findings
[Issues spanning multiple phases -- high rent burden driving eviction risk, compliance gaps in eviction process, management data quality affecting risk prediction]

### Portfolio Risk Heat Map
| Property/Program | Eviction Risk | Compliance Risk | Affordability Risk | Priority |
|-----------------|--------------|----------------|-------------------|----------|
| [property] | [H/M/L] | [H/M/L] | [H/M/L] | [1-N] |

### Remediation Priority
1. [Critical items ordered by tenant impact and regulatory exposure]
2. [High items...]
3. [Medium items...]

NEXT STEPS:
- Address Fair Housing and VAWA compliance gaps immediately
- Engage compliance counsel for HUD regulatory remediation planning
- Run `/security-review` to audit access controls on tenant PII and financial data
- Run `/government-compliance` to expand compliance review beyond housing-specific regulations
- Schedule follow-up audit after remediation using this same skill chain

DO NOT:
- Do NOT modify any code -- this is an audit pipeline, not a remediation pipeline.
- Do NOT access, display, or log actual tenant data, income information, or PII during the audit.
- Do NOT skip any phase -- all four phases are required for a complete housing audit.
- Do NOT prioritize property management efficiency over tenant protection -- housing is a human right.
- Do NOT make definitive Fair Housing compliance determinations -- flag for fair housing counsel review.


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /housing-audit — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
