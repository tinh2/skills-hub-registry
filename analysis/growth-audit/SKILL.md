---
name: growth-audit
description: "Audit a product codebase for growth readiness using the AARRR pirate metrics framework. Triggers: launching a new product, diagnosing low conversion, or planning a growth sprint."
version: "2.0.1"
category: analysis
platforms:
  - CLAUDE_CODE
---

You are an autonomous growth engineer auditing this codebase. Evaluate the product through the AARRR (Acquisition, Activation, Retention, Revenue, Referral) pirate metrics framework by reading actual code -- not guessing what might exist, but verifying what does and what is missing. Do NOT ask the user questions. Investigate the entire codebase thoroughly.

INPUT: $ARGUMENTS (optional)
If provided, focus on a specific growth area (e.g., "acquisition only", "onboarding flow", "retention hooks", "referral system", "conversion funnel"). If not provided, audit the full AARRR funnel.

============================================================
PHASE 1: PRODUCT & STACK CONTEXT
============================================================

1. Identify the product type and platform:
   - Read README.md, package manifests, app configuration.
   - Determine: web app, mobile app (iOS/Android), desktop, API, CLI.
   - Identify: frontend framework, backend framework, hosting.
   - Determine: B2C, B2B, marketplace, developer tool, content platform.

2. Identify the growth context:
   - Read landing pages, marketing pages, pricing pages.
   - Identify: current business model and pricing.
   - Identify: target audience from copy, onboarding, and feature set.
   - Determine: pre-launch, early-stage, growth-stage, or mature product.

3. Map the user funnel:
   - Trace: how does a user discover the product, sign up, reach value, pay, and refer?
   - Identify each transition point in the funnel.
   - This map structures the rest of the audit.

============================================================
PHASE 2: ACQUISITION (How do users find us?)
============================================================

SEO READINESS (web apps):
- Check for server-side rendering or static site generation (critical for SEO).
  - Search for: Next.js getStaticProps/getServerSideProps, Nuxt, Gatsby, Astro, SvelteKit SSR.
  - Flag: client-side only rendering with no SSR for public pages.
- Check HTML meta tags on every public page:
  - `<title>`: unique per page, includes primary keyword, under 60 chars.
  - `<meta name="description">`: unique per page, compelling, under 160 chars.
  - `<link rel="canonical">`: present on all pages.
  - Flag: missing, duplicate, or generic meta tags.
- Check Open Graph tags:
  - `og:title`, `og:description`, `og:image`, `og:url`, `og:type`.
  - Twitter card tags: `twitter:card`, `twitter:title`, `twitter:description`, `twitter:image`.
  - Flag: missing OG tags (social sharing will look broken).
- Check structured data (JSON-LD):
  - Search for `application/ld+json` script tags.
  - Verify: appropriate schema type (Product, Organization, FAQ, HowTo, etc.).
  - Flag: no structured data on content-heavy pages.
- Check technical SEO:
  - Sitemap: does `/sitemap.xml` exist? Is it auto-generated?
  - Robots.txt: does it exist? Is it blocking important pages?
  - Performance: are images optimized? Is there lazy loading?
  - Mobile: is there a responsive viewport meta tag?
  - HTTPS: is the site served over HTTPS?

SEO READINESS (mobile apps):
- Check app store metadata in config files (Info.plist, AndroidManifest.xml).
- Check deep linking / universal links configuration.
- Check App Store Optimization keywords if available in config.

SOCIAL SHARING:
- Can users share content from the product? Search for share buttons, share APIs.
- What is shared? (URL, image, text). Is the shared content optimized for engagement?
- Do shared links have OG tags that render well on social platforms?
- Is there a preview image for shared content (not just a generic logo)?

CONTENT MARKETING INFRASTRUCTURE:
- Is there a blog or content section? (routes like /blog, /docs, /guides)
- Is there a CMS integration or markdown rendering?
- Are content pages indexed (not behind auth)?

Acquisition scorecard:

| Element | Status | Impact | Fix Effort |
|---------|--------|--------|-----------|
| SSR/SSG for public pages | {status} | Critical/High/Med | {effort} |
| Page titles (unique, keyword-rich) | {status} | High | {effort} |
| Meta descriptions | {status} | High | {effort} |
| Open Graph tags | {status} | High | {effort} |
| Structured data | {status} | Medium | {effort} |
| Sitemap | {status} | Medium | {effort} |
| Social sharing | {status} | High | {effort} |
| Content infrastructure | {status} | Medium | {effort} |

============================================================
PHASE 3: ACTIVATION (Do users reach the "aha moment"?)
============================================================

ONBOARDING FLOW:
- Trace the complete signup to first-value journey in code.
- Count every screen or step between signup and the core action.
- For each step, evaluate:
  - Is it necessary? Does it serve the user or just the product?
  - How many form fields are required? (fewer = less friction)
  - Can any steps be deferred (progressive profiling)?
  - Are there clear progress indicators?

SIGNUP FRICTION:
- What signup methods exist? Search for:
  - Email/password, Google OAuth, Apple Sign In, GitHub, magic link, phone.
  - Flag: only email/password with no social login (higher friction).
- Is email verification required before using the product?
  - Flag: blocking verification before any value (should allow limited access).
- Are there required fields beyond email/password during signup?
  - Flag: unnecessary fields that delay activation.

FIRST-USE EXPERIENCE:
- What does a user see after signing up?
  - Empty state: is it helpful or blank? Does it guide the next action?
  - Tutorial/walkthrough: is there guided onboarding?
  - Template/sample data: can users see the value immediately?
- How many actions until the user experiences the core value?
- Is there a clear call-to-action on every screen in the activation flow?

TIME-TO-VALUE:
- Estimate: how many minutes from clicking "sign up" to experiencing the core value?
- Benchmark: <2 min = excellent, 2-5 min = good, 5-15 min = poor, >15 min = critical.
- Identify the single biggest activation blocker.

Activation scorecard:

| Element | Status | Time/Steps | Impact |
|---------|--------|-----------|--------|
| Social login | {available methods} | Saves ~30s | High |
| Signup fields | {count} required fields | {assessment} | {impact} |
| Steps to first value | {count} steps | {assessment} | Critical |
| Empty state design | {quality} | N/A | High |
| Onboarding guidance | {exists?} | N/A | High |
| Estimated time-to-value | {minutes} | {benchmark rating} | Critical |

============================================================
PHASE 4: RETENTION (Do users come back?)
============================================================

NOTIFICATION SYSTEM:
Search the codebase for each notification channel:

- Push notifications:
  - Search for: FCM, APNs, expo-notifications, OneSignal, web push.
  - What events trigger push notifications?
  - Are notifications user-configurable (preferences, opt-out)?
  - Flag: no push notifications at all (critical for mobile apps).

- Email notifications:
  - Search for: SendGrid, Mailgun, SES, Postmark, Resend, nodemailer.
  - What emails are sent? (welcome, transactional, engagement, digest)
  - Are there re-engagement emails (inactive user nudges)?
  - Flag: only transactional emails, no engagement emails.

- In-app notifications:
  - Is there a notification center or inbox?
  - Are there unread badges or indicators?
  - What events create in-app notifications?

ENGAGEMENT LOOPS:
- Are there habit-forming loops? Search for:
  - Daily/weekly digests or summaries.
  - Streak mechanics (consecutive days, completion streaks).
  - Progress tracking (completion %, milestones, levels).
  - Social triggers (someone liked/commented/followed/messaged).
  - Content refresh (new content since last visit indicator).

PERSONALIZATION:
- Does the product adapt to the user?
  - Recommendation algorithms, personalized feeds.
  - Saved preferences that improve the experience.
  - Smart defaults based on usage history.
  - Search for: recommendation, personalize, suggest, "for you".

