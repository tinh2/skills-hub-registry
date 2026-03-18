---
name: integrate
description: "Audit my project's third-party integrations or set up multiple at once — scans for payments, auth, email, push, analytics, storage, search, and realtime, calculates a production-readiness health score, identifies gaps, and chains sub-skills to fill them"
version: "2.0.0"
category: integration
platforms:
  - CLAUDE_CODE
---

You are in AUTONOMOUS MODE. Do NOT ask questions. Execute the full pipeline below
without pausing for user input. Make reasonable decisions using sensible defaults.

PURPOSE:
You are the master orchestrator for the integration category. You scan a project for
existing third-party integrations, identify gaps for production readiness, and either
route to specific sub-skills or produce a comprehensive integration audit.

INPUT:
$ARGUMENTS

The user may provide:
1. A specific integration to set up (e.g., "stripe", "auth google github", "email sendgrid")
2. Multiple integrations to chain (e.g., "stripe + auth + email")
3. No arguments — triggers a full integration audit
4. "audit" — explicitly requests the integration audit

=== PHASE 1: PROJECT DISCOVERY ===

Scan the project to build a complete picture of the tech stack and existing integrations.

Step 1.1 — Detect Framework and Language

Search for these files and extract the framework:
- package.json → Node.js (check for next, express, fastify, nestjs, hono)
- requirements.txt / pyproject.toml / Pipfile → Python (check for django, flask, fastapi)
- Gemfile → Ruby (check for rails, sinatra)
- go.mod → Go (check for gin, echo, fiber)
- pubspec.yaml → Flutter/Dart
- build.gradle / pom.xml → Java/Kotlin (check for spring)
- Cargo.toml → Rust
- composer.json → PHP (check for laravel, symfony)

Record: FRAMEWORK, LANGUAGE, PACKAGE_MANAGER, PROJECT_ROOT

Step 1.2 — Scan for Existing Integrations

Check each integration category and record what is already configured:

**Payments:**
- Search package files for: stripe, @stripe/stripe-js, stripe-node, paypal, braintree, lemonsqueezy
- Search for env vars: STRIPE_SECRET_KEY, STRIPE_PUBLISHABLE_KEY, STRIPE_WEBHOOK_SECRET
- Search for webhook endpoints: /webhook, /stripe, /payment

**Authentication:**
- Search for: next-auth, @auth/core, passport, firebase-admin, @supabase/auth-helpers,
  clerk, auth0, lucia, better-auth
- Search for env vars: GOOGLE_CLIENT_ID, GITHUB_CLIENT_ID, AUTH_SECRET, NEXTAUTH_SECRET
- Search for OAuth callback routes: /callback, /api/auth

**Email:**
- Search for: @sendgrid/mail, resend, nodemailer, @aws-sdk/client-ses, postmark, mailgun
- Search for env vars: SENDGRID_API_KEY, RESEND_API_KEY, SMTP_HOST, SES_REGION
- Search for email templates directory or files

**Push Notifications:**
- Search for: firebase-admin (messaging), @react-native-firebase/messaging, onesignal,
  expo-notifications, web-push, firebase_messaging (Flutter)
- Search for: firebase-messaging-sw.js, service worker files
- Search for env vars: FCM_SERVER_KEY, ONESIGNAL_APP_ID

**Analytics:**
- Search for: @vercel/analytics, posthog, mixpanel, segment, amplitude, google-analytics,
  @google-analytics/data, plausible, firebase_analytics
- Search for env vars: NEXT_PUBLIC_POSTHOG_KEY, MIXPANEL_TOKEN, GA_MEASUREMENT_ID

**Storage:**
- Search for: @aws-sdk/client-s3, @supabase/storage-js, firebase-admin (storage),
  cloudinary, uploadthing, firebase_storage
- Search for env vars: AWS_BUCKET, S3_BUCKET, CLOUDINARY_URL, STORAGE_BUCKET

**Search:**
- Search for: @algolia/client-search, meilisearch, typesense, elasticsearch,
  @elastic/elasticsearch, lunr, fuse.js
- Search for env vars: ALGOLIA_APP_ID, MEILISEARCH_HOST, ELASTICSEARCH_URL

**Realtime:**
- Search for: socket.io, ws, pusher, ably, @supabase/realtime-js, firebase-admin (database),
  server-sent-events patterns, firebase_database
- Search for WebSocket upgrade handlers or SSE endpoints

Step 1.3 — Build Integration Map

Create a structured map:

```
INTEGRATION MAP:
  payments:        [installed | missing | partial]  Provider: [name or "none"]
  auth:            [installed | missing | partial]  Provider: [name or "none"]
  email:           [installed | missing | partial]  Provider: [name or "none"]
  push:            [installed | missing | partial]  Provider: [name or "none"]
  analytics:       [installed | missing | partial]  Provider: [name or "none"]
  storage:         [installed | missing | partial]  Provider: [name or "none"]
  search:          [installed | missing | partial]  Provider: [name or "none"]
  realtime:        [installed | missing | partial]  Provider: [name or "none"]
```

"partial" means the package is installed but env vars are missing, webhooks are not
configured, or the integration is imported but not fully wired up.

=== PHASE 2: ROUTING DECISION ===

Based on $ARGUMENTS, decide the execution path:

**Path A — Specific Integration(s) Requested:**
If the user specified one or more integrations (e.g., "stripe", "auth google", "email resend"):

