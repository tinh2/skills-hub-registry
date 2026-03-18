---
name: soc2
description: "SOC 2 Type II readiness assessment against all five Trust Service Criteria. Evaluates Security controls (CC6/CC7 -- RBAC, access provisioning/removal, network segmentation, TLS enforcement, input validation, vulnerability management, incident detection and response), Availability controls (A1 -- capacity management, auto-scaling, backup frequency, disaster recovery, RTO/RPO, health checks, uptime monitoring), Processing Integrity (PI1 -- data validation, error handling, transaction logging, idempotency, race condition protection), Confidentiality (C1 -- data classification, encryption at rest and in transit, access logging, secure disposal, key rotation), and Privacy (P1-P8 -- notice, consent, collection limitation, retention/disposal, data access/export, third-party disclosure, data quality, privacy monitoring). Produces a control-by-control PASS/PARTIAL/FAIL matrix with evidence references, remediation roadmap, and evidence collection checklist. Use when preparing for a SOC 2 audit, evaluating enterprise readiness, or building compliance controls into your application."
version: "2.0.0"
category: security
platforms:
  - CLAUDE_CODE
---

You are in AUTONOMOUS MODE. Do NOT ask questions. Evaluate, assess, and produce a readiness report.

TARGET:
$ARGUMENTS

If no arguments provided, evaluate the entire project in the current working directory against all five SOC 2 Trust Service Criteria.

============================================================
PHASE 0: TECH STACK AND INFRASTRUCTURE DETECTION
============================================================

Auto-detect the project's technology and infrastructure:

APPLICATION LAYER:
- Backend framework and language
- Frontend framework
- Database technology
- Authentication mechanism

INFRASTRUCTURE:
- Cloud provider (AWS, GCP, Azure) — check for config files, SDK imports
- Container orchestration (Docker, Kubernetes) — check for manifests
- CI/CD pipeline (GitHub Actions, GitLab CI, Jenkins) — check workflow files
- Infrastructure as Code (Terraform, CloudFormation, Pulumi) — check configs

INTEGRATIONS:
- Monitoring/alerting services
- Logging infrastructure
- Secret management (Vault, AWS Secrets Manager, etc.)
- Backup services

Record all detected components. SOC2 controls apply across the entire stack.

============================================================
PHASE 1: SECURITY (CC / Common Criteria)
============================================================

Evaluate security controls:

CC6.1 — LOGICAL ACCESS CONTROLS:
- Authentication mechanism exists and enforces strong credentials
- Role-based access control (RBAC) implemented
- Principle of least privilege applied
- Service accounts use minimal permissions
- API authentication on all endpoints

CC6.2 — ACCESS PROVISIONING:
- User registration flow with proper validation
- Admin user management capabilities
- Ability to disable/revoke access
- Access review mechanisms

CC6.3 — ACCESS REMOVAL:
- Account deactivation/deletion capability
- Session invalidation on logout
- Token revocation mechanisms
- Cleanup of associated resources on user removal

CC6.6 — SYSTEM BOUNDARIES:
- Network segmentation (Docker networks, VPC config)
- Firewall rules / security groups defined
- Internal services not exposed publicly
- Rate limiting on public endpoints

CC6.7 — DATA TRANSMISSION:
- TLS/HTTPS enforced for all external communication
- Certificate validation enabled (no `rejectUnauthorized: false`)
- Sensitive data not transmitted in URL parameters
- WebSocket connections use WSS

CC6.8 — MALICIOUS SOFTWARE PREVENTION:
- Input validation on all user-supplied data
- File upload type and size restrictions
- Dependency vulnerability scanning configured
- No `eval()` or dynamic code execution with user input

CC7.1 — VULNERABILITY MANAGEMENT:
- Dependency audit tool configured (npm audit, pip-audit, etc.)
- CI pipeline includes security scanning
- Process for addressing reported vulnerabilities

CC7.2 — INCIDENT DETECTION:
- Security event logging (failed logins, access denied, etc.)
- Anomaly detection or alerting configured
- Error monitoring service integrated

CC7.3 — INCIDENT RESPONSE:
- Incident response documentation exists
- Contact information for security issues
- Mechanism to disable compromised accounts/keys

For each control: PASS / PARTIAL / FAIL with evidence and gaps.

============================================================
PHASE 2: AVAILABILITY (A1)
============================================================

Evaluate availability controls:

A1.1 — CAPACITY MANAGEMENT:
- Resource limits configured (memory, CPU, connections)
- Auto-scaling configuration (if cloud-hosted)
- Database connection pooling
- Queue/worker capacity planning

A1.2 — RECOVERY:
- Database backup configuration
- Backup frequency and retention
- Tested restore procedures (documentation)
- Point-in-time recovery capability
- Disaster recovery plan documented

A1.3 — RECOVERY TESTING:
- Evidence of backup restoration tests
- Failover testing documentation
- Recovery time objectives (RTO) defined
- Recovery point objectives (RPO) defined

MONITORING:
- Health check endpoints implemented
- Uptime monitoring configured
- Performance monitoring (response times, error rates)
- Alerting thresholds defined
- Status page or incident communication channel

============================================================
PHASE 3: PROCESSING INTEGRITY (PI)
============================================================

Evaluate processing integrity controls:

PI1.1 — DATA VALIDATION:
- Input validation on API endpoints (type checking, length limits, format)
- Schema validation for data models
- Request payload validation middleware
- Output encoding/sanitization

PI1.2 — ERROR HANDLING:
- Structured error handling (try/catch, error middleware)
- Error responses do not expose internal details
- Failed operations rolled back cleanly
- Partial failure handling (batch operations)

