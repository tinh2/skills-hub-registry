# Security

Security scanning, penetration testing, compliance auditing, encryption, vulnerability remediation, and industry-specific security standards (HIPAA, PCI DSS).

## Main Skill

**[secure](secure/)** -- Comprehensive security posture scan covering dependencies, code patterns, config, auth, and data handling with risk scoring. Routes to sub-skills for detailed analysis.

## Skills (11)

| Skill | Version | Description |
|-------|---------|-------------|
| [secure](secure/) | 1.0.0 | Main orchestrator. Comprehensive security posture scan with risk scoring across dependencies, code, config, auth, and data |
| [owasp](owasp/) | 1.0.0 | Audit codebase against the OWASP 2021 Top 10 web application security risks with severity-rated findings |
| [pentest](pentest/) | 1.0.0 | Static-analysis penetration testing -- find exploitable vulnerabilities with proof-of-concept and remediation guidance |
| [gdpr](gdpr/) | 1.0.0 | Scan codebase for GDPR and CCPA compliance gaps -- PII handling, consent, data rights, and third-party sharing |
| [soc2](soc2/) | 1.0.0 | Evaluate codebase against SOC2 Trust Service Criteria -- security, availability, integrity, confidentiality, privacy |
| [encryption](encryption/) | 1.0.0 | Audit and implement encryption -- data at rest, in transit, key management, password hashing, and token security |
| [dependency-scan](dependency-scan/) | 1.0.0 | Auto-detect package manager, scan for vulnerable dependencies, auto-fix where possible, and generate SBOM |
| [check-vanta](check-vanta/) | 2.0.0 | Fetches Vanta vulnerabilities due for remediation, creates a Jira story, then fixes, commits, pushes, and opens PRs |
| [hipaa](hipaa/) | 1.0.0 | Deep HIPAA Security Rule audit -- administrative, physical, and technical safeguards with code-level CFR mappings |
| [pci-dss](pci-dss/) | 1.0.0 | PCI DSS v4.0 audit -- network security, data protection, encryption, access controls, logging, and vulnerability management |
| [benefits-fraud](benefits-fraud/) | 1.0.0 | Benefits fraud detection -- identity verification, duplicate detection, anomaly detection, overpayment recovery |

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
- Public services audit (combo): `/public-services-audit` chains benefits-processing, benefits-fraud, government-compliance, security-review
