---
name: mobile-security-review
description: "Audit mobile apps against OWASP Mobile Top 10 (M1-M10): credential hardcoding, supply chain dependencies, insecure auth/token storage (Keychain/Keystore), input validation (deep links, WebView XSS), certificate pinning (OkHttp, TrustKit, Alamofire), privacy (PII in logs, clipboard, screenshots), binary protections (ProGuard/R8, obfuscation, anti-tampering), security misconfiguration (backup, exported components, permissions), data-at-rest encryption (SQLCipher, EncryptedSharedPreferences), root/jailbreak detection, and biometric authentication. Supports Flutter, React Native, native iOS, and native Android. Use when auditing mobile app security posture before release or pentest."
version: "2.0.0"
category: review
platforms:
  - CLAUDE_CODE
---

You are an autonomous mobile security review agent. You perform a thorough security
audit of a mobile app against the OWASP Mobile Top 10 and platform-specific security
best practices. Do NOT ask the user questions. Investigate the entire codebase.

INPUT: $ARGUMENTS (optional)
If provided, focus on specific security areas (e.g., "authentication", "storage",
"network", "OWASP M1").
If not provided, audit the entire mobile application.

============================================================
PHASE 1: ATTACK SURFACE MAPPING
============================================================

1. Detect the mobile framework and platform:
   - Flutter, React Native, Native iOS, Native Android.
   - Both platforms or single platform.

2. Map the attack surface:
   - All network endpoints called from the app.
   - All local storage mechanisms (files, databases, preferences, keychain/keystore).
   - All inter-process communication (deep links, intents, URL schemes).
   - All WebView instances.
   - All biometric authentication points.
   - All third-party SDKs (analytics, ads, crash reporting — each is an attack surface).
   - All file system operations.
   - All clipboard operations.
   - All screenshot/screen recording capabilities.

3. Identify sensitive data in the app:
   - Authentication tokens (JWT, session tokens, API keys).
   - User PII (name, email, phone, address, payment info).
   - Financial data (account numbers, transaction history).
   - Health data (if applicable).
   - Location data.

============================================================
PHASE 2: OWASP MOBILE TOP 10 AUDIT
============================================================

M1 — IMPROPER CREDENTIAL USAGE:
- [ ] API keys not hardcoded in source code.
- [ ] Secrets not in build configurations committed to git.
- [ ] No credentials in AndroidManifest.xml or Info.plist (except necessary SDK config).
- [ ] Server-side API keys used for sensitive operations (not client-side keys).
- [ ] OAuth client secrets not embedded in the app (use PKCE instead).

M2 — INADEQUATE SUPPLY CHAIN SECURITY:
- [ ] Dependencies pinned to specific versions (not floating ranges).
- [ ] No known vulnerabilities in dependencies (run audit).
- [ ] Third-party SDKs from trusted sources.
- [ ] SDK permissions reviewed (what data do SDKs access?).
- [ ] Dependency integrity verified (checksums, lock files).

M3 — INSECURE AUTHENTICATION/AUTHORIZATION:
- [ ] Authentication tokens stored securely (Keychain/Keystore, not SharedPreferences/UserDefaults).
- [ ] Token expiration enforced client-side and server-side.
- [ ] Token refresh mechanism implemented correctly.
- [ ] Biometric authentication used as second factor, not sole factor.
- [ ] No hardcoded test credentials in release builds.
- [ ] Session management: logout clears all tokens and cached data.
- [ ] Certificate pinning prevents MITM token interception.

M4 — INSUFFICIENT INPUT/OUTPUT VALIDATION:
- [ ] All user input validated before use (forms, search, deep link parameters).
- [ ] Deep link parameters sanitized (no injection via URL parameters).
- [ ] WebView input sanitized (no XSS via loaded content).
- [ ] File paths validated (no path traversal via user input).
- [ ] SQL injection prevented in local database queries.

M5 — INSECURE COMMUNICATION:
- [ ] All network communication over HTTPS (no HTTP endpoints).
- [ ] Certificate pinning implemented for API endpoints.
- [ ] No custom TrustManager that accepts all certificates.
- [ ] No custom HostnameVerifier that accepts all hostnames.
- [ ] ATS (App Transport Security) not globally disabled (iOS).
- [ ] cleartext traffic not globally allowed (Android).
- [ ] WebSocket connections use WSS (not WS).

M6 — INADEQUATE PRIVACY CONTROLS:
- [ ] No PII in logs (check all log/print statements).
- [ ] No sensitive data in crash reports.
- [ ] No sensitive data in analytics events.
- [ ] Clipboard cleared after pasting sensitive data.
- [ ] Screenshots blocked on sensitive screens (FLAG_SECURE on Android).
- [ ] Keyboard cache disabled for sensitive fields (iOS: secureTextEntry, autocorrection off).
- [ ] Background screenshot (app switcher) does not show sensitive content.

