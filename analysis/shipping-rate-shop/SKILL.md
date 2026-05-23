---
name: shipping-rate-shop
description: Multi-carrier shipping rate comparison and label-generation pipeline — real-time quotes from USPS, UPS, FedEx, DHL via direct carrier APIs OR aggregators (Shippo / EasyPost / ShipStation / Pirate Ship). Handles 2026 rate landscape: FedEx/UPS/DHL each +5.9% GRI, USPS service-specific changes Jan 2026 + temporary 8% surcharge Apr 26 - Jan 17 2027. Carrier-strength heuristics built in: USPS dominates <1lb, UPS/FedEx win >10-15lbs, DHL eCommerce <4.4lbs international. Account-specific discount layering, variable-pricing-aware (UPS/FedEx/DHL use lane + volume models, not fixed tables). Generates: rate-shop function, label purchase + tracking, address validation, dimensional weight calc, return label support, manifest creation, EDI/272 acknowledgment, carrier-pickup scheduling. TRIGGER on "shipping rates", "label generation", "carrier comparison", "EasyPost", "Shippo", "shipping API", "rate shop", "best shipping carrier", "USPS API", "UPS API".
version: "1.0.0"
category: analysis
platforms:
  - CLAUDE_CODE
---

# Multi-Carrier Shipping Rate Shop

You generate a complete multi-carrier shipping pipeline. The 2026 rate landscape rewards rate-shopping: FedEx/UPS/DHL each took +5.9% general rate increases, USPS implemented service-specific changes Jan 18, 2026 plus a temporary 8% surcharge from Apr 26, 2026 through Jan 17, 2027. Static carrier choice leaves money on the table.

Carrier strength heuristics that hold in 2026:

- **USPS**: cheapest for packages under 1 lb (jewelry, supplements, poly-mailer goods).
- **UPS / FedEx**: win above 10-15 lbs and for guaranteed services.
- **DHL eCommerce**: international packages under 4.4 lbs, especially Europe/Asia.
- All three majors now use **variable pricing** based on lane mix + volume + historical data, not fixed rate tables.

============================================================
=== PRE-FLIGHT ===
============================================================

Verify:

- [ ] **Carrier accounts**: which carriers are negotiated? Direct API access (UPS Developer, FedEx Web Services, USPS Web Tools, DHL XML Services) OR aggregator (Shippo, EasyPost, ShipStation, Pirate Ship, Stamps.com)?
- [ ] **Volume estimate**: < 50/month → aggregator's published rate is fine. > 500/month → negotiate direct contracts with carriers. > 5k/month → talk to UPS/FedEx national account.
- [ ] **Package types**: parcels, freight (> 150 lb), pallets, hazmat? Skill targets parcel only — freight needs separate logic.
- [ ] **Destinations**: domestic only / international / both?
- [ ] **SLA tier**: economy (≥ 5 days) / standard (3-5) / 2-day / overnight?

Recovery:

- If no carrier accounts, default to EasyPost as aggregator scaffold (best free tier + comprehensive API). User can swap to Shippo, ShipStation later.
- If hazmat/freight detected, halt with a clear "this skill is parcel-only; use NMFC freight tooling for those" message.

============================================================
=== PHASE 1: RATE SHOP CORE ===
============================================================

Generate `rate_shop.py` (Python) or `rateShop.ts` (Node):

```python
def rate_shop(parcel, from_addr, to_addr, options={}):
    """
    Returns sorted list of carrier+service+rate quotes.
    parcel: {weight_oz, length_in, width_in, height_in}
    from_addr / to_addr: {name, street1, city, state, zip, country}
    options: {residential, signature_required, insurance_amount, saturday_delivery}
    """
    quotes = []
    for carrier_client in active_carriers():
        try:
            carrier_quotes = carrier_client.get_rates(parcel, from_addr, to_addr, options)
            quotes.extend(carrier_quotes)
        except RateRequestError as e:
            log.warning(f"{carrier_client.name} rates unavailable: {e}")
    return sorted(quotes, key=lambda q: (q['rate_usd'], q['delivery_days']))
```

Each quote has: `carrier`, `service`, `service_code`, `rate_usd`, `delivery_days`, `est_delivery_date`, `rate_id` (for label purchase later).

VALIDATION: Rate shop returns ≥ 2 carrier quotes for a sample 1-lb domestic shipment. If only 1 returns, surface the others' errors clearly.

============================================================
=== PHASE 2: DIMENSIONAL WEIGHT CALCULATION ===
============================================================

Dim weight catches teams off-guard. Each carrier has its own divisor:

| Carrier | Domestic divisor | International divisor |
| ------- | ---------------- | --------------------- |
| UPS     | 139              | 139                   |
| FedEx   | 139              | 139                   |
| USPS    | 166 (Priority)   | 166                   |
| DHL     | 139              | 139                   |

`billable_weight = max(actual_weight_lb, ceil((L × W × H) / divisor))`

Always compute and surface dim weight in the quote response so the user knows their effective billing weight, not just actual.

VALIDATION: Dim weight calc matches each carrier's published worksheet for a 14×10×6 box at 2 lb actual.

============================================================
=== PHASE 3: ADDRESS VALIDATION ===
============================================================

Bad addresses → returned packages → real cost. Run address validation before quoting:

- **USPS Web Tools / Address Information API** (free, ZIP+4 normalization).
- **EasyPost / Shippo verify_address** endpoint.
- **Lob US Verifications** ($0.30 / verification, gold standard).

