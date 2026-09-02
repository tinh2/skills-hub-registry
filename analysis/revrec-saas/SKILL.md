---
name: revrec-saas
description: "Generate an ASC 606 / IFRS 15 revenue recognition engine for SaaS — the five-step model (identify contract, identify performance obligations, determine transaction price, allocate to performance obligations, recognize as POs are satisfied) applied to subscription contracts."
version: "1.0.1"
category: analysis
platforms:
  - CLAUDE_CODE
---

# ASC 606 / IFRS 15 Revenue Recognition Engine for SaaS

You generate a production-grade revenue recognition engine. ASC 606 (Topic 606) and IFRS 15 are converged standards — same five-step model — applied differently to SaaS than to product sales. Getting it wrong is a material weakness; getting it right earns a clean audit.

The core rule: **revenue is recognized when (or as) you satisfy a performance obligation**, not when cash is received. A customer paying $12k for an annual subscription generates $1k/month of recognized revenue, not $12k on day one. The contract value sits in **deferred revenue** until performed.

============================================================
=== PRE-FLIGHT ===
============================================================

Verify:

- [ ] **Reporting standard**: US GAAP (ASC 606) or IFRS (IFRS 15). Identical model, footnote differences.
- [ ] **Contract types in scope**: standard subscription, multi-year, ramp deals (e.g., $5k/mo year 1, $10k/mo year 2), usage-based, hybrid (committed + overage), one-time license + maintenance.
- [ ] **Billing platform**: Stripe (subscriptions + metered), Chargebee, Maxio (Stax Bill), Recurly, Zuora, custom. Drives where billing events come from.
- [ ] **Implementation / training / data migration**: sold separately or bundled? If bundled, may need SSP allocation.
- [ ] **Contract acquisition costs**: sales commissions, broker fees — capitalize per ASC 340-40 if amortization period > 1 year.
- [ ] **Audit posture**: pre-revenue (no audit yet), SOC 2 for ops, full SOX (public or pre-IPO).

Recovery:

- If contract structure is simple (single SaaS subscription, no implementation, monthly billing), reduce to the minimum viable engine: pro-rate over service period, recognize ratably.
- If contracts are complex (ramps, modifications, usage tiers), surface that complexity is real and outputs require accounting review.

============================================================
=== PHASE 1: STEP 1 — IDENTIFY THE CONTRACT ===
============================================================

ASC 606 contract criteria (must meet ALL):

1. Parties have approved the contract (written, oral, or implied) and are committed.
2. Each party's rights are identifiable.
3. Payment terms are identifiable.
4. Contract has commercial substance.
5. Collection is **probable** (more likely than not).

Generate `contract.py` capturing:

```python
@dataclass
class Contract:
    id: str
    customer_id: str
    signed_date: date
    start_date: date
    end_date: date  # subscription term
    contract_value_committed: Decimal  # MRR × months OR fixed total
    payment_terms: PaymentTerms
    auto_renews: bool
    cancellation_terms: CancellationTerms
    related_contracts: list[str]  # for combined-contracts analysis
```

**Contract combination rule**: separate written contracts may need to be combined if (a) negotiated as a package, (b) consideration in one depends on the other, or (c) services are a single PO. Flag this on signed-date proximity (within 30 days) for human review.

VALIDATION: Contract object captures collectibility assessment. Combination candidates flagged.

============================================================
=== PHASE 2: STEP 2 — IDENTIFY PERFORMANCE OBLIGATIONS ===
============================================================

A performance obligation is a **distinct** promise. Test for distinct:

1. Can the customer benefit from the good/service on its own or with other readily-available resources?
2. Is the promise separately identifiable from other promises in the contract?

**Common SaaS PO splits**:

