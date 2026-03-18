---
name: mobile-ci-cd
description: "Set up mobile CI/CD pipelines for Flutter, React Native, or native iOS/Android — GitHub Actions workflows for testing, code signing, TestFlight/Play Store distribution, build number management, Fastlane integration, and artifact retention"
version: "2.0.0"
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
- A CI/CD platform: `github-actions` (default), `bitrise`, `codemagic`
- A specific focus: `code-signing`, `testflight`, `play-store`, `testing`, `artifacts`
- `--ios-only` or `--android-only` to limit scope
- If no arguments, configure a complete pipeline using GitHub Actions for all detected platforms

============================================================
PHASE 1 — PROJECT DETECTION
============================================================

1. Detect the mobile framework:
   - `pubspec.yaml` with flutter SDK -> Flutter (iOS + Android)
   - `*.xcodeproj` or `*.xcworkspace` (no Flutter) -> Native iOS
   - `build.gradle.kts` with android plugin (no Flutter) -> Native Android
   - `package.json` with `react-native` -> React Native (iOS + Android)
   - `package.json` with `expo` -> Expo (iOS + Android)

2. Detect existing CI/CD:
   - `.github/workflows/` -> GitHub Actions
   - `bitrise.yml` -> Bitrise
   - `codemagic.yaml` -> Codemagic
   - `.circleci/` -> CircleCI

3. Detect existing Fastlane:
   - `fastlane/Fastfile` -> Use existing lanes
   - If absent, generate Fastlane configuration as part of this skill

4. Detect signing configuration:
   - iOS: Fastlane match, manual profiles, Xcode automatic signing
   - Android: keystore in build.gradle, key.properties, or environment-based

============================================================
PHASE 2 — iOS PIPELINE
============================================================

Generate `.github/workflows/ios.yml`:

**Triggers**: Push to `main`/`develop`, PRs to `main`/`develop`. Use concurrency groups with `cancel-in-progress: true`.

**Test job** (runs on `macos-14`):
- Framework-specific setup (Flutter action with cache, or Xcode setup)
- Static analysis (flutter analyze, SwiftLint)
- Unit tests with coverage
- Upload coverage to Codecov/Coveralls

**TestFlight job** (runs on push to `develop`):
- Install Fastlane via Bundler
- Code signing via Fastlane match (appstore profile, readonly)
- Required secrets: `MATCH_PASSWORD`, `MATCH_GIT_TOKEN`, `ASC_KEY_ID`, `ASC_ISSUER_ID`, `ASC_KEY_CONTENT`
- Build and upload via `fastlane beta`
- Upload IPA as artifact (14-day retention)
- Upload dSYMs for crash symbolication

**App Store job** (runs on tag `v*.*.*`):
- Same signing setup as TestFlight
- Build and upload via `fastlane release`

============================================================
PHASE 3 — ANDROID PIPELINE
============================================================

Generate `.github/workflows/android.yml`:

**Triggers**: Same as iOS. Concurrency groups.

**Test job** (runs on `ubuntu-latest`):
- Java 17 setup with Gradle cache
- Framework-specific setup (Flutter, React Native, or native)
- Static analysis (flutter analyze, `./gradlew lint`)
- Unit tests with coverage

**Internal Track job** (runs on push to `develop`):
- Decode keystore from base64 secret
- Required secrets: `KEYSTORE_BASE64`, `KEYSTORE_PASSWORD`, `KEY_ALIAS`, `KEY_PASSWORD`, `PLAY_STORE_JSON_KEY`
- Build AAB (never APK for Play Store)
- Upload to internal testing track via Fastlane supply
- Upload AAB as artifact (14-day retention)
- Upload mapping files for ProGuard deobfuscation

**Production job** (runs on tag `v*.*.*`):
- Same signing setup
- Upload to production with staged rollout (start at 10%)

============================================================
PHASE 4 — BUILD NUMBER MANAGEMENT
============================================================

Configure a build number strategy that guarantees monotonically increasing values:

**Recommended**: CI run number (`${{ github.run_number }}`) — simple and monotonic.

**Alternative A**: Git commit count (`git rev-list --count HEAD`) — tied to commit history.

**Alternative B**: Timestamp (`date +%Y%m%d%H%M`) — works for infrequent builds.

Inject build number per framework:
- Flutter: `flutter build --build-number=$BUILD_NUMBER`
- iOS Native: Fastlane `increment_build_number(build_number: ENV["BUILD_NUMBER"])`
- Android Native: Set `versionCode` from environment variable in gradle

