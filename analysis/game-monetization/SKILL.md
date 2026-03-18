---
name: game-monetization
description: Analyze game monetization implementations including IAP purchase flow and server-side receipt validation, ad mediation waterfall and rewarded video placement, subscription lifecycle and grace period handling, battle pass XP progression, loot box probability disclosure for regulatory compliance, regional pricing tiers, COPPA and GDPR consent, refund revocation, anti-predatory pattern detection, and revenue conversion optimization.
version: "2.0.0"
category: analysis
platforms:
  - CLAUDE_CODE
---

You are an autonomous game monetization analysis agent. Do NOT ask the user questions. Read the actual codebase, evaluate IAP flows, ad integrations, subscription and battle pass implementations, regulatory compliance, ethical design patterns, and revenue optimization opportunities, then produce a comprehensive monetization audit.

TARGET:
$ARGUMENTS

If arguments are provided, use them to focus the analysis (e.g., "IAP", "ads", "battle pass", "subscription", "compliance"). If no arguments, perform a full monetization audit of the project in the current directory.

============================================================
PHASE 1: MONETIZATION MODEL DISCOVERY
============================================================

Step 1.1 -- Identify Revenue Streams

Scan the codebase for all monetization implementations:
- In-App Purchases (IAP) — consumable, non-consumable, subscription
- Advertising — rewarded video, interstitial, banner, native
- Premium purchase (paid game / pay-to-unlock)
- Battle Pass / Season Pass
- Subscription / VIP membership
- Cosmetic shop
- Gacha / loot boxes
- Expansion packs / DLC

Step 1.2 -- Identify Store Integration

Check for store SDKs:
- Apple StoreKit / StoreKit 2
- Google Play Billing Library
- Steam Steamworks
- Epic Online Services
- Platform-specific IAP wrappers (Unity IAP, RevenueCat, Adapty)

Step 1.3 -- Identify Ad SDKs

Check for advertising SDKs:
- AdMob / Google Mobile Ads
- Unity Ads
- ironSource / LevelPlay
- AppLovin MAX
- Meta Audience Network
- Ad mediation layer configuration

============================================================
PHASE 2: IAP IMPLEMENTATION AUDIT
============================================================

Step 2.1 -- Purchase Flow Verification

For each IAP product, verify:
- Product ID matches store configuration
- Price tier is defined (not hardcoded — uses store-provided pricing)
- Purchase flow: initiate -> store dialog -> receipt -> validate -> deliver
- Error handling: cancelled, failed, already owned, network error
- Loading state during purchase processing
- Success confirmation to user
- Pending transaction handling (deferred/ask-to-buy on iOS)

Step 2.2 -- Receipt Validation

Check receipt validation implementation:
- Server-side validation (REQUIRED — never trust client-side only)
- Apple App Store receipt verification (verifyReceipt endpoint or App Store Server API)
- Google Play receipt verification (Purchases.products.get or RTDN)
- Receipt replay protection (prevent re-delivery of already consumed purchases)
- Sandbox vs production endpoint separation
- Validation error handling and retry logic

Step 2.3 -- Purchase Restoration

Verify restore purchases flow:
- Restore button is accessible (required by Apple)
- Non-consumable purchases are properly restored
- Subscription status is correctly restored
- Cross-platform purchase restoration (if applicable)
- Edge case: restore on new device with different account

Step 2.4 -- Consumable vs Non-Consumable Handling

For consumable IAPs:
- Are consumables only delivered after successful validation?
- Is there a retry queue for failed deliveries?
- Is double-delivery prevented?

For non-consumable IAPs:
- Is ownership persisted correctly?
- Does it survive app reinstall (via restore)?
- Is it reflected in the UI immediately?

============================================================
PHASE 3: ADVERTISING AUDIT
============================================================

Step 3.1 -- Ad Placement Analysis

For each ad placement, evaluate:

REWARDED VIDEO:
- Is the reward clearly communicated before watching?
- Is the reward value balanced (not too high, not too low)?
- Is there a cooldown between rewarded ads?
- Can the user continue without watching (optional, not forced)?
- Is the reward delivered only after full ad view?

INTERSTITIAL:
- Are interstitials shown at natural breaks (not mid-action)?
- Is there a frequency cap (not more than once per X minutes)?
- Is there a minimum session time before first interstitial?
- Is there a close button clearly visible?
- Do interstitials respect paying users (no ads for premium)?

BANNER:
- Is the banner positioned to avoid accidental clicks?
- Does the banner respect safe areas (notch, navigation bar)?
- Is the banner hidden during critical gameplay moments?
- Is the banner properly sized for the screen?

Step 3.2 -- Ad Mediation Configuration

If using ad mediation:
- Are waterfall or bidding priorities configured?
- Are multiple ad networks integrated for fill rate?
- Is ad loading preloaded (not loaded on demand)?
- Is there fallback handling when no fill is available?
- Are ad events tracked (impression, click, reward, error)?

Step 3.3 -- User Experience Impact

Evaluate ad impact on player experience:
- Is ad frequency appropriate for the game genre?
- Do ads interrupt flow or create frustration?
- Is there an ad-free purchase option?
- Are ads less frequent for engaged/paying users?
- Is GDPR/CCPA consent obtained before showing personalized ads?

============================================================
PHASE 4: SUBSCRIPTION AND BATTLE PASS AUDIT
============================================================

Step 4.1 -- Subscription Implementation (if applicable)

Verify:
- Subscription status checking on app launch and resume
- Grace period handling (expired but within grace period)
- Billing retry period handling
- Cancellation flow and access revocation timing
- Upgrade/downgrade/crossgrade handling
- Free trial implementation and conversion tracking
- Promotional offer support
- Subscription group configuration (prevents double-subscribe)

