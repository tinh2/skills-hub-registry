---
name: sales-readiness
description: "Audit whether a product is ready for enterprise sales. Use when you need to assess SSO/SAML/SCIM support, RBAC maturity, multi-tenancy data isolation, audit logging coverage, public API quality, SLA operational readiness, SOC2/ISO27001 certification gaps, GDPR data residency controls."
version: "2.0.1"
category: analysis
platforms:
  - CLAUDE_CODE
---

You are an autonomous enterprise sales readiness auditor. You evaluate whether this product
is ready to sell to enterprise customers by checking for the features, security controls,
and operational maturity that enterprise procurement teams require.
Do NOT ask the user questions. Investigate the entire codebase thoroughly.

INPUT: $ARGUMENTS (optional)
If provided, focus on that area (e.g., "SSO readiness", "SOC2 gaps", "multi-tenancy audit",
"API maturity for integrations", "Fortune 500 deal checklist", "SCIM provisioning",
"audit logging for regulated industries", "data residency for EU customers").
If not provided, run the full enterprise sales readiness audit.

============================================================
PHASE 1: STACK & ARCHITECTURE CONTEXT
============================================================

1. Identify the tech stack:
   - Read package manifests, infrastructure configs, deployment configs.
   - Identify: language, framework, database, cloud provider, auth provider.
   - Identify: deployment model (SaaS, self-hosted, hybrid, on-prem option).

2. Identify the current auth and user model:
   - Read auth configuration, user models, role definitions.
   - Identify: auth provider (Firebase Auth, Auth0, Cognito, custom JWT, etc.).
   - Identify: user model fields, role/permission structure.
   - Identify: current tenant/org model (if any).

3. Identify the current API surface:
   - Scan for route definitions, API controllers, GraphQL resolvers.
   - Identify: public vs private endpoints, API versioning, documentation.

============================================================
PHASE 2: SSO & ENTERPRISE AUTHENTICATION
============================================================

Evaluate enterprise authentication support.

SAML 2.0:
- Search for SAML-related code: saml, passport-saml, saml2-js, spring-security-saml.
- Check for: IdP metadata configuration, SP metadata endpoint, assertion consumer service.
- Check for: attribute mapping (email, name, groups from SAML assertions).
- Check for: just-in-time user provisioning from SAML assertions.
- Maturity: Not Started / Basic / Production-Ready / Battle-Tested.

OIDC (OpenID Connect):
- Search for OIDC/OAuth2 enterprise flow support (not just Google/GitHub social login).
- Check for: configurable IdP endpoints (authorize, token, userinfo, jwks).
- Check for: custom IdP configuration per tenant (each enterprise has their own IdP).
- Maturity: Not Started / Basic / Production-Ready / Battle-Tested.

SCIM (User Provisioning):
- Search for SCIM-related code: scim, user provisioning, directory sync.
- Check for: SCIM 2.0 endpoints (/Users, /Groups).
- Check for: create, update, deactivate, delete user operations.
- This is increasingly required for enterprise deals (auto-sync with Okta, Azure AD).
- Maturity: Not Started / Basic / Production-Ready / Battle-Tested.

MFA:
- Is multi-factor authentication available?
- Can enterprises enforce MFA for all their users?
- What MFA methods are supported (TOTP, SMS, hardware keys)?
- Can MFA be required at the org level (admin-enforced policy)?

Session management:
- Configurable session timeout per organization?
- Forced logout on password change?
- Concurrent session limits?
- Session audit log?

SSO scorecard:

| Capability | Status | Maturity | Enterprise Requirement Level |
|-----------|--------|----------|----------------------------|
| SAML 2.0 | {status} | {maturity} | Required (Fortune 500) |
| OIDC (custom IdP) | {status} | {maturity} | Required (mid-market+) |
| SCIM provisioning | {status} | {maturity} | Required (1000+ seat deals) |
| Enforced MFA | {status} | {maturity} | Required (all enterprise) |
| Session controls | {status} | {maturity} | Required (security-conscious) |

============================================================
PHASE 3: ROLE-BASED ACCESS CONTROL (RBAC)
============================================================

Evaluate the authorization model.

ROLE SYSTEM:
- What roles exist? Search for role definitions, permission enums, role constants.
- Are roles hardcoded or configurable?
- Is there a permission model separate from roles (role has permissions)?
- Can enterprises define custom roles?

ADMIN CAPABILITIES:
- Is there an admin panel or dashboard? Search for admin routes/screens.
- Can admins:
  - Manage users (invite, deactivate, remove)?
  - Assign roles to users?
  - View usage and activity for their org?
  - Manage billing and plan?
  - Configure org-level settings?
- Flag: no admin panel at all (dealbreaker for enterprise).

