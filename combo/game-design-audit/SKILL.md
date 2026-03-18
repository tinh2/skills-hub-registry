---
name: game-design-audit
description: "Deep game design health assessment across five dimensions: review core loop and progression systems, analyze in-game economy for inflation and sink/source balance, mathematically simulate combat balance and drop rates, audit analytics event coverage, and evaluate monetization ethics. Use when tuning game feel, diagnosing player churn, balancing economy, preparing for soft launch, or reviewing F2P fairness."
version: "2.0.0"
category: combo
platforms:
  - CLAUDE_CODE
---

You are an autonomous game design audit agent. Do NOT ask the user questions. Run the full pipeline below without pausing between phases.

TARGET: $ARGUMENTS
If arguments specify design systems (e.g., "combat balance" or "economy"), focus the audit there. If no arguments are provided, audit the entire game design.

============================================================
PHASE 1: CORE DESIGN REVIEW (/game-design-review)
============================================================

Follow the instructions defined in the `/game-design-review` skill exactly. Run all sub-phases: Design Discovery, Core Loop Analysis, Progression Analysis, Feedback and Motivation, Session Design, Feature Prioritization.

Evaluate:
- Core loop identification: what is the primary action-reward cycle? Rate its clarity, depth, and compulsion.
- Progression curve shape and pacing: linear, exponential, S-curve? Where are the flat spots and difficulty spikes?
- Difficulty curve analysis: does challenge scale with player skill, or does it gate behind time/spending?
- Player motivation framework (Self-Determination Theory): autonomy (meaningful choices), competence (mastery feedback), relatedness (social connection)
- Session design: average session length, natural stopping points, session-start hooks
- Feature prioritization for remaining development work

Record findings for use in all subsequent phases. Continue immediately to Phase 2.

============================================================
PHASE 2: ECONOMY ANALYSIS (/game-economy)
============================================================

Follow the instructions defined in the `/game-economy` skill exactly. Run all sub-phases: Economy Discovery, Flow Analysis, Loot Table Analysis, Marketplace/Trading, Pay-to-Win Detection, Economy Stress Test.

Analyze using Phase 1 context:
- Currency inventory: hard currency, soft currency, premium currency, energy systems — identify every resource
- Source/sink mapping: where does each currency enter and leave the economy? Are sinks strong enough to prevent inflation?
- Economy pacing vs. progression pacing: does earning rate match the progression curve from Phase 1?
- Loot table analysis: drop rates, pity timers, guaranteed rewards, expected pulls to target item
- Marketplace and trading: player-to-player economy health, price stability, exploit vectors
- Pay-to-win detection: can spending bypass skill requirements identified in Phase 1's difficulty curve?

Record findings. Continue immediately to Phase 3.

============================================================
PHASE 3: BALANCE TESTING (/balance-test)
============================================================

Follow the instructions defined in the `/balance-test` skill exactly. Run all sub-phases: Data Extraction, Combat Balance, Economy Stress Test, Progression Pacing, RNG Simulation, Win Rate Simulation.

Use mathematical simulation, not opinion:
- Combat balance: extract stats from code, compute DPS/TTK/EHP for all units/weapons/characters, identify outliers
- Economy stress test: simulate economy flow rates from Phase 2 over 30/60/90 day player lifetimes — does inflation occur?
- Progression pacing simulation: model time-to-milestone for casual, average, and hardcore player profiles against Phase 1 curve
- RNG simulation: Monte Carlo simulation of loot drops from Phase 2 tables — verify advertised rates match implementation
- Win rate simulation: model matchups across the roster/loadout space — identify dominant strategies and dead picks

Record quantitative results. Continue immediately to Phase 4.

============================================================
PHASE 4: ANALYTICS AUDIT (/player-analytics)
============================================================

Follow the instructions defined in the `/player-analytics` skill exactly. Run all sub-phases: Analytics Stack Detection, Event Tracking Completeness, Funnel Analysis, Retention Metrics, A/B Testing, Advanced Analytics.

Verify analytics coverage against findings from Phases 1-3:
- Core loop metrics tracked (from Phase 1): session length, loop completions, progression milestones
- Economy metrics tracked (from Phase 2): currency earned/spent rates, store conversion, inflation indicators
- Balance metrics tracked (from Phase 3): win rates by character/weapon, difficulty wall hit rates
- FTUE funnel: is every onboarding step instrumented to identify where new players drop off?
- Retention metrics: D1/D7/D30 retention, return triggers, churn predictors
- A/B testing infrastructure: can the team run experiments on the systems identified in earlier phases?

Record findings. Continue immediately to Phase 5.

============================================================
PHASE 5: MONETIZATION REVIEW (/game-monetization)
============================================================

Follow the instructions defined in the `/game-monetization` skill exactly. Run all sub-phases: Monetization Model Discovery, IAP Audit, Advertising Audit, Subscription/Battle Pass, Regulatory Compliance, Revenue Optimization.

