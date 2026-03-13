---
name: ota-updates
description: "Configure over-the-air mobile updates — Shorebird for Flutter, CodePush or EAS Update for React Native — with update channels, staged rollout, forced vs optional update policies, rollback procedures, crash-rate monitoring, and CI integration"
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
- A specific OTA platform: `shorebird`, `codepush`, `eas-update`
- A specific focus: `rollback`, `channels`, `ci-integration`, `update-policy`
- If no arguments, configure the complete OTA infrastructure for the detected framework

============================================================
PHASE 1 — FRAMEWORK DETECTION
============================================================

1. Detect the mobile framework:
   - `pubspec.yaml` with flutter SDK -> Flutter (use Shorebird)
   - `package.json` with `react-native` -> React Native (use CodePush or EAS Update)
   - `package.json` with `expo` -> Expo (use EAS Update)
   - `*.xcodeproj` (native iOS) -> Custom OTA or no-code-push strategy
   - `build.gradle.kts` (native Android) -> Play In-App Updates API

2. Determine OTA eligibility:
   - OTA CAN update: JavaScript bundles (RN), Dart code (Flutter/Shorebird), assets, configuration
   - OTA CANNOT update: native code, new permissions, native module changes, new SDK integrations
   - Document what changes require a full store release vs OTA

============================================================
PHASE 2 — FLUTTER / SHOREBIRD SETUP
============================================================

If Flutter is detected, configure Shorebird:

**Initialization**:
- Install Shorebird CLI
- Run `shorebird init` in project
- Generate `shorebird.yaml` with app ID and flavor-based channel definitions

**Channel configuration**:
- `development`: dev app ID
- `staging`: staging app ID
- `production`: production app ID

**Release workflow**:
- `shorebird release android/ios --flavor production` — creates a new store release baseline
- `shorebird patch android/ios --flavor production` — pushes OTA patch to existing release

**CI integration** (`.github/workflows/ota-patch.yml`):
- `workflow_dispatch` with platform and flavor inputs
- Uses `shorebirdtech/setup-shorebird@v1` with `SHOREBIRD_TOKEN` secret
- Runs on `macos-14` for iOS, `ubuntu-latest` for Android

============================================================
PHASE 3 — REACT NATIVE / CODEPUSH / EAS UPDATE
============================================================

If React Native is detected, configure the appropriate OTA solution:

**Expo (EAS Update)**:
- Configure `eas.json` with update channels per environment (development, staging, production)
- Push updates: `eas update --channel staging --message "description"`
- Channel promotion flow: staging -> production

**Bare React Native (CodePush)**:
- Install `react-native-code-push` SDK
- Configure update check behavior:
  - `checkFrequency: ON_APP_RESUME`
  - `installMode: ON_NEXT_RESUME` (non-mandatory)
  - `mandatoryInstallMode: IMMEDIATE` (mandatory/critical)
  - `minimumBackgroundDuration: 60` seconds

============================================================
PHASE 4 — NATIVE APPS
============================================================

For native iOS/Android apps without OTA framework support:

**Android — Play In-App Updates**:
- Flexible update (downloads in background, non-blocking)
- Immediate update (blocks app usage until installed)
- Check `updateAvailability()` and `isUpdateTypeAllowed()` before prompting

**iOS — App Store Version Check**:
- Query iTunes lookup API for latest version
- Compare with current bundle version
- Prompt user to update if newer version exists

**Custom OTA for config/assets**:
- Firebase Remote Config for feature flags and configuration
- Asset bundles downloaded on demand
- No code changes via OTA (would violate store guidelines)

============================================================
PHASE 5 — UPDATE CHANNELS & ENVIRONMENTS
============================================================

Configure update channels matching deployment environments:

| Channel | Target | Update Mode | Rollout |
|---------|--------|-------------|---------|
| development | Dev builds | Immediate | 100% |
| staging | QA/staging | Immediate | 100% |
| production-canary | 5% of production | On next resume | 5% |
| production | All production | On next resume | 100% |

Channel promotion flow:
1. Push patch to staging channel
2. QA verifies on staging builds
3. Promote to production-canary (5% rollout)
4. Monitor crash-free rate for 24 hours
5. If stable (crash-free > 99%), promote to production (100%)

============================================================
PHASE 6 — UPDATE POLICIES
============================================================

Implement update policy logic with three severity tiers:

**Critical (forced)** — blocks app until installed:
- Security vulnerability fix
- Data corruption fix
- Authentication bypass fix
- API breaking change requiring client update

**Important (strongly recommended)** — persistent banner, dismissible once per session:
- Major bug fix
- Performance improvement
- New required feature

**Optional (informational)** — dismissible dialog, not shown again for this version:
- Minor improvement
- New optional feature
- UI polish

Generate a version compatibility config:
```json
{
  "minSupportedVersion": "2.1.0",
  "latestVersion": "2.3.0",
  "forceUpdateBelow": "2.0.0"
}
```

============================================================
PHASE 7 — ROLLBACK STRATEGY
============================================================

Document rollback procedures for each platform:

**Shorebird**: `shorebird patch rollback android/ios --release-version 1.0.0`

**EAS Update**: `eas update:republish --group <previous-update-group-id> --channel production`

**CodePush**: `appcenter codepush rollback -a owner/AppName-Platform Production`

**Automated rollback trigger**:
- Monitor crash-free rate after OTA push
- If crash-free rate drops below 98%, automatically rollback
- Send alert to team channel (Slack, PagerDuty)

============================================================
PHASE 8 — A/B UPDATE TESTING
============================================================

Configure A/B testing for OTA updates:
1. Create two update variants targeting different user segments
2. Use rollout percentage to split traffic
3. Monitor metrics per variant: crash-free rate, session duration, feature adoption, retention
4. Promote the winning variant to 100%

============================================================
OUTPUT
============================================================

```
## OTA Update Infrastructure Complete

### Framework: {Flutter / React Native / Expo / Native}
### OTA Platform: {Shorebird / EAS Update / CodePush / Custom}

### Update Channels
| Channel | Target | Mode | Rollout |
|---------|--------|------|---------|
| {channel} | {audience} | {immediate/resume} | {%} |

### Update Policy
| Severity | Behavior | User Experience |
|----------|----------|-----------------|
| Critical | Force update | Blocks app until updated |
| Important | Recommend | Persistent banner |
| Optional | Inform | Dismissible dialog |

### Rollback Procedure
{step-by-step rollback for the configured platform}

### CI Integration
{workflow files created for automated OTA patches}

### Files Created
{list all generated files with paths}
```

============================================================
NEXT STEPS
============================================================

1. Push your first OTA patch to the staging channel to verify the setup
2. Run `deploy/mobile-ci-cd` to integrate OTA patches into the CI/CD pipeline
3. Set up crash monitoring (Sentry, Crashlytics) to enable automated rollback triggers
4. Test the rollback procedure before relying on it in production

============================================================
DO NOT
============================================================

- Do NOT push OTA updates that include native code changes — these require store review
- Do NOT skip staging channel testing before production push
- Do NOT set all updates to force-update — this creates a poor user experience
- Do NOT deploy without a tested rollback procedure
- Do NOT push to production without monitoring crash-free rate
- Do NOT bypass store guidelines by delivering app functionality via remote config that would normally require review
- Do NOT store OTA tokens or API keys in source code
