# Integration

Third-party service connectors -- authentication, payments, email, push notifications, search, storage, realtime, and analytics.

## Main Skill

**[integrate](integrate/)** -- Master integration orchestrator that audits existing integrations, identifies gaps, routes to sub-skills, and produces an integration health score for production readiness.

## Skills (14)

| Skill | Version | Description |
|-------|---------|-------------|
| [integrate](integrate/) | 1.0.0 | Main orchestrator. Audits existing integrations, routes to sub-skills, produces integration health score |
| [auth-provider](auth-provider/) | 1.0.0 | Sets up complete OAuth/SSO authentication with provider configuration, session management, and login UI |
| [stripe](stripe/) | 1.0.0 | Sets up complete Stripe payment integration with checkout sessions, webhooks, and subscription billing |
| [email](email/) | 1.0.0 | Sets up transactional email with provider SDK, templated messages, delivery tracking, and webhook handling |
| [push-notifications](push-notifications/) | 1.0.0 | Sets up mobile and web push notifications with FCM, APNs, or OneSignal including deep linking |
| [search](search/) | 1.0.0 | Sets up full-text search with indexing, search UI, and ranking -- supports Algolia, Typesense, Meilisearch, Elasticsearch |
| [storage](storage/) | 1.0.0 | Sets up object storage with upload, download, presigned URLs, and CDN integration -- supports S3, GCS, R2, Supabase |
| [realtime](realtime/) | 1.0.0 | Sets up WebSocket or SSE-based realtime communication with channels, presence, and offline handling |
| [analytics-tracking](analytics-tracking/) | 1.0.0 | Sets up event tracking with analytics providers -- auto-detects framework, installs SDK, and instruments key flows |

## Usage

- Full integration audit and gap analysis: `/integrate`
- Set up OAuth/SSO authentication: `/auth-provider`
- Set up Stripe payments and subscriptions: `/stripe`
- Set up transactional email: `/email`
- Set up push notifications: `/push-notifications`
- Set up full-text search: `/search`
- Set up object storage: `/storage`
- Set up realtime communication: `/realtime`
- Set up analytics tracking: `/analytics-tracking`

## Recently Added

| Skill | Version | Description |
|-------|---------|-------------|
| [perplexity-search](perplexity-search/) | 1.0.0 | AI-powered web search and research using the Perplexity API (Sonar models). Performs deep web research with citations, fact-checking, competitive analysis, market research, and... |
| [stitch-bridge](stitch-bridge/) | 1.0.0 | >- |
| [stitch-compare](stitch-compare/) | 1.0.0 | >- |
| [stitch-explore](stitch-explore/) | 1.0.0 | >- |
| [x-mcp](x-mcp/) | 2.0.0 | Safely connects X (formerly Twitter) data through MCP, preserves existing providers, discloses data flow, and runs bounded workflows |

<!-- BEGIN GENERATED: skills-hub-index (scripts/gen-index.mjs, do not edit by hand) -->
## All Integration skills on skills-hub.ai