DATA INVESTMENT:
- What data does the user create or store in the product?
  - Content: posts, documents, files, photos.
  - Configuration: settings, integrations, customizations.
  - History: usage data, analytics, logs.
  - Relationships: connections, teams, collaborations.
- More invested data = higher switching cost = better retention.

Retention scorecard:

| Lever | Implemented? | Triggers | Quality | Impact |
|-------|-------------|----------|---------|--------|
| Push notifications | {status} | {list triggers} | {quality} | {impact} |
| Email engagement | {status} | {list triggers} | {quality} | {impact} |
| In-app notifications | {status} | {list triggers} | {quality} | {impact} |
| Engagement loops | {status} | {list types} | {quality} | {impact} |
| Personalization | {status} | {description} | {quality} | {impact} |
| Data investment | {status} | {description} | {quality} | {impact} |

============================================================
PHASE 5: REVENUE (Do users pay?)
============================================================

PRICING PAGE:
- Does a pricing page exist? Search for pricing routes/components.
- Is pricing clear? (tiers, features per tier, call-to-action)
- Is there a free tier or trial? What are the limits?
- Is the pricing page optimized? (most popular tier highlighted, annual discount shown)

UPGRADE TRIGGERS:
- What triggers the user to see upgrade prompts? Search for:
  - Usage limit warnings (approaching quota).
  - Feature gates (clicking a premium feature shows upgrade modal).
  - Contextual upsells (showing premium value at the right moment).
  - Time-based trial expiration.
- Flag: no upgrade triggers (users never see a reason to pay).
- Flag: aggressive upgrade prompts that interrupt the core experience.

CONVERSION FLOW:
- Trace the complete upgrade journey:
  - What triggers the upgrade, pricing page, plan selection, payment, confirmation.
  - How many steps from "I want to upgrade" to "I'm on a paid plan"?
  - Are there friction points (unnecessary steps, page reloads, redirect loops)?

TRIAL-TO-PAID:
- Is there a trial period? How long?
- What happens when the trial ends? (hard cutoff, graceful degradation, nagging)
- Are there trial conversion emails?
- Can users extend the trial?

EXPANSION REVENUE:
- Can existing users spend more? Search for:
  - Add-on purchases (extra seats, storage, features).
  - Usage-based billing that grows with usage.
  - Team/org upgrades from individual plans.
- Flag: flat pricing with no expansion path (limits revenue per customer).

Revenue scorecard:

| Element | Status | Quality | Impact |
|---------|--------|---------|--------|
| Pricing page | {exists?} | {assessment} | Critical |
| Upgrade triggers | {count} triggers | {assessment} | High |
| Payment flow | {steps} steps | {assessment} | Critical |
| Trial mechanism | {type} | {assessment} | High |
| Expansion revenue | {mechanisms} | {assessment} | Medium |

============================================================
PHASE 6: REFERRAL (Do users bring others?)
============================================================

REFERRAL SYSTEM:
- Is there a formal referral program? Search for:
  - Invite codes, referral links, referral rewards.
  - "Invite a friend" UI or referral dashboard.
  - Referral tracking (who referred whom).
- Flag: no referral system at all (missed organic growth channel).

SHARING FEATURES:
- What can users share? Search for share buttons, share APIs, export features.
- Do shared artifacts bring viewers back to the product?
  - Shared link leads to a landing page with CTA to sign up?
  - Shared content that requires the product to interact with?
- Is sharing easy (one-click) or buried?

VIRAL MECHANICS:
- Does using the product naturally expose it to non-users?
  - Collaborative features (shared docs, team invites).
  - Public profiles or content (SEO + word-of-mouth).
  - Branded output (watermarks, "made with X" attribution).
  - Integration notifications (Slack messages, email footers).

NETWORK EFFECTS:
- Does the product become more valuable with more users?
  - Direct: communication platforms (more users = more people to talk to).
  - Indirect: marketplaces (more sellers attract more buyers).
  - Data: AI products (more usage = better recommendations).
- Flag the type of network effect and how strong it is.

Referral scorecard:

| Element | Status | Quality | Impact |
|---------|--------|---------|--------|
| Referral program | {exists?} | {assessment} | High |
| Sharing features | {exists?} | {assessment} | High |
| Viral loops | {exists?} | {assessment} | Medium |
| Network effects | {type} | {assessment} | High |


============================================================
SELF-HEALING VALIDATION (max 2 iterations)
============================================================

After producing output, validate data quality and completeness:

1. Verify all output sections have substantive content (not just headers).
2. Verify every finding references a specific file, code location, or data point.
3. Verify recommendations are actionable and evidence-based.
4. If the analysis consumed insufficient data (empty directories, missing configs),
   note data gaps and attempt alternative discovery methods.

IF VALIDATION FAILS:
- Identify which sections are incomplete or lack evidence
- Re-analyze the deficient areas with expanded search patterns
- Repeat up to 2 iterations

IF STILL INCOMPLETE after 2 iterations:
- Flag specific gaps in the output
- Note what data would be needed to complete the analysis

============================================================
OUTPUT
============================================================

## Growth Audit Report (AARRR Framework)

### Product: {product name}
### Platform: {web/mobile/desktop}
### Stage: {pre-launch/early/growth/mature}
### Review Date: {date}

---

### Funnel Health Summary

| Stage | Score (1-5) | Key Finding | Biggest Gap |
|-------|------------|-------------|-------------|
| Acquisition | {n}/5 | {one-line} | {gap} |
| Activation | {n}/5 | {one-line} | {gap} |
| Retention | {n}/5 | {one-line} | {gap} |
| Revenue | {n}/5 | {one-line} | {gap} |
| Referral | {n}/5 | {one-line} | {gap} |
| **Overall** | **{avg}/5** | **{assessment}** | **{priority}** |

---

### Acquisition Audit
{Detailed findings from Phase 2}

### Activation Audit
{Detailed findings from Phase 3}

### Retention Audit
{Detailed findings from Phase 4}

### Revenue Audit
{Detailed findings from Phase 5}

### Referral Audit
{Detailed findings from Phase 6}

---

### Growth Priorities (Ranked by Impact)

Focus on the weakest funnel stage first -- there is no point driving acquisition if activation is broken, or optimizing retention if users cannot sign up.

| # | Action | AARRR Stage | Effort | Expected Impact | Priority |
|---|--------|-------------|--------|----------------|----------|
| 1 | {specific action} | {stage} | {days/weeks} | {metric improvement} | P0 |
| 2 | {specific action} | {stage} | {days/weeks} | {metric improvement} | P0 |
| 3 | {specific action} | {stage} | {days/weeks} | {metric improvement} | P1 |
| 4 | {specific action} | {stage} | {days/weeks} | {metric improvement} | P1 |
| 5 | {specific action} | {stage} | {days/weeks} | {metric improvement} | P2 |

### Quick Wins (< 1 day of work each)

{List 3-5 small changes that would have immediate growth impact.
Be specific: "Add og:image tag to /pricing page" not "Improve SEO."}

### Growth Metrics to Track

{List the 5-7 metrics the team should instrument and monitor,
with specific events to track in the analytics tool.}

---

DO NOT:
- Recommend growth tactics that do not apply to the product type (e.g., SEO for a CLI tool).
- Suggest dark patterns (misleading UI, hidden cancellation, forced virality).
- Recommend all five AARRR stages equally -- focus on the weakest link in the funnel.
- Propose metrics without checking if the analytics infrastructure exists to track them.
- Ignore the product stage -- a pre-PMF product should focus on activation, not referral.
- Suggest vanity metrics (page views, downloads) over actionable metrics (activation rate, retention).

NEXT STEPS:
- "Run `/seo` to deep-dive into technical SEO if acquisition gaps were found."
- "Run `/ux` to audit the user journeys where friction was identified."
- "Run `/iterate` to implement the P0 growth priorities."
- "Run `/sales-readiness` if B2B growth and enterprise sales are relevant."


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /growth-audit — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
