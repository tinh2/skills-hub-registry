---
name: app-store-publish
description: "Configure a complete iOS App Store publishing pipeline — sets up Fastlane with code signing (match), App Store Connect API key, TestFlight and release lanes, screenshot automation, metadata templates, review compliance checklist, and phased rollout. Use for any iOS or Flutter app ready to submit to the App Store."
version: "2.0.0"
category: deploy
platforms:
  - CLAUDE_CODE
---

You are an autonomous iOS App Store publishing agent. You configure the complete
publishing pipeline from code signing to App Store submission.
Do NOT ask the user questions. Investigate the project and configure everything needed.

INPUT: $ARGUMENTS (optional)
If provided, focus on specific aspects (e.g., "TestFlight only", "screenshots", "metadata").
If not provided, configure the complete publishing pipeline.

============================================================
PHASE 1: PROJECT ASSESSMENT
============================================================

1. Detect the iOS project:
   - Look for *.xcodeproj, *.xcworkspace, or pubspec.yaml (Flutter).
   - Read the project's bundle identifier, version, and build number.
   - Identify the deployment target and supported devices.
   - Check for existing Fastlane configuration (fastlane/ directory).

2. Assess signing status:
   - Check for existing provisioning profiles in ~/Library/MobileDevice/Provisioning Profiles/.
   - Check for certificates in Keychain Access.
   - Identify the Apple Developer Team ID from project settings.
   - Determine if manual or automatic signing is configured.

3. Check App Store Connect readiness:
   - Verify Fastlane credentials availability (app-specific password or API key).
   - Check for existing app record in App Store Connect (via Fastlane).

============================================================
PHASE 2: CODE SIGNING SETUP
============================================================

FASTLANE MATCH (recommended for teams):

Generate fastlane/Matchfile:
```ruby
git_url("https://github.com/org/certificates")
storage_mode("git")
type("appstore")
app_identifier(["com.example.app", "com.example.app.clip"])
username("developer@example.com")
team_id("TEAM_ID")
```

Configure match for three types:
- development: local development and device testing.
- adhoc: internal distribution outside TestFlight.
- appstore: App Store and TestFlight distribution.

MANUAL SIGNING (alternative):

If match is not desired, configure manual signing:
- Document certificate creation steps.
- Generate provisioning profiles via Fastlane sigh.
- Store encrypted profiles in the repository.

============================================================
PHASE 3: FASTLANE CONFIGURATION
============================================================

Generate fastlane/Fastfile:

```ruby
default_platform(:ios)

platform :ios do
  desc "Run tests"
  lane :test do
    run_tests(
      scheme: "AppName",
      devices: ["iPhone 15 Pro"],
      code_coverage: true
    )
  end

  desc "Build and push to TestFlight"
  lane :beta do
    ensure_git_status_clean
    increment_build_number(xcodeproj: "AppName.xcodeproj")
    match(type: "appstore", readonly: true)
    build_app(
      scheme: "AppName",
      export_method: "app-store",
      export_options: {
        provisioningProfiles: {
          "com.example.app" => "match AppStore com.example.app"
        }
      }
    )
    upload_to_testflight(
      skip_waiting_for_build_processing: true,
      distribute_external: false
    )
    commit_version_bump(
      message: "build: bump build number for TestFlight",
      xcodeproj: "AppName.xcodeproj"
    )
  end

  desc "Build and submit to App Store"
  lane :release do
    ensure_git_status_clean
    increment_build_number(xcodeproj: "AppName.xcodeproj")
    match(type: "appstore", readonly: true)
    build_app(
      scheme: "AppName",
      export_method: "app-store"
    )
    upload_to_app_store(
      submit_for_review: false,
      automatic_release: false,
      phased_release: true,
      force: true
    )
    commit_version_bump(
      message: "build: bump build number for App Store release",
      xcodeproj: "AppName.xcodeproj"
    )
  end
end
```

Generate fastlane/Appfile:
```ruby
app_identifier("com.example.app")
apple_id("developer@example.com")
team_id("TEAM_ID")
itc_team_id("ITC_TEAM_ID")
```

Generate fastlane/Gemfile:
```ruby
source "https://rubygems.org"
gem "fastlane", "~> 2.220"
gem "cocoapods", "~> 1.15" # if using CocoaPods
```

============================================================
PHASE 4: APP STORE CONNECT API KEY
============================================================

Configure API key authentication (preferred over password):

Generate fastlane/Appfile addition:
```ruby
# App Store Connect API Key (preferred)
# Generate at: https://appstoreconnect.apple.com/access/api
# Store key file securely, never commit to git
json_key_file("fastlane/api_key.json")
```

Generate fastlane/.env.default template:
```
APP_STORE_CONNECT_API_KEY_ID=XXXXXXXXXX
APP_STORE_CONNECT_API_ISSUER_ID=XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
APP_STORE_CONNECT_API_KEY_PATH=./fastlane/AuthKey_XXXXXXXXXX.p8
```

Add to .gitignore:
```
fastlane/AuthKey_*.p8
fastlane/api_key.json
fastlane/.env
```

============================================================
PHASE 5: SCREENSHOT AUTOMATION
============================================================

Generate fastlane/Snapfile:
```ruby
devices([
  "iPhone 16 Pro Max",     # 6.7"
  "iPhone 16 Pro",         # 6.3"
  "iPhone SE (3rd generation)", # 4.7" (if supporting)
  "iPad Pro 13-inch (M4)", # iPad (if supporting)
])
languages(["en-US"])
scheme("AppNameUITests")
output_directory("./fastlane/screenshots")
clear_previous_screenshots(true)
override_status_bar(true)
```

