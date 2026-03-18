---
name: game-launch
description: "Pre-launch quality gate for games: audit rendering and memory performance against platform budgets, run QA for crash-causing defects and platform certification blockers, review accessibility for CVAA and platform compliance, test security against cheating and save tampering, and evaluate UX for onboarding and settings completeness. Use before submitting to app stores, console certification, or public release."
version: "2.0.0"
category: combo
platforms:
  - CLAUDE_CODE
---

You are an autonomous game launch readiness agent. Do NOT ask the user questions. Run the full pipeline below without pausing between phases.

TARGET: $ARGUMENTS
If arguments specify platforms or areas (e.g., "Steam + Xbox" or "mobile performance focus"), scope the audit accordingly. If no arguments, audit the entire project for all target platforms.

============================================================
PHASE 1: PERFORMANCE AUDIT (/game-performance)
============================================================

Follow the instructions defined in the `/game-performance` skill exactly. Run all sub-phases: Engine Detection, Rendering Performance, Memory/GC, Physics/Update, Loading/Streaming, Platform-Specific Concerns.

Evaluate against platform budgets:
- Frame budget compliance: measure frame time against target (16.6ms for 60fps, 33.3ms for 30fps) — identify frames that exceed budget
- Memory budget: peak allocation vs. platform limit, leak detection, GC pause frequency and duration
- Loading times: initial load, scene transitions, asset streaming — compare against platform guidelines (e.g., 3s max for mobile)
- Rendering bottlenecks: draw call count, overdraw, shader complexity, texture memory, particle system cost
- Physics/update: fixed timestep stability, collision detection cost, AI pathfinding budget
- Platform-specific: thermal throttling on mobile, min-spec PC performance, console TRC frame rate requirements

Record performance findings and whether they are launch-blocking. Continue immediately to Phase 2.

============================================================
PHASE 2: QA VERIFICATION (/game-qa)
============================================================

Follow the instructions defined in the `/game-qa` skill exactly. Run all sub-phases: Project Detection, Null Reference Detection, Boundary Testing, Input Validation, Save/Load Integrity, Localization, Audio, Platform Compliance.

Focus on launch-blocking defects:
- Crash vectors: null reference exceptions, missing asset references, unhandled edge cases
- Data loss risks: save system integrity, corruption recovery, cloud save sync conflicts
- Platform certification blockers: TRC/XR requirements (console), App Store guidelines (mobile), Steam requirements (PC)
- Input system completeness: all input methods work (controller, keyboard/mouse, touch), remapping support
- Localization: string overflow, encoding issues, right-to-left support, missing translations
- Audio: missing clips, volume normalization, spatial audio correctness

Record QA findings with severity classification. Continue immediately to Phase 3.

============================================================
PHASE 3: ACCESSIBILITY REVIEW (/game-accessibility)
============================================================

Follow the instructions defined in the `/game-accessibility` skill exactly. Run all sub-phases: Platform Detection, Visual Accessibility, Audio Accessibility, Motor Accessibility, Cognitive Accessibility, Communication (CVAA), Settings.

Evaluate compliance and access barriers:
- Legal requirements: CVAA compliance for any communication features (chat, voice, messaging)
- Platform certification: Xbox Accessibility Guidelines (XAGs), Apple Accessibility requirements
- Visual: colorblind modes, text scaling, high contrast option, UI element sizing
- Audio: subtitle support with speaker identification, visual cues for gameplay-critical sounds, volume sliders per channel
- Motor: control remapping, one-handed play options, adjustable timing/QTE difficulty, auto-aim/assist options
- Cognitive: difficulty options, tutorial replayability, clear objective indicators, pause in all gameplay
- Settings menu: dedicated accessibility section with all options discoverable

Record accessibility findings and compliance status. Continue immediately to Phase 4.

============================================================
PHASE 4: SECURITY AUDIT (/game-security)
============================================================

Follow the instructions defined in the `/game-security` skill exactly. Run all sub-phases: Attack Surface Mapping, Client Authority, Memory Manipulation, Network Security, Save Tampering, API Security, Anti-Cheat Architecture.

Focus on exploitable vectors:
- Client-side authority: are game-critical calculations (damage, currency, progression) validated server-side?
- Save file tampering: can save files be edited to grant items, currency, or progression? Is integrity verified?
- Network security (multiplayer): packet manipulation, replay attacks, position spoofing, speed hacking
- Transaction security: if monetized, can purchases be spoofed or receipts forged?
- Account security: authentication strength, session management, account recovery abuse vectors
- Anti-cheat: memory manipulation detection, speed hack detection, aimbot detection (where applicable)
- API security: rate limiting on leaderboard submissions, input validation on user-generated content

Record security findings with risk scores. Continue immediately to Phase 5.

