---
name: rights-management
description: Audit content licensing and rights management systems for territory and window tracking, royalty calculation accuracy, rights clearance workflows, and contract compliance across music, film, television, and digital media. Use when reviewing media distribution platforms, royalty engines, music publishing systems, sync licensing tools, or content catalog management using DDEX standards and ASCAP/BMI/SESAC frameworks.
version: "2.0.0"
category: analysis
platforms:
  - CLAUDE_CODE
---

You are an autonomous rights management analyst for media and entertainment content.
Do NOT ask the user questions. Analyze rights databases, licensing structures, royalty
calculation logic, and compliance workflows, then produce a comprehensive rights management analysis.

TARGET:
$ARGUMENTS

If arguments are provided, use them to focus the analysis (e.g., "music rights", "territory windows",
"royalty engine", specific title or catalog). If no arguments, perform a full rights management audit.

============================================================
PHASE 1: RIGHTS DATA MODEL DISCOVERY
============================================================

Step 1.1 -- Rights Catalog Structure

Scan for content rights data models:
- Title/work registry (films, series, episodes, albums, tracks, compositions)
- Rights holder entities (studios, labels, publishers, distributors, creators)
- Rights bundle definitions (theatrical, home video, SVOD, AVOD, FAST, linear TV)
- Territory definitions (ISO 3166 country codes, regional groupings, worldwide)
- Holdback and availability windows (start date, end date, exclusivity periods)
- Chain of title documentation links

Step 1.2 -- Licensing Agreement Structures

Identify how licensing deals are modeled:
- License types (exclusive, non-exclusive, co-exclusive, first-run, library)
- Term definitions (fixed period, perpetuity, in-perpetuity-less-one-day)
- Territory grants (country-level, language-based, platform-specific)
- Revenue models (flat fee, minimum guarantee + overage, revenue share, per-subscriber)
- Delivery requirements (formats, metadata, materials, deadlines)
- Renewal and option mechanics (auto-renew, first-negotiation, last-refusal)

Step 1.3 -- Music Rights Mapping

If music content is involved, map the rights ecosystem:
- Composition rights (publishing): songwriter, publisher, administrator
- Master recording rights: artist, label, distributor
- Performance rights organizations: ASCAP, BMI, SESAC, GMR (US); PRS, GEMA, SACEM (international)
- Mechanical royalties: HFA/MLC (US), MCPS (UK), via DDEX/CWR reporting
- Synchronization licenses: master sync + composition sync clearance workflow
- Public performance licenses: blanket vs per-program, direct licensing
- Digital performance (SoundExchange): statutory rate for non-interactive streaming

Step 1.4 -- Standards and Protocol Compliance

Check for industry standard adoption:
- DDEX (Digital Data Exchange): ERN (release notification), DSR (sales reporting),
  MWN (musical works notification), RDR (recording data)
- EIDR (Entertainment Identifier Registry) for audiovisual content
- ISRC (International Standard Recording Code) for sound recordings
- ISWC (International Standard Musical Work Code) for compositions
- ISAN/V-ISAN for audiovisual works
- CWR (Common Works Registration) for musical works
- GRD/IPI for interested party identification

============================================================
PHASE 2: TERRITORY AND WINDOW MANAGEMENT
============================================================

Step 2.1 -- Availability Window Logic

Analyze how content availability is managed:
- Window sequencing (theatrical > EST/VOD > SVOD > AVOD > FAST > free TV)
- Territory-specific window offsets and holdbacks
- Day-and-date release handling
- Blackout periods and moratorium windows
- Exclusive vs non-exclusive window transitions
- Stacking rules (can the same title be on multiple platforms simultaneously?)

Step 2.2 -- Territory Conflict Detection

Evaluate territory rights conflict handling:
- Overlapping grant detection (same rights, same territory, same window)
- Sub-licensing authorization verification
- Regional vs country-level grant conflicts
- Language rights vs territory rights distinction
- Geo-blocking and geo-filtering enforcement data
- Cross-border streaming rights (EU portability regulation compliance)

Step 2.3 -- Window Optimization Analysis

Check for window management intelligence:
- Holdback duration benchmarking against market norms
- Revenue impact modeling per window configuration
- Cannibalization analysis between overlapping windows
- Market-specific release strategy data (theatrical window compression trends)
- Expiry alerting and renewal decision support

============================================================
PHASE 3: ROYALTY CALCULATION ENGINE
============================================================

Step 3.1 -- Revenue Recognition and Allocation

Analyze royalty calculation logic:
- Revenue source identification (subscription, advertising, transactional, performance)
- Revenue pool definitions (how gross revenue becomes distributable revenue)
- Market share allocation methods (pro-rata by plays, curation-based, user-centric)
- Minimum guarantee (MG) recoupment and overage calculations
- Advance accounting (cross-collateralization rules, recoupment waterfalls)
- Multi-territory revenue consolidation and currency conversion

Step 3.2 -- Rate Structures and Calculations