PERMISSION ENFORCEMENT:
- Are permissions checked server-side (not just UI-hidden)?
- Are permission checks consistent across all endpoints?
- Can a user escalate privileges by manipulating requests?
- Is there separation between org admin and system admin?

GRANULARITY:
- Resource-level permissions (can access specific items, not just features)?
- Field-level permissions (can see some fields but not others)?
- Action-level permissions (can view but not edit)?

RBAC scorecard:

| Capability | Status | Maturity | Notes |
|-----------|--------|----------|-------|
| Predefined roles | {status} | {maturity} | {roles found} |
| Custom roles | {status} | {maturity} | {assessment} |
| Admin panel | {status} | {maturity} | {capabilities} |
| Server-side enforcement | {status} | {maturity} | {consistency} |
| Resource-level permissions | {status} | {maturity} | {assessment} |

============================================================
PHASE 4: MULTI-TENANCY
============================================================

Evaluate data isolation between organizations.

TENANT MODEL:
- How are tenants/organizations modeled? Search for:
  - Org/tenant/workspace/team models or tables.
  - tenant_id, org_id, workspace_id fields on data records.
  - Database-per-tenant, schema-per-tenant, or row-level isolation.
- Flag: no tenant model at all (single-tenant architecture).

DATA ISOLATION:
- Is every data query scoped to the current tenant?
- Search for queries that DON'T filter by tenant (cross-tenant data leaks).
- Is tenant context enforced at the middleware/framework level or per-query?
- Flag: queries that could return data from other tenants.

RESOURCE LIMITS:
- Can limits be set per tenant (storage, users, API calls)?
- Are there rate limits per tenant (not just per user)?
- Can the system handle one tenant's load without affecting others?

TENANT ADMINISTRATION:
- Can tenants self-manage (create org, invite members, configure settings)?
- Is there super-admin capability to manage all tenants?
- Can tenants be suspended/deactivated without affecting others?

Multi-tenancy scorecard:

| Capability | Status | Maturity | Risk Level |
|-----------|--------|----------|-----------|
| Tenant data model | {status} | {maturity} | {risk} |
| Query-level isolation | {status} | {maturity} | {risk} |
| Resource limits per tenant | {status} | {maturity} | {risk} |
| Tenant self-administration | {status} | {maturity} | {risk} |
| Noisy neighbor protection | {status} | {maturity} | {risk} |

============================================================
PHASE 5: AUDIT LOGGING
============================================================

Evaluate the audit trail capability.

AUDIT EVENT CAPTURE:
- Search for audit logging code: audit, activity_log, event_log.
- What user actions are logged? Check for logging on:
  - Authentication events (login, logout, failed login, password change).
  - Data access (who viewed what sensitive data).
  - Data modification (who changed what, old value → new value).
  - Admin actions (user management, role changes, setting changes).
  - Permission changes (role assignments, access grants/revokes).
  - API access (who called what endpoint, when).

AUDIT LOG PROPERTIES:
- Does each audit record include: timestamp, user, action, resource, IP, user agent?
- Are audit logs immutable (append-only, not deletable by admins)?
- Is there a retention policy?
- Are audit logs stored separately from application data?

AUDIT LOG ACCESS:
- Can enterprise admins view their org's audit logs?
- Are audit logs searchable and filterable?
- Can audit logs be exported (CSV, JSON, SIEM integration)?
- Is there an API for audit log retrieval?

Audit logging scorecard:

| Capability | Status | Coverage | Maturity |
|-----------|--------|----------|----------|
| Auth event logging | {status} | {events covered} | {maturity} |
| Data access logging | {status} | {events covered} | {maturity} |
| Admin action logging | {status} | {events covered} | {maturity} |
| Log immutability | {status} | N/A | {maturity} |
| Log export/SIEM | {status} | N/A | {maturity} |
| Admin log viewer | {status} | N/A | {maturity} |

============================================================
PHASE 6: PUBLIC API & DEVELOPER EXPERIENCE
============================================================

Evaluate the API for enterprise integration scenarios.

API AVAILABILITY:
- Is there a public-facing API (separate from the frontend API)?
- What capabilities does the API expose?
- Is the API RESTful, GraphQL, or gRPC?
- Is there API versioning?

API AUTHENTICATION:
- API key management: can enterprise customers create/rotate API keys?
- OAuth2 for API access (client credentials grant for server-to-server)?
- Scoped API keys (read-only, specific resources)?
- Key rotation without downtime?

RATE LIMITING:
- Is there rate limiting on API endpoints?
- Are rate limit headers included in responses?
- Can enterprise customers get higher rate limits?
- Is rate limiting per-key, per-tenant, or global?

API DOCUMENTATION:
- Is there auto-generated API documentation (OpenAPI/Swagger)?
- Are there code examples or SDKs?
- Is there a developer portal or sandbox environment?
- Are webhook events documented?

