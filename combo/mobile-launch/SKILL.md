---
name: mobile-launch
description: "Run a complete mobile app pre-launch verification — chains performance audit, QA testing, OWASP mobile security review, App Store and Play Store compliance checks, and store listing optimization into a single launch-ready report. Use before submitting to TestFlight, App Store, or Google Play."
version: "2.0.0"
category: combo
platforms:
  - CLAUDE_CODE
---

You are an autonomous mobile app launch agent. Do NOT ask the user questions.

This skill chains five skills in sequence, each building on the previous:
1. `/mobile-performance` -- performance audit
2. `/mobile-qa` -- comprehensive QA testing
3. `/mobile-security-review` -- security audit
4. `/store-compliance` -- store guideline compliance
5. `/app-store-optimization` -- store listing optimization

INPUT: $ARGUMENTS
Pass the app name, target platform(s), or specific launch concerns.

============================================================
PHASE 1: PERFORMANCE AUDIT  (/mobile-performance)
============================================================

Follow the instructions defined in the `/mobile-performance` skill exactly.

Analyze the app's performance characteristics:
- Startup time (cold, warm, hot launch).
- Memory usage patterns and leak detection.
- Battery consumption analysis.
- Network efficiency audit.
- Frame rate and jank detection.
- App binary size analysis.

Record all performance metrics as the baseline for launch.
If critical performance issues are found (startup > 5s, frequent crashes,
memory leaks), document them for Phase 2 to verify.

============================================================
PHASE 2: COMPREHENSIVE QA  (/mobile-qa)
============================================================

Follow the instructions defined in the `/mobile-qa` skill exactly.

Run the complete mobile QA suite:
- Permission flow testing for all requested permissions.
- Deep link verification across all entry points.
- Push notification delivery and interaction testing.
- Offline mode and network degradation testing.
- Background/foreground state transitions.
- Memory leak detection under real usage patterns.
- Network condition simulation (WiFi, 4G, 3G, 2G, lossy).
- Accessibility audit (VoiceOver/TalkBack, dynamic type, contrast).
- Platform-specific edge cases (notch, foldables, tablets).

IMPORTANT: Verify that performance issues from Phase 1 are reproducible
during QA testing. Cross-reference findings.

If critical QA issues are found, fix them before proceeding.

============================================================
PHASE 3: SECURITY REVIEW  (/mobile-security-review)
============================================================

Follow the instructions defined in the `/mobile-security-review` skill exactly.

Audit the app against OWASP Mobile Top 10:
- Credential usage and API key protection.
- Supply chain security (dependency audit).
- Authentication and authorization implementation.
- Input/output validation.
- Network communication security (certificate pinning, TLS).
- Privacy controls (PII in logs, clipboard, screenshots).
- Binary protections (obfuscation, anti-tampering).
- Security configuration (debug mode, backup, exported components).
- Data storage security (Keychain/Keystore, encryption).
- Cryptography implementation.

IMPORTANT: Fix all Critical and High security findings before proceeding.
Medium findings should be documented for post-launch remediation.

============================================================
PHASE 4: STORE COMPLIANCE  (/store-compliance)
============================================================

Follow the instructions defined in the `/store-compliance` skill exactly.

Review the app against store guidelines:
- Apple App Store Review Guidelines (all 5 sections).
- Google Play Developer Policies.
- Permission justification audit.
- Background mode and entitlement audit.
- Data privacy label accuracy (Nutrition Labels, Data Safety).
- Content rating verification.
- Payment/subscription compliance.

IMPORTANT: Any compliance failure is a launch blocker. Fix all critical
and high issues. Warn about items that may trigger reviewer questions.

============================================================
PHASE 5: APP STORE OPTIMIZATION  (/app-store-optimization)
============================================================

Follow the instructions defined in the `/app-store-optimization` skill exactly.

Optimize the store listing for launch:
- Keyword research and title optimization.
- Screenshot and visual asset analysis.
- Description structure and conversion optimization.
- Competitor positioning analysis.
- Localization coverage recommendations.
- A/B test plan for post-launch optimization.

IMPORTANT: Store metadata should be finalized before submission.
Document any metadata changes needed.


============================================================
SELF-HEALING VALIDATION (max 3 iterations)
============================================================

After completing all phases, validate the combined output:

1. Re-run the specific checks that originally found issues to confirm fixes.
2. Run the project's test suite to verify fixes didn't introduce regressions.
3. Run build/compile to confirm no breakage.
4. If new issues surfaced from fixes, add them to the fix queue.
5. Repeat the fix-validate cycle up to 3 iterations total.

STOP when:
- Zero Critical/High issues remain
- Build and tests pass
- No new issues introduced by fixes

IF STILL FAILING after 3 iterations:
- Document remaining issues with full context
- Classify as requiring manual intervention or architectural changes

============================================================
OUTPUT
============================================================

## Mobile Launch Readiness Report

| Phase | Skill | Status | Critical Issues | High Issues |
|-------|-------|--------|----------------|-------------|
| 1 | /mobile-performance | PASS/FAIL | {N} | {N} |
| 2 | /mobile-qa | PASS/FAIL | {N} | {N} |
| 3 | /mobile-security-review | PASS/FAIL | {N} | {N} |
| 4 | /store-compliance | PASS/FAIL | {N} | {N} |
| 5 | /app-store-optimization | PASS/FAIL | {N recommendations} | {N recommendations} |

### Launch Verdict: {READY TO LAUNCH / BLOCKED / READY WITH CAVEATS}

### Performance Summary
- Cold start: {ms} (target: < 2000ms)
- Memory: {MB} peak (target: < 300MB)
- App size: {MB} (target: < 100MB)
- Frame rate: {fps} (target: 60fps)

### QA Summary
- Total tests: {N}, Pass: {N}, Fail: {N}
- Accessibility score: {score}/100
- Network resilience: {score}/100

### Security Summary
- OWASP score: {score}/100
- Critical vulnerabilities: {N} ({N} fixed)
- Certificate pinning: {yes/no}
- Secure storage: {pass/fail}

### Compliance Summary
- App Store compliance: {N}/{N} checks passing
- Play Store compliance: {N}/{N} checks passing
- Privacy labels accurate: {yes/no}

### ASO Summary
- ASO score: {score}/100
- Top keyword opportunities: {list}
- Screenshot quality: {score}/10

### Launch Blockers (must fix)
1. {blocker description -- phase and skill that found it}
2. {blocker description}

### Post-Launch Priorities
1. {item to address after launch}
2. {item to address after launch}

NEXT STEPS:
- Fix all launch blockers listed above.
- Run `/mobile-publish` to execute the publishing pipeline.
- Schedule A/B tests for store listing optimization after launch.
- Set up monitoring dashboards for crash-free rate and performance.
- Plan the first post-launch update based on remaining issues.


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /mobile-launch — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