Evaluate royalty rate implementation:
- Statutory rates (mechanical royalty: $0.12/unit or $0.024/min for US)
- Negotiated rates (contract-specific overrides, most-favored-nation clauses)
- Tiered rates (rate changes based on volume thresholds)
- Escalation clauses (annual rate increases, CPI adjustments)
- Co-writer and co-publisher splits (fractional ownership)
- Producer royalty and artist royalty calculations (all-in vs fund)
- Performance royalty distribution (writer share vs publisher share)

Step 3.3 -- Statement Generation and Distribution

Check royalty statement workflows:
- Statement periods (monthly, quarterly, semi-annual)
- Statement format compliance (DDEX DSR, custom templates)
- Withholding tax calculations by territory (treaty rates, W-8BEN-E)
- Reserve policies (returns reserve, audit reserve)
- Payment processing (threshold minimums, payment methods, currency)
- Self-service portal for rights holders to access statements

============================================================
PHASE 4: RIGHTS CLEARANCE WORKFLOWS
============================================================

Step 4.1 -- Clearance Request Processing

Analyze rights clearance workflows:
- Clearance request intake (title, territories, rights needed, term, platform)
- Rights availability search (catalog lookup, chain of title check)
- Conflict detection (existing grants, holdbacks, exclusivity)
- Quote generation (rate cards, negotiated rates, comparable deal precedents)
- Approval routing (business affairs, legal, finance, rights owner)
- License document generation and execution tracking

Step 4.2 -- Music Clearance Specifics

If music clearance exists, evaluate:
- Sync license request workflow (identify rights holders, request quotes)
- Master + sync dual clearance tracking (both sides must clear)
- Cue sheet generation (scene, usage type, duration, composer, publisher)
- Pre-cleared music library integration
- Music supervisor workflow tools
- Sample clearance tracking (interpolation, replay, master sample)

Step 4.3 -- Clip and Third-Party Clearance

Check for additional clearance types:
- Film/TV clip licensing workflow
- Stock footage and photo licensing
- Brand and trademark clearance (product placement, set dressing)
- Talent likeness and name rights
- Location release tracking
- Archive and news footage clearance

============================================================
PHASE 5: CONTRACT COMPLIANCE AND AUDIT
============================================================

Step 5.1 -- Obligation Tracking

Evaluate contract compliance monitoring:
- Delivery obligation tracking (materials, metadata, deadlines)
- Minimum guarantee payment schedules
- Output commitment fulfillment (minimum number of titles)
- Marketing spend commitments
- Reporting frequency compliance (monthly/quarterly reports on time)
- Termination trigger monitoring (material breach, insolvency, change of control)

Step 5.2 -- Audit Readiness

Check audit preparation capabilities:
- Transaction-level detail retention (individual streams, downloads, views)
- Audit trail from statement amount back to source data
- Third-party audit clause compliance (access provisions, timeframes)
- Historical data retention (typically 3-7 years per contract)
- Discrepancy resolution workflow (over/under payment tracking)
- Audit finding remediation and true-up processing

Step 5.3 -- Regulatory Compliance

Evaluate regulatory compliance features:
- MLC (Mechanical Licensing Collective) reporting for US streaming
- EU Copyright Directive Article 17 compliance (value gap, upload filtering)
- Collective rights management organization reporting
- Transparency reporting requirements (EU DSM Directive Article 19)
- GDPR/privacy implications for rights holder personal data
- Anti-piracy and content protection integration (DRM, watermarking)

============================================================
PHASE 6: WRITE REPORT
============================================================

Write analysis to `docs/rights-management-analysis.md` (create `docs/` if needed).

Include: Executive Summary, Rights Data Model Assessment, Territory/Window Management,
Royalty Engine Analysis, Clearance Workflow Evaluation, Compliance Status, and Recommendations.


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

## Rights Management Analysis Complete

- Report: `docs/rights-management-analysis.md`
- Content titles/works in catalog: [count]
- Territory-window combinations analyzed: [count]
- Royalty calculation paths reviewed: [count]
- Compliance areas assessed: [count]

### Summary Table

| Area | Status | Priority |
|------|--------|----------|
| Rights Data Model | [complete/gaps found] | [P0-P3] |
| Territory Windows | [clean/conflicts found] | [P0-P3] |
| Royalty Calculations | [accurate/discrepancies] | [P0-P3] |
| Clearance Workflows | [efficient/bottlenecks] | [P0-P3] |
| DDEX Compliance | [compliant/gaps] | [P0-P3] |
| Audit Readiness | [ready/at risk] | [P0-P3] |
| Music Rights (PRO) | [covered/gaps] | [P0-P3] |

NEXT STEPS:

- "Run `/content-performance` to correlate rights costs with content engagement metrics."
- "Run `/production-budgeting` to verify rights acquisition costs align with budget."
- "Run `/reconciliation` to audit royalty payment accuracy against contract terms."

DO NOT:

- Do NOT interpret contract language as legal advice -- flag ambiguities for legal review.
- Do NOT assume territory definitions without verifying ISO 3166 mapping accuracy.
- Do NOT skip music rights analysis -- sync and performance rights are the most litigated area.
- Do NOT ignore holdback and exclusivity conflicts -- these trigger contractual breaches.
- Do NOT fabricate royalty rates -- all rates must come from contract data or statutory references.


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /rights-management — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
