---
name: checkout-audit
description: "Audit an ecommerce checkout flow against the 2026 conversion playbook. Triggers: \"checkout audit\", \"checkout optimization\", \"Shopify checkout\", \"Stripe checkout\", \"Apple Pay\"."
version: "1.0.1"
category: analysis
platforms:
  - CLAUDE_CODE
---

# Checkout Conversion Audit

You audit a checkout funnel against the 2026 conversion playbook. The math: Baymard's 2026 meta-analysis of 50+ studies puts the average cart abandonment at 70.22%. Best-in-class checkouts achieve 30-40%. The gap is mostly fixable.

Baseline opportunity sizes:

- One-page checkout: -20% abandonment vs multi-step
- Express checkout above fold: 2× conversion vs at-end (Stripe)
- Apple Pay enabled: +22.3% conversion, +22.5% revenue
- Shop Pay returning customer: +50%
- Apple/Google Pay clicks: 4 vs 120 traditional

============================================================
=== PRE-FLIGHT ===
============================================================

- [ ] **Site URL** + ability to walk through checkout (test card, sandbox mode).
- [ ] **Platform**: Shopify (with or without Hydrogen / headless), WooCommerce, BigCommerce, Stripe Checkout, custom React, Magento, Salesforce Commerce.
- [ ] **Region**: US-only, multi-region, EU (Strong Customer Authentication required), APAC.
- [ ] **Mobile share**: typically 60-75%. Drives priority on mobile-specific findings.
- [ ] **Avg order value (AOV)**: drives BNPL relevance (Klarna/Afterpay/Affirm shine > $100).

Recovery:

- Can't walk checkout (auth-walled cart, requires real product): generate test product and full E2E flow.
- Custom CSR checkout that's hard to instrument: layer in PostHog session replay or LogRocket for drop-off attribution.

============================================================
=== PHASE 1: FUNNEL STEP MAP ===
============================================================

Walk the checkout, recording every step + every required field + every click:

```yaml
funnel:
  - step: cart
    fields_required: []
    clicks_to_advance: 1
    drop_off_observed: 10-15% # baseline
  - step: contact
    fields_required: [email]
    clicks_to_advance: 1
    drop_off_observed: 8-12%
  - step: shipping_address
    fields_required:
      [first_name, last_name, address1, city, state, zip, country, phone]
    clicks_to_advance: 1
    drop_off_observed: 15-25% # biggest leakage in poor flows
  - step: shipping_method
    fields_required: []
    clicks_to_advance: 1
    drop_off_observed: 5-10%
  - step: payment
    fields_required: [card_number, exp, cvc, billing_address]
    clicks_to_advance: 1
    drop_off_observed: 10-15%
  - step: review_and_pay
    fields_required: []
    clicks_to_advance: 1
```

Each step = a drop-off opportunity. Goal: ≤ 3 steps mobile, ≤ 4 steps desktop.

VALIDATION: Step map captures real flow, not assumed. Field count per step is exact.

============================================================
=== PHASE 2: EXPRESS CHECKOUT AUDIT ===
============================================================

| Express Method                 | Required for                                     | Position                                                       |
| ------------------------------ | ------------------------------------------------ | -------------------------------------------------------------- |
| **Apple Pay**                  | All Safari/iOS users (60%+ of US mobile)         | ABOVE shipping form, not "or pay another way"                  |
| **Google Pay**                 | All Android Chrome users                         | Adjacent to Apple Pay                                          |
| **Shop Pay**                   | Shopify stores (massive returning-customer lift) | Top of checkout                                                |
| **PayPal**                     | Cross-platform; older demo + cross-border        | Express button OR payment-method                               |
| **Amazon Pay**                 | Amazon-loyal demo (saves 2-step)                 | Optional, evaluate per AOV                                     |
| **Klarna / Afterpay / Affirm** | AOV > $50                                        | Both cart AND payment step (cart messaging boosts add-to-cart) |

**Audit checks**:

- [ ] Express buttons render BEFORE shipping form (above the fold)
- [ ] Apple Pay button correctly displays on Safari + iOS (test in actual Safari, not Chrome dev tools — Apple Pay uses Webkit API)
- [ ] No "and / or" framing that buries express options
- [ ] Express buttons have correct styling (Apple's brand guidelines specific)

VALIDATION: Express checkout available at the FIRST point of checkout, not buried at the bottom.

============================================================
=== PHASE 3: GUEST CHECKOUT + ACCOUNT TIMING ===
============================================================

Forced account creation is the #2 abandonment cause (24% per Baymard).

**Required**:

- [ ] Guest checkout offered prominently, NOT as a small link.
- [ ] Account creation offered AFTER purchase ("Create account in one click — your details are saved").
- [ ] Returning user lookup by email/phone (offer to sign in, but allow guest).
- [ ] Single email field, not "email" + "confirm email" (12% drop when duplicated).

VALIDATION: Guest checkout is at least as prominent as account checkout in the UI.

============================================================
=== PHASE 4: FORM FIELD MINIMIZATION ===
============================================================

Every additional field drops conversion ~7% (Baymard). Audit each field:

**Eliminate**:

- Phone number unless required for shipping (carrier delivery notifications use email)
- Company name unless B2B
- Address line 2 default-hidden (show on click)
- Birthdate unless age-restricted product

**Auto-fill / inference**:

- City + state from ZIP (US: zipcode-to-city API)
- Country from IP geolocation (let user change)
- Billing same-as-shipping (default checked)

**Smart validation**:

- Inline error messages, not page reload
- Email format check on blur
- Credit card type auto-detect (no manual selector)
- Address validation via Google Places / Stripe Address Element (typeahead reduces error rate 50%)

VALIDATION: Total checkout field count ≤ 8 for a US guest flow.

============================================================
=== PHASE 5: PAYMENT METHOD COVERAGE ===
============================================================

Region-aware payment menu:

| Region | Must-have methods                                                                                            |
| ------ | ------------------------------------------------------------------------------------------------------------ |
| US     | Card (Visa/MC/Amex/Discover), Apple Pay, Google Pay, Shop Pay (if Shopify), PayPal, ACH for high-AOV         |
| EU     | Card, Apple/Google Pay, iDEAL (NL), Bancontact (BE), SOFORT (DE/AT), Giropay (DE), Klarna, SEPA Direct Debit |
| LatAm  | Card, OXXO (MX), Boleto (BR), Pix (BR), MercadoPago                                                          |
| APAC   | Card, Apple/Google Pay, Alipay (CN), WeChat Pay (CN), GrabPay (SEA), PayNow (SG), UPI (IN)                   |
| MENA   | Card, Apple Pay, COD prominent (for trust)                                                                   |

VALIDATION: Region detection (IP / billing country) drives payment menu. Don't show iDEAL to US buyers; don't show Pix to EU.

============================================================
=== PHASE 6: COST TRANSPARENCY ===
============================================================

Unexpected shipping costs = #1 abandonment cause (48% per Baymard). Audit:

- [ ] Shipping estimate shown ON cart page (not first-revealed at checkout)
- [ ] Free shipping threshold messaging ("Spend $15 more for free shipping")
- [ ] Tax included or labeled clearly (some regions show tax-inclusive prices)
- [ ] Customs / import fees disclosed for international (DDP vs DDU)
- [ ] No "service fees" or "convenience fees" introduced at the last step

VALIDATION: Order total shown at checkout matches order total shown on cart. No surprise additions > 5%.

============================================================
=== PHASE 7: MOBILE-SPECIFIC AUDIT ===
============================================================

Mobile checkout has different failure modes:

- [ ] Tap targets ≥ 44×44 px
- [ ] Inputs have correct `inputmode` (numeric for card, email for email, tel for phone)
- [ ] No zoom-on-focus on inputs (set `font-size: 16px` minimum)
- [ ] Native autofill compatible (`autocomplete` attributes correct per WHATWG)
- [ ] Sticky CTA bar at bottom (always-visible "Complete order")
- [ ] No mid-checkout app-install prompts
- [ ] CardScan via device camera (iOS / Android Pay Request API)

VALIDATION: Test on actual iOS Safari + Android Chrome, not desktop dev tools.

============================================================
=== PHASE 8: PRIORITIZED PUNCH LIST ===
============================================================

Generate `checkout_audit_{date}.md`:

```markdown
# Checkout Audit — {site} — {date}

## Current state

- Steps: N
- Express checkout: Apple Pay {present/missing}, Google Pay {present/missing}, Shop Pay {present/missing}
- Guest checkout: {prominent/buried/missing}
- Field count: N
- Mobile checkout: {smooth/issues}
- Estimated current abandonment: {x}%

## P0 — Highest impact

- [ ] Add Apple Pay above fold. Expected lift: +22% conversion. Effort: 2 hours via Stripe Payment Element.
- [ ] Enable guest checkout. Expected lift: +25% from forced-account abandonment population. Effort: 4 hours.

## P1 — High impact

- [ ] Reduce form fields from 14 to 8. Expected lift: +35%. Effort: 8 hours UX + backend.
- [ ] Show shipping estimate on cart page. Expected lift: +20% (eliminates #1 abandonment cause). Effort: 6 hours.

## P2 — Medium

- [ ] Move from 4-step to 1-page checkout. Expected lift: +20%. Effort: 2-4 days.
- [ ] Add Klarna/Afterpay/Affirm for AOV > $50. Expected AOV lift: +15%. Effort: 1 week.

## P3 — Polish

- [ ] Sticky bottom CTA on mobile. Effort: 2 hours.

## Re-audit after fixes

Re-run `/checkout-audit` after each P0/P1 ships.
```

VALIDATION: Each item has expected lift (numeric) + effort + concrete fix.

============================================================
=== SELF-REVIEW ===
============================================================

- **Complete**: All 8 phases run? Step map + express + guest + fields + payment + cost + mobile + punch list?
- **Robust**: Tested in actual Safari/iOS + Android Chrome, not just desktop dev tools?
- **Clean**: Punch list prioritized by impact × effort, not by alphabet?
- **CRO-credible**: Would a Baymard-trained CRO consultant accept this audit as production-ready?

Common gap: missing actual mobile test → desktop dev-tools "looks fine" while real Safari has zoom-on-focus killing 30% of mobile.

============================================================
=== LEARNINGS CAPTURE ===
============================================================

`~/.claude/skills/checkout-audit/LEARNINGS.md`.

============================================================
=== STRICT RULES ===
============================================================

- Never audit without walking the actual flow. Code review alone misses runtime issues.
- Never report "fix XYZ" without measuring impact. Every recommendation needs an expected lift.
- Never recommend disabling guest checkout to "capture more leads." Capture lift is < lift from removing the gate.
- Never display payment methods irrelevant to the user's region.
- Always test on real mobile devices, not browser device emulation.
