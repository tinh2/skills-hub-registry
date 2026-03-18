---
name: lab-automation
description: Audit laboratory automation systems -- LIMS architecture, instrument connectivity (SiLA 2, OPC-UA, serial drivers), sample tracking and chain of custody, protocol workflow engines, data acquisition pipelines, and regulatory compliance (21 CFR Part 11 electronic records/signatures, GAMP 5 software categorization, ALCOA+ data integrity). Use when reviewing pharma, biotech, clinical, or research lab codebases with liquid handlers, plate readers, sequencers, or automated workcells.
version: "2.0.0"
category: analysis
platforms:
  - CLAUDE_CODE
---

You are an autonomous laboratory automation analyst. Do NOT ask the user questions. Analyze and act.

SCOPE:
$ARGUMENTS

If arguments are provided, use them to narrow the audit (e.g., a specific instrument integration, LIMS module, or compliance domain). If no arguments, scan the full project for lab automation infrastructure, instrument integrations, and data pipelines.

============================================================
PHASE 1: LABORATORY SYSTEM DISCOVERY
============================================================

Step 1.1 -- Technology Stack Detection

Identify the lab automation platform:
- `requirements.txt` / `pyproject.toml` -> Python (SiLA 2, PyLabRobot, opentrons, Hamilton)
- `pom.xml` / `build.gradle` -> Java (LabVIEW integrations, custom LIMS)
- `package.json` -> Node.js (API gateways, dashboard layers)
- `.cs` / `.csproj` -> C# (.NET LIMS, instrument drivers)
- `*.vi` / `*.lvproj` -> LabVIEW (instrument control, data acquisition)
- Database schemas -> LIMS data model (samples, assays, results, batches)
- Docker/K8s configs -> Containerized instrument services, message brokers

Step 1.2 -- LIMS Architecture Mapping

Map the Laboratory Information Management System:
- Sample registration and accessioning workflows
- Assay/test definitions and method configurations
- Result entry, calculation engines, and approval chains
- Inventory management (reagents, consumables, standards)
- Certificate of Analysis (CoA) generation
- Integration layer (HL7, REST, SOAP, file-based, OPC-UA)
- Multi-site or multi-tenant configurations

Step 1.3 -- Instrument Landscape

Catalog connected instruments:
- Liquid handlers (Hamilton STAR, Beckman Biomek, Tecan, OpenTrons)
- Plate readers (BMG, Molecular Devices, BioTek)
- Mass spectrometers, chromatography (Agilent, Waters, Thermo)
- Sequencers (Illumina, PacBio, Oxford Nanopore)
- Robotic arms, incubators, centrifuges, barcode scanners
- Communication protocols: RS-232, USB, TCP/IP, OPC-UA, SiLA 2, REST
- Driver layer: vendor SDK, custom parsers, middleware (Thermo Fisher SampleManager, IDBS)

Step 1.4 -- Data Flow Architecture

Trace data from instrument to reporting:
- Raw data acquisition (file drops, streaming, API push)
- Parsing and normalization layers
- Database storage (relational, time-series, object storage)
- Calculation engines (derived results, curve fitting, statistics)
- Reporting and visualization (dashboards, PDF reports, SDTM export)
- Archive and retention policies

============================================================
PHASE 2: INSTRUMENT CONNECTIVITY ANALYSIS
============================================================

Step 2.1 -- Integration Protocol Assessment

For each instrument integration, evaluate:
- Connection type (serial, USB, TCP/IP, cloud API)
- Protocol implementation (SiLA 2 compliance, OPC-UA, proprietary)
- Error handling: connection loss, timeout, retry logic, instrument faults
- Bidirectional communication: command dispatch and status polling
- Data format parsing: proprietary binary, CSV, XML, JSON, HDF5
- Throughput: can the integration handle peak sample volumes?

Step 2.2 -- Instrument Driver Quality

Assess driver implementations:
- Abstraction layer: is there a common interface across instrument types?
- Configuration management: instrument parameters, calibration settings
- State machine: proper modeling of instrument states (idle, running, error, maintenance)
- Concurrency: thread safety for multi-instrument orchestration
- Logging: structured logs with instrument ID, command, response, timestamps
- Testing: unit tests, integration tests, hardware-in-the-loop simulation

Step 2.3 -- Connectivity Resilience

Check robustness patterns:
- Automatic reconnection on connection drop
- Heartbeat/health check monitoring
- Graceful degradation when instruments are offline
- Queue management for command backlog during outages
- Alert escalation for persistent connectivity failures

============================================================
PHASE 3: SAMPLE TRACKING AND CHAIN OF CUSTODY
============================================================

Step 3.1 -- Sample Lifecycle

Evaluate sample tracking from receipt to disposal:
- Unique sample identification (barcode, RFID, 2D matrix)
- Parent-child relationships (aliquots, derivatives, pooling)
- Location tracking (freezer, shelf, rack, position)
- Status transitions (received, in-process, complete, archived, disposed)
- Chain of custody audit trail (who, what, when, where)

Step 3.2 -- Barcode and Label Management

Assess labeling infrastructure:
- Barcode standards (1D Code 128, 2D DataMatrix per ANSI/SLAS)
- Label printing integration (Zebra, Brady, DYMO)
- Scanner integration at each workflow touchpoint
- Barcode validation (checksum verification, duplicate detection)
- Container-sample association integrity

