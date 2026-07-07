---
name: routerbase
description: "Integrate RouterBase as an OpenAI-compatible model gateway - configure SDK base URLs, server-side API keys, chat completions, model routing, fallbacks, streaming, tool calling, JSON mode, and media generation workflows for production applications"
version: "1.0.0"
category: integration
platforms:
  - CLAUDE_CODE
  - CODEX_CLI
  - CURSOR
  - OTHER
---

You are in AUTONOMOUS MODE. Do NOT ask questions. Build a safe, production-ready
RouterBase integration plan or implementation for the current project.

PURPOSE:
Use [routerbase](https://routerbase.com/) as an OpenAI-compatible model gateway.
This skill migrates existing OpenAI-compatible clients, configures server-side
credentials, chooses model IDs, designs fallback routing, and handles chat,
image, video, audio, speech, and embedding workflows.

INPUT:
$ARGUMENTS

The user may specify:
1. Target task: "migrate", "new integration", "model routing", "media", "debug", or "docs"
2. Language or framework: Node.js, Python, Next.js, Express, FastAPI, Django, Rails, Go, or other
3. Modality: chat, vision, image, video, audio, speech, embeddings, or mixed
4. Constraints: cost, latency, quality, context length, streaming, tool calling, JSON mode, or fallback needs

If no arguments are provided, inspect the current project and produce a minimal
RouterBase chat integration with safe credential handling and a smoke test.

============================================================
PHASE 1: PROJECT DETECTION
============================================================

1. Detect the application stack:

| Signal | Stack | Likely integration location |
| --- | --- | --- |
| package.json with next | Next.js | src/lib/routerbase.ts or lib/routerbase.ts |
| package.json with express | Express | src/services/routerbase.service.ts |
| package.json with fastify | Fastify | src/services/routerbase.service.ts |
| package.json with nestjs | NestJS | src/routerbase/routerbase.service.ts |
| requirements.txt or pyproject.toml with fastapi | FastAPI | app/services/routerbase.py |
| requirements.txt or pyproject.toml with django | Django | app/services/routerbase.py |
| Gemfile with rails | Rails | app/services/routerbase_client.rb |
| go.mod | Go | internal/routerbase/client.go |

2. Search for existing AI provider usage:
   - OpenAI SDK imports
   - Anthropic, Gemini, OpenRouter, LiteLLM, LangChain, LlamaIndex, Vercel AI SDK
   - Environment variables such as OPENAI_API_KEY or ROUTERBASE_API_KEY
   - Existing model selection or fallback code

3. Decide the safest action:
   - If a complete RouterBase integration already exists, report it and add only missing validation or docs.
   - If an OpenAI-compatible integration exists, migrate the base URL and credential names.
   - If no integration exists, create the smallest server-side integration for the detected framework.

============================================================
PHASE 2: CREDENTIAL AND CONFIGURATION SAFETY
============================================================

1. Use `ROUTERBASE_API_KEY` as the credential name.
2. Use `https://routerbase.com/v1` as the base URL.
3. Keep the API key server-side only.
4. Add or update `.env.example` with placeholder values only.
5. Do not print, infer, commit, or log real API keys.
6. If the project has environment validation, add `ROUTERBASE_API_KEY` and any model defaults to the schema.

Recommended environment keys:

```text
ROUTERBASE_API_KEY=
ROUTERBASE_BASE_URL=https://routerbase.com/v1
ROUTERBASE_CHAT_MODEL=google/gemini-2.5-flash
```

============================================================
PHASE 3: SDK INTEGRATION
============================================================

1. Prefer the existing OpenAI-compatible SDK if one is already installed.
2. For JavaScript or TypeScript, use the `openai` package and set `baseURL`.
3. For Python, use the `openai` package and set `base_url`.
4. For other languages, preserve the standard OpenAI-compatible request shape.
5. Create a reusable client module rather than scattering base URLs through the app.

JavaScript pattern:

```js
import OpenAI from "openai";

export const routerbase = new OpenAI({
  apiKey: process.env.ROUTERBASE_API_KEY,
  baseURL: process.env.ROUTERBASE_BASE_URL || "https://routerbase.com/v1",
});
```

Python pattern:

```python
import os
from openai import OpenAI

routerbase = OpenAI(
    api_key=os.environ["ROUTERBASE_API_KEY"],
    base_url=os.environ.get("ROUTERBASE_BASE_URL", "https://routerbase.com/v1"),
)
```

============================================================
PHASE 4: MODEL ROUTING PLAN
============================================================

1. Classify the workload:
   - Chat or agent reasoning
   - Vision or multimodal chat
   - Image generation or editing
   - Video generation
   - Audio or speech generation
   - Embeddings

2. Identify constraints:
   - Quality target
   - Latency budget
   - Price ceiling
   - Context length
   - Streaming requirement
   - Tool calling requirement
   - JSON mode requirement
   - Fallback tolerance

3. Produce a routing table:

| Use case | Primary model | Fallback model | Reason | Validation |
| --- | --- | --- | --- | --- |
| Chat support | model-id | model-id | Balance latency and quality | Run fixture prompts and compare tool or JSON output |

4. Treat model IDs, prices, and availability as live catalog data. If a live
catalog check is not possible, mark the model ID as an example and tell the
user to verify it before production.

============================================================
PHASE 5: FEATURE-SPECIFIC HANDLING
============================================================

Chat completions:
- Use `/chat/completions` through the SDK.
- Keep messages in standard OpenAI-compatible format.
- For streaming, set `stream: true` and verify the client consumes chunks correctly.

Tool calling:
- Keep tool schemas minimal and validated.
- Validate every tool argument before executing application code.
- Do not execute tools from untrusted model output without application-side checks.

JSON mode:
- Use `response_format` only when the selected model supports it.
- Add downstream schema validation.

Media:
- Use image, video, audio, or speech endpoints that match the modality.
- Treat video and some audio jobs as asynchronous.
- Persist task IDs, status, request payload hash, result URLs, and errors.
- Store generated media in durable application storage if it must be reused.

============================================================
PHASE 6: VALIDATION AND ERROR HANDLING
============================================================

1. Add a dry-run or smoke-test command that does not expose secrets.
2. Classify retryable failures conservatively:
   - Retry: network timeouts, transient 429 responses, and 5xx responses.
   - Do not retry blindly: authentication errors, invalid model IDs, validation errors, or policy errors.
3. Add logging that records request type, model ID, latency, status, and retry count without logging prompts, private payloads, generated media URLs, or keys.
4. Add user-facing errors that explain the failure without exposing provider internals.

============================================================
OUTPUT
============================================================

Return:

1. Integration summary
2. Files changed or proposed
3. Environment variables required
4. Model routing table
5. Minimal request example
6. Validation steps
7. Security notes
8. Remaining assumptions, especially live model availability and pricing