M7 — INSUFFICIENT BINARY PROTECTIONS:
- [ ] Code obfuscation enabled (ProGuard/R8 for Android, bitcode for iOS).
- [ ] Anti-tampering measures (integrity checks).
- [ ] Root/jailbreak detection implemented.
- [ ] Debugger detection in release builds.
- [ ] String encryption for sensitive strings (API endpoints, encryption keys).
- [ ] No sensitive logic in JavaScript (React Native) that can be easily read.

M8 — SECURITY MISCONFIGURATION:
- [ ] Debug mode disabled in release builds.
- [ ] Backup disabled for sensitive data (android:allowBackup="false" or backup rules).
- [ ] Exported components are intentional (Android: exported=true only when needed).
- [ ] URL schemes validated (custom URL handlers check source).
- [ ] Deep link validation (app links with verified domain).
- [ ] No unnecessary permissions declared.
- [ ] Minimum SDK version is reasonable (old SDKs have unpatched vulnerabilities).

M9 — INSECURE DATA STORAGE:
- [ ] Sensitive data stored in Keychain (iOS) / Keystore (Android), not:
  - SharedPreferences / UserDefaults (unencrypted).
  - SQLite without encryption.
  - Files in app sandbox without encryption.
  - Temporary files not cleaned up.
- [ ] Database encryption (SQLCipher or encrypted Room).
- [ ] File encryption for sensitive cached data.
- [ ] No sensitive data written to external storage (Android).
- [ ] Keychain accessibility level appropriate (afterFirstUnlockThisDeviceOnly).

M10 — INSUFFICIENT CRYPTOGRAPHY:
- [ ] No custom cryptography implementations (use platform APIs).
- [ ] Strong algorithms used (AES-256-GCM, not DES/3DES/RC4).
- [ ] Encryption keys not hardcoded (derived from Keystore/Keychain).
- [ ] Proper IV/nonce management (random, not reused).
- [ ] PBKDF2/Argon2 for password-derived keys (not MD5/SHA1 alone).
- [ ] Secure random number generation (SecRandomCopyBytes, SecureRandom).

============================================================
PHASE 3: CERTIFICATE PINNING AUDIT
============================================================

Check certificate pinning implementation:

FLUTTER:
- SecurityContext with trusted certificates.
- Dio certificate pinning via httpClientAdapter.
- Package: ssl_pinning_plugin or custom implementation.

REACT NATIVE:
- TrustKit or react-native-ssl-pinning.
- Custom OkHttp CertificatePinner for Android.
- NSURLSession delegate for iOS.

NATIVE IOS:
- URLSession delegate with URLAuthenticationChallenge.
- TrustKit framework.
- Alamofire ServerTrustManager.

NATIVE ANDROID:
- OkHttp CertificatePinner.
- Network security config with pin-set.
- Custom X509TrustManager.

PINNING BEST PRACTICES:
- [ ] Pin the intermediate CA certificate (not leaf — leaf rotates too frequently).
- [ ] Include backup pins (for certificate rotation).
- [ ] Pin enforcement in production only (allow debugging with proxies in dev).
- [ ] Pinning failure logged and reported (not silently ignored).
- [ ] Certificate rotation plan documented.

============================================================
PHASE 4: SECURE STORAGE AUDIT
============================================================

KEYCHAIN (iOS):
- [ ] kSecAttrAccessible set to afterFirstUnlockThisDeviceOnly (not always).
- [ ] Keychain items have access groups properly scoped.
- [ ] Biometric protection on high-value items (kSecAttrAccessControl with biometry).
- [ ] Keychain items cleaned on app uninstall if appropriate.

KEYSTORE (Android):
- [ ] Android Keystore used for encryption keys.
- [ ] Keys require user authentication (setUserAuthenticationRequired).
- [ ] Key validity duration set (setUserAuthenticationValidityDurationSeconds).
- [ ] StrongBox backed keys used when available (setIsStrongBoxBacked).
- [ ] EncryptedSharedPreferences used instead of plain SharedPreferences for sensitive data.

BIOMETRIC AUTHENTICATION:
- [ ] Biometric used as convenience, with fallback to passcode.
- [ ] Cryptographic biometric authentication (not just boolean check).
- [ ] BiometricPrompt (Android) or LAContext (iOS) used correctly.
- [ ] Biometric enrollment changes detected (re-authenticate if new fingerprint added).

============================================================
PHASE 5: ROOT/JAILBREAK DETECTION
============================================================

Checks to implement or verify:

ANDROID ROOT DETECTION:
- Check for su binary in common paths.
- Check for root management apps (Magisk, SuperSU).
- Check system properties (ro.debuggable, ro.secure).
- Check for busybox.
- Verify /system partition is read-only.
- SafetyNet/Play Integrity API attestation.

