---
name: owasp
description: "Systematic audit against the OWASP 2021 Top 10 web application security risks with severity-rated, file-level findings. Checks A01 Broken Access Control (IDOR, path traversal, CORS, privilege escalation), A02 Cryptographic Failures (weak algorithms, exposed secrets, missing TLS), A03 Injection (SQL, NoSQL, command, XSS, LDAP, XPath, template injection), A04 Insecure Design (missing rate limiting, business logic flaws, race conditions), A05 Security Misconfiguration (debug mode, default credentials, missing security headers, CSP), A06 Vulnerable Components (dependency CVEs, outdated frameworks, EOL runtimes), A07 Auth Failures (weak passwords, session fixation, missing MFA), A08 Data Integrity (insecure deserialization, CI/CD integrity, dependency confusion), A09 Logging Failures (missing security events, PII in logs, log injection), A10 SSRF (user-supplied URLs, cloud metadata access, DNS rebinding). Use for web app security audits, pre-release security checks, or compliance evidence gathering."
version: "2.0.0"
category: security
platforms:
  - CLAUDE_CODE
---

You are in AUTONOMOUS MODE. Do NOT ask questions. Audit every OWASP category systematically.

TARGET:
$ARGUMENTS

If no arguments provided, audit the entire project in the current working directory against all OWASP Top 10 categories.

============================================================
PHASE 0: TECH STACK DETECTION
============================================================

Auto-detect the project's technology stack:

- `package.json` → Node.js (Express, Fastify, NestJS, Next.js, etc.)
- `pubspec.yaml` → Flutter / Dart
- `requirements.txt` / `pyproject.toml` → Python (Django, Flask, FastAPI, etc.)
- `Cargo.toml` → Rust (Actix, Axum, Rocket, etc.)
- `go.mod` → Go (Gin, Echo, Fiber, etc.)
- `pom.xml` / `build.gradle` → Java/Kotlin (Spring, Quarkus, etc.)
- `Gemfile` → Ruby (Rails, Sinatra, etc.)
- `*.php` → PHP (Laravel, Symfony, etc.)

Identify the web framework, ORM/database layer, auth library, and template engine.
These determine what patterns to scan for in each OWASP category.

============================================================
PHASE 1: A01 — BROKEN ACCESS CONTROL
============================================================

Scan for access control failures:

AUTH MIDDLEWARE COVERAGE:
- List all route definitions (Express routes, Flask routes, Django urls, etc.)
- Flag routes that handle sensitive data but lack auth middleware
- Flag admin routes accessible without admin/role checks

IDOR (Insecure Direct Object References):
- Find endpoints using user-supplied IDs to fetch resources
- Check if ownership/permission is verified before returning data
- Pattern: `findById(req.params.id)` without ownership check

PATH TRAVERSAL:
- Find file operations using user input in paths
- Check for `../` sanitization
- Pattern: `fs.readFile(userInput)`, `open(user_path)`

CORS MISCONFIGURATION:
- Check CORS origin settings — flag `*` or overly permissive origins
- Verify credentials flag is not combined with wildcard origin

PRIVILEGE ESCALATION:
- Check if role/permission changes require re-authentication
- Verify role checks on mutation endpoints (not just read)

For each finding: file path, line number, severity, description, fix.

============================================================
PHASE 2: A02 — CRYPTOGRAPHIC FAILURES
============================================================

Scan for cryptographic weaknesses:

WEAK ALGORITHMS:
- MD5 used for anything security-related (passwords, tokens, signatures)
- SHA1 used for security (acceptable for checksums only)
- DES, 3DES, RC4, or other deprecated ciphers
- RSA key sizes below 2048 bits
- ECB mode block cipher usage

EXPOSED SECRETS:
- API keys, tokens, passwords hardcoded in source
- Private keys committed to repository
- Connection strings with embedded credentials
- Secrets in client-side/frontend code

WEAK TRANSPORT:
- HTTP URLs for API calls (not HTTPS)
- Missing TLS verification (`rejectUnauthorized: false`, `verify=False`)
- Insecure WebSocket connections (`ws://` instead of `wss://`)

DATA EXPOSURE:
- Sensitive data in logs (passwords, tokens, PII)
- Sensitive data in error messages returned to clients
- Sensitive data stored in localStorage/sessionStorage
- Missing encryption for PII at rest

============================================================
PHASE 3: A03 — INJECTION
============================================================

Scan for injection vulnerabilities:

SQL INJECTION:
- String concatenation in SQL queries
- Template literals in SQL without parameterization
- Raw queries with user input: `query("SELECT * FROM users WHERE id = " + id)`
- Missing prepared statements in database calls

