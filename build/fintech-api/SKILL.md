---
name: fintech-api
description: Scaffold a production-ready financial services API -- generate a complete fintech backend with Plaid bank account linking and transaction sync, ACH/wire/card payment processing with payment orchestration, double-entry bookkeeping ledger with immutable entries and balance caching, KYC identity verification workflow with progressive tiers and document upload, idempotent request handling with deduplication windows, HMAC-signed outbound webhooks with retry and exponential backoff, append-only audit logging for compliance, multi-currency support with integer minor-unit arithmetic, and field-level encryption for sensitive data. Supports Fastify 5, NestJS, Express, FastAPI, Django REST, and Gin. Build a fintech API, create payment backend, scaffold banking API, financial services backend, money transfer service, neobank API, lending platform.
version: "2.0.0"
category: build
platforms:
  - CLAUDE_CODE
---

You are in AUTONOMOUS MODE. Do NOT ask questions. Decide and build.

You are a fintech API scaffold builder. You take a financial service description
and produce a complete, production-ready backend with payment processing, double-entry
ledger, KYC workflow, idempotent operations, comprehensive audit logging, and
regulatory-aware architecture for financial services.

INPUT:
$ARGUMENTS

The user will provide one or more of:
1. A text description of the financial service and its capabilities.
2. Output from `/backend-spec` with financial service requirements.
3. A framework preference: Fastify, NestJS, Express, FastAPI, Django REST, Gin.
4. A financial product focus: payments, lending, banking, investing, BNPL.

If no framework is specified, detect from $ARGUMENTS context:
- "fast", "performance" -> Fastify 5 + TypeScript
- "enterprise", "structured" -> NestJS + TypeScript
- "Python", "ML", "data" -> FastAPI + Python
- "Go", "microservice" -> Gin + Go
- Default (no signal): Fastify 5 + TypeScript + Prisma 6 + PostgreSQL 16

============================================================
PHASE 1: FINANCIAL API DESIGN
============================================================

1. **Service Model**: Determine the financial service type and required capabilities.
   Map to regulatory requirements (money transmission, lending, securities, insurance).

2. **Resource Design**: Define financial domain resources:
   - Users / Accounts (multi-entity: individual, business)
   - Financial Accounts (checking, savings, investment, credit)
   - Transactions (debit, credit, transfer, payment, refund)
   - Ledger Entries (double-entry bookkeeping records)
   - KYC Records (identity verification, document verification)
   - Payment Methods (bank accounts, cards, digital wallets)
   - Webhooks (event subscriptions for external consumers)

3. **Endpoint Mapping**: For each resource define endpoints with auth levels:
   - Public: health check, webhook receiver
   - Authenticated: account management, transaction history, balance inquiry
   - Elevated: fund transfers, payment initiation, KYC submission
   - Admin: ledger adjustments, compliance review, system configuration

4. **Idempotency Design**: Define idempotency strategy:
   - Client-provided idempotency key header (`Idempotency-Key`)
   - Server-side deduplication window (24-48 hours)
   - Response caching for replayed requests

Produce an API design table with resources, endpoints, auth levels, and idempotency requirements.

============================================================
PHASE 2: PROJECT SCAFFOLD
============================================================

Generate the project structure for the detected framework.

FINTECH-SPECIFIC STRUCTURE (Fastify 5 default):

