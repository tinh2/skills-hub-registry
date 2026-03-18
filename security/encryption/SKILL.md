---
name: encryption
description: "Audit and harden encryption across the full stack. Checks data-at-rest encryption (database TDE, field-level AES-256-GCM, file storage SSE, backup encryption), data-in-transit security (TLS 1.2+, HSTS, certificate pinning, mTLS, WebSocket WSS), key management (KMS, envelope encryption, key rotation, key separation), password hashing (argon2id, bcrypt, scrypt, PBKDF2 work factors, salt uniqueness, migration plans), token security (JWT signing algorithms, CSPRNG, refresh token rotation), and API key management (hashed storage, scoping, revocation). Use when you need to audit crypto, fix weak hashing, implement envelope encryption, rotate keys, upgrade TLS, or harden token generation."
version: "2.0.0"
category: security
platforms:
  - CLAUDE_CODE
---

You are in AUTONOMOUS MODE. Do NOT ask questions. Audit current encryption state, then implement improvements.

TARGET:
$ARGUMENTS

If no arguments provided, perform a full encryption audit and generate an implementation plan. If arguments specify an area (e.g., "password hashing", "TLS", "key rotation"), focus on that area and implement changes.

============================================================
PHASE 0: TECH STACK DETECTION
============================================================

Auto-detect the project's technology stack:

- Language and framework (Node.js, Python, Go, Java, Rust, etc.)
- Database (PostgreSQL, MySQL, MongoDB, Firestore, DynamoDB, etc.)
- Cloud provider (AWS, GCP, Azure, self-hosted)
- Authentication system (Firebase Auth, Auth0, Passport.js, custom)
- File storage (S3, GCS, local filesystem)
- Mobile/web platform (affects certificate pinning requirements)
- Secret management (Vault, AWS Secrets Manager, GCP Secret Manager, env vars)

Record the stack — encryption implementation varies significantly by technology.

============================================================
PHASE 1: DATA AT REST ENCRYPTION AUDIT
============================================================

Assess current encryption of stored data:

DATABASE ENCRYPTION:
- Check if database-level encryption is enabled (TDE for SQL, encryption at rest for cloud DBs)
- Check database connection strings for SSL/TLS parameters
- For cloud databases: verify encryption is enabled in config/IaC files

FIELD-LEVEL ENCRYPTION:
- Identify PII fields in data models (email, phone, SSN, payment info, health data)
- Check if sensitive fields are encrypted before storage
- Check encryption algorithm used (AES-256-GCM preferred)
- Check if initialization vectors (IVs) are unique per record (not reused)
- Verify encrypted fields are searchable only via exact match or encrypted index

FILE ENCRYPTION:
- Check if uploaded files are encrypted at rest
- Check if file storage service has encryption enabled (S3 SSE, GCS encryption)
- Verify temporary files are cleaned up (not left unencrypted on disk)

BACKUP ENCRYPTION:
- Check if database backups are encrypted
- Check if backup encryption keys are separate from primary keys
- Verify backup retention and key retention align

For each area: current state, gaps, and recommended implementation.

============================================================
PHASE 2: DATA IN TRANSIT ENCRYPTION AUDIT
============================================================

Assess encryption of data in motion:

TLS CONFIGURATION:
- Check TLS version requirements (minimum TLS 1.2, prefer TLS 1.3)
- Search for disabled certificate verification:
  - Node.js: `rejectUnauthorized: false`, `NODE_TLS_REJECT_UNAUTHORIZED=0`
  - Python: `verify=False`, `ssl._create_unverified_context()`
  - Go: `InsecureSkipVerify: true`
  - Java: custom TrustManager accepting all certificates
- Check for HTTP (not HTTPS) URLs in API calls
- Check for insecure WebSocket (`ws://`) connections

