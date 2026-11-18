# Security

Security scanning, penetration testing, compliance auditing, encryption, vulnerability remediation, and industry-specific security standards (HIPAA, PCI DSS).

## Main Skill

**[secure](secure/)** -- Comprehensive security posture scan covering dependencies, code patterns, config, auth, and data handling with risk scoring. Routes to sub-skills for detailed analysis.

## Skills (12)

| Skill | Version | Description |
|-------|---------|-------------|
| [secure](secure/) | 1.0.0 | Main orchestrator. Comprehensive security posture scan with risk scoring across dependencies, code, config, auth, and data |
| [owasp](owasp/) | 1.0.0 | Audit codebase against the OWASP 2021 Top 10 web application security risks with severity-rated findings |
| [pentest](pentest/) | 1.0.0 | Static-analysis penetration testing -- find exploitable vulnerabilities with proof-of-concept and remediation guidance |
| [gdpr](gdpr/) | 1.0.0 | Scan codebase for GDPR and CCPA compliance gaps -- PII handling, consent, data rights, and third-party sharing |
| [soc2](soc2/) | 1.0.0 | Evaluate codebase against SOC2 Trust Service Criteria -- security, availability, integrity, confidentiality, privacy |
| [encryption](encryption/) | 1.0.0 | Audit and implement encryption -- data at rest, in transit, key management, password hashing, and token security |
| [dependency-scan](dependency-scan/) | 1.0.0 | Auto-detect package manager, scan for vulnerable dependencies, auto-fix where possible, and generate SBOM |
| [check-vanta](check-vanta/) | 2.1.0 | Fetches Vanta vulnerabilities due for remediation, creates a Jira story, then fixes, commits, pushes, and opens PRs |
| [hipaa](hipaa/) | 1.0.0 | Deep HIPAA Security Rule audit -- administrative, physical, and technical safeguards with code-level CFR mappings |
| [pci-dss](pci-dss/) | 1.0.0 | PCI DSS v4.0 audit -- network security, data protection, encryption, access controls, logging, and vulnerability management |
| [benefits-fraud](benefits-fraud/) | 1.0.0 | Benefits fraud detection -- identity verification, duplicate detection, anomaly detection, overpayment recovery |
| [game-security](game-security/) | 1.0.0 | Reviews game security including client-side authority vulnerabilities, memory manipulation, packet tampering, speed hacking, save tampering, API abuse, DDoS resilience, and anti-cheat architecture |

## Usage

- Full security posture scan: `/secure`
- OWASP Top 10 audit: `/owasp`
- Penetration testing (static analysis): `/pentest`
- GDPR/CCPA compliance check: `/gdpr`
- SOC2 compliance evaluation: `/soc2`
- Encryption audit and implementation: `/encryption`
- Dependency vulnerability scan with SBOM: `/dependency-scan`
- Vanta vulnerability remediation pipeline: `/check-vanta`
- HIPAA Security Rule audit for healthcare: `/hipaa`
- PCI DSS v4.0 audit for payment processing: `/pci-dss`
- Full compliance pass (combo): `/compliance-gate` chains secure, GDPR, dependency-scan, and pentest
- Security-first build (combo): `/secure-ship` chains OWASP, ship, security-review, and pentest
- Healthcare audit (combo): `/healthcare-audit` chains HIPAA, clinical-data-review, healthcare-compliance, security-review
- Fintech launch (combo): `/fintech-launch` chains PCI DSS, fintech-api, fraud-detection, credit-risk, preflight
- Benefits fraud detection for government services: `/benefits-fraud`
- Game security review (anti-cheat, packet tampering, exploits): `/game-security`
- Public services audit (combo): `/public-services-audit` chains benefits-processing, benefits-fraud, government-compliance, security-review

<!-- BEGIN GENERATED: skills-hub-index (scripts/gen-index.mjs, do not edit by hand) -->
## All Security skills on skills-hub.ai

Each skill page on skills-hub.ai shows ratings and reviews, install counts, a one-command install, and related skills. 14 of 14 skills in this folder have a page. You can also [browse the Security category on skills-hub.ai](https://skills-hub.ai/browse?category=security), which includes skills from other publishers.

| Skill | Description | Page |
|-------|-------------|------|
| [agent-authorization](agent-authorization/) | Audits and implements authorization controls for production AI agent systems — policy definition, tool-call enforcement, immutable audit... | [View on skills-hub](https://skills-hub.ai/skills/agent-authorization) |
| [benefits-fraud](benefits-fraud/) | Audit government benefits and entitlement systems for fraud prevention, detection, and recovery capabilities. | [View on skills-hub](https://skills-hub.ai/skills/benefits-fraud) |
| [check-vanta](check-vanta/) | Fetches dependency vulnerabilities from Vanta, Snyk, Dependabot, or GitHub Security Advisories, creates a tracking issue in... | [View on skills-hub](https://skills-hub.ai/skills/check-vanta) |
| [cursor-agent-safety](cursor-agent-safety/) | Audits and hardens Cursor agent run mode settings for Cursor 3.6+. | [View on skills-hub](https://skills-hub.ai/skills/cursor-agent-safety) |
| [dependency-scan](dependency-scan/) | Scan project dependencies for known vulnerabilities (CVEs), auto-fix safe patches, and generate SBOM. | [View on skills-hub](https://skills-hub.ai/skills/dependency-scan) |
| [encryption](encryption/) | Audit and harden encryption across the full stack. | [View on skills-hub](https://skills-hub.ai/skills/encryption) |
| [game-security](game-security/) | Game-specific security review covering cheat prevention, exploit surfaces, and server authority. | [View on skills-hub](https://skills-hub.ai/skills/game-security) |
| [gdpr](gdpr/) | GDPR and CCPA/CPRA privacy compliance audit for codebases. | [View on skills-hub](https://skills-hub.ai/skills/gdpr) |
| [hipaa](hipaa/) | Deep HIPAA Security Rule technical audit mapping code-level findings to 45 CFR sections. | [View on skills-hub](https://skills-hub.ai/skills/hipaa) |
| [owasp](owasp/) | Systematic audit against the OWASP 2021 Top 10 web application security risks with severity-rated, file-level findings. | [View on skills-hub](https://skills-hub.ai/skills/owasp) |
| [pci-dss](pci-dss/) | PCI DSS v4.0 compliance audit for payment-handling codebases. | [View on skills-hub](https://skills-hub.ai/skills/pci-dss) |
| [pentest](pentest/) | Static-analysis penetration test that hunts for exploitable vulnerabilities with proof-of-concept payloads and fix code. | [View on skills-hub](https://skills-hub.ai/skills/pentest) |
| [secure](secure/) | Full-stack security posture assessment with 0-100 risk scoring. | [View on skills-hub](https://skills-hub.ai/skills/secure) |
| [soc2](soc2/) | SOC 2 Type II readiness assessment against all five Trust Service Criteria. | [View on skills-hub](https://skills-hub.ai/skills/soc2) |
<!-- END GENERATED: skills-hub-index -->