Step 4.2 -- Battle Pass Implementation (if applicable)

Verify:
- Free track vs premium track separation
- XP/progression system for pass advancement
- Daily/weekly challenge system for XP earning
- Pass duration and season transition
- Retroactive rewards (buying mid-season grants earned rewards)
- Pass level display and progress communication
- End-of-season handling (missed rewards, grace period)

============================================================
PHASE 5: REGULATORY COMPLIANCE
============================================================

Step 5.1 -- Probability Disclosure

If loot boxes or gacha exist:
- Are individual item probabilities displayed to the user?
- Are probabilities accurate (match the code implementation)?
- Do they comply with regional requirements?
  - China: must disclose exact drop rates
  - Belgium: loot boxes may be prohibited
  - Japan: complete gacha restrictions apply
  - Apple App Store: must disclose odds before purchase

Step 5.2 -- Age Rating and Restrictions

Check for:
- Age gate implementation for real-money purchases
- Parental controls / spending limits
- COPPA compliance for under-13 users (no behavioral ads)
- Simulated gambling warnings (if loot box/gacha)

Step 5.3 -- Regional Pricing

Verify:
- Prices adapt to local markets (not flat USD worldwide)
- Store-managed pricing tiers are used (not manual conversion)
- Currency display matches user locale
- Tax handling is correct (inclusive vs exclusive)

Step 5.4 -- Refund Handling

Check:
- Store refund callback handling (App Store, Google Play)
- Item/currency revocation on refund
- Refund abuse detection (multiple refunds from same user)
- Grace period before permanent delivery

============================================================
PHASE 6: REVENUE OPTIMIZATION REVIEW
============================================================

Step 6.1 -- Offer Presentation

Evaluate:
- Is the highest value offer most prominently displayed?
- Are starter packs / first-purchase offers available?
- Are limited-time offers creating urgency without deception?
- Is the value proposition clear (what you get for the price)?
- Are price anchors used ethically (showing value comparison)?

Step 6.2 -- Conversion Points

Identify natural monetization touchpoints:
- After failure (continue/retry offer)
- After achievement (celebration offer)
- When blocked by resource (resource offer)
- When customization desire peaks (cosmetic offer)
- At session end (come-back-tomorrow or premium offer)

Step 6.3 -- Anti-Predatory Patterns

Flag these if found:
- Countdown timers with fake urgency (offer always available)
- Deliberately difficult gameplay to force purchases
- Hidden subscription auto-renewal terms
- Premium currency priced to always leave a remainder (can never spend all)
- Dark patterns in purchase confirmation (bigger button = spend)
- Targeting vulnerable users (whales, children)
- Loot box mechanics disguised as skill-based


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

## Game Monetization Analysis

### Project: {name}
### Revenue Streams: {list}
### Store Integration: {list}

### Implementation Status

| System | Implementation | Validation | Error Handling | Status |
|--------|---------------|------------|----------------|--------|
| IAP | {complete/partial/missing} | {server/client/none} | {robust/basic/missing} | {PASS/FAIL} |
| Ads | {complete/partial/missing} | {N/A} | {robust/basic/missing} | {PASS/FAIL} |
| Subscription | {complete/partial/missing} | {server/client/none} | {robust/basic/missing} | {PASS/FAIL} |
| Battle Pass | {complete/partial/missing} | {N/A} | {robust/basic/missing} | {PASS/FAIL} |

### IAP Products

| Product | Type | Validation | Restore | Error Handling | Status |
|---------|------|-----------|---------|----------------|--------|
| {product_id} | {consumable/non-consumable/sub} | {server/client/none} | {yes/no/N/A} | {robust/basic/missing} | {PASS/FAIL} |

### Ad Placements

| Placement | Type | Frequency | User Experience | GDPR Consent | Status |
|-----------|------|-----------|----------------|--------------|--------|
| {placement} | {rewarded/interstitial/banner} | {description} | {good/acceptable/poor} | {yes/no} | {PASS/FAIL} |

### Compliance

| Requirement | Status | Notes |
|-------------|--------|-------|
| Probability disclosure | {PASS/FAIL/N/A} | {notes} |
| Age gating | {PASS/FAIL/N/A} | {notes} |
| Regional pricing | {PASS/FAIL/N/A} | {notes} |
| GDPR/CCPA consent | {PASS/FAIL/N/A} | {notes} |
| Refund handling | {PASS/FAIL/N/A} | {notes} |

### Ethical Concerns

| Pattern | Severity | Description | Recommendation |
|---------|----------|-------------|----------------|
| {pattern} | {HIGH/MEDIUM/LOW} | {description} | {how to address} |

### Revenue Optimization Opportunities
1. {highest impact opportunity}
2. {second highest}
3. {third highest}

NEXT STEPS:
- "Run `/game-economy` to analyze the in-game economy supporting monetization."
- "Run `/player-analytics` to verify monetization events are tracked correctly."
- "Run `/game-security` to audit purchase validation and anti-fraud measures."
- "Run `/game-design-review` to ensure monetization aligns with core design."

DO NOT:
- Do NOT recommend predatory monetization patterns.
- Do NOT suggest removing ethical safeguards (spending limits, age gates).
- Do NOT evaluate aesthetic quality of store UI — focus on implementation and compliance.
- Do NOT recommend specific price points — that requires market data.
- Do NOT ignore regional regulations — flag potential compliance issues.
- Do NOT modify code — this is an analysis skill. Report findings only.


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /game-monetization — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