SECURITY HEADERS:
- `Strict-Transport-Security` (HSTS) — present, max-age >= 31536000, includeSubDomains
- `Content-Security-Policy` — restricts resource loading
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY` or `SAMEORIGIN`
- `Referrer-Policy: strict-origin-when-cross-origin` or stricter

CERTIFICATE PINNING (mobile apps):
- Flutter: check for certificate pinning in HTTP client config
- iOS: check for `NSAppTransportSecurity` settings in Info.plist
- Android: check for `network_security_config.xml`
- Verify pins are for intermediate certificates (not leaf — avoids rotation issues)

INTERNAL COMMUNICATION:
- Service-to-service communication encrypted (mTLS or service mesh)
- Database connections use SSL/TLS
- Redis/cache connections encrypted
- Message queue connections encrypted (RabbitMQ, Kafka SSL)

============================================================
PHASE 3: KEY MANAGEMENT AUDIT AND IMPLEMENTATION
============================================================

Assess and improve cryptographic key management:

CURRENT STATE AUDIT:
- Where are encryption keys stored? (env vars, config files, code, KMS)
- Are keys hardcoded in source code? (Critical finding if yes)
- Are keys in version control? (Critical finding if yes)
- Is there a key rotation process?
- Are different keys used for different purposes (separation of concerns)?

KEY ROTATION STRATEGY:
Generate a key rotation plan based on the detected stack:

For AWS:
```
- Use AWS KMS for master keys
- Implement envelope encryption: KMS key → data key → encrypt data
- Enable automatic annual rotation for KMS keys
- Data keys rotated per-session or per-record
```

For GCP:
```
- Use Cloud KMS for master keys
- Enable automatic rotation (90-day recommended)
- Use envelope encryption pattern
- Separate key rings per environment
```

For self-hosted / Vault:
```
- Use HashiCorp Vault Transit secrets engine
- Configure auto-rotation policies
- Implement key versioning for re-encryption
- Set up audit logging for key access
```

ENVELOPE ENCRYPTION IMPLEMENTATION:
If the project needs field-level encryption, implement the envelope encryption pattern:
1. Master key stored in KMS (never leaves KMS)
2. Data Encryption Key (DEK) generated per record or per batch
3. DEK encrypted by master key, stored alongside encrypted data
4. On decrypt: KMS decrypts DEK, DEK decrypts data

Provide implementation code specific to the detected stack.

============================================================
PHASE 4: PASSWORD HASHING AUDIT
============================================================

Assess password storage security:

ALGORITHM CHECK:
- Identify the password hashing algorithm in use
- Rate the algorithm:
  - argon2id — EXCELLENT (preferred, memory-hard)
  - bcrypt — GOOD (widely supported, CPU-hard)
  - scrypt — GOOD (memory-hard)
  - PBKDF2 — ACCEPTABLE (if iteration count >= 600,000 for SHA-256)
  - SHA-256/SHA-512 with salt — WEAK (too fast, upgrade needed)
  - MD5 / SHA-1 — CRITICAL (must replace immediately)
  - Plaintext — CRITICAL (must replace immediately)

CONFIGURATION CHECK:
- bcrypt: work factor >= 12 (recommended: 12-14)
- argon2: memory >= 64MB, iterations >= 3, parallelism >= 1
- scrypt: N >= 2^15, r >= 8, p >= 1
- PBKDF2: iterations >= 600,000 (SHA-256) or >= 210,000 (SHA-512)

SALT CHECK:
- Unique salt per password (not global salt)
- Salt length >= 16 bytes
- Salt generated with cryptographic RNG

MIGRATION PLAN:
If the current algorithm is weak, generate a migration plan:
1. Implement new hashing algorithm alongside old
2. On login: verify with old algorithm, re-hash with new, store new hash
3. Set deadline for forced password reset for accounts not yet migrated
4. Remove old algorithm support after migration period

============================================================
PHASE 5: TOKEN AND API KEY SECURITY
============================================================

Assess token generation and API key management:

TOKEN GENERATION:
- JWT signing algorithm (HS256 acceptable, RS256/ES256 preferred for distributed systems)
- JWT secret strength (>= 256 bits for HMAC, proper key pair for RSA/ECDSA)
- JWT expiration configured (access tokens: 15-60 minutes, refresh tokens: 7-30 days)
- Session tokens use `crypto.randomBytes(32)` or equivalent CSPRNG
- No `Math.random()` for security-sensitive tokens
- OTP/verification codes use cryptographic randomness

API KEY MANAGEMENT:
- API keys stored hashed (like passwords), not in plaintext
- API keys scoped to minimum required permissions
- API key rotation mechanism exists
- Rate limiting per API key
- API key revocation capability
- API keys not logged or exposed in error messages

REFRESH TOKEN SECURITY:
- Refresh tokens stored securely (httpOnly cookie or secure storage)
- Refresh token rotation on use (one-time use)
- Refresh token family tracking (detect stolen tokens)
- Absolute expiration on refresh tokens

============================================================
PHASE 6: IMPLEMENTATION
============================================================

If the $ARGUMENTS request implementation (not just audit), apply fixes:

For each issue found in Phases 1-5:
1. Implement the fix using the project's existing patterns and dependencies
2. Add or update configuration as needed
3. Write migration scripts if data format changes
4. Verify the fix works (run tests, verify encryption/decryption roundtrip)
5. Commit each logical change separately with descriptive messages

Priority order for implementation:
1. Hardcoded secrets → move to environment variables or secret manager
2. Weak password hashing → upgrade algorithm
3. Missing TLS verification → enable proper certificate validation
4. Unencrypted PII → add field-level encryption
5. Missing security headers → add header middleware
6. Key rotation → implement rotation strategy


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

## Encryption Audit Report

**Project:** [name]
**Stack:** [detected technologies]
**Date:** [date]

### Summary

| Area | Status | Findings |
|------|--------|----------|
| Data at Rest | [GOOD/PARTIAL/WEAK/NONE] | N issues |
| Data in Transit | [GOOD/PARTIAL/WEAK/NONE] | N issues |
| Key Management | [GOOD/PARTIAL/WEAK/NONE] | N issues |
| Password Hashing | [GOOD/PARTIAL/WEAK/NONE] | N issues |
| Token Security | [GOOD/PARTIAL/WEAK/NONE] | N issues |
| API Key Security | [GOOD/PARTIAL/WEAK/NONE] | N issues |

### Critical Findings (fix immediately)
[Hardcoded secrets, plaintext passwords, disabled TLS, etc.]

### Recommendations
[Ordered list by priority with implementation guidance]

### Implementation Plan

| Priority | Area | Action | Effort | Dependencies |
|----------|------|--------|--------|-------------|
| P0 | Secrets | Move to env vars | 1 hour | None |
| P1 | Passwords | Upgrade to argon2 | 4 hours | Migration script |
| P2 | PII | Field-level encryption | 1 day | KMS setup |

### Changes Made (if implementation was performed)
[List of commits with descriptions of what was implemented]

============================================================
NEXT STEPS
============================================================

After reviewing the encryption audit:
- "Run `/secure` to verify overall security posture after encryption improvements."
- "Run `/soc2` to check Confidentiality (C1) controls with new encryption."
- "Run `/gdpr` to verify PII encryption meets compliance requirements."
- "Run `/pentest` to verify secrets are no longer exposed."
- "Set up automated key rotation on the schedule recommended above."


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /encryption — {{YYYY-MM-DD}}
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

- Do NOT store or log encryption keys, passwords, or secrets in the output.
- Do NOT downgrade existing encryption (e.g., replacing AES-256 with AES-128).
- Do NOT implement custom cryptographic algorithms — use well-vetted libraries.
- Do NOT use ECB mode for block ciphers — use GCM or CBC with HMAC.
- Do NOT generate keys with `Math.random()` or non-cryptographic PRNGs.
- Do NOT disable TLS verification as a "fix" for certificate issues.
- Do NOT commit secrets even temporarily — use environment variables from the start.
- Do NOT implement encryption without a decryption/migration path.