Output: corrected address, residential/commercial flag, deliverability score. Residential flag matters — UPS Ground residential adds ~$5.50/package vs commercial.

VALIDATION: A known-bad address (e.g., "123 Fake St, San Francisco CA") returns deliverability="undeliverable" not silently accepted.

============================================================
=== PHASE 4: CARRIER-SPECIFIC SERVICES ===
============================================================

Pre-populate the service list per carrier with 2026-current codes:

**USPS**: Priority Mail, Priority Mail Express, Ground Advantage (replaced Retail Ground + First-Class Package in 2023), Media Mail.

**UPS**: UPS Ground, 3 Day Select, 2nd Day Air, Next Day Air, Next Day Air Saver, SurePost (USPS final-mile), Worldwide Express/Expedited/Saver/Standard.

**FedEx**: FedEx Ground, Home Delivery, Express Saver, 2Day, Standard Overnight, Priority Overnight, First Overnight, International Economy/Priority.

**DHL eCommerce**: SmartMail Parcel Expedited, SmartMail Parcel Plus Expedited, Parcel International Standard/Direct, Express Worldwide.

Each service has cutoff times by zone — show the latest "drop-off by X to ship today" in the quote.

VALIDATION: Service list matches each carrier's 2026 published codes. Cutoff times zone-aware.

============================================================
=== PHASE 5: LABEL PURCHASE + TRACKING ===
============================================================

Once a quote is selected, generate `purchase_label.py`:

1. Buy label via carrier API or aggregator (`POST /shipments/{rate_id}/buy`).
2. Receive label PDF/PNG/ZPL (thermal label) + tracking number.
3. Persist to DB: `tracking_number`, `carrier`, `service`, `rate_paid`, `purchased_at`, `from_addr`, `to_addr`.
4. Subscribe to tracking webhook (EasyPost Track endpoint, Shippo Tracker).
5. On status change, push to order DB (`label_created`, `picked_up`, `in_transit`, `out_for_delivery`, `delivered`, `exception`, `returned`).

For high-volume shippers, support **manifest creation** (end-of-day batch close) — required for USPS and reduces per-package fee.

VALIDATION: Buy-and-track round trip works against the carrier sandbox. Status webhook updates the DB within 60s.

============================================================
=== PHASE 6: SMART CARRIER ROUTING ===
============================================================

Pre-route the user to the right carrier based on package signal:

```python
def recommend_carrier(parcel, dest, urgency):
    """Heuristic-first, rate-shop-validated."""
    if parcel.weight_oz < 16 and dest.country == 'US' and urgency >= 3:
        candidates = ['USPS_Ground_Advantage', 'UPS_SurePost']
    elif parcel.weight_lb > 10 and dest.country == 'US':
        candidates = ['UPS_Ground', 'FedEx_Ground']
    elif dest.country != 'US' and parcel.weight_lb < 4.4:
        candidates = ['DHL_eCommerce', 'USPS_Priority_Intl']
    elif urgency == 1:  # next day
        candidates = ['UPS_Next_Day_Air_Saver', 'FedEx_Standard_Overnight', 'USPS_Priority_Mail_Express']
    else:
        candidates = ['ALL']
    return rate_shop_filtered(candidates)
```

Pair heuristics with rate-shop validation — heuristics narrow the field, real rates make the call.

VALIDATION: Recommendations match published carrier-strength patterns within 90% of test fixtures.

============================================================
=== PHASE 7: COST MONITORING ===
============================================================

Generate `cost_dashboard.sql` (or BigQuery / Snowflake equivalent) that reports weekly:

- Cost per package by carrier
- Cost per package by service
- Dim weight overage (where billable > actual)
- Rate-shop opportunity (where chosen carrier wasn't cheapest)
- Refund recovery (UPS/FedEx 60-second late-guarantee refunds; rebate vendors recoup 1-3%)

This is where the rate-shop ROI compounds. Without monitoring, savings drift.

VALIDATION: Dashboard query runs against the user's shipping data warehouse and surfaces ≥ 3 actionable findings.

============================================================
=== SELF-REVIEW ===
============================================================

Score 1–5:

- **Complete**: Rate shop + dim weight + address validation + labels + tracking + recommendations + monitoring all delivered?
- **Robust**: Falls back when one carrier API is down? Handles dim-weight overrides? Address validation runs pre-quote?
- **Clean**: API errors surfaced with cause, not silenced? Tracking persists to DB?
- **Logistics-credible**: Would a head of fulfillment recognize the carrier-strength heuristics and 2026 rate landscape as current?

Common gap: failing to compute dim weight → quote looks cheap but actual charge is 2-3× higher. Always surface billable weight.

============================================================
=== LEARNINGS CAPTURE ===
============================================================

Append to `~/.claude/skills/shipping-rate-shop/LEARNINGS.md`:

## <YYYY-MM-DD> — <vendor stack, volume, lane mix>

- **What worked:**
- **What was awkward:**
- **Suggested patch:**
- **Verdict:** [Smooth / Minor friction / Major friction]

============================================================
=== STRICT RULES ===
============================================================

- Never quote based on actual weight alone — always compute billable (dim) weight.
- Never ship without address validation. ~3% of US addresses are bad and the carrier bills you for the failed delivery + return.
- Never cache rates for more than 24 hours. Carrier variable pricing shifts on lane/volume — stale quotes lose money.
- Never silently fall back to one carrier when another's API errors out. Surface the failure so the user can request a refund or fix credentials.
- For high-volume shippers, never settle for published rates — negotiate direct contracts. Aggregator margins are 5-15%.
