---
name: grants-gov-monitor
description: "Monitor federal grant opportunities across Grants.gov (Simpler.grants.gov is the modern UX), SAM.gov assistance listings (the post-CFDA replacement that preserves CFDA program numbers), and direct agency portals — NIH RePORTER + NIH Guide, NSF Funding, DOE OSTI, USDA NIFA, EPA Grants."
version: "1.0.1"
category: analysis
platforms:
  - CLAUDE_CODE
---

# Federal Grants Monitor

You build a pipeline of federal grant opportunities matched to your organization's eligibility, capability, and capacity. The 2026 landscape: 2,200+ federal assistance programs (per SAM.gov assistance listings, which replaced CFDA). GrantMetric reports ~900+ active opportunities across NIH/NSF/DOD/USDA/EPA/etc. The discipline isn't finding grants — it's filtering them.

============================================================
=== PRE-FLIGHT ===
============================================================

- [ ] **Organization type**: 501(c)(3), 501(c)(6), educational (IHE), state/local government, tribal, for-profit small business (SBIR/STTR eligibility), individual researcher.
- [ ] **Mission focus / research domain**: biomedical, energy, education, environment, social services, arts, defense, agriculture.
- [ ] **NAICS / discipline codes**: define what the org can credibly execute.
- [ ] **Past awards**: prior NIH/NSF/agency grants enable continuation funding paths.
- [ ] **DUNS/UEI**: org must have UEI (Unique Entity Identifier) at SAM.gov to receive awards.
- [ ] **Cost-share capacity**: many federal programs require 10-50% match. If you can't match, filter those out.
- [ ] **Indirect rate**: federally negotiated rate or de minimis 10% MTDC.

Recovery:

- New org without UEI: route to SAM.gov registration first (3-5 days for new registrations).
- For SBIR/STTR: validate small-business criteria (≤ 500 employees, US-owned, primary place of business in US).

============================================================
=== PHASE 1: OPPORTUNITY INGESTION ===
============================================================

Pull from multiple sources daily:

**Grants.gov API** (open, no key required):

```
GET https://api.grants.gov/v1/api/search2
  ?keyword={query}
  &oppStatuses=forecasted|posted
  &eligibilities={code_list}
  &fundingCategories={cat_list}
  &agencies={agency_list}
```

**SAM.gov Assistance Listings**: 2,200+ programs with CFDA numbers (still used as program identifiers post-CFDA sunset). Use SAM.gov API.

**Agency-specific portals**:

- **NIH Guide**: parameterized RSS / API for FOAs (R01, K series, R21, R03, SBIR, STTR). https://grants.nih.gov/grants/guide/
- **NSF Funding**: https://www.nsf.gov/funding/opportunities/ — programs across directorates (BIO, CSE, ENG, GEO, MPS, EHR, SBE).
- **DOE OSTI**: science.osti.gov for DOE Office of Science.
- **USDA NIFA**: https://www.nifa.usda.gov/grants/funding-opportunities — AFRI, BFRDP, etc.
- **EPA Grants**: epa.gov/grants
- **NEH/NEA**: humanities + arts.
- **IES** (Department of Education): https://ies.ed.gov/funding/

Persist all opportunities to a local DB with schema:

```json
{
  "opp_id": "...",
  "source": "GRANTS_GOV|SAM_AL|NIH|NSF|DOE|...",
  "title": "...",
  "agency": "...",
  "cfda_number": "93.279",
  "summary": "...",
  "eligibility_codes": ["...", "..."],
  "category": ["...", "..."],
  "funding_total_estimate": 5000000,
  "award_floor": 100000,
  "award_ceiling": 500000,
  "expected_award_count": 10,
  "post_date": "2026-04-01",
  "loi_due": "2026-06-15",
  "full_app_due": "2026-08-15",
  "url": "...",
  "match_required_pct": 25,
  "indirect_cap_pct": null,
  "geographic_restriction": null,
  "performance_period_months": 36
}
```

VALIDATION: Daily ingestion captures > 95% of newly-posted opportunities. Diff vs previous day produces a clean "new today" list.

============================================================
=== PHASE 2: ELIGIBILITY FILTER ===
============================================================

Filter the universe to opportunities the user can actually apply for:

| Eligibility Code | Org Types                                                       |
| ---------------- | --------------------------------------------------------------- |
| 00               | Unrestricted                                                    |
| 01               | County governments                                              |
| 02               | City or township                                                |
| 04               | Special district                                                |
| 05               | Independent school district                                     |
| 06               | Public/State controlled IHE                                     |
| 07               | Native American tribal organizations (federally recognized)     |
| 08               | Public housing authorities                                      |
| 11               | Native American tribal organizations (non-federally recognized) |
| 12               | Nonprofits with 501(c)(3) status                                |
| 13               | Nonprofits without 501(c)(3) status                             |
| 20               | Private institutions of higher education                        |
| 21               | Individuals                                                     |
| 22               | For-profit organizations (non-small businesses)                 |
| 23               | Small businesses                                                |
| 25               | Others                                                          |
| 99               | Unrestricted                                                    |

Map user's org type → eligibility codes → opportunities. Hide non-eligible. Surface "near eligible" (e.g., need fiscal sponsor) separately.

VALIDATION: Filter precision ≥ 95% (no false-positive "eligible" opportunities).

============================================================
=== PHASE 3: CAPABILITY MATCH SCORING ===
============================================================

Beyond eligibility, score each opportunity on capability fit:

| Dimension                   | Score 1-5                                                                          | Notes                                                        |
| --------------------------- | ---------------------------------------------------------------------------------- | ------------------------------------------------------------ |
| **Subject-matter fit**      | 1 = adjacent, 5 = on-mission                                                       | Cosine similarity of opp summary vs org capability statement |
| **Prior award credibility** | 1 = no past, 5 = active funded researcher in the program                           | Pull from NIH RePORTER / USAspending                         |
| **Award size fit**          | 1 = too small to bother / too big to credibly win, 5 = right size for org capacity | $25k-$1M sweet spot for small nonprofits                     |
| **Deadline reality**        | 1 = < 30 days (rushed), 5 = > 90 days                                              | Quality proposals need 6-12 weeks                            |
| **Match feasibility**       | 1 = can't meet match, 5 = no match required                                        | Tag opps with > 25% match if user lacks capacity             |
| **Competition density**     | 1 = R01 (10% success rate), 5 = niche small business (40%+)                        | Pull historical award rate per program                       |

**Composite Pwin** = weighted average. Pursue threshold: ≥ 3.5.

VALIDATION: Each opp has Pwin score with rationale per dimension.

============================================================
=== PHASE 4: DEADLINE CALENDAR ===
============================================================

Generate calendar with critical dates per opportunity:

- **LOI (Letter of Intent) deadline** — often 6-8 weeks before full app
- **Full application deadline** — the binding date
- **Pre-application consultation window** — for programs that strongly encourage agency contact (NSF program officer, NIH program contact)
- **Renewal / continuation cycles** — for K/R awards
- **JIT (Just-In-Time) submission** — NIH-specific (post-review)

Output `grants_calendar.ics`. Reminder: 12 weeks / 8 weeks / 4 weeks / 2 weeks / 1 week before each deadline.

VALIDATION: Calendar imports cleanly. Reminders fire at expected intervals.

============================================================
=== PHASE 5: SAM.GOV + UEI READINESS ===
============================================================

Before applying, verify:

- [ ] UEI exists at SAM.gov
- [ ] SAM.gov registration is ACTIVE (not expired — annual renewal required)
- [ ] Org has Federal Tax ID (EIN) on file
- [ ] If applicable: System for Award Management (SAM) Reps & Certs current
- [ ] Negotiated Indirect Cost Rate Agreement (NICRA) — or default to de minimis 10% MTDC
- [ ] CCR / SAM Entity Management has no exclusions / debarments
- [ ] Workspace at Grants.gov configured with the right roles (AOR, signing official, etc.)

Generate `sam_uei_health_check.md` flagging any gaps.

VALIDATION: SAM.gov registration verified within 30 days. Expired registration blocks federal awards.

============================================================
=== PHASE 6: PROPOSAL READINESS SCAFFOLD ===
============================================================

For each "pursue" opportunity, generate the proposal-prep package:

- **Capability statement** (org-level, agency-tailored)
- **Bio sketches** for key personnel (NIH biosketch format if NIH; NSF Current & Pending Support if NSF)
- **Specific Aims / Research Strategy** template per agency (NIH 1-page Specific Aims, 12-page Research Strategy)
- **Budget** template per agency rules (PHS 398, NSF FastLane / Research.gov, etc.)
- **Budget justification** template (personnel by % effort, equipment, supplies, travel, indirect)
- **Data Management Plan** (NSF DMP, NIH DMSP)
- **Resource Sharing Plan** (NIH model organisms, software)
- **Letters of Support** template (collaborators, vendors, advisors)
- **Compliance**: IRB / IACUC / IBC / Conflict of Interest disclosures
- **Single Audit** awareness: $750k+/yr federal aggregate triggers 2 CFR Part 200 Subpart F single audit

Output `proposal_kit/{opp_id}/` directory.

VALIDATION: Kit has all standard sections; agency-specific templates populated.

============================================================
=== PHASE 7: WEEKLY DIGEST ===
============================================================

Schedule weekly Monday digest:

```markdown
# Grants Pipeline — Week of {date}

## New opportunities this week ({N})

{Filtered list with Pwin ≥ 2 — surface broader pool, even if below pursue threshold}

## Pursue queue ({M})

{Opps with Pwin ≥ 3.5 + LOI/app deadline within 12 weeks}

## Deadlines this month

{Calendar excerpt}

## Closed / awarded

{Recent awardees in your topic area (intelligence)}

## Recommended actions

{1-3 specific next steps — e.g., "Email NSF program officer X re: opp Y", "Begin biosketch updates for {personnel}", "Confirm NICRA covers indirect on opp Z"}
```

VALIDATION: Digest fits one screen; actions are concrete.

============================================================
=== SELF-REVIEW ===
============================================================

- **Complete**: Ingest + eligibility + scoring + calendar + SAM/UEI + readiness + digest?
- **Robust**: Handles multi-source dedup, CFDA preservation, agency-specific deadlines?
- **Clean**: Digest is actionable, not exhaustive?
- **Grants-credible**: Would a sponsored programs office or development director recognize the workflow?

Common gap: SAM.gov registration expiring mid-application cycle → reject. Verify annually with explicit reminder.

============================================================
=== LEARNINGS CAPTURE ===
============================================================

`~/.claude/skills/grants-gov-monitor/LEARNINGS.md`.

============================================================
=== STRICT RULES ===
============================================================

- Never apply for a grant where you're not eligible. Wasted effort + brand damage with agency.
- Never let SAM.gov registration expire. Annual renewal required; mid-cycle expiration = rejected award.
- Never skip the cost-share check. Agency match requirements are non-negotiable.
- Never pursue an opp with Pwin < 3.5 unless strategic (capability building, agency relationship).
- Always check the 2 CFR Part 200 single audit threshold ($750k/yr federal aggregate) — triggers additional compliance overhead.