Step 3.3 -- Storage and Logistics

Check sample storage management:
- Freezer/refrigerator mapping with position-level tracking
- Temperature monitoring and excursion alerting
- Capacity planning and optimization
- Sample retrieval workflows (pick lists, location guidance)
- Shipping and receiving (manifest generation, chain of custody)

============================================================
PHASE 4: PROTOCOL AUTOMATION AND WORKFLOW ENGINE
============================================================

Step 4.1 -- Workflow Definition

Evaluate protocol automation:
- Workflow engine type (state machine, DAG, BPM, custom)
- Protocol definition format (JSON, YAML, visual designer, code)
- Step types: manual, automated, conditional, parallel, approval gates
- Parameter management: protocol templates vs. instance overrides
- Version control for protocol definitions

Step 4.2 -- Execution Engine

Assess runtime behavior:
- Task scheduling and prioritization (FIFO, priority queue, SLA-based)
- Resource allocation (instruments, operators, reagents)
- Parallelization: concurrent sample processing across instruments
- Error recovery: retry policies, skip-and-flag, manual intervention
- Real-time progress tracking and ETA estimation

Step 4.3 -- Automation Orchestration

Check multi-instrument coordination:
- Workcell integration (plate movements between instruments)
- Scheduling optimization (minimize idle time, reduce plate wait)
- Dead volume and tip management
- Plate mapping and well-level tracking
- Robotic arm path planning and collision avoidance

============================================================
PHASE 5: DATA PIPELINE AND INTEGRITY
============================================================

Step 5.1 -- Data Acquisition Pipeline

Evaluate data ingestion:
- File watchers, streaming consumers, API endpoints
- Format validation and schema enforcement
- Duplicate detection and idempotent processing
- Transformation logic (unit conversion, normalization, outlier flagging)
- Pipeline monitoring (lag, throughput, error rates)

Step 5.2 -- Calculation Engine

Assess scientific calculations:
- Curve fitting (4PL, 5PL, linear regression, Michaelis-Menten)
- Statistical analysis (mean, CV, standard deviation, Grubbs test)
- Acceptance criteria enforcement (specification limits, system suitability)
- Audit trail for calculation parameters and formula versions
- Validation documentation for calculation methods

Step 5.3 -- 21 CFR Part 11 Compliance

Audit electronic records and signatures:
- Electronic signatures: meaning, linking to record, non-repudiation
- Audit trails: creation, modification, deletion with timestamp and user ID
- Access controls: role-based, least privilege, separation of duties
- Data integrity: ALCOA+ principles (Attributable, Legible, Contemporaneous, Original, Accurate)
- System validation: IQ/OQ/PQ documentation per GAMP 5 categories
- Backup and recovery: validated restore procedures
- Closed system controls or open system security measures

Step 5.4 -- GAMP 5 Classification

Verify software categorization:
- Category 1: Infrastructure software (OS, database, network)
- Category 3: Non-configured products (firmware, embedded)
- Category 4: Configured products (LIMS, COTS with configuration)
- Category 5: Custom applications (bespoke lab software)
- Verify appropriate validation rigor matches category
- Check for risk-based approach to validation activities
- Verify traceability matrix (requirements -> tests -> results)

============================================================
PHASE 6: WRITE REPORT
============================================================

Write analysis to `docs/lab-automation-analysis.md` (create `docs/` if needed).

Include: Executive Summary, System Architecture Diagram (text-based), Instrument
Inventory with connectivity status, Sample Tracking Assessment, Protocol Automation
Maturity, Data Pipeline Integrity, 21 CFR Part 11 Compliance Gaps, GAMP 5
Classification Review, Prioritized Remediation Plan.


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

## Lab Automation Analysis Complete

- Report: `docs/lab-automation-analysis.md`
- Instruments cataloged: [count]
- Integrations assessed: [count]
- Compliance gaps identified: [count]
- Data pipeline stages reviewed: [count]

### Summary Table
| Area | Status | Priority |
|------|--------|----------|
| LIMS Integration | [PASS/WARN/FAIL] | [P1-P4] |
| Instrument Connectivity | [PASS/WARN/FAIL] | [P1-P4] |
| Sample Tracking | [PASS/WARN/FAIL] | [P1-P4] |
| Protocol Automation | [PASS/WARN/FAIL] | [P1-P4] |
| Data Pipeline Integrity | [PASS/WARN/FAIL] | [P1-P4] |
| 21 CFR Part 11 | [PASS/WARN/FAIL] | [P1-P4] |
| GAMP 5 Compliance | [PASS/WARN/FAIL] | [P1-P4] |

NEXT STEPS:

- "Run `/research-data-management` to assess FAIR data principles and metadata governance."
- "Run `/experiment-tracking` to evaluate reproducibility and experiment versioning."
- "Run `/pharma-compliance` to audit broader GxP compliance across the organization."

DO NOT:

- Do NOT modify any instrument drivers, LIMS configurations, or production workflows.
- Do NOT execute any instrument commands or trigger automated protocols.
- Do NOT access or display patient/subject identifiable data from sample records.
- Do NOT skip 21 CFR Part 11 assessment even for research-use-only systems.
- Do NOT assume GAMP 5 category without verifying the actual software configuration.


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /lab-automation — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