| Item                       | Typical PO treatment                                                                                             |
| -------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| Subscription access        | **Single PO** — series of distinct daily services, recognized over time                                          |
| Implementation services    | If material modification of platform → **bundled with subscription**; if standalone capability → **separate PO** |
| Data migration             | Usually bundled (no value without subscription)                                                                  |
| Training                   | Often separate PO if generic; bundled if proprietary                                                             |
| Customer success / CSM     | Usually subsumed into subscription (no standalone value)                                                         |
| Custom development         | Separate PO if customer takes title to IP                                                                        |
| Premium support tier       | Separate PO (distinct value)                                                                                     |
| Setup fee (non-refundable) | **Not a PO** — material right or up-front payment → recognized over expected customer life                       |

Generate `performance_obligations.py` that takes a contract and outputs a list of PO records with `recognition_pattern` enum: `OVER_TIME_RATABLE`, `OVER_TIME_USAGE`, `OVER_TIME_INPUT_METHOD`, `POINT_IN_TIME`.

VALIDATION: Standard subscription = 1 PO recognized ratably. Implementation w/ standalone value = 2 POs.

============================================================
=== PHASE 3: STEP 3 — DETERMINE TRANSACTION PRICE ===
============================================================

Total consideration the entity expects, including:

- Fixed consideration (subscription fee × term)
- **Variable consideration** (usage overage, performance bonuses, refunds) — estimate using EITHER expected value OR most-likely-amount, whichever better predicts.
- **Constraint on variable consideration**: only include amounts not subject to "significant revenue reversal" — i.e., be conservative on usage estimates that haven't materialized.
- **Significant financing component** (if payment is > 1 year before/after performance) — discount to present value.
- **Non-cash consideration** at fair value.
- **Consideration payable to customer** (rebates, credits) — reduce transaction price.

Generate `transaction_price.py` with:

```python
def determine_transaction_price(contract: Contract, usage_forecast: UsageForecast) -> Decimal:
    fixed = contract.committed_value
    variable = constrained_expected_value(usage_forecast)
    financing_adj = discount_if_significant(contract.payment_terms)
    rebates = contract.consideration_payable_to_customer
    return fixed + variable - rebates + financing_adj
```

VALIDATION: Variable consideration is constrained (not booked at gross-optimistic value).

============================================================
=== PHASE 4: STEP 4 — ALLOCATE TO POs ===
============================================================

If contract has multiple POs, allocate transaction price using **standalone selling prices** (SSP):

- **Observable SSP**: prices when items sold separately.
- **Adjusted-market-assessment SSP**: similar offerings in market.
- **Expected-cost-plus-margin SSP**: cost + reasonable margin.
- **Residual approach**: only when SSP highly variable or uncertain.

Generate `ssp_calculator.py` that pulls observed sale prices from billing platform history and computes per-item SSP. Allocation formula:

```
allocated_price_PO_i = transaction_price × (ssp_PO_i / sum(ssp_all_POs))
```

VALIDATION: Allocation sums to transaction price. SSP basis documented per PO (observable / adjusted-market / cost-plus / residual).

============================================================
=== PHASE 5: STEP 5 — RECOGNIZE AS POs ARE SATISFIED ===
============================================================

For OVER_TIME POs (subscription), pro-rate over the service period:

```
revenue_per_day = allocated_price / total_service_days
recognized_revenue_period = revenue_per_day × days_in_period
deferred_revenue_remaining = allocated_price - cumulative_recognized
```

For POINT_IN_TIME POs (e.g., one-time license, where customer gains control), recognize the full allocated amount when delivered/transferred.

For USAGE-BASED POs, recognize as usage is consumed.

Generate `recognition_engine.py` that takes contract + as-of date + previously recognized + usage data → emits new revenue and updated deferred balance per PO.

Generate journal entries (double-entry):

| Event                                                | Dr                              | Cr                              |
| ---------------------------------------------------- | ------------------------------- | ------------------------------- |
| Invoice issued (annual prepaid)                      | A/R                             | Deferred revenue                |
| Cash collected                                       | Cash                            | A/R                             |
| Month-end revenue recognition (1/12 of subscription) | Deferred revenue                | Subscription revenue            |
| Commission paid (capitalized per ASC 340-40)         | Contract acquisition cost asset | Cash                            |
| Commission amortization                              | Sales & marketing expense       | Contract acquisition cost asset |
| Contract modification (mid-term upgrade)             | (depends on type — see Phase 6) |                                 |

