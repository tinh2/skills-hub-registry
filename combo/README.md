# Combo

Multi-skill chains and pipeline compositions -- automated sequences that run multiple skills without user intervention.

## Skills (14)

| Skill | Version | Chain | Description |
|-------|---------|-------|-------------|
| [polish](polish/) | 3.0.0 | /ux ∥ /scale-audit → /qa → /analyze | Full quality pass with parallel UX + scalability audit |
| [research](research/) | 1.0.0 | /compete → /new-features | Competitive gap analysis + feature ideation |
| [spec](spec/) | 1.0.0 | /mvp → /backend-spec | App analysis + story generation |
| [story](story/) | 1.0.0 | /arch-review → /story-implementer → /pr | Full story lifecycle from review to PR |
| [review-implement](review-implement/) | 1.0.0 | /arch-review → /story-implementer | Review architecture then implement |
| [full-test](full-test/) | 1.0.0 | /e2e → /manual-test-plan | Automated E2E tests + manual test plan |
| [retro](retro/) | 1.0.0 | /recall → /new-features | Dev retrospective + feature ideation |
| [fix-and-ship](fix-and-ship/) | 1.0.0 | /hotfix → /preflight | Emergency fix + deploy verification |
| [secure-ship](secure-ship/) | 1.0.0 | /owasp → /ship → /security-review → /pentest | Security-first build chain |
| [compliance-gate](compliance-gate/) | 1.0.0 | /secure → /gdpr → /dependency-scan → /pentest | Full compliance pass with unified report |
| [full-deploy](full-deploy/) | 1.0.0 | /docker → /github-actions → /monitoring → /preflight | Complete deploy pipeline |
| [design-to-code](design-to-code/) | 1.0.0 | /design-system → /responsive → /dark-mode → /ux | Full design implementation chain |
| [data-pipeline](data-pipeline/) | 1.0.0 | /api-scaffold → /integration-test → /load-test | Data-heavy app setup chain |
| [tech-debt-sprint](tech-debt-sprint/) | 1.0.0 | /tech-debt → /code-smell → /dead-code → /iterate-review | Debt reduction sprint |

## Usage

Combo skills chain multiple skills together into automated pipelines. They run sequentially (or in parallel where noted) without user intervention. Each phase passes its output as context to the next.

**Quality:**
- `/polish` -- Full quality pass with parallel UX + scalability audit, then QA and domain analysis
- `/full-test` -- Automated E2E tests with self-healing, then manual test plan for edge cases

**Build + Ship:**
- `/story` -- Full story lifecycle: architecture review, implementation, PR creation
- `/review-implement` -- Review architecture then implement
- `/fix-and-ship` -- Emergency bug fix then pre-deploy verification
- `/secure-ship` -- Security-first build: OWASP scan, build, security review, pentest

**Research + Planning:**
- `/research` -- Competitive gap analysis then feature ideation
- `/spec` -- MVP analysis from video/screenshots then story generation
- `/retro` -- Development retrospective then feature ideation

**Infrastructure:**
- `/full-deploy` -- Containerize, CI/CD, monitoring, pre-deploy checks
- `/compliance-gate` -- Security scan, GDPR, dependency audit, pentest

**Design:**
- `/design-to-code` -- Design system, responsive layout, dark mode, UX audit

**Data:**
- `/data-pipeline` -- API scaffold, integration tests, load tests

**Maintenance:**
- `/tech-debt-sprint` -- Debt inventory, code smell fixes, dead code removal, review pass
