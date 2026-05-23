---
name: cart-recovery
description: Generate a multi-channel abandoned cart recovery sequence — SMS at 15 min (98% open rate, 25-40% conversion) followed by email cadence at 1hr / 24hr / 72hr, plus optional push and retargeting touchpoints. Cart-value-segmented (under $50 / $50-$150 / over $150) with discount discipline (no incentive in Email 1, free shipping in Email 2 for mid-tier, full discount only in final touchpoint). Generates: ESP-ready templates (Klaviyo, Postscript, Attentive, Sendlane, Omnisend), webhook handlers for Shopify/WooCommerce/BigCommerce/Stripe Checkout, dynamic product blocks with real cart items, inventory urgency only when stock < N (FTC-safe), suppression rules (purchased? stop the sequence), and revenue attribution tracking. Target recovery: 20-35% of carts. TRIGGER on "abandoned cart", "cart recovery", "cart abandonment", "Klaviyo flow", "win back lost sales", "browse abandonment", "checkout abandonment". Distinct from PDP work — this is post-cart, pre-payment.
version: "1.0.0"
category: analysis
platforms:
  - CLAUDE_CODE
---

# Abandoned Cart Recovery Sequence Generator

You generate a complete multi-channel cart abandonment recovery flow. Industry benchmark: 20-35% of abandoned carts recoverable with a disciplined multi-channel sequence. SMS-led sequences convert 25-40% (98% open rate); email-only converts 5-15%.

============================================================
=== PRE-FLIGHT ===
============================================================

Verify:

- [ ] **Commerce platform**: Shopify, WooCommerce, BigCommerce, Stripe Checkout, custom.
- [ ] **ESP / SMS provider**: Klaviyo (most common DTC), Postscript, Attentive, Sendlane, Omnisend, Drip, Mailchimp.
- [ ] **Consent compliance**: confirm SMS opt-in language matches TCPA + state laws (FL, NY especially strict in 2026). Email needs CAN-SPAM unsubscribe + physical address.
- [ ] **Discount strategy decided**: when can you give a discount, and how much? (Brand-protection caps matter.)
- [ ] **Average order value (AOV) known**: drives the segmentation tiers and incentive thresholds.

Recovery:

- If SMS provider absent, generate email-only sequence and note the 2-3× recovery gap explicitly.
- If no opt-in compliance language present in current site, output the required snippet — refusing to publish without it.

============================================================
=== PHASE 2: SEQUENCE TIMING ===
============================================================

Default sequence (mid-tier $50-$150 cart):

| Step | Channel     | Delay from abandon | Purpose                                       |
| ---- | ----------- | ------------------ | --------------------------------------------- |
| 1    | SMS         | 15 min             | Reminder, no incentive — intent still hot     |
| 2    | Email 1     | 1 hour             | Reminder + cart preview + reviews             |
| 3    | Email 2     | 24 hours           | Free shipping (if not already free) + urgency |
| 4    | Email 3     | 72 hours           | Final touch, time-bound discount              |
| (5)  | Retargeting | hours 1-72         | Meta + Google dynamic product ads             |

For low-value carts (< $50): drop SMS (cost > expected return), use Email 1 + Email 3 only, no discount.

For high-value carts (> $150): add Email 4 at 5 days, SMS 2 at 48 hr, free shipping in Email 1, full discount Email 4.

VALIDATION: Sequence config matches the user's AOV tier. Frequency cap honored (no double-send on same day).

============================================================
=== PHASE 3: TEMPLATE COPY ===
============================================================

Generate each touchpoint with platform-native dynamic tags.

**SMS @ 15min** (≤ 160 chars, single segment to control cost):

```
Hey {first_name}, your {top_item_name} is waiting. Grab it before it sells out: {short_url}
Reply STOP to opt out.
```

**Email 1 @ 1hr** — subject: "You left something behind 👀"

- Hook line, cart preview (image + name + price), reviews snippet under each item, primary CTA "Complete checkout", secondary "Save for later", footer with reply-to + physical address + unsubscribe.

**Email 2 @ 24hr** — subject: "Still thinking? Free shipping is on us"

- Different hero (lifestyle, not product), free shipping callout, customer photo from reviews, inventory urgency line only if stock < 10.

**Email 3 @ 72hr** — subject: "Last chance: 10% off your cart"

- Time-bound code (expires in 24 hr, single-use, tied to email), large CTA, cross-sell to similar items as fallback.

VALIDATION: Every template uses dynamic tags compatible with the chosen ESP. No hardcoded product names. Unsubscribe + opt-out present.