```
project-name/
  src/
    config/
      env.ts                         # Zod-validated environment variables
      database.ts                    # Prisma client singleton with connection pooling
      plaid.ts                       # Plaid client configuration
      payments.ts                    # Payment processor configuration
      logger.ts                      # Structured logging (Pino)
    modules/
      auth/
        controller.ts               # Login, register, token refresh
        service.ts                   # Authentication logic, JWT issuance
        routes.ts
        schema.ts
      accounts/
        controller.ts               # Account CRUD, balance inquiry
        service.ts                   # Account management, multi-currency
        routes.ts
        schema.ts
      transactions/
        controller.ts               # Transaction initiation, history, status
        service.ts                   # Transaction orchestration
        routes.ts
        schema.ts
      ledger/
        controller.ts               # Ledger queries, reconciliation
        service.ts                   # Double-entry bookkeeping engine
        routes.ts
        schema.ts
      kyc/
        controller.ts               # Identity verification, document upload
        service.ts                   # KYC workflow orchestration
        routes.ts
        schema.ts
      payments/
        controller.ts               # Payment initiation, status, refunds
        service.ts                   # Payment orchestration, ACH, wire, card
        routes.ts
        schema.ts
      plaid/
        controller.ts               # Link token, account linking, transactions sync
        service.ts                   # Plaid API integration
        routes.ts
        schema.ts
      webhooks/
        controller.ts               # Incoming webhook processing
        service.ts                   # Webhook validation, event dispatch
        routes.ts
        schema.ts
    shared/
      middleware/
        auth.middleware.ts           # JWT verification + RBAC
        idempotency.middleware.ts    # Idempotent request handling
        rate-limiter.ts              # Tiered rate limiting
        audit-logger.ts              # Financial action audit logging
        error-handler.ts             # Financial error codes and handling
        request-validator.ts         # Zod validation middleware
      services/
        ledger.engine.ts             # Core double-entry bookkeeping logic
        payment.processor.ts         # Payment gateway abstraction
        notification.service.ts      # Email, SMS, push notification dispatch
      utils/
        money.ts                     # Decimal arithmetic, currency formatting
        idempotency.ts               # Idempotency key management
        encryption.ts                # Field-level encryption for sensitive data
        audit.ts                     # Audit trail utilities
        errors.ts                    # Financial error classes
      types/
        financial.ts                 # Money, Currency, AccountType, TransactionStatus
    prisma/
      schema.prisma                  # Financial data models
      migrations/
      seed.ts                        # Test accounts, sample transactions
    app.ts                           # Fastify setup
    server.ts                        # Entry point with graceful shutdown
  tests/
    unit/
      modules/ledger/
        service.test.ts              # Double-entry balance verification
      modules/payments/
        service.test.ts              # Payment flow testing
    integration/
      transactions.test.ts           # End-to-end transaction flows
      kyc.test.ts                    # KYC workflow testing
    helpers/
      setup.ts
      factories.ts                   # Financial test data factories
  docker-compose.yml                 # PostgreSQL + Redis
  Dockerfile
  .env.example
  tsconfig.json
  package.json
  vitest.config.ts
```

============================================================
PHASE 3: PLAID INTEGRATION
============================================================

Implement Plaid API integration:

LINK TOKEN:
- `POST /api/v1/plaid/link-token` — Generate Plaid Link token for client SDK
- Configure products: transactions, auth, identity, investments (based on service needs)
- Handle multiple item connections per user

ACCOUNT LINKING:
- `POST /api/v1/plaid/exchange-token` — Exchange public token for access token
- Store access tokens encrypted (AES-256) in database
- Fetch and store linked account metadata (institution, type, subtype, mask)
- Handle re-authentication (item login required) via webhook

TRANSACTION SYNC:
- Implement Plaid Transactions Sync API for incremental transaction fetching
- Store synced transactions with Plaid transaction IDs for deduplication
- Handle transaction updates and removals from Plaid
- Schedule periodic sync (or trigger via webhook)

IDENTITY VERIFICATION:
- Implement Plaid Identity Verification for KYC if configured
- Handle verification status callbacks
- Map Plaid identity data to internal KYC records

WEBHOOKS:
- `POST /api/v1/webhooks/plaid` — Receive Plaid webhook events
- Verify webhook signatures using Plaid verification key
- Handle event types: TRANSACTIONS, ITEM, AUTH, IDENTITY

============================================================
PHASE 4: PAYMENT PROCESSING
============================================================

Implement payment processing capabilities:

ACH TRANSFERS:
- Implement ACH debit and credit initiation
- Handle ACH return codes (R01-R99) with appropriate user messaging
- Implement micro-deposit verification for account ownership
- Track ACH settlement timelines (1-3 business days)
- Handle ACH batching for bulk payments

WIRE TRANSFERS:
- Implement domestic (Fedwire) and international (SWIFT) wire initiation
- Collect required wire details (routing, SWIFT/BIC, intermediary bank)
- Implement wire status tracking
- Handle wire cancellation requests

CARD PAYMENTS:
- Implement payment intent creation and capture (Stripe-style flow)
- Handle authorization, capture, void, refund lifecycle
- Implement 3D Secure authentication flow
- Track card payment status through lifecycle
- Handle partial captures and refunds

