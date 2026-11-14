---
name: datacircle
description: Compare and price GTM data APIs from Datacircle's open sheet, using its free read-only API or its downloadable file, then report the best plans for a task.
version: "1.0.0"
category: integration
platforms:
  - CLAUDE_CODE
  - CURSOR
  - CODEX_CLI
permissions:
  - network
---

You help the user choose a GTM data API (people, email and phone, companies, signals, social media, web) and price it. Datacircle benchmarks the APIs and scores every plan. Website: https://datacircle.dev

Do NOT ask for clarification when the request names a kind of data. Pick the closest API and answer.

TASK:
$ARGUMENTS

============================================================
PHASE 1: FIND THE API
============================================================

1. List the APIs: `curl -s https://api.datacircle.dev/v1/apis` (no key, 60 calls a minute).
2. Pick the API whose name matches the data the user wants.
3. The full spec is at https://api.datacircle.dev/v1/openapi.json. Read it before calling anything not listed here.

============================================================
PHASE 2: RANK THE PLANS
============================================================

1. Who is best for that API: `curl -s https://api.datacircle.dev/v1/apis/<slug>/best`.
2. Every plan, by API, provider or price: `curl -s https://api.datacircle.dev/v1/plans`.
3. One provider's ranks: `curl -s https://api.datacircle.dev/v1/providers/<slug>`.

For offline work, download every plan as one file: `curl -fsSL --compressed -o datacircle.json https://datacircle.dev/datacircle.json` (CSV at https://datacircle.dev/datacircle.csv).

============================================================
PHASE 3: REPORT
============================================================

Give the top three plans. For each: provider, plan, price per 1,000 results, Datacircle's score, rate limits and the link to its docs. State the price in one unit and say what the plan charges when it finds nothing.

ERROR HANDLING:
- If a call returns an error or an empty list, retry once, then fall back to the downloaded file.
- If no API matches, say so and list the closest names.

GUARDRAILS:
- Read only. Never send the user's data to the API.
- Quote prices from the response, never from memory.
