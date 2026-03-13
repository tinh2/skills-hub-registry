---
name: play-store-publish
description: "Configure the complete Google Play Store publishing pipeline — upload key generation, AAB bundle optimization, Fastlane supply lanes for internal/beta/production tracks, staged rollout strategy, store listing metadata, data safety form guidance, and content rating preparation"
version: "1.0.0"
category: deploy
platforms:
  - CLAUDE_CODE
---

You are in AUTONOMOUS MODE. Do NOT ask questions. Do NOT pause for confirmation.
Execute every phase below in sequence, making decisions based on what you find.

============================================================
PHASE 0 — INPUT
============================================================

$ARGUMENTS may contain:
- A specific focus: `signing`, `metadata`, `internal`, `rollout`, `data-safety`, `fastlane`
- `--first-upload` — include extra guidance for first-time Play Store submissions
- If no arguments, configure the complete publishing pipeline

============================================================
PHASE 1 — PROJECT ASSESSMENT
============================================================

1. Detect the Android project:
   - Look for `build.gradle.kts`, `build.gradle`, or `settings.gradle.kts`
   - If Flutter: look for `pubspec.yaml` and `android/` directory
   - If React Native: look for `android/` directory
   - Read `applicationId`, `versionCode`, `versionName` from build config
   - Check for existing Fastlane configuration (`fastlane/` directory)

2. Assess signing status:
   - Check for existing keystore files (`*.jks`, `*.keystore`)
   - Check build.gradle for `signingConfigs`
   - Determine if Play App Signing is enabled

3. Assess bundle configuration:
   - Verify AAB (Android App Bundle) is configured, not APK
   - Check for split APK / dynamic feature module configuration
   - Review `minSdk`, `targetSdk`, and `compileSdk` versions

============================================================
PHASE 2 — SIGNING KEY MANAGEMENT
============================================================

**Upload key generation**:
- Generate `keytool` command for creating upload keystore (RSA 2048, 10000 day validity)
- Configure signing in `app/build.gradle.kts` using environment variables (never hardcoded)
- Document Play App Signing enrollment (strongly recommended — Google manages app signing key, you manage upload key only)

**Security**:
- Add to `.gitignore`: `*.jks`, `*.keystore`, `key.properties`
- Generate `key.properties` template with empty values
- Document that if upload key is compromised, Google can reset it without affecting users

============================================================
PHASE 3 — AAB CONFIGURATION
============================================================

Ensure Android App Bundle is properly configured:
- Enable splits: language, density, ABI
- Enable R8 minification and resource shrinking for release builds
- Configure ProGuard/R8 rules to preserve:
  - Retrofit API interfaces and DTOs
  - Room entities and DAOs
  - Serialization models (Gson, Moshi, Kotlinx)
  - Firebase classes
  - Any reflection-based code

============================================================
PHASE 4 — FASTLANE CONFIGURATION
============================================================

Generate `fastlane/Fastfile` with these lanes:

| Lane | Action | Trigger |
|------|--------|---------|
| `test` | Run `./gradlew test` | Pre-flight check |
| `build_release` | Build signed AAB | Called by other lanes |
| `internal` | Build + upload to internal testing track | Merge to develop |
| `beta` | Promote internal to closed testing (beta) | Manual trigger |
| `release` | Promote beta to production at 10% rollout | Tag on main |
| `increase_rollout` | Increase production rollout percentage | Manual trigger |

Generate `fastlane/Appfile` with `json_key_file` and `package_name` references.

All signing credentials passed via environment variables, never hardcoded.

============================================================
PHASE 5 — PLAY CONSOLE SERVICE ACCOUNT
============================================================

Document the Google Play Console API setup:
1. Create a Google Cloud project linked to Play Console
2. Enable the Google Play Android Developer API
3. Create a service account with Editor role
4. Download the JSON key file
5. Grant the service account access in Play Console (Settings > API access)
6. Required permissions: Release management, Store presence editing

Generate `fastlane/.env.default` template with placeholder values.
Add to `.gitignore`: `fastlane/play-store-key.json`, `fastlane/.env`

============================================================
PHASE 6 — STORE LISTING METADATA
============================================================

Generate `fastlane/metadata/android/en-US/` directory structure:
- `title.txt` (max 30 chars) — primary keyword + brand
- `short_description.txt` (max 80 chars) — strongest value proposition
- `full_description.txt` (max 4000 chars) — structure: value prop, key features, social proof, CTA. First 5 lines visible before "Read more". Include relevant keywords naturally.
- `changelogs/default.txt` — release notes template

