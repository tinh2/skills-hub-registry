---
name: rental-underwriting
description: "Analyze a residential rental property as an investment — 1-4 unit single-family / duplex / triplex / quadplex, condo, townhome. Triggers: \"rental analysis\", \"rental underwriting\", \"cap rate calculator\", \"BRRRR\", \"DSCR loan\"."
version: "1.0.1"
category: analysis
platforms:
  - CLAUDE_CODE
---

# Residential Rental Underwriting

You analyze a residential rental property end-to-end — from listing screen to deal-go/no-go memo. Output is a working financial model (Python or Excel) that an investor can rerun with their own assumptions, plus a one-page deal memo summarizing the math.

============================================================
=== PRE-FLIGHT ===
============================================================

- [ ] **Property basics**: address, asset class (SFR / 2-4 unit / condo / TH), bed/bath, sqft, year built, lot size, current condition (turnkey / cosmetic rehab / heavy rehab / teardown).
- [ ] **Acquisition**: purchase price, closing costs, rehab budget, holding period.
- [ ] **Rental**: current rent (if leased) or market rent comp. Unit count + per-unit rent for multifamily.
- [ ] **Financing**: down payment %, interest rate, term, points, lender (conventional / DSCR / FHA / VA / hard money + refi).
- [ ] **Operating expenses**: property tax (county), insurance, HOA, utilities (LL pays vs tenant), PM fee %, vacancy %, maintenance %, capex reserve %.
- [ ] **Strategy**: long-term rental (LTR), short-term rental (STR), BRRRR (refi target), Section 8.

Recovery:

- If rent comp is missing, pull from Rentometer / Zillow Rental Manager / RentCast API → fall back to local CMA.
- If property tax unknown, estimate via county assessor's mill rate × assessed value (≈ purchase price × assessment ratio).

============================================================
=== PHASE 1: ACQUISITION COSTS ===
============================================================

```
Purchase Price                  $X
+ Closing Costs (2-3% buyer)    $X
+ Initial Rehab Budget          $X
+ Holding Costs (rehab period × $/mo)  $X
+ Lease-up / Reserves           $X
= Total Cash Invested (All-In Basis)    $X

If financed:
  Down Payment                  $X (purchase × DP%)
  Loan Amount                   $X
  Cash to Close = DP + Closing + Points + Initial Rehab + Holding + Reserves
```

VALIDATION: Cash to close ≤ user's available capital. If not, surface gap.

============================================================
=== PHASE 2: STABILIZED OPERATING STATEMENT ===
============================================================

```
Gross Potential Rent              $X (sum of monthly rents × 12)
Less: Vacancy & Credit Loss       ($X)  (5-10% typical, lower for Section 8)
= Effective Gross Income          $X

Operating Expenses:
  Property Tax                    $X
  Insurance                       $X
  HOA / Condo Fee                 $X
  Utilities (LL portion)          $X
  Repairs & Maintenance           $X (8-12% of EGI common rule of thumb)
  Property Management             $X (8-10% of collected rent)
  Lawn / Snow / Pool              $X
  Reserves (CapEx)                $X (5-10% of EGI to fund roofs, HVAC, water heaters)
  Other                           $X
= Total Operating Expenses        $X

Net Operating Income (NOI)        $X
Less: Annual Debt Service         $X
= Cash Flow Before Tax            $X
```

VALIDATION: Expense ratio plausible (35-50% of EGI for SFR; 40-55% for small multifamily).

============================================================
=== PHASE 3: KEY METRICS ===
============================================================

Compute and label all of:

| Metric                          | Formula                                                 | 2026 Target                   |
| ------------------------------- | ------------------------------------------------------- | ----------------------------- |
| **Gross Rent Multiplier (GRM)** | Purchase Price / Annual Gross Rent                      | < 10 = good, > 15 = thin      |
| **Cap Rate**                    | NOI / Purchase Price                                    | A: 4-6% / B: 6-8% / C: 8-12%  |
| **Cash-on-Cash Return**         | Annual CF Before Tax / Total Cash Invested              | 8-12% target                  |
| **DSCR**                        | NOI / Annual Debt Service                               | DSCR lenders want ≥ 1.25      |
| **Debt Yield**                  | NOI / Loan Amount                                       | ≥ 10% typical lender ask      |
| **Cap Rate vs Loan Constant**   | Cap Rate - Loan Constant                                | Positive = positive leverage  |
| **Break-even Occupancy**        | (OpEx + Debt Service) / GPR                             | < 80% is comfortable          |
| **Total ROI Year 1**            | (CF + Principal Paydown + Appreciation) / Cash Invested | 12-25% with leverage          |
| **1% Rule**                     | Monthly Rent / Purchase Price                           | ≥ 1% (HCOL-area exception)    |
| **2% Rule**                     | Same                                                    | ≥ 2% (low-cost market screen) |