============================================================
=== PHASE 4: WEBHOOK HANDLERS ===
============================================================

Generate `checkout/abandoned.handler.{ts|py}` that fires on:

- Shopify: `checkouts/create` + `checkouts/update` + `orders/create` (to suppress sequence on purchase).
- WooCommerce: `woocommerce_cart_updated` action + `woocommerce_thankyou`.
- Stripe Checkout: webhook `checkout.session.async_payment_succeeded`, `expired`, `completed`.

The handler MUST:

1. Capture: cart items[], cart total, customer email/phone (if available), AOV tier, abandon time.
2. Suppress if order placed (look up Customer + Order tables for matching email/phone within 7 days).
3. Honor unsubscribe / STOP lists.
4. Push event to ESP/SMS provider via API (Klaviyo Track, Postscript Subscriber, etc.).

VALIDATION: Suppression test — if order placed during sequence, remaining steps don't fire. Test fixture covers this.

============================================================
=== PHASE 5: DYNAMIC PRODUCT BLOCKS ===
============================================================

Don't send "you left stuff behind" — show the actual items.

Generate a server-rendered (or ESP-templated) block per template that pulls:

- Item image (CDN-optimized, fixed aspect ratio so email renders cleanly).
- Item name + variant + price.
- Cart line subtotal.
- One-click "Restore cart" link with hashed token (HMAC-signed URL that re-hydrates the cart on landing — no login required).

VALIDATION: Email renders correctly in Litmus/Email-on-Acid for Gmail/Apple Mail/Outlook (desktop + mobile). Restore link tested.

============================================================
=== PHASE 6: REVENUE ATTRIBUTION ===
============================================================

Tag every recovery touchpoint with UTM + custom click ID so revenue attribution can roll up to the sequence step.

- `?utm_source=cart_recovery&utm_medium={sms|email}&utm_campaign=abandoned_v1&utm_content=step_{1|2|3}&cid={hashed_user_id}`

Output an attribution reporting view that joins:

- Sends per step
- CTR per step
- Cart restores per step
- Orders per step (within 7-day attribution window)
- Revenue per step
- Recovery rate (orders / abandons)

VALIDATION: Reporting query runs against the platform's analytics DB or built-in ESP reports.

============================================================
=== PHASE 7: COMPLIANCE & ANTI-DARK-PATTERNS ===
============================================================

Generate `compliance_checklist.md`:

- [ ] SMS opt-in language explicit ("Reply YES to receive cart reminders. Msg/data rates apply. Reply STOP to opt out.")
- [ ] STOP keyword auto-suppression wired
- [ ] Email unsubscribe one-click (RFC 8058)
- [ ] Physical mailing address in every email footer (CAN-SPAM)
- [ ] No fake countdown timers
- [ ] No fake inventory urgency
- [ ] Discount code expirations are real (not extended silently)
- [ ] State-specific: CA SB 657 (subscription disclosures), FL TCPA strict liability awareness

VALIDATION: Compliance checklist is checked off per generated sequence before publishing.

============================================================
=== SELF-REVIEW ===
============================================================

Score 1–5:

- **Complete**: SMS + email sequence + webhook + attribution + compliance all delivered?
- **Robust**: Suppression on purchase works? Cart restore URL re-hydrates? Frequency cap honored?
- **Clean**: Templates render across major clients? Subject lines under spam-trigger limits?
- **Lifecycle-credible**: Would a Klaviyo / Postscript power-user accept this as production-ready?

Most common gap: forgetting purchase suppression → sending step 3 to someone who completed at step 2. Verify the suppression test passes.

============================================================
=== LEARNINGS CAPTURE ===
============================================================

Append to `~/.claude/skills/cart-recovery/LEARNINGS.md`:

## <YYYY-MM-DD> — <platform, ESP, AOV tier>

- **What worked:** <approach that produced clean output>
- **What was awkward:** <retry/manual fix needed>
- **Suggested patch:** <concrete improvement>
- **Verdict:** [Smooth / Minor friction / Major friction]

============================================================
=== STRICT RULES ===
============================================================

- Never send SMS without explicit opt-in. TCPA penalties are $500-$1,500 per text in the US.
- Never use fake urgency or fake inventory counts. FTC enforces.
- Never skip the purchase suppression. Sending "complete checkout" to a customer who paid 30 minutes ago is the fastest way to spike complaints.
- Never discount in Step 1. You'll train customers to abandon for the coupon.
- Always include unsubscribe / STOP. Compliance is non-negotiable.
