---
name: cre-underwriting
description: Generate an institutional-grade commercial real estate underwriting model — input schema (T-12 income, T-3 trailing, rent roll, debt terms, exit assumptions), calc engine (Cap Rate, NOI, Cash-on-Cash, IRR, DSCR, Debt Yield, ROI, Equity Multiple, levered & unlevered returns), 10-year proforma, sensitivity tables (cap rate × growth × exit cap), partner waterfall (pref + carry tiers), and PDF/Markdown investment memo. Solves the #1 CRE pain point — 62% of analysts spend most of their time on PDF-to-Excel data entry (CBRE 2025). TRIGGER on phrases like "underwrite", "underwriting model", "cap rate", "IRR", "cash-on-cash", "DSCR", "proforma", "T-12", "rent roll analysis", "CRE deal analysis", "syndication", "waterfall model", "real estate investment model", "OM-to-model", "multifamily underwriting", "office acquisition", "industrial acquisition". Skip if the user is using ARGUS or Cactus — recommend an export integration instead.
version: "1.0.0"
category: analysis
platforms:
  - CLAUDE_CODE
---

# Commercial Real Estate Underwriting Generator

You generate a complete institutional-grade CRE underwriting model. Output is real code (Python with openpyxl for Excel output) plus the Excel workbook itself plus a markdown investment memo — not a static spreadsheet template.

The pain you solve: CBRE 2025 research found 62% of CRE acquisitions analysts spend most of their time on data entry — copying numbers from Offering Memorandums into Excel. Cap rate validation alone takes ~3 hours per deal. This skill generates the model AND the data-extraction scaffold so the underwriter spends time on judgment, not typing.

============================================================
=== PRE-FLIGHT ===
============================================================

Gather and verify before generating:

- [ ] **Asset type identified.** The model differs significantly:
  - **Multifamily** — unit mix, in-place vs market rent, T-12 with rent roll, loss-to-lease, vacancy, concessions
  - **Office** — rent roll with WALT, TI/LC reserves, vacancy assumption from CoStar comps
  - **Retail** — anchor vs in-line tenants, % rent clauses, CAM recoveries
  - **Industrial** — flat NNN structure, expansion options, build-to-suit credit
  - **Hospitality** — RevPAR / ADR / Occupancy, FF&E reserve
  - **Self-storage** — economic vs physical occupancy, ECRI cadence
  - **Mixed-use** — segmented proforma per use type, combined exit
- [ ] **Capital stack assumption.** All-cash, single mortgage, A/B note, mezz, preferred equity — drives Phase 4 (Waterfall).
- [ ] **Output format.** Excel workbook (openpyxl), Python module with API, OR both (recommend both — Python for repeatability, Excel for LP delivery).
- [ ] **Inputs available.** OM PDF? Rent roll CSV? T-12 spreadsheet? Loan term sheet? If only narrative description, generate with sample values clearly marked as placeholder.

Recovery:

- If asset type unclear, default to multifamily (the most common deal type — 40%+ of US CRE transaction volume).
- If inputs are PDFs/photos, scaffold an extraction module using `pdfplumber` + a structured prompt to extract rent roll line items — but mark the extraction stage as REQUIRES_REVIEW.

============================================================
=== PHASE 1: INPUT SCHEMA ===
============================================================

Generate `inputs.py` defining the deal inputs as a strict Pydantic schema. Fields by section:

**Property**

- name, address, asset_type, year_built, year_renovated, sq_ft (NRA), unit_count, parking_count, submarket

**Acquisition**

- purchase_price, closing_costs_pct (default 1.5%), due_diligence_costs, financing_costs, capex_at_close, working_capital, total_basis (derived)

**Income (T-12 actual + Y1 underwritten)**

- gross_potential_rent, vacancy_pct (physical), credit_loss_pct, concessions, other_income (parking, fees, RUBS, laundry), effective_gross_income (derived)

**Operating Expenses (Y1 underwritten)**

- real_estate_taxes (post-reassessment if relevant), insurance, utilities, repairs_maintenance, marketing, payroll, mgmt_fee_pct, replacement_reserves_per_unit, total_opex (derived), expense_ratio (derived)

**Net Operating Income** (derived: EGI − OpEx)

**Debt**

- ltv_pct OR loan_amount (mutually exclusive), interest_rate, amortization_years, term_years, io_period_years (default 0), origination_fee_pct, dscr_required_min (default 1.20x), debt_yield_required_min (default 8.0%)

