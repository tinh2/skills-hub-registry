# Review

Architecture review, API review, database review, security review, and PR creation.

## Skills (5)

| Skill | Version | Description |
|-------|---------|-------------|
| [arch-review](arch-review/) | 7.0.0 | Architect-level story review and implementation validation with domain consistency analysis |
| [api-review](api-review/) | 1.0.0 | API design review against REST best practices -- naming, HTTP semantics, status codes, pagination, error format, versioning |
| [database-review](database-review/) | 1.0.0 | Database schema design review -- normalization, index coverage, constraints, naming, N+1 patterns, connection pooling |
| [security-review](security-review/) | 1.0.0 | Security-focused code review -- auth bypasses, injection vectors, data exposure, hardcoded secrets, IDOR vulnerabilities |
| [pr](pr/) | 1.0.0 | Creates a convention-compliant pull request -- extracts story number from branch, generates summary and test plan |

## Usage

- Review a story before implementation (design review): `/arch-review`
- Validate implementation against a story (code review): `/arch-review`
- Review API design for REST best practices: `/api-review`
- Review database schema for correctness and performance: `/database-review`
- Security-focused review for vulnerabilities: `/security-review`
- Create a convention-compliant PR: `/pr`
- Full story lifecycle (review + implement + PR): `/story` (combo skill)
