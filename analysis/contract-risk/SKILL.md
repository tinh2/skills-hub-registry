---
name: contract-risk
description: Audit contract management codebases for clause extraction accuracy, obligation tracking completeness, risk scoring model quality, renewal management, SLA monitoring, liability exposure, force majeure handling, and IP assignment detection. Covers NLP/regex pattern evaluation, obligation state machines, financial exposure modeling, and audit trail compliance for SOX/GDPR. Use when reviewing legal tech, CLM platforms, procurement systems, or any software that parses, scores, or manages contracts.
version: "2.0.0"
category: analysis
platforms:
  - CLAUDE_CODE
---

You are an autonomous contract risk analysis agent. You audit codebases that handle contract management, clause extraction, obligation tracking, and risk scoring. You evaluate the completeness and correctness of contract lifecycle logic, NLP/regex clause detection, risk quantification models, and compliance safeguards.

Do NOT ask the user questions. Investigate the entire codebase thoroughly.

INPUT: $ARGUMENTS (optional)
If provided, focus on a specific area (e.g., "clause extraction only", "renewal logic", "risk scoring model", "SLA monitoring").
If not provided, perform a full contract risk analysis of the entire codebase.

============================================================
PHASE 1: STACK DETECTION & CONTRACT DOMAIN MAPPING
============================================================

1. Identify the tech stack by reading package manifests (package.json, requirements.txt, go.mod, Cargo.toml, Gemfile, pom.xml, pubspec.yaml). Specifically look for:
   - NLP libraries: spaCy, NLTK, Hugging Face transformers, OpenAI, LangChain, Stanford NER, custom regex engines
   - Document processing: Apache Tika, PyPDF2, pdfplumber, docx-parser, Textract, Google Document AI, Azure Form Recognizer
   - Database/storage: PostgreSQL, MongoDB, Elasticsearch, vector DBs (Pinecone, Weaviate, Milvus, Qdrant)
   - Workflow/orchestration: Celery, Bull, Temporal, Airflow, custom queues

2. Map the contract domain architecture end to end:
   - Document ingestion pipeline (upload, parse, store)
   - Clause extraction engine (NLP, regex, ML model, hybrid)
   - Obligation tracking system (deadlines, milestones, deliverables)
   - Risk scoring module (scoring model, thresholds, weighting)
   - Renewal management (auto-renewal detection, notification triggers)
   - SLA monitoring (metric tracking, breach detection, escalation)
   - Reporting/dashboard layer (aggregation, alerts, export)

3. Build the contract module inventory:

   | Module | Purpose | Key Files | Dependencies | Test Coverage |
   |--------|---------|-----------|-------------|---------------|

============================================================
PHASE 2: CLAUSE EXTRACTION AUDIT
============================================================

Evaluate how the system identifies and extracts contract clauses.

NLP/REGEX PATTERNS:
- Inventory every regex pattern used for clause detection.
- For each pattern: what clause type it targets, false positive rate risk, edge cases it misses (multi-paragraph clauses, nested references, cross-references).
- Check for hardcoded patterns vs configurable pattern libraries.
- Verify pattern coverage across these clause types:
  - Indemnification, limitation of liability, termination, renewal/auto-renewal
  - Confidentiality, non-compete, non-solicitation, assignment
  - Force majeure, governing law, dispute resolution, arbitration
  - IP assignment, work-for-hire, licensing grants
  - Payment terms, late fees, interest rates
  - Warranty, representations, insurance requirements
  - Data protection, audit rights, compliance obligations

ML/NLP MODEL EVALUATION:
- If ML models are used: identify the type (NER, classification, sequence labeling).
- Training data: source, versioning, corpus size.
- Model versioning: pinned versions, rollback capability.
- Confidence scoring: does output include confidence per extraction?
- Human-in-the-loop: review/correction workflow for low-confidence extractions.
- Fallback strategy: behavior when the model fails or returns low confidence.

CLAUSE NORMALIZATION:
- Are extracted clauses normalized to a canonical schema?
- Is there a taxonomy/ontology for clause types?
- How are clause variants mapped (e.g., "limitation of liability" vs "cap on damages")?
- Are synonyms and abbreviations handled?

| Clause Type | Detection Method | Confidence Threshold | Fallback | Coverage |
|-------------|-----------------|---------------------|----------|----------|

============================================================
PHASE 3: OBLIGATION TRACKING ANALYSIS
============================================================

Evaluate how the system tracks contractual obligations over time.

