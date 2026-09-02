---
name: sam-gov-monitor
description: "Monitor SAM.gov federal contract opportunities (and follow-on awards) by NAICS, PSC, agency, set-aside, and keyword — produces a daily pipeline report with pursue/no-pursue scoring, capture-management cadence."
version: "1.0.1"
category: analysis
platforms:
  - CLAUDE_CODE
---

# SAM.gov Federal Contract Opportunity Monitor

You generate a complete capture-management pipeline anchored on SAM.gov as the source of truth. Saved searches beat email alerts (email rolls in 24-72 hours late). Pre-RFP engagement (RFI, Sources Sought) is where the bid is won — by the time the solicitation drops, the requirement is often written around an incumbent.

============================================================
=== PRE-FLIGHT ===
============================================================

Verify:

- [ ] **NAICS codes**: at minimum primary code; ideally a full list (most companies are credible across 3-8 NAICS). Incomplete NAICS limits which opportunities surface.
- [ ] **PSC codes**: Product Service Codes — narrower than NAICS, helps eliminate noise.
- [ ] **Set-aside status**: small business, 8(a), WOSB / EDWOSB, SDVOSB, HUBZone, none. If certified, restrict searches; if not, expand.
- [ ] **Geographic preferences**: any place-of-performance restrictions?
- [ ] **Capacity**: what's your annual capture bandwidth (number of proposals you can credibly write)? Default 12-20/year for a mid-size GovCon.
- [ ] **SAM.gov API key**: register at api.sam.gov; free tier 1,000 requests/day.

Recovery:

- Without API key, fall back to RSS feed at https://sam.gov/rss/ and HTML scraping (lower fidelity, no full-record retrieval).
- If no PSC codes provided, derive from primary NAICS using NAICS→PSC crosswalk.

============================================================
=== PHASE 1: SAM.GOV API CLIENT ===
============================================================

Generate `sam_client.py` (or Node equivalent):

```python
class SAMClient:
    BASE = "https://api.sam.gov/opportunities/v2"

    def search(self, *, posted_from, posted_to, naics=None, psc=None,
               keyword=None, set_aside=None, agency=None, limit=1000):
        """Returns list of opportunities. Handles pagination + rate limit."""
        params = {
            "limit": min(limit, 1000),  # API max per page
            "postedFrom": posted_from.strftime("%m/%d/%Y"),
            "postedTo": posted_to.strftime("%m/%d/%Y"),
            "api_key": self.api_key,
        }
        if naics: params["ncode"] = ",".join(naics)
        if psc:   params["ccode"] = ",".join(psc)
        if keyword: params["q"] = keyword
        if set_aside: params["typeOfSetAside"] = set_aside
        if agency: params["organizationCode"] = agency
        # Paginate, respect 429s with exp backoff, dedupe by noticeId
        ...

    def get_details(self, notice_id):
        """Full opportunity record including attachments URL list."""
        ...
```

Cache responses to local SQLite — re-running same search shouldn't burn quota.

VALIDATION: Client paginates correctly past 1000 results. 429 (rate limit) triggers exp backoff, not crash. Dedupes by `noticeId`.

============================================================
=== PHASE 2: SAVED SEARCHES ===
============================================================

Generate `searches.yaml` — one entry per pursuit profile:

```yaml
searches:
  - name: "IT modernization at HHS"
    naics: [541511, 541512, 541513, 541519, 518210]
    psc: [DA01, DA02, DA10, DA12, DJ01]
    keywords: ["modernization", "legacy", "cloud migration", "FedRAMP"]
    agencies: [HHS, CMS, FDA, NIH]
    set_aside: ["SBA", "8A", "TOTAL_SMALL"]

  - name: "Cyber assessments DoD"
    naics: [541511, 541512, 541513, 541690, 541990]
    psc: [DA10, R425, R408]
    keywords: ["pentest", "red team", "RMF", "ATO", "FedRAMP"]
    agencies: [DOD, USAF, USN, USA, USMC, DISA]
```

Run searches daily via cron. Surface deltas (new notices, amended notices, awarded notices).

VALIDATION: Search YAML is human-editable. Cron runs without intervention. Deltas dedupe against prior runs.

============================================================
=== PHASE 3: PRE-RFP SIGNAL TRACKING ===
============================================================

The bid is often won before the RFP is published. Track notice types:

| Notice Type       | Stage             | Action                                                     |
| ----------------- | ----------------- | ---------------------------------------------------------- |
| Special Notice    | Pre-pre-RFP       | Read. Mark agency for future intel.                        |
| RFI               | Market research   | RESPOND. Get on agency's vendor list. Free intel ride.     |
| Sources Sought    | Market research   | RESPOND. Strongest signal of upcoming SOL. Capture begins. |
| Presolicitation   | RFP draft         | Engage agency BD POC. Influence requirements (legal!).     |
| Solicitation      | RFP issued        | Decide pursue/no-pursue NOW.                               |
| Combined Synopsis | Simplified acq    | Often a sole-source workaround — investigate.              |
| Award             | Won by competitor | Read winning company. Track who has the work.              |
| Justification     | Sole-source       | Read carefully — sometimes contestable.                    |