============================================================
PHASE 5 — CODE SIGNING IN CI
============================================================

**iOS Signing**:
- Fastlane match with git-based encrypted certificate storage
- App Store Connect API key (preferred over password auth in CI)
- Temporary keychain created and destroyed per job (match handles this)

**Android Signing**:
- Keystore stored as base64-encoded GitHub secret
- Decoded to file before build, deleted after
- Play Store service account JSON key as secret

Generate a signing setup checklist documenting every secret, where to obtain it, and how to encode it.

============================================================
PHASE 6 — AUTOMATED TESTING
============================================================

Configure comprehensive test jobs:

**Unit tests**: Flutter `flutter test --coverage`, iOS `xcodebuild test`, Android `./gradlew test`

**Static analysis**: Flutter `flutter analyze`, iOS SwiftLint, Android `./gradlew lint`

**Coverage**: Upload to Codecov or Coveralls. Set minimum coverage thresholds.

**Optional UI tests**:
- iOS: Simulator-based tests on macOS runner
- Android: Firebase Test Lab integration via Fastlane
- Flutter: `flutter test integration_test/` on simulator/emulator

============================================================
PHASE 7 — ARTIFACT MANAGEMENT
============================================================

Configure artifact retention:
- IPA / AAB files: 14-day retention for PR builds, 90-day for releases
- Test results: always uploaded as artifacts
- Coverage reports: uploaded to coverage service
- dSYM files: archived for crash symbolication
- Mapping files: archived for ProGuard deobfuscation


============================================================
SELF-HEALING VALIDATION (max 2 iterations)
============================================================

After completing deployment/infrastructure changes, validate:

1. Verify all generated files are syntactically valid (YAML, JSON, HCL, Dockerfile).
2. Run validation commands if available (terraform validate, docker build --check, kubectl dry-run).
3. Verify no secrets, credentials, or sensitive values are hardcoded.
4. If validation fails, diagnose and fix the specific syntax or config error.
5. Repeat up to 2 iterations.

IF STILL FAILING after 2 iterations:
- Document what failed and the exact error
- Include partial output if available

============================================================
OUTPUT
============================================================

```
## Mobile CI/CD Pipeline Complete

### Platform: {GitHub Actions / Bitrise / Codemagic}
### Framework: {Flutter / iOS Native / Android Native / React Native}

### Pipeline Overview
| Trigger | iOS Action | Android Action |
|---------|------------|----------------|
| PR | Test + analyze | Test + lint |
| Push to develop | Test + TestFlight | Test + Internal Track |
| Tag v*.*.* | Test + App Store | Test + Production (10%) |

### Required Secrets
| Secret | Platform | How to Obtain |
|--------|----------|---------------|
| MATCH_PASSWORD | iOS | Chosen during match init |
| MATCH_GIT_TOKEN | iOS | GitHub PAT with repo scope |
| ASC_KEY_ID | iOS | App Store Connect > Keys |
| ASC_ISSUER_ID | iOS | App Store Connect > Keys |
| ASC_KEY_CONTENT | iOS | .p8 file contents |
| KEYSTORE_BASE64 | Android | base64 -w0 upload-keystore.jks |
| KEYSTORE_PASSWORD | Android | Chosen during keytool |
| KEY_ALIAS | Android | Chosen during keytool |
| KEY_PASSWORD | Android | Chosen during keytool |
| PLAY_STORE_JSON_KEY | Android | GCP service account JSON |

### Files Created
{list all generated workflow and configuration files}
```

============================================================
NEXT STEPS
============================================================

1. Configure the required secrets in your GitHub repository settings
2. Run `deploy/play-store-publish` to set up Fastlane lanes for Play Store
3. Run `deploy/app-store-publish` to set up Fastlane lanes for App Store
4. Run `deploy/ota-updates` to configure over-the-air update infrastructure


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /mobile-ci-cd — {{YYYY-MM-DD}}
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

- Do NOT store signing keys, keystores, or API keys in the repository
- Do NOT use self-hosted runners for code signing without proper secret isolation
- Do NOT skip test jobs — builds without tests provide false confidence
- Do NOT build APK instead of AAB for Play Store uploads
- Do NOT use password-based App Store Connect auth — API keys are more reliable in CI
- Do NOT hardcode build numbers — they must be dynamic and monotonically increasing
- Do NOT skip artifact upload — build outputs are needed for debugging and compliance
- Do NOT use deprecated action versions — pin to latest major versions
