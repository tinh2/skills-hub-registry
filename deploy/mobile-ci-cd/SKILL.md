---
name: mobile-ci-cd
description: Sets up mobile CI/CD pipeline — GitHub Actions, Bitrise, or Codemagic for iOS and Android, code signing in CI, build number management, automated testing, beta distribution, and release automation.
version: "1.0.0"
category: deploy
platforms:
  - CLAUDE_CODE
---

You are an autonomous mobile CI/CD configuration agent. You set up a complete
continuous integration and delivery pipeline for iOS and Android mobile apps.
Do NOT ask the user questions. Detect the project type and configure accordingly.

INPUT: $ARGUMENTS (optional)
If provided, focus on specific CI/CD platform or aspect (e.g., "GitHub Actions", "Bitrise",
"code signing only", "TestFlight only").
If not provided, configure a complete pipeline using GitHub Actions.

============================================================
PHASE 1: PROJECT DETECTION
============================================================

1. Detect the mobile framework:
   - pubspec.yaml with flutter SDK -> Flutter (iOS + Android)
   - *.xcodeproj or *.xcworkspace (no Flutter) -> Native iOS
   - build.gradle.kts with android plugin (no Flutter) -> Native Android
   - package.json with react-native -> React Native (iOS + Android)
   - package.json with expo -> Expo (iOS + Android)

2. Detect existing CI/CD:
   - .github/workflows/ -> GitHub Actions
   - bitrise.yml -> Bitrise
   - codemagic.yaml -> Codemagic
   - .circleci/ -> CircleCI
   - Jenkinsfile -> Jenkins

3. Detect existing Fastlane:
   - fastlane/Fastfile -> Use existing lanes.
   - If absent, generate Fastlane configuration as part of this skill.

4. Detect signing configuration:
   - iOS: Fastlane match, manual profiles, Xcode automatic signing.
   - Android: keystore in build.gradle, key.properties, or environment-based.

============================================================
PHASE 2: GITHUB ACTIONS — IOS PIPELINE
============================================================

Generate .github/workflows/ios.yml:

```yaml
name: iOS Build & Deploy

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

concurrency:
  group: ios-${{ github.ref }}
  cancel-in-progress: true

jobs:
  test:
    name: Test
    runs-on: macos-14
    steps:
      - uses: actions/checkout@v4

      # Framework-specific setup
      # Flutter:
      - uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.x'
          channel: stable
          cache: true
      - run: flutter pub get
      - run: flutter analyze
      - run: flutter test --coverage

      # Native iOS:
      # - uses: maxim-lobanov/setup-xcode@v1
      #   with:
      #     xcode-version: latest-stable
      # - run: xcodebuild test -scheme AppName -destination 'platform=iOS Simulator,name=iPhone 15 Pro'

  build-testflight:
    name: Build & TestFlight
    needs: test
    if: github.ref == 'refs/heads/develop' && github.event_name == 'push'
    runs-on: macos-14
    steps:
      - uses: actions/checkout@v4

      - name: Install Fastlane
        run: |
          gem install bundler
          bundle install --jobs 4 --retry 3

      - name: Setup code signing
        env:
          MATCH_PASSWORD: ${{ secrets.MATCH_PASSWORD }}
          MATCH_GIT_BASIC_AUTHORIZATION: ${{ secrets.MATCH_GIT_TOKEN }}
          APP_STORE_CONNECT_API_KEY_ID: ${{ secrets.ASC_KEY_ID }}
          APP_STORE_CONNECT_API_ISSUER_ID: ${{ secrets.ASC_ISSUER_ID }}
          APP_STORE_CONNECT_API_KEY_CONTENT: ${{ secrets.ASC_KEY_CONTENT }}
        run: bundle exec fastlane match appstore --readonly

      - name: Build and upload to TestFlight
        env:
          APP_STORE_CONNECT_API_KEY_ID: ${{ secrets.ASC_KEY_ID }}
          APP_STORE_CONNECT_API_ISSUER_ID: ${{ secrets.ASC_ISSUER_ID }}
          APP_STORE_CONNECT_API_KEY_CONTENT: ${{ secrets.ASC_KEY_CONTENT }}
        run: bundle exec fastlane beta

      - name: Upload build artifacts
        uses: actions/upload-artifact@v4
        with:
          name: ios-ipa
          path: "*.ipa"
          retention-days: 14

  build-release:
    name: Build & App Store
    needs: test
    if: startsWith(github.ref, 'refs/tags/v')
    runs-on: macos-14
    steps:
      - uses: actions/checkout@v4
      - name: Install Fastlane
        run: bundle install --jobs 4 --retry 3
      - name: Build and upload to App Store
        env:
          MATCH_PASSWORD: ${{ secrets.MATCH_PASSWORD }}
          MATCH_GIT_BASIC_AUTHORIZATION: ${{ secrets.MATCH_GIT_TOKEN }}
          APP_STORE_CONNECT_API_KEY_ID: ${{ secrets.ASC_KEY_ID }}
          APP_STORE_CONNECT_API_ISSUER_ID: ${{ secrets.ASC_ISSUER_ID }}
          APP_STORE_CONNECT_API_KEY_CONTENT: ${{ secrets.ASC_KEY_CONTENT }}
        run: bundle exec fastlane release
```

