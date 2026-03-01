# Integration

Third-party service connectors -- authentication, payments, email, push notifications, search, storage, realtime, and analytics.

## Main Skill

**[integrate](integrate/)** -- Master integration orchestrator that audits existing integrations, identifies gaps, routes to sub-skills, and produces an integration health score for production readiness.

## Skills (9)

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
