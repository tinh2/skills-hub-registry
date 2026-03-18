---
name: analytics-tracking
description: "Set up production-ready event tracking with Amplitude, Mixpanel, PostHog, or GA4. Auto-detects your framework (React, Next.js, Vue, Flutter, Angular, Python, Go, Rails), installs the correct SDK, creates a provider-agnostic analytics service wrapper, defines a typed event taxonomy, instruments page views and key user flows, and adds privacy/consent controls. Use when you need analytics, event tracking, user tracking, product analytics, usage metrics, or telemetry."
version: "2.0.0"
category: integration
platforms:
  - CLAUDE_CODE
---

You are in AUTONOMOUS MODE. Do NOT ask questions. Detect everything from the codebase and proceed.

PURPOSE:
Set up production-ready analytics event tracking. Auto-detect the project's framework and the
requested analytics provider. Install the SDK, create a framework-agnostic analytics service,
define a core event taxonomy, and instrument key user flows.

TASK:
$ARGUMENTS

============================================================
PHASE 0: DETECTION
============================================================

1. FRAMEWORK DETECTION -- scan the project root to identify the tech stack:
   - package.json with "react" or "next" -> React / Next.js
   - package.json with "vue" -> Vue
   - package.json with "angular" -> Angular
   - pubspec.yaml -> Flutter / Dart
   - package.json with "react-native" -> React Native
   - package.json with "svelte" -> SvelteKit
   - requirements.txt or pyproject.toml with "django" or "flask" or "fastapi" -> Python backend
   - go.mod -> Go backend
   - Gemfile with "rails" -> Ruby on Rails
   - If multiple detected (e.g., monorepo), handle each workspace.

2. PROVIDER DETECTION -- determine analytics provider from $ARGUMENTS or existing config:
   - If $ARGUMENTS names a provider, use it.
   - If an existing SDK is installed (check package.json / pubspec.yaml), match it.
   - If no provider specified and none installed, default to PostHog (open-source, self-hostable).
   - Supported providers: Amplitude, Mixpanel, PostHog, Google Analytics 4 (GA4).

3. EXISTING ANALYTICS CHECK -- search for existing analytics wrappers:
   - Grep for "analytics", "track", "mixpanel", "amplitude", "posthog", "gtag" in src/.
   - If a wrapper already exists, extend it rather than creating a duplicate.

============================================================
PHASE 1: SDK INSTALLATION
============================================================

Install the correct SDK for the detected provider and framework:

AMPLITUDE:
  - JS/TS: `@amplitude/analytics-browser` (web), `@amplitude/analytics-node` (server)
  - Flutter: `amplitude_flutter`
  - React Native: `@amplitude/analytics-react-native`

MIXPANEL:
  - JS/TS: `mixpanel-browser` (web), `mixpanel` (server)
  - Flutter: `mixpanel_flutter`
  - React Native: `mixpanel-react-native`

POSTHOG:
  - JS/TS: `posthog-js` (web), `posthog-node` (server)
  - Flutter: `posthog_flutter`
  - React Native: `posthog-react-native`

GA4:
  - JS/TS: `@google-analytics/data` (server), gtag.js snippet (web)
  - Flutter: `firebase_analytics`
  - React Native: `@react-native-firebase/analytics`

After installing:
- Add the API key / project ID to the project's .env or environment config.
- Use placeholder values with clear variable names: `ANALYTICS_API_KEY`, `ANALYTICS_PROJECT_ID`.
- Add these env vars to .env.example if it exists.
- NEVER commit real API keys. Use environment variables exclusively.

============================================================
PHASE 2: ANALYTICS SERVICE
============================================================

Create a framework-agnostic analytics service wrapper. This abstraction lets the team swap
providers without touching feature code.

FILE LOCATION:
  - JS/TS: `src/lib/analytics.ts` or `src/services/analytics.ts`
  - Flutter: `lib/services/analytics_service.dart`
  - Python: `app/services/analytics.py`
  - Go: `internal/analytics/analytics.go`

THE SERVICE MUST EXPOSE:

  init(config)          -- Initialize the SDK with API key and options.
  identify(userId, properties)  -- Set the current user identity and traits.
  track(eventName, properties)  -- Track a named event with arbitrary properties.
  page(name, properties)        -- Track a page/screen view.
  reset()               -- Clear the user identity on logout.
  setUserProperties(properties) -- Update user-level properties without an event.
  group(groupType, groupId)     -- Associate user with a group/company (if supported).
  flush()               -- Force-send queued events (for server-side or before app close).

IMPLEMENTATION REQUIREMENTS:
  - Wrap all SDK calls in try/catch -- analytics must NEVER crash the app.
  - Add a debug mode that logs events to console instead of sending them.
  - Support a kill switch: if `ANALYTICS_ENABLED=false`, all methods become no-ops.
  - Batch events where the SDK supports it (reduce network calls).
  - Include TypeScript types / Dart typing for event names and properties.

============================================================
PHASE 3: EVENT TAXONOMY
============================================================

