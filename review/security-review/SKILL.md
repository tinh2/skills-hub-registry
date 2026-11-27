---
name: security-review
description: "Evidence-based security audit of a codebase: auth and authz gaps, IDOR, JWT/OAuth flaws, injection, data exposure, secrets and session issues, with exploit scenarios and fixes. Triggers: security review, audit auth, find vulnerabilities."
version: "2.1.0"
category: review
platforms:
  - CLAUDE_CODE
---

Audit the codebase for exploitable security flaws and report each with evidence, an exploit scenario and a concrete fix. Work autonomously; investigate rather than ask.

**Scope:** `$ARGUMENTS` if given (e.g. "changed files only", "auth module"); otherwise the whole codebase.

## Approach

1. **Map the attack surface.** Detect the stack from manifests, then enumerate HTTP routes, WebSocket handlers, serverless functions, upload endpoints, DB query sites, outbound requests, admin routes and webhook receivers. Identify the auth provider, where checks run (middleware, guard, inline) and the role model.
2. **Audit each area below.** Report only what the code actually shows.
3. **Check your report** before finishing: every finding has `file:line`, a believable exploit and a specific fix, and severities match the evidence.

## What to check

**Authentication**

- Every route that reads or changes data has an auth check; pay attention to admin, export, webhook (signature verification) and health endpoints that expose internal state.
- JWT: `alg: none` / algorithm confusion, missing `exp`/`aud`/`iss` checks, weak secrets (<256 bits).
- OAuth: `state` validation, exact redirect URI matching, PKCE.
- API keys: validated per request, scoped, rotatable.
- Flows: password reset tokens expire and are single-use; login is rate-limited; MFA can't be skipped; registration can't set a role; email verification is enforced where it matters.

**Authorization**

- IDOR: every by-ID resource access (`/orders/:id`) verifies ownership or tenancy. This is the most common real bug.
- Role checks happen server-side, not just in the UI; request bodies can't set `role`/`isAdmin`.
- Revoked permissions, deactivated accounts and scoped keys actually lose access.
- Firebase/Firestore/Supabase rules: ownership enforced, no `allow ... if true`.

**Injection**

- SQL: string-built queries and raw-query escape hatches in ORMs.
- NoSQL: user input reaching operators (`$where`, `$regex`, `$gt`), prototype pollution.
- XSS: `dangerouslySetInnerHTML`, `v-html`, `[innerHTML]`, unescaped stored values, reflected URL params.
- Command injection (`exec`, `spawn` with shell, `subprocess(shell=True)`), path traversal on user paths and upload names, SSRF on user-supplied URLs (block private ranges, metadata IPs, redirects).

**Data exposure**

- PII, tokens or request bodies in logs.
- Stack traces, SQL errors or internal paths in client responses.
- Over-fetching: whole DB rows returned, password hashes or admin flags in responses, open GraphQL introspection.
- Debug endpoints, `X-Powered-By`, public `.env`/`.git`.

**Secrets**

- Hardcoded keys (`sk_live_`, `AKIA`, `ghp_`, private key blocks, credentialed connection strings), committed `.env`, real values in `.env.example`.
- `.gitignore` gaps (`.env`, `*.pem`, `*.key`, service-account JSON). Secrets in git history need rotation, not just deletion.

**Sessions and transport**

- Session ID regenerated on login; cookies `Secure`/`HttpOnly`/`SameSite`; idle and absolute timeouts; CSRF protection on cookie-authenticated mutations.
- HTTPS redirect and HSTS; CORS doesn't allow `*` (or reflected origins) with credentials on authenticated routes.

**Don't report:** theoretical issues without code evidence, missing browser headers on non-web backends, or "missing auth" on intentionally public endpoints (login, register, health). Don't skip client-side issues just because a backend exists.

## Output

```
## Security Review Report
### Stack: … | Scope: … | Attack surface: N endpoints, N query sites, N integrations

| Severity | Count |   (Critical / High / Medium / Low)

### Critical Findings
1. **VULN-001: title**
   - Category: Authentication | Authorization | Injection | Exposure | Secrets | Session
   - Location: `file:line`
   - Description
   - Exploit scenario
   - Fix: the specific code change
### High / Medium / Low Findings (same format)

### Auth Coverage Matrix
| Endpoint | Method | Auth Required | Auth Check Present | Ownership Check | Status |

### Secrets Scan
- Hardcoded secrets: n | .gitignore gaps: … | Rotate: …

### Security Score: N/100
```

Suggest follow-ups where useful: `/iterate` to fix critical and high findings, `/owasp` for a full Top 10 pass, `/pentest` for attack scenarios.

## Telemetry

If a project memory directory exists under `~/.claude/projects/`, append to its `skill-telemetry.md` (skip silently otherwise):

```
### /security-review — YYYY-MM-DD
- Outcome: SUCCESS | PARTIAL | FAILED
- Self-healed: yes (what) | no
- Bottleneck: phase that struggled, or none
- Suggestion: one-line improvement, or none
```