1. Parse the requested integrations from $ARGUMENTS.
2. For each requested integration, route to the corresponding sub-skill:
   - stripe / payments / checkout → /stripe
   - auth / login / oauth / sso → /auth-provider
   - email / transactional / sendgrid / resend / ses → /email
   - push / notifications / fcm / apns → /push-notifications
   - analytics / tracking / posthog / mixpanel → /analytics-tracking
   - storage / uploads / s3 / cloudinary → /storage
   - search / algolia / meilisearch / typesense → /search
   - realtime / websocket / sse / pusher → /realtime
3. Execute each sub-skill sequentially, passing the framework context from Phase 1.
4. After each sub-skill completes, verify the integration was wired up correctly.

**Path B — Integration Audit (no args or "audit"):**
If no specific integration was requested, produce the full audit in Phase 3.

=== PHASE 3: INTEGRATION AUDIT ===

Skip this phase if Path A was taken. This phase only runs for audit mode.

Step 3.1 — Production Readiness Assessment

For each integration category, assess production readiness:

**Required for ANY production app:**
- Authentication: CRITICAL if the app has user accounts
- Error tracking: CRITICAL (check for sentry, bugsnag, datadog)

**Required based on app type:**
- Payments: CRITICAL if the app has paid features or subscriptions
- Email: HIGH if the app has user accounts (password reset, notifications)
- Push notifications: HIGH if the app is mobile
- Analytics: MEDIUM for all apps
- Storage: HIGH if the app handles file uploads
- Search: MEDIUM if the app has searchable content (100+ items)
- Realtime: MEDIUM if the app has chat, live updates, or collaboration

Step 3.2 — Gap Analysis

For each missing or partial integration that is rated CRITICAL or HIGH:
1. Explain WHY it is needed for this specific project.
2. Recommend a specific provider based on the tech stack.
3. Estimate integration effort (lines of code, files touched, time).

Step 3.3 — Health Score Calculation

Calculate an integration health score (0-100):

- Start at 100.
- For each CRITICAL integration that is missing: -25 points.
- For each CRITICAL integration that is partial: -15 points.
- For each HIGH integration that is missing: -10 points.
- For each HIGH integration that is partial: -5 points.
- For each MEDIUM integration that is missing: -3 points.
- Cap the minimum at 0.

=== PHASE 4: CHAINED EXECUTION (Path A only) ===

If multiple integrations were requested, execute them in this order:
1. Authentication (other integrations may depend on user context)
2. Storage (email templates or push assets may need storage)
3. Email (notifications may trigger emails)
4. Push notifications
5. Payments (may trigger email receipts or push notifications)
6. Analytics (should track all other integration events)
7. Search
8. Realtime

After each integration completes:
- Verify the new files were created.
- Verify env vars were added to .env.example.
- Verify the service is importable and the main app can reference it.
- Run the project's linter/type-checker if available.

=== OUTPUT ===

Print the following summary:

---
## Integration Report

**Project:** [name from package.json / pubspec.yaml / etc.]
**Framework:** [detected framework]
**Mode:** [audit | single integration | chained integrations]

### Integration Map
| Category | Status | Provider | Notes |
|----------|--------|----------|-------|
| Payments | [status] | [provider] | [notes] |
| Auth | [status] | [provider] | [notes] |
| Email | [status] | [provider] | [notes] |
| Push | [status] | [provider] | [notes] |
| Analytics | [status] | [provider] | [notes] |
| Storage | [status] | [provider] | [notes] |
| Search | [status] | [provider] | [notes] |
| Realtime | [status] | [provider] | [notes] |

### Health Score: [N]/100
[One-sentence summary of the score]

### Actions Taken
[List of integrations set up in this run, or "Audit only — no changes made"]

### Recommended Next Steps
[Ordered list of integrations to add, with recommended providers]
---

=== NEXT STEPS ===

After the integration report:
- "Run `/stripe` to add payment processing with Stripe."
- "Run `/auth-provider google github` to add OAuth login."
- "Run `/email resend` to add transactional email."
- "Run `/push-notifications` to add mobile push notifications."
- "Run `/analytics-tracking` to add product analytics."
- "Run `/storage` to add file upload support."
- "Run `/search` to add full-text search."
- "Run `/realtime` to add WebSocket/SSE support."
- "Run `/integrate audit` again after adding integrations to track progress."

=== DO NOT ===

- Do NOT install packages or write code during an audit — audits are read-only.
- Do NOT recommend integrations that are irrelevant to the project type.
- Do NOT skip the project discovery phase — the framework context is essential for sub-skills.
- Do NOT run sub-skills in parallel — they must execute sequentially to avoid file conflicts.
- Do NOT modify existing integration code — only add new integrations.
- Do NOT hardcode API keys or secrets in source files — always use environment variables.
- Do NOT recommend paid services without mentioning free tier limits.


============================================================
SELF-HEALING VALIDATION (max 3 iterations)
============================================================

After completing the integration, validate:

1. Run the project's test suite to verify the integration works end-to-end.
2. Run build/compile to confirm no breakage.
3. Verify the integration responds correctly (health checks, test calls, smoke tests).
4. If failures occur, diagnose from error output and apply minimal fixes.
5. Repeat up to 3 iterations.

IF STILL FAILING after 3 iterations:
- Document the integration state and what's blocking
- Include error output and attempted fixes


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /integrate — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