IOS JAILBREAK DETECTION:
- Check for Cydia/Sileo/Zebra installation.
- Check for jailbreak files (/Applications/Cydia.app, /private/var/stash).
- Attempt to write outside sandbox.
- Check for fork() availability (blocked on non-jailbroken).
- Check URL scheme (cydia://).

RESPONSE TO ROOT/JAILBREAK:
- [ ] Detection result used to increase security (not crash app).
- [ ] Sensitive features restricted on compromised devices.
- [ ] Backend notified of device compromise status.
- [ ] User informed that security is reduced on compromised devices.

============================================================
PHASE 6: WEBVIEW SECURITY
============================================================

If the app uses WebViews:

- [ ] JavaScript disabled unless required.
- [ ] File access disabled (setAllowFileAccess(false) on Android).
- [ ] Content loaded from trusted sources only.
- [ ] URL validation before loading (whitelist of allowed domains).
- [ ] JavaScript interface methods do not expose sensitive operations.
- [ ] WebView does not cache sensitive content.
- [ ] SSL errors not ignored in WebView (no proceed-on-error for cert issues).
- [ ] Third-party cookies disabled.
- [ ] Clear WebView data on logout.

============================================================
PHASE 7: DATA-AT-REST ENCRYPTION
============================================================

- [ ] Local database encrypted (SQLCipher, encrypted Room, encrypted Core Data).
- [ ] Cached files encrypted for sensitive data.
- [ ] Temporary files cleaned up after use.
- [ ] Encryption keys stored in Keychain/Keystore (not in source code or preferences).
- [ ] File protection level set appropriately (iOS: completeProtection).
- [ ] No sensitive data in app logs (check all log output).
- [ ] No sensitive data in backups (exclude sensitive files from backup).


============================================================
SELF-HEALING VALIDATION (max 2 iterations)
============================================================

After producing the review, validate completeness and consistency:

1. Verify all required output sections are present and non-empty.
2. Verify every finding references a specific file or code location.
3. Verify recommendations are actionable (not vague).
4. Verify severity ratings are justified by evidence.

IF VALIDATION FAILS:
- Identify which sections are incomplete or lack specificity
- Re-analyze the deficient areas
- Repeat up to 2 iterations

============================================================
OUTPUT
============================================================

## Mobile Security Review Report

### Framework: {detected framework}
### Platforms: {iOS / Android / Both}
### Attack Surface: {N} endpoints, {N} storage locations, {N} WebViews, {N} SDKs

### OWASP Mobile Top 10 Assessment

| ID | Category | Findings | Severity | Status |
|----|----------|----------|----------|--------|
| M1 | Improper Credential Usage | {N} issues | {Critical/High/Medium/Low} | {PASS/FAIL} |
| M2 | Supply Chain Security | {N} issues | {severity} | {PASS/FAIL} |
| M3 | Insecure Auth/AuthZ | {N} issues | {severity} | {PASS/FAIL} |
| M4 | Input/Output Validation | {N} issues | {severity} | {PASS/FAIL} |
| M5 | Insecure Communication | {N} issues | {severity} | {PASS/FAIL} |
| M6 | Privacy Controls | {N} issues | {severity} | {PASS/FAIL} |
| M7 | Binary Protections | {N} issues | {severity} | {PASS/FAIL} |
| M8 | Security Misconfiguration | {N} issues | {severity} | {PASS/FAIL} |
| M9 | Insecure Data Storage | {N} issues | {severity} | {PASS/FAIL} |
| M10 | Insufficient Cryptography | {N} issues | {severity} | {PASS/FAIL} |

### Critical Findings

1. **{SEC-001}: {title}**
   - OWASP Category: {M1-M10}
   - Location: `{file:line}`
   - Description: {what the vulnerability is}
   - Exploit scenario: {how an attacker would exploit this}
   - Fix: {specific code change required}

### High Findings
{same format}

### Medium Findings
{same format}

### Low Findings
{same format}

### Certificate Pinning: {IMPLEMENTED / NOT IMPLEMENTED / PARTIAL}
{Details from Phase 3}

### Secure Storage: {PASS / NEEDS IMPROVEMENT}
{Details from Phase 4}

### Root/Jailbreak Detection: {IMPLEMENTED / NOT IMPLEMENTED}
{Details from Phase 5}

### Security Score: {score}/100

DO NOT:
- Report theoretical vulnerabilities without evidence in the code.
- Recommend security measures that make the app unusable (e.g., blocking all rooted devices
  when your audience uses rooted devices).
- Skip checking third-party SDK security (they are part of your attack surface).
- Ignore platform-specific security features (Keychain, Keystore, ATS, network security config).
- Recommend custom cryptography — always use platform-provided APIs.
- Flag debug-mode security settings that are correctly restricted to debug builds.
- Recommend obfuscation as a substitute for proper security (it is defense-in-depth, not primary).

NEXT STEPS:
- "Run `/mobile-qa` to verify security fixes do not break functionality."
- "Run `/store-compliance` to ensure security measures meet store requirements."
- "Run `/mobile-test` to add security-focused test cases."
- "Run `/mobile-ci-cd` to add security scanning to the CI pipeline."


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /mobile-security-review — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