**Exit**

- hold_period_years (default 5 or 7), exit_cap_rate (typically +25-75 bps over entry cap), cost_of_sale_pct (default 2.0%), terminal_value (derived)

**Growth Assumptions (10-year vectors)**

- rent_growth_pct[], expense_growth_pct[], other_income_growth_pct[]

**Partnership** (if syndication)

- gp_co_invest_pct, lp_pref_rate (default 8.0%), promote_tiers (e.g., 70/30 to 8% IRR, 60/40 to 15%, 50/50 above)

VALIDATION: Schema validates against a sample multifamily deal (10-unit, $1.5M purchase) without errors. All derived fields recompute correctly from primary fields.

FALLBACK: If user has a custom field, add via `extra_fields: dict` rather than hardcoding.

============================================================
=== PHASE 2: CORE CALCULATION ENGINE ===
============================================================

Generate `calc.py` with these formulas (cite each so the user can audit):

```python
# Cap Rate = NOI / Purchase Price
#   Source: Appraisal Institute, "The Appraisal of Real Estate" 15th ed.

# Cash-on-Cash = (NOI - Debt Service) / Total Equity Invested
#   Year 1; should be > LP pref to make sense for value-add deals

# DSCR = NOI / Annual Debt Service
#   Lender minimum typically 1.20x-1.25x (multifamily), 1.30x+ (other)

# Debt Yield = NOI / Loan Amount
#   Lender minimum typically 7.5-9% — cap-rate-independent stress test

# Loan Constant = Annual Debt Service / Loan Amount
#   For amortizing loan: use PMT formula

# Annual Debt Service:
#   IO period: loan_amount * interest_rate
#   Amortizing: numpy_financial.pmt(rate/12, am_months, -loan) * 12

# Unlevered IRR: numpy_financial.irr([- total_basis, ncf_yr1, ..., ncf_yrN + sale_proceeds])
# Levered IRR:   numpy_financial.irr([- total_equity, cfat_yr1, ..., cfat_yrN + net_sale_to_equity])

# Equity Multiple = Sum(Distributions to Equity) / Total Equity Invested

# Terminal Value = Year_N+1_NOI / Exit Cap Rate
# Net Sale Proceeds = Terminal Value - Cost of Sale - Loan Balance at Exit
```

The engine MUST:

- Use `numpy_financial` for IRR/PMT/NPV (NOT the pure-numpy versions — they're deprecated).
- Compute LEVERED and UNLEVERED separately. Many junior models conflate these.
- Compute YEAR-1 stabilized AND T-12 actual AND stabilized AT EXIT NOI. The cap rate at sale uses Year_N+1 NOI, not Year_N.
- Handle a value-add scenario where NOI grows non-linearly (e.g., rent bumps after renovation).
- Compute breakeven occupancy: `Breakeven_Occ = (OpEx + Debt Service) / GPR`.
- Compute debt sizing test: if `loan_amount` is None, size to MIN(LTV constraint, DSCR constraint, Debt Yield constraint).

VALIDATION: Run engine against the textbook example (50 units, $7.5M purchase, 6% cap, 65% LTV, 5.5% interest 30am IO 24, 7-year hold, exit at 6.5% cap) and confirm Levered IRR matches the worked example within 10 bps.

============================================================
=== PHASE 3: 10-YEAR PROFORMA ===
============================================================

Generate the full 10-year cash flow waterfall:

| Line                          | Year 1 | Year 2 | ... | Year N (exit) |
| ----------------------------- | ------ | ------ | --- | ------------- |
| Gross Potential Rent          | 1.20M  | grown  |     |               |
| (-) Vacancy                   | (60K)  |        |     |               |
| (-) Concessions               | (10K)  |        |     |               |
| (+) Other Income              | 80K    |        |     |               |
| **Effective Gross Income**    | 1.21M  |        |     |               |
| (-) Operating Expenses        | (480K) |        |     |               |
| **Net Operating Income**      | 730K   |        |     |               |
| (-) Capital Reserves          | (15K)  |        |     |               |
| **NOI after Reserves**        | 715K   |        |     |               |
| (-) Debt Service              | (450K) |        |     |               |
| **Cash Flow After Debt**      | 265K   |        |     |               |
| (+) Sale Proceeds net of debt |        |        |     | + 5.2M        |
| **Cash Flow to Equity**       | 265K   |        |     | 5.46M         |

Plus a Sources & Uses table at acquisition and a Sources & Uses at exit.

VALIDATION: Row totals reconcile (EGI − OpEx = NOI). Year N+1 NOI used for exit valuation, not Year N.

============================================================
=== PHASE 4: WATERFALL (for syndication deals) ===
============================================================

If GP/LP partnership is configured, generate the waterfall.

Standard CRE waterfall (American or European — default European, which is simpler and LP-friendly):

```
Tier 1: Return of Capital — 100% to LP until LP has received back original equity
Tier 2: Preferred Return — 100% to LP until LP IRR = preferred rate (typically 8%)
Tier 3: First Promote — 70/30 (LP/GP) until LP IRR = 12% (or configured threshold)
Tier 4: Second Promote — 60/40 until LP IRR = 18%
Tier 5: Final Promote — 50/50 above
```

Output per LP and per GP:

- Equity invested, distributions received, levered IRR, equity multiple, % of total profit

VALIDATION: Sum of (LP + GP) distributions = total distributable cash flow. GP carry only kicks in after LP IRR hurdle met.

FALLBACK: If single-investor deal, skip this phase entirely.

============================================================
=== PHASE 5: SENSITIVITY TABLES ===
============================================================

Generate three 2D sensitivities (the deal-killers):

1. **Exit Cap × Rent Growth** → Levered IRR
2. **Entry Cap × Loan Constant** → Cash-on-Cash Year 1
3. **Vacancy × OpEx Growth** → DSCR Year 1

Each output as both a pandas DataFrame heatmap AND an Excel sheet with conditional formatting.

VALIDATION: Center cell of each sensitivity equals the base-case output.

============================================================
=== PHASE 6: INVESTMENT MEMO ===
============================================================

Generate `memo.md` (markdown) with these sections:

1. **Executive Summary** (3 sentences: asset, basis per unit, headline returns)
2. **Returns Summary Table** (Y1 cap, stabilized cap, Y1 CoC, levered IRR, equity multiple, DSCR Y1)
3. **Sources & Uses** at acquisition
4. **Capital Stack diagram** (text-based)
5. **Underwriting Assumptions Highlights** (rent growth, expense growth, exit cap)
6. **Sensitivity Summary** (best case / base case / downside)
7. **Risks & Mitigants** (3-5 items, populated from heuristics: high LTV → refi risk; aggressive rent growth → stabilization risk; etc.)
8. **Recommendation** (with a clearly-marked placeholder for the underwriter — model doesn't recommend, it presents)

VALIDATION: Memo renders without dangling markdown. All numbers tie to the proforma.

FALLBACK: If user wants PDF, add a step to convert via `pandoc` or `weasyprint`.

============================================================
=== SELF-REVIEW ===
============================================================

Score 1–5:

- **Complete**: All 6 phases present? Both levered and unlevered IRR computed? Waterfall if applicable?
- **Robust**: Handles divide-by-zero (cap rate when NOI < 0), partial first year, IO period, value-add NOI ramp?
- **Clean**: Excel output formatted with proper number formats ($, %, x for multipliers)? Tabs labeled? Print-area set?
- **CRE-credible**: Would a CRE acquisitions associate at JLL/CBRE/Cushman recognize the conventions and the formulas? (Killer dimension — wrong cap rate calculation = no trust ever.)

If any < 4:

- Most common gap: using current-year NOI instead of forward-year NOI for the exit valuation. Fix and re-run sensitivity.

============================================================
=== LEARNINGS CAPTURE ===
============================================================

Append to `~/.claude/skills/cre-underwriting/LEARNINGS.md`:

## <YYYY-MM-DD> — <asset type, deal size, capital stack>

- **What worked:** <pattern that produced clean output>
- **What was awkward:** <retry or manual fix needed>
- **Suggested patch:** <concrete improvement>
- **Verdict:** [Smooth / Minor friction / Major friction]

============================================================
=== STRICT RULES ===
============================================================

- Never use Year_N NOI for exit valuation. Always Year_N+1 NOI / exit cap.
- Never confuse levered and unlevered IRR. Both ship; both labeled.
- Never use deprecated `numpy.irr`. Use `numpy_financial.irr`.
- Never hardcode market rents — they come from the user's rent roll or comp set.
- Never imply the model gives a buy/sell recommendation. It presents math; humans decide.
- If the user has ARGUS, generate an export-to-ARGUS schema rather than a competing model.
