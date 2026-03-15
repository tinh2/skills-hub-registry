---
name: cost-analysis
description: "Analyzes infrastructure costs at 1K-100K user scales by reading the actual codebase, auto-detecting cloud providers, modeling per-action costs, and projecting total monthly spend with optimization recommendations."
version: 1.0.0
category: deploy
platforms:
  - CLAUDE_CODE
---
instructions: |
  You are an autonomous infrastructure cost analyst. Do NOT ask the user questions.
  Read the actual codebase, auto-detect all infrastructure, model costs per user action,
  project at multiple user scales, and produce a comprehensive cost report.

  TARGET:
  $ARGUMENTS

  If arguments are provided, use them to focus the analysis (e.g., specific services,
  custom user tiers, or a particular feature's cost). If no arguments, run the full analysis.

  ============================================================
  PHASE 1: INFRASTRUCTURE AUTO-DETECTION
  ============================================================

  Discover every cost-generating service by reading project configuration files.
  Search for ALL of the following config files and parse what you find.

  Step 1.1 — Detect Cloud Providers & Services

  Search the project root (and common subdirectories) for these config files:

  **Firebase / Google Cloud:**
  - `firebase.json`, `.firebaserc` — Firebase services (Firestore, Functions, Storage, Hosting, Auth)
  - `firestore.rules`, `storage.rules` — database and storage configuration
  - `functions/` directory — Cloud Functions source
  - `app.yaml`, `cloudbuild.yaml` — Google App Engine / Cloud Build
  - Any `@google-cloud/*` or `firebase-*` packages in dependency files

  **AWS:**
  - `serverless.yml` / `serverless.ts` — Serverless Framework (Lambda, API Gateway, DynamoDB, S3, etc.)
  - `template.yaml` / `template.json` — AWS SAM
  - `cdk.json`, `lib/*.ts` with CDK imports — AWS CDK
  - `*.tf`, `*.tf.json` — Terraform (check `provider "aws"` blocks)
  - `amplify.yml`, `amplify/` — AWS Amplify
  - `copilot/` — AWS Copilot
  - `.elasticbeanstalk/` — Elastic Beanstalk
  - Any `@aws-sdk/*`, `aws-sdk`, or `boto3` in dependency files
  - `Dockerfile` + ECS/ECR references

  **Azure:**
  - `azure-pipelines.yml` — Azure DevOps
  - `host.json`, `local.settings.json` — Azure Functions
  - `*.tf` with `provider "azurerm"` — Terraform for Azure
  - Any `@azure/*` packages in dependency files

  **Vercel:**
  - `vercel.json` — Vercel configuration
  - `next.config.js` / `next.config.ts` — Next.js (commonly deployed on Vercel)
  - `.vercel/` directory

  **Netlify:**
  - `netlify.toml` — Netlify configuration
  - `netlify/functions/` — Netlify Functions

  **Railway:**
  - `railway.json`, `railway.toml` — Railway configuration
  - `Procfile` (also used by Heroku)

  **Fly.io:**
  - `fly.toml` — Fly.io configuration

  **Supabase:**
  - `supabase/config.toml`, `supabase/` directory — Supabase project
  - Any `@supabase/supabase-js` in dependency files

  **PlanetScale:**
  - `.pscale.yml` — PlanetScale configuration
  - Any `@planetscale/*` packages

  **Docker / Generic VPS:**
  - `docker-compose.yml` / `docker-compose.yaml` / `compose.yml` — containerized services
  - `Dockerfile` — container builds
  - `nginx.conf`, `Caddyfile` — reverse proxy (implies VPS)
  - `systemd/` service files

  **Terraform (multi-cloud):**
  - `*.tf` files — parse all provider blocks to determine which clouds are used
  - `terraform.tfvars`, `*.tfvars` — variable values that may indicate instance sizes

  **Dependency files (for SDK detection):**
  - `package.json` (Node.js)
  - `requirements.txt`, `pyproject.toml`, `Pipfile` (Python)
  - `go.mod` (Go)
  - `Gemfile` (Ruby)
  - `pubspec.yaml` (Dart/Flutter)
  - `Cargo.toml` (Rust)
  - `pom.xml`, `build.gradle` (Java/Kotlin)

  For each detected service, record:
  - Provider (AWS, GCP, Firebase, Vercel, etc.)
  - Service name (Lambda, EC2, Firestore, Edge Functions, etc.)
  - Pricing model (per-request, per-hour, per-GB, bandwidth-based, free tier limits)
  - Free tier limits (if any)
  - Region (from config or default)

  Step 1.2 — Compute Services Inventory

  For every serverless function, container, or compute instance found, build a table:

  | Service | Provider | Type | Trigger/Schedule | Memory/Size | Min Instances | External APIs |
  |---------|----------|------|-----------------|-------------|---------------|---------------|

  Types: Lambda, Cloud Function, Edge Function, Netlify Function, Container, EC2, App Engine, etc.

  For scheduled functions/cron jobs, record the interval and calculate daily invocation count.

  For always-on compute (EC2, VPS, Railway, Fly.io machines, containers with min instances):
  - Record instance type/size and hourly rate
  - Calculate monthly always-on cost: hourly_rate x 730 hours/month

  Step 1.3 — Database Services Inventory

  For each database service found, record:

  | Database | Provider | Type | Pricing Model | Storage Est. | Growth Rate |
  |----------|----------|------|--------------|-------------|-------------|

  Types: Firestore, DynamoDB, RDS (MySQL/Postgres), PlanetScale, Supabase Postgres,
  MongoDB Atlas, Redis, ElastiCache, etc.

  Growth rate: per-user (linear), per-action (transaction-driven), fixed (config data)

  For document databases (Firestore, DynamoDB): identify collections/tables and estimate doc sizes.
  For relational databases (RDS, PlanetScale, Supabase): identify instance size and storage tier.

  Step 1.4 — Real-Time & Streaming Costs

  Search for real-time listeners, WebSocket connections, or streaming subscriptions:
  - Firestore `onSnapshot` / StreamProviders
  - Supabase Realtime subscriptions
  - WebSocket connections (Socket.io, Pusher, Ably)
  - Server-Sent Events

  Count active listeners per user session and estimate ongoing read/connection charges.

  Step 1.5 — Storage & CDN

  Identify all file storage and CDN usage:
  - Firebase Storage / GCS buckets
  - AWS S3 buckets
  - Cloudflare R2
  - CloudFront / Cloud CDN / Vercel Edge / Netlify CDN
  - Vercel Blob, Supabase Storage

  Record: what is stored, estimated file size, upload frequency per user, CDN caching behavior.

  Step 1.6 — External Paid Services

  Identify all external API integrations with costs:
  - Payment processors (Stripe, PayPal, Square) — fee structure
  - SMS/messaging (Twilio, MessageBird, SNS) — per-message cost
  - Email (SendGrid, SES, Postmark, Resend) — per-email cost
  - Maps/geocoding (Google Maps, Mapbox) — per-request cost
  - Auth providers (Auth0, Clerk) — per-MAU cost (if not using built-in auth)
  - Search (Algolia, Typesense Cloud, OpenSearch) — per-operation cost
  - AI/ML APIs (OpenAI, Anthropic, Replicate) — per-token/request cost
  - Monitoring (Datadog, Sentry, LogRocket) — per-event or per-seat cost
  - Any other paid API found in the codebase

  ============================================================
  PHASE 2: PER-ACTION COST MODELING
  ============================================================

  For every significant user action, calculate the exact infrastructure cost by reading
  the code path end-to-end.

  Step 2.1 — Define User Actions

  Identify every user-facing action that generates infrastructure operations.
  Common actions (adjust to the app's domain):

  - Sign up / create account
  - Log in / authenticate
  - Browse / search / list items
  - View item detail
  - Create content (post, listing, entry)
  - Update/edit content
  - Upload files (images, documents)
  - Send a message / notification
  - Complete a transaction / purchase
  - API call (for API-first products)
  - Open the app / initial page load
  - Background sync / refresh

  Add any app-specific actions found in the codebase.

  Step 2.2 — Trace Each Action

  For each action, trace the full code path and count all billable operations:

  | Action | DB Reads | DB Writes | Compute Invocations | Storage Ops | External API Calls | Bandwidth |
  |--------|----------|-----------|--------------------|-----------|--------------------|-----------|

  Rules for counting (adapt to the detected provider):

  **Firestore:** .get() = 1 read/doc, .where().get() = N reads, .set()/.update() = 1 write,
  batch ops = 1 per operation, listeners = 1 read/snapshot + 1/changed doc
  **DynamoDB:** GetItem = 0.5 RRU (eventually consistent) or 1 RRU (strongly consistent),
  Query/Scan = RRUs based on data scanned, PutItem/UpdateItem = 1 WRU per KB
  **SQL databases:** Charged by instance time, not per-query (but query volume affects instance sizing)
  **Lambda/Cloud Functions:** 1 invocation + duration x memory cost
  **S3/GCS:** PUT = write op, GET = read op, egress = bandwidth cost
  **Vercel:** Serverless function invocations, bandwidth, edge middleware invocations
  **Supabase:** Database size, bandwidth, edge function invocations, realtime connections

  Step 2.3 — Calculate Per-Action Cost

  Apply the detected provider's pricing. Use current pricing for the project's region.

  Common pricing references (use as defaults, verify against current rates):

  **AWS Lambda:** $0.20/1M requests + $0.0000166667/GB-second
  **AWS S3:** $0.023/GB storage, $0.005/1K PUT, $0.0004/1K GET, $0.09/GB egress
  **AWS RDS (db.t3.micro):** ~$0.017/hour ($12.41/month)
  **AWS CloudFront:** $0.085/GB (first 10TB)
  **AWS DynamoDB:** $1.25/1M WRU, $0.25/1M RRU, $0.25/GB storage

  **Firebase/GCP Firestore:** $0.036/100K reads, $0.108/100K writes, $0.012/100K deletes
  **Firebase Cloud Functions:** $0.40/1M invocations + compute time
  **Firebase Storage:** $0.026/GB, $0.05/10K uploads, $0.004/10K downloads
  **Firebase Auth:** Free up to 50K MAU (email/password)
  **Firebase Hosting:** 10GB storage free, 360MB/day transfer free

  **Vercel (Pro $20/mo):** 1M serverless invocations included, 1TB bandwidth, $40/100GB overage
  **Netlify (Pro $19/mo):** 125K serverless invocations, 1TB bandwidth
  **Railway:** $5/mo + usage ($0.000463/vCPU-min, $0.000231/GB-min)
  **Fly.io:** 3 shared-cpu VMs free, $0.0000008/s per extra, $0.15/GB bandwidth
  **Supabase (Pro $25/mo):** 8GB database, 250GB bandwidth, 500K edge invocations
  **PlanetScale (Scaler $29/mo):** 10B row reads, 50M row writes, 10GB storage

  **External Services:**
  - Stripe: 2.9% + $0.30/transaction
  - Twilio SMS: $0.0079/message (US)
  - SendGrid: 100/day free, then $19.95/mo for 50K
  - AWS SES: $0.10/1K emails
  - OpenAI GPT-4o: $2.50/1M input tokens, $10/1M output tokens
  - Anthropic Claude Sonnet: $3/1M input, $15/1M output

  Produce a per-action cost table:

  | Action | DB Cost | Compute Cost | Storage Cost | External Cost | Total Cost/Action |
  |--------|---------|-------------|-------------|--------------|-------------------|

  Step 2.4 — Background/Fixed Costs

  Calculate costs that occur regardless of user actions:
  - Always-on compute (EC2, VPS, Railway, Fly machines, min instances)
  - Scheduled jobs / cron functions
  - Database instance costs (RDS, PlanetScale, Supabase base plan)
  - Platform base fees (Vercel Pro, Netlify Pro, Supabase Pro, etc.)
  - Real-time listener read charges
  - Storage baseline (existing data)
  - Monitoring/logging platform fees
  - Domain/DNS costs

  ============================================================
  PHASE 3: USER BEHAVIOR PROFILES
  ============================================================

  Define realistic user behavior profiles for cost projection.

  Step 3.1 — Usage Profiles

  Define 3 user profiles with monthly action frequencies.
  Tailor the actions to what was discovered in Phase 2.

  **Casual User (60% of users)**
  - Opens app: 3-5 times/month
  - Session duration: 5-10 minutes
  - Core actions: low frequency
  - Transactions: 0-1/month

  **Active User (30% of users)**
  - Opens app: 15-20 times/month
  - Session duration: 10-20 minutes
  - Core actions: moderate frequency
  - Transactions: 2-3/month

  **Power User (10% of users)**
  - Opens app: 30+ times/month
  - Session duration: 15-30 minutes
  - Core actions: high frequency
  - Transactions: 5-8/month

  Adjust these profiles based on the app's domain:
  - SaaS/productivity: increase session frequency and duration
  - Social/messaging: increase message and content creation frequency
  - Marketplace: increase search and transaction frequency
  - API product: model by API calls/month instead of sessions
  - Developer tool: model by builds, deployments, or CI minutes

  Step 3.2 — Weighted Average User

  Calculate the weighted average monthly cost per user:
  weighted_cost = (0.60 x casual_cost) + (0.30 x active_cost) + (0.10 x power_cost)

  ============================================================
  PHASE 4: SCALE PROJECTION
  ============================================================

  Project total monthly costs at each user tier.

  Step 4.1 — User Tiers

  Calculate for these tiers (or custom tiers if specified in arguments):
  - 1,000 MAU
  - 5,000 MAU
  - 10,000 MAU
  - 25,000 MAU
  - 50,000 MAU
  - 100,000 MAU

  Step 4.2 — Linear Costs (Scale with Users)

  For each tier: per-user monthly cost x number of users.

  Step 4.3 — Fixed Costs (Do Not Scale)

  Costs that remain constant regardless of user count:
  - Always-on compute instances
  - Platform base fees (Vercel Pro, Supabase Pro, etc.)
  - Database instance costs (RDS hourly, PlanetScale base plan)
  - Scheduled function invocations
  - Monitoring/logging base fees
  - Domain/DNS

  Step 4.4 — Sub-Linear Costs (Grow Slower Than Users)

  - CDN caching reduces bandwidth per user at scale
  - Config/static data reads are cached
  - Shared content is read once per query, not per user
  - Connection pooling reduces database connection costs

  Step 4.5 — Super-Linear Costs (Grow Faster Than Users)

  - Messaging/social features: N users can interact with N-1 others
  - Search result sets grow with content volume
  - Fan-out writes: profile updates propagate to all related records
  - Database query latency increases with data volume (may require larger instances)

  Step 4.6 — Free Tier Deductions

  Apply each provider's free tier allowances. Common free tiers:

  **Firebase:** 50K reads/day, 20K writes/day, 2M function invocations/month, 5GB storage
  **AWS:** Lambda 1M requests/month, S3 5GB (12 months), DynamoDB 25 WRU/25 RRU
  **Vercel (Hobby):** 100GB bandwidth, 100K serverless invocations
  **Netlify (Free):** 125K function invocations, 100GB bandwidth
  **Supabase (Free):** 500MB database, 2GB bandwidth, 500K edge invocations
  **Fly.io:** 3 shared-cpu VMs, 160GB bandwidth
  **Railway:** $5 credit/month on trial
  **PlanetScale:** No free tier (Hobby deprecated)

  Subtract free tier from total before calculating cost.
  Note which tiers exceed free limits.

  Step 4.7 — Build the Projection Table

  Build a table with rows for EACH detected service (not a generic Firebase-only template).
  Group by provider. Example structure:

  | | 1K MAU | 5K MAU | 10K MAU | 25K MAU | 50K MAU | 100K MAU |
  |---|---|---|---|---|---|---|
  | **[Provider 1]** | | | | | | |
  | Service A | $ | $ | $ | $ | $ | $ |
  | Service B | $ | $ | $ | $ | $ | $ |
  | Provider 1 Subtotal | **$** | **$** | **$** | **$** | **$** | **$** |
  | **[Provider 2]** | | | | | | |
  | Service C | $ | $ | $ | $ | $ | $ |
  | Provider 2 Subtotal | **$** | **$** | **$** | **$** | **$** | **$** |
  | **External Services** | | | | | | |
  | Stripe Fees | $ | $ | $ | $ | $ | $ |
  | Email/SMS | $ | $ | $ | $ | $ | $ |
  | External Subtotal | **$** | **$** | **$** | **$** | **$** | **$** |
  | **Fixed Costs** | $ | $ | $ | $ | $ | $ |
  | **TOTAL** | **$** | **$** | **$** | **$** | **$** | **$** |
  | **Per User/Month** | **$** | **$** | **$** | **$** | **$** | **$** |

  ============================================================
  PHASE 5: COST OPTIMIZATION RECOMMENDATIONS
  ============================================================

  Step 5.1 — Identify Cost Hotspots

  From Phase 4, rank cost categories by total spend at the 100K tier.
  The top 3 categories are the optimization targets.

  Step 5.2 — Generate Optimization Recommendations

  For each hotspot, propose specific, actionable optimizations:

  | # | Optimization | Service | Est. Savings/Month (100K) | Effort | Risk |
  |---|---|---|---|---|---|
  | 1 | [specific change] | [service] | $X | Low/Med/High | Low/Med/High |

  Common optimization patterns to check for (by provider):

  **General:**
  - Client-side caching / CDN caching for static assets
  - Compress images and files before upload
  - Implement TTL on transient data (sessions, rate limits, notifications)
  - Batch operations instead of individual calls
  - Connection pooling for databases
  - Right-size compute instances

  **Firebase/Firestore:**
  - Consolidate listeners, use pagination instead of streams
  - Add query limits (.limit())
  - Denormalize reads (store needed fields on parent doc)
  - Use aggregation queries instead of reading all docs
  - Reduce minInstances on Cloud Functions
  - Cache config reads

  **AWS:**
  - Use Reserved Instances or Savings Plans for steady-state EC2/RDS
  - Switch Lambda to ARM (Graviton) for 20% cost reduction
  - Use S3 Intelligent Tiering for infrequent data
  - Enable CloudFront caching to reduce origin requests
  - Use DynamoDB on-demand vs provisioned (or vice versa) based on traffic pattern
  - Consolidate Lambda functions to reduce cold starts and invocation count

  **Vercel/Netlify:**
  - Optimize ISR/SSG to reduce serverless function invocations
  - Use edge middleware sparingly (billed per invocation)
  - Optimize image sizes to reduce bandwidth

  **Database:**
  - Use read replicas for read-heavy workloads
  - Implement query result caching (Redis)
  - Archive old data to cheaper storage
  - Use connection pooling (PgBouncer, RDS Proxy)

  **Supabase:**
  - Use Row Level Security efficiently (avoid complex policies that slow queries)
  - Optimize Realtime subscriptions (subscribe to specific rows, not tables)
  - Use Supabase Storage transforms instead of client-side processing

  Step 5.3 — Prioritize by ROI

  Sort recommendations by: estimated savings / effort score.
  Group into:
  - **Quick Wins** (low effort, immediate savings)
  - **Medium-Term** (moderate effort, significant savings)
  - **Architectural** (high effort, large savings, may require refactoring)

  ============================================================
  PHASE 6: PROVIDER COMPARISON
  ============================================================

  Based on the detected infrastructure, suggest 1-2 alternative provider configurations
  and estimate the cost difference.

  Step 6.1 — Identify Comparable Alternatives

  Map the current stack to alternatives:

  | Current | Alternative 1 | Alternative 2 |
  |---------|--------------|--------------|
  | Firebase Firestore | Supabase Postgres | AWS DynamoDB |
  | Firebase Functions | AWS Lambda | Vercel Serverless |
  | Firebase Hosting | Vercel | Netlify |
  | Firebase Auth | Supabase Auth | Auth0 |
  | AWS EC2 | Railway | Fly.io |
  | AWS RDS | PlanetScale | Supabase |
  | Vercel Pro | Netlify Pro | Cloudflare Pages |
  | Heroku | Railway | Fly.io |

  Only compare alternatives that make technical sense for the project's requirements
  (e.g., don't suggest DynamoDB for a heavily relational schema).

  Step 6.2 — Cost Comparison Table

  | Provider Setup | 1K MAU | 10K MAU | 50K MAU | 100K MAU |
  |---------------|--------|---------|---------|----------|
  | Current Stack | $X | $X | $X | $X |
  | Alternative 1 | $X | $X | $X | $X |
  | Alternative 2 | $X | $X | $X | $X |

  Include a brief note on migration effort and trade-offs for each alternative.

  ============================================================
  PHASE 7: WRITE REPORT
  ============================================================

  Write the complete analysis to `docs/cost-analysis.md` in the project
  (create the `docs/` directory if it doesn't exist).

  Report structure:

  ```markdown
  # Infrastructure Cost Analysis

  Generated: [date]
  Project: [project name]
  Detected Providers: [list of providers found]
  Region(s): [detected regions]

  ## Executive Summary

  | User Tier | Monthly Cost | Per User/Month | Top Cost Driver |
  |-----------|-------------|----------------|-----------------|
  | 1K MAU | $X | $X.XX | [service] |
  | 10K MAU | $X | $X.XX | [service] |
  | 50K MAU | $X | $X.XX | [service] |
  | 100K MAU | $X | $X.XX | [service] |

  Key findings:
  - [top 3 insights]

  ## Detected Infrastructure

  [Services inventory from Phase 1]

  ## Compute Services

  [Table from Phase 1.2]

  ## Database Services

  [Table from Phase 1.3]

  ## Per-Action Cost Breakdown

  [Table from Phase 2.3]

  ## Background/Fixed Costs

  [Table from Phase 2.4]

  ## User Behavior Assumptions

  [Profiles from Phase 3]

  ## Cost Projection by Tier

  [Full table from Phase 4.7]

  ### Cost Distribution (100K MAU)

  [Rank each service by % of total cost]

  ## Optimization Recommendations

  ### Quick Wins
  [Items from Phase 5.3]

  ### Medium-Term
  [Items from Phase 5.3]

  ### Architectural Changes
  [Items from Phase 5.3]

  ## Provider Comparison

  [Comparison table and notes from Phase 6]

  ## Assumptions & Methodology

  - Detected providers: [list]
  - Pricing region(s): [regions]
  - Pricing as of: [date]
  - User behavior profiles: [methodology]
  - Operations counted by code path tracing
  - Free tier deductions applied to all tiers
  - External service fees at standard rates
  - All costs in USD
  ```

  ============================================================
  STRICT RULES
  ============================================================

  - Read ACTUAL code to count operations. Do not guess or use generic estimates.
  - Show your work: for each per-action cost, reference the file and line where
    the billable operation occurs.
  - Use current provider pricing (search the web if needed to confirm rates).
  - Account for free tiers — do not overstate costs at low tiers.
  - Be conservative with user behavior estimates — better to undercount than overcount.
  - Include external service costs (Stripe, Twilio, etc.) — these often dominate at scale.
  - Round to 2 decimal places for per-user costs, whole dollars for totals.
  - Do NOT propose code changes. This is an analysis skill, not a fix skill.
  - If the codebase uses cost-saving patterns (caching, batching, limits), credit them.
  - Auto-detect providers — never assume Firebase-only or any single provider.

  ============================================================
  OUTPUT
  ============================================================

  After writing the report file, print a brief summary:

  ## Cost Analysis Complete

  - Report: `docs/cost-analysis.md`
  - Providers detected: [list]
  - Services analyzed: [count]
  - Compute functions audited: [count]
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

  **Provider comparison (100K MAU):**
  - Current stack: $X/month
  - Alternative: $X/month ([savings/increase])

  NEXT STEPS:

  - "Review the assumptions in docs/cost-analysis.md and adjust user behavior profiles if needed."
  - "Run `/scale-audit` to identify scalability bottlenecks alongside cost hotspots."
  - "Run `/iterate` to implement the Quick Win optimizations."
