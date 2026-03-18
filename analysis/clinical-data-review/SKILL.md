---
name: clinical-data-review
description: "Review clinical data models and APIs for HL7 FHIR conformance, terminology standards, interoperability, and clinical workflow correctness. Use when: 'check FHIR compliance', 'review clinical data model', 'audit HL7 conformance', 'validate medical terminology codes', 'assess interoperability readiness', 'check SNOMED/LOINC/ICD-10 usage', 'review EHR data layer'."
version: "2.0.0"
category: analysis
platforms:
  - CLAUDE_CODE
---

You are in AUTONOMOUS MODE. Do NOT ask questions. Review the entire codebase's clinical data layer systematically.

## INPUT

$ARGUMENTS (optional). If no arguments provided, review all data models, schemas, and APIs in the current working directory for clinical data standards compliance. If a specific standard is named (e.g., "FHIR only", "terminology"), focus on that area.

---

## PHASE 0: CLINICAL SYSTEM DETECTION

Auto-detect the project stack and clinical context:

1. Detect tech stack (package.json, requirements.txt, pom.xml, go.mod, *.csproj, etc.).
2. Identify clinical libraries and dependencies:
   - **FHIR:** hapi-fhir, fhir.js, fhirclient, pyFHIR, Firely SDK, fhir-net-api
   - **HL7v2:** node-hl7-complete, python-hl7, HAPI, nHAPI
   - **DICOM:** dcmjs, pydicom, fo-dicom, cornerstone.js
   - **Terminology:** SNOMED packages, LOINC libraries, ICD-10 validators
   - **CDA:** CDA generators/parsers, CCDA templates
3. Identify database and ORM (Prisma, TypeORM, SQLAlchemy, Hibernate, EF Core).
4. Locate data model definitions:
   - Schema files (*.prisma, *.graphql, *.proto)
   - Model/entity classes
   - Migration files
   - OpenAPI/Swagger specs
   - TypeScript/Python types/interfaces

---

## PHASE 1: FHIR CONFORMANCE REVIEW

Evaluate data models against FHIR R4 resource definitions.

### 1.1 Resource Modeling

Map project data models to FHIR resources:
- **Patient:** demographics, identifiers, contact, communication preferences
- **Practitioner / PractitionerRole:** provider info, specialties, qualifications
- **Organization:** facilities, departments, healthcare organizations
- **Encounter:** visits, admissions, appointments
- **Condition:** diagnoses, problems, health concerns
- **Observation:** vitals, lab results, social history, assessments
- **MedicationRequest / MedicationStatement:** prescriptions, current meds
- **AllergyIntolerance:** allergies, adverse reactions
- **Procedure:** surgical, diagnostic, therapeutic procedures
- **DiagnosticReport:** lab reports, imaging reports, pathology
- **DocumentReference:** clinical documents, notes, external records
- **CarePlan:** treatment plans, goals, activities
- **Immunization:** vaccination records

For each mapped resource, check:
- Required FHIR elements present (status, subject, code, etc.).
- Correct cardinality (0..1, 0..*, 1..1, 1..*).
- Proper data types (CodeableConcept vs string, Reference vs ID, Period vs DateTime).
- Resource references use proper Reference type with resource type + ID.
- Extensions are properly defined (not ad-hoc fields breaking FHIR structure).

### 1.2 Search Parameters
- Verify FHIR search parameter support on API endpoints.
- Check standard search params: _id, _lastUpdated, _tag, _profile.
- Check resource-specific params: Patient?name, Observation?code, etc.
- Verify search modifiers: :exact, :contains, :missing.
- Check chained search support: Observation?subject:Patient.name.
- Verify _include and _revinclude support.

### 1.3 Capability Statement
- Check for /metadata endpoint returning CapabilityStatement resource.
- Verify it accurately reflects implemented resources and operations.
- Check for declared profiles and supported search parameters.

### 1.4 Bundle Support
- Verify transaction Bundle support (POST to root with type: transaction).
- Check for batch Bundle support.
- Verify searchset Bundle response format for search endpoints.
- Check Bundle entry fullUrl and resource consistency.

