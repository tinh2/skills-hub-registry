---
name: healthcare-compliance
description: Audit healthcare software codebase for HIPAA, HITECH, 21st Century Cures Act, and state regulatory compliance with severity-rated findings and remediation priorities.
version: "1.0.0"
category: analysis
platforms:
  - CLAUDE_CODE
---

You are in AUTONOMOUS MODE. Do NOT ask questions. Audit the entire codebase systematically against all healthcare regulatory frameworks.

TARGET:
$ARGUMENTS

If no arguments provided, audit the entire project in the current working directory
against all healthcare compliance categories. If a specific regulation is named
(e.g., "HIPAA only", "Cures Act"), focus on that regulation but still note
cross-cutting issues.

============================================================
PHASE 0: TECH STACK AND HEALTHCARE CONTEXT DETECTION
============================================================

Auto-detect the project's technology stack:

- `package.json` -> Node.js (Express, Fastify, NestJS, Next.js, etc.)
- `pubspec.yaml` -> Flutter / Dart
- `requirements.txt` / `pyproject.toml` -> Python (Django, Flask, FastAPI, etc.)
- `pom.xml` / `build.gradle` -> Java/Kotlin (Spring Boot, etc.)
- `*.csproj` / `*.sln` -> .NET (ASP.NET Core, etc.)
- `go.mod` -> Go
- `Gemfile` -> Ruby on Rails

Identify healthcare-specific dependencies:
- FHIR libraries (hapi-fhir, fhir.js, fhirclient, pyFHIR)
- HL7v2 parsers (node-hl7-complete, python-hl7, HAPI)
- DICOM libraries (dcmjs, pydicom, fo-dicom)
- Clinical terminology libraries (SNOMED, LOINC, ICD-10 packages)
- Healthcare auth (SMART on FHIR, OAuth2 for health)

Determine the application type:
- EHR/EMR system
- Patient portal
- Telehealth platform
- Medical billing/RCM
- Clinical decision support
- Health information exchange
- mHealth / wearable integration
- Population health / analytics

============================================================
PHASE 1: HIPAA PRIVACY RULE COMPLIANCE
============================================================

Scan for PHI handling violations:

PHI IDENTIFICATION:
- Search data models/schemas for PHI fields: name, DOB, SSN, MRN, address,
  phone, email, insurance ID, account numbers, device identifiers, biometrics,
  photos, medical record numbers, health plan beneficiary numbers.
- Map ALL locations where PHI is stored, processed, or transmitted.
- Flag any PHI fields stored without classification/tagging.

MINIMUM NECESSARY STANDARD:
- Check API endpoints that return PHI -- do they return only the fields needed?
- Flag endpoints returning full patient records when partial data suffices.
- Check database queries -- are SELECT * queries used on PHI tables?
- Verify role-based data filtering (nurse sees different fields than billing).

DE-IDENTIFICATION:
- Search for de-identification functions or utilities.
- Check if Safe Harbor method is implemented (removal of 18 identifiers).
- Check if Expert Determination method is referenced.
- Flag any analytics/reporting endpoints that return identifiable PHI.
- Verify test/seed data uses synthetic data, not real PHI.

CONSENT MANAGEMENT:
- Search for consent models, tables, or schemas.
- Verify consent is checked before PHI disclosure.
- Check for consent revocation workflows.
- Flag PHI sharing endpoints that lack consent verification.
- Search for Notice of Privacy Practices references.

PATIENT RIGHTS:
- Right to access: is there an endpoint for patients to download their records?
- Right to amend: can patients request corrections?
- Right to accounting of disclosures: is PHI access logged with recipient info?
- Right to restrict: can patients limit PHI use for treatment/payment/operations?
- Check for request fulfillment within 30-day requirement references.

For each finding: file path, line number, severity (Critical/High/Medium/Low), description, fix.

============================================================
PHASE 2: HIPAA SECURITY RULE COMPLIANCE
============================================================

Scan for Security Rule technical safeguard violations:

ACCESS CONTROLS:
- Unique user identification: verify each user has unique ID (no shared accounts).
- Emergency access procedure: search for break-glass or emergency access mechanisms.
- Automatic logoff: check session timeout configuration (must exist for PHI systems).
- Encryption: verify PHI is encrypted at rest (database-level or field-level).

AUDIT CONTROLS:
- Search for audit logging implementation covering ALL PHI access.
- Verify audit logs capture: who, what, when, where, why (CRUD on PHI).
- Check that audit logs are tamper-evident (append-only, signed, or external).
- Verify audit log retention (minimum 6 years per HIPAA).
- Flag PHI access operations that bypass audit logging.

INTEGRITY CONTROLS:
- Check for data integrity mechanisms (checksums, hashing) on PHI records.
- Verify database transaction handling prevents partial PHI updates.
- Search for data validation on PHI input (format, range, consistency).

TRANSMISSION SECURITY:
- Verify TLS 1.2+ for all PHI transmission.
- Check API endpoints handling PHI for HTTPS enforcement.
- Flag any HTTP (non-TLS) endpoints that transmit PHI.
- Check email sending for PHI -- must use encryption.
- Verify WebSocket connections use WSS for PHI.
- Check file transfer mechanisms (SFTP, not FTP).

WORKFORCE SECURITY:
- Check for role definitions and role-based access control (RBAC).
- Verify separation of duties in admin functions.
- Search for credential management (password policies, MFA support).

============================================================
PHASE 3: HITECH ACT COMPLIANCE
============================================================

Scan for HITECH-specific requirements:

BREACH NOTIFICATION:
- Search for breach detection mechanisms or incident response code.
- Check for notification workflows (individual, HHS, media for 500+ records).
- Verify breach risk assessment implementation (factors: nature, unauthorized person,
  whether PHI was acquired/viewed, extent of risk mitigation).
- Check for breach logging and documentation.

MEANINGFUL USE / PROMOTING INTEROPERABILITY:
- Clinical decision support: are CDS alerts implemented?
- e-Prescribing: check for NCPDP SCRIPT standard support.
- Health information exchange: verify ability to send/receive clinical documents.
- Patient engagement: check for patient portal features (view/download/transmit).
- Public health reporting: check for immunization, syndromic surveillance interfaces.

BUSINESS ASSOCIATE AGREEMENTS:
- Search for BAA references in configuration, documentation, or code comments.
- Identify third-party services that handle PHI (cloud providers, analytics, etc.).
- Flag third-party integrations that process PHI without BAA documentation.
- Check subcontractor chain -- do downstream services also need BAAs?

============================================================
PHASE 4: 21ST CENTURY CURES ACT COMPLIANCE
============================================================

Scan for Cures Act requirements:

INFORMATION BLOCKING:
- Check if APIs restrict patient access to their own data.
- Verify no unnecessary delays in data availability.
- Check for paywalls blocking standard data access.
- Verify bulk FHIR export capability (if applicable).
- Check for USCDI (US Core Data for Interoperability) data class support.

PATIENT ACCESS API:
- Verify FHIR R4 Patient Access API endpoints exist (if applicable).
- Check for proper OAuth2/SMART on FHIR authorization flows.
- Verify patient-facing token management.
- Check scope restrictions -- patients should access their own data.

PROVIDER DIRECTORY API:
- Check for provider directory endpoints (if applicable).
- Verify NPI, specialty, location data availability.

ELECTRONIC HEALTH INFORMATION (EHI) EXPORT:
- Check for EHI export functionality.
- Verify export includes all designated record set data.
- Check export format (FHIR preferred, CCDA acceptable).

============================================================
PHASE 5: STATE REGULATION SCAN
============================================================

Scan codebase for state-specific compliance indicators:

STATE LAW REFERENCES:
- Search for state abbreviations in compliance-related code/config.
- Look for state-specific consent requirements (e.g., California CMIA,
  New York Public Health Law, Texas HB 300).
- Check for minor consent handling (age varies by state).

SENSITIVE CONDITION HANDLING:
- Mental health records: additional protections (42 CFR Part 2 for substance abuse).
- HIV/AIDS: many states require separate consent for disclosure.
- Genetic information: GINA compliance + state genetic privacy laws.
- Reproductive health: state-varying disclosure restrictions.
- Search for condition-code-based access restrictions.

