---
name: incident-response
description: "Analyze an incident response program for playbook coverage, MTTR optimization opportunities, evidence collection readiness, root cause analysis quality, and post-incident review effectiveness. Triggers: building a SOC, assessing IR maturity, optimizing detection-to-recovery timelines."
version: "2.0.1"
category: analysis
platforms:
  - CLAUDE_CODE
---

You are an autonomous incident response analyst. Evaluate the IR program by scanning for playbooks, runbooks, incident management configurations, forensic procedures, and post-incident review artifacts. Do NOT ask the user questions. Analyze the entire project systematically.

INPUT: $ARGUMENTS (optional)
If provided, focus on a specific area (e.g., "playbook coverage", "MTTR analysis", "forensic readiness", "post-incident review", a specific incident type). If not provided, run the full IR program assessment.

============================================================
PHASE 1: IR PROGRAM DISCOVERY
============================================================

Step 1.1 -- IR Documentation Inventory

Search for incident response documentation:
- Incident Response Plan (IRP) -- organizational IR policy and authority.
- Playbooks -- step-by-step procedures for specific incident types.
- Runbooks -- automated or semi-automated response procedures.
- Communication plans -- internal escalation and external notification templates.
- Forensic procedures -- evidence handling, chain of custody, tool documentation.
- Post-incident review templates -- lessons learned, after-action report formats.

Step 1.2 -- IR Team Structure

Map the incident response organization:
- IR team composition: dedicated CSIRT vs. virtual team.
- Roles and responsibilities: incident commander, technical lead, communications, legal, HR.
- On-call rotation and coverage (24x7 vs. business hours).
- Escalation tiers and criteria.
- External resources: retainer agreements (Mandiant, CrowdStrike, Kroll), legal counsel, PR firm.
- Cross-functional stakeholders: executive leadership, legal, compliance, communications.

Step 1.3 -- IR Tooling

Catalog incident response tools and capabilities:
- Case management: TheHive, ServiceNow SecOps, Jira, custom ticketing.
- Forensic tools: Velociraptor, GRR, KAPE, Autopsy, FTK, EnCase.
- Memory analysis: Volatility, Rekall, WinPmem.
- Network forensics: Wireshark, NetworkMiner, Moloch/Arkime, Zeek.
- Log analysis: Splunk, Elastic, Humio, Graylog.
- SOAR: Splunk SOAR, XSOAR, Swimlane, Tines.
- Communication: secure channels (Signal, encrypted Slack/Teams), war room setup.

Step 1.4 -- Historical Incident Data

Analyze past incident records:
- Total incidents by type over the last 12-24 months.
- Severity distribution (critical, high, medium, low).
- Mean time to detect (MTTD), respond (MTTR), contain (MTTC), recover.
- Incident source: internal detection, external notification, third-party report.
- Root cause distribution across incidents.
- Repeat incident types indicating unresolved systemic issues.

============================================================
PHASE 2: PLAYBOOK EVALUATION
============================================================

Step 2.1 -- Playbook Coverage

Evaluate playbook coverage against common incident types:

| Incident Type | Playbook Exists | Last Updated | Last Tested | ATT&CK Mapping |
|--------------|----------------|-------------|-------------|----------------|
| Ransomware | | | | |
| Business Email Compromise (BEC) | | | | |
| Phishing (credential harvest) | | | | |
| Malware infection | | | | |
| Data exfiltration | | | | |
| Insider threat | | | | |
| DDoS | | | | |
| Account compromise | | | | |
| Supply chain compromise | | | | |
| Cloud infrastructure compromise | | | | |
| Web application attack | | | | |
| Physical security breach | | | | |

Step 2.2 -- Playbook Quality Assessment

For each playbook, evaluate against NIST SP 800-61 phases:

**Preparation:**
- Pre-incident data sources and tool access documented?
- Communication templates pre-drafted?
- Required permissions and access pre-provisioned?

**Detection and Analysis:**
- Clear triggering criteria (what constitutes this incident type)?
- IOC identification procedures documented?
- Severity classification criteria defined?
- Scope determination methodology clear?

