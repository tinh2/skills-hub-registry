---
name: kyc-aml-screener
description: Generate a production-grade KYC / AML / sanctions screening pipeline for customer onboarding, transaction monitoring, and ongoing review. Screens against OFAC SDN, OFAC Consolidated, EU sanctions, UK HMT, UN Security Council, plus PEP (politically exposed persons), adverse media, and UBO (ultimate beneficial owner) traces. Implements fuzzy name matching (Damerau-Levenshtein + Jaro-Winkler), alias awareness, transliteration handling (Cyrillic/Arabic/Hangul to Latin), geo correlation, DOB matching, and configurable match thresholds to reduce the false-positive rate that buries compliance teams. Generates: list ingestion + nightly refresh, customer screening API, batch rescreening cron, watchlist diff detection (alert when an existing customer becomes newly listed), case management UI scaffold with disposition (clear / escalate / SAR), and SAR (Suspicious Activity Report) FinCEN Form 111 prep helpers. 70%+ of 2026 onboarding is automated via these systems. TRIGGER on "KYC", "AML", "OFAC", "sanctions screening", "PEP", "watchlist", "compliance onboarding", "FinCEN", "BSA", "SAR", "CIP", "CDD", "EDD", "ultimate beneficial owner", "UBO", "FATF", "MLRO".
version: "1.0.0"
category: analysis
platforms:
  - CLAUDE_CODE
---

# KYC / AML / Sanctions Screening Pipeline

You generate a complete screening pipeline for customer onboarding and continuous monitoring. The 2026 regulatory floor: customer identification (CIP), customer due diligence (CDD), enhanced due diligence (EDD) for high-risk, sanctions screening against multiple lists, PEP screening, and transaction monitoring. The dominant cost driver is **false positives** — sloppy matching buries compliance teams in noise and slows real-money revenue.

============================================================
=== PRE-FLIGHT ===
============================================================

Verify:

- [ ] **Regulatory regime**: US (BSA / FinCEN / OFAC), EU (AMLD6), UK (MLR 2017), Singapore (MAS), or multi-jurisdiction.
- [ ] **Customer type**: retail individuals, small business (KYB), institutions, fintech (regulated by OCC / Fed / state).
- [ ] **Onboarding volume**: < 100/day → in-house tooling viable. > 1k/day → must use specialist vendor (ComplyAdvantage, Dow Jones, LSEG World-Check, dilisense, Sayari, Sanctions.io).
- [ ] **Risk appetite**: tighter thresholds = fewer false negatives but more analyst review. Calibrate per regulator expectations.
- [ ] **Existing stack**: identity verification vendor (Persona, Plaid Identity, Veriff, Onfido, Jumio) feeds this pipeline; if absent, route there first.

Recovery:

- For sub-100/day startups, generate the in-house pipeline with OpenSanctions (free, comprehensive, daily updates) as primary data source.
- For higher volume, generate adapter scaffolds for ComplyAdvantage + Dow Jones APIs.

============================================================
=== PHASE 1: LIST INGESTION + REFRESH ===
============================================================

Source the watchlists. Frequency: nightly refresh for sanctions (lists update daily), weekly for PEP.

| List                             | Source                                               | Format            | Frequency |
| -------------------------------- | ---------------------------------------------------- | ----------------- | --------- |
| OFAC SDN                         | sanctionssearch.ofac.treas.gov + Treasury data files | XML/CSV/JSON      | Daily     |
| OFAC Consolidated (non-SDN)      | OFAC                                                 | XML/CSV           | Daily     |
| EU Consolidated Sanctions        | data.europa.eu                                       | XML               | Daily     |
| UK HMT Sanctions                 | gov.uk OFSI                                          | CSV               | Daily     |
| UN Security Council Consolidated | scsanctions.un.org                                   | XML               | Daily     |
| Australian DFAT                  | dfat.gov.au                                          | XLS               | Weekly    |
| Canada (OSFI)                    | osfi-bsif.gc.ca                                      | XML               | Daily     |
| OpenSanctions (aggregator)       | opensanctions.org                                    | JSON / Statements | Daily     |
| PEP                              | Dow Jones Risk & Compliance or OpenSanctions PEP     | Various           | Weekly    |

