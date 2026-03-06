# Meta

Skills about skills -- creation, testing, evolution, templates, cross-project sync, and registry maintenance.

## Skills (7)

| Skill | Version | Description |
|-------|---------|-------------|
| [bootstrap](bootstrap/) | 3.1.0 | Scaffolds a new project from a saved template -- creates CLAUDE.md, initial memory, and recommends first skill |
| [evolve](evolve/) | 1.1.0 | Self-improving skill that reads /recall and /metrics output, identifies which skills need patching, and applies fixes |
| [extract-template](extract-template/) | 1.0.0 | Extracts a reusable project template from a successful project -- captures pipeline, conventions, and pitfalls |
| [promote](promote/) | 1.1.0 | Cross-project pattern detection -- reads all project memories, finds recurring patterns, promotes to global conventions |
| [skill-creator](skill-creator/) | 1.0.0 | Creates new Claude Code skills following the marketplace SKILL.md format with proper frontmatter and quality scoring |
| [skill-test](skill-test/) | 1.0.0 | Validates a SKILL.md file against the marketplace quality rubric, checking schema, structure, and computing a score |
| [registry-sync](registry-sync/) | 1.0.0 | Scans and validates all SKILL.md files in the registry, checks category READMEs, detects duplicates, produces health report |

## Usage

**Self-improvement loop:**
```
/recall → /metrics → /evolve → /promote
```

- `/recall` analyzes git history for development patterns
- `/metrics` computes quality scores from the findings
- `/evolve` patches skills based on the data
- `/promote` detects cross-project patterns and promotes to global conventions

**Skill development:**
- Create a new skill: `/skill-creator`
- Validate a skill against the quality rubric: `/skill-test`
- Scan the full registry for issues: `/registry-sync`

**Project lifecycle:**
- Scaffold a new project from template: `/bootstrap`
- Extract a template from a mature project: `/extract-template`