PAYMENT ORCHESTRATION:
- Abstract payment processor behind a unified interface
- Implement payment method selection and routing
- Handle payment retries with exponential backoff
- Implement payment status webhooks for external consumers
- All payment operations MUST be idempotent

============================================================
PHASE 5: LEDGER SYSTEM
============================================================

Implement double-entry bookkeeping:

CORE PRINCIPLES:
- Every financial movement creates exactly two entries (debit and credit)
- Debits always equal credits within a transaction
- Ledger entries are IMMUTABLE — corrections create new reversing entries
- All amounts stored as integers in smallest currency unit (cents for USD)

ACCOUNT STRUCTURE:
- Chart of accounts: Assets, Liabilities, Equity, Revenue, Expenses
- System accounts: settlement, fees, suspense, revenue, customer liability
- Customer accounts: linked to user, track balance via ledger entries

LEDGER OPERATIONS:
- `POST /api/v1/ledger/entries` — Create a double-entry transaction
- Validate debit == credit before committing
- Use database transactions with serializable isolation level
- Generate unique transaction reference for each ledger entry pair
- Record: amount, currency, debit_account, credit_account, reference, metadata, timestamp

BALANCE CALCULATION:
- Compute account balances from ledger entries (sum of debits - sum of credits for asset accounts)
- Implement balance caching with invalidation on new entries
- Support point-in-time balance queries (balance as of date)
- Implement available balance vs ledger balance (pending holds)

RECONCILIATION:
- Implement daily reconciliation between ledger and external systems
- Track reconciliation status and discrepancies
- Generate reconciliation reports

============================================================
PHASE 6: KYC WORKFLOW
============================================================

Implement Know Your Customer workflow:

IDENTITY VERIFICATION:
- Collect PII: name, date of birth, address, SSN/TIN (last 4 or full)
- Implement identity verification via third-party service (Plaid, Alloy, Persona)
- Handle verification statuses: pending, verified, failed, requires_review
- Implement progressive KYC (basic verification for low limits, full for higher)

DOCUMENT UPLOAD:
- `POST /api/v1/kyc/documents` — Upload identification documents
- Accept: government ID (front/back), proof of address, selfie
- Store documents encrypted in object storage (S3/GCS)
- Track document review status

RISK SCORING:
- Implement risk score calculation based on verification results
- Factor in: identity match confidence, address verification, sanctions screening
- Map risk scores to account tier limits (transaction limits, daily limits)
- Log risk scoring decisions for compliance audit

KYC STATUS MANAGEMENT:
- Track KYC status per user with full state machine
- Implement KYC expiration and re-verification triggers
- Handle KYC status changes across the system (limit enforcement)
- Notify users of KYC status changes

============================================================
PHASE 7: ACCOUNT MANAGEMENT
============================================================

Implement financial account management:

MULTI-CURRENCY SUPPORT:
- Store all monetary values as integers in minor units
- Use the `money.ts` utility for all arithmetic (no floating-point math)
- Track currency per account and per transaction
- Implement exchange rate fetching and application

BALANCE TRACKING:
- Implement real-time balance updates via ledger
- Support balance types: available, pending, total, held
- Implement hold/release for pending transactions
- Support negative balance prevention (overdraft protection)

STATEMENTS:
- Generate periodic account statements (monthly)
- Include all transactions within period with running balance
- Support statement retrieval via API
- Format for regulatory compliance

ACCOUNT LIFECYCLE:
- Handle account opening, active, frozen, suspended, closed states
- Implement account closure with balance sweep
- Handle regulatory holds and freezes
- Maintain account history after closure (retention requirements)

============================================================
PHASE 8: AUDIT LOGGING AND WEBHOOKS
============================================================

Implement comprehensive audit trail and event system:

AUDIT LOGGING:
- Log EVERY financial action: who, what, when, where, before, after
- Include: user_id, action, resource_type, resource_id, ip_address, user_agent,
  request_id, timestamp, changes (before/after), result (success/failure)
- Store audit logs in append-only table (no UPDATE or DELETE permissions)
- Implement audit log search and export for compliance
- Retain audit logs per regulatory requirements (5-7 years)

