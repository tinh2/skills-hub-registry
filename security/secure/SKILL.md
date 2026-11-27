---
name: secure
description: "Read-only full-stack security posture assessment with a 0-100 risk score: dependency CVEs, dangerous code patterns, auth gaps, config and secrets, PII handling; routes to deeper skills. Triggers: 'security posture', 'how secure is this', 'security scan', 'risk score'."
version: "2.1.0"
category: security
platforms:
  - CLAUDE_CODE
---

Assess the security posture of `$ARGUMENTS` (default: the project in the current directory) and produce a scored report. This is assessment only: don't modify code, don't run attacks against live systems, don't install scanners (use what is already available), and redact any secret you find.

## What to check

Detect the stack first (package manifests, Dockerfiles, `firebase.json`, `serverless.yml`, IaC) and adapt every check to it.

**Dependencies.** Run whichever applies: `npm audit --json` / `pnpm audit --json` / `yarn npm audit`, `pip-audit -f json`, `cargo audit --json`, `govulncheck ./...`, `bundle audit`, OSV-Scanner if installed. For each vulnerable package record version, CVE/GHSA ID, severity, whether a fixed version exists, and whether the vulnerable code path is plausibly reachable.

**Code patterns.**

- Injection: SQL/NoSQL built by string concatenation or interpolation; `eval`/`Function`/`exec` on dynamic input; shell execution with user input (`child_process.exec`, `os.system`, `subprocess(..., shell=True)`); ReDoS-prone regexes on user input; SSRF (server fetches of user-supplied URLs); path traversal in file access; unsafe deserialization (`pickle`, YAML `load`).
- XSS: `innerHTML`, `dangerouslySetInnerHTML`, `v-html`, `document.write`, templates with escaping disabled.
- Auth: routes missing auth middleware, and authorization gaps (handlers that load a record by ID without checking the caller owns it), missing CSRF on cookie-authenticated state changes, hardcoded JWT secrets, JWTs accepted without signature/`alg` checks, sessions without secure flags.
- Crypto: MD5/SHA-1/unsalted hashes for passwords (expect bcrypt/scrypt/argon2), `Math.random()` for tokens, hardcoded keys or IVs.

**Configuration.**

- Secrets: committed `.env` files, keys/tokens/private keys/credentialed connection strings in source or git history (`git log -p -S` on suspicious names, or gitleaks/trufflehog if present).
- Debug: debug mode or dev env in production config, stack traces in error responses, sensitive data in logs, public source maps.
- HTTP: wildcard CORS with credentials or on private APIs; missing CSP (including `frame-ancestors`), HSTS, `X-Content-Type-Options`; cookies without `Secure`/`HttpOnly`/`SameSite`.
- Infrastructure: containers running as root, internal services exposed on public ports, default database credentials, overly broad IAM/Firebase/Supabase rules.

**Data handling.** PII in logs, error messages or URLs; PII stored unencrypted where it matters; missing input validation at API boundaries; uploads without type/size limits; no rate limiting on login, signup, password reset or other expensive endpoints.

Read each flagged line in context before reporting it. Give each finding a file:line and a confidence level, and mark anything unconfirmed as such.

## Risk score

0-100, lower is better: +15 per Critical, +8 per High, +3 per Medium, +1 per Low, capped at 100. Levels: 0-15 EXCELLENT, 16-35 GOOD, 36-60 MODERATE, 61-80 HIGH, 81-100 CRITICAL.

## Report

```
## Security Posture Report

**Project:** name
**Stack:** detected technologies
**Risk Score:** N/100 (LEVEL)
**Scan Date:** YYYY-MM-DD

### Summary
| Severity | Count | Auto-Fixable |
|---|---|---|
| Critical | N | N |
| High | N | N |
| Medium | N | N |
| Low | N | N |

### Critical Findings (fix immediately)
- file:line: description, impact, recommended fix, confidence

### High Findings
### Medium Findings
### Low Findings
### Dependency Vulnerabilities (table: package, version, CVE, severity, fixed in)
### Configuration Issues
### Recommended Next Steps
```

Route the next steps by what you found:

- vulnerable dependencies: `/dependency-scan`
- injection, XSS, CSRF: `/pentest`
- broad OWASP coverage: `/owasp`
- PII handling: `/gdpr`
- encryption gaps: `/encryption`
- compliance needs: `/soc2`
