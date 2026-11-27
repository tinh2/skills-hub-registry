---
name: database-review
description: "Review schema, query patterns and data access code for correctness and performance: normalization, indexes, constraints, types, N+1s, pooling, transactions. Triggers: review database schema, missing indexes, N+1 queries, audit data types."
version: "2.1.0"
category: review
platforms:
  - CLAUDE_CODE
---

Audit the database layer (schema plus the code that queries it) and report findings with file locations and concrete fixes. This is a review: don't change code.

**Input:** `$ARGUMENTS` optionally narrows the scope (a table, a module, "new migrations"); otherwise review everything.

## Discover

Identify the database (Postgres, MySQL, SQLite, MongoDB, Firestore, DynamoDB...), the ORM or query builder, and the migration tool. Reconstruct the current schema from its source of truth: `schema.prisma`, the full migration history, `models.py`, `db/schema.rb`, Mongoose schemas, or (Firestore/Mongo) the code plus security rules. Then find every place queries execute, because a schema review without query context is incomplete.

## What to check

- **Normalization.** Duplicated data that can drift (`order.customer_name` vs `customer.name`), JSON columns or arrays holding structured data you query (should be tables), 3NF violations. In the other direction: lookup tables that should be enums, unexplained 1:1 splits, tables always joined and never read alone. Respect intentional denormalization where the read pattern justifies it.
- **Indexes.** For each query, map WHERE / JOIN / ORDER BY / GROUP BY columns to existing indexes and weight by how hot the path is. Composite column order vs actual predicates, covering indexes for hot queries, partial indexes for skewed columns, and indexes no code uses (they slow writes, but ad-hoc/BI use is invisible to you, so say so). Skip index advice for tables under ~1,000 rows.
- **Constraints.** Missing NOT NULL (email, timestamps, status, FKs), missing foreign keys on `*_id` columns and whether each ON DELETE is intentional, missing unique (email, slug, external IDs, compound keys like user_id+date), missing CHECKs for ranges and enums, missing defaults (`now()`, initial status, booleans false). Document stores have no FKs; don't flag that.
- **Types.** Float for money (use numeric or integer cents), INT primary keys that may pass 2B rows, string enums without enforcement, timestamps without time zone or not UTC, 0/1 integers or nullable booleans, mixed UUID/serial ID strategy, JSON instead of JSONB, JSON queried by nested keys.
- **Query patterns.** N+1s (queries in loops, missing `include` / `select_related` / `includes`), rated by path heat. Pool configured and sized for expected concurrency, connections not leaked. Multi-step writes wrapped in transactions; transactions that hold locks across network calls; isolation level. `SELECT *` on wide tables, unbounded list queries, `LIKE '%x%'` that should be full-text search.
- **Migrations (brief; `/migration-verify` goes deep).** All changes tracked, reversible, no unbacked destructive steps, no long locks on large tables.

Before reporting, check every finding points at a file or table, has a justified severity and a specific fix.

## Output

```
## Database Review Report
Database: <db> | ORM: <orm> | Tables/collections: <n>
Schema health score: <0-100>

### Findings summary
| Category | Critical | High | Medium | Low |
(Normalization, Indexes, Constraints, Data types, Query patterns, Connection config)

### Critical and high findings
1. **DB-001: <title>** (Critical|High)
   - Table: `<table>`  Location: `<file:line>`
   - Issue / Impact (data loss, slow queries, inconsistency) / Fix (exact schema or code change)

### Index coverage
| Table | Queries found | Indexed | Unindexed | Missing indexes |

### N+1 queries
| Location | Parent query | Child query | Est. queries per request | Fix |

### Constraint coverage
| Table | NOT NULL | FKs | Unique | Check | Defaults |

### Recommendations (by impact, with effort S/M/L, weighing migration cost)
```

Suggested follow-ups: `/migration-verify`, `/perf`, `/security-review`.

## Telemetry

If a memory directory for this project exists under `~/.claude/projects/`, append to its `skill-telemetry.md`:

```
### /database-review — YYYY-MM-DD
- Outcome: SUCCESS | PARTIAL | FAILED
- Bottleneck: <phase that struggled, or none>
- Suggestion: <one-line improvement for /evolve, or none>
```