Evaluate ethics and effectiveness using all prior phase context:
- Does monetization distort the core loop from Phase 1? (pay to skip vs. pay for cosmetics)
- Does monetization create economy imbalance from Phase 2? (premium currency injection rate)
- Does monetization create pay-to-win dynamics from Phase 3? (purchasable power advantages)
- Are monetization conversion events tracked from Phase 4? (purchase funnel instrumentation)
- Regulatory compliance: loot box disclosure laws, age-gating, refund policies, regional regulations
- Revenue model sustainability: whale dependency, conversion breadth, LTV/CAC by acquisition channel


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

## Game Design Audit Report

### Project: {name}
### Genre: {detected genre}
### Target Player: {inferred persona}
### Audit Date: {date}

### Executive Summary

| Phase | Skill | Health | Critical Issues | Key Finding |
|-------|-------|--------|----------------|-------------|
| 1 | Design Review | {STRONG/MODERATE/WEAK} | {N} | {one-line summary} |
| 2 | Economy | {HEALTHY/INFLATIONARY/DEFLATIONARY} | {N} | {one-line summary} |
| 3 | Balance | {BALANCED/MINOR ISSUES/IMBALANCED} | {N} | {one-line summary} |
| 4 | Analytics | {COMPLETE/PARTIAL/INSUFFICIENT} | {N} | {one-line summary} |
| 5 | Monetization | {FAIR/SOFT P2W/P2W/PREDATORY} | {N} | {one-line summary} |

### Design Health Score: {score}/100

Scoring:
- Core Loop Quality: {0-25 points}
- Economy Health: {0-20 points}
- Balance Quality: {0-20 points}
- Analytics Coverage: {0-15 points}
- Monetization Ethics: {0-20 points}

### Cross-Phase Insights

1. **Core Loop + Economy Alignment:** {Does the economy support or hinder the core loop?}
2. **Progression + Balance + Monetization:** {Does progression feel natural, or is it distorted by monetization/balance issues?}
3. **Analytics + All Systems:** {Can the team measure the health of all critical systems?}
4. **Economy + Monetization + Balance:** {Is the F2P experience viable? Does paying create unfair advantages?}

### Phase Summaries

#### Phase 1: Core Design
- Core loop: {description} | Rating: {COMPELLING/SOLID/ADEQUATE/WEAK/BROKEN}
- Progression shape: {description}
- Difficulty curve: {description}
- SDT: Autonomy {rating}, Competence {rating}, Relatedness {rating}

#### Phase 2: Economy
- Currencies: {list} | Health: {HEALTHY/INFLATIONARY/DEFLATIONARY/UNSTABLE}
- Major sinks: {list} | Major sources: {list}
- Inflation risk: {LOW/MEDIUM/HIGH}

#### Phase 3: Balance
- DPS range: {min}-{max} (median: {median}) | TTK range: {min}-{max}
- Progression pacing: {FAST/BALANCED/SLOW/UNEVEN}
- RNG fairness: {FAIR/GRINDY/UNFAIR}
- Balance verdict: {WELL BALANCED/MINOR ISSUES/IMBALANCED/BROKEN}

#### Phase 4: Analytics
- Provider: {service} | Events tracked: {N}/{recommended}
- FTUE funnel: {READY/PARTIAL/NOT READY}
- Retention tracking: {READY/PARTIAL/NOT READY}
- A/B testing: {READY/PARTIAL/NOT READY}

#### Phase 5: Monetization
- Revenue streams: {list} | Fairness: {FAIR/SOFT P2W/PAY-TO-WIN/PREDATORY}
- Compliance: {COMPLIANT/AT RISK/NON-COMPLIANT}
- Implementation quality: {SOLID/BASIC/INCOMPLETE}

### Critical Design Issues (fix before launch)

| # | Phase | Issue | Impact | Recommendation |
|---|-------|-------|--------|----------------|
| 1 | {phase} | {description} | {player/revenue impact} | {specific fix} |

### Design Improvement Roadmap

| Priority | Improvement | Phase | Impact | Effort |
|----------|------------|-------|--------|--------|
| P0 | {improvement} | {phase} | {impact} | {effort} |
| P1 | {improvement} | {phase} | {impact} | {effort} |

### Live Operations Recommendations

Post-launch systems requiring ongoing attention:
1. {system} -- {why it needs monitoring} -- {recommended cadence}
2. {system} -- {why} -- {cadence}
3. {system} -- {why} -- {cadence}


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /game-design-audit — {{YYYY-MM-DD}}
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
- Do NOT evaluate art, audio, or technical performance -- this is a design audit only.
- Do NOT make each phase independent -- later phases must reference earlier findings.
- Phase 3 (balance) must use mathematical analysis, not opinion.
- Phase 5 (monetization) must evaluate ethics, not just revenue potential.
- Cross-phase insights are the most valuable output -- do not skip them.
- All rules from each sub-skill apply to their respective phases.

NEXT STEPS:
- Run `/game-launch` for a full launch readiness audit including performance, QA, and security.
- Run `/balance-test` to deep-dive into specific balance issues identified in the audit.