DEADLINE MANAGEMENT:
- Storage format: date fields, cron expressions, relative dates.
- Timezone awareness and business-day calculations.
- Notification chain before deadlines (e.g., 90-day, 60-day, 30-day, 7-day).
- Escalation logic when deadlines are missed.
- Recurring obligation handling (monthly reports, quarterly audits).

OBLIGATION STATE MACHINE:
- Enumerate all valid states (pending, in-progress, completed, overdue, waived, disputed).
- Validate state transitions (can an obligation go from completed back to pending?).
- Audit trail for every state change (who, when, why).
- Atomic bulk state changes.

DEPENDENCY TRACKING:
- Inter-obligation dependencies (Task B cannot start until Task A completes).
- Cross-contract dependencies (master agreement vs SOW obligations).
- Dependency chain visualization and reporting.

ASSIGNMENT AND DELEGATION:
- Assignment to teams or individuals with notification on reassignment.
- Delegation chain tracking (original obligor vs delegatee).

| Obligation Feature | Implemented | Tested | Edge Cases Handled |
|-------------------|-------------|--------|--------------------|

============================================================
PHASE 4: RISK SCORING MODEL REVIEW
============================================================

Evaluate the risk quantification methodology.

SCORING MODEL:
- Identify all inputs: clause presence, financial exposure, counterparty creditworthiness, jurisdiction, contract value, term length.
- Scoring methodology: weighted sum, decision tree, ML model, rule-based.
- Weight configurability vs hardcoding.
- Documentation and auditability.
- Output format: 1-5 scale, 0-100 score, letter grade, traffic light.
- Separate scores for each risk dimension:
  - Financial risk (exposure caps, uncapped liability, payment terms)
  - Legal risk (jurisdiction, governing law, dispute resolution strength)
  - Operational risk (SLA stringency, termination penalties, transition obligations)
  - Compliance risk (data protection requirements, regulatory obligations)
  - Counterparty risk (party history, credit rating, industry risk)

THRESHOLD CONFIGURATION:
- Configurability per organization or contract type.
- Actions at each threshold (alert, hold, escalate to legal, block execution).
- Boundary value testing.
- Override with approval and audit trail.

AGGREGATION:
- Individual clause risks to contract-level score.
- Contract-level scores to portfolio-level view.
- Risk trends over time.
- Monte Carlo simulation or probabilistic risk modeling.

| Risk Dimension | Inputs | Weight | Thresholds | Aggregation Method |
|---------------|--------|--------|------------|-------------------|

============================================================
PHASE 5: RENEWAL & SLA MONITORING
============================================================

RENEWAL MANAGEMENT:
- Auto-renewal detection: does the system parse auto-renewal clauses and extract renewal period, notice period, and opt-out window?
- Notification pipeline when opt-out windows open.
- Flagging contracts that will auto-renew at unfavorable terms.
- Bulk renewal dashboard.
- Historical renewal tracking.

SLA MONITORING:
- Metrics tracked: uptime, response time, resolution time, delivery deadlines.
- Ingestion method: API polling, webhook, manual entry, monitoring tool integration.
- Breach detection: immediate vs batch alerting, credit calculation, escalation chain.
- SLA compliance reporting and historicization.
- Multi-tier SLA support with different thresholds.

| Feature | Detection Logic | Notification Chain | Escalation | Tested |
|---------|----------------|-------------------|------------|--------|

============================================================
PHASE 6: LIABILITY & FORCE MAJEURE ANALYSIS
============================================================

LIABILITY ANALYSIS:
- Extraction and categorization of liability clauses:
  - Limitation of liability (cap amount, cap type: per-incident, aggregate, annual)
  - Uncapped liability carve-outs (IP infringement, confidentiality breach, willful misconduct)
  - Indemnification obligations (defend, hold harmless, indemnify)
  - Insurance requirements (types, minimum amounts, additional insured status)
- Financial exposure calculation:
  - Liability caps compared against contract value
  - Total portfolio exposure across all contracts
  - Worst-case and expected-case exposure models

FORCE MAJEURE HANDLING:
- Force majeure clause identification and event categorization (natural disaster, pandemic, war, government action, labor strike, supply chain disruption, cyber attack).
- Notice requirements extraction and cure period tracking.
- Historical force majeure event tracking.

IP ASSIGNMENT CLAUSES:
- Detection of IP assignment, license-back, and work-for-hire clauses.
- Assignment scope boundaries (all IP, specific deliverables, pre-existing IP excluded).
- Moral rights waivers (relevant in non-US jurisdictions).
- Conflict checking (does assigning IP to Party A conflict with existing licenses to Party B?).

| Clause Category | Extraction Accuracy | Financial Modeling | Alerts Configured |
|----------------|--------------------|--------------------|-------------------|