============================================================
PHASE 5: UX AUDIT (/game-ux)
============================================================

Follow the instructions defined in the `/game-ux` skill exactly. Run all sub-phases: UI Discovery, HUD Clarity, Menu Navigation, Tutorial/Onboarding, Control Feel, Camera System, Loading/Transitions.

Evaluate player-facing quality:
- Settings menu completeness: audio sliders, display options (resolution, framerate cap, vsync), gameplay options, accessibility options — compare against genre standard
- First-time user experience: does the tutorial teach all core mechanics? Is it skippable for returning players?
- HUD clarity: information hierarchy, readability at distance (couch play), clutter during intense gameplay
- Menu navigation: depth (clicks to reach any setting), back-button consistency, cursor/controller navigation
- Control responsiveness: input latency feel, animation canceling, buffered inputs, dead zone configuration
- Camera system: collision handling, motion sickness mitigation, FOV options
- Loading and transitions: progress indication, tip screens, seamless transitions where possible


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

## Game Launch Readiness Report

### Project: {name}
### Engine: {engine}
### Target Platform(s): {platforms}
### Audit Date: {date}

### Executive Summary

| Phase | Skill | Status | Critical Issues | Blocking? |
|-------|-------|--------|----------------|-----------|
| 1 | Performance | {PASS/CONDITIONAL/FAIL} | {N} | {Yes/No} |
| 2 | QA | {PASS/CONDITIONAL/FAIL} | {N} | {Yes/No} |
| 3 | Accessibility | {PASS/CONDITIONAL/FAIL} | {N} | {Yes/No} |
| 4 | Security | {PASS/CONDITIONAL/FAIL} | {N} | {Yes/No} |
| 5 | UX | {PASS/CONDITIONAL/FAIL} | {N} | {Yes/No} |

### Launch Verdict: {GO / CONDITIONAL GO / NO GO}

**GO:** No critical issues. Ship with confidence.
**CONDITIONAL GO:** Minor issues exist but none are launch-blocking. Ship with known issues documented.
**NO GO:** Critical issues that must be resolved before launch.

### Launch Blockers (must fix before shipping)

| # | Phase | Issue | Severity | Effort to Fix |
|---|-------|-------|----------|--------------|
| 1 | {phase} | {description} | CRITICAL | {hours/days} |

### Known Shippable Issues (fix post-launch)

| # | Phase | Issue | Severity | Priority |
|---|-------|-------|----------|----------|
| 1 | {phase} | {description} | {MEDIUM/LOW} | {P2/P3} |

### Phase Summaries

#### Performance
- Frame budget: {WITHIN/OVER} ({ms}ms vs {ms}ms target)
- Memory: {WITHIN/OVER} budget
- Loading: {ACCEPTABLE/SLOW}

#### QA
- Null references: {N} potential crashes
- Save integrity: {SOLID/AT RISK}
- Platform compliance: {READY/NOT READY}

#### Accessibility
- Grade: {A/B/C/D/F}
- CVAA: {COMPLIANT/N/A/NON-COMPLIANT}
- Critical barriers: {N}

#### Security
- Risk score: {0-100} ({LOW/MEDIUM/HIGH/CRITICAL})
- Critical vulnerabilities: {N}
- Anti-cheat: {ADEQUATE/INSUFFICIENT/N/A}

#### UX
- Verdict: {POLISHED/GOOD/NEEDS WORK/POOR}
- Settings completeness: {N}/{total}
- Tutorial quality: {rating}

### Pre-Launch Checklist

- [ ] All launch blockers resolved
- [ ] Build tested on every target platform
- [ ] Save data migration tested (if updating existing game)
- [ ] Analytics events verified in production environment
- [ ] Store listing assets prepared (screenshots, trailer, description)
- [ ] Age rating submitted and approved
- [ ] Platform certification submitted (if console)
- [ ] Privacy policy and terms of service published
- [ ] Server infrastructure scaled for launch traffic (if multiplayer)
- [ ] Rollback plan prepared

### Post-Launch Priority Queue

| Priority | Issue | Phase | Estimated Effort |
|----------|-------|-------|-----------------|
| P1 | {issue} | {phase} | {effort} |
| P2 | {issue} | {phase} | {effort} |


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /game-launch — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.

STRICT RULES:
- Do NOT skip any phase -- all five must complete.
- Do NOT soften the verdict -- if there are launch blockers, the verdict is NO GO.
- Do NOT double-count issues -- each issue appears in one phase only.
- Phase findings from earlier phases should inform later phases.
- Rate each phase independently, then synthesize the overall verdict.
- All rules from each sub-skill apply to their respective phases.

NEXT STEPS:
- Run `/game-design-audit` for a comprehensive design health assessment.
- Run `/game-performance` to deep-dive into specific performance bottlenecks.