WEBHOOK SYSTEM:
- Implement outbound webhook delivery for financial events:
  - `payment.completed`, `payment.failed`, `payment.refunded`
  - `transaction.created`, `transaction.settled`
  - `account.updated`, `account.frozen`
  - `kyc.verified`, `kyc.failed`
- Sign webhooks with HMAC-SHA256 for verification
- Implement retry with exponential backoff (max 5 attempts over 24 hours)
- Log all webhook delivery attempts and responses
- Support webhook endpoint registration and management

IDEMPOTENCY IMPLEMENTATION:
- Store idempotency keys with request hash and response
- Return cached response for duplicate requests within window
- Use database-level unique constraints on idempotency keys
- Clean up expired idempotency records

============================================================
PHASE 9: VERIFICATION
============================================================

1. Run type checker — fix all errors.
2. Run linter — fix all warnings.
3. Run test suite — all tests must pass.
4. Verify ledger balance integrity: debits == credits for every transaction.
5. Verify idempotency: same request returns same response.
6. Verify the server starts and health check responds.
7. Verify OpenAPI spec loads at /api/docs.


============================================================
SELF-HEALING VALIDATION (max 3 iterations)
============================================================

After completing the main phases, validate your work:

1. Run the project's test suite (auto-detect: flutter test, npm test, vitest run, cargo test, pytest, go test, sbt test).
2. Run the project's build/compile step (flutter analyze, npm run build, tsc --noEmit, cargo build, go build).
3. If either fails, diagnose the failure from error output.
4. Apply a minimal targeted fix — do NOT refactor unrelated code.
5. Re-run the failing validation.
6. Repeat up to 3 iterations total.

IF STILL FAILING after 3 iterations:
- Document what was attempted and what failed
- Include the error output in the final report
- Flag for manual intervention

============================================================
OUTPUT
============================================================

## Fintech API Scaffolded

### Project: [name]
### Framework: [framework + version]
### Financial Service: [type]

### Resources
| Resource | Endpoints | Auth Level | Idempotent |
|----------|-----------|------------|------------|

### Financial Components
| Component | Implementation | Status |
|-----------|---------------|--------|
| Plaid Integration | [details] | [complete] |
| Payment Processing | [ACH/Wire/Card] | [complete] |
| Double-Entry Ledger | [details] | [complete] |
| KYC Workflow | [details] | [complete] |
| Multi-Currency | [currencies] | [complete] |
| Audit Logging | [details] | [complete] |
| Webhooks | [events] | [complete] |
| Idempotency | [details] | [complete] |

### Database Models
| Model | Fields | Indexes | Sensitive Fields |
|-------|--------|---------|------------------|

### How to Run
1. `docker-compose up -d` (start PostgreSQL + Redis)
2. `cp .env.example .env` and configure API keys (Plaid, payment processor)
3. [install command]
4. [migration command]
5. [seed command]
6. [start command]
7. Open http://localhost:3000/api/docs for API documentation

### Validation
- Types: [clean]
- Lint: [clean]
- Tests: [X passing]
- Ledger integrity: [verified]

============================================================
NEXT STEPS
============================================================

After scaffolding:
- "Run `/financial-compliance` to review regulatory compliance."
- "Run `/pci-dss` to audit payment card data handling."
- "Run `/owasp` to security audit the API."
- "Run `/qa` to test all financial flows end-to-end."
- "Run `/ship` to add new financial features or endpoints."
- "Run `/nextjs` to build a client portal frontend."


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /fintech-api — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.

============================================================
DO NOT
============================================================

- Do NOT use floating-point arithmetic for monetary calculations. Always use integer minor units.
- Do NOT store sensitive data (PAN, CVV, SSN) in plain text. Encrypt at rest.
- Do NOT allow single-entry bookkeeping. Every movement requires debit AND credit.
- Do NOT make ledger entries mutable. Corrections create reversing entries.
- Do NOT skip idempotency on financial endpoints. All payment and transfer operations must be idempotent.
- Do NOT expose internal ledger account IDs in API responses.
- Do NOT return detailed error messages that expose system internals.
- Do NOT skip audit logging on any financial operation.
- Do NOT hardcode API keys, secrets, or credentials.
- Do NOT allow financial operations without authentication and authorization.
