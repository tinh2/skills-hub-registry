---
name: cost-analysis
description: Analyzes Firebase infrastructure costs at 1K-100K user scales by reading the actual codebase, modeling per-action costs, and projecting total monthly spend with optimization recommendations.
version: "1.0.0"
category: analysis
platforms:
  - CLAUDE_CODE
---

You are an autonomous infrastructure cost analyst. Do NOT ask the user questions.
Read the actual codebase, model costs per user action, project at multiple user scales,
and produce a comprehensive cost report.

TARGET:
$ARGUMENTS

If arguments are provided, use them to focus the analysis (e.g., specific services,
custom user tiers, or a particular feature's cost). If no arguments, run the full analysis.

============================================================
PHASE 1: SERVICE DISCOVERY
============================================================

Discover every cost-generating service by reading project configuration files.

Step 1.1 — Firebase Services

Read these files to identify all Firebase services in use:
- `firebase.json` — enabled services (firestore, functions, storage, hosting, etc.)
- `.firebaserc` — project ID(s)
- `lib/firebase_options.dart` or equivalent — configured services
- `pubspec.yaml` or `package.json` — Firebase SDK packages

For each service found, record:
- Service name
- Pricing model (per-read, per-invocation, per-GB, free tier limits)
- Whether it has a free tier and what the limits are

Step 1.2 — Cloud Functions Inventory

Read every file in `functions/src/` and build a complete function table:

| Function | Type | Trigger | minInstances | Schedule | External APIs | Memory |
|----------|------|---------|--------------|----------|---------------|--------|

Types: onCall, onDocumentCreated, onDocumentUpdated, onDocumentDeleted, onSchedule, onRequest
External APIs: Stripe, Twilio, SendGrid, etc.

For scheduled functions, record the interval (every 5 min, hourly, daily, etc.)
and calculate daily invocation count.

For minInstances > 0, calculate always-on cost:
- Cost = minInstances × $0.000002388/vCPU-second × 86400 seconds/day × memory_factor

Step 1.3 — Firestore Collections

Read Firestore security rules (`firestore.rules`) and service layer code to build
a collection inventory:

| Collection | Subcollections | Estimated Doc Size | Growth Rate |
|------------|---------------|-------------------|-------------|

Growth rate: per-user (linear), per-action (transaction-driven), fixed (config docs)

Step 1.4 — Real-Time Listeners

Search for all `StreamProvider` declarations in providers/ directory.
Each active StreamProvider = 1 Firestore listener = ongoing read charges.

Count total active listeners per user session:
- Always-on listeners (active while app is open)
- Screen-specific listeners (active only on certain screens)
- Background listeners (active in background)

Step 1.5 — Storage Operations

Search for all Storage upload/download calls in the service layer.
Record: what is stored, estimated file size, upload frequency per user.

Step 1.6 — External Paid Services

Identify all external API integrations with costs:
- Payment processor (Stripe, PayPal) — fee structure
- SMS provider (Twilio) — per-message cost
- Email provider — per-email cost
- Maps/geocoding API — per-request cost
- Any other paid API

============================================================
PHASE 2: PER-ACTION COST MODELING
============================================================

For every significant user action, calculate the exact Firebase cost by reading
the code path from screen → provider → service → Cloud Function.

Step 2.1 — Define User Actions

Identify every user-facing action that generates Firebase operations.
Common actions for marketplace apps:

- Sign up / create account
- Log in
- Browse / search listings
- View listing detail
- Create a listing / post
- Book a service
- Send a message
- Write a review
- Upload a photo
- Complete a transaction
- View profile
- Edit profile
- Receive a notification
- Open the app (initial load)

Add any app-specific actions found in the codebase.

Step 2.2 — Trace Each Action

For each action, trace the full code path and count:

| Action | Firestore Reads | Firestore Writes | Firestore Deletes | CF Invocations | FCM Sends | Storage Ops | External API Calls |
|--------|----------------|-----------------|-------------------|----------------|-----------|-------------|-------------------|

Rules for counting:
- A `.get()` call = 1 read per document returned
- A `.where().get()` query = N reads (estimate N from limit or typical result size)
- A StreamProvider snapshot = 1 read per snapshot + 1 read per changed doc
- A `.set()` or `.update()` = 1 write
- A `batch.set()` or `batch.update()` = 1 write per operation in the batch
- A `db.runTransaction()` = reads + writes inside the transaction
- A `.delete()` = 1 delete
- A Cloud Function invocation that itself does reads/writes = count those too
- An FCM notification = 1 send per device token (up to N devices per user)

Step 2.3 — Calculate Per-Action Cost

Apply Firebase pricing to each action:

| Operation | Price per 100K | Price per 1 |
|-----------|---------------|-------------|
| Firestore read | $0.036 | $0.00000036 |
| Firestore write | $0.108 | $0.00000108 |
| Firestore delete | $0.012 | $0.00000012 |
| CF invocation | $0.40/1M | $0.0000004 |
| CF compute (256MB, 1s) | ~$0.000000297 | per invocation |
| CF compute (512MB, 1s) | ~$0.000000594 | per invocation |
| FCM notification | $0/1M (free) | $0 |
| Storage write | $0.05/10K | $0.000005 |
| Storage read | $0.004/10K | $0.0000004 |
| Storage (per GB/month) | $0.026 | — |
| Auth (email/password) | Free up to 50K MAU | $0 |

Note: Use the pricing for the project's Firebase region (check firebase.json).
Default to us-central1 pricing if region is not specified.

Produce a per-action cost table:

| Action | Total Reads | Total Writes | Total Deletes | CF Cost | Ext. API Cost | Total Cost |
|--------|------------|-------------|---------------|---------|--------------|------------|

Step 2.4 — Background/Fixed Costs

Calculate costs that occur regardless of user actions:

- Scheduled Cloud Functions: invocations/day × cost per invocation
- minInstances always-on: count × daily compute cost
- Firestore real-time listeners: reads per minute while app is active
- Storage baseline: total stored data × monthly rate
- Active listener reads: estimate reads per active session hour

============================================================
PHASE 3: USER BEHAVIOR PROFILES
============================================================

Define realistic user behavior profiles for cost projection.

Step 3.1 — Usage Profiles

Define 3 user profiles with monthly action frequencies:

**Casual User (60% of users)**
- Opens app: 3-5 times/month
- Session duration: 5-10 minutes
- Searches: 5/month
- Messages: 5/month
- Bookings: 0-1/month
- Reviews: 0/month
- Photo uploads: 0/month

**Active User (30% of users)**
- Opens app: 15-20 times/month
- Session duration: 10-20 minutes
- Searches: 20/month
- Messages: 30/month
- Bookings: 2-3/month
- Reviews: 1-2/month
- Photo uploads: 1/month

**Power User (10% of users)**
- Opens app: 30+ times/month
- Session duration: 15-30 minutes
- Searches: 50/month
- Messages: 100/month
- Bookings: 5-8/month
- Reviews: 3-5/month
- Photo uploads: 3/month

Adjust these profiles based on the app's specific domain:
- For social apps: increase message/post frequency
- For marketplace apps: increase search/booking frequency
- For utility apps: increase session frequency, decrease social features

Step 3.2 — Weighted Average User

Calculate the weighted average monthly cost per user:

weighted_cost = (0.60 × casual_cost) + (0.30 × active_cost) + (0.10 × power_cost)

============================================================
PHASE 4: SCALE PROJECTION
============================================================

Project total monthly costs at each user tier.

Step 4.1 — User Tiers

Calculate for these tiers (or custom tiers if specified in arguments):
- 1,000 monthly active users (MAU)
- 5,000 MAU
- 10,000 MAU
- 25,000 MAU
- 50,000 MAU
- 100,000 MAU

Step 4.2 — Linear Costs (Scale with Users)

For each tier, multiply:
- Per-user monthly cost × number of users
- Per-action costs × (action frequency × users)

Step 4.3 — Fixed Costs (Do Not Scale)

Add costs that remain constant regardless of user count:
- Scheduled function invocations (same frequency at 1K or 100K)
- minInstances always-on compute
- Firebase Hosting (if used)
- Base storage (app assets, config docs)

Step 4.4 — Sub-Linear Costs (Grow Slower Than Users)

Some costs grow sub-linearly:
- Storage egress has CDN caching (repeated image views don't re-download)
- Config reads are cached (loadCachedConfig pattern)
- Shared data (sitter listings) is read once per query, not per user

Step 4.5 — Super-Linear Costs (Grow Faster Than Users)

Some costs grow faster than linearly:
- Messaging: N users can message N-1 others (O(N) per user, O(N^2) total in worst case)
- Search results: more sitters = larger query results
- Fan-out writes: user profile update propagates to all their listings/conversations

Step 4.6 — Free Tier Deductions

Apply Firebase Spark/Blaze free tier allowances:
- Firestore: 50K reads/day, 20K writes/day, 20K deletes/day free
- Cloud Functions: 2M invocations/month free
- Storage: 5 GB free, 1 GB/day egress free
- Auth: free for email/password (all tiers)
- FCM: free (all tiers)
- Hosting: 10 GB storage, 360 MB/day transfer free

Subtract free tier from total before calculating cost.

Step 4.7 — Build the Projection Table

| | 1K MAU | 5K MAU | 10K MAU | 25K MAU | 50K MAU | 100K MAU |
|---|---|---|---|---|---|---|
| Firestore Reads | $ | $ | $ | $ | $ | $ |
| Firestore Writes | $ | $ | $ | $ | $ | $ |
| Firestore Deletes | $ | $ | $ | $ | $ | $ |
| Cloud Functions | $ | $ | $ | $ | $ | $ |
| Storage | $ | $ | $ | $ | $ | $ |
| FCM | $ | $ | $ | $ | $ | $ |
| Auth | $ | $ | $ | $ | $ | $ |
| Hosting | $ | $ | $ | $ | $ | $ |
| **Firebase Subtotal** | **$** | **$** | **$** | **$** | **$** | **$** |
| Stripe Fees | $ | $ | $ | $ | $ | $ |
| Twilio/SMS | $ | $ | $ | $ | $ | $ |
| Other External | $ | $ | $ | $ | $ | $ |
| **External Subtotal** | **$** | **$** | **$** | **$** | **$** | **$** |
| **TOTAL** | **$** | **$** | **$** | **$** | **$** | **$** |
| **Per User/Month** | **$** | **$** | **$** | **$** | **$** | **$** |

============================================================
PHASE 5: COST OPTIMIZATION RECOMMENDATIONS
============================================================

Based on the analysis, identify the top cost optimization opportunities.

Step 5.1 — Identify Cost Hotspots

From Phase 4, rank cost categories by total spend at the 100K tier.
The top 3 categories are the optimization targets.

Step 5.2 — Generate Optimization Recommendations

For each hotspot, propose specific, actionable optimizations:

| # | Optimization | Service | Est. Savings/Month (100K) | Effort | Risk |
|---|---|---|---|---|---|
| 1 | [specific change] | Firestore | $X | Low/Med/High | Low/Med/High |
| 2 | ... | ... | ... | ... | ... |

Common optimization patterns to check for:
- **Reduce listener count**: Consolidate StreamProviders, use pagination instead of streams
- **Add query limits**: Unbounded queries → add .limit()
- **Cache config reads**: Already done? Verify all config reads use cache
- **Reduce scheduled function frequency**: Can 5-min → 30-min? Daily → weekly?
- **Batch writes**: Multiple individual writes → batch operation
- **Denormalize reads**: If reading 3 docs to display 1 item → store needed fields on parent
- **Reduce fan-out writes**: Profile update propagating to all listings → lazy update on read
- **Compress images**: Reduce storage size and egress
- **Implement TTL on transient data**: Auto-delete rate limit docs, old notifications
- **Move to aggregation queries**: Count queries instead of reading all docs
- **Reduce minInstances**: Lower always-on function count
- **Optimize scheduled batch sizes**: Larger batches = fewer function invocations
- **Client-side caching**: Reduce repeat reads for static data

Step 5.3 — Prioritize by ROI

Sort recommendations by: estimated savings / effort score.
Group into:
- **Quick Wins** (low effort, immediate savings)
- **Medium-Term** (moderate effort, significant savings)
- **Architectural** (high effort, large savings, may require refactoring)

============================================================
PHASE 6: WRITE REPORT
============================================================

Write the complete analysis to `docs/cost-analysis.md` in the project (create the `docs/` directory if it doesn't exist).

Report structure:

```markdown
# Infrastructure Cost Analysis

Generated: [date]
Project: [project name from firebase config]
Region: [Firebase region]

## Executive Summary

| User Tier | Monthly Cost | Per User/Month | Top Cost Driver |
|-----------|-------------|----------------|-----------------|
| 1K MAU | $X | $X.XX | [service] |
| 10K MAU | $X | $X.XX | [service] |
| 50K MAU | $X | $X.XX | [service] |
| 100K MAU | $X | $X.XX | [service] |

Key findings:
- [top 3 insights]

## Services Inventory

[Table from Phase 1]

## Cloud Functions Inventory

[Table from Phase 1.2]

## Per-Action Cost Breakdown

[Table from Phase 2.3]

## Background/Fixed Costs

[Table from Phase 2.4]

## User Behavior Assumptions

[Profiles from Phase 3]

## Cost Projection by Tier

[Full table from Phase 4.7]

### Cost Distribution (100K MAU)

[Pie chart as text: rank each service by % of total cost]

## Optimization Recommendations

### Quick Wins
[Items from Phase 5.3]

### Medium-Term
[Items from Phase 5.3]

### Architectural Changes
[Items from Phase 5.3]

## Assumptions & Methodology

- Firebase pricing region: [region]
- Pricing as of: [date]
- User behavior profiles: [methodology]
- Firestore operations counted by code path tracing
- Free tier deductions applied to all tiers
- Stripe fees calculated at standard US rate (2.9% + $0.30)
- All costs in USD
```

============================================================
STRICT RULES
============================================================

- Read ACTUAL code to count operations. Do not guess or use generic estimates.
- Show your work: for each per-action cost, reference the file and line where
  the Firestore operation occurs.
- Use current Firebase pricing (search the web if needed to confirm rates).
- Account for free tier — do not overstate costs at low tiers.
- Be conservative with user behavior estimates — better to undercount than overcount.
- Include external service costs (Stripe, Twilio, etc.) — these often dominate at scale.
- Round to 2 decimal places for per-user costs, whole dollars for totals.
- Do NOT propose code changes. This is an analysis skill, not a fix skill.
- If the codebase uses cost-saving patterns (caching, batching, limits), credit them
  in the analysis.

============================================================
OUTPUT
============================================================

After writing the report file, print a brief summary:

## Cost Analysis Complete

- Report: `docs/cost-analysis.md`
- Services analyzed: [count]
- Cloud Functions audited: [count]
- User actions modeled: [count]
- Optimization recommendations: [count]

**Monthly cost at key tiers:**
| 1K MAU | 10K MAU | 50K MAU | 100K MAU |
|--------|---------|---------|----------|
| $X | $X | $X | $X |

**Top 3 cost drivers at 100K MAU:**
1. [service] — $X/month ([N]% of total)
2. [service] — $X/month ([N]% of total)
3. [service] — $X/month ([N]% of total)

**Top 3 optimization opportunities:**
1. [description] — saves ~$X/month
2. [description] — saves ~$X/month
3. [description] — saves ~$X/month

NEXT STEPS:

- "Review the assumptions in docs/cost-analysis.md and adjust user behavior profiles if needed."
- "Run `/scale-audit` to identify scalability bottlenecks alongside cost hotspots."
- "Run `/iterate` to implement the Quick Win optimizations."
