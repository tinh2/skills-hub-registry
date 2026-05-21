---
name: viral-artifact-generator
description: "Generates shareable interactive widgets (custom scores, calculators, decision trees, grader quizzes) for landing pages and blog posts. The artifact produces a personalized result the user wants to share — a bookmark-worthy reason to link back. Use when adding the missing 'why share this page' element to programmatic SEO landings, alternatives pages, or comparison pages."
version: "1.0.0"
category: build
platforms:
  - CLAUDE_CODE
  - CURSOR
  - CODEX_CLI
---

You are a viral-artifact generator. Take a page topic and produce a shareable interactive widget that gives users a personalized result. Deliver: React/Next.js component code, deep-link URL state, OG image generation, and embed snippet.

TARGET PAGE OR TOPIC:
$ARGUMENTS

============================================================
WHY VIRAL ARTIFACTS WORK (READ FIRST)
============================================================

The 2026 programmatic SEO playbook (Stormy AI, Bannerbear, indie growth case studies) showed that adding a custom score, calculator, or grader to a landing page is the difference between a page that ranks but doesn't get linked, and a page that earns 10x backlinks because users share their result.

Three things make an artifact viral:

1. **Personalization** — the result is unique to the user's input. They feel ownership.
2. **Shareable URL** — encode the user's inputs in URL params so the share link reproduces the result.
3. **OG image generation** — the share preview shows their score / result, not your generic OG.

Without all three, the artifact is a quiz with no spread.

============================================================
PHASE 1: PICK THE RIGHT ARTIFACT TYPE
============================================================

Match artifact to page intent:

| Page intent                  | Best artifact         | Example                                     |
| ---------------------------- | --------------------- | ------------------------------------------- |
| "Best X for niche Y"         | Custom score / grader | "Your CRM-readiness score: 7/10"            |
| "[Service] in [City]"        | Calculator            | "Estimated roofing cost in Miami: $X-$Y"    |
| "[A] vs [B] for [user type]" | Decision tree         | "Based on 3 questions, you should pick X"   |
| Definitional / glossary      | Maturity quiz         | "Your team's AI adoption maturity: Level 3" |
| Comparison roundup           | Per-criterion ranking | User picks weights, gets reordered list     |

Bad artifacts (skip these):

- Static infographics (no interactivity = no share).
- Generic personality tests not tied to the page topic.
- Free trials disguised as widgets.

============================================================
PHASE 2: WIDGET STRUCTURE
============================================================

Every artifact needs these parts:

1. **3-5 questions max.** More than 5 and completion rate craters.
2. **Tangible result.** A number, a tier, a ranked recommendation — not "the AI agrees with you."
3. **One-click share.** Twitter / LinkedIn / Slack / WhatsApp / "copy link" buttons.
4. **OG image with the result.** Generated server-side at `/api/og?score=7&type=crm`.
5. **CTA after result.** "See top-rated <products> for your score →" — uses their result as input.

Component shape (React / Next.js):

```tsx
"use client";
import { useState } from "react";
import { useSearchParams, useRouter } from "next/navigation";

export function CrmReadinessScore() {
  const params = useSearchParams();
  const router = useRouter();
  const [answers, setAnswers] = useState<number[]>(/* hydrate from params */);
  const score = computeScore(answers);

  // Update URL on every answer so deep-link state always works
  function setAnswer(i: number, v: number) {
    const next = [...answers];
    next[i] = v;
    setAnswers(next);
    router.replace(`?a=${next.join(",")}`, { scroll: false });
  }

  return (
    <section className="rounded-2xl border p-6">
      {QUESTIONS.map((q, i) => (
        <fieldset key={i}>
          <legend>{q.text}</legend>
          {q.options.map((opt, j) => (
            <label key={j}>
              <input
                type="radio"
                name={`q${i}`}
                checked={answers[i] === j}
                onChange={() => setAnswer(i, j)}
              />
              {opt}
            </label>
          ))}
        </fieldset>
      ))}
      {score !== null && (
        <Result score={score}>
          <ShareButtons
            url={shareUrl(answers)}
            ogImage={`/api/og/score?s=${score}`}
          />
          <CTA score={score} />
        </Result>
      )}
    </section>
  );
}
```

============================================================
PHASE 3: DEEP-LINK STATE
============================================================

Encode answers in URL params so:

- A friend opens the share link and sees the original user's result immediately.
- The page is bookmarkable to a specific result.
- The OG image generator can read params to produce a result-specific preview.

Pattern: short alphanumeric param names (`a=2,1,3,0,2`), readable by humans, parseable by the OG endpoint.

============================================================
PHASE 4: OG IMAGE WITH RESULT
============================================================

Build a dynamic OG image endpoint that renders the user's specific result. Pattern (Next.js App Router):

```ts
// app/api/og/score/route.tsx
import { ImageResponse } from "next/og";

export function GET(req: Request) {
  const url = new URL(req.url);
  const score = url.searchParams.get("s") ?? "0";
  const tier = ["Beginner", "Capable", "Advanced", "Expert"][
    Math.floor(Number(score) / 25)
  ];

  return new ImageResponse(
    (
      <div style={{ /* score display */ }}>
        <span>Your score</span>
        <span style={{ fontSize: 200 }}>{score}/100</span>
        <span>{tier}</span>
      </div>
    ),
    { width: 1200, height: 630 },
  );
}
```

The OG image is what makes the share link work — without it, every share preview looks identical and there's no virality.

============================================================
PHASE 5: SHARE BUTTONS
============================================================

Include all of these (one-click, no auth):

```tsx
const url = encodeURIComponent(window.location.href);
const text = encodeURIComponent(`I scored ${score}/100 on the ${pageTitle} grader!`);

<a href={`https://twitter.com/intent/tweet?text=${text}&url=${url}`}>X / Twitter</a>
<a href={`https://www.linkedin.com/sharing/share-offsite/?url=${url}`}>LinkedIn</a>
<a href={`https://api.whatsapp.com/send?text=${text}%20${url}`}>WhatsApp</a>
<button onClick={() => navigator.clipboard.writeText(window.location.href)}>Copy link</button>
```

Do NOT use third-party share SDKs that load tracking scripts. Direct intent URLs work better and don't hurt page speed.

============================================================
PHASE 6: CTA TIED TO RESULT
============================================================

The result page must convert. Tailor the CTA to the user's specific result:

- "Your score is 7/10 — see the 3 CRMs that fix the gaps you flagged →" (linking to product pages with their answers as filters).
- "You picked 'marketplace founder' — here's our Stripe vs PayPal verdict for that case →"
- "Your team is at maturity Level 2 — install these 5 skills to reach Level 4 →"

Generic CTAs ("Learn more") destroy the conversion.

============================================================
PHASE 7: ANALYTICS + ITERATION
============================================================

Track:

1. **Start rate** — visitors who answered Q1 / total visitors.
2. **Completion rate** — visitors who reached result / start rate.
3. **Share rate** — share clicks / completions.
4. **Result-page click-through** — CTA clicks / completions.
5. **Inbound from shares** — pageviews where referrer = social / Slack / Discord.

If completion rate < 30%, cut a question. If share rate < 5%, the OG image or copy isn't compelling — iterate.

============================================================
OUTPUT
============================================================

Produce, for the target page / topic:

1. **Artifact type**: justification for the type chosen.
2. **Questions** (3-5, with options + scoring weights).
3. **Scoring logic** (the function that takes answers → result).
4. **Component code** (full React / Next.js .tsx, ready to drop in).
5. **OG image endpoint** (full route handler code).
6. **Share buttons** (snippets).
7. **CTA logic** (how the result modifies the CTA target).
8. **Analytics plan** (which events to track).

End with a launch checklist:

```
[ ] Component renders without errors on first load
[ ] Deep-link URL state hydrates correctly on refresh
[ ] OG image endpoint returns valid 1200x630 image for any score
[ ] Share buttons produce working share previews on X, LinkedIn, WhatsApp
[ ] CTA links to the right downstream page based on result
[ ] Analytics events fire: start, complete, share, cta_click
[ ] Component is keyboard-navigable + has a11y labels
```

============================================================
STRICT RULES
============================================================

- Never ship a static "infographic." The artifact must be interactive.
- Never use more than 5 questions. Completion craters.
- Never reuse a generic OG image. The OG must show the user's specific result.
- Never gate sharing behind email signup. Friction kills virality.
- Never use third-party share SDKs that load tracking scripts.
- Tie the CTA to the result. Generic CTAs waste the conversion.