Also project 10-year IRR with assumptions: rent growth (default 3% annual), expense growth (3%), appreciation (3-4%), exit cap rate (entry +25-50 bps).

VALIDATION: All metrics computed without div-by-zero. Negative leverage flagged.

============================================================
=== PHASE 4: BRRRR REFINANCE MATH ===
============================================================

If strategy = BRRRR, compute the refinance event explicitly:

```
After-Repair Value (ARV)             $X (comp-based)
× LTV (cash-out)                     75-80%
= New Loan Amount                    $X
Less: Existing Loan Payoff           ($X)
Less: Refi Closing Costs             ($X)
= Cash Out at Refi                   $X

Cash Invested After Refi:
  Original Cash Invested             $X
  Less: Cash Out at Refi             ($X)
  = Net Cash Left In                 $X (target ≤ original DP, ideally $0 — "infinite return")

Post-refi monthly cash flow:
  NOI                                 $X
  - New Debt Service                  $X
  = Cash Flow                         $X (must be positive)
```

VALIDATION: New debt service supportable by NOI (DSCR ≥ 1.20 post-refi). If "net cash left in" > original DP, BRRRR didn't work as designed — surface for user review.

============================================================
=== PHASE 5: SECTION 8 SCENARIO ===
============================================================

For affordable housing investors, run a side-by-side:

```
Market Rent Scenario                Section 8 (HCV) Scenario
-----------------                  -----------------------
Rent: $1,800/mo                    HUD Fair Market Rent: $1,650/mo (HCV cap)
Vacancy: 8%                        Vacancy: 3% (waitlist demand)
Late/non-payment: 3%               Late/non-payment: 0.5% (HUD direct deposit)
Turnover cost: $1,500              Turnover cost: $1,200 (longer tenancy)
Inspection cost: $0                Inspection cost: HQS annual + bi-annual
Marketing: $300/turnover           Marketing: PHA waitlist (zero)
```

Output side-by-side Year-1 cash flow comparison. Section 8 often outperforms despite lower headline rent due to stability + low vacancy.

VALIDATION: HCV FMR pulled from HUD's official table by zip + bedroom count.

============================================================
=== PHASE 6: DEAL MEMO ===
============================================================

Generate `deal_memo.md`:

```markdown
# Deal Memo — {Address}

**Strategy:** {LTR/STR/BRRRR/S8}  
**Purchase Price:** $X  
**All-in Basis:** $X  
**ARV / Stabilized Value:** $X

## Returns

- Cap Rate: X.X% (target {min} for {class})
- Cash-on-Cash: X.X% (target 8-12%)
- DSCR: X.XX (lender minimum 1.25)
- Year-1 Total ROI: XX% (incl. appreciation + paydown)
- 10-yr IRR: XX%

## Strengths

-

## Risks

-

## Recommendation

- [ ] Buy
- [ ] Pass
- [ ] Buy at lower price ($X max)
- [ ] Need more diligence (specify)
```

VALIDATION: Memo fits on one page. Metrics tie to the proforma.

============================================================
=== SELF-REVIEW ===
============================================================

- Complete: All 6 phases present? BRRRR + S8 scenarios if strategy matches?
- Robust: Handles div-by-zero? Flags negative leverage? Realistic expense %?
- Clean: Excel model + memo tie out exactly?
- Investor-credible: Would a BiggerPockets-active investor accept the analysis?

Common gap: forgetting reserves (CapEx for roof, HVAC, water heaters). Real numbers, not aspirational.

============================================================
=== LEARNINGS CAPTURE ===
============================================================

`~/.claude/skills/rental-underwriting/LEARNINGS.md` — what worked / awkward / patch / verdict.

============================================================
=== STRICT RULES ===
============================================================

- Never use a vacancy assumption of 0%. Realistic floor is 5%.
- Never skip CapEx reserves. Deferred maintenance kills cash flow long-term.
- Never present the 1% rule as a primary metric in HCOL markets. Use cap rate + CoC.
- Never assume rent grows at expense rate. Expenses (esp. insurance, taxes) often outpace rent growth.
- Always run sensitivity on rent (-10%) and rate (+1%) — that's where deals break.