Generate screenshot UI test template:
```swift
// AppNameUITests/ScreenshotTests.swift
import XCTest

class ScreenshotTests: XCTestCase {
    let app = XCUIApplication()

    override func setUp() {
        super.setUp()
        continueAfterFailure = false
        app.launchArguments.append("--uitesting")
        setupSnapshot(app)
        app.launch()
    }

    func testHomeScreen() {
        snapshot("01_HomeScreen")
    }

    func testDetailScreen() {
        // Navigate to detail
        snapshot("02_DetailScreen")
    }

    // ... one test per screenshot needed
}
```

============================================================
PHASE 6: METADATA PREPARATION
============================================================

Generate fastlane/metadata/en-US/ directory structure:

```
fastlane/metadata/en-US/
  name.txt                    # App name (max 30 chars)
  subtitle.txt                # Subtitle (max 30 chars)
  description.txt             # Full description (max 4000 chars)
  keywords.txt                # Comma-separated keywords (max 100 chars)
  release_notes.txt           # What's new in this version
  promotional_text.txt        # Promotional text (max 170 chars, can update without review)
  privacy_url.txt             # Privacy policy URL
  support_url.txt             # Support URL
  marketing_url.txt           # Marketing URL (optional)
```

Write metadata templates with guidance comments:
- name.txt: App name that includes primary keyword if possible.
- subtitle.txt: Value proposition in 30 chars.
- description.txt: First 3 lines are critical (visible before "more" tap).
  Structure: hook -> key features (bullet points) -> social proof -> CTA.
- keywords.txt: 100 chars of comma-separated keywords. No spaces after commas.
  Prioritize: long-tail keywords, avoid duplicating words in title/subtitle.

============================================================
PHASE 7: REVIEW COMPLIANCE CHECK
============================================================

Audit the app against common App Store Review rejection reasons:

METADATA:
- [ ] App name does not contain generic terms like "app" or "free".
- [ ] Screenshots accurately represent the app's functionality.
- [ ] Description does not mention other platforms (Android, etc.).
- [ ] Age rating matches app content.

FUNCTIONALITY:
- [ ] App provides meaningful functionality (not a thin wrapper around a website).
- [ ] All features shown in screenshots are functional.
- [ ] Login/signup works without invitation codes (or demo credentials provided).
- [ ] App does not crash on launch or during normal use.

PRIVACY:
- [ ] Privacy policy URL is valid and accessible.
- [ ] App Tracking Transparency prompt shown before IDFA access.
- [ ] Data collection matches App Privacy Nutrition Label declarations.
- [ ] Location permission usage description is specific (not generic).

PAYMENTS:
- [ ] All digital goods/services use In-App Purchase (not Stripe, PayPal, etc.).
- [ ] Physical goods/services may use external payment.
- [ ] No links to external purchase pages for digital content.

DESIGN:
- [ ] App uses standard iOS UI patterns or provides clear custom alternatives.
- [ ] No misleading UI that mimics system alerts.
- [ ] App respects user's system settings (dark mode, accessibility).

Generate a compliance checklist with PASS/FAIL/MANUAL-CHECK for each item.

============================================================
PHASE 8: PHASED RELEASE CONFIGURATION
============================================================

Configure phased release in the Fastlane deliver configuration:
- Day 1: 1% of users
- Day 2: 2% of users
- Day 3: 5% of users
- Day 4: 10% of users
- Day 5: 20% of users
- Day 6: 50% of users
- Day 7: 100% of users

Monitor crash-free rate between phases. Document how to pause/resume rollout.


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

## App Store Publishing Pipeline Complete

### Signing
- **Method:** {Fastlane match / Manual}
- **Team ID:** {detected or placeholder}
- **Bundle ID:** {detected}
- **Profiles:** development, adhoc, appstore

### Fastlane Lanes
| Lane | Action | Trigger |
|------|--------|---------|
| test | Run tests with coverage | Pre-flight |
| beta | Build + TestFlight upload | PR merge to develop |
| release | Build + App Store upload | Tag on main |

### Metadata Status
| File | Status | Notes |
|------|--------|-------|
| name.txt | {READY / TEMPLATE} | {guidance} |
| description.txt | {READY / TEMPLATE} | {guidance} |
| keywords.txt | {READY / TEMPLATE} | {guidance} |
| screenshots | {AUTOMATED / MANUAL} | {device list} |

### Review Compliance
| Category | Checks | Pass | Fail | Manual |
|----------|--------|------|------|--------|
| Metadata | N | N | N | N |
| Functionality | N | N | N | N |
| Privacy | N | N | N | N |
| Payments | N | N | N | N |
| Design | N | N | N | N |

### Files Created
{list all generated files with paths}

DO NOT:
- Commit signing certificates or private keys to the repository.
- Hardcode App Store Connect credentials in Fastfile -- use environment variables.
- Submit for review automatically on first setup -- let the user review metadata first.
- Skip compliance checks -- rejection delays releases significantly.
- Use password-based authentication -- prefer App Store Connect API key.
- Generate screenshots without proper UI test coverage.
- Include placeholder text in metadata files that could be accidentally submitted.

NEXT STEPS:
- "Run `bundle exec fastlane beta` to push your first TestFlight build."
- "Run `/app-store-optimization` to optimize keywords and metadata for discoverability."
- "Run `/store-compliance` for a deep compliance review before submission."
- "Run `/mobile-ci-cd` to automate TestFlight and App Store builds in CI."


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /app-store-publish — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