---

## PHASE 2: TERMINOLOGY AND CODING STANDARDS

### 2.1 ICD-10 (Diagnoses)
- Search for ICD-10-CM code handling in data models and business logic.
- Verify code format validation (letter + 2 digits + optional decimal + up to 4 digits).
- Check for code versioning (ICD-10 updates annually in October).
- Verify code descriptions are stored or lookable.
- Check for ICD-10-PCS (procedure codes) if surgical/procedural data exists.
- Flag hardcoded ICD-10 codes without version tracking.

### 2.2 CPT / HCPCS (Procedures and Services)
- Search for CPT code handling in billing, orders, or procedure models.
- Verify CPT code validation (5 digits or 4 digits + letter).
- Check for HCPCS Level II codes (letter + 4 digits) for supplies/equipment.
- Verify modifier support (CPT modifiers: -25, -59, -76, etc.).
- Check for annual code updates handling.

### 2.3 SNOMED CT (Clinical Terms)
- Search for SNOMED concept IDs in data models.
- Verify SNOMED codes use proper SCTID format (6-18 digit numeric).
- Check for concept hierarchy navigation capability.
- Verify SNOMED-to-ICD-10 mapping if cross-coding is needed.
- Check for SNOMED version/edition tracking.

### 2.4 LOINC (Lab and Observations)
- Search for LOINC codes in observation/lab models.
- Verify LOINC code format validation (numeric with optional dash and check digit).
- Check for proper units of measure (UCUM standard) paired with LOINC codes.
- Verify lab result value sets align with LOINC answer lists.

### 2.5 RxNorm (Medications)
- Search for medication coding in prescription/medication models.
- Check for RxNorm concept unique identifiers (RxCUI).
- Verify NDC (National Drug Code) handling if pharmacy integration exists.
- Check for drug-drug interaction checking capability.

### 2.6 Terminology Service
- Check for terminology server integration ($lookup, $validate-code, $expand).
- Verify ValueSet binding on coded fields.
- Check for CodeSystem resources or external terminology service configuration.
- Flag coded fields that accept free text without code validation.

---

## PHASE 3: INTEROPERABILITY ASSESSMENT

### 3.1 CDA / CCDA Documents
- Search for CDA document generation or parsing.
- Check for CCDA template conformance (CCD, Discharge Summary, Progress Note, etc.).
- Verify required sections: allergies, medications, problems, procedures, results.
- Check for structured vs narrative-only sections.
- Verify XML schema validation on generated documents.

### 3.2 Bulk Data Export
- Check for FHIR Bulk Data Access ($export) implementation.
- Verify NDJSON output format.
- Check for group-level and system-level export support.
- Verify async export pattern (kick-off, status polling, file download).

### 3.3 ADT Messaging
- Search for HL7v2 ADT (Admit/Discharge/Transfer) message handling.
- Check for A01 (admit), A02 (transfer), A03 (discharge), A04 (register), A08 (update) message type support.
- Verify PID, PV1, NK1 segment parsing/generation.

### 3.4 ORU / ORM Messaging
- Search for HL7v2 ORU (results) and ORM (orders) message handling.
- Check for OBR, OBX segment handling in results.
- Verify order/result linking via placer/filler order numbers.

### 3.5 Direct Messaging
- Check for Direct protocol support (secure email for clinical data).
- Verify S/MIME encryption compliance.

---

## PHASE 4: CLINICAL WORKFLOW VALIDATION

### 4.1 Order Management
- Check order lifecycle: draft -> active -> completed/cancelled.
- Verify order validation (appropriate order for patient context).
- Check for duplicate order detection.
- Verify order modification and cancellation workflows.
- Check for clinical decision support at order entry.

### 4.2 Results Management
- Verify result status workflow: preliminary -> final -> corrected -> amended.
- Check for abnormal result flagging (reference ranges, critical values).
- Verify result acknowledgment tracking.
- Check for result routing based on ordering provider.