NOSQL INJECTION:
- User input directly in MongoDB/Firestore query operators
- Pattern: `{ $where: userInput }`, `{ field: { $gt: userInput } }`
- JSON.parse on user input used directly in queries

COMMAND INJECTION:
- `exec()`, `spawn()`, `system()` with user-controlled arguments
- Shell commands built with string concatenation
- Missing input sanitization before shell execution

XSS (Cross-Site Scripting):
- `innerHTML`, `dangerouslySetInnerHTML` with user data
- Template rendering without auto-escape (`| safe`, `{!! !!}`, `<%- %>`)
- `document.write()`, `eval()` with user-controlled strings
- Reflected user input in HTML responses without encoding

LDAP INJECTION:
- User input in LDAP filter strings without escaping

XPATH INJECTION:
- User input in XPath queries without parameterization

For each: exact code location, injection type, proof pattern, fix.

============================================================
PHASE 4: A04 — INSECURE DESIGN
============================================================

Scan for design-level security flaws:

MISSING RATE LIMITING:
- Login/auth endpoints without rate limiting
- Password reset without rate limiting
- API endpoints without throttling
- OTP/verification code endpoints allowing brute force

BUSINESS LOGIC FLAWS:
- Price/quantity manipulation possible via API
- Workflow steps that can be skipped
- Race conditions in concurrent operations (check-then-act)
- Missing server-side validation (client-only checks)

MISSING SECURITY CONTROLS:
- No account lockout after failed attempts
- No CAPTCHA on public-facing forms
- Missing input length limits
- No abuse detection mechanisms

============================================================
PHASE 5: A05 — SECURITY MISCONFIGURATION
============================================================

Scan for configuration issues:

DEBUG/DEVELOPMENT MODE:
- `DEBUG=True`, `NODE_ENV=development` in production configs
- Stack traces in error responses
- Verbose error messages exposing internals
- Development tools/routes accessible (e.g., `/debug`, `/swagger` unprotected)

DEFAULT CREDENTIALS:
- Default database passwords (`postgres`, `root`, `admin`)
- Default admin accounts
- Default API keys or tokens
- Sample/demo credentials in config files

UNNECESSARY FEATURES:
- Unused endpoints or services exposed
- Directory listing enabled
- Server version headers exposed (`X-Powered-By`)
- Unnecessary HTTP methods enabled (TRACE, OPTIONS wide open)

MISSING SECURITY HEADERS:
- Content-Security-Policy absent or permissive
- Strict-Transport-Security missing
- X-Frame-Options / X-Content-Type-Options missing
- Referrer-Policy not set
- Permissions-Policy not set

============================================================
PHASE 6: A06 — VULNERABLE AND OUTDATED COMPONENTS
============================================================

Scan for vulnerable dependencies:

DEPENDENCY AUDIT:
- Run the appropriate audit command for the detected package manager
- Parse results grouping by severity
- Check for components with no maintainer or archived repositories
- Flag dependencies more than 2 major versions behind

KNOWN CVE CHECK:
- Cross-reference dependency versions against known CVEs
- Flag any dependency with a Critical or High CVE
- Note if patches or upgrades are available

FRAMEWORK VERSIONS:
- Check if the web framework itself is up to date
- Check runtime version (Node.js, Python, Ruby, etc.)
- Flag end-of-life runtime versions

============================================================
PHASE 7: A07 — IDENTIFICATION AND AUTHENTICATION FAILURES
============================================================

Scan for authentication weaknesses:

PASSWORD POLICIES:
- Check if password strength validation exists
- Minimum length, complexity requirements
- Check for password breach list validation (HaveIBeenPwned integration)

SESSION MANAGEMENT:
- Session token generation (cryptographically random?)
- Session expiration configured
- Session invalidation on logout
- Session fixation prevention (regenerate on login)
- Cookie flags: Secure, HttpOnly, SameSite

MFA:
- Check if MFA is available for sensitive operations
- Verify MFA cannot be bypassed

CREDENTIAL STORAGE:
- Password hashing algorithm (bcrypt/scrypt/argon2 = good; MD5/SHA = bad)
- Salt usage for password hashing
- Iteration count / work factor adequacy

============================================================
PHASE 8: A08 — SOFTWARE AND DATA INTEGRITY FAILURES
============================================================

Scan for integrity issues:

INSECURE DESERIALIZATION:
- `JSON.parse()` on untrusted input without validation
- `pickle.loads()`, `yaml.load()` (unsafe loaders) on user data
- Java `ObjectInputStream` with untrusted data
- XML external entity (XXE) processing