Generate `pre_rfp_pipeline.csv` that surfaces all RFI / Sources Sought / Presolicitation notices in your saved-search domain, with response deadlines.

VALIDATION: RFI / Sources Sought items get auto-flagged as P0 in the digest. Deadlines tracked.

============================================================
=== PHASE 4: CAPTURE-MANAGEMENT SCORING ===
============================================================

Each opportunity scores on Pwin × value × strategic fit:

| Dimension              | Score 1-5                                                      |
| ---------------------- | -------------------------------------------------------------- |
| Incumbent strength     | 1 = strong incumbent, low Pwin. 5 = no incumbent or weak.      |
| Customer intimacy      | 1 = no prior touch. 5 = sold-to in last 12 months.             |
| Set-aside fit          | 1 = full + open. 5 = your set-aside category restricted.       |
| Past performance match | 1 = adjacent. 5 = exact past work.                             |
| NAICS / PSC fit        | 1 = secondary code. 5 = primary code.                          |
| Solution maturity      | 1 = new build. 5 = productized.                                |
| Bid value (annual)     | (raw $).                                                       |
| Strategic value        | 1 = no follow-on. 5 = pipeline gate for $10M+ multi-year work. |

Composite **Pwin** = average of first 6, multiplied by strategic-value adjustment.

**Pursue threshold**: Pwin ≥ 3.5 AND capacity available AND no calendar conflict with higher-Pwin pursuit.

VALIDATION: Each scored opp produces a single pursue/hold/no-pursue decision with rationale.

============================================================
=== PHASE 5: INCUMBENT + COMPETITOR INTELLIGENCE ===
============================================================

For each opportunity, query USAspending.gov + SAM.gov contract-data API for:

- Prior awards with same NAICS + agency + matching scope.
- Top 5 competitors by revenue in that lane.
- Their typical award size + win rate.
- GSA Schedule holders (if applicable).

Output `competitor_dossier.md` per pursuit.

VALIDATION: Each pursuit has a competitor dossier with ≥ 3 named competitors and their prior award value.

============================================================
=== PHASE 6: SMALL BUSINESS ELIGIBILITY CHECK ===
============================================================

If the opportunity is set-aside, verify your company's eligibility _automatically_:

- SBA Dynamic Small Business Search (DSBS) registration current?
- 8(a) program: in program & not within 9-year graduation window?
- WOSB / EDWOSB: SBA-certified (no longer self-cert as of 2020)?
- SDVOSB: VA-verified via SBA after 2023 transition?
- HUBZone: SBA-certified AND principal office in HUBZone AND 35% workforce in HUBZone?
- Size standards: revenue & employee count below NAICS-specific cap?

Generate `eligibility_check.md` per pursuit — green/yellow/red per dimension.

VALIDATION: Real-time SBA DSBS check or fallback to user-supplied certs.

============================================================
=== PHASE 7: PROPOSAL READINESS PACKAGE ===
============================================================

Once a "pursue" decision is made, generate the proposal-readiness scaffold:

- **Color teaming template**: Pink team (concept review), Red team (writeable), Gold team (final).
- **Proposal compliance matrix**: maps each RFP requirement (Section L instructions, Section M evaluation criteria, FAR clauses) to a proposal section + owner.
- **Pricing prep template**: BOE format (Basis of Estimate), labor categories, indirect rates.
- **Past performance template**: 3-5 contracts maximum, with CPARS reference if applicable.
- **Tech volume outline**: aligned to Section M factors.
- **Capability statement** (one-pager, agency-specific tailoring).

VALIDATION: Compliance matrix has 100% coverage of RFP requirements (no orphan Section L instructions).

============================================================
=== SELF-REVIEW ===
============================================================

Score 1–5:

- **Complete**: API client + searches + pre-RFP tracker + scoring + intel + eligibility + proposal scaffold?
- **Robust**: Handles pagination + rate limits? Respects set-aside semantics correctly?
- **Clean**: Pursue decisions traceable to scoring rubric?
- **GovCon-credible**: Would a capture manager at a $50M-$500M GovCon recognize the workflow?

Common gap: chasing every RFP. The discipline is no-bid more than bid.

============================================================
=== LEARNINGS CAPTURE ===
============================================================

Append to `~/.claude/skills/sam-gov-monitor/LEARNINGS.md`:

## <YYYY-MM-DD> — <NAICS focus, agency cluster>

- **What worked:**
- **What was awkward:**
- **Suggested patch:**
- **Verdict:** [Smooth / Minor friction / Major friction]

============================================================
=== STRICT RULES ===
============================================================

- Never bid every RFP. Win rate × proposal cost is the real metric.
- Never miss the response deadline on RFIs / Sources Sought — those are the cheapest seat at the agency table.
- Never reveal incumbent intelligence sources (USAspending data) in client deliverables. Synthesize, don't cite raw export.
- Never assume set-aside eligibility — verify against SBA real-time data.
- Capacity discipline: if you're at proposal capacity, raise the pursue threshold rather than over-commit.
