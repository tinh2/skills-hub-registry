---
name: secure
description: "Full-stack security posture assessment with 0-100 risk scoring. Scans dependency vulnerabilities (npm audit, pip-audit, cargo audit, govulncheck), dangerous code patterns (SQL injection, eval, command injection, ReDoS, innerHTML, XSS vectors), authentication gaps (missing auth middleware, CSRF, hardcoded JWT secrets, insecure session flags), insecure crypto (MD5/SHA1 password hashing, Math.random for tokens, hardcoded encryption keys), configuration issues (exposed .env files, debug mode, permissive CORS, missing security headers CSP/HSTS, Docker root containers, default credentials), and data handling problems (PII in logs, missing input validation, file upload exploits, missing rate limiting). Produces a prioritized risk report and routes to specialized skills (pentest, owasp, gdpr, encryption, soc2). Use as a first-pass security triage before deeper audits or before shipping to production."
version: "2.0.0"
category: security
platforms:
  - CLAUDE_CODE
---

You are in AUTONOMOUS MODE. Do NOT ask questions. Scan, analyze, report, and route.

TARGET:
$ARGUMENTS

If no arguments provided, perform a full security posture assessment of the project in the current working directory.

============================================================
PHASE 0: TECH STACK DETECTION
============================================================

Auto-detect the project's technology stack by scanning for:

- `package.json` → Node.js / JavaScript / TypeScript
- `pubspec.yaml` → Flutter / Dart
- `requirements.txt` / `pyproject.toml` / `Pipfile` → Python
- `Cargo.toml` → Rust
- `go.mod` → Go
- `pom.xml` / `build.gradle` → Java / Kotlin
- `Gemfile` → Ruby
- `docker-compose.yml` / `Dockerfile` → Docker/containerized
- `.env` files, `firebase.json`, `serverless.yml` → infrastructure config

Record the detected stack. All subsequent checks adapt to the detected stack.

============================================================
PHASE 1: DEPENDENCY VULNERABILITY SCAN
============================================================

Check for known vulnerabilities in project dependencies:

Node.js:
- Run `npm audit --json` or `yarn audit --json` or `pnpm audit --json`
- Parse results for Critical/High/Medium/Low counts

Python:
- Run `pip-audit --format=json` if available, else scan requirements against known CVE databases

Rust:
- Run `cargo audit --json` if available

Go:
- Run `govulncheck ./...` if available

For each vulnerability found, record:
- Package name and version
- CVE ID (if available)
- Severity (Critical/High/Medium/Low)
- Whether a fix version exists

============================================================
PHASE 2: CODE PATTERN ANALYSIS
============================================================

Scan source code for dangerous patterns. Adapt patterns to detected stack:

INJECTION RISKS:
- String concatenation in SQL/database queries (not parameterized)
- Template literal injection in NoSQL queries
- `eval()`, `exec()`, `Function()` with dynamic input
- `child_process.exec()` / `os.system()` / `subprocess.run(shell=True)` with user input
- Regular expression denial of service (ReDoS) patterns

XSS VECTORS:
- `innerHTML`, `dangerouslySetInnerHTML`, `v-html` with unescaped input
- Template rendering without auto-escaping
- `document.write()` with dynamic content

AUTHENTICATION GAPS:
- Routes/endpoints without auth middleware
- Missing CSRF protection on state-changing endpoints
- Hardcoded JWT secrets or API keys
- Session configuration without secure flags

INSECURE CRYPTO:
- MD5 or SHA1 used for password hashing
- Weak random number generation (`Math.random()` for tokens)
- Hardcoded encryption keys or IVs

============================================================
PHASE 3: CONFIGURATION AUDIT
============================================================

Scan project configuration for security issues:

EXPOSED SECRETS:
- `.env` files committed to git (check `.gitignore`)
- API keys, tokens, passwords in source code
- Private keys or certificates in the repository
- Database connection strings with credentials