DATA RESIDENCY:
- Check for data residency configuration (some states restrict PHI storage location).
- Verify cloud provider region configuration.
- Flag any cross-border data transfer without appropriate controls.

============================================================
PHASE 6: INFRASTRUCTURE AND DEPLOYMENT REVIEW
============================================================

Scan deployment configuration for compliance:

ENVIRONMENT SECURITY:
- Check Docker/container configurations for PHI exposure (env vars, logs).
- Verify secrets management (Vault, AWS Secrets Manager, etc. -- not plaintext).
- Check CI/CD pipelines for PHI in test data or logs.
- Verify production environment isolation from development.

DATA BACKUP AND RECOVERY:
- Search for backup configuration (frequency, encryption, retention).
- Check for disaster recovery documentation or configuration.
- Verify backup encryption matches production encryption standards.

MONITORING AND ALERTING:
- Check for intrusion detection / anomaly detection configuration.
- Verify PHI access monitoring (unusual access patterns).
- Check for failed authentication alerting.

============================================================
OUTPUT
============================================================

## Healthcare Compliance Audit Report

**Project:** [name]
**Stack:** [detected technologies]
**Application Type:** [EHR/portal/telehealth/billing/etc.]
**Date:** [date]

### Regulatory Coverage Summary

| Regulation | Status | Critical | High | Medium | Low |
|---|---|---|---|---|---|
| HIPAA Privacy Rule | [PASS/WARN/FAIL] | N | N | N | N |
| HIPAA Security Rule | [PASS/WARN/FAIL] | N | N | N | N |
| HITECH Act | [PASS/WARN/FAIL] | N | N | N | N |
| 21st Century Cures Act | [PASS/WARN/FAIL] | N | N | N | N |
| State Regulations | [PASS/WARN/FAIL/N/A] | N | N | N | N |
| Infrastructure | [PASS/WARN/FAIL] | N | N | N | N |

### PHI Data Flow Map
[Diagram or description of where PHI enters, is stored, processed, and exits the system]

### Detailed Findings

For each regulation with WARN or FAIL:

#### [Regulation — Section]

| # | Severity | File | Line | Rule | Description | Fix |
|---|----------|------|------|------|-------------|-----|
| 1 | Critical | path/to/file.ts | 42 | HIPAA 164.312(a)(1) | Description | Fix |

### Risk Assessment
- **Critical findings:** N (regulatory violation, immediate remediation required)
- **High findings:** N (likely violation, fix before next release)
- **Medium findings:** N (potential gap, plan remediation)
- **Low findings:** N (best practice recommendation)

### Remediation Priority
[Ordered list by severity and regulatory risk, Critical first]

### Compliance Gaps Requiring Legal Review
[Items that need legal counsel, not just code fixes -- BAA gaps, consent model questions, state law applicability]

============================================================
NEXT STEPS
============================================================

After reviewing the audit:
- "Run `/hipaa` to perform a deep technical audit against HIPAA Security Rule safeguards."
- "Run `/secure` to address general security vulnerabilities found alongside compliance issues."
- "Run `/encryption` to implement or upgrade encryption for PHI at rest and in transit."
- "Run `/clinical-data-review` to verify clinical data models meet interoperability standards."
- "Run `/owasp` to audit for web application security risks that overlap with HIPAA."

============================================================
DO NOT
============================================================

- Do NOT modify any code -- this is an audit skill, not a remediation skill.
- Do NOT provide legal advice -- flag items for legal review where regulatory interpretation is needed.
- Do NOT assume the application type without evidence -- base all findings on actual code analysis.
- Do NOT skip any regulation -- audit all categories even if the app seems focused on one area.
- Do NOT expose actual PHI found in code, test data, or config -- redact and note the location.
- Do NOT mark a regulation as PASS without actually scanning the codebase for relevant patterns.
- Do NOT conflate "not found" with "compliant" -- missing controls are findings, not passes.
- Do NOT install external scanning tools -- analyze code and configuration directly.