============================================================
PHASE 3: GITHUB ACTIONS — ANDROID PIPELINE
============================================================

Generate .github/workflows/android.yml:

```yaml
name: Android Build & Deploy

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

concurrency:
  group: android-${{ github.ref }}
  cancel-in-progress: true

jobs:
  test:
    name: Test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      # Flutter:
      - uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.x'
          channel: stable
          cache: true
      - run: flutter pub get
      - run: flutter analyze
      - run: flutter test --coverage

      # Native Android:
      # - uses: actions/setup-java@v4
      #   with:
      #     distribution: temurin
      #     java-version: 17
      #     cache: gradle
      # - run: ./gradlew test

  build-internal:
    name: Build & Internal Track
    needs: test
    if: github.ref == 'refs/heads/develop' && github.event_name == 'push'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Java
        uses: actions/setup-java@v4
        with:
          distribution: temurin
          java-version: 17
          cache: gradle

      - name: Decode keystore
        run: echo "${{ secrets.KEYSTORE_BASE64 }}" | base64 --decode > upload-keystore.jks

      - name: Build AAB
        env:
          KEYSTORE_PATH: upload-keystore.jks
          KEYSTORE_PASSWORD: ${{ secrets.KEYSTORE_PASSWORD }}
          KEY_ALIAS: ${{ secrets.KEY_ALIAS }}
          KEY_PASSWORD: ${{ secrets.KEY_PASSWORD }}
        run: bundle exec fastlane internal

      - name: Upload build artifacts
        uses: actions/upload-artifact@v4
        with:
          name: android-aab
          path: "**/*.aab"
          retention-days: 14

  build-release:
    name: Build & Production
    needs: test
    if: startsWith(github.ref, 'refs/tags/v')
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Java
        uses: actions/setup-java@v4
        with:
          distribution: temurin
          java-version: 17
          cache: gradle
      - name: Decode keystore
        run: echo "${{ secrets.KEYSTORE_BASE64 }}" | base64 --decode > upload-keystore.jks
      - name: Build and publish to production
        env:
          KEYSTORE_PATH: upload-keystore.jks
          KEYSTORE_PASSWORD: ${{ secrets.KEYSTORE_PASSWORD }}
          KEY_ALIAS: ${{ secrets.KEY_ALIAS }}
          KEY_PASSWORD: ${{ secrets.KEY_PASSWORD }}
          PLAY_STORE_JSON_KEY: ${{ secrets.PLAY_STORE_JSON_KEY }}
        run: bundle exec fastlane release
```

============================================================
PHASE 4: BUILD NUMBER MANAGEMENT
============================================================

Generate a build number strategy:

OPTION A — Git-based (recommended for CI):
```bash
# Use total git commit count as build number
BUILD_NUMBER=$(git rev-list --count HEAD)
```

OPTION B — CI run number:
```yaml
# GitHub Actions
env:
  BUILD_NUMBER: ${{ github.run_number }}
```

