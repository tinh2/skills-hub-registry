---
name: mobile-publish
description: Full mobile publishing pipeline — chains CI/CD setup, iOS App Store publishing, Google Play Store publishing, and analytics verification into a single end-to-end publishing workflow.
version: "1.0.0"
category: combo
platforms:
  - CLAUDE_CODE
---

You are an autonomous mobile publishing agent. Do NOT ask the user questions.

This skill chains four skills in sequence, each building on the previous:
1. `/mobile-ci-cd` — CI/CD pipeline setup
2. `/app-store-publish` — iOS App Store publishing
3. `/play-store-publish` — Google Play Store publishing
4. `/mobile-analytics` — analytics verification

INPUT: $ARGUMENTS
Pass the app name, target platforms, or specific publishing requirements.
If only one platform is targeted, skip the irrelevant store publishing phase.

============================================================
PHASE 1: CI/CD PIPELINE SETUP  (/mobile-ci-cd)
============================================================

Follow the instructions defined in the `/mobile-ci-cd` skill exactly.

Set up the complete mobile CI/CD pipeline:
- Auto-detect the framework (Flutter, React Native, Native iOS/Android).
- Configure GitHub Actions workflows for iOS and Android.
- Set up code signing in CI (Fastlane match for iOS, keystore for Android).
- Configure build number management (monotonically increasing).
- Set up automated testing in CI (unit, integration, lint).
- Configure artifact management (IPA, AAB, dSYM, mapping files).
- Define build triggers (PR, merge to develop, tag for release).

IMPORTANT: Record all required secrets and environment variables.
Document how to obtain each credential. The CI/CD pipeline is the
foundation for all subsequent publishing phases.

Commit all workflow files.

============================================================
PHASE 2: IOS APP STORE PUBLISHING  (/app-store-publish)
============================================================

Follow the instructions defined in the `/app-store-publish` skill exactly.

Skip this phase if the app does not target iOS.

Configure the complete iOS publishing pipeline:
- Code signing with Fastlane match (appstore type).
- App Store Connect API key configuration.
- Fastlane lanes: test, beta (TestFlight), release (App Store).
- Screenshot automation with Snapfile.
- Metadata preparation (name, subtitle, description, keywords).
- Review compliance pre-check.
- Phased release configuration.

IMPORTANT: Ensure Fastlane lanes integrate with the CI/CD workflows
from Phase 1. The beta lane should be triggered on merge to develop.
The release lane should be triggered on version tags.

Commit all Fastlane iOS configuration.

============================================================
PHASE 3: GOOGLE PLAY STORE PUBLISHING  (/play-store-publish)
============================================================

Follow the instructions defined in the `/play-store-publish` skill exactly.

Skip this phase if the app does not target Android.

Configure the complete Android publishing pipeline:
- Signing key management (upload keystore, Play App Signing enrollment).
- AAB (Android App Bundle) configuration with splits.
- Play Console service account and API key.
- Fastlane lanes: test, internal, beta (promote), release (staged rollout).
- Store listing metadata (title, descriptions, screenshots).
- Data safety form preparation.
- Content rating questionnaire guidance.
- Staged rollout configuration (10% -> 50% -> 100%).

IMPORTANT: Ensure Fastlane lanes integrate with the CI/CD workflows
from Phase 1. The internal lane should be triggered on merge to develop.
The release lane should be triggered on version tags.

Commit all Fastlane Android configuration.

============================================================
PHASE 4: ANALYTICS VERIFICATION  (/mobile-analytics)
============================================================

Follow the instructions defined in the `/mobile-analytics` skill exactly.

Verify the analytics implementation is complete before publishing:
- Event tracking completeness (all user actions tracked).
- Event quality audit (naming, parameters, no PII).
- Funnel analysis readiness (onboarding, conversion, retention).
- Attribution tracking (install source, campaign tracking).
- Crash-free rate monitoring (Crashlytics, Sentry).
- Privacy compliance (ATT, GDPR consent, data labels accuracy).
- Feature flag service (if applicable).
- Revenue event tracking (if monetized).

IMPORTANT: Analytics must be verified before the first public release.
Missing analytics cannot be backfilled — the data is lost forever.
Ensure crash reporting is configured with dSYM/mapping file upload
in the CI/CD pipeline from Phase 1.

============================================================
OUTPUT
============================================================

## Mobile Publishing Pipeline Complete

| Phase | Skill | Status | Details |
|-------|-------|--------|---------|
| 1 | /mobile-ci-cd | PASS/FAIL | {platform}, {N} workflows, {N} jobs |
| 2 | /app-store-publish | PASS/FAIL/SKIPPED | Fastlane configured, {N} lanes |
| 3 | /play-store-publish | PASS/FAIL/SKIPPED | Fastlane configured, {N} lanes |
| 4 | /mobile-analytics | PASS/FAIL | {N}% event coverage, {N} funnels ready |

### Publishing Readiness: {READY / BLOCKED}

### CI/CD Summary
| Workflow | Trigger | iOS | Android |
|----------|---------|-----|---------|
| Test | PR | {configured} | {configured} |
| Beta | Merge to develop | TestFlight | Internal Track |
| Release | Version tag | App Store | Production (staged) |

### Required Secrets (configure in repo settings)
| Secret | Platform | Status | How to Obtain |
|--------|----------|--------|---------------|
| {secret} | {iOS/Android/Both} | {configured/needed} | {instructions} |

### Store Metadata Status
| Element | iOS | Android | Status |
|---------|-----|---------|--------|
| Title | {ready/template} | {ready/template} | {action} |
| Description | {ready/template} | {ready/template} | {action} |
| Screenshots | {ready/needed} | {ready/needed} | {action} |
| Keywords | {ready/template} | N/A | {action} |
| Privacy Policy | {url set/needed} | {url set/needed} | {action} |

### Analytics Coverage
- Event coverage: {N}%
- Funnels ready: {N}/{N}
- Crash reporting: {configured/missing}
- Attribution: {configured/missing}
- Privacy compliance: {pass/fail}

### Publishing Checklist
- [ ] All CI/CD secrets configured in repository settings.
- [ ] Code signing verified (match/keystore).
- [ ] Store metadata reviewed and finalized.
- [ ] Privacy policy URL valid and accessible.
- [ ] Analytics events verified in staging builds.
- [ ] Crash reporting verified (test crash captured).
- [ ] First beta build successfully deployed.
- [ ] First internal test build successfully uploaded.

### Files Created
{list all generated files: workflows, Fastlane configs, metadata}

NEXT STEPS:
- Configure all required secrets listed above in your repository settings.
- Push to develop to trigger the first beta/internal build.
- Verify TestFlight and Play Internal builds install and function correctly.
- Run `/mobile-launch` for the full pre-launch quality pipeline.
- Create a version tag to trigger the first production release.
- Monitor crash-free rate and analytics in the first 24 hours post-launch.