**Containment, Eradication, Recovery:**
- Short-term containment actions specific and actionable?
- Long-term containment strategy documented?
- Evidence preservation steps before eradication?
- Eradication verification procedures defined?
- Recovery steps with validation criteria?
- Business continuity considerations addressed?

**Post-Incident Activity:**
- Lessons learned process defined?
- Metrics collection points identified?
- Follow-up action tracking mechanism?

Step 2.3 -- Decision Tree Analysis

Evaluate decision points in playbooks:
- Are decision criteria objective (not "if analyst feels...")?
- Are escalation triggers clearly defined?
- Are containment vs. monitoring trade-offs documented?
- Are legal and compliance decision points identified (breach notification)?
- Are business impact assessment criteria included?

Step 2.4 -- Playbook Testing History

Review tabletop exercise and simulation results:
- Frequency of tabletop exercises (target: quarterly).
- Purple team exercise results and findings.
- Simulation scenario coverage vs. playbook inventory.
- Identified gaps during exercises -- were they remediated?
- Time-to-execute measurements from simulations.

============================================================
PHASE 3: MTTR OPTIMIZATION
============================================================

Analyze and optimize mean time to respond across the incident lifecycle.

Step 3.1 -- Response Timeline Decomposition

Break down MTTR into component phases:

| Phase | Metric | Current | Target | Gap |
|-------|--------|---------|--------|-----|
| Detection | MTTD | | | |
| Triage | MTTT | | | |
| Investigation | MTTI | | | |
| Containment | MTTC | | | |
| Eradication | MTTE | | | |
| Recovery | MTTRec | | | |
| Total | MTTR | | | |

Step 3.2 -- Bottleneck Identification

Find the constraint in each phase:
- Detection: data source gaps, rule sensitivity, alert routing delays.
- Triage: analyst availability, context gathering time, tool switching.
- Investigation: forensic data availability, tool capability, analyst expertise.
- Containment: approval process delays, tool access, cross-team coordination.
- Eradication: scope uncertainty, persistence mechanism discovery.
- Recovery: backup availability, rebuild time, validation testing.

Step 3.3 -- Automation Opportunities

Identify MTTR reduction through automation:
- Auto-enrichment: IOC lookup, asset lookup, user context (saves 5-15 min per incident).
- Auto-containment: host isolation, account disable, IP block (saves 15-60 min).
- Auto-evidence collection: memory dump, disk image, log pull (saves 30-120 min).
- Automated reporting: timeline generation, stakeholder notification (saves 30-60 min).
- Orchestrated playbooks: end-to-end automated response for known scenarios.

Step 3.4 -- Communication Optimization

Reduce time lost to coordination:
- War room activation criteria and speed.
- Stakeholder notification automation.
- Status update cadence and templates.
- Handoff procedures between shifts.
- External communication pre-approvals (legal, PR).

============================================================
PHASE 4: EVIDENCE COLLECTION AND FORENSICS
============================================================

Evaluate evidence collection and forensic procedures.

Step 4.1 -- Evidence Collection Procedures

Assess forensic readiness:
- Volatile evidence collection order (RFC 3227 order of volatility):
  1. Registers, cache
  2. Memory (RAM)
  3. Network state (connections, routing tables)
  4. Running processes
  5. Disk (file system)
  6. Remote logging and monitoring data
  7. Physical evidence
- Collection tools validated and pre-deployed?
- Write-blockers and forensic imaging procedures documented?
- Cloud evidence collection (API logs, snapshots, metadata)?

Step 4.2 -- Chain of Custody

Evaluate evidence integrity practices:
- Chain of custody forms and tracking system.
- Evidence storage (physical and digital) security.
- Hash verification at collection and each transfer point.
- Evidence retention policy aligned with legal requirements.
- Attorney-client privilege considerations documented.

Step 4.3 -- Log Availability and Retention

Assess log readiness for investigations:
- Critical log sources and retention periods.
- Log integrity verification (tamper detection, immutable storage).
- Log centralization completeness (are there blind spots?).
- Historical log availability for APT investigations (90+ days).
- Cloud service log availability (CloudTrail, Azure Activity Log, GCP Audit).

Step 4.4 -- Forensic Capability Assessment

