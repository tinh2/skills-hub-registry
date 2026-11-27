---
name: humanizer
description: "Rewrite AI-drafted content so it reads human: cut filler and hedging, vary sentence length, curb em dashes, add specifics and voice. Triggers: humanize this, remove AI tells, sounds like ChatGPT, make it sound human."
version: "1.1.0"
category: analysis
platforms:
  - CLAUDE_CODE
  - CURSOR
  - CODEX_CLI
---

Rewrite the draft so a reader can't tell it was AI-written. Rewrite it; don't summarize it or ask about tone. Infer tone from the draft and its platform.

**Draft:** `$ARGUMENTS`

## AI tells to find

Count these before rewriting so the user sees what changed:

1. **Filler:** "In today's fast-paced world", "It's important/worth noting", "Whether you're a beginner or an expert", "Let's dive into", "At the end of the day", "In conclusion".
2. **Hedging:** "on one hand… on the other", "while X has merit, so does Y", "it depends", "your mileage may vary".
3. **Bullet cadence:** everything forced into three-bullet lists where prose would read better.
4. **Em dashes:** more than one per 200 words.
5. **Adverb stacking:** very, really, truly, incredibly, absolutely.
6. **Tricolons:** suspiciously parallel triplets ("fast, scalable, and reliable").
7. **Assistant framing:** "As a…, I", "Let me explain".
8. **Generic CTAs:** "Learn more", "Get started today", "Take your X to the next level".
9. **Buzzwords:** leverage, synergy, unlock, transform your workflow, best-in-class.
10. **Uniform sentence length:** AI drafts sit around 18 to 25 words; human writing ranges from 4 to 30.

## Rewrite

- Delete filler. A paragraph collapsing to one sentence is fine.
- Commit: turn hedges into direct claims with a reason ("Pick Y because…").
- Vary rhythm: some short sentences, some long ones.
- Keep em dashes to at most one per 200 words; use commas, parentheses or full stops instead.
- Make vague claims concrete ("many users", "studies show"): use a specific number or name **only if it's in the draft or the user gave it**; otherwise cut the claim. Never invent facts, stats, quotes or anecdotes.
- Add voice: about one or two sharp opinions or asides per 500 words, consistent with the author's stated position. Don't fabricate personal experiences.
- Make CTAs specific to the offer ("Install in one command: `npx …`").

## Check before delivering

- Em dashes ≤ 1 per 200 words.
- At least 3 sentences of 8 words or fewer and 3 of 25 or more (for drafts long enough to allow it).
- Zero filler phrases from the list; at most one tricolon per 500 words.
- Every quantitative claim is sourced or removed.
- At least one clear opinion per 500 words.

If a check fails, do another pass.

## Output

A short report, then the cleaned text with no preamble such as "Here's the humanized version":

```
HUMANIZER REPORT
Original: N words → Rewritten: N words (−X%)
Removed: filler N, hedges N, em dashes N → N, tricolons N, buzzwords N
Voice insertions: N
Checks: em-dash ratio …, sentence variance pass/fail, specificity pass/fail, voice pass/fail
```