OPTION C — Timestamp-based:
```bash
BUILD_NUMBER=$(date +%Y%m%d%H%M)
```

Configure build number injection:
- Flutter: `flutter build --build-number=$BUILD_NUMBER`
- iOS Native: Fastlane `increment_build_number(build_number: ENV["BUILD_NUMBER"])`
- Android Native: Set versionCode in gradle from environment variable.

Ensure build numbers are monotonically increasing (required by both stores).

============================================================
PHASE 5: CODE SIGNING IN CI
============================================================

IOS SIGNING:
- Fastlane match with git-based certificate storage (encrypted).
- Secrets needed: MATCH_PASSWORD, MATCH_GIT_TOKEN.
- App Store Connect API key stored as secret: ASC_KEY_ID, ASC_ISSUER_ID, ASC_KEY_CONTENT.
- Temporary keychain created and destroyed in CI (match handles this).

ANDROID SIGNING:
- Keystore stored as base64-encoded secret: KEYSTORE_BASE64.
- Key credentials as secrets: KEYSTORE_PASSWORD, KEY_ALIAS, KEY_PASSWORD.
- Play Store service account JSON as secret: PLAY_STORE_JSON_KEY.
- Decode keystore from secret before build, delete after.

Generate a secrets documentation template listing all required secrets and how to obtain them.

============================================================
PHASE 6: AUTOMATED TESTING IN CI
============================================================

Configure test jobs:

UNIT TESTS:
- Flutter: `flutter test --coverage`
- iOS: `xcodebuild test` or `fastlane test`
- Android: `./gradlew test` or `fastlane test`

STATIC ANALYSIS:
- Flutter: `flutter analyze`
- iOS: SwiftLint via build phase or separate step.
- Android: `./gradlew lint`

COVERAGE REPORTING:
- Upload coverage to Codecov or Coveralls.
- Set minimum coverage thresholds (fail build if coverage drops).

OPTIONAL — UI TESTS IN CI:
- iOS: Simulator-based tests on macOS runner.
- Android: Firebase Test Lab integration via Fastlane.
- Flutter: `flutter test integration_test/` on simulator/emulator.

============================================================
PHASE 7: ARTIFACT MANAGEMENT
============================================================

Configure artifact retention:
- IPA / AAB files: 14-day retention for PR builds, 90-day for releases.
- Test results: Always uploaded as artifacts.
- Coverage reports: Uploaded to coverage service.
- dSYM files: Archived for crash symbolication.
- Mapping files: Archived for ProGuard deobfuscation.

============================================================
OUTPUT
============================================================

## Mobile CI/CD Pipeline Complete

### Platform: {GitHub Actions / Bitrise / Codemagic}
### Framework: {Flutter / iOS Native / Android Native / React Native}

### Pipeline Overview
| Trigger | iOS Action | Android Action |
|---------|------------|----------------|
| PR to develop | Test + analyze | Test + lint |
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
| KEYSTORE_BASE64 | Android | base64 encode of .jks |
| KEYSTORE_PASSWORD | Android | Chosen during keytool |
| KEY_ALIAS | Android | Chosen during keytool |
| KEY_PASSWORD | Android | Chosen during keytool |
| PLAY_STORE_JSON_KEY | Android | GCP service account |

### Files Created
{list all generated workflow and configuration files}

DO NOT:
- Store signing keys, keystores, or API keys in the repository.
- Use self-hosted runners for code signing — secrets on shared runners are isolated per job.
- Skip test jobs — builds without tests provide false confidence.
- Build APK instead of AAB for Play Store uploads.
- Use password-based App Store Connect auth — API keys are more reliable in CI.
- Hardcode build numbers — they must be dynamic and monotonically increasing.
- Skip artifact upload — build outputs are needed for debugging and compliance.

NEXT STEPS:
- "Configure the required secrets in your repository settings."
- "Run `/app-store-publish` to set up Fastlane lanes if not already done."
- "Run `/play-store-publish` to configure Play Store Fastlane lanes."
- "Run `/mobile-test` to ensure test coverage before enabling CI test gates."
