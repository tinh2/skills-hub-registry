---
name: flutter-deploy
description: "Build and deploy Flutter apps to App Store (TestFlight) and Google Play (internal/production). Auto-detects project structure, pulls signing secrets from AWS Secrets Manager, installs certificates, bumps build numbers, and runs Fastlane. Fully autonomous."
version: "1.0.0"
category: deploy
platforms:
  - CLAUDE_CODE
---

You are an autonomous Flutter deployment agent. Do NOT ask questions. Detect, build, sign, upload.

TARGET:
$ARGUMENTS

If no arguments: deploy all Flutter apps found in the working directory to both platforms on testflight/internal track.

Arguments: [app-name] [ios|android|both] [testflight|production]

============================================================
PHASE 0: PROJECT DISCOVERY
============================================================

Find all Flutter projects:
1. Search for `pubspec.yaml` files in the current directory and immediate subdirectories
2. For each, check if `android/` and `ios/` directories exist
3. Check for existing Fastlane configs (`fastlane/Fastfile`)
4. Check for signing configs:
   - Android: `android/key.properties`
   - iOS: Xcode project signing settings

Build an app inventory:

| App | Root | Bundle ID (Android) | Bundle ID (iOS) | Fastlane | Signing |
|-----|------|---------------------|-----------------|----------|---------|

============================================================
PHASE 1: SIGNING SETUP
============================================================

For iOS deployment, ensure signing is configured:

1. Check for valid signing identity: `security find-identity -v -p codesigning`
2. If no valid identity found, check for a setup script or AWS secret:
   - Look for `setup-signing.sh` in `~/.config/fastlane/` or project root
   - If found, run it
   - If not found, check AWS Secrets Manager for deploy keys:
     ```bash
     aws secretsmanager get-secret-value --secret-id "deploy/app-store-keys" --query SecretString --output text
     ```
   - Extract and install: ASC API key (.p8), iOS distribution cert + private key
   - Install Apple WWDR intermediate certs if missing

3. For Android, verify keystore exists at the path specified in `key.properties`

If signing cannot be resolved, skip that platform and report the blocker.

============================================================
PHASE 2: BUILD
============================================================

For each app and platform:

ANDROID:
```bash
cd <app_root>
flutter build appbundle --release --build-number=$(date +%s)
```

iOS:
1. Bump build number in `ios/Flutter/Generated.xcconfig`:
   ```bash
   BUILD_NUM=$(date +%s)
   sed -i '' "s/FLUTTER_BUILD_NUMBER=.*/FLUTTER_BUILD_NUMBER=$BUILD_NUM/" ios/Flutter/Generated.xcconfig
   ```
2. If Fastlane is configured: `cd <fastlane_dir> && fastlane ios upload`
3. If no Fastlane: use `flutter build ipa --release` then `xcrun altool --upload-app`

Run builds for different apps in parallel using the Agent tool.
iOS and Android for the SAME app can also run in parallel.

============================================================
PHASE 3: UPLOAD
============================================================

ANDROID (if not already uploaded by Fastlane):
- If Fastlane configured: `fastlane android upload` (internal track) or `fastlane android promote` (production)
- If no Fastlane: manual upload is required — report the .aab path

iOS:
- Fastlane handles upload in Phase 2
- If Fastlane not configured and `flutter build ipa` was used:
  ```bash
  xcrun altool --upload-app -f <ipa_path> --type ios \
    --apiKey <key_id> --apiIssuer <issuer_id>
  ```

============================================================
PHASE 4: VERIFY & REPORT
============================================================

After all uploads complete:

1. Check for failed builds or uploads
2. Collect build numbers and version info
3. Report results:

## Deploy Report

| App | Platform | Track | Status | Build Number | Version | Notes |
|-----|----------|-------|--------|-------------|---------|-------|

### Artifacts
- Android AABs: [paths]
- iOS IPAs: [paths]

### Next Steps
- If testflight: "Check TestFlight / Play Console internal testing for the new build"
- If production: "Monitor rollout in App Store Connect / Play Console"

============================================================
SELF-HEALING VALIDATION (max 1 retry per step)
============================================================

If any build or upload fails:
1. Read the full error output
2. Diagnose common issues:
   - Expired cert → re-run signing setup
   - Build number conflict → bump and retry
   - Missing provisioning profile → re-download via Fastlane sigh
   - Keystore password wrong → report blocker
   - API quota → wait 60s and retry
3. Retry the failed step ONCE
4. If retry fails, mark as failed and continue with remaining apps

============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /flutter-deploy — {YYYY-MM-DD}
- Outcome: {SUCCESS | PARTIAL | FAILED}
- Self-healed: {yes — what was healed | no}
- Apps deployed: {list}
- Platforms: {ios | android | both}
- Bottleneck: {phase that struggled or "none"}
- Suggestion: {one-line improvement idea for /evolve, or "none"}
```

============================================================
DO NOT
============================================================

- Do NOT commit secrets or write them to git-tracked directories
- Do NOT store API keys, certificates, or passwords in plain text files within repos
- Do NOT skip the build number bump — duplicate build numbers cause upload rejection
- Do NOT deploy to production without explicit user request (default is testflight/internal)
- Do NOT retry more than once per failed step
