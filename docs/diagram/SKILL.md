---
name: diagram
description: "Generate Mermaid architecture diagrams from the codebase: C4 context/container, sequence diagrams for key flows, ER from schemas, module dependency graphs. Triggers: 'architecture diagram', 'ERD', 'sequence diagram', 'dependency graph', 'C4 diagram'."
version: "2.1.0"
category: docs
platforms:
  - CLAUDE_CODE
---

Generate accurate Mermaid diagrams of this codebase into `docs/diagrams/`. Diagram only what exists in the code; never invent services, tables or calls.

## Input

`$ARGUMENTS`:

- empty: every diagram type the project has data for
- `c4`: context + container only
- `sequence`: key flows only
- `er`: ER diagram only
- `deps` / `dependency`: module dependency graph only
- a flow description ("user login flow"): one sequence diagram for that flow

## Gather the facts

- **Architecture:** project type, languages/frameworks, databases, caches, queues, workers, and external services (auth, payments, email, storage) from config, env var names, SDK imports, `docker-compose.yml`/K8s manifests. For monoliths, find module/domain boundaries and trace imports.
- **Schema:** read whichever source exists (`schema.prisma`, Drizzle `schema.ts`, TypeORM/MikroORM entities, Django/SQLAlchemy models, `db/schema.rb`, Mongoose models, SQL migrations). Take tables, columns, keys, relationships with cardinality, and enums.
- **Flows:** authentication (login, signup, token refresh) if auth exists, the primary business flow, and any background-job flow. Trace each from entry point through middleware, service, data access and external calls to the response.

## Diagrams

- **C4 Context** (`C4Context`): people, the system, external systems, labeled `Rel`s. No internals.
- **C4 Container** (`C4Container`): apps, APIs, `ContainerDb`, `ContainerQueue`, workers, with protocols on relationships (HTTPS, SQL, AMQP). Mermaid's C4 support is still experimental and lays out poorly past ~10 nodes; for larger systems use a `flowchart` with subgraphs as the system boundary.
- **Sequence** (`sequenceDiagram`): one per key flow, with notes for important payloads and `alt` blocks for meaningful error paths.
- **ER** (`erDiagram`): every table with column types and PK/FK/UK markers, crow's-foot cardinality (`||--o{`, `}o--o{`).
- **Dependencies** (`flowchart TD`): entry points at the top, data stores at the bottom, externals at the sides, `classDef` colors per layer, circular dependencies called out.

Leave out credentials, internal hostnames and IPs. Skip types with no data (no ER without a database). Read existing files before overwriting them.

## Output files

Write `c4-context.md`, `c4-container.md`, `sequence-auth.md`, `sequence-<flow>.md`, `er-diagram.md` and `dependency-graph.md` as applicable. Each has a heading, a sentence or two of explanation, the Mermaid block, and notes on what was simplified. Add a `docs/diagrams/README.md` index linking them.

Check that every diagram parses: render with `npx -y @mermaid-js/mermaid-cli -i <file> -o /tmp/x.svg` when Node is available, otherwise review the syntax carefully. GitHub renders Mermaid natively, so use Mermaid rather than PlantUML.

## Report

```
## Diagrams Generated

### System Profile
- Type: monolith / microservices / monorepo
- Services: N | Tables: N | External systems: N

### Diagrams
| Diagram | File | Entities |
|---|---|---|

### Observations
- circular dependencies, isolated modules, relationships that couldn't be determined
```

Useful follow-ups: `/adr` to record the decisions the diagrams show, and `/onboarding` to put them in the onboarding guide.
