# Review

Architecture review, API review, database review, security review, PR creation, executive-level strategic reviews (CTO, CFO, CPO), and industry-specific compliance reviews.

## Skills (15)

### Core Reviews

| Skill | Version | Description |
|-------|---------|-------------|
| [arch-review](arch-review/) | 7.0.0 | Architect-level story review and implementation validation with domain consistency analysis |
| [api-review](api-review/) | 1.0.0 | API design review against REST best practices -- naming, HTTP semantics, status codes, pagination, error format, versioning |
| [database-review](database-review/) | 1.0.0 | Database schema design review -- normalization, index coverage, constraints, naming, N+1 patterns, connection pooling |
| [security-review](security-review/) | 1.0.0 | Security-focused code review -- auth bypasses, injection vectors, data exposure, hardcoded secrets, IDOR vulnerabilities |
| [pr](pr/) | 1.0.0 | Creates a convention-compliant pull request -- extracts story number from branch, generates summary and test plan |

### Executive Reviews

| Skill | Version | Description |
|-------|---------|-------------|
| [cto-review](cto-review/) | 1.0.0 | CTO-perspective technical strategy review -- architecture decisions, scaling readiness, engineering velocity, technical debt ratio, security posture |
| [cfo-review](cfo-review/) | 1.0.0 | CFO-perspective financial impact review -- infrastructure costs, pricing model alignment, build-vs-buy economics, technical debt as financial liability |
| [cpo-review](cpo-review/) | 1.0.0 | CPO-perspective product strategy review -- feature completeness, user journey gaps, retention architecture, growth levers, competitive moat |

### Industry Compliance Reviews

| Skill | Version | Description |
|-------|---------|-------------|
| [healthcare-ops](healthcare-ops/) | 1.0.0 | Hospital operations review -- scheduling, workflows, integrations, patient flow, reporting, and staff management |
| [financial-compliance](financial-compliance/) | 1.0.0 | Financial software review against KYC/AML, BSA, Reg E, SOX, GLBA, and state money transmitter regulations |
| [procurement-review](procurement-review/) | 1.0.0 | Procurement software review -- sourcing workflows, PO management, vendor scorecards, spend analytics |
| [permit-compliance](permit-compliance/) | 1.0.0 | Construction software review for permit tracking, building code compliance, environmental regulations, and inspections |
| [manufacturing-compliance](manufacturing-compliance/) | 1.0.0 | Manufacturing regulatory review -- ISO 9001/13485/14001, FDA 21 CFR Part 11, GMP, OSHA, lot/serial traceability |
| [regulatory-compliance](regulatory-compliance/) | 1.0.0 | Cross-industry regulatory review -- audit trails, data retention, RBAC/ABAC, change management, breach notification |
| [energy-compliance](energy-compliance/) | 1.0.0 | Energy sector compliance review -- NERC CIP, FERC reporting, EPA emissions, renewable portfolio standards, pipeline safety |

## Usage

- Review a story before implementation (design review): `/arch-review`
- Validate implementation against a story (code review): `/arch-review`
- Review API design for REST best practices: `/api-review`
- Review database schema for correctness and performance: `/database-review`
- Security-focused review for vulnerabilities: `/security-review`
- Create a convention-compliant PR: `/pr`
- CTO-level technical strategy review: `/cto-review`
- CFO-level financial impact review: `/cfo-review`
- CPO-level product strategy review: `/cpo-review`
- Healthcare operations review: `/healthcare-ops`
- Financial regulatory compliance: `/financial-compliance`
- Manufacturing regulatory compliance: `/manufacturing-compliance`
- Energy sector compliance: `/energy-compliance`
- Cross-industry regulatory review: `/regulatory-compliance`
- Full executive review chain (combo): `/cto-review → /cfo-review → /cpo-review`
- Investor due diligence pipeline (combo): `/investor-ready`