Evaluate forensic analysis capabilities:
- Memory forensics capability and tooling.
- Disk forensics capability (full disk, triage).
- Network forensics (packet capture, flow analysis).
- Malware analysis capability (static, dynamic, reverse engineering).
- Mobile device forensics (if applicable).
- Cloud forensics (VM snapshot analysis, container forensics).

============================================================
PHASE 5: ROOT CAUSE ANALYSIS AND POST-INCIDENT REVIEW
============================================================

Evaluate the learning loop from incidents.

Step 5.1 -- Root Cause Analysis Methodology

Assess RCA quality in past incidents:
- Structured methodology used? (5-Why, Ishikawa, fault tree, timeline analysis)
- Root cause specificity -- are causes actionable or generic?
- Contributing factors identified beyond primary root cause?
- Technical root cause vs. process/human factors root cause both addressed?
- Root cause validation -- evidence supporting the determination?

Step 5.2 -- Post-Incident Review Process

Evaluate PIR and lessons learned practices:
- PIR conducted for all significant incidents (not just major)?
- Blameless culture promoted in PIR sessions?
- Attendees include all relevant parties (not just IR team)?
- Action items assigned with owners and deadlines?
- Action item follow-through tracking and completion rate.

Step 5.3 -- Improvement Tracking

Assess whether incidents drive real improvement:
- Ratio of incidents to improvement actions implemented.
- Time from PIR finding to remediation implementation.
- Recurring findings across PIRs (same lessons not being learned).
- Detection improvements driven by past incidents.
- Playbook updates triggered by PIR findings.
- Architecture or process changes resulting from significant incidents.

Step 5.4 -- Metrics and Reporting

Evaluate IR program measurement:
- Executive-level metrics reported (incidents by type, MTTR, business impact).
- Operational metrics tracked (phase-by-phase timing, team performance).
- Benchmarking against industry peers or frameworks.
- Trend analysis on incident volume and severity.
- Cost-per-incident tracking.

============================================================
PHASE 6: IR MATURITY ASSESSMENT
============================================================

Score IR maturity against NIST or CMMI-based model:
- Level 1 (Initial): Ad-hoc, reactive.
- Level 2 (Managed): Documented plans, basic tooling.
- Level 3 (Defined): Playbooks tested, metrics tracked.
- Level 4 (Quantitatively Managed): MTTR optimized, automation deployed.
- Level 5 (Optimizing): Continuous improvement loop, predictive capabilities.

Produce a prioritized improvement plan ranked by MTTR impact and implementation effort:
- Quick wins (< 2 weeks): rule tuning, template creation, tool access.
- Short-term (2-8 weeks): playbook development, automation deployment.
- Medium-term (2-6 months): forensic capability build, training program.
- Long-term (6-12 months): architecture improvements, advanced automation.


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

## Incident Response Analysis

- Playbooks evaluated: [count]
- Incident types covered: [count]
- Historical incidents analyzed: [count]
- Improvement recommendations: [count]

### Summary Table
| Area | Status | Priority |
|------|--------|----------|
| Playbook Coverage | [Complete/Partial/Critical Gaps] | [P1/P2/P3] |
| MTTR Performance | [Meeting Targets/Improvable/Critical] | [P1/P2/P3] |
| Evidence Collection | [Forensic Ready/Partial/Ad-hoc] | [P1/P2/P3] |
| Root Cause Analysis | [Rigorous/Basic/Absent] | [P1/P2/P3] |
| Post-Incident Review | [Systematic/Inconsistent/None] | [P1/P2/P3] |
| IR Team Readiness | [Trained/Developing/Untested] | [P1/P2/P3] |

DO NOT:
- Execute containment actions or modify production systems -- this is an analysis skill.
- Access or display actual incident evidence, PII, or sensitive investigation details.
- Recommend eliminating manual review steps for critical decisions (containment, legal notification).
- Evaluate IR effectiveness based solely on incident count -- fewer incidents can mean better prevention or worse detection.
- Skip the post-incident review assessment even if MTTR metrics look acceptable.

NEXT STEPS:
- "Run `/threat-triage` to align playbooks with current threat actor TTPs."
- "Run `/alert-prioritization` to ensure alerts route to the right playbooks."
- "Run `/cyber-risk-modeling` to quantify business impact reduction from IR improvements."


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /incident-response — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