### 4.3 Medication Management
- Check prescription lifecycle: draft -> active -> stopped/completed.
- Verify drug allergy checking against patient allergies.
- Check for formulary validation.
- Verify medication reconciliation support.
- Check for e-prescribing (NCPDP SCRIPT) readiness.

### 4.4 Documentation
- Check for clinical note types (progress notes, H&P, discharge summary).
- Verify note signing/cosigning workflow.
- Check for addendum support (append, not edit).
- Verify template support for structured documentation.

### 4.5 Data Quality
- Check for required field enforcement on critical clinical data.
- Verify referential integrity between related clinical records.
- Check for data validation rules (date ranges, numeric ranges, code validation).
- Verify duplicate detection mechanisms (patient matching, record deduplication).

---


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

## OUTPUT FORMAT

```
## Clinical Data Model Review

**Project:** [name]
**Stack:** [detected technologies]
**Clinical Domain:** [EHR/lab/pharmacy/imaging/billing/etc.]
**Date:** [date]

### Standards Conformance Summary

| Standard | Coverage | Conformance | Issues |
|---|---|---|---|
| FHIR R4 | [N resources mapped] | [FULL/PARTIAL/NONE] | N |
| ICD-10-CM/PCS | [usage found?] | [VALID/PARTIAL/NONE] | N |
| CPT/HCPCS | [usage found?] | [VALID/PARTIAL/NONE] | N |
| SNOMED CT | [usage found?] | [VALID/PARTIAL/NONE] | N |
| LOINC | [usage found?] | [VALID/PARTIAL/NONE] | N |
| RxNorm | [usage found?] | [VALID/PARTIAL/NONE] | N |
| CDA/CCDA | [support found?] | [CONFORMANT/PARTIAL/NONE] | N |
| HL7v2 | [usage found?] | [VALID/PARTIAL/NONE] | N |

### FHIR Resource Mapping

| Project Model | FHIR Resource | Required Elements | Missing Elements | Extensions |
|---|---|---|---|---|
| [model name] | Patient | [present] | [missing] | [non-standard fields] |

### Data Model Findings

| # | Severity | File | Model/Field | Standard | Issue | Fix |
|---|----------|------|-------------|----------|-------|-----|
| 1 | High | path/to/model.ts | Patient.identifier | FHIR R4 | Missing system URI on identifier | Add system field per FHIR Identifier datatype |

### Terminology Gaps

| Coded Field | Current Implementation | Required Standard | Gap |
|---|---|---|---|
| [diagnosis_code] | Free text string | ICD-10-CM CodeableConcept | No code validation, no system URI |

### Interoperability Readiness
- FHIR API: [Ready/Partial/Not implemented]
- Bulk Export: [Ready/Partial/Not implemented]
- CDA/CCDA: [Ready/Partial/Not implemented]
- HL7v2: [Ready/Partial/Not implemented]
- Patient matching: [algorithm used or none]

### Clinical Workflow Assessment
| Workflow | Status | Key Gaps |
|---|---|---|
| Order management | [Complete/Partial/Missing] | [gaps] |
| Results delivery | [Complete/Partial/Missing] | [gaps] |
| Medication mgmt | [Complete/Partial/Missing] | [gaps] |
| Documentation | [Complete/Partial/Missing] | [gaps] |
```

---

## RULES

- Do NOT modify any code -- this is a review skill, not a build skill.
- Do NOT assume FHIR compliance from library presence alone -- verify actual resource structure.
- Do NOT accept free-text fields as valid coded data -- flag missing terminology binding.
- Do NOT skip checking cardinality and data types against FHIR spec.
- Do NOT ignore custom extensions -- evaluate if standard FHIR elements would suffice.
- Do NOT treat terminology code presence as validation -- verify format and system URI.
- Do NOT overlook data quality rules -- missing validation is a finding.
- Do NOT install external tools or FHIR validators -- analyze schemas and code directly.

---

## NEXT STEPS

- "Run `/healthcare-compliance` to audit regulatory compliance of the clinical data layer."
- "Run `/compliance-ops` to evaluate broader organizational compliance operations."
- "Run `/api-surface` to evaluate API design patterns for clinical endpoints."


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /clinical-data-review — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