DEBUG MODE:
- `DEBUG=true` or `NODE_ENV=development` in production configs
- Stack traces exposed in error responses
- Verbose logging of sensitive data
- Source maps exposed in production builds

CORS/HEADERS:
- `Access-Control-Allow-Origin: *` in production
- Missing security headers (CSP, HSTS, X-Frame-Options, X-Content-Type-Options)
- Permissive cookie settings (missing Secure, HttpOnly, SameSite)

INFRASTRUCTURE:
- Docker containers running as root
- Exposed ports that should be internal
- Missing network segmentation in docker-compose
- Default credentials in database configs

============================================================
PHASE 4: DATA HANDLING REVIEW
============================================================

Scan for PII and sensitive data handling issues:

PII EXPOSURE:
- User data (email, phone, name, address) logged or exposed in errors
- PII stored without encryption
- PII transmitted without TLS
- PII in URL parameters (visible in logs/history)

DATA VALIDATION:
- Missing input validation on API endpoints
- Missing output encoding/sanitization
- File upload without type/size validation
- Missing rate limiting on sensitive endpoints

============================================================
PHASE 5: RISK SCORING
============================================================

Calculate a risk score (0-100, lower is better):

Scoring weights:
- Each Critical finding: +15 points
- Each High finding: +8 points
- Each Medium finding: +3 points
- Each Low finding: +1 point
- Cap at 100

Risk levels:
- 0-15: EXCELLENT — minimal risk
- 16-35: GOOD — minor issues, low priority
- 36-60: MODERATE — several issues need attention
- 61-80: HIGH — significant vulnerabilities present
- 81-100: CRITICAL — immediate action required

============================================================
PHASE 6: ROUTING
============================================================

Based on findings, recommend specific sub-skills:

- Dependency vulns found → "Run `/dependency-scan` for auto-fix of vulnerable packages"
- Injection/XSS/CSRF found → "Run `/pentest` for detailed exploitation analysis"
- OWASP category matches → "Run `/owasp` for full OWASP Top 10 audit"
- PII handling issues → "Run `/gdpr` for compliance assessment"
- Encryption gaps → "Run `/encryption` to audit and implement proper encryption"
- Enterprise/compliance needs → "Run `/soc2` for SOC2 readiness assessment"


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

## Security Posture Report

**Project:** [name]
**Stack:** [detected technologies]
**Risk Score:** [0-100] — [EXCELLENT/GOOD/MODERATE/HIGH/CRITICAL]
**Scan Date:** [date]

### Summary

| Severity | Count | Auto-Fixable |
|----------|-------|-------------|
| Critical | N     | N           |
| High     | N     | N           |
| Medium   | N     | N           |
| Low      | N     | N           |

### Critical Findings (fix immediately)
[List each Critical finding with file:line, description, and recommended fix]

### High Findings (fix soon)
[List each High finding]

### Medium Findings (plan to fix)
[List each Medium finding]

### Low Findings (nice to have)
[List each Low finding]

### Dependency Vulnerabilities
[Summary table of vulnerable packages]

### Configuration Issues
[List of config problems found]

### Recommended Next Steps
[Ordered list of sub-skills to run based on findings]

============================================================
NEXT STEPS
============================================================

After reviewing the posture report:
- "Run `/dependency-scan` to auto-fix vulnerable packages."
- "Run `/owasp` for a comprehensive OWASP Top 10 audit."
- "Run `/pentest` for code-level penetration testing."
- "Run `/gdpr` to assess privacy compliance."
- "Run `/encryption` to audit encryption implementation."
- "Run `/soc2` to evaluate SOC2 readiness."


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /secure — {{YYYY-MM-DD}}
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

- Do NOT modify any code in this skill — this is assessment only.
- Do NOT run actual network attacks or exploit vulnerabilities.
- Do NOT expose or log any secrets found — redact them in output.
- Do NOT skip any phase — run all checks even if early phases find issues.
- Do NOT report false positives as confirmed — mark confidence level.
- Do NOT install security scanning tools — use only what is already available.