CI/CD INTEGRITY:
- Unsigned dependencies or plugins
- Missing lock file integrity checks
- Auto-merge without review
- Missing dependency pinning (using `latest` or `*`)

UPDATE MECHANISMS:
- Unsigned auto-update payloads
- Missing checksum verification on downloads
- Dependency confusion risk (private package names matching public)

============================================================
PHASE 9: A09 — SECURITY LOGGING AND MONITORING FAILURES
============================================================

Scan for logging deficiencies:

MISSING SECURITY EVENTS:
- Failed login attempts not logged
- Access control failures not logged
- Input validation failures not logged
- High-value transactions not logged

LOG QUALITY:
- Sensitive data in logs (passwords, tokens, PII)
- Missing timestamps or user identifiers in log entries
- Log injection possible (user input in log messages without sanitization)
- Logs not structured (hard to parse/alert on)

MONITORING:
- No alerting configuration found
- No health check endpoints
- No error tracking integration (Sentry, Datadog, etc.)

============================================================
PHASE 10: A10 — SERVER-SIDE REQUEST FORGERY (SSRF)
============================================================

Scan for SSRF vulnerabilities:

URL HANDLING:
- User-supplied URLs passed to HTTP clients without validation
- URL fetching without allowlist/denylist
- Internal service URLs constructable from user input
- Redirect following without origin validation

DNS REBINDING:
- Missing DNS resolution validation
- Time-of-check-to-time-of-use gaps in URL validation

CLOUD METADATA:
- Potential access to cloud metadata endpoints (169.254.169.254)
- Missing network segmentation for internal services
- Internal service discovery exposed to user input


============================================================
SELF-HEALING VALIDATION (max 2 iterations)
============================================================

After producing the security analysis, validate thoroughness:

1. Verify every category in the audit was actually checked (not skipped).
2. Verify every finding has a specific file:line location.
3. Verify severity ratings are justified by impact assessment.
4. Verify no false positives by re-reading flagged code in context.

IF VALIDATION FAILS:
- Re-audit skipped categories or vague findings
- Verify or remove false positives
- Repeat up to 2 iterations

============================================================
OUTPUT
============================================================

## OWASP Top 10 Audit Report

**Project:** [name]
**Stack:** [detected technologies]
**Date:** [date]

### Summary

| ID  | Category                          | Status | Findings |
|-----|-----------------------------------|--------|----------|
| A01 | Broken Access Control             | [PASS/WARN/FAIL] | N |
| A02 | Cryptographic Failures            | [PASS/WARN/FAIL] | N |
| A03 | Injection                         | [PASS/WARN/FAIL] | N |
| A04 | Insecure Design                   | [PASS/WARN/FAIL] | N |
| A05 | Security Misconfiguration         | [PASS/WARN/FAIL] | N |
| A06 | Vulnerable Components             | [PASS/WARN/FAIL] | N |
| A07 | Auth Failures                     | [PASS/WARN/FAIL] | N |
| A08 | Data Integrity Failures           | [PASS/WARN/FAIL] | N |
| A09 | Logging Failures                  | [PASS/WARN/FAIL] | N |
| A10 | SSRF                              | [PASS/WARN/FAIL] | N |

### Detailed Findings

For each category with WARN or FAIL:

#### [Category Name]

| # | Severity | File | Line | Description | Fix |
|---|----------|------|------|-------------|-----|
| 1 | Critical | path/to/file.ts | 42 | Description | Recommended fix |

### Risk Assessment
- **Critical findings:** N (must fix immediately)
- **High findings:** N (fix before next release)
- **Medium findings:** N (plan to address)
- **Low findings:** N (track and review)

### Remediation Priority
[Ordered list of fixes by severity and effort, Critical first]

============================================================
NEXT STEPS
============================================================

After reviewing the audit:
- "Run `/pentest` to verify exploitability of injection and auth findings."
- "Run `/dependency-scan` to auto-fix vulnerable components (A06)."
- "Run `/encryption` to address cryptographic failures (A02)."
- "Run `/secure` for the full security posture assessment."


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /owasp — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.

============================================================
DO NOT
============================================================

- Do NOT modify any code — this is an audit skill, not a fix skill.
- Do NOT run actual exploits or attacks against the application.
- Do NOT expose discovered secrets in the output — redact them (show first 4 chars + ***).
- Do NOT skip categories — audit all 10 even if some seem irrelevant.
- Do NOT mark a category as PASS without actually scanning for it.
- Do NOT conflate suspicion with confirmed findings — note confidence level.
- Do NOT install external scanning tools — analyze code directly.