Create a typed event catalog. This prevents typo-driven event sprawl.

FILE: `src/lib/analytics-events.ts` (or framework equivalent)

CORE EVENTS (define all of these):

  page_view          -- { page_name, referrer?, duration_ms? }
  sign_up            -- { method: "email" | "google" | "github" | "apple", referral_source? }
  login              -- { method, success: boolean }
  logout             -- {}
  purchase           -- { item_id, item_name, price, currency, quantity }
  subscription_start -- { plan, billing_period, trial: boolean }
  feature_used       -- { feature_name, context? }
  search             -- { query, results_count, filters? }
  error_occurred     -- { error_type, error_message, screen?, severity }
  cta_clicked        -- { cta_name, location, destination? }
  onboarding_step    -- { step_number, step_name, completed: boolean }
  share              -- { content_type, method }
  feedback_submitted -- { rating?, comment?, screen? }

RULES:
  - Use snake_case for all event names.
  - Every event must have a typed properties interface/type.
  - Export a single `AnalyticsEvents` enum or const object for autocompletion.
  - Add JSDoc / dartdoc comments explaining when each event fires.

============================================================
PHASE 4: INSTRUMENTATION
============================================================

Wire tracking into the application's key flows:

1. PAGE VIEWS:
   - React/Next.js: Hook into router (usePathname, router.events, or App Router layout).
   - Vue: Router afterEach guard.
   - Flutter: NavigatorObserver or GoRouter redirect.
   - Angular: Router events subscription.
   - Automatic -- no manual calls needed per page.

2. USER IDENTIFICATION:
   - After successful login/signup, call identify() with user ID and initial properties.
   - On logout, call reset().
   - Set super properties: app_version, platform, locale.

3. KEY FLOW INSTRUMENTATION:
   - Instrument sign_up in the registration flow.
   - Instrument login in the authentication flow.
   - Instrument feature_used on 3-5 primary feature entry points.
   - Instrument error_occurred in the global error handler / error boundary.

4. SERVER-SIDE EVENTS (if backend detected):
   - Create server-side analytics client using the node/python/go SDK.
   - Track purchase and subscription_start server-side for accuracy.
   - Use a middleware/decorator pattern to track API-level events.

============================================================
PHASE 5: PRIVACY AND COMPLIANCE
============================================================

1. DNT (Do Not Track):
   - Check `navigator.doNotTrack` (web) before initializing.
   - If DNT is set, disable tracking or limit to anonymous aggregate events.

2. COOKIE CONSENT:
   - Do NOT auto-initialize analytics on page load for web apps.
   - Create a `consentGranted()` method that initializes tracking after user consent.
   - Provide `consentRevoked()` that calls reset() and disables future tracking.

3. GDPR / DATA MINIMIZATION:
   - Never track PII (email, name, phone) in event properties.
   - Use hashed or opaque user IDs, not raw emails.
   - Document which events contain user data in the event catalog.
   - Provide a `deleteUser(userId)` helper that calls the provider's deletion API.

4. APP STORE COMPLIANCE (mobile):
   - Flutter/RN: Add ATT (App Tracking Transparency) prompt for iOS.
   - Add privacy manifest entries for iOS 17+.
   - Respect the user's ATT choice -- disable IDFA-based tracking if denied.

============================================================
PHASE 6: VALIDATION
============================================================

1. Run the project's build/compile step -- fix any errors.
2. Run existing tests -- fix any failures caused by analytics integration.
3. Verify the analytics service can be imported and instantiated without errors.
4. If a dev server is available, confirm no console errors from the analytics SDK.


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /analytics-tracking — {{YYYY-MM-DD}}
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

- Do NOT commit real API keys or project IDs. Use env vars only.
- Do NOT make analytics initialization blocking -- it must not slow app startup.
- Do NOT track events before user consent on web apps.
- Do NOT store analytics data in localStorage/SharedPreferences without consent.
- Do NOT add analytics to test files or test utilities.
- Do NOT create a second analytics wrapper if one already exists -- extend it.
- Do NOT use deprecated SDK versions or legacy tracking APIs.
- Do NOT track raw PII (emails, names, phone numbers) in event properties.


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
OUTPUT
============================================================

## Analytics Tracking Setup

- **Framework**: [detected framework and version]
- **Provider**: [analytics provider configured]
- **SDK**: [package name and version installed]
- **Service**: [path to analytics service file]
- **Events**: [count of defined events, path to event catalog]
- **Instrumented flows**: [list of flows wired up]
- **Privacy**: [DNT, consent, GDPR controls implemented]
- **Server-side**: [yes/no, details if applicable]
- **Build status**: [passing/failing]
- **Caveats**: [any known issues or manual steps remaining]

NEXT STEPS:

After analytics tracking is set up:
- "Run `/ship` to continue building features with tracking already wired in."
- "Run `/search` to add full-text search -- tracking search queries gives great product insight."
- "Run `/qa` to verify analytics events fire correctly in all user flows."
- "Run `/perf` to ensure the analytics SDK does not degrade page load or app startup times."
