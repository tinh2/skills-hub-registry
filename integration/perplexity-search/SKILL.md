---
name: perplexity-search
description: AI-powered web search and research using the Perplexity API (Sonar models). Performs deep web research with citations, fact-checking, competitive analysis, market research, and technical documentation lookup. Supports streaming responses, search domain filtering, and recency filtering.
version: 1.0.0
category: integration
platforms:
  - CLAUDE_CODE
  - CURSOR
permissions:
  - network
  - api
---

# Perplexity Search

Use the Perplexity API for AI-powered web search and research. Perplexity's Sonar models combine large language models with real-time web search to provide accurate, cited answers.

## Prerequisites

- `PERPLEXITY_API_KEY` environment variable set
- Get your API key at: https://www.perplexity.ai/settings/api

## API Reference

### Basic Search

```bash
curl -s https://api.perplexity.ai/chat/completions \
  -H "Authorization: Bearer $PERPLEXITY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "sonar",
    "messages": [
      {"role": "user", "content": "What are the latest React 19 features?"}
    ]
  }' | jq '.choices[0].message.content'
```

### Models

| Model | Best For | Context |
|-------|----------|---------|
| `sonar` | General web search, quick answers | 128K |
| `sonar-pro` | Complex research, multi-step reasoning | 200K |
| `sonar-reasoning` | Deep analysis with chain-of-thought | 128K |
| `sonar-reasoning-pro` | Most thorough research and reasoning | 128K |
| `sonar-deep-research` | Comprehensive multi-source deep dives | 128K |

### Search with Citations

```python
import requests
import os

def perplexity_search(query: str, model: str = "sonar") -> dict:
    """Search the web using Perplexity API."""
    response = requests.post(
        "https://api.perplexity.ai/chat/completions",
        headers={
            "Authorization": f"Bearer {os.environ['PERPLEXITY_API_KEY']}",
            "Content-Type": "application/json",
        },
        json={
            "model": model,
            "messages": [{"role": "user", "content": query}],
        },
    )
    data = response.json()
    return {
        "answer": data["choices"][0]["message"]["content"],
        "citations": data.get("citations", []),
    }

result = perplexity_search("What are the best practices for Next.js 15 App Router?")
print(result["answer"])
for i, url in enumerate(result["citations"], 1):
    print(f"[{i}] {url}")
```

### TypeScript/Node.js

```typescript
import OpenAI from "openai";

const perplexity = new OpenAI({
  apiKey: process.env.PERPLEXITY_API_KEY,
  baseURL: "https://api.perplexity.ai",
});

async function search(query: string, model = "sonar") {
  const response = await perplexity.chat.completions.create({
    model,
    messages: [{ role: "user", content: query }],
  });

  return {
    answer: response.choices[0].message.content,
    citations: (response as any).citations ?? [],
  };
}
```

### Advanced Options

```python
response = requests.post(
    "https://api.perplexity.ai/chat/completions",
    headers={
        "Authorization": f"Bearer {os.environ['PERPLEXITY_API_KEY']}",
        "Content-Type": "application/json",
    },
    json={
        "model": "sonar-pro",
        "messages": [
            {
                "role": "system",
                "content": "You are a technical researcher. Provide detailed, accurate answers with specific version numbers and code examples."
            },
            {
                "role": "user",
                "content": "Compare Bun vs Deno vs Node.js performance benchmarks in 2025"
            }
        ],
        # Filter to specific domains
        "search_domain_filter": ["github.com", "stackoverflow.com", "dev.to"],
        # Only recent results
        "search_recency_filter": "month",  # day, week, month
        # Temperature for response generation
        "temperature": 0.2,
        # Return related follow-up questions
        "return_related_questions": True,
    },
)
```

### Streaming Responses

```python
import requests
import json

response = requests.post(
    "https://api.perplexity.ai/chat/completions",
    headers={
        "Authorization": f"Bearer {os.environ['PERPLEXITY_API_KEY']}",
        "Content-Type": "application/json",
    },
    json={
        "model": "sonar",
        "messages": [{"role": "user", "content": "Latest TypeScript 5.5 features"}],
        "stream": True,
    },
    stream=True,
)

for line in response.iter_lines():
    if line:
        data = line.decode("utf-8").removeprefix("data: ")
        if data == "[DONE]":
            break
        chunk = json.loads(data)
        content = chunk["choices"][0]["delta"].get("content", "")
        if content:
            print(content, end="", flush=True)
```

## Use Cases

### Competitive Analysis

```python
result = perplexity_search(
    "What are the main competitors to Stripe for payment processing? "
    "Compare pricing, features, and market share as of 2025.",
    model="sonar-pro"
)
```

### Technical Research

```python
result = perplexity_search(
    "What are the security best practices for JWT token handling "
    "in Node.js applications? Include recent CVEs and vulnerabilities.",
    model="sonar-reasoning"
)
```

### Market Research

```python
result = perplexity_search(
    "What is the current market size for AI code assistants? "
    "Include growth projections and key players.",
    model="sonar-deep-research"
)
```

### Fact-Checking

```python
result = perplexity_search(
    "Is it true that React Server Components eliminate the need "
    "for getServerSideProps in Next.js? Explain with citations.",
    model="sonar"
)
```

## MCP Server Integration

For direct Claude Code integration, use the official Perplexity MCP server:

```bash
# Install via Homebrew
brew install perplexityai/tap/pplx-mcp

# Or via Go
go install github.com/perplexityai/modelcontextprotocol/cmd/pplx-mcp@latest
```

Add to Claude Code MCP config:
```json
{
  "mcpServers": {
    "perplexity": {
      "command": "pplx-mcp",
      "env": {
        "PERPLEXITY_API_KEY": "pplx-..."
      }
    }
  }
}
```

Source: [Perplexity API Docs](https://docs.perplexity.ai), [perplexityai/modelcontextprotocol](https://github.com/perplexityai/modelcontextprotocol)