PI1.3 — TRANSACTION LOGGING:
- Critical operations logged with timestamps
- Audit trail for data modifications
- Transaction IDs for traceability
- Immutable log storage (logs cannot be tampered with)

PI1.4 — DATA PROCESSING ACCURACY:
- Idempotent operations (safe to retry)
- Race condition protection (locks, transactions, optimistic concurrency)
- Data transformation validation
- Calculation verification (financial, statistical)

============================================================
PHASE 4: CONFIDENTIALITY (C1)
============================================================

Evaluate confidentiality controls:

C1.1 — DATA CLASSIFICATION:
- Data sensitivity levels defined (public, internal, confidential, restricted)
- PII fields identified and labeled
- Classification applied to database schemas
- Different handling based on classification level

C1.2 — ENCRYPTION AT REST:
- Database encryption enabled
- File storage encryption enabled
- Field-level encryption for highly sensitive data
- Encryption key management (rotation, access control)

C1.3 — ENCRYPTION IN TRANSIT:
- TLS 1.2+ enforced
- HSTS headers configured
- Certificate management process
- Internal service communication encrypted

C1.4 — ACCESS LOGGING:
- Data access logged (who accessed what, when)
- Admin actions logged
- API access logging
- Log retention policy

C1.5 — SECURE DISPOSAL:
- Data deletion actually removes data (not just soft delete)
- Secure wipe for sensitive data
- Media disposal procedures (for physical infrastructure)
- Backup expiry aligned with retention policy

============================================================
PHASE 5: PRIVACY (P1)
============================================================

Evaluate privacy controls:

P1.1 — NOTICE:
- Privacy policy accessible and up to date
- Data collection notice at point of collection
- Cookie notice/consent mechanism

P2.1 — CONSENT:
- Explicit consent obtained for data processing
- Separate consent for separate purposes
- Consent withdrawal mechanism
- Consent records maintained

P3.1 — COLLECTION LIMITATION:
- Data minimization practiced (collect only what is needed)
- Purpose limitation (data used only for stated purpose)
- Collection points documented

P4.1 — USE/RETENTION/DISPOSAL:
- Retention periods defined per data category
- Automated data expiry mechanisms
- Purpose limitation on data use
- Disposal procedures implemented

P5.1 — ACCESS:
- Users can access their data
- Data export in machine-readable format
- Response time for data requests defined

P6.1 — DISCLOSURE:
- Third-party data sharing documented
- Data processing agreements in place
- Cross-border transfer safeguards

P7.1 — QUALITY:
- Users can correct their data
- Data validation at entry
- Duplicate detection mechanisms

P8.1 — MONITORING AND ENFORCEMENT:
- Privacy incident response process
- Privacy impact assessments for new features
- Regular privacy reviews scheduled


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

## SOC2 Readiness Report

**Project:** [name]
**Stack:** [detected technologies]
**Assessment Date:** [date]

### Executive Summary

| Trust Service Criteria | Controls Assessed | PASS | PARTIAL | FAIL |
|----------------------|-------------------|------|---------|------|
| Security (CC)        | N                 | N    | N       | N    |
| Availability (A1)    | N                 | N    | N       | N    |
| Processing Integrity | N                 | N    | N       | N    |
| Confidentiality (C1) | N                 | N    | N       | N    |
| Privacy (P1)         | N                 | N    | N       | N    |

**Overall Readiness:** [NOT READY / PARTIAL / READY]

### Detailed Control Assessment

#### Security Controls

| Control | Status | Evidence | Gap | Remediation |
|---------|--------|----------|-----|-------------|
| CC6.1 Logical Access | [PASS/PARTIAL/FAIL] | [what exists] | [what's missing] | [how to fix] |

[Repeat for each control across all criteria]

### Critical Gaps (must fix before audit)
[Ordered list of FAIL items with remediation effort estimates]

### Partial Controls (should improve)
[List of PARTIAL items with specific improvement steps]

### Remediation Roadmap

| Priority | Control | Effort | Description |
|----------|---------|--------|-------------|
| P0 — Critical | CC6.1 | 2 days | Implement RBAC |
| P1 — High | A1.2 | 1 day | Configure automated backups |
| P2 — Medium | PI1.3 | 3 days | Add audit logging |

### Evidence Collection Checklist
- [ ] Access control policies documented
- [ ] Encryption configuration documented
- [ ] Incident response plan written
- [ ] Backup and recovery procedures tested
- [ ] Change management process documented
- [ ] Vendor management (third-party DPAs)
- [ ] Employee security awareness training
- [ ] Penetration test results (annual)

============================================================
NEXT STEPS
============================================================

After reviewing the readiness report:
- "Fix critical gaps identified in the Security (CC) section first."
- "Run `/encryption` to address Confidentiality (C1) encryption gaps."
- "Run `/gdpr` for deeper Privacy (P1) compliance assessment."
- "Run `/pentest` to generate evidence for CC7.1 vulnerability management."
- "Run `/secure` for a technical security baseline before SOC2 prep."
- "Engage a SOC2 auditor once all P0 gaps are remediated."


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /soc2 — {{YYYY-MM-DD}}
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

- Do NOT modify any code — this is an assessment skill, not an implementation skill.
- Do NOT claim SOC2 certification or compliance — only assess readiness.
- Do NOT provide legal or audit advice — focus on technical controls.
- Do NOT skip any Trust Service Criteria — assess all five.
- Do NOT mark a control as PASS without finding concrete evidence in the codebase.
- Do NOT conflate "not applicable" with "PASS" — mark N/A separately with justification.
- Do NOT assess organizational controls (HR policies, training) — focus on what is visible in code and config.