**Image requirements**:
- `phoneScreenshots/` — 2-8 phone screenshots required
- `sevenInchScreenshots/` — 7" tablet screenshots
- `tenInchScreenshots/` — 10" tablet screenshots
- `featureGraphic.png` — 1024x500 required
- `icon.png` — 512x512 hi-res icon

============================================================
PHASE 7 — DATA SAFETY FORM
============================================================

Analyze the app's actual data collection and generate a data safety response template:

| Data Type | Collected | Shared | Purpose | Optional | User Control |
|-----------|-----------|--------|---------|----------|--------------|
| Email | ? | ? | Account management | ? | Can delete |
| Name | ? | ? | App functionality | ? | Can delete |
| Crash logs | ? | ? | Analytics | ? | Cannot opt out |
| Device ID | ? | ? | Analytics | ? | Cannot opt out |

Check for:
- Analytics SDKs (Firebase Analytics, Amplitude, Mixpanel)
- Crash reporting (Crashlytics, Sentry)
- Ad SDKs (AdMob, Unity Ads)
- Auth providers and what user data they collect
- Network calls to identify data sent to servers

============================================================
PHASE 8 — CONTENT RATING
============================================================

Generate content rating questionnaire guidance based on app analysis:
- Violence, sexual content, language, controlled substances
- User interaction (can users communicate?)
- Personal information sharing
- Ad content

Recommend the expected IARC rating based on findings.

============================================================
PHASE 9 — STAGED ROLLOUT STRATEGY
============================================================

| Stage | Rollout | Duration | Gate Criteria | Action if Issues |
|-------|---------|----------|---------------|------------------|
| Internal | Invite only | 3-5 days | Manual testing passes | Fix and re-upload |
| Closed beta | Select users | 1-2 weeks | Crash-free > 99.5% | Fix critical issues |
| Open beta | Public opt-in | 1 week | ANR rate < 0.5% | Fix or halt |
| Production 10% | 10% | 2 days | Crash-free > 99% | Halt if < 98% |
| Production 50% | 50% | 2 days | Same metrics hold | Halt if regression |
| Production 100% | 100% | Ongoing | Ongoing monitoring | Hotfix if needed |

Document how to: pause, resume, halt, and rollback a staged rollout.

============================================================
OUTPUT
============================================================

```
## Play Store Publishing Pipeline Complete

### Signing
- Upload Key: {generated / existing}
- Play App Signing: {enabled / not enrolled}
- Package Name: {detected applicationId}

### Fastlane Lanes
| Lane | Action | Trigger |
|------|--------|---------|
| test | Run unit tests | Pre-flight |
| internal | Build AAB + upload to internal | Merge to develop |
| beta | Promote internal to beta | Manual |
| release | Promote beta to production (10%) | Tag on main |
| increase_rollout | Increase production rollout | Manual |

### Metadata Status
| File | Status | Notes |
|------|--------|-------|
| title.txt | {READY / TEMPLATE} | max 30 chars |
| full_description.txt | {READY / TEMPLATE} | max 4000 chars |
| screenshots | {PRESENT / NEEDED} | 2-8 phone required |
| featureGraphic.png | {PRESENT / NEEDED} | 1024x500 required |

### Data Safety
| Data Type | Collected | Shared | Purpose |
|-----------|-----------|--------|---------|
| {type} | {yes/no} | {yes/no} | {purpose} |

### Files Created
{list all generated files with paths}
```

============================================================
NEXT STEPS
============================================================

1. Run `bundle exec fastlane internal` to push your first internal test build
2. Complete the data safety form in Play Console using the generated template
3. Run `deploy/mobile-ci-cd` to automate builds and track promotion in CI
4. Run `deploy/ota-updates` if you need over-the-air patching between releases

============================================================
DO NOT
============================================================

- Do NOT commit signing keystores or service account keys to the repository
- Do NOT hardcode signing passwords in build files — use environment variables
- Do NOT upload APK instead of AAB — Play Store requires AAB for new apps
- Do NOT skip data safety form — incomplete declarations delay review
- Do NOT use production track for first upload — start with internal testing
- Do NOT forget ProGuard rules for serialization classes — this causes runtime crashes
- Do NOT set rollout to 100% immediately — always use staged rollout for production