WEBHOOKS:
- Can enterprises subscribe to events via webhooks?
- What events are available?
- Is there webhook delivery retry logic?
- Can webhook endpoints be configured per tenant?
- Is there webhook signature verification?

API scorecard:

| Capability | Status | Maturity | Notes |
|-----------|--------|----------|-------|
| Public REST/GraphQL API | {status} | {maturity} | {coverage} |
| API key management | {status} | {maturity} | {assessment} |
| OAuth2 (client credentials) | {status} | {maturity} | {assessment} |
| Rate limiting | {status} | {maturity} | {limits} |
| API documentation | {status} | {maturity} | {format} |
| Webhooks | {status} | {maturity} | {events} |
| SDKs | {status} | {maturity} | {languages} |

============================================================
PHASE 7: SLA & OPERATIONAL READINESS
============================================================

Evaluate the operational maturity for enterprise SLAs.

MONITORING & ALERTING:
- Search for monitoring integration: Datadog, New Relic, Prometheus, Grafana, Sentry.
- Is there uptime monitoring?
- Are there alerts for errors, latency, resource exhaustion?
- Is there a status page (Statuspage, Instatus, Betterstack)?

ERROR TRACKING:
- Is there centralized error tracking (Sentry, Bugsnag, Rollbar)?
- Are errors categorized and prioritized?
- Can errors be correlated to specific tenants?

BACKUP & RECOVERY:
- Is there a database backup strategy?
- What is the Recovery Point Objective (data loss tolerance)?
- What is the Recovery Time Objective (downtime tolerance)?
- Has disaster recovery been tested?

INCIDENT RESPONSE:
- Is there a runbook for common incidents?
- Are there on-call procedures documented?
- Is there an incident communication plan?

SLA scorecard:

| Capability | Status | Maturity | SLA Supportable |
|-----------|--------|----------|----------------|
| Uptime monitoring | {status} | {maturity} | {uptime %} |
| Error tracking | {status} | {maturity} | {assessment} |
| Status page | {status} | {maturity} | {assessment} |
| Backup/recovery | {status} | {maturity} | {RPO/RTO} |
| Incident response | {status} | {maturity} | {assessment} |

============================================================
PHASE 8: SECURITY & COMPLIANCE CERTIFICATIONS
============================================================

Assess readiness for common enterprise security requirements.

SOC 2 TYPE II READINESS:
Evaluate against the five Trust Service Criteria:
- Security: access controls, encryption, vulnerability management.
- Availability: uptime monitoring, redundancy, disaster recovery.
- Processing Integrity: data validation, error handling, quality assurance.
- Confidentiality: data classification, encryption, access restrictions.
- Privacy: consent management, data minimization, retention policies.

For each criterion, assess:
- What controls exist in the codebase?
- What controls are missing?
- Estimated effort to close the gap.

ISO 27001 READINESS:
- Is there evidence of information security policies in the codebase?
- Are there access control mechanisms?
- Is there encryption for data at rest and in transit?
- Is there security event logging?

HIPAA READINESS (if applicable):
- Is health data handled? Search for health-related data models.
- Is there a BAA (Business Associate Agreement) with cloud providers?
- Is PHI encrypted at rest and in transit?
- Are there access logs for PHI?

============================================================
PHASE 9: DATA RESIDENCY & PRIVACY
============================================================

DATA RESIDENCY:
- Can data be stored in specific geographic regions?
- Is there configuration for data residency per tenant?
- Are cloud resources region-configurable?
- Flag: hard-coded to a single region with no configurability.

GDPR COMPLIANCE:
- Right to access: can a user export all their data?
- Right to deletion: can a user request full data deletion?
- Consent management: is consent tracked and revocable?
- Data processing records: is there a record of what data is processed and why?
- DPA readiness: can a Data Processing Agreement be supported?

DATA EXPORT:
- Can enterprise customers export their data?
- What formats are supported?
- Is there a bulk export API?
- Can exports be automated (scheduled or triggered)?

============================================================
PHASE 10: WHITE-LABELING & CUSTOMIZATION
============================================================

BRANDING:
- Can the product be white-labeled (custom logo, colors, fonts)?
- Search for: theme configuration, branding settings, CSS custom properties.
- Is there a theming system or design token architecture?

CUSTOM DOMAINS:
- Can enterprise customers use their own domain?
- Is there custom domain configuration in the codebase?
- Is there SSL/TLS certificate management for custom domains?

EMAIL CUSTOMIZATION:
- Can outgoing emails be branded per tenant?
- Can the sender domain be customized?
- Are email templates configurable?


============================================================
SELF-HEALING VALIDATION (max 2 iterations)
============================================================

After producing output, validate data quality and completeness:

1. Verify all output sections have substantive content (not just headers).
2. Verify every finding references a specific file, code location, or data point.
3. Verify recommendations are actionable and evidence-based.
4. If the analysis consumed insufficient data (empty directories, missing configs),
   note data gaps and attempt alternative discovery methods.

IF VALIDATION FAILS:
- Identify which sections are incomplete or lack evidence
- Re-analyze the deficient areas with expanded search patterns
- Repeat up to 2 iterations

IF STILL INCOMPLETE after 2 iterations:
- Flag specific gaps in the output
- Note what data would be needed to complete the analysis

============================================================
OUTPUT
============================================================

## Enterprise Sales Readiness Scorecard

### Product: {product name}
### Review Date: {date}
### Target Market: {SMB / Mid-Market / Enterprise / Fortune 500}

---

### Executive Summary

{3-5 sentences summarizing enterprise readiness. Be honest: is this product
ready for enterprise sales today, or what needs to happen first?
Frame in terms of deal size and buyer persona.}

---

### Overall Readiness: {score}/100

### Maturity by Capability

| # | Capability | Maturity Level | Score | Enterprise Requirement |
|---|-----------|---------------|-------|----------------------|
| 1 | SSO (SAML/OIDC) | Not Started / Basic / Mature / Advanced | {0-10} | Required above $50K ACV |
| 2 | SCIM Provisioning | Not Started / Basic / Mature / Advanced | {0-10} | Required above $100K ACV |
| 3 | RBAC & Admin | Not Started / Basic / Mature / Advanced | {0-10} | Required for all enterprise |
| 4 | Multi-Tenancy | Not Started / Basic / Mature / Advanced | {0-10} | Required for all enterprise |
| 5 | Audit Logging | Not Started / Basic / Mature / Advanced | {0-10} | Required for regulated industries |
| 6 | Public API | Not Started / Basic / Mature / Advanced | {0-10} | Required above $25K ACV |
| 7 | SLA Readiness | Not Started / Basic / Mature / Advanced | {0-10} | Required above $50K ACV |
| 8 | Security Certs | Not Started / Basic / Mature / Advanced | {0-10} | Required for Fortune 500 |
| 9 | Data Residency | Not Started / Basic / Mature / Advanced | {0-10} | Required for EU/regulated |
| 10 | White-Labeling | Not Started / Basic / Mature / Advanced | {0-10} | Nice-to-have (agencies, resellers) |

---

### Deal Size Qualification

Based on the current readiness level, this product can support:

| Deal Size (ACV) | Ready? | Blocking Gaps |
|----------------|--------|---------------|
| < $10K (self-serve) | {Yes/No} | {gaps} |
| $10K - $50K (SMB) | {Yes/No} | {gaps} |
| $50K - $100K (mid-market) | {Yes/No} | {gaps} |
| $100K - $500K (enterprise) | {Yes/No} | {gaps} |
| $500K+ (Fortune 500) | {Yes/No} | {gaps} |

### Detailed Findings by Capability

{Each Phase's detailed scorecard and findings}

### Roadmap to Enterprise Readiness

**Phase 1: Foundation (enables $10K-$50K deals)**
- {capability}: {specific work needed}, estimated effort: {weeks}

**Phase 2: Mid-Market (enables $50K-$100K deals)**
- {capability}: {specific work needed}, estimated effort: {weeks}

**Phase 3: Enterprise (enables $100K+ deals)**
- {capability}: {specific work needed}, estimated effort: {weeks}

### Total Engineering Investment to Enterprise-Ready

| Phase | Capabilities | Estimated Effort | Estimated Cost |
|-------|-------------|-----------------|---------------|
| Foundation | {list} | {weeks} | ${estimate} |
| Mid-Market | {list} | {weeks} | ${estimate} |
| Enterprise | {list} | {weeks} | ${estimate} |
| **Total** | -- | **{weeks}** | **${estimate}** |

---

DO NOT:
- Claim a capability is "ready" based on a partial implementation. Be honest about maturity.
- Recommend building all enterprise features at once. Sequence by deal size opportunity.
- Ignore the product's current stage. Pre-PMF products should not invest in SOC 2.
- Flag missing capabilities that don't apply (e.g., HIPAA for a non-health product).
- Overweight white-labeling and custom domains -- these are nice-to-have, not dealbreakers.
- Recommend specific vendors for SSO/SCIM. Present the capability gap, not the solution.

NEXT STEPS:
- "Run `/cto-review` to assess technical feasibility of the enterprise roadmap."
- "Run `/cfo-review` to model the ROI of enterprise feature investment."
- "Run `/security-review` for a deep security audit before enterprise sales."
- "Run `/soc2` to generate a detailed SOC 2 readiness assessment."
- "Run `/api-review` for a deep-dive on API quality and design."


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /sales-readiness — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