Generate `list_refresh.py` that pulls each list, normalizes to a common schema, and diffs against the previous version. Newly listed entities trigger an alert against your customer base.

VALIDATION: After refresh, list count is plausible (SDN ~16k entries in 2026). Diff produces both additions and removals.

============================================================
=== PHASE 2: CANONICAL ENTITY SCHEMA ===
============================================================

Normalize every list entry into:

```json
{
  "list_id": "OFAC-SDN-12345",
  "source_list": "OFAC_SDN",
  "first_listed_date": "2024-03-15",
  "last_updated": "2026-02-08",
  "entity_type": "individual" | "vessel" | "aircraft" | "entity",
  "primary_name": "Smith, John",
  "alt_names": ["Johnny Smith", "Иван Смит", "...transliterations..."],
  "dob": ["1965-06-12"],
  "place_of_birth": "Damascus, Syria",
  "nationalities": ["SY", "LB"],
  "addresses": [...],
  "identifications": [{"type": "passport", "country": "SY", "number": "..."}],
  "linked_entities": [...],
  "programs": ["SDGT", "SYRIA"],
  "remarks": "..."
}
```

Same schema applies to PEP entries (with positions, parties, etc.) and adverse media (with article references).

VALIDATION: Schema validates with strict types. Cross-list dedup catches the same entity present on multiple lists.

============================================================
=== PHASE 3: NAME MATCHING ENGINE ===
============================================================

This is the highest-leverage component. Match quality = (recall) × (1 / false positives).

**Layered approach**:

1. **Exact + alias** (deterministic): full match against primary_name and any alt_name.
2. **Phonetic** (Soundex, Metaphone, BMPM): handles transliteration variants (Mohammed/Muhammad/Mohamed).
3. **Edit distance** (Damerau-Levenshtein): handles typos. Threshold: ≥ 0.85 similarity.
4. **Token-based** (Jaccard, Jaro-Winkler): handles word reorderings ("John Smith" vs "Smith, John"). JW threshold ≥ 0.92.
5. **Substring + n-gram**: catches partial matches in long entity names.
6. **Cross-script**: transliterate Cyrillic/Arabic/Greek/Chinese to Latin before comparing.

For each candidate match, compute a **match score**:

```
match_score = w_name * name_sim
            + w_dob * dob_match
            + w_country * country_match
            + w_id * id_match
            - w_disambig * disambiguation_signal
```

Default weights: name 0.5, dob 0.2, country 0.15, id 0.15. Tune per false-positive rate.

**Filter cascade**:

- Score < 0.6 → drop (likely noise).
- 0.6-0.79 → secondary review queue.
- 0.80-0.95 → analyst review.
- > 0.95 → block + analyst review.

VALIDATION: Benchmark against the FuzzyWuzzy test corpus (sanction-name pairs with known matches/non-matches). Precision ≥ 95% and recall ≥ 90%.

============================================================
=== PHASE 4: ONBOARDING SCREENING API ===
============================================================

Generate `screen.py` exposing:

```python
def screen_customer(customer: CustomerProfile) -> ScreeningResult:
    """
    Returns ScreeningResult with:
      - status: CLEAR | HOLD | ESCALATE | BLOCK
      - matches: list of MatchCandidate with scores + list_id refs
      - pep_matches, sanctions_matches, adverse_media_matches
      - risk_score: 0-100
      - explainer: human-readable reasoning
    """
```

Key behavior:

- **Hard block** on sanctions match > 0.95 (compliance failure to block = personal liability for the MLRO).
- **Hold** on PEP match — most jurisdictions require EDD before opening, not a hard block.
- **Risk score** combines screening hits + geography (high-risk country FATF lists) + transaction type + occupation.

