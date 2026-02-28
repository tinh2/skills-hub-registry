---
name: stripe
description: Sets up complete Stripe payment integration with checkout sessions, webhooks, subscription billing, and customer portal for any framework.
version: "1.0.0"
category: integration
platforms:
  - CLAUDE_CODE
---

You are in AUTONOMOUS MODE. Do NOT ask questions. Execute the full pipeline below
without pausing for user input. Make reasonable decisions using sensible defaults.

PURPOSE:
Set up a complete Stripe payment integration in the current project. This includes
SDK installation, API key configuration, checkout flow, webhook handling with
signature verification, and optionally subscription billing and customer portal.

INPUT:
$ARGUMENTS

The user may specify:
1. Payment type: "one-time", "subscription", "both" (default: "both")
2. Specific products/prices to configure
3. A provider preference (always Stripe for this skill)
If no arguments, default to a complete setup with both one-time and subscription support.

=== PHASE 1: PROJECT DETECTION ===

Step 1.1 — Detect Framework

Scan for project files to determine the tech stack:

| File | Framework | Server Library |
|------|-----------|---------------|
| package.json with "next" | Next.js | Built-in API routes |
| package.json with "fastify" | Fastify | Fastify routes |
| package.json with "express" | Express | Express routes |
| package.json with "nestjs" | NestJS | NestJS controllers |
| package.json with "hono" | Hono | Hono routes |
| requirements.txt with "django" | Django | Django views |
| requirements.txt with "fastapi" | FastAPI | FastAPI routes |
| requirements.txt with "flask" | Flask | Flask routes |
| Gemfile with "rails" | Rails | Rails controllers |
| go.mod with "gin" | Gin | Gin handlers |

Record: FRAMEWORK, LANGUAGE, PROJECT_ROOT, SRC_DIR, ROUTES_DIR

Step 1.2 — Check Existing Stripe Setup

Search for any existing Stripe integration:
- Package installed: stripe, @stripe/stripe-js, stripe-node
- Env vars: STRIPE_SECRET_KEY, STRIPE_PUBLISHABLE_KEY, STRIPE_WEBHOOK_SECRET
- Existing webhook endpoint
- Existing checkout or payment intent code

If a complete Stripe integration already exists, report it and exit.
If a partial integration exists, identify gaps and fill them.

=== PHASE 2: SDK INSTALLATION ===

Step 2.1 — Install Server-Side SDK

Based on the detected language:
- **Node.js/TypeScript:** `npm install stripe` (or yarn/pnpm based on lockfile)
- **Python:** `pip install stripe` (add to requirements.txt)
- **Ruby:** Add `gem 'stripe'` to Gemfile
- **Go:** `go get github.com/stripe/stripe-go/v80`
- **PHP:** `composer require stripe/stripe-php`

Step 2.2 — Install Client-Side SDK (if applicable)

If the project has a frontend:
- **Next.js / React:** `npm install @stripe/stripe-js @stripe/react-stripe-js`
- **Flutter:** Add `flutter_stripe` to pubspec.yaml
- **No separate frontend:** Skip client SDK

Step 2.3 — Configure Environment Variables

Add to .env.example (create if it does not exist):
```
# Stripe
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
```

If .env exists, add the same keys with placeholder values.
If the project uses a config validation system (e.g., Zod env schema), update it.

=== PHASE 3: STRIPE CLIENT MODULE ===

Step 3.1 — Create Stripe Client Singleton

Create a Stripe client module at the appropriate location based on the framework:
- Next.js: `lib/stripe.ts` or `src/lib/stripe.ts`
- Fastify/Express: `src/config/stripe.ts` or `src/lib/stripe.ts`
- Django/FastAPI: `app/services/stripe_client.py` or `config/stripe.py`
- Rails: `config/initializers/stripe.rb`

The client module MUST:
- Import the Stripe SDK
- Initialize with the secret key from environment variables
- Set the API version explicitly (use the latest stable version)
- Export a singleton instance
- Include TypeScript types if applicable

Step 3.2 — Create Stripe Service Layer

Create a service module that encapsulates all Stripe operations:

Location: `src/services/stripe.service.ts` (adjust path for framework)

The service MUST include these methods:

```
createCheckoutSession(params):
  - Accepts: priceId, customerId (optional), successUrl, cancelUrl, mode (payment | subscription)
  - Creates a Stripe Checkout Session
  - Returns the session URL and ID

createPaymentIntent(params):
  - Accepts: amount, currency, customerId (optional), metadata
  - Creates a Payment Intent for custom payment flows
  - Returns the client secret

createCustomer(params):
  - Accepts: email, name, metadata
  - Creates a Stripe Customer
  - Returns the customer object

getCustomerPortalSession(params):
  - Accepts: customerId, returnUrl
  - Creates a Billing Portal Session
  - Returns the portal URL

constructWebhookEvent(payload, signature):
  - Accepts: raw request body, Stripe-Signature header value
  - Verifies the webhook signature using STRIPE_WEBHOOK_SECRET
  - Returns the verified event object
  - Throws on invalid signature
```

Every method MUST:
- Use try/catch with meaningful error messages
- Log errors (using the project's logger if one exists)
- Never expose raw Stripe errors to clients — wrap in application errors

=== PHASE 4: CHECKOUT FLOW ===

Step 4.1 — Create Checkout Endpoint

Create an API endpoint for initiating checkout:

Route: POST /api/payments/checkout (or framework equivalent)

The endpoint MUST:
- Accept: priceId, mode (payment | subscription), successUrl, cancelUrl
- Optionally accept customerId (link to existing customer)
- Call stripeService.createCheckoutSession()
- Return the session URL to the client
- Require authentication if the project has auth middleware

Step 4.2 — Create Payment Intent Endpoint (for custom UI)

Route: POST /api/payments/create-intent

The endpoint MUST:
- Accept: amount, currency (default "usd")
- Call stripeService.createPaymentIntent()
- Return the client secret
- Require authentication

Step 4.3 — Create Success/Cancel Handlers

If the project has a frontend:
- Create a success page/route that displays confirmation
- Create a cancel page/route that allows retry
- Both should handle the session_id query parameter from Stripe redirect

=== PHASE 5: WEBHOOK HANDLER ===

Step 5.1 — Create Webhook Endpoint

Route: POST /api/webhooks/stripe

This is the MOST CRITICAL part of the integration. The webhook MUST:

1. Read the raw request body (NOT parsed JSON — Stripe needs the raw body for verification)
2. Extract the Stripe-Signature header
3. Call stripeService.constructWebhookEvent() to verify the signature
4. Return 400 immediately if signature verification fails
5. Handle events in a switch/case block
6. Return 200 quickly — do async processing outside the request if needed

**Framework-specific raw body handling:**
- **Next.js App Router:** Use the raw request body from the Request object
- **Next.js Pages Router:** Disable body parser for the webhook route
- **Express:** Use express.raw() middleware on the webhook route only
- **Fastify:** Use addContentTypeParser for the webhook route to get raw body
- **Django:** Use request.body (already raw bytes)
- **FastAPI:** Use Request.body() directly
- **Rails:** Use request.body.read

Step 5.2 — Handle Core Webhook Events

Implement handlers for these events:

```
checkout.session.completed:
  - Extract session data
  - Link payment to user/order in your database
  - Send confirmation email if email service exists

payment_intent.succeeded:
  - Update payment status in database
  - Fulfill the order

payment_intent.payment_failed:
  - Update payment status
  - Notify the user of failure

customer.subscription.created:
  - Store subscription details in database
  - Update user's plan/tier

customer.subscription.updated:
  - Update stored subscription details
  - Handle plan changes (upgrade/downgrade)

customer.subscription.deleted:
  - Mark subscription as canceled in database
  - Downgrade user's plan/tier
  - Handle grace period if applicable

invoice.payment_succeeded:
  - Record successful invoice payment
  - Extend subscription access

invoice.payment_failed:
  - Notify user of payment failure
  - Begin dunning process (retry logic)
```

Each handler should call a dedicated function — do NOT put business logic inline in the switch.

Step 5.3 — Webhook Idempotency

Every webhook handler MUST be idempotent:
- Check if the event has already been processed (store event IDs in database)
- If already processed, return 200 without re-processing
- Use database transactions where applicable

=== PHASE 6: SUBSCRIPTION BILLING (if requested) ===

Skip this phase if the user only requested one-time payments.

Step 6.1 — Price Configuration

Create a prices/products configuration file:
```
// src/config/stripe-prices.ts
export const PRICES = {
  FREE: { id: null, name: 'Free', features: [...] },
  PRO: { id: 'price_xxx', name: 'Pro', features: [...] },
  ENTERPRISE: { id: 'price_xxx', name: 'Enterprise', features: [...] },
} as const;
```

Step 6.2 — Customer Portal Endpoint

Route: POST /api/payments/portal

The endpoint MUST:
- Require authentication
- Look up the Stripe customer ID for the authenticated user
- Call stripeService.getCustomerPortalSession()
- Return the portal URL
- Handle the case where the user has no Stripe customer record

Step 6.3 — Subscription Status Middleware

Create middleware or a helper function that:
- Checks the user's current subscription status
- Can be used to gate premium features
- Caches the subscription status to avoid excessive Stripe API calls
- Falls back gracefully if Stripe is unreachable

=== PHASE 7: VERIFICATION ===

Step 7.1 — Static Verification

Run the project's type checker and linter:
- TypeScript: `tsc --noEmit`
- Python: `mypy` or `pyright` if configured
- Linter: ESLint, Ruff, Rubocop, etc.

Fix all errors introduced by the Stripe integration.

Step 7.2 — Integration Checklist

Verify and report:
- [ ] Stripe SDK installed (server + client if applicable)
- [ ] Environment variables documented in .env.example
- [ ] Stripe client singleton created with explicit API version
- [ ] Checkout session endpoint functional
- [ ] Webhook endpoint with raw body parsing
- [ ] Webhook signature verification implemented
- [ ] Core webhook events handled
- [ ] Webhook idempotency implemented
- [ ] Subscription billing configured (if requested)
- [ ] Customer portal endpoint created (if subscriptions)
- [ ] All errors wrapped — no raw Stripe errors leaked to clients
- [ ] Type checking passes

=== OUTPUT ===

Print the following summary:

---
## Stripe Integration Complete

**Framework:** [detected framework]
**Payment types:** [one-time | subscription | both]

### Files Created/Modified
| File | Purpose |
|------|---------|
| [path] | [description] |

### Environment Variables Required
| Variable | Purpose | Where to get it |
|----------|---------|-----------------|
| STRIPE_SECRET_KEY | Server-side API key | Stripe Dashboard > API Keys |
| STRIPE_PUBLISHABLE_KEY | Client-side API key | Stripe Dashboard > API Keys |
| STRIPE_WEBHOOK_SECRET | Webhook verification | Stripe Dashboard > Webhooks |

### Endpoints Added
| Method | Path | Purpose |
|--------|------|---------|
| POST | /api/payments/checkout | Create checkout session |
| POST | /api/payments/create-intent | Create payment intent |
| POST | /api/payments/portal | Customer billing portal |
| POST | /api/webhooks/stripe | Stripe webhook handler |

### Webhook Events Handled
[List of events with brief description]

### Test Mode Setup
1. Use `sk_test_...` and `pk_test_...` keys from Stripe Dashboard
2. Run `stripe listen --forward-to localhost:[PORT]/api/webhooks/stripe` for local testing
3. Use Stripe CLI to trigger test events: `stripe trigger payment_intent.succeeded`

### Going Live Checklist
- [ ] Switch to live API keys in production environment
- [ ] Configure webhook endpoint URL in Stripe Dashboard
- [ ] Set up Stripe Tax if required
- [ ] Configure Stripe Radar for fraud protection
- [ ] Test the complete flow with Stripe test cards
---

=== NEXT STEPS ===

After Stripe integration:
- "Run `/auth-provider` to add user authentication (needed to link payments to users)."
- "Run `/email` to add transactional email for payment receipts and invoices."
- "Run `/analytics-tracking` to track conversion funnels and payment events."
- "Run `/integrate audit` to check overall integration health."

=== DO NOT ===

- Do NOT store raw credit card numbers or sensitive payment data — Stripe handles this.
- Do NOT skip webhook signature verification — this is a security requirement.
- Do NOT parse the webhook request body as JSON before signature verification.
- Do NOT use deprecated Stripe APIs (Charges API) — use Payment Intents and Checkout Sessions.
- Do NOT hardcode Stripe API keys in source code — always use environment variables.
- Do NOT log full Stripe event payloads in production — they may contain PII.
- Do NOT ignore webhook delivery failures — implement proper error handling and retry logic.
- Do NOT create Stripe resources (products, prices) via code — configure them in the Dashboard
  and reference by ID, unless the user specifically requests programmatic product creation.
- Do NOT skip the raw body configuration for the webhook route — this is the most common
  source of "signature verification failed" errors.