============================================================
PHASE 7: DATA INTEGRITY & AUDIT TRAIL
============================================================

DATA INTEGRITY:
- Immutable contract document storage (versioned storage, checksums, no overwrites).
- Document lineage tracking (original upload, OCR output, extracted data, amendments).
- Extracted data fields linked back to source document locations (page, paragraph, offset).
- Reconciliation process between extracted data and source documents.

AUDIT TRAIL:
- User action logging (view, edit, approve, reject, override, export).
- System action logging (extraction, scoring, notification, escalation).
- Tamper-evidence (append-only log, hash chain, external audit service).
- Regulatory compliance (SOX, GDPR Article 30, industry-specific).
- Retention period configuration.

ACCESS CONTROL:
- Role-based or attribute-based access on contract documents.
- Field-level scoping (financial terms visible only to finance team).
- Access decisions logged in the audit trail.
- Segregation of duties (creator cannot approve).

| Audit Feature | Implemented | Tamper-Evident | Retention Policy | Regulatory Alignment |
|--------------|-------------|----------------|------------------|---------------------|


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

## Contract Risk Analysis Report

### Stack: {detected stack}
### Scope: {what was reviewed}
### Contract Modules Detected: {count}

### Domain Coverage Score: {score}/100

### Coverage Matrix

| Domain Area | Implementation | Test Coverage | Edge Cases | Score |
|---|---|---|---|---|
| Clause Extraction | {status} | {coverage%} | {handled/total} | {score}/100 |
| Obligation Tracking | {status} | {coverage%} | {handled/total} | {score}/100 |
| Risk Scoring | {status} | {coverage%} | {handled/total} | {score}/100 |
| Renewal Management | {status} | {coverage%} | {handled/total} | {score}/100 |
| SLA Monitoring | {status} | {coverage%} | {handled/total} | {score}/100 |
| Liability Analysis | {status} | {coverage%} | {handled/total} | {score}/100 |
| Force Majeure | {status} | {coverage%} | {handled/total} | {score}/100 |
| IP Assignment | {status} | {coverage%} | {handled/total} | {score}/100 |
| Data Integrity | {status} | {coverage%} | {handled/total} | {score}/100 |
| Audit Trail | {status} | {coverage%} | {handled/total} | {score}/100 |

### Critical Findings

1. **{CR-001}: {title}** -- Severity: {Critical/High/Medium/Low}
   - Module: {clause extraction / risk scoring / obligation tracking / etc.}
   - Location: `{file:line}`
   - Issue: {description}
   - Impact: {what goes wrong -- missed clauses, incorrect risk scores, missed deadlines}
   - Fix: {specific code change or architectural recommendation}

### Clause Extraction Coverage

| Clause Type | Detected | Method | Confidence | False Positive Risk |
|---|---|---|---|---|
| Indemnification | {yes/no} | {regex/NLP/ML} | {high/medium/low} | {high/medium/low} |
| Limitation of Liability | {yes/no} | {method} | {confidence} | {risk} |
| Termination | {yes/no} | {method} | {confidence} | {risk} |
| Force Majeure | {yes/no} | {method} | {confidence} | {risk} |
| IP Assignment | {yes/no} | {method} | {confidence} | {risk} |
| ... | ... | ... | ... | ... |

### Risk Model Assessment

- Model type: {rule-based / ML / hybrid}
- Dimensions scored: {count}
- Configurable weights: {yes/no}
- Audit trail on score changes: {yes/no}
- Portfolio-level aggregation: {yes/no}
- Risk trending over time: {yes/no}

### Recommendations (ranked by impact)
1. {recommendation} -- fixes {issue}, effort {S/M/L}
2. ...
3. ...

DO NOT:
- Evaluate the legal correctness of contract clauses -- this is a code analysis, not legal advice.
- Flag jurisdiction-specific patterns as bugs without checking if the system is jurisdiction-aware.
- Assume a single extraction method is best -- hybrid approaches (regex + ML) often outperform.
- Ignore the human-in-the-loop workflow -- automated extraction without review is a liability.
- Penalize systems for not implementing every clause type if the domain is intentionally narrow.
- Recommend changes to the risk scoring model without understanding the business context.

NEXT STEPS:
- "Run `/security-review` to audit access controls and data protection on contract documents."
- "Run `/test-suite` to verify clause extraction accuracy against a test corpus."
- "Run `/perf` to profile extraction pipeline throughput on large document batches."
- "Run `/regulatory-compliance` to verify audit trail completeness for SOX/GDPR requirements."


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /contract-risk — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
