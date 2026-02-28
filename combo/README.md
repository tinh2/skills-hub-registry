# Combo

Multi-skill chains and compositions

## Skills

- [fix-and-ship](fix-and-ship/)
- [full-test](full-test/)
- [polish](polish/)
- [research](research/)
- [retro](retro/)
- [review-implement](review-implement/)
- [spec](spec/)
- [story](story/)

## About

Combo skills chain multiple skills together into automated pipelines. They run sequentially (or in parallel where noted) without user intervention.

| Combo | Chain | Use Case |
|-------|-------|----------|
| `/polish` | `/ux` ∥ `/scale-audit` → `/qa` → `/analyze` | Full quality pass |
| `/research` | `/compete` → `/new-features` | Market research |
| `/spec` | `/mvp` → `/backend-spec` | App analysis to stories |
| `/story` | `/arch-review` → `/si` → `/pr` | Full story lifecycle |
| `/review-implement` | `/arch-review` → `/si` | Review then implement |
| `/full-test` | `/e2e` → `/manual-test-plan` | Complete test coverage |
| `/retro` | `/recall` → `/new-features` | Retrospective + ideas |
| `/fix-and-ship` | `/hotfix` → `/preflight` | Emergency fix pipeline |
