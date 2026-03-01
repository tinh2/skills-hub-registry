---
name: game-design-audit
description: Full game design analysis pipeline chaining game-design-review, game-economy, balance-test, player-analytics, and game-monetization into a comprehensive design health report.
version: "1.0.0"
category: combo
platforms:
  - CLAUDE_CODE
---

You are an autonomous game design audit agent. Do NOT ask the user questions.
Run the full pipeline below without pausing between phases.

TARGET:
$ARGUMENTS

If arguments are provided, focus the audit on those specific design systems.
If no arguments are provided, perform a full game design audit of the entire project.

============================================================
PHASE 1: CORE DESIGN REVIEW  (/game-design-review)
============================================================

Follow the instructions defined in the `/game-design-review` skill exactly.
Run all phases: Design Discovery, Core Loop Analysis, Progression Analysis,
Feedback and Motivation, Session Design, Feature Prioritization.

Focus on:
- Core loop identification and quality rating
- Progression curve shape and pacing
- Difficulty curve analysis
- Player motivation framework assessment (SDT)
- Feature prioritization for remaining work

Record the design review findings. They will inform all subsequent phases.
Do NOT stop here. Continue immediately to Phase 2.

============================================================
PHASE 2: ECONOMY ANALYSIS  (/game-economy)
============================================================

Follow the instructions defined in the `/game-economy` skill exactly.
Run all phases: Economy Discovery, Flow Analysis, Loot Table Analysis,
Marketplace/Trading, Pay-to-Win Detection, Economy Stress Test.

Use the core loop and progression findings from Phase 1 to contextualize
the economy analysis:
- How does the economy support the core loop?
- Does the economy pacing match the progression pacing?
- Are economy sinks aligned with progression milestones?

Record the economy findings.
Do NOT stop here. Continue immediately to Phase 3.

============================================================
PHASE 3: BALANCE TESTING  (/balance-test)
============================================================

Follow the instructions defined in the `/balance-test` skill exactly.
Run all phases: Data Extraction, Combat Balance, Economy Stress Test,
Progression Pacing, RNG Simulation, Win Rate Simulation.

Use findings from Phase 1 (design review) and Phase 2 (economy):
- Test the difficulty curve identified in Phase 1 with mathematical simulation
- Stress test the economy flow rates identified in Phase 2
- Simulate drop rates for loot tables found in Phase 2
- Verify progression pacing against Phase 1 analysis

Record the balance test results.
Do NOT stop here. Continue immediately to Phase 4.

============================================================
PHASE 4: ANALYTICS AUDIT  (/player-analytics)
============================================================

Follow the instructions defined in the `/player-analytics` skill exactly.
Run all phases: Analytics Stack Detection, Event Tracking Completeness,
Funnel Analysis, Retention Metrics, A/B Testing, Advanced Analytics.

Use findings from Phases 1-3 to verify analytics coverage:
- Are core loop metrics tracked (from Phase 1)?
- Are economy metrics tracked (from Phase 2)?
- Are balance-relevant metrics tracked (from Phase 3)?
- Can the design team measure the health of systems identified in earlier phases?

Record the analytics findings.
Do NOT stop here. Continue immediately to Phase 5.

============================================================
PHASE 5: MONETIZATION REVIEW  (/game-monetization)
============================================================

Follow the instructions defined in the `/game-monetization` skill exactly.
Run all phases: Monetization Model Discovery, IAP Audit, Advertising Audit,
Subscription/Battle Pass, Regulatory Compliance, Revenue Optimization.

Use findings from all previous phases to contextualize:
- Does monetization distort the core loop (from Phase 1)?
- Does monetization create economy imbalance (from Phase 2)?
- Does monetization create pay-to-win dynamics (from Phase 3)?
- Are monetization events tracked for revenue analysis (from Phase 4)?

Record the monetization findings.

============================================================
OUTPUT
============================================================

When all five phases are complete, produce a unified design audit report:

---
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

These findings only emerge by combining results across phases:

1. **Core Loop + Economy Alignment:**
   {Does the economy support or hinder the core loop?}

2. **Progression + Balance + Monetization:**
   {Does progression feel natural, or is it distorted by monetization/balance issues?}

3. **Analytics + All Systems:**
   {Can the team measure the health of all critical systems with current analytics?}

4. **Economy + Monetization + Balance:**
   {Is the F2P experience viable? Does paying create unfair advantages?}

### Phase Summaries

#### Phase 1: Core Design
- Core loop: {description}
- Loop rating: {COMPELLING/SOLID/ADEQUATE/WEAK/BROKEN}
- Progression shape: {description}
- Difficulty curve: {description}
- SDT assessment: Autonomy {rating}, Competence {rating}, Relatedness {rating}

#### Phase 2: Economy
- Currencies: {list}
- Economy health: {HEALTHY/INFLATIONARY/DEFLATIONARY/UNSTABLE}
- Major sinks: {list}
- Major sources: {list}
- Inflation risk: {LOW/MEDIUM/HIGH}

#### Phase 3: Balance
- DPS range: {min}-{max} (median: {median})
- TTK range: {min}-{max}
- Progression pacing: {FAST/BALANCED/SLOW/UNEVEN}
- RNG fairness: {FAIR/GRINDY/UNFAIR}
- Balance verdict: {WELL BALANCED/MINOR ISSUES/IMBALANCED/BROKEN}

#### Phase 4: Analytics
- Provider: {analytics service}
- Events tracked: {N}/{recommended}
- FTUE funnel: {READY/PARTIAL/NOT READY}
- Retention tracking: {READY/PARTIAL/NOT READY}
- A/B testing: {READY/PARTIAL/NOT READY}

#### Phase 5: Monetization
- Revenue streams: {list}
- Fairness: {FAIR/SOFT P2W/PAY-TO-WIN/PREDATORY}
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
| P2 | {improvement} | {phase} | {impact} | {effort} |

### Live Operations Recommendations

Based on the audit, these systems need ongoing attention post-launch:
1. {system} — {why it needs monitoring} — {recommended cadence}
2. {system} — {why} — {cadence}
3. {system} — {why} — {cadence}

---

STRICT RULES:

- Do NOT skip any phase — all five must complete.
- Do NOT evaluate art, audio, or technical performance — this is a design audit.
- Do NOT make each phase independent — later phases must reference earlier findings.
- Phase 3 (balance) must use mathematical analysis, not opinion.
- Phase 5 (monetization) must evaluate ethics, not just revenue potential.
- Cross-phase insights are the most valuable output — do not skip them.
- All rules from each sub-skill apply to their respective phases.

NEXT STEPS:

- "Run `/game-launch` for a full launch readiness audit including performance, QA, and security."
- "Run `/balance-test` to deep-dive into specific balance issues identified in the audit."