Auditability: every screening decision persists `who, when, what, why` in tamper-evident storage (append-only, S3 Object Lock or equivalent).

VALIDATION: Round-trip an onboarding with a known-OFAC-listed test name; system blocks and records the decision.

============================================================
=== PHASE 5: ONGOING MONITORING + WATCHLIST DIFF ===
============================================================

After a customer is onboarded, screening doesn't stop. Generate:

1. **Nightly rescreen** of every active customer against the latest lists.
2. **Watchlist diff alert**: when a name is newly added that fuzzy-matches an existing customer, raise a HIGH priority case.
3. **Address / occupation / nationality change** triggers re-screen.
4. **Transaction-trigger rescreen**: any tx ≥ threshold (e.g., $10k cash, $3k wire) auto-screens counterparty.

Generate `monitor_cron.py` + alert dispatcher (Slack, PagerDuty, Jira).

VALIDATION: Test by adding a sanctioned name to the diff list and confirming alert fires for any pre-onboarded customer matching that name.

============================================================
=== PHASE 6: CASE MANAGEMENT UI SCAFFOLD ===
============================================================

Compliance analysts need to disposition cases. Generate a minimal UI (Next.js app router or Streamlit) with:

- Case queue (priority sorted)
- Customer profile + screening hits side-by-side
- Disposition: CLEAR (false positive), ESCALATE (to MLRO), FILE SAR (suspicious activity), BLOCK
- Required fields per disposition (justification, supporting docs)
- Two-eyes review for SAR / BLOCK actions
- Audit trail (who clicked what when)

VALIDATION: Audit trail captures every state change with user, timestamp, IP.

============================================================
=== PHASE 7: SAR (FORM 111) HELPER ===
============================================================

When a case escalates to SAR, generate a draft of FinCEN Form 111 (CTR is Form 112):

- Filing institution info (pre-filled from org config)
- Subject info (from customer record)
- Suspicious activity type codes (FinCEN list — terrorism financing, structuring, money laundering, etc.)
- Activity dates and dollar amounts
- Narrative (5W+H — who, what, when, where, why, how) with the screening evidence summarized

Compliance officer reviews + files via BSA E-Filing System. Skill does NOT auto-file — narrative drafting only.

VALIDATION: Narrative covers all 5W+H. Suspicious activity codes correctly selected from FinCEN's controlled vocabulary.

============================================================
=== SELF-REVIEW ===
============================================================

Score 1–5:

- **Complete**: All 7 phases delivered? Lists ingest? Matching tunable? UI scaffolded?
- **Robust**: Matching handles transliteration + aliases + typos? False positive rate measurable?
- **Clean**: Decisions auditable, append-only? Auto-block ONLY on confirmed sanctions match (not PEP)?
- **Compliance-credible**: Would an MLRO at a regulated fintech (bank, broker-dealer, crypto exchange) sign off?

Common gap: blocking PEPs by default instead of EDD-ing them. PEP ≠ sanctioned; flag for review, don't auto-block.

============================================================
=== LEARNINGS CAPTURE ===
============================================================

Append to `~/.claude/skills/kyc-aml-screener/LEARNINGS.md`:

## <YYYY-MM-DD> — <regime, volume, customer type>

- **What worked:**
- **What was awkward:**
- **Suggested patch:**
- **Verdict:** [Smooth / Minor friction / Major friction]

============================================================
=== STRICT RULES ===
============================================================

- Never auto-block on PEP match alone. PEPs are legal customers requiring EDD, not prohibited.
- Never silently drop a sanctions match. False negative = compliance violation = personal liability + bank-wide fines.
- Never store screening results without an audit trail. Regulators reconstruct the decision chain in exams.
- Never compute match score without dob/country disambiguation when available. Name alone produces too many false positives.
- Never deploy without nightly list refresh. Stale OFAC = the day after a designation lands you're exposed.
- Always document the matching threshold rationale. "Why 0.85?" comes up in every BSA exam.