VALIDATION: Deferred revenue balance reconciles: `deferred = sum(invoiced_to_date) − sum(recognized_to_date) − sum(refunds_to_date)`.

============================================================
=== PHASE 6: CONTRACT MODIFICATIONS ===
============================================================

Mid-contract changes get one of three treatments:

1. **Separate contract** — if mod adds distinct PO AND price reflects SSP of added items → account prospectively as new contract.
2. **Termination of old + creation of new** — if remaining goods/services are distinct from those already provided → reset blended price prospectively.
3. **Modification of existing contract** — if remaining goods/services NOT distinct from already-provided → cumulative catch-up adjustment.

Common cases:

- **Upgrade mid-term**: usually case 2 (new blended rate over remaining term).
- **Adding seats**: usually case 1 (new PO).
- **Downgrade**: case 2 (new lower blended rate prospectively).
- **Cancellation with refund**: refund reduces transaction price; reverse recognized revenue if applicable.

Generate `modifications.py` that classifies and computes the right adjustment.

VALIDATION: Each modification path tested with a fixture (upgrade, add-seats, downgrade, cancel).

============================================================
=== PHASE 7: COMMISSIONS (ASC 340-40) ===
============================================================

Sales commissions paid to obtain a contract are capitalized if the amortization period > 1 year (practical expedient for shorter periods). Amortize over **expected customer life**, not just initial contract term.

Generate `commissions.py`:

- Record commission as asset on payment.
- Amortize over expected life (e.g., 5 years for a 1-year contract with 80% renewal rate).
- Impair if customer churns.

VALIDATION: Asset balance reconciles to expected-life amortization schedule.

============================================================
=== PHASE 8: DISCLOSURES ===
============================================================

ASC 606 footnote requirements:

1. **Disaggregation of revenue** — by product line, geography, contract type, customer type.
2. **Contract balances** — receivables, contract assets, contract liabilities (deferred revenue), with rollforward.
3. **Remaining performance obligations** — disclose if expected to recognize more than 1 year out (with amount + when).
4. **Significant judgments** — variable consideration estimation, SSP method, PO identification.
5. **Costs to obtain a contract** — capitalized balance + amortization period.

Generate `disclosures.md` template with placeholders auto-filled from the engine's state.

VALIDATION: Disclosures cover all five required categories.

============================================================
=== SELF-REVIEW ===
============================================================

Score 1–5:

- **Complete**: All 5 steps + modifications + commissions + disclosures delivered?
- **Robust**: Edge cases handled (mid-term mods, refunds, ramp deals, usage-based)?
- **Clean**: Journal entries balance? Deferred revenue reconciles to invoiced − recognized?
- **Audit-credible**: Would a Big Four manager accept the engine output as ASC 606 compliant?

Common gap: treating non-refundable setup fees as POs. They're material-right / up-front consideration recognized over expected customer life, not at contract start.

============================================================
=== LEARNINGS CAPTURE ===
============================================================

Append to `~/.claude/skills/revrec-saas/LEARNINGS.md`:

## <YYYY-MM-DD> — <contract structure, complexity>

- **What worked:**
- **What was awkward:**
- **Suggested patch:**
- **Verdict:** [Smooth / Minor friction / Major friction]

============================================================
=== STRICT RULES ===
============================================================

- Never recognize cash receipt as revenue. Cash and revenue are independent under accrual accounting.
- Never skip the collectibility threshold. If collection is not probable, you don't have an ASC 606 contract.
- Never book variable consideration at gross-optimistic. Constrain to amounts not subject to significant reversal.
- Never amortize commissions over the initial contract term alone — use expected customer life including renewals.
- Always classify contract modifications before booking the change. Three different treatments produce three different P&L paths.
- Always reconcile deferred revenue monthly. Drift = audit finding.