Each skill page on skills-hub.ai shows ratings and reviews, install counts, a one-command install, and related skills. 27 of 27 skills in this folder have a page. You can also [browse the Integration category on skills-hub.ai](https://skills-hub.ai/browse?category=integration), which includes skills from other publishers.

| Skill | Description | Page |
|-------|-------------|------|
| [acp-agent-setup](acp-agent-setup/) | Configure your development environment for Agent Client Protocol (ACP) Spec 1.0 — registers Claude Code, Codex, Devin Local, and... | [View on skills-hub](https://skills-hub.ai/skills/acp-agent-setup) |
| [analytics-tracking](analytics-tracking/) | Set up production-ready event tracking with Amplitude, Mixpanel, PostHog, or GA4. | [View on skills-hub](https://skills-hub.ai/skills/analytics-tracking) |
| [antigravity-sdk](antigravity-sdk/) | Scaffold, configure, and deploy custom AI agents with the Google Antigravity 2.0 SDK and agy CLI. | [View on skills-hub](https://skills-hub.ai/skills/antigravity-sdk) |
| [auth-provider](auth-provider/) | Set up complete OAuth/SSO authentication with Google, GitHub, Apple, or SAML providers. | [View on skills-hub](https://skills-hub.ai/skills/auth-provider) |
| [codex-bedrock](codex-bedrock/) | Sets up and optimizes OpenAI Codex CLI + GPT-5.5 on Amazon Bedrock (GA June 2026). | [View on skills-hub](https://skills-hub.ai/skills/codex-bedrock) |
| [copilot-model-routing](copilot-model-routing/) | Intelligent task-to-model routing for GitHub Copilot's multi-lab model picker (2026). | [View on skills-hub](https://skills-hub.ai/skills/copilot-model-routing) |
| [email](email/) | Add transactional email to my app — set up Resend, SendGrid, SES, Postmark, or Mailgun with HTML templates for welcome, password reset,... | [View on skills-hub](https://skills-hub.ai/skills/email) |
| [figma-mcp](figma-mcp/) | Connect the Figma Dev Mode MCP server to your AI coding agent and implement designs against your real component library. | [View on skills-hub](https://skills-hub.ai/skills/figma-mcp) |
| [gemini-cli-migration](gemini-cli-migration/) | Migrate Gemini CLI workflows to a new AI coding tool (Claude Code, Antigravity CLI, or Codex CLI). | [View on skills-hub](https://skills-hub.ai/skills/gemini-cli-migration) |
| [integrate](integrate/) | Audit my project's third-party integrations or set up multiple at once — scans for payments, auth, email, push, analytics, storage,... | [View on skills-hub](https://skills-hub.ai/skills/integrate) |
| [kiro-custom-agent](kiro-custom-agent/) | Design, configure, and iterate on custom Kiro agents using the 1.0 Markdown agent format. | [View on skills-hub](https://skills-hub.ai/skills/kiro-custom-agent) |
| [kiro-headless-ci](kiro-headless-ci/) | Wire Kiro CLI into CI/CD pipelines using headless mode. | [View on skills-hub](https://skills-hub.ai/skills/kiro-headless-ci) |
| [mcp-apps-builder](mcp-apps-builder/) | Build MCP Apps — the interactive HTML UI primitive introduced in the 2026-07-28 MCP specification. | [View on skills-hub](https://skills-hub.ai/skills/mcp-apps-builder) |
| [mcp-enterprise-auth](mcp-enterprise-auth/) | Audit and configure enterprise-managed MCP authorization (EMA) for organizations using Okta and Claude Team/Enterprise. | [View on skills-hub](https://skills-hub.ai/skills/mcp-enterprise-auth) |
| [mcp-protocol-migration](mcp-protocol-migration/) | Migrates an MCP server from the original session-oriented protocol to the 2026 stateless spec (finalising July 28, 2026). | [View on skills-hub](https://skills-hub.ai/skills/mcp-protocol-migration) |
| [north-mini-code](north-mini-code/) | Wires Cohere's North Mini Code 1.0 (30B MoE, Apache 2.0) into your coding workflow: detects your hardware tier, selects the right... | [View on skills-hub](https://skills-hub.ai/skills/north-mini-code) |
| [opencode-model-router](opencode-model-router/) | Sets up and optimises an OpenCode terminal-agent project: installs the CLI, configures multi-provider routing (Claude for hard tasks,... | [View on skills-hub](https://skills-hub.ai/skills/opencode-model-router) |
| [perplexity-search](perplexity-search/) | AI-powered web search and research using the Perplexity API (Sonar models). | [View on skills-hub](https://skills-hub.ai/skills/perplexity-search) |
| [push-notifications](push-notifications/) | Add push notifications to my app — set up FCM, APNs, or OneSignal for Flutter, React Native, Expo, or web with permission flows,... | [View on skills-hub](https://skills-hub.ai/skills/push-notifications) |
| [realtime](realtime/) | Add realtime features to my app — set up WebSockets or SSE with Socket.io, Pusher, Ably, Supabase Realtime, or Firebase using channels,... | [View on skills-hub](https://skills-hub.ai/skills/realtime) |
| [search](search/) | Add full-text search to my app — set up Algolia, Meilisearch, Typesense, or Elasticsearch with index configuration, typo tolerance,... | [View on skills-hub](https://skills-hub.ai/skills/search) |
| [stitch-bridge](stitch-bridge/) | Bidirectional sync between your codebase and Google Stitch. | [View on skills-hub](https://skills-hub.ai/skills/stitch-bridge) |
| [stitch-compare](stitch-compare/) | Side-by-side comparison of your current design against Stitch variations. | [View on skills-hub](https://skills-hub.ai/skills/stitch-compare) |
| [stitch-explore](stitch-explore/) | Generate design alternatives in Google Stitch with constraints. | [View on skills-hub](https://skills-hub.ai/skills/stitch-explore) |
| [storage](storage/) | Add file uploads and object storage to my app — set up AWS S3, Google Cloud Storage, Cloudflare R2, or Supabase Storage with presigned... | [View on skills-hub](https://skills-hub.ai/skills/storage) |
| [stripe](stripe/) | Add Stripe payments to my app — set up checkout sessions, payment intents, webhook handling with signature verification, subscription... | [View on skills-hub](https://skills-hub.ai/skills/stripe) |
| [x-mcp](x-mcp/) | Safely connect X (formerly Twitter) data to Claude Code, Codex, Cursor, or Windsurf through MCP. | [View on skills-hub](https://skills-hub.ai/skills/x-mcp) |
<!-- END GENERATED: skills-hub-index -->
